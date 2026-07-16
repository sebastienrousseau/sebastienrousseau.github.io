#!/usr/bin/env python3
"""Generate the 10 non-index layouts from the new index.html shell.

The shared shell is everything except the body's `<section class="ap-hero">…</section>`,
`<main>…</main>`, and `<aside>…</aside>`. Each layout below substitutes its own hero +
main body. Aside is dropped (it lives on the homepage only).
"""

from __future__ import annotations

import sys as _sys  # path bootstrap — scripts reorg (scripts/lib/ on sys.path)
from pathlib import Path as _Path

_sys.path.insert(0, str(_Path(__file__).resolve().parents[1] / "lib"))

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LAYOUTS = ROOT / "_layouts"
INDEX = (LAYOUTS / "index.html").read_text()


def slice_shell(index_html: str) -> tuple[str, str]:
    """Return (top, bottom): top ends just before the hero, bottom starts at footer."""
    hero_start = index_html.index("<!-- gen-layouts:hero-start -->")
    footer_start = index_html.index("<!-- gen-layouts:footer-start -->")
    return index_html[:hero_start], index_html[footer_start:]


TOP, BOTTOM = slice_shell(INDEX)


# Page-scoped CSS for /speaking/ and the /iso20022-mcp/ hub. Both pages
# fork the BUILT articles page as their shell (build_speaking.py /
# build_iso20022_mcp.py), so these rules must ship inside articles.html.
# Injected only there (see main()) to keep the other layouts lean.
# Raw string: CSS content escapes like \2713 must reach the page verbatim.
SPEAKING_MCP_HUB_CSS = r"""      /* ============================================================
         Speaking page: FT/Bloomberg-style speaker template, adapted to
         the site's light+dark theme tokens. All rules scoped to
         .speaking-page and spk- prefixed so no other page is touched.
         Standards identifiers (ISO 20022, FIPS 203, ...) set in mono.
         ============================================================ */
      .speaking-page{--spk-band:var(--paper-card);--spk-line:var(--rule);--spk-line-strong:var(--border);--spk-blue:var(--link-color);--spk-green:#005f33;--spk-serif:var(--type-display);--spk-sans:var(--type-body);--spk-mono:var(--type-mono);font-family:var(--spk-sans);color:var(--ink);line-height:1.65}
      /* Dark surfaces need a light green: #005f33 is 2.31:1 on --card #161617. */
      [data-theme="dark"] .speaking-page{--spk-green:#6fd49a}
      @media (prefers-color-scheme: dark){html:not([data-theme="light"]) .speaking-page{--spk-green:#6fd49a}}
      .speaking-page .spk-wrap{max-width:1120px;margin-inline:auto;padding-inline:clamp(20px,5vw,64px)}
      .speaking-page section{padding-block:clamp(44px,6vw,82px)}
      .speaking-page .spk-band{background:var(--spk-band);border-block:1px solid var(--spk-line)}
      .speaking-page h1,.speaking-page h2,.speaking-page h3{font-family:var(--spk-serif);font-weight:500;line-height:1.07;letter-spacing:-.01em;color:var(--ink)}
      .speaking-page h1{font-size:clamp(2.4rem,5.2vw,4.1rem);margin:0 0 1.3rem}
      .speaking-page h2{font-size:clamp(1.8rem,3.3vw,2.8rem);letter-spacing:-.015em;margin:0}
      .speaking-page h3{font-size:1.26rem;line-height:1.2;margin:0}
      .speaking-page p{color:var(--ink-soft);margin:0}
      .speaking-page .spk-lede{font-size:clamp(1.04rem,1.4vw,1.2rem);color:var(--ink-soft);line-height:1.6;max-width:62ch}
      .speaking-page .spk-eyebrow{font-family:var(--spk-mono);font-size:.76rem;font-weight:600;text-transform:uppercase;letter-spacing:.13em;color:var(--spk-blue);display:block;margin-block-end:1rem}
      .speaking-page .spk-mono{font-family:var(--spk-mono);font-size:.86em;letter-spacing:-.01em;color:var(--spk-blue)}
      .speaking-page .spk-head{max-width:64ch}
      .speaking-page .spk-head.spk-center{margin-inline:auto;text-align:center}
      .speaking-page .spk-head.spk-center .spk-lede{margin-inline:auto}
      .speaking-page .spk-head p{margin-block-start:.9rem}
      /* buttons */
      .speaking-page .spk-btn{display:inline-flex;align-items:center;gap:.5em;font-family:var(--spk-sans);font-size:.95rem;font-weight:500;padding:.8em 1.5em;border-radius:7px;border:1px solid transparent;cursor:pointer;text-align:center;transition:background .18s,color .18s,border-color .18s,transform .18s}
      .speaking-page .spk-btn-primary{background:var(--spk-blue);color:var(--bg)}
      .speaking-page .spk-btn-primary:hover{filter:brightness(.92)}
      .speaking-page .spk-btn-ghost{background:transparent;color:var(--ink);border-color:var(--spk-line-strong)}
      .speaking-page .spk-btn-ghost:hover{border-color:var(--ink)}
      .speaking-page .spk-btn:hover .spk-arw{transform:translateX(2px)}
      .speaking-page .spk-arw{transition:transform .18s}
      .speaking-page .spk-textlink{color:var(--spk-blue);font-weight:500;border-block-end:1px solid transparent}
      .speaking-page .spk-textlink:hover{border-block-end-color:var(--spk-blue)}
      /* hero */
      .speaking-page .spk-hero{padding-block:clamp(32px,5vw,64px) clamp(40px,6vw,80px)}
      .speaking-page .spk-hero-grid{max-width:1120px;margin-inline:auto;padding-inline:clamp(20px,5vw,64px);display:grid;grid-template-columns:1.15fr .85fr;gap:clamp(32px,5vw,64px);align-items:center}
      .speaking-page .spk-hero .spk-lede{margin-block:0 1.7rem}
      .speaking-page .spk-cta-row{display:flex;flex-wrap:wrap;gap:.8rem;margin-block-end:1.1rem}
      .speaking-page .spk-press-nudge{font-size:.9rem;color:var(--ink-faint)}
      .speaking-page .spk-press-nudge a{color:var(--ink-soft)}
      .speaking-page .spk-microproof{margin-block-start:1.6rem;padding-block-start:1.4rem;border-block-start:1px solid var(--spk-line);font-size:.88rem;color:var(--ink-faint);line-height:1.6}
      .speaking-page .spk-microproof strong{color:var(--ink-soft);font-weight:500}
      .speaking-page .spk-hero-photo{border-radius:12px;overflow:hidden;background:var(--bg-alt);border:1px solid var(--spk-line-strong);aspect-ratio:4/5}
      .speaking-page .spk-hero-photo img{width:100%;height:100%;object-fit:cover;object-position:top center;display:block;filter:grayscale(1) contrast(1.03)}
      @media (max-width:860px){.speaking-page .spk-hero-grid{grid-template-columns:1fr}.speaking-page .spk-hero-photo{max-width:420px;aspect-ratio:16/11}}
      /* proof strip */
      .speaking-page .spk-strip{padding-block:clamp(28px,4vw,42px);border-block-start:1px solid var(--spk-line)}
      .speaking-page .spk-strip-label{font-family:var(--spk-mono);font-size:.72rem;text-transform:uppercase;letter-spacing:.14em;color:var(--ink-mute);margin-block-end:1rem}
      .speaking-page .spk-logos{display:flex;flex-wrap:wrap;gap:1.3rem 2.4rem;align-items:center}
      .speaking-page .spk-logos span{font-family:var(--spk-serif);font-size:1.02rem;color:var(--ink-faint);font-weight:500}
      /* stats */
      .speaking-page .spk-stats{display:grid;grid-template-columns:repeat(4,1fr);gap:clamp(20px,3vw,36px);text-align:center}
      .speaking-page .spk-num{font-family:var(--spk-serif);font-size:clamp(2.1rem,3.4vw,2.9rem);font-weight:500;color:var(--ink);letter-spacing:-.02em;line-height:1}
      .speaking-page .spk-lbl{font-family:var(--spk-mono);font-size:.7rem;text-transform:uppercase;letter-spacing:.1em;color:var(--ink-mute);margin-block-start:.7rem}
      .speaking-page .spk-stats-foot{margin-block-start:2.1rem;text-align:center;font-size:.86rem;color:var(--ink-faint);line-height:1.6;max-width:70ch;margin-inline:auto}
      @media (max-width:640px){.speaking-page .spk-stats{grid-template-columns:repeat(2,1fr);gap:30px 20px}}
      /* two paths */
      .speaking-page .spk-paths{display:grid;grid-template-columns:1fr 1fr;gap:22px;margin-block-start:2.6rem}
      .speaking-page .spk-path{border:1px solid var(--spk-line);border-radius:12px;padding:clamp(24px,3vw,36px);background:var(--card);display:flex;flex-direction:column}
      .speaking-page .spk-path .spk-eyebrow{margin-block-end:.8rem}
      .speaking-page .spk-path h3{margin-block-end:.7rem}
      .speaking-page .spk-path p{font-size:.98rem;margin-block-end:1.3rem}
      .speaking-page .spk-path ul{list-style:none;margin-block-end:1.5rem;padding:0}
      .speaking-page .spk-path li{font-size:.92rem;color:var(--ink-soft);padding-inline-start:1.3em;position:relative;margin-block-end:.5em}
      .speaking-page .spk-path li::before{content:"·";position:absolute;inset-inline-start:0;color:var(--spk-blue);font-family:var(--spk-mono);font-weight:700}
      .speaking-page .spk-path .spk-btn{margin-block-start:auto;align-self:flex-start}
      @media (max-width:760px){.speaking-page .spk-paths{grid-template-columns:1fr}}
      /* keynote cards */
      .speaking-page .spk-talks{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-block-start:2.7rem}
      .speaking-page .spk-talk{border:1px solid var(--spk-line);border-radius:12px;background:var(--card);padding:clamp(22px,2.4vw,30px);display:flex;flex-direction:column;transition:transform .2s,box-shadow .2s,border-color .2s}
      .speaking-page .spk-talk:hover{transform:translateY(-3px);box-shadow:0 14px 34px -18px rgba(13,27,42,.28);border-color:var(--spk-line-strong)}
      .speaking-page .spk-flag{font-family:var(--spk-mono);font-size:.66rem;text-transform:uppercase;letter-spacing:.12em;color:var(--spk-green);margin-block-end:.9rem}
      .speaking-page .spk-flag-new{color:var(--spk-blue)}
      .speaking-page .spk-talk h3{margin-block-end:.85rem}
      .speaking-page .spk-desc{font-size:.93rem;line-height:1.55;margin-block-end:1.1rem}
      .speaking-page .spk-outcome{font-size:.88rem;color:var(--ink);border-inline-start:2px solid var(--spk-blue);padding-inline-start:.85em;margin-block-end:1.2rem;line-height:1.5}
      .speaking-page .spk-outcome b{font-weight:600}
      .speaking-page .spk-talk-foot{margin-block-start:auto;padding-block-start:1.1rem;border-block-start:1px solid var(--spk-line)}
      .speaking-page .spk-audience{font-family:var(--spk-mono);font-size:.68rem;text-transform:uppercase;letter-spacing:.06em;color:var(--ink-mute);line-height:1.5}
      .speaking-page .spk-talk-cta{background:transparent;border-style:dashed;justify-content:center;align-items:flex-start}
      .speaking-page .spk-talk-cta .spk-desc{margin-block-end:1.4rem}
      @media (max-width:900px){.speaking-page .spk-talks{grid-template-columns:1fr 1fr}}
      @media (max-width:620px){.speaking-page .spk-talks{grid-template-columns:1fr}}
      /* how I work */
      .speaking-page .spk-formats{display:grid;grid-template-columns:repeat(3,1fr);gap:0;margin-block-start:2.4rem;border:1px solid var(--spk-line);border-radius:12px;overflow:hidden;background:var(--card)}
      .speaking-page .spk-format{padding:clamp(24px,3vw,34px);border-inline-end:1px solid var(--spk-line)}
      .speaking-page .spk-format:last-child{border-inline-end:0}
      .speaking-page .spk-format h3{font-size:1.14rem;margin-block-end:.4rem}
      .speaking-page .spk-dur{font-family:var(--spk-mono);font-size:.8rem;color:var(--spk-blue);margin-block-end:.9rem}
      .speaking-page .spk-format p{font-size:.9rem}
      .speaking-page .spk-locs{margin-block-start:1.8rem;display:flex;flex-wrap:wrap;gap:.6rem;justify-content:center}
      .speaking-page .spk-chip{font-family:var(--spk-mono);font-size:.74rem;color:var(--ink-soft);border:1px solid var(--spk-line-strong);border-radius:20px;padding:.4em 1em}
      @media (max-width:720px){.speaking-page .spk-formats{grid-template-columns:1fr}.speaking-page .spk-format{border-inline-end:0;border-block-end:1px solid var(--spk-line)}.speaking-page .spk-format:last-child{border-block-end:0}}
      /* press & media: deliberately branded dark-blue panel in both themes.
         Band-scoped tokens (global theme tokens flip with the theme, so they
         cannot supply a stable white chip on this theme-invariant navy):
         chip text derives from --spk-media-bg. Ratios: #04182f on #fff
         17.84:1, on hover #eaf0f8 15.57:1, chip vs band 17.84:1. AAA. */
      .speaking-page .spk-media{--spk-media-bg:#04182f;--spk-media-chip:#fff;--spk-media-chip-hover:#eaf0f8;background:var(--spk-media-bg);color:#c3d2e6;border-radius:16px;padding:clamp(30px,5vw,56px)}
      .speaking-page .spk-media h2{color:#fff}
      .speaking-page .spk-media .spk-eyebrow{color:#8fb4e4}
      .speaking-page .spk-media-grid{display:grid;grid-template-columns:1fr 1fr;gap:clamp(28px,4vw,48px);margin-block-start:2rem;align-items:start}
      .speaking-page .spk-avail{display:inline-flex;align-items:center;gap:.6em;font-family:var(--spk-mono);font-size:.82rem;letter-spacing:.04em;color:#cfe0f5;margin-block-end:1.2rem}
      .speaking-page .spk-dot{width:9px;height:9px;border-radius:50%;background:#2ecc80;box-shadow:0 0 0 0 rgba(31,138,91,.6);animation:spkpulse 2.4s infinite}
      .speaking-page .spk-dot-static{animation:none;box-shadow:none}
      @keyframes spkpulse{0%{box-shadow:0 0 0 0 rgba(31,138,91,.55)}70%{box-shadow:0 0 0 10px rgba(31,138,91,0)}100%{box-shadow:0 0 0 0 rgba(31,138,91,0)}}
      @media (prefers-reduced-motion:reduce){.speaking-page .spk-dot{animation:none}}
      .speaking-page .spk-media p{color:#c3d2e6}
      .speaking-page .spk-spec{font-family:var(--spk-mono);font-size:.82rem;color:#9fbce0;margin-block-start:1.4rem;line-height:1.9}
      .speaking-page .spk-media-topics{list-style:none;margin:0;padding:0}
      .speaking-page .spk-media-topics li{padding-block:.85em;border-block-end:1px solid rgba(255,255,255,.12);font-size:.97rem;color:#e4ecf6;display:flex;gap:.7em;align-items:baseline}
      .speaking-page .spk-media-topics li:last-child{border-block-end:0}
      .speaking-page .spk-tag{font-family:var(--spk-mono);font-size:.66rem;color:#7fa8da;text-transform:uppercase;letter-spacing:.1em;white-space:nowrap;padding-block-start:.15em}
      .speaking-page .spk-media .spk-mono{color:#bcd4f2}
      .speaking-page .spk-media-actions{margin-block-start:1.7rem;display:flex;flex-wrap:wrap;gap:.8rem}
      .speaking-page .spk-btn-onblue{background:var(--spk-media-chip);color:var(--spk-media-bg);border-color:var(--spk-media-chip)}
      .speaking-page .spk-btn-onblue:hover{background:var(--spk-media-chip-hover)}
      @media (max-width:760px){.speaking-page .spk-media-grid{grid-template-columns:1fr}}
      /* biography */
      .speaking-page .spk-bio-grid{display:grid;grid-template-columns:220px 1fr;gap:clamp(28px,4vw,56px);align-items:start;margin-block-start:2rem}
      .speaking-page .spk-bio-photo{aspect-ratio:1;border-radius:10px;overflow:hidden;background:var(--bg-alt);border:1px solid var(--spk-line-strong)}
      .speaking-page .spk-bio-photo img{width:100%;height:100%;object-fit:cover;filter:grayscale(1) contrast(1.03)}
      .speaking-page .spk-bio-body p{margin-block-end:1.1rem;font-size:1.02rem;color:var(--ink-soft)}
      .speaking-page .spk-bio-body p:last-child{margin-block-end:0}
      @media (max-width:640px){.speaking-page .spk-bio-grid{grid-template-columns:1fr;max-width:440px}}
      /* ready-to-use bios */
      .speaking-page .spk-bios{display:grid;gap:16px;margin-block-start:2.4rem}
      .speaking-page .spk-biocard{border:1px solid var(--spk-line);border-radius:12px;background:var(--card);padding:clamp(22px,2.6vw,30px);position:relative}
      .speaking-page .spk-len{font-family:var(--spk-mono);font-size:.68rem;text-transform:uppercase;letter-spacing:.13em;color:var(--spk-blue);margin-block-end:.9rem}
      .speaking-page .spk-biocard p{font-size:.95rem;line-height:1.6;color:var(--ink);padding-inline-end:5.5rem}
      .speaking-page .spk-copybtn{position:absolute;inset-block-start:clamp(22px,2.6vw,30px);inset-inline-end:clamp(22px,2.6vw,30px);font-family:var(--spk-mono);font-size:.7rem;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-soft);background:var(--spk-band);border:1px solid var(--spk-line-strong);border-radius:6px;padding:.5em .9em;cursor:pointer;transition:border-color .15s,color .15s}
      .speaking-page .spk-copybtn:hover{border-color:var(--ink);color:var(--ink)}
      @media (max-width:560px){.speaking-page .spk-biocard p{padding-inline-end:0;margin-block-start:.4rem}.speaking-page .spk-copybtn{position:static;margin-block-end:.8rem}}
      /* FAQ: canonical .qa accordion (see the shared .qa-item rules); only
         the section-level offset is speaking-specific. */
      .speaking-page .spk-faq{margin-block-start:2.4rem}
      /* booking */
      .speaking-page .spk-booking-grid{display:grid;grid-template-columns:1.15fr .85fr;gap:clamp(32px,5vw,64px);align-items:start}
      .speaking-page .spk-book-intro .spk-lede{margin-block:.9rem 1.6rem}
      .speaking-page .spk-book-aside .spk-eyebrow{margin-block-end:.9rem}
      .speaking-page .spk-book-aside h3{margin-block-end:.8rem}
      .speaking-page .spk-book-aside p{font-size:.96rem;margin-block-end:1.2rem}
      .speaking-page .spk-book-aside .spk-avail{color:var(--ink-soft)}
      .speaking-page .spk-aside-list{list-style:none;margin-block-start:1rem;padding:0}
      .speaking-page .spk-aside-list li{font-size:.9rem;color:var(--ink-soft);padding-block:.7em;border-block-start:1px solid var(--spk-line);display:flex;justify-content:space-between;gap:1rem}
      .speaking-page .spk-aside-list li b{color:var(--ink);font-weight:500}
      @media (max-width:820px){.speaking-page .spk-booking-grid{grid-template-columns:1fr}}
      /* final CTA */
      .speaking-page .spk-finalcta{text-align:center}
      .speaking-page .spk-finalcta h2{margin-block-end:1rem}
      .speaking-page .spk-finalcta .spk-lede{margin:0 auto 1.7rem}
      .speaking-page .spk-finalcta .spk-cta-row{justify-content:center}
      /* --- ISO 20022 MCP hub: Apple Partner Network styling ----------------
         Scoped to .iso20022-mcp-page; accents use the site's own --spk-blue /
         --link-color so links + buttons stay on-brand. */
      .iso20022-mcp-page section{margin-block:clamp(44px,7vw,96px)}
      .iso20022-mcp-page .spk-hero{margin-block-start:clamp(24px,5vw,52px)}
      .iso20022-mcp-page .spk-hero-grid{grid-template-columns:1fr}
      .iso20022-mcp-page .spk-hero h1{font-size:clamp(2.5rem,6vw,4.1rem);line-height:1.05;letter-spacing:-.022em;font-weight:600;max-width:22ch;text-wrap:balance}
      .iso20022-mcp-page .spk-hero .spk-lede{font-size:clamp(1.12rem,1.8vw,1.4rem);line-height:1.45;color:var(--ink-soft);max-width:46ch}
      .iso20022-mcp-page .mcp-hero-media{margin-block:clamp(28px,5vw,52px) clamp(44px,7vw,96px)}
      .iso20022-mcp-page .mcp-hero-img{width:100%;border-radius:22px;aspect-ratio:16/8;object-fit:cover;display:block}
      .iso20022-mcp-page .mcp-band-img{width:100%;border-radius:18px;aspect-ratio:16/6;object-fit:cover;display:block}
      .iso20022-mcp-page .mcp-band-img-tall{width:100%;border-radius:18px;aspect-ratio:16/9;object-fit:cover;display:block}
      .iso20022-mcp-page .spk-head{max-width:42ch}
      .iso20022-mcp-page .spk-head h2{font-size:clamp(1.7rem,3.4vw,2.5rem);line-height:1.1;letter-spacing:-.016em;font-weight:600;text-wrap:balance}
      .iso20022-mcp-page .spk-paths{gap:clamp(16px,1.6vw,22px)}
      .iso20022-mcp-page .spk-path{background:var(--bg-alt);border:0;border-radius:18px;padding:clamp(28px,3.2vw,44px)}
      .iso20022-mcp-page .spk-path h3{font-size:1.3rem;letter-spacing:-.01em;margin-block:.15rem .5rem}
      .iso20022-mcp-page .mcp-icon{display:block;width:34px;height:34px;color:var(--ink);margin-block-end:1.15rem}
      .iso20022-mcp-page .mcp-icon svg{width:100%;height:100%;stroke:currentColor;fill:none}
      .iso20022-mcp-page .spk-band{background:transparent;color:inherit;border-radius:0;padding:0}
      .iso20022-mcp-page .spk-band h2{color:var(--ink)}
      .iso20022-mcp-page .spk-band p{color:var(--ink-soft)}
      .iso20022-mcp-page .spk-band .spk-eyebrow{color:var(--spk-blue)}
      .iso20022-mcp-page .mcp-start-cta{margin-block-start:1.8rem}
      .iso20022-mcp-page .spk-path .spk-eyebrow{color:var(--ink-soft)}
      @media (max-width:720px){.iso20022-mcp-page .spk-paths{grid-template-columns:1fr}}
      /* --- MCP hub: trust flow (generate/validate local, human approval
         wall before dispatch). All text pairs are AAA (>=7:1) in both
         themes: --ink 16.8/19.3, --ink-soft 11.4/14.2, --ink-soft on
         --bg-alt 10.1/11.4, --spk-blue on --bg 7.9/11.1, badge (--bg on
         --spk-blue) 7.9/11.1, --ink-faint 8.1/9.6, --ink on --card
         16.8/16.6, --spk-blue on --bg-alt 7.0/8.9. */
      .iso20022-mcp-page .mcp-flow{list-style:none;margin:2.6rem 0 0;padding:0;display:grid;grid-template-columns:repeat(4,1fr);gap:clamp(14px,1.6vw,22px)}
      .iso20022-mcp-page .mcp-step{min-width:0;position:relative;background:var(--bg-alt);border:2px solid transparent;border-radius:18px;padding:clamp(24px,2.6vw,36px)}
      .iso20022-mcp-page .mcp-step-num{font-family:var(--spk-mono);font-size:.78rem;letter-spacing:.12em;color:var(--ink-soft);display:block;margin-block-end:.9rem}
      .iso20022-mcp-page .mcp-step h3{font-size:1.16rem;margin-block-end:.55rem}
      .iso20022-mcp-page .mcp-step p{font-size:.92rem;color:var(--ink-soft);margin:0}
      .iso20022-mcp-page .mcp-step-gate{border-color:var(--spk-blue)}
      .iso20022-mcp-page .mcp-gate-badge{position:absolute;inset-block-start:-.8em;inset-inline-start:clamp(24px,2.6vw,36px);background:var(--spk-blue);color:var(--bg);font-family:var(--spk-mono);font-size:.62rem;font-weight:600;text-transform:uppercase;letter-spacing:.12em;padding:.35em .9em;border-radius:20px}
      @media (max-width:980px){.iso20022-mcp-page .mcp-flow{grid-template-columns:1fr 1fr}}
      @media (max-width:560px){.iso20022-mcp-page .mcp-flow{grid-template-columns:1fr}}
      /* --- MCP hub: security strip */
      .iso20022-mcp-page .mcp-sec{display:grid;grid-template-columns:repeat(4,1fr);gap:clamp(18px,2.4vw,32px);margin-block-start:2.4rem}
      .iso20022-mcp-page .mcp-sec-cell .mcp-icon{width:28px;height:28px;margin-block-end:.9rem}
      .iso20022-mcp-page .mcp-sec-cell .spk-eyebrow{margin-block-end:.5rem}
      .iso20022-mcp-page .mcp-sec-cell h3{font-size:1.1rem;margin-block-end:.5rem}
      .iso20022-mcp-page .mcp-sec-cell p{font-size:.9rem;color:var(--ink-soft);margin:0}
      @media (max-width:860px){.iso20022-mcp-page .mcp-sec{grid-template-columns:1fr 1fr}}
      @media (max-width:520px){.iso20022-mcp-page .mcp-sec{grid-template-columns:1fr}}
      /* --- MCP hub: code blocks + copy affordance */
      .iso20022-mcp-page .mcp-code{background:var(--bg-alt);border:1px solid var(--spk-line);border-radius:12px;padding:14px 18px;margin:0;overflow-x:auto}
      .iso20022-mcp-page .mcp-code code{font-family:var(--spk-mono);font-size:.8rem;line-height:1.6;color:var(--ink);background:transparent;white-space:pre}
      /* Copy buttons ride the shared .ap-cta-mini pill recipe (the generator
         emits class="ap-cta-mini mcp-copy"); only the button-element reset
         and the copied checkmark are added here. */
      .iso20022-mcp-page .mcp-copy{margin-block-start:.6rem;align-self:flex-start;border:0;cursor:pointer;font-family:var(--spk-sans)}
      .iso20022-mcp-page .mcp-copy[data-copied="1"]::after{content:" \2713"}
      /* --- MCP hub: multi-client grid */
      .iso20022-mcp-page .mcp-clients{display:grid;grid-template-columns:repeat(2,1fr);gap:clamp(16px,1.6vw,22px);margin-block-start:2.4rem}
      .iso20022-mcp-page .mcp-clients-3{grid-template-columns:repeat(3,1fr);margin-block-start:1.2rem}
      .iso20022-mcp-page .mcp-client{min-width:0;background:var(--bg-alt);border-radius:18px;padding:clamp(22px,2.6vw,32px);display:flex;flex-direction:column;gap:.6rem}
      .iso20022-mcp-page .mcp-client h3{font-size:1.12rem;margin:0}
      .iso20022-mcp-page .mcp-client-where{font-size:.88rem;color:var(--ink-soft);margin:0 0 .4rem}
      .iso20022-mcp-page .mcp-client p{margin:0}
      .iso20022-mcp-page .mcp-client .mcp-code{background:var(--card)}
      .iso20022-mcp-page .mcp-client-remote p{font-size:.92rem;color:var(--ink-soft)}
      .iso20022-mcp-page .mcp-clients-label{font-family:var(--spk-mono);font-size:.72rem;text-transform:uppercase;letter-spacing:.14em;color:var(--ink-faint);margin-block:2.2rem .2rem}
      .iso20022-mcp-page .mcp-clients-foot{margin-block-start:1.6rem;font-size:.86rem;color:var(--ink-faint)}
      @media (max-width:900px){.iso20022-mcp-page .mcp-clients,.iso20022-mcp-page .mcp-clients-3{grid-template-columns:1fr}}
      /* --- MCP hub: CSS-only install tabs (radio inputs; :checked drives
         the visible panel; radios stay keyboard-focusable). */
      .iso20022-mcp-page .mcp-tabs{margin-block-start:2.2rem}
      .iso20022-mcp-page .mcp-tab-in{position:absolute;width:1px;height:1px;margin:-1px;overflow:hidden;clip:rect(0 0 0 0);clip-path:inset(50%)}
      .iso20022-mcp-page .mcp-tab-labels{display:flex;flex-wrap:wrap;gap:.5rem;border-block-end:1px solid var(--spk-line);margin-block-end:1.2rem}
      .iso20022-mcp-page .mcp-tab-labels label{font-family:var(--spk-sans);font-size:.92rem;font-weight:500;color:var(--ink-soft);padding:.7em 1.1em;border-block-end:2px solid transparent;cursor:pointer}
      .iso20022-mcp-page .mcp-tab-labels label:hover{color:var(--ink)}
      .iso20022-mcp-page #mcp-tab-uvx:checked~.mcp-tab-labels label[for="mcp-tab-uvx"],.iso20022-mcp-page #mcp-tab-pip:checked~.mcp-tab-labels label[for="mcp-tab-pip"],.iso20022-mcp-page #mcp-tab-json:checked~.mcp-tab-labels label[for="mcp-tab-json"],.iso20022-mcp-page #mcp-tab-cursor:checked~.mcp-tab-labels label[for="mcp-tab-cursor"],.iso20022-mcp-page #mcp-tab-vscode:checked~.mcp-tab-labels label[for="mcp-tab-vscode"],.iso20022-mcp-page #mcp-tab-agents:checked~.mcp-tab-labels label[for="mcp-tab-agents"]{color:var(--ink);border-block-end-color:var(--spk-blue)}
      .iso20022-mcp-page #mcp-tab-uvx:focus-visible~.mcp-tab-labels label[for="mcp-tab-uvx"],.iso20022-mcp-page #mcp-tab-pip:focus-visible~.mcp-tab-labels label[for="mcp-tab-pip"],.iso20022-mcp-page #mcp-tab-json:focus-visible~.mcp-tab-labels label[for="mcp-tab-json"],.iso20022-mcp-page #mcp-tab-cursor:focus-visible~.mcp-tab-labels label[for="mcp-tab-cursor"],.iso20022-mcp-page #mcp-tab-vscode:focus-visible~.mcp-tab-labels label[for="mcp-tab-vscode"],.iso20022-mcp-page #mcp-tab-agents:focus-visible~.mcp-tab-labels label[for="mcp-tab-agents"]{outline:2px solid var(--focus-ring-color);outline-offset:2px}
      .iso20022-mcp-page .mcp-tab-panel{display:none}
      .iso20022-mcp-page #mcp-tab-uvx:checked~#mcp-panel-uvx,.iso20022-mcp-page #mcp-tab-pip:checked~#mcp-panel-pip,.iso20022-mcp-page #mcp-tab-json:checked~#mcp-panel-json,.iso20022-mcp-page #mcp-tab-cursor:checked~#mcp-panel-cursor,.iso20022-mcp-page #mcp-tab-vscode:checked~#mcp-panel-vscode,.iso20022-mcp-page #mcp-tab-agents:checked~#mcp-panel-agents{display:block}
      .iso20022-mcp-page .mcp-tab-note{margin-block-start:.9rem;font-size:.9rem;color:var(--ink-soft)}
      /* --- MCP hub: captured tool-schema viewer. Canonical .qa accordion
         (marker, hairline rows, width and typography come from the shared
         .qa-item rules); the hub only adds the three-part summary layout:
         tool name chip + one-line brief. */
      .iso20022-mcp-page .mcp-schemas{margin-block-start:2.2rem}
      .iso20022-mcp-page .mcp-schema > summary .spk-mono{font-size:1rem;flex:none}
      .iso20022-mcp-page .mcp-schema-sum{font-size:.9rem;font-weight:400;color:var(--ink-soft);overflow:hidden;text-overflow:ellipsis;white-space:nowrap;flex:1}
      .iso20022-mcp-page .mcp-schema-body p{font-size:.92rem;color:var(--ink-soft);max-width:72ch;margin-block-end:.9rem}
      .iso20022-mcp-page .mcp-props{list-style:none;margin:0;padding:0}
      .iso20022-mcp-page .mcp-props li{display:grid;grid-template-columns:minmax(110px,max-content) max-content 1fr;gap:.4rem 1.2rem;font-size:.88rem;padding-block:.5em;border-block-start:1px solid var(--spk-line)}
      .iso20022-mcp-page .mcp-prop-type{font-family:var(--spk-mono);font-size:.72rem;color:var(--ink-faint);text-transform:uppercase;letter-spacing:.06em}
      .iso20022-mcp-page .mcp-prop-desc{color:var(--ink-soft)}
      .iso20022-mcp-page .mcp-props-none{font-size:.88rem;color:var(--ink-faint)}
      .iso20022-mcp-page .mcp-schema-note{margin-block-start:1.4rem;font-size:.86rem;color:var(--ink-faint)}
      @media (max-width:640px){.iso20022-mcp-page .mcp-props li{grid-template-columns:1fr;gap:.15rem}.iso20022-mcp-page .mcp-schema-sum{display:none}}
      /* --- MCP hub: hero terminal (corral-README-style animated session).
         CSS-only: typed lines clip their width with steps(); output lines
         fade in on a delay; prefers-reduced-motion shows the finished
         session statically. Real selectable text, so the hero needs no
         1920w webp and the LCP candidate becomes the h1 headline.
         Theme-invariant GitHub-dark palette, all pairs AAA on #0d1117:
         #f0f6fc 17.39:1, #9ea7b3 7.78:1, #7ee787 12.32:1, #79c0ff 9.73:1;
         title bar #c9d1d9 on #161b22 11.21:1.
         Typed-line ch widths are len(text) incl. the prompt glyph and MUST
         match _TERM_LINES in build_iso20022_mcp.py: 72ch / 17ch / 83ch. */
      .iso20022-mcp-page .mcp-term{margin:0;background:#0d1117;border:1px solid #30363d;border-radius:18px;overflow:hidden;box-shadow:0 24px 60px -32px rgba(13,27,42,.45)}
      .iso20022-mcp-page .mcp-term-bar{display:flex;align-items:center;gap:8px;background:#161b22;border-block-end:1px solid #30363d;padding:12px 16px}
      .iso20022-mcp-page .mcp-term-dot{width:12px;height:12px;border-radius:50%;background:#30363d;flex:none}
      .iso20022-mcp-page .mcp-term-title{font-family:var(--spk-mono);font-size:.76rem;letter-spacing:.04em;color:#c9d1d9;margin-inline-start:8px}
      .iso20022-mcp-page .mcp-term-body{margin:0;padding:clamp(18px,2.4vw,30px);overflow-x:auto;background:transparent;border:0}
      .iso20022-mcp-page .mcp-term-body code{display:block;font-family:var(--spk-mono);font-size:clamp(.78rem,1.1vw,.92rem);line-height:1.9;color:#f0f6fc;background:transparent;padding:0;white-space:pre}
      .iso20022-mcp-page .mcp-tl{display:block;min-width:0}
      .iso20022-mcp-page .mcp-tl-ps{color:#7ee787}
      .iso20022-mcp-page .mcp-tl-ask .mcp-tl-ps{color:#79c0ff}
      .iso20022-mcp-page .mcp-tl-out{color:#9ea7b3}
      .iso20022-mcp-page .mcp-tl-ok{color:#7ee787}
      .iso20022-mcp-page .mcp-tl-caret::after{content:"\258B";color:#79c0ff;animation:mcpblink 1.1s step-end infinite}
      @keyframes mcptype{from{width:0}to{width:var(--tw)}}
      @keyframes mcpfade{from{opacity:0}to{opacity:1}}
      @keyframes mcpblink{50%{opacity:0}}
      .iso20022-mcp-page .mcp-tl-typed{overflow:hidden;white-space:nowrap;width:var(--tw);animation:mcptype var(--td) steps(var(--ts),end) both;animation-delay:var(--ta)}
      .iso20022-mcp-page .mcp-tl-fade{animation:mcpfade .3s ease both;animation-delay:var(--ta)}
      .iso20022-mcp-page .mcp-tl-t1{--tw:72ch;--ts:72;--td:1.9s;--ta:.4s}
      .iso20022-mcp-page .mcp-tl-t2{--tw:17ch;--ts:17;--td:.6s;--ta:2.7s}
      .iso20022-mcp-page .mcp-tl-f3{--ta:3.5s}
      .iso20022-mcp-page .mcp-tl-t3b{--tw:8ch;--ts:8;--td:.5s;--ta:4.2s}
      .iso20022-mcp-page .mcp-tl-t4{--tw:83ch;--ts:83;--td:2.2s;--ta:5.1s}
      .iso20022-mcp-page .mcp-tl-f5{--ta:7.6s}
      .iso20022-mcp-page .mcp-tl-f6{--ta:8.3s}
      @media (prefers-reduced-motion:reduce){.iso20022-mcp-page .mcp-tl-typed,.iso20022-mcp-page .mcp-tl-fade{animation:none;width:auto;opacity:1}.iso20022-mcp-page .mcp-tl-caret::after{animation:none}}
"""

