---
title: "KyberLib: uno scudo Rust contro le minacce quantistiche"
subtitle: "Un'implementazione Rust robusta di CRYSTALS-Kyber per i servizi finanziari"
description: "KyberLib è un'implementazione Rust robusta di CRYSTALS-Kyber, lo standard NIST FIPS 203 per l'incapsulamento delle chiavi post-quantistico di uso generale."
date: "November 28, 2023"
language: "it-IT"
locale: "it_IT"
banner: "https://cloudcdn.pro/clients/kyberlib/v1/logos/kyberlib.svg"
banner_alt: "Comunicazioni sicure nell'era quantistica con KyberLib"
keywords: "KyberLib, CRYSTALS-Kyber, NIST, FIPS 203, Rust, KEM, post-quantistica, autenticazione"
---

---

> **TL;DR.** KyberLib offre un'implementazione Rust pulita e auditabile dello standard NIST FIPS 203 (CRYSTALS-Kyber). Il fondamento dell'autenticazione di pagamento resistente al quantum.
>
> **Punti chiave**
>
> - **Implementazione di riferimento** — segue la specifica FIPS 203 in modo verificabile e testabile.
> - **Sicurezza Rust** — memory-safety, immunità da buffer overflow, build deterministica.
> - **Performance bancaria** — tempi di esecuzione misurati e prevedibili, adatti a integrazione in motore di autenticazione.
> - **Open source** — disponibile con licenza Apache-2.0 per audit e riuso.

---

