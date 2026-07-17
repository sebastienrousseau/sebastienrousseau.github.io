---
title: "Skapandet av Express Transaction Credits-plattformen"
subtitle: "Utformningen av Express Transaction Credits-plattformen med smarta kontrakt enligt ERC-223."
description: "En teknisk djupdykning i hur EXTC-plattformen byggdes på Ethereum ERC-223 under 2018: tokenarkitektur, multisignaturutbetalningar, tidslåsta överföringar och säkerställda direktlån."
date: "February 15, 2018"
language: "sv-SE"
locale: "sv_SE"
banner: "https://cloudcdn.pro/stocks/images/tarik-haiga-3637943.webp"
banner_alt: "Gigantiska vita pelare"
keywords: "EXTC-plattformen, ERC-223, Ethereum smarta kontrakt, tokenarkitektur, multisignatur, tidslåst överföring, blockchain-betalningar, säkerställda lån, decentraliserad finans, krypto 2018"
---

![Gigantiska vita pelare](https://cloudcdn.pro/stocks/images/tarik-haiga-3637943.webp).class=\"img-fluid clearfix\"

> **Sammanfattning för ledningen / Viktiga slutsatser**
>
> - **Grundproblemet.** ERC-20, den dominerande tokenstandarden på Ethereum 2018, hade en strukturell brist: tokens som överfördes direkt till en smart kontraktsadress förstördes i tysthet om kontraktet saknade en hanterare. Varje betalningsplattform byggd på ERC-20 ärvde den risken ([Ethereum EIPs](https://eips.ethereum.org/EIPS/eip-20 "Tokenstandarden EIP-20")).
> - **ERC-223 som lösning.** ERC-223 krävde att mottagande kontrakt implementerade funktionen `tokenFallback(address, uint, bytes)`. Saknades den återställdes överföringen atomärt. Inga tokens kunde gå förlorade i tysthet ([Ethereum EIPs GitHub](https://github.com/ethereum/EIPs/issues/223 "Förslag till tokenstandarden ERC-223")).
> - **EXTC:s fem kontraktsprimitiver.** Tokenidentitet (namn, symbol, 18 decimalers precision), fast utbud, ERC-223-kompatibel överföring, multisignatur för företagsutbetalningar och stående överföringar tidslåsta med blockhöjd.
> - **Mekanismen för säkerställda lån.** Låntagare låste EXTC-tokens i kontraktets depå; kontraktet frigjorde lånebeloppet atomärt vid mottagandet av säkerheten, utan fördröjande kreditprövning eller godkännande av en kreditkommitté.
> - **Vad experimentet visade om Ethereums gränser.** Vid en genomströmning på huvudnätet om cirka 15 TPS och gaskostnader på $0.10–$1.00 per transaktion vid toppen i januari 2018 var ett betalningsnätverk som hanterade ens remitteringsvolymer ekonomiskt och tekniskt ogenomförbart på publika Ethereum utan Layer-2-infrastruktur.

---

## Designproblemet: varför ERC-20 inte räckte

ERC-20-standarden, föreslagen 2015 och formaliserad i Ethereum Improvement Proposal 20, definierade det kanoniska gränssnittet för fungibla tokens som drev ICO-vågen 2017–2018. Dess sex kärnfunktioner (`totalSupply`, `balanceOf`, `transfer`, `transferFrom`, `approve` och `allowance`) räckte för enkel tokenutgivning och tokenhandel.

För en betalningsplattform hade ERC-20 dock en produktionskritisk brist. Funktionen `transfer(address _to, uint256 _value)` flyttade tokens till vilken adress som helst, inklusive kontraktsadresser, utan att någon kod i det mottagande kontraktet aktiverades. Ett kontrakt som inte uttryckligen programmerats att spåra inkommande ERC-20-överföringar hade inget sätt att upptäcka dem. Tokens som skickades på detta sätt satt fast permanent, utan någon mekanism för återvinning.

Ethereum-gemenskapen uppskattade att ERC-20-tokens till ett värde av tiotals miljoner dollar hade gått permanent förlorade genom denna mekanism vid mitten av 2018. Att bygga en betalningsplattform där överföringar kunde misslyckas i tysthet och förstöra användarnas medel var inte acceptabelt.

## ERC-223-lösningen: atomär överföring med notifiering

ERC-223, föreslagen i Ethereum EIPs ärendehanterare på GitHub, angrep problemet med tysta förluster genom att ändra vad en tokenöverföring var skyldig att göra. Enligt ERC-223 kontrollerade `transfer(address _to, uint256 _value, bytes _data)` om mottagaradressen innehöll kontraktskod. Om så var fallet anropade överföringen `_to.tokenFallback(address _from, uint256 _value, bytes _data)`.

Den avgörande egenskapen: om det mottagande kontraktet inte implementerade `tokenFallback` återställdes hela överföringstransaktionen. Inga tokens lämnade avsändarens saldo. Inga tokens fastnade. Överföringen var atomär: antingen fullbordades den med mottagarens kod exekverad, eller så misslyckades den helt med oförändrat tillstånd.

För EXTC innebar detta:

- **Betalningar till smarta kontrakt var säkra genom konstruktion.** Depåkontrakt, multisignaturplånböcker och lånekontrakt kunde ta emot EXTC-tokens utan risk för att medel oåterkalleligen gick förlorade.
- **Fältet `_data` möjliggjorde rik betalningsmetadata.** Byte-nyttolasten kunde bära fakturareferenser, routingkoder eller efterlevnadsintyg, information som en enkel ERC-20-överföring inte kunde förmedla.
- **Gaskostnaderna var marginellt högre.** Anropet av `tokenFallback` adderade cirka 2 000–5 000 gas per överföring, en mindre overhead vid 2018 års gaspriser.

## EXTC-kontraktets arkitektur

EXTC-tokenkontraktet var en Solidity-implementation strukturerad kring fem moduler:

### 1. Tokenidentitet

```
string public name = "Express Transaction Credits";
string public symbol = "EXTC";
uint8 public decimals = 18;
```

Arton decimaler gav EXTC en precision under centnivå, vilket motsvarade den granularitet som krävdes för mikrobetalningar och mikrolån. Symbolen `EXTC` var den identifierare på kedjan som registrerades i tokenkontraktet.

### 2. Fast totalt utbud

Det totala utbudet fastställdes vid kontraktets driftsättning och kunde inte ökas genom senare myntningar. Detta designval gjorde EXTC deflationärt: tokens som permanent togs ur cirkulation, genom oåterkalleliga bränningsoperationer, minskade utbudet utan ersättning. Modellen med fast utbud var standard i 2018 års betalningstokendesigner och speglade det Bitcoin-influerade antagandet att deflationstryck var en fördel för ett betalningsmedel.

### 3. Saldo och överföring enligt ERC-223

Kärnöverföringsfunktionen implementerade hela ERC-223-gränssnittet. Interna saldomappningar spårade innehaven för varje adress. Hjälpfunktionen `isContract(address)` skilde EOA-adresser (externally owned account) från kontraktsadresser för att avgöra om `tokenFallback` behövde anropas.

### 4. Multisignatur för företagsutbetalningar

Betalningsflöden i företag krävde medgodkännande: ingen enskild undertecknare kunde ensidigt initiera en utbetalning över ett definierat tröskelvärde. EXTC-kontraktet implementerade ett två-av-N-multisignaturschema:

1. En utsedd initiativtagare föreslog en överföring och angav mottagare, belopp och en nonce.
2. En medundertecknare bekräftade denna nonce.
3. Först när båda signaturerna registrerats på kedjan verkställdes överföringen.

Detta eliminerade risken för en enskild felpunkt för företagskonton, samtidigt som hela godkännandeflödet förblev på kedjan och granskningsbart utan clearinghus som mellanhand.

### 5. Stående överföringar tidslåsta med blockhöjd

Återkommande betalningar (löner, prenumerationer, schemalagda låneavbetalningar) krävde en primitiv för stående överföringar. EXTC implementerade detta som ett tidslås: en överföringspost lagrades i kontraktet med en parameter `releaseBlock`. Överföringen kunde inte verkställas förrän Ethereums blockhöjd nådde `releaseBlock`.

Blockhöjd som tidsproxy var ett pragmatiskt val 2018. Ethereum siktade på ett blockintervall om 15 sekunder, vilket gjorde blockhöjden till en rimligt tillförlitlig proxy för klocktid inom ett spann av minuter. Absoluta tidsstämplar (`block.timestamp`) fanns tillgängliga men kunde manipuleras av miners inom ett fönster på ±900 sekunder, vilket gjorde blockhöjden till den säkrare referensen för finansiella kontrakt.

## Mekanismen för säkerställda direktlån

EXTC:s låneprimitiv var den mest komplexa komponenten. Designen:

1. **Låntagaren låser säkerheten.** Låntagaren anropade `lockCollateral(uint256 _collateralAmount)` och överförde EXTC-tokens till lånekontraktets depå via ett ERC-223-`tokenFallback`.
2. **Kontroll av belåningsgrad.** Kontraktet läste en förkonfigurerad LTV-kvot (t.ex. 50 %) och beräknade det maximala lånebeloppet mot den låsta säkerheten.
3. **Atomär utbetalning av lånet.** Om säkerheten nådde minimitröskeln överförde kontraktet omedelbart lånebeloppet till låntagarens adress. Ingen kreditprövningskö, ingen kreditkommitté, ingen avvecklingsfördröjning.
4. **Återbetalning och frisläppande.** Vid återbetalning (kapitalbelopp plus en fast ränta) frigjorde kontraktet säkerheten tillbaka till låntagaren. Utebliven återbetalning före `releaseBlock` utlöste automatisk likvidation: kontraktet överförde säkerheten till långivarens angivna adress.

Hela flödet upprätthölls av kontraktskod. Ingen av parterna behövde lita på den andra eller förlita sig på en mellanhand för att genomdriva villkoren.

## Vad experimentet visade

EXTC-kontraktsarkitekturen var tekniskt sammanhängande. ERC-223 löste ERC-20:s allvarligaste säkerhetsbrist. Multisignatur- och tidslåsprimitiverna motsvarade direkt verkliga betalningsflöden i företag. Mekanismen för säkerställda lån visade att lån mot säkerhet kunde automatiseras fullt ut och vara självupprätthållande på kedjan.

Två begränsningar visade sig i praktiken:

**Gaskostnader.** Vid toppen i januari 2018 nådde Ethereums gaspriser 50–100 gwei, vilket gjorde att en enda ERC-223-tokenöverföring kostade $0.50–$2.00. För mikrobetalningar eller remitteringar på $10–$50 var dessa avgifter oöverkomliga.

**Genomströmning.** Blockgasgränsen på Ethereums huvudnät i början av 2018 var cirka 8 miljoner gas. En ERC-223-överföring förbrukade ungefär 50 000–80 000 gas. Nätverket kunde därför behandla cirka 100–160 EXTC-tokenöverföringar per block, eller ungefär 7–11 per sekund vid blockintervallet på 15 sekunder. Betalningsnätverksskala, hundratals eller tusentals transaktioner per sekund, gick inte att nå på publika Ethereum utan Layer-2-infrastruktur som ännu inte fanns i produktionsform.

Detta var infrastrukturbegränsningar, inte designfel i EXTC. Kontraktslogiken var korrekt. Den underliggande blockchainen kunde ännu inte bära betalningsvolymer i finansbranschens skala.

## Idéerna som nådde produktion

Flera designmönster från EXTC validerades av senare utveckling:

**Atomär tokenöverföring med mottagarnotifiering** (den centrala ERC-223-egenskapen) blev grunden för ERC-777 (2019), som utökade notifieringsmodellen och senare införlivades i DeFi-låneprotokoll. Mönstret `tokenFallback` återfinns genomgående i modern DeFi-arkitektur.

**Multisignaturgodkännande för företagsutbetalningar**, mönstret att kräva flera signaturer på kedjan före verkställande, blev standardmodellen för DAO-treasuryförvaltning och institutionella förvaringslösningar. Gnosis Safe, lanserad 2018, populariserade detta mönster i stor skala.

**Säkerställda direktlån utan mellanhänder**, mekanismen att låsa säkerhet i depå och frigöra lånebelopp atomärt, är den grundläggande designen i DeFi-låneprotokoll som Compound (2018) och Aave (2020).

**Tidslås baserade på blockhöjd för schemalagda betalningar**, mönstret att koda in framtida exekveringstidpunkt i kontraktet, återfinns i kontrakt för tokenvesting, fördröjda styrningsförslag och TWAP-orakeldesigner (time-weighted average price) i hela DeFi-ekosystemet.

EXTC-experimentet nådde aldrig produktionsskala. Infrastrukturen som krävdes för att göra designen genomförbar behövde ytterligare tre till fem år för att mogna. Designfrågorna det ställde var de rätta för 2018.

## Vanliga frågor

**Varför blev ERC-223 aldrig den dominerande tokenstandarden trots att den åtgärdade ERC-20:s brist?**

ERC-223 krävde att mottagande kontrakt implementerade `tokenFallback`, vilket bröt bakåtkompatibiliteten med de tusentals kontrakt som redan driftsatts för ERC-20-tokens. Det befintliga ERC-20-ekosystemet var för stort för att migrera. Senare förslag, framför allt ERC-777 och ERC-1363, angrep samma problem med andra kompatibilitetsavvägningar, men ERC-20 förblev dominerande genom en kombination av nätverkseffekter och införandet av mönster med inslagna tokens (wrapped tokens) som undvek scenariot med tysta förluster.

**Vad hände med EXTC-tokenen och plattformen?**

EXTC var ett koncepttest och ett tidigt forskningsprojekt från 2018. Den bredare marknaden för ICO:er och betalningstokens krympte kraftigt under 2018–2019 i takt med att Ethereums skalbarhetsgränser och den regulatoriska osäkerheten blev tydliga. Idéerna i EXTC-designen dök upp igen i senare protokoll som hade tillgång till Layer-2-infrastruktur, bättre verktyg och tydligare regelverk.

**Hur står sig EXTC:s modell för säkerställda lån mot moderna DeFi-protokoll som Aave?**

Kärnmekanismen är densamma: lås säkerhet, ta emot ett lån dimensionerat efter en LTV-kvot, återbetala eller likvideras. Skillnaderna är: (1) moderna DeFi-protokoll använder orakelprisflöden för dynamisk LTV i stället för fasta kvoter; (2) de använder algoritmiska räntor som svarar på poolutnyttjandet; (3) de körs på Layer-2-nätverk med gaskostnader 10–100 gånger lägre än 2018 års huvudnät; (4) Aave och Compound har genomgått formella säkerhetsrevisioner och förvaltat likviditet för miljarder dollar, vilket ger empirisk bekräftelse på att grundmodellen är sund.

**Vilka var begränsningarna i Solidity-versionerna i början av 2018?**

EXTC-kontraktet skrevs för Solidity 0.4.x, den dominerande versionen i början av 2018. Solidity 0.4 saknade många säkerhetsfunktioner som infördes i senare versioner: kontroll av heltalsspill (tillagd automatiskt i 0.8.0), `require`/`revert` med felmeddelanden (begränsat i 0.4) och explicit funktionssynlighet (standard var public i 0.4). Kontraktet förlitade sig på OpenZeppelins bibliotek SafeMath som skydd mot spill, ett vanligt mönster innan kompilatorn upprätthöll detta inbyggt.

## Referenser

- Ethereum Foundation, (2015). [EIP-20: tokenstandarden ⧉](https://eips.ethereum.org/EIPS/eip-20 "Tokenstandarden EIP-20").
- Dexaran, Ethereum GitHub, (2017). [Förslag till tokenstandarden ERC-223 ⧉](https://github.com/ethereum/EIPs/issues/223 "ERC-223-diskussion").
- OpenZeppelin, (2018). [OpenZeppelin Contracts – SafeMath ⧉](https://github.com/OpenZeppelin/openzeppelin-contracts "OpenZeppelin Contracts").
- Ethereum Foundation, (2014). [Ethereums whitepaper ⧉](https://ethereum.org/whitepaper "Ethereums whitepaper").