# Page-scoped CSS for /trust/: Economist-Pro-solutions-page anatomy on the
# site's tokens. /trust/ forks the BUILT articles page as its shell
# (build_trust.py), so these rules ride articles.html next to
# SPEAKING_MCP_HUB_CSS. Scoped to .trust-page / tr- prefixes.
# Text pairs, all AAA (>= 7:1), light/dark:
#   --ink on --bg 16.83/19.29, --ink on --bg-alt 14.92/15.46,
#   --ink-soft on --bg 11.35/14.22, --ink-soft on --bg-alt 10.06/11.40,
#   --ink-soft on --card 11.35/12.24, --ink-mute on --bg 7.99/9.75,
#   --ink-mute on --bg-alt 7.08/7.81, --accent on --bg 8.95/11.10,
#   --accent on --bg-alt 7.93/8.89, pill/copy chip (#fff on --accent) 8.95,
#   dark pill (#000 on #8cc0ff) 11.10.
TRUST_CSS = r"""      /* ============================================================
         /trust/: enterprise governance & trust. Full-width band rhythm
         (tinted hero, white, tinted, ...), left-aligned, one measure.
         ============================================================ */
      main.content:has(.trust-page){padding:0}
      .trust-page{font-family:var(--type-body);color:var(--ink);line-height:1.6}
      .trust-page .tr-wrap{max-width:1200px;margin-inline:auto;padding-inline:clamp(22px,5vw,64px)}
      .trust-page section{padding-block:clamp(72px,9vw,112px)}
      .trust-page .tr-tint{background:var(--bg-alt)}
      .trust-page .tr-kicker{display:block;font-size:13px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--accent);margin:0 0 16px;max-width:none}
      .trust-page h1{font-size:clamp(40px,5.4vw,68px);font-weight:700;letter-spacing:-.022em;line-height:1.04;color:var(--ink);margin:0 0 22px;max-width:18ch;text-wrap:balance}
      .trust-page h2{font-size:clamp(28px,3.4vw,42px);font-weight:600;letter-spacing:-.018em;line-height:1.1;color:var(--ink);margin:0;max-width:24ch;text-wrap:balance}
      .trust-page h3{font-size:17px;line-height:1.3;font-weight:600;color:var(--ink);margin:0 0 8px;max-width:none}
      .trust-page p{color:var(--ink-soft)}
      .trust-page .tr-lede{font-size:clamp(17px,1.6vw,20px);line-height:1.55;color:var(--ink-soft);margin:0 0 30px;max-width:62ch}
      .trust-page .tr-head{margin:0 0 clamp(32px,4vw,48px)}
      .trust-page .tr-cta{display:flex;flex-wrap:wrap;align-items:center;gap:14px 18px;margin:0}
      /* hero band */
      .trust-page .tr-hero{padding-block:clamp(88px,11vw,136px) clamp(80px,10vw,120px)}
      /* provenance: balanced 4-across icon cards, equal geometry
         (icon / heading / body / action zones; action pinned to the foot) */
      .trust-page .tr-cards{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:clamp(14px,1.5vw,20px)}
      .trust-page .tr-card{background:var(--card);border:1px solid var(--border);border-radius:16px;padding:clamp(22px,2.2vw,30px);display:flex;flex-direction:column;min-width:0}
      .trust-page .tr-card-icon{display:block;width:28px;height:28px;color:var(--accent);margin:0 0 16px;flex:none}
      .trust-page .tr-card-icon svg{width:100%;height:100%;stroke:currentColor;fill:none}
      .trust-page .tr-card h3{text-wrap:balance}
      .trust-page .tr-card p{font-size:14.5px;line-height:1.55;color:var(--ink-soft);margin:0;max-width:none}
      .trust-page .tr-card-act{margin-block-start:auto;padding-block-start:16px;font-size:14.5px}
      .trust-page .tr-card pre{margin:14px 0 0;background:var(--bg-alt);border:1px solid var(--rule);border-radius:10px;padding:12px 14px;font-size:12.5px;line-height:1.6;color:var(--ink);white-space:pre-wrap;word-break:break-word;max-width:none}
      .trust-page .tr-copy{border:0;cursor:pointer;font-family:inherit}
      @media (max-width:1100px){.trust-page .tr-cards{grid-template-columns:repeat(2,minmax(0,1fr))}}
      @media (max-width:640px){.trust-page .tr-cards{grid-template-columns:1fr}}
      /* preview panel: two content-sampler cards with imagery */
      .trust-page .tr-preview{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:clamp(16px,2vw,24px)}
      .trust-page .tr-prev-card{background:var(--card);border:1px solid var(--border);border-radius:18px;overflow:hidden;display:flex;flex-direction:column;min-width:0}
      .trust-page .tr-prev-card img{width:100%;aspect-ratio:16/10;object-fit:cover;display:block}
      .trust-page .tr-prev-img-b{object-position:center bottom}
      .trust-page .tr-prev-body{padding:clamp(22px,2.4vw,32px);display:flex;flex-direction:column;flex:1}
      .trust-page .tr-prev-body .tr-kicker{margin-block-end:10px}
      .trust-page .tr-prev-body h3{font-size:clamp(19px,1.8vw,23px);margin:0 0 10px;text-wrap:balance}
      .trust-page .tr-prev-body h3 a{color:var(--ink);text-decoration:none}
      .trust-page .tr-prev-body h3 a:hover{color:var(--accent)}
      .trust-page .tr-prev-body p{font-size:15px;line-height:1.55;margin:0;max-width:none}
      .trust-page .tr-prev-more{margin-block-start:auto;padding-block-start:16px;font-size:14.5px;font-weight:600}
      .trust-page .tr-prev-more a{color:var(--accent);text-decoration:none}
      .trust-page .tr-prev-more a:hover{text-decoration:underline;text-underline-offset:3px}
      @media (max-width:900px){.trust-page .tr-preview{grid-template-columns:1fr}}
      /* side-by-side heading + content bands (licensing / governance /
         recognition) */
      .trust-page .tr-cols{display:grid;grid-template-columns:minmax(0,4fr) minmax(0,7fr);gap:clamp(32px,5vw,72px);align-items:start}
      .trust-page .tr-col-head .tr-lede{margin:18px 0 0;font-size:16.5px}
      @media (max-width:960px){.trust-page .tr-cols{grid-template-columns:minmax(0,1fr);gap:32px}}
      /* licensing table: full width of its column; the wrapper scrolls on
         narrow viewports instead of widening the page */
      .trust-page .tr-table-wrap{overflow-x:auto}
      .trust-page .tr-table{width:100%;border-collapse:collapse;font-size:15px;line-height:1.5;margin:0}
      .trust-page .tr-table th{text-align:start}
      .trust-page .tr-table thead th{font-size:12px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-mute);padding:0 20px 12px 0;border-block-end:1px solid var(--border)}
      .trust-page .tr-table tbody th,.trust-page .tr-table tbody td{padding:15px 20px 15px 0;border-block-end:1px solid var(--rule);vertical-align:top;font-weight:400;color:var(--ink-soft)}
      .trust-page .tr-table tbody th a{font-weight:600}
      .trust-page .tr-note{font-size:15px;line-height:1.6;margin:22px 0 0;max-width:none}
      /* governance: left-aligned styled list items */
      .trust-page .tr-gov-list{list-style:none;margin:0;padding:0;display:grid;gap:14px;max-width:none}
      .trust-page .tr-gov-list li{background:var(--card);border:1px solid var(--rule);border-radius:14px;padding:clamp(18px,2vw,24px);font-size:15px;line-height:1.6;color:var(--ink-soft);text-align:start;max-width:none}
      .trust-page .tr-gov-list li strong{display:block;color:var(--ink);font-weight:600;margin-block-end:4px}
      /* recognition rows: title / org / date / role columns */
      .trust-page .tr-rec{list-style:none;margin:0;padding:0;max-width:none}
      .trust-page .tr-rec li{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,3fr) max-content minmax(0,3fr);gap:6px 24px;align-items:baseline;padding-block:18px;border-block-start:1px solid var(--rule)}
      .trust-page .tr-rec li:last-child{border-block-end:1px solid var(--rule)}
      .trust-page .tr-rec-title{font-size:16px;font-weight:600;line-height:1.4}
      .trust-page .tr-rec-org{font-size:14.5px;color:var(--ink-soft)}
      .trust-page .tr-rec-date{font-size:13px;color:var(--ink-mute);font-variant-numeric:tabular-nums;white-space:nowrap}
      .trust-page .tr-rec-role{font-size:13px;color:var(--ink-mute)}
      @media (max-width:760px){.trust-page .tr-rec li{grid-template-columns:1fr}.trust-page .tr-rec-date{white-space:normal}}
      /* end CTA band */
      .trust-page .tr-final{text-align:center}
      .trust-page .tr-final h2{margin-inline:auto}
      .trust-page .tr-final .tr-cta{justify-content:center;margin-block-start:28px}
"""

