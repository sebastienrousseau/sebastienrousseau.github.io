# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""postbuild_lib/content_decisions.py: noindex and merge decisions (B-3)."""

from __future__ import annotations

import json
from pathlib import Path

from postbuild_lib import content_decisions as cd

PAGE = (
    '<html><head><meta name="robots" content="index, follow">'
    '<link rel="canonical" href="https://sebastienrousseau.com/{slug}/">'
    '<link rel="alternate" hreflang="fr" href="https://sebastienrousseau.com/fr/x/"></head><body></body></html>'
)


def _site(tmp: Path) -> tuple[Path, Path]:
    public, i18n = tmp / "public", tmp / "i18n"
    for rel in ("2026-01-01-a", "2026-01-02-b", "fr/a-fr", "fr/b-fr", "de/a-de"):
        (public / rel).mkdir(parents=True)
        (public / rel / "index.html").write_text(PAGE.format(slug=rel), encoding="utf-8")
    for lang, arts in (
        ("fr", {"2026-01-01-a": "a-fr", "2026-01-02-b": "b-fr"}),
        ("de", {"2026-01-01-a": "a-de"}),
        ("it", {"2026-01-01-a": "a-it-not-built"}),
    ):
        (i18n / lang).mkdir(parents=True)
        (i18n / lang / "slugs.json").write_text(json.dumps({"articles": arts}), encoding="utf-8")
    return public, i18n


def _read(public: Path, rel: str) -> str:
    return (public / rel / "index.html").read_text(encoding="utf-8")


def test_noindex_covers_the_article_and_its_translations(tmp_path: Path) -> None:
    public, i18n = _site(tmp_path)
    assert cd.apply_content_decisions(public, {"/2026-01-01-a/": "noindex"}, i18n) == (3, 0)
    for rel in ("2026-01-01-a", "fr/a-fr", "de/a-de"):
        assert "noindex" in _read(public, rel)
    assert "noindex" not in _read(public, "2026-01-02-b")


def test_merge_redirects_each_page_to_the_target_in_its_locale(tmp_path: Path) -> None:
    public, i18n = _site(tmp_path)
    decisions = {"/2026-01-01-a/": "merge:/2026-01-02-b/", "/2026-01-02-b/": "keep"}
    assert cd.apply_content_decisions(public, decisions, i18n) == (0, 3)
    assert 'url=https://sebastienrousseau.com/2026-01-02-b/"' in _read(public, "2026-01-01-a")
    assert "url=https://sebastienrousseau.com/fr/b-fr/" in _read(public, "fr/a-fr")
    # No German translation of the target: the German page goes to the English target.
    assert "url=https://sebastienrousseau.com/2026-01-02-b/" in _read(public, "de/a-de")
    assert 'hreflang="fr"' not in _read(public, "2026-01-01-a")


def test_validate_reports_missing_pages_bad_targets_and_unknown_actions(tmp_path: Path) -> None:
    public, _ = _site(tmp_path)
    problems = cd.validate(
        {
            "/2026-01-01-a/": "merge:/2026-09-09-gone/",
            "/2026-09-09-none/": "noindex",
            "/2026-01-02-b/": "delete",
            "/fr/a-fr/": "merge:/2026-01-02-b/",
            "/fr/b-fr/": "keep",
        },
        public,
    )
    assert "merge target /2026-09-09-gone/ does not exist" in problems[0]
    assert "no such page" in problems[1]
    assert "unknown action 'delete'" in problems[2]
    assert "is itself delete" in problems[3]
    assert cd.validate({"/2026-01-01-a/": "noindex"}, public) == []


def test_load_reads_the_yaml_and_tolerates_absence(tmp_path: Path) -> None:
    f = tmp_path / "d.yml"
    f.write_text("/a/: noindex\n/b/: ' keep '\n", encoding="utf-8")
    assert cd.load(f) == {"/a/": "noindex", "/b/": "keep"}
    assert cd.load(tmp_path / "missing.yml") == {}
    (tmp_path / "empty.yml").write_text("{}\n", encoding="utf-8")
    assert cd.load(tmp_path / "empty.yml") == {}
    assert cd.load() == {}  # nothing decided yet
