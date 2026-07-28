---
title: "Att säkra huvudboken: en vägledning på styrelsenivå för postkvantmigration inom företagsfinans"
subtitle: "Kvantrisken har gått från forskningskuriosa till aktivt regulatoriskt krav. Med G7-färdplanen publicerad i januari 2026 och BIS Project Leap som bevisat genomförbarhet i skarpa betalningssystem är frågan på styrelsenivå inte längre om man ska migrera, utan om migrationen hinner slutföras innan hållbarhetstiden för dagens data löper ut."
description: "Kvantrisken har gått från forskningskuriosa till aktivt regulatoriskt krav. Med G7-färdplanen publicerad i januari 2026, tidplanerna för EU, Storbritannien och Australien förtydligade, och BIS Project Leap som bevisat genomförbarhet i skarpa betalningssystem, är frågan för styrelser inte längre om man ska migrera, utan om migrationen hinner slutföras innan den kryptografiska hållbarhetstiden för dagens data löper ut."
date: "May 14, 2026"
language: "sv-SE"
locale: "sv_SE"
banner: "https://cloudcdn.pro/stocks/images/getty-images-LaU3HadwEeE-unsplash.webp"
banner_alt: "Diagram över färdplan för postkvantkryptografisk migration: infrastruktur för företagsbank som går från RSA till ML-KEM och ML-DSA"
keywords: "postkvantkryptografi, PQC-migration, företagsbank, finansiella tjänster, G7 CEG-färdplan, BIS Project Leap, ML-KEM, ML-DSA, FIPS 203, FIPS 204"
---

Kvantrisken har gått från forskningskuriosa till aktivt regulatoriskt krav. Med G7-färdplanen publicerad i januari 2026, tidplanerna för EU, Storbritannien och Australien förtydligade, och BIS Project Leap som har bevisat genomförbarhet i skarpa betalningssystem, är frågan för styrelser inte längre om man ska migrera. Frågan är om migrationen hinner slutföras innan den kryptografiska hållbarhetstiden för dagens data löper ut.

---

