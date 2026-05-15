#!/usr/bin/env python3
"""Sign every rendered article with Sigstore (cosign sign-blob).

Each ``public/<slug>/index.html`` for a dated article gets a detached
signature at ``public/sigstore/<slug>.sig`` + a Sigstore bundle at
``public/sigstore/<slug>.bundle``. The visible article footer then
links to the bundle so any reader can verify the page bytes match
what the author signed.

**Activation.** This script no-ops unless ``_data/sigstore/config.json``
exists and points at a usable cosign key. That guard is intentional:
the build pipeline must never emit fake signatures (a footer that
says "Signed" but isn't is worse than no footer at all). To activate:

  1. Install cosign: ``brew install cosign`` (or distro equivalent).
  2. Generate a keypair: ``cosign generate-key-pair``. Treat
     ``cosign.key`` like an SSH private key — never commit.
  3. Publish ``cosign.pub`` to a stable URL (the site itself, GitHub,
     keys server, …).
  4. Author ``_data/sigstore/config.json`` with:
        {
          "identity": "<email or DID>",
          "public_key_url": "https://sebastienrousseau.com/sigstore/cosign.pub",
          "key_env_var": "COSIGN_KEY_PATH",
          "password_env_var": "COSIGN_PASSWORD"
        }
  5. CI/runtime sets the env vars from secrets.
  6. Push and watch the build sign every dated article.

Until then this script prints a one-line status and exits 0 — so the
build stays green; just no signatures are emitted.

See ``DEPLOY.md`` for the runbook.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
SIGSTORE_DIR = PUBLIC / "sigstore"
CONFIG_PATH = ROOT / "_data" / "sigstore" / "config.json"

_DATED_DIR_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-")


def _load_config() -> dict | None:
    if not CONFIG_PATH.is_file():
        return None
    try:
        return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        print(f"sigstore: cannot read {CONFIG_PATH}: {e}", file=sys.stderr)
        return None


def _cosign_available() -> bool:
    return shutil.which("cosign") is not None


def _sign_one(html_path: Path, out_dir: Path, cfg: dict) -> bool:
    """Run ``cosign sign-blob`` against one article and write the
    detached signature + bundle to ``out_dir``. Returns True on success."""
    key_path = os.environ.get(cfg.get("key_env_var", "COSIGN_KEY_PATH"))
    if not key_path or not Path(key_path).is_file():
        return False
    sig_path = out_dir / f"{html_path.parent.name}.sig"
    bundle_path = out_dir / f"{html_path.parent.name}.bundle"
    cmd = [
        "cosign", "sign-blob",
        "--key", key_path,
        "--bundle", str(bundle_path),
        "--output-signature", str(sig_path),
        "--yes",
        str(html_path),
    ]
    env = dict(os.environ)
    pw_env = cfg.get("password_env_var")
    if pw_env and pw_env in env:
        env["COSIGN_PASSWORD"] = env[pw_env]
    try:
        result = subprocess.run(
            cmd, check=False, capture_output=True, text=True, env=env, timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired) as e:
        print(f"sigstore: cosign failed for {html_path.parent.name}: {e}",
              file=sys.stderr)
        return False
    if result.returncode != 0:
        print(f"sigstore: cosign error for {html_path.parent.name}: "
              f"{result.stderr.strip()}", file=sys.stderr)
        return False
    return True


def main() -> int:
    cfg = _load_config()
    if cfg is None:
        print("sigstore: no _data/sigstore/config.json — signing skipped "
              "(see scripts/sigstore_sign.py docstring for activation)")
        return 0
    if not _cosign_available():
        print("sigstore: cosign binary not on PATH — signing skipped", file=sys.stderr)
        return 0
    if not PUBLIC.is_dir():
        print("sigstore: public/ not built — run ./build.sh first", file=sys.stderr)
        return 1

    SIGSTORE_DIR.mkdir(parents=True, exist_ok=True)

    # Mirror the cosign public key into /sigstore/cosign.pub so the
    # verify command in the article footer works without external hops.
    pub_src = cfg.get("public_key_local")
    if pub_src and Path(pub_src).is_file():
        shutil.copy2(pub_src, SIGSTORE_DIR / "cosign.pub")

    signed = 0
    failed = 0
    for article_dir in sorted(PUBLIC.iterdir()):
        if not article_dir.is_dir() or not _DATED_DIR_RE.match(article_dir.name):
            continue
        html = article_dir / "index.html"
        if not html.is_file():
            continue
        if _sign_one(html, SIGSTORE_DIR, cfg):
            signed += 1
        else:
            failed += 1
    print(f"sigstore: {signed} article(s) signed, {failed} failed")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
