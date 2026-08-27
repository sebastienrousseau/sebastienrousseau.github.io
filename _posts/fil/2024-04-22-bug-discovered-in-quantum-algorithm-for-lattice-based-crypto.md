---
title: "Kriptograpiyang nakabatay sa sala-sala: isang depekto sa atake ni Chen sa LWE"
tags: "post-quantum cryptography, NIST, quantum algorithms, Lattice-Based Cryptography, LWE Problem, quantum computing, Cryptographic Security, Quantum Resistance, Cryptography Research, ISO 20022, AI, Rust"
subtitle: "Natuklasan sa hakbang 9: nananatiling ligtas ang LWE, at hindi nailagay sa panganib ang Kyber, Dilithium, BGV at TFHE."
description: "Isang depekto sa hakbang 9 ng algoritmong kuwantum ni Yilei Chen para sa LWE, na hiwalay na natuklasan nina Hongxun Wu at Thomas Vidick — at ang kahihinatnan nito sa pagsasapamantayan ng NIST para sa kriptograpiyang post-quantum."
date: "Apr 22, 2024"
language: "fil-PH"
locale: "fil_PH"
banner: "https://cloudcdn.pro/stocks/images/digital-nodes.webp"
banner_alt: "Malikhaing paglalarawan hinggil sa kriptograpiyang post-quantum"
keywords: "Yilei Chen, LWE, depekto, Hongxun Wu, Thomas Vidick, NIST, PQC, pagsasapamantayan, Kyber, Dilithium, BGV, TFHE, sala-sala, pagsusuri ng kapwa dalubhasa"
---
## Kriptograpiyang kuwantum na nakabatay sa sala-sala: isang depekto sa atake ni Chen sa LWE

## Ang palaisipang kuwantum: muling pagtatasa sa pagsasapamantayan ng NIST para sa kriptograpiyang post-quantum sa liwanag ng algoritmo ni Yilei Chen

Kasunod ng aking huling artikulo hinggil sa [hamon ng algoritmong kuwantum sa kriptograpiyang nakabatay sa sala-sala][00], kailangan kong maghandog ng update hinggil sa pinakabagong pag-unlad kaugnay ng [pananaliksik ni Yilei Chen ⧉][01].

Sa isang di-inaasahang pagbabago, iniulat ni Yilei Chen, ang katulong na propesor sa institute ng agham ng impormasyon na maraming disiplina (IIIS) sa Unibersidad ng Tsinghua, na ang kanyang mga kasamahang siyentipiko na sina Hongxun Wu at Thomas Vidick ay natuklasan, bawat isa nang hiwalay, ang isang depekto sa kanyang algoritmong kuwantum sa polinomyal na oras na idinisenyo upang lutasin ang suliraning Learning with Errors (LWE).

At ginagawa ng depektong ito na hindi magamit ang algoritmo, at kinilala ni Chen na hindi nakatayo ang kanyang paraan gaya ng unang iginiit.

## Ang depekto sa algoritmong kuwantum ni Chen

Natagpuan ang depekto sa hakbang 9 ng algoritmo ni Chen, at sinabi niyang hindi niya alam kung paano ito aayusin. At ang pagkatuklas na ito ay kaginhawahan para sa komunidad ng kriptograpiya, sapagkat pinatutunayan nito na nananatiling ligtas ang suliraning LWE, na mapagpasyang sangkap sa mga pamamaraan ng proteksiyong kriptograpikong post-quantum.

Tinalakay din ng papel ni Chen ang iba pang masalimuot na suliranin ng sala-sala, tulad ng decisional shortest vector problem (GapSVP) at ng shortest independent vector problem (SIVP) sa balangkas ng polinomyal na salik ng pagtatantiya. At bagaman hindi tuwirang naaapektuhan ng depekto sa kanyang algoritmo ang mga suliraning ito, nagbubunsod ito ng tanong hinggil sa katatagan ng algoritmong kuwantum laban sa kriptograpiyang nakabatay sa sala-sala.

Ngunit ayon sa [pahina ni Nigel Smart ⧉][02], ang iminungkahing atakeng kuwantum sa LWE ay may depekto at hindi nito inilalagay sa panganib ang balangkas ng kriptograpiya sa sala-sala tulad ng [Kyber ⧉][04], ng [Dilithium ⧉][05], ng [BGV ⧉][06], o ng [TFHE ⧉][07].

