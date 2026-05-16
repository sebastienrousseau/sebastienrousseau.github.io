---
title: "El estándar de token ERC-20"
subtitle: "La interfaz unificada que permitiu prosperar ao ecosistema Ethereum"
description: "ERC-20: o tipo de token mais extendido em a blockchain Ethereum, frequentemente descrito como um contrato digital inteligente (smart contract)."
date: "January 24, 2018"
language: "pt-BR"
locale: "pt_BR"
banner: "https://cloudcdn.pro/stocks/images/m-ZzOa5G8hSPI.webp"
banner_alt: "Ordenador portátil apagado sobre uma mesa de madera marrón"
keywords: "ERC-20, Ethereum, token, smart contract, DeFi, EIP, blockchain, interoperabilidade, DApps, estándar"
---

![Ordenador portátil apagado sobre uma mesa de madera marrón](https://cloudcdn.pro/stocks/images/m-ZzOa5G8hSPI.webp).class=\"img-fluid clearfix\"

## Perspectiva

### La necessidade de uma interfaz de token estandarizada

Antes do advenimiento do estándar ERC-20 (Ethereum Request for Comments 20), a blockchain Ethereum se parecía ao Lejano Oeste de as arquitecturas de token. Cada novo token acuñado tinha seu próprio conjunto único de reglas, funciones e interfaces. Esto imponía a os desenvolvedores uma curva de aprendizado pronunciada e frenaba a interoperabilidade de os tokens. En poucas palabras, cada novo token era como um novo idioma que aprender, compreender e implementar. Esta fragmentación obstaculizaba a escalabilidade e a adoção masiva de tokens em a plataforma Ethereum.

La introdução do estándar ERC-20 actuó como um lenguaje unificador, estableciendo um conjunto común de reglas e funciones a as que todos os tokens Ethereum devem ajustarse. A partir de então, os desenvolvedores disponen de uma interfaz coherente, sea cual sea o token. Esta padronização fluidificó os procesos de interacción com os tokens, permitiendo uma integração mais fluida em diversas aplicações e serviços. Como consecuencia, os desenvolvedores podem interactuar de maneira mais útil com os tokens, propiciando um entorno favorable a a innovación e ao crescimento em o ecosistema Ethereum.

#### El Lejano Oeste de as arquitecturas de token

La blockchain Ethereum se diseñó inicialmente para soportar um único tipo de token: ETH. Pero à medida que a plataforma ganó popularidad, os desenvolvedores comenzaron a criar seus próprios tokens para representar uma variedad de activos e conceptos. Esto dio lugar a uma proliferación de arquitecturas de token diferentes, cada uma com seu próprio conjunto único de reglas e funciones.

Esta fragmentación dificultaba a os desenvolvedores a criação de aplicações capaces de interactuar com vários tokens. También complicaba a os usuários a gestión de seus activos de token em distintas plataformas.

#### El estándar ERC-20

El estándar ERC-20 se introdujo em 2015 para responder a os retos planteados por este Lejano Oeste de arquitecturas de token. El estándar define um conjunto común de reglas e funciones a as que todos os tokens Ethereum devem ajustarse. Esta padronização facilita a criação de aplicações capaces de interactuar com cualquier token ERC-20, e também simplifica a gestión de os activos de token por parte de os usuários.

El estándar ERC-20 foi ampliamente adotado por a comunidade Ethereum. Hoy em día se contabilizan mais de 200.000 tokens ERC-20 e o estándar é utilizado por uma gran variedad de aplicações, incluídos exchanges descentralizados, plataformas de préstamo e dapps de juegos.

## Idea

### Um conjunto común de funciones e propriedades para todos os tokens

El estándar ERC-20 define um conjunto de seis funciones esenciales que todos os tokens conformes a ERC-20 devem implementar. Estas funciones são:

- `transfer(address to, uint256 amount)`: transfiere um importe de tokens desde a direção do invocador rumo a a direção especificada.
- `approve(address spender, uint256 amount)`: autoriza a a direção especificada a gastar um importe de tokens em nombre do invocador.
- `allowance(address owner, address spender)`: devuelve o importe de tokens que o «spender» especificado está autorizado a gastar em nombre do «owner» especificado.
- `totalSupply()`: devuelve o número total de tokens em circulación.
- `balanceOf(address owner)`: devuelve o número de tokens que posee a direção especificada.
- `name()`: devuelve o nombre do token.
- `symbol()`: devuelve o símbolo do token.

El estándar ERC-20 também define dois eventos que devem emitirse tras a execução exitosa de as funciones correspondientes:

- `Transfer(address from, address to, uint256 amount)`: emitido quando um importe de tokens se transfiere de uma direção a otra.
- `Approval(address owner, address spender, uint256 amount)`: emitido quando a direção especificada é autorizada a gastar um importe de tokens em nombre do «owner» especificado.

## Impacto

### El crescimento de DeFi e a adoção de Ethereum

El estándar ERC-20 teve um impacto significativo em o ecosistema Ethereum. Ha sido um catalizador clave do movimiento DeFi (finanzas descentralizadas) e também tem contribuido a aumentar a adoção de Ethereum.

Las plataformas DeFi, que oferecem toda uma gama de serviços financeiros que van desde ou préstamo até a gestión de activos, se apoyan masivamente em os tokens para facilitar as transações. Con ERC-20 actuando como um adaptador universal, se volvió muito mais sencillo para as aplicações DeFi integrar um amplio abanico de tokens sem tener que adaptar seu código a cada uno.

El estándar ERC-20 também tem facilitado a gestión de os activos de token por parte de os usuários. Con tokens que respetan as mesmas reglas básicas, a os usuários les resulta mais fácil transferir, gastar e gestionar seus activos de token em várias plataformas. Esta experiência de usuário mejorada foi um motor do aumento de as tasas de adoção de Ethereum.

## Incentivos

### Costes de desenvolvimento reducidos e segurança mejorada

La padronização aportada por o protocolo ERC-20 também teve um impacto econômico directo. Al proporcionar um plano probado e aprobado por a comunidade para a criação de tokens, tem reducido significativamente a barrera de entrada para os desenvolvedores. Ahora podem criar um novo token com costes de desenvolvimento reducidos e um prazo de comercialización mais corto, sem tener que reinventar a rueda. El estándar fomenta também indirectamente a criação de DApps (aplicações descentralizadas) e serviços capaces de interactuar universalmente com cualquier token ERC-20, cultivando así um ecosistema mais dinâmico.

Otro beneficio notable: uma segurança reforzada. El estándar ERC-20 foi sometido a um examen riguroso por parte de a comunidade Ethereum, convirtiéndolo em um modelo robusto e seguro para a implementación de tokens. El respeto de este estándar implica que os aspectos fundamentales do smart contract do token seguem as buenas práticas aceptadas por a comunidade. Esto minimiza o riesgo de vulnerabilidades de segurança que de otro modo poderiam derivarse de um modelo de token mal diseñado. Aunque no é uma garantía contra tudo tipo de vulnerabilidades, é um paso significativo rumo a a segurança global de os tokens e, por extensión, de os projetos que os utilizam.