# Page-scoped CSS for the /iso20022-mcp-reference/ tool catalog
# (layout: story). Rows ride the canonical .qa accordion; this adds the
# three-part summary layout and the parameter table.
MCP_REFERENCE_CSS = r"""      /* --- ISO 20022 MCP reference: live-captured tool catalog. Tool rows
         ride the canonical .qa accordion (shared marker, full-width hairline
         rows, sans summary typography); the reference adds only the
         three-part summary layout and the parameter table. All text uses the
         AAA token pairs (--ink / --ink-soft / --ink-mute / --ink-faint on
         --bg or --bg-alt, each >= 7:1 in both themes). */
      .ref-totals{font-size:15.5px;color:var(--ink-soft)}
      .ref-index{margin:32px 0 0}
      .ref-index-list{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
      .ref-index-item{margin:0}
      main.content .ref-index-link{display:flex;flex-direction:column;gap:6px;height:100%;padding:18px;border:1px solid var(--border);border-radius:12px;color:var(--ink);text-decoration:none;transition:border-color .15s ease}
      main.content .ref-index-link:hover{border-color:var(--accent)}
      .ref-index-name code{font-family:var(--type-mono,ui-monospace,monospace);font-size:14px;color:var(--ink);background:transparent;padding:0;border:0}
      .ref-index-role{font-size:13px;line-height:1.5;color:var(--ink-soft)}
      .ref-index-count{font-family:var(--type-mono,ui-monospace,monospace);font-size:11px;letter-spacing:.04em;color:var(--ink-mute)}
      @media (max-width:860px){.ref-index-list{grid-template-columns:1fr 1fr}}
      @media (max-width:560px){.ref-index-list{grid-template-columns:1fr}}
      .ref-capture{font-family:var(--type-mono,ui-monospace,monospace);font-size:12.5px;line-height:1.7;color:var(--ink-mute);margin:8px 0 20px}
      .ref-capture code{font-family:inherit;font-size:inherit;background:transparent;padding:0;border:0}
      .ref-tools{margin:0 0 8px}
      .ref-tool > summary .ref-tool-name{flex:none}
      .ref-tool > summary .ref-tool-name code{font-family:var(--type-mono,ui-monospace,monospace);font-size:15px;color:inherit;background:transparent;padding:0;border:0}
      .ref-tool-brief{flex:1;min-width:0;font-size:14px;font-weight:400;color:var(--ink-soft);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
      .ref-tool-brief code,.ref-tool-desc code{background:transparent;padding:0;border:0}
      .ref-tool-meta{flex:none;font-family:var(--type-mono,ui-monospace,monospace);font-size:11px;letter-spacing:.04em;text-transform:uppercase;font-weight:400;color:var(--ink-mute);white-space:nowrap}
      @media (max-width:720px){.ref-tool-brief,.ref-tool-meta{display:none}}
      main.content .ref-tool-desc{margin:0 0 14px;font-size:14.5px;line-height:1.6;color:var(--ink-soft);max-width:none}
      .ref-noparams{margin:0;font-size:14px;color:var(--ink-mute)}
      .ref-params-wrap{overflow-x:auto}
      .ref-params{width:100%;border-collapse:collapse;font-size:14px;line-height:1.55}
      .ref-params th{font-family:var(--type-mono,ui-monospace,monospace);font-size:11px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-mute);text-align:start;padding:8px 16px 8px 0;border-bottom:1px solid var(--border)}
      .ref-params td{padding:10px 16px 10px 0;border-bottom:1px solid var(--rule);color:var(--ink-soft);vertical-align:top}
      .ref-params td code{background:transparent;padding:0;border:0;font-size:13px}
      .ref-req{font-family:var(--type-mono,ui-monospace,monospace);font-size:11px;letter-spacing:.06em;text-transform:uppercase;white-space:nowrap}
      .ref-req-required{color:var(--ink);font-weight:600}
      .ref-req-optional{color:var(--ink-mute)}
"""

