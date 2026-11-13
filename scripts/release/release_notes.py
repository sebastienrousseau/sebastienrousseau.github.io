#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Release notes in the dotfiles format, from CHANGELOG.md and git.

Every release of this site follows the format of
https://github.com/sebastienrousseau/dotfiles/releases:

    title   sebastienrousseau.github.io X.Y.Z   (tag vX.Y.Z)

    ## Highlights ⭐️
    * **Lead**: first sentence.            (from the CHANGELOG section)

    ## What's Changed
    * `PR title` by @author in <PR url>    (first-parent merges since the
                                            previous tag)

    **Full Changelog**: <compare url>

Usage:
    release_notes.py v0.0.35                 # notes for an existing tag
    release_notes.py v0.0.35 --ref HEAD      # before the tag exists
    release_notes.py v0.0.35 --title         # print the release title only
    release_notes.py v0.0.29 --changelog-ref origin/main   # a backfill
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

REPO = "sebastienrousseau/sebastienrousseau.github.io"
NAME = "sebastienrousseau.github.io"
ROOT = Path(__file__).resolve().parents[2]
_TAG_RE = re.compile(r"^v(\d+)\.(\d+)\.(\d+)$")
_PR_RE = re.compile(r"\s*\(#(\d+)\)\s*$")
_MERGE_RE = re.compile(r"^Merge pull request #(\d+) from \S+$")
_BULLET_RE = re.compile(r"^- \*\*(?P<lead>.+?)\*\*(?P<rest>.*)$")
# CHANGELOG subsections whose bullets are release highlights.
_HIGHLIGHT_SECTIONS = ("Added", "Changed", "Fixed", "Security", "Removed", "Deprecated")


@dataclass(frozen=True)
class Change:
    """One merged pull request."""

    title: str
    number: int
    author: str


def version_of(tag: str) -> str:
    """'v0.0.35' -> '0.0.35'; anything else is an error."""
    m = _TAG_RE.match(tag)
    if not m:
        raise ValueError(f"not a release tag: {tag!r} (expected vX.Y.Z)")
    return tag[1:]


def title(tag: str) -> str:
    """The release title: 'sebastienrousseau.github.io 0.0.35'."""
    return f"{NAME} {version_of(tag)}"


def changelog_section(changelog: str, version: str) -> str:
    """The body of '## [version]' up to the next '## ['. Empty if absent."""
    m = re.search(
        rf"^## \[{re.escape(version)}\][^\n]*\n(.*?)(?=^## \[|\Z)", changelog, re.M | re.S
    )
    return m.group(1) if m else ""


def _first_sentence(text: str) -> str:
    text = text.strip()
    m = re.search(r"(?<=[.!?])\s+(?=[A-Z`(])", text)
    return text[: m.start()] if m else text


def _tail(rest: str) -> str:
    """What follows a bullet's bold lead, trimmed to its first sentence:
    ": text" after a colon, the continuation (", so ...") otherwise. A
    leading "(`path`)" naming the changed file is dropped."""
    rest = re.sub(r"^\s*\([^)]*\)", "", rest)
    if rest.lstrip().startswith(":"):
        text = _first_sentence(rest.lstrip()[1:])
        return f": {text}" if text else ""
    if not rest.strip():
        return ""
    # Keep the space between the bold lead and the words that follow it.
    text = _first_sentence(rest)
    return f" {text}" if rest[0].isspace() else text


def highlights(section: str) -> list[str]:
    """One '* **Lead**: first sentence' line per bold-led bullet in the
    Added / Changed / Fixed / Security / Removed / Deprecated subsections."""
    out: list[str] = []
    current = ""
    for line in section.splitlines():
        if line.startswith("### "):
            current = line[4:].strip()
            continue
        m = _BULLET_RE.match(line)
        if not m or not any(current.startswith(s) for s in _HIGHLIGHT_SECTIONS):
            continue
        out.append(f"* **{m.group('lead')}**{_tail(m.group('rest'))}")
    return out


