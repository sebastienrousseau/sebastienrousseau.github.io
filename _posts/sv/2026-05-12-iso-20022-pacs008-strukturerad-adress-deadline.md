---
title: "pacs.008-deadline för strukturerad adress i november 2026: en sexmånadersöversikt"
subtitle: "Från mitten av november 2026 avvisar SWIFT CBPR+ ostrukturerade postadresser i pacs.008 och relaterade meddelanden för gränsöverskridande betalningar. Med omkring 65 % av meddelandena fortfarande icke-kompatibla stängs åtgärdsfönstret snabbt."
description: "Från november 2026 kräver SWIFT CBPR+ strukturerade postadresser i meddelanden för gränsöverskridande betalningar. Ostrukturerade adressrader (enbart AdrLine) godtas inte längre för centrala partsfält i pacs.008. Som minimum krävs TwnNm och Ctry, med StrtNm och BldgNb eller PstBx rekommenderade. Med sex månader kvar innehåller 65 % av betalningsmeddelandena fortfarande ostrukturerade adresser och 44 % av bankerna ligger efter tidplanen."
date: "May 12, 2026"
language: "sv-SE"
locale: "sv_SE"
banner: "https://cloudcdn.pro/stocks/images/markus-winkler-IrRbSND5EUc-unsplash.webp"
banner_alt: "ISO 20022 pacs.008-diagram över strukturerad adress: fält i meddelanden för gränsöverskridande betalningar med TwnNm och Ctry markerade"
keywords: "ISO 20022, pacs.008, SWIFT CBPR+, strukturerad adress, november 2026, postadress, TwnNm, Ctry, StrtNm, BldgNb"
---

Från mitten av november 2026 avvisar SWIFT CBPR+ ostrukturerade postadresser i pacs.008 och relaterade meddelanden för gränsöverskridande betalningar. Med omkring 65 % av meddelandena fortfarande icke-kompatibla och 44 % av bankerna efter tidplanen stängs åtgärdsfönstret snabbare än vad de flesta beredskapsprogram är utformade för att hantera.

---

