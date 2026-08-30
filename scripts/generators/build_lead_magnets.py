#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Render every Markdown file under ``_data/lead-magnets/`` to a PDF
under ``public/resources/``.

Used to produce the free-PDF lead-magnets linked from landing pages
like ``/resources-pacs008-checklist/``. Source markdown lives in the
repo; the generated PDFs land in ``public/resources/`` so the deployed
site serves them from e.g. ``/resources/pacs008-checklist.pdf``.

Requires a working ``pandoc`` and LaTeX engine (``xelatex``
preferred). If either is missing *or does not run*, the committed
copies under ``_data/lead-magnets/pdf/`` are copied into
``public/resources/`` instead, so non-author developers and CI
runners (no TeX install) still ship the PDFs. When the tooling *is*
usable, freshly rendered PDFs are mirrored back into
``_data/lead-magnets/pdf/`` so the committed store stays current.

"Missing" deliberately means unusable, not merely absent: a mise/asdf
shim resolves on PATH yet exits non-zero when no version is bound for
the directory, which used to slip past the fallback and fail the whole
build. See ``usable()``.

Reproducibility
---------------
pandoc renders through LaTeX, and the PDF a LaTeX engine emits is NOT a
pure function of its input: xelatex stamps a build timestamp inside a
*compressed* object stream, so two runs over identical markdown differ in
45,270 of 57,408 bytes. ``SOURCE_DATE_EPOCH`` pins the trailer ``/ID`` but
not that stream, and the one engine that does honour it (pdflatex) emits a
4x larger file — so neither is a fix.

Re-rendering unconditionally therefore made ``./build.sh`` non-idempotent
and left ``_data/lead-magnets/pdf/`` dirty after every build and every test
run. The byte-identical-rebuild gate in CI only stayed green because CI
runners have no LaTeX and take the fallback path above.

So the committed PDF is the canonical artefact, and rendering is driven by
*content*: each committed PDF carries a ``.sha256`` stamp over its source
markdown plus the pandoc option list. Unchanged source means the committed
PDF is reused verbatim, which is both deterministic and much faster. Change
the markdown or the options and the next build re-renders and re-stamps it.
``--force`` re-renders regardless.
"""

from __future__ import annotations

import sys as _sys  # path bootstrap — scripts reorg (scripts/lib/ on sys.path)
from pathlib import Path as _Path

_sys.path.insert(0, str(_Path(__file__).resolve().parents[1] / "lib"))

import hashlib
import shutil
import subprocess
import sys
from pathlib import Path

SRC = Path("_data/lead-magnets")
OUT = Path("public/resources")
COMMITTED = Path("_data/lead-magnets/pdf")

# Content-affecting pandoc arguments, kept in one place so the freshness
# stamp can hash them: changing a layout flag must invalidate every PDF.
# The engine is deliberately NOT part of the fingerprint — which LaTeX is
# installed is a property of the developer's machine, not of the repo, and
# the committed PDF is the canonical artefact either way.
PANDOC_OPTIONS = (
    "-V",
    "geometry:margin=2cm",
    "-V",
    "fontsize=11pt",
    "-V",
    "linkcolor=blue",
    "-V",
    "urlcolor=blue",
    "-V",
    "colorlinks=true",
    "--toc",
    "--toc-depth=2",
    "--standalone",
)


def usable(exe: str) -> bool:
    """True only if ``exe`` resolves on PATH *and* actually runs.

    Presence on PATH is not proof a tool works. Version managers (mise,
    asdf) install shims that resolve happily but exit non-zero when no
    version is bound for the current directory — ``shutil.which()``
    reports those as available, so the caller sails past the fallback
    and dies later on a real invocation. Probing ``--version`` is the
    cheapest way to tell a working binary from a dangling shim.
    """
    path = shutil.which(exe)
    if not path:
        return False
    try:
        proc = subprocess.run(
            [path, "--version"],
            capture_output=True,
            timeout=30,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        # Not executable, killed, or timed out — all mean "cannot use".
        return False
    return proc.returncode == 0


def have_tooling() -> tuple[bool, str]:
    if not usable("pandoc"):
        return False, "pandoc not usable — falling back to committed PDFs"
    if not (usable("xelatex") or usable("pdflatex")):
        return False, "no working LaTeX engine — falling back to committed PDFs"
    return True, ""


def fallback_copy_from_committed(out: Path) -> int:
    """When pandoc/LaTeX isn't installed (CI runners, contributors without
    a TeX install), we still need the deployed PDF reachable from
    ``public/resources/`` so the internal-link audit passes. Each PDF is
    canonicalised as a committed artefact under ``_data/lead-magnets/pdf/``;
    the fallback mirrors that into ``public/`` for the current build."""
    if not COMMITTED.is_dir():
        return 0
    out.mkdir(parents=True, exist_ok=True)
    n = 0
    for pdf in sorted(COMMITTED.glob("*.pdf")):
        shutil.copy2(pdf, out / pdf.name)
        n += 1
    return n


def render(md: Path, out: Path) -> None:
    engine = "xelatex" if shutil.which("xelatex") else "pdflatex"
    cmd = ["pandoc", str(md), "-o", str(out), "--pdf-engine", engine, *PANDOC_OPTIONS]
    subprocess.run(cmd, check=True)


def source_fingerprint(md: Path) -> str:
    """Digest of everything that determines the rendered PDF's content."""
    h = hashlib.sha256()
    h.update(md.read_bytes())
    h.update(b"\0")
    h.update("\0".join(PANDOC_OPTIONS).encode("utf-8"))
    return h.hexdigest()


