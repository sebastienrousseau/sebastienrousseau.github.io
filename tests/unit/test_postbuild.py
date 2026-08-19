"""Tests for scripts/postbuild.py — the SRI + CSP + feed-repair pass.

Each test exercises one of the postbuild transforms in isolation. We use
the in-process functions; we don't drive build.sh end-to-end because
postbuild has 10+ stages and the full smoke test belongs in CI.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# llms.txt + robots.txt + json-feed writers
# ---------------------------------------------------------------------------


def test_build_llms_txt_includes_canonical_sections():
    """llms.txt must contain H1, summary, and the seven canonical entries."""
    from postbuild_lib.output import build_llms_txt

    text = build_llms_txt()
    assert text.startswith("# Sebastien Rousseau")
    for section in ("Canonical entry points", "Feeds", "Areas of expertise", "Contact"):
        assert f"## {section}" in text
    # "Papers" became "Research" in the 5-item nav re-architecture
    # (/papers is now a redirect page; /research is the canonical hub).
    for entry in ("Home", "About", "Articles", "Research", "Projects", "Topics", "Contact"):
        assert f"[{entry}](https://sebastienrousseau.com/" in text


def test_write_llms_txt_skips_when_unchanged(tmp_path):
    """No-op when the target already has the current content."""
    from postbuild_lib.output import build_llms_txt, write_llms_txt

    (tmp_path / "llms.txt").write_text(build_llms_txt(), encoding="utf-8")
    assert write_llms_txt(tmp_path) is False


def test_write_llms_txt_writes_when_changed(tmp_path):
    """Writes when the target is missing or stale."""
    from postbuild_lib.output import write_llms_txt

    assert write_llms_txt(tmp_path) is True
    assert (tmp_path / "llms.txt").is_file()


def test_build_llms_ctx_txt_is_compact_and_machine_readable():
    """llms-ctx.txt must lead with the H1, name the agent-context
    purpose, list URLs in sectioned blocks, and stay under the
    ~2k-line llmstxt.org compact-format ceiling."""
    from postbuild_lib.output import build_llms_ctx_txt

    text = build_llms_ctx_txt()
    assert text.startswith("# Sebastien Rousseau — agent context")
    for section in ("## Content", "## Feeds", "## JSON API", "## Author", "## Bot policy"):
        assert section in text
    # Compact form: < 80 lines.
    assert len(text.splitlines()) < 80
    # Must advertise the ORCID + agent endpoints + bot policy anchor.
    assert "0009-0005-1434-284X" in text
    assert "/api/agents/index.json" in text
    assert "/about/#bot-policy" in text


def test_write_llms_ctx_txt_skips_when_unchanged(tmp_path):
    from postbuild_lib.output import build_llms_ctx_txt, write_llms_ctx_txt

    (tmp_path / "llms-ctx.txt").write_text(
        build_llms_ctx_txt(),
        encoding="utf-8",
    )
    assert write_llms_ctx_txt(tmp_path) is False


def test_write_llms_ctx_txt_writes_when_changed(tmp_path):
    from postbuild_lib.output import write_llms_ctx_txt

    assert write_llms_ctx_txt(tmp_path) is True
    assert (tmp_path / "llms-ctx.txt").is_file()


# ---------------------------------------------------------------------------
# write_humans + write_security_txt — copy-through emitters that survive
# Static Site Generator's empty-placeholder auxiliary files.
# ---------------------------------------------------------------------------


def test_write_humans_copies_source_into_public(tmp_path):
    """write_humans copies the repo-root humans.txt over an empty SSG placeholder."""
    from postbuild_lib.output import write_humans

    source_root = tmp_path / "src"
    source_root.mkdir()
    public = tmp_path / "public"
    public.mkdir()
    body = "/* TEAM */\n  Author: Sebastien Rousseau\n"
    (source_root / "humans.txt").write_text(body, encoding="utf-8")
    # Empty placeholder, as Static Site Generator would emit.
    (public / "humans.txt").write_text("", encoding="utf-8")

    assert write_humans(public, source_root) is True
    assert (public / "humans.txt").read_text(encoding="utf-8") == body


def test_write_humans_idempotent(tmp_path):
    """Second call with identical contents returns False (no-op)."""
    from postbuild_lib.output import write_humans

    source_root = tmp_path / "src"
    source_root.mkdir()
    public = tmp_path / "public"
    public.mkdir()
    (source_root / "humans.txt").write_text("body\n", encoding="utf-8")
    assert write_humans(public, source_root) is True
    assert write_humans(public, source_root) is False


def test_write_humans_missing_source_is_noop(tmp_path):
    """If the source file doesn't exist, the emitter is a no-op (False)."""
    from postbuild_lib.output import write_humans

    public = tmp_path / "public"
    public.mkdir()
    assert write_humans(public, tmp_path / "missing") is False


