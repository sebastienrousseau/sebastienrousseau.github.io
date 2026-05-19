---
title: "Reset kvantové kryptografie v roce 2026: standardy PQC, ujištění o QKD a migrační práce, kterou banky nemohou odložit"
subtitle: "Kvantová kryptografie přešla od skenování horizontu k implementační disciplíně: standardy NIST PQC jsou připraveny, britská NCSC zúžila volbu algoritmů, protokolová práce IETF stále zraje a ujištění o QKD se posouvá z laboratorní důvěry k certifikační dikci."
description: "Kvantová kryptografie v roce 2026 už není debatou o tom, zda jsou kvantové počítače na spadnutí. Je to migrační program napříč postkvantovou kryptografií, kryptografickou agilitou, ujištěním o kvantové distribuci klíčů, protokolovými standardy, připraveností dodavatelů a dlouhožijícími finančními daty, která jsou již vystavena riziku harvest-now-decrypt-later."
date: "May 18, 2026"
language: "cs-CZ"
locale: "cs_CZ"
banner: "https://cloudcdn.pro/stocks/images/alex-shuper-YYZnrK8NrSw-unsplash.webp"
banner_alt: "Mapa migrace na kvantově odolnou kryptografii pro rok 2026 zobrazující standardy NIST PQC, hybridní protokolovou práci, ujištění QKD, kryptografickou agilitu a úrovně rizika bankovních dat"
keywords: "kvantová kryptografie 2026, postkvantová kryptografie, NIST FIPS 203, FIPS 204, FIPS 205, ML-KEM, ML-DSA, SLH-DSA, NCSC PQC, IETF TLS, IPsec, RFC 9794, hybridní výměna klíčů, QKD, ETSI QKD, ISO IEC 23837, kryptografická agilita, harvest now decrypt later, HNDL, kryptografie finančních služeb, bankovní bezpečnost"
---

# Reset kvantové kryptografie v roce 2026: standardy PQC, ujištění o QKD a migrační práce, kterou banky nemohou odložit

