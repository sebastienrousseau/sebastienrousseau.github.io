# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""postbuild_lib/image_ratio.py: stock images keep their file's ratio."""

from __future__ import annotations

import json
from pathlib import Path

from postbuild_lib.image_ratio import correct_stock_image_ratio, load_dims, true_height

STOCK = "https://cloudcdn.pro/stocks/images/denys-nevozhai-2vmT5_FeMck"
DIMS = {"denys-nevozhai-2vmT5_FeMck": (2584, 1597)}


def _img(src: str, w: str, h: str) -> str:
    return f'<img class="story-hero-img" src="{src}" width="{w}" height="{h}" />'


def test_story_hero_gets_the_true_ratio() -> None:
    html = _img(f"{STOCK}-1920.webp", "1920", "1080")
    assert correct_stock_image_ratio(html, DIMS) == _img(f"{STOCK}-1920.webp", "1920", "1187")


def test_the_postbuild_default_is_corrected_keeping_the_width() -> None:
    out = correct_stock_image_ratio(_img(f"{STOCK}-1920.webp", "1200", "675"), DIMS)
    assert 'width="1200" height="742"' in out


def test_square_card_and_original_are_corrected() -> None:
    assert 'height="494"' in correct_stock_image_ratio(
        _img(f"{STOCK}-640.webp", "800", "800"), DIMS
    )
    assert 'height="1597"' in correct_stock_image_ratio(_img(f"{STOCK}.webp", "2584", "1000"), DIMS)


def test_right_sizes_unknown_images_and_partial_tags_are_left_alone() -> None:
    right = _img(f"{STOCK}-1920.webp", "1920", "1186")
    other = _img("https://cloudcdn.pro/stocks/images/unknown-1920.webp", "1200", "675")
    logo = '<img src="https://cloudcdn.pro/stocks/images/denys-nevozhai-2vmT5_FeMck.webp" width="10" />'
    page = f"{right}{other}{logo}"
    assert correct_stock_image_ratio(page, DIMS) == page


def test_pages_without_stock_images_are_returned_unchanged() -> None:
    page = '<img src="/a.png" width="1" height="1" />'
    assert correct_stock_image_ratio(page, DIMS) is page


def test_og_image_height_follows_the_image() -> None:
    head = (
        f'<meta property="og:image" content="{STOCK}-1920.webp">'
        '<meta property="og:image:width" content="1920">'
        '<meta property="og:image:height" content="1080">'
    )
    assert 'og:image:height" content="1187"' in correct_stock_image_ratio(head, DIMS)
    right = head.replace('content="1080"', 'content="1187"')
    assert correct_stock_image_ratio(right, DIMS) == right
    no_width = f'<meta property="og:image" content="{STOCK}-1920.webp">'
    assert correct_stock_image_ratio(no_width, DIMS) == no_width


def test_true_height_needs_a_stock_url() -> None:
    assert true_height("https://example.com/a.webp", 100, DIMS) is None
    assert true_height(f"{STOCK}-320.webp?x=1", 320, DIMS) == 198


def test_load_dims_reads_the_manifest(tmp_path: Path) -> None:
    path = tmp_path / "dims.json"
    path.write_text(json.dumps({"a": [4, 2]}), encoding="utf-8")
    assert load_dims(path) == {"a": (4, 2)}
    assert load_dims()["denys-nevozhai-2vmT5_FeMck"] == (2584, 1597)
    assert correct_stock_image_ratio(_img(f"{STOCK}-1920.webp", "1920", "1080")).count("1187") == 1
