---
title: "De reset van kwantumcryptografie in 2026: PQC-standaarden, QKD-assurance en het migratiewerk dat banken niet langer kunnen uitstellen"
subtitle: "Kwantumcryptografie is verschoven van horizonverkenning naar implementatiediscipline: de NIST PQC-standaarden zijn klaar, de leidraad van het Britse NCSC heeft de algoritmekeuzes versmald, het protocolwerk van de IETF rijpt nog, en QKD-assurance verschuift van laboratoriumvertrouwen naar certificeringstaal."
description: "Kwantumcryptografie in 2026 is niet langer een debat over de vraag of kwantumcomputers nakend zijn. Het is een migratieprogramma dat post-kwantumcryptografie, crypto-agility, QKD-assurance, protocolstandaarden, leveranciersparaatheid en langlevende financiële data raakt die al worden blootgesteld aan het «harvest-now-decrypt-later»-risico."
date: "May 18, 2026"
language: "nl-NL"
locale: "nl_NL"
banner: "https://cloudcdn.pro/stock/images/alex-shuper-YYZnrK8NrSw-unsplash.webp"
banner_alt: "Migratiekaart voor kwantumveilige cryptografie voor 2026 — NIST PQC-standaarden, werk aan hybride protocollen, QKD-assurance, crypto-agility en risiconiveaus voor bankgegevens"
keywords: "kwantumcryptografie 2026, post-kwantumcryptografie, NIST FIPS 203, FIPS 204, FIPS 205, ML-KEM, ML-DSA, SLH-DSA, NCSC PQC, IETF TLS, IPsec, RFC 9794, hybride sleuteluitwisseling, QKD, ETSI QKD, ISO IEC 23837, crypto-agility, harvest now decrypt later, HNDL, cryptografie voor financiële dienstverlening, bankbeveiliging"
tags: "kwantumcryptografie, post-kwantumcryptografie, PQC, NIST, FIPS 203, FIPS 204, FIPS 205, ML-KEM, ML-DSA, SLH-DSA, NCSC, IETF, TLS, IPsec, QKD, ETSI, crypto-agility, HNDL, bankbeveiliging"
item_title: "De reset van kwantumcryptografie in 2026: PQC-standaarden, QKD-assurance en het migratiewerk dat banken niet langer kunnen uitstellen"
item_description: "De reset van kwantumcryptografie 2026 — NIST PQC-standaarden, migratieadvies van de NCSC, protocolrijpheid van de IETF, QKD-assurance, crypto-agility en waar banken deze week prioriteit aan moeten geven."
twitter_title: "Kwantumcryptografie 2026: PQC-standaarden en bankmigratie"
twitter_description: "De reset van kwantumcryptografie 2026 — NIST PQC-standaarden, migratieadvies van de NCSC, protocolrijpheid van de IETF, QKD-assurance, crypto-agility en waar banken deze week prioriteit aan moeten geven."
---

# De reset van kwantumcryptografie in 2026: PQC-standaarden, QKD-assurance en het migratiewerk dat banken niet langer kunnen uitstellen

