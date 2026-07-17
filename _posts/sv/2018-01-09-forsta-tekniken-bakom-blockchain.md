---
title: "Att förstå tekniken bakom blockchain"
subtitle: "En praktisk genomgång av kryptografin och konsensusmekanismerna bakom blockchain."
description: "En teknisk introduktion till hur blockchain fungerar: kryptografiska hashkedjor, Merkle-träd, distribuerad konsensus och varför Ethereums programmerbara lager förvandlade en betalningsliggare till en plattform för smarta kontrakt och tokeniserade tillgångar."
date: "January 9, 2018"
language: "sv-SE"
locale: "sv_SE"
banner: "https://cloudcdn.pro/stocks/images/adam-smigielski-K5mPtONmpHM.webp"
banner_alt: "Abstrakta digitala liggarblock sammanlänkade av ljusspår mot mörk bakgrund"
keywords: "blockchainteknik, kryptografisk hash, Merkle-träd, distribuerad konsensus, proof of work, Ethereum, smarta kontrakt, EVM, Solidity, ERC-20, distribuerad liggare, decentraliserad finans"
---

![Abstrakta digitala liggarblock sammanlänkade av ljusspår mot mörk bakgrund](https://cloudcdn.pro/stocks/images/adam-smigielski-K5mPtONmpHM.webp).class=\"img-fluid clearfix\"

> **Sammanfattning för ledningen / Viktiga slutsatser**
>
> - **Problemet.** Digitala kontanter kräver en lösning på dubbelspenderingsproblemet: att förhindra att samma enhet spenderas två gånger utan ett betrott clearinginstitut. Bitcoins whitepaper från 2008 löste detta genom att ersätta betrodda mellanhänder med kryptografiska bevis och distribuerad konsensus ([Nakamoto, 2008](https://bitcoin.org/bitcoin.pdf "Bitcoin: ett elektroniskt kontantsystem peer-to-peer")).
> - **Datastrukturen.** En blockchain är en länkad lista av block där varje blockhuvud innehåller SHA-256-hashen av det föregående huvudet. Hashkedjan gör historiken enbart tilläggsbar: att ändra ett tidigare block ogiltigförklarar varje efterföljande hash och tvingar en angripare att göra om allt efterföljande proof-of-work.
> - **Merkle-träd.** Transaktionerna i ett block hashas till ett binärt Merkle-träd. Rothashen, som lagras i blockhuvudet, möjliggör effektiv verifiering av varje enskild transaktion utan att hela blocket behöver laddas ned: grunden för lättviktiga SPV-klienter.
> - **Ethereums utvidgning.** Ethereums Yellow Paper (2014) introducerade EVM, en deterministisk stackmaskin som körs på varje fullnod. Smarta kontrakt är bytekod som distribueras till kedjan; de exekveras identiskt på alla noder och avvecklas atomärt, vilket ersätter betrodda mellanhänder med självverkställande kod ([Wood, 2014](https://ethereum.github.io/yellowpaper/paper.pdf "Ethereum Yellow Paper")).
> - **Praktisk betydelse.** Varje tokeniserad tillgång, stablecoin och DeFi-protokoll som lanserats sedan 2017 vilar på dessa grunder. Att förstå hashkedjan, Merkle-trädet och EVM:s exekveringsmodell är förutsättningen för att arbeta med varje Ethereum-baserat system.

---

## Problemet som blockchain löste

Före Bitcoin krävde digitala betalningar en betrodd mellanhand (en bank, en betalningsförmedlare eller ett clearinginstitut) för att förhindra dubbelspendering. Om Alice skickade en digital fil som representerade 10 pund till Bob fanns det inget i själva filen som hindrade henne från att skicka en identisk kopia till Carol. Lösningen i varje befintligt system var centraliserad bokföring: bankens liggare angav att pengarna var spenderade, och därför kunde de inte spenderas igen.

Bitcoins bidrag var att ersätta den betrodda liggaren med en distribuerad sådan, där registret över alla transaktioner replikeras över tusentals oberoende noder. Ömsesidig misstro mellan noder omvandlades till säkerhet genom två mekanismer:

1. **Kryptografisk länkning.** Varje transaktionsblock innehåller hashen av det föregående blocket. En hashfunktion är en deterministisk envägsavbildning: för varje given indata producerar funktionen en utdata med fast längd, och en ändring av en enda bit i indatan ger en helt annan utdata. Det innebär att varje förändring av ett historiskt block ogiltigförklarar alla block som följer efter det.

2. **Proof-of-work-konsensus.** Att lägga till ett nytt block kräver att man hittar ett nonce-värde sådant att blockets hash hamnar under ett tröskelvärde: beräkningsmässigt dyrt att finna, trivialt billigt att verifiera. Det gör att kostnaden för att skriva om historiken växer i proportion till djupet på det block som ändras, eftersom en angripare måste göra om allt proof-of-work från det blocket fram till kedjans spets.

Kombinationen innebär att den längsta kedjan med mest ackumulerat proof-of-work per konstruktion är den som upprätthålls av ärliga deltagare som spenderar verkliga resurser.

## De kryptografiska byggstenarna

Blockchaintekniken sammanfogar tre redan existerande kryptografiska primitiver till en ny arkitektur:

### SHA-256-hashfunktioner

SHA-256 (Secure Hash Algorithm 256-bit) tillhör SHA-2-familjen som standardiserats av NIST. Den tar en indata av godtycklig längd och producerar en 256-bitars utdata. Nyckelegenskaper för användning i blockchain:

- **Deterministisk.** Samma indata ger alltid samma utdata.
- **Preimage-resistens.** Givet en hashutdata är det beräkningsmässigt ogörligt att rekonstruera indatan.
- **Lavineffekt.** En ändring av en enda indatabit ändrar ungefär hälften av utdatabitarna, vilket gör brute-force-sökning ineffektiv.
- **Kollisionsresistens.** Det är beräkningsmässigt ogörligt att hitta två olika indata som ger samma hash.

Bitcoin tillämpar SHA-256 två gånger (SHA-256d) för extra skydd mot längdförlängningsattacker. Ethereum använder Keccak-256, en variant som var SHA-3-finalist.

### Merkle-träd

Ett Merkle-träd är ett binärt träd av hashar. Varje lövnod är hashen av en transaktion. Varje intern nod är hashen av sina två barn. Roten, Merkle-roten, sammanfattar alla transaktioner i blocket i ett enda 32-byte-värde som lagras i blockhuvudet.

Den praktiska konsekvensen: för att verifiera att en viss transaktion ingår i ett block behövs bara `log₂(n)` hashar, inte alla `n` transaktioner. För ett block med 2 000 transaktioner kräver verifieringen 11 hashar i stället för 2 000: grunden för Simplified Payment Verification (SPV) i lättviktiga klienter.

### Digitala signaturer (ECDSA)

Transaktionsauktorisering i Bitcoin och Ethereum använder Elliptic Curve Digital Signature Algorithm (ECDSA) över kurvan secp256k1. En privat nyckel signerar en transaktion; varje nod kan verifiera signaturen med motsvarande publika nyckel utan att känna till den privata nyckeln. Det säkerställer att endast innehavaren av den privata nyckeln kan auktorisera en betalning från en adress.

Ethereum-adresser är de sista 20 byten av Keccak-256-hashen av den publika nyckeln, en härledning som gör adresserna kompakta och portabla samtidigt som de förblir kryptografiskt knutna till nyckelparet.

## Hur Bitcoins blockchain fungerar

Ett Bitcoin-block innehåller tre logiska komponenter:

**Blockhuvudet**: 80 byte som omfattar protokollversionen, hashen av det föregående blockhuvudet, Merkle-roten av transaktionerna, en Unix-tidsstämpel, det aktuella svårighetsmålet och noncen. Miners itererar noncen (och ibland tidsstämpeln eller extra-noncen i coinbase-transaktionen) tills dubbel-SHA-256-hashen av huvudet hamnar under svårighetsmålet.

**Transaktionslistan**: den ordnade mängden transaktioner som ingår i blocket. Coinbase-transaktionen (den första) tilldelar blockbelöningen och transaktionsavgifterna till minerns adress.

**Kedjan**: länkningen av huvuden. Det ackumulerade proof-of-work i kedjan (summan av allt arbete som lagts ned för att producera varje block) avgör vilken förgrening som är den kanoniska kedjan. Noder följer alltid kedjan med mest ackumulerat arbete.

Blocktiden är satt till 10 minuter för Bitcoin. Svårigheten justeras var 2 016:e block (ungefär varannan vecka) för att bibehålla det målet när nätverkets totala hashkraft förändras.

## Ethereums programmerbara lager

Ethereum generaliserade Bitcoins transaktionsmodell från "överför värde" till "exekvera kod". De viktigaste tilläggen:

**Ethereum Virtual Machine (EVM).** En stackbaserad virtuell maskin med 256-bitars ord som exekverar deterministiskt på alla fullnoder. Varje opkod har en explicit gaskostnad. Beräkningen begränsas av blockets gasgräns, vilket förhindrar att oändliga loopar stoppar nätverket. Alla noder som exekverar samma bytekod på samma tillstånd måste producera samma utdata; denna konsensus om exekveringen är det som gör smarta kontrakt tillitslösa.

**Konton.** Ethereum har två kontotyper: externt ägda konton (EOA) som styrs av privata nycklar, och kontraktskonton vars kod lagras på kedjan. En transaktion som skickas till en kontraktsadress utlöser exekvering av kontraktets bytekod.

**Tillstånd.** Ethereums globala tillstånd är en avbildning från adresser till kontotillstånd (nonce, saldo, lagring, kodhash). Tillståndsroten, ett Merkle-Patricia-trie över alla kontotillstånd, ingår i varje blockhuvud och möjliggör effektiva bevis av varje kontos tillstånd vid varje blockhöjd.

**Gas.** Användare betalar gas (i ETH) för varje EVM-operation. Gas fyller två funktioner: den kompenserar miners/validerare för beräkningsarbete, och den begränsar de resurser en enskild transaktion kan förbruka, vilket förhindrar överbelastningsattacker via dyra operationer.

## Att skriva smarta kontrakt i Solidity

Solidity är ett statiskt typat, kontraktsorienterat språk som kompileras till EVM-bytekod. Ett minimalt tokenkontrakt illustrerar kärnbegreppen:

```solidity
pragma solidity ^0.8.0;

contract MyToken {
    string public name;
    string public symbol;
    uint8 public decimals;
    uint256 public totalSupply;
    mapping(address => uint256) public balanceOf;

    event Transfer(address indexed from, address indexed to, uint256 value);

    constructor(
        string memory _name,
        string memory _symbol,
        uint8 _decimals,
        uint256 _totalSupply
    ) {
        name = _name;
        symbol = _symbol;
        decimals = _decimals;
        totalSupply = _totalSupply;
        balanceOf[msg.sender] = _totalSupply;
    }

    function transfer(address _to, uint256 _value) external returns (bool) {
        require(balanceOf[msg.sender] >= _value, "Insufficient balance");
        balanceOf[msg.sender] -= _value;
        balanceOf[_to] += _value;
        emit Transfer(msg.sender, _to, _value);
        return true;
    }
}
```

Viktiga observationer: `mapping(address => uint256)` är en lagringslayout i EVM, inte en datastruktur i minnet; läsningar och skrivningar kostar gas. `require` återkallar hela transaktionen vid fel och returnerar oanvänd gas. `event Transfer` avger en logg som indexerare utanför kedjan använder för att spåra överföringar utan att läsa om hela tillståndet. `constructor` körs en gång vid distributionen; efterföljande anrop går till de namngivna funktionerna.

ERC-20-standarden formaliserade ett gemensamt gränssnitt för fungibla token, `transfer`, `transferFrom`, `approve`, `allowance`, `balanceOf` och `totalSupply`, vilket gör att varje ERC-20-kompatibel token fungerar med varje ERC-20-medveten börs eller plånbok utan skräddarsydd integration.

## Från liggare till finansiell infrastruktur

De blockchainprimitiver som beskrivs här (hashkedjor, Merkle-träd, EVM och ERC-20) blev grunden för en bredare uppsättning finansiella tillämpningar mellan 2018 och 2026:

**Decentraliserad finans (DeFi).** Utlåningsprotokoll (Compound, Aave), automatiserade marknadsgaranter (Uniswap) och avkastningsaggregatorer körs alla som smarta kontrakt i EVM. De ersätter de traditionella finansiella mellanhändernas clearing-, förvarings- och avvecklingsfunktioner med självexekverande kod och likviditetspooler på kedjan.

**Tokeniserade tillgångar.** Centralbanker och affärsbanker genomför pilotprojekt med tokeniserade insättningar, tokeniserade obligationer och tokeniserade penningmarknadsfonder på behörighetsstyrda varianter av EVM-kompatibla kedjor. Den underliggande mekaniken, hashsäkrade tillståndsövergångar, atomär avveckling och programmerbara överföringsregler, är direkta ättlingar till Ethereum-arkitekturen från 2014.

**Digitala centralbanksvalutor.** Bank of Englands forskning om wholesale-CBDC, ECB:s program för en digital euro och Project Agorá utforskar alla DLT-arkitekturer som härstammar från eller är kompatibla med grunddesignerna i Bitcoin och Ethereum. Konsensus- och hashkedjestrukturerna förblir relevanta även där behörighets- och styrningsmodellen skiljer sig helt från publika blockkedjor.

Resan från Bitcoins whitepaper 2008 till tokeniserad finans 2026 spänner över två decennier, men den vilar på en sammanhängande teknisk härstamning. Att förstå hur en SHA-256-hashkedja upprätthåller oföränderlighet, hur ett Merkle-träd möjliggör effektiv verifiering och hur EVM exekverar smarta kontrakt atomärt är förutsättningen för att kunna bedöma varje påstående om vad blockchain kan och inte kan göra i reglerade finansiella tjänster.

## Vanliga frågor

**Vad är skillnaden mellan en blockchain och en distribuerad databas?**

En traditionell distribuerad databas replikerar data över noder för tillgänglighet och prestanda, men förtroendet är centraliserat: en administratör kan ändra poster. En blockchain gör manipulation beräkningsmässigt dyr genom hashkedjning och konsensus: att ändra en historisk post kräver att allt efterföljande proof-of-work eller proof-of-stake görs om, och att nätverket övertygas om att acceptera den ändrade förgreningen. Den särskiljande egenskapen är manipulationsevidens som upprätthålls av kryptografi och incitamentsdesign snarare än av åtkomstkontroller.

**Varför använder Ethereum Keccak-256 i stället för SHA-256?**

Ethereum valde Keccak-256 (SHA-3-finalisten före NIST:s standardiseringsjusteringar) delvis för att dess konstruktörer ville vara oberoende av SHA-2-linjen som Bitcoin redan var beroende av. Keccak har också andra algebraiska egenskaper som gjorde den attraktiv för vissa EVM-operationer. Den praktiska effekten för utvecklare är att Ethereums adresshärledning och hashning av lagringsplatser använder Keccak-256, inte SHA-256d som i Bitcoin.

**Vad förhindrar "gas" i EVM?**

Gas förhindrar två kategorier av attacker. För det första förhindrar den överbelastning via beräkningsmässigt dyra operationer: varje opkod kostar gas, så en angripare kan inte tvinga nätverket att exekvera oändliga loopar utan kostnad. För det andra begränsar blockets gasgräns den totala beräkningen per block, vilket säkerställer att valideringstiden per block förblir begränsad och förutsägbar för fullnoder. Utan gas skulle ett enda kontraktsanrop kunna stoppa nätverket genom att exekvera obegränsad beräkning.

**Hur förändrar proof-of-stake säkerhetsmodellen jämfört med proof-of-work?**

I proof-of-work tillhandahålls säkerheten genom energiförbrukning: att attackera kedjan kräver kontroll över mer än 50 % av nätverkets hashkraft, vilket innebär kontroll över mer än 50 % av dess fysiska hårdvara och elkraft. I proof-of-stake (som Ethereum använder sedan the Merge 2022) tillhandahålls säkerheten genom ekonomisk insats: validerare låser ETH som säkerhet, vilken dras in (slashas) om de signerar motstridiga block. En 51 %-attack kräver att man förvärvar och riskerar mer än 50 % av all stakad ETH: en kapitalkostnad snarare än en hårdvaru- och energikostnad. Säkerhetsmodellen är annorlunda men matematiskt jämförbar i ekonomiska termer under antagandet att rationella validerare föredrar avgiftsintäkter framför kapitalförstöring.

## Referenser

- Nakamoto, S., (2008). [Bitcoin: ett elektroniskt kontantsystem peer-to-peer ⧉](https://bitcoin.org/bitcoin.pdf "Bitcoins whitepaper").
- Buterin, V., (2014). [Ethereum: en nästa generations plattform för smarta kontrakt och decentraliserade applikationer ⧉](https://ethereum.org/whitepaper "Ethereums whitepaper").
- Wood, G., (2014). [Ethereum: en säker decentraliserad generaliserad transaktionsliggare ⧉](https://ethereum.github.io/yellowpaper/paper.pdf "Ethereum Yellow Paper").
- NIST, (2015). [SHA-3-standarden: permutationsbaserade hashfunktioner och funktioner med utökningsbar utdata ⧉](https://www.nist.gov/publications/sha-3-standard-permutation-based-hash-and-extendable-output-functions "NIST FIPS 202").
