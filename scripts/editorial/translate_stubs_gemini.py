#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Translate incomplete locale posts with the Gemini API.

This backend is intended for long-form posts that exceed practical Ollama
Cloud reliability. It reuses the same source mapping, prompt, and validation
logic as the Ollama translator.
"""

from __future__ import annotations

import argparse
import contextlib
import http.client
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

sys.path.insert(0, str(Path(__file__).resolve().parent))
import translate_stubs_ollama as shared


def load_api_key(key_file: Path | None = None) -> str:
    if api_key := os.environ.get("GEMINI_API_KEY"):
        return api_key
    if key_file:
        return key_file.read_text(encoding="utf-8").strip()
    if key_file_env := os.environ.get("GEMINI_API_KEY_FILE"):
        return Path(key_file_env).read_text(encoding="utf-8").strip()
    return ""


def _post_json(request: urllib.request.Request, timeout: int) -> str:
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8")


def _retry_delay_seconds(detail: str) -> int:
    """Seconds to wait after a 429, from the API's own ``retryDelay`` hint.

    A couple of seconds are added so we never come back before the window
    the server named. Falls back to 35s when the body doesn't carry a hint.
    """
    with contextlib.suppress(KeyError, ValueError, json.JSONDecodeError, TypeError):
        hint = json.loads(detail)["error"]["details"][-1]["retryDelay"]
        return int(hint.rstrip("s")) + 2
    return 35


def _build_request(model: str, prompt: str, api_key: str) -> urllib.request.Request:
    """The generateContent POST for one prompt."""
    model_path = urllib.parse.quote(model, safe="")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_path}:generateContent"
    payload = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.2,
            "topP": 0.9,
            "maxOutputTokens": 65536,
            "responseMimeType": "text/plain",
        },
    }
    return urllib.request.Request(
        f"{url}?key={urllib.parse.quote(api_key)}",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )


def _post_with_retries(request: urllib.request.Request, timeout: int, retries: int) -> str:
    """POST the request, backing off on 429 and transient transport errors."""
    for attempt in range(retries + 1):
        try:
            return _post_json(request, timeout)
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            if exc.code == 429 and attempt < retries:
                time.sleep(_retry_delay_seconds(detail))
                continue
            raise RuntimeError(f"Gemini API request failed: HTTP {exc.code}: {detail}") from exc
        except (urllib.error.URLError, http.client.RemoteDisconnected) as exc:
            if attempt < retries:
                time.sleep(2 + attempt * 4)
                continue
            raise RuntimeError(f"Gemini API request failed: {exc}") from exc
    raise RuntimeError("Gemini API request failed after retries")


def _join_candidate_text(body: str) -> str:
    """Concatenate the text parts of every candidate in a response body."""
    data = json.loads(body)
    parts: list[str] = []
    for candidate in data.get("candidates", []):
        parts.extend(
            text
            for part in candidate.get("content", {}).get("parts", [])
            if (text := part.get("text"))
        )
    if not parts:
        raise RuntimeError(f"Gemini API returned no text: {body[:1000]}")
    return "\n".join(parts)


def gemini_generate(model: str, prompt: str, timeout: int, api_key: str, retries: int = 2) -> str:
    request = _build_request(model, prompt, api_key)
    body = _post_with_retries(request, timeout, retries)
    return shared.extract_translation(_join_candidate_text(body))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default="gemini-2.5-pro", help="Gemini model name")
    parser.add_argument("--langs", nargs="*", help="optional locale codes to process")
    parser.add_argument("--limit", type=int, help="maximum number of files to translate")
    parser.add_argument("--timeout", type=int, default=1200, help="per-file timeout in seconds")
    parser.add_argument(
        "--dry-run", action="store_true", help="list target files without translating"
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        help="write translated files here for testing instead of overwriting repo files",
    )
    parser.add_argument("--api-key-file", type=Path, help="read the Gemini API key from this file")
    args = parser.parse_args()

    api_key = load_api_key(args.api_key_file)
    if not api_key and not args.dry_run:
        raise SystemExit("GEMINI_API_KEY is not set; alternatively set GEMINI_API_KEY_FILE")

    langs = set(args.langs) if args.langs else None
    paths = shared.defect_paths(langs)
    if args.limit is not None:
        paths = paths[: args.limit]

    if not paths:
        print("No incomplete locale posts matched.")
        return 0

    for path in paths:
        rel = path.relative_to(ROOT)
        source = shared.english_source_for(path)
        print(f"{rel} <- {source.relative_to(ROOT)}")
        if args.dry_run:
            continue

        prompt = shared.prompt_for(
            path.parent.name,
            source.read_text(encoding="utf-8"),
            path.read_text(encoding="utf-8"),
        )
        translated = gemini_generate(args.model, prompt, args.timeout, api_key or "")
        shared.validate(path, translated)

        if args.out_dir:
            out_path = args.out_dir / rel
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(translated.rstrip() + "\n", encoding="utf-8")
        else:
            path.write_text(translated.rstrip() + "\n", encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
