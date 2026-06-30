"""Golden-file snapshot tests for the listing generators' pure render
functions — improvement-plan-2026 Phase 1.4.

Each generator turns structured data into a fixed block of markup. A silent
change to that markup (a dropped field, a renamed class, a reordered
attribute) is the "gen_papers silently dropped an entry" class of bug: the
build still succeeds and the page still renders, so nothing fails — the
output is just quietly wrong.

These tests pin the exact bytes each render function emits for a fixed
input. When a change is intentional, regenerate the goldens:

    UPDATE_GOLDEN=1 python3 -m pytest tests/unit/test_generator_golden.py

and review the diff before committing. When a change is *un*intentional, the
test fails with a unified diff pointing at the regression.
"""

from __future__ import annotations

import difflib
import os
from pathlib import Path

import gen_articles
import gen_papers
import gen_projects
import pytest

GOLDEN_DIR = Path(__file__).parent / "golden"

# Fixed, representative inputs. Deliberately boring values so the golden
# captures structure, not data — and so an attribute/field regression shows
# up as a clear diff.
_PROJECT_ITEM = (
    "Python · ISO 20022",
    "examplelib",
    "https://cloudcdn.pro/clients/examplelib/v1/logos/examplelib.svg",
    "examplelib logo",
    "A one-line summary of what examplelib does for the catalogue card.",
    "https://example.com/examplelib",
)
_PROJECT_SECTION = {
    "kicker": "EXAMPLE CATEGORY",
    "title": "Example category title.",
    "lede": "A short lede describing the example category.",
    "items": [_PROJECT_ITEM],
}
_ARTICLE_TUPLE = (
    "2026-06-30",
    "June 30, 2026",
    "Agentic Ai · Banking · Governance",
    "An Example Article Title",
    "https://cloudcdn.pro/stocks/images/example-1920.webp",
    "Example banner alt text",
    "A one-sentence excerpt that appears under the article card.",
    "https://example.com/2026-06-30-example-article",
)


def _render_cases() -> dict[str, str]:
    """name -> rendered markup. One entry per golden file."""
    a_eyebrow, a_title, a_img, a_alt, a_iso, a_disp, a_excerpt, a_href = (
        "Agentic Ai · Banking · Governance",
        "An Example Article Title",
        "https://cloudcdn.pro/stocks/images/example-1920.webp",
        "Example banner alt text",
        "2026-06-30",
        "June 30, 2026",
        "A one-sentence excerpt that appears under the article card.",
        "https://example.com/2026-06-30-example-article",
    )
    return {
        # gen_articles
        "gen_articles.card_block": gen_articles.card_block(
            a_eyebrow, a_title, a_img, a_alt, a_iso, a_disp, a_excerpt, a_href
        ),
        "gen_articles.featured_block": gen_articles.featured_block(_ARTICLE_TUPLE),
        "gen_articles._eyebrow_from_tags": gen_articles._eyebrow_from_tags(
            "agentic ai, banking, governance, extra, ignored"
        ),
        # gen_papers — the two featured cards read module constants, so the
        # golden also guards the committed featured-paper metadata.
        "gen_papers.epaa_card_block": gen_papers.epaa_card_block(),
        "gen_papers.whisper_card_block": gen_papers.whisper_card_block(),
        "gen_papers.card_block": gen_papers.card_block(
            a_iso, a_disp, a_eyebrow, a_title, a_img, a_alt, a_excerpt, a_href
        ),
        # gen_projects
        "gen_projects.card_block": gen_projects.card_block(_PROJECT_ITEM),
        "gen_projects.featured_block": gen_projects.featured_block(_PROJECT_ITEM),
        "gen_projects.section_block": gen_projects.section_block(_PROJECT_SECTION),
    }


CASES = _render_cases()


@pytest.mark.parametrize("name", sorted(CASES))
def test_generator_render_matches_golden(name: str) -> None:
    actual = CASES[name]
    golden_path = GOLDEN_DIR / f"{name}.html"

    if os.environ.get("UPDATE_GOLDEN"):
        GOLDEN_DIR.mkdir(exist_ok=True)
        golden_path.write_text(actual, encoding="utf-8")
        pytest.skip(f"updated golden: {golden_path.name}")

    assert golden_path.is_file(), (
        f"missing golden {golden_path.name}; run "
        f"UPDATE_GOLDEN=1 pytest {Path(__file__).name} to create it"
    )
    expected = golden_path.read_text(encoding="utf-8")
    if actual != expected:
        diff = "\n".join(
            difflib.unified_diff(
                expected.splitlines(),
                actual.splitlines(),
                fromfile=f"{name} (golden)",
                tofile=f"{name} (actual)",
                lineterm="",
            )
        )
        raise AssertionError(f"{name} render drifted from golden:\n{diff}")
