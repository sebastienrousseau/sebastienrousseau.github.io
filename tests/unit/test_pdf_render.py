# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Unit coverage for fly/pdf-render/app.py (SSRF guard, asset caching, and endpoints)."""

from __future__ import annotations

import importlib.util
import sys
import types
from pathlib import Path
from typing import Any

import pytest

APP_PATH = Path(__file__).resolve().parents[2] / "fly" / "pdf-render" / "app.py"


class _HTTPException(Exception):
    code = 500


class _BadRequest(_HTTPException):
    code = 400


class _Forbidden(_HTTPException):
    code = 403


class _NotFound(_HTTPException):
    code = 404


class _BadGateway(_HTTPException):
    code = 502


class _RequestException(Exception):
    pass


class _FakeResponse:
    def __init__(
        self,
        body: Any = b"",
        *,
        mimetype: str = "text/plain",
        headers: dict[str, str] | None = None,
        status_code: int = 200,
    ) -> None:
        self.body = body
        self.mimetype = mimetype
        self.headers = headers or {}
        self.status_code = status_code


def _load_pdf_app(monkeypatch: pytest.MonkeyPatch) -> Any:
    """Load fly/pdf-render/app.py with hermetic stubs for container-only deps."""
    fake_flask = types.ModuleType("flask")
    fake_request = types.SimpleNamespace(args={}, headers={})

    class _FakeFlask:
        def __init__(self, name: str) -> None:
            self.name = name

        def get(self, _route: str):
            def _decorator(fn: Any) -> Any:
                return fn

            return _decorator

    def _abort(code: int, description: str = "") -> None:
        raise _BadRequest(f"{code}: {description}")

    fake_flask.Flask = _FakeFlask  # type: ignore[attr-defined]
    fake_flask.Response = _FakeResponse  # type: ignore[attr-defined]
    fake_flask.abort = _abort  # type: ignore[attr-defined]
    fake_flask.jsonify = lambda payload: _FakeResponse(payload, mimetype="application/json")  # type: ignore[attr-defined]
    fake_flask.request = fake_request  # type: ignore[attr-defined]

    fake_weasy = types.ModuleType("weasyprint")
    recorded_html: list[dict[str, Any]] = []

    class _FakeHTML:
        def __init__(self, *, string: str, base_url: str, url_fetcher: Any = None) -> None:
            recorded_html.append(
                {"string": string, "base_url": base_url, "url_fetcher": url_fetcher}
            )

        def write_pdf(self, *, target: Any, presentational_hints: bool = False) -> None:
            assert presentational_hints is True
            target.write(b"%PDF-1.7-test")

    fake_weasy.HTML = _FakeHTML  # type: ignore[attr-defined]
    fake_weasy.recorded = recorded_html  # type: ignore[attr-defined]

    fake_werkzeug = types.ModuleType("werkzeug")
    fake_werkzeug_exc = types.ModuleType("werkzeug.exceptions")
    fake_werkzeug_exc.BadGateway = _BadGateway  # type: ignore[attr-defined]
    fake_werkzeug_exc.BadRequest = _BadRequest  # type: ignore[attr-defined]
    fake_werkzeug_exc.Forbidden = _Forbidden  # type: ignore[attr-defined]
    fake_werkzeug_exc.NotFound = _NotFound  # type: ignore[attr-defined]

    fake_requests = types.ModuleType("requests")
    fake_requests.RequestException = _RequestException  # type: ignore[attr-defined]
    fake_requests.get = lambda *_a, **_kw: None  # type: ignore[attr-defined]

    monkeypatch.setitem(sys.modules, "flask", fake_flask)
    monkeypatch.setitem(sys.modules, "weasyprint", fake_weasy)
    monkeypatch.setitem(sys.modules, "werkzeug", fake_werkzeug)
    monkeypatch.setitem(sys.modules, "werkzeug.exceptions", fake_werkzeug_exc)
    monkeypatch.setitem(sys.modules, "requests", fake_requests)

    spec = importlib.util.spec_from_file_location("fly_pdf_render_app", APP_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_validate_subresource_url_allows_canonical_and_cdn(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    app_mod = _load_pdf_app(monkeypatch)
    host, path = app_mod._validate_subresource_url(
        "https://sebastienrousseau.com/fonts/inter.woff2"
    )
    assert host == "sebastienrousseau.com"
    assert path == "/fonts/inter.woff2"

    host2, path2 = app_mod._validate_subresource_url("https://cloudcdn.pro/stocks/images/hero.webp")
    assert host2 == "cloudcdn.pro"
    assert path2 == "/stocks/images/hero.webp"


def test_validate_subresource_url_blocks_ssrf_targets(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    app_mod = _load_pdf_app(monkeypatch)
    for bad in (
        "http://sebastienrousseau.com/fonts/inter.woff2",
        "http://169.254.169.254/latest/meta-data/",
        "https://evil.example.com/payload.css",
        "file:///etc/passwd",
    ):
        with pytest.raises(ValueError, match="blocked subresource URL"):
            app_mod._validate_subresource_url(bad)


def test_safe_url_fetcher_caches_immutable_assets_and_enforces_size_cap(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    app_mod = _load_pdf_app(monkeypatch)
    calls: list[str] = []

    class _StreamResp:
        def __init__(self, chunks: list[bytes], content_type: str = "font/woff2") -> None:
            self._chunks = chunks
            self.headers = {"Content-Type": f"{content_type}; charset=binary"}
            self.closed = False

        def raise_for_status(self) -> None:
            return None

        def iter_content(self, chunk_size: int = 65536):
            assert chunk_size == 65536
            yield from self._chunks

        def close(self) -> None:
            self.closed = True

    def _fake_get(url: str, **_kwargs: Any) -> _StreamResp:
        calls.append(url)
        return _StreamResp([b"woff2-", b"", b"bytes"])

    monkeypatch.setattr(app_mod.requests, "get", _fake_get)
    font_url = "https://sebastienrousseau.com/fonts/inter-latin.woff2"
    first = app_mod.safe_url_fetcher(font_url)
    second = app_mod.safe_url_fetcher(font_url)
    assert first == {"string": b"woff2-bytes", "mime_type": "font/woff2"}
    assert second == first
    assert calls == [font_url], "second fetch of /fonts/ asset must hit LRU cache"

    # Non-immutable CDN image is fetched directly and enforces MAX_ASSET_BYTES
    monkeypatch.setattr(app_mod, "MAX_ASSET_BYTES", 4)
    with pytest.raises(ValueError, match="subresource exceeds 4 bytes"):
        app_mod.safe_url_fetcher("https://cloudcdn.pro/stocks/images/large.webp")


def test_healthz_and_render_pipeline(monkeypatch: pytest.MonkeyPatch) -> None:
    app_mod = _load_pdf_app(monkeypatch)
    health = app_mod.healthz()
    assert health.body["status"] == "ok"

    class _UpstreamResp:
        status_code = 200
        ok = True
        text = "<!doctype html><html><body><h1>Article</h1></body></html>"

    monkeypatch.setattr(app_mod.requests, "get", lambda *_a, **_kw: _UpstreamResp())
    app_mod.request.args = {"slug": "2026-06-08-banking-resilience-index"}
    resp = app_mod.render()
    assert resp.mimetype == "application/pdf"
    assert resp.body == b"%PDF-1.7-test"
    assert resp.headers["Cache-Control"] == "public, max-age=86400, immutable"


def test_origin_token_and_upstream_error_branches(monkeypatch: pytest.MonkeyPatch) -> None:
    app_mod = _load_pdf_app(monkeypatch)
    monkeypatch.setattr(app_mod, "ORIGIN_VERIFY_TOKEN", "secret-token")
    app_mod.request.headers = {"X-Origin-Verify": "wrong"}
    with pytest.raises(_Forbidden):
        app_mod._verify_origin_token()

    app_mod.request.headers = {"X-Origin-Verify": "secret-token"}
    app_mod._verify_origin_token()

    with pytest.raises(_BadRequest):
        app_mod._fetch_article_html("../traversal")

    app_mod.request.args = {"slug": "UPPERCASE"}
    with pytest.raises(_BadRequest):
        app_mod.render()

    class _Resp404:
        status_code = 404
        ok = False
        text = ""

    monkeypatch.setattr(app_mod.requests, "get", lambda *_a, **_kw: _Resp404())
    with pytest.raises(_NotFound):
        app_mod._fetch_article_html("2026-06-08-missing")

    class _Resp500:
        status_code = 500
        ok = False
        text = ""

    monkeypatch.setattr(app_mod.requests, "get", lambda *_a, **_kw: _Resp500())
    with pytest.raises(_BadGateway):
        app_mod._fetch_article_html("2026-06-08-error")

    def _raise_req(*_a: Any, **_kw: Any) -> Any:
        raise _RequestException("timeout")

    monkeypatch.setattr(app_mod.requests, "get", _raise_req)
    with pytest.raises(_BadGateway):
        app_mod._fetch_article_html("2026-06-08-timeout")