# Page-scoped CSS for /iso20022-mcp-docs/ (layout: story): FMP-density x
# Apple-Partner-Network layout for the four-chapter tutorial. Scoped to
# .docs-shell / .docs-* / .tut-* classes, which exist only in that post's
# markup, so the other story pages are untouched. The tut-path progress
# rail becomes a sticky side rail at >=1100px (CSS-only, position:sticky);
# chapter sections use the full content width with side-by-side prose/code
# (.docs-split) and 2x2 / 3-across card grids (.docs-cardlist).
# Text pairs, all AAA (>= 7:1), light/dark: --ink 16.83/19.29,
# --ink-soft on --bg 11.35/14.22, --ink-soft on --bg-alt 10.06/11.40,
# --ink-mute on --bg 7.99/9.75, --ink-mute on --bg-alt 7.08/7.81,
# --accent on --bg 8.95/11.10, --accent on --card 8.95/9.56.
MCP_DOCS_CSS = r"""      /* --- ISO 20022 MCP docs: sticky-rail tutorial layout ------------- */
      main.content:has(.docs-shell) .wrap{max-width:var(--max-wide)}
      .docs-shell{margin-block-start:clamp(20px,3vw,40px)}
      .docs-rail{padding:0}
      .docs-rail .tut-path{list-style:none;margin:0;padding:0;display:grid;gap:12px;max-width:none}
      .tut-path-item{margin:0}
      /* main.content .docs-rail prefix = (0,3,2): beats the shell's
         `main.content :is(p,li,...) a:not([class])` underline rule (0,2,3) */
      main.content .docs-rail .tut-path-item a{display:block;height:100%;padding:16px 18px;border:1px solid var(--rule);border-radius:14px;background:var(--card);color:var(--ink);text-decoration:none;transition:border-color .15s ease}
      main.content .docs-rail .tut-path-item a:hover{border-color:var(--accent)}
      .tut-path-chapter{display:block;font-size:11px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--accent);margin-block-end:6px}
      .tut-path-title{display:block;font-size:15.5px;font-weight:600;line-height:1.3;color:var(--ink);margin-block-end:4px}
      .tut-path-sub{display:block;font-size:13px;line-height:1.5;color:var(--ink-soft);margin-block-end:10px}
      .tut-mins{display:inline-block;font-size:11px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:var(--ink-mute)}
      @media (min-width:640px) and (max-width:1099.98px){.docs-rail .tut-path{grid-template-columns:1fr 1fr}}
      @media (min-width:1100px){
        .docs-shell{display:grid;grid-template-columns:264px minmax(0,1fr);gap:clamp(36px,4vw,72px);align-items:start}
        .docs-rail{position:sticky;top:calc(var(--nav-h,64px) + 24px);max-height:calc(100vh - var(--nav-h,64px) - 48px);overflow-y:auto}
      }
      .docs-flow{min-width:0}
      /* chapter heads: full-width, left-aligned, hairline rhythm */
      .docs-flow .tut-chapter-head{margin:clamp(56px,7vw,88px) 0 0;padding-block-start:clamp(28px,3.4vw,44px);border-block-start:1px solid var(--border);text-align:start;scroll-margin-block-start:calc(var(--nav-h,64px) + 16px)}
      .docs-flow .tut-chapter-head:first-child{margin-block-start:0;padding-block-start:0;border-block-start:0}
      .tut-chapter-num{display:inline-flex;align-items:center;justify-content:center;width:44px;height:44px;border:1px solid var(--border);border-radius:50%;font-size:18px;font-weight:600;color:var(--ink-mute);margin-block-end:18px}
      .docs-flow .tut-chapter-head .cat-headline{font-size:clamp(30px,3.6vw,44px)}
      .docs-flow .tut-chapter-head .cat-lede{max-width:66ch !important}
      .docs-flow .tut-chapter-head .tut-mins{margin-block-start:12px}
      /* section heads: left-aligned within the flow column */
      .docs-flow .cat-section-head{text-align:start;margin:clamp(40px,5vw,60px) 0 22px;max-width:none}
      .docs-flow .cat-section-head .cat-headline{font-size:clamp(24px,2.6vw,32px)}
      .docs-flow .cat-section-head .cat-lede{max-width:72ch !important}
      .docs-flow .story-why{margin-block:18px 26px}
      .docs-flow section.newsroom{margin:0;padding:0;max-width:none}
      .docs-flow .story-intro{font-size:16.5px;margin-block:18px 0}
      /* code: comfortable measure instead of a full-bleed strip */
      .docs-flow pre{background:var(--bg-alt);border:1px solid var(--rule);border-radius:14px;padding:18px 20px;overflow-x:auto;max-width:860px;font-size:13.5px;line-height:1.65;color:var(--ink)}
      .docs-flow pre pre{background:transparent;border:0;border-radius:0;padding:0;margin:0;max-width:none}
      .docs-flow pre code{background:transparent;padding:0;border:0}
      .docs-code-col{min-width:0}
      .docs-code-col pre{max-width:none}
      /* side-by-side: step prose left, code right at >=1100px */
      @media (min-width:1100px){
        .docs-flow section.docs-split{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.15fr);gap:clamp(24px,3vw,48px);grid-auto-flow:dense;align-items:start}
        .docs-split > .cat-section-head{grid-column:1/-1}
        .docs-split > .docs-code-col{grid-column:2}
        .docs-split > .story-why,.docs-split > .story-intro{grid-column:1}
        .docs-split .story-why{margin-block:0}
      }
      /* informational bullet lists as card grids (2x2, or 3-across) */
      .docs-cardlist .story-why-list{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:clamp(14px,1.6vw,20px)}
      .docs-cards-3 .story-why-list{grid-template-columns:repeat(3,minmax(0,1fr))}
      .docs-cardlist .story-why-list li{background:var(--bg-alt);border-radius:16px;padding:clamp(20px,2vw,26px);padding-inline-start:clamp(20px,2vw,26px);max-width:none;font-size:15px;line-height:1.6;min-width:0}
      .docs-cardlist .story-why-list li::before{content:none}
      @media (max-width:900px){.docs-cardlist .story-why-list,.docs-cards-3 .story-why-list{grid-template-columns:1fr}}
      /* client cards: FMP-style dataset-grid density, 3-across at wide */
      .docs-client-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:clamp(14px,1.6vw,20px);margin-block-start:20px}
      .docs-client{min-width:0;background:var(--bg-alt);border-radius:16px;padding:clamp(20px,2vw,26px);display:flex;flex-direction:column;gap:10px;margin:0}
      .docs-client h4{margin:0;font-size:17px;line-height:1.3;color:var(--ink)}
      .docs-client p{font-size:14.5px;line-height:1.55;color:var(--ink-soft);margin:0;max-width:none}
      .docs-client pre{background:var(--card);border-color:var(--rule);margin:4px 0 0;max-width:none;font-size:12.5px}
      @media (max-width:1200px){.docs-client-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
      @media (max-width:720px){.docs-client-grid{grid-template-columns:1fr}}
"""


