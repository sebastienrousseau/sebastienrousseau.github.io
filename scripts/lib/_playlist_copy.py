# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""English source copy for the /playlists/ page.

Single source of truth shared by two consumers:

* ``scripts/generators/gen_layouts.py`` renders ``_layouts/playlist.html``
  from it (the English page).
* ``scripts/generators/build_translations`` reads it to know the exact
  English strings to swap out when forking that page into each of the
  34 localized trees, keyed by ``_data/i18n/<code>/playlists.json``.

Keeping the copy here rather than inline in the generator is what makes
the page translatable at all: the localized catalogues key off the
Spotify playlist id / lane key / FAQ index, and the renderer needs the
matching English string to find in the built HTML.

Every artist named in a blurb is actually on that playlist's tracklist
(copy is written against the real Spotify embed payload). Genre terms
lead because they are what people search for.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Page furniture
# ---------------------------------------------------------------------------

HERO_H1 = "Playlists"
HERO_JUMP = "Hear the latest playlist"
PLATFORMS_LABEL = "The full collection is on Apple Music too"
NAV_LABEL = "Jump to a genre"
PLAY_LABEL = "Play on Spotify"
FOLLOW_LABEL = "Follow on Spotify"
APPLE_LABEL = "Listen on Apple Music"
LANE_COUNT_ONE = "playlist"
LANE_COUNT_OTHER = "playlists"
# ``{title}`` is the playlist name, which is a proper noun and never
# translated; only the frame around it is.
COVER_ALT = "Cover artwork for the {title} playlist"
OPEN_ARIA = "Open {title} on Spotify"
FRAME_TITLE = "{title} playlist on Spotify"

# Intro paragraphs. These are the *body* of ``_posts/playlists.md`` —
# the generator renders the markdown, not this tuple. They are mirrored
# here so the translation pipeline knows the exact strings to swap;
# ``tests/unit/test_playlist_copy_intro.py`` fails if the two drift.
INTRO_PARAGRAPHS: tuple[str, ...] = (
    "Thirty-nine playlists and 1,763 tracks, built for the hours that need a "
    "soundtrack — deep work, long reads and late rewrites.",
    "Neo soul and nu jazz when the work needs patience. Boom bap and jazz rap "
    "when it needs momentum. French touch, deep house and disco house when it "
    "needs lift. Lo-fi for the head-down stretch, and West African rhythms "
    "running through it all.",
    "Every playlist streams free on Spotify, and the whole collection is on Apple Music.",
)

# The featured band's meta line: "<date> · <genres>".
FEATURED_GENRES = "Indie pop · French house"
FEATURED_DATETIME = "2026-08-22"


# (title, eyebrow, description, spotify_id, artwork_id)
#
# Copy is written against each playlist's real tracklist (fetched from the
# Spotify embed payload), so every artist named is actually in the list.
# Genre terms lead because they are what people search for.
PLAYLISTS_FEATURED = (
    "Lōkahi 🌺",
    "Latest playlist",
    "August 2026",
    "Sun-drenched indie pop sliding into French house — Tame Impala and almost monday giving way to Justice, L'Impératrice and Afro house from HUGEL.",
    "6dhwZBIQ4dpoc9lne6b7Aj",
    "https://i.scdn.co/image/ab67706c0000da84fa9411fea3e5385a56df77d2",
)

