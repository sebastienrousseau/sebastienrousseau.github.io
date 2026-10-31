# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""PDF render service for sebastienrousseau.com.

Single endpoint: ``GET /render?slug=<article-slug>`` — fetches the live
article HTML from the public site, runs it through WeasyPrint with the
site's existing ``@media print`` stylesheet honoured, and returns a
PDF/A-quality download.

Designed to sit behind the lang-router Cloudflare Worker at
``/api/pdf/<slug>.pdf``; the Worker proxies, the Edge caches for 24 h
``immutable``, repeat reads never hit this service.

Health endpoint: ``GET /healthz`` for Fly.io machine probes.

Security:
- Slug must match ``^[a-z0-9][a-z0-9\\-]{0,127}$`` — every dated article
  slug fits; everything else is rejected with 400. Stops directory-
  traversal + reflected-fetch shenanigans.
- ``base_url`` for relative-link resolution is hard-pinned to the
  canonical origin — the Worker can't be tricked into fetching an
  attacker-controlled HTML.
- ``presentational_hints=True`` lets WeasyPrint pick up font/color
  attributes the site's stylesheet may rely on; nothing executes JS.
"""

from __future__ import annotations

import hmac
import logging
import os
import re
from functools import lru_cache
from io import BytesIO
from urllib.parse import urlparse

import requests
from flask import Flask, Response, abort, jsonify, request
from weasyprint import HTML
from werkzeug.exceptions import BadGateway, BadRequest, Forbidden, NotFound

LOG = logging.getLogger("pdf-render")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

ORIGIN = os.environ.get("ORIGIN_BASE", "https://sebastienrousseau.com").rstrip("/")
SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9\-]{0,127}$")
FETCH_TIMEOUT = float(os.environ.get("FETCH_TIMEOUT", "10"))
RENDER_TIMEOUT = float(os.environ.get("RENDER_TIMEOUT", "20"))
MAX_ASSET_BYTES = int(os.environ.get("MAX_ASSET_BYTES", str(10 * 1024 * 1024)))
ORIGIN_VERIFY_TOKEN = os.environ.get("PDF_ORIGIN_TOKEN", "")
ALLOWED_ASSET_HOSTS = frozenset(
    {
        "sebastienrousseau.com",
        "cloudcdn.pro",
        urlparse(ORIGIN).hostname or "sebastienrousseau.com",
    }
)
IMMUTABLE_PATH_PREFIXES = ("/fonts/", "/_csp/")

app = Flask(__name__)


@app.get("/healthz")
def healthz() -> Response:
    """Liveness probe used by Fly.io. Returns 200 with build metadata."""
    return jsonify(
        {
            "status": "ok",
            "service": "pdf-render",
            "origin": ORIGIN,
        }
    )


def _validate_subresource_url(url: str) -> tuple[str, str]:
    """Ensure WeasyPrint subresource fetches only target trusted HTTPS hosts."""
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()
    if parsed.scheme != "https" or host not in ALLOWED_ASSET_HOSTS:
        raise ValueError(f"blocked subresource URL: {url}")
    return host, parsed.path or "/"


def _fetch_bounded_url(url: str) -> dict[str, object]:
    """Fetch an allowed subresource with a strict timeout and byte ceiling."""
    _validate_subresource_url(url)
    res = requests.get(
        url,
        timeout=FETCH_TIMEOUT,
        stream=True,
        headers={"User-Agent": "pdf-render/1 (+https://sebastienrousseau.com/contact/)"},
    )
    try:
        res.raise_for_status()
        chunks: list[bytes] = []
        total = 0
        for chunk in res.iter_content(chunk_size=65536):
            if not chunk:
                continue
            total += len(chunk)
            if total > MAX_ASSET_BYTES:
                raise ValueError(f"subresource exceeds {MAX_ASSET_BYTES} bytes: {url}")
            chunks.append(chunk)
        content_type = res.headers.get("Content-Type", "application/octet-stream")
        mime_type = content_type.split(";", 1)[0].strip() or "application/octet-stream"
        return {"string": b"".join(chunks), "mime_type": mime_type}
    finally:
        res.close()


@lru_cache(maxsize=64)
def _fetch_immutable_asset(url: str) -> dict[str, object]:
    """Cache immutable self-hosted fonts and fingerprinted CSS across renders."""
    return _fetch_bounded_url(url)


def safe_url_fetcher(
    url: str,
    timeout: int = 10,
    ssl_context: object = None,
) -> dict[str, object]:
    """WeasyPrint url_fetcher enforcing host allowlist, byte limits, and font caching."""
    host, path = _validate_subresource_url(url)
    origin_host = (urlparse(ORIGIN).hostname or "sebastienrousseau.com").lower()
    if host == origin_host and path.startswith(IMMUTABLE_PATH_PREFIXES):
        return _fetch_immutable_asset(url)
    return _fetch_bounded_url(url)


def _verify_origin_token() -> None:
    """Enforce optional shared origin token when PDF_ORIGIN_TOKEN is configured."""
    if not ORIGIN_VERIFY_TOKEN:
        return
    provided = request.headers.get("X-Origin-Verify", "")
    if not hmac.compare_digest(provided, ORIGIN_VERIFY_TOKEN):
        raise Forbidden("invalid origin token")


def _fetch_article_html(slug: str) -> str:
    """Fetch the canonical EN article HTML from the public site. Errors
    bubble up as 502 to the Worker so the cache-bust isn't promoted."""
    # Defense-in-depth: re-validate the slug at the network sink. The slug is
    # the only user-controlled input that flows into the outbound URL, so an
    # explicit charset guard here means the request host can never be
    # attacker-influenced (SSRF barrier) and the logged URL is provably free
    # of control characters (log-injection barrier). `raise` (not a bare
    # `abort`) makes the guard unambiguously terminating to static analysis.
    if not SLUG_RE.fullmatch(slug):
        raise BadRequest("invalid slug")
    url = f"{ORIGIN}/{slug}/"
    LOG.info("fetch %s", url)
    try:
        res = requests.get(
            url,
            timeout=FETCH_TIMEOUT,
            headers={"User-Agent": "pdf-render/1 (+https://sebastienrousseau.com/contact/)"},
        )
    except requests.RequestException as exc:
        LOG.warning("fetch error: %s", exc)
        raise BadGateway(f"upstream fetch error: {exc}") from exc
    # `res` is guaranteed bound here: the only way out of the try/except
    # without it is the `raise` above.
    if res.status_code == 404:
        raise NotFound("article not found")
    if not res.ok:
        raise BadGateway(f"upstream {res.status_code}")
    return res.text