# Per-page Schema.org JSON-LD. Each non-home layout gets a single inline
# `application/ld+json` block. Person/Website nodes are identity-only refs (linked
# by @id back to the canonical entries on the home page) so Google and AI crawlers
# merge them into one knowledge graph.
PERSON_REF = '{"@id":"https://sebastienrousseau.com/#person"}'
SITE_REF = '{"@id":"https://sebastienrousseau.com/#website"}'
BLOG_REF = (
    '{"@type":"Blog","@id":"https://sebastienrousseau.com/articles/#blog",'
    '"name":"Articles by Sebastien Rousseau",'
    '"url":"https://sebastienrousseau.com/articles/"}'
)
BREADCRUMB = (
    ',{"@type":"BreadcrumbList","itemListElement":['
    '{"@type":"ListItem","position":1,"name":"Home","item":"https://sebastienrousseau.com/"},'
    '{"@type":"ListItem","position":2,"name":"{{title}}","item":"{{url}}"}'
    "]}"
)
# Dated posts (the "report" layout) live inside the /articles/ Blog graph,
# so their breadcrumb is three levels deep: Home > Articles > <post title>.
REPORT_BREADCRUMB = (
    ',{"@type":"BreadcrumbList","itemListElement":['
    '{"@type":"ListItem","position":1,"name":"Home","item":"https://sebastienrousseau.com/"},'
    '{"@type":"ListItem","position":2,"name":"Articles","item":"https://sebastienrousseau.com/articles/"},'
    '{"@type":"ListItem","position":3,"name":"{{title}}","item":"{{url}}"}'
    "]}"
)
IMAGE_OBJ = '{"@type":"ImageObject","url":"{{image}}","width":"{{image_width}}","height":"{{image_height}}"}'
# The article banner is the visual lead, and the right artwork for
# Article.image per Google's structured-data guidance. ``{{image}}`` was
# the small 162×162 author headshot — wrong shape for a social preview.
BANNER_OBJ = (
    '{"@type":"ImageObject","url":"{{banner}}","width":"{{banner_width}}",'
    '"height":"{{banner_height}}","caption":"{{banner_alt}}"}'
)
SPEAKABLE = (
    ',"speakable":{"@type":"SpeakableSpecification",'
    '"cssSelector":[".post-lead",".post-lead-tldr",".post-lead-takeaways",'
    '".article-toc",".author-card"]}'
)
# FAQ block for the publications hub (the "papers" layout, rendered at /research/
# since the 5-item nav re-architecture). Mirrors the on-page `<details class="qa-item">` accordion
# so AI crawlers (Google AI Overviews, Perplexity, ChatGPT) can cite the answers
# directly. Kept as a separate node so we don't pollute the CollectionPage entity.
PAPERS_FAQ = (
    ',{"@type":"FAQPage","@id":"{{url}}#faq","mainEntity":['
    '{"@type":"Question","name":"What kind of research and papers do you publish?",'
    '"acceptedAnswer":{"@type":"Answer","text":"Two strands sit side-by-side. Industry white papers, produced for organisations such as the Emerging Payments Association Asia (EPAA), examine structural shifts to payment infrastructure, most recently the impact of cryptographically-relevant quantum computing on wholesale and real-time settlement rails. Applied research papers, published independently, share reproducible engineering work, for example, real-time speech recognition on macOS using OpenAI Whisper and Metal Performance Shaders."}},'
    '{"@type":"Question","name":"Who is the intended audience?",'
    '"acceptedAnswer":{"@type":"Answer","text":"Heads of payments, CISOs and senior architects in Tier-1 banks, central banks, payment system operators and scheme owners. The applied research is written for engineers and product leaders building on top of large language models, on-device AI, and quantum-resistant cryptography."}},'
    '{"@type":"Question","name":"Are the white papers free to read?",'
    '"acceptedAnswer":{"@type":"Answer","text":"The EPAA Quantum-Safe Payments paper is a free 18.9 MB PDF download from emergingpaymentsasia.org. The independent research paper on real-time speech recognition with OpenAI Whisper and Metal Performance Shaders is licensed and available for individual purchase at $49.00 (English, PDF, ~95 KB). One copy per buyer; downloads are personal-use only."}},'
    '{"@type":"Question","name":"May I cite or quote from these papers?",'
    '"acceptedAnswer":{"@type":"Answer","text":"Yes. Short quotations with attribution are welcome under fair-dealing or fair-use norms. For EPAA papers, cite the EPAA as publisher with the working group, year and PDF URL. For independent research papers, cite as Rousseau, S. (year). Title. Self-published. with the canonical URL."}},'
    '{"@type":"Question","name":"Can I commission a paper or speak at an event?",'
    '"acceptedAnswer":{"@type":"Answer","text":"Yes, limited and by selection. Commissioned work focuses on wholesale payments, ISO 20022 migration, post-quantum cryptography for financial services, and applied AI in banking. Speaking engagements at industry conferences, central-bank fora, and regulator round-tables are considered case-by-case."}},'
    '{"@type":"Question","name":"How do I follow new publications?",'
    '"acceptedAnswer":{"@type":"Answer","text":"New papers and research notes are announced first through the site RSS feed at /rss.xml and the Banking On Quantum newsletter at news.bankingonquantum.com, which covers post-quantum cryptography, central-bank policy, and the migration roadmap across major payment schemes."}}'
    "]}"
)
# FAQ block for /projects/. Mirrors the on-page accordion so AI engines can
# cite licence, production-readiness, contribution and commercial-support
# answers directly.
PROJECTS_FAQ = (
    ',{"@type":"FAQPage","@id":"{{url}}#faq","mainEntity":['
    '{"@type":"Question","name":"What licence are these projects released under?",'
    '"acceptedAnswer":{"@type":"Answer","text":"Most projects are dual-licensed under MIT and Apache-2.0, the standard for the Rust ecosystem, which gives commercial users explicit patent rights as well as permissive redistribution. A small number of clients\' tools are released under Apache-2.0 only. The licence file at the root of each repository is the authoritative source."}},'
    '{"@type":"Question","name":"Are these projects production-ready?",'
    '"acceptedAnswer":{"@type":"Answer","text":"Many are. pain001 is used by banks and payment-service providers to automate ISO 20022 file creation. KyberLib tracks the NIST FIPS 203 specification and ships test vectors. Each repository\'s README and CI badges will tell you the current status; if you need a specific guarantee for production use, get in touch."}},'
    '{"@type":"Question","name":"How can I contribute or report an issue?",'
    '"acceptedAnswer":{"@type":"Answer","text":"Every project has a public GitHub repository under github.com/sebastienrousseau. Open an issue describing the problem (a minimal reproducer helps) or a pull request linked to an issue. Contributions are governed by the Developer Certificate of Origin and require signed commits."}},'
    '{"@type":"Question","name":"Can I use these libraries in a regulated banking environment?",'
    '"acceptedAnswer":{"@type":"Answer","text":"Yes, with the usual caveats. The libraries are independent open-source work, not a regulated product. Run your normal supply-chain, security, and dependency-review processes, such as vendoring through your internal mirror, scanning with SBOM tools, and pinning by Git SHA or cryptographic hash, before deploying to production payment infrastructure."}},'
    '{"@type":"Question","name":"Do you offer commercial support or consulting?",'
    '"acceptedAnswer":{"@type":"Answer","text":"Yes, on a selective basis. Engagements focus on ISO 20022 migration, post-quantum cryptography migration roadmaps, and applied AI in financial services. Get in touch with a short brief, your timeline and any constraints."}},'
    '{"@type":"Question","name":"How do I follow new releases?",'
    '"acceptedAnswer":{"@type":"Answer","text":"New papers and research notes are announced first through the site RSS feed and the Banking On Quantum newsletter, which covers post-quantum cryptography, central-bank policy, and the migration roadmap across major payment schemes. Individual repositories also publish releases on GitHub, which you can watch directly."}}'
    "]}"
)


