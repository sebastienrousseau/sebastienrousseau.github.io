---
title: "KyberLib: CRYSTALS-Kyber em Rust para o pós-quântico"
subtitle: "KyberLib, uma implementación Rust robusta de CRYSTALS-Kyber para a era quântica"
description: "Implementación criptográfica robusta e resistente a lo quântico do algoritmo CRYSTALS-Kyber, para proteger seus dados de as ameaças quânticas e ataques criptoanalíticos."
date: "November 28, 2023"
language: "pt-BR"
locale: "pt_BR"
banner: "https://cloudcdn.pro/clients/kyberlib/v1/logos/kyberlib.svg"
banner_alt: "Reforzar a comunicação segura em a era quântica com KyberLib"
keywords: "KyberLib, Rust CRYSTALS-Kyber, criptografia pós-quântica, criptografia sobre retículos, intercambio de claves resistente a lo quântico, NIST FIPS 203, Sebastien Rousseau, KEM, autenticação de pagos, biblioteca PQC"
---

[![Reforzar a comunicação segura em a era quântica com KyberLib](https://cloudcdn.pro/clients/kyberlib/v1/logos/kyberlib.svg).class=\"img-fluid clearfix\"][07]

`KyberLib` é uma biblioteca Rust que protege seus dados frente a a amenaza potencial de a computação quântica. Construida sobre ou **algoritmo [CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html)**, `KyberLib` oferece uma segurança, uma eficiência e uma versatilidad excepcionales, integrándose facilmente em diversas plataformas, incluídos os entornos `no-std`.

![divider][divider].class=\"m-10 w-100\"

## Asegurar seus dados em a era quântica

El advenimiento de a computação quântica tem introducido uma amenaza significativa para as medidas criptográficas convencionales. Para abordar este desafío, o campo de a criptografia resistente a lo quântico (QSC) evolui rapidamente.

A a vanguarda de este movimiento transformador, o National Institute of Standards and Technology (NIST) lidera a padronização de os algoritmos QSC.

En 2023, o NIST retuvo quatro algoritmos innovadores:

- [**CRYSTALS-Kyber** ⧉][01] (mecanismo de encapsulación de claves)
- [**CRYSTALS-Dilithium** ⧉][02] (firmas digitais)
- [**FALCON** ⧉][03] (firmas digitais ligeras)
- [**SPHINCS+** ⧉][04] (firmas digitais basadas em hash)

Estos algoritmos revolucionários se apoyan em principios matemáticos diversos: criptografia sobre retículos, basada em hash, basada em códigos, com o objetivo de proporcionar uma defensa robusta contra os ataques quânticos.

## Explorar a criptografia sobre retículos

La criptografia sobre retículos (LBC — Lattice-Based Cryptography) emerge como favorita em QSC, ofreciendo uma solução prometedora de criptografia pós-quântica (PQC). La LBC é polivalente, com aplicações que van desde os mecanismos de encapsulación de claves (KEM) até as firmas digitais e os esquemas de criptografia de clave pública, anclados em os retículos matemáticos.

Los retículos são um concepto fundamental de as matemáticas que têm hallado aplicações em diversos campos, entre olos a criptografia. En términos simples, um retículo é um arreglo regular de pontos em o espacio, formando uma estructura semejante a uma cuadrícula. Estos pontos estão conectados por linhas, formando uma red de celdas interconectadas. La disposición específica de os pontos e seu espaciado definen as características únicas de um retículo.

### Representación 3D de um retículo com vectores base

Este gráfico presenta uma estructura de retículo 3D generada por três vectores base:

- `b1 = [1, 0, 0]` em rojo,
- `b2 = [0, 1, 0]` em verde, e
- `b3 = [0, 0, 1]` em azul.

Cada ponto do retículo se forma combinando estes vectores base em proporciones enteras variadas, criando um esquema de cuadrícula que se extiende em as três dimensões espaciales. La visualización captura a esencia de um retículo 3D, concepto ampliamente utilizado em física e matemáticas para representar o arreglo regular e repetido de pontos em o espacio.

![3D Lattice Representation with Basis Vectors][06].class=\"img-fluid mx-auto d-block\"

En criptografia, os retículos se emplean como base de ciertos algoritmos criptográficos. La criptografia sobre retículos aproveita as propriedades matemáticas de os retículos para criar esquemas criptográficos seguros que resistan os ataques de os computadores quânticos. Los computadores quânticos suponen uma amenaza significativa para a criptografia convencional, já que podem romper eficientemente algoritmos que se apoyan em a factorización de grandes números ou em a resolución de os problemas de logaritmo discreto.

CRYSTALS-Kyber ilustra as fortalezas de a LBC, proporcionando uma resistencia robusta contra os ataques quânticos junto com uma eficiência e um tamaño de clave excepcionales. Su compatibilidade multiplataforma e criptográfica a convierten em uma opção fiable de segurança de dados em a era quântica.

Las especificaciones actuales de CRYSTALS-Kyber são:

- **Kyber512**: proporciona um nivel de segurança equivalente ao criptografia AES de 128 bits, protegiendo os dados sensibles com uma protección estándar do sector.
- **Kyber768**: proporciona um nivel de segurança equivalente ao criptografia AES de 256 bits, garantizando a confidencialidad de informação altamente sensible.
- **Kyber1024**: proporciona um nivel de segurança que supera AES de 256 bits, ofreciendo uma protección robusta contra os ataques quânticos e preservando a integridad de os dados em um futuro lejano.

### Comparación de niveles de segurança entre algoritmos clásicos e resistentes a lo quântico

Este gráfico ilustra os niveles de segurança relativos de os algoritmos criptográficos clásicos como RSA-2048 e ECDSA, comparados com as especificaciones de as variantes resistentes a lo quântico de CRYSTALS-Kyber (Kyber512, Kyber768 e Kyber1024).

Aunque o gráfico oferece uma comparación visual, é crucial señalar que os niveles de segurança no são directamente comparables, já que se basan em principios matemáticos diferentes.

Sin embargo, o gráfico aporta um ponto de referencia útil para compreender os niveles de segurança de os algoritmos resistentes a lo quântico.

![Lattice-Based Cryptography][05].class=\"img-fluid mx-auto d-block\"

![divider][divider].class=\"m-10 w-100\"

## KyberLib: uma biblioteca Rust para a criptografia resistente a lo quântico

KyberLib aproveita a potencia de CRYSTALS-Kyber para oferecer uma segurança de memoria reforzada e uma segurança de sistema robusta. Admite várias especificaciones de CRYSTALS-Kyber (Kyber512, Kyber768, Kyber1024), ofreciendo um abanico de niveles de segurança adaptados a seus necessidades específicas. Su conformidad `no_std` a convierte em uma elección ideal para os sistemas embebidos, e seu compatibilidade com WebAssembly (WASM) facilita a integração com as aplicações web.

![divider][divider].class=\"m-10 w-100\"

## Proteger as aplicações web mediante a criptografia resistente a lo quântico

Diseñada para uma huella de memoria mínima, KyberLib é ideal para os sistemas embebidos e com recursos limitados, sem comprometer a segurança. Su implementación em Rust capitaliza as funcionalidades de segurança do lenguaje, fortificando a segurança ofrecida por o algoritmo CRYSTALS-Kyber.

Além disso, a compatibilidade WebAssembly de KyberLib refuerza seu utilidad em as aplicações web, garantizando que siga siendo uma ferramenta vital em o campo dinâmico de a criptografia.

[Empiece com KyberLib agora mesmo. ⧉][00] Fácil de instalar, gratuita para uso personal ou comercial, KyberLib é seu solução de referencia para a criptografia resistente a lo quântico.

[00]: https://kyberlib.com/getting-started/index.html "Getting Started"
[01]: https://pq-crystals.org/kyber/ "Kyber: A CCA-secure module-lattice-based KEM"
[02]: https://pq-crystals.org/dilithium/ "Dilithium: A CCA-secure lattice-based signature scheme"
[03]: https://falcon-sign.info/ "FALCON: A post-quantum signature scheme"
[04]: https://sphincs.org/ "SPHINCS+: A stateless hash-based signature scheme"
[05]: https://cloudcdn.pro/stocks/diagrams/kyber-vs-classical.svg "Comparison of Security Levels between Classical and Quantum-Resistant Algorithms"
[06]: https://cloudcdn.pro/stocks/diagrams/3D-lattice-graph.svg "3D Lattice Representation with Basis Vectors"
[07]: https://kyberlib.com/ "Privacy and Security in a Quantum World"

[divider]: https://cloudcdn.pro/clients/common/images/elements/divider.svg "Divider"
