---
title: "Die Technologie hinter Blockchain verstehen"
subtitle: "Eine Kryptowährung auf Ethereum aufbauen — Schritt für Schritt"
description: "Eine Kryptowährung auf der Ethereum-Blockchain entwickeln: ein umfassender Leitfaden zur Blockchain-Entwicklung, Tokenisierung und Implementierung einer Kryptowährung."
date: "January 9, 2018"
language: "de"
locale: "de_DE"
banner: "https://cloudcdn.pro/stocks/images/adam-smigielski-K5mPtONmpHM.webp"
banner_alt: "Ausgeschalteter Laptop auf einem braunen Holztisch"
keywords: "Blockchain, Ethereum, Smart Contract, Kryptowährung, Solidity, Geth, dApps, ERC-20, Tokenisierung, Testnet"
---

![Ausgeschalteter Laptop auf einem braunen Holztisch](https://cloudcdn.pro/stocks/images/adam-smigielski-K5mPtONmpHM.webp).class=\"img-fluid clearfix\"

## Überblick

Die Blockchain-Technologie hat die Tür zu einer neuen Ära dezentraler Anwendungen (dApps) geöffnet, die unabhängig und ohne zentrale Kontrolle laufen. Ethereum bietet eine leistungsstarke Plattform, um komplexe dApps und Smart Contracts zu erstellen.

Eine der vielversprechendsten Einsatzmöglichkeiten von Ethereum ist die Einführung individueller Kryptowährungen und digitaler Tokens. In diesem umfassenden Leitfaden gehen wir Schritt für Schritt durch, wie Sie Ihr eigenes Krypto-Token auf Ethereum erstellen.

## Idee

Unser Ziel ist es, eine einfache Kryptowährung auf Ethereum aufzubauen und Ihnen damit praktische Erfahrung in der Blockchain-Entwicklung zu vermitteln. Im Folgenden die wichtigsten Schritte, die wir behandeln:

### Die Kryptowährung entwerfen

Die erste entscheidende Aufgabe besteht darin, Ihre Kryptowährung zu entwerfen. Dazu gehört die Definition der wichtigsten Attribute:

- **Name**: Wählen Sie einen einzigartigen Namen, der die Identität und den Zweck des Tokens widerspiegelt.
- **Symbol**: Wählen Sie ein kurzes Symbol wie BTC für Bitcoin. Es wird an Börsen verwendet.
- **Gesamtangebot**: Legen Sie die maximale Anzahl an im Umlauf befindlichen Tokens fest.
- **Dezimalstellen**: Definieren Sie die Teilbarkeit Ihres Tokens, etwa 2 für Cent-Einheiten.
- **Zusatzfunktionen**: Ergänzen Sie optional Extras wie Minting, Burning, Freezing usw.

### Smart Contracts schreiben

Um Ihre Kryptowährung zum Leben zu erwecken, müssen Sie Smart Contracts programmieren, die die Funktionalität und die Regeln des Tokens definieren. Smart Contracts sind programmatische Skripte, die auf der Blockchain gespeichert sind und automatisch ausgeführt werden, sobald bestimmte Bedingungen erfüllt sind.

Einige zentrale Eigenschaften, die Smart Contracts ideal für Kryptowährungen machen, sind:

- **Selbstausführend** — sie laufen ohne Beteiligung Dritter automatisch ab, sobald sie ausgelöst werden.
- **Unveränderlichkeit** — einmal bereitgestellt, kann der Code nicht mehr geändert werden. Dies sorgt für Sicherheit.
- **Autonomie** — es ist keine zentrale Instanz nötig, um Smart Contracts zu verwalten.
- **Transparenz** — jeder kann die Logik eines Smart Contracts einsehen.
- **Automatisierung** — Aktionen wie Mittelübertragungen lassen sich über den Vertragscode automatisieren.
- **Sicherheit** — Mittel in einem Contract sind gesichert, bis die Freigabebedingungen erfüllt sind.
- **Effizienz** — Smart Contracts schalten Intermediäre aus und machen Prozesse schneller und günstiger.

Beispielcode für einen Contract in Solidity.

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

Dieser einfache Contract erlaubt es, ein Token mit Eigenschaften wie Name, Symbol, Dezimalstellen und Gesamtangebot zu erstellen.

Die `constructor`-Funktion initialisiert diese Parameter beim Deployment des Contracts.

Dieses Beispiel richtet lediglich grundlegende Token-Eigenschaften ein. Sie würden den Contract erweitern, um weitere Funktionen hinzuzufügen, wie etwa:

- Token-Transfers zwischen Adressen
- Verwaltung von Guthaben
- Allowances für das Ausgeben von Tokens
- Minting und Burning von Tokens
- Einfrieren oder Sperren von Token-Transfers
- Implementierung von Token-Standards wie ERC-20
- Bereitstellung und Interaktion mit dem Contract

### Lokale Entwicklung und Tests

Bevor Sie Ihre Kryptowährung auf der Ethereum-Blockchain bereitstellen, ist es ratsam, gründliche lokale Tests durchzuführen. So stellen Sie sicher, dass Ihre Kryptowährung wie vorgesehen funktioniert, ohne unvorhergesehene Fehler oder Schwachstellen.

Folgen Sie diesen Schritten, um loszulegen:

#### Go-Ethereum (Geth) herunterladen

Beginnen Sie mit dem Download von [Go-Ethereum][00], auch als Geth bekannt — einem in Go geschriebenen Ethereum-Client. Geth ist der Command-Line-Interface-(CLI-)Ethereum-Client, der auf Windows-, Mac- und Linux-Plattformen läuft. Es handelt sich um ein vielseitiges Werkzeug, mit dem Sie minen, Smart Contracts erstellen und mit ihnen im Ethereum-Netzwerk interagieren können. Sie können Geth hier herunterladen.

#### Ethereum installieren

Sobald Sie Geth heruntergeladen haben, fahren Sie mit der Installation von Ethereum fort. Detaillierte Voraussetzungen und vollständige Build-Anleitungen finden Sie in den [Installation Instructions][01] im offiziellen Wiki.

#### Eine Entwicklungsumgebung einrichten

Um die Entwicklung Ihrer Kryptowährung zu erleichtern, benötigen Sie eine Entwicklungsumgebung, ein Test-Framework und eine Asset-Pipeline für Ethereum. Detaillierte Anleitungen zur Einrichtung dieser unverzichtbaren Werkzeuge finden Sie im Ethereum-Wiki.

#### Auf einem Testnet bereitstellen

Sobald Ihre Kryptowährung die lokalen Tests besteht, können Sie sie in einem Testnet bereitstellen. Ein Testnet ist eine sichere und kontrollierte Umgebung, die das Ethereum-Mainnet nachbildet, sodass Sie die Leistung Ihrer Kryptowährung unter realen Bedingungen bewerten können, ohne reale finanzielle Risiken einzugehen.

## Auswirkungen

Indem Sie eine auf Ethereum basierende Kryptowährung von Grund auf aufbauen, gewinnen Sie:

- Fundiertes Wissen zu dezentralen Anwendungen (dApps) und der Programmierung von Smart Contracts
- Praktische Erfahrung mit der Solidity-Programmierung
- Verständnis der Konsensprotokolle von Ethereum
- Vertrautheit mit Token-Standards wie ERC-20

Dieses Wissen befähigt Sie, die Blockchain-Technologie für innovative Lösungen zu nutzen.

## Anreize

Der vollständige Aufbau eines Tokens vermittelt unmittelbar praktische Erfahrung mit:

- Blockchain-Architektur
- Mechanik von Kryptowährungen
- Smart-Contract-Entwicklung
- Möglichkeiten und Grenzen von Ethereum

Sie erwerben wertvolle Fähigkeiten, um Ihre Karriere in der Blockchain-Programmierung voranzutreiben.

## Fazit

Im Bereich der Blockchain-Technologie wird Verständnis am besten durch praktische Umsetzung erreicht. Eine Kryptowährung auf der Ethereum-Plattform zu bauen, bietet eine einzigartige Gelegenheit, aus erster Hand Erfahrung mit den Möglichkeiten und Grenzen der Technologie zu sammeln. Dieser Leitfaden gibt Ihnen das Wissen und die Fähigkeiten an die Hand, um diese spannende Reise zu beginnen — und fördert Innovation und Entdeckergeist in der sich stetig weiterentwickelnden Welt der Blockchain- und Kryptowährungsentwicklung.

[00]: https://geth.ethereum.org/downloads/
[01]: https://geth.ethereum.org/docs/getting-started/installing-geth
