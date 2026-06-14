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

import logging
import os
import re
from io import BytesIO

import requests
from flask import Flask, Response, abort, jsonify, request
from weasyprint import HTML

LOG = logging.getLogger("pdf-render")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

ORIGIN = os.environ.get("ORIGIN_BASE", "https://sebastienrousseau.com").rstrip("/")
SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9\-]{0,127}$")
FETCH_TIMEOUT = float(os.environ.get("FETCH_TIMEOUT", "10"))
RENDER_TIMEOUT = float(os.environ.get("RENDER_TIMEOUT", "20"))

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


def _fetch_article_html(slug: str) -> str:
    """Fetch the canonical EN article HTML from the public site. Errors
    bubble up as 502 to the Worker so the cache-bust isn't promoted."""
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
        abort(502, description=f"upstream fetch error: {exc}")
    if res.status_code == 404:
        abort(404, description="article not found")
    if not res.ok:
        abort(502, description=f"upstream {res.status_code}")
    return res.text


def _render_pdf(html: str, slug: str) -> bytes:
    """Render to PDF in-memory. WeasyPrint reads relative URLs using
    base_url, so /main.css and /fonts/*.woff2 resolve against the
    canonical origin (never the Fly machine)."""
    buf = BytesIO()
    HTML(string=html, base_url=ORIGIN).write_pdf(target=buf, presentational_hints=True)
    pdf = buf.getvalue()
    LOG.info("render slug=%s bytes=%d", slug, len(pdf))
    return pdf


@app.get("/render")
def render() -> Response:
    """Render one article to PDF.

    Query string:
      slug — dated article slug, e.g.
             ``2026-06-08-banking-resilience-index-...-2026``.

    Cache-Control on the response is immutable for 24 h — the Worker
    re-emits it so the Cloudflare Edge absorbs every repeat hit and
    the Fly machine sees one request per article per day at most.
    """
    slug = (request.args.get("slug") or "").strip()
    if not slug or not SLUG_RE.match(slug):
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
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8080")))
