---
title: "Az Express Transaction Credits platform megalkotása"
tags: "EXTC platform, ERC-223, Ethereum, smart contracts, token architecture, multi-signature, time-locked transfer, blockchain, decentralised finance, collateral-backed loans, ISO 20022, post-quantum cryptography, AI, stablecoins"
subtitle: "Az Express Transaction Credits platform megtervezése ERC-223 okosszerződésekkel."
description: "Technikai mélymerülés abba, hogyan épült fel az EXTC platform az Ethereum ERC-223 szabványán 2018-ban: tokenarchitektúra, többaláírásos kifizetések, időzárolt átutalások és fedezetalapú azonnali hitelek."
date: "Feb 15, 2018"
language: "hu"
locale: "hu_HU"
banner: "https://cloudcdn.pro/stocks/images/tarik-haiga-3637943.webp"
banner_alt: "Óriási fehér oszlopok"
keywords: "EXTC platform, ERC-223, Ethereum okosszerződések, tokenarchitektúra, többaláírásos, időzárolt átutalás, blokklánc fizetések, fedezetalapú hitelek, decentralizált pénzügyek, 2018-as kripto"
---

![Óriási fehér oszlopok](https://cloudcdn.pro/stocks/images/tarik-haiga-3637943.webp).class=\"img-fluid clearfix\"

> **Vezetői összefoglaló / Legfontosabb tanulságok**
>
> - **Az alapprobléma.** Az ERC-20, a 2018-ban meghatározó Ethereum token-szabvány, szerkezeti hibában szenvedett: a közvetlenül egy okosszerződés címére átutalt tokenek csendben megsemmisültek, ha a szerződésnek nem volt kezelője. Bármely ERC-20-ra épített fizetési platform megörökölte ezt a kockázatot ([Ethereum EIPs](https://eips.ethereum.org/EIPS/eip-20 "EIP-20: Token Standard")).
> - **Az ERC-223 mint megoldás.** Az ERC-223 megkövetelte, hogy a fogadó szerződések implementáljanak egy `tokenFallback(address, uint, bytes)` függvényt. Ha ez hiányzott, az átutalás atomi módon visszagördült. Egyetlen token sem veszhetett el csendben ([Ethereum EIPs GitHub](https://github.com/ethereum/EIPs/issues/223 "ERC-223 Token Standard Proposal")).
> - **Az EXTC öt szerződéses primitívje.** Tokenidentitás (név, szimbólum, 18 tizedesjegyű pontosság), rögzített kínálat, ERC-223-kompatibilis átutalás, többaláírásos vállalati kifizetés és blokkmagasság szerint időzárolt tartós megbízások.
> - **A fedezeti hitel mechanizmusa.** A hitelfelvevők EXTC tokeneket zároltak egy szerződéses letétben; a szerződés a fedezet kézhezvételekor atomi módon szabadította fel a hitelösszeget, jóváhagyási késedelem vagy hitelbizottsági döntés nélkül.
> - **Amit a kísérlet feltárt az Ethereum korlátairól.** A főhálózat ~15 TPS áteresztőképessége és a 2018 januári csúcson tranzakciónkénti 0,10–1,00 dolláros gázköltségek mellett egy fizetési hálózat, amely akár csak utalás-nagyságrendű forgalmat dolgozott fel, gazdaságilag és technikailag megvalósíthatatlan volt a nyilvános Ethereumon Layer-2 infrastruktúra nélkül.

---

## A tervezési probléma: miért volt elégtelen az ERC-20

Az ERC-20 szabvány, amelyet 2015-ben javasoltak és a 20. számú Ethereum Improvement Proposalban formalizáltak, definiálta azt a kanonikus, helyettesíthető tokeninterfészt, amely a 2017–2018-as ICO-fellendülést hajtotta. Hat alapfüggvénye, a `totalSupply`, `balanceOf`, `transfer`, `transferFrom`, `approve` és `allowance`, elegendő volt az egyszerű tokenkibocsátáshoz és -cseréhez.

Egy fizetési platform számára azonban az ERC-20 üzemi szempontból kritikus hibában szenvedett. A `transfer(address _to, uint256 _value)` függvény bármely címre, beleértve a szerződéscímeket is, átmozgatta a tokeneket anélkül, hogy bármilyen kódot elindított volna a fogadó szerződésben. Egy olyan szerződés, amelyet nem programoztak kifejezetten a beérkező ERC-20 átutalások nyomon követésére, nem tudta azokat érzékelni. Az így elküldött tokenek véglegesen csapdába estek, mindenféle helyreállítási mechanizmus nélkül.

Az Ethereum közösség becslése szerint 2018 közepéig több tízmillió dollár értékű ERC-20 token veszett el véglegesen ezen a módon. Elfogadhatatlan volt olyan fizetési platformot építeni, ahol az átutalások csendben meghiúsulhatnak és megsemmisíthetik a felhasználók pénzét.

## Az ERC-223 megoldás: atomi átutalás értesítéssel

Az ERC-223, amelyet az Ethereum EIPs GitHub hibakövetőjén javasoltak, a csendes veszteség problémáját azzal orvosolta, hogy megváltoztatta, mit kellett egy tokenátutalásnak megtennie. Az ERC-223 keretében a `transfer(address _to, uint256 _value, bytes _data)` ellenőrizte, hogy a fogadó cím tartalmaz-e szerződéskódot. Ha igen, az átutalás meghívta a `_to.tokenFallback(address _from, uint256 _value, bytes _data)` függvényt.

A kritikus tulajdonság: ha a fogadó szerződés nem implementálta a `tokenFallback` függvényt, az egész átutalási tranzakció visszagördült. Egyetlen token sem hagyta el a küldő egyenlegét. Egyetlen token sem esett csapdába. Az átutalás atomi volt: vagy teljesült a fogadó kódjának végrehajtásával, vagy teljesen meghiúsult, változatlan állapottal.

Az EXTC szempontjából ez a következőt jelentette:

- **Az okosszerződéseknek küldött fizetés konstrukció szerint biztonságos volt.** A letéti szerződések, a többaláírásos pénztárcák és a hitelezési szerződések fogadhattak EXTC tokeneket anélkül, hogy a pénzeszközök visszafordíthatatlan elvesztésének bármilyen kockázata állt volna fenn.
- **A `_data` mező gazdag fizetési metaadatokat tett lehetővé.** A bájtokból álló hasznos teher számlahivatkozásokat, útvonalkódokat vagy megfelelőségi tanúsítványokat hordozhatott, olyan információt, amelyet egy egyszerű ERC-20 átutalás nem tudott közvetíteni.
- **A gázköltségek marginálisan magasabbak voltak.** A `tokenFallback` meghívása átutalásonként hozzávetőleg 2000–5000 gázt adott hozzá, ami a 2018-as gázárak mellett csekély többletköltség volt.

## Az EXTC szerződésarchitektúrája

Az EXTC token-szerződés egy öt modul köré szervezett Solidity-implementáció volt:

### 1. Tokenidentitás

```
string public name = "Express Transaction Credits";
string public symbol = "EXTC";
uint8 public decimals = 18;
```

A tizennyolc tizedesjegy centnél kisebb pontosságot adott az EXTC-nek, ami megfelelt a mikrofizetési és mikrohitelezési felhasználási esetekhez szükséges felbontásnak. Az `EXTC` szimbólum volt a token-szerződésben regisztrált láncon belüli azonosító.

### 2. Rögzített teljes kínálat

A teljes kínálat a szerződés telepítésekor került beállításra, és későbbi kibocsátásokkal nem lehetett felfújni. Ez a tervezési döntés deflációssá tette az EXTC-t: minden véglegesen forgalomból kivont token, visszafordíthatatlan égetési műveletek révén, pótlás nélkül csökkentette a kínálatot. A rögzített kínálati modell szabványos volt a 2018-as fizetésitoken-tervekben, tükrözve a Bitcoin által befolyásolt feltételezést, miszerint a deflációs nyomás előnyös tulajdonság egy csereeszköz számára.

### 3. ERC-223-kompatibilis egyenleg és átutalás

Az alapvető átutalási függvény a teljes ERC-223 interfészt implementálta. Belső egyenleg-leképezések követték nyomon az egyes címek birtokállományát. Az `isContract(address)` segédfüggvény megkülönböztette az EOA (externally owned account) címeket a szerződéscímektől, hogy eldöntse, meg kell-e hívni a `tokenFallback` függvényt.

### 4. Többaláírásos vállalati kifizetések

A vállalati fizetési munkafolyamatok együttes engedélyezést igényeltek: egyetlen aláíró sem kezdeményezhetett egyoldalúan egy meghatározott küszöb feletti kifizetést. Az EXTC szerződés kettő-N típusú többaláírásos sémát valósított meg:

1. Egy kijelölt kezdeményező javasolt egy átutalást, megadva a címzettet, az összeget és egy nonce-t.
2. Egy társaláíró megerősítette a nonce-t.
3. Az átutalás csak azután hajtódott végre, hogy mindkét aláírás rögzítésre került a láncon.

Ez kiküszöbölte a vállalati számlák egyetlen hibapontból eredő kockázatát, miközben az egész engedélyezési folyamatot a láncon és auditálhatóan tartotta, elszámolóházi közvetítő nélkül.

### 5. Blokkmagasság szerint időzárolt tartós megbízások

Az ismétlődő fizetések, a fizetések, előfizetések, ütemezett hiteltörlesztések, tartós megbízási primitívet igényeltek. Az EXTC ezt időzárként valósította meg: egy átutalási rekord egy `releaseBlock` paraméterrel tárolódott a szerződésben. Az átutalás nem hajtódhatott végre, amíg az Ethereum blokkmagassága el nem érte a `releaseBlock` értéket.

A blokkmagasság mint időhelyettesítő pragmatikus választás volt 2018-ban. Az Ethereum 15 másodperces blokk-intervallumot célzott meg, ezáltal a blokkmagasság néhány perces tartományon belül ésszerűen megbízható helyettesítője volt a valós időnek. Az abszolút időbélyegek (`block.timestamp`) rendelkezésre álltak, de egy ±900 másodperces ablakon belül ki voltak téve a bányászok manipulációjának, ami a blokkmagasságot tette a biztonságosabb hivatkozássá a pénzügyi szerződések számára.

## A fedezetalapú azonnali hitel mechanizmusa

Az EXTC hitelezési primitívje volt a legösszetettebb komponens. A terv:

1. **A hitelfelvevő zárolja a fedezetet.** A hitelfelvevő meghívta a `lockCollateral(uint256 _collateralAmount)` függvényt, EXTC tokeneket utalva a hitelezési szerződés letétjébe egy ERC-223 `tokenFallback` révén.
2. **Hitel/fedezet arány ellenőrzése.** A szerződés beolvasott egy előre konfigurált LTV-arányt (pl. 50%), és kiszámította a maximális hitelösszeget a zárolt fedezethez képest.
3. **Atomi hitelfolyósítás.** Ha a fedezet elérte a minimumküszöböt, a szerződés azonnal átutalta a hitelösszeget a hitelfelvevő címére. Nincs jóváhagyási sor, nincs hitelbizottság, nincs elszámolási késedelem.
4. **Törlesztés és felszabadítás.** Törlesztéskor, a tőke plusz egy rögzített kamatláb, a szerződés visszaadta a fedezetet a hitelfelvevőnek. A `releaseBlock` időpontjáig történő törlesztés elmulasztása automatikus felszámolást váltott ki: a szerződés átutalta a fedezetet a hitelező kijelölt címére.

Az egész folyamatot szerződéskód érvényesítette. Egyik félnek sem kellett megbíznia a másikban, sem közvetítőre támaszkodnia a feltételek érvényesítéséhez.

## Amit a kísérlet feltárt

Az EXTC szerződésarchitektúrája technikailag koherens volt. Az ERC-223 megoldotta az ERC-20 legsúlyosabb biztonsági hibáját. A többaláírásos és időzáras primitívek közvetlenül leképeződtek a valós vállalati fizetési munkafolyamatokra. A fedezeti hitel mechanizmusa bebizonyította, hogy a fedezett hitelezés teljesen automatizálható és önérvényesítővé tehető a láncon.

Két korlát mutatkozott meg a gyakorlatban:

**Gázköltségek.** A 2018 januári csúcson az Ethereum gázárai elérték az 50–100 gwei-t, ami egyetlen ERC-223 tokenátutalás költségét 0,50–2,00 dollárra emelte. A 10–50 dolláros mikrofizetések vagy utalások esetében ezek a díjak prohibitívek voltak.

**Áteresztőképesség.** Az Ethereum főhálózat blokkonkénti gázkorlátja 2018 elején hozzávetőleg 8 millió gáz volt. Egy ERC-223 átutalás nagyjából 50 000–80 000 gázt fogyasztott. A hálózat így blokkonként hozzávetőleg 100–160 EXTC tokenátutalást tudott feldolgozni, azaz nagyjából 7–11-et másodpercenként a 15 másodperces blokk-intervallum mellett. A fizetési hálózati méret, másodpercenként több száz vagy több ezer tranzakció, nem volt elérhető a nyilvános Ethereumon olyan Layer-2 infrastruktúra nélkül, amely akkor még nem létezett üzemi formában.

Ezek infrastrukturális korlátok voltak, nem az EXTC tervezési hibái. A szerződéslogika helyes volt. Az alapul szolgáló blokklánc még nem tudta pénzügyi ágazati léptékben támogatni a fizetési forgalmat.

## Az ötletek, amelyek elérték a gyártást

Az EXTC több tervezési mintáját is megerősítette a későbbi fejlődés:

**Atomi tokenátutalás fogadói értesítéssel**, az ERC-223 alapvető tulajdonsága, az ERC-777 (2019) alapjává vált, amely kiterjesztette az értesítési modellt, és amelyet később DeFi hitelezési protokollokba építettek be. A `tokenFallback` minta a modern DeFi architektúra egészében megjelenik.

**Többaláírásos engedélyezés vállalati kifizetésekhez**, az a minta, amely a végrehajtás előtt több láncon belüli aláírást követel meg, a DAO-kincstárkezelés és az intézményi letétkezelési megoldások szabványos modelljévé vált. A 2018-ban indult Gnosis Safe népszerűsítette ezt a mintát nagy léptékben.

**Fedezetalapú azonnali hitelek közvetítők nélkül**, a fedezet letétbe zárásának és a hitelösszeg atomi felszabadításának mechanizmusa, az olyan DeFi hitelezési protokollok alapvető terve, mint a Compound (2018) és az Aave (2020).

**Blokkmagasság-alapú időzárak ütemezett fizetésekhez**, a jövőbeli végrehajtási időzítés szerződésbe kódolásának mintája, megjelenik a token-vesting szerződésekben, a késleltetett kormányzási javaslatokban és az idősúlyozott átlagár (TWAP) orákulum-tervekben a DeFi ökoszisztéma egészében.

Az EXTC kísérlet nem érte el a gyártási léptéket. A terv életképessé tételéhez szükséges infrastruktúrának további három-öt évre volt szüksége, hogy megérjen. A kérdések, amelyeket a terv felvetett, 2018 számára a helyes kérdések voltak.

## Gyakran ismételt kérdések

**Miért nem terjedt el az ERC-223 mint meghatározó token-szabvány, annak ellenére, hogy orvosolta az ERC-20 hibáját?**

Az ERC-223 megkövetelte, hogy a fogadó szerződések implementálják a `tokenFallback` függvényt, megtörve a visszafelé kompatibilitást az ERC-20 tokenekhez már telepített ezernyi szerződéssel. A meglévő ERC-20 ökoszisztéma túl nagy volt a migrációhoz. A későbbi javaslatok, nevezetesen az ERC-777 és az ERC-1363, ugyanezt a problémát különböző kompatibilitási kompromisszumokkal kezelték, de az ERC-20 a hálózati hatások és a csendes veszteség forgatókönyvét elkerülő becsomagolt token-minták bevezetésének kombinációja révén megmaradt meghatározónak.

**Mi történt az EXTC tokennel és platformmal?**

Az EXTC egy 2018-as koncepcióbizonyíték és korai kutatási projekt volt. A szélesebb ICO- és fizetésitoken-piac 2018–2019 folyamán erősen összezsugorodott, ahogy az Ethereum skálázhatósági korlátai és a szabályozási bizonytalanság világossá vált. Az EXTC tervbe ágyazott ötletek olyan későbbi protokollokban bukkantak fel újra, amelyek hozzáféréssel bírtak Layer-2 infrastruktúrához, jobb eszközkészlethez és világosabb szabályozási keretekhez.

**Hogyan viszonyul az EXTC fedezeti hitelmodellje a modern DeFi protokollokhoz, például az Aave-hez?**

Az alapvető mechanizmus ugyanaz: fedezet zárolása, egy LTV-arány szerint méretezett hitel felvétele, törlesztés vagy felszámolás. A különbségek: (1) a modern DeFi protokollok orákulum-árfolyamokat használnak a dinamikus LTV-hez a rögzített arányok helyett; (2) algoritmikus kamatlábakat alkalmaznak, amelyek reagálnak a poolkihasználtságra; (3) Layer-2 hálózatokon működnek, ahol a gázköltségek 10–100-szor alacsonyabbak, mint a 2018-as főhálózaton; (4) az Aave és a Compound formális biztonsági auditokon esett át, és több milliárd dollárnyi likviditást tartott, empirikus igazolást nyújtva arra, hogy az alapmodell megbízható.

**Milyen Solidity-verziós korlátok álltak fenn 2018 elején?**

Az EXTC szerződés a Solidity 0.4.x verzióra íródott, amely 2018 elején a meghatározó verzió volt. A Solidity 0.4-ből sok, a későbbi verziókban bevezetett biztonsági funkció hiányzott: egész számok túlcsordulásának ellenőrzése (automatikusan hozzáadva a 0.8.0-ban), `require`/`revert` hibaüzenetekkel (korlátozottan a 0.4-ben), és explicit függvény-láthatóság (az alapértelmezett a 0.4-ben a public volt). A szerződés az OpenZeppelin SafeMath könyvtárára támaszkodott a túlcsordulás elleni védelemhez, ami gyakori minta volt, mielőtt a fordító natívan érvényesítette volna ezt.

## Hivatkozások

- Ethereum Foundation, (2015). [EIP-20: Token Standard ⧉](https://eips.ethereum.org/EIPS/eip-20 "EIP-20 Token Standard").
- Dexaran, Ethereum GitHub, (2017). [ERC-223 Token Standard Proposal ⧉](https://github.com/ethereum/EIPs/issues/223 "ERC-223 discussion").
- OpenZeppelin, (2018). [OpenZeppelin Contracts - SafeMath ⧉](https://github.com/OpenZeppelin/openzeppelin-contracts "OpenZeppelin Contracts").
- Ethereum Foundation, (2014). [Ethereum Whitepaper ⧉](https://ethereum.org/whitepaper "Ethereum Whitepaper").

