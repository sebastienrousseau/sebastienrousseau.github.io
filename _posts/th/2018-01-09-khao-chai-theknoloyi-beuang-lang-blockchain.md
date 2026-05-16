---
title: "Comprender la tecnología detrás de blockchain"
subtitle: "Construir una criptomoneda sobre Ethereum, paso a paso"
description: "Construir una criptomoneda en la blockchain Ethereum: una guía completa de desarrollo blockchain, tokenización e implementación."
date: "January 9, 2018"
language: "th-TH"
locale: "th_TH"
banner: "https://cloudcdn.pro/stocks/images/adam-smigielski-K5mPtONmpHM.webp"
banner_alt: "Ordenador portátil apagado sobre una mesa de madera marrón"
keywords: "blockchain, Ethereum, smart contract, criptomoneda, Solidity, Geth, dApps, ERC-20, tokenización, testnet"
---


> **TL;DR.** บทความนี้เป็น DRAFT แปลจากต้นฉบับภาษาสเปน รอการตรวจสอบโดยเจ้าของภาษา เนื้อหาหลัก ตัวอย่าง และการอ้างอิงยังคงเป็นภาษาสเปน เฉพาะ frontmatter เท่านั้นที่ถูกเปลี่ยนเป็นภาษาไทย

**ประเด็นสำคัญ**

![Ordenador portátil apagado sobre una mesa de madera marrón](https://cloudcdn.pro/stocks/images/adam-smigielski-K5mPtONmpHM.webp).class=\"img-fluid clearfix\"

## Perspectiva

La tecnología blockchain ha abierto la puerta a una nueva era de aplicaciones descentralizadas (dApps) que operan de forma independiente, sin control centralizado. Ethereum proporciona una plataforma potente para crear dApps complejas y smart contracts.

Uno de los usos más prometedores de Ethereum es el lanzamiento de criptomonedas y tokens digitales personalizados. En esta guía completa examinaremos paso a paso cómo crear su propio token criptográfico sobre Ethereum.

## Idea

Nuestro objetivo es construir una criptomoneda sencilla sobre Ethereum, ofreciéndole una experiencia práctica de desarrollo blockchain. Estos son los pasos clave que cubriremos:

### Diseñar la criptomoneda

La primera tarea crucial es diseñar su criptomoneda. Esto abarca la definición de atributos clave:

- **Nombre**: elija un nombre único que represente la identidad y el propósito del token.
- **Símbolo**: elija un símbolo corto como BTC para Bitcoin. Se utiliza en los exchanges.
- **Oferta total**: determine el número máximo de tokens en circulación.
- **Decimales**: defina la divisibilidad de su token, como 2 para céntimos.
- **Funcionalidades adicionales**: añada opcionalmente extras como minting, burning, freezing, etc.

### Escribir smart contracts

Para dar vida a su criptomoneda, deberá codificar smart contracts que definan la funcionalidad y las reglas del token. Los smart contracts son scripts programáticos almacenados en la blockchain que se ejecutan automáticamente cuando se cumplen ciertas condiciones.

Estas son algunas capacidades clave que hacen que los smart contracts sean idóneos para las criptomonedas:

- **Autoejecución**: se activan automáticamente, sin intervención de un tercero.
- **Inmutabilidad**: una vez desplegado, el código no puede modificarse. Esto garantiza la seguridad.
- **Autonomía**: no es necesaria ninguna autoridad central para gestionar los smart contracts.
- **Transparencia**: cualquiera puede inspeccionar la lógica de un smart contract.
- **Automatización**: acciones como la transferencia de fondos pueden automatizarse mediante el código del contrato.
- **Seguridad**: los fondos depositados en un contrato quedan protegidos hasta que se cumplen las condiciones de liberación.
- **Eficiencia**: los smart contracts eliminan intermediarios, haciendo los procesos más rápidos y menos costosos.

Ejemplo de código de contrato en Solidity.

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

Este contrato básico permite crear un token con propiedades como nombre, símbolo, decimales y oferta total.

La función `constructor` inicializa estos parámetros en el momento del despliegue del contrato.

Este ejemplo se limita a configurar propiedades básicas. Extendería el contrato para añadir más funcionalidades:

- Transferencias de tokens entre direcciones
- Gestión de saldos
- Autorizaciones (allowances) para gastar tokens
- Minting y burning de tokens
- Congelación o bloqueo de transferencias de tokens
- Implementación de estándares de token como ERC-20
- Despliegue e interacción con el contrato

### Desarrollo y pruebas locales

Antes de desplegar su criptomoneda en la blockchain Ethereum, es prudente realizar pruebas locales exhaustivas. Esto garantiza que su criptomoneda funcione como se espera, sin bugs ni vulnerabilidades imprevistas.

Para empezar, siga estos pasos:

#### Descargar Go-Ethereum (Geth)

Comience descargando [Go-Ethereum][00], también llamado Geth, un cliente Ethereum escrito en Go. Geth actúa como interfaz de línea de comandos (CLI) Ethereum, ejecutable en Windows, Mac y Linux. Es una herramienta versátil que permite minar, crear e interactuar con smart contracts en la red Ethereum.

#### Instalar Ethereum

Una vez descargado Geth, instale Ethereum. Para los requisitos previos detallados e instrucciones de compilación completas, consulte las [Installation Instructions][01] disponibles en su wiki oficial.

#### Configurar un entorno de desarrollo

Para facilitar el desarrollo de su criptomoneda, necesitará un entorno de desarrollo, un framework de pruebas y una canalización de activos para Ethereum. Las instrucciones detalladas para instalar estas herramientas esenciales se encuentran en la wiki de Ethereum.

#### Desplegar en una testnet

Una vez que su criptomoneda supere las pruebas locales, puede desplegarla en una testnet. Una testnet es un entorno seguro y controlado que imita el mainnet de Ethereum, permitiéndole evaluar el rendimiento de su criptomoneda en un entorno real, sin riesgo financiero real.

## Impacto

Al construir una criptomoneda basada en Ethereum desde cero, obtendrá:

- Un conocimiento profundo de las aplicaciones descentralizadas (dApps) y de la programación de smart contracts
- Experiencia práctica con la programación en Solidity
- Una comprensión de los protocolos de consenso de Ethereum
- Familiaridad con estándares de token como ERC-20

Este aprendizaje le otorgará los medios para aprovechar la tecnología blockchain en soluciones innovadoras.

## Incentivos

Completar una construcción de token de extremo a extremo desbloquea una experiencia práctica de primera mano con:

- La arquitectura blockchain
- La mecánica de las criptomonedas
- El desarrollo de smart contracts
- Las capacidades y limitaciones de Ethereum

Adquirirá competencias valiosas para hacer avanzar su carrera en programación blockchain.

## Conclusión

En el campo de la tecnología blockchain, la comprensión se gana mejor a través de la puesta en práctica. Construir una criptomoneda sobre la plataforma Ethereum ofrece una oportunidad única de adquirir experiencia de primera mano con las capacidades y limitaciones de la tecnología. Esta guía le arma con los conocimientos y competencias para emprender este apasionante viaje, favoreciendo la innovación y el descubrimiento en el universo en perpetua evolución del desarrollo blockchain y cripto.

[00]: https://geth.ethereum.org/downloads/
[01]: https://geth.ethereum.org/docs/getting-started/installing-geth
