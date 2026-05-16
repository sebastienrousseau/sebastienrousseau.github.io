---
title: "De technologie achter blockchain begrijpen"
subtitle: "Cryptografie, consensus en de architectuur van gedecentraliseerde netwerken"
description: "Een toegankelijke gids voor de technologie achter blockchain: cryptografische primitieven, consensusmechanismen en gedistribueerde netwerken."
date: "January 9, 2018"
language: "nl-NL"
locale: "nl_NL"
banner: "https://cloudcdn.pro/stocks/images/adam-smigielski-K5mPtONmpHM.webp"
banner_alt: "Abstracte weergave van blockchain-blokken die met elkaar verbonden zijn"
keywords: "Blockchain, cryptografie, consensus, hashing, proof-of-work, proof-of-stake, gedistribueerd grootboek"
---
![Ausgeschoudeter Laptop op een braunen Holztisch](https://cloudcdn.pro/stocks/images/adam-smigielski-K5mPtONmpHM.webp).class=\"img-fluid clearfix\"

## Overzicht

De blockchaintechnologie heeft de Tür tot een nieuwen Ära gedecentraliseerde toepassingen (dApps) geöffnet, de onafhankelijk en zonder centrale controle laufen. Ethereum biedt een leistungsstarke platform, um komplexe dApps en Smart Contracts tot pasellen.

Een de vielversprechendsten inzetmogelijkkeiten van Ethereum is de Einführung individueller cryptovaluta's en digitaaler Tokens. In deze umfassenden Leitfaden gehen we stap voor stap door, zoals Sie uw eigens Krypto-Token op Ethereum pasellen.

## Idee

Ons Ziel is es, een einfache cryptovaluta op Ethereum aufzubouwen en u daarmee praktische Erfahrung in de Blockchain-ontwikkeling tot vermitteln. Im gevolgenden de belangrijksten stape, de we behandeln:

### De cryptovaluta entwerfen

De pase doorslaggevende Aufgabe bestaat darin, uw cryptovaluta tot entwerfen. Dazu gehört de Definition de belangrijksten Attribute:

- **Name**: Wählen Sie een einzigartigen Namen, de de Identität en de Zweck des Tokens widerspiegelt.
- **Symbol**: Wählen Sie een kurzes Symbol zoals BTC voor Bitcoin. Es wordt aan Börsen gebruikt.
- **Gesamtangebot**: Legen Sie de maximale Anzahl aan in Umlauf befindlichen Tokens fest.
- **Dezimalstellen**: Definooitren Sie de Teilbarkeit Ihres Tokens, ongeveer 2 voor Cent-Einheiten.
- **Zusatzfunktionen**: Ergänzen Sie optional Extras zoals Minting, Burning, Freezing usw.

### Smart Contracts schreiben

Um uw cryptovaluta tot Leben tot erwecken, moeten Sie Smart Contracts programmieren, de de Funktionalität en de Regeln des Tokens definooitren. Smart Contracts zijn programmatische Skripte, de op de Blockchain gespeichert zijn en automatisch ausgeführt worden, sobald bestimmte voorwaarden erfüllt zijn.

Einige centrale Eigenschaften, de Smart Contracts ideal voor cryptovaluta's machen, zijn:

- **Selbstausführend** — ze laufen zonder Beteiligung Dritter automatisch ab, sobald ze uitgeontketent worden.
- **Unveränderlichkeit** — einmal bereitgestelt, kan de Code niet meer geändert worden. Dies sorgt voor beveiliging.
- **Autonomie** — es is keine centrale instantie nötig, um Smart Contracts tot verwouden.
- **Transparenz** — iedere kan de Logik een Smart Contracts einsehen.
- **Automatisierung** — actieen zoals Mittelübertragungen lassen sich over de Vertragscode automatisieren.
- **beveiliging** — Mittel in een Contract zijn gesichert, bis de Freigabebedingungen erfüllt zijn.
- **efficiëntie** — Smart Contracts schouden Intermediäre uit en machen procese sneler en günstiger.

voorbeeldcode voor een Contract in Solidity.

```solidity
pragma solidity ^0.8.0;

contract MyToken {

  string public name;
  string public symbol;
  uint256 public decimals;
  uint256 public totalSupply;

  constructor(string memory _name, string memory _symbol, uint8 _decimals, uint256 _totalSupply) {
    name = _name;
    symbol = _symbol;
    decimals = _decimals;
    totalSupply = _totalSupply;
  }

}
```

Deze einfache Contract erlaubt es, een Token met Eigenschaften zoals Name, Symbol, Dezimalstellen en Gesamtangebot tot pasellen.

De `constructor`-Funktion initialisiert deze Parameter bij Deployment des Contracts.

Dit voorbeeld richtet lediglich gongeveerleggende Token-Eigenschaften een. U würden de Contract uitbreiden, um weitere Funktionen hinzuzufügen, zoals ongeveer:

- Token-Transfers tussen Adressen
- Verwoudung van Guthaben
- Allowances voor het Ausgeben van Tokens
- Minting en Burning van Tokens
- Einfrieren of Sperren van Token-Transfers
- Implementierung van Token-standaards zoals ERC-20
- Bereitstellung en Interaktion met de Contract

### Lokale ontwikkeling en Tests

Bevor Sie uw cryptovaluta op de Ethereum-Blockchain reedstellen, is es ratsam, gründliche lokale Tests durchzuführen. So stellen Sie sicher, dat uw cryptovaluta zoals vorgesehen funktionooitrt, zonder unvorhergesehene Fehler of Schwachstellen.

gevolgen Sie deze stapen, um loszuleggen:

#### Go-Ethereum (Geth) herunterladen

beginen Sie met de Download van [Go-Ethereum][00], ook als Geth bekannt — een in Go geschriebenen Ethereum-Client. Geth is de Command-Line-Interface-(CLI-)Ethereum-Client, de op Windows-, Mac- en Linux-platformen läuft. Es handelt sich um een vielseitiges tool, met de Sie minen, Smart Contracts pasellen en met ihnen in Ethereum-netwerk interagieren kunnen. U kunnen Geth hier herunterladen.

#### Ethereum installieren

Sobald Sie Geth heruntergeladen hebben, fahren Sie met de Installation van Ethereum fort. Detaillierte Voraussetzungen en vollvoortdurende Build-Anleitungen finden Sie in de [Installation Instructions][01] in offiziellen Wiki.

#### Een ontwikkelomgeving inrichten

Um de ontwikkeling uw cryptovaluta tot erleichtern, vereisen Sie een ontwikkelomgeving, een Test-Framework en een Asset-Pipeline voor Ethereum. Detaillierte Anleitungen tot Einrichtung deze unverzichtbaren tools finden Sie in Ethereum-Wiki.

#### Auf een Testnet reedstellen

Sobald uw cryptovaluta de lokalen Tests bestaat, kunnen Sie ze in een Testnet reedstellen. Een Testnet is een sichere en gecontroleerde Umgebung, de het Ethereum-meinnet nachvormt, sodass Sie de Leistung uw cryptovaluta onder realen voorwaarden bewerten kunnen, zonder reale financiële risico's einzugehen.

## impact

Indem Sie een op Ethereum basierende cryptovaluta van Gongeveer op aufbouwen, gewinnen Sie:

- Fundiertes kennis tot gedecentraliseerde toepassingen (dApps) en de Programmierung van Smart Contracts
- Praktische Erfahrung met de Solidity-Programmierung
- Vpasändnis de Konsensprotokolle van Ethereum
- Vertrautheit met Token-standaards zoals ERC-20

Dit kennis befähigt Sie, de blockchaintechnologie voor innovative oplossingen tot benutten.

## prikkels

De vollvoortdurende Aufbau een Tokens vermittelt unmittelbar praktische Erfahrung met:

- Blockchain-Architektur
- Mechanik van cryptovaluta's
- Smart-Contract-ontwikkeling
- mogelijkheiden en Grenzen van Ethereum

U erwerben wertvolle Fähigkeiten, um uw Karriere in de Blockchain-Programmierung voranzudrijven.

## Fazit

Im domein de blockchaintechnologie wordt Vpasändnis am besten door praktische Umsetzung erreicht. Een cryptovaluta op de Ethereum-platform tot bouwen, biedt een einzigartige Geleggenheit, uit paser Hand Erfahrung met de mogelijkheiden en Grenzen de Technologie tot sammeln. Deze Leitfaden gibt u het kennis en de Fähigkeiten aan de Hand, um deze spannende Reise tot beginnen — en fördert innovatie en Entdeckergeist in de sich stetig weiterontwikkelenden wereld de Blockchain- en cryptovalutasentwicklung.

[00]: https://geth.ethereum.org/downloads/
[01]: https://geth.ethereum.org/docs/getting-started/installing-geth
