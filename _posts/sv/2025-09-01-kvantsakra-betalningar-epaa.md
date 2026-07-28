---
title: "Kvantsäkra betalningar: varför branschen måste agera nu"
subtitle: "Kvantsäker beredskap är ett beslut om infrastruktur i dag. Inte i framtiden."
description: "Kvantdatorer hotar kryptografin i betalningssystemen. EPAA:s vitbok redogör för den strukturella risken och det brådskande behovet av migrering till PQC."
date: "September 01, 2025"
language: "sv-SE"
locale: "sv_SE"
banner: "https://cloudcdn.pro/stocks/images/digital-nodes.webp"
banner_alt: "Kretskort för kvantdatorer i blått ljus"
keywords: "kvantsäkra betalningar, postkvantkryptografi, SEPA, SWIFT gpi, ISO 20022, säkerhet inom finansiella tjänster, EPAA, harvest-now decrypt-later, kryptografisk agilitet, Sebastien Rousseau"
---

## Kvanthotet mot betalningssystemen

Modern betalningsinfrastruktur bygger på kryptografi med öppen nyckel, som RSA, ECC och Diffie-Hellman, för att autentisera transaktioner, skydda kortinnehavarnas data och säkra meddelanden mellan finansinstitut. Dessa algoritmer ligger till grund för SWIFT, SEPA, system för bruttoavveckling i realtid och i praktiken varje kortsystem som är i drift i dag.

Kvantdatorer som kör Shors algoritm kommer att kunna bryta dessa kryptografiska primitiver. Feltoleranta kvantmaskiner finns ännu inte i den skala som krävs, men utvecklingen av hårdvaran, som IBM, Google och andra har demonstrerat, gör detta till en fråga om ingenjörsmässig tidsplan snarare än teori. National Institute of Standards and Technology (NIST) har redan färdigställt sin första uppsättning postkvantkryptografiska standarder (FIPS 203, 204 och 205) som svar.

## Risken med harvest-now decrypt-later

Hotet är inte begränsat till ett framtida datum då kvantdatorer når tillräcklig kapacitet. Statliga aktörer och avancerade motståndare avlyssnar och lagrar redan i dag krypterade data i avsikt att dekryptera dem när kvantresurser blir tillgängliga. Denna strategi, harvest-now decrypt-later (HNDL), innebär att alla betalningsdata med långvarig känslighet, som regulatoriska register, arkiv för regelefterlevnad och avtalsförpliktelser, redan är utsatta för risk.

Finansiella tillsynsmyndigheter har börjat reagera. Monetary Authority of Singapore (MAS) har utfärdat vägledning om kvantberedskap. Australian Prudential Regulation Authority (APRA) har lyft fram kryptografisk risk i sitt ramverk för teknisk motståndskraft. Europeiska unionens Digital Operational Resilience Act (DORA) kräver en hantering av IKT-risker som måste ta hänsyn till framväxande hot, inklusive kvantdatorer.

## Konsekvenser för betalningskanalerna

Konsekvenserna omfattar hela bredden av betalningsinfrastrukturen:

**SWIFT-meddelanden:** Meddelandeformaten MT och MX förlitar sig på TLS och digitala signaturer för integritet och autentisering. En komprometterad nyckelinfrastruktur skulle undergräva den förtroendemodell som binder samman över 11 000 institut globalt.

**SEPA och omedelbara betalningar:** European Payments Councils system SEPA Instant Credit Transfer behandlar oåterkalleliga transaktioner på under tio sekunder. En kryptografisk kompromettering i denna hastighet lämnar inget utrymme för mänsklig inblandning eller manuell verifiering.

**Betalningssystem i realtid:** Faster Payments (UK), FedNow (US) och NPP (Australien) delar alla samma beroende av klassiska kryptografiska primitiver för meddelandeautentisering och verifiering av deltagare.

**Regelefterlevnad och långlivade data:** Betalningsregister som bevaras av regulatoriska skäl, ofta ett krav under fem till tio år eller längre, kommer att överleva säkerhetsgarantierna hos den kryptografi som skyddade dem när de skapades. Migreringsprogram för [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) måste beakta den kryptografiska hållbarhetstiden för de data de producerar.

