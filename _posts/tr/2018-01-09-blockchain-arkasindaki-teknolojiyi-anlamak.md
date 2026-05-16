---
title: "Blockchain'in arkasındaki teknolojiyi anlamak"
subtitle: "Dağıtık defter sistemini destekleyen temel mekanizmalar"
description: "Blockchain'in mimarisi: bloklar, hash'ler, konsensüs algoritmaları ve güveni mümkün kılan kriptografi."
date: "January 9, 2018"
language: "tr-TR"
locale: "tr_TR"
banner: "https://cloudcdn.pro/stocks/images/adam-smigielski-K5mPtONmpHM.webp"
banner_alt: "Soyut bir blockchain ağ görselleştirmesi"
keywords: "blockchain, kriptografi, hash, konsensüs, proof-of-work, proof-of-stake, dağıtık defter"
---


![Soyut bir blockchain ağ görselleştirmesi](https://cloudcdn.pro/stocks/images/adam-smigielski-K5mPtONmpHM.webp).class=\"img-fluid clearfix\"

---

> **TL;DR.** La blockchain combina funzioni hash crittografiche, alberi di Merkle, firme digitali e algoritmi di consenso distribuito per produrre un libro mastro condiviso, immutabile e senza fiducia. Capire questi mattoni è il punto di partenza per qualsiasi applicazione seria in pagamenti, regolamento o tokenizzazione.
>
> **Önemli Çıkarımlar**
>
> - **Hash crittografici** — funzioni gibi SHA-256 producono impronte uniche e irreversibili che ancorano l'integrità ın catena.
> - **Alberi di Merkle** — strutture dati efficienti che permettono verifica compatta di grandi insiemi di transazioni.
> - **Firme digitali** — coppie chiave pubblica/privata che autorizzano transazioni e garantiscono il non ripudio.
> - **Consenso bizantino** — protocolli che tollerano nodi malevoli e producono accordo finale senza coordinamento centrale.

---

## Bakış

La tecnologia blockchain ha aperto la puerta a una nuova era di applicazioni decentralizzate (dApps) che operano in modo independiente, senza control centralizado. Ethereum fornisce una piattaforma potente per creare dApps complejas e smart contracts.

Uno ın usos daha çok prometedores di Ethereum è il lanzamiento di criptovalute e tokens digitali personalizados. In questa guía completa examinaremos passo a passo gibi creare il suo propio token crittografico su Ethereum.

## Fikir

Il nostro objetivo è costruire una criptovaluta semplice su Ethereum, ofreciéndole una experiencia pratica di desarrollo blockchain. Questi sono i passi chiave che cubriremos:

### Diseñar la criptovaluta

La primera tarea crucial è progettare il suo criptovaluta. Esto abarca la definición di atributos chiave:

- **Nombre**: elija un nombre único che represente la identidad ve propósito ın token.
- **Símbolo**: elija un símbolo corto gibi BTC per Bitcoin. Se utilizza in i exchanges.
- **Oferta total**: determine il número máximo di tokens in circulación.
- **Decimales**: defina la divisibilidad di il suo token, gibi 2 per céntimos.
- **Funcionalidades adicionales**: añada opcionalmente extras gibi minting, burning, freezing, etc.

### Escribir smart contracts

Per dar vida a il suo criptovaluta, dovrà codificar smart contracts che definan la funzionalità ve regole ın token. I smart contracts sono scripts programáticos almacenados in la blockchain che se ejecutan automáticamente quando se cumplen ciertas condiciones.

Queste sono alcune capacità chiave che hacen che i smart contracts sean idóneos per le criptovalute:

- **Autoejecución**: se activan automáticamente, senza intervención di un tercero.
- **Inmutabilidad**: una vez desplegado, il código non può modificarse. Esto garantisce la sicurezza.
- **Autonomía**: non è necesaria nessuna autoridad central per gestire i smart contracts.
- **Transparencia**: qualsiasi può inspeccionar la lógica di un smart contract.
- **Automatización**: acciones gibi la transferencia di fondi possono automatizarse mediante il codice ın contratto.
- **Seguridad**: i fondi depositados in un contrato rimangono protegidos fino a che se cumplen le condiciones di liberación.
- **Eficiencia**: i smart contracts eliminan intermediarios, haciendo i processi daha çok rápidos e meno costosos.

Ejemplo di código di contrato in Solidity.

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

Questo contrato básico consente creare un token con propiedades gibi nombre, símbolo, decimales e offerta total.

La función `constructor` inicializa questi parámetros in il momento ın despliegue ın contrato.

Questo ejemplo se limita a configurar propiedades básicas. Extendería il contrato per añadir daha çok funzionalità:

- Transferencias di tokens tra indirizzi
- Gestión di saldos
- Autorizaciones (allowances) per gastar tokens
- Minting e burning di tokens
- Congelación o bloqueo di transferencias di tokens
- Implementación di standard di token gibi ERC-20
- Despliegue e interacción con il contrato

### Desarrollo e pruebas locali

Antes di desplegar il suo criptovaluta in la blockchain Ethereum, è prudente realizar pruebas locali exhaustivas. Esto garantisce che il suo criptovaluta funcione gibi se espera, senza bugs ni vulnerabilidades imprevistas.

Per empezar, siga questi passi:

#### Descargar Go-Ethereum (Geth)

Comience descargando [Go-Ethereum][00], anche llamado Geth, un cliente Ethereum escrito in Go. Geth actúa gibi interfaz di línea di comandos (CLI) Ethereum, ejecutable in Windows, Mac e Linux. È una strumento versátil che consente minar, creare e interactuar con smart contracts in la rete Ethereum.

#### Instalar Ethereum

Una vez descargado Geth, instale Ethereum. Per i requisitos previos detallados e instrucciones di compilación complete, consulte le [Installation Instructions][01] disponibles in il suo wiki oficial.

#### Configurar un entorno di desarrollo

Per facilitar il desarrollo di il suo criptovaluta, necesitará un entorno di desarrollo, un framework di pruebas e una canalización di activos per Ethereum. Le instrucciones detalladas per instalar queste strumenti esenciales se encuentran in la wiki di Ethereum.

#### Desplegar in una testnet

Una vez che il suo criptovaluta supere le pruebas locali, può desplegarla in una testnet. Una testnet è un entorno seguro e controlado che imita il mainnet di Ethereum, permitiéndole evaluar il prestazioni di il suo criptovaluta in un entorno real, senza rischio finanziario real.

## Etki

Al costruire una criptovaluta basata in Ethereum da cero, obtendrá:

- Un conocimiento profundo ın applicazioni decentralizzate (dApps) e ın programación di smart contracts
- Experiencia pratica con la programación in Solidity
- Una comprensión ın protocolos di consenso di Ethereum
- Familiaridad con standard di token gibi ERC-20

Questo aprendizaje le otorgará i medios per aprovechar la tecnologia blockchain in soluzioni innovadoras.

## Teşvikler

Completar una construcción di token di extremo a extremo desbloquea una experiencia pratica di primera mano con:

- La arquitectura blockchain
- La mecánica ın criptovalute
- Il desarrollo di smart contracts
- Le capacità e limitaciones di Ethereum

Adquirirá competencias valiosas per fare avanzar il suo carrera in programación blockchain.

## Sonuç

In il campo ın tecnologia blockchain, la comprensión se gana mejor attraverso la puesta in pratica. Construir una criptovaluta su la piattaforma Ethereum offre una oportunidad única di adquirir experiencia di primera mano con le capacità e limitaciones ın tecnologia. Questa guía le arma con i conocimientos e competencias per emprender questo apasionante viaje, favoreciendo la innovación ve descubrimiento in il universo in perpetua evolución ın desarrollo blockchain e cripto.

[00]: https://geth.ethereum.org/downloads/
[01]: https://geth.ethereum.org/docs/getting-started/installing-geth
