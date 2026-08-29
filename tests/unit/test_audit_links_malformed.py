"""A malformed URL must be reported, not abort the audit.

http.client.InvalidURL derives from HTTPException, not from OSError or
ValueError, so it escaped check_external's handler. The external audit died
on the first malformed URL it met — a CDN path built from a front-matter
field containing a space — and every link after it went unchecked.
"""

from __future__ import annotations

import http.client
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts" / "seo_and_audit"))

import audit_links


def test_invalid_url_is_reported_not_raised():
    url, status = audit_links.check_external("https://example.test/a path/favicon.ico")
    assert url.endswith("favicon.ico")
    assert status == "ERR InvalidURL"


def test_invalid_url_is_not_an_oserror_or_valueerror():
    """The reason the old handler missed it — guard the assumption."""
    assert not issubclass(http.client.InvalidURL, OSError)
    assert not issubclass(http.client.InvalidURL, ValueError)
    assert issubclass(http.client.InvalidURL, http.client.HTTPException)


@pytest.mark.parametrize("bad", ["https://example.test/a\tb", "https://example.test/a\nb"])
def test_other_control_characters_are_reported_too(bad):
    _url, status = audit_links.check_external(bad)
    assert str(status).startswith("ERR ")