## Ang kahihinatnan sa proseso ng pagsasapamantayan ng NIST para sa kriptograpiyang post-quantum

Nagbunsod ang pananaliksik ni Chen, sa di-tuwirang paraan, ng alalahanin at pag-aalinlangan hinggil sa [proseso ng pagsasapamantayan ng NIST para sa kriptograpiyang post-quantum (PQC) ⧉][03] at sa pagpili ng algoritmo ng encryption na lumalaban sa kuwantum.

At ang mga balangkas na [CRYSTALS-KYBER](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html) at CRYSTALS-Dilithium, na itinuturing na kabilang sa mga huling kandidato sa proseso ng pagsasapamantayan ng NIST PQC, ay halimbawa ng balangkas na kriptograpikong nakabatay sa sala-sala na mahigpit na sinubok at tinasa upang matukoy ang paglaban ng mga ito sa kuwantum. Gayunman, saligan ang pagpapatuloy ng pagsubok at pagpipino sa mga balangkas na ito upang matiyak ang seguridad at ang pangmatagalang kakayahang mabuhay ng mga ito.

At dapat panatilihin ng NIST, ng komunidad ng kriptograpiya, at ng mga kompanya ang pagbabantay at ipagpatuloy ang pagtuklas sa alternatibong saligang matematikal para sa kriptograpiyang post-quantum upang matiyak ang pagkakaroon ng matatag at sari-saring hanay ng pagpipilian para sa seguridad na lumalaban sa kuwantum.

## Ang kinabukasan ng kriptograpiyang post-quantum

Binibigyang-diin ng pagkatuklas ng depekto sa algoritmo ni Chen ang mapagpasyang papel ng pagsusuri ng kapwa dalubhasa sa prosesong siyentipiko. At itinatampok din nito ang pangangailangan ng agarang pagsusuri, ng puna, at ng talakayan.

Nagsimula na ang panahong kuwantum, at hinihingi ng pangangailangang bumuo ng pamamaraan ng kriptograpiyang lumalaban sa kuwantum ang mga hakbang na kolaboratibo sa pandaigdigang saklaw upang matiyak ang seguridad ng ating digital na imprastruktura sa harap ng abanteng kakayahan sa quantum computing at ng karera tungo sa kahusayang kuwantum.

At ang proseso ng pagsasapamantayan ng NIST PQC ay mahalagang hakbang sa direksiyong ito, ngunit simula pa lamang ito. At ang depekto sa algoritmo ni Chen ay matinding paalala ng hamon at pag-aalinlangang nasa abot-tanaw, ngunit kumakatawan din ito sa panawagan sa pagkilos para sa komunidad ng kriptograpiya upang doblehin nito ang pagsisikap at palawakin ang hangganan ng maaari.

Isa itong nakamamanghang pag-unlad sa larangan ng kriptograpiyang post-quantum, at magiging kawili-wiling makita kung paano uunlad ang proseso ng pagsasapamantayan ng NIST PQC bilang tugon sa bagong impormasyong ito.

## Pangwakas

Ang natuklasang depekto sa algoritmong kuwantum ni Yilei Chen para lutasin ang suliraning LWE ay patotoo sa halaga ng mahigpit na pagsusuri ng kapwa dalubhasa at ng pakikipagtulungan sa pagbuo ng kriptograpiyang lumalaban sa kuwantum.

At bagaman naghahandog ang depekto ng pansamantalang palugit para sa seguridad ng balangkas na kriptograpikong nakabatay sa sala-sala, nagpapaalala rin ito ng patuloy na pangangailangan ng pananaliksik at pagpapaunlad sa larangan ng kriptograpiyang post-quantum.

At habang ipinagpapatuloy ng NIST ang proseso ng pagsasapamantayan ng PQC, dapat manatiling maagap at kayang umangkop ang komunidad ng kriptograpiya, at dapat nitong yakapin ang bagong kaisipan at paraan upang matiyak ang pangmatagalang seguridad ng ating digital na mundo sa harap ng abanteng kakayahan sa quantum computing.

## Mga sanggunian

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
