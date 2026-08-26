---
title: "KyberLib: CRYSTALS-Kyber sa Rust para sa panahong post-quantum"
tags: "KyberLib, Rust, CRYSTALS-Kyber, post-quantum cryptography, lattice-based cryptography, key encapsulation mechanism, NIST, libsignal, cryptography, ISO 20022, quantum computing, AI"
subtitle: "Isang aklatang Rust na nagpapatupad ng CRYSTALS-Kyber, may suporta sa no_std at WebAssembly para sa mga nakapaloob na sistema at aplikasyong web."
description: "Ang KyberLib: isang aklatang Rust na nagpapatupad ng CRYSTALS-Kyber — ang apat na algoritmong hinirang ng NIST, ang kriptograpiyang nakabatay sa sala-sala, at ang suporta sa no_std at WebAssembly para sa mga sistemang limitado ang mapagkukunan."
date: "Nov 28, 2023"
language: "fil-PH"
locale: "fil_PH"
banner: "https://cloudcdn.pro/clients/kyberlib/v1/logos/kyberlib.svg"
banner_alt: "Pagpapatibay ng ligtas na komunikasyon sa panahong quantum gamit ang KyberLib"
keywords: "KyberLib, CRYSTALS-Kyber, Rust, kriptograpiyang post-quantum, PQC, sala-sala, LBC, NIST, no_std, WebAssembly, WASM, Dilithium, FALCON, SPHINCS+"
---
## KyberLib: CRYSTALS-Kyber sa wikang Rust para sa panahong post-quantum