[![Reforzar la comunicación segura in la era quantistica con KyberLib](https://cloudcdn.pro/clients/kyberlib/v1/logos/kyberlib.svg).class=\"img-fluid clearfix\"][07]

`KyberLib` è una libreria Rust che protege i suoi dati rispetto alla amenaza potencial della calcolo quantistico. Construida su il **algoritmo [CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html)**, `KyberLib` offre una sicurezza, una eficiencia e una versatilidad excepcionales, integrándose fácilmente in diversas piattaforme, incluidos i entornos `non-std`.

![divider][divider].class=\"m-10 w-100\"

## Asegurar i suoi dati in la era quantistica

Il advenimiento della calcolo quantistico ha introducido una amenaza significativa per le medidas crittografiche convencionales. Per abordar questo sfida, il campo della criptografía resistente a lo quantistico (QSC) evoluciona rapidamente.

Alla vanguardia di questo movimiento transformador, il National Institute of Standards and Technology (NIST) lidera la estandarización dei algoritmos QSC.

In 2023, il NIST retuvo cuatro algoritmos innovadores:

- [**CRYSTALS-Kyber** ⧉][01] (mecanismo di encapsulación di chiavi)
- [**CRYSTALS-Dilithium** ⧉][02] (firmas digitali)
- [**FALCON** ⧉][03] (firmas digitali ligeras)
- [**SPHINCS+** ⧉][04] (firmas digitali basate in hash)

Questi algoritmos revolucionarios se apoyan in principios matemáticos diversos: criptografía su retículos, basata in hash, basata in códigos, con l'obiettivo di fornire una defensa robusta contra i ataques quantistici.

## Explorar la criptografía su retículos

La criptografía su retículos (LBC — Lattice-Based Cryptography) emerge come favorita in QSC, ofreciendo una soluzione prometedora di crittografia post-quantistica (PQC). La LBC è polivalente, con applicazioni che van da i mecanismos di encapsulación di chiavi (KEM) fino a le firmas digitali e i esquemas di cifrado di chiave pública, anclados in i retículos matemáticos.

I retículos sono un concepto fundamental delle matemáticas che hanno hallado applicazioni in diversos campos, tra ellos la criptografía. In términos simples, un retículo è un arreglo regular di puntos in il espacio, formando una estructura semejante a una cuadrícula. Questi puntos sono conectados per líneas, formando una rete di celdas interconectadas. La disposición específica dei puntos e il suo espaciado definen le caratteristiche únicas di un retículo.

### Representación 3D di un retículo con vectores base

Questo gráfico presenta una estructura di retículo 3D generata per tres vectores base:

- `b1 = [1, 0, 0]` in rojo,
- `b2 = [0, 1, 0]` in verde, e
- `b3 = [0, 0, 1]` in azul.

Ogni punto del retículo se forma combinando questi vectores base in proporciones enteras variadas, creando un esquema di cuadrícula che se extiende in le tres dimensiones espaciales. La visualización captura la esencia di un retículo 3D, concepto ampliamente utilizzato in física e matemáticas per representar il arreglo regular e repetido di puntos in il espacio.

![3D Lattice Representation with Basis Vectors][06].class=\"img-fluid mx-auto d-block\"

In criptografía, i retículos se emplean come base di ciertos algoritmos crittografici. La criptografía su retículos aprovecha le propiedades matemáticas dei retículos per creare esquemas crittografici seguros che resistan i ataques dei computer quantistici. I computer quantistici suponen una amenaza significativa per la criptografía convencional, già che possono romper eficientemente algoritmos che se apoyan in la factorización di grandi números o in la resolución dei problemas di logaritmo discreto.

CRYSTALS-Kyber ilustra le fortalezas della LBC, proporcionando una resistencia robusta contra i ataques quantistici insieme con una eficiencia e un tamaño di chiave excepcionales. Il suo compatibilidad multiplataforma e crittografica la convertono in una opción fiable di sicurezza di dati in la era quantistica.

Le especificaciones actuales di CRYSTALS-Kyber sono:

- **Kyber512**: fornisce un livello di sicurezza equivalente al cifrado AES di 128 bits, protegiendo i dati sensibles con una protección standard del settore.
- **Kyber768**: fornisce un livello di sicurezza equivalente al cifrado AES di 256 bits, garantizando la confidencialidad di informazione altamente sensible.
- **Kyber1024**: fornisce un livello di sicurezza che supera AES di 256 bits, ofreciendo una protección robusta contra i ataques quantistici e preservando la integridad dei dati in un futuro lejano.

### Comparación di livelli di sicurezza tra algoritmos clásicos e resistentes a lo quantistico

Questo gráfico ilustra i livelli di sicurezza relativos dei algoritmos crittografici clásicos come RSA-2048 e ECDSA, comparados con le especificaciones delle variantes resistentes a lo quantistico di CRYSTALS-Kyber (Kyber512, Kyber768 e Kyber1024).

Sebbene il gráfico offre una comparación visual, è crucial señalar che i livelli di sicurezza non sono direttamente comparables, già che se basan in principios matemáticos diferentes.

Tuttavia, il gráfico aporta un punto di referencia útil per comprender i livelli di sicurezza dei algoritmos resistentes a lo quantistico.

![Lattice-Based Cryptography][05].class=\"img-fluid mx-auto d-block\"

![divider][divider].class=\"m-10 w-100\"

## KyberLib: una libreria Rust per la criptografía resistente a lo quantistico

KyberLib aprovecha la potencia di CRYSTALS-Kyber per offrire una sicurezza di memoria reforzada e una sicurezza di sistema robusta. Admite diverse especificaciones di CRYSTALS-Kyber (Kyber512, Kyber768, Kyber1024), ofreciendo un abanico di livelli di sicurezza adaptados a i suoi necesidades específicas. Il suo conformidad `no_std` la converte in una elección ideal per i sistemi embebidos, e il suo compatibilidad con WebAssembly (WASM) facilita la integración con le applicazioni web.

![divider][divider].class=\"m-10 w-100\"

## Proteger le applicazioni web mediante la criptografía resistente a lo quantistico

Diseñada per una huella di memoria mínima, KyberLib è ideal per i sistemi embebidos e con recursos limitados, senza comprometer la sicurezza. Il suo implementación in Rust capitaliza le funzionalità di sicurezza del lenguaje, fortificando la sicurezza ofrecida per il algoritmo CRYSTALS-Kyber.

Inoltre, la compatibilidad WebAssembly di KyberLib refuerza il suo utilidad in le applicazioni web, garantizando che siga siendo una strumento vital in il campo dinámico della criptografía.

[Empiece con KyberLib ora stesso. ⧉][00] Fácil di instalar, gratuita per uso personal o commerciale, KyberLib è il suo soluzione di referencia per la criptografía resistente a lo quantistico.

[00]: https://kyberlib.com/getting-started/index.html "Getting Started"
[01]: https://pq-crystals.org/kyber/ "Kyber: A CCA-secure module-lattice-based KEM"
[02]: https://pq-crystals.org/dilithium/ "Dilithium: A CCA-secure lattice-based signature scheme"
[03]: https://falcon-sign.info/ "FALCON: A post-quantum signature scheme"
[04]: https://sphincs.org/ "SPHINCS+: A stateless hash-based signature scheme"
[05]: https://cloudcdn.pro/stocks/diagrams/kyber-vs-classical.svg "Comparison of Security Levels between Classical and Quantum-Resistant Algorithms"
[06]: https://cloudcdn.pro/stocks/diagrams/3D-lattice-graph.svg "3D Lattice Representation with Basis Vectors"
[07]: https://kyberlib.com/ "Privacy and Security in a Quantum World"

[divider]: https://cloudcdn.pro/clients/common/images/elements/divider.svg "Divider"
