"""Unit tests for scripts/build_lead_magnets.py.

Covers tool detection and all four code paths through main():
  - pandoc missing *or unusable* → fallback copy from _data/lead-magnets/pdf/
  - LaTeX missing *or unusable* → fallback copy from _data/lead-magnets/pdf/
  - tooling usable + no _data/lead-magnets/ → no-op
  - tooling usable + sources → renders each, or surfaces pandoc errors

Plus the freshness stamp that makes the build reproducible. LaTeX PDFs are
not a pure function of their input (see the module docstring), so an
unconditional re-render made ./build.sh non-idempotent. The stamp tests below
pin both directions: a matching stamp must reuse the committed PDF verbatim,
and ANY change to the source or the pandoc options must re-render. A bug in
either direction is silent — one leaves the tree permanently dirty, the other
ships a stale PDF forever.

"Unusable" is the interesting case: a mise/asdf shim resolves on PATH but
exits non-zero when no version is bound for the directory. Detection must
probe the binary, not just locate it, or the fallback never fires and the
whole build dies at the render step.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import build_lead_magnets as blm

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------


class _Proc:
    """Stand-in for subprocess.CompletedProcess — only returncode is read."""

    def __init__(self, returncode: int) -> None:
        self.returncode = returncode


def _stub_tools(monkeypatch, *, on_path, probe_rc=None, raises=None):
    """Pretend ``on_path`` resolve on PATH and answer ``--version`` probes.

    ``probe_rc`` maps executable name → exit status (default 0). ``raises``
    maps executable name → exception instance to raise instead.
    """
    probe_rc = probe_rc or {}
    raises = raises or {}
    monkeypatch.setattr(blm.shutil, "which", lambda n: f"/usr/bin/{n}" if n in on_path else None)

    def fake_run(cmd, **kwargs):
        exe = Path(cmd[0]).name
        assert cmd[1] == "--version", f"probe must use --version, got {cmd!r}"
        if exe in raises:
            raise raises[exe]
        return _Proc(probe_rc.get(exe, 0))

    monkeypatch.setattr(blm.subprocess, "run", fake_run)


# ---------------------------------------------------------------------------
# usable
# ---------------------------------------------------------------------------


def test_usable_false_when_not_on_path(monkeypatch):
    monkeypatch.setattr(blm.shutil, "which", lambda _: None)

    def explode(*a, **kw):  # pragma: no cover - must never run
        raise AssertionError("must not probe a tool that is not on PATH")

    monkeypatch.setattr(blm.subprocess, "run", explode)
    assert blm.usable("pandoc") is False


def test_usable_true_when_probe_succeeds(monkeypatch):
    _stub_tools(monkeypatch, on_path={"pandoc"}, probe_rc={"pandoc": 0})
    assert blm.usable("pandoc") is True


def test_usable_false_when_shim_exits_nonzero(monkeypatch):
    """The mise/asdf regression: on PATH, but no version bound for the dir."""
    _stub_tools(monkeypatch, on_path={"pandoc"}, probe_rc={"pandoc": 1})
    assert blm.usable("pandoc") is False


def test_usable_false_when_probe_raises_oserror(monkeypatch):
    _stub_tools(
        monkeypatch,
        on_path={"pandoc"},
        raises={"pandoc": FileNotFoundError("vanished between which() and run()")},
    )
    assert blm.usable("pandoc") is False


def test_usable_false_when_probe_times_out(monkeypatch):
    _stub_tools(
        monkeypatch,
        on_path={"pandoc"},
        raises={"pandoc": subprocess.TimeoutExpired(["pandoc"], 30)},
    )
    assert blm.usable("pandoc") is False


def test_usable_probes_resolved_path_not_bare_name(monkeypatch):
    seen = {}
    monkeypatch.setattr(blm.shutil, "which", lambda n: f"/opt/custom/{n}")

    def fake_run(cmd, **kwargs):
        seen["cmd"] = cmd
        seen["kwargs"] = kwargs
        return _Proc(0)

    monkeypatch.setattr(blm.subprocess, "run", fake_run)
    assert blm.usable("pandoc") is True
    assert seen["cmd"] == ["/opt/custom/pandoc", "--version"]
    # A hung shim must not wedge the build, and a noisy one must not
    # pollute build output.
    assert seen["kwargs"]["timeout"] == 30
    assert seen["kwargs"]["capture_output"] is True
    assert seen["kwargs"]["check"] is False


# ---------------------------------------------------------------------------
# have_tooling
# ---------------------------------------------------------------------------


def test_have_tooling_missing_pandoc(monkeypatch):
    _stub_tools(monkeypatch, on_path=set())
    ok, msg = blm.have_tooling()
    assert ok is False
    assert "pandoc" in msg


def test_have_tooling_pandoc_on_path_but_broken(monkeypatch):
    """Regression: a dangling shim used to pass have_tooling() and then
    fail the build at render time with a non-zero exit."""
    _stub_tools(monkeypatch, on_path={"pandoc", "xelatex"}, probe_rc={"pandoc": 1})
    ok, msg = blm.have_tooling()
    assert ok is False
    assert "pandoc" in msg


def test_have_tooling_missing_latex(monkeypatch):
    _stub_tools(monkeypatch, on_path={"pandoc"})
    ok, msg = blm.have_tooling()
    assert ok is False
    assert "LaTeX" in msg


def test_have_tooling_latex_on_path_but_broken(monkeypatch):
    _stub_tools(
        monkeypatch,
        on_path={"pandoc", "xelatex", "pdflatex"},
        probe_rc={"xelatex": 1, "pdflatex": 1},
    )
    ok, msg = blm.have_tooling()
    assert ok is False
    assert "LaTeX" in msg


def test_have_tooling_all_present_xelatex(monkeypatch):
    _stub_tools(monkeypatch, on_path={"pandoc", "xelatex"})
    ok, msg = blm.have_tooling()
    assert ok is True
    assert msg == ""


def test_have_tooling_falls_back_to_pdflatex(monkeypatch):
    _stub_tools(monkeypatch, on_path={"pandoc", "pdflatex"})
    ok, _ = blm.have_tooling()
    assert ok is True


def test_have_tooling_uses_pdflatex_when_xelatex_shim_broken(monkeypatch):
    _stub_tools(
        monkeypatch,
        on_path={"pandoc", "xelatex", "pdflatex"},
        probe_rc={"xelatex": 1},
    )
    ok, msg = blm.have_tooling()
    assert ok is True
    assert msg == ""


# ---------------------------------------------------------------------------
# fallback_copy_from_committed
# ---------------------------------------------------------------------------


def test_fallback_copy_returns_zero_when_committed_missing(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert blm.fallback_copy_from_committed(tmp_path / "public" / "resources") == 0


def test_fallback_copy_mirrors_committed_pdfs(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    committed = tmp_path / "_data" / "lead-magnets" / "pdf"
    committed.mkdir(parents=True)
    (committed / "a.pdf").write_bytes(b"PDF-A")
    (committed / "b.pdf").write_bytes(b"PDF-B")
    out = tmp_path / "public" / "resources"
    n = blm.fallback_copy_from_committed(out)
    assert n == 2
    assert (out / "a.pdf").read_bytes() == b"PDF-A"
    assert (out / "b.pdf").read_bytes() == b"PDF-B"


# ---------------------------------------------------------------------------
# render
# ---------------------------------------------------------------------------


def test_render_invokes_pandoc_with_xelatex(tmp_path, monkeypatch):
    src = tmp_path / "src.md"
    src.write_text("# title\n", encoding="utf-8")
    pdf = tmp_path / "out.pdf"

    captured = {}
    monkeypatch.setattr(
        blm.shutil,
        "which",
        lambda n: f"/usr/bin/{n}" if n == "xelatex" else None,
    )

    def fake_run(cmd, **kwargs):
        captured["cmd"] = cmd

    monkeypatch.setattr(blm.subprocess, "run", fake_run)
    blm.render(src, pdf)
    assert captured["cmd"][0] == "pandoc"
    assert "xelatex" in captured["cmd"]
    assert "--toc" in captured["cmd"]


def test_render_falls_back_to_pdflatex_when_no_xelatex(tmp_path, monkeypatch):
    src = tmp_path / "src.md"
    src.write_text("# title\n", encoding="utf-8")
    pdf = tmp_path / "out.pdf"
    monkeypatch.setattr(blm.shutil, "which", lambda _: None)
    captured = {}
    monkeypatch.setattr(
        blm.subprocess,
        "run",
        lambda cmd, **kw: captured.update({"cmd": cmd}),
    )
    blm.render(src, pdf)
    assert "pdflatex" in captured["cmd"]


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------


def test_main_falls_back_when_tooling_missing(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(blm, "have_tooling", lambda: (False, "missing"))
    monkeypatch.setattr(blm, "fallback_copy_from_committed", lambda out: 3)
    rc = blm.main()
    assert rc == 0
    out = capsys.readouterr().out
    assert "3 pre-built PDF(s) copied" in out


def test_main_fallback_no_committed_pdfs(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(blm, "have_tooling", lambda: (False, "missing"))
    monkeypatch.setattr(blm, "fallback_copy_from_committed", lambda out: 0)
    rc = blm.main()
    assert rc == 0
    assert "no committed PDFs found" in capsys.readouterr().out


def test_main_no_op_when_src_missing(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(blm, "have_tooling", lambda: (True, ""))
    monkeypatch.setattr(blm, "SRC", tmp_path / "missing")
    rc = blm.main()
    assert rc == 0
    assert "_data/lead-magnets/ missing" in capsys.readouterr().out


def test_main_renders_each_markdown(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    src = tmp_path / "_data" / "lead-magnets"
    src.mkdir(parents=True)
    (src / "a.md").write_text("# A\n", encoding="utf-8")
    (src / "b.md").write_text("# B\n", encoding="utf-8")
    out = tmp_path / "public" / "resources"
    monkeypatch.setattr(blm, "have_tooling", lambda: (True, ""))
    monkeypatch.setattr(blm, "SRC", src)
    monkeypatch.setattr(blm, "OUT", out)
    rendered = []
    monkeypatch.setattr(blm, "render", lambda md, pdf: rendered.append((md.name, pdf.name)))
    rc = blm.main()
    assert rc == 0
    assert ("a.md", "a.pdf") in rendered
    assert ("b.md", "b.pdf") in rendered
    msg = capsys.readouterr().out
    assert "wrote 2 PDF(s)" in msg


def test_main_mirrors_rendered_pdfs_to_committed_store(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    src = tmp_path / "_data" / "lead-magnets"
    src.mkdir(parents=True)
    (src / "a.md").write_text("# A\n", encoding="utf-8")
    out = tmp_path / "public" / "resources"
    committed = tmp_path / "_data" / "lead-magnets" / "pdf"
    monkeypatch.setattr(blm, "have_tooling", lambda: (True, ""))
    monkeypatch.setattr(blm, "SRC", src)
    monkeypatch.setattr(blm, "OUT", out)
    monkeypatch.setattr(blm, "COMMITTED", committed)
    monkeypatch.setattr(blm, "render", lambda md, pdf: pdf.write_bytes(b"PDF-A"))
    rc = blm.main()
    assert rc == 0
    assert (committed / "a.pdf").read_bytes() == b"PDF-A"


def test_main_returns_one_on_pandoc_failure(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    src = tmp_path / "_data" / "lead-magnets"
    src.mkdir(parents=True)
    (src / "a.md").write_text("# A\n", encoding="utf-8")
    out = tmp_path / "public" / "resources"
    monkeypatch.setattr(blm, "have_tooling", lambda: (True, ""))
    monkeypatch.setattr(blm, "SRC", src)
    monkeypatch.setattr(blm, "OUT", out)

    def boom(md, pdf):
        raise subprocess.CalledProcessError(1, ["pandoc"])

    monkeypatch.setattr(blm, "render", boom)
    rc = blm.main()
    assert rc == 1
    assert "pandoc failed" in capsys.readouterr().err


def test_main_reports_no_sources_when_dir_empty(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    src = tmp_path / "_data" / "lead-magnets"
    src.mkdir(parents=True)
    out = tmp_path / "public" / "resources"
    monkeypatch.setattr(blm, "have_tooling", lambda: (True, ""))
    monkeypatch.setattr(blm, "SRC", src)
    monkeypatch.setattr(blm, "OUT", out)
    rc = blm.main()
    assert rc == 0
    assert "no markdown sources found" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# freshness stamp / reproducibility
# ---------------------------------------------------------------------------


def _stamped(tmp_path, monkeypatch, body="# A\n"):
    """A source tree whose committed PDF is stamped as current."""
    monkeypatch.chdir(tmp_path)
    src = tmp_path / "_data" / "lead-magnets"
    src.mkdir(parents=True)
    md = src / "a.md"
    md.write_text(body, encoding="utf-8")
    committed = src / "pdf"
    committed.mkdir()
    monkeypatch.setattr(blm, "SRC", src)
    monkeypatch.setattr(blm, "OUT", tmp_path / "public" / "resources")
    monkeypatch.setattr(blm, "COMMITTED", committed)
    (committed / "a.pdf").write_bytes(b"COMMITTED-PDF")
    blm.write_stamp(md)
    return md, committed


def test_fingerprint_changes_with_source(tmp_path):
    a = tmp_path / "a.md"
    a.write_text("one", encoding="utf-8")
    first = blm.source_fingerprint(a)
    a.write_text("two", encoding="utf-8")
    assert blm.source_fingerprint(a) != first


def test_fingerprint_changes_with_pandoc_options(tmp_path, monkeypatch):
    a = tmp_path / "a.md"
    a.write_text("one", encoding="utf-8")
    first = blm.source_fingerprint(a)
    monkeypatch.setattr(blm, "PANDOC_OPTIONS", (*blm.PANDOC_OPTIONS, "--number-sections"))
    assert blm.source_fingerprint(a) != first


def test_fingerprint_is_stable_for_identical_input(tmp_path):
    a = tmp_path / "a.md"
    a.write_text("one", encoding="utf-8")
    assert blm.source_fingerprint(a) == blm.source_fingerprint(a)


def test_is_current_true_when_stamp_matches(tmp_path, monkeypatch):
    md, _ = _stamped(tmp_path, monkeypatch)
    assert blm.is_current(md) is True


def test_is_current_false_when_source_changed(tmp_path, monkeypatch):
    md, _ = _stamped(tmp_path, monkeypatch)
    md.write_text("# A changed\n", encoding="utf-8")
    assert blm.is_current(md) is False


def test_is_current_false_without_stamp(tmp_path, monkeypatch):
    md, _committed = _stamped(tmp_path, monkeypatch)
    blm.stamp_path(md).unlink()
    assert blm.is_current(md) is False


def test_is_current_false_without_committed_pdf(tmp_path, monkeypatch):
    md, committed = _stamped(tmp_path, monkeypatch)
    (committed / "a.pdf").unlink()
    assert blm.is_current(md) is False


def test_main_reuses_committed_pdf_without_rendering(tmp_path, monkeypatch, capsys):
    _stamped(tmp_path, monkeypatch)
    monkeypatch.setattr(blm, "have_tooling", lambda: (True, ""))

    def explode(*a, **kw):  # pragma: no cover - must never run
        raise AssertionError("must not render when the stamp is current")

    monkeypatch.setattr(blm, "render", explode)
    assert blm.main([]) == 0
    out = capsys.readouterr().out
    assert "reused committed PDF" in out
    assert (blm.OUT / "a.pdf").read_bytes() == b"COMMITTED-PDF"


def test_main_rerenders_when_source_changed(tmp_path, monkeypatch):
    md, _ = _stamped(tmp_path, monkeypatch)
    md.write_text("# A changed\n", encoding="utf-8")
    monkeypatch.setattr(blm, "have_tooling", lambda: (True, ""))
    monkeypatch.setattr(blm, "render", lambda m, pdf: pdf.write_bytes(b"FRESH"))
    assert blm.main([]) == 0
    assert (blm.OUT / "a.pdf").read_bytes() == b"FRESH"
    assert blm.is_current(md) is True


def test_main_force_rerenders_a_current_pdf(tmp_path, monkeypatch):
    _stamped(tmp_path, monkeypatch)
    monkeypatch.setattr(blm, "have_tooling", lambda: (True, ""))
    monkeypatch.setattr(blm, "render", lambda m, pdf: pdf.write_bytes(b"FORCED"))
    assert blm.main(["--force"]) == 0
    assert (blm.OUT / "a.pdf").read_bytes() == b"FORCED"


def test_failed_render_leaves_no_stamp(tmp_path, monkeypatch, capsys):
    """A stamp written despite a failed render would mark a stale PDF current
    forever — the one failure mode this scheme must never have."""
    monkeypatch.chdir(tmp_path)
    src = tmp_path / "_data" / "lead-magnets"
    src.mkdir(parents=True)
    md = src / "a.md"
    md.write_text("# A\n", encoding="utf-8")
    monkeypatch.setattr(blm, "SRC", src)
    monkeypatch.setattr(blm, "OUT", tmp_path / "public" / "resources")
    monkeypatch.setattr(blm, "COMMITTED", src / "pdf")
    monkeypatch.setattr(blm, "have_tooling", lambda: (True, ""))

    def boom(m, pdf):
        raise subprocess.CalledProcessError(1, ["pandoc"])

    monkeypatch.setattr(blm, "render", boom)
    assert blm.main([]) == 1
    assert not blm.stamp_path(md).exists()
    assert "pandoc failed" in capsys.readouterr().err


def test_repeated_main_is_idempotent(tmp_path, monkeypatch):
    """The regression this whole scheme exists to prevent: build twice, get
    byte-identical artefacts. `render` deliberately emits different bytes on
    every call, standing in for LaTeX's non-determinism."""
    monkeypatch.chdir(tmp_path)
    src = tmp_path / "_data" / "lead-magnets"
    src.mkdir(parents=True)
    (src / "a.md").write_text("# A\n", encoding="utf-8")
    committed = src / "pdf"
    monkeypatch.setattr(blm, "SRC", src)
    monkeypatch.setattr(blm, "OUT", tmp_path / "public" / "resources")
    monkeypatch.setattr(blm, "COMMITTED", committed)
    monkeypatch.setattr(blm, "have_tooling", lambda: (True, ""))

    calls = {"n": 0}

    def unstable_render(m, pdf):
        calls["n"] += 1
        pdf.write_bytes(b"PDF-run-%d" % calls["n"])

    monkeypatch.setattr(blm, "render", unstable_render)

    assert blm.main([]) == 0
    first = (committed / "a.pdf").read_bytes()
    assert calls["n"] == 1, "first build must render"

    for _ in range(3):
        assert blm.main([]) == 0
    assert calls["n"] == 1, "later builds must not render again"
    assert (committed / "a.pdf").read_bytes() == first
    assert (blm.OUT / "a.pdf").read_bytes() == first


def test_render_uses_the_shared_option_tuple(tmp_path, monkeypatch):
    """render() and the fingerprint must read the SAME options, or a layout
    change could ship without invalidating a single stamp."""
    src = tmp_path / "src.md"
    src.write_text("# t\n", encoding="utf-8")
    captured = {}
    monkeypatch.setattr(blm.shutil, "which", lambda n: f"/usr/bin/{n}")
    monkeypatch.setattr(blm.subprocess, "run", lambda cmd, **kw: captured.update({"cmd": cmd}))
    blm.render(src, tmp_path / "out.pdf")
    for opt in blm.PANDOC_OPTIONS:
        assert opt in captured["cmd"]
