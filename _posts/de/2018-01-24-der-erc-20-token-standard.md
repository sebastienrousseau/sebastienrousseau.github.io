---
title: "Der ERC-20-Token-Standard"
subtitle: "Die einheitliche Schnittstelle, die das Ethereum-Ökosystem zum Blühen brachte"
description: "ERC-20: der am weitesten verbreitete Token-Typ auf der Ethereum-Blockchain, häufig auch als intelligenter digitaler Vertrag (Smart Contract) beschrieben."
date: "January 24, 2018"
language: "de"
locale: "de_DE"
banner: "https://cloudcdn.pro/stocks/images/m-ZzOa5G8hSPI.webp"
banner_alt: "Ausgeschalteter Laptop auf einem braunen Holztisch"
keywords: "ERC-20, Ethereum, Token, Smart Contract, DeFi, EIP, Blockchain, Interoperabilität, DApps, Standard"
---

![Ausgeschalteter Laptop auf einem braunen Holztisch](https://cloudcdn.pro/stocks/images/m-ZzOa5G8hSPI.webp).class=\"img-fluid clearfix\"

## Überblick

### Der Bedarf an einer standardisierten Token-Schnittstelle

Vor dem Aufkommen des ERC-20-Standards (Ethereum Request for Comments 20) glich die Ethereum-Blockchain einem Wilden Westen der Token-Architekturen. Jedes neu geschaffene Token hatte seinen eigenen, einzigartigen Satz an Regeln, Funktionen und Schnittstellen. Das stellte Entwickler nicht nur vor eine steile Lernkurve, sondern behinderte auch die Interoperabilität der Tokens. Im Grunde war jedes neue Token wie eine neue Sprache, die erlernt, verstanden und implementiert werden musste. Diese Fragmentierung hemmte die Skalierbarkeit und die breite Akzeptanz von Tokens auf der Ethereum-Plattform.

Die Einführung des ERC-20-Standards wirkte wie eine vereinheitlichende Sprache und legte einen gemeinsamen Satz an Regeln und Funktionen fest, an die sich alle Ethereum-Tokens halten müssen. Entwickler verfügen nun über eine einheitliche Schnittstelle, unabhängig vom jeweiligen Token. Diese Standardisierung hat die Interaktionsprozesse mit Tokens vereinfacht und eine reibungslosere Integration in verschiedene Anwendungen und Dienste ermöglicht. Dadurch können Entwickler bedeutsamer mit Tokens arbeiten und ein Umfeld schaffen, das Innovation und Wachstum im Ethereum-Ökosystem begünstigt.

#### Der Wilde Westen der Token-Architekturen

Die Ethereum-Blockchain war ursprünglich darauf ausgelegt, einen einzigen Token-Typ zu unterstützen: ETH. Mit zunehmender Popularität der Plattform begannen Entwickler jedoch, eigene Tokens zu erstellen, um unterschiedlichste Vermögenswerte und Konzepte abzubilden. Das führte zu einer Vielzahl unterschiedlicher Token-Architekturen, jede mit ihrem eigenen Regelwerk und ihren eigenen Funktionen.

Diese Fragmentierung erschwerte es Entwicklern, Anwendungen zu erstellen, die mit mehreren Tokens interagieren konnten. Sie machte es auch für Nutzer schwierig, ihre Token-Vermögenswerte plattformübergreifend zu verwalten.

#### Der ERC-20-Standard

Der ERC-20-Standard wurde 2015 eingeführt, um die Herausforderungen dieses Wilden Westens der Token-Architekturen zu adressieren. Der Standard definiert einen gemeinsamen Satz von Regeln und Funktionen, an die sich alle Ethereum-Tokens halten müssen. Diese Standardisierung erleichtert es Entwicklern, Anwendungen zu erstellen, die mit jedem ERC-20-Token interagieren können, und vereinfacht für Nutzer die Verwaltung ihrer Token-Vermögenswerte.

Der ERC-20-Standard wurde von der Ethereum-Community breit übernommen. Heute existieren über 200.000 ERC-20-Tokens, und der Standard kommt in einer Vielzahl von Anwendungen zum Einsatz, darunter dezentrale Börsen, Lending-Plattformen und Gaming-DApps.

## Idee

### Ein gemeinsamer Satz von Funktionen und Eigenschaften für alle Tokens

Der ERC-20-Standard definiert sechs essenzielle Funktionen, die alle ERC-20-konformen Tokens implementieren müssen. Diese Funktionen sind:

- `transfer(address to, uint256 amount)`: Überträgt einen Token-Betrag von der Adresse des Aufrufers an die angegebene Adresse.
- `approve(address spender, uint256 amount)`: Genehmigt der angegebenen Adresse, im Namen des Aufrufers einen Token-Betrag auszugeben.
- `allowance(address owner, address spender)`: Gibt zurück, welchen Token-Betrag der angegebene Spender im Namen des angegebenen Eigentümers ausgeben darf.
- `totalSupply()`: Gibt die Gesamtzahl der im Umlauf befindlichen Tokens zurück.
- `balanceOf(address owner)`: Gibt die Anzahl der von der angegebenen Adresse gehaltenen Tokens zurück.
- `name()`: Gibt den Namen des Tokens zurück.
- `symbol()`: Gibt das Symbol des Tokens zurück.

Der ERC-20-Standard definiert außerdem zwei Events, die bei erfolgreicher Ausführung der entsprechenden Funktionen ausgelöst werden müssen:

- `Transfer(address from, address to, uint256 amount)`: Wird ausgelöst, wenn ein Token-Betrag von einer Adresse an eine andere übertragen wird.
- `Approval(address owner, address spender, uint256 amount)`: Wird ausgelöst, wenn der angegebenen Adresse die Berechtigung erteilt wird, im Namen des angegebenen Eigentümers einen Token-Betrag auszugeben.

## Auswirkungen

### Das Wachstum von DeFi und die Adoption von Ethereum

Der ERC-20-Standard hat das Ethereum-Ökosystem maßgeblich geprägt. Er war ein Schlüsselfaktor für die DeFi-Bewegung (Decentralized Finance) und hat zudem die Verbreitung von Ethereum gefördert.

DeFi-Plattformen, die ein breites Spektrum an Finanzdienstleistungen vom Kreditgeschäft bis zur Vermögensverwaltung anbieten, stützen sich stark auf Tokens, um Transaktionen abzuwickeln. Da ERC-20 als universeller Adapter fungiert, ist es für DeFi-Anwendungen erheblich einfacher geworden, eine Vielzahl von Tokens zu integrieren, ohne den Code für jedes einzelne anpassen zu müssen.

Der ERC-20-Standard hat es Nutzern zudem erleichtert, ihre Token-Vermögenswerte zu verwalten. Da sich Tokens an dieselben Grundregeln halten, fällt es Anwendern leichter, Tokens plattformübergreifend zu transferieren, auszugeben und zu verwalten. Diese verbesserte Nutzererfahrung war ein treibender Faktor für die wachsenden Adoptionsraten von Ethereum.

## Anreize

### Geringere Entwicklungskosten und verbesserte Sicherheit

Die durch das ERC-20-Protokoll geschaffene Standardisierung hatte auch unmittelbare wirtschaftliche Auswirkungen. Durch die Bereitstellung einer erprobten und von der Community akzeptierten Vorlage für die Token-Erstellung wurden die Einstiegshürden für Entwickler deutlich gesenkt. Sie können nun ein neues Token mit reduzierten Entwicklungskosten und kürzerer Time-to-Market erstellen, ohne das Rad neu zu erfinden. Der Standard fördert indirekt auch die Entstehung von DApps (dezentralen Anwendungen) und Diensten, die universell mit jedem ERC-20-Token interagieren können, und nährt so ein dynamischeres Ökosystem.

Ein weiterer bemerkenswerter Vorteil ist die verbesserte Sicherheit. Der ERC-20-Standard wurde von der Ethereum-Community gründlich geprüft, was ihn zu einem robusten und sicheren Modell für die Token-Implementierung macht. Die Einhaltung dieses Standards bedeutet, dass die grundlegenden Aspekte des Smart Contracts eines Tokens den von der Community akzeptierten Best Practices folgen. Das minimiert das Risiko von Sicherheitslücken, die sonst aus einem unsachgemäß entworfenen Token-Modell resultieren könnten. Auch wenn dies keine Garantie gegen alle Arten von Schwachstellen bietet, ist es ein wichtiger Schritt zur Gewährleistung der Gesamtsicherheit der Tokens und damit auch der Projekte, die sie nutzen.
