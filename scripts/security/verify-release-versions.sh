#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2026 Sebastien Rousseau <sebastian.rousseau@gmail.com>
# SPDX-License-Identifier: Apache-2.0 OR MIT
#
# Fail unless every place that names the release version names the same
# one: the newest CHANGELOG heading, pyproject.toml, CITATION.cff, and the
# release notes under docs/releases/.
#
# Usage:
#   scripts/security/verify-release-versions.sh            # newest CHANGELOG version
#   scripts/security/verify-release-versions.sh v1.2.1     # a named version
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/../.."

newest=$(sed -nE 's/^## \[([0-9]+\.[0-9]+\.[0-9]+)\].*/\1/p' CHANGELOG.md | head -n1)
tag="${1:-${newest}}"
ver="${tag#v}"
[ -n "${ver}" ] || { echo "verify-release-versions: CHANGELOG.md has no '## [x.y.z]' heading" >&2; exit 2; }
fail=0
bad() { echo "verify-release-versions: $*" >&2; fail=1; }

[ "${newest}" = "${ver}" ] || bad "newest CHANGELOG.md heading is '${newest}', not ${ver}"

pyproject_ver=$(sed -nE 's/^version = "([0-9]+\.[0-9]+\.[0-9]+)"/\1/p' pyproject.toml | head -n1)
[ "${pyproject_ver}" = "${ver}" ] || bad "pyproject.toml version is '${pyproject_ver}', not ${ver}"

citation_ver=$(sed -nE 's/^version: ([0-9]+\.[0-9]+\.[0-9]+)/\1/p' CITATION.cff | head -n1)
[ "${citation_ver}" = "${ver}" ] || bad "CITATION.cff version is '${citation_ver}', not ${ver}"

notes="docs/releases/v${ver}.md"
if [ ! -f "${notes}" ]; then
  bad "${notes} does not exist"
elif ! grep -q '^## Highlights ⭐️$' "${notes}"; then
  bad "${notes} has no '## Highlights ⭐️' section"
fi

[ "${fail}" -eq 0 ] && echo "verify-release-versions: all version references agree on ${ver}"
exit "${fail}"
