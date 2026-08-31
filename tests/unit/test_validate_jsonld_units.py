# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Unit-level checks for the JSON-LD / feed validator's own predicates.

validate_jsonld runs as a build gate over the whole site, and
test_builder_main_smoke already runs its main(). What that does not do is
exercise each predicate against the inputs it exists to reject — so a check
that quietly stopped detecting would still report success on a clean site.

Each test here feeds a predicate the exact shape it was written to catch. The
CSP one matters most: it is the gate protecting hash-pinned inline scripts,
and if it stopped noticing 'unsafe-inline' the site would silently lose that
guarantee while the build stayed green.
"""

from __future__ import annotations

import validate_jsonld as vj

# ---------------------------------------------------------------------------
# meta CSP
# ---------------------------------------------------------------------------


def _csp(value: str) -> str:
    return f'<meta http-equiv="Content-Security-Policy" content="{value}">'


def test_csp_missing_is_an_error() -> None:
    errors = vj.validate_meta_csp("<html><head></head></html>")
    assert len(errors) == 1
    assert "missing" in errors[0]


def test_csp_without_script_src_is_an_error() -> None:
    errors = vj.validate_meta_csp(_csp("default-src 'self'"))
    assert any("no script-src" in e for e in errors)


def test_csp_with_unsafe_inline_is_an_error() -> None:
    """unsafe-inline defeats the entire point of hash pinning."""
    errors = vj.validate_meta_csp(_csp("script-src 'self' 'unsafe-inline' 'sha256-abc'"))
    assert any("unsafe-inline" in e for e in errors)


def test_csp_without_a_hash_token_is_an_error() -> None:
    errors = vj.validate_meta_csp(_csp("script-src 'self'"))
    assert any("sha256" in e for e in errors)


def test_csp_hash_pinned_without_unsafe_inline_is_clean() -> None:
    assert vj.validate_meta_csp(_csp("script-src 'self' 'sha256-abc123'")) == []


def test_csp_extraction_tolerates_reversed_attribute_order() -> None:
    """A minifier may emit content before http-equiv."""
    html = "<meta content=\"script-src 'self' 'sha256-x'\" http-equiv=\"Content-Security-Policy\">"
    assert vj._extract_meta_csp(html) is not None


def test_csp_extraction_returns_none_when_absent() -> None:
    assert vj._extract_meta_csp("<html></html>") is None


# ---------------------------------------------------------------------------
# Node traversal
# ---------------------------------------------------------------------------


def test_iter_typed_nodes_finds_a_top_level_node() -> None:
    found = list(vj.iter_typed_nodes({"@type": "Article", "name": "x"}))
    assert found[0][0] == "Article"


def test_iter_typed_nodes_recurses_into_a_graph() -> None:
    doc = {"@graph": [{"@type": "Article"}, {"@type": "Person"}]}
    assert {t for t, _ in vj.iter_typed_nodes(doc)} == {"Article", "Person"}


def test_iter_typed_nodes_handles_a_list_valued_type() -> None:
    """@type may be a list; every member is a node type."""
    types = {t for t, _ in vj.iter_typed_nodes({"@type": ["Article", "TechArticle"]})}
    assert types == {"Article", "TechArticle"}


def test_iter_typed_nodes_recurses_into_nested_objects() -> None:
    doc = {"@type": "Article", "author": {"@type": "Person", "name": "A"}}
    assert {t for t, _ in vj.iter_typed_nodes(doc)} == {"Article", "Person"}


def test_iter_typed_nodes_ignores_a_non_string_type() -> None:
    assert list(vj.iter_typed_nodes({"@type": 42})) == []


def test_iter_typed_nodes_on_a_bare_scalar() -> None:
    assert list(vj.iter_typed_nodes("just a string")) == []


# ---------------------------------------------------------------------------
# Template leakage
# ---------------------------------------------------------------------------


def test_template_leak_flags_an_unresolved_token() -> None:
    errors: list[str] = []
    vj._check_template_leak('{"name": "{{title}}"}', 0, errors)
    assert errors and "unresolved template token" in errors[0]


def test_template_leak_is_silent_on_resolved_output() -> None:
    errors: list[str] = []
    vj._check_template_leak('{"name": "A real title"}', 0, errors)
    assert errors == []


def test_template_leak_flags_an_unbalanced_closing_brace() -> None:
    errors: list[str] = []
    vj._check_template_leak('"name": "x"}}', 0, errors)
    assert errors


# ---------------------------------------------------------------------------
# Required properties
# ---------------------------------------------------------------------------


def test_required_properties_missing_is_reported() -> None:
    type_str = next(iter(vj.REQUIRED))
    errors: list[str] = []
    vj._check_node_required(type_str, {"@type": type_str}, errors)
    assert errors and "missing required" in errors[0]


def test_required_properties_present_is_clean() -> None:
    type_str, required = next(iter(vj.REQUIRED.items()))
    node = {"@type": type_str} | dict.fromkeys(required, "value")
    errors: list[str] = []
    vj._check_node_required(type_str, node, errors)
    assert errors == []


def test_required_properties_accepts_an_at_prefixed_key() -> None:
    """`id` and `@id` are the same property for this purpose."""
    type_str, required = next(iter(vj.REQUIRED.items()))
    node = {"@type": type_str} | {f"@{k}": "v" for k in required}
    errors: list[str] = []
    vj._check_node_required(type_str, node, errors)
    assert errors == []


def test_unknown_type_has_no_requirements() -> None:
    errors: list[str] = []
    vj._check_node_required("NotASchemaType", {}, errors)
    assert errors == []


# ---------------------------------------------------------------------------
# Empty URL fields — the Lucy-post regression
# ---------------------------------------------------------------------------


def test_empty_url_string_is_an_error() -> None:
    errors: list[str] = []
    vj._check_node_empty_urls("Article", {"url": ""}, errors)
    assert errors and "empty string" in errors[0]


def test_whitespace_only_url_is_an_error() -> None:
    errors: list[str] = []
    vj._check_node_empty_urls("Article", {"image": "   "}, errors)
    assert errors


def test_empty_string_inside_a_url_list_is_an_error() -> None:
    errors: list[str] = []
    vj._check_node_empty_urls("Article", {"sameAs": ["https://a", ""]}, errors)
    assert errors and "[]" in errors[0]


def test_populated_url_fields_are_clean() -> None:
    errors: list[str] = []
    vj._check_node_empty_urls("Article", {"url": "https://a", "sameAs": ["https://b"]}, errors)
    assert errors == []


def test_absent_url_fields_are_clean() -> None:
    errors: list[str] = []
    vj._check_node_empty_urls("Article", {"name": "x"}, errors)
    assert errors == []


# ---------------------------------------------------------------------------
# URL taint and SEO shape
# ---------------------------------------------------------------------------


def test_localhost_url_is_tainted() -> None:
    errors: list[str] = []
    vj._check_url_taint("canonical", "http://localhost:8000/a/", errors)
    assert errors and "dev artefact" in errors[0]


def test_loopback_ip_is_tainted() -> None:
    errors: list[str] = []
    vj._check_url_taint("canonical", "http://127.0.0.1/a/", errors)
    assert errors


def test_ssg_meta_path_is_tainted() -> None:
    errors: list[str] = []
    vj._check_url_taint("canonical", "https://sebastienrousseau.com/.meta/x", errors)
    assert errors


def test_a_clean_url_is_not_tainted() -> None:
    errors: list[str] = []
    vj._check_url_taint("canonical", "https://sebastienrousseau.com/a/", errors)
    assert errors == []


def test_taint_check_ignores_an_absent_url() -> None:
    errors: list[str] = []
    vj._check_url_taint("canonical", None, errors)
    vj._check_url_taint("canonical", "", errors)
    assert errors == []


def test_http_url_is_a_seo_warning() -> None:
    warnings: list[str] = []
    vj._check_url_seo("canonical", "http://sebastienrousseau.com/a/", warnings)
    assert warnings and "https" in warnings[0]


def test_an_over_long_url_is_a_seo_warning() -> None:
    warnings: list[str] = []
    vj._check_url_seo("canonical", "https://x.com/" + "a" * 2100, warnings)
    assert any("2048" in w for w in warnings)


def test_a_normal_https_url_warns_about_nothing() -> None:
    warnings: list[str] = []
    vj._check_url_seo("canonical", "https://sebastienrousseau.com/a/", warnings)
    assert warnings == []


# ---------------------------------------------------------------------------
# Feed date shapes
# ---------------------------------------------------------------------------


def test_rfc822_accepts_the_canonical_shape() -> None:
    assert vj.RFC822_RE.match("Mon, 11 May 2026 06:06:06 +0000")


def test_rfc822_accepts_gmt_and_utc_zones() -> None:
    assert vj.RFC822_RE.match("Mon, 11 May 2026 06:06:06 GMT")
    assert vj.RFC822_RE.match("Mon, 11 May 2026 06:06:06 UTC")


def test_rfc822_rejects_a_single_digit_day() -> None:
    """Feed readers reject the loose form; so must the gate."""
    assert not vj.RFC822_RE.match("Mon, 1 May 2026 06:06:06 +0000")


def test_rfc822_rejects_an_iso_date() -> None:
    assert not vj.RFC822_RE.match("2026-05-11T06:06:06+00:00")


def test_rfc3339_accepts_a_bare_date_and_a_full_timestamp() -> None:
    assert vj.RFC3339_RE.match("2026-05-11")
    assert vj.RFC3339_RE.match("2026-05-11T06:06:06+00:00")
    assert vj.RFC3339_RE.match("2026-05-11T06:06:06Z")


def test_rfc3339_rejects_a_timestamp_with_no_zone() -> None:
    assert not vj.RFC3339_RE.match("2026-05-11T06:06:06")


def test_localname_strips_a_namespace() -> None:
    assert vj._localname("{http://www.w3.org/2005/Atom}entry") == "entry"
    assert vj._localname("item") == "item"
