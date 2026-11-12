# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""The "Services" section of llms.txt, from ``_data/services.yml`` (plan F-10)."""

from __future__ import annotations

from pathlib import Path

import yaml

SERVICES = Path(__file__).resolve().parents[3] / "_data" / "services.yml"


def services_lines(base: str, path: Path = SERVICES) -> list[str]:
    """The "Services" section: the Work with me pages (_data/services.yml),
    each with its one-paragraph answer, so an assistant can say what is
    offered and link the right page (plan F-10)."""
    if not path.is_file():
        return []
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    hub = data.get("hub", {})
    hub_answer = " ".join(str(hub.get("answer", "")).split())
    lines = [
        "## Services",
        "",
        f"- [Work with me]({base}{hub.get('path', '/work-with-me/')}): {hub_answer}",
    ]
    lines.append(f"- [Speaking]({base}/speaking/): keynotes, panels and expert comment.")
    for page in data.get("pages", []):
        answer = " ".join(str(page.get("answer", "")).split())
        lines.append(f"- [{page['service_type']}]({base}{page['path']}): {answer}")
    return [*lines, ""]
