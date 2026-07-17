---
title: "Presentation av en ny kryptovaluta och en snabbare betalningslösning"
subtitle: "En ny kryptovaluta och en lösning för snabbare betalningar för nästa generations finansvärld."
description: "I början av 2018 undersökte EXTC-plattformen snabbare gränsöverskridande betalningar via smarta ERC-223-kontrakt på Ethereum, en tidig ritning för det som decentraliserad finans senare skulle bygga."
date: "February 4, 2018"
language: "sv-SE"
locale: "sv_SE"
banner: "https://cloudcdn.pro/stocks/images/laureen-missaire-DBbuhMbAIsQ.webp"
banner_alt: "Avstängd bärbar dator på ett brunt träbord"
keywords: "EXTC, ERC-223, smarta kontrakt på Ethereum, snabbare betalningar, kryptovaluta, blockchain-betalningar, betalningstoken, decentraliserad finans, ERC-20, gränsöverskridande betalningar"
---

![En mycket hög byggnad med många hål i fasaden](https://cloudcdn.pro/stocks/images/laureen-missaire-DBbuhMbAIsQ.webp).class=\"img-fluid clearfix\"

> **Sammanfattning / Viktigaste slutsatser**
>
> - **Kärnhypotesen.** Smarta kontrakt på Ethereum skulle kunna ersätta korrespondentbankernas stafettlopp för gränsöverskridande betalningar, med avveckling på sekunder i stället för dagar och utan avgiftslagret på 3–7 % ([Världsbanken, 2018](https://www.worldbank.org/en/topic/migrationremittancesdiasporaissues/brief/migration-remittances-data "Världsbankens remitteringspriser")).
> - **ERC-223:s specifika bidrag.** Standarden åtgärdade bristen med tyst tokenförlust i ERC-20 genom att kräva att smarta kontrakt exponerar en `tokenFallback`-funktion, så att misslyckade överföringar återkallas i stället för att token bränns oåterkalleligt ([Ethereum EIPs](https://eips.ethereum.org/EIPS/eip-20 "EIP-20: Tokenstandard")).
> - **EXTC:s betalningsprimitiver.** Tokendesignen stödde enskilda atomära överföringar, tidsstyrda stående betalningsuppdrag, företagsutbetalningar med multisignatur och omedelbara mikrolån mot säkerhet, allt utan clearinginstitut.
> - **Vad experimentet visade.** Den tekniska designen var sammanhängande, men Ethereums mainnet behandlade 2018 ungefär 15 transaktioner per sekund. Betalningsvolymer i stor skala krävde Layer-2-lösningar som ännu inte var produktionsklara.
> - **Arvet.** De arkitektoniska idéerna i EXTC (programmerbara pengar, atomär avveckling, tokenlogik med inbyggd regelefterlevnad) återkom senare i DeFi-protokoll, CBDC-designer och ramverk för tokeniserade insättningar.

---

## Problemet: gränsöverskridande betalningar 2018

Internationella betalningar i början av 2018 var långsamma, dyra och ogenomskinliga till sin konstruktion. En privatöverföring från Storbritannien till Sydostasien involverade vanligtvis två till fyra korrespondentbanker, som var och en tog ut en avgift och lade en dag till avvecklingskedjan. Världsbankens databas Remittance Prices Worldwide noterade en global genomsnittskostnad på 6,9 % för en remittering på USD 200 under första kvartalet 2018.

Kryptovalutor hade redan visat att digitala kontanter peer-to-peer var tekniskt genomförbara. Bitcoin avvecklade transaktioner globalt på ungefär tio minuter, och Ethereums programmerbara lager tillförde smarta kontrakt: självexekverande kod som kunde koda in betalningsregler direkt i själva överföringen. Gapet mellan vad som var tekniskt möjligt på kedjan och vad den traditionella korrespondentbankverksamheten levererade var det designutrymme som EXTC klev in i.

## Den tekniska grunden: ERC-20 och dess brist

ERC-20-standarden, formaliserad i Ethereum Improvement Proposal 20, definierade det kanoniska gränssnittet för fungibla token: `balanceOf`, `transfer`, `transferFrom`, `approve` och `allowance`. I början av 2018 var ERC-20 den dominerande tokenstandarden, med hundratals token utplacerade på mainnet.

ERC-20 hade dock ett strukturellt problem. När token skickades direkt till en smart kontraktsadress med den vanliga `transfer`-funktionen hade kontraktet inget sätt att upptäcka den inkommande överföringen eller agera på den. Token som skickades på detta sätt blev permanent låsta. Ethereum-gemenskapen uppskattade att ERC-20-token till ett värde av miljontals dollar hade gått förlorade på detta sätt vid mitten av 2018.

ERC-223, föreslagen av Dexaran i Ethereums ärendehanterare på GitHub, åtgärdade detta genom att lägga till ett krav på en funktion `tokenFallback(address _from, uint _value, bytes _data)` hos mottagande kontrakt. Om det mottagande kontraktet inte implementerade `tokenFallback` återkallades överföringen och token returnerades till avsändaren. Detta gjorde ERC-223-överföringar atomära: antingen accepterade kontraktet token och utförde sin logik, eller så misslyckades transaktionen på ett rent sätt.

## Tokendesignen i EXTC

Token Express Transaction Credits utformades kring fem kärnattribut:

- **Namn, symbol och decimaler.** Standardmässiga identitetsfält enligt ERC-223, med 18 decimaler för precision under centnivå.
- **Total tillgång.** Fastställd vid utgivningen, vilket gjorde EXTC till en deflationär tillgång eftersom förlorade eller outnyttjade token inte kunde ges ut på nytt.
- **Saldo och överföring.** Standardfunktioner för läsning och skrivning, utökade med ERC-223:s krav på `tokenFallback`.
- **Stöd för multisignatur.** Företagsutbetalningar krävde medsignering från flera auktoriserade adresser före verkställande, vilket gav revisionsspår utan ett centraliserat clearinghus.
- **Tidslåsta överföringar.** En primitiv för stående betalningsuppdrag lät EXTC schemalägga framtida betalningar, en förmåga som traditionella banköverföringar krävde externa instruktioner för att uppnå.

## Betalningsprimitiver som plattformen siktade på

EXTC:s arkitektur utformades för att ersätta fyra specifika betalningsflöden som äldre system hanterade ineffektivt:

**Enskilda atomära betalningar**: en engångsöverföring som avvecklades i en enda Ethereum-transaktion, vanligtvis inom 15–30 sekunder på 2018 års mainnet.

**Tidsbaserade stående betalningsuppdrag**: återkommande överföringar kodade som tidslåsta anrop till smarta kontrakt, vilket eliminerade behovet av att en bank tar emot och på nytt verkställer periodiska instruktioner.

**Massutbetalningar från företag**: batchbetalningar till flera mottagare i en transaktion, där varje enskild överföring krävde auktorisering med multisignatur, vilket minskade kostnader och motpartsrisk.

**Omedelbara lån mot säkerhet**: låntagare låste EXTC-token som säkerhet i ett smart kontrakt; kontraktet frigjorde lånebeloppet automatiskt vid mottagandet, utan kreditkommitté eller fördröjning för kreditprövning.

## Vad experimentet visade

EXTC-designen var tekniskt sammanhängande. ERC-223-grunden löste den mest betydande säkerhetsbristen i den dominerande tokenstandarden, och betalningsprimitiverna motsvarade direkt verkliga arbetsflöden som korrespondentbankverksamheten hanterade ineffektivt.

Den praktiska begränsningen var Ethereums genomströmning. Under första kvartalet 2018 hanterade mainnet i genomsnitt 15 transaktioner per sekund med en gasgräns på cirka 8 miljoner per block. Ett betalningsnätverk som behandlade ens en liten andel av de globala remitteringsvolymerna (Världsbanken uppskattade att 270 miljoner migranter skickade pengar hem 2017) skulle ha mättat mainnet inom några minuter.

Layer-2-skalningslösningar, i synnerhet state channels och de tidiga versionerna av det som blev rollup-teknik, var föremål för aktiv forskning 2018 men var inte produktionsklara. Lightning Network hade just lanserats på Bitcoins mainnet i januari 2018 med betydande förbehåll. De tekniska förutsättningarna för att ett blockchain-baserat betalningsnätverk skulle kunna verka i korrespondentbankskala fanns ännu inte.

## Idéerna som överlevde

Flera arkitektoniska koncept från EXTC och samtida betalningstokenprojekt bekräftades av den efterföljande utvecklingen:

**Programmerbara pengar**, det vill säga betalningsregler kodade direkt i överföringslogiken, blev ett centralt inslag i DeFi-utlåningsprotokoll som Compound och Aave, lanserade 2018 respektive 2020.

**Atomär avveckling utan clearinghus**, egenskapen att en överföring antingen lyckas fullständigt eller återkallas, är i dag ett designkrav i ramverk för tokeniserade insättningar och i de arkitekturer för wholesale-CBDC som utforskas av centralbanker, däribland Bank of England och Europeiska centralbanken.

**Token med inbyggd regelefterlevnad**, där överföringsrestriktioner och rapporteringsskyldigheter kodas in i själva tokenkontraktet, återfinns i reglerade tokenstandarder som ERC-1400 (värdepapperstoken) och i designen av efterlevnadslagret för Project Agorá och liknande tokeniseringsexperiment mellan flera centralbanker.

EXTC-experimentet nådde aldrig produktionsskala, men frågorna det ställde, om programmerbar avveckling, atomära överföringar och självverkställande betalningsregler, var de rätta frågorna för 2018. Infrastrukturen som krävdes för att besvara dem tog ytterligare fem år att mogna.

## Vanliga frågor

**Vad var ERC-223 och varför använde EXTC den i stället för ERC-20?**

ERC-20-token som skickades direkt till smarta kontraktsadresser gick tyst förlorade eftersom kontrakten inte hade något sätt att upptäcka den inkommande överföringen. ERC-223 åtgärdade detta genom att kräva att mottagande kontrakt implementerar en `tokenFallback`-funktion; om funktionen saknades återkallades överföringen i stället för att token brändes. EXTC valde ERC-223 för att göra alla överföringar på kedjan atomära och säkra.

**Varför skalade tidiga betalningstokenprojekt inte upp och ersatte korrespondentbankverksamheten?**

Ethereums mainnet behandlade 2018 ungefär 15 transaktioner per sekund. Enbart de globala remitteringsvolymerna, utan att räkna handelsfinansiering eller företagsbetalningar, skulle kräva tiotusentals transaktioner per sekund. Den Layer-2-skalningsinfrastruktur som behövdes för att nå den genomströmningen var inte produktionsklar förrän 2021–2023.

**Vad hände med idéerna bakom EXTC?**

Kärnkoncepten, programmerbara betalningsregler, atomär avveckling och tokenlogik med inbyggd regelefterlevnad, togs upp av DeFi-protokoll, reglerade standarder för värdepapperstoken (ERC-1400) och forskningen om centralbankers digitala valutor. De ramverk för tokeniserade insättningar som nu pilottestas av affärsbanker går direkt tillbaka till de designfrågor som tidiga betalningstokenexperiment som EXTC först ställde.

**Hur står sig 2018 års EXTC-design mot 2026 års förslag om tokeniserade insättningar?**

Avvecklingsmodellen är likartad: token som representerar monetära fordringar och överförs atomärt på en distribuerad liggare. De viktigaste skillnaderna är: (1) 2026 års tokeniserade insättningar är affärsbankers skulder snarare än innehavartoken; (2) de körs på behörighetsstyrda eller hybrida liggare under regulatorisk tillsyn snarare än på publikt mainnet; (3) regelefterlevnad och identitetsverifiering upprätthålls på protokollnivå snarare än att lämnas till deltagarna.

## Referenser

- Ethereum Foundation, (2018). [EIP-20: Tokenstandard ⧉](https://eips.ethereum.org/EIPS/eip-20 "EIP-20 Tokenstandard").
- Dexaran, Ethereum GitHub, (2017). [Förslag till tokenstandarden ERC-223 ⧉](https://github.com/ethereum/EIPs/issues/223 "ERC-223-diskussion").
- Världsbanken, (2018). [Remittance Prices Worldwide, Q1 2018 ⧉](https://www.worldbank.org/en/topic/migrationremittancesdiasporaissues/brief/migration-remittances-data "Världsbankens remitteringspriser").
- Buterin, V., (2014). [Ethereum: en plattform för nästa generations smarta kontrakt och decentraliserade applikationer ⧉](https://ethereum.org/whitepaper "Ethereums whitepaper").
