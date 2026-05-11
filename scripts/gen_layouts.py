#!/usr/bin/env python3
"""Generate the 10 non-index layouts from the new index.html shell.

The shared shell is everything except the body's `<section class="ap-hero">…</section>`,
`<main>…</main>`, and `<aside>…</aside>`. Each layout below substitutes its own hero +
main body. Aside is dropped (it lives on the homepage only).
"""
from __future__ import annotations
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
LAYOUTS = ROOT / "_layouts"
INDEX = (LAYOUTS / "index.html").read_text()


def slice_shell(index_html: str) -> tuple[str, str]:
    """Return (top, bottom): top ends just before the hero, bottom starts at footer."""
    hero_start = index_html.index("<!-- gen-layouts:hero-start -->")
    footer_start = index_html.index("<!-- gen-layouts:footer-start -->")
    return index_html[:hero_start], index_html[footer_start:]


TOP, BOTTOM = slice_shell(INDEX)


# Per-page Schema.org JSON-LD. Each non-home layout gets a single inline
# `application/ld+json` block. Person/Website nodes are identity-only refs (linked
# by @id back to the canonical entries on the home page) so Google and AI crawlers
# merge them into one knowledge graph.
PERSON_REF = '{"@id":"https://sebastienrousseau.com/#person"}'
SITE_REF = '{"@id":"https://sebastienrousseau.com/#website"}'
BREADCRUMB = (
    ',{"@type":"BreadcrumbList","itemListElement":['
    '{"@type":"ListItem","position":1,"name":"Home","item":"https://sebastienrousseau.com/"},'
    '{"@type":"ListItem","position":2,"name":"{{title}}","item":"{{url}}"}'
    ']}'
)
IMAGE_OBJ = (
    '{"@type":"ImageObject","url":"{{image}}","width":"{{image_width}}","height":"{{image_height}}"}'
)
# Each schema is wrapped in an @graph array so we can attach the BreadcrumbList
# as a second top-level node without breaking the JSON envelope.
WRAP = lambda body: '"@graph":[{' + body + '}' + BREADCRUMB + ']'

SCHEMA_TEMPLATES = {
    "default":  WRAP('"@type":"WebPage","name":"{{title}}","description":"{{description}}","url":"{{url}}","inLanguage":"{{hreflang}}","image":' + IMAGE_OBJ + ',"author":' + PERSON_REF + ',"publisher":' + PERSON_REF + ',"isPartOf":' + SITE_REF),
    "about":    WRAP('"@type":"AboutPage","name":"{{title}}","description":"{{description}}","url":"{{url}}","inLanguage":"{{hreflang}}","mainEntity":' + PERSON_REF + ',"isPartOf":' + SITE_REF),
    "contact":  WRAP('"@type":"ContactPage","name":"{{title}}","description":"{{description}}","url":"{{url}}","inLanguage":"{{hreflang}}","mainEntity":' + PERSON_REF + ',"isPartOf":' + SITE_REF),
    "articles": WRAP('"@type":"CollectionPage","name":"{{title}}","description":"{{description}}","url":"{{url}}","inLanguage":"{{hreflang}}","about":"Banking, payments, AI and post-quantum cryptography","author":' + PERSON_REF + ',"isPartOf":' + SITE_REF),
    "papers":   WRAP('"@type":"CollectionPage","name":"{{title}}","description":"{{description}}","url":"{{url}}","inLanguage":"{{hreflang}}","about":"Research papers and white papers on wholesale payments and post-quantum cryptography","author":' + PERSON_REF + ',"isPartOf":' + SITE_REF),
    "projects": WRAP('"@type":"CollectionPage","name":"{{title}}","description":"{{description}}","url":"{{url}}","inLanguage":"{{hreflang}}","about":"Open-source projects applied to finance and banking","author":' + PERSON_REF + ',"isPartOf":' + SITE_REF),
    "playlist": WRAP('"@type":"CollectionPage","name":"{{title}}","description":"{{description}}","url":"{{url}}","inLanguage":"{{hreflang}}","about":"Curated Spotify playlists","author":' + PERSON_REF + ',"isPartOf":' + SITE_REF),
    "report":   WRAP('"@type":"BlogPosting","headline":"{{title}}","description":"{{description}}","image":' + IMAGE_OBJ + ',"url":"{{url}}","datePublished":"{{item_pub_date}}","dateModified":"{{last_build_date}}","inLanguage":"{{hreflang}}","keywords":"{{keywords}}","articleSection":"{{category}}","author":' + PERSON_REF + ',"publisher":' + PERSON_REF + ',"mainEntityOfPage":{"@type":"WebPage","@id":"{{url}}"}'),
}


