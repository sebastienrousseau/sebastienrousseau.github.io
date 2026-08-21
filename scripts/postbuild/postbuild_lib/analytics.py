"""Privacy-preserving traffic measurement, off by default until configured.

Nothing measured the site. No Plausible, Umami, Fathom, GA4 or Cloudflare
beacon was loaded on any page — the only occurrence of ``cloudflareinsights``
anywhere in the HTML was inside the CSP allowlist, permitting a script that
was never included. The consequence is that none of the site's SEO or AI
distribution work is falsifiable from the inside: which of the 28 locales earn
traffic, whether the tag experiment ever helped, what the real Core Web Vitals
field data says (the Lighthouse number in CI is a lab estimate, and CrUX is
the only source that counts for ranking) — all unknown.

Cloudflare Web Analytics is the right default here: free, cookieless, no
personal data, so no consent banner is required, and the edge is already
Cloudflare. ``script-src`` already permits
``https://static.cloudflareinsights.com``, so enabling it needs no CSP change.

**Activation is one step.** Create the site in Cloudflare → Web Analytics,
then put its token in either:

  * the environment: ``CF_BEACON_TOKEN=<token> ./build.sh``, or
  * ``_data/analytics.json``: ``{"cloudflare_beacon_token": "<token>"}``
    (gitignored — the token is not a secret, but it is deployment config).

With neither present this pass does nothing at all, so a fork or a local build
stays beacon-free. That is deliberate: measurement should be opt-in and
visible in config, never a surprise in the HTML.
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path

BEACON_SRC = "https://static.cloudflareinsights.com/beacon.min.js"
_CONFIG = Path("_data") / "analytics.json"
_ENV_VAR = "CF_BEACON_TOKEN"
# A Cloudflare beacon token is a 32-character hex string. Validating it keeps a
# malformed value out of the markup instead of shipping a broken script tag.
_TOKEN_RE = re.compile(r"^[0-9a-f]{32}$")
_BODY_CLOSE_RE = re.compile(r"</body>", re.IGNORECASE)
_MARKER = "static.cloudflareinsights.com/beacon.min.js"


def beacon_token(config: Path = _CONFIG) -> str | None:
    """The configured token, or None when analytics is not enabled.

    Environment wins over the config file so CI can inject it without a
    working-tree change."""
    raw = os.environ.get(_ENV_VAR, "").strip()
    if not raw and config.is_file():
        try:
            raw = str(json.loads(config.read_text(encoding="utf-8")).get(
                "cloudflare_beacon_token", ""
            )).strip()
        except (OSError, ValueError):
            return None
    return raw if _TOKEN_RE.match(raw) else None


def inject_analytics_beacon(html: str, token: str | None) -> str:
    """Append the Cloudflare Web Analytics beacon before ``</body>``.

    No-op when no token is configured or the beacon is already present, so the
    pass is idempotent and inert on an unconfigured build. ``defer`` keeps it
    off the critical path — measurement must never cost LCP."""
    if not token or _MARKER in html:
        return html
    tag = (
        f'<script defer src="{BEACON_SRC}" '
        f"data-cf-beacon='{json.dumps({'token': token})}'></script>"
    )
    return _BODY_CLOSE_RE.sub(tag + "</body>", html, count=1)
