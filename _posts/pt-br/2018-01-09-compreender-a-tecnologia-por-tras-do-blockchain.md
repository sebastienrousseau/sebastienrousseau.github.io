---
title: "Comprender a tecnologia atrás de blockchain"
subtitle: "Construir uma criptomoeda sobre Ethereum, paso a paso"
description: "Construir uma criptomoeda em a blockchain Ethereum: uma guía completa de desenvolvimento blockchain, tokenización e implementación."
date: "January 9, 2018"
language: "pt-BR"
locale: "pt_BR"
banner: "https://cloudcdn.pro/stocks/images/adam-smigielski-K5mPtONmpHM.webp"
banner_alt: "Ordenador portátil apagado sobre uma mesa de madera marrón"
keywords: "blockchain, Ethereum, smart contract, criptomoeda, Solidity, Geth, dApps, ERC-20, tokenización, testnet"
---

![Ordenador portátil apagado sobre uma mesa de madera marrón](https://cloudcdn.pro/stocks/images/adam-smigielski-K5mPtONmpHM.webp).class=\"img-fluid clearfix\"

## Perspectiva

La tecnologia blockchain tem abierto a puerta a uma nova era de aplicações descentralizadas (dApps) que operan de forma independiente, sem control centralizado. Ethereum proporciona uma plataforma potente para criar dApps complejas e smart contracts.

Uno de os usos mais prometedores de Ethereum é o lanzamiento de criptomoedas e tokens digitais personalizados. En esta guía completa examinaremos paso a paso cómo criar seu próprio token criptográfico sobre Ethereum.

## Idea

Nuestro objetivo é construir uma criptomoeda sencilla sobre Ethereum, ofreciéndole uma experiência prática de desenvolvimento blockchain. Estos são os pasos clave que cubriremos:

### Diseñar a criptomoeda

La primeira tarea crucial é diseñar seu criptomoeda. Esto abarca a definición de atributos clave:

- **Nombre**: elija um nombre único que represente a identidade e o propósito do token.
- **Símbolo**: elija um símbolo corto como BTC para Bitcoin. Se utiliza em os exchanges.
- **Oferta total**: determine o número máximo de tokens em circulación.
- **Decimales**: defina a divisibilidad de seu token, como 2 para céntimos.
- **Funcionalidades adicionales**: añada opcionalmente extras como minting, burning, freezing, etc.

### Escribir smart contracts

Para dar vida a seu criptomoeda, deberá codificar smart contracts que definan a funcionalidad e as reglas do token. Los smart contracts são scripts programáticos almacenados em a blockchain que se ejecutan automaticamente quando se cumplen ciertas condiciones.

Estas são algunas capacidades clave que fazem que os smart contracts sean idóneos para as criptomoedas:

- **Autoejecución**: se activan automaticamente, sem intervención de um tercero.
- **Inmutabilidad**: uma vez desplegado, o código no pode modificarse. Esto garantiza a segurança.
- **Autonomía**: no é necessária ninguna autoridade central para gestionar os smart contracts.
- **Transparencia**: cualquiera pode inspeccionar a lógica de um smart contract.
- **Automatización**: ações como a transferencia de fondos podem automatizarse mediante o código do contrato.
- **Seguridad**: os fondos depositados em um contrato quedan protegidos hasta que se cumplen as condiciones de liberación.
- **Eficiencia**: os smart contracts eliminan intermediarios, fazendo os procesos mais rápidos e menos costosos.

Ejemplo de código de contrato em Solidity.

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

Este contrato básico permite criar um token com propriedades como nombre, símbolo, decimales e oferta total.

La función `constructor` inicializa estes parámetros em o momento do despliegue do contrato.

Este exemplo se limita a configurar propriedades básicas. Extendería o contrato para añadir mais funcionalidades:

- Transferencias de tokens entre direções
- Gestión de saldos
- Autorizaciones (allowances) para gastar tokens
- Minting e burning de tokens
- Congelación ou bloqueo de transferencias de tokens
- Implementación de estándares de token como ERC-20
- Despliegue e interacción com o contrato

### Desarrollo e pruebas locales

Antes de desplegar seu criptomoeda em a blockchain Ethereum, é prudente realizar pruebas locales exhaustivas. Esto garantiza que seu criptomoeda funcione como se espera, sem bugs ni vulnerabilidades imprevistas.

Para empezar, siga estes pasos:

#### Descargar Go-Ethereum (Geth)

Comience descargando [Go-Ethereum][00], também llamado Geth, um cliente Ethereum escrito em Go. Geth actúa como interfaz de linha de comandos (CLI) Ethereum, ejecutable em Windows, Mac e Linux. Es uma ferramenta versátil que permite minar, criar e interactuar com smart contracts em a red Ethereum.

#### Instalar Ethereum

Una vez descargado Geth, instale Ethereum. Para os requisitos previos detallados e instrucciones de compilación completas, consulte as [Installation Instructions][01] disponibles em seu wiki oficial.

#### Configurar um entorno de desenvolvimento

Para facilitar o desenvolvimento de seu criptomoeda, necesitará um entorno de desenvolvimento, um framework de pruebas e uma canalización de activos para Ethereum. Las instrucciones detalladas para instalar estas ferramentas esenciales se encontram em a wiki de Ethereum.

#### Desplegar em uma testnet

Una vez que seu criptomoeda supere as pruebas locales, pode desplegarla em uma testnet. Una testnet é um entorno seguro e controlado que imita o mainnet de Ethereum, permitiéndole avaliar o rendimiento de seu criptomoeda em um entorno real, sem riesgo financeiro real.

## Impacto

Al construir uma criptomoeda basada em Ethereum desde cero, obtendrá:

- Um conhecimento profundo de as aplicações descentralizadas (dApps) e de a programación de smart contracts
- Experiencia prática com a programación em Solidity
- Una comprensión de os protocolos de consenso de Ethereum
- Familiaridad com estándares de token como ERC-20

Este aprendizado le otorgará os meios para aproveitar a tecnologia blockchain em soluções innovadoras.

## Incentivos

Completar uma construcción de token de extremo a extremo desbloquea uma experiência prática de primeira mano com:

- La arquitectura blockchain
- La mecánica de as criptomoedas
- El desenvolvimento de smart contracts
- Las capacidades e limitaciones de Ethereum

Adquirirá competencias valiosas para fazer avanzar seu carrera em programación blockchain.

## Conclusión

En o campo de a tecnologia blockchain, a comprensión se gana melhor através de a colocada em prática. Construir uma criptomoeda sobre a plataforma Ethereum oferece uma oportunidade única de adquirir experiência de primeira mano com as capacidades e limitaciones de a tecnologia. Esta guía le arma com os conhecimentos e competencias para emprender este apasionante viaje, favoreciendo a innovación e o descubrimiento em o universo em perpetua evolução do desenvolvimento blockchain e cripto.

[00]: https://geth.ethereum.org/downloads/
[01]: https://geth.ethereum.org/docs/getting-started/installing-geth
