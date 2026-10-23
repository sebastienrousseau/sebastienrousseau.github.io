# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""mark_untranslated_english marks English left on translated pages.

The property that matters is WCAG 3.1.2: English text on a page that
declares another language must carry ``lang="en"``, and translated text
must not. Getting it wrong either way is silent: the page renders the
same and only a screen reader's voice changes.
"""

from __future__ import annotations

from pathlib import Path

import mark_untranslated_english as mue

EN_MAIN = (
    '<html lang="en-GB"><body><main>'
    "<h2>Articles in this topic</h2>"
    "<p>Browse the editorial corpus by pillar.</p>"
    "<p>Rails &amp; settlement and treasury.</p>"
    "<pre>Do not mark this code sample</pre>"
    "</main><footer><p>Read the privacy notice</p></footer></body></html>"
)


def _english() -> set[str]:
    return mue.english_phrases(EN_MAIN)


def test_english_phrases_reads_main_of_an_english_page() -> None:
    phrases = _english()
    assert "Articles in this topic" in phrases
    assert "Rails & settlement and treasury." in phrases
    assert "Read the privacy notice" not in phrases  # outside <main>
    assert "Do not mark this code sample" not in phrases  # inside <pre>


def test_whole_element_text_gets_lang_on_the_element() -> None:
    page = '<html lang="zh-Hans"><main><h2 class="t">Articles in this topic</h2></main></html>'
    out, count = mue.mark_untranslated(page, _english())
    assert count == 1
    assert '<h2 class="t" lang="en">Articles in this topic</h2>' in out


def test_text_beside_other_content_is_wrapped_in_a_span() -> None:
    page = (
        '<html lang="fr"><main><p>Articles in this topic <a href="/fr/">ici</a></p></main></html>'
    )
    out, count = mue.mark_untranslated(page, _english())
    assert count == 1
    assert '<p><span lang="en">Articles in this topic </span><a href="/fr/">ici</a></p>' in out


def test_text_with_an_entity_is_matched_as_one_node() -> None:
    page = '<html lang="de"><main><p>Rails &amp; settlement and treasury.</p></main></html>'
    out, count = mue.mark_untranslated(page, _english())
    assert count == 1
    assert '<p lang="en">Rails &amp; settlement and treasury.</p>' in out


def test_translated_text_is_left_alone() -> None:
    page = '<html lang="zh-Hans"><main><h2>本主题的文章</h2></main></html>'
    assert mue.mark_untranslated(page, _english()) == (page, 0)


def test_text_outside_main_and_in_code_is_left_alone() -> None:
    page = (
        '<html lang="fr"><main><pre>Do not mark this code sample</pre></main>'
        "<footer><p>Articles in this topic</p></footer></html>"
    )
    assert mue.mark_untranslated(page, _english() | {"Do not mark this code sample"}) == (page, 0)


def test_short_phrases_are_not_candidates() -> None:
    """Brand names and two-word labels read the same in every language."""
    assert "Sebastien Rousseau" not in mue.english_phrases(
        '<html lang="en"><main><p>Sebastien Rousseau</p></main></html>'
    )


def test_a_second_run_changes_nothing() -> None:
    page = '<html lang="ja"><main><p>Articles in this topic <b>x</b></p><h2>Articles in this topic</h2></main></html>'
    once, first = mue.mark_untranslated(page, _english())
    twice, second = mue.mark_untranslated(once, _english())
    assert first == 2
    assert (twice, second) == (once, 0)


def test_process_marks_translated_pages_from_the_english_site(tmp_path: Path) -> None:
    """Any English page is a reference, not only the page's own counterpart."""
    (tmp_path / "topics").mkdir()
    (tmp_path / "topics" / "index.html").write_text(EN_MAIN, encoding="utf-8")
    page = tmp_path / "zh-hans" / "biaoqian" / "index.html"
    page.parent.mkdir(parents=True)
    page.write_text(
        '<html lang="zh-Hans"><body><main><h2>Articles in this topic</h2>'
        "<p>翻译过的文字</p></main></body></html>",
        encoding="utf-8",
    )
    english_before = (tmp_path / "topics" / "index.html").read_text(encoding="utf-8")
    assert mue.process(tmp_path) == (1, 1)
    text = page.read_text(encoding="utf-8")
    assert '<h2 lang="en">Articles in this topic</h2>' in text
    assert "<p>翻译过的文字</p>" in text
    assert (tmp_path / "topics" / "index.html").read_text(encoding="utf-8") == english_before
    assert mue.process(tmp_path) == (0, 0)


def test_process_leaves_pages_without_a_language_alone(tmp_path: Path) -> None:
    (tmp_path / "index.html").write_text(EN_MAIN, encoding="utf-8")
    stub = tmp_path / "papers" / "index.html"
    stub.parent.mkdir()
    stub.write_text("<html><main><h2>Articles in this topic</h2></main></html>", encoding="utf-8")
    assert mue.process(tmp_path) == (0, 0)
