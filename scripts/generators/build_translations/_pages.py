# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Listing / static-page renderers: articles hub, home page, static-page
mirrors and topic sub-pages."""

from __future__ import annotations

import html as _html
import re

from . import _state as st
from ._chrome import (
    _CANONICAL_RE,
    _DESC_META_RE,
    _KW_META_RE,
    _OG_DESC_RE,
    _OG_LOCALE_RE,
    _OG_TITLE_RE,
    _OG_URL_RE,
    _TITLE_RE,
    _TW_DESC_RE,
    _TW_TITLE_RE,
    _localize_inlanguage_globally,
    _patch_jsonld_scripts,
    _set_html_lang,
    localize_feed_links,
    translate_chrome,
)
from ._maps import (
    rewrite_en_descs_in_text,
    rewrite_en_titles_in_text,
    rewrite_en_urls,
    rewrite_fr_link_titles,
    rewrite_newsroom_card_titles,
)
from ._playlists import localize_playlists_page
from ._projects import localize_projects_page

# ---------------------------------------------------------------------------
# Hub: /fr/articles/
# ---------------------------------------------------------------------------

_LDJSON_RE = re.compile(r'<script type="application/ld\+json">[\s\S]*?</script>', re.IGNORECASE)


def render_home() -> str | None:  # noqa: C901 — orchestrates the FR home fork end-to-end
    """Fork ``public/index.html`` (the EN home) to produce
    ``public/fr/index.html`` so the FR landing page mirrors the EN
    structure (hero + projects + quote + paper + latest + experience).
    """
    shell_src = st.PUBLIC / "index.html"
    if not shell_src.is_file():
        return None
    shell = shell_src.read_text(encoding="utf-8")

    # Per-locale home <title> + meta description, natively phrased. Faithful
    # to the EN home title "Sebastien Rousseau: AI, Payments & Quantum
    # Cryptography" and its description. Every active locale must have an
    # entry here; locales missing from the map fall back to English, never
    # to another translation.
    _en_home_title = "Sebastien Rousseau: AI, Payments & Quantum Cryptography"
    _en_home_desc = (
        "The future of banking through applied AI, payments and quantum-resistant "
        "security. Research, open-source libraries and product consulting for "
        "financial services."
    )
    _home_titles = {
        "ar": "سيباستيان روسو: الذكاء الاصطناعي والمدفوعات والتشفير الكمومي",
        "bn": "Sebastien Rousseau: এআই, পেমেন্ট ও কোয়ান্টাম ক্রিপ্টোগ্রাফি",
        "cs": "Sebastien Rousseau: AI, platby a kvantová kryptografie",
        "de": "Sebastien Rousseau: KI, Zahlungen und Quantenkryptografie",
        "es": "Sebastien Rousseau: IA, pagos y criptografía cuántica",
        "fil": "Sebastien Rousseau: AI, mga pagbabayad at quantum cryptography",
        "fr": "Sebastien Rousseau : IA, paiements et cryptographie quantique",
        "ha": "Sebastien Rousseau: AI, biyan kuɗi da quantum cryptography",
        "he": "סבסטיאן רוסו: בינה מלאכותית, תשלומים והצפנה קוונטית",
        "hi": "Sebastien Rousseau: एआई, पेमेंट्स और क्वांटम क्रिप्टोग्राफी",
        "hu": "Sebastien Rousseau: MI, fizetések és kvantumkriptográfia",
        "id": "Sebastien Rousseau: AI, pembayaran, dan kriptografi kuantum",
        "it": "Sebastien Rousseau: IA, pagamenti e crittografia quantistica",
        "ja": "Sebastien Rousseau：AI・決済・量子暗号",
        "ko": "Sebastien Rousseau: AI, 결제, 양자 암호",
        "nl": "Sebastien Rousseau: AI, betalingen en kwantumcryptografie",
        "pl": "Sebastien Rousseau: AI, płatności i kryptografia kwantowa",
        "pt-br": "Sebastien Rousseau: IA, pagamentos e criptografia quântica",
        "ro": "Sebastien Rousseau: IA, plăți și criptografie cuantică",
        "ru": "Себастьен Руссо: ИИ, платежи и квантовая криптография",
        "sv": "Sebastien Rousseau: AI, betalningar och kvantkryptografi",
        "th": "Sebastien Rousseau: เอไอ การชำระเงิน และการเข้ารหัสเชิงควอนตัม",
        "tr": "Sebastien Rousseau: Yapay Zeka, Ödemeler ve Kuantum Kriptografi",
        "uk": "Себастьєн Руссо: ШІ, платежі та квантова криптографія",
        "vi": "Sebastien Rousseau: AI, thanh toán và mật mã lượng tử",
        "yo": "Sebastien Rousseau: AI, ìsanwó àti quantum cryptography",
        "el": "Sebastien Rousseau: Τεχνητή νοημοσύνη, πληρωμές και κβαντική κρυπτογραφία",
        "fa": "Sebastien Rousseau: هوش مصنوعی، پرداخت‌ها و رمزنگاری کوانتومی",
        "mr": "Sebastien Rousseau: एआय, पेमेंट्स आणि क्वांटम क्रिप्टोग्राफी",
        "ms": "Sebastien Rousseau: AI, pembayaran dan kriptografi kuantum",
        "ta": "Sebastien Rousseau: செயற்கை நுண்ணறிவு, கட்டணங்கள், குவாண்டம் குறியாக்கவியல்",
        "te": "Sebastien Rousseau: ఏఐ, చెల్లింపులు, క్వాంటం క్రిప్టోగ్రఫీ",
        "zh-hans": "Sebastien Rousseau：AI、支付与量子密码学",
        "zh-hant": "Sebastien Rousseau：AI、支付與量子密碼學",
    }
    _home_descs = {
        "ar": (
            "مستقبل الخدمات المصرفية عبر الذكاء الاصطناعي التطبيقي والمدفوعات "
            "والأمن المقاوم للحوسبة الكمومية. أبحاث ومكتبات مفتوحة المصدر "
            "واستشارات منتجات للخدمات المالية."
        ),
        "bn": (
            "প্রায়োগিক এআই, পেমেন্ট এবং কোয়ান্টাম-প্রতিরোধী নিরাপত্তার মাধ্যমে "
            "ব্যাংকিংয়ের ভবিষ্যৎ। আর্থিক পরিষেবার জন্য গবেষণা, ওপেন-সোর্স "
            "লাইব্রেরি এবং প্রোডাক্ট কনসালটিং।"
        ),
        "cs": (
            "Budoucnost bankovnictví skrze aplikovanou AI, platby a zabezpečení "
            "odolné vůči kvantovým počítačům. Výzkum, open source knihovny a "
            "produktové poradenství pro finanční služby."
        ),
        "de": (
            "Die Zukunft des Bankwesens durch angewandte KI, Zahlungen und "
            "quantensichere Sicherheit. Forschung, Open-Source-Bibliotheken und "
            "Produktberatung für Finanzdienstleistungen."
        ),
        "es": (
            "El futuro de la banca a través de la IA aplicada, los pagos y la "
            "seguridad resistente a la computación cuántica. Investigación, "
            "bibliotecas open source y consultoría de producto para servicios "
            "financieros."
        ),
        "fil": (
            "Ang hinaharap ng pagbabangko sa pamamagitan ng applied AI, mga "
            "pagbabayad at seguridad na matibay laban sa quantum computing. "
            "Pananaliksik, open-source na mga library at product consulting "
            "para sa mga serbisyong pinansyal."
        ),
        "fr": (
            "L'avenir de la banque par l'IA appliquée, les paiements et la sécurité "
            "résistante au quantique. Recherche, bibliothèques open source et "
            "conseil produit pour les services financiers."
        ),
        "ha": (
            "Makomar harkokin banki ta hanyar AI mai amfani, hanyoyin biyan kuɗi "
            "da tsaro mai jure kwamfutar quantum. Bincike, ɗakunan karatu na "
            "open source da shawarwarin samfur don ayyukan kuɗi."
        ),
        "he": (
            "עתיד הבנקאות באמצעות בינה מלאכותית יישומית, תשלומים ואבטחה עמידה "
            "בפני מחשוב קוונטי. מחקר, ספריות קוד פתוח וייעוץ מוצר לשירותים "
            "פיננסיים."
        ),
        "hi": (
            "एप्लाइड एआई, पेमेंट्स और क्वांटम-प्रतिरोधी सुरक्षा के माध्यम से "
            "बैंकिंग का भविष्य। वित्तीय सेवाओं के लिए शोध, ओपन-सोर्स लाइब्रेरी "
            "और प्रोडक्ट कंसल्टिंग।"
        ),
        "hu": (
            "A bankszektor jövője az alkalmazott MI, a fizetések és a "
            "kvantumbiztos védelem révén. Kutatás, nyílt forráskódú könyvtárak "
            "és terméktanácsadás pénzügyi szolgáltatásokhoz."
        ),
        "id": (
            "Masa depan perbankan melalui AI terapan, pembayaran, dan keamanan "
            "tahan kuantum. Riset, pustaka open source, dan konsultasi produk "
            "untuk layanan keuangan."
        ),
        "it": (
            "Il futuro della banca attraverso l'IA applicata, i pagamenti e la "
            "sicurezza resistente al quantum. Ricerca, librerie open source e "
            "consulenza di prodotto per i servizi finanziari."
        ),
        "ja": (
            "応用AI・決済・耐量子セキュリティが切り拓く銀行の未来。"
            "金融サービスのための研究、オープンソースライブラリ、"
            "プロダクトコンサルティング。"
        ),
        "ko": (
            "응용 AI, 결제, 양자 내성 보안이 이끄는 은행의 미래. 금융 서비스를 "
            "위한 연구, 오픈소스 라이브러리, 제품 컨설팅."
        ),
        "nl": (
            "De toekomst van het bankwezen via toegepaste AI, betalingen en "
            "kwantumbestendige beveiliging. Onderzoek, open source bibliotheken "
            "en productadvies voor financiële dienstverlening."
        ),
        "pl": (
            "Przyszłość bankowości dzięki stosowanej AI, płatnościom i "
            "bezpieczeństwu odpornemu na komputery kwantowe. Badania, biblioteki "
            "open source i doradztwo produktowe dla usług finansowych."
        ),
        "pt-br": (
            "O futuro do setor bancário por meio de IA aplicada, pagamentos e "
            "segurança resistente à computação quântica. Pesquisa, bibliotecas "
            "open source e consultoria de produto para serviços financeiros."
        ),
        "ro": (
            "Viitorul serviciilor bancare prin IA aplicată, plăți și securitate "
            "rezistentă la calculul cuantic. Cercetare, biblioteci open source "
            "și consultanță de produs pentru servicii financiare."
        ),
        "ru": (
            "Будущее банковского дела через прикладной ИИ, платежи и "
            "квантово-устойчивую безопасность. Исследования, библиотеки с "
            "открытым кодом и продуктовый консалтинг для финансовых услуг."
        ),
        "sv": (
            "Bankväsendets framtid genom tillämpad AI, betalningar och "
            "kvantresistent säkerhet. Forskning, open source-bibliotek och "
            "produktrådgivning för finansiella tjänster."
        ),
        "th": (
            "อนาคตของธนาคารผ่านเอไอเชิงประยุกต์ การชำระเงิน "
            "และความปลอดภัยที่ทนทานต่อควอนตัม งานวิจัย ไลบรารีโอเพนซอร์ส "
            "และที่ปรึกษาด้านผลิตภัณฑ์สำหรับบริการทางการเงิน"
        ),
        "tr": (
            "Uygulamalı yapay zeka, ödemeler ve kuantuma dayanıklı güvenlikle "
            "bankacılığın geleceği. Finansal hizmetler için araştırma, açık "
            "kaynak kütüphaneler ve ürün danışmanlığı."
        ),
        "uk": (
            "Майбутнє банківської справи через прикладний ШІ, платежі та "
            "квантово-стійку безпеку. Дослідження, бібліотеки з відкритим кодом "
            "і продуктовий консалтинг для фінансових послуг."
        ),
        "vi": (
            "Tương lai của ngân hàng qua AI ứng dụng, thanh toán và bảo mật "
            "kháng lượng tử. Nghiên cứu, thư viện mã nguồn mở và tư vấn sản "
            "phẩm cho dịch vụ tài chính."
        ),
        "yo": (
            "Ọjọ́ iwájú ilé-ìfowópamọ́ nípasẹ̀ AI alámùúlò, ìsanwó àti ààbò tí ó "
            "lè dojú kọ kọ̀mpútà quantum. Ìwádìí, àwọn ibi ìkówèésí orísun-ṣíṣí "
            "àti ìgbani-nímọ̀ràn ọjà fún àwọn iṣẹ́ ìnáwó."
        ),
        "el": (
            "Το μέλλον των τραπεζών μέσα από την εφαρμοσμένη τεχνητή νοημοσύνη, "
            "τις πληρωμές και την ασφάλεια που αντέχει στους κβαντικούς "
            "υπολογιστές. Έρευνα, βιβλιοθήκες ανοιχτού κώδικα και συμβουλευτική "
            "προϊόντος για τις χρηματοοικονομικές υπηρεσίες."
        ),
        "fa": (
            "آیندهٔ بانکداری از رهگذر هوش مصنوعی کاربردی، پرداخت‌ها و امنیت مقاوم "
            "در برابر رایانش کوانتومی. پژوهش، کتابخانه‌های متن‌باز و مشاورهٔ محصول "
            "برای خدمات مالی."
        ),
        "mr": (
            "उपयोजित एआय, पेमेंट्स आणि क्वांटम-प्रतिरोधक सुरक्षेच्या माध्यमातून "
            "बँकिंगचे भविष्य. वित्तीय सेवांसाठी संशोधन, ओपन-सोर्स लायब्ररी आणि "
            "उत्पादन सल्लागारी."
        ),
        "ms": (
            "Masa depan perbankan menerusi AI gunaan, pembayaran dan keselamatan "
            "kalis kuantum. Penyelidikan, pustaka sumber terbuka dan perundingan "
            "produk untuk perkhidmatan kewangan."
        ),
        "ta": (
            "பயன்பாட்டுச் செயற்கை நுண்ணறிவு, கட்டணங்கள், குவாண்டம்-எதிர்ப்புப் "
            "பாதுகாப்பு வழியாக வங்கியியலின் எதிர்காலம். நிதிச் சேவைகளுக்கான "
            "ஆராய்ச்சி, திறந்த மூல நூலகங்கள், தயாரிப்பு ஆலோசனை."
        ),
        "te": (
            "అనువర్తిత ఏఐ, చెల్లింపులు, క్వాంటం-నిరోధక భద్రత ద్వారా బ్యాంకింగ్ "
            "భవిష్యత్తు. ఆర్థిక సేవల కోసం పరిశోధన, ఓపెన్-సోర్స్ లైబ్రరీలు, "
            "ఉత్పత్తి సలహా సేవలు."
        ),
        "zh-hans": (
            "以应用 AI、支付与抗量子安全塑造银行业的未来。面向金融服务的研究、开源库与产品咨询。"
        ),
        "zh-hant": (
            "以應用 AI、支付與抗量子安全塑造銀行業的未來。面向金融服務的研究、開源庫與產品諮詢。"
        ),
    }
    title = _home_titles.get(st.LANG_CODE, _en_home_title)
    desc = _home_descs.get(st.LANG_CODE, _en_home_desc)
    url_fr = f"{st.BASE}/{st.LANG_CODE}/"

    shell = _set_html_lang(shell)
    shell = _TITLE_RE.sub(f"<title>{_html.escape(title)}</title>", shell, count=1)
    shell = _DESC_META_RE.sub(rf"\g<1>{_html.escape(desc, quote=True)}\g<2>", shell, count=1)
    shell = _OG_TITLE_RE.sub(rf"\g<1>{_html.escape(title, quote=True)}\g<2>", shell, count=1)
    shell = _OG_DESC_RE.sub(rf"\g<1>{_html.escape(desc, quote=True)}\g<2>", shell, count=1)
    shell = _OG_URL_RE.sub(rf"\g<1>{url_fr}\g<2>", shell, count=1)
    shell = _OG_LOCALE_RE.sub(rf"\g<1>{st.LANG_LOCALE}\g<2>", shell, count=1)
    shell = _TW_TITLE_RE.sub(rf"\g<1>{_html.escape(title, quote=True)}\g<2>", shell, count=1)
    shell = _TW_DESC_RE.sub(rf"\g<1>{_html.escape(desc, quote=True)}\g<2>", shell, count=1)
    shell = _CANONICAL_RE.sub(rf"\g<1>{url_fr}\g<2>", shell, count=1)

    # Rewrite article URLs (EN → FR) + ensure all internal links keep visitor in /fr/.
    shell = rewrite_en_urls(shell)
    shell = rewrite_en_titles_in_text(shell)
    shell = rewrite_en_descs_in_text(shell)

    # Apply chrome (nav, footer, search, aria, language selector, dates).
    shell = translate_chrome(shell)

    # Per-section body patches.
    for pat, repl in st._HOME_FR_COMPILED:
        shell = pat.sub(repl, shell)

    # Card titles + tooltips for any article link.
    shell = rewrite_fr_link_titles(shell)
    shell = rewrite_newsroom_card_titles(shell)

    # Localise feed links.
    shell = localize_feed_links(shell)

    # Patch JSON-LD WebSite / Person / breadcrumb on the home page.
    def patch_node(node: dict) -> bool:
        t = node.get("@type")
        local = False
        if t == "WebSite":
            if "url" in node:
                node["url"] = url_fr
                local = True
            if "name" in node:
                node["name"] = title
                local = True
            if "description" in node:
                node["description"] = desc
                local = True
            if "inLanguage" in node:
                node["inLanguage"] = st.LANG_CODE
                local = True
        if t == "WebPage":
            if "url" in node:
                node["url"] = url_fr
                local = True
            if "name" in node:
                node["name"] = title
                local = True
            if "description" in node:
                node["description"] = desc
                local = True
            if "inLanguage" in node:
                node["inLanguage"] = st.LANG_CODE
                local = True
        return local

    shell = _patch_jsonld_scripts(shell, patch_node)

    # Reciprocal hreflang: strip any stale links here; the canonical full
    # 35-locale reciprocal set is emitted for the home by the postbuild
    # hreflang pass. (Previously this function also appended a 3-entry
    # en/self/x-default block, which the postbuild pass does NOT strip on
    # the home — unlike the hubs — so the block duplicated en/self/x-default
    # on every localized home. Dropping it leaves the postbuild set as the
    # single source of truth.)
    shell = re.sub(
        r'<link rel="alternate"[^>]+hreflang="[^"]+"[^>]*/>',
        "",
        shell,
    )
    shell = _localize_inlanguage_globally(shell, st.LANG_CODE)

    return shell


# ---------------------------------------------------------------------------
# Static-page translations (about, papers, projects, topics, tags, …)
# ---------------------------------------------------------------------------

_STATIC_WRAP_RE = re.compile(
    r'(<main\b[^>]*>\s*<div class="wrap[^"]*"[^>]*>)([\s\S]*?)(</div>\s*</main>)',
    re.IGNORECASE,
)


def _replace_static_main_body(html: str, fr_body: str) -> str:
    """Swap the inner content of ``<main><div class="wrap">…</div></main>``
    for a curated FR body. Falls back unchanged if the structure doesn't
    match (e.g. layouts that use a different wrapper)."""

    def repl(m: re.Match[str]) -> str:
        return m.group(1) + fr_body + m.group(3)

    return _STATIC_WRAP_RE.sub(repl, html, count=1)


def render_static_translation(slug: str) -> str | None:  # noqa: C901 — per-page pipeline
    """Fork the rendered EN page at ``public/{slug}/index.html``,
    translate chrome + body text, patch meta tags, swap canonical/og to
    point at ``/fr/{slug}/``, then return the HTML.
    """
    cfg = st.STATIC_PAGES_FR.get(slug)
    if cfg is None:
        return None
    shell_src = st.PUBLIC / slug / "index.html"
    if not shell_src.is_file():
        return None
    shell = shell_src.read_text(encoding="utf-8")

    title = cfg["title"]
    description = cfg["description"]
    subtitle = cfg.get("subtitle", description)
    keywords = cfg.get("keywords", "")
    fr_slug_str = st.STATIC_SLUG_FR.get(slug, slug)
    url_fr = f"{st.BASE}/{st.LANG_CODE}/{fr_slug_str}/"

    shell = _set_html_lang(shell)
    shell = _TITLE_RE.sub(f"<title>{_html.escape(title)}</title>", shell, count=1)
    shell = _DESC_META_RE.sub(rf"\g<1>{_html.escape(description, quote=True)}\g<2>", shell, count=1)
    if keywords:
        shell = _KW_META_RE.sub(rf"\g<1>{_html.escape(keywords, quote=True)}\g<2>", shell, count=1)
    shell = _OG_TITLE_RE.sub(rf"\g<1>{_html.escape(title, quote=True)}\g<2>", shell, count=1)
    shell = _OG_DESC_RE.sub(rf"\g<1>{_html.escape(description, quote=True)}\g<2>", shell, count=1)
    shell = _OG_URL_RE.sub(rf"\g<1>{url_fr}\g<2>", shell, count=1)
    shell = _OG_LOCALE_RE.sub(rf"\g<1>{st.LANG_LOCALE}\g<2>", shell, count=1)
    shell = _TW_TITLE_RE.sub(rf"\g<1>{_html.escape(title, quote=True)}\g<2>", shell, count=1)
    shell = _TW_DESC_RE.sub(rf"\g<1>{_html.escape(description, quote=True)}\g<2>", shell, count=1)
    shell = _CANONICAL_RE.sub(rf"\g<1>{url_fr}\g<2>", shell, count=1)
    # Hero subtitle (<p class="sub">…</p>) is per-page — replace it.
    shell = re.sub(
        r'<p class="sub">[^<]*</p>',
        f'<p class="sub">{_html.escape(subtitle)}</p>',
        shell,
        count=1,
    )

    # /playlists/ carries 39 generated cards, a featured band, five lane
    # heads, a 7-question FAQ and a device aside — far more body copy
    # than the chrome pass or a curated body can cover. Swap it from the
    # page's own catalogue first, while the EN anchors are still intact.
    if slug == "playlists":
        shell, missed = localize_playlists_page(shell, st.LANG_CODE)
        if missed:
            print(
                f"build_translations: playlists[{st.LANG_CODE}] — "
                f"{len(missed)} anchor(s) not found; first: {missed[0]!r}"
            )

    # /projects/ is 1,583 words of page copy in a generated 29-card
    # layout. Swap the text and keep the markup — see _projects.py.
    if slug == "projects":
        shell, problems = localize_projects_page(shell, st.LANG_CODE)
        for problem in problems:
            print(f"build_translations: projects[{st.LANG_CODE}] — {problem}")

    # Rewrite EN article URLs inside the body to FR counterparts.
    shell = rewrite_en_urls(shell)

    # Swap the EN <main> body for the curated FR body when one is
    # provided. Falls through to STATIC_BODY_PATCHES (light text-swap)
    # for pages without a curated translation.
    fr_body = st.STATIC_BODIES_FR.get(slug)
    if fr_body:
        shell = _replace_static_main_body(shell, fr_body)

    # EN title + description substitutions FIRST — before chrome runs
    # localize_en_dates() (which would otherwise rewrite "August 2026" →
    # "août 2026" inside an EN description and break the verbatim match).
    shell = rewrite_en_titles_in_text(shell)
    shell = rewrite_en_descs_in_text(shell)

    # Localise chrome (nav / footer / search / aria) + body text.
    shell = translate_chrome(shell)
    for pat, repl in st._STATIC_BODY_COMPILED:
        shell = pat.sub(repl, shell)

    # Rewrite article-card titles + tooltips on listing pages
    # (papers, projects, tags, topic hub, …) to the FR title.
    shell = rewrite_fr_link_titles(shell)
    shell = rewrite_newsroom_card_titles(shell)

    # Localise feed links.
    shell = localize_feed_links(shell)

    # Patch the WebPage / WebSite JSON-LD's @id, url, name, description.
    def patch_node(node: dict) -> bool:
        local = False
        t = node.get("@type")
        if t in ("WebPage", "AboutPage", "ProfilePage", "ContactPage", "CollectionPage"):
            if "name" in node:
                node["name"] = title
                local = True
            if "description" in node:
                node["description"] = description
                local = True
            if "url" in node:
                node["url"] = url_fr
                local = True
            if "inLanguage" in node:
                node["inLanguage"] = st.LANG_CODE
                local = True
        if t == "BreadcrumbList":
            items = node.get("itemListElement", [])
            for item in items:
                if not isinstance(item, dict):
                    continue
                pos = item.get("position")
                if pos == 1:
                    item["name"] = st.I18N_FR.get("Home", "Home")
                    item["item"] = f"{st.BASE}/"
                    local = True
                elif pos == 2:
                    item["name"] = title.split(" — ")[0]
                    item["item"] = url_fr
                    local = True
        return local

    shell = _patch_jsonld_scripts(shell, patch_node)

    # Reciprocal hreflang — strip stale links and emit fresh ones so the
    # language selector's JS resolves 🇬🇧 English to the EN counterpart.
    # Must run AFTER translate_chrome (which calls rewrite_static_links
    # and would rewrite an EN absolute URL → /fr/<slug>/).
    shell = re.sub(
        r'<link rel="alternate"[^>]+hreflang="[^"]+"[^>]*/>',
        "",
        shell,
    )
    en_url = f"{st.BASE}/{slug}/"
    hreflang_block = (
        f'<link rel="alternate" hreflang="en" href="{en_url}" />'
        f'<link rel="alternate" hreflang="{st.LANG_CODE}" href="{url_fr}" />'
        f'<link rel="alternate" hreflang="x-default" href="{en_url}" />'
    )
    shell = shell.replace("</head>", hreflang_block + "</head>", 1)
    shell = _localize_inlanguage_globally(shell, st.LANG_CODE)

    return shell


def write_static_translations() -> int:
    """Render and write every FR static page. Returns count written."""
    n = 0
    for slug in st.STATIC_PAGES_FR:
        page = render_static_translation(slug)
        if page is None:
            print(f"build_translations: skip static '{slug}' — EN shell missing")
            continue
        fr_slug_str = st.STATIC_SLUG_FR.get(slug, slug)
        dst = st.OUT / fr_slug_str / "index.html"
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(page, encoding="utf-8")
        n += 1

    # Topic sub-pages — clone each /topics/<topic>/ as /<lang>/<topics_slug>/<topic>/.
    # build_topics.py emits the EN versions before us; we fork + translate.
    topics_dir = st.PUBLIC / "topics"
    if topics_dir.is_dir():
        topics_slug_lang = st.STATIC_SLUG_FR.get("topics", "topics")
        for topic_dir in sorted(topics_dir.iterdir()):
            if not topic_dir.is_dir():
                continue
            src = topic_dir / "index.html"
            if not src.is_file():
                continue
            page = _render_topic_subpage_fr(topic_dir.name, src.read_text(encoding="utf-8"))
            dst = st.OUT / topics_slug_lang / topic_dir.name / "index.html"
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_text(page, encoding="utf-8")
            n += 1

    return n


def _render_topic_subpage_fr(topic_slug: str, shell: str) -> str:  # noqa: C901 — topic-page chrome patches
    """Fork an EN /topics/<slug>/ page into /fr/sujets/<slug>/."""
    cfg = st.TOPIC_FR_LABELS.get(
        topic_slug,
        {
            "title": topic_slug.replace("-", " ").title(),
            "lede": "",
        },
    )
    title = cfg["title"]
    lede = cfg["lede"]
    page_title = f"{title} — Sebastien Rousseau"
    topics_slug_lang = st.STATIC_SLUG_FR.get("topics", "topics")
    url_fr = f"{st.BASE}/{st.LANG_CODE}/{topics_slug_lang}/{topic_slug}/"

    shell = _set_html_lang(shell)
    shell = _TITLE_RE.sub(f"<title>{_html.escape(page_title)}</title>", shell, count=1)
    if lede:
        shell = _DESC_META_RE.sub(rf"\g<1>{_html.escape(lede, quote=True)}\g<2>", shell, count=1)
        shell = _OG_DESC_RE.sub(rf"\g<1>{_html.escape(lede, quote=True)}\g<2>", shell, count=1)
    shell = _OG_TITLE_RE.sub(rf"\g<1>{_html.escape(page_title, quote=True)}\g<2>", shell, count=1)
    shell = _OG_URL_RE.sub(rf"\g<1>{url_fr}\g<2>", shell, count=1)
    shell = _OG_LOCALE_RE.sub(rf"\g<1>{st.LANG_LOCALE}\g<2>", shell, count=1)
    shell = _CANONICAL_RE.sub(rf"\g<1>{url_fr}\g<2>", shell, count=1)
    shell = _TW_TITLE_RE.sub(rf"\g<1>{_html.escape(page_title, quote=True)}\g<2>", shell, count=1)
    if lede:
        shell = _TW_DESC_RE.sub(rf"\g<1>{_html.escape(lede, quote=True)}\g<2>", shell, count=1)

    # Rewrite article cards (EN slugs → FR slugs).
    shell = rewrite_en_urls(shell)

    # Translate the topic H1 + lede in the body if present.
    # Pattern from build_topics.py: <h1>{TITLE}</h1>...<p class="topic-lede">{LEDE}</p>
    shell = re.sub(
        r"<h1>[^<]+</h1>",
        f"<h1>{_html.escape(title)}</h1>",
        shell,
        count=1,
    )
    if lede:
        shell = re.sub(
            r'(<p class="topic-lede">)[^<]+(</p>)',
            rf"\g<1>{_html.escape(lede)}\g<2>",
            shell,
            count=1,
        )
    # Breadcrumb in body: "Home · Topics · Title" → "Accueil · Sujets · Titre"
    shell = re.sub(
        r'<nav aria-label="Breadcrumb" class="topic-breadcrumb">[\s\S]*?</nav>',
        f'<nav aria-label="Fil d\'Ariane" class="topic-breadcrumb">'
        f'<a href="/{st.LANG_CODE}/">Accueil</a> &middot; '
        f'<a href="/{st.LANG_CODE}/{st.STATIC_SLUG_FR.get("topics", "topics")}/index.html">Sujets</a> &middot; '
        f"<span>{_html.escape(title)}</span></nav>",
        shell,
        count=1,
    )
    # Topics-page lede on the hub
    shell = re.sub(
        r"Curated topic clusters[^<]+",
        "Clusters de sujets curated — choisissez un fil et suivez-le à travers l'archive.",
        shell,
    )
    shell = re.sub(
        r"PILLARS",
        "PILIERS",
        shell,
    )
    shell = re.sub(
        r">Topics</h1>",
        ">Sujets</h1>",
        shell,
    )
    shell = re.sub(
        r"PILLAR · TOPIC",
        "PILIER · SUJET",
        shell,
    )
    shell = re.sub(
        r"(\d+) article\(s\)",
        r"\1 article(s)",
        shell,
    )

    # Patch JSON-LD breadcrumb + URLs to point to /fr/topics/.
    def patch_node(node: dict) -> bool:
        local = False
        t = node.get("@type")
        if t == "CollectionPage":
            if "name" in node:
                node["name"] = title
                local = True
            if "description" in node and lede:
                node["description"] = lede
                local = True
            if "url" in node:
                node["url"] = url_fr
                local = True
            if "inLanguage" in node:
                node["inLanguage"] = st.LANG_CODE
                local = True
        if t == "BreadcrumbList":
            for item in node.get("itemListElement", []):
                if not isinstance(item, dict):
                    continue
                pos = item.get("position")
                if pos == 1:
                    item["name"] = st.I18N_FR.get("Home", "Home")
                    item["item"] = f"{st.BASE}/"
                    local = True
                elif pos == 2:
                    item["name"] = "Sujets"
                    item["item"] = (
                        f"{st.BASE}/{st.LANG_CODE}/{st.STATIC_SLUG_FR.get('topics', 'topics')}/"
                    )
                    local = True
                elif pos == 3:
                    item["name"] = title
                    item["item"] = url_fr
                    local = True
        return local

    shell = _patch_jsonld_scripts(shell, patch_node)

    # EN title/description substitutions FIRST — before chrome runs
    # localize_en_dates() which would otherwise break verbatim matches.
    shell = rewrite_en_titles_in_text(shell)
    shell = rewrite_en_descs_in_text(shell)
    # Chrome localisation (includes localize_en_dates)
    shell = translate_chrome(shell)
    shell = rewrite_fr_link_titles(shell)
    shell = rewrite_newsroom_card_titles(shell)
    # Reciprocal hreflang
    shell = re.sub(
        r'<link rel="alternate"[^>]+hreflang="[^"]+"[^>]*/>',
        "",
        shell,
    )
    en_url = f"{st.BASE}/topics/{topic_slug}/"
    hreflang_block = (
        f'<link rel="alternate" hreflang="en" href="{en_url}" />'
        f'<link rel="alternate" hreflang="{st.LANG_CODE}" href="{url_fr}" />'
        f'<link rel="alternate" hreflang="x-default" href="{en_url}" />'
    )
    shell = shell.replace("</head>", hreflang_block + "</head>", 1)
    # Feed links
    shell = localize_feed_links(shell)
    shell = _localize_inlanguage_globally(shell, st.LANG_CODE)
    return shell
