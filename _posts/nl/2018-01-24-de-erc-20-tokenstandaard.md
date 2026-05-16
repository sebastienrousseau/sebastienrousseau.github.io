---
title: "De ERC-20-tokenstandaard"
subtitle: "De technische basis van interoperabele tokens op Ethereum"
description: "ERC-20 als interface-standaard die de uitwisselbare token de facto interoperabel maakt op Ethereum-gebaseerde smart contracts."
date: "January 24, 2018"
language: "nl-NL"
locale: "nl_NL"
banner: "https://cloudcdn.pro/stocks/images/m-ZzOa5G8hSPI.webp"
banner_alt: "Visualisatie van ERC-20-tokens binnen het Ethereum-netwerk"
keywords: "ERC-20, Ethereum, smart contracts, tokens, ICO, blockchain, interoperabiliteit"
---
![Ausgeschoudeter Laptop op een braunen Holztisch](https://cloudcdn.pro/stocks/images/m-ZzOa5G8hSPI.webp).class=\"img-fluid clearfix\"

## Overzicht

### De Bedarf aan een gestandaardiseerden Token-Schnittstelle

Vor de Aufkommen des ERC-20-standaards (Ethereum Request for Comments 20) glich de Ethereum-Blockchain een Wilden Westen de Token-Architekturen. Jedes nieuw gecreërene Token had zijn eigenn, einzigartigen Satz aan Regeln, Funktionen en Schnittstellen. Het stelte ontwikkelaars niet alleen vóór een steile Lernkurve, sondern behinderte ook de Interoperabilität de Tokens. Im Gongeveere was ieder nieuwe Token zoals een nieuwe Sprache, de erlernt, vpasanden en implementiert worden moest. Deze Fragmentierung hemmte de schaalbaarheid en de breite acceptatie van Tokens op de Ethereum-platform.

De Einführung des ERC-20-standaards wirkte zoals een vereinheitlichende Sprache en legte een gezamenlijken Satz aan Regeln en Funktionen fest, aan de sich alle Ethereum-Tokens houden moeten. ontwikkelaars verfügen nun over een einheitliche Schnittstelle, onafhankelijk vom jeweiligen Token. Deze standaardisierung heeft de Interaktionsprozesse met Tokens vereenvoudigd en een reibungslosere Integration in verschillende toepassingen en dienste maakt mogelijk. Dadurch kunnen ontwikkelaars bedeutsamer met Tokens arbeiten en een Umfeld creëren, het innovatie en groei in Ethereum-Ökosystem begünstigt.

#### De Wilde Westen de Token-Architekturen

De Ethereum-Blockchain was ursprünglich darauf ausgelegd, een einzigen Token-Typ tot untpasützen: ETH. Mit zunehmender Popularität de platform begannen ontwikkelaars echter, eigen Tokens tot pasellen, um unterschiedlichste activa en concepte abzuvormen. Het führte tot een Vielzahl unterschiedlicher Token-Architekturen, iedere met haar eigenn Regelwerk en haar eigenn Funktionen.

Deze Fragmentierung erschwerte es ontwikkelaarsn, toepassingen tot pasellen, de met mehreren Tokens interagieren konden. U machte es ook voor gebruikers schwierig, haar Token-activa plattformübergrijpend tot verwouden.

#### De ERC-20-standaard

De ERC-20-standaard werd 2015 ingevoerd, um de uitdagingen dit Wilden Westens de Token-Architekturen tot adressieren. De standaard definooitrt een gezamenlijken Satz van Regeln en Funktionen, aan de sich alle Ethereum-Tokens houden moeten. Deze standaardisierung erleichtert es ontwikkelaarsn, toepassingen tot pasellen, de met jedem ERC-20-Token interagieren kunnen, en vereenvoudigd voor gebruikers de Verwoudung haar Token-activa.

De ERC-20-standaard werd van de Ethereum-Community breit übernommen. Heute existieren over 200.000 ERC-20-Tokens, en de standaard kommt in een Vielzahl van toepassingen tot inzet, darunter gedecentraliseerde Börsen, Lending-platformen en Gaming-DApps.

## Idee

### Een gezamenlijker Satz van Funktionen en Eigenschaften voor alle Tokens

De ERC-20-standaard definooitrt sechs essenzielle Funktionen, de alle ERC-20-conformen Tokens implementieren moeten. Deze Funktionen zijn:

- `transfer(address to, uint256 amount)`: Überträgt een Token-Betrag van de Adresse des Aufrufers aan de angegebene Adresse.
- `approve(address spender, uint256 amount)`: Genehmigt de angegebenen Adresse, in Namen des Aufrufers een Token-Betrag auszugeben.
- `allowance(address owner, address spender)`: Gibt zurück, welchen Token-Betrag de angegebene Spender in Namen des angegebenen Eigentümers ausgeben darf.
- `totalSupply()`: Gibt de Gesamtzahl de in Umlauf befindlichen Tokens zurück.
- `balanceOf(address owner)`: Gibt de Anzahl de van de angegebenen Adresse gehoudenen Tokens zurück.
- `name()`: Gibt de Namen des Tokens zurück.
- `symbol()`: Gibt het Symbol des Tokens zurück.

De ERC-20-standaard definooitrt bovendien zwei Events, de bij succesvoler Ausführung de entsprechenden Funktionen uitgeontketent worden moeten:

- `Transfer(address from, address to, uint256 amount)`: Wird uitgeontketent, indien een Token-Betrag van een Adresse aan een andere übertragen wordt.
- `Approval(address owner, address spender, uint256 amount)`: Wird uitgeontketent, indien de angegebenen Adresse de Berechtigung erdeelt wordt, in Namen des angegebenen Eigentümers een Token-Betrag auszugeben.

## impact

### Het groei van DeFi en de adoptie van Ethereum

De ERC-20-standaard heeft het Ethereum-Ökosystem maßgeblich geprägt. Hij was een sleutelfaktor voor de DeFi-Bewegung (Decentralized Finance) en heeft bovendien de verspreiding van Ethereum bevorderd.

DeFi-platformen, de een breites Spektrum aan financiële dienstverlening vom Kreditgeschäft bis tot Vermögensverwoudung anbieden, stützen sich stark op Tokens, um Transaktionen abzuwickeln. Da ERC-20 als universeller Adapter fungiert, is es voor DeFi-toepassingen erheblich einfacher geworden, een Vielzahl van Tokens tot integrieren, zonder de Code voor ieder einzelne anpassen tot moeten.

De ERC-20-standaard heeft es gebruikersn bovendien erleichtert, haar Token-activa tot verwouden. Da sich Tokens aan dieselben Gongeveerregeln houden, fällt es Anwendern leichter, Tokens plattformübergrijpend tot transferieren, auszugeben en tot verwouden. Deze verbeterde gebruikerserfahrung was een drijvender Faktor voor de wachsenden adoptiesraten van Ethereum.

## prikkels

### Geringere ontwikkelingskosten en verbeterde beveiliging

De door het ERC-20-Protokoll gecreërene standaardisierung had ook unmittelbare economische impact. Durch de Bereitstellung een erprobten en van de Community akzeptierten Vorlage voor de Token-Erstellung werden de Einstiegshürden voor ontwikkelaars duidelijk gesenkt. U kunnen nun een nieuwes Token met reduzierten ontwikkelingskosten en kürzerer Time-to-Market pasellen, zonder het Rad nieuw tot erfinden. De standaard fördert indirekt ook de Entstehung van DApps (gedecentraliseerde toepassingen) en diensten, de universell met jedem ERC-20-Token interagieren kunnen, en nährt so een dynamischeres Ökosystem.

Een weiterer bemerkenswerter voordeel is de verbeterde beveiliging. De ERC-20-standaard werd van de Ethereum-Community gründlich geprüft, was ihn tot een robusten en sicheren model voor de Token-Implementierung macht. De Einhoudung dit standaards bedeutet, dat de gongeveerleggenden Aspekte des Smart Contracts een Tokens de van de Community akzeptierten Best Practices folgen. Het minimiert het risico van beveiligingslücken, de sonst uit een unsachgemäß entworfenen Token-model resultieren könnten. Auch indien dies keine Garantie tegen alle Arten van Schwachstellen biedt, is es een belangrijker stap tot Gewährleistung de Gesamtsicherheit de Tokens en daarmee ook de Projekte, de ze benutten.
