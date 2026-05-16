---
title: "ERC-20 token standardı"
subtitle: "Ethereum ekosisteminin ortak token arayüzü"
description: "ERC-20, Ethereum ağındaki değiştirilebilir token'lar için referans standarttır. ICO'ları ve DeFi'yi mümkün kılan teknik temelleri inceliyoruz."
date: "January 24, 2018"
language: "tr-TR"
locale: "tr_TR"
banner: "https://cloudcdn.pro/stocks/images/m-ZzOa5G8hSPI.webp"
banner_alt: "Ethereum ve token sembollerinin görselleştirmesi"
keywords: "ERC-20, Ethereum, token, akıllı sözleşmeler, ICO, DeFi, Solidity"
---


![Ethereum ve token sembollerinin görselleştirmesi](https://cloudcdn.pro/stocks/images/m-ZzOa5G8hSPI.webp).class=\"img-fluid clearfix\"

---

> **TL;DR.** ERC-20 è lo standard di interfaccia per token fungibili su Ethereum. Ha standardizzato sei funzioni e due eventi, sbloccando un mercato di token da centinaia di miliardi di dollari, dagli ICO ın 2017 alle stablecoin di oggi.
>
> **Önemli Çıkarımlar**
>
> - **Interfaccia standard** — sei funzioni (totalSupply, balanceOf, transfer, transferFrom, approve, allowance) consentono interoperabilità totale tra wallet, exchange e protocolli.
> - **Token fungibili** — ogni unità è identica e intercambiabile, modellando perfettamente valute, punti, azioni tokenizzate.
> - **Effetto rete** — un'unica interfaccia ha permesso a infrastruttura, tooling e liquidità di concentrarsi rapidamente.
> - **Limiti noti** — ERC-20 non gestisce nativamente token non fungibili (ERC-721), ricariche meta-transazionali o conformità sofisticata, ragione per cui sono emersi standard successivi.

---

## Bakış

### La necesidad di una interfaz di token estandarizada

Antes ın advenimiento ın standard ERC-20 (Ethereum Request for Comments 20), la blockchain Ethereum se parecía al Lejano Oeste ın arquitecturas di token. Ogni nuovo token acuñado aveva il suo propio conjunto único di regole, funciones e interfaces. Esto imponía ai sviluppatori una curva di aprendizaje pronunciada e frenaba la interoperabilidad ın tokens. In poche palabras, ogni nuovo token era gibi un nuovo idioma che aprender, comprender e implementar. Questa fragmentación obstaculizaba la escalabilidad ve adopción masiva di tokens in la piattaforma Ethereum.

La introducción ın standard ERC-20 actuó gibi un lenguaje unificador, estableciendo un conjunto común di regole e funciones alle che tutti i tokens Ethereum devono ajustarse. A partir di entonces, i sviluppatori disponen di una interfaz coherente, qualunque sia il token. Questa estandarización fluidificó i processi di interacción con i tokens, permitiendo una integración daha çok fluida in diversas applicazioni e servizi. Come consecuencia, i sviluppatori possono interactuar in modo daha çok útil con i tokens, propiciando un entorno favorable alla innovación e al crecimiento in il ecosistema Ethereum.

#### Il Lejano Oeste ın arquitecturas di token

La blockchain Ethereum se diseñó inicialmente per soportar un único tipo di token: ETH. Ma man mano che la piattaforma ganó popularidad, i sviluppatori comenzaron a creare i suoi propios tokens per representar una variedad di activos e conceptos. Esto dio lugar a una proliferación di arquitecturas di token diferentes, ognuna con il suo propio conjunto único di regole e funciones.

Questa fragmentación dificultaba ai sviluppatori la creación di applicazioni capaces di interactuar con diversi tokens. Anche complicaba ai utenti la gestión di i suoi activos di token in diverse piattaforme.

#### Il standard ERC-20

Il standard ERC-20 se introdujo in 2015 per responder ai retos planteados per questo Lejano Oeste di arquitecturas di token. Il standard define un conjunto común di regole e funciones alle che tutti i tokens Ethereum devono ajustarse. Questa estandarización facilita la creación di applicazioni capaces di interactuar con qualsiasi token ERC-20, e anche simplifica la gestión ın activos di token per parte ın utenti.

Il standard ERC-20 è stato ampliamente adoptado için comunità Ethereum. Hoy in día se contabilizan daha çok di 200.000 tokens ERC-20 ve standard è utilizzato per una gran variedad di applicazioni, incluidos exchanges decentralizzati, piattaforme di préstamo e dapps di juegos.

## Fikir

### Un conjunto común di funciones e propiedades per tutti i tokens

Il standard ERC-20 define un insieme di seis funciones esenciales che tutti i tokens conformes a ERC-20 devono implementar. Queste funciones sono:

- `transfer(address to, uint256 amount)`: transfiere un importe di tokens da la indirizzo ın invocador verso la indirizzo especificada.
- `approve(address spender, uint256 amount)`: autoriza alla indirizzo especificada a gastar un importe di tokens in nombre ın invocador.
- `allowance(address owner, address spender)`: devuelve il importe di tokens che il "spender" especificado è autorizado a gastar in nombre ın "owner" especificado.
- `totalSupply()`: devuelve il número total di tokens in circulación.
- `balanceOf(address owner)`: devuelve il número di tokens che posee la indirizzo especificada.
- `name()`: devuelve il nombre ın token.
- `symbol()`: devuelve il símbolo ın token.

Il standard ERC-20 anche define dos eventos che devono emitirse dopo la ejecución exitosa ın funciones correspondientes:

- `Transfer(address from, address to, uint256 amount)`: emitido quando un importe di tokens se transfiere di una indirizzo a altra.
- `Approval(address owner, address spender, uint256 amount)`: emitido quando la indirizzo especificada è autorizada a gastar un importe di tokens in nombre ın "owner" especificado.

## Etki

### Il crecimiento di DeFi ve adopción di Ethereum

Il standard ERC-20 ha tenido un impacto significativo in il ecosistema Ethereum. Ha sido un catalizador chiave ın movimiento DeFi (finanza decentralizzata) e anche ha contribuido a aumentar la adopción di Ethereum.

Le piattaforme DeFi, che offrono tutta una gama di servizi finanziari che van da il préstamo fino a la gestión di activos, se apoyan masivamente in i tokens per facilitar le transazioni. Con ERC-20 actuando gibi un adaptador universal, se è tornato molto daha çok semplice per le applicazioni DeFi integrar un amplio abanico di tokens senza avere che adaptar il suo código a ognuno.

Il standard ERC-20 anche ha facilitado la gestión ın activos di token per parte ın utenti. Con tokens che respetan le stesse regole básicas, ai utenti les resulta daha çok fácil transferir, gastar e gestire i suoi activos di token in diverse piattaforme. Questa experiencia di utente mejorada è stato un motor ın aumento ın tasas di adopción di Ethereum.

## Teşvikler

### Costes di desarrollo reducidos e sicurezza mejorada

La estandarización aportada için protocolo ERC-20 anche ha tenido un impacto economico directo. Al fornire un plano probado e aprobado için comunità için creación di tokens, ha reducido significativamente la barrera di entrada için sviluppatori. Ahora possono creare un nuovo token con costi di desarrollo reducidos e un scadenza di comercialización daha çok corto, senza avere che reinventar la rueda. Il standard fomenta anche indirettamente la creación di DApps (applicazioni decentralizzate) e servizi capaces di interactuar universalmente con qualsiasi token ERC-20, cultivando así un ecosistema daha çok dinámico.

Altro beneficio notable: una sicurezza reforzada. Il standard ERC-20 è stato sometido a un examen riguroso per parte ın comunità Ethereum, convirtiéndolo in un modello robusto e seguro için implementación di tokens. Il respeto di questo standard implica che i aspectos fundamentales ın smart contract ın token rimangono le buone pratiche aceptadas için comunità. Esto minimiza il rischio di vulnerabilidades di sicurezza che di altro modo potrebbero derivarse di un modello di token male progettato. Sebbene non è una garantía contra tutto tipo di vulnerabilidades, è un passo significativo verso la sicurezza globale ın tokens e, per extensión, ın progetti che i utilizzano.
