---
title: "A blockchain mögötti technológia megértése"
tags: "blockchain, Ethereum, smart contracts, cryptography, Merkle tree, consensus mechanism, proof of work, EVM, Solidity, ERC-20, decentralised finance, ISO 20022, post-quantum cryptography, AI, stablecoins, tokenised deposits"
subtitle: "Gyakorlati áttekintés a blockchain mögött álló kriptográfiáról és konszenzusról."
description: "Technikai bevezetés a blockchain működésébe: kriptográfiai hash-láncok, Merkle-fák, elosztott konszenzus, és annak megvilágítása, hogy az Ethereum programozható rétege miként alakított át egy fizetési főkönyvet az okosszerződések és tokenizált eszközök platformjává."
date: "Jan 09, 2018"
language: "hu"
locale: "hu_HU"
banner: "https://cloudcdn.pro/stocks/images/adam-smigielski-K5mPtONmpHM.webp"
banner_alt: "Absztrakt digitális főkönyvi blokkok, amelyeket fénycsíkok kötnek össze sötét háttéren"
keywords: "blockchain-technológia, kriptográfiai hash, Merkle-fa, elosztott konszenzus, munkabizonyíték, Ethereum, okosszerződések, EVM, Solidity, ERC-20, elosztott főkönyv, decentralizált pénzügyek"
---

