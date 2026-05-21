---
title: "KyberLib: CRYSTALS-Kyber en Rust para el postcuántico"
subtitle: "KyberLib, una implementación Rust robusta de CRYSTALS-Kyber para la era cuántica"
description: "Implementación criptográfica robusta y resistente a lo cuántico del algoritmo CRYSTALS-Kyber, para proteger sus datos de las amenazas cuánticas y ataques criptoanalíticos."
date: "November 28, 2023"
language: "cs-CZ"
locale: "cs_CZ"
banner: "https://cloudcdn.pro/clients/kyberlib/v1/logos/kyberlib.svg"
banner_alt: "Reforzar la comunicación segura en la era cuántica con KyberLib"
keywords: "KyberLib, Rust CRYSTALS-Kyber, criptografía postcuántica, criptografía sobre retículos, intercambio de claves resistente a lo cuántico, NIST FIPS 203, Sebastien Rousseau, KEM, autenticación de pagos, biblioteca PQC"
---


> **TL;DR.** Tento článek je DRAFT překlad původně španělského zdroje, čekající na revizi rodilým mluvčím. Hlavní obsah, příklady a citace zůstávají ve španělštině; pouze záhlaví/frontmatter byly přepnuty na češtinu.

**Klíčové body**

[![Reforzar la comunicación segura en la era cuántica con KyberLib](https://cloudcdn.pro/clients/kyberlib/v1/logos/kyberlib.svg).class=\"img-fluid clearfix\"][07]

`KyberLib` es una biblioteca Rust que protege sus datos frente a la amenaza potencial de la computación cuántica. Construida sobre el **algoritmo [CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html)**, `KyberLib` ofrece una seguridad, una eficiencia y una versatilidad excepcionales, integrándose fácilmente en diversas plataformas, incluidos los entornos `no-std`.

![divider][divider].class=\"m-10 w-100\"

## Asegurar sus datos en la era cuántica

El advenimiento de la computación cuántica ha introducido una amenaza significativa para las medidas criptográficas convencionales. Para abordar este desafío, el campo de la criptografía resistente a lo cuántico (QSC) evoluciona rápidamente.

A la vanguardia de este movimiento transformador, el National Institute of Standards and Technology (NIST) lidera la estandarización de los algoritmos QSC.

En 2023, el NIST retuvo cuatro algoritmos innovadores:

- [**CRYSTALS-Kyber** ⧉][01] (mecanismo de encapsulación de claves)
- [**CRYSTALS-Dilithium** ⧉][02] (firmas digitales)
- [**FALCON** ⧉][03] (firmas digitales ligeras)
- [**SPHINCS+** ⧉][04] (firmas digitales basadas en hash)

Estos algoritmos revolucionarios se apoyan en principios matemáticos diversos: criptografía sobre retículos, basada en hash, basada en códigos, con el objetivo de proporcionar una defensa robusta contra los ataques cuánticos.

## Explorar la criptografía sobre retículos

La criptografía sobre retículos (LBC — Lattice-Based Cryptography) emerge como favorita en QSC, ofreciendo una solución prometedora de criptografía postcuántica (PQC). La LBC es polivalente, con aplicaciones que van desde los mecanismos de encapsulación de claves (KEM) hasta las firmas digitales y los esquemas de cifrado de clave pública, anclados en los retículos matemáticos.

Los retículos son un concepto fundamental de las matemáticas que han hallado aplicaciones en diversos campos, entre ellos la criptografía. En términos simples, un retículo es un arreglo regular de puntos en el espacio, formando una estructura semejante a una cuadrícula. Estos puntos están conectados por líneas, formando una red de celdas interconectadas. La disposición específica de los puntos y su espaciado definen las características únicas de un retículo.

### Representación 3D de un retículo con vectores base

Este gráfico presenta una estructura de retículo 3D generada por tres vectores base:

- `b1 = [1, 0, 0]` en rojo,
- `b2 = [0, 1, 0]` en verde, y
- `b3 = [0, 0, 1]` en azul.

Cada punto del retículo se forma combinando estos vectores base en proporciones enteras variadas, creando un esquema de cuadrícula que se extiende en las tres dimensiones espaciales. La visualización captura la esencia de un retículo 3D, concepto ampliamente utilizado en física y matemáticas para representar el arreglo regular y repetido de puntos en el espacio.

![3D Lattice Representation with Basis Vectors][06].class=\"img-fluid mx-auto d-block\"

En criptografía, los retículos se emplean como base de ciertos algoritmos criptográficos. La criptografía sobre retículos aprovecha las propiedades matemáticas de los retículos para crear esquemas criptográficos seguros que resistan los ataques de los ordenadores cuánticos. Los ordenadores cuánticos suponen una amenaza significativa para la criptografía convencional, ya que pueden romper eficientemente algoritmos que se apoyan en la factorización de grandes números o en la resolución de los problemas de logaritmo discreto.

CRYSTALS-Kyber ilustra las fortalezas de la LBC, proporcionando una resistencia robusta contra los ataques cuánticos junto con una eficiencia y un tamaño de clave excepcionales. Su compatibilidad multiplataforma y criptográfica la convierten en una opción fiable de seguridad de datos en la era cuántica.

Las especificaciones actuales de CRYSTALS-Kyber son:

- **Kyber512**: proporciona un nivel de seguridad equivalente al cifrado AES de 128 bits, protegiendo los datos sensibles con una protección estándar del sector.
- **Kyber768**: proporciona un nivel de seguridad equivalente al cifrado AES de 256 bits, garantizando la confidencialidad de información altamente sensible.
- **Kyber1024**: proporciona un nivel de seguridad que supera AES de 256 bits, ofreciendo una protección robusta contra los ataques cuánticos y preservando la integridad de los datos en un futuro lejano.

### Comparación de niveles de seguridad entre algoritmos clásicos y resistentes a lo cuántico

Este gráfico ilustra los niveles de seguridad relativos de los algoritmos criptográficos clásicos como RSA-2048 y ECDSA, comparados con las especificaciones de las variantes resistentes a lo cuántico de CRYSTALS-Kyber (Kyber512, Kyber768 y Kyber1024).

Aunque el gráfico ofrece una comparación visual, es crucial señalar que los niveles de seguridad no son directamente comparables, ya que se basan en principios matemáticos diferentes.

Sin embargo, el gráfico aporta un punto de referencia útil para comprender los niveles de seguridad de los algoritmos resistentes a lo cuántico.

![Lattice-Based Cryptography][05].class=\"img-fluid mx-auto d-block\"

![divider][divider].class=\"m-10 w-100\"

## KyberLib: una biblioteca Rust para la criptografía resistente a lo cuántico

KyberLib aprovecha la potencia de CRYSTALS-Kyber para ofrecer una seguridad de memoria reforzada y una seguridad de sistema robusta. Admite varias especificaciones de CRYSTALS-Kyber (Kyber512, Kyber768, Kyber1024), ofreciendo un abanico de niveles de seguridad adaptados a sus necesidades específicas. Su conformidad `no_std` la convierte en una elección ideal para los sistemas embebidos, y su compatibilidad con WebAssembly (WASM) facilita la integración con las aplicaciones web.

![divider][divider].class=\"m-10 w-100\"

## Proteger las aplicaciones web mediante la criptografía resistente a lo cuántico

Diseñada para una huella de memoria mínima, KyberLib es ideal para los sistemas embebidos y con recursos limitados, sin comprometer la seguridad. Su implementación en Rust capitaliza las funcionalidades de seguridad del lenguaje, fortificando la seguridad ofrecida por el algoritmo CRYSTALS-Kyber.

Además, la compatibilidad WebAssembly de KyberLib refuerza su utilidad en las aplicaciones web, garantizando que siga siendo una herramienta vital en el campo dinámico de la criptografía.

[Empiece con KyberLib ahora mismo. ⧉][00] Fácil de instalar, gratuita para uso personal o comercial, KyberLib es su solución de referencia para la criptografía resistente a lo cuántico.

[00]: https://kyberlib.com/getting-started/index.html "Getting Started"
[01]: https://pq-crystals.org/kyber/ "Kyber: A CCA-secure module-lattice-based KEM"
[02]: https://pq-crystals.org/dilithium/ "Dilithium: A CCA-secure lattice-based signature scheme"
[03]: https://falcon-sign.info/ "FALCON: A post-quantum signature scheme"
[04]: https://sphincs.org/ "SPHINCS+: A stateless hash-based signature scheme"
[05]: https://cloudcdn.pro/stocks/diagrams/kyber-vs-classical.svg "Comparison of Security Levels between Classical and Quantum-Resistant Algorithms"
[06]: https://cloudcdn.pro/stocks/diagrams/3D-lattice-graph.svg "3D Lattice Representation with Basis Vectors"
[07]: https://kyberlib.com/ "Privacy and Security in a Quantum World"

[divider]: https://cloudcdn.pro/clients/common/images/elements/divider.svg "Divider"
