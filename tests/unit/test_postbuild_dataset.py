"""Dataset JSON-LD pass — postbuild_lib.schemas.inject_dataset."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from postbuild_lib import schemas

ENTRY = {
    "slug": "2026-06-02-an-index",
    "name": "The 2026 Index",
    "description": "What it measures.",
    "keywords": "banking, quantum,  ,",
    "date": "June 2, 2026",
    "measures": "Index Layer",
    "variables": [{"name": "Agentic AI", "description": "Readiness Metric: task success"}],
}

PAGE_HTML = "<html><body><p>x</p></body></html>"


@pytest.fixture(autouse=True)
def _clear_cache(monkeypatch):
    monkeypatch.setattr(schemas, "_DATASETS", None)


def _manifest(tmp_path: Path, entries: list[dict]) -> Path:
    path = tmp_path / "datasets.json"
    path.write_text(json.dumps({"datasets": entries}), encoding="utf-8")
    return path


def _dataset_block(html: str) -> dict:
    marker = '{"@context":"https://schema.org","@type":"Dataset"'
    start = html.index(marker)
    end = html.index("</script>", start)
    return json.loads(html[start:end])


def test_a_declared_article_gets_a_dataset(tmp_path, monkeypatch):
    monkeypatch.setattr(schemas, "_DATASETS_PATH", _manifest(tmp_path, [ENTRY]))
    page = Path("public") / ENTRY["slug"] / "index.html"
    out = schemas.inject_dataset(page, PAGE_HTML)
    data = _dataset_block(out)
    assert data["@type"] == "Dataset"
    assert data["name"] == "The 2026 Index"
    assert data["url"].endswith(ENTRY["slug"])
    assert data["isAccessibleForFree"] is True


def test_variables_become_variable_measured(tmp_path, monkeypatch):
    """The frameworks are qualitative, so they describe what is measured."""
    monkeypatch.setattr(schemas, "_DATASETS_PATH", _manifest(tmp_path, [ENTRY]))
    page = Path("public") / ENTRY["slug"] / "index.html"
    data = _dataset_block(schemas.inject_dataset(page, PAGE_HTML))
    assert data["variableMeasured"] == [
        {
            "@type": "PropertyValue",
            "name": "Agentic AI",
            "description": "Readiness Metric: task success",
        }
    ]


def test_both_distributions_are_offered(tmp_path, monkeypatch):
    monkeypatch.setattr(schemas, "_DATASETS_PATH", _manifest(tmp_path, [ENTRY]))
    page = Path("public") / ENTRY["slug"] / "index.html"
    data = _dataset_block(schemas.inject_dataset(page, PAGE_HTML))
    formats = {d["encodingFormat"]: d["contentUrl"] for d in data["distribution"]}
    assert set(formats) == {"application/json", "text/csv"}
    assert formats["text/csv"].endswith(f"/data/{ENTRY['slug']}.csv")


def test_blank_keywords_are_dropped(tmp_path, monkeypatch):
    monkeypatch.setattr(schemas, "_DATASETS_PATH", _manifest(tmp_path, [ENTRY]))
    page = Path("public") / ENTRY["slug"] / "index.html"
    data = _dataset_block(schemas.inject_dataset(page, PAGE_HTML))
    assert data["keywords"] == ["banking", "quantum"]


def test_an_undeclared_page_is_untouched(tmp_path, monkeypatch):
    monkeypatch.setattr(schemas, "_DATASETS_PATH", _manifest(tmp_path, [ENTRY]))
    page = Path("public") / "2026-06-26-something-else" / "index.html"
    assert schemas.inject_dataset(page, PAGE_HTML) == PAGE_HTML


def test_missing_manifest_is_a_no_op(tmp_path, monkeypatch):
    monkeypatch.setattr(schemas, "_DATASETS_PATH", tmp_path / "absent.json")
    page = Path("public") / ENTRY["slug"] / "index.html"
    assert schemas.inject_dataset(page, PAGE_HTML) == PAGE_HTML


@pytest.mark.parametrize("existing", ['"@type":"Dataset"', '"@type": "Dataset"'])
def test_idempotent_for_both_json_spacings(tmp_path, monkeypatch, existing):
    monkeypatch.setattr(schemas, "_DATASETS_PATH", _manifest(tmp_path, [ENTRY]))
    page = Path("public") / ENTRY["slug"] / "index.html"
    html = f"<html><body><script>{existing}</script></body></html>"
    assert schemas.inject_dataset(page, html) == html


def test_manifest_is_read_once(tmp_path, monkeypatch):
    path = _manifest(tmp_path, [ENTRY])
    monkeypatch.setattr(schemas, "_DATASETS_PATH", path)
    page = Path("public") / ENTRY["slug"] / "index.html"
    schemas.inject_dataset(page, PAGE_HTML)
    path.unlink()  # cached, so a second call must still work
    assert '"@type":"Dataset"' in schemas.inject_dataset(page, PAGE_HTML)