PLAYLISTS_SECTIONS = [
    (
        "electronic",
        "Electronic",
        "Disco, house and workout",
        "House, disco and French touch",
        [
            (
                "ETERNAL GROOVE 🪩",
                "Disco house · Garage",
                "Late-nineties disco house and garage that still fills a floor — Kings Of Tomorrow, David Morales, Moloko, Armand Van Helden and Boris Dlugosch.",
                "79rcQ3HAOu3RQTu0hyPFVX",
                "https://i.scdn.co/image/ab67706c0000da84ea3cd37ea58de627af7ab3af",
            ),
            (
                "Lōkahi 🌺",
                "Indie pop · French house",
                "Sun-drenched indie pop sliding into French house — Tame Impala and almost monday giving way to Justice, L'Impératrice and Afro house from HUGEL.",
                "6dhwZBIQ4dpoc9lne6b7Aj",
                "https://i.scdn.co/image/ab67706c0000da84fa9411fea3e5385a56df77d2",
            ),
            (
                "FOREVER ♾️",
                "French touch · Electro",
                "French touch at full beam — Daft Punk, Justice, Kavinsky, L'Impératrice and Angèle trading neon synths and motorik basslines.",
                "2r2g4G5wTSucqWda5MkuXH",
                "https://i.scdn.co/image/ab67706c0000da84f6ea0a0bfa74c52c95690cc4",
            ),
            (
                "GOLDEN HOUR 🌟",
                "Indie dance · Synth pop",
                "Golden-hour synth pop and indie dance — Blu DeTiger, Merty Shango, Citrus Sun and Enne carrying the shimmer into the evening.",
                "3YiO3L3LMWlXaGEGtJFdXo",
                "https://i.scdn.co/image/ab67706c0000da84e8a289b744da9c54e867ce52",
            ),
            (
                "LOOK 💋",
                "Nu-disco · French house",
                "Nu-disco and French house with the filter open — Fred Falke, Breakbot, Madeon, Lemaitre and Yelle.",
                "0S31oWFMppEkhtHiSsldI1",
                "https://i.scdn.co/image/ab67706c0000da84e5f9a33792844a185541953b",
            ),
            (
                "CITY ⛩️",
                "Progressive house · Electro",
                "Progressive house and electro built for movement — Madeon, Paul Woolford, Martin Solveig, Secondcity and The Knocks.",
                "5OQTseRtYQtZF6kERLvcSz",
                "https://i.scdn.co/image/ab67706c0000da84b01797b3eaa398e5be8a19c8",
            ),
            (
                "NEO DANCE 🪩",
                "Nu-disco · Filtered house",
                "Nu-disco and filtered house built for movement — Lenno, Oliver, Tollef and Yelle over clipped guitars and fat synth bass.",
                "5OksFu1fF3eHNifxxAcev6",
                "https://i.scdn.co/image/ab67706c0000da84c99c974c5fc72d354495ffa0",
            ),
            (
                "ESSENTIAL 💚",
                "Deep house · Melodic house",
                "A hundred deep and melodic house tracks that stay out of the way — Chris Malinchak, Sultan + Shepard, Lenno and Nora Van Elken.",
                "1lZbauO3yCPB3YAyT5xLCW",
                "https://i.scdn.co/image/ab67706c0000da84f7cdb833e8c21996a92c1c1c",
            ),
            (
                "EVOLUTION ☀️",
                "Future house · Electro pop",
                "Bright future house and electro pop — Lenno, La Felix, The Knocks, Kraak & Smaak and Chris Malinchak across a hundred tracks.",
                "5vKhAAaO06St5XoCh96PxR",
                "https://i.scdn.co/image/ab67706c0000da84ef337638a24f69f31d0567da",
            ),
        ],
    ),
    (
        "soul-jazz",
        "Soul &amp; Jazz",
        "Soulful, jazz and downtempo",
        "Neo soul, nu jazz and slow tempo",
        [
            (
                "THE DATE",
                "Jazzy hip-hop · Boom bap",
                "Jazz-sampling boom bap for slow evenings — Blu & Exile, Large Professor, 3582 and Scienze trading warm loops and unhurried verses.",
                "2CeSPJPwxmhbIIdfXyap3F",
                "https://i.scdn.co/image/ab67706c0000da8452cbacbd7c6cf52a2c2b2a78",
            ),
            (
                "Groovation 🎷",
                "Jazz-hop · Boom bap",
                "Golden-era jazz-hop from the Phoniks camp — Awon & Phoniks, Anti Lilly, Dephlow and Tiff the Gift over dusty horns and upright bass.",
                "0mrwKGH6s0MWsNfMCtcTQz",
                "https://i.scdn.co/image/ab67706c0000da840924f35ba443453381778c15",
            ),
            (
                "Thrill Seekers 🌀",
                "Alternative R&B · Neo soul",
                "Alternative R&B and late-night neo soul — Brent Faiyaz, Elujay, J.Robb and Lou Phelps over woozy drums and unhurried basslines.",
                "56Vs5RzfyK1uqwWFoTz3SB",
                "https://i.scdn.co/image/ab67706c0000da84e7baa033889bbb3bf6657d4e",
            ),
            (
                "1975 🪩",
                "Disco · Boogie",
                "Seventies and eighties floor fillers — CHIC, Luther Vandross, The Jacksons, Change and Oliver Cheatham. Strings, claps and basslines that do the work.",
                "1q8SfSUHyFxjUWucE9A1wR",
                "https://i.scdn.co/image/ab67706c0000da84d762254e7a9fd7b28eaf61d9",
            ),
            (
                "Back to Life 🛟",
                "Acid jazz · Nu jazz",
                "Acid jazz and nu jazz with a live band behind it — The Brand New Heavies, Incognito, Robert Glasper, Carleen Anderson and Count Basic.",
                "7GLBaZHcJ5st67eMCILolm",
                "https://i.scdn.co/image/ab67706c0000da8443105358a81c27b7357bc798",
            ),
            (
                "UBUNTU 🍥",
                "Gospel · Soul",
                "Gospel-rooted soul that lifts a room — Kirk Franklin, Aretha Franklin, Yolanda Adams, Jennifer Hudson, Mica Paris and Avery*Sunshine.",
                "2WxvFba2Sgg4Sd3lZJHmHP",
                "https://i.scdn.co/image/ab67706c0000da84b553ef6f2c246695cc5cfdf1",
            ),
            (
                "NEOVIE 🌱",
                "Broken beat · Nu jazz",
                "Broken beat and UK nu jazz for slow afternoons — Emma-Jean Thackray, Blue Lab Beats, Galliano and The Brand New Heavies.",
                "36Rkih8f9fgd92jI3QVMrQ",
                "https://i.scdn.co/image/ab67706c0000da84f2628cb7fa5462dabcd8fba7",
            ),
            (
                "TIMES ⏳",
                "British soul · Broken beat",
                "British soul at its warmest — Incognito, Shaun Escoffery, Cherri V and Tortured Soul, with Stevie Wonder in the room.",
                "261aHSqcEnM5KnTCLSNFQz",
                "https://i.scdn.co/image/ab67706c0000da8465f695e82cbb1b08e5a296b3",
            ),
            (
                "WAVES 🌊",
                "Modern jazz · R&B",
                "Modern jazz and R&B in conversation — Robert Glasper, August Greene, Common, Karriem Riggins and Brandy.",
                "2XO0Kw6aCXdfUT3coih7vg",
                "https://i.scdn.co/image/ab67706c0000da84a2f65062cc32aca8a80335b6",
            ),
            (
                "LOVE ❤️",
                "Soul · Jazz funk",
                "Love songs with real players behind them — 4hero and Marc Mac, Incognito, Imaani, Natalie Duncan and Adi Oasis.",
                "0UWRprsfYCjbnpLHCNUCPF",
                "https://i.scdn.co/image/ab67706c0000da845e321bde595bb619410594a1",
            ),
            (
                "SUMMERTIME 🌞",
                "Neo soul · Jazz",
                "Fifty-five neo soul and jazz cuts for warm evenings — India.Arie, Robert Glasper, Lucy Pearl, Anthony David and Ronny Jordan.",
                "5RQ9X2WmRseY9SEU5oLwwX",
                "https://i.scdn.co/image/ab67706c0000da84194d2347398021360c2fd549",
            ),
            (
                "NEO SOUL 🎶",
                "Neo soul · Modern R&B",
                "Seventy-three neo soul and modern R&B cuts — Alex Isley, Yebba, Ego Ella May, Robert Glasper and Blue Lab Beats.",
                "7yvugJcCzkaWN908rXTSIL",
                "https://i.scdn.co/image/ab67706c0000da84ab134bdb207cccad40efcaf9",
            ),
            (
                "SPOTLIGHT 🔆",
                "Jazz funk · Neo soul",
                "A hundred tracks with the spotlight on the players — Erykah Badu, Jill Scott, Omar, Esperanza Spalding and Stevie Wonder.",
                "5wjy0SY2jCwAZ4UFLF3eXC",
                "https://i.scdn.co/image/ab67706c0000da846c1230cdbadc6b04d1eabb5d",
            ),
        ],
    ),
    (
        "hip-hop",
        "Hip-Hop",
        "Rap, R&amp;B and beats",
        "Boom bap, jazz rap and golden-era grooves",
        [
            (
                "ETHEREAL",
                "Rap · West coast",
                "A hundred tracks of rap across four decades — 2Pac and Dr. Dre, Snoop Dogg and Tha Dogg Pound, Ghostface Killah, Nicki Minaj and DJ Muggs.",
                "6rCGkdLLdt6IXhkQvXSwyF",
                "https://i.scdn.co/image/ab67706c0000da84b4d17e7e80d28b850a7e1bf9",
            ),
            (
                "OBLIVION 💫",
                "Rap · Soul · French touch",
                "A hundred-track crate dig with no genre rule — Dr. Dre and Eminem beside MC Solaar and 113, Charles Aznavour beside DJ Mehdi and Thomas Bangalter.",
                "5mKe1KjwZRzTS4FtU2jejT",
                "https://i.scdn.co/image/ab67706c0000da84bf4753aa2e1bfe52f24dc42a",
            ),
            (
                "BLAST 💥",
                "Hardcore rap · Boom bap",
                "Hardcore nineties rap with the volume up — M.O.P., Busta Rhymes, Big L, Westside Connection, Dr. Dre and Snoop Dogg.",
                "6830pCYVUFYHtnkE4SJfhR",
                "https://i.scdn.co/image/ab67706c0000da84e1f98d87d37ba214a465652b",
            ),
            (
                "HIP-HOP 🎤",
                "Boom bap · Jazz rap",
                "Eighty-six cuts of nineties boom bap and jazz rap — Gang Starr, A Tribe Called Quest, The Roots, The Pharcyde and Guru's Jazzmatazz.",
                "6jFJIxFfpUx0oGkbLDImKB",
                "https://i.scdn.co/image/ab67706c0000da846bf59c3ee949f0b5203ee8ee",
            ),
            (
                "HIP HOP MIXTAPE 📼",
                "Underground · Boom bap",
                "Underground boom bap and instrumentals — Apollo Brown, People Under The Stairs, J-Live, One Be Lo, Marcus D and Shing02.",
                "5yUR35ZVOOpxyPOBhAvhkR",
                "https://i.scdn.co/image/ab67706c0000da844be1d414769f27e5c2f76eda",
            ),
            (
                "WORKOUT BEATS 💿",
                "Indie hip-hop · Pop rap",
                "Indie hip-hop and pop rap with momentum — Quinn XCII, Kid Quill, EMAN8, gianni & kyle and YONAS.",
                "5yegPuy33SiP7DIwL6MF0J",
                "https://i.scdn.co/image/ab67706c0000da84b7a032c4641457f36e6abbb6",
            ),
        ],
    ),
    (
        "morning-mood",
        "Morning &amp; Mood",
        "Energy and tone",
        "Downtempo, lo-fi and wake-up energy",
        [
            (
                "SWIM 🏊",
                "Chillwave · Downtempo",
                "Weightless downtempo for a long drive or a slow morning — Zero 7, Les Imprimés and Ciao Ciao Marigold over soft-focus drums.",
                "40OkPs9Yk4AtBZrtYz5xtW",
                "https://i.scdn.co/image/ab67706c0000da84808664129c9412b41219d18a",
            ),
            (
                "PARISIAN DESTINY 🗼",
                "Trip-hop · Jazz-hop",
                "Jazz-sampling trip-hop from Proleter, Poldoore, Souleance and The Geek x Vrv. Cinematic, unhurried, built for writing.",
                "4PBfAfwUv5fEJAYErxvNJ4",
                "https://i.scdn.co/image/ab67706c0000da84249221c7ca82936f59a3b3aa",
            ),
            (
                "TETRA 🔱",
                "Downtempo · Nu jazz",
                "Downtempo and nu jazz to think against — Zero 7, The Cinematic Orchestra, Souleance, Mozez and Ida Nielsen.",
                "2KTuNfNOJsvUmrcTK3Erh5",
                "https://i.scdn.co/image/ab67706c0000da84c101708017adfc783a7a6ff1",
            ),
            (
                "COLOURS 🌈",
                "Trip-hop · Downtempo",
                "Trip-hop and downtempo with a soul core — Massive Attack, Thievery Corporation, Air, Zero 7, The Cinematic Orchestra and Nina Simone reworked.",
                "2JGGk44Nopf8BX7oYJsler",
                "https://i.scdn.co/image/ab67706c0000da8475e09afb846f2658b29bd236",
            ),
            (
                "LO-FI BEATS 🎹",
                "Lo-fi · Study beats",
                "Fifty-two lo-fi hip hop beats for studying and deep work — Idealism, j'san, Joey Pecoraro, Sugi.wa and aimless. No vocals to argue with.",
                "6Utj7AwHY6VkgGtm9wAneh",
                "https://i.scdn.co/image/ab67706c0000da84204903094655b4749439b10f",
            ),
            (
                "COOL 🎧",
                "French house · Nu-disco",
                "Funky French house and nu-disco on an even keel — Breakbot, Modjo, Fred Falke, Kartell and Chris Malinchak.",
                "4y3b1FXh8eVhwRRoKwrtSx",
                "https://i.scdn.co/image/ab67706c0000da840ab6193f96b895c1264badc3",
            ),
            (
                "LOTUS 🪷",
                "Nu jazz · Downtempo",
                "Soothing nu jazz and downtempo to unwind to — Zero 7, 4hero, The Cinematic Orchestra, Lemon Jelly and Kid Loco.",
                "7hZsKoasqFogxZVqDKYJwA",
                "https://i.scdn.co/image/ab67706c0000da84f4c33289cea18b51ca669850",
            ),
            (
                "MORNING ☕️",
                "Soul · Jazz funk",
                "Soul and jazz funk to start the day — Adi Oasis, Durand Jones, Azymuth, Kraak & Smaak and Stevie Wonder.",
                "3GspTYbjOA4oCSulh3YLng",
                "https://i.scdn.co/image/ab67706c0000da8440c76601a3cc8932f2b74d5e",
            ),
            (
                "POP WORKOUT 🥤",
                "Uplifting pop",
                "Sixty-four bright, up-tempo pop tracks to move to — Riley Clemmons, Lauren Daigle, Sarah Reeves, Elle Limebear and Madison.",
                "3Eg1SZ5yYbtdytaV3sVg6C",
                "https://i.scdn.co/image/ab67706c0000da8444ec7469e1ccb1dab6d21c6d",
            ),
            (
                "LIFETIME ⏳",
                "Jazz rap · Alt R&B",
                "Jazz rap and alternative R&B with something to say — Noname, Anderson .Paak, KAYTRANADA, Q-Tip and A Tribe Called Quest.",
                "1RnzXyrj73nyo4yK6j3xT9",
                "https://i.scdn.co/image/ab67706c0000da84e86212b31675303f2c19b4c1",
            ),
        ],
    ),
    (
        "global",
        "Global",
        "World rhythms",
        "Rhythms from everywhere else",
        [
            (
                "WASSULU DON 🦁",
                "Afrobeat · Wassoulou",
                "West African voices front and centre — Oumou Sangaré, Fatoumata Diawara, Dobet Gnahoré, Sona Jobarteh and Kareyce Fotso, from Wassoulou to kora.",
                "13oQhLqxlNuPrn9pOIx6Vx",
                "https://i.scdn.co/image/ab67706c0000da8436f3d01be810b7f02b0235dd",
            ),
        ],
    ),
]

