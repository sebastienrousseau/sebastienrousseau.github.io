---
title: "ERC-20: Ethereum-tokengränssnittet som förändrade världen"
subtitle: "ERC-20-token, smarta kontrakt på Ethereum och standardiseringen av digitala tillgångar."
description: "ERC-20: Ethereum-token ERC-20 är den vanligaste typen av token på Ethereums blockchain och beskrivs ofta som ett digitalt kontrakt i form av ett smart kontrakt"
date: "January 24, 2018"
language: "sv-SE"
locale: "sv_SE"
banner: "https://cloudcdn.pro/stocks/images/m-ZzOa5G8hSPI.webp"
banner_alt: "Avstängd bärbar dator på ett brunt träbord"
keywords: "ethereum, erc20, eip, token, kontrakt, blockchain, kryptovalutor, smart-token, solidity"
---

![En mycket hög byggnad med många hål i fasaden](https://cloudcdn.pro/stocks/images/m-ZzOa5G8hSPI.webp).class=\"img-fluid clearfix\"

## Insikt

### Behovet av ett standardiserat tokengränssnitt

Innan ERC-20-standarden (Ethereum Request for Comments 20) infördes liknade Ethereums blockchain vilda västern i fråga om tokenarkitekturer. Varje nypräglad token hade sin egen unika uppsättning regler, funktioner och gränssnitt. Detta innebar inte bara en brant inlärningskurva för utvecklare utan hämmade också interoperabiliteten mellan token. I praktiken var varje ny token som ett nytt språk som behövde läras in, förstås och implementeras. Denna fragmentering hindrade skalbarheten och den breda användningen av token på Ethereum-plattformen.

Införandet av ERC-20-standarden fungerade som ett enande språk och fastställde en gemensam uppsättning regler och funktioner som alla Ethereum-token måste följa. Utvecklare har nu ett enhetligt gränssnitt att arbeta med, oavsett vilken token det gäller. Denna standardisering effektiviserade processerna för interaktion med token och möjliggjorde en smidigare integration i olika applikationer och tjänster. Som ett resultat kan utvecklare arbeta mer meningsfullt med token, vilket skapar en miljö som gynnar innovation och tillväxt inom Ethereum-ekosystemet.

#### Vilda västern bland tokenarkitekturer

Ethereums blockchain var ursprungligen utformad för att stödja en enda typ av token: ETH. I takt med att plattformen växte i popularitet började utvecklare emellertid skapa egna token för att representera en mängd olika tillgångar och koncept. Detta ledde till en snabb spridning av olika tokenarkitekturer, var och en med sin egen unika uppsättning regler och funktioner.

Denna fragmentering gjorde det svårt för utvecklare att skapa applikationer som kunde interagera med flera token. Den gjorde det också svårt för användare att hantera sina tokentillgångar över olika plattformar.

#### ERC-20-standarden

ERC-20-standarden introducerades 2015 för att möta de utmaningar som vilda västern av tokenarkitekturer gav upphov till. Standarden definierar en gemensam uppsättning regler och funktioner som alla Ethereum-token måste följa. Denna standardisering gör det enklare för utvecklare att skapa applikationer som kan interagera med vilken ERC-20-token som helst, och den gör det också enklare för användare att hantera sina tokentillgångar.

ERC-20-standarden har fått bred spridning i Ethereum-gemenskapen. I dag finns det över 200 000 ERC-20-token, och standarden används av en lång rad applikationer, däribland decentraliserade börser, utlåningsplattformar och spel-dappar.

## Idé

### En gemensam uppsättning funktioner och egenskaper för alla token

ERC-20-standarden definierar en uppsättning av sex grundläggande funktioner som alla ERC-20-kompatibla token måste implementera. Dessa funktioner är:

- `transfer(address to, uint256 amount)`: Överför ett antal token från anroparens adress till den angivna adressen.
- `approve(address spender, uint256 amount)`: Godkänner att den angivna adressen får spendera ett antal token för anroparens räkning.
- `allowance(address owner, address spender)`: Returnerar det antal token som den angivna spenderaren är godkänd att spendera för den angivna ägarens räkning.
- `totalSupply()`: Returnerar det totala antalet token i omlopp.
- `balanceOf(address owner)`: Returnerar det antal token som den angivna adressen innehar.
- `name()`: Returnerar tokenens namn.
- `symbol()`: Returnerar tokenens symbol.

ERC-20-standarden definierar även två händelser som måste emitteras när motsvarande funktioner har utförts framgångsrikt. Dessa händelser är:

- `Transfer(address from, address to, uint256 amount)`: Emitteras när ett antal token överförs från en adress till en annan.
- `Approval(address owner, address spender, uint256 amount)`: Emitteras när den angivna adressen godkänns att spendera ett antal token för den angivna ägarens räkning.

## Genomslag

### DeFi-sektorns tillväxt och Ethereums ökade användning

ERC-20-standarden har haft ett betydande genomslag i Ethereum-ekosystemet. Den har varit en avgörande möjliggörare för DeFi-rörelsen (decentraliserad finans) och har också bidragit till att öka användningen av Ethereum.

DeFi-plattformar, som erbjuder en rad finansiella tjänster från utlåning till kapitalförvaltning, är starkt beroende av token för att underlätta transaktioner. Med ERC-20 som en universell adapter har det blivit avsevärt enklare för DeFi-applikationer att integrera ett brett urval av token utan att behöva anpassa sin kod för var och en.

ERC-20-standarden har också gjort det enklare för användare att hantera sina tokentillgångar. När token följer samma grundläggande regler blir det lättare för användare att överföra, spendera och hantera sina tokentillgångar över flera plattformar. Denna förbättrade användarupplevelse har varit en drivande faktor bakom Ethereums ökade användning.

## Incitament

### Lägre utvecklingskostnader och förbättrad säkerhet

Den standardisering som ERC-20-protokollet medfört har även haft en direkt ekonomisk effekt. Genom att tillhandahålla en beprövad och gemenskapsgodkänd mall för tokenskapande har den avsevärt sänkt inträdesbarriärerna för utvecklare. De kan nu skapa en ny token med lägre utvecklingskostnader och kortare tid till marknaden, eftersom de inte längre behöver uppfinna hjulet på nytt. Standarden uppmuntrar också indirekt skapandet av DApps (decentraliserade applikationer) och tjänster som universellt kan interagera med vilken ERC-20-token som helst, vilket främjar ett mer livskraftigt ekosystem.

En annan påtaglig fördel är förbättrad säkerhet. ERC-20-standarden har genomgått rigorös granskning av Ethereum-gemenskapen, vilket gör den till en robust och säker modell för tokenimplementering. Att följa standarden innebär att de grundläggande delarna av tokenens smarta kontrakt följer gemenskapens vedertagna bästa praxis. Detta minimerar risken för säkerhetssårbarheter som annars skulle kunna uppstå ur en illa utformad tokenmodell. Även om det inte utgör en garanti mot alla typer av sårbarheter är det ett betydande steg mot att säkerställa den övergripande säkerheten för token och, i förlängningen, för de projekt som använder dem.

![divider](https://cloudcdn.pro/clients/common/images/elements/divider.svg).class=\"m-10 w-100\"

**Därmed är vår genomgång till ända. Tack för din tid!**
