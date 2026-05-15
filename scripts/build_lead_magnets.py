#!/usr/bin/env python3
"""Render every Markdown file under ``_data/lead-magnets/`` to a PDF
under ``public/resources/``.

Used to produce the free-PDF lead-magnets linked from landing pages
like ``/resources-pacs008-checklist/``. Source markdown lives in the
repo; the generated PDFs land in ``public/`` (then mirrored into
``docs/`` by build.sh's rsync) so the deployed site serves them from
e.g. ``/resources/pacs008-checklist.pdf``.

Requires ``pandoc`` and a LaTeX engine (``xelatex`` preferred) on
PATH. If either is missing, this script is a no-op — it prints what
it would have done and exits 0, so non-author developers can build
the site without a TeX install. CI does not require PDFs to be
regenerated on every build; PDFs are committed to ``docs/`` and only
refreshed when ``_data/lead-magnets/`` content changes.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

SRC = Path("_data/lead-magnets")
OUT = Path("public/resources")


def have_tooling() -> tuple[bool, str]:
    if not shutil.which("pandoc"):
        return False, "pandoc not on PATH — falling back to committed PDFs"
    if not (shutil.which("xelatex") or shutil.which("pdflatex")):
        return False, "no LaTeX engine on PATH — falling back to committed PDFs"
    return True, ""


def fallback_copy_from_docs(out: Path) -> int:
    """When pandoc/LaTeX isn't installed (CI runners, contributors without
    a TeX install), we still need the deployed PDF reachable from
    ``public/resources/`` so the internal-link audit passes. We canonicalise
    each PDF as a committed artefact under ``docs/resources/`` (deployed
    via GitHub Pages from main/docs anyway); the fallback just mirrors
    that into ``public/`` for the current build."""
    docs_dir = Path("docs/resources")
    if not docs_dir.is_dir():
        return 0
    out.mkdir(parents=True, exist_ok=True)
    n = 0
    for pdf in sorted(docs_dir.glob("*.pdf")):
        shutil.copy2(pdf, out / pdf.name)
        n += 1
    return n


def render(md: Path, out: Path) -> None:
    engine = "xelatex" if shutil.which("xelatex") else "pdflatex"
    cmd = [
        "pandoc",
        str(md),
        "-o", str(out),
        "--pdf-engine", engine,
        "-V", "geometry:margin=2cm",
        "-V", "fontsize=11pt",
        "-V", "linkcolor=blue",
        "-V", "urlcolor=blue",
        "-V", "colorlinks=true",
        "--toc",
        "--toc-depth=2",
        "--standalone",
    ]
    subprocess.run(cmd, check=True)


def main() -> int:
    ok, msg = have_tooling()
    if not ok:
        n = fallback_copy_from_docs(OUT)
        suffix = f" ({n} pre-built PDF(s) copied)" if n else " (no committed PDFs found)"
        print(f"build_lead_magnets: {msg}{suffix}")
        return 0
    if not SRC.is_dir():
        print("build_lead_magnets: _data/lead-magnets/ missing — nothing to do")
        return 0
    OUT.mkdir(parents=True, exist_ok=True)
    built: list[str] = []
    for md in sorted(SRC.glob("*.md")):
        pdf = OUT / f"{md.stem}.pdf"
        try:
            render(md, pdf)
        except subprocess.CalledProcessError as exc:
            print(f"build_lead_magnets: pandoc failed on {md.name} (exit {exc.returncode})", file=sys.stderr)
            return 1
        built.append(f"{md.name} → {pdf}")
    if built:
        print(f"build_lead_magnets: wrote {len(built)} PDF(s)")
        for line in built:
            print(f"  {line}")
    else:
        print("build_lead_magnets: no markdown sources found in _data/lead-magnets/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
