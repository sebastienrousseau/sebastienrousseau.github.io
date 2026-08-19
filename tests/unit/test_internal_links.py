"""Contextual internal linking (F-05).

The corpus had a median of 2 unique internal links per article inside
<main>, 65 % of articles below three, and zero contextual in-prose links on
the pages sampled — while averaging 8 outbound links each.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "lib"))
sys.path.insert(0, str(ROOT / "scripts" / "postbuild"))

from postbuild_lib.internal_links import (
    _alias_patterns,
    alias_to_canonical,
    canonicalise_absolute_self_links,
    inject_contextual_links,
    inject_related_cluster,
    load_corpus,
    rank_targets,
)

PUBLIC = Path("public")
PAGE = PUBLIC / "2026-08-04-data-act-cloud-switching-dora-exit-strategies-2026" / "index.html"

TAXONOMY = {
    "dora": {
        "name": "DORA",
        "aliases": ["DORA", "Digital Operational Resilience Act"],
        "category": "policy",
    },
    "iso-20022": {"name": "ISO 20022", "aliases": ["ISO 20022"], "category": "payments"},
    "banking": {"name": "Banking", "aliases": ["banking"], "category": "policy"},
}

CORPUS = [
    {"stem": "2026-08-03-cra-reporting", "title": "The CRA Clock", "tags": {"dora", "banking"}},
    {"stem": "2026-07-29-tlpt", "title": "Red Team & Supply Chain", "tags": {"dora"}},
    {"stem": "2023-11-12-old-post", "title": "An Older Post", "tags": {"dora", "banking"}},
    {"stem": "2026-06-01-iso", "title": "ISO 20022 After Migration", "tags": {"iso-20022"}},
    {
        "stem": "2026-08-04-data-act-cloud-switching-dora-exit-strategies-2026",
        "title": "Self",
        "tags": {"dora", "banking"},
    },
]


def _page(body: str, lang: str = "en-GB") -> str:
    return f'<html lang="{lang}"><body><main>{body}</main></body></html>'


def _anchors(html: str) -> list[tuple[str, str]]:
    return re.findall(r'<a href="([^"]+)"[^>]*data-topic-link>([^<]+)</a>', html)


# ----------------------------------------------------------------- ranking


def test_ranking_prefers_more_shared_tags_then_recency() -> None:
    order = [a["stem"] for a in rank_targets({"dora", "banking"}, CORPUS, "2026-08-04-data-act-cloud-switching-dora-exit-strategies-2026")]
    # 2-tag matches first, newest of those first.
    assert order[0] == "2026-08-03-cra-reporting"
    assert order[1] == "2023-11-12-old-post"
    assert "2026-07-29-tlpt" in order


def test_ranking_never_returns_the_article_itself() -> None:
    stems = [a["stem"] for a in rank_targets({"dora"}, CORPUS, "2026-07-29-tlpt")]
    assert "2026-07-29-tlpt" not in stems


# -------------------------------------------------------------- contextual


def test_first_prose_mention_is_linked() -> None:
    html = _page("<p>DORA already asked for more than a document here.</p>")
    out = inject_contextual_links(PAGE, html, CORPUS, TAXONOMY, public=PUBLIC)
    assert _anchors(out) == [("/2026-08-03-cra-reporting/", "DORA")]


def test_recent_sibling_wins_over_an_older_one() -> None:
    """A 2026 regulatory piece must link the current treatment, not a 2023 post."""
    html = _page("<p>DORA already asked for more than a document here.</p>")
    out = inject_contextual_links(PAGE, html, CORPUS, TAXONOMY, public=PUBLIC)
    assert "2023-11-12-old-post" not in out


def test_paragraph_with_an_existing_link_is_skipped() -> None:
    html = _page('<p>DORA and <a href="/x/">something</a> here in prose.</p>')
    assert inject_contextual_links(PAGE, html, CORPUS, TAXONOMY, public=PUBLIC) == html


def test_code_is_never_linked() -> None:
    html = _page("<p>Run <code>DORA</code> in the shell to see it.</p>")
    assert inject_contextual_links(PAGE, html, CORPUS, TAXONOMY, public=PUBLIC) == html


def test_lead_aside_is_skipped() -> None:
    html = _page('<p class="post-lead-tldr">DORA already asked for more here.</p>')
    assert inject_contextual_links(PAGE, html, CORPUS, TAXONOMY, public=PUBLIC) == html


def test_one_link_per_tag_and_per_target() -> None:
    html = _page("<p>DORA one here.</p><p>DORA two here.</p><p>DORA three here.</p>")
    out = inject_contextual_links(PAGE, html, CORPUS, TAXONOMY, public=PUBLIC)
    assert len(_anchors(out)) == 1


def test_link_count_is_capped() -> None:
    body = "".join(f"<p>DORA and ISO 20022 and banking, paragraph {i}.</p>" for i in range(40))
    out = inject_contextual_links(PAGE, _page(body), CORPUS, TAXONOMY, public=PUBLIC)
    assert 0 < len(_anchors(out)) <= 6


def test_contextual_linking_is_idempotent() -> None:
    html = _page("<p>DORA already asked for more than a document here.</p><p>ISO 20022 matters.</p>")
    once = inject_contextual_links(PAGE, html, CORPUS, TAXONOMY, public=PUBLIC)
    assert inject_contextual_links(PAGE, once, CORPUS, TAXONOMY, public=PUBLIC) == once


def test_locale_pages_are_left_alone() -> None:
    html = _page("<p>DORA already asked for more here.</p>", lang="fr-FR")
    page = PUBLIC / "fr" / "2026-08-04-data-act-cloud-switching-dora-exit-strategies-2026" / "index.html"
    assert inject_contextual_links(page, html, CORPUS, TAXONOMY, public=PUBLIC) == html


def test_non_article_pages_are_left_alone() -> None:
    html = _page("<p>DORA already asked for more here.</p>")
    assert inject_contextual_links(PUBLIC / "about" / "index.html", html, CORPUS, TAXONOMY, public=PUBLIC) == html


def test_word_boundaries_are_respected() -> None:
    html = _page("<p>The DORATRON machine is unrelated to anything here.</p>")
    assert inject_contextual_links(PAGE, html, CORPUS, TAXONOMY, public=PUBLIC) == html


def test_target_title_becomes_the_link_title_attribute() -> None:
    html = _page("<p>DORA already asked for more than a document here.</p>")
    out = inject_contextual_links(PAGE, html, CORPUS, TAXONOMY, public=PUBLIC)
    assert 'title="The CRA Clock"' in out


# ------------------------------------------------------------------ cluster


def test_cluster_block_links_unlinked_siblings() -> None:
    out = inject_related_cluster(PAGE, _page("<p>Body.</p>"), CORPUS, public=PUBLIC)
    assert 'class="cluster-links"' in out
    hrefs = re.findall(r'<li><a href="([^"]+)"', out)
    assert "/2026-08-03-cra-reporting/" in hrefs
    assert "/2026-08-04-data-act-cloud-switching-dora-exit-strategies-2026/" not in hrefs


def test_cluster_block_skips_already_linked_articles() -> None:
    html = _page('<p>See <a href="/2026-08-03-cra-reporting/">this</a>.</p>')
    out = inject_related_cluster(PAGE, html, CORPUS, public=PUBLIC)
    assert out.count("/2026-08-03-cra-reporting/") == 1


def test_cluster_block_is_idempotent() -> None:
    once = inject_related_cluster(PAGE, _page("<p>Body.</p>"), CORPUS, public=PUBLIC)
    assert inject_related_cluster(PAGE, once, CORPUS, public=PUBLIC) == once


def test_cluster_block_is_a_labelled_nav_landmark() -> None:
    out = inject_related_cluster(PAGE, _page("<p>Body.</p>"), CORPUS, public=PUBLIC)
    assert '<nav class="cluster-links" aria-labelledby="cluster-links-heading">' in out
    assert 'id="cluster-links-heading"' in out


# ------------------------------------------------------------- canonical URLs


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        (
            '<a href="https://sebastienrousseau.com/2026-08-03-slug">x</a>',
            '<a href="https://sebastienrousseau.com/2026-08-03-slug/">x</a>',
        ),
        (
            '<a href="https://sebastienrousseau.com/2026-08-03-slug/">x</a>',
            '<a href="https://sebastienrousseau.com/2026-08-03-slug/">x</a>',
        ),
        ('<a href="https://example.com/2026-08-03-slug">x</a>', '<a href="https://example.com/2026-08-03-slug">x</a>'),
        ('<a href="https://sebastienrousseau.com/about">x</a>', '<a href="https://sebastienrousseau.com/about">x</a>'),
    ],
)
def test_absolute_self_links_get_the_canonical_trailing_slash(raw: str, expected: str) -> None:
    assert canonicalise_absolute_self_links(raw) == expected


def test_canonicalising_is_idempotent() -> None:
    raw = '<a href="https://sebastienrousseau.com/2026-08-03-slug">x</a>'
    once = canonicalise_absolute_self_links(raw)
    assert canonicalise_absolute_self_links(once) == once


# --------------------------------------------------------------- real repo


def test_real_taxonomy_and_corpus_load() -> None:
    """Guards the wiring against a taxonomy or front-matter shape change."""
    corpus = load_corpus(ROOT / "_posts")
    assert len(corpus) > 50
    assert all(a["title"] and isinstance(a["tags"], set) for a in corpus)
    assert any(a["tags"] for a in corpus)


def test_slug_shaped_aliases_are_not_matched_in_prose() -> None:
    patterns = _alias_patterns({"iso-20022": {"aliases": ["iso-20022", "ISO 20022"]}})
    assert [p.pattern for _, p in patterns] == [r"(?<![\w-])ISO\ 20022(?![\w-])"]


def test_alias_map_includes_the_slug_itself() -> None:
    assert alias_to_canonical(TAXONOMY)["dora"] == "dora"


# ------------------------------------------------- edge cases and guard rails
#
# The postbuild_lib coverage gate is 100 %, so every defensive branch needs a
# case. These are the failure modes the pass must survive on a real tree: a
# missing taxonomy, a post with no front matter, a page outside public/, a
# locale with no slug map.


def test_missing_taxonomy_file_yields_empty(tmp_path: Path) -> None:
    from postbuild_lib.internal_links import load_taxonomy

    assert load_taxonomy(tmp_path / "absent.yml") == {}


def test_missing_posts_dir_yields_empty_corpus(tmp_path: Path) -> None:
    assert load_corpus(tmp_path / "nope") == []


def test_posts_without_frontmatter_are_skipped(tmp_path: Path) -> None:
    posts = tmp_path / "_posts"
    posts.mkdir()
    (posts / "2026-01-01-no-frontmatter.md").write_text("# Just a heading", encoding="utf-8")
    (posts / "2026-01-02-no-tags.md").write_text(
        '---\ntitle: "T"\n---\nbody', encoding="utf-8"
    )
    (posts / "not-dated.md").write_text('---\ntitle: "T"\ntags: "dora"\n---\n', encoding="utf-8")
    (posts / "2026-01-03-good.md").write_text(
        '---\ntitle: "Good"\ntags: "DORA"\n---\nbody', encoding="utf-8"
    )
    corpus = load_corpus(posts, taxonomy=TAXONOMY)
    assert [a["stem"] for a in corpus] == ["2026-01-03-good"]


def test_unparseable_page_path_is_ignored() -> None:
    """A page outside public/ has no stem and must not be linked."""
    outside = Path("/somewhere/else/index.html")
    html = _page("<p>DORA already asked for more here.</p>")
    assert inject_contextual_links(outside, html, CORPUS, TAXONOMY, public=PUBLIC) == html
    assert inject_related_cluster(outside, html, CORPUS, public=PUBLIC) == html


def test_bare_public_root_is_not_an_article() -> None:
    html = _page("<p>DORA already asked for more here.</p>")
    assert inject_contextual_links(PUBLIC / "index.html", html, CORPUS, TAXONOMY, public=PUBLIC) == html


def test_article_absent_from_the_corpus_is_skipped() -> None:
    page = PUBLIC / "2026-01-01-unknown-article" / "index.html"
    html = _page("<p>DORA already asked for more here.</p>")
    assert inject_contextual_links(page, html, CORPUS, TAXONOMY, public=PUBLIC) == html
    assert inject_related_cluster(page, html, CORPUS, public=PUBLIC) == html


def test_article_with_no_canonical_tags_is_skipped() -> None:
    corpus = [{"stem": PAGE.parent.name, "title": "Self", "tags": set()}]
    html = _page("<p>DORA already asked for more here.</p>")
    assert inject_contextual_links(PAGE, html, corpus, TAXONOMY, public=PUBLIC) == html


def test_single_article_corpus_has_no_targets() -> None:
    corpus = [{"stem": PAGE.parent.name, "title": "Self", "tags": {"dora"}}]
    html = _page("<p>DORA already asked for more here.</p>")
    assert inject_contextual_links(PAGE, html, corpus, TAXONOMY, public=PUBLIC) == html
    assert inject_related_cluster(PAGE, html, corpus, public=PUBLIC) == html


def test_page_without_main_is_left_alone() -> None:
    html = '<html lang="en-GB"><body><p>DORA already asked for more here.</p></body></html>'
    assert inject_contextual_links(PAGE, html, CORPUS, TAXONOMY, public=PUBLIC) == html


def test_cluster_block_needs_a_close_tag() -> None:
    html = '<html lang="en-GB"><body><main><p>Body.</p>'
    assert inject_related_cluster(PAGE, html, CORPUS, public=PUBLIC) == html


def test_cluster_block_prefers_article_close_over_main_close() -> None:
    html = '<html lang="en-GB"><body><main><article><p>Body.</p></article></main></body></html>'
    out = inject_related_cluster(PAGE, html, CORPUS, public=PUBLIC)
    assert out.index("cluster-links") < out.index("</article>")


def test_locale_url_uses_the_slug_map(monkeypatch: pytest.MonkeyPatch) -> None:
    from postbuild_lib import internal_links as il

    monkeypatch.setattr(
        il, "_slug_maps", lambda _c: {"articles_en_to_lang": {"2026-08-03-cra-reporting": "fr-slug"}}
    )
    assert il._localised_url("2026-08-03-cra-reporting", "fr") == "/fr/fr-slug/"


def test_locale_url_falls_back_to_the_english_stem(monkeypatch: pytest.MonkeyPatch) -> None:
    from postbuild_lib import internal_links as il

    monkeypatch.setattr(il, "_slug_maps", lambda _c: {"articles_en_to_lang": {}})
    assert il._localised_url("2026-08-03-cra-reporting", "de") == "/de/2026-08-03-cra-reporting/"


def test_missing_slug_map_never_fails_the_build(monkeypatch: pytest.MonkeyPatch) -> None:
    from postbuild_lib import internal_links as il

    monkeypatch.setattr(
        il, "_slug_maps", lambda _c: (_ for _ in ()).throw(RuntimeError("no slugs"))
    )
    assert il._localised_url("2026-08-03-cra-reporting", "es") == "/es/2026-08-03-cra-reporting/"


def test_non_index_page_is_not_an_article() -> None:
    """/_csp/asset.html and friends must never be treated as posts."""
    page = PUBLIC / "2026-08-04-slug" / "amp.html"
    html = _page("<p>DORA already asked for more here.</p>")
    assert inject_contextual_links(page, html, CORPUS, TAXONOMY, public=PUBLIC) == html


def test_cluster_block_skips_locale_pages() -> None:
    page = PUBLIC / "fr" / PAGE.parent.name / "index.html"
    html = _page("<p>Corps.</p>", lang="fr-FR")
    assert inject_related_cluster(page, html, CORPUS, public=PUBLIC) == html