> **Viktiga slutsatser**
>
> - Från och med **november 2026** godtar SWIFT CBPR+ inte längre ostrukturerade postadresser i meddelanden för gränsöverskridande betalningar. Förändringen gäller **pacs.008** (kundkreditöverföring), **pacs.009** (kreditöverföring mellan finansinstitut), **pacs.004** (returer) och **pacs.003** (autogireringar), liksom de uppströms **pain.001**-flöden som matar dem.
> - Som minimum måste **ortnamn (TwnNm)** och **land (Ctry)** finnas i dedikerade strukturerade fält. **Gatunamn (StrtNm)** och antingen **husnummer (BldgNb)** eller **postbox (PstBx)** rekommenderas starkt. Adressrader i fritext (AdrLine) ensamma uppfyller inte längre kravet för centrala partsfält.
> - Förändringen förbättrar träffsäkerheten i sanktionsscreening, minskar andelen manuella korrigeringar och skyddar straight-through-bearbetningen, men bara för institut som har åtgärdat sina kunddata uppströms, inte enbart sina meddelandemotorer.
> - Branschens beredskap är ojämn. I mars 2026 bär omkring **65 % av CBPR+-meddelandena fortfarande ostrukturerade adresser**, **44 % av bankerna** ligger inte i fas med tidplanen och **32 % av kundernas adressuppgifter** är i genomsnitt fortfarande ostrukturerade.
> - Verktyg med öppen källkod, bland annat **[pacs008](https://pacs008.com/ "pacs008 — ISO 20022 pacs.008 Toolkit and API")**, ett Python-bibliotek och en FastAPI-tjänst för att generera, validera och orkestrera pacs.008-meddelandeflöden, kan korta ned åtgärdstidplaner genom att automatisera schemavalidering, kontroller av adresskvalitet och kontroll på CI-nivå innan meddelandena når SWIFT-nätverket.

---

## En deadline som alltid var på väg

Kravet på strukturerad adress i november 2026 är inte ett plötsligt regulatoriskt utspel. Det har funnits på färdplanen för SWIFT CBPR+ ända sedan den ursprungliga [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html)-migreringen tillkännagavs, och det följer på att MT/MX-samexistensen upphörde i november 2025. Det som har förändrats under 2026 är närheten. Med omkring sex månader kvar arbetar branschen nu inom det fönster där olösta datakvalitetsproblem blir operativ risk.

Siffrorna talar sitt tydliga språk. SWIFT:s egen samhällsuppdatering från mars 2026 noterar att [omkring 65 % av betalningsmeddelandena fortfarande innehåller ostrukturerade adresser ⧉](https://www.swift.com/news-events/news/iso-20022-milestone-november-2026-unstructured-addresses-be-removed "ISO 20022 milestone for November 2026: Unstructured addresses to be removed"), och att införandet är fortsatt ojämnt mellan geografier och institutionstyper. En [undersökning från RedCompass Labs i mars 2026 bland 308 seniora betalningsspecialister ⧉](https://financialit.net/news/banking/nearly-half-banks-are-behind-iso-20022 "Nearly Half of Banks Are Behind on ISO 20022") fann att 44 % av bankerna för närvarande inte ligger i fas med att klara deadline för strukturerad adress, trots att de i genomsnitt lagt 20 miljoner USD, och i de största instituten över 30 miljoner USD, på 2026 års beredskap, med i genomsnitt 13 ytterligare medarbetare avdelade till [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html)-programmen. Samma undersökning fann att 32 % av kundernas adressuppgifter i genomsnitt fortfarande är ostrukturerade, och att 60 % av bankerna rapporterar brister i kärnbanksystemen när de ska stödja strukturerade adressfält.

Det är med andra ord inte ett problem som kan lösas med ännu en månads arbete på meddelandemotorn. Det är ett datakvalitetsproblem som löper uppströms från meddelandelagret in i onboardingsystem, KYC-processer, företagskanaler och decennier av ackumulerade kundhuvuddata i fritext.

## Vad regeln faktiskt kräver

Under SWIFT CBPR+ Standards Release 2026 (SR2026) är kärnkravet enkelt i princip och oförlåtande i detaljerna. Från mitten av november 2026 måste [ortnamn och land anges i sina anvisade strukturerade fält ⧉](https://www.swift.com/news-events/news/iso-20022-milestone-november-2026-unstructured-addresses-be-removed "ISO 20022 milestone for November 2026: Unstructured addresses to be removed") för alla agenter och parter i CBPR+-betalningsmeddelanden, med mycket begränsade undantag (kontoutdrag och aviseringar i camt.052, camt.053, camt.054 samt ett fåtal administrativa meddelanden faller utanför det strikta kravet). För agenter är fortsatt användning av enbart BIC ett giltigt alternativ till namn-och-adress.

Två adressformat är tillåtna efter övergången:

- **Fullt strukturerat**: varje komponent i postadressen mappas till sitt dedikerade [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html)-element: StrtNm (gatunamn), BldgNb (husnummer) eller BldgNm (byggnadsnamn), PstCd (postnummer), TwnNm (ortnamn), CtrySubDvsn (landsindelning), Ctry (land, som en ISO 3166-1 alpha-2-kod). Det är det format som SWIFT uttryckligen anger som det mer önskvärda alternativet där det är möjligt.
- **Hybrid**: ortnamn och land fylls i sina strukturerade fält, medan resten av adressen får använda upp till två ostrukturerade AdrLine-element. Viktigt: [strukturerade element får inte upprepas inuti de ostrukturerade raderna ⧉](https://www.statestreet.com/web/insights/articles/documents/state-street-client-guide-to-iso-20022-2025.pdf "State Street Client Guide to ISO 20022 2025"); för en given komponent är adressen antingen det ena eller det andra.

Helt ostrukturerade adresser, där hela adressen ligger i AdrLine-element utan TwnNm eller Ctry, godtas inte för något av de berörda partsfälten. European Payments Council har anpassat sitt SEPA-regelverk till samma övergång, så från och med [den 15 november 2026 är det ostrukturerade formatet förbjudet även i SCT, SDD och SCT Inst ⧉](https://clearingpost.com/insights/iso-20022-structured-address-deadline-november-2026/ "The November 2026 Structured Address Deadline: What Every PSP Needs to Do Now"). Samordningen är avsiktlig: SWIFT och EPC har konstruerat en enda övergångshelg för hela branschen.

För att undvika tvivel listar [pacs008-dokumentationen de berörda meddelandena direkt ⧉](https://pacs008.com/structured-address/ "November 2026 structured-address deadline — pacs008"): pacs.008 (betalare och betalningsmottagare i kundkreditöverföringar), pacs.009 (institutsadresser i kreditöverföringar mellan finansinstitut och täckningsbetalningar), pacs.004 (partsadresser i returer) och pacs.003 (autogireringar). Kravet löper också uppströms: företags pain.001-filer med ostrukturerade adresser blockerar generering av regelenlig pacs.008 hos den mottagande banken.

## Varför branschen har gjort detta till en prioritet

Argumentet för strukturerade adresser är inte estetiskt. Det är operativt, och det visar sig på tre ställen.

**Sanktionsscreening.** Den enskilt största praktiska nyttan är att strukturerade adresser låter screeningsystem skilja partsnamn från platsdata. Adressblock i fritext orsakar regelbundet falska positiva träffar när ett ortnamn råkar sammanfalla med ett namntoken för en sanktionerad person, eller när ett land inbäddat i fritext missas helt. Strukturerade fält låter screeningmotorer tillämpa landsspecifika riskregler deterministiskt, och de gör det möjligt att matcha mot sanktionslistor utifrån landskoden i stället för att gissa utifrån en tolkad sträng. CGI UK:s analys, publicerad i mars 2026, understryker detta uttryckligen: [strukturerade adressdata blir centrala för operativ motståndskraft, inte enbart en efterlevnadsskyldighet ⧉](https://www.cgi.com/uk/en-gb/blog/banking-and-financial-markets/2026-defining-year-iso-20022-and-structured-data-enforcement "2026: A defining year for ISO 20022 and structured data enforcement").

**Andel manuella korrigeringar.** Gränsöverskridande betalningar bär i dag en betydande operativ kostnad i form av manuella utredningar, undantagshantering och korrigeringsköer, till stor del driven av adresser som screening- eller dirigeringssystem inte kan tolka med säkerhet. Banker som redan gått över till strukturerade adresser rapporterar påtagliga minskningar av undantag i straight-through-bearbetningen, särskilt i flöden mitt i korridoren där mellanliggande agenter tidigare måste tolka fritextdata som de inte själva skapat.

**Kontroll på nätverksnivå.** SR2026 skärper valideringen i SWIFT:s nätverkslager. Vissa av de nya kontrollerna arbetar inledningsvis i icke-blockerande läge, genom att flagga datakvalitetsproblem utan att stoppa betalningar, men riktningen är tydlig, och efter övergången [avvisas icke-regelenliga meddelanden rakt av ⧉](https://www.redcompasslabs.com/insights/iso-20022-is-arriving-all-at-once-for-us-banks/ "ISO 20022 is arriving all at once for US banks"). Flera amerikanska betalningsinfrastrukturer (Fedwire, CHIPS) och SWIFT CBPR+ konvergerar mot i allt väsentligt samma tidplan, vilket tar bort möjligheten till stegvis övergång som vissa institut förutsatt i tidigare planer.

## Fältnivån: vad som ändras i meddelandet

pacs.008-meddelandet har haft stöd för strukturerad adress sedan de tidiga CBPR+-användningsanvisningarna började gälla i mars 2023. Det som ändras i november 2026 är inte schemat, utan valideringen. Fram till nu har banker fått fylla AdrLine-element med fritext och skicka detta genom nätverket. Från och med deadline måste innehållet i partsblocken uppfylla minimikraven på strukturerade fält.

### Obligatoriskt, rekommenderat och avvecklat

| Element | XPath (under `PstlAdr`) | Status efter nov 2026 | Anmärkningar |
|---|---|---|---|
| Ortnamn | `<TwnNm>` | **Obligatoriskt** | Minst ett strukturerat ortnamn per berörd part |
| Land | `<Ctry>` | **Obligatoriskt** | ISO 3166-1 alpha-2-kod |
| Gatunamn | `<StrtNm>` | Rekommenderas starkt | Krävs för fullt strukturerat format |
| Husnummer | `<BldgNb>` | Rekommenderas | Antingen BldgNb eller PstBx, inte båda |
| Postbox | `<PstBx>` | Rekommenderas | Alternativ till BldgNb |
| Postnummer | `<PstCd>` | Rekommenderas | Krävs av vissa lokala system |
| Landsindelning | `<CtrySubDvsn>` | Valfritt | Delstat, region, provins |
| Adressrad (fritext) | `<AdrLine>` | **Begränsat** | Max 2 rader vid hybrid; aldrig tillsammans med samma komponent i strukturerade fält |
| Adresstyp | `<AdrTp>` | Valfritt | Användning av `ADDR` rekommenderas för postadresser |

*Källa: sammanställning av SWIFT CBPR+-användningsanvisningar för SR2026 och [pacs008.com:s dokumentation om strukturerad adress ⧉](https://pacs008.com/structured-address/ "November 2026 structured-address deadline — pacs008").*

Den praktiska följden är att varje institut som fortfarande förlitar sig på enbart AdrLine, oavsett om det är i den egna meddelandegenereringen, i pain.001-filer mottagna från företagskunder eller i huvuddataposter som används för att berika betalningar under flödet, måste migrera dessa data till strukturerade fält före övergången. SWIFT:s översättningstjänst under flödet kan hjälpa till i transit, men [den beläggs med tilläggsavgifter från januari 2026 ⧉](https://www.pcbb.com/products/international-banking/international-payments/iso20022-faq "ISO 20022 FAQ — PCBB") och kan inte tillförlitligt tolka alla adressformat. SWIFT har också släppt [en AI-modell för adresstrukturering med öppen källkod ⧉](https://www.swift.com/standards/iso-20022/iso-20022-faqs/swift-ai-address-structuring-model "ISO 20022: The Swift AI address structuring model") tränad på data från över 200 länder för att härleda ort och land ur ostrukturerade äldre data med konfidenspoäng, men den är uttryckligen ett åtgärdshjälpmedel, inte en långsiktig ersättning för rena data uppströms.

## Hur pacs008.com bidrar till att korta tidplanen

För institut som snabbt behöver industrialisera sina pipelines för adresskvalitet och meddelandevalidering tillhandahåller [pacs008 ⧉](https://pacs008.com/ "pacs008 — ISO 20022 pacs.008 Toolkit and API") en MIT-licensierad verktygslåda med öppen källkod och en FastAPI-tjänst utformad specifikt för arbetsflödet för kundkreditöverföring mellan finansinstitut. Den adresserar de tre lager där åtgärdsprogram oftast kör fast: datavalidering, XML-generering och kontroll i pipeline.

Verktygslådans funktioner för strukturerad adress är anpassade till SR2026-kraven:

- **Validering före generering** av strukturerade och hybrida postadressfält, så att icke-regelenliga data fångas innan någon XML produceras eller skickas.
- **Flaggning av ostrukturerade adressdata** som skulle underkännas efter deadline i november 2026, med en tydlig åtskillnad mellan fall som är godtagbara i hybridform och fall som är helt ostrukturerade.
- **Stöd för dubbla format** för både hybridformat före deadline och fullt strukturerade layouter efter deadline, vilket låter institut migrera stegvis utan att bryta interoperabiliteten med motparter som ännu inte slutfört sina egna övergångar.
- **Integration i CI-pipeline** så att kontroller av adresskvalitet blir en del av byggprocessen, inte en eftertanke i slutet av flödet. Det är det praktiska svaret på [CGI:s observation att datastyrning måste vara en grundläggande designprincip ⧉](https://www.cgi.com/uk/en-gb/blog/banking-and-financial-markets/2026-defining-year-iso-20022-and-structured-data-enforcement "2026: A defining year for ISO 20022 and structured data enforcement") snarare än ett efterlevnadslager ovanpå.

Utöver adresser täcker verktygslådan den bredare valideringsytan som SR2026-utgåvan skärper: JSON Schema-validering mot 20 meddelandespecifika scheman, kontroll av IBAN-format och checksumma i 75 länder, XSD-validering av genererad XML mot de officiella [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html)-schemana och versionsmedveten generering över samtliga 13 stödda pacs.008-revisioner (pacs.008.001.01 till pacs.008.001.13). För drift- och efterlevnadsteam ingår även XXE-skydd via defusedxml, strikt skydd mot path traversal och PII-maskering i strukturerade JSON-loggar för att uppfylla kraven i GDPR och PCI DSS. Det är den typ av kontroller som är icke förhandlingsbara i produktionssatta betalningsflöden men ofta läggs till sent i leverantörsledda migreringar.

Biblioteket finns tillgängligt [på PyPI ⧉](https://pypi.org/project/pacs008/ "pacs008 on PyPI") som paketet `pip install pacs008` och på [GitHub ⧉](https://github.com/sebastienrousseau/pacs008 "pacs008 on GitHub") med full insyn i källkoden. För institut som utvärderar sina alternativ spelar detta roll: verktyg med öppen källkod låter interna team granska valideringslogiken, integrera den i befintliga Python- eller FastAPI-miljöer utan licensförhandlingar och bidra med rättningar när deras egna gränsfall dyker upp.

Det är värt att vara precis om omfattningen. pacs008 är en verktygslåda på meddelandelagret; den ersätter inte en betalningsmotor, ett screeningsystem eller den åtgärd av kundhuvuddata som ett institut fortfarande måste göra vid källan. Vad den gör är att ta det åtgärdsarbetet och göra det verkställbart, genom att förvandla efterlevnad av strukturerad adress från en manuell granskning i slutet av en lång pipeline till en automatiserad grind vid genereringstillfället. För program med ont om tid är den grinden skillnaden mellan en ren övergång och en våg av avvisningar efter övergången.

## Verktygsekosystemet

pacs008 ingår i ett bredare ekosystem av verktyg för [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html)-meddelanden, och valet av angreppssätt beror på institutets teknikstack, skala och migreringsfilosofi. Utbudet av öppen källkod och kommersiella lösningar omfattar [pyiso20022 ⧉](https://github.com/phoughton/pyiso20022 "pyiso20022 — an ISO 20022 message generator and parser") (ett brett Python-bibliotek för flera meddelandekategorier med validering i beta), det relaterade biblioteket [pain001 ⧉](https://pain001.com/ "Pain001 — Automate ISO 20022-compliant payment file creation") för betalningsinitiering uppströms, [Prowide ISO 20022 ⧉](https://www.prowidesoftware.com/development-tools/iso20022 "Prowide ISO 20022 — open source MX message parser for Java") (ett omfattande Java-bibliotek under Apache 2.0 med ett kommersiellt lager för CBPR+-validering och översättningar) och ett antal kommersiella plattformar, bland andra Mambu, Kyriba och PaymentComponents, som bakar in [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html)-funktionalitet i bredare erbjudanden för treasury eller betalningsplattformar.

Avvägningen är välbekant. Kommersiella plattformar minskar den interna ingenjörsbördan men binder institutet till en leverantörs färdplan som kanske inte matchar dess egen. Omfattande bibliotek för flera kategorier täcker en bredare yta men kräver mer integrationsarbete för en enskild meddelandetyp. Fokuserade bibliotek med öppen källkod, pacs008 för kundkreditöverföring mellan finansinstitut och [pain001](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) för betalningsinitiering, minimerar integrationstiden för institut som snabbt behöver åtgärda specifika flaskhalsar, och de låter institutet behålla kontrollen över sina egna valideringsregler. För just problemet med strukturerad adress har ett fokuserat angreppssätt fördelen att de regler som tillämpas är avgränsade, väldefinierade och osannolika att ändras före övergången.

## Vad detta innebär per sektor

Deadline i november 2026 påverkar inte alla institut lika. Rätt respons beror på volymen gränsöverskridande trafik, mognaden i den befintliga datamiljön och den roll institutet spelar i betalningskedjan.

### Stora korrespondent- och gränsöverskridande banker

För tier-one-banker som hanterar betydande CBPR+-trafik är kravet på strukturerad adress ett arbetsflöde inom ett mycket större SR2026-beredskapsprogram som också omfattar undantag och utredningar, härdning av BAH och (i USA) den samtidiga migreringen av Fedwire och CHIPS. Data från RedCompass Labs tyder på att de flesta av dessa institut lägger 20–30 miljoner USD på 2026 års beredskap, med leveransteam på 10–20 specialister. Risken för denna grupp är inte teknisk förmåga, utan leveranskapacitet. När flera parallella arbetsflöden konkurrerar om samma releasefönster kan åtgärdandet av adresskvalitet i tysthet halka efter mer synliga arbetsflöden tills det blir ett problem under övergångsveckan. Den praktiska motåtgärden är att flytta adressvalideringen tidigare i pipelinen, så att fel visar sig i utvecklings- och testmiljöer månader innan de skulle ha nått produktion.

### Medelstora banker och betalningsinstitut

För medelstora banker och EMI/PI-institut är kravet på strukturerad adress ofta den mest väsentliga 2026-skyldighet de möter, eftersom de inte bär samma omgivande arbetsflödesbörda som tier-one-bankerna. Utmaningen här är oftast datakvaliteten uppströms. Kundonboardingprocesser som fångat adresser som fritext under decennier ger huvuddatamiljöer som inte är enkelt tolkbara. Automatiserad åtgärd, med hjälp av SWIFT:s adresstruktureringsmodell med öppen källkod, kommersiella tjänster för adressrensning eller en kombination, kan hantera en betydande andel av posterna, men en kvarvarande lång svans av komplexa internationella adresser kräver manuell granskning. Ju tidigare detta arbete börjar, desto mindre blir den svansen.

### Företag och betaltjänstleverantörer

Företag som initierar betalningar via pain.001 ligger uppströms om bankens pacs.008-generering men är inte undantagna från kravet på strukturerad adress. Banker fyller inte i mottagaradresser retroaktivt åt företagskunder; de strukturerade uppgifterna måste komma från företagets egna system. För företagens treasury-funktioner innebär detta att säkerställa att ERP- och treasury-system fångar mottagaradresser i strukturerad form, att uppgifter om firmatecknare och slutlig betalare är strukturerade på samma sätt och att mallar för betalningsinitiering inte i tysthet tappar fält vid filgenerering. Förhandsvalidering av pain.001-filer, med antingen företagets egna verktyg eller tjänster som banken tillhandahåller, blir den praktiska kontrollpunkten.

### Leverantörer, fintechbolag och systemintegratörer

För leverantörer som bygger ovanpå betalningsinfrastruktur är deadline en tvingande faktor för [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html)-funktionalitet som kan ha skjutits till senare faser. Fintechbolag som dirigerar eller initierar gränsöverskridande betalningar via bankpartner behöver lyfta fram insamling av strukturerad adress i sina egna gränssnitt och API:er, eller acceptera att regelenliga pain.001-filer inte kan produceras ur deras data. Möjligheten, för leverantörer som kan agera snabbt, är att ta över åtgärdsbördan åt företagskunderna och förvandla ett efterlevnadsproblem till en tjänst.

## Slutsats

Deadline för strukturerad adress i november 2026 är i en mening en avgränsad förändring: två obligatoriska fält, ett par rekommenderade och avvecklingen av ett fritextalternativ som aldrig borde ha använts för sanktionsrelevanta data över huvud taget. I en annan mening är det den operativt mest betydelsefulla [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html)-milstolpen sedan den ursprungliga CBPR+-migreringen, eftersom den tvingar in strukturerade data inte bara i meddelandelagret utan i de uppströms system som matar det.

Beredskapsbilden på branschnivå, sex månader ut, är inte uppmuntrande. Två tredjedelar av CBPR+-meddelandena bär fortfarande ostrukturerade adresser. Nästan hälften av bankerna ligger inte i fas. Nästan en tredjedel av kundernas adressuppgifter är fortfarande otolkbara. Finansieringen finns på plats, undersökningarna visar genomgående investeringar på åtta- och niosiffriga belopp, men arbetet finns inte, och datakvalitetsdimensionen av problemet kan inte lösas enbart med utgifter under de sista månaderna.

Det som hjälper nu är automatisering vid valideringstillfället: att lägga in reglerna i pipelines som fångar problem innan de når nätverket, snarare än efteråt. För institut som driver Python- eller FastAPI-miljöer ger verktyg med öppen källkod som [pacs008 ⧉](https://pacs008.com/ "pacs008 — ISO 20022 pacs.008 Toolkit and API") ett praktiskt sätt att göra den omställningen utan en leverantörsupphandling. För alla, oavsett teknikstack, är den strategiska poängen densamma: de institut som industrialiserar förändringen nu kommer att stå betydligt starkare än de som förlitar sig på efterlevnad i sista stund, för att låna formuleringen från RedCompass Labs forskning som har ramat in mycket av 2026 års samtal.

Övergångshelgen i november stänger ett kapitel. De institut som kommer dit med rena data, automatiserad validering och en fungerande förståelse för vad strukturerade adresser faktiskt gör för sanktionsscreening kommer att tillbringa den helgen med att övervaka trafiken. De som kommer dit utan detta kommer att tillbringa den i telefon.

## Vanliga frågor

**Vad ändras exakt vid deadline i november 2026?**

Från mitten av november 2026 avvisar SWIFT CBPR+ meddelandena pacs.008, pacs.009, pacs.004 och pacs.003 vars partsfält innehåller enbart ostrukturerade postadresser. Minimikravet på struktur är ortnamnet i elementet TwnNm och landet i elementet Ctry (med ISO 3166-1 alpha-2-koden). Hybridadresser är fortfarande tillåtna, med ort och land i strukturerade fält plus upp till två AdrLine-element i fritext för de återstående komponenterna, men samma komponent kan inte förekomma i både strukturerade och ostrukturerade fält. Fullt strukturerade adresser är det format som föredras. European Payments Council har anpassat SEPA-systemen (SCT, SDD, SCT Inst) till samma övergångsdatum.

**Vilka meddelanden och vilka partsfält berörs?**

För pacs.008 gäller kravet betalarens och betalningsmottagarens postadresser. För pacs.009 gäller det institutsadresser i kreditöverföringar mellan finansinstitut och täckningsbetalningar. För pacs.004 gäller det partsadresser i betalningsreturer. För pacs.003 gäller det borgenärs- och gäldenärsadresser i kundautogireringar. Kontoutdrags- och aviseringsmeddelanden (camt.052, camt.053, camt.054) samt vissa administrativa meddelanden faller utanför det strikta kravet. Uppströms pain.001-meddelanden från företagskunder styrs inte direkt av CBPR+, men ostrukturerade adresser i pain.001-filer blockerar regelenlig pacs.008-generering nedströms och omfattas därför i praktiken.

**Vad är skillnaden mellan strukturerad, hybrid och ostrukturerad adress?**

En fullt strukturerad adress mappar varje komponent till sitt dedikerade [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html)-element: StrtNm, BldgNb eller PstBx, PstCd, TwnNm, CtrySubDvsn, Ctry. En hybridadress har ortnamn och land i strukturerade fält, med resten av adressen i upp till två AdrLine-element i fritext; samma komponent får inte förekomma i båda. En ostrukturerad adress har hela postadressen i AdrLine-element utan strukturerat TwnNm eller Ctry. Det är det format som avvecklas i november 2026 för de berörda partsfälten.

**Hur hjälper pacs008.com till med denna övergång?**

Biblioteket [pacs008 ⧉](https://pacs008.com/ "pacs008 — ISO 20022 pacs.008 Toolkit and API") validerar strukturerade och hybrida postadressfält före XML-generering, flaggar ostrukturerade data som skulle underkännas efter deadline, stöder både hybridformat före deadline och fullt strukturerade format efter deadline och integreras i CI-pipelines och arbetsflöden för batchvalidering. Det genererar XML för samtliga 13 stödda pacs.008-versioner, validerar mot de officiella [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html)-XSD-schemana och exponerar en FastAPI-tjänst för automatiserad orkestrering. Det är öppen källkod under en MIT-liknande licens, tillgängligt på PyPI och utformat specifikt för arbetsflöden för kundkreditöverföring mellan finansinstitut, så valideringsreglerna är kalibrerade mot SR2026:s CBPR+-användningsanvisningar snarare än abstraherade över många meddelandetyper.

**Vad händer om mitt institut inte är redo i november 2026?**

Meddelanden med ostrukturerade adresser i de berörda partsfälten avvisas på nätverksnivå efter övergången. I praktiken innebär detta betalningsfel, ökade undantagsvolymer, vågor av manuell korrigering och sannolik kundpåverkan. SWIFT:s översättningstjänst under flödet är tillgänglig för vissa övergångsfall men beläggs med tilläggsavgifter från januari 2026 och kan inte tillförlitligt tolka alla adressformat. SWIFT har också släppt en AI-modell för adresstrukturering med öppen källkod som härleder ort och land ur äldre ostrukturerade data, men den är utformad för åtgärd och förbehandling, inte som en permanent ersättning för rena data uppströms. Institut som når deadline utan en åtgärdad miljö för kundhuvuddata och en automatiserad valideringspipeline bör räkna med en svår övergångsvecka och ett påtagligt operativt merarbete under de månader som följer.

## Referenser

- Sebastien Rousseau, (2023). [Automating ISO 20022-Compliant Payment File Creation with Pain001](https://sebastienrousseau.com/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html "Automating ISO 20022-Compliant Payment File Creation with Pain001").
- pacs008, (2026). [November 2026 structured-address deadline ⧉](https://pacs008.com/structured-address/ "November 2026 structured-address deadline — pacs008"). pacs008.com.
- pacs008, (2026). [pacs008 — ISO 20022 pacs.008 Toolkit and API ⧉](https://pacs008.com/ "pacs008 — ISO 20022 pacs.008 Toolkit and API"). pacs008.com.
- SWIFT, (2026). [ISO 20022 milestone for November 2026: Unstructured addresses to be removed ⧉](https://www.swift.com/news-events/news/iso-20022-milestone-november-2026-unstructured-addresses-be-removed "ISO 20022 milestone for November 2026: Unstructured addresses to be removed"). SWIFT.
- SWIFT, (2026). [ISO 20022 for Financial Institutions ⧉](https://www.swift.com/standards/iso-20022/iso-20022-financial-institutions-focus-payments-instructions "ISO 20022 for Financial Institutions"). SWIFT.
- SWIFT, (2026). [The Swift AI address structuring model ⧉](https://www.swift.com/standards/iso-20022/iso-20022-faqs/swift-ai-address-structuring-model "ISO 20022: The Swift AI address structuring model"). SWIFT.
- RedCompass Labs, (2026). [Nearly Half of Banks Are Behind on ISO 20022 ⧉](https://financialit.net/news/banking/nearly-half-banks-are-behind-iso-20022 "Nearly Half of Banks Are Behind on ISO 20022"). Financial IT.
- RedCompass Labs, (2026). [ISO 20022 is arriving all at once for US banks ⧉](https://www.redcompasslabs.com/insights/iso-20022-is-arriving-all-at-once-for-us-banks/ "ISO 20022 is arriving all at once for US banks"). RedCompass Labs.
- ClearingPost, (2026). [The November 2026 Structured Address Deadline: What Every PSP Needs to Do Now ⧉](https://clearingpost.com/insights/iso-20022-structured-address-deadline-november-2026/ "The November 2026 Structured Address Deadline"). ClearingPost.
- CGI UK, (2026). [2026: A defining year for ISO 20022 and structured data enforcement ⧉](https://www.cgi.com/uk/en-gb/blog/banking-and-financial-markets/2026-defining-year-iso-20022-and-structured-data-enforcement "2026: A defining year for ISO 20022 and structured data enforcement"). CGI UK.
- J.P. Morgan, (2026). [ISO 20022 Migration: Guidance, Messaging & More ⧉](https://www.jpmorgan.com/insights/payments/fx-cross-border/iso-20022-migration "ISO 20022 Migration: Guidance, Messaging & More"). J.P. Morgan.
- ING, (2026). [FAQ Swift ISO 20022 ⧉](https://www.ingwb.com/en/service/payments-and-collections/swift-iso20022/faq-swift-iso-20022 "FAQ Swift ISO 20022 — ING"). ING Wholesale Banking.
- Mambu, (2026). [CBPR+ is live: what ISO 20022 means in practice ⧉](https://mambu.com/en/insights/articles/cbpr-is-live-what-iso-20022-means-in-practice "CBPR+ is live: what ISO 20022 means in practice"). Mambu.
- Kyriba, (2026). [ISO 20022 migration: what every treasury team needs to know about what's next ⧉](https://www.kyriba.com/blog/iso-20022-corporate-treasury-2026/ "ISO 20022 migration: what every treasury team needs to know about what's next"). Kyriba.
- Standard Chartered, (2025). [ISO 20022 – Standard Chartered Address Guidelines (H2H and API) ⧉](https://www.sc.com/en/uploads/sites/66/content/docs/sc-cib-tb-ISO-20022%E2%80%93CBPR-Address-guidelines-H2H-and-API-sept-2025.pdf "Standard Chartered ISO 20022 Address Guidelines"). Standard Chartered.
- State Street, (2025). [Client Guide to ISO 20022 ⧉](https://www.statestreet.com/web/insights/articles/documents/state-street-client-guide-to-iso-20022-2025.pdf "State Street Client Guide to ISO 20022 2025"). State Street.
- ISO 20022, (2026). [Message Definitions Catalogue ⧉](https://www.iso20022.org/iso-20022-message-definitions "ISO 20022 Message Definitions"). ISO 20022.
