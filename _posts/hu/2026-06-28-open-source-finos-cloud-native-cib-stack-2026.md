---
title: "Nyílt forráskód, FINOS és a felhőnatív CIB-verem"
tags: "open source banking, FINOS, Linux Foundation, cloud-native CIB, Rust banking, PSD3, FiDA, supply-chain, SBOM, SLSA, sigstore, CycloneDX, SPDX, CNCF, OSSF, MIT, Apache 2.0, BSD-3-Clause, DORA, Basel III, MCP"
subtitle: "A Morgan Stanley, a JPMorgan és a Citi egyre inkább a FINOS-ra és a Linux Foundationre helyezi a hangsúlyt. Egy Rust-alapú, nulla függőségű verem: noyalib, http-handle, hsh, KyberLib, megmutatja, hogyan néz ki a felhőnatív CIB-verem 2026-ban."
description: "Hogyan alakítja át a FINOS, a Linux Foundation és egy Rust-alapú, nulla függőségű verem a felhőnatív CIB-vermet: tehetség, megfelelés, PSD3 és az ellátási lánc eredetigazolása."
date: "June 28, 2026"
language: "hu"
locale: "hu_HU"
banner: "https://cloudcdn.pro/stocks/images/joe-taylor-T3o-XtCfe6U.webp"
banner_alt: "Egy vállalati-befektetési banki kereskedési terem üveg és acél belső csarnoka, amely a FINOS, a Linux Foundation és a Rust-könyvtárak köré épülő nyílt forráskódú, felhőnatív CIB-vermet jelképezi."
keywords: "nyílt forráskódú bankolás, FINOS, Linux Foundation, felhőnatív CIB, Rust bankolás, modernizáció, Morgan Stanley nyílt forráskód, JPMorgan nyílt forráskód, PSD3, nyílt pénzügyek, FiDA, ellátásilánc-biztonság, SBOM, CycloneDX, SPDX, SLSA, sigstore, CNCF, OSSF, MIT licenc, Apache 2.0, BSD-3-Clause, DORA, Basel III, MCP"
---

## Nyílt forráskód, FINOS és a felhőnatív CIB-verem

