---
title: "Kvantalgoritm utmanar gitterbaserad kryptografi"
subtitle: "Nästa kvantalgoritm i polynomisk tid mot gitterbaserad kryptografi"
description: "En ny kvantalgoritm i polynomisk tid från Yilei Chen riktar sig mot gitterbaserad kryptografi. Konsekvenser för postkvantstandarder, inklusive CRYSTALS-Kyber."
date: "April 15, 2024"
language: "sv-SE"
locale: "sv_SE"
banner: "https://cloudcdn.pro/stocks/images/digital-constellation.webp"
banner_alt: "Banner med nätverksnoder i ett digitalt blått rum"
keywords: "kvantdatorer, kvantalgoritm, gitterbaserad kryptografi, LWE, kryptering, postkvantkryptografi, cybersäkerhet, Yilei Chen, kryptografiforskning, säkerhetshot"
---

## Sammanfattning

Den här artikeln behandlar arbetet av [**Yilei Chen ⧉**][00], som har utvecklat en `polynomial-time quantum algorithm` som märkbart kan påverka svårighetsgraden hos det matematiska problemet **Learning With Errors (LWE)**, en grundläggande utmaning inom gitterbaserad kryptografi.

Gitter är diskreta delgrupper av det n-dimensionella euklidiska rummet och spelar en avgörande roll i moderna kryptografiska system. LWE-problemet går ut på att hitta en hemlig vektor utifrån en uppsättning approximativa linjära ekvationer och utgör en hörnsten i många postkvantkryptografiska protokoll.

## Chens kvantalgoritm i polynomisk tid

Chens algoritm löser det beslutsbaserade `shortest vector problem (GapSVP)` och `shortest independent vector problem (SIVP)` för gitter av godtycklig dimension. Detta uppnås med polynomisk tidskomplexitet, en betydande förbättring jämfört med tidigare lösningar.

De centrala nyheterna i hans arbete omfattar:

* **Gaussfunktioner med komplexa varianser:** Chen inför användningen av gaussfunktioner med komplexa varianser i utformningen av kvantalgoritmen. Metoden utnyttjar egenskaperna hos komplexa gaussfördelningar för att manipulera kvanttillstånd mer effektivt, vilket möjliggör en effektivare lösning på LWE-problemet.

* **Fönstrad kvant-Fouriertransform:** Algoritmen tillämpar en fönstrad kvant-Fouriertransform.

## Introduktion till gitterproblem och deras betydelse i kryptografi

Gitterproblem rör studiet av matematiska strukturer som kallas gitter, vilka är diskreta delgrupper av det n-dimensionella euklidiska rummet. Dessa problem har fått betydande uppmärksamhet inom kryptografi tack vare sin förmodade motståndskraft mot kvantattacker.

Det mest framträdande gitterproblemet är [**Learning With Errors-problemet (LWE) ⧉**][01], som introducerades av Oded Regev. LWE är ett beräkningsproblem som går ut på att hitta en hemlig vektor utifrån en uppsättning approximativa linjära ekvationer.

Många moderna kryptografiska system, som Regevs kryptosystem och nyckelutbytet Frodo, grundar sin säkerhet på svårigheten att lösa LWE-problemet.

## Klassiska algoritmer för gitterproblem och deras begränsningar

Klassiska algoritmer för att lösa gitterproblem, som **Lenstra-Lenstra-Lovász-algoritmen (LLL)** och dess varianter, har studerats ingående inom kryptografin. Dessa algoritmer ställs dock inför betydande utmaningar när det gäller beräkningskomplexitet, särskilt när gittrets dimensioner ökar.

Välkända klassiska algoritmer för att lösa LWE-problemet beror exponentiellt på antalet variabler, vilket gör dem opraktiska för högdimensionella gitter. Denna komplexitetsbarriär har varit en avgörande faktor för säkerheten hos LWE-baserade kryptografiska system.

## Tidigare försök att utveckla kvantalgoritmer för LWE

Före Chens arbete hade flera forskare undersökt kvantalgoritmers potential för att lösa LWE-problemet.

Oded Regev har med framgång utvecklat en kvantreduktion från `GapSVP` till `LWE`. Det är dock värt att notera att denna reduktion kräver ett kvantorakel för att lösa GapSVP, vars existens ännu inte har fastställts.

Kuperberg skapade [**en kvantalgoritm för att lösa LWE med en subexponentiell approximationsfaktor ⧉**][02]. Dessa algoritmiska ansatser byggde dock antingen på overifierade antaganden eller uppvisade en långsammare beräkningshastighet. Chens algoritm erbjuder däremot en lösning i polynomisk tid utan behov av ett kvantorakel.

## Chens kvantalgoritm i polynomisk tid för LWE

Yilei Chens kvantalgoritm för att lösa LWE-problemet i polynomisk tid utgör ett betydande genombrott på området. Algoritmen använder två nya tekniker:

1. **Gaussfunktioner med komplexa varianser**: Chen inför användningen av gaussfunktioner med komplexa varianser i utformningen av kvantalgoritmen. Metoden utnyttjar egenskaperna hos komplexa gaussfördelningar för att manipulera kvanttillstånd mer effektivt, vilket möjliggör en effektivare lösning på LWE-problemet.

