---
title: "Kvanttrösklarna rörs igen"
subtitle: "En ny artikel antyder att Shors algoritm skulle kunna köras på så få som 10 000 qubitar. Tröskeln för kryptografiskt relevant kvantberäkning sjunker snabbare än de flesta antagit."
description: "En ny artikel antyder att Shors algoritm skulle kunna köras på så få som 10 000 qubitar. Tröskeln för kryptografiskt relevant kvantberäkning sjunker snabbare än de flesta antagit."
date: "April 11, 2026"
language: "sv-SE"
locale: "sv_SE"
banner: "https://cloudcdn.pro/stocks/images/leo_visions-Q_y8ZzhQ2_s-unsplash.webp"
banner_alt: "Diagram över qubittröskeln för Shors algoritm. Kretskort för kvantberäkning med blå ljusmönster"
keywords: "kvantberäkning, Shors algoritm, 10000 qubitar, postkvantkryptografi, RSA-2048, elliptisk kurvkryptografi, neutralatomqubitar, kvantfelrättning, kryptografisk agilitet, kvanthotets tidslinje"
---

## Kvanttrösklarna rörs igen

En ny artikel antyder att Shors algoritm skulle kunna köras på så få som 10 000 qubitar. Tröskeln för kryptografiskt relevant kvantberäkning sjunker snabbare än de flesta antagit.

> **Viktiga slutsatser**
>
> - En ny artikel föreslår att Shors algoritm skulle kunna köras på så få som **10 000 fysiska qubitar**. Ungefär hundra gånger färre än tidigare konsensusuppskattningar.
> - Minskningen drivs av tre sammanfallande framsteg: kvantfelrättande koder med hög hastighet, omkonfigurerbara matriser av neutrala atomer och ökad parallellism.
> - Hotet är inte enhetligt. **Elliptisk kurvkryptografi (ECC)** är mer sårbar vid lägre antal qubitar; RSA-2048 kräver betydligt längre körtider vid jämförbara skalor.
> - Detta är en **teoretisk projektion**, inte en fungerande demonstration. Ett betydande ingenjörsmässigt gap kvarstår mellan dagens hårdvara och feltolerant drift i denna skala.
> - Standarderna för postkvantkryptografi är redan färdigställda. Prioriteten nu är att **påskynda migreringen**. Inte att vänta på att ett kvantsystem ska dyka upp.

## Ett välbekant antagande, nu under press

Under det senaste decenniet har diskussionerna om kvantberäkning och kryptografi följt en välbekant båge. Kvantmaskiner erkändes som teoretiskt kraftfulla, men betraktades som opraktiska i stor skala. Att knäcka moderna kryptografiska system skulle kräva miljontals fysiska qubitar, och tidslinjen förblev bekvämt avlägsen. Det antagandet är nu under allvarlig press.