def _render_pdf(html: str, slug: str) -> bytes:
    """Render to PDF in-memory. WeasyPrint reads relative URLs using
    base_url, so /main.css and /fonts/*.woff2 resolve against the
    canonical origin (never the Fly machine) via safe_url_fetcher."""
    buf = BytesIO()
    HTML(string=html, base_url=ORIGIN, url_fetcher=safe_url_fetcher).write_pdf(
        target=buf,
        presentational_hints=True,
    )
    pdf = buf.getvalue()
    LOG.info("render slug=%s bytes=%d", slug, len(pdf))
    return pdf


@app.get("/render")
def render() -> Response:
    """Render one article to PDF.

    Query string:
      slug - dated article slug, e.g.
             ``2026-06-08-banking-resilience-index-...-2026``.

    Cache-Control on the response is immutable for 24 h - the Worker
    re-emits it so the Cloudflare Edge absorbs every repeat hit and
    the Fly machine sees one request per article per day at most.
    """
    _verify_origin_token()
    slug = (request.args.get("slug") or "").strip()
    if not SLUG_RE.fullmatch(slug):
        abort(400, description="invalid slug")
    html = _fetch_article_html(slug)
    pdf = _render_pdf(html, slug)
    return Response(
        pdf,
        mimetype="application/pdf",
        headers={
            "Content-Disposition": f'inline; filename="{slug}.pdf"',
            "Cache-Control": "public, max-age=86400, immutable",
        },
    )


if __name__ == "__main__":  # pragma: no cover
    host = os.environ.get("HOST", "127.0.0.1")
    app.run(host=host, port=int(os.environ.get("PORT", "8080")))
