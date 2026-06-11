"""Unit tests for scripts/sigstore_sign.py.

The script no-ops in three branches (no config / no cosign / no public),
runs the cosign subprocess for each dated article in the fourth, and
mirrors the public key when configured. Each branch is verified here
with monkeypatched filesystem + subprocess.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import sigstore_sign as ss

# ---------------------------------------------------------------------------
# _load_config
# ---------------------------------------------------------------------------


def test_load_config_returns_none_when_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(ss, "CONFIG_PATH", tmp_path / "missing.json")
    assert ss._load_config() is None


def test_load_config_parses_valid_json(tmp_path, monkeypatch):
    cfg = tmp_path / "config.json"
    cfg.write_text(json.dumps({"identity": "x@y"}), encoding="utf-8")
    monkeypatch.setattr(ss, "CONFIG_PATH", cfg)
    assert ss._load_config() == {"identity": "x@y"}


def test_load_config_handles_bad_json(tmp_path, monkeypatch, capsys):
    cfg = tmp_path / "config.json"
    cfg.write_text("{not json", encoding="utf-8")
    monkeypatch.setattr(ss, "CONFIG_PATH", cfg)
    assert ss._load_config() is None
    assert "cannot read" in capsys.readouterr().err


# ---------------------------------------------------------------------------
# _cosign_available
# ---------------------------------------------------------------------------


def test_cosign_available_returns_bool(monkeypatch):
    monkeypatch.setattr(ss.shutil, "which", lambda _: "/usr/local/bin/cosign")
    assert ss._cosign_available() is True
    monkeypatch.setattr(ss.shutil, "which", lambda _: None)
    assert ss._cosign_available() is False


# ---------------------------------------------------------------------------
# _sign_one
# ---------------------------------------------------------------------------


def test_sign_one_returns_false_when_key_path_missing(tmp_path, monkeypatch):
    html = tmp_path / "art" / "index.html"
    html.parent.mkdir()
    html.write_text("<html></html>", encoding="utf-8")
    out = tmp_path / "out"
    out.mkdir()
    monkeypatch.delenv("COSIGN_KEY_PATH", raising=False)
    assert ss._sign_one(html, out, {}) is False


def test_sign_one_returns_false_when_key_file_does_not_exist(
    tmp_path,
    monkeypatch,
):
    html = tmp_path / "art" / "index.html"
    html.parent.mkdir()
    html.write_text("<html></html>", encoding="utf-8")
    out = tmp_path / "out"
    out.mkdir()
    monkeypatch.setenv("COSIGN_KEY_PATH", str(tmp_path / "no.key"))
    assert ss._sign_one(html, out, {}) is False


def test_sign_one_invokes_cosign_and_returns_true_on_success(
    tmp_path,
    monkeypatch,
):
    html = tmp_path / "art" / "index.html"
    html.parent.mkdir()
    html.write_text("<html></html>", encoding="utf-8")
    out = tmp_path / "out"
    out.mkdir()
    key = tmp_path / "key"
    key.write_text("KEY", encoding="utf-8")
    monkeypatch.setenv("COSIGN_KEY_PATH", str(key))
    monkeypatch.setenv("MY_PASS", "secret")

    captured = {}

    class _Result:
        returncode = 0
        stderr = ""

    def fake_run(cmd, **kwargs):
        captured["cmd"] = cmd
        captured["env"] = kwargs.get("env", {})
        return _Result()

    monkeypatch.setattr(ss.subprocess, "run", fake_run)
    ok = ss._sign_one(html, out, {"password_env_var": "MY_PASS"})
    assert ok is True
    assert captured["cmd"][0] == "cosign"
    assert captured["env"]["COSIGN_PASSWORD"] == "secret"  # noqa: S105 — fake test value


def test_sign_one_returns_false_on_nonzero_exit(tmp_path, monkeypatch, capsys):
    html = tmp_path / "art" / "index.html"
    html.parent.mkdir()
    html.write_text("<html></html>", encoding="utf-8")
    out = tmp_path / "out"
    out.mkdir()
    key = tmp_path / "key"
    key.write_text("KEY", encoding="utf-8")
    monkeypatch.setenv("COSIGN_KEY_PATH", str(key))

    class _Result:
        returncode = 1
        stderr = "boom"

    monkeypatch.setattr(ss.subprocess, "run", lambda *a, **kw: _Result())
    assert ss._sign_one(html, out, {}) is False
    assert "cosign error" in capsys.readouterr().err


def test_sign_one_returns_false_on_oserror(tmp_path, monkeypatch, capsys):
    html = tmp_path / "art" / "index.html"
    html.parent.mkdir()
    html.write_text("<html></html>", encoding="utf-8")
    out = tmp_path / "out"
    out.mkdir()
    key = tmp_path / "key"
    key.write_text("KEY", encoding="utf-8")
    monkeypatch.setenv("COSIGN_KEY_PATH", str(key))

    def boom(*a, **kw):
        raise OSError("cosign binary not found")

    monkeypatch.setattr(ss.subprocess, "run", boom)
    assert ss._sign_one(html, out, {}) is False
    assert "cosign failed" in capsys.readouterr().err


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------


def test_main_skips_when_no_config(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(ss, "CONFIG_PATH", tmp_path / "missing.json")
    rc = ss.main()
    assert rc == 0
    out = capsys.readouterr().out
    assert "no _data/sigstore/config.json" in out


def test_main_skips_when_cosign_missing(tmp_path, monkeypatch, capsys):
    cfg = tmp_path / "config.json"
    cfg.write_text("{}", encoding="utf-8")
    monkeypatch.setattr(ss, "CONFIG_PATH", cfg)
    monkeypatch.setattr(ss, "_cosign_available", lambda: False)
    rc = ss.main()
    assert rc == 0
    assert "cosign binary not on PATH" in capsys.readouterr().err


def test_main_fails_when_public_dir_missing(tmp_path, monkeypatch, capsys):
    cfg = tmp_path / "config.json"
    cfg.write_text("{}", encoding="utf-8")
    monkeypatch.setattr(ss, "CONFIG_PATH", cfg)
    monkeypatch.setattr(ss, "_cosign_available", lambda: True)
    monkeypatch.setattr(ss, "PUBLIC", tmp_path / "no-public")
    rc = ss.main()
    assert rc == 1
    assert "public/ not built" in capsys.readouterr().err


def test_main_signs_each_dated_article(tmp_path, monkeypatch, capsys):
    cfg = tmp_path / "config.json"
    cfg.write_text("{}", encoding="utf-8")
    public = tmp_path / "public"
    sigstore = public / "sigstore"
    public.mkdir()

    for name in ["2026-05-19-foo", "2026-05-18-bar", "static-page", "labs"]:
        d = public / name
        d.mkdir()
        (d / "index.html").write_text("<html></html>", encoding="utf-8")

    monkeypatch.setattr(ss, "CONFIG_PATH", cfg)
    monkeypatch.setattr(ss, "PUBLIC", public)
    monkeypatch.setattr(ss, "SIGSTORE_DIR", sigstore)
    monkeypatch.setattr(ss, "BUNDLES_DIR", tmp_path / "sigstore-bundles")
    monkeypatch.setattr(ss, "_cosign_available", lambda: True)
    monkeypatch.setattr(ss, "_sign_one", lambda *a, **kw: True)

    rc = ss.main()
    assert rc == 0
    msg = capsys.readouterr().out
    assert "2 article(s) signed, 0 failed" in msg


def test_main_counts_failures_and_returns_one(tmp_path, monkeypatch, capsys):
    cfg = tmp_path / "config.json"
    cfg.write_text("{}", encoding="utf-8")
    public = tmp_path / "public"
    sigstore = public / "sigstore"
    public.mkdir()
    d = public / "2026-05-19-foo"
    d.mkdir()
    (d / "index.html").write_text("<html></html>", encoding="utf-8")

    monkeypatch.setattr(ss, "CONFIG_PATH", cfg)
    monkeypatch.setattr(ss, "PUBLIC", public)
    monkeypatch.setattr(ss, "SIGSTORE_DIR", sigstore)
    monkeypatch.setattr(ss, "_cosign_available", lambda: True)
    monkeypatch.setattr(ss, "_sign_one", lambda *a, **kw: False)

    rc = ss.main()
    assert rc == 1
    assert "0 article(s) signed, 1 failed" in capsys.readouterr().out


def test_main_skips_dated_dirs_without_index_html(tmp_path, monkeypatch, capsys):
    cfg = tmp_path / "config.json"
    cfg.write_text("{}", encoding="utf-8")
    public = tmp_path / "public"
    sigstore = public / "sigstore"
    public.mkdir()
    (public / "2026-05-19-empty").mkdir()  # no index.html

    monkeypatch.setattr(ss, "CONFIG_PATH", cfg)
    monkeypatch.setattr(ss, "PUBLIC", public)
    monkeypatch.setattr(ss, "SIGSTORE_DIR", sigstore)
    monkeypatch.setattr(ss, "_cosign_available", lambda: True)
    sign_called = []
    monkeypatch.setattr(
        ss,
        "_sign_one",
        lambda *a, **kw: sign_called.append(a) or True,
    )

    rc = ss.main()
    assert rc == 0
    assert sign_called == []


def test_main_copies_public_key_when_configured(tmp_path, monkeypatch):
    cfg_path = tmp_path / "config.json"
    pub_src = tmp_path / "cosign.pub"
    pub_src.write_text("KEY", encoding="utf-8")
    cfg_path.write_text(
        json.dumps({"public_key_local": str(pub_src)}),
        encoding="utf-8",
    )
    public = tmp_path / "public"
    sigstore = public / "sigstore"
    public.mkdir()
    monkeypatch.setattr(ss, "CONFIG_PATH", cfg_path)
    monkeypatch.setattr(ss, "PUBLIC", public)
    monkeypatch.setattr(ss, "SIGSTORE_DIR", sigstore)
    monkeypatch.setattr(ss, "BUNDLES_DIR", tmp_path / "sigstore-bundles")
    monkeypatch.setattr(ss, "_cosign_available", lambda: True)
    monkeypatch.setattr(ss, "_sign_one", lambda *a, **kw: True)

    ss.main()
    assert (sigstore / "cosign.pub").read_text(encoding="utf-8") == "KEY"


def test_main_mirrors_bundles_into_committed_store(tmp_path, monkeypatch):
    cfg_path = tmp_path / "config.json"
    pub_src = tmp_path / "cosign.pub"
    pub_src.write_text("KEY", encoding="utf-8")
    cfg_path.write_text(
        json.dumps({"public_key_local": str(pub_src)}),
        encoding="utf-8",
    )
    public = tmp_path / "public"
    sigstore = public / "sigstore"
    bundles = tmp_path / "sigstore-bundles"
    public.mkdir()
    d = public / "2026-05-19-foo"
    d.mkdir()
    (d / "index.html").write_text("<html></html>", encoding="utf-8")

    def fake_sign(html, out_dir, cfg):
        (out_dir / f"{html.parent.name}.bundle").write_text("BUNDLE", encoding="utf-8")
        return True

    monkeypatch.setattr(ss, "CONFIG_PATH", cfg_path)
    monkeypatch.setattr(ss, "PUBLIC", public)
    monkeypatch.setattr(ss, "SIGSTORE_DIR", sigstore)
    monkeypatch.setattr(ss, "BUNDLES_DIR", bundles)
    monkeypatch.setattr(ss, "_cosign_available", lambda: True)
    monkeypatch.setattr(ss, "_sign_one", fake_sign)

    rc = ss.main()
    assert rc == 0
    assert (bundles / "2026-05-19-foo.bundle").read_text(encoding="utf-8") == "BUNDLE"
    assert (bundles / "cosign.pub").read_text(encoding="utf-8") == "KEY"


def test_main_does_not_touch_committed_store_when_nothing_signed(tmp_path, monkeypatch):
    cfg = tmp_path / "config.json"
    cfg.write_text("{}", encoding="utf-8")
    public = tmp_path / "public"
    bundles = tmp_path / "sigstore-bundles"
    public.mkdir()
    d = public / "2026-05-19-foo"
    d.mkdir()
    (d / "index.html").write_text("<html></html>", encoding="utf-8")

    monkeypatch.setattr(ss, "CONFIG_PATH", cfg)
    monkeypatch.setattr(ss, "PUBLIC", public)
    monkeypatch.setattr(ss, "SIGSTORE_DIR", public / "sigstore")
    monkeypatch.setattr(ss, "BUNDLES_DIR", bundles)
    monkeypatch.setattr(ss, "_cosign_available", lambda: True)
    monkeypatch.setattr(ss, "_sign_one", lambda *a, **kw: False)

    rc = ss.main()
    assert rc == 1
    assert not bundles.exists()