En färsk artikel, [Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits ⧉](https://arxiv.org/pdf/2603.28627 "Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits (PDF)"), föreslår något mer betydelsefullt än ett enskilt genombrott. Den antyder att tröskeln för kryptografiskt relevant kvantberäkning kan vara en storleksordning lägre än man tidigare trott. Inte miljontals qubitar, utan tiotusentals. Distinktionen har betydelse, och den riktning den antyder är svår att ignorera.

## Konvergensen som driver skiftet: felrättning, arkitektur och parallellism

Resultatet uppstår inte ur en enda upptäckt. Det speglar en konvergens av förbättringar i flera lager av kvantberäkningsstacken som, tagna tillsammans, förskjuter gränsen för vad som framstår som genomförbart.

Den första förbättringen gäller felrättning. Traditionella metoder krävde stora omkostnader, ofta hundratals fysiska qubitar för att representera en enda logisk qubit. Artikeln bygger i stället på kvantfelrättande koder med hög hastighet, vilka avsevärt minskar den omkostnaden. ([Emergent Mind ⧉](https://www.emergentmind.com/papers/2603.28627 "Shor's Algorithm with 10000 Atomic Qubits")) Den andra gäller arkitektur. Systemet är byggt på omkonfigurerbara matriser av neutrala atomer, som kan omorganiseras under beräkningen för att möjliggöra mer flexibel konnektivitet och effektivare exekvering. ([The Quantum Insider ⧉](https://thequantuminsider.com/2026/03/31/oratomic-launches-to-build-utility-scale-quantum-computers/ "Oratomic Launches to Build Utility-scale Quantum Computers")) Den tredje är parallellism: att öka antalet qubitar gör det möjligt att köra fler operationer samtidigt, vilket minskar den totala exekveringstiden.

Ingen av dessa idéer är ny för sig. Kombinerade omformar de dock det som tidigare behandlades som en hård gräns.

## Från miljoner till tiotusentals: vad siffrorna faktiskt betyder

Under åratal krävde konsensusuppskattningen för att köra Shors algoritm i kryptografiska skalor miljontals fysiska qubitar. Den nya analysen antyder att detta antal, under vissa antaganden, skulle kunna sjunka till ungefär 10 000. ([arXiv ⧉](https://arxiv.org/abs/2603.28627 "Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits")) Den siffran ger dock inte hela bilden.

I den nedre delen av det intervallet förblir körtiderna långa. Att faktorisera RSA-2048 vid minimala antal qubitar skulle fortfarande kunna ta år av kontinuerlig drift. Snabbare exekvering kräver fler qubitar, potentiellt tiotusentals. Förhållandet mellan antalet qubitar och körtiden är inte linjärt, och artikeln är noga med att presentera detta som ett spektrum snarare än en fast tröskel. Det som förändras är riktningen: barriären är inte längre rent teoretisk. Det är nu en fråga om ingenjörskonst.

### Gamla antaganden mot nya realiteter

| Dimension | Gammalt antagande | Ny verklighet |
|---|---|---|
| Fysiska qubitar som krävs (Shors algoritm) | ~1 000 000+ | ~10 000–26 000 |
| Tid att knäcka RSA-2048 (vid minimum av qubitar) | Inte genomförbart detta decennium | År (vid 10 000 qubitar); snabbare med fler |
| Tid att knäcka ECC-256 | Inte genomförbart detta decennium | Dagar (uppskattat vid ~26 000 qubitar) |
| Dominerande hårdvaruparadigm | Supraledande qubitar | Omkonfigurerbara matriser av neutrala atomer |
| Omkostnad för felrättning | Hundratals fysiska qubitar per logisk qubit | Avsevärt minskad via koder med hög hastighet |
| Barriärens natur | Teoretisk | Ingenjörsmässig |
| Migreringens brådska | Långsiktig planering | Aktiv utrullning krävs nu |

*Källa: analys baserad på [arXiv:2603.28627 ⧉](https://arxiv.org/abs/2603.28627) och tidigare litteratur.*

## Tid, skala och den ojämna sårbarheten hos kryptografiska system

Ett av artikelns mer betydande bidrag är den nyans den introducerar kring tid. Kvantfördelen anländer inte på en gång. Den existerar längs ett spektrum som bestäms av systemets skala och det kryptografiska målets natur.

Med ungefär 26 000 qubitar uppskattar författarna att det skulle kunna ta dagar att knäcka elliptisk kurvkryptografi under gynnsamma förhållanden. ([arXiv ⧉](https://arxiv.org/abs/2603.28627 "Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits")) För RSA-2048 är tidslinjerna avsevärt längre. Denna asymmetri är viktig. Den antyder att olika kryptografiska system kan bli sårbara vid olika tidpunkter, snarare än samtidigt, och att övergången till postkvantstandarder sannolikt inte blir en enskild händelse med en enda tidsfrist.

Detta mönster är förenligt med bredare rapportering. Analyser från de senaste månaderna antyder att kvantsystem som kan utmana allmänt använd kryptering skulle kunna dyka upp före decenniets slut. ([Nature ⧉](https://www.nature.com/articles/d41586-026-01054-1 "Quantum-computing breakthroughs pose risks to encryption")) Regeringar och standardiseringsorgan planerar redan övergångar till postkvantkryptografi, med implementeringstidslinjer som sträcker sig in på 2030-talet. ([The Quantum Insider ⧉](https://thequantuminsider.com/2026/03/31/oratomic-launches-to-build-utility-scale-quantum-computers/ "Oratomic Launches to Build Utility-scale Quantum Computers")) Diskussionen har flyttat från om till när.

## Det ingenjörsmässiga gap som kvarstår

Det är viktigt att vara precis om vad denna artikel representerar. Den är en projektion, inte en demonstration. De föreslagna systemen är beroende av antaganden om felfrekvenser, hårdvarustabilitet och skalningsbeteende som ännu inte har validerats i den skala som krävs. Nuvarande experiment opererar på nivån hundratals till några tusen qubitar, inte tiotusentals som fungerar feltolerant under längre perioder. ([Phys.org ⧉](https://phys.org/news/2026-04-quantum-built-qubits-team.html "Useful quantum computers could be built with as few as 10,000 qubits"))

Ett betydande ingenjörsmässigt gap kvarstår. Vägen från en övertygande teoretisk modell till ett fungerande system som klarar ihållande, feltolerant drift i denna skala inbegriper utmaningar som ännu inte är fullt förstådda, än mindre lösta. Det som har förändrats är inte närheten till en fungerande maskin, utan målets trovärdighet. Gapet krymper, och framstegens riktning är konsekvent.

## Varför den krympande tidslinjen kräver uppmärksamhet nu

Betydelsen av detta arbete är inte att kryptografin kommer att knäckas på kort sikt. Det är att tidslinjen krymper på sätt som påverkar beslut som fattas i dag. Säkerhetssystem utformas med långa livscykler i åtanke. Data som krypteras nu kan behöva förbli konfidentiella i decennier. Infrastrukturbeslut som fattas i år blir svåra att återställa inom ett fönster på fem år. Om kvantförmågor anländer tidigare än väntat blir dessa antaganden bräckliga.

Det är därför postkvantkryptografi redan rullas ut inom kritiska sektorer. Inte för att hotet är omedelbart, utan för att övergången tar tid och kostnaden för att vara sen är asymmetrisk. Det finns ett återkommande mönster i databehandlingens historia: framsteg framstår som långsamma tills de plötsligt inte är det. Det som börjar som en teoretisk förbättring blir en praktisk begränsning, och det som en gång avfärdades som avlägset blir något som måste planeras för. Kvantberäkning kan följa exakt den banan, inte genom ett enskilt dramatiskt genombrott, utan genom stadiga minskningar av kostnad, komplexitet och skala.

## Vad detta betyder per bransch: en praktisk vägledning

Konsekvenserna av denna forskning är inte enhetliga över sektorerna. Rätt svar beror på vilken typ av kryptografiska tillgångar som är i riskzonen, på hur känsliga och långlivade de berörda uppgifterna är, och på i vilken takt de regulatoriska förväntningarna rör sig.

### Finansiella tjänster och FinTech

Finansiella institutioner står inför en sammansatt risk: de innehar långlivade känsliga data, opererar på infrastruktur med långsamma utbytescykler och är föremål för ökande regulatorisk granskning kring kryptografisk motståndskraft. ECC används i stor utsträckning i TLS-anslutningar, mobil autentisering och digitala signaturer över betalningsräls. Den kryptografiska kategori som artikeln identifierar som mest sårbar vid lägre antal qubitar. Institutioner som ännu inte har påbörjat en kryptografisk inventering eller inlett en färdplan för postkvantmigration bör behandla denna artikel som en anledning att påskynda, inte en anledning till panik. [CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html) och CRYSTALS-Dilithium, båda nu standardiserade av NIST, är de lämpliga migrationsmålen för nyckelinkapsling respektive digitala signaturer.

### Offentlig sektor och försvar

Statliga aktörer har den starkaste motivationen. Och i många fall resurserna. Att påskynda utvecklingen av kvanthårdvara bortom vad som är offentligt känt. Regeringar som förvaltar känslig kommunikation, underrättelsedata eller nycklar till kritisk infrastruktur måste anta att motståndare redan skördar krypterade data för framtida dekryptering, en strategi som vanligen kallas ”harvest now, decrypt later”. För organisationer i offentlig sektor blir efterlevnad av nationella mandat för kvantberedskap alltmer oundviklig, och fönstret för proaktiv migration krymper.

### Hälso- och sjukvård samt kritisk infrastruktur

Patientjournaler, styrsystem för samhällstjänster och industriella nätverk delar en gemensam sårbarhet: data och system med mycket lång driftslivslängd, skyddade av kryptografiska standarder som utformades för en förkvantmässig hotmodell. En patientjournal som krypteras i dag kan behöva förbli privat i femtio år. Ett styrsystem som certifieras i år kan förbli i drift i två decennier. För dessa sektorer är den krympande tidslinjen inte en abstrakt oro. Det är en direkt utmaning mot de grundläggande antagandena bakom dagens säkerhetsarkitekturer.

## Slutsats

Den viktigaste aspekten av denna artikel är inte det specifika antal qubitar den presenterar. Det är den riktning som antalet antyder. Frågan är inte längre om kvantdatorer kan utmana modern kryptografi. Det är hur snabbt de nödvändiga systemen kan byggas, och om de organisationer som är beroende av dagens standarder rör sig tillräckligt snabbt som svar.

Tills vidare förblir svaren osäkra. Men marginalen för att skjuta upp frågan krymper, och kostnaden för att vänta växer med varje trovärdig sänkning av den teoretiska tröskeln. Det kryptografiska samfundet, säkerhetsplanerare och de branscher som förlitar sig på dem gör klokt i att behandla denna artikel inte som skäl till larm, utan som en allvarlig anledning att påskynda övergångar som redan pågår.

## Vanliga frågor

**Kan 10 000 qubitar verkligen knäcka RSA-kryptering?**

Teoretiskt, ja. Men med viktiga förbehåll. Medan tidigare uppskattningar antydde att miljontals fysiska qubitar krävdes, antyder ny forskning om felrättande koder med hög hastighet och omkonfigurerbara matriser av neutrala atomer att tröskeln är betydligt lägre. Vid 10 000 qubitar förblir dock den uppskattade körtiden för att faktorisera RSA-2048 extremt lång. Potentiellt år av kontinuerlig drift. Snabbare attacker kräver fler qubitar, sannolikt i intervallet tiotusentals. Artikeln utgör en projektion baserad på modellerade antaganden, inte en demonstration på ett fungerande system.

**Vilken kryptering löper störst risk från kvantberäkning?**

Elliptisk kurvkryptografi (ECC) är generellt mer sårbar för lägre antal qubitar än RSA-2048. Artikeln uppskattar att det skulle kunna ta dagar att knäcka ECC med ungefär 26 000 omkonfigurerbara qubitar under gynnsamma förhållanden. RSA-2048 kräver en betydligt längre körtid vid jämförbara antal qubitar. Denna asymmetri innebär att ECC-beroende system. Vanliga i TLS, mobil autentisering och blockkedja. Kan möta risk på en kortare tidslinje än RSA-baserad infrastruktur.

**Vad är en omkonfigurerbar neutralatomqubit?**

Neutralatomqubitar är enskilda atomer. Vanligtvis rubidium eller cesium. Fångade och manipulerade med laserljus i en vakuumkammare. ”Omkonfigurerbar” betyder att atomernas arrangemang kan ändras dynamiskt under beräkningen, vilket möjliggör effektivare exekvering av komplexa kvantkretsar. Denna flexibilitet minskar antalet fysiska qubitar som behövs för att implementera feltoleranta logiska operationer, och är ett viktigt skäl till att den nya artikeln uppnår lägre qubituppskattningar än tidigare arbete baserat på supraledande qubitarkitekturer.

**Vad är postkvantkryptografi och varför rullas den ut nu?**

Postkvantkryptografi (PQC) avser kryptografiska algoritmer som tros vara säkra mot både klassiska datorer och kvantdatorer. NIST färdigställde sin första uppsättning PQC-standarder 2024, inklusive [CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html) för nyckelinkapsling och CRYSTALS-Dilithium för digitala signaturer. Utrullningen börjar nu. Långt innan kvantdatorer utgör ett omedelbart hot. Eftersom kryptografiska övergångar är långsamma. Att ersätta inbäddade standarder över global infrastruktur tar vanligtvis ett decennium eller mer, och data som krypteras i dag kan behöva förbli konfidentiella långt efter att kvantförmågorna mognat.

**Hur många qubitar har den mest kraftfulla kvantdatorn i dag?**

I början av 2026 opererar ledande kvantsystem i intervallet hundratals till några tusen fysiska qubitar. Avgörande är att de flesta ännu inte är feltoleranta. De opererar under de trösklar för felrättning som krävs för ihållande, tillförlitlig logisk beräkning. Gapet mellan dagens hårdvara och de tiotusentals logiska qubitar med hög trohet och feltolerans som beskrivs i den nya artikeln förblir betydande, även om framstegstakten över supraledande plattformar, neutralatomplattformar och plattformar med fångade joner accelererar.

## Referenser

- Sebastien Rousseau, (2025). [Quantum-Safe Payments: Why the Payments Industry Must Act Now](https://sebastienrousseau.com/2025-09-01-quantum-safe-payments-epaa/index.html "Quantum-Safe Payments: Why the Payments Industry Must Act Now").
- Sebastien Rousseau, (2023). [Quantum Key Distribution: Revolutionising Security in Banking](https://sebastienrousseau.com/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html "Quantum Key Distribution: Revolutionising Security in Banking").
- Sebastien Rousseau, (2023). [CRYSTALS-Kyber: The Safeguarding Algorithm in a Quantum Age](https://sebastienrousseau.com/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html "CRYSTALS-Kyber: The Safeguarding Algorithm in a Quantum Age").
- Anonymous, (2026). [Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits ⧉](https://arxiv.org/abs/2603.28627 "Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits"). arXiv preprint arXiv:2603.28627.
- Castelvecchi, D. (2026). [Quantum-computing breakthroughs pose risks to encryption ⧉](https://www.nature.com/articles/d41586-026-01054-1 "Quantum-computing breakthroughs pose risks to encryption"). Nature.
- Phys.org, (2026). [Useful quantum computers could be built with as few as 10,000 qubits ⧉](https://phys.org/news/2026-04-quantum-built-qubits-team.html "Useful quantum computers could be built with as few as 10,000 qubits"). Phys.org.
