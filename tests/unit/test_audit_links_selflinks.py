# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Absolute self-links are internal links.

Classifying them as external meant 113 of them could 404 while the internal
audit reported "0 broken" — and only a network run that is not part of CI
would ever have noticed. Coverage went from 10770 links to 13417 when they
were reclassified.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts" / "seo_and_audit"))

import audit_links


def test_an_absolute_self_link_is_internal():
    internal, external = audit_links.partition_hrefs(
        {"https://sebastienrousseau.com/2026-01-01-a-post/"}
    )
    assert internal == ["/2026-01-01-a-post/"]
    assert external == []


def test_a_third_party_link_stays_external():
    internal, external = audit_links.partition_hrefs({"https://example.test/x"})
    assert internal == []
    assert external == ["https://example.test/x"]


def test_root_relative_links_are_unchanged():
    internal, _ = audit_links.partition_hrefs({"/about/"})
    assert internal == ["/about/"]


def test_the_bare_origin_maps_to_root():
    internal, _ = audit_links.partition_hrefs({"https://sebastienrousseau.com"})
    assert internal == ["/"]


def test_http_and_https_self_links_both_count():
    internal, external = audit_links.partition_hrefs(
        {"http://sebastienrousseau.com/x/", "https://sebastienrousseau.com/x/"}
    )
    assert internal == ["/x/"]
    assert external == []


def test_localhost_is_ignored():
    _internal, external = audit_links.partition_hrefs({"http://127.0.0.1:8000/x"})
    assert external == []


def test_a_missing_target_is_reported_and_fails(tmp_path, capsys):
    broken = audit_links._audit_internal(["/definitely-missing/"], tmp_path)
    out = capsys.readouterr().out
    assert broken == ["/definitely-missing/"]
    assert "[missing] /definitely-missing/" in out
    assert "1 broken" in out