> **Viktiga slutsatser**
>
> - **2026 är året då regelverket skärptes.** G7 Cyber Expert Groups januarifärdplan, EU:s NIS-samarbetsgrupps samordnade tidplan och brittiska NCSC:s trefasplan har flyttat samtalet från medvetenhet till genomförande. Australian Signals Directorate har gått ännu längre och satt ett hårt slutdatum till 2030 för klassisk asymmetrisk kryptografi.
> - **Exponeringen är asymmetrisk.** RSA, ECC och Diffie–Hellman är det omedelbara problemet, de asymmetriska algoritmer som ligger till grund för SWIFT-handskakningar, TLS, PKI, kodsignering och autentisering i clearingnät. Symmetrisk kryptering (AES-256) förblir stabil om nyckellängderna bibehålls. Fokus på styrelsenivå måste ligga på den asymmetriska ytan.
> - **Harvest-now-decrypt-later är inget framtidsscenario.** Motståndare avlyssnar och lagrar redan i dag krypterade finansiella loggar, avvecklingsuppgifter, M&A-material och gränsöverskridande betalningsdata, med den uttalade avsikten att dekryptera dem så snart en kryptografiskt relevant kvantdator (CRQC) finns. För data med ett konfidentialitetskrav på 10 till 20 år är den risken redan realiserad.
> - **Branschen har nu en fungerande referenspunkt.** [BIS Project Leap Phase 2 ⧉](https://www.bis.org/publ/othp107.htm "Project Leap phase 2: quantum-proofing payment systems"), publicerad i december 2025, ersatte framgångsrikt traditionella digitala signaturer med postkvantkryptografi i skarpa likviditetsöverföringar över TARGET2, och synliggjorde de specifika tekniska kostnaderna (verifieringslatens, paketstorlek) som varje migrationsprogram kommer att möta.
> - **NIST-sviten är det globala ankaret.** [FIPS 203 (ML-KEM) ⧉](https://csrc.nist.gov/pubs/fips/203/final "FIPS 203, Module-Lattice-Based Key-Encapsulation Mechanism Standard") och FIPS 204 (ML-DSA) refereras av alla större jurisdiktioner, även där nationella ståndpunkter skiljer sig åt om parameteruppsättningar och hybridkrav. Styrelser bör betrakta ML-KEM-768/ML-DSA-65 som golvet och ML-KEM-1024/ML-DSA-87 som den konservativa baslinjen för långlivade data.
> - **Hybrid är den enda trovärdiga vägen.** Ingen större myndighet rekommenderar en rak övergång. Att köra klassiska och kvantresistenta algoritmer parallellt är det utrullningsmönster som NCSC, ANSSI och BSI ställer sig bakom och som bevisats i Project Leap. Det är tyngre än båda alternativen, men det är det enda som hanterar både dagens kompatibilitet och morgondagens hot.

---

## Året då regelverket skärptes

Under större delen av det senaste decenniet levde postkvantkryptografin i ett bekvämt hörn av den långsiktiga färdplanen. Kvantdatorer var imponerande men avlägsna, den kryptografiska matematik som ligger till grund för RSA och elliptiska kurvor behandlades som ett stabilt underlag, och samtalet om migration var till stor del begränsat till specialiserade arbetsgrupper. Den positionen är inte längre hållbar.

I januari 2026 publicerade [G7 Cyber Expert Group sitt mest betydelsefulla uttalande hittills ⧉](https://www.gov.uk/government/publications/advancing-a-coordinated-roadmap-for-the-transition-to-post-quantum-cryptography-in-the-financial-sector/g7-cyber-expert-group-statement-on-advancing-a-coordinated-roadmap-for-the-transition-to-post-quantum-cryptography-in-the-financial-sector-january-20 "G7 CEG Statement on Advancing a Coordinated Roadmap for the Transition to Post-Quantum Cryptography in the Financial Sector"), med amerikanska finansdepartementet och Bank of England som medordförande. Dokumentet är ingen reglering, men det väger tyngre än vanlig vägledning: det speglar den gemensamma uppfattningen hos finansdepartement, centralbanker och tillsynsmyndigheter i G7-jurisdiktionerna att kryptografisk övergång nu är en fråga om systemisk riskhantering. Färdplanen lägger sin planeringshorisont kring mitten av 2030-talet, med kritiska finansiella system uppmanade att migrera tidigare, ett språkbruk som i centralbankernas försiktiga idiom signalerar förväntan snarare än förslag.

Två månader tidigare publicerade BIS Innovation Hub och Eurosystemet resultaten av [Project Leap Phase 2 ⧉](https://www.bis.org/publ/othp107.htm "Project Leap phase 2: quantum-proofing payment systems"), ett tekniskt experiment som ersatte traditionella digitala signaturer med postkvantkryptografi i skarpa likviditetsöverföringar mellan Bank of Italy, Banque de France, Deutsche Bundesbank, Nexi-Colt och Swift. Huvudresultatet var en framgång: kvantresistenta signerade överföringar gick hela vägen genom ett operativt betalningssystem. Detaljerna under rubriken är mer lärorika, och de granskas längre fram i den här artikeln.

Kombinationen av dessa två händelser, ett samordnat G7-policyramverk och en fungerande bevispunkt i ett verkligt betalningssystem, har gett det som den tekniska gemenskapen har väntat ett decennium på: ett definitivt svar på frågan ”är detta verkligt?”. Svaret, i maj 2026, är ja. Den återstående frågan gäller takten.

## Tre hotvektorer som bör bekymra styrelsen

Innan vi diskuterar migrationens mekanik är det värt att vara precis om vad som specifikt står på spel. Kvantrisken inom företagsbank är inte enhetlig över hela det kryptografiska beståndet, och styrelsens uppmärksamhet riktas bäst mot de tre vektorer där exponeringen är som mest akut.

### 1. Harvest now, decrypt later (HNDL)

Den mest omedelbara oron ligger inte i framtiden. Den är närvarande. Statliga och avancerade kriminella motståndare avlyssnar och lagrar systematiskt krypterad finansiell trafik, betalningsöverföringar, SWIFT-meddelandeflöden, M&A-kommunikation, gränsöverskridande avvecklingsloggar, swapavtal och KYC-filer, utan någon nuvarande förmåga att läsa dem. Deras mål är enkelt: lagra nu, dekryptera senare, så snart en CRQC finns. Som [Bank for International Settlements uttryckligen har noterat ⧉](https://www.bis.org/about/bisih/topics/cyber_security/leap.htm "Project Leap: quantum-proofing the financial system") pågår denna insamling redan.

För styrelser är innebörden obekväm men konkret: alla känsliga data som i dag överförs under klassisk asymmetrisk kryptering, och vars konfidentialitetskrav sträcker sig bortom ankomsten av en CRQC, måste redan betraktas som exponerade. Det finns ingen incidentanmälan när HNDL inträffar. Det finns inget larm i SIEM-systemet. Krypteringen håller, för stunden, men data har redan lämnat perimetern.

### 2. Långsiktig känslighetsrisk

Data inom företagsbank har ovanligt lång institutionell hållbarhet. Strategisk M&A-dokumentation kan förbli marknadskänslig i ett decennium. Kommunikation om affärshemligheter och värderingar av immateriella tillgångar kan förbli konfidentiella i femton till tjugo år. Gränsöverskridande avvecklingsloggar, exponeringar mot centrala motparter och kreditbedömningar av motparter behåller kommersiell känslighet långt bortom sin omedelbara transaktionslivslängd.

[Mosca-ekvationen ⧉](https://www.cryptomathic.com/a-bankers-guide-to-quantum-safe-cryptography-part-3-roadmap-to-pqc-migration-for-financial-institutions-cryptomathic "A Banker's Guide to Quantum Safe Cryptography — Part 3"), ursprungligen formulerad av Michele Mosca och nu inbäddad i varje seriöst migrationsramverk, formaliserar problemet. Om **S** är datas hållbarhet, **M** är den tid som krävs för att migrera de system som skyddar dem, och **Q** är tiden till dess att en CRQC finns tillgänglig, gäller:

```
Om S + M > Q är data redan exponerade.
```

För data med en konfidentialitetshorisont på tjugo år och ett migrationsprogram som realistiskt kräver fem till sju år att slutföra, ligger det implicita Q-värde som styrelsen satsar på minst 25 år bort. En växande mängd expertbedömningar, [Forresters APAC-prognoser för 2026 ⧉](https://www.forrester.com/press-newsroom/forrester-apac-2026-predictions/ "Forrester's 2026 APAC Predictions"), Global Risk Institutes årliga undersökningar, och ett arkitekturdokument från februari 2026 som föreslår en CRQC vid ungefär 100 000 fysiska qubitar med QLDPC-koder, tyder på att den satsningen är osäker.

### 3. Sårbarheten hos centrala handskakningar

Den tredje vektorn är den arkitektoniskt mest betydelsefulla. Symmetriska chiffer (AES-256) förblir jämförelsevis stabila; Grovers algoritm halverar den effektiva säkerhetsnivån, men en dubblerad nyckellängd återställer marginalen. Den katastrofala exponeringen gäller asymmetriska algoritmer, och det är just de algoritmer som ligger till grund för varje autentiserad handskakning inom företagsfinans: RSA i SWIFT:s infrastruktur för öppna nycklar, ECDSA i klient- och serverautentisering över TLS, ECDH i etablering av sessionsnycklar, och ECC-varianter genom hela den mobila klientautentiseringen, API-signaturer och kedjor för kodsignering.

En funktionell CRQC som kör Shors algoritm försvagar inte dessa system gradvis. Den knäcker dem. Så snart en CRQC är i drift blir varje RSA-skyddad handskakning, varje ECDSA-signatur och varje nyckelutbyte med elliptiska kurvor återställbart, inte efter månaders arbete, utan på timmar. Övergången från ”säker” till ”komprometterad” är binär, och den sprider sig samtidigt över varje system som använder den drabbade algoritmen. Detta är grunden som den regulatoriska brådskan vilar på.

## Skärpta regelverk: en genomgång jurisdiktion för jurisdiktion

Den globala regulatoriska bilden i maj 2026 är inte längre ett lapptäcke av förslag. Det är en samordnad uppsättning tidplaner som varierar i stränghet men konvergerar mot samma mål. En multinationell bank som verkar över de större finansiella centren omfattas nu av den strängaste tillämpliga jurisdiktionen, inte den mildaste.

### USA

USA har den mest föreskrivande hållningen för varje institution som berör federala system. NSA:s [Commercial National Security Algorithm Suite 2.0 ⧉](https://informedclearly.com/en/technology/46563/quantum-encryption-race-post-quantum-security-standards-2026 "Quantum-Encryption Race 2026") kräver ML-KEM-1024 och ML-DSA-87 för system för nationell säkerhet, där nya system måste driftsätta PQC från januari 2027 och slutföra infrastrukturmigrationen senast 2035. OMB-memorandum M-23-02 binder federala myndigheter till samma bana. För affärsbanker går den omedelbara exponeringen genom federala upphandlingskedjor, NSS-närliggande kontrakt och det indirekta tryck som NSA:s vägledning lägger på den bredare marknaden.

### Europeiska unionen

EU verkar i tre lager. [Europeiska kommissionens samordnade genomförandefärdplan ⧉](https://pqshield.com/pqc-transition-roadmaps-and-guidance/ "PQC Roadmaps and Transition Guidance"), utarbetad av NIS-samarbetsgruppen i juni 2025, sätter fasindelade milstolpar vid 2026 (nationella strategier), 2030 (högriskssystem migrerade) och 2035 (fullständig övergång). Cyber Resilience Act kommer att kräva säkerhetsuppdateringar enligt senaste teknik för digitala produkter från slutet av 2027. NIS2 förstärker hanteringen av IKT-risker, även om ingetdera direktivet innehåller ett uttryckligt PQC-krav. Nationella tillsynsmyndigheter har dock gått före kommissionen. Tysklands BSI kräver hybrid nyckelutväxling och godkänner en konservativ korg av ML-KEM, FrodoKEM och Classic McEliece. Frankrikes ANSSI kräver hybrid för både nyckelinkapsling och signaturer. Nederländernas NLNCSA och Norges myndigheter har enats kring ML-KEM-1024 som konservativ baslinje för långlivade data.

### Storbritannien

Brittiska NCSC publicerade sin definitiva vägledning i mars 2025 och bekräftade den på nytt genom Annual Review 2025. Den treindelade tidplanen är tydlig:

- **Fram till 2028**: identifiera de kryptografiska tjänster som behöver uppgraderas, bygg migrationsplanen och ta fram ett fullständigt kryptografiskt inventarium.
- **2028 till 2031**: genomför högprioriterade uppgraderingar, särskilt på kritiska system och externt exponerade internetprotokoll.
- **2031 till 2035**: slutför migrationen över alla system, tjänster och produkter.

För brittiska finansinstitut ligger [CMORG (Cross-Market Operational Resilience Group) PQC-vägledning ⧉](https://www.cmorg.org.uk/sites/default/files/2025-06/CMORG%20-%20Guidance%20for%20Post-Quantum%20Cryptography%20-%20April%202025%20-%20TLP%20CLEAR%20(1).pdf "CMORG Guidance for Post-Quantum Cryptography") vid sidan av NCSC-ramverket, behandlar bankerna som kritisk nationell infrastruktur och betonar leverantörsberedskap och samordning i leveranskedjan.

### Asien och Stillahavsregionen

Hållningen i APAC är mer fragmenterad men rör sig snabbt. Australiens ASD har den hårdaste ståndpunkten globalt: klassisk kryptografi med öppen nyckel får inte användas bortom slutet av 2030, ingen hybridrekommendation, och ML-KEM-1024 krävs (ML-KEM-768 godtas endast fram till 2030). Organisationer bör ha en förfinad övergångsplan senast i slutet av 2026. Singapores Monetary Authority har utfärdat formell vägledning om kvantsäker beredskap. Japan och Sydkorea investerar avsevärt, även om båda har nationella algoritmspår (Korea har valt NTRU+ och SMAUG-T som KEM, ALMer och HAETAE som signaturer). Indiens National Quantum Mission, med ett statligt anslag på 6 003,65 crore rupier, pekar uttryckligen ut bank- och finanssystem som en strategisk prioritering. [Forresters APAC-prognoser för 2026 ⧉](https://www.forrester.com/press-newsroom/forrester-apac-2026-predictions/ "Forrester's 2026 APAC predictions") uppskattar att andelen regionala företag som väntas investera i postkvantteknik i år uppgår till mer än 90 %.

### Nettoläget

För en styrelse är den praktiska syntesen av dessa jurisdiktionella ståndpunkter enkel. En multinationell bank kan inte styra efter en enskild tillsynsmyndighets tidplan; den måste styra efter den strängaste tillämpliga. För de flesta större institutioner innebär det en planeringshorisont till slutet av 2030 för högriskssystem och slutet av 2035 för den långa svansen, där ASD-exponerade enheter siktar på ren PQC senast 2030 och CNSA-exponerade enheter siktar på samma fönster specifikt med ML-KEM-1024 och ML-DSA-87.

## BIS Project Leap: vad branschen faktiskt har bevisat

Project Leap förtjänar en styrelses uppmärksamhet inte för att det är en marknadsföringsmilstolpe, utan för att det är den mest trovärdiga demonstrationen från ände till ände av postkvantkryptografi i ett skarpt finansiellt betalningssystem hittills. Huvudslutsatsen är enkel: det fungerar. Detaljerna under ytan är där de operativa konsekvenserna ligger.

Fas 1, avslutad 2023, etablerade en kvantresistent VPN mellan IT-systemen hos Bank of France och Deutsche Bundesbank, med betalningsmeddelanden överförda mellan Paris och Frankfurt under ett hybridkrypteringsschema. Fas 2, avslutad i slutet av 2025 och [rapporterad i december ⧉](https://www.bis.org/publ/othp107.htm "Project Leap phase 2: quantum-proofing payment systems"), gick betydligt längre. Konsortiet ersatte traditionella RSA-baserade digitala signaturer med postkvantsignaturer i genomförandet av likviditetsöverföringar över TARGET2, Eurosystemets system för bruttoavveckling i realtid. Deltagarna, BIS Innovation Hub Eurosystem Centre, Bank of Italy, Banque de France, Deutsche Bundesbank, Nexi-Colt (som tillhandahåller TARGET2-anslutning) och Swift, representerar just de institutioner vars infrastruktur till slut måste migrera.

Rapporten lyfte fram tre resultat som varje migrationsprogram bör ta till sig:

- **Verifieringslatensen är påtagligt högre.** Verifiering av postkvantsignaturer tog väsentligt längre tid än RSA-baserad verifiering på samma hårdvara. För ett RTGS-system utformat kring meddelandehantering under en sekund är det inte en marginell observation; det är ett indata för kapacitetsplanering.
- **Paketstorlekar kräver ombyggnad av systemet.** PQC-signaturer är en storleksordning större än ECDSA-motsvarigheterna (mer om detta nedan). Betalningssystem vars interna köer, övervakningsverktyg och databasscheman dimensionerats för äldre meddelandestorlekar kan inte rymma den nya nyttolasten utan omkonstruktion. Project Leap konstaterade uttryckligen att TARGET2 inte kunde ”rymma enkelt” hybridmodellen utan omfattande ombyggnad.
- **Hybrid är det rätta svaret, men det är tyngre.** Att köra klassiska och postkvantalgoritmer parallellt bevarade bakåtkompatibiliteten och gav djupförsvar, men det fördubblade den kryptografiska bearbetningskostnaden. Detta är den operativa kostnaden för att göra PQC korrekt under övergången; den går inte att undvika enbart genom skicklig teknik.

För en finanschef som granskar ett affärscase för PQC är Project Leaps resultat användbara just för att de är precisa. Kostnaden för postkvantmigration är inte en enda kapitalpost. Det är verifieringslatens som fortplantar sig genom SLA-avtal, ökad meddelandestorlek som påverkar budgetar för lagring och bandbredd, och en övergångsperiod med dubblerade kryptografiska operationer som påverkar planeringen av beräkningskapacitet. Inget av detta är spekulativt. Det har mätts i ett skarpt centralbankssystem.

## NIST-verktygslådan: ML-KEM och ML-DSA jämförda

Den tekniska kärnan i varje trovärdigt nationellt ramverk är NIST-sviten av postkvantstandarder som publicerades i augusti 2024. Två av dessa standarder är i omedelbart fokus för företagsbank: ML-KEM (FIPS 203) för nyckelinkapsling och ML-DSA (FIPS 204) för digitala signaturer. De delar en matematisk grund, båda vilar på svårigheten i problemen Module Learning With Errors (ML-LWE) och Module Short Integer Solution över strukturerade gitter, men de fyller mycket olika roller i det kryptografiska beståndet, och deras prestanda- och storleksprofiler skiljer sig väsentligt.

### ML-KEM (FIPS 203): nyckelinkapsling

ML-KEM, härlett ur [CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html), är ersättaren för ECDH och RSA-KEM i protokoll där två parter behöver etablera en gemensam symmetrisk nyckel över en osäker kanal. Det är, i praktiken, dit TLS-handskakningar tar vägen efter att RSA och ECDH har pensionerats. NIST definierar tre parameteruppsättningar med stigande säkerhetsstyrka och sjunkande prestanda: ML-KEM-512 (NIST-kategori 1), ML-KEM-768 (kategori 3) och ML-KEM-1024 (kategori 5).

### ML-DSA (FIPS 204): digitala signaturer

ML-DSA, härlett ur CRYSTALS-Dilithium, är ersättaren för RSA- och ECDSA-signaturer. Det hanterar certifikatsignering, kodsignering, dokumentsignering och autentisering. De tre parameteruppsättningarna är ML-DSA-44, ML-DSA-65 och ML-DSA-87, som i grova drag motsvarar NIST-kategorierna 2, 3 och 5.

### Storleks- och prestandaprofil

För en IT-chef som ska dimensionera migrationskapaciteten är de viktigaste siffrorna artefaktstorlekarna. Det är indata till planering av nätverkskapacitet, lagringsprognoser och test på protokollnivå.

| Algoritm | Öppen nyckel | Chiffertext / signatur | Närmaste klassiska motsvarighet | Storlek mot klassisk |
|---|---|---|---|---|
| ML-KEM-512 | 800 byte | 768 byte (chiffertext) | ECDH P-256 (~32 byte öppen nyckel) | ~25× större |
| ML-KEM-768 | 1 184 byte | 1 088 byte (chiffertext) | ECDH P-384 | ~25× större |
| ML-KEM-1024 | 1 568 byte | 1 568 byte (chiffertext) | ECDH P-521 | ~25× större |
| ML-DSA-44 | 1 312 byte | ~2 420 byte (signatur) | ECDSA P-256 (64 byte signatur) | ~38× större |
| ML-DSA-65 | 1 952 byte | ~3 293 byte (signatur) | ECDSA P-384 | ~50× större |
| ML-DSA-87 | 2 592 byte | ~4 595 byte (signatur) | ECDSA P-521 | ~70× större |

*Källa: syntes av specifikationerna [NIST FIPS 203 ⧉](https://csrc.nist.gov/pubs/fips/203/final "FIPS 203, Module-Lattice-Based Key-Encapsulation Mechanism Standard") och FIPS 204, med jämförande data från oberoende benchmarklitteratur.*

Tre operativa konsekvenser följer direkt. **För det första** är signaturstorleken den bindande begränsningen för de flesta företagsutrullningar. En ML-DSA-65-signatur är ungefär femtio gånger så stor som en ECDSA P-256-signatur, och TLS-certifikatkedjor som bär mellanliggande CA:er växer proportionellt. Kapacitetsarbete på denna yta är inte valfritt, det är bärande. **För det andra** är ML-KEM beräkningsmässigt konkurrenskraftigt med ECDH och i vissa implementationer påtagligt snabbare, särskilt på hårdvara med vektoriserat stöd för den underliggande gitteraritmetiken. **För det tredje** är ML-DSA-verifiering genomgående snabb (ofta snabbare än ECDSA-verifiering), men ML-DSA-signering innefattar en förkastningsurvalsloop som kan kräva flera försök på begränsad hårdvara. För signeringstjänster med hög genomströmning är detta ett riktmärke att verifiera snarare än att anta.

### Att välja parameteruppsättningar

De jurisdiktionella ståndpunkterna om parameterval är inte identiska, men konvergensen är tydlig. ML-KEM-768 och ML-DSA-65 är företagsgolvet, förordade av brittiska NCSC som baslinje för brittiska organisationer och godtagbara under de flesta europeiska ramverk. ML-KEM-1024 och ML-DSA-87 är det konservativa taket, obligatoriska enligt NSA CNSA 2.0 för amerikanska system för nationell säkerhet och krävda av ASD för australiska reglerade enheter senast 2030. För data med extremt långsiktig känslighet, statliga avvecklingsloggar, immateriella tillgångar med decennielång horisont, depåförteckningar för långa instrument, är de högre parameteruppsättningarna det försvarbara förvalet.

### En gemensam matematisk grund, en gemensam risk

En poäng på styrelsenivå värd att notera: både ML-KEM och ML-DSA hämtar sin säkerhet från samma familj av gitterproblem. Ett framtida kryptoanalytiskt genombrott mot Module-LWE skulle påverka båda standarderna samtidigt. Det är just därför flera nationella myndigheter, framför allt Tysklands BSI och Frankrikes ANSSI, rekommenderar att man kompletterar den gitterbaserade stacken med hashbaserade signaturer (SLH-DSA, FIPS 205) för långsiktig signering och kodsignering. Kryptoagilitet handlar i denna mening inte bara om att kunna byta ut RSA mot ML-KEM. Det handlar om att kunna byta en PQC-algoritm mot en annan när det kryptoanalytiska läget förändras.

## En logisk migrationsväg: inventering → triage → hybridutrullning

För en styrelse som godkänner ett flerårigt PQC-program är den operativa frågan hur arbetet ska fasas utan att ta oacceptabla risker för tjänstetillgänglighet. Mönstret som har vuxit fram över G7-färdplanen, NCSC-ramverket, BIS Project Leap och de större nationella vägledningsdokumenten konvergerar mot tre faser.

```
┌──────────────────────┐   ┌──────────────────────┐   ┌──────────────────────┐
│ 1. INVENTERING & CBOM│ → │  2. TRIAGE (MOSCA)   │ → │  3. HYBRID-UTRULLNING│
│  Kryptografiskt      │   │  Riskbaserad         │   │  Dubbelt hölje       │
│  inventarium över    │   │  prioritering efter  │   │  klassisk + PQC,     │
│  alla system         │   │  datas hållbarhet    │   │  kryptoagil          │
└──────────────────────┘   └──────────────────────┘   └──────────────────────┘
```

### Fas 1: inventering och den kryptografiska materialförteckningen (CBOM)

Migration kan inte planeras för ett kryptografiskt bestånd som inte har kartlagts, och de flesta institutioner saknar en exakt karta. Den första fasen är därför framtagningen av en Cryptographic Bill of Materials, ett strukturerat inventarium över varje förekomst av asymmetrisk kryptografi i organisationen, där varje förekomst märks med algoritm, nyckellängd, protokollkontext, datakänslighet och systemägare. Automatiserad genomsökning av kodbaser, webbapplikationer, containeravbildningar, databaskonfigurationer, certifikatlager, hårdvarusäkerhetsmoduler och leverantörsgränssnitt är den praktiska mekanismen; manuell inventering av äldre system och proprietära protokoll är det oundvikliga komplementet.

Resultatet av fas 1 är inte glamoröst, men det är den enda grund som fas 2 och 3 kan vila på. Det är också den leverabel som de flesta internrevisionsfunktioner och externa tillsynsmyndigheter kommer att fråga efter först när intyg om PQC-efterlevnad börjar begäras.

### Fas 2: risktriage med Mosca-ekvationen

Med CBOM i handen kan institutionen tillämpa Moscas ramverk tillgång för tillgång. För varje kryptografiskt beroende är frågan om **S + M > Q**, det vill säga om datas hållbarhet plus migrationstiden överstiger den uppskattade tiden till en CRQC. Tillgångar där olikheten är som mest akut, långlivade känsliga data på infrastruktur som tar år att migrera, hamnar först i kön. Tillgångar med kort datalivslängd eller redan moderniserad infrastruktur kan sekvenseras senare i programmet.

Detta är den fas där styrelsens riskaptit är som mest synlig. Det Q-värde som institutionen väljer att planera mot är i praktiken en strategisk satsning på takten i kvanthårdvarans utveckling. Ett konservativt Q (mitten av 2030-talet) ger en mer aggressiv migrationsplan och en högre kapitalpost på kort sikt. Ett optimistiskt Q (efter 2040) ger en mer avspänd plan och en högre kvarstående exponering för data som redan skördas. Ingetdera är fel; båda bör vara uttryckliga beslut av styrelsen, inte underförstådda förval hos teknikfunktionen.

### Fas 3: hybridutrullning

När prioriterade tillgångar har identifierats bör utrullningen följa det hybridmönster som bevisats i Project Leap och som förordas av NCSC, ANSSI, BSI och G7-färdplanen. En hybridutrullning kör en klassisk algoritm och en postkvantalgoritm parallellt och kombinerar deras utdata i ett enda hölje. Sammansättningen är säker mot både klassiska angrepp (den klassiska algoritmen håller i dag) och kvantangrepp (PQC-algoritmen håller i morgon). Konkret är det vanliga mönstret X25519 kombinerat med ML-KEM-768 eller ML-KEM-1024 för nyckelinkapsling, och ECDSA kombinerat med ML-DSA för signaturer där dubbla signaturer är operativt genomförbara.

Project Leaps konstaterande att hybrid är ”mycket, mycket tyngre” än något av de rena tillvägagångssätten är den ärliga motvikten till denna rekommendation. Styrelser bör räkna med ökad beräknings- och lagringskapacitet, längre handskakningar och ytterligare komplexitet i certifikatkedjor under övergången. Avvägningen är att hybrid tar bort den enskilt största källan till migrationsrisk: den stupbranta övergången från en kryptografisk grund till en annan i en produktionsmiljö.

## Vad detta kostar och varför att inte göra något kostar mer

Mastercards analys, [rapporterad i början av 2026 ⧉](https://www.qnulabs.com/blog/bank-2030-expiry-date-q-day-fatal-strategy "Your Bank's 2030 Expiry — QNu Labs"), uppskattade kostnaden för PQC-migration i den globala finanssektorn till 28–42 miljarder US-dollar. Inom det aggregatet tyder [forskningen från RedCompass Labs och CMORG ⧉](https://www.cmorg.org.uk/sites/default/files/2025-06/CMORG%20-%20Guidance%20for%20Post-Quantum%20Cryptography%20-%20April%202025%20-%20TLP%20CLEAR%20(1).pdf "CMORG Guidance for Post-Quantum Cryptography"), som följer den faktiska institutionella utgiften, på att banker i första ledet avsätter 20–30 miljoner US-dollar per år till beredskapsprogram, med genomförandetidplaner som sträcker sig över flera ledarskapscykler. Detta är betydande belopp. De är dock inte den relevanta jämförelsen.

Den relevanta jämförelsen är kostnaden för en enda retroaktiv dekrypteringshändelse. För en institution vars skördade betalningstrafik, M&A-korrespondens eller data om motpartsexponering blir läsbar för en motståndare 2032 begränsas den operativa och anseendemässiga kostnaden inte av migrationens investeringspost. Den begränsas av värdet på det underliggande decenniet av strategisk information, vilket för varje systemviktig institution är väsentligt större än varje rimlig migrationsbudget. G7:s inramning av kryptografisk övergång som en fråga om systemisk riskhantering snarare än en teknikuppgradering är korrekt, och styrelser bör förhålla sig till den på den grunden.

Det finns en andra kostnadspost värd att särskilja. Migration till PQC är en tvingande funktion för kryptoagilitet, den arkitektoniska förmågan att byta kryptografiska algoritmer utan att bygga om de system som är beroende av dem. De flesta institutioner har i dag inte kryptoagilitet; deras beroenden av RSA och ECC är djupt inbäddade i PKI:er, kedjor för kodsignering, leverantörsintegrationer och skräddarsydda protokoll som har ackumulerats över decennier. Investeringen i agilitet, gjord under trycket av PQC-övergången, är varaktig. Den kommer att tas i anspråk igen när nästa kryptografiska övergång inträffar, oavsett om det är en efterföljare till gitterbaserad PQC, ett överlägg med kvantnyckeldistribution eller något som ännu inte finns på standardernas färdplan. Om den hanteras rätt är PQC-migrationens investering en engångsinvestering som ger återkommande valmöjligheter.

## Slutsats

Argumentet för att behandla postkvantmigration som en prioritering på styrelsenivå under 2026 vilar inte på att en CRQC är nära förestående. Uppskattningarna av detta förblir genuint osäkra, trovärdig vetenskaplig bedömning sätter sannolikheten för en CRQC senast 2028 långt under en procent, stigande till ungefär femtio procent kring 2037–2040. Argumentet vilar på tre andra observationer som inte är osäkra.

För det första pågår harvest-now-decrypt-later i dag, och data med ett konfidentialitetskrav på ett decennium eller mer är exponerade oavsett när CRQC:n anländer. För det andra tar migrationen av ett stort finansinstituts kryptografiska bestånd fem till sju år även med tillräcklig finansiering och ledningsfokus, vilket innebär att programmet som påbörjas 2026 avslutas omkring 2031, vilket ligger väl inom den konservativa änden av sannolikhetsfördelningen för CRQC. För det tredje har de regulatoriska förväntningarna skärpts väsentligt de senaste tolv månaderna, och de institutioner vars styrelseprotokoll för 2026 dokumenterar ett tydligt PQC-program kommer att stå i en påtagligt starkare position än de vars protokoll endast noterar en avvaktande hållning.

De institutioner som börjar nu har fördelen av att kunna välja. De kan sekvensera arbetet över ledarskapscykler, integrera det med bredare resiliensinitiativ och ta upp de operativa kostnaderna för hybridutrullning inom normal kapitalplanering. De institutioner som väntar kommer att möta samma arbete under snävare tidsfrister, med mindre utrymme för sekvensering, och mot en bakgrund av leveransbegränsningar för PQC-kapabel hårdvara, expertis och leverantörskapacitet. Kostnaden för att agera tidigt är känd; kostnaden för att agera sent är asymmetrisk på precis det sätt som riskhantering är utformad för att undvika.

För tidigare sammanhang på den här sajten granskade [artikeln från april 2026 om komprimeringen av kvanttrösklar](https://sebastienrousseau.com/2026-04-11-quantum-thresholds-are-moving-again/index.html "Quantum Thresholds Are Moving Again") den underliggande hårdvaruutvecklingen, [analysen från november 2023 av CRYSTALS-Kyber](https://sebastienrousseau.com/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html "CRYSTALS-Kyber: The Safeguarding Algorithm in a Quantum Age") täckte de matematiska grunder som nu standardiserats som ML-KEM, [artikeln från december 2023 om kvantnyckeldistribution](https://sebastienrousseau.com/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html "Quantum Key Distribution Revolutionising Security in Banking") behandlade det kompletterande [QKD](/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html)-överlägget, och [referensimplementationen KyberLib med öppen källkod](https://sebastienrousseau.com/2023-11-28-kyberlib-a-rust-powered-shield-against-quantum-threats/index.html "KyberLib: A Rust-Powered Shield Against Quantum Threats") tillhandahåller en fungerande Rust-implementation av de underliggande primitiverna för institutioner som vill granska den kryptografiska ytan direkt. Att fördjupa sig i den praktiska och tekniska detaljen, inte bara de regulatoriska rubrikerna, är hur styrelser skiljer trovärdiga migrationsprogram från efterlevnadsteater.

## Vanliga frågor

**När kommer en kryptografiskt relevant kvantdator faktiskt att finnas?**

Trovärdiga uppskattningar varierar kraftigt. I början av 2026 har offentliga kvantdemonstrationer uppnått ungefär 24 till 28 logiska qubitar, medan en CRQC uppskattas kräva omkring 6 000 logiska qubitar understödda av någonstans mellan 100 000 och flera miljoner fysiska qubitar, beroende på metoden för felkorrigering. Expertkonsensus sätter sannolikheten för en CRQC under en procent senast 2028, kring femtio procent kring 2037–2040, med betydande variation mellan prognoser. Nyliga sänkningar av de teoretiska resursuppskattningarna, från 20 miljoner qubitar för några år sedan till under en miljon i Gidneys arbete från 2025, och till ungefär 100 000 i QLDPC-arkitekturdokumentet från februari 2026, har komprimerat planeringshorisonten. För styrelseändamål är det lämpliga planeringsantagandet mitten av 2030-talet för högriskssystem, slutet av 2030-talet som konservativ mittpunkt, och tidigare om HNDL-exponering är den bindande oron.

**Varför hybridutrullning snarare än ren postkvant?**

Tre skäl. För det första har ML-KEM och ML-DSA, även om de är väl granskade, kortare kryptoanalytisk historik än RSA och ECC. Ett hybridschema förblir säkert om någon av komponenterna håller; ett rent PQC-schema är exponerat om gitterproblemet oväntat försvagas. För det andra bevarar hybrid bakåtkompatibiliteten med motparter som ännu inte har migrerat, vilket är kritiskt i en flerårig branschövergång. För det tredje rekommenderar varje större myndighet utanför Australian Signals Directorate uttryckligen hybrid för övergångsperioden: NCSC, ANSSI, BSI, NLNCSA och G7-ramverket ställer sig alla bakom tillvägagångssättet med dubbelt hölje. Avvägningen, som Project Leap kvantifierade, är en påtagligt högre kostnad i beräkning och lagring. Det är priset för valmöjlighet.

**Behöver vi både ML-KEM och ML-DSA, eller kan vi välja en?**

Båda. ML-KEM och ML-DSA fyller olika kryptografiska roller. ML-KEM ersätter primitiverna för nyckeletablering i TLS, VPN, mobil autentisering och liknande protokoll där två parter behöver komma överens om en gemensam symmetrisk nyckel. ML-DSA ersätter primitiverna för digital signatur i PKI-certifikat, kodsignering, dokumentsignering, autentiserad meddelandehantering av SWIFT-typ och identitetspåståenden. En institutions kryptografiska bestånd använder båda typerna av primitiv på olika ställen; migrationen måste hantera båda. ML-DSA:s betydligt större signaturstorlek (50–70× ECDSA) är vanligtvis den mer operativt krävande av de två; planeringsarbetet för nätverk och lagring för ML-DSA dominerar de flesta bedömningar av migrationskapacitet.

**Hur mäter vi framsteg i ett program av denna storlek?**

Tre mått är praktiska och ligger i linje med de större regulatoriska ramverken. **Täckning av CBOM:en**, hur stor andel av institutionens asymmetriska kryptografiska förekomster som har inventerats, klassificerats och märkts för migrationsprioritet. **Migrationstäckning för högrisktillgångar**, hur stor andel av de tillgångar där Moscas villkor S + M > Q gäller som har flyttats till hybrid-PQC. **Täckning av kryptoagilitet**, hur stor andel av de system med kryptografiskt beroende som kan byta algoritm utan kodändringar, enbart genom konfiguration. G7 CEG-färdplanen, NCSC:s treindelade ramverk och EU:s samordnade färdplan pekar alla mot ungefär dessa tre mått, även där de använder olika terminologi.

**Vad kostar det att vänta ytterligare ett år?**

Den är inte noll, och den är inte symmetrisk. Att vänta ett år förverkar ett års HNDL-skydd på långlivade data, data vars konfidentialitetskrav sträcker sig till 2040 är exponerade ett år längre än nödvändigt. Det komprimerar migrationsfönstret mot fasta regulatoriska tidsfrister (ASD 2030, NSA CNSA 2.0-milstolpar, EU:s mål för kritiska system 2030), vilket översätts till högre leveransrisk och minskad flexibilitet i sekvenseringen. Det exponerar institutionen för leverantörs- och kompetensbegränsningar som redan syns på marknaden och som kommer att förvärras när branschens största aktörer går från planering till genomförande. Kostnaden är inte katastrofal under ett enskilt år, men den ackumuleras, och det regulatoriska klimatet konvergerar mot en position där styrelser förväntas förklara dröjsmålet snarare än utgiften.

## Referenser

- Sebastien Rousseau, (2026). [Quantum Thresholds Are Moving Again](https://sebastienrousseau.com/2026-04-11-quantum-thresholds-are-moving-again/index.html "Quantum Thresholds Are Moving Again").
- Sebastien Rousseau, (2023). [CRYSTALS-Kyber: The Safeguarding Algorithm in a Quantum Age](https://sebastienrousseau.com/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html "CRYSTALS-Kyber: The Safeguarding Algorithm in a Quantum Age").
- Sebastien Rousseau, (2023). [Quantum Key Distribution Revolutionising Security in Banking](https://sebastienrousseau.com/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html "Quantum Key Distribution Revolutionising Security in Banking").
- Sebastien Rousseau, (2023). [KyberLib: A Rust-Powered Shield Against Quantum Threats](https://sebastienrousseau.com/2023-11-28-kyberlib-a-rust-powered-shield-against-quantum-threats/index.html "KyberLib: A Rust-Powered Shield Against Quantum Threats").
- G7 Cyber Expert Group, (2026). [Advancing a Coordinated Roadmap for the Transition to Post-Quantum Cryptography in the Financial Sector ⧉](https://www.gov.uk/government/publications/advancing-a-coordinated-roadmap-for-the-transition-to-post-quantum-cryptography-in-the-financial-sector/g7-cyber-expert-group-statement-on-advancing-a-coordinated-roadmap-for-the-transition-to-post-quantum-cryptography-in-the-financial-sector-january-20 "G7 CEG Statement, January 2026"). GOV.UK.
- Bank for International Settlements, (2025). [Project Leap Phase 2: Quantum-Proofing Payment Systems ⧉](https://www.bis.org/publ/othp107.htm "Project Leap phase 2: quantum-proofing payment systems"). BIS.
- Bank for International Settlements, (2025). [Project Leap: Quantum-Proofing the Financial System ⧉](https://www.bis.org/about/bisih/topics/cyber_security/leap.htm "Project Leap: quantum-proofing the financial system"). BIS.
- NIST, (2024). [FIPS 203: Module-Lattice-Based Key-Encapsulation Mechanism Standard ⧉](https://csrc.nist.gov/pubs/fips/203/final "FIPS 203, Module-Lattice-Based Key-Encapsulation Mechanism Standard"). NIST.
- UK NCSC, (2025). [Timelines for Migration to Post-Quantum Cryptography ⧉](https://www.ncsc.gov.uk/guidance/pqc-migration-timelines "Timelines for migration to post-quantum cryptography — NCSC"). UK National Cyber Security Centre.
- CMORG, (2025). [Guidance for Post-Quantum Cryptography ⧉](https://www.cmorg.org.uk/sites/default/files/2025-06/CMORG%20-%20Guidance%20for%20Post-Quantum%20Cryptography%20-%20April%202025%20-%20TLP%20CLEAR%20(1).pdf "CMORG Guidance for Post-Quantum Cryptography"). Cross-Market Operational Resilience Group.
- Post-Quantum Cryptography Coalition, (2025). [International PQC Requirements ⧉](https://pqcc.org/international-pqc-requirements/ "International PQC Requirements — Post-Quantum Cryptography Coalition"). PQCC.
- PQShield, (2025). [PQC Roadmaps and Transition Guidance ⧉](https://pqshield.com/pqc-transition-roadmaps-and-guidance/ "PQC Roadmaps and Transition Guidance"). PQShield.
- Banking.Vision, (2026). [The Year of Quantum Computing: 2026 ⧉](https://banking.vision/en/the-year-of-quantum-computing/ "The Year of Quantum Computing 2026"). Banking.Vision / msg for banking.
- The Quantum Insider, (2026). [How to Prep For Post-Quantum Cryptography: G7 Releases Roadmap ⧉](https://thequantuminsider.com/2026/01/15/how-to-prep-for-post-quantum-crytography-g7-releases-roadmap-to-help-financial-sector-navigate-transition-to-quantum-era/ "How to Prep For Post-Quantum Cryptography — The Quantum Insider"). The Quantum Insider.
- Quantum Computing Report, (2026). [Shor, QLDPC Codes, and the Compression of RSA-2048 Resource Estimates ⧉](https://quantumcomputingreport.com/shor-qldpc-codes-and-the-compression-of-rsa-2048-resource-estimates-part-i/ "Shor, QLDPC Codes, and the Compression of RSA-2048 Resource Estimates"). Quantum Computing Report.
- Cryptomathic, (2025). [A Banker's Guide to Quantum Safe Cryptography — Roadmap to PQC Migration for Financial Institutions ⧉](https://www.cryptomathic.com/a-bankers-guide-to-quantum-safe-cryptography-part-3-roadmap-to-pqc-migration-for-financial-institutions-cryptomathic "A Banker's Guide to Quantum Safe Cryptography"). Cryptomathic.
- Forrester, (2025). [2026 Asia Pacific Predictions: Quantum Security ⧉](https://www.forrester.com/press-newsroom/forrester-apac-2026-predictions/ "Forrester's 2026 APAC Predictions"). Forrester Research.
- The Asian Banker, (2025). [Building Resilience for a Quantum-Ready Financial System ⧉](https://www.theasianbanker.com/updates-and-articles/building-resilience-for-a-quantum-ready-financial-system "Building resilience for a quantum-ready financial system"). The Asian Banker.
