---
title: "Cryptographie sur réseaux : un bug dans l'attaque LWE de Chen"
subtitle: "La revue par les pairs révèle une faille dans le travail révolutionnaire de Chen"
description: "Un bug dans l'algorithme quantique LWE de Yilei Chen offre un sursis temporaire à la cryptographie sur réseaux. Ce que cela signifie pour CRYSTALS-Kyber, Dilithium et la feuille de route PQC."
date: "April 22, 2024"
language: "fr"
locale: "fr_FR"
banner: "https://cloudcdn.pro/stocks/images/digital-nodes.webp"
banner_alt: "Image générée avec MidJourney — un réseau de nœuds numériques aux tons rouges et bleus."
keywords: "cryptographie post-quantique, NIST, standardisation PQC, Yilei Chen, algorithme quantique, cryptographie sur réseaux, problème LWE, CRYSTALS-KYBER, CRYSTALS-Dilithium, cryptographie quantique-résistante"
---

## L'énigme quantique : réévaluation de la standardisation NIST de cryptographie post-quantique à la lumière de l'algorithme de Yilei Chen

Suite à mon article récent sur les [défis des algorithmes quantiques pour la cryptographie sur réseaux][00], je dois apporter une mise à jour sur les derniers développements concernant [la recherche de Yilei Chen ⧉][01].

Dans un retournement inattendu, Yilei Chen, professeur adjoint à l'Institute for Interdisciplinary Information Science (IIIS) de l'Université Tsinghua, a rapporté que ses confrères Hongxun Wu et Thomas Vidick ont indépendamment découvert un bug dans son algorithme quantique en temps polynomial conçu pour résoudre le problème Learning with Errors (LWE).

Ce bug rend l'algorithme inopérant, et Chen a reconnu que son approche ne tient pas comme initialement revendiqué.

## Le bug dans l'algorithme quantique de Chen

Le bug a été trouvé à l'étape 9 de l'algorithme de Chen, et il a déclaré ne pas savoir comment le corriger. Cette découverte est un soulagement pour la communauté cryptographique, car elle confirme que le problème LWE, composant critique des méthodes de protection en cryptographie post-quantique, demeure sûr.

L'article de Chen examinait également d'autres problèmes complexes sur réseaux, tels que le decisional shortest vector problem (GapSVP) et le shortest independent vector problem (SIVP), dans des facteurs d'approximation polynomiaux. Si le bug dans son algorithme n'affecte pas directement ces problèmes, il soulève des questions sur la robustesse des algorithmes quantiques contre la cryptographie sur réseaux.

Mais selon [la page de Nigel Smart ⧉][02], l'attaque quantique proposée contre LWE est défectueuse et ne compromet pas les schémas de cryptographie sur réseaux comme [Kyber ⧉][04], [Dilithium ⧉][05], [BGV ⧉][06] ou [TFHE ⧉][07].

## Implications pour le processus de standardisation NIST de cryptographie post-quantique

La recherche de Chen a indirectement soulevé des préoccupations et des doutes sur le [processus de standardisation NIST de cryptographie post-quantique (PQC) ⧉][03] et la sélection des algorithmes cryptographiques quantique-résistants.

Les schémas [CRYSTALS-KYBER](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html) et CRYSTALS-Dilithium, parmi les finalistes du processus de standardisation NIST PQC, sont des exemples de schémas cryptographiques sur réseaux qui ont été rigoureusement testés et évalués pour leur résistance quantique. Cependant, il est crucial de continuer à tester et affiner ces schémas pour garantir leur sécurité et leur viabilité à long terme.

Le NIST, la communauté cryptographique et les entreprises doivent rester vigilants et continuer à explorer des fondements mathématiques alternatifs pour la cryptographie post-quantique, afin de garantir qu'un ensemble robuste et diversifié d'options de sécurité quantique-résistante soit en place.

## L'avenir de la cryptographie post-quantique

La découverte du bug dans l'algorithme de Chen souligne le rôle critique de la revue par les pairs dans le processus scientifique. Elle met aussi en évidence le besoin de revue instantanée, de retours et de débat.

L'ère quantique a commencé, et le besoin de développer des méthodes cryptographiques quantique-résistantes exige des mesures coopératives à l'échelle mondiale pour garantir la sécurité de notre infrastructure numérique face aux capacités croissantes du calcul quantique et à la course à la suprématie quantique.

Le processus de standardisation NIST PQC est une étape significative dans cette direction, mais ce n'est qu'un commencement. Le bug dans l'algorithme de Chen est un rappel brutal des défis et incertitudes à venir, mais il sert aussi d'appel à l'action pour que la communauté cryptographique redouble ses efforts et repousse les frontières de ce qui est possible.

C'est un développement fascinant dans le domaine de la cryptographie post-quantique, et il sera intéressant de voir comment le processus de standardisation NIST PQC évolue en réponse à cette nouvelle information.

## Conclusion

Le bug découvert dans l'algorithme quantique de Yilei Chen pour résoudre le problème LWE témoigne de l'importance d'une revue par les pairs rigoureuse et de la collaboration dans le développement de la cryptographie quantique-résistante.

Si le bug offre un sursis temporaire à la sécurité des schémas cryptographiques sur réseaux, il rappelle aussi le besoin continu de recherche et de développement dans le domaine de la cryptographie post-quantique.

Alors que le NIST poursuit son processus de standardisation PQC, la communauté cryptographique doit rester proactive et adaptative, en embrassant les nouvelles idées et approches pour garantir la sécurité à long terme de notre monde numérique face aux capacités croissantes du calcul quantique.

## Références

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
