"""Query strings survive href collection.

They used to be discarded along with the fragment. That is right for an
internal link — a static file is found by path — and wrong for an external
one, where the query often *is* the resource. Every EUR-Lex citation on the
site is /legal-content/EN/TXT/?uri=CELEX:…; stripping the query left a bare
path that legitimately 404s, so 11 working citations were reported broken.
False positives on that scale are how a real dead link goes unnoticed.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts" / "seo_and_audit"))

import audit_links


def _collect(tmp_path: Path, html: str) -> set[str]:
    (tmp_path / "index.html").write_text(html, encoding="utf-8")
    return audit_links.collect_hrefs(tmp_path)


def test_a_query_string_is_kept(tmp_path):
    url = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32022R2554"
    assert _collect(tmp_path, f'<a href="{url}">x</a>') == {url}


def test_a_fragment_is_dropped(tmp_path):
    got = _collect(tmp_path, '<a href="https://example.test/page#section">x</a>')
    assert got == {"https://example.test/page"}


def test_query_kept_and_fragment_dropped_together(tmp_path):
    got = _collect(tmp_path, '<a href="https://example.test/p?a=1&b=2#frag">x</a>')
    assert got == {"https://example.test/p?a=1&b=2"}


def test_unquoted_href_keeps_its_query(tmp_path):
    got = _collect(tmp_path, "<a href=https://example.test/p?a=1>x</a>")
    assert got == {"https://example.test/p?a=1"}


def test_non_navigational_schemes_are_ignored(tmp_path):
    got = _collect(tmp_path, '<a href="mailto:a@b.test">x</a><a href="tel:+1">y</a>')
    assert got == set()


def test_an_internal_link_is_resolved_without_its_query(tmp_path):
    """The file is found by path; the query must not break the lookup."""
    (tmp_path / "about").mkdir()
    (tmp_path / "about" / "index.html").write_text("x", encoding="utf-8")
    assert audit_links.check_internal("/about/?utm_source=x", tmp_path)
    assert not audit_links.check_internal("/missing/?utm_source=x", tmp_path)


def test_share_endpoints_are_not_audited():
    """They are actions, not citations: each page produces a distinct one and
    they 404 to a HEAD from a datacentre.

    Keeping the query string so a real citation resolves made every share
    button its own URL — 3675 of 3832 reported-broken links were one
    bsky.app share repeated once per page, which buried the real result.
    """
    for url in (
        "https://bsky.app/intent/compose?text=hi",
        "https://twitter.com/intent/tweet?url=x",
        "https://www.facebook.com/sharer/sharer.php?u=x",
        "https://www.linkedin.com/sharing/share-offsite/?url=x",
    ):
        assert audit_links.is_share_endpoint(url), url


def test_a_cited_resource_is_still_audited():
    for url in (
        "https://www.bis.org/publ/bcbs189.pdf",
        "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32022R2554",
        "https://bsky.app/profile/someone",
    ):
        assert not audit_links.is_share_endpoint(url), url
