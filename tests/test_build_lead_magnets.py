"""Unit tests for scripts/build_lead_magnets.py.

Covers all four code paths through main():
  - no pandoc → fallback copy from docs/
  - no LaTeX → fallback copy from docs/
  - tooling present + no _data/lead-magnets/ → no-op
  - tooling present + sources → renders each, or surfaces pandoc errors
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import build_lead_magnets as blm

# ---------------------------------------------------------------------------
# have_tooling
# ---------------------------------------------------------------------------


def test_have_tooling_missing_pandoc(monkeypatch):
    monkeypatch.setattr(blm.shutil, "which", lambda _: None)
    ok, msg = blm.have_tooling()
    assert ok is False
    assert "pandoc" in msg


def test_have_tooling_missing_latex(monkeypatch):
    def which(name):
        return "/usr/bin/pandoc" if name == "pandoc" else None
    monkeypatch.setattr(blm.shutil, "which", which)
    ok, msg = blm.have_tooling()
    assert ok is False
    assert "LaTeX" in msg


def test_have_tooling_all_present_xelatex(monkeypatch):
    monkeypatch.setattr(
        blm.shutil, "which",
        lambda n: f"/usr/bin/{n}" if n in ("pandoc", "xelatex") else None,
    )
    ok, msg = blm.have_tooling()
    assert ok is True
    assert msg == ""


def test_have_tooling_falls_back_to_pdflatex(monkeypatch):
    monkeypatch.setattr(
        blm.shutil, "which",
        lambda n: f"/usr/bin/{n}" if n in ("pandoc", "pdflatex") else None,
    )
    ok, _ = blm.have_tooling()
    assert ok is True


# ---------------------------------------------------------------------------
# fallback_copy_from_docs
# ---------------------------------------------------------------------------


def test_fallback_copy_returns_zero_when_docs_missing(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert blm.fallback_copy_from_docs(tmp_path / "public" / "resources") == 0


def test_fallback_copy_mirrors_committed_pdfs(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    docs = tmp_path / "docs" / "resources"
    docs.mkdir(parents=True)
    (docs / "a.pdf").write_bytes(b"PDF-A")
    (docs / "b.pdf").write_bytes(b"PDF-B")
    out = tmp_path / "public" / "resources"
    n = blm.fallback_copy_from_docs(out)
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
        blm.shutil, "which",
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
        blm.subprocess, "run", lambda cmd, **kw: captured.update({"cmd": cmd}),
    )
    blm.render(src, pdf)
    assert "pdflatex" in captured["cmd"]


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------


def test_main_falls_back_when_tooling_missing(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(blm, "have_tooling", lambda: (False, "missing"))
    monkeypatch.setattr(blm, "fallback_copy_from_docs", lambda out: 3)
    rc = blm.main()
    assert rc == 0
    out = capsys.readouterr().out
    assert "3 pre-built PDF(s) copied" in out


def test_main_fallback_no_committed_pdfs(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(blm, "have_tooling", lambda: (False, "missing"))
    monkeypatch.setattr(blm, "fallback_copy_from_docs", lambda out: 0)
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