# ---------------------------------------------------------------------------
# FAQ — (question, answer) pairs, rendered into schema.org/FAQPage markup.
# ---------------------------------------------------------------------------

FAQ_HEADING = "Questions? Answers."
FAQ_SUB = "How to listen, on what, and where the music comes from."

FAQ_ITEMS: list[tuple[str, str]] = [
    (
        "Do I need a Spotify subscription to listen?",
        "No. Every playlist plays in the embedded player above on a free Spotify "
        "account, with ads between tracks. A Premium account removes the ads and "
        "allows offline listening, but nothing here is behind a paywall.",
    ),
    (
        "Can I listen on Apple Music instead?",
        "Yes — follow the profile at music.apple.com/profile/bxhero. The playlists "
        "on this page are the Spotify versions, because Apple Music does not expose "
        "individual playlist links publicly. Following the profile is the reliable "
        "route on that platform.",
    ),
    (
        "What devices do these work on?",
        "Anywhere Spotify runs: iPhone, iPad, Android, Mac, Windows, Apple Watch, "
        "Apple TV, CarPlay, Sonos, Google Nest, PlayStation, Xbox, and any browser. "
        "The players on this page work on mobile and desktop without an app.",
    ),
    (
        "Which playlist should I start with for deep work?",
        "Morning &amp; Mood for focus without distraction — downtempo, nu jazz and "
        "lo-fi with little or no vocal to compete with reading. Electronic suits "
        "work that needs momentum rather than calm.",
    ),
    (
        "How often are the playlists updated?",
        "Regularly, and in place. Following a playlist on Spotify or the profile on "
        "either service means new tracks arrive without checking back here.",
    ),
    (
        "Can I share or embed these playlists?",
        "Yes. Every card links to the playlist on Spotify, where the share menu "
        "provides links and embed codes. They are public playlists, free to share.",
    ),
    (
        "Who makes these playlists?",
        "Sebastien Rousseau — as BXHERO on Spotify and Apple Music. They are the "
        "playlists used while writing about payments and engineering, not an "
        "algorithmic feed.",
    ),
]

# ---------------------------------------------------------------------------
# "Listen on every device" aside.
# ---------------------------------------------------------------------------

EVERYWHERE_HEADING = "Listen on every device"
# Line breaks are preserved verbatim in the rendered HTML — they are what
# the committed _layouts/playlist.html contains.
EVERYWHERE_BODY = (
    "Every playlist plays in the browser above, and in the Spotify app on the\n"
    "devices you already use. Follow the profile on either service and new\n"
    "playlists arrive on their own."
)
# Device names are product names — never translated, listed here so the
# catalogue can carry them for completeness.
DEVICES: tuple[str, ...] = (
    "iPhone",
    "iPad",
    "Android",
    "Mac",
    "Windows",
    "Apple Watch",
    "Apple TV",
    "CarPlay",
    "Sonos",
    "Google Nest",
    "PlayStation",
    "Xbox",
    "Web browser",
)