# Each schema is wrapped in an @graph array so we can attach the BreadcrumbList
# as a second top-level node without breaking the JSON envelope. ``breadcrumb``
# defaults to the two-level form (Home > <page>); the "report" layout uses
# REPORT_BREADCRUMB to slot Articles as the parent collection.
def WRAP(body: str, extra: str = "", breadcrumb: str = BREADCRUMB) -> str:
    return '"@graph":[{' + body + "}" + breadcrumb + extra + "]"


SCHEMA_TEMPLATES = {
    "default": WRAP(
        '"@type":"WebPage","name":"{{title}}","description":"{{description}}","url":"{{url}}","inLanguage":"{{hreflang}}","image":'
        + IMAGE_OBJ
        + ',"author":'
        + PERSON_REF
        + ',"publisher":'
        + PERSON_REF
        + ',"isPartOf":'
        + SITE_REF
    ),
    "about": WRAP(
        '"@type":"ProfilePage","name":"{{title}}","description":"{{description}}","url":"{{url}}","inLanguage":"{{hreflang}}","mainEntity":'
        + PERSON_REF
        + ',"isPartOf":'
        + SITE_REF
        + ',"dateCreated":"2007-01-01","dateModified":"{{last_reviewed}}"'
    ),
    "contact": WRAP(
        '"@type":"ContactPage","name":"{{title}}","description":"{{description}}","url":"{{url}}","inLanguage":"{{hreflang}}","mainEntity":'
        + PERSON_REF
        + ',"isPartOf":'
        + SITE_REF
    ),
    "articles": WRAP(
        '"@type":"CollectionPage","name":"{{title}}","description":"{{description}}","url":"{{url}}","inLanguage":"{{hreflang}}","about":"Banking, payments, AI and post-quantum cryptography","author":'
        + PERSON_REF
        + ',"isPartOf":'
        + SITE_REF
    ),
    "papers": WRAP(
        '"@type":"CollectionPage","name":"{{title}}","description":"{{description}}","url":"{{url}}","inLanguage":"{{hreflang}}","about":"Research papers and white papers on wholesale payments and post-quantum cryptography","author":'
        + PERSON_REF
        + ',"isPartOf":'
        + SITE_REF,
        PAPERS_FAQ,
    ),
    "projects": WRAP(
        '"@type":"CollectionPage","name":"{{title}}","description":"{{description}}","url":"{{url}}","inLanguage":"{{hreflang}}","about":"Open-source projects applied to finance and banking","author":'
        + PERSON_REF
        + ',"isPartOf":'
        + SITE_REF,
        PROJECTS_FAQ,
    ),
    "playlist": WRAP(
        '"@type":"CollectionPage","name":"{{title}}","description":"{{description}}","url":"{{url}}","inLanguage":"{{hreflang}}","about":"Curated Spotify playlists","author":'
        + PERSON_REF
        + ',"isPartOf":'
        + SITE_REF
    ),
    "report": WRAP(
        '"@type":"BlogPosting","headline":"{{title}}","description":"{{description}}","image":'
        + BANNER_OBJ
        + ',"url":"{{url}}","datePublished":"{{item_pub_date}}","dateModified":"{{last_reviewed}}",'
        '"inLanguage":"{{hreflang}}","keywords":"{{keywords}}","articleSection":"{{category}}",'
        '"author":' + PERSON_REF + ',"publisher":' + PERSON_REF + ","
        '"mainEntityOfPage":{"@type":"WebPage","@id":"{{url}}"},'
        '"isPartOf":' + BLOG_REF + SPEAKABLE,
        breadcrumb=REPORT_BREADCRUMB,
    ),
}


