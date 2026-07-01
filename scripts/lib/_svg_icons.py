"""Shared inline SVG glyphs for per-card share rails.

Six monochrome 16x16 icons (X, LinkedIn, Facebook, WhatsApp, email, copy-link)
used by the article-card share rails. Consolidated here from byte-identical
copies previously carried in build_listings.py and build_tag_landings.py
(Phase 4.2 de-duplication).
"""

from __future__ import annotations

_CARD_SVG_X = '<svg viewBox="0 0 16 16" aria-hidden="true" focusable="false"><path d="M9.52 6.88L14.86 1h-1.42L8.83 6.07 4.94 1H.78l5.6 7.7L.78 15h1.42l4.78-5.27L11.07 15h4.16L9.52 6.88zM2.71 2.07h1.83l7.61 10.51h-1.83L2.71 2.07z"/></svg>'
_CARD_SVG_LI = '<svg viewBox="0 0 16 16" aria-hidden="true" focusable="false"><path d="M13.6 13.6h-2.37V9.93c0-.87-.02-2-1.22-2-1.22 0-1.4.95-1.4 1.93v3.74H6.24V6.04h2.27v1.04h.03c.32-.6 1.09-1.22 2.25-1.22 2.4 0 2.85 1.58 2.85 3.64v4.1zM3.56 5C2.81 5 2.2 4.39 2.2 3.64S2.81 2.28 3.56 2.28s1.36.61 1.36 1.36S4.31 5 3.56 5zm1.18 8.6H2.39V6.04h2.36V13.6z"/></svg>'
_CARD_SVG_FB = '<svg viewBox="0 0 16 16" aria-hidden="true" focusable="false"><path d="M9 14H6.5V8.5H5V6h1.5V4.5C6.5 3.07 7.07 2 9.07 2H10.5v2.5H9.43c-.38 0-.43.14-.43.43V6h1.5L10 8.5H9V14z"/></svg>'
_CARD_SVG_WA = '<svg viewBox="0 0 16 16" aria-hidden="true" focusable="false"><path d="M8 1C4.13 1 1 4.13 1 8c0 1.27.34 2.46.93 3.5L1 15l3.6-.93C5.62 14.66 6.79 15 8 15c3.87 0 7-3.13 7-7s-3.13-7-7-7zm0 12.7c-1.06 0-2.05-.29-2.9-.78l-.2-.12-2.13.56.57-2.08-.13-.21A5.69 5.69 0 012.3 8c0-3.14 2.56-5.7 5.7-5.7s5.7 2.56 5.7 5.7-2.56 5.7-5.7 5.7z"/></svg>'
_CARD_SVG_EMAIL = '<svg viewBox="0 0 16 16" aria-hidden="true" focusable="false"><path d="M2 3h12c.55 0 1 .45 1 1v8c0 .55-.45 1-1 1H2c-.55 0-1-.45-1-1V4c0-.55.45-1 1-1zm6 5.18L13.18 4H2.82L8 8.18zM2 5.46V12h12V5.46L8 9.5 2 5.46z"/></svg>'
_CARD_SVG_LINK = '<svg viewBox="0 0 16 16" aria-hidden="true" focusable="false"><path d="M6.6 10.4a1.5 1.5 0 010-2.1l2.8-2.8a1.5 1.5 0 112.1 2.1L10 9.1l1.1 1.1 1.5-1.5a3 3 0 00-4.2-4.2L5.6 7.3a3 3 0 000 4.2 3 3 0 002.1.9l-1-1c-.1 0-.1-.1-.1-.1zM9.4 5.6L8.3 6.7l1.4 1.4 1.1-1.1A1.5 1.5 0 0112.9 9l-2.8 2.8a1.5 1.5 0 11-2.1-2.1L9.1 8.6 8 7.5 6.5 9a3 3 0 004.2 4.2l 2.8-2.8a3 3 0 000-4.2 3 3 0 00-4.1-.6z"/></svg>'
