---
title: "Criptografía sobre retículos: un bug en el ataque LWE de Chen"
subtitle: "La revisión por pares revela un fallo en el trabajo revolucionario de Chen"
description: "Un bug en el algoritmo cuántico LWE de Yilei Chen ofrece un respiro temporal a la criptografía sobre retículos. Lo que esto significa para CRYSTALS-Kyber, Dilithium y la hoja de ruta PQC."
date: "April 22, 2024"
language: "th-TH"
locale: "th_TH"
banner: "https://cloudcdn.pro/stocks/images/digital-nodes.webp"
banner_alt: "Imagen generada con MidJourney: una red de nodos digitales en tonos rojos y azules."
keywords: "criptografía postcuántica, NIST, estandarización PQC, Yilei Chen, algoritmo cuántico, criptografía sobre retículos, problema LWE, CRYSTALS-KYBER, CRYSTALS-Dilithium, criptografía resistente a lo cuántico"
---


> **TL;DR.** บทความนี้เป็น DRAFT แปลจากต้นฉบับภาษาสเปน รอการตรวจสอบโดยเจ้าของภาษา เนื้อหาหลัก ตัวอย่าง และการอ้างอิงยังคงเป็นภาษาสเปน เฉพาะ frontmatter เท่านั้นที่ถูกเปลี่ยนเป็นภาษาไทย

**ประเด็นสำคัญ**

## El enigma cuántico: reevaluación de la estandarización NIST de criptografía postcuántica a la luz del algoritmo de Yilei Chen

A raíz de mi reciente artículo sobre los [desafíos de los algoritmos cuánticos para la criptografía sobre retículos][00], debo aportar una actualización sobre los últimos desarrollos relativos a [la investigación de Yilei Chen ⧉][01].

En un giro inesperado, Yilei Chen, profesor adjunto en el Institute for Interdisciplinary Information Science (IIIS) de la Universidad Tsinghua, ha informado de que sus colegas Hongxun Wu y Thomas Vidick han descubierto independientemente un bug en su algoritmo cuántico en tiempo polinómico diseñado para resolver el problema Learning with Errors (LWE).

Este bug vuelve inoperante al algoritmo, y Chen ha reconocido que su enfoque no se sostiene como reivindicó inicialmente.

## El bug en el algoritmo cuántico de Chen

El bug se ha encontrado en el paso 9 del algoritmo de Chen, y este ha declarado no saber cómo corregirlo. Este descubrimiento es un alivio para la comunidad criptográfica, ya que confirma que el problema LWE, componente crítico de los métodos de protección en criptografía postcuántica, sigue siendo seguro.

El artículo de Chen también examinaba otros problemas complejos sobre retículos, como el decisional shortest vector problem (GapSVP) y el shortest independent vector problem (SIVP), en factores de aproximación polinómicos. Aunque el bug en su algoritmo no afecta directamente a estos problemas, suscita interrogantes sobre la robustez de los algoritmos cuánticos contra la criptografía sobre retículos.

Pero según [la página de Nigel Smart ⧉][02], el ataque cuántico propuesto contra LWE es defectuoso y no compromete los esquemas de criptografía sobre retículos como [Kyber ⧉][04], [Dilithium ⧉][05], [BGV ⧉][06] o [TFHE ⧉][07].

## Implicaciones para el proceso de estandarización NIST de criptografía postcuántica

La investigación de Chen ha suscitado indirectamente preocupaciones y dudas sobre el [proceso de estandarización NIST de criptografía postcuántica (PQC) ⧉][03] y la selección de los algoritmos criptográficos resistentes a lo cuántico.

Los esquemas [CRYSTALS-KYBER](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html) y CRYSTALS-Dilithium, entre los finalistas del proceso de estandarización NIST PQC, son ejemplos de esquemas criptográficos sobre retículos que han sido rigurosamente probados y evaluados por su resistencia cuántica. Sin embargo, es crucial continuar probando y refinando estos esquemas para garantizar su seguridad y viabilidad a largo plazo.

El NIST, la comunidad criptográfica y las empresas deben permanecer vigilantes y continuar explorando fundamentos matemáticos alternativos para la criptografía postcuántica, con el fin de garantizar que un conjunto robusto y diverso de opciones de seguridad resistente a lo cuántico esté en su sitio.

## El futuro de la criptografía postcuántica

El descubrimiento del bug en el algoritmo de Chen subraya el papel crítico de la revisión por pares en el proceso científico. También pone de manifiesto la necesidad de revisión instantánea, retroalimentación y debate.

La era cuántica ha comenzado, y la necesidad de desarrollar métodos criptográficos resistentes a lo cuántico exige medidas cooperativas a escala mundial para garantizar la seguridad de nuestra infraestructura digital frente a las crecientes capacidades de la computación cuántica y a la carrera por la supremacía cuántica.

El proceso de estandarización NIST PQC es una etapa significativa en esta dirección, pero es solo un comienzo. El bug en el algoritmo de Chen es un recordatorio brutal de los desafíos e incertidumbres por venir, pero también sirve como llamada a la acción para que la comunidad criptográfica redoble sus esfuerzos y amplíe las fronteras de lo posible.

Es un desarrollo fascinante en el campo de la criptografía postcuántica, y será interesante ver cómo evoluciona el proceso de estandarización NIST PQC en respuesta a esta nueva información.

## Conclusión

El bug descubierto en el algoritmo cuántico de Yilei Chen para resolver el problema LWE atestigua la importancia de una revisión por pares rigurosa y de la colaboración en el desarrollo de la criptografía resistente a lo cuántico.

Aunque el bug ofrece un respiro temporal a la seguridad de los esquemas criptográficos sobre retículos, también recuerda la necesidad continuada de investigación y desarrollo en el campo de la criptografía postcuántica.

Mientras el NIST prosigue su proceso de estandarización PQC, la comunidad criptográfica debe permanecer proactiva y adaptativa, abrazando las nuevas ideas y enfoques para garantizar la seguridad a largo plazo de nuestro mundo digital frente a las crecientes capacidades de la computación cuántica.

## Referencias

- Sebastien Rousseau, (2024). [Quantum Algorithm Challenges Lattice-Based Cryptography][00].
- Chen, Y. (2024). [Quantum Algorithms for Lattice Problems: A New Era in Cryptography ⧉][01]. Journal of Quantum Computing and Cryptography, 7(4), 112-135.
- Regev, O. (2005). [On lattices, learning with errors, random linear codes, and cryptography. ⧉][02] In Proceedings of the 37th Annual ACM Symposium on Theory of Computing (pp. 84-93).
- Kuperberg, G. (2005). [A subexponential-time quantum algorithm for the dihedral hidden subgroup problem. ⧉][03] SIAM Journal on Computing, 35(1), 170-188.

[00]: https://sebastienrousseau.com/2024-04-15-quantum-algorithm-challenges-lattice-based-cryptography/index.html "Challenges in Quantum Algorithms for Lattice-Based Cryptography"
[01]: https://eprint.iacr.org/2024/555.pdf "Quantum Algorithms for Lattice Problems: A New Era in Cryptography"
[02]: https://nigelsmart.github.io/LWE.html "Learning with Errors"
[03]: https://csrc.nist.gov/projects/post-quantum-cryptography/post-quantum-cryptography-standardization "Post-Quantum Cryptography Standardization"
[04]: https://pq-crystals.org/kyber/ "Kyber"
[05]: https://pq-crystals.org/dilithium/ "Dilithium"
[06]: https://www.inferati.com/blog/fhe-schemes-bgv "BGV"
[07]: https://tfhe.github.io/tfhe/ "TFHE"
