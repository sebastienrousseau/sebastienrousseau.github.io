---
title: "ERC-20: Az Ethereum tokeninterfész, amely megváltoztatta a világot"
tags: "ethereum, erc20, eip, tokens, contracts, blockchain, cryptocurrencies, smart-token, solidity, ISO 20022, post-quantum cryptography, AI, stablecoins"
subtitle: "ERC-20 tokenek, Ethereum okosszerződések és a digitális eszközök szabványosítása."
description: "ERC-20: Az ERC-20 a leggyakrabban használt tokentípus az Ethereum blokkláncon, és gyakran okosszerződés-alapú digitális szerződésként hivatkoznak rá."
date: "Jan 24, 2018"
language: "hu"
locale: "hu_HU"
banner: "https://cloudcdn.pro/stocks/images/m-ZzOa5G8hSPI.webp"
banner_alt: "Kikapcsolt laptop egy barna faasztalon"
keywords: "ethereum, erc20, eip, tokenek, szerződések, blokklánc, kriptovaluták, smart-token, solidity"
---

## ERC-20: Az Ethereum tokeninterfész, amely megváltoztatta a világot

Az ERC-20 a leggyakrabban használt tokentípus az Ethereum blokkláncon, és gyakran okosszerződés-alapú digitális szerződésként hivatkoznak rá.

> **Legfontosabb tanulságok**
>
> - **Ötlet.** Az ERC-20 szabvány hat alapvető függvényt határoz meg, amelyeket minden ERC-20 kompatibilis tokennek meg kell valósítania.
> - **Hatás.** Az ERC-20 szabvány jelentős hatást gyakorolt az Ethereum ökoszisztémára.
> - **Ösztönző.** Az ERC-20 protokoll által létrehozott szabványosítás közvetlen gazdasági hatással is járt.
> - **A szabványosított tokeninterfész szükségessége.** Az ERC-20 (Ethereum Request for Comments 20) szabvány megjelenése előtt az Ethereum blokklánc olyan volt, mint a tokenarchitektúrák vadnyugata.

