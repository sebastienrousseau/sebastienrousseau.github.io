# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""postbuild_lib/llms_services.py: the llms.txt Services section."""

from __future__ import annotations

from pathlib import Path

from postbuild_lib.llms_services import services_lines

BASE = "https://sebastienrousseau.com"


def test_lists_the_hub_speaking_and_each_service_page() -> None:
    lines = services_lines(BASE)
    assert lines[0] == "## Services" and lines[-1] == ""
    text = "\n".join(lines)
    for path in (
        "/work-with-me/",
        "/speaking/",
        "/work-with-me/research/",
        "/work-with-me/open-source/",
    ):
        assert f"]({BASE}{path})" in text


def test_missing_or_empty_data(tmp_path: Path) -> None:
    assert services_lines(BASE, tmp_path / "none.yml") == []
    empty = tmp_path / "s.yml"
    empty.write_text("{}\n", encoding="utf-8")
    assert services_lines(BASE, empty)[2].startswith(f"- [Work with me]({BASE}/work-with-me/)")