def schema_for(kind: str) -> str:
    body = SCHEMA_TEMPLATES.get(kind, SCHEMA_TEMPLATES["default"])
    return (
        '    <script type="application/ld+json">\n'
        '{"@context":"https://schema.org",' + body + "}\n"
        "    </script>\n"
    )


def inject_schema(html: str, kind: str) -> str:
    """Insert the JSON-LD block before the first existing /main.js script tag."""
    marker = '<script src="/main.js" defer></script>'
    return html.replace(marker, schema_for(kind) + marker, 1)


# Standard page hero used by most layouts.
PAGE_HERO_MAIN = """    <section class="ap-hero">
      <h1>{{name}}</h1>
      <p class="sub">{{subtitle}}</p>
    </section>

    <main id="main" class="content ap-section">
      <div class="wrap">{{content}}</div>
    </main>

"""


def page_layout() -> str:
    return TOP + PAGE_HERO_MAIN + BOTTOM


# /projects/ hero: the rotating animated title IS the page H1 (no duplicate
# block in the body). Static layout markup — not a {{var}}, so unaffected by
# template escaping. The last word repeats so the CSS loop resets seamlessly.
PROJECT_HERO_MAIN = """    <section class="ap-hero">
      <h1 class="rotating-title" aria-label="Open source for banks, financial institutions, enterprise and small business.">
        <span class="rotating-title-lead">Open source for</span>
        <span class="rotating-title-mask" aria-hidden="true"><span class="rotating-title-words"><span><span class="rt-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="m12 2 9 5H3z"/><path d="M5 10v8m4-8v8m6-8v8m4-8v8M3 21h18"/></svg></span>banks.</span><span><span class="rt-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3c2.5 2.5 3.5 6 3.5 9s-1 6.5-3.5 9c-2.5-2.5-3.5-6-3.5-9s1-6.5 3.5-9Z"/></svg></span>financial institutions.</span><span><span class="rt-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 21V4a1 1 0 0 1 1-1h10a1 1 0 0 1 1 1v17"/><path d="M3 21h18"/><path d="M10 7h4M10 11h4M10 15h4"/></svg></span>enterprise.</span><span><span class="rt-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="m4 9 1.2-5h13.6L20 9"/><path d="M5 9v11a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V9"/><path d="M9 21v-6h6v6"/></svg></span>small business.</span><span><span class="rt-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="m12 2 9 5H3z"/><path d="M5 10v8m4-8v8m6-8v8m4-8v8M3 21h18"/></svg></span>banks.</span></span></span>
      </h1>
      <p class="sub">{{subtitle}}</p>
      <p class="ap-hero-cta"><a class="pill" href="/contact/index.html">Talk to us</a> <a class="pill ghost" href="#catalog">Browse all products</a></p>
    </section>

    <main id="main" class="content ap-section">
      <div class="wrap">{{content}}</div>
    </main>

"""


def project_layout() -> str:
    return TOP + PROJECT_HERO_MAIN + BOTTOM


# /projects-*/ story pages: apple.com/government-style hero. The banner is a
# full-bleed image with the title and subtitle overlaid in white over a scrim.
# It sits outside the content wrap, so it is full width without a 100vw hack.
STORY_HERO_MAIN = """    <section class="story-hero">
      <img class="story-hero-img" src="{{banner}}" alt="{{banner_alt}}" loading="eager" fetchpriority="high" decoding="async" />
      <div class="story-hero-inner">
        <h1>{{name}}</h1>
        <p class="story-hero-sub">{{subtitle}}</p>
      </div>
    </section>

    <main id="main" class="content ap-section">
      <div class="wrap">{{content}}</div>
    </main>

"""


def story_layout() -> str:
    html = TOP + STORY_HERO_MAIN + BOTTOM
    return html.replace(
        "    </style>", MCP_REFERENCE_CSS + MCP_DOCS_CSS + "    </style>"
    )


def contact_layout() -> str:
    body = """    <section class="ap-hero">
      <span class="eyebrow">Contact</span>
      <h1>{{title}}</h1>
      <p class="sub">{{subtitle}}</p>
    </section>

    <section class="proof-rail contact-promise" aria-label="What to expect" data-reveal>
      <div class="kpi-cell"><span class="kpi-cell-value">&lt; 48 h</span><span class="kpi-cell-label">Typical first response</span></div>
      <div class="kpi-cell"><span class="kpi-cell-value">London</span><span class="kpi-cell-label">Time zone · UK + EU + APAC overlap</span></div>
      <div class="kpi-cell"><span class="kpi-cell-value">Tier-1</span><span class="kpi-cell-label">Banking · payments · post-quantum</span></div>
    </section>

    <main id="main" class="content ap-section">
      <div class="wrap contact-wrap">
        <div class="contact-layout" data-reveal>
          <div class="contact-form-col">
            <p class="lede">{{content}}</p>
            <form class="ap-form" action="https://formspree.io/f/{{form-id}}" method="POST">
              <fieldset>
              <legend class="visually-hidden">Send a message</legend>
              <div class="ap-form-row">
                <label for="sender">Name</label>
                <input type="text" id="sender" name="name" autocomplete="name" required />
              </div>
              <div class="ap-form-row">
                <label for="email">Email</label>
                <input type="email" id="email" name="email" autocomplete="email" required />
              </div>
              <div class="ap-form-row">
                <label for="subject">Subject</label>
                <select id="subject" name="subject" required>
                  <option value="">Choose a subject</option>
                  <option value="business">Consulting / advisory engagement</option>
                  <option value="press">Press, podcast or speaking</option>
                  <option value="papers">White paper / research collaboration</option>
                  <option value="product">Open-source project question</option>
                  <option value="feedback">Editorial feedback</option>
                  <option value="support">Product support</option>
                  <option value="general">Something else</option>
                </select>
              </div>
              <div class="ap-form-row">
                <label for="message">Message</label>
                <textarea id="message" name="message" rows="6" required placeholder="A line about your bank, your role, and the question you're trying to answer."></textarea>
              </div>
              <div class="ap-form-row">
                <label class="visually-hidden" for="g-recaptcha-response">Google reCAPTCHA</label>
                <div class="g-recaptcha" data-sitekey="{{recaptcha}}"></div>
              </div>
              <div class="ap-form-row ap-form-actions">
                <button type="submit" class="pill no-chev">Send message</button>
              </div>
              </fieldset>
            </form>
          </div>
          <aside class="contact-aside" aria-label="Other ways to reach Sebastien">
            <h2 class="contact-aside-title">Faster paths</h2>
            <ul class="contact-aside-list">
              <li>
                <span class="contact-aside-eyebrow">Direct</span>
                <a href="mailto:contact@sebastienrousseau.com">contact@sebastienrousseau.com</a>
              </li>
              <li>
                <span class="contact-aside-eyebrow">Verified</span>
                <a href="https://www.linkedin.com/in/sebastienrousseau/" rel="external me noopener">LinkedIn · sebastienrousseau</a>
              </li>
              <li>
                <span class="contact-aside-eyebrow">Editorial</span>
                <a href="https://news.bankingonquantum.com" rel="external noopener">Banking On Quantum · newsletter</a>
              </li>
            </ul>
            <p class="contact-aside-note">If your question is already covered in the <a href="/research/index.html">research FAQ</a> or a <a href="/case-studies/index.html">case study</a>, link to it, which saves a round trip.</p>
          </aside>
        </div>
      </div>
    </main>

"""
    contact_css = """      .contact-wrap{max-width:var(--max-wide)}
      .contact-wrap .lede{font-size:clamp(17px,1.6vw,19px);color:var(--ink-mute);margin:0 0 36px;line-height:1.5}
      .contact-promise{max-width:var(--max-wide);margin-block:0}
      /* Contact rhythm (audit P1). The generic hero, the promise rail and
         main.ap-section each carry their own block padding, which stacked
         to ~200px of dead space above the form. Scoped to this layout:
         the hero closes on the site's 96px section scale and the form grid
         rides main.ap-section's padding instead of adding its own. */
      section.ap-hero{padding-block:clamp(56px,8vw,112px) clamp(40px,6vw,72px)}
      .contact-layout{display:grid;grid-template-columns:1fr;gap:48px;padding-block:0}
      @media (min-width:64em){.contact-layout{grid-template-columns:minmax(0,1fr) 320px;gap:64px;align-items:start}}
      .contact-form-col{min-width:0;max-width:680px}
      .ap-form{display:flex;flex-direction:column;gap:20px}
      .ap-form fieldset{border:0;margin:0;padding:0;min-inline-size:0;display:flex;flex-direction:column;gap:20px}
      .ap-form-row{display:flex;flex-direction:column;gap:6px}
      .ap-form-row label{font-size:13px;font-weight:600;color:var(--ink);letter-spacing:-.005em}
      .ap-form input[type=text],.ap-form input[type=email],.ap-form select,.ap-form textarea{
        font-family:inherit;font-size:16px;line-height:1.4;color:var(--ink);
        background:var(--paper);border:1px solid var(--border);border-radius:12px;
        padding:14px 16px;width:100%;min-height:48px;transition:border-color .15s,box-shadow .15s;
      }
      .ap-form textarea{min-height:160px;resize:vertical}
      .ap-form input:focus,.ap-form select:focus,.ap-form textarea:focus{outline:none;border-color:var(--accent);box-shadow:0 0 0 4px rgba(var(--accent-rgb),.15)}
      .ap-form-actions{align-items:flex-start;margin-top:8px}
      .ap-form button.pill{font-size:16px;padding:14px 28px;border:none;cursor:pointer}
      .contact-aside{padding:28px 28px 32px;background:var(--card);border:1px solid var(--rule);border-radius:var(--radius);position:sticky;top:calc(var(--nav-h) + 24px)}
      .contact-aside-title{font-family:var(--type-body);font-size:12.5px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--ink-mute);margin:0 0 18px}
      .contact-aside-list{list-style:none;margin:0 0 20px;padding:0;display:flex;flex-direction:column;gap:18px}
      .contact-aside-list li{display:flex;flex-direction:column;gap:4px}
      .contact-aside-eyebrow{font-family:var(--type-body);font-size:11px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--ink-mute)}
      .contact-aside-list a{font-size:15px;font-weight:500;color:var(--ink-deep);text-decoration:none;line-height:1.35;word-break:break-word}
      .contact-aside-list a:hover{color:var(--accent);text-decoration:underline;text-underline-offset:3px}
      .contact-aside-note{font-size:13.5px;line-height:1.5;color:var(--ink-mute);margin:0;padding-block-start:18px;border-block-start:1px solid var(--rule)}
"""
    html = TOP + body + BOTTOM
    html = html.replace("    </style>", contact_css + "    </style>")
    # reCAPTCHA is lazy-loaded on first form interaction by main.js
    # (recaptchaLazy) so its ~800 KB of third-party JS stays off the initial
    # /contact/ load — previously it eager-loaded here and pushed LCP to ~2.7s.
    return html