![Absztrakt digitális főkönyvi blokkok, amelyeket fénycsíkok kötnek össze sötét háttéren](https://cloudcdn.pro/stocks/images/adam-smigielski-K5mPtONmpHM.webp).class=\"img-fluid clearfix\"

## A blockchain mögötti technológia megértése

Technikai bevezetés a blockchain működésébe: kriptográfiai hash-láncok, Merkle-fák, elosztott konszenzus, és annak megvilágítása, hogy az Ethereum programozható rétege miként alakított át egy egyszerű fizetési főkönyvet az okosszerződések és tokenizált eszközök platformjává.

> **Vezetői összefoglaló / Legfontosabb tanulságok**
>
> - **A probléma.** A digitális készpénzhez meg kell oldani a kétszeres költés problémáját: annak megakadályozását, hogy ugyanazt az egységet kétszer költsék el megbízható elszámolóház nélkül. A Bitcoin 2008-as tanulmánya ezt úgy oldotta meg, hogy a megbízható közvetítőket kriptográfiai bizonyítékkal és elosztott konszenzussal váltotta fel ([Nakamoto, 2008](https://bitcoin.org/bitcoin.pdf "Bitcoin: A Peer-to-Peer Electronic Cash System")).
> - **Az adatszerkezet.** A blockchain blokkok láncolt listája, amelyben minden blokk fejléce tartalmazza az előző fejléc SHA-256 hash-ét. A hash-lánc a történelmet csak hozzáfűzhetővé teszi: bármely múltbeli blokk módosítása érvényteleníti az összes ezt követő hash-t, ami arra kényszeríti a támadót, hogy újra elvégezze az összes ezt követő munkabizonyítékot.
> - **Merkle-fák.** A blokkon belüli tranzakciók egy bináris Merkle-fába kerülnek hash-elésre. A blokk fejlécében tárolt gyökér-hash lehetővé teszi bármely egyedi tranzakció hatékony ellenőrzését a teljes blokk letöltése nélkül; ez a könnyűsúlyú SPV-kliensek alapja.
> - **Az Ethereum kiterjesztése.** Az Ethereum Yellow Paper (2014) bemutatta az EVM-et, egy determinisztikus veremgépet, amely minden teljes csomóponton fut. Az okosszerződések a láncra telepített bájtkódok; minden csomóponton azonosan hajtódnak végre, és atomi módon zárulnak le, önérvényesítő kóddal váltva fel a megbízható közvetítőket ([Wood, 2014](https://ethereum.github.io/yellowpaper/paper.pdf "Ethereum Yellow Paper")).
> - **Gyakorlati jelentőség.** Minden 2017 óta telepített tokenizált eszköz, stablecoin és DeFi-protokoll ezekre az alapokra épül. A hash-lánc, a Merkle-fa és az EVM végrehajtási modelljének megértése előfeltétele bármely Ethereum-alapú rendszerrel való munkának.

---

## A probléma, amelyet a blockchain megoldott

A Bitcoin előtt a digitális fizetésekhez megbízható közvetítőre volt szükség, például bankra, fizetésfeldolgozóra vagy elszámolóházra, a kétszeres költés megakadályozása érdekében. Ha Alice egy 10 fontot megtestesítő digitális fájlt küldött Bobnak, magában a fájlban semmi sem akadályozta meg abban, hogy egy azonos másolatot küldjön Carolnak. A megoldás minden létező rendszerben a központosított nyilvántartás volt: a bank főkönyve szerint a pénzt elköltötték, így azt nem lehetett újra elkölteni.

A Bitcoin hozzájárulása az volt, hogy ezt a megbízható főkönyvet egy elosztottra cserélte, amelyben az összes tranzakció nyilvántartása több ezer független csomóponton replikálódik. A csomópontok közötti kölcsönös bizalmatlanságot két mechanizmus alakította biztonsággá:

1. **Kriptográfiai összekapcsolás.** Minden tranzakcióblokk tartalmazza az előző blokk hash-ét. A hash-függvény egyirányú, determinisztikus leképezés: bármely bemenetre a függvény rögzített hosszúságú kimenetet állít elő, és a bemenet akár egyetlen bitjének megváltoztatása is teljesen eltérő kimenetet eredményez. Ez azt jelenti, hogy egy múltbeli blokk bármely módosítása érvényteleníti az utána következő összes blokkot.

2. **Munkabizonyíték-konszenzus.** Egy új blokk hozzáadásához olyan nonce-értéket kell találni, amelynél a blokk hash-e egy célküszöb alá esik; ezt számításigényes megtalálni, de triviálisan olcsó ellenőrizni. Ez a történelem újraírását a módosítandó blokk mélységével arányosan drágává teszi, mivel a támadónak újra el kell végeznie az összes munkabizonyítékot az adott blokktól a lánc csúcsáig.

A kombináció azt jelenti, hogy a legtöbb halmozott munkabizonyítékkal rendelkező leghosszabb lánc a felépítéséből adódóan az, amelyet valós erőforrásokat felhasználó becsületes résztvevők tartanak fenn.

## A kriptográfiai építőelemek

A blockchain-technológia három, már korábban is létező kriptográfiai primitívet illeszt össze egy új architektúrába:

### SHA-256 hash-függvények

A SHA-256 (Secure Hash Algorithm 256-bit) a NIST által szabványosított SHA-2 család tagja. Tetszőleges hosszúságú bemenetet fogad, és 256 bites kimenetet állít elő. A blockchain-használat szempontjából kulcsfontosságú tulajdonságai:

- **Determinisztikus.** Ugyanaz a bemenet mindig ugyanazt a kimenetet eredményezi.
- **Ősképellenállás.** Egy adott hash-kimenetből a bemenet rekonstruálása számításilag kivitelezhetetlen.
- **Lavinahatás.** A bemenet egyetlen bitjének megváltoztatása a kimeneti bitek nagyjából felét megváltoztatja, ami hatékonytalanná teszi a nyers erővel történő keresést.
- **Ütközésellenállás.** Számításilag kivitelezhetetlen két különböző olyan bemenetet találni, amely ugyanazt a hash-t eredményezi.

A Bitcoin kétszer alkalmazza a SHA-256-ot (SHA-256d) a hosszkiterjesztéses támadásokkal szembeni fokozott biztonság érdekében. Az Ethereum a Keccak-256-ot használja, amely egy SHA-3 döntős változat.

### Merkle-fák

A Merkle-fa hash-ek bináris fája. Minden levélcsomópont egy tranzakció hash-e. Minden belső csomópont a két gyermekének hash-e. A gyökér, azaz a Merkle-gyökér, a blokk összes tranzakcióját egyetlen, a blokk fejlécében tárolt 32 bájtos értékben foglalja össze.

A gyakorlati következmény: annak igazolásához, hogy egy adott tranzakció szerepel egy blokkban, csak `log₂(n)` hash-re van szükség, nem pedig mind az `n` tranzakcióra. Egy 2000 tranzakciót tartalmazó blokk esetében az ellenőrzéshez 11 hash szükséges 2000 helyett; ez az egyszerűsített fizetésellenőrzés (SPV) alapja a könnyűsúlyú kliensekben.

### Digitális aláírások (ECDSA)

A Bitcoinban és az Ethereumban a tranzakciók engedélyezése az elliptikus görbén alapuló digitális aláírási algoritmust (ECDSA) használja a secp256k1 görbe felett. Egy privát kulcs aláír egy tranzakciót; bármely csomópont ellenőrizni tudja az aláírást a megfelelő nyilvános kulccsal, anélkül hogy ismerné a privát kulcsot. Ez biztosítja, hogy csak a privát kulcs birtokosa engedélyezhet költést egy címről.

Az Ethereum-címek a nyilvános kulcs Keccak-256 hash-ének utolsó 20 bájtját jelentik; ez a származtatás kompakttá és hordozhatóvá teszi a címeket, miközben kriptográfiailag a kulcspárhoz kötve maradnak.

## Hogyan működik a Bitcoin blockchain

Egy Bitcoin-blokk három logikai összetevőt tartalmaz:

**A blokk fejléce:** 80 bájt, amely a következőket tartalmazza: a protokoll verziója, az előző blokk fejlécének hash-e, a tranzakciók Merkle-gyökere, egy Unix időbélyeg, az aktuális nehézségi célérték és a nonce. A bányászok addig iterálják a nonce-ot (és néha az időbélyeget vagy a coinbase-tranzakció extra nonce-át), amíg a fejléc kétszeres SHA-256 hash-e a nehézségi célérték alá nem esik.

**A tranzakciólista:** a blokkban szereplő tranzakciók rendezett halmaza. A coinbase-tranzakció (az első) a blokkjutalmat és a tranzakciós díjakat a bányász címére rendeli.

**A lánc:** a fejlécek összekapcsolása. A láncban felhalmozott munkabizonyíték (az összes blokk létrehozásához elvégzett munka összege) határozza meg, melyik elágazás a kanonikus lánc. A csomópontok mindig a legtöbb halmozott munkát tartalmazó láncot követik.

A blokkidő célértéke a Bitcoin esetében 10 perc. A nehézség 2016 blokkonként (körülbelül kéthetente) igazodik, hogy fenntartsa ezt a célértéket a teljes hálózati hash-ráta változásaival.

## Az Ethereum programozható rétege

Az Ethereum a Bitcoin tranzakciós modelljét az „érték átvitele” szintjéről a „kód végrehajtása” szintjére általánosította. A legfontosabb kiegészítések:

**Az Ethereum virtuális gép (EVM).** 256 bites szavakkal dolgozó, veremalapú virtuális gép, amely minden teljes csomóponton determinisztikusan hajtódik végre. Minden operációs kódnak (opcode) explicit gázköltsége van. A számítást a blokk gázkerete korlátozza, megakadályozva, hogy végtelen ciklusok megállítsák a hálózatot. Minden csomópontnak, amely ugyanazt a bájtkódot ugyanazon az állapoton hajtja végre, ugyanazt a kimenetet kell előállítania; a végrehajtásra vonatkozó konszenzus teszi az okosszerződéseket bizalommentessé.

**Fiókok.** Az Ethereum két fióktípussal rendelkezik: a privát kulcsokkal vezérelt, külső tulajdonú fiókok (EOA-k) és a szerződésfiókok, amelyek kódja a láncon van tárolva. Egy szerződés címére küldött tranzakció elindítja a szerződés bájtkódjának végrehajtását.

**Állapot.** Az Ethereum globális állapota a címek leképezése a fiókállapotokra (nonce, egyenleg, tárhely, kódhash). Az állapotgyökér, amely az összes fiókállapot Merkle-Patricia-trie-je, minden blokk fejlécében szerepel, lehetővé téve bármely fiók állapotának hatékony igazolását bármely blokkmagasságon.

**Gáz.** A felhasználók minden EVM-műveletért gázt fizetnek (ETH-ban). A gáz két funkciót lát el: kompenzálja a bányászokat/validátorokat a számításért, és korlátozza az erőforrásokat, amelyeket egyetlen tranzakció felhasználhat, megelőzve a költséges műveleteken keresztüli szolgáltatásmegtagadásos támadásokat.

## Okosszerződések írása Solidityben

A Solidity egy statikusan típusos, szerződésorientált nyelv, amely EVM-bájtkódra fordul. Egy minimális token-szerződés szemlélteti az alapfogalmakat:

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

Fontos megfigyelések: a `mapping(address => uint256)` egy EVM-tárolási elrendezés, nem pedig memóriabeli adatszerkezet; az olvasások és írások gázba kerülnek. A `require` hiba esetén visszavonja a teljes tranzakciót, visszaadva a fel nem használt gázt. Az `event Transfer` olyan naplóbejegyzést bocsát ki, amelyet a láncon kívüli indexelők a transzferek nyomon követésére használnak anélkül, hogy újraolvasnák a teljes állapotot. A `constructor` egyszer fut le a telepítéskor; a további hívások a megnevezett függvényekhez kerülnek.

Az ERC-20 szabvány közös interfészt formalizált a helyettesíthető tokenekhez (`transfer`, `transferFrom`, `approve`, `allowance`, `balanceOf`, `totalSupply`), lehetővé téve, hogy bármely ERC-20-kompatibilis token bármely ERC-20-tudatos tőzsdével vagy tárcával működjön egyedi integráció nélkül.

## A főkönyvtől a pénzügyi infrastruktúráig

Az itt leírt blockchain-primitívek (hash-láncok, Merkle-fák, az EVM és az ERC-20) 2018 és 2026 között a pénzügyi alkalmazások szélesebb körének alapjává váltak:

**Decentralizált pénzügyek (DeFi).** A hitelezési protokollok (Compound, Aave), az automatizált piaci árjegyzők (Uniswap) és a hozamaggregátorok mind EVM-okosszerződésként futnak. A hagyományos pénzügyi közvetítők elszámolási, letéti és kiegyenlítési funkcióit önvégrehajtó kóddal és láncon belüli likviditási poolokkal váltják fel.

**Tokenizált eszközök.** A központi bankok és a kereskedelmi bankok tokenizált betéteket, tokenizált kötvényeket és tokenizált pénzpiaci alapokat tesztelnek az EVM-kompatibilis láncok engedélyhez kötött változatain. Az alapul szolgáló mechanizmusok, azaz a hash-szel biztosított állapotátmenetek, az atomi kiegyenlítés és a programozható transzferszabályok, a 2014-es Ethereum-architektúra közvetlen leszármazottai.

**Központi banki digitális valuták.** A Bank of England nagybani CBDC-kutatása, az ECB digitális euró programja és a Project Agorá mind olyan DLT-architektúrákat vizsgál, amelyek a Bitcoin és az Ethereum alapvető terveiből származnak, vagy azokkal kompatibilisek. A konszenzus- és hash-lánc-struktúrák akkor is relevánsak maradnak, ahol az engedélyezési és irányítási modell teljesen eltér a nyilvános blockchainektől.

A 2008-as Bitcoin-tanulmánytól a 2026-os tokenizált pénzügyekig tartó út két évtizedet ölel fel, mégis egy koherens technikai leszármazási vonalra épül. Annak megértése, hogy egy SHA-256 hash-lánc miként érvényesíti a megváltoztathatatlanságot, egy Merkle-fa miként teszi lehetővé a hatékony ellenőrzést, és az EVM miként hajtja végre atomi módon az okosszerződéseket, előfeltétele annak, hogy értékelni tudjunk bármely állítást arról, mire képes és mire nem a blockchain a szabályozott pénzügyi szolgáltatásokban.

## Gyakran ismételt kérdések

**Mi a különbség a blockchain és az elosztott adatbázis között?**

A hagyományos elosztott adatbázis a rendelkezésre állás és a teljesítmény érdekében replikálja az adatokat a csomópontok között, de a bizalom központosított: egy rendszergazda módosíthatja a rekordokat. A blockchain a hash-láncolással és a konszenzussal számításigényessé teszi a manipulációt: bármely múltbeli rekord módosításához újra el kell végezni az összes ezt követő munkabizonyítékot vagy tétbizonyítékot, és rá kell venni a hálózatot, hogy elfogadja a módosított elágazást. A megkülönböztető tulajdonság a manipuláció felismerhetősége, amelyet a kriptográfia és az ösztönzőtervezés érvényesít, nem pedig a hozzáférés-vezérlés.

**Miért használ az Ethereum Keccak-256-ot a SHA-256 helyett?**

Az Ethereum részben azért választotta a Keccak-256-ot (a SHA-3 döntősét a NIST szabványosítási módosításai előtt), mert tervezői függetlenséget akartak a SHA-2 vonaltól, amelytől a Bitcoin már függött. A Keccaknak emellett eltérő algebrai tulajdonságai vannak, amelyek vonzóvá tették bizonyos EVM-műveletekhez. A fejlesztők számára a gyakorlati hatás az, hogy az Ethereum-címek származtatása és a tárhelyrések hash-elése Keccak-256-ot használ, nem pedig SHA-256d-t, mint a Bitcoin.

**Mit előz meg a „gáz” az EVM-ben?**

A gáz kétféle támadást előz meg. Először is megakadályozza a számításigényes műveleteken keresztüli szolgáltatásmegtagadást: minden operációs kód gázba kerül, így a támadó nem kényszerítheti a hálózatot arra, hogy ingyen hajtson végre végtelen ciklusokat. Másodszor, a blokk gázkerete korlátozza a blokkonkénti teljes számítást, biztosítva, hogy a blokkellenőrzés ideje korlátozott és kiszámítható maradjon a teljes csomópontok számára. Gáz nélkül egyetlen szerződéshívás megállíthatná a hálózatot azáltal, hogy korlátlan számítást hajt végre.

**Hogyan változtatja meg a tétbizonyíték a biztonsági modellt a munkabizonyítékhoz képest?**

A munkabizonyíték esetében a biztonságot az energiaráfordítás nyújtja: a lánc megtámadásához a hálózat hash-rátájának több mint 50%-át kell ellenőrizni, ami a fizikai hardver és energia több mint 50%-ának ellenőrzését jelenti. A tétbizonyíték esetében (amelyet az Ethereum a 2022-es Merge óta használ) a biztonságot a gazdasági tét nyújtja: a validátorok ETH-t zárolnak fedezetként, amelyet levágnak, ha egymásnak ellentmondó blokkokat írnak alá. Egy 51%-os támadáshoz az összes zárolt ETH több mint 50%-át kell megszerezni és kockáztatni; ez inkább tőkeköltség, mint hardver- és energiaköltség. A biztonsági modell eltérő, de gazdasági értelemben matematikailag összehasonlítható azzal a feltételezéssel, hogy a racionális validátorok a díjbevételt előnyben részesítik a tőke elpusztításával szemben.

## Hivatkozások

- Nakamoto, S., (2008). [Bitcoin: A Peer-to-Peer Electronic Cash System ⧉](https://bitcoin.org/bitcoin.pdf "Bitcoin Whitepaper").
- Buterin, V., (2014). [Ethereum: A Next-Generation Smart Contract and Decentralised Application Platform ⧉](https://ethereum.org/whitepaper "Ethereum Whitepaper").
- Wood, G., (2014). [Ethereum: A Secure Decentralised Generalised Transaction Ledger ⧉](https://ethereum.github.io/yellowpaper/paper.pdf "Ethereum Yellow Paper").
- NIST, (2015). [SHA-3 Standard: Permutation-Based Hash and Extendable-Output Functions ⧉](https://www.nist.gov/publications/sha-3-standard-permutation-based-hash-and-extendable-output-functions "NIST FIPS 202").