Kvantová kryptografie se v roce 2026 rozdělila do dvou praktických směrů. Postkvantová kryptografie je nyní implementačním programem, protože NIST říká, že tři postkvantové standardy jsou připraveny k použití a federální systémy s nimi musí zacházet jako se standardy FIPS ([NIST](https://www.nist.gov/pqc "NIST Post-Quantum Cryptography")); kvantová distribuce klíčů se stává otázkou ujištění a certifikace, protože nasazení QKD potřebují evaluační dikci, ochranné profily a provozní standardy, nikoli jen laboratorní demonstrace ([ID Quantique / ETSI QKD 016](https://www.idquantique.com/etsi-releases-qkd-protection-profile/ "ETSI vydává ochranný profil QKD")).

---

> **Shrnutí pro vedení / Klíčové závěry**
>
> - **NIST přesunul PQC do implementace.** Aktuální standardy jsou FIPS 203 pro ustavení klíče ML-KEM, FIPS 204 pro podpisy ML-DSA a FIPS 205 pro podpisy SLH-DSA, přičemž NIST nabádá organizace, aby identifikovaly zranitelnou kryptografii a začaly s migrací nyní ([NIST](https://www.nist.gov/pqc "NIST Post-Quantum Cryptography")).
> - **Britská NCSC zúžila praktické volby.** Pro většinu případů použití doporučuje ML-KEM-768 a ML-DSA-65 a varuje, že systémy by se měly spoléhat na robustní implementace finálních standardů, nikoli na experimenty kompatibilní s návrhy ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "NCSC – další kroky v přípravě na PQC")).
> - **Připravenost protokolů je nerovnoměrná.** IETF aktualizuje TLS a IPsec pro PQC a hybridní výměnu klíčů, ale NCSC upozorňuje, že provozní systémy by měly upřednostnit publikované RFC před měnícími se Internet Drafts ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "NCSC – další kroky v přípravě na PQC")).
> - **Hybridní řešení je přechodový mechanismus, ne cílový stav.** Hybridní schémata s veřejným klíčem plus postkvantová schémata pomáhají rozfázovat migraci a zajistit se proti implementačnímu riziku, ale přidávají složitost a mohou vyžadovat druhou migraci na čistě PQC později ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "NCSC – další kroky v přípravě na PQC")).
> - **QKD není náhradou za PQC.** QKD může sloužit specializovaným linkám s vysokým ujištěním, ale její bankovní relevance závisí na certifikaci, interoperabilitě, provozních nákladech a integraci se stávajícími systémy správy klíčů, nikoli jen na fyzice ([ID Quantique / ETSI QKD 016](https://www.idquantique.com/etsi-releases-qkd-protection-profile/ "ETSI vydává ochranný profil QKD")).
> - **Otázka na úrovni banky je inventura.** Finanční instituce, která neumí lokalizovat RSA, ECDH, ECDSA, EdDSA, proprietární VPN kryptografii, šablony HSM, doby životnosti certifikátů a kryptografii spravovanou dodavateli, nemůže migrovat, bez ohledu na to, které standardy jsou k dispozici.
> - **Riziko je již aktivní.** Útoky harvest-now-decrypt-later činí dlouhožijící finanční data zranitelnými ještě předtím, než existují kryptograficky relevantní kvantové počítače, protože protivník dnes potřebuje jen nasbírat šifrový text.
> - **Kryptografická agilita je trvanlivá kontrola.** Vítězná architektura není jednorázová výměna RSA za ML-KEM; je to platformová schopnost rotovat algoritmy, parametry, knihovny, certifikáty, hardwarové politiky a protokolové režimy, aniž by se musela banka přestavovat.
>
---

## Proč na tomto týdnu záleží

Diskuse o standardech překročila bod abstrakce. Veřejný návod NIST říká, že organizace by měly začít aplikovat nové standardy nyní, identifikovat, kde se používají zranitelné algoritmy, a plánovat aktualizace produktů, služeb a protokolů ([NIST](https://www.nist.gov/pqc "NIST Post-Quantum Cryptography")). Tato dikce je důležitá, protože mění PQC z výzkumného tématu v závislost technologické obnovy.

Časování je rovněž důležité, protože finanční data mají dlouhý poločas důvěrnosti. Materiály k M&A, treasury toky, vyšetřování sankcí, identifikační dokumenty klientů, metadata směrování plateb a záznamy o velkoobchodním vypořádání mohou zůstat citlivé roky. Kvantový počítač, který prolomí klasickou kryptografii s veřejným klíčem, dnes nemusí existovat, aby byla expozice racionální už dnes.

## Kryptografická základna 2026: čtyři pracovní proudy

### 1. Standardy PQC jsou dostatečně připraveny pro plánování

První základnou je algoritmická. Program PQC NIST nyní dává technologickým lídrům pojmenované cíle: ML-KEM pro ustavení klíčů, ML-DSA pro obecné digitální podpisy a SLH-DSA pro podpisy založené na hashích ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "NCSC – další kroky v přípravě na PQC")). Praktickým dopadem je, že týmy nákupu, architektury a správy dodavatelů mohou přestat klást otázku, zda standardy PQC budou existovat, a začít se ptát, kdy je každý systém bude podporovat.

Tvrdším bodem je kompatibilita. NCSC varuje, že implementace založené na návrzích standardů nemusí být kompatibilní s finálními standardy, což je přesně ten druh detailu, který rozbíjí migrace velkých bank, pokud se ignoruje ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "NCSC – další kroky v přípravě na PQC")). Banky by proto měly oddělit experimentální piloty od produkčních migračních cest.

### 2. Protokoly jsou úzkým hrdlem

Algoritmy samy o sobě nezajišťují bankovní provoz. TLS, IPsec, SSH, S/MIME, platební API, integrace HSM a stacky správy certifikátů – to vše potřebuje podporu na úrovni protokolu. NCSC uvádí, že IETF aktualizuje široce používané protokoly jako TLS a IPsec tak, aby algoritmy PQC mohly být začleněny do mechanismů výměny klíčů a podpisů ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "NCSC – další kroky v přípravě na PQC")).