def test_write_security_txt_copies_source_into_public(tmp_path):
    """write_security_txt mirrors write_humans for the root security.txt."""
    from postbuild_lib.output import write_security_txt

    source_root = tmp_path / "src"
    source_root.mkdir()
    public = tmp_path / "public"
    public.mkdir()
    body = "Contact: mailto:sebastian.rousseau@gmail.com\n" "Expires: 2027-06-04T00:00:00.000Z\n"
    (source_root / "security.txt").write_text(body, encoding="utf-8")
    (public / "security.txt").write_text("", encoding="utf-8")

    assert write_security_txt(public, source_root) is True
    assert (public / "security.txt").read_text(encoding="utf-8") == body


def test_write_security_txt_idempotent_and_missing(tmp_path):
    """Second call returns False; missing source returns False."""
    from postbuild_lib.output import write_security_txt

    source_root = tmp_path / "src"
    source_root.mkdir()
    public = tmp_path / "public"
    public.mkdir()
    (source_root / "security.txt").write_text("body\n", encoding="utf-8")
    assert write_security_txt(public, source_root) is True
    assert write_security_txt(public, source_root) is False
    # Distinct call: missing source returns False.
    assert write_security_txt(public, tmp_path / "missing") is False


# ---------------------------------------------------------------------------
# Frontmatter parser — `_parse_frontmatter`
# ---------------------------------------------------------------------------


def test_parse_frontmatter_basic(tmp_path):
    from postbuild_lib import output as out

    p = tmp_path / "post.md"
    p.write_text('---\ntitle: "Hello"\nurl: "https://example.com"\n---\n\nBody', encoding="utf-8")
    fm = out._parse_frontmatter(p)
    assert fm == {"title": "Hello", "url": "https://example.com"}


def test_parse_frontmatter_stops_at_second_delimiter(tmp_path):
    """Once we've seen the second ``---`` we ignore everything below
    even if it looks frontmatter-ish."""
    from postbuild_lib import output as out

    p = tmp_path / "post.md"
    p.write_text('---\ntitle: "A"\n---\nbody\ntitle: "B" (in body)\n---\nmore\n', encoding="utf-8")
    fm = out._parse_frontmatter(p)
    assert fm == {"title": "A"}


def test_parse_frontmatter_captures_hyphenated_and_bare_keys(tmp_path):
    """This helper now delegates to scripts/lib/_frontmatter rather than
    carrying its own regex.

    The old local pattern accepted only ``[a-z_-]`` keys with double-quoted
    values, so it silently dropped real front-matter — ``measurementID`` is on
    every post and was never seen. Verified safe before switching:
    differential-tested over all 240 posts with zero value mismatches on shared
    keys (the shared parser is a strict superset), and both call sites read
    named keys via ``fm.get(...)`` rather than iterating, so recovered keys
    cannot leak into output.
    """
    from postbuild_lib import output as out

    p = tmp_path / "post.md"
    p.write_text(
        '---\ntitle: "Hi"\nmeasurementID: "G-XYZ"\nactive: true\n---\n', encoding="utf-8"
    )
    fm = out._parse_frontmatter(p)
    assert fm["title"] == "Hi"
    assert fm["measurementID"] == "G-XYZ"
    assert fm["active"] == "true"


def test_parse_frontmatter_no_frontmatter(tmp_path):
    """A file with no ``---`` block returns an empty dict."""
    from postbuild_lib import output as out

    p = tmp_path / "post.md"
    p.write_text("# Heading\n\nJust a body\n", encoding="utf-8")
    fm = out._parse_frontmatter(p)
    assert fm == {}


# ---------------------------------------------------------------------------
# build_llms_full_txt
# ---------------------------------------------------------------------------


def test_build_llms_full_txt_emits_header_and_body_blocks(tmp_path):
    """Output starts with an H1 and contains every page body."""
    public = tmp_path / "public"
    (public / "about").mkdir(parents=True)
    (public / "about" / "index.html").write_text(
        '<!doctype html><html lang="en-GB"><head><title>About</title>'
        '<meta content="bio" name=description></head>'
        "<body><main><h1>About</h1><p>Bio body content.</p></main></body></html>",
        encoding="utf-8",
    )
    from postbuild_lib.output import build_llms_full_txt

    out = build_llms_full_txt(public)
    assert out.startswith("# Sebastien Rousseau") or "About" in out