[![Pagpapatibay ng ligtas na komunikasyon sa panahong quantum gamit ang KyberLib](https://cloudcdn.pro/clients/kyberlib/v1/logos/kyberlib.svg).class=\"img-fluid clearfix\"][07]

Ang `KyberLib` ay isang aklatan sa wikang Rust na nagsasanggalang sa inyong datos laban sa posibleng banta ng quantum computing. Nakabuo sa **algoritmong [CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html)**, naghahandog ang `KyberLib` ng pambihirang seguridad, kahusayan, at sari-saring gamit, at madali itong naisasanib sa maraming plataporma, kabilang na ang mga kapaligirang `no-std`.

![divider][divider].class=\"m-10 w-100\"

## Pagtiyak ng seguridad ng inyong datos sa panahong quantum

Nagdala ang pagdating ng quantum computing ng saligang banta sa tradisyunal na hakbang na kriptograpiko. Upang tugunan ang hamong ito, mabilis na umuunlad ang larangan ng kriptograpiyang ligtas sa quantum (QSC).

Sa unahan ng mapagbagong kilusang ito, pinamumunuan ng National Institute of Standards and Technology (NIST) ang proseso ng pagsasapamantayan ng mga algoritmong QSC.

Noong 2023, pumili ang NIST ng apat na mapanlikhang algoritmo bilang maikling talaan:

- [**[CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html)** ⧉][01] (mekanismo ng pagbabalot ng susi)
- [**CRYSTALS-Dilithium** ⧉][02] (mga digital na lagda)
- [**FALCON** ⧉][03] (magaang digital na lagda)
- [**SPHINCS+** ⧉][04] (digital na lagdang nakabatay sa hash)

Nakasalalay ang mga mapanimulang algoritmong ito sa iba't ibang prinsipyong matematikal, kabilang ang kriptograpiyang nakabatay sa sala-sala, ang kriptograpiyang nakabatay sa hash, at ang kriptograpiyang nakabatay sa kodigo, na naglalayong maghandog ng matatag na depensa laban sa mga atakeng quantum.

## Pagtuklas sa kriptograpiyang nakabatay sa sala-sala

Namumukod ang kriptograpiyang nakabatay sa sala-sala (LBC — Lattice-Based Cryptography) bilang nangungunang kandidato sa QSC, at naghahandog ito ng maaasahang solusyon para sa kriptograpiyang post-quantum (PQC). Sari-sari ang gamit ng LBC, mula sa mekanismo ng pagbabalot ng susi (KEMs) hanggang sa mga digital na lagda at sa mga balangkas ng encryption sa pamamagitan ng pampublikong susi, na nakaugat sa matematikal na sala-sala.

Ang sala-sala ay saligang konsepto sa matematika na nakahanap ng gamit sa iba't ibang larangan, kabilang na ang kriptograpiya. Sa pinakasimpleng pananalita, ang sala-sala ay regular na pagkakaayos ng mga punto sa espasyo, na bumubuo ng balangkas na parang lambat. Magkakaugnay ang mga puntong ito sa pamamagitan ng linya, kaya bumubuo sila ng lambat ng magkakadugtong na selda. At ang tiyak na pagkakaayos ng mga punto at ang agwat sa pagitan ng mga ito ang nagtatakda ng natatanging katangian ng sala-sala.

### Tatlong-dimensiyong paglalarawan ng sala-sala gamit ang mga saligang bektor

Ipinapakita ng guhit na ito ang balangkas ng tatlong-dimensiyong sala-sala na nilikha ng tatlong saligang bektor:

- `b1 = [1, 0, 0]` sa pula,
- `b2 = [0, 1, 0]` sa berde, at
- `b3 = [0, 0, 1]` sa asul.

Nabubuo ang bawat punto sa sala-sala sa pamamagitan ng pagsasama ng mga saligang bektor na ito sa iba't ibang buong-bilang na proporsiyon, kaya nalilikha ang huwarang parang lambat na umaabot sa tatlong dimensiyon ng espasyo. Ipinamamalas ng larawang ito ang diwa ng tatlong-dimensiyong sala-sala, isang konseptong malawakang ginagamit sa pisika at matematika upang katawanin ang regular at paulit-ulit na pagkakaayos ng mga punto sa espasyo.

![Tatlong-dimensiyong paglalarawan ng sala-sala gamit ang mga saligang bektor][06].class=\"img-fluid mx-auto d-block\"

Sa kriptograpiya, pangunahing ginagamit ang sala-sala para sa ilang algoritmong kriptograpiko. Sinasamantala ng kriptograpiyang nakabatay sa sala-sala (LBC) ang matematikal na katangian ng sala-sala upang lumikha ng ligtas na balangkas na kriptograpikong lumalaban sa atake ng mga quantum na kompyuter. Kumakatawan ang mga quantum na kompyuter sa saligang banta sa tradisyunal na kriptograpiya, sapagkat kaya nilang basagin nang mahusay ang mga algoritmong umaasa sa pagpapaktor ng malalaking bilang o sa paglutas ng suliraning diskretong logaritmo.

Ipinamamalas ng CRYSTALS-Kyber ang lakas ng LBC, at naghahandog ito ng matatag na paglaban sa atakeng quantum na sinasamahan ng pambihirang kahusayan at angkop na laki ng susi. At ginagawa itong maaasahang pagpipilian para sa seguridad ng datos sa panahong quantum ng kakayahan nitong gumana sa maraming plataporma at ng pagkakatugma nito sa encryption.

Ang kasalukuyang espesipikasyon ng CRYSTALS-Kyber ay ang mga sumusunod:

- **Kyber512**: naghahandog ng antas ng seguridad na katumbas ng encryption na AES sa 128 bit, kaya pinagsasanggalang nito ang sensitibong datos nang naaayon sa pamantayan ng industriya.
- **Kyber768**: naghahandog ng antas ng seguridad na katumbas ng encryption na AES sa 256 bit, kaya tinitiyak nito ang pagkalihim ng napakasensitibong impormasyon.
- **Kyber1024**: naghahandog ng antas ng seguridad na lampas sa encryption na AES sa 256 bit, kaya naghahatid ito ng matatag na proteksiyon laban sa atakeng quantum at pinananatili ang integridad ng datos sa mahabang panahon sa hinaharap.

### Paghahambing ng antas ng seguridad sa pagitan ng klasiko at ng lumalaban-sa-quantum na algoritmo

Ipinapaliwanag ng grapikong ito ang kaugnay na antas ng seguridad ng mga klasikong algoritmong kriptograpiko tulad ng RSA-2048 at ng algoritmo ng digital na lagda sa elliptic curve (ECDSA), kumpara sa espesipikasyon ng mga baryanteng lumalaban sa quantum ng CRYSTALS-Kyber (Kyber512, Kyber768, at Kyber1024).

Bagaman naghahandog ang grapiko ng biswal na paghahambing, mahalagang banggitin na hindi tuwirang maihahambing ang mga antas ng seguridad, sapagkat nakabatay ang mga ito sa magkakaibang prinsipyong matematikal.

Gayunman, naghahandog ang grapiko ng kapaki-pakinabang na sanggunian sa pag-unawa sa antas ng seguridad ng mga algoritmong lumalaban sa quantum.

![Kriptograpiyang nakabatay sa sala-sala][05].class=\"img-fluid mx-auto d-block\"

![divider][divider].class=\"m-10 w-100\"

## KyberLib: isang aklatang Rust para sa kriptograpiyang lumalaban sa quantum computing

Ginagamit ng KyberLib ang lakas ng CRYSTALS-Kyber upang maghandog ng pinatatag na kaligtasan ng memorya at matatag na seguridad ng sistema. Sinusuportahan nito ang iba't ibang espesipikasyon ng CRYSTALS-Kyber (Kyber512, Kyber768, at Kyber1024), kaya naghahandog ito ng hanay ng antas ng seguridad na angkop sa inyong tiyak na pangangailangan. Ginagawa itong angkop na angkop na pagpipilian para sa mga nakapaloob na sistema ng pagkakatugma nito sa `no_std`, samantalang pinadadali naman ng pagkakatugma nito sa WebAssembly (WASM) ang maayos na pagsasanib sa mga aplikasyong web.

![divider][divider].class=\"m-10 w-100\"

## Pagsanggalang sa mga aplikasyong web gamit ang kriptograpiyang lumalaban sa quantum

Ang KyberLib, na idinisenyo nang may pinakamaliit na bakas sa memorya, ay angkop na angkop sa mga nakapaloob at limitado-sa-mapagkukunang sistema nang hindi isinasakripisyo ang seguridad. Sinasamantala ng pagpapatupad nito sa wikang Rust ang mga katangian ng kaligtasan ng wika, kaya pinatatatag nito ang seguridad na inihahandog ng algoritmong CRYSTALS-Kyber.

Bukod dito, pinatatatag ng pagkakatugma ng KyberLib sa WebAssembly ang pakinabang nito sa mga aplikasyong web, kaya tinitiyak nitong mananatili itong mahalagang kasangkapan sa dinamikong mundo ng kriptograpiya.

[Magsimula sa KyberLib ngayon! ⧉][00] Madaling i-install, at libre para sa personal at komersiyal na paggamit, ang KyberLib ang inyong pinakamainam na solusyon para sa kriptograpiyang lumalaban sa quantum computing.

[00]: https://kyberlib.com/getting-started/index.html "Getting Started"
[01]: https://pq-crystals.org/kyber/ "Kyber: A CCA-secure module-lattice-based KEM"
[02]: https://pq-crystals.org/dilithium/ "Dilithium: A CCA-secure lattice-based signature scheme"
[03]: https://falcon-sign.info/ "FALCON: A post-quantum signature scheme"
[04]: https://sphincs.org/ "SPHINCS+: A stateless hash-based signature scheme"
[05]: https://cloudcdn.pro/stocks/diagrams/kyber-vs-classical.svg "Comparison of Security Levels between Classical and Quantum-Resistant Algorithms"
[06]: https://cloudcdn.pro/stocks/diagrams/3D-lattice-graph.svg "3D Lattice Representation with Basis Vectors"
[07]: https://kyberlib.com/ "Privacy and Security in a Quantum World"

[divider]: https://cloudcdn.pro/clients/common/images/elements/divider.svg "Divider"
