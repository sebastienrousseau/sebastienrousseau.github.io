<!--
PR description template. Global rule: see ~/Code/AGENTS.md "PR Descriptions"
and "Release Page Format".
Rules:
  - A two-line BLUF (bottom line up front):
    Line 1 begins "This PR " and announces what it does in one plain line.
    Line 2 explains why it matters or the outcome in one plain line.
    Separate line 1 and line 2 each with a blank line.
  - Never use the em dash character anywhere in the body. Use commas, colons, parentheses, or spaced hyphens.
  - Write directly, concretely, and friendly with zero conversational filler.
  - Omit greetings on the user's own repositories.
  - No tool-attribution footer.
-->

This PR {{announces what it does, in one plain line}}.

{{BLUF_LINE_2: why it matters or outcome, in one plain line}}

## Highlights ⭐️

* **{{HEADLINE}}**: {{one or two plain sentences on what changed for the user}}.
* **{{HEADLINE}}**: {{one or two plain sentences}}.

## What's Changed

* `{{COMMIT_SUBJECT}}` by @{{AUTHOR}} in {{PR_URL}}

## Validation

* `python3 -m pytest tests/unit/test_requirements_locks_agree.py`: 9 passed.
* `python3 -m ruff check scripts/ tests/ fly/`: clean (zero warnings).
* `python3 -m ruff format --check scripts/ tests/ fly/`: clean.
* `./scripts/typecheck.sh`: mypy strict tier clean.

## Checksums

SHA-256 of artifacts produced on this branch:

```text
{{SHA256}}  requirements.lock
{{SHA256}}  requirements-dev.lock
```

**Full Changelog**: https://github.com/sebastienrousseau/sebastienrousseau.github.io/compare/{{PREV_TAG}}...{{CURR_TAG}}
