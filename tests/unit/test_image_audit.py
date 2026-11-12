# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""scripts/seo_and_audit/image_audit.py (plan F-1)."""

from __future__ import annotations

from pathlib import Path

import image_audit as ia

GOOD = '<img src="/a.webp" width="1200" height="742" fetchpriority="high">'


def test_clean_page() -> None:
    page = f"<body>{GOOD}<img src='/b.svg' width='1' height='1' loading='lazy'></body>"
    assert ia.audit_page(page) == ([], [])


def test_errors_for_size_lazy_first_and_missing_priority() -> None:
    errors, _ = ia.audit_page('<body><img src="/a.webp" loading="lazy"></body>')
    assert len(errors) == 1
    avatar = '<img src="/me.webp" width="36" height="36" loading="lazy">'
    errors, _ = ia.audit_page(
        f'<body>{avatar}<img src="/b.webp" width="1200" height="742" loading="lazy"></body>'
    )
    assert len(errors) == 2


def test_warnings_for_legacy_formats_and_oversized_variants() -> None:
    page = (
        f"<body>{GOOD}"
        '<img src="/x.jpg" width="5" height="5">'
        '<img src="https://cloudcdn.pro/stocks/images/a-1920.webp" width="600" height="371">'
        '<img src="https://cloudcdn.pro/stocks/images/a-1920.webp" width="600" height="371" srcset="x">'
        "</body>"
    )
    errors, warnings = ia.audit_page(page)
    assert errors == [] and len(warnings) == 2


def test_main_reports_and_fails_on_errors(tmp_path: Path) -> None:
    (tmp_path / "a").mkdir()
    (tmp_path / "a" / "index.html").write_text("<body><img src='/x.webp'></body>", encoding="utf-8")
    assert ia.main([str(tmp_path)]) == 1
    (tmp_path / "a" / "index.html").write_text(f"<body>{GOOD}</body>", encoding="utf-8")
    assert ia.main([str(tmp_path)]) == 0
    assert ia.audit_page(GOOD) == ([], [])
