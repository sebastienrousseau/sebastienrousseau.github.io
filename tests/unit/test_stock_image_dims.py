# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""scripts/editorial/stock_image_dims.py and the manifest it writes."""

from __future__ import annotations

import json
import struct
from pathlib import Path

import pytest
import stock_image_dims as sid

ROOT = Path(__file__).resolve().parents[2]


def _riff(chunk: bytes, body: bytes) -> bytes:
    return b"RIFF\x00\x00\x00\x00WEBP" + chunk + body


def test_every_referenced_stock_image_has_its_size_recorded() -> None:
    manifest = json.loads((ROOT / "_data" / "stock_image_dims.json").read_text(encoding="utf-8"))
    missing = sid.referenced_stems() - manifest.keys()
    assert not missing, f"run scripts/editorial/stock_image_dims.py; missing: {sorted(missing)}"
    assert all(w > 0 and h > 0 for w, h in manifest.values())


def test_vp8x_header() -> None:
    body = b"\x00" * 8 + (2583).to_bytes(3, "little") + (1596).to_bytes(3, "little")
    assert sid.webp_size(_riff(b"VP8X", body)) == (2584, 1597)


def test_vp8_lossy_header() -> None:
    body = b"\x00" * 10 + struct.pack("<HH", 1920, 1187)
    assert sid.webp_size(_riff(b"VP8 ", body)) == (1920, 1187)


def test_vp8l_lossless_header() -> None:
    bits = (640 - 1) | ((400 - 1) << 14)
    body = b"\x00" * 5 + bits.to_bytes(4, "little")
    assert sid.webp_size(_riff(b"VP8L", body)) == (640, 400)


def test_bad_headers_raise() -> None:
    with pytest.raises(ValueError, match="not a WebP"):
        sid.webp_size(b"\x89PNG" + b"\x00" * 30)
    with pytest.raises(ValueError, match="unknown WebP chunk"):
        sid.webp_size(_riff(b"ALPH", b"\x00" * 20))


def test_update_records_sizes_and_reports_failures() -> None:
    good = _riff(b"VP8 ", b"\x00" * 10 + struct.pack("<HH", 10, 5))

    def fetch(stem: str) -> bytes:
        if stem == "bad":
            raise OSError("404")
        return good

    out, failed = sid.update({"old": [1, 1]}, {"b", "bad", "a"}, fetch=fetch)
    assert out == {"a": [10, 5], "b": [10, 5], "old": [1, 1]} and list(out) == ["a", "b", "old"]
    assert failed == ["bad"]


def test_referenced_stems_strip_variant_suffixes(tmp_path: Path) -> None:
    (tmp_path / "_posts").mkdir()
    (tmp_path / "_posts" / "a.md").write_text(
        "https://cloudcdn.pro/stocks/images/x-y-1920.webp https://cloudcdn.pro/stocks/images/z.webp",
        encoding="utf-8",
    )
    assert sid.referenced_stems(tmp_path) == {"x-y", "z"}
