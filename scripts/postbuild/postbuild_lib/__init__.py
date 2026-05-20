"""Postbuild support modules.

This package exists to keep ``scripts/postbuild.py`` to a tractable
size. Each submodule owns a logical slice of the postbuild pipeline:

* :mod:`postbuild_lib.github_stats` — repo-stats injection
* (more to come — feeds, sitemap, text_files, …)

The entry point ``scripts/postbuild.py`` imports the per-pass
functions it needs and orchestrates them in ``main()``. Module-level
state is kept inside each submodule; nothing here exports mutable
globals.
"""
from __future__ import annotations