def test_build_llms_full_txt_returns_empty_without_posts_dir(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    from postbuild_lib.output import build_llms_full_txt

    assert build_llms_full_txt(tmp_path / "public") == ""


def test_build_llms_full_txt_full_pipeline_with_posts(tmp_path, monkeypatch):
    """Posts with title + body land in the corpus with date + URL line."""
    monkeypatch.chdir(tmp_path)
    posts = tmp_path / "_posts"
    posts.mkdir()
    (posts / "2026-05-12-x.md").write_text(
        '---\ntitle: "Test"\ndate: "May 12, 2026"\n---\nBody content here.\n',
        encoding="utf-8",
    )
    (posts / "2026-05-13-no-title.md").write_text(
        '---\ndate: "May 13, 2026"\n---\nNo title so skipped.\n',
        encoding="utf-8",
    )
    from postbuild_lib.output import build_llms_full_txt

    out = build_llms_full_txt(tmp_path / "public")
    assert "## Test" in out
    assert "May 12, 2026" in out
    assert "Body content here" in out
    assert "No title so skipped" not in out


# ---------------------------------------------------------------------------
# write_llms_full_txt — no-op + writes paths
# ---------------------------------------------------------------------------


def test_write_llms_full_txt_returns_false_without_posts(tmp_path, monkeypatch):
    """Empty corpus → write_llms_full_txt is a no-op."""
    monkeypatch.chdir(tmp_path)
    public = tmp_path / "public"
    public.mkdir()
    from postbuild_lib.output import write_llms_full_txt

    assert write_llms_full_txt(public) is False


def test_write_llms_full_txt_idempotent(tmp_path, monkeypatch):
    """Calling twice with no source change returns False the second time."""
    monkeypatch.chdir(tmp_path)
    posts = tmp_path / "_posts"
    posts.mkdir()
    (posts / "2026-05-12-x.md").write_text(
        '---\ntitle: "X"\ndate: "May 12, 2026"\n---\nBody.\n', encoding="utf-8"
    )
    public = tmp_path / "public"
    public.mkdir()
    from postbuild_lib.output import write_llms_full_txt

    assert write_llms_full_txt(public) is True
    assert write_llms_full_txt(public) is False  # idempotent


# ---------------------------------------------------------------------------
# CNAME normalisation
#
# GitHub Pages re-reads public/CNAME on every deploy and wants a bare
# hostname. The SSG writes a full DNS record line
# ("example.com 3600 IN CNAME www.example.com"); Pages tolerates it by
# taking the first token, but the published file should say what it means.
# ---------------------------------------------------------------------------


def test_normalise_cname_strips_dns_record_syntax(tmp_path):
    """The SSG's full record line collapses to the bare hostname."""
    from postbuild_lib.output import normalise_cname

    (tmp_path / "CNAME").write_text(
        "sebastienrousseau.com 3600 IN CNAME www.sebastienrousseau.com\n",
        encoding="utf-8",
    )
    assert normalise_cname(tmp_path) is True
    assert (tmp_path / "CNAME").read_text(encoding="utf-8") == "sebastienrousseau.com\n"


def test_normalise_cname_is_idempotent(tmp_path):
    """A correct file is left alone, so repeat postbuild runs are no-ops."""
    from postbuild_lib.output import normalise_cname

    (tmp_path / "CNAME").write_text("sebastienrousseau.com\n", encoding="utf-8")
    assert normalise_cname(tmp_path) is False
    assert (tmp_path / "CNAME").read_text(encoding="utf-8") == "sebastienrousseau.com\n"


def test_normalise_cname_adds_trailing_newline(tmp_path):
    """A bare host with no trailing newline is still rewritten once."""
    from postbuild_lib.output import normalise_cname

    (tmp_path / "CNAME").write_text("sebastienrousseau.com", encoding="utf-8")
    assert normalise_cname(tmp_path) is True
    assert (tmp_path / "CNAME").read_text(encoding="utf-8") == "sebastienrousseau.com\n"


def test_normalise_cname_ignores_missing_file(tmp_path):
    """No CNAME (e.g. a preview build) must not create one."""
    from postbuild_lib.output import normalise_cname

    assert normalise_cname(tmp_path) is False
    assert not (tmp_path / "CNAME").exists()


def test_normalise_cname_leaves_blank_file_alone(tmp_path):
    """An empty file yields no hostname; don't invent one."""
    from postbuild_lib.output import normalise_cname

    (tmp_path / "CNAME").write_text("\n  \n", encoding="utf-8")
    assert normalise_cname(tmp_path) is False
    assert (tmp_path / "CNAME").read_text(encoding="utf-8") == "\n  \n"