def changes_from_subjects(subjects: list[str], author_of: Callable[[int], str]) -> list[Change]:
    """First-parent commit subjects ending '(#N)' -> Changes, oldest first."""
    found = []
    for subject in reversed(subjects):
        m = _PR_RE.search(subject)
        if m:
            number = int(m.group(1))
            found.append(Change(_PR_RE.sub("", subject), number, author_of(number)))
    return found


def pr_subjects(log: str) -> list[str]:
    """``git log --format=%s%x1f%b%x1e`` output -> one subject per commit.
    A merge commit's subject only says "Merge pull request #N from ...";
    GitHub writes the pull request's title as the first line of its body,
    so the subject becomes "<title> (#N)" like a squash merge's."""
    subjects = []
    for record in log.split("\x1e"):
        subject, _, body = record.strip("\n").partition("\x1f")
        if not subject:
            continue
        m = _MERGE_RE.match(subject)
        pr_title = next((ln.strip() for ln in body.splitlines() if ln.strip()), "")
        subjects.append(f"{pr_title or subject} (#{m.group(1)})" if m else subject)
    return subjects


def render(tag: str, prev: str | None, section: str, changes: list[Change]) -> str:
    """The release body."""
    lines = ["## Highlights ⭐️", ""]
    lines += highlights(section) or ["* Maintenance release; see What's Changed."]
    lines += ["", "## What's Changed", ""]
    lines += [
        f"* `{c.title}` by @{c.author} in https://github.com/{REPO}/pull/{c.number}"
        for c in changes
    ] or ["* No pull requests merged since the previous release."]
    compare = f"compare/{prev}...{tag}" if prev else f"commits/{tag}"
    lines += ["", f"**Full Changelog**: https://github.com/{REPO}/{compare}", ""]
    return "\n".join(lines)


def _git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout


def previous_tag(tag: str, ref: str) -> str | None:
    """The highest vX.Y.Z tag below ``tag`` reachable from ``ref``."""
    want = tuple(int(p) for p in version_of(tag).split("."))
    tags = [t for t in _git("tag", "--merged", ref).split() if _TAG_RE.match(t)]
    below = [t for t in tags if tuple(int(p) for p in t[1:].split(".")) < want]
    return max(below, key=lambda t: tuple(int(p) for p in t[1:].split(".")), default=None)


def _gh_author(number: int) -> str:
    out = subprocess.run(
        ["gh", "pr", "view", str(number), "-R", REPO, "--json", "author"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    return str(json.loads(out)["author"]["login"])


def build(
    tag: str,
    ref: str,
    author_of: Callable[[int], str] = _gh_author,
    changelog_ref: str | None = None,
) -> str:
    """Notes for ``tag``, whose commit is ``ref`` (the tag itself once it
    exists). The Highlights come from CHANGELOG.md at ``changelog_ref``
    (default ``ref``): a backfilled release reads today's changelog, which
    has the section its own tree did not."""
    prev = previous_tag(tag, ref)
    rng = f"{prev}..{ref}" if prev else ref
    subjects = pr_subjects(_git("log", "--first-parent", "--format=%s%x1f%b%x1e", rng))
    changelog = _git("show", f"{changelog_ref or ref}:CHANGELOG.md")
    section = changelog_section(changelog, version_of(tag))
    return render(tag, prev, section, changes_from_subjects(subjects, author_of))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Print release notes in the dotfiles format.")
    parser.add_argument("tag", help="release tag, vX.Y.Z")
    parser.add_argument("--ref", help="commit to describe (default: the tag)")
    parser.add_argument("--changelog-ref", help="read CHANGELOG.md here (default: --ref)")
    parser.add_argument("--title", action="store_true", help="print the release title only")
    args = parser.parse_args(argv)
    if args.title:
        print(title(args.tag))
        return 0
    sys.stdout.write(build(args.tag, args.ref or args.tag, changelog_ref=args.changelog_ref))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