![Nagyon magas épület, amelyen sok lyuk van](https://cloudcdn.pro/stocks/images/m-ZzOa5G8hSPI.webp).class=\"img-fluid clearfix\"

## Betekintés

### A szabványosított tokeninterfész szükségessége

Az ERC-20 (Ethereum Request for Comments 20) szabvány megjelenése előtt az Ethereum blokklánc olyan volt, mint a tokenarchitektúrák vadnyugata. Minden újonnan kibocsátott token saját, egyedi szabály-, függvény- és interfészkészlettel rendelkezett. Ez nemcsak ijesztő tanulási görbét jelentett a fejlesztők számára, hanem a tokenek együttműködési képességét is akadályozta. Lényegében minden új token olyan volt, mint egy új nyelv, amelyet meg kellett tanulni, megérteni és megvalósítani. Ez a széttöredezettség gátolta a tokenek skálázhatóságát és széles körű elterjedését az Ethereum platformon.

Az ERC-20 szabvány bevezetése egységesítő nyelvként hatott, közös szabály- és függvénykészletet állapítva meg, amelyet minden Ethereum tokennek be kell tartania. A fejlesztők immár egységes interfészen dolgozhatnak, függetlenül attól, hogy melyik tokenről van szó. Ez a szabványosítás leegyszerűsítette a tokenekkel való interakció folyamatait, lehetővé téve a zökkenőmentesebb integrációt különféle alkalmazásokba és szolgáltatásokba. Ennek eredményeként a fejlesztők érdemibb módon dolgozhatnak a tokenekkel, olyan környezetet teremtve, amely elősegíti az innovációt és a növekedést az Ethereum ökoszisztémán belül.

#### A tokenarchitektúrák vadnyugata

Az Ethereum blokkláncot eredetileg egyetlen tokentípus, az ETH támogatására tervezték. Ahogy azonban a platform népszerűsége nőtt, a fejlesztők elkezdtek saját tokeneket létrehozni, hogy sokféle eszközt és fogalmat képviseljenek. Ez különféle tokenarchitektúrák elszaporodásához vezetett, amelyek mindegyike saját, egyedi szabály- és függvénykészlettel rendelkezett.

Ez a széttöredezettség megnehezítette a fejlesztők számára olyan alkalmazások létrehozását, amelyek több tokennel is képesek együttműködni. Ugyancsak megnehezítette a felhasználók számára, hogy tokeneszközeiket különböző platformokon kezeljék.

#### Az ERC-20 szabvány

Az ERC-20 szabványt 2015-ben vezették be, hogy kezeljék a tokenarchitektúrák vadnyugata által támasztott kihívásokat. A szabvány közös szabály- és függvénykészletet határoz meg, amelyet minden Ethereum tokennek be kell tartania. Ez a szabványosítás megkönnyíti a fejlesztők számára olyan alkalmazások létrehozását, amelyek bármely ERC-20 tokennel képesek együttműködni, és megkönnyíti a felhasználók számára is tokeneszközeik kezelését.

Az ERC-20 szabványt széles körben elfogadta az Ethereum közösség. Ma több mint 200 000 ERC-20 token létezik, és a szabványt az alkalmazások széles köre használja, beleértve a decentralizált tőzsdéket, a hitelezési platformokat és a játék-dappokat.

## Ötlet

### Közös függvény- és tulajdonságkészlet minden token számára

Az ERC-20 szabvány hat alapvető függvényt határoz meg, amelyeket minden ERC-20 kompatibilis tokennek meg kell valósítania. Ezek a függvények a következők:

- `transfer(address to, uint256 amount)`: Átutal egy adott mennyiségű tokent a hívó címéről a megadott címre.
- `approve(address spender, uint256 amount)`: Engedélyezi a megadott cím számára, hogy a hívó nevében egy adott mennyiségű tokent költsön el.
- `allowance(address owner, address spender)`: Visszaadja azt a tokenmennyiséget, amelynek elköltésére a megadott költő a megadott tulajdonos nevében jogosult.
- `totalSupply()`: Visszaadja a forgalomban lévő tokenek teljes számát.
- `balanceOf(address owner)`: Visszaadja a megadott cím tulajdonában lévő tokenek számát.
- `name()`: Visszaadja a token nevét.
- `symbol()`: Visszaadja a token szimbólumát.

Az ERC-20 szabvány két eseményt is meghatároz, amelyeket a megfelelő függvények sikeres végrehajtásakor ki kell bocsátani. Ezek az események a következők:

- `Transfer(address from, address to, uint256 amount)`: Akkor bocsátódik ki, amikor egy adott mennyiségű token átkerül egyik címről a másikra.
- `Approval(address owner, address spender, uint256 amount)`: Akkor bocsátódik ki, amikor a megadott cím engedélyt kap, hogy a megadott tulajdonos nevében egy adott mennyiségű tokent költsön el.

## Hatás

### A DeFi növekedése és az Ethereum elterjedése

Az ERC-20 szabvány jelentős hatást gyakorolt az Ethereum ökoszisztémára. Kulcsszerepet játszott a DeFi (decentralizált pénzügyek) mozgalom lehetővé tételében, és hozzájárult az Ethereum elterjedésének növekedéséhez is.

A DeFi platformok, amelyek a hitelezéstől a vagyonkezelésig terjedő pénzügyi szolgáltatások sorát kínálják, nagymértékben támaszkodnak a tokenekre a tranzakciók lebonyolításához. Mivel az ERC-20 univerzális adapterként működik, a DeFi alkalmazások számára sokkal egyszerűbbé vált a tokenek széles skálájának beépítése anélkül, hogy mindegyikhez külön kellene szabniuk a kódjukat.

Az ERC-20 szabvány megkönnyítette a felhasználók számára tokeneszközeik kezelését is. Mivel a tokenek ugyanazokat az alapvető szabályokat követik, a felhasználók könnyebben utalhatják át, költhetik el és kezelhetik tokeneszközeiket több platformon keresztül. Ez a jobb felhasználói élmény hajtóerő volt az Ethereum növekvő elterjedési arányában.

## Ösztönző

### Csökkentett fejlesztési költségek és javított biztonság

Az ERC-20 protokoll által létrehozott szabványosítás közvetlen gazdasági hatással is járt. Azzal, hogy tesztelt és a közösség által jóváhagyott tervrajzot biztosított a tokenek létrehozásához, jelentősen csökkentette a fejlesztők belépési korlátait. Immár csökkentett fejlesztési költségekkel és gyorsabb piacra jutással hozhatnak létre új tokent, mivel többé nem kell újra feltalálniuk a kereket. A szabvány közvetve ösztönzi olyan DApp-ok (decentralizált alkalmazások) és szolgáltatások létrehozását is, amelyek univerzálisan képesek együttműködni bármely ERC-20 tokennel, ezáltal élénkebb ökoszisztémát táplálva.

Egy másik figyelemre méltó előny a fokozott biztonság. Az ERC-20 szabvány szigorú vizsgálaton esett át az Ethereum közösség részéről, ami robusztus és biztonságos modellé teszi a tokenek megvalósításához. E szabvány betartása azt jelenti, hogy a token okosszerződésének alapvető elemei megfelelnek a közösség által elfogadott legjobb gyakorlatoknak. Ez minimálisra csökkenti azokat a biztonsági sebezhetőségeket, amelyek egyébként egy nem megfelelően megtervezett tokenmodellből eredhetnének. Bár ez nem jelent garanciát minden típusú sebezhetőség ellen, jelentős lépés a tokenek, és ezáltal az azokat használó projektek általános biztonságának biztosítása felé.

![divider](https://cloudcdn.pro/clients/common/images/elements/divider.svg).class=\"m-10 w-100\"

**Ezzel véget ért a közös időnk. Köszönöm a figyelmét!**

Ha bármilyen kérdése van, kérem, ne habozzon felvenni velem a kapcsolatot a [LinkedIn ⧉][11] oldalon vagy a [Kapcsolat oldalon][10]. Köszönöm ismét a figyelmét, és várom megkeresését.

[**❬ Vissza a cikkekhez**][09]

[09]: /articles/index.html "Vissza a cikkekhez"
[10]: /contact/index.html "Kapcsolat Sebastien Rousseau-val"
[11]: https://www.linkedin.com/in/sebastienrousseau/ "Sebastien Rousseau a LinkedInen"
