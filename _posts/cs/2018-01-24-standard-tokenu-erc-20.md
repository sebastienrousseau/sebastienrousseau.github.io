---
title: "El estándar de token ERC-20"
subtitle: "La interfaz unificada que permitió prosperar al ecosistema Ethereum"
description: "ERC-20: el tipo de token más extendido en la blockchain Ethereum, a menudo descrito como un contrato digital inteligente (smart contract)."
date: "January 24, 2018"
language: "cs-CZ"
locale: "cs_CZ"
banner: "https://cloudcdn.pro/stocks/images/m-ZzOa5G8hSPI.webp"
banner_alt: "Ordenador portátil apagado sobre una mesa de madera marrón"
keywords: "ERC-20, Ethereum, token, smart contract, DeFi, EIP, blockchain, interoperabilidad, DApps, estándar"
---


> **TL;DR.** Tento článek je DRAFT překlad původně španělského zdroje, čekající na revizi rodilým mluvčím. Hlavní obsah, příklady a citace zůstávají ve španělštině; pouze záhlaví/frontmatter byly přepnuty na češtinu.

**Klíčové body**

![Ordenador portátil apagado sobre una mesa de madera marrón](https://cloudcdn.pro/stocks/images/m-ZzOa5G8hSPI.webp).class=\"img-fluid clearfix\"

## Perspectiva

### La necesidad de una interfaz de token estandarizada

Antes del advenimiento del estándar ERC-20 (Ethereum Request for Comments 20), la blockchain Ethereum se parecía al Lejano Oeste de las arquitecturas de token. Cada nuevo token acuñado tenía su propio conjunto único de reglas, funciones e interfaces. Esto imponía a los desarrolladores una curva de aprendizaje pronunciada y frenaba la interoperabilidad de los tokens. En pocas palabras, cada nuevo token era como un nuevo idioma que aprender, comprender e implementar. Esta fragmentación obstaculizaba la escalabilidad y la adopción masiva de tokens en la plataforma Ethereum.

La introducción del estándar ERC-20 actuó como un lenguaje unificador, estableciendo un conjunto común de reglas y funciones a las que todos los tokens Ethereum deben ajustarse. A partir de entonces, los desarrolladores disponen de una interfaz coherente, sea cual sea el token. Esta estandarización fluidificó los procesos de interacción con los tokens, permitiendo una integración más fluida en diversas aplicaciones y servicios. Como consecuencia, los desarrolladores pueden interactuar de manera más útil con los tokens, propiciando un entorno favorable a la innovación y al crecimiento en el ecosistema Ethereum.

#### El Lejano Oeste de las arquitecturas de token

La blockchain Ethereum se diseñó inicialmente para soportar un único tipo de token: ETH. Pero a medida que la plataforma ganó popularidad, los desarrolladores comenzaron a crear sus propios tokens para representar una variedad de activos y conceptos. Esto dio lugar a una proliferación de arquitecturas de token diferentes, cada una con su propio conjunto único de reglas y funciones.

Esta fragmentación dificultaba a los desarrolladores la creación de aplicaciones capaces de interactuar con varios tokens. También complicaba a los usuarios la gestión de sus activos de token en distintas plataformas.

#### El estándar ERC-20

El estándar ERC-20 se introdujo en 2015 para responder a los retos planteados por este Lejano Oeste de arquitecturas de token. El estándar define un conjunto común de reglas y funciones a las que todos los tokens Ethereum deben ajustarse. Esta estandarización facilita la creación de aplicaciones capaces de interactuar con cualquier token ERC-20, y también simplifica la gestión de los activos de token por parte de los usuarios.

El estándar ERC-20 ha sido ampliamente adoptado por la comunidad Ethereum. Hoy en día se contabilizan más de 200.000 tokens ERC-20 y el estándar es utilizado por una gran variedad de aplicaciones, incluidos exchanges descentralizados, plataformas de préstamo y dapps de juegos.

## Idea

### Un conjunto común de funciones y propiedades para todos los tokens

El estándar ERC-20 define un conjunto de seis funciones esenciales que todos los tokens conformes a ERC-20 deben implementar. Estas funciones son:

- `transfer(address to, uint256 amount)`: transfiere un importe de tokens desde la dirección del invocador hacia la dirección especificada.
- `approve(address spender, uint256 amount)`: autoriza a la dirección especificada a gastar un importe de tokens en nombre del invocador.
- `allowance(address owner, address spender)`: devuelve el importe de tokens que el «spender» especificado está autorizado a gastar en nombre del «owner» especificado.
- `totalSupply()`: devuelve el número total de tokens en circulación.
- `balanceOf(address owner)`: devuelve el número de tokens que posee la dirección especificada.
- `name()`: devuelve el nombre del token.
- `symbol()`: devuelve el símbolo del token.

El estándar ERC-20 también define dos eventos que deben emitirse tras la ejecución exitosa de las funciones correspondientes:

- `Transfer(address from, address to, uint256 amount)`: emitido cuando un importe de tokens se transfiere de una dirección a otra.
- `Approval(address owner, address spender, uint256 amount)`: emitido cuando la dirección especificada es autorizada a gastar un importe de tokens en nombre del «owner» especificado.

## Impacto

### El crecimiento de DeFi y la adopción de Ethereum

El estándar ERC-20 ha tenido un impacto significativo en el ecosistema Ethereum. Ha sido un catalizador clave del movimiento DeFi (finanzas descentralizadas) y también ha contribuido a aumentar la adopción de Ethereum.

Las plataformas DeFi, que ofrecen toda una gama de servicios financieros que van desde el préstamo hasta la gestión de activos, se apoyan masivamente en los tokens para facilitar las transacciones. Con ERC-20 actuando como un adaptador universal, se volvió mucho más sencillo para las aplicaciones DeFi integrar un amplio abanico de tokens sin tener que adaptar su código a cada uno.

El estándar ERC-20 también ha facilitado la gestión de los activos de token por parte de los usuarios. Con tokens que respetan las mismas reglas básicas, a los usuarios les resulta más fácil transferir, gastar y gestionar sus activos de token en varias plataformas. Esta experiencia de usuario mejorada ha sido un motor del aumento de las tasas de adopción de Ethereum.

## Incentivos

### Costes de desarrollo reducidos y seguridad mejorada

La estandarización aportada por el protocolo ERC-20 también ha tenido un impacto económico directo. Al proporcionar un plano probado y aprobado por la comunidad para la creación de tokens, ha reducido significativamente la barrera de entrada para los desarrolladores. Ahora pueden crear un nuevo token con costes de desarrollo reducidos y un plazo de comercialización más corto, sin tener que reinventar la rueda. El estándar fomenta también indirectamente la creación de DApps (aplicaciones descentralizadas) y servicios capaces de interactuar universalmente con cualquier token ERC-20, cultivando así un ecosistema más dinámico.

Otro beneficio notable: una seguridad reforzada. El estándar ERC-20 ha sido sometido a un examen riguroso por parte de la comunidad Ethereum, convirtiéndolo en un modelo robusto y seguro para la implementación de tokens. El respeto de este estándar implica que los aspectos fundamentales del smart contract del token siguen las buenas prácticas aceptadas por la comunidad. Esto minimiza el riesgo de vulnerabilidades de seguridad que de otro modo podrían derivarse de un modelo de token mal diseñado. Aunque no es una garantía contra todo tipo de vulnerabilidades, es un paso significativo hacia la seguridad global de los tokens y, por extensión, de los proyectos que los utilizan.