def schema_for(kind: str) -> str:
    body = SCHEMA_TEMPLATES.get(kind, SCHEMA_TEMPLATES["default"])
    return (
        '    <script type="application/ld+json">\n'
        '{"@context":"https://schema.org",' + body + '}\n'
        '    </script>\n'
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

    <main id="main" class="content ap-section" aria-label="main">
      <div class="wrap">{{content}}</div>
    </main>

"""


def page_layout() -> str:
    return TOP + PAGE_HERO_MAIN + BOTTOM


def contact_layout() -> str:
    body = """    <section class="ap-hero">
      <span class="eyebrow" style="display:inline-block;font-size:13px;font-weight:600;color:var(--accent);letter-spacing:.04em;text-transform:uppercase;margin-bottom:10px">Contact</span>
      <h1>{{title}}</h1>
      <p class="sub">{{subtitle}}</p>
    </section>

    <main id="main" class="content ap-section" aria-label="main">
      <div class="wrap contact-wrap">
        <p class="lede">{{content}}</p>
        <form class="ap-form" action="https://formspree.io/f/{{form-id}}" method="POST">
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
            <select id="subject" name="subject" required aria-label="Select a subject">
              <option value="">Choose a subject</option>
              <option value="press">Advertising / press enquiries</option>
              <option value="business">Business enquiries</option>
              <option value="feedback">Feedback / feature request</option>
              <option value="general">General questions</option>
              <option value="papers">Request instant access</option>
              <option value="product">Product questions</option>
              <option value="support">Product support</option>
            </select>
          </div>
          <div class="ap-form-row">
            <label for="message">Message</label>
            <textarea id="message" name="message" rows="6" required placeholder="How can I help?"></textarea>
          </div>
          <div class="ap-form-row">
            <label class="visually-hidden" for="g-recaptcha-response">Google reCAPTCHA</label>
            <div class="g-recaptcha" data-sitekey="{{recaptcha}}"></div>
          </div>
          <div class="ap-form-row ap-form-actions">
            <button type="submit" class="pill no-chev">Send message</button>
          </div>
        </form>
      </div>
    </main>

"""
    contact_css = """      .contact-wrap{max-width:680px}
      .contact-wrap .lede{font-size:18px;color:var(--ink-mute);margin:0 0 36px;line-height:1.5}
      .ap-form{display:flex;flex-direction:column;gap:20px}
      .ap-form-row{display:flex;flex-direction:column;gap:6px}
      .ap-form-row label{font-size:13px;font-weight:600;color:var(--ink);letter-spacing:-.005em}
      .ap-form input[type=text],.ap-form input[type=email],.ap-form select,.ap-form textarea{
        font-family:inherit;font-size:16px;line-height:1.4;color:var(--ink);
        background:#fff;border:1px solid var(--border);border-radius:12px;
        padding:12px 14px;width:100%;transition:border-color .15s,box-shadow .15s;
      }
      .ap-form textarea{min-height:140px;resize:vertical}
      .ap-form input:focus,.ap-form select:focus,.ap-form textarea:focus{outline:none;border-color:var(--accent);box-shadow:0 0 0 4px rgba(var(--accent-rgb),.15)}
      .ap-form-actions{align-items:flex-start;margin-top:8px}
      .ap-form button.pill{font-size:16px;padding:14px 28px;border:none;cursor:pointer}
"""
    html = TOP + body + BOTTOM
    html = html.replace("    </style>", contact_css + "    </style>")
    # reCAPTCHA loader
    html = html.replace(
        '<script src="/main.js" defer></script>',
        '<script src="/main.js" defer></script>\n    <script async defer src="https://www.google.com/recaptcha/api.js"></script>',
    )
    return html


def report_layout() -> str:
    body = """    <section class="ap-hero">
      <h1>{{title}}</h1>
      <p class="sub">{{subtitle}}</p>
    </section>

    <main id="main" class="content ap-section" aria-label="main">
      <div class="wrap report-wrap">{{content}}</div>
    </main>

"""
    return TOP + body + BOTTOM


# (title, eyebrow, description, spotify_id)
PLAYLISTS_FEATURED = (
    "TETRA 🔱", "Latest · Soul · Uplift", "May 11, 2024",
    "Step into the harmonious realm of TETRA. A euphoric playlist curated to uplift your spirits and fill your soul with joy.",
    "2KTuNfNOJsvUmrcTK3Erh5",
)

PLAYLISTS_SECTIONS = [
    ("SOUL & JAZZ", "Soulful, jazz and downtempo", "Smooth Jazz, Neo Soul, and laid-back grooves. Playlists for when the day calls for a slower tempo.", [
        ("SUMMERTIME 🌞", "Soul · Jazz", "Unwind and embrace the essence of summer with this curated selection of Jazz, Soul, R&B and Neo Soul beats.", "5RQ9X2WmRseY9SEU5oLwwX"),
        ("NEO SOUL 🎶", "Soul · R&B", "A deep dive into the quintessential collection of Jazz, Soul, R&B and Neo Soul beats.", "7yvugJcCzkaWN908rXTSIL"),
        ("LOTUS 🪷", "Nu-Jazz · Downtempo", "Take a break from a busy day and relax with soothing nu jazz and downtempo beats.", "7hZsKoasqFogxZVqDKYJwA"),
    ]),
    ("MORNING & MOOD", "Energy and tone", "Tracks to kick off the day or shift the room. Fashion-forward soul, vivid colour, and laid-back energy.", [
        ("MORNING ☕️", "Soul · Mood", "Soulful tracks with a fashion-forward vibe. Music to set the tone for a productive and stylish day.", "3GspTYbjOA4oCSulh3YLng"),
        ("COLOURS 🌈", "Soul · Joy", "Celebrate the joy of life and dive into a world of vivid emotions, vibrant hues and soulful rhythms.", "2JGGk44Nopf8BX7oYJsler"),
        ("ESSENTIAL 💚", "House · Deep house", "Laid-back beats, house-influenced grooves and new deep house tracks.", "1lZbauO3yCPB3YAyT5xLCW"),
    ]),
    ("ELECTRONIC", "Disco, house and workout", "Funky disco, French touch and electro. Energetic listening for movement, focus or the dance floor.", [
        ("COOL 🎧", "Disco · French house", "Seamlessly blending funky disco, house, French touch and other genres into an ultra-cool and energetic musical experience.", "4y3b1FXh8eVhwRRoKwrtSx"),
        ("LOOK 💋", "Nu-disco · Electro", "A sonic voyage featuring Nu-Disco, French House, Electro and Disco House tunes from artists like Madeon and Fred Falke.", "0S31oWFMppEkhtHiSsldI1"),
        ("WORKOUT BEATS 💿", "Hip-hop · Indie pop", "Laid-back beats, hip-hop-influenced grooves and new indie pop tracks.", "5yegPuy33SiP7DIwL6MF0J"),
    ]),
    ("HIP-HOP", "Rap, R&B and beats", "From original Hip Hop sessions to hardcore rap, contemporary R&B and Lo-Fi. The full breadth of beats.", [
        ("HIP-HOP 🎤", "Hip-hop · R&B", "Original Hip Hop, Rap and R&B Flavor Sessions.", "6jFJIxFfpUx0oGkbLDImKB"),
        ("BLAST 💥", "Hip-hop · Rap", "Brace yourself for hardcore rap and hip hop tracks.", "6830pCYVUFYHtnkE4SJfhR"),
        ("HIP HOP MIXTAPE 📼", "Hip-hop", "A few of the favourite hip-hop gems.", "5yUR35ZVOOpxyPOBhAvhkR"),
        ("LIFETIME ⏳", "Hip-hop · R&B", "Soulful beats and thoughtful lyrics. A captivating look into the world of contemporary hip hop, R&B and rap.", "1RnzXyrj73nyo4yK6j3xT9"),
        ("LO-FI BEATS 🎹", "Lo-fi", "Laid-back vibes and mellow rhythms with this stunning playlist of Lo-Fi Hip Hop beats.", "6Utj7AwHY6VkgGtm9wAneh"),
    ]),
    ("GLOBAL", "World rhythms", None, [
        ("WASSULU DON 🦁", "Africa · World", "Celebrate the diverse heritage of African music. From the soulful rhythms of Wassoulou to the lively beats of Londonko.", "13oQhLqxlNuPrn9pOIx6Vx"),
    ]),
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


def _playlist_section(kicker: str, title: str, lede, items) -> str:
    head = f'<header class="newsroom-section-head"><p class="newsroom-kicker">{kicker}</p><h2>{title}</h2>'
    if lede:
        head += f'<p class="newsroom-lede">{lede}</p>'
    head += "</header>"
    cards = "\n\n".join(_playlist_card(i) for i in items)
    return head + '\n\n<div class="newsroom-grid">\n\n' + cards + "\n\n</div>"


def playlist_layout() -> str:
    sections_html = "\n\n".join(
        _playlist_section(k, t, l, items) for k, t, l, items in PLAYLISTS_SECTIONS
    )
    body = f"""    <section class="ap-hero">
      <h1>{{{{name}}}}</h1>
      <p class="sub">{{{{subtitle}}}}</p>
    </section>

    <main id="main" class="content ap-section" aria-label="main">
      <div class="wrap" style="max-width:var(--max-wide)">
        <div class="playlist-intro">{{{{content}}}}</div>
        <section class="newsroom">

          <header class="newsroom-section-head"><p class="newsroom-kicker">FEATURED</p><h2>Latest playlist</h2></header>

          {_playlist_featured()}

          {sections_html}

        </section>
      </div>
    </main>

"""
    playlist_css = """      .playlist-intro{max-width:760px;margin:0 auto 40px;text-align:center;font-size:clamp(18px,2vw,22px);line-height:1.45;color:var(--ink-mute)}
      .playlist-intro p{margin:0}
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
        "project.html": "projects",
    }
    for name, kind in kind_map.items():
        write(name, inject_schema(page_html, kind))
    write("contact.html",  inject_schema(contact_layout(),  "contact"))
    write("report.html",   inject_schema(report_layout(),   "report"))
    write("playlist.html", inject_schema(playlist_layout(), "playlist"))


if __name__ == "__main__":
    main()