def report_layout() -> str:
    body = """    <section class="ap-hero">
      <h1>{{title}}</h1>
      <p class="sub">{{subtitle}}</p>
    </section>

    <main id="main" class="content ap-section">
      <div class="wrap report-wrap"><article class="report-article">{{content}}</article></div>
    </main>

"""
    return TOP + body + BOTTOM


# (title, eyebrow, description, spotify_id)
PLAYLISTS_FEATURED = (
    "TETRA 🔱",
    "Latest · Soul · Uplift",
    "May 11, 2024",
    "Step into the harmonious realm of TETRA. A euphoric playlist curated to uplift your spirits and fill your soul with joy.",
    "2KTuNfNOJsvUmrcTK3Erh5",
)

PLAYLISTS_SECTIONS = [
    (
        "SOUL & JAZZ",
        "Soulful, jazz and downtempo",
        "Smooth Jazz, Neo Soul, and laid-back grooves. Playlists for when the day calls for a slower tempo.",
        [
            (
                "SUMMERTIME 🌞",
                "Soul · Jazz",
                "Unwind and embrace the essence of summer with this curated selection of Jazz, Soul, R&B and Neo Soul beats.",
                "5RQ9X2WmRseY9SEU5oLwwX",
            ),
            (
                "NEO SOUL 🎶",
                "Soul · R&B",
                "A deep dive into the quintessential collection of Jazz, Soul, R&B and Neo Soul beats.",
                "7yvugJcCzkaWN908rXTSIL",
            ),
            (
                "LOTUS 🪷",
                "Nu-Jazz · Downtempo",
                "Take a break from a busy day and relax with soothing nu jazz and downtempo beats.",
                "7hZsKoasqFogxZVqDKYJwA",
            ),
        ],
    ),
    (
        "MORNING & MOOD",
        "Energy and tone",
        "Tracks to kick off the day or shift the room. Fashion-forward soul, vivid colour, and laid-back energy.",
        [
            (
                "MORNING ☕️",
                "Soul · Mood",
                "Soulful tracks with a fashion-forward vibe. Music to set the tone for a productive and stylish day.",
                "3GspTYbjOA4oCSulh3YLng",
            ),
            (
                "COLOURS 🌈",
                "Soul · Joy",
                "Celebrate the joy of life and dive into a world of vivid emotions, vibrant hues and soulful rhythms.",
                "2JGGk44Nopf8BX7oYJsler",
            ),
            (
                "ESSENTIAL 💚",
                "House · Deep house",
                "Laid-back beats, house-influenced grooves and new deep house tracks.",
                "1lZbauO3yCPB3YAyT5xLCW",
            ),
        ],
    ),
    (
        "ELECTRONIC",
        "Disco, house and workout",
        "Funky disco, French touch and electro. Energetic listening for movement, focus or the dance floor.",
        [
            (
                "COOL 🎧",
                "Disco · French house",
                "Seamlessly blending funky disco, house, French touch and other genres into an ultra-cool and energetic musical experience.",
                "4y3b1FXh8eVhwRRoKwrtSx",
            ),
            (
                "LOOK 💋",
                "Nu-disco · Electro",
                "A sonic voyage featuring Nu-Disco, French House, Electro and Disco House tunes from artists like Madeon and Fred Falke.",
                "0S31oWFMppEkhtHiSsldI1",
            ),
            (
                "WORKOUT BEATS 💿",
                "Hip-hop · Indie pop",
                "Laid-back beats, hip-hop-influenced grooves and new indie pop tracks.",
                "5yegPuy33SiP7DIwL6MF0J",
            ),
        ],
    ),
    (
        "HIP-HOP",
        "Rap, R&B and beats",
        "From original Hip Hop sessions to hardcore rap, contemporary R&B and Lo-Fi. The full breadth of beats.",
        [
            (
                "HIP-HOP 🎤",
                "Hip-hop · R&B",
                "Original Hip Hop, Rap and R&B Flavor Sessions.",
                "6jFJIxFfpUx0oGkbLDImKB",
            ),
            (
                "BLAST 💥",
                "Hip-hop · Rap",
                "Brace yourself for hardcore rap and hip hop tracks.",
                "6830pCYVUFYHtnkE4SJfhR",
            ),
            (
                "HIP HOP MIXTAPE 📼",
                "Hip-hop",
                "A few of the favourite hip-hop gems.",
                "5yUR35ZVOOpxyPOBhAvhkR",
            ),
            (
                "LIFETIME ⏳",
                "Hip-hop · R&B",
                "Soulful beats and thoughtful lyrics. A captivating look into the world of contemporary hip hop, R&B and rap.",
                "1RnzXyrj73nyo4yK6j3xT9",
            ),
            (
                "LO-FI BEATS 🎹",
                "Lo-fi",
                "Laid-back vibes and mellow rhythms with this stunning playlist of Lo-Fi Hip Hop beats.",
                "6Utj7AwHY6VkgGtm9wAneh",
            ),
        ],
    ),
    (
        "GLOBAL",
        "World rhythms",
        None,
        [
            (
                "WASSULU DON 🦁",
                "Africa · World",
                "Celebrate the diverse heritage of African music. From the soulful rhythms of Wassoulou to the lively beats of Londonko.",
                "13oQhLqxlNuPrn9pOIx6Vx",
            ),
        ],
    ),
]


def _playlist_card(item: tuple) -> str:
    title, eyebrow, desc, pid = item
    return f"""<article class="newsroom-card playlist-card">
<div class="newsroom-card-body">
<span class="newsroom-eyebrow">{eyebrow}</span>
<h3>{title}</h3>
<p class="newsroom-excerpt">{desc}</p>
<iframe class="spotify-frame" src="https://open.spotify.com/embed/playlist/{pid}?utm_source=generator&theme=0" width="100%" height="152" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy" title="{title} on Spotify"></iframe>
</div>
</article>"""


def _playlist_featured() -> str:
    title, eyebrow, date, desc, pid = PLAYLISTS_FEATURED
    return f"""<article class="newsroom-featured playlist-featured">
<div class="newsroom-featured-media spotify-media">
<iframe class="spotify-frame" src="https://open.spotify.com/embed/playlist/{pid}?utm_source=generator&theme=0" width="100%" height="100%" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy" title="{title} on Spotify"></iframe>
</div>
<div class="newsroom-featured-body">
<span class="newsroom-eyebrow">{eyebrow}</span>
<h3>{title}</h3>
<p class="newsroom-meta"><time datetime="2024-05-11">{date}</time> · Spotify</p>
<p>{desc}</p>
</div>
</article>"""


def _section_slug(kicker: str) -> str:
    """Stable anchor slug for a playlist section header (e.g. 'SOUL & JAZZ' -> 'soul-jazz')."""
    import re as _re

    return _re.sub(r"[^a-z0-9]+", "-", kicker.lower()).strip("-")


def _playlist_section(kicker: str, title: str, lede, items) -> str:
    anchor = _section_slug(kicker)
    head = (
        f'<header class="newsroom-section-head" id="lane-{anchor}" data-reveal>'
        f'<p class="newsroom-kicker">{kicker}</p><h2>{title}</h2>'
    )
    if lede:
        head += f'<p class="newsroom-lede">{lede}</p>'
    head += "</header>"
    cards = "\n\n".join(_playlist_card(i) for i in items)
    return head + '\n\n<div class="newsroom-grid">\n\n' + cards + "\n\n</div>"


def playlist_layout() -> str:
    sections_html = "\n\n".join(
        _playlist_section(key, title, link, items) for key, title, link, items in PLAYLISTS_SECTIONS
    )
    # Lane chip nav (Apple-HIG selective navigation): one chip per
    # section, anchor-jumps to lane-<slug>. Mirrors /topics/ pattern.
    chip_html = "".join(
        f'<a class="playlist-chip" href="#lane-{_section_slug(key)}">{title}</a>'
        for key, title, _link, _items in PLAYLISTS_SECTIONS
    )
    body = f"""    <section class="ap-hero">
      <span class="ap-hero-eyebrow">Listening</span>
      <h1>Playlists</h1>
      <p class="sub">{{{{subtitle}}}}</p>
    </section>

    <main id="main" class="content ap-section">
      <div class="wrap" style="max-width:var(--max-wide)">
        <div class="playlist-intro" data-reveal>{{{{content}}}}</div>
        <nav class="playlist-chips" aria-label="Jump to a lane">{chip_html}</nav>
        <section class="newsroom">

          <header class="newsroom-section-head" data-reveal><p class="newsroom-kicker">FEATURED</p><h2>Latest playlist</h2></header>

          {_playlist_featured()}

          {sections_html}

        </section>
      </div>
    </main>

"""
    playlist_css = """      .playlist-intro{max-width:680px;margin:0 auto 32px;text-align:center;font-size:clamp(17px,1.6vw,20px);line-height:1.5;color:var(--ink-mute)}
      .playlist-intro p{margin:0}
      .playlist-chips{display:flex;flex-wrap:wrap;gap:10px;justify-content:center;margin:0 auto 48px;max-width:780px}
      .playlist-chip{display:inline-flex;align-items:center;min-height:36px;padding:8px 18px;border:1px solid var(--rule);border-radius:999px;font-family:var(--type-body);font-size:13px;font-weight:600;color:var(--ink-deep);text-decoration:none;background:var(--paper);transition:background .15s,border-color .15s}
      .playlist-chip:hover,.playlist-chip:focus-visible{background:var(--card);border-color:var(--ink-mute)}
      .newsroom-section-head[id^=lane-]{scroll-margin-block-start:calc(var(--nav-h) + 16px)}
      .spotify-frame{border-radius:12px;border:0;display:block;width:100%}
      .playlist-card .newsroom-card-body{padding:22px 24px 22px}
      .playlist-card .newsroom-excerpt{margin-bottom:16px}
      .playlist-featured .newsroom-featured-media.spotify-media{background:#1f1f1f;aspect-ratio:1/1;padding:0;display:block}
      .playlist-featured .spotify-frame{width:100%;height:100%;border-radius:0}
      @media (max-width:833px){.playlist-featured .newsroom-featured-media.spotify-media{aspect-ratio:16/9}}
"""
    out = TOP + body + BOTTOM
    out = out.replace("    </style>", playlist_css + "    </style>")
    return out


def write(name: str, html: str) -> None:
    (LAYOUTS / name).write_text(html)
    print(f"wrote _layouts/{name}  ({len(html):,} bytes)")


def main() -> None:
    page_html = page_layout()
    kind_map = {
        "about.html": "about",
        "articles.html": "articles",
        "papers.html": "papers",
        "page.html": "default",
        "link.html": "default",
        "thank-you.html": "default",
    }
    for name, kind in kind_map.items():
        html = inject_schema(page_html, kind)
        if name == "articles.html":
            # /speaking/, /iso20022-mcp/ and /trust/ fork the built articles
            # page as their shell, so the page-scoped CSS rides articles.html
            # only.
            html = html.replace(
                "    </style>", SPEAKING_MCP_HUB_CSS + TRUST_CSS + "    </style>"
            )
        write(name, html)
    # /projects/ has its own hero: the rotating animated title is the page H1.
    write("project.html", inject_schema(project_layout(), "projects"))
    # /projects-*/ story pages: full-bleed image hero with overlaid title.
    write("story.html", inject_schema(story_layout(), "default"))
    write("contact.html", inject_schema(contact_layout(), "contact"))
    write("report.html", inject_schema(report_layout(), "report"))
    write("playlist.html", inject_schema(playlist_layout(), "playlist"))


if __name__ == "__main__":
    main()