2026 júniusában a vállalati-befektetési banki (CIB) technológiai napirend végre felhagyott a színleléssel. A Morgan Stanley, a JPMorgan és a Citi a FINOS irányító testületében ül, és a nyílt forráskódot immár alapinfrastruktúraként kezeli, nem pedig mellékprojektként: ezt a váltást a Banking Dive is megörökítette a három bankról szóló friss beszámolójában, amelyben azok egyre inkább a [FINOS](https://www.finos.org/) és a [Linux Foundation](https://www.linuxfoundation.org/) révén megosztott kódra helyezik a hangsúlyt ([Banking Dive, 2026](https://www.bankingdive.com/news/bank-technology-open-source-finos-morgan-stanley-jpmorgan-citi/743937/ "Bank tech leaders double down on open source")). Az ok kényelmetlen a szállítók számára: a CIB-veremnek immár teljes egészében átvizsgálhatónak kell lennie, és a zárt dobozok nem élnek túl egy DORA 5. cikk szerinti auditot.

Ez a cikk ezt a váltást a mérnöki oldallal köti össze. Az általam közzétett Rust-könyvtárak: [noyalib](https://github.com/sebastienrousseau/noyalib), [http-handle](https://github.com/sebastienrousseau/http-handle), [hsh](https://github.com/sebastienrousseau/hsh), [KyberLib](https://github.com/sebastienrousseau/kyberlib), [html-generator](https://github.com/sebastienrousseau/html-generator), [Shokunin SSG](https://github.com/sebastienrousseau/shokunin), önmagukban nem a lényeget jelentik. Konkrét példák arra, hogyan néz ki ma egy felhőnatív CIB-verem, ha komolyan vesszük a FINOS tézisét: megengedő licencek, nulla `unsafe`, aláírt műtermékek és fordítási időben beépített ellátásilánc-eredetigazolás.

## 01. Miért nyitnak a CIB-ek a nyílt forráskód felé

Három nyomás tereli a CIB-eket a nyílt forráskód felé, és egyik sem ideológiai.

**Tehetség.** 2026-ban a legerősebb infrastruktúra-mérnökök nyilvánosan fejlesztenek. A 2025-ös FINOS State of Open Source in Financial Services jelentés a közreműködői bázist a növekedés felső sávjába helyezi, és bankokhoz kötődő karbantartók immár láthatók a CNCF futásidejű projektjeiben és a FINOS munkafolyamataiban ([Linux Foundation, 2025](https://www.linuxfoundation.org/hubfs/Research%20Reports/05_FINOS_2025_Report.pdf?hsLang=en "State of Open Source in Financial Services 2025")). Amikor egy Tier-1 CTO-nak olyan tapasztalt Rust- vagy Kotlin-mérnökre van szüksége, aki képes leszállítani egy klíringrendszer újraírását, az a mérnök elvárja, hogy upstream commitolhasson. A kizárólag zárt forráskódot használó cégek már korán elveszítik a toborzási beszélgetést.

**Megfelelés.** A DORA 5. cikk át nem ruházható IKT-kockázati elszámoltathatóságot ró az igazgatótanácsra. A Basel III a működési kockázati tőkét a kiesésekhez köti. Mindkét szabályozás feltételezi, hogy az intézmény minden összetevőt auditálni tud a gyártási útvonalon, és ez szerkezetileg egyszerűbb a MIT, Apache 2.0 vagy BSD-3-Clause licencű, megengedő nyílt forráskóddal, mint egy fekete dobozos ISV-kiadással, ahol az SBOM annyi, hogy „bízz bennünk”. A CycloneDX és SPDX anyagjegyzékek, a SLSA eredetigazolások és a sigstore-aláírások ma már azt a minimumot jelentik, amelyet egy szabályozó egy kiadási folyamathoz csatolva elvár.

**Szállítási sebesség.** Az a CIB-platformcsapat, amely egy fizetési motor módosítását napok, nem pedig negyedévek alatt szállítja le, nem hőstettekkel győz. Megosztott alaprétegen győz: Kubernetes, OpenTelemetry, [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) sémakönyvtárak, FINOS Common Domain Model, amelyek újraimplementálásáért senki sem fizet. A gazdaságosság már nem az egyedi megoldások mellett szól.

Három nyomás, egy következtetés. A nyílt forráskódra váltás szállítási döntés, nem beszerzési.

## 02. A Rust-alapú, nulla függőségű verem

A felhőnatív CIB-verem 2026-ban már nem a LAMP-korszak „nyílt forráskód = Linux + nginx + Postgres” képe. Megengedő licencű, memóriabiztos összetevők rétegzett halmaza, amelyek mindegyike saját SBOM-mal, saját eredetigazolással és saját minimális támadási felülettel rendelkezik. Az általam karbantartott Rust-könyvtárak tisztán illeszkednek erre a rétegzésre.

- **Peremhálózati bejövő forgalom.** A [http-handle](https://github.com/sebastienrousseau/http-handle) egy nulla függőségű, RFC 7230 / 9112-kompatibilis HTTP/1.1-kiszolgáló, biztonságos Rustban megírva: arra a pillanatra készült, amikor egy CIB-platformcsapat rájön, hogy a bejövő rétegnek nem szabadna 200 tranzitív crate-et behúznia. Az érvelést a [http-handle: nulla függőségű peremhálózati bejövő forgalom bankoláshoz Rustban](https://sebastienrousseau.com/2026-06-20-http-handle-zero-dependency-edge-ingress-banking-rust-2026) fejti ki.
- **Konfigurációs sík.** A [noyalib](https://github.com/sebastienrousseau/noyalib) a YAML 1.2-t 406/406 specifikációmegfeleléssel, JSON-Schema-validációval és veszteségmentes konkrét szintaxisfával elemzi, így a Kubernetes-manifesztek, az MCP-kiszolgálóregiszterek és a CI-munkafolyamatok megszűnnek néma támadási felület lenni. Lásd: [Miért van szüksége a YAML-nek biztonságosabb Rust-veremre az AI, az MCP és a pénzügyi infrastruktúra számára 2026-ban](https://sebastienrousseau.com/2026-06-18-noyalib-safe-yaml-rust-ai-mcp-financial-infrastructure-2026).
- **Kriptográfiai alapelemek.** A [hsh](https://github.com/sebastienrousseau/hsh) Argon2id, bcrypt és scrypt jelszóhashelést biztosít állandó idejű ellenőrző API-val. A [KyberLib](https://github.com/sebastienrousseau/kyberlib) ML-KEM-512/768/1024-et valósít meg FIPS 203 alatt a poszt-kvantum migrációhoz, amelyet a [KyberLib és a poszt-kvantum banki migráció 2026-ban](https://sebastienrousseau.com/2026-06-12-kyberlib-post-quantum-banking-migration-standards-code-2026) tár fel.
- **Tartalom- és peremkézbesítés.** A [html-generator](https://github.com/sebastienrousseau/html-generator) az akadálymentes Markdownt strukturált HTML-be fordítja; a [Shokunin SSG](https://github.com/sebastienrousseau/shokunin) építi a most olvasott kiadványt; a [CloudCDN](https://sebastienrousseau.com/2026-06-11-cloudcdn-open-source-blueprint-ai-native-edge-2026) pedig előtte áll nyílt forráskódú, AI-natív peremként.

Ezek egyike sem „keretrendszer” a hagyományos banki értelemben. Kicsi, megengedő licencű, aláírt összetevők, kifejezett fenyegetésmodellel. Ez az a működési forma, amelyet a FINOS tézise ösztönöz, és amelyet egy CIB-platformcsapat diavetítés nélkül is meg tud védeni egy szabályozó előtt.

Egy apró, őszinte fenntartás: a cél nem „a bank újraírása Rustban”. Az, hogy a CIB-platformcsapatok számára biztosítsuk egy memóriabiztos, alacsony függőségű verem lehetőségét a teherhordó rétegekben: bejövő forgalom, elemzés, kriptográfia, build, ellátási lánc, anélkül, hogy máshol vallásos döntést kényszerítenénk ki.

## 03. A nyílt forráskód az ISO-, AI- és kvantumnapirendek alapja

2026 három strukturális CIB-napirendje: az ISO 20022 átállás, az ügynöki AI a működésben és a poszt-kvantum kriptográfiai migráció, mind átvizsgálható kódon fut. Egyikük sem működik zárt forráskódú veremként.

**ISO 20022.** A pacs.008 / pacs.009 / camt sémacsalád ma már a nagykereskedelmi fizetések alapértelmezése. A FINOS a Common Domain Modelt olyan nyílt forráskódú Java- és Kotlin-könyvtárak mellett üzemelteti, amelyek elemzik, validálják és irányítják ezeket az üzeneteket. A [pacs.008-automatizálás és ISO 20022 bankközi fizetések](https://sebastienrousseau.com/2026-06-15-pacs008-automation-iso-20022-interbank-payments-2026) munkája megmutatja, hogyan áll össze egy klíringszintű folyamat ezekből a nyílt összetevőkből: sémavalidáció, strukturált átutalási adatok, végpontok közötti nyomon követhetőség, anélkül, hogy minden banknál újra kellene építeni az elemzőt.

**Ügynöki AI.** A Model Context Protocol (MCP) az a lingua franca, amely lehetővé teszi, hogy az AI-ügynökök belső banki eszközöket hívjanak, és az MCP-kiszolgálók YAML-regisztereken, OAuth-korlátozott szolgáltatásfiókokon és auditnapló-folyamatokon futnak. A vezérlősík nyílt forráskódú, mert annak kell lennie: bármely ügynöknek, amely éles főkönyvhöz nyúl, átvizsgálható, körülhatárolt munkafolyamatra van szüksége. Az az érv, hogy ezt mérnöki problémaként, ne pedig szállítóválasztásként kezeljük, a [Miért van szüksége a YAML-nek biztonságosabb Rust-veremre](https://sebastienrousseau.com/2026-06-18-noyalib-safe-yaml-rust-ai-mcp-financial-infrastructure-2026) cikken és az [AI-tudatos dotfile-ok 2026-ban](https://sebastienrousseau.com/2026-06-16-ai-aware-dotfiles-secure-reproducible-workstation-2026) munkaállomás-munkán keresztül vezet.

**Poszt-kvantum kriptográfia.** A FIPS 203 (ML-KEM) és a FIPS 204 (ML-DSA) ma már a migrációs célok. A hibrid X25519MLKEM768 kulcscsere a gyakorlati alapértelmezés a TLS 1.3-ban. Ebből semmi sem működik olyan nyílt implementációk nélkül, amelyeket az auditorok és a bankok kriptográfiai csapatai sorról sorra el tudnak olvasni: a [KyberLib](/2023-11-28-kyberlib-a-rust-powered-shield-against-quantum-threats/index.html) az egyik példa, a tágabb migrációs keretezés pedig a [KyberLib és a poszt-kvantum banki migráció 2026-ban](https://sebastienrousseau.com/2026-06-12-kyberlib-post-quantum-banking-migration-standards-code-2026) tárgya.

Három napirend. Egy közös függőség: nyílt kód, amelyet a sigstore ír alá, a SLSA igazol, egy CycloneDX- vagy SPDX-SBOM-ban szerepel, és az OSSF-pontkártyák szabályoznak. Ez a felhőnatív CIB-verem 2026-ban.

## 04. Platformizáció a PSD3 és a FiDA keretében

Az európai platformizációs napirend: a PSD3, a fizetési szolgáltatásokról szóló rendelet és a pénzügyi adathozzáférési keretrendszer (FiDA), szabályozói elköteleződés a nyílt pénzügyek mellett. Feltételezi, hogy a bankok nagy léptékben képesek adatáramlásokat feltárni, szabályozni és auditálni. A nyílt szabványok az előfeltételt jelentik, nem a mellékhatást.

A Consultancy.uk 2026-os kitekintése a nyílt bankolás platformnövekedés érdekében történő megszervezéséről ugyanezt a megfigyelést teszi az üzleti oldalról: a PSD3 keretében nyertes intézmények azok, amelyek az API-állományt termékként kezelik, nem pedig utólagos megfelelési feladatként ([Consultancy.uk, 2026](https://www.consultancy.uk/news/42202/orchestrating-open-banking-for-platform-growth-2026-outlook "Orchestrating open banking for platform growth - 2026 outlook")). Ez a hozzáállás lehetetlen zárt veremen. Az API-k termékesítéséhez verziózott OpenAPI-specifikációk, automatizált szerződéstesztek, minden fogyasztóra kiterjedő megfigyelhetőség és olyan szabályozási réteg szükséges, amelyet egy auditor végig tud járni. 2026-ban ezen alapelemek mindegyike nyílt forráskódú, és többségük CNCF- vagy FINOS-projektekben található.

Ugyanez a logika kiterjed a FiDA tágabb adathozzáférési peremére is: nyugdíjak, jelzáloghitelek, befektetési termékek. Az a bank, amely az elemzését, a bejövő forgalmát, a konfigurációját és a kriptográfiáját átvizsgálható kóddal felügyeli, újratervezés nélkül tudja kiterjeszteni a peremet. Az a bank, amely ezeket a rétegeket zárt szállítókhoz szervezte ki, a következő három évben integrációs tanácsadókat fog fizetni. A FINOS tézise lényegében platformizációs tézis: birtokold a szabványokat, oszd meg az alapréteget, versenyezz a felületen.

## Következtetés

A CIB-verem 2026-ban alapból nyílt. Nem ideológiából, hanem mert a három nyomás: tehetség, megfelelés, szállítási sebesség, ugyanabba az irányba húz, és a szabályozók (DORA, Basel III, PSD3, FiDA) ezt megerősítették. A Banking Dive Morgan Stanleyről, JPMorganról és Citiről szóló beszámolója egy olyan magánbeszélgetés nyilvános változata, amelyet a vezető platformcsapatok két éve folytatnak.

Az igazgatótanácsok számára a következtetés egyértelmű. A kérdés már nem az, hogy „használjunk-e nyílt forráskódot”. Hanem: rendelkezünk-e az SBOM-okkal, a SLSA-eredetigazolással, a sigstore-aláírásokkal, az OSSF-pontkártyákkal és a FINOS-hoz igazodó hozzájárulási szabályzattal ahhoz, hogy biztonságosan használjuk. Ha a válasz nem, akkor a szabályozónak adott válasz is nem lesz.

A mérnöki vezetők számára a következtetés élesebb. Válaszd ki a teherhordó rétegeket: bejövő forgalom, elemzés, kriptográfia, build, ellátási lánc, és szabványosíts megengedő licencű, memóriabiztos, kifejezett fenyegetésmodellel rendelkező összetevőkre. Az e cikkben szereplő Rust-alapú, nulla függőségű példák egy érvényes halmazt alkotnak. A lényeg a forma, nem a márka. Építsd meg az alapréteget, hogy a felület gyorsan mozoghasson.

A nyílt forráskód már nem a modernizáció kérdése. Ez a modernizáció válasza.
