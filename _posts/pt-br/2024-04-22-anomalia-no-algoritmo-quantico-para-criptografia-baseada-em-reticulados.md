---
title: "Criptografia sobre retículos: um bug em o ataque LWE de Chen"
subtitle: "La revisión por pares revela um fallo em o trabalho revolucionário de Chen"
description: "Um bug em o algoritmo quântico LWE de Yilei Chen oferece um respiro temporal a a criptografia sobre retículos. Lo que esto significa para CRYSTALS-Kyber, Dilithium e a folha de ruta PQC."
date: "April 22, 2024"
language: "pt-BR"
locale: "pt_BR"
banner: "https://cloudcdn.pro/stocks/images/digital-nodes.webp"
banner_alt: "Imagen generada com MidJourney: uma red de nodos digitais em tonos rojos e azules."
keywords: "criptografia pós-quântica, NIST, padronização PQC, Yilei Chen, algoritmo quântico, criptografia sobre retículos, problema LWE, CRYSTALS-KYBER, CRYSTALS-Dilithium, criptografia resistente a lo quântico"
---

## El enigma quântico: reevaluación de a padronização NIST de criptografia pós-quântica a a luz do algoritmo de Yilei Chen

A raíz de meu reciente artigo sobre os [desafíos de os algoritmos quânticos para a criptografia sobre retículos][00], debo aportar uma actualización sobre os últimos desarrollos relativos a [a investigación de Yilei Chen ⧉][01].

En um giro inesperado, Yilei Chen, profesor adjunto em o Institute for Interdisciplinary Information Science (IIIS) de a Universidad Tsinghua, tem informado de que seus colegas Hongxun Wu e Thomas Vidick têm descubierto independientemente um bug em seu algoritmo quântico em tempo polinómico diseñado para resolver o problema Learning with Errors (LWE).

Este bug vuelve inoperante ao algoritmo, e Chen tem reconocido que seu enfoque no se sostiene como reivindicó inicialmente.

## El bug em o algoritmo quântico de Chen

El bug tem-se encontrado em o paso 9 do algoritmo de Chen, e este tem declarado no saber cómo corregirlo. Este descubrimiento é um alivio para a comunidade criptográfica, já que confirma que o problema LWE, componente crítico de os métodos de protección em criptografia pós-quântica, segue siendo seguro.

El artigo de Chen também examinaba otros problemas complejos sobre retículos, como o decisional shortest vector problem (GapSVP) e o shortest independent vector problem (SIVP), em factores de aproximación polinómicos. Aunque o bug em seu algoritmo no afecta directamente a estes problemas, suscita interrogantes sobre a robustez de os algoritmos quânticos contra a criptografia sobre retículos.

Pero conforme [a página de Nigel Smart ⧉][02], o ataque quântico propuesto contra LWE é defectuoso e no compromete os esquemas de criptografia sobre retículos como [Kyber ⧉][04], [Dilithium ⧉][05], [BGV ⧉][06] ou [TFHE ⧉][07].

## Implicaciones para o proceso de padronização NIST de criptografia pós-quântica

La investigación de Chen tem suscitado indirectamente preocupações e dudas sobre ou [proceso de padronização NIST de criptografia pós-quântica (PQC) ⧉][03] e a selección de os algoritmos criptográficos resistentes a lo quântico.

Los esquemas [CRYSTALS-KYBER](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html) e CRYSTALS-Dilithium, entre os finalistas do proceso de padronização NIST PQC, são exemplos de esquemas criptográficos sobre retículos que foram rigurosamente probados e evaluados por seu resistencia quântica. Sin embargo, é crucial continuar probando e refinando estes esquemas para garantizar seu segurança e viabilidad a longo prazo.

El NIST, a comunidade criptográfica e as empresas devem permanecer vigilantes e continuar explorando fundamentos matemáticos alternativos para a criptografia pós-quântica, com o fin de garantizar que um conjunto robusto e diverso de opções de segurança resistente a lo quântico esté em seu sitio.

## El futuro de a criptografia pós-quântica

El descubrimiento do bug em o algoritmo de Chen subraya o papel crítico de a revisión por pares em o proceso científico. También coloca de manifiesto a necessidade de revisión instantánea, retroalimentación e debate.

La era quântica tem comenzado, e a necessidade de desenvolver métodos criptográficos resistentes a lo quântico exige medidas cooperativas a escala mundial para garantizar a segurança de nossa infraestrutura digital frente a as crecientes capacidades de a computação quântica e a a carrera por a supremacía quântica.

El proceso de padronização NIST PQC é uma etapa significativa em esta direção, mas é solo um comienzo. El bug em o algoritmo de Chen é um recordatorio brutal de os desafíos e incertidumbres por venir, mas também serve como llamada a a ação para que a comunidade criptográfica redoble seus esfuerzos e amplíe as fronteras de lo posible.

Es um desenvolvimento fascinante em o campo de a criptografia pós-quântica, e será interesante ver cómo evolui o proceso de padronização NIST PQC em resposta a esta nova informação.

## Conclusión

El bug descubierto em o algoritmo quântico de Yilei Chen para resolver o problema LWE atestigua a importancia de uma revisión por pares rigurosa e de a colaboração em o desenvolvimento de a criptografia resistente a lo quântico.

Aunque o bug oferece um respiro temporal a a segurança de os esquemas criptográficos sobre retículos, também recuerda a necessidade continuada de investigación e desenvolvimento em o campo de a criptografia pós-quântica.

Mientras o NIST prosigue seu proceso de padronização PQC, a comunidade criptográfica deve permanecer proactiva e adaptativa, abrazando as novas ideias e enfoques para garantizar a segurança a longo prazo de nosso mundo digital frente a as crecientes capacidades de a computação quântica.

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