**Blockkedjeteknik och distribuerad liggare:** Plattformar för digitala tillgångar och tokeniserade betalningsinstrument som är beroende av kryptografi baserad på elliptiska kurvor möter ett direkt och väldokumenterat hot från kvantalgoritmer.

## Vad organisationer måste göra nu

Övergången till kvantsäker kryptografi är inte en enskild uppgradering utan ett flerårigt program som kräver strukturerade förberedelser:

**Kryptografisk inventering:** Organisationer måste katalogisera varje system, protokoll och datalager som är beroende av klassisk kryptografi med öppen nyckel. Detta omfattar TLS-certifikat, API-autentisering, HSM-konfigurationer, system för nyckelhantering och kryptering av vilande data.

**Införande av postkvantalgoritmer:** NIST har standardiserat ML-KEM (FIPS 203) för nyckelinkapsling och ML-DSA (FIPS 204) för digitala signaturer. Organisationer bör börja testa dessa algoritmer i miljöer utanför produktion och ta fram migreringsplaner för kritiska system.

**Kryptografisk agilitet:** System måste utformas, eller omstruktureras, så att kryptografiska algoritmer kan bytas ut utan att hela applikationen behöver konstrueras om. Denna princip gäller lika mycket för betalningsgateways, meddelandemellanprogram och kundvända API:er.

**Hybridansatser:** Under övergångsperioden ger hybrida kryptografiska scheman som kombinerar klassiska och postkvantalgoritmer ett djupförsvar. Denna ansats bevarar bakåtkompatibiliteten samtidigt som den inför kvantmotståndskraft.

## EPAA:s arbetsgrupp och branschsamarbete

Emerging Payments Association Asia (EPAA) inrättade sin arbetsgrupp Quantum Safe Cryptography för att möta dessa utmaningar genom samordnade branschinsatser. Arbetsgruppen samlar deltagare från hela betalningsekosystemet, däribland IBM, HSBC, KPMG, JPMorgan Chase och PayPal.

Genom workshoppar i Sydney, Hongkong och Singapore har arbetsgruppen tagit fram ett gemensamt ramverk för att bedöma kvantrisk i betalningssystem och identifiera praktiska migreringsvägar. Den resulterande vitboken, [Quantum-Safe Payments: Why the Payments Industry Must Act Now][epaa], utgör en samsyn om utmaningens angelägenhetsgrad och omfattning.

Arbetsgruppens analys drar slutsatsen att kvantsäker beredskap är ett beslut om infrastruktur i dag, inte i framtiden. Organisationer som dröjer riskerar att inte kunna leva upp till regulatoriska förväntningar, skydda långlivade data eller bibehålla interoperabilitet med partner som redan har migrerat.

## Om författaren

Sebastien Rousseau är Senior Digital Product Manager på HSBC Bank plc, där han leder API-produkter för företagsbetalningar inom HSBC:s Commercial & Investment Bank. Han har bidragit till EPAA:s arbetsgrupp Quantum Safe Cryptography och forskar om tillämpningen av postkvantkryptografi inom finansiella tjänster. [Läs mer om Sebastien ❯][00]

## Relaterade artiklar

- [[Kvantnyckeldistribution](/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html): stärker säkerheten inom bankväsendet][rel1]
- [[CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html): skyddsalgoritmen i kvantåldern][rel2]

[00]: /about/index.html "Om Sebastien Rousseau"
[epaa]: https://emergingpaymentsasia.org/wp-content/uploads/2025/09/Quantum-Safe-Payments-Why-the-Payments-Industry-Must-Act-Now.pdf "EPAA:s vitbok om kvantsäkra betalningar"
[rel1]: /2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html "Kvantnyckeldistribution: stärker säkerheten inom bankväsendet"
[rel2]: /2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html "CRYSTALS-Kyber: skyddsalgoritmen i kvantåldern"