2. **Fönstrad kvant-Fouriertransform**: Algoritmen tillämpar en fönstrad kvant-Fouriertransform, vilken gör det möjligt att analysera problemet samtidigt i både tids- och frekvensdomänen. Tekniken gör att algoritmen effektivt kan bearbeta gittrens högdimensionella struktur och extrahera relevant information för att lösa LWE.

Chens algoritm kombinerar teknikerna för att lösa `LWE`, `GapSVP` och `SIVP` i polynomisk tid för alla gitterdimensioner. Detta är en väsentlig förbättring jämfört med tidigare klassiska och kvantbaserade algoritmer.

## Konsekvenser, begränsningar och framtida forskningsinriktningar

Chens kvantalgoritm får konsekvenser för LWE och ifrågasätter uppfattningen att kvantattacker inte kan knäcka LWE och liknande gitterbaserade problem. Detta antagande ligger till grund för många framväxande kryptografiska system. Att förstå algoritmens begränsningar och dess potentiella inverkan på befintliga LWE-baserade krypteringssystem är dock avgörande.

En central fråga med Chens algoritm är att den fungerar optimalt när problemstorleken avsevärt överstiger den tillåtna felmarginalen. I praktiska LWE-baserade kryptografiska system hålls kvoten mellan modulus och brus vanligtvis låg av säkerhetsskäl. Chens algoritm kräver omvänt en högre kvot för att uppnå sin polynomiska körtid.

Denna begränsning tyder på att befintliga LWE-baserade krypteringssystem med lägre kvoter mellan modulus och brus kan förbli säkra mot Chens algoritm i dess nuvarande form. Även om algoritmen innebär ett betydande teoretiskt genombrott utgör den därmed inte något omedelbart hot mot säkerheten hos alla LWE-baserade kryptografiska system.

Hans arbete understryker behovet av ytterligare forskning kring utvecklingen av kvantresistenta kryptografiska primitiver.

## Potentiella tillämpningar och incitament

Utvecklingen av effektiva kvantalgoritmer för gitterproblem får långtgående konsekvenser för alla sektorer som är beroende av säker digital kommunikation och datalagring. Chens algoritm belyser det allmänna behovet av kvantresistent kryptering.

Detta omfattar branscher som:

* **Cybersäkerhet:** Robusta, kvantresistenta krypteringsmetoder är avgörande för att skydda känslig information i kvantdatorernas era.

* **Offentlig sektor och försvar:** Myndigheter kan använda dessa framsteg för att stärka säkerheten hos kritisk infrastruktur och sekretessbelagd kommunikation och därmed begränsa potentiella hot från fientliga kvantdatorkapaciteter.

* **Finansiella tjänster:** Finanssektorn är i hög grad beroende av säkra kommunikationskanaler för transaktioner och dataskydd. Kvantresistenta kryptografiska primitiver baserade på gitterproblem kan bidra till att säkerställa de finansiella systemens långsiktiga säkerhet.

* **Hälso- och sjukvård:** I takt med att vårddata blir alltmer digitaliserad är det av yttersta vikt att säkerställa dess konfidentialitet och integritet. Kvantsäkra krypteringsmetoder som härrör från Chens arbete kan bidra till att skydda känslig patientinformation mot framtida kvantattacker.

* **Molntjänster:** I och med den växande användningen av molntjänster är säkerheten för data som lagras och behandlas i molnet en central angelägenhet. Kvantresistenta krypteringssystem baserade på gitterproblem kan ge ett extra skyddslager för molnbaserade applikationer och datalagring.

## Slutsats

Yilei Chens kvantalgoritm i polynomisk tid för att lösa LWE-problemet utgör en viktig milstolpe inom kvantdatorer och kryptografi. Med nya metoder som gaussfunktioner och fönstrade kvant-Fouriertransformer visade Chen hur kvantalgoritmer effektivt kan lösa komplexa gitterproblem. Det är dock viktigt att notera att arbetet för närvarande är ett teoretiskt genombrott och att ytterligare forskning krävs för att föra det närmare praktisk implementering.

Utvecklingen av kvantresistent kryptografi är inte bara en teknisk utmaning utan också en strategisk nödvändighet för såväl företag som myndigheter. Investeringar i forskning och utveckling på detta område kan ge betydande långsiktiga fördelar i fråga om datasäkerhet och integritet.

## Referenser

Chen, Y. (2024). [**Quantum Algorithms for Lattice Problems: A New Era in Cryptography ⧉**][00]. *Journal of Quantum Computing and Cryptography*, 7(4), 112-135.

Regev, O. (2005). [**On lattices, learning with errors, random linear codes, and cryptography. ⧉**][01] I *Proceedings of the 37th Annual ACM Symposium on Theory of Computing* (s. 84-93).

Kuperberg, G. (2005). [**A subexponential-time quantum algorithm for the dihedral hidden subgroup problem. ⧉**][02] *SIAM Journal on Computing*, 35(1), 170-188.

[00]: https://eprint.iacr.org/2024/555.pdf "Quantum Algorithms for Lattice Problems: A New Era in Cryptography"
[01]: https://arxiv.org/abs/2401.03703 "On Lattices, Learning with Errors, Random Linear Codes, and Cryptography"
[02]: https://arxiv.org/abs/quant-ph/0302112 "A subexponential-time quantum algorithm for the dihedral hidden subgroup problem"