Kwantumcryptografie is in 2026 in twee praktische sporen gesplitst. Post-kwantumcryptografie is nu een implementatieprogramma, omdat NIST aangeeft dat drie post-kwantumstandaarden klaar zijn voor gebruik en dat federale systemen ze als FIPS-standaarden moeten behandelen ([NIST](https://www.nist.gov/pqc "NIST Post-Quantum Cryptography")); kwantumsleuteldistributie wordt een assurance- en certificeringsvraagstuk, omdat QKD-implementaties evaluatietaal, beschermingsprofielen en operationele standaarden nodig hebben in plaats van uitsluitend laboratoriumdemonstraties ([ID Quantique / ETSI QKD 016](https://www.idquantique.com/etsi-releases-qkd-protection-profile/ "ETSI publiceert QKD-beschermingsprofiel")).

---

> **Samenvatting / Belangrijkste inzichten**
>
> - **NIST heeft PQC in de implementatiefase gebracht.** De huidige standaarden zijn FIPS 203 voor ML-KEM-sleutelvestiging, FIPS 204 voor ML-DSA-handtekeningen en FIPS 205 voor SLH-DSA-handtekeningen; NIST dringt er bij organisaties op aan kwetsbare cryptografie te identificeren en nu met de migratie te beginnen ([NIST](https://www.nist.gov/pqc "NIST Post-Quantum Cryptography")).
> - **Het Britse NCSC heeft de praktische keuzes versmald.** Het beveelt ML-KEM-768 en ML-DSA-65 aan voor de meeste toepassingen en waarschuwt dat systemen moeten leunen op robuuste implementaties van definitieve standaarden, niet op concept-compatibele experimenten ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "Volgende stappen ter voorbereiding op PQC")).
> - **De protocolrijpheid is ongelijk.** De IETF werkt TLS en IPsec bij voor PQC en hybride sleuteluitwisseling, maar het NCSC waarschuwt dat operationele systemen gepubliceerde RFC's moeten verkiezen boven veranderende Internet Drafts ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "Volgende stappen ter voorbereiding op PQC")).
> - **Hybride is een overgangsmechanisme, geen eindtoestand.** Hybride publieke-sleutel-plus-post-kwantumschema's helpen de migratie te faseren en het implementatierisico af te dekken, maar voegen complexiteit toe en kunnen later een tweede migratie naar uitsluitend-PQC vereisen ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "Volgende stappen ter voorbereiding op PQC")).
> - **QKD is geen vervanging voor PQC.** QKD kan gespecialiseerde verbindingen met hoge assurance bedienen, maar de bancaire relevantie ervan hangt af van certificering, interoperabiliteit, operationele kosten en integratie met bestaande sleutelmanagementsystemen, niet alleen van de fysica ([ID Quantique / ETSI QKD 016](https://www.idquantique.com/etsi-releases-qkd-protection-profile/ "ETSI publiceert QKD-beschermingsprofiel")).
> - **De vraag op bankniveau is de inventaris.** Een financiële instelling die RSA, ECDH, ECDSA, EdDSA, proprietary VPN-cryptografie, HSM-templates, certificaatlooptijden en leveranciersbeheerde cryptografie niet kan lokaliseren, kan niet migreren, ongeacht welke standaarden beschikbaar zijn.
> - **Het risico is al actief.** Harvest-now-decrypt-later-aanvallen maken langlevende financiële data kwetsbaar voordat cryptografisch relevante kwantumcomputers bestaan, omdat de tegenstander vandaag slechts de cijfertekst hoeft te verzamelen.
> - **Crypto-agility is de duurzame controle.** De winnende architectuur is geen eenmalige overstap van RSA naar ML-KEM; het is een platformvermogen om algoritmen, parameters, bibliotheken, certificaten, hardwarebeleid en protocolmodi te rouleren zonder de bank te herbouwen.
>
---

## Waarom deze week ertoe doet

Het standaarden-gesprek is voorbij het punt van abstractie. De publieke leidraad van NIST stelt dat organisaties nu moeten beginnen met het toepassen van de nieuwe standaarden, identificeren waar kwetsbare algoritmen worden gebruikt en updates van producten, diensten en protocollen plannen ([NIST](https://www.nist.gov/pqc "NIST Post-Quantum Cryptography")). Die formulering doet ertoe omdat zij PQC verandert van een onderzoeksonderwerp in een afhankelijkheid voor technologie-vernieuwing.

Het tijdpad doet er ook toe omdat financiële data een lange vertrouwelijkheidshalfwaardetijd hebben. M&A-materialen, treasury-stromen, sanctie-onderzoeken, klantidentiteitsdocumenten, betalingsroutering-metadata en wholesale-settlementgegevens kunnen jarenlang gevoelig blijven. De kwantumcomputer die klassieke publieke-sleutel-cryptografie breekt, hoeft vandaag niet te bestaan opdat de blootstelling vandaag rationeel is.

## De cryptografische basislijn 2026: vier werkstromen

### 1. PQC-standaarden zijn klaar genoeg om mee te plannen

De eerste basis is algoritmisch. Het PQC-programma van NIST geeft technologieleiders nu benoemde doelen: ML-KEM voor sleutelvestiging, ML-DSA voor algemene digitale handtekeningen en SLH-DSA voor hashgebaseerde handtekeningen ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "Volgende stappen ter voorbereiding op PQC")). De praktische impact is dat procurement-, architectuur- en leveranciersbeheer-teams kunnen stoppen met vragen of PQC-standaarden zullen bestaan en kunnen beginnen te vragen wanneer elk systeem ze zal ondersteunen.

Het delicatere punt is compatibiliteit. Het NCSC waarschuwt dat implementaties gebaseerd op conceptstandaarden mogelijk niet compatibel zijn met definitieve standaarden, precies het soort detail dat migraties in grote banken doet ontsporen als het wordt genegeerd ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "Volgende stappen ter voorbereiding op PQC")). Banken zouden daarom experimentele pilots moeten scheiden van productiemigratiepaden.

### 2. Protocollen zijn het knelpunt

Algoritmen beveiligen het bankverkeer niet vanzelf. TLS, IPsec, SSH, S/MIME, betalings-API's, HSM-integraties en certificaatbeheer-stacks hebben allemaal ondersteuning op protocolniveau nodig. Het NCSC stelt dat de IETF veelgebruikte protocollen zoals TLS en IPsec bijwerkt, zodat PQC-algoritmen in sleuteluitwisseling- en handtekeningmechanismen kunnen worden opgenomen ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "Volgende stappen ter voorbereiding op PQC")).

Dat creëert een gefaseerd implementatieprobleem. Een bank kan onmiddellijk cryptografie inventariseren, onmiddellijk leveranciersroadmaps eisen en onmiddellijk crypto-agility ontwerpen, maar moet mogelijk nog wachten op stabiele protocolimplementaties voordat zij kritische productie-kanalen verplaatst.

### 3. QKD wordt een assurance-discipline

Kwantumsleuteldistributie blijft relevant voor zeer gespecialiseerde verbindingen, vooral wanneer de instelling de eindpunten en netwerkroutes beheert. De belangrijke ontwikkeling in 2026 is geen nieuwe QKD-doos; het is het ontstaan van certificeringstaal, met ETSI GS QKD 016 beschreven als een mijlpaal van een beschermingsprofiel voor de evaluatie van QKD-producten ([ID Quantique / ETSI QKD 016](https://www.idquantique.com/etsi-releases-qkd-protection-profile/ "ETSI publiceert QKD-beschermingsprofiel")).

Voor banken verschuift dit het inkoopgesprek. De juiste vraag is niet langer of QKD in beginsel kwantum-veilig is. De juiste vraag is of het apparaat, de integratie, het sleutelmanagementproces, de operationele omgeving en het certificeringsbewijs voldoen aan het dreigingsmodel van de bank.

### 4. Crypto-agility is de architectuur

Crypto-agility is het vermogen om algoritmen te veranderen zonder het hele systeem te veranderen. Het omvat softwarebibliotheken, protocolonderhandeling, HSM-policy, certificaatprofielen, sleutellevensduur, ondertekendiensten, auditbewijs en rollback-paden. Zonder dit wordt elke cryptografische migratie een maatwerkproject.

Dat is de centrale architecturale les. De post-kwantum-overgang zal niet de laatste cryptografische overgang zijn waarmee het financiële systeem wordt geconfronteerd. Banken die nu crypto-agility opbouwen, krijgen een herbruikbaar controleniveau voor algoritme-updates, leveranciersrisico, noodintrekking en bewijs voor de toezichthouder.

## Wat banken nu moeten doen

### Bouw de cryptografische asset-inventaris op

Het eerste op te leveren product is een cryptografische bill of materials. Dit moet publieke-sleutel-algoritmen, sleutellengtes, certificaatautoriteiten, HSM-templates, TLS-versies, VPN-producten, betalingsgateways, API's van derden, mobiele SDK's, wrappers voor versleuteling van data-at-rest, ondertekensleutels, firmware-ondertekenprocessen en leveranciersbeheerde cryptografie omvatten.

De inventaris moet onderscheid maken tussen vertrouwelijkheid en authenticiteit. Langlevende versleutelde data zijn blootgesteld aan het harvest-now-decrypt-later-risico, terwijl langlevende ondertekensleutels toekomstige vervalsingsrisico's creëren als zij verankerd blijven in kwetsbare publieke-sleutel-algoritmen.

### Segmenteer naar halfwaardetijd van data

Niet alle data behoeven dezelfde migratievolgorde. Een real-time kaartautorisatiebericht kan een andere vertrouwelijkheidshalfwaardetijd hebben dan een sanctie-onderzoek, een corporate-acquisitie-dossier, een private-banking-identiteitspak of een document over de uitgifte van staatsschuld. Daarom hoort kwantummigratie evenzeer thuis bij dataclassificatie als bij netwerkbeveiliging.

De prioriteit moet liggen bij systemen die langlevende data beschermen met kwetsbare sleutelvestiging. Dat zijn de systemen waarin verzameling van vandaag de blootstelling van morgen creëert.

### Dwing leveranciersroadmaps af in contracten

NIST stelt dat producten, diensten en protocollen updates nodig hebben voor de overgang ([NIST](https://www.nist.gov/pqc "NIST Post-Quantum Cryptography")). Dat betekent dat de inkooptaal moet veranderen. Leveranciers moeten PQC-ondersteuningsschema's, compatibiliteit met definitieve standaarden, gedrag in hybride modus, beperkingen van hardwaremodules, prestatie-impact, ondersteuning van certificaatprofielen en fallback-controles bekendmaken.

Een leverancier die alleen «quantum-safe roadmap» zegt, heeft de vraag niet beantwoord. De bank heeft data, algoritmen, integratiegrenzen en bewijs nodig.

## PQC, QKD en hybride: een praktische beslissingstabel

| Controle | Beste gebruik | Status 2026 | Bancair voorbehoud |
|---|---|---|---|
| **ML-KEM / FIPS 203** | Sleutelvestiging voor toekomstbestendige vertrouwelijkheid | Gestandaardiseerd en klaar voor implementatieplanning ([NIST](https://www.nist.gov/pqc "NIST Post-Quantum Cryptography")) | Heeft protocol- en bibliotheekondersteuning nodig vóór kritieke productie-uitrol |
| **ML-DSA / FIPS 204** | Algemene digitale handtekeningen | Aanbevolen door het NCSC voor de meeste algemene handtekeningscenario's ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "Volgende stappen ter voorbereiding op PQC")) | Certificaatketens en PKI-migratie zijn operationeel moeilijk |
| **SLH-DSA / FIPS 205** | Hashgebaseerde handtekeningen voor firmware- en softwareondertekening | Definitieve NIST-standaard waaraan het NCSC refereert ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "Volgende stappen ter voorbereiding op PQC")) | Grotere handtekeningen kunnen beperkte omgevingen beïnvloeden |
| **Hybride PQ/T-schema's** | Tussenliggende migratie en interoperabiliteit | Nuttig als overgangsmaatregel ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "Volgende stappen ter voorbereiding op PQC")) | Voegt complexiteit toe en kan een tweede migratie vereisen |
| **QKD** | Gespecialiseerde verbindingen met hoge assurance | Assurance-werk rijpt via ETSI-beschermingsprofielactiviteit ([ID Quantique / ETSI QKD 016](https://www.idquantique.com/etsi-releases-qkd-protection-profile/ "ETSI publiceert QKD-beschermingsprofiel")) | Lost geen authenticatie op internetschaal of ondernemingsbrede crypto-inventaris op |

## Wat dit betekent per type instelling

### Tier-one universele banken

Tier-one banken hebben een programmakantoor nodig, geen proof of concept. Het doelbedrijfsmodel moet cryptografische inventarisatie, leveranciersafdwinging, HSM-roadmap-management, testomgevingen voor hybride TLS/IPsec en bewijs gereed voor de toezichthouder combineren. Het werk met de hoogste vroege waarde is niet om elke cipher onmiddellijk te wijzigen; het is het opbouwen van het controlevlak dat verandering veilig maakt.

### Middelgrote en regionale banken

Middelgrote banken moeten PQC behandelen als een oefening in leveranciersbeheer en platformstandaardisatie. Zij kunnen dure maatwerk-werk vermijden door systemen te concentreren rond ondersteunde bibliotheken, standaard TLS-stacks, beheerde certificaatdiensten en duidelijke leveranciersdeadlines. Het belangrijkste risico is verborgen cryptografie binnen appliances, betalingsgateways en legacy-middleware.

### Fintechs, PSP's en crypto-aanverwante instellingen

Fintechs kunnen sneller bewegen omdat zij meestal minder legacy-vertrouwensankers hebben. Het risico is zelfgenoegzaamheid in API's van derden, cloud-KMS-standaarden, wallet-infrastructuur en custody-integraties. Crypto-aanverwante firma's moeten er bijzonder voor waken om blockchain-eigen beveiligingsverhalen niet te verwarren met post-kwantum-paraatheid.

### Engineers en beveiligingsarchitecten

De engineering-discipline is concreet: voeg algoritme-metadata toe aan service-inventarissen, log onderhandelde protocolmodi, creëer veilige feature flags voor hybride tests, verkort certificaatlevensduren waar mogelijk, verwijder hardcoded algoritme-aannames en maak crypto-policy uitrolbaar via configuratie in plaats van code-forks.

## Conclusie

De reset van kwantumcryptografie is geen eenmalige technologieaankoop. Het is een cryptografisch operationeel model. NIST heeft de industrie een standaarden-basislijn gegeven, het NCSC heeft de praktische leidraad versmald, protocolorganen bewegen nog, en QKD-assurance wordt formeler. De bankinstellingen die deze overgang winnen, zijn niet diegene die de grootste pilot aankondigen. Het zijn de instellingen die weten waar hun cryptografie leeft, weten welke data eerst bescherming nodig heeft en cryptografische primitieven kunnen veranderen zonder de bank te herbouwen.

## Veelgestelde vragen

**Is post-kwantumcryptografie klaar voor gebruik door banken?**

Zij is klaar voor planning, leveranciersbetrokkenheid, pilots en geselecteerd implementatiewerk. NIST stelt dat drie standaarden klaar zijn om te worden geïmplementeerd, terwijl het NCSC waarschuwt dat operationeel gebruik moet leunen op robuuste implementaties van definitieve standaarden en stabiele protocollen ([NIST](https://www.nist.gov/pqc "NIST Post-Quantum Cryptography"), [NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "Volgende stappen ter voorbereiding op PQC")).

**Maakt QKD de noodzaak van PQC overbodig?**

Nee. QKD kan nuttig zijn voor gespecialiseerde gecontroleerde verbindingen, maar PQC is het schaalbare migratiepad voor algemene software, internetprotocollen, API's, certificaten en ondernemingssystemen. QKD hangt ook af van assurance- en certificeringskaders voordat het als infrastructuur op bankniveau kan worden behandeld ([ID Quantique / ETSI QKD 016](https://www.idquantique.com/etsi-releases-qkd-protection-profile/ "ETSI publiceert QKD-beschermingsprofiel")).

**Wat moet als eerste worden gemigreerd?**

Systemen die langlevende gevoelige data beschermen, moeten worden geprioriteerd. Dat omvat archiefversleuteling, betalingsonderzoeken, treasury- en kapitaalmarktdocumenten, private-banking-identiteitsdossiers, strategische dealbestanden, root-certificaatautoriteiten, firmware-ondertekening en interbancaire kanalen.

**Wat is de grootste implementatieval?**

De grootste val is om PQC te behandelen als een algoritmewissel. De migratie raakt protocollen, certificaten, HSM's, leveranciers, prestatie-testen, incident response, monitoring en governance. Zonder crypto-agility creëert de instelling eenvoudigweg hetzelfde migratieprobleem opnieuw voor de volgende algoritmewijziging.

## Referenties

- NIST, (2025). [Post-kwantumcryptografie ⧉](https://www.nist.gov/pqc "Post-quantum cryptography").
- NCSC, (2024). [Volgende stappen ter voorbereiding op post-kwantumcryptografie ⧉](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "NCSC PQC guidance").
- NIST CSRC, (2026). [The NIST Post-Quantum Cryptography Project ⧉](https://csrc.nist.gov/presentations/2026/mpts2026-3b1 "The NIST PQC Project").
- ID Quantique, (2024). [ETSI publiceert 's werelds eerste beschermingsprofiel voor QKD ⧉](https://www.idquantique.com/etsi-releases-qkd-protection-profile/ "ETSI QKD 016").
<!-- enrich-start -->
<aside class="author-card" aria-label="Over de auteur"><img alt="Portret van Sebastien Rousseau" src="https://cloudcdn.pro/stocks/images/sebastien-rousseau.png" width="64" height="64" loading="lazy" decoding="async" /><span class="author-card-body"><strong class="author-card-name"><a href="/about/index.html">Sebastien Rousseau</a></strong><span class="author-card-bio">Senior banking technologist, schrijft over toegepaste AI, ISO 20022-migratie, post-kwantumcryptografie voor financiële dienstverlening en de structurele transformatie van wholesale betalingen.</span><span class="author-credentials">Meer dan 20 jaar bij HSBC Commercial &amp; Investment Bank, PayPal, Barclays, Shazam, AKQA, Virgin Group. <a href="/about/index.html">Volledig profiel</a> &middot; <a href="https://www.linkedin.com/in/sebastienrousseau/" rel="external noopener">LinkedIn</a> &middot; <a href="https://github.com/sebastienrousseau" rel="external noopener">GitHub</a></span></span></aside>
<p class="post-reviewed">Laatst beoordeeld <time datetime="2026-05-18">2026-05-18</time>.</p>
<!-- enrich-end -->
