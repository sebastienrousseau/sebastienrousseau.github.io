# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Open or update the ``search-alert`` issue for a weekly impressions drop.

Runs inside ``.github/workflows/search-weekly.yml`` with the workflow's own
``GITHUB_TOKEN`` (``issues: write``). One open issue carries the alert:

* no open ``search-alert`` issue: create one, labelled;
* one is open: add this week's report to it as a comment;
* this week is already on it (body or a recent comment carries the week's
  hidden marker): do nothing, so a re-run or a manual dispatch in the same
  week never posts twice.

Pull requests (which the issues API also returns) are ignored, and if more
than one issue is open the oldest is updated.
"""

from __future__ import annotations

import datetime as dt
import json
import urllib.request
from typing import Any, Protocol

API = "https://api.github.com"
LABEL = "search-alert"
TIMEOUT = 30


class Client(Protocol):
    def call(self, method: str, path: str, body: dict[str, Any] | None = None) -> Any: ...


class GitHub:
    """Minimal GitHub REST client over ``urllib``."""

    def __init__(self, token: str) -> None:
        self.token = token

    def call(self, method: str, path: str, body: dict[str, Any] | None = None) -> Any:
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(
            API + path,
            data=data,
            method=method,
            headers={
                "Authorization": f"Bearer {self.token}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
                "Content-Type": "application/json",
            },
        )
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return json.loads(resp.read().decode("utf-8"))


def marker(week: str) -> str:
    """Hidden de-duplication marker for the report week ending ``week``."""
    return f"<!-- {LABEL} week={week} -->"


def _open_issue(gh: Client, repo: str) -> dict[str, Any] | None:
    found = gh.call("GET", f"/repos/{repo}/issues?labels={LABEL}&state=open&per_page=100")
    issues = [i for i in found if "pull_request" not in i]
    return min(issues, key=lambda i: i["number"]) if issues else None


def _already_reported(gh: Client, repo: str, issue: dict[str, Any], tag: str) -> bool:
    if tag in (issue.get("body") or ""):
        return True
    since = (dt.datetime.now(dt.UTC) - dt.timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:%SZ")
    comments = gh.call(
        "GET", f"/repos/{repo}/issues/{issue['number']}/comments?since={since}&per_page=100"
    )
    return any(tag in (c.get("body") or "") for c in comments)


def file_alert(gh: Client, repo: str, title: str, body: str, week: str) -> str:
    """Create, comment on, or leave the alert issue; returns what happened."""
    tag = marker(week)
    text = f"{body}\n\n{tag}\n"
    issue = _open_issue(gh, repo)
    if issue is None:
        made = gh.call(
            "POST", f"/repos/{repo}/issues", {"title": title, "body": text, "labels": [LABEL]}
        )
        return f"created #{made['number']}"
    number = issue["number"]
    if _already_reported(gh, repo, issue, tag):
        return f"already reported on #{number}"
    gh.call("POST", f"/repos/{repo}/issues/{number}/comments", {"body": text})
    return f"commented on #{number}"