def stamp_path(md: Path) -> Path:
    return COMMITTED / f"{md.stem}.pdf.sha256"


def committed_pdf(md: Path) -> Path:
    return COMMITTED / f"{md.stem}.pdf"


def is_current(md: Path) -> bool:
    """True when the committed PDF was rendered from exactly this input."""
    stamp = stamp_path(md)
    if not committed_pdf(md).is_file() or not stamp.is_file():
        return False
    return stamp.read_text(encoding="utf-8").strip() == source_fingerprint(md)


def write_stamp(md: Path) -> None:
    stamp_path(md).write_text(source_fingerprint(md) + "\n", encoding="utf-8")


def _render_all(
    sources: list[Path],
) -> list[tuple[Path, Path, subprocess.CalledProcessError | None]]:
    """Render each source to ``OUT`` in parallel, collecting failures.

    pandoc spawns a separate OS process — safe to fan out across a thread
    pool because the GIL is irrelevant once ``subprocess.run()`` has handed
    off to the child. On 5+ lead magnets this cuts wall time to ~one pandoc
    invocation.
    """
    from concurrent.futures import ThreadPoolExecutor

    def _render_one(md: Path) -> tuple[Path, Path, subprocess.CalledProcessError | None]:
        pdf = OUT / f"{md.stem}.pdf"
        try:
            render(md, pdf)
        except subprocess.CalledProcessError as exc:
            return md, pdf, exc
        return md, pdf, None

    with ThreadPoolExecutor(max_workers=min(4, len(sources))) as pool:
        return list(pool.map(_render_one, sources))


def _reuse_committed(md: Path) -> str:
    """Copy the committed PDF into ``OUT`` unchanged; return a log line."""
    pdf = OUT / f"{md.stem}.pdf"
    shutil.copy2(committed_pdf(md), pdf)
    return f"{md.name} → {pdf} (unchanged, reused committed PDF)"


def _nothing_to_render() -> int | None:
    """Exit code when this run cannot or need not render, else ``None``.

    Both early exits are successes, not errors: no usable tooling means the
    committed PDFs get mirrored instead, and an absent source directory means
    there is simply nothing to do.
    """
    ok, msg = have_tooling()
    if not ok:
        n = fallback_copy_from_committed(OUT)
        suffix = f" ({n} pre-built PDF(s) copied)" if n else " (no committed PDFs found)"
        print(f"build_lead_magnets: {msg}{suffix}")
        return 0
    if not SRC.is_dir():
        print("build_lead_magnets: _data/lead-magnets/ missing — nothing to do")
        return 0
    return None


def _partition(sources: list[Path], force: bool) -> tuple[list[Path], list[Path]]:
    """Split sources into (reuse committed, re-render) by stamp freshness."""
    if force:
        return [], list(sources)
    reuse = [md for md in sources if is_current(md)]
    return reuse, [md for md in sources if md not in reuse]


def _publish(
    results: list[tuple[Path, Path, subprocess.CalledProcessError | None]],
) -> tuple[list[str], bool]:
    """Mirror freshly rendered PDFs into the committed store and stamp them.

    Returns the log lines and whether every render succeeded. The stamp is
    written only after the PDF lands, so a failed render can never leave a
    stamp claiming an artefact is current.
    """
    lines: list[str] = []
    for md, pdf, exc in results:
        if exc is not None:
            print(
                f"build_lead_magnets: pandoc failed on {md.name} (exit {exc.returncode})",
                file=sys.stderr,
            )
            return lines, False
        if pdf.is_file():
            shutil.copy2(pdf, committed_pdf(md))
            write_stamp(md)
        lines.append(f"{md.name} → {pdf}")
    return lines, True


def main(argv: list[str] | None = None) -> int:
    rc = _nothing_to_render()
    if rc is not None:
        return rc
    OUT.mkdir(parents=True, exist_ok=True)
    sources = sorted(SRC.glob("*.md"))
    if not sources:
        print("build_lead_magnets: no markdown sources found in _data/lead-magnets/")
        return 0

    COMMITTED.mkdir(parents=True, exist_ok=True)
    force = "--force" in (sys.argv[1:] if argv is None else argv)
    reuse, to_render = _partition(sources, force)

    built = [_reuse_committed(md) for md in reuse]
    rendered, ok = _publish(_render_all(to_render)) if to_render else ([], True)
    if not ok:
        return 1
    built += rendered

    print(f"build_lead_magnets: wrote {len(built)} PDF(s)")
    for line in built:
        print(f"  {line}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