To vytváří etapový implementační problém. Banka může okamžitě inventarizovat kryptografii, okamžitě vyžadovat dodavatelské roadmapy a okamžitě navrhnout kryptografickou agilitu, ale stále může čekat na stabilní implementace protokolů, než přesune kriticky důležité produkční kanály.

### 3. QKD se stává disciplínou ujištění

Kvantová distribuce klíčů zůstává relevantní pro vysoce specializované linky, zvláště tam, kde instituce kontroluje koncové body a síťové trasy. Důležitým vývojem roku 2026 není jeden nový QKD box; je to vznik certifikační dikce, kde je ETSI GS QKD 016 popsáno jako milník ochranného profilu pro evaluaci produktů QKD ([ID Quantique / ETSI QKD 016](https://www.idquantique.com/etsi-releases-qkd-protection-profile/ "ETSI vydává ochranný profil QKD")).

Pro banky to posouvá nákupní konverzaci. Správnou otázkou už není, zda je QKD principiálně kvantově bezpečná. Správnou otázkou je, zda zařízení, integrace, proces správy klíčů, provozní prostředí a certifikační důkazy splňují bankovní model hrozeb.

### 4. Kryptografická agilita je architektura

Kryptografická agilita je schopnost změnit algoritmy bez změny celého systému. Pokrývá softwarové knihovny, vyjednávání protokolu, politiku HSM, profily certifikátů, životnost klíčů, podpisové služby, audit a cesty zpětného vrácení. Bez ní se každá kryptografická migrace stává projektem na míru.

To je hlavní architektonická lekce. Postkvantový přechod nebude poslední kryptografický přechod, kterému finanční systém čelí. Banky, které si vybudují kryptografickou agilitu nyní, získají znovupoužitelnou kontrolní rovinu pro aktualizace algoritmů, dodavatelské riziko, mimořádné odvolávání a regulatorní důkazy.

## Co by banky měly udělat nyní

### Vybudovat inventář kryptografických aktiv

Prvním dodávkou je kryptografický soupis materiálu. Měl by zahrnovat algoritmy s veřejným klíčem, délky klíčů, certifikační autority, šablony HSM, verze TLS, VPN produkty, platební brány, API třetích stran, mobilní SDK, obálky šifrování dat v klidu, podpisové klíče, procesy podepisování firmwaru a kryptografii spravovanou dodavateli.

Inventář by měl rozlišovat mezi důvěrností a autentičností. Dlouhožijící šifrovaná data jsou vystavena riziku harvest-now-decrypt-later, zatímco dlouhožijící podpisové klíče vytvářejí budoucí riziko padělání, pokud zůstávají zakotveny ve zranitelných algoritmech s veřejným klíčem.

### Segmentovat podle poločasu dat

Ne všechna data potřebují stejné pořadí migrace. Autorizační zpráva o platbě kartou v reálném čase může mít jiný poločas důvěrnosti než vyšetřování sankcí, soubor korporátní akvizice, balíček identity privátního bankovnictví nebo dokument o emisi suverénního dluhu. Proto kvantová migrace patří ke klasifikaci dat, nejen k síťové bezpečnosti.

Prioritou by měly být systémy, které chrání dlouhožijící data zranitelným ustavením klíče. To jsou systémy, kde dnešní sběr vytváří zítřejší expozici.

### Vynutit dodavatelské roadmapy do smluv

NIST říká, že produkty, služby a protokoly potřebují pro přechod aktualizace ([NIST](https://www.nist.gov/pqc "NIST Post-Quantum Cryptography")). To znamená, že se musí změnit smluvní dikce. Dodavatelé by měli zveřejňovat časové harmonogramy podpory PQC, kompatibilitu s finálními standardy, chování v hybridním režimu, omezení hardwarových modulů, dopady na výkon, podporu profilů certifikátů a fallback kontroly.

Dodavatel, který říká jen „kvantově bezpečná roadmapa“, neodpověděl na otázku. Banka potřebuje data, algoritmy, integrační hranice a důkazy.

## PQC, QKD a hybridní řešení: praktická rozhodovací tabulka

| Kontrola | Nejlepší použití | Stav 2026 | Bankovní výhrada |
|---|---|---|---|
| **ML-KEM / FIPS 203** | Ustavení klíče pro budoucí důvěrnost | Standardizováno a připraveno pro implementační plánování ([NIST](https://www.nist.gov/pqc "NIST Post-Quantum Cryptography")) | Před kritickým produkčním nasazením potřebuje podporu protokolů a knihoven |
| **ML-DSA / FIPS 204** | Obecné digitální podpisy | NCSC doporučuje pro většinu obecných případů použití podpisů ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "NCSC – další kroky v přípravě na PQC")) | Řetězce certifikátů a migrace PKI jsou provozně obtížné |
| **SLH-DSA / FIPS 205** | Podpisy založené na hashích pro podpisování firmwaru a softwaru | Finální standard NIST referencovaný NCSC ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "NCSC – další kroky v přípravě na PQC")) | Větší podpisy mohou ovlivnit omezená prostředí |
| **Hybridní PQ/T schémata** | Přechodná migrace a interoperabilita | Užitečné jako přechodové opatření ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "NCSC – další kroky v přípravě na PQC")) | Přidává složitost a může vyžadovat druhou migraci |
| **QKD** | Specializované linky s vysokým ujištěním | Práce na ujištění zraje prostřednictvím aktivity ETSI okolo ochranného profilu ([ID Quantique / ETSI QKD 016](https://www.idquantique.com/etsi-releases-qkd-protection-profile/ "ETSI vydává ochranný profil QKD")) | Neřeší obecnou autentizaci v internetovém měřítku ani podnikový kryptografický inventář |

## Co to znamená podle typu instituce

### Univerzální banky první úrovně

Banky první úrovně potřebují programovou kancelář, nikoli proof of concept. Cílový provozní model by měl kombinovat kryptografický inventář, vynucování vůči dodavatelům, správu roadmapy HSM, testovací prostředí pro hybridní TLS/IPsec a regulátorům připravené důkazy. Nejhodnotnější včasná práce není okamžitá výměna každé šifry; je to vybudování kontrolní roviny, která činí změnu bezpečnou.

### Středně velké a regionální banky

Banky střední úrovně by měly s PQC zacházet jako se cvičením správy dodavatelů a standardizace platforem. Mohou se vyhnout drahé práci na míru tím, že soustředí systémy kolem podporovaných knihoven, standardních TLS stacků, řízených služeb certifikátů a jasných termínů dodavatelů. Klíčovým rizikem je skrytá kryptografie uvnitř appliancí, platebních bran a starší middlewaru.

### Fintech, PSP a instituce blízké kryptu

Fintech může postupovat rychleji, protože obvykle má méně starých kotev důvěry. Rizikem je samolibost v API třetích stran, výchozích nastaveních cloudových KMS, infrastruktuře peněženek a integracích custody. Firmy blízké kryptu by měly zvláště dbát na to, aby si nepletly narativy o nativní bezpečnosti blockchainu s postkvantovou připraveností.

### Inženýři a bezpečnostní architekti

Inženýrská disciplína je konkrétní: přidat metadata algoritmů do inventářů služeb, logovat vyjednané režimy protokolů, vytvořit bezpečné feature flagy pro hybridní testy, zkrátit životnost certifikátů, kde je to možné, odstranit napevno zadané algoritmické předpoklady a učinit kryptografickou politiku nasaditelnou skrze konfiguraci místo přes forky kódu.

## Závěr

Reset kvantové kryptografie není jeden technologický nákup. Je to kryptografický provozní model. NIST dal odvětví standardní základnu, NCSC zúžila praktický návod, protokolové orgány se stále hýbou a ujištění o QKD nabývá formálnější podoby. Bankovní instituce, které tento přechod vyhrají, nebudou ty, které oznámí největší pilot. Budou to instituce, které vědí, kde jejich kryptografie sídlí, vědí, která data je třeba chránit nejdříve, a umí měnit kryptografické primitivy bez přestavby banky.

## Často kladené otázky

**Je postkvantová kryptografie připravena k použití pro banky?**

Je připravena pro plánování, spolupráci s dodavateli, piloty a vybranou implementační práci. NIST říká, že tři standardy jsou připraveny k implementaci, zatímco NCSC varuje, že provozní použití by se mělo spoléhat na robustní implementace finálních standardů a stabilní protokoly ([NIST](https://www.nist.gov/pqc "NIST Post-Quantum Cryptography"), [NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "NCSC – další kroky v přípravě na PQC")).

**Odstraňuje QKD potřebu PQC?**

Ne. QKD může být užitečná pro specializované řízené linky, ale PQC je škálovatelná migrační cesta pro obecný software, internetové protokoly, API, certifikáty a podnikové systémy. QKD navíc závisí na rámcích ujištění a certifikace, než s ní lze zacházet jako s infrastrukturou bankovní úrovně ([ID Quantique / ETSI QKD 016](https://www.idquantique.com/etsi-releases-qkd-protection-profile/ "ETSI vydává ochranný profil QKD")).

**Co by mělo být migrováno jako první?**

Prioritu by měly mít systémy chránící dlouhožijící citlivá data. To zahrnuje šifrování archivů, vyšetřování plateb, dokumenty treasury a kapitálových trhů, identifikační záznamy privátního bankovnictví, strategické obchodní spisy, kořenové certifikační autority, podpisování firmwaru a mezibankovní kanály.

**Jaká je největší implementační past?**

Největší pastí je zacházet s PQC jako s pouhou výměnou algoritmu. Migrace se dotýká protokolů, certifikátů, HSM, dodavatelů, testování výkonu, reakce na incidenty, monitoringu a governance. Bez kryptografické agility instituce jednoduše znovu vytvoří stejný migrační problém pro příští změnu algoritmu.

## Reference

- NIST, (2025). [Postkvantová kryptografie ⧉](https://www.nist.gov/pqc "Postkvantová kryptografie").
- NCSC, (2024). [Další kroky v přípravě na postkvantovou kryptografii ⧉](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "Návod NCSC k PQC").
- NIST CSRC, (2026). [Projekt NIST Postkvantová kryptografie ⧉](https://csrc.nist.gov/presentations/2026/mpts2026-3b1 "Projekt NIST PQC").
- ID Quantique, (2024). [ETSI vydává první ochranný profil pro QKD na světě ⧉](https://www.idquantique.com/etsi-releases-qkd-protection-profile/ "ETSI QKD 016").
<!-- enrich-start -->
<aside class="author-card" aria-label="About the author"><img alt="Portrait of Sebastien Rousseau" src="https://cloudcdn.pro/stocks/images/sebastien-rousseau.png" width="64" height="64" loading="lazy" decoding="async" /><span class="author-card-body"><strong class="author-card-name"><a href="/about/index.html">Sebastien Rousseau</a></strong><span class="author-card-bio">Senior banking technologist writing on applied AI, ISO 20022 migration, post-quantum cryptography for financial services, and the structural transformation of wholesale payments.</span><span class="author-credentials">20+ years across HSBC Commercial &amp; Investment Bank, PayPal, Barclays, Shazam, AKQA, Virgin Group. <a href="/about/index.html">Full profile</a> &middot; <a href="https://www.linkedin.com/in/sebastienrousseau/" rel="external noopener">LinkedIn</a> &middot; <a href="https://github.com/sebastienrousseau" rel="external noopener">GitHub</a></span></span></aside>
<p class="post-reviewed">Last reviewed <time datetime="2026-05-18">2026-05-18</time>.</p>
<!-- enrich-end -->
