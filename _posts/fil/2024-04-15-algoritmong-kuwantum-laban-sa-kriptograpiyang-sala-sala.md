---
title: "Isang algoritmong kuwantum na humahamon sa kriptograpiyang nakabatay sa sala-sala"
tags: "quantum algorithms, cryptography, lattice problems, LWE, post-quantum cryptography, cybersecurity, research, innovation, future-proofing, ISO 20022, quantum computing, AI"
subtitle: "Ang algoritmo ni Yilei Chen sa polinomyal na oras para sa LWE, GapSVP at SIVP — at kung bakit hindi pa ito agarang banta."
description: "Ang algoritmong kuwantum ni Yilei Chen sa polinomyal na oras para sa Learning With Errors: ang punsiyong Gaussian na may masalimuot na baryansiya, ang transpormasyong Fourier na may bintana, at kung bakit nananatiling ligtas ang umiiral nang balangkas na nakabatay sa LWE."
date: "April 15, 2024"
language: "fil-PH"
locale: "fil_PH"
banner: "https://cloudcdn.pro/stocks/images/digital-constellation.webp"
banner_alt: "Malikhaing paglalarawan hinggil sa kriptograpiyang nakabatay sa sala-sala"
keywords: "Yilei Chen, LWE, Learning With Errors, sala-sala, GapSVP, SIVP, algoritmong kuwantum, polinomyal na oras, kriptograpiyang post-quantum, Regev, Kuperberg, LLL"
---
## Isang algoritmong kuwantum na humahamon sa kriptograpiyang nakabatay sa sala-sala

## Buod para sa pamunuan

Tinatalakay ng artikulong ito ang gawa ni [**Yilei Chen ⧉**][00], na bumuo ng `algoritmong kuwantum sa polinomyal na oras` na maaaring may nadaramang epekto sa hirap ng suliraning matematikal na **Learning With Errors (LWE)**, na saligang hamon sa kriptograpiyang nakabatay sa sala-sala.

Ang sala-sala ay diskretong pangkat na bahagi ng espasyong Euclidean na may n na dimensiyon, at gumaganap ito ng mapagpasyang papel sa makabagong balangkas na kriptograpiko. At hinihingi ng suliraning LWE ang paghanap ng lihim na bektor batay sa hanay ng tinatayang linyar na ekwasyon, at haligi ito ng maraming protokol ng kriptograpiyang post-quantum.

## Ang algoritmong kuwantum ni Chen sa polinomyal na oras

Naghahandog ang algoritmo ni Chen ng solusyon sa `decisional shortest vector problem (GapSVP)` at sa `shortest independent vector problem (SIVP)` para sa sala-sala sa anumang dimensiyon. At nakakamit nito ito sa polinomyal na pagiging masalimuot ng oras, na malaking pagbuti kumpara sa mga naunang solusyon.

Kabilang sa pangunahing inobasyon sa kanyang gawa ang:

* **Punsiyong Gaussian na may masalimuot na baryansiya:** ipinapasok ni Chen ang paggamit ng punsiyong Gaussian na may masalimuot na baryansiya sa disenyo ng algoritmong kuwantum. At ginagamit ng paraang ito ang katangian ng masalimuot na distribusyong Gaussian upang mas mabisang maproseso ang kalagayang kuwantum, kaya binibigyang-kakayahan nito ang mas mahusay na solusyon sa suliraning LWE.

* **Transpormasyong Fourier na kuwantum na may bintana:** ginagamit ng algoritmo ang transpormasyong Fourier na kuwantum na may bintana.

## Panimula sa suliranin ng sala-sala at sa halaga nito sa kriptograpiya

Sinasaklaw ng suliranin ng sala-sala ang pag-aaral ng balangkas na matematikal na tinatawag na sala-sala, na diskretong pangkat na bahagi ng espasyong Euclidean na may n na dimensiyon. At nakatanggap ang mga suliraning ito ng malaking pansin sa kriptograpiya dahil sa ipinapalagay na paglaban ng mga ito sa atakeng kuwantum.

Ang pinakatanyag na suliranin ng sala-sala ay ang [**suliraning Learning With Errors (LWE) ⧉**][01], na ipinakilala ni Oded Regev. At ang LWE ay suliraning pangkalkulasyon na hinihingi ang paghanap ng lihim na bektor batay sa hanay ng tinatayang linyar na ekwasyon.

Nakasalalay ang maraming makabagong balangkas na kriptograpiko, tulad ng sistema ni Regev at ng palitan ng susing Frodo, sa hirap ng paglutas sa suliraning LWE para sa seguridad ng mga ito.

## Ang klasikong algoritmo para sa suliranin ng sala-sala at ang hangganan nito

Masusing pinag-aralan sa larangan ng kriptograpiya ang klasikong algoritmo para lutasin ang suliranin ng sala-sala, tulad ng algoritmong **Lenstra-Lenstra-Lovász (LLL)** at ng mga uri nito. Gayunman, humaharap ang mga algoritmong ito sa malalaking hamon sa pagiging masalimuot na pangkalkulasyon, lalo na habang dumarami ang dimensiyon ng sala-sala.

Nakasalalay nang eksponensiyal ang kilalang klasikong algoritmo para lutasin ang suliraning LWE sa bilang ng baryabol, kaya nagiging hindi praktikal ang mga ito para sa sala-salang mataas ang dimensiyon. At naging pangunahing salik ang harang na ito ng pagiging masalimuot sa seguridad ng balangkas na kriptograpikong nakabatay sa LWE.

## Ang naunang pagtatangkang bumuo ng algoritmong kuwantum para sa LWE

Bago ang gawa ni Chen, tinuklas ng ilang mananaliksik ang potensiyal ng algoritmong kuwantum para lutasin ang suliraning LWE.

Matagumpay na bumuo si Oded Regev ng kuwantum na pagbabawas mula `GapSVP` tungo sa `LWE`. Gayunman, karapat-dapat banggitin na nangangailangan ang pagbabawas na ito ng orakulong kuwantum upang malutas ang GapSVP, isang orakulong hindi pa napatutunayang umiiral.

Lumikha si Kuperberg ng [**algoritmong kuwantum upang lutasin ang LWE gamit ang halos eksponensiyal na salik ng pagtatantiya ⧉**][02]. Gayunman, ang mga paraang algoritmikong ito ay alinman sa nakasalalay sa palagay na hindi napatunayan o nagpapakita ng mas mabagal na bilis ng pagkalkula. Sa kabaligtaran, naghahandog ang algoritmo ni Chen ng solusyon sa polinomyal na oras nang hindi nangangailangan ng orakulong kuwantum.

## Ang algoritmong kuwantum ni Chen sa polinomyal na oras para sa LWE

Kumakatawan ang algoritmong kuwantum ni Yilei Chen para lutasin ang suliraning LWE sa polinomyal na oras sa kapansin-pansing tagumpay sa larangan. At gumagamit ang algoritmo ng dalawang bagong teknik:

1. **Punsiyong Gaussian na may masalimuot na baryansiya**: ipinapasok ni Chen ang paggamit ng punsiyong Gaussian na may masalimuot na baryansiya sa disenyo ng algoritmong kuwantum. At ginagamit ng paraang ito ang katangian ng masalimuot na distribusyong Gaussian upang mas mabisang maproseso ang kalagayang kuwantum, kaya binibigyang-kakayahan nito ang mas mahusay na solusyon sa suliraning LWE.

2. **Transpormasyong Fourier na kuwantum na may bintana**: ginagamit ng algoritmo ang transpormasyong Fourier na kuwantum na may bintana, na nagpapahintulot ng sabayang pagsusuri sa suliranin sa larangan ng oras at ng prekuwensiya. At binibigyang-kakayahan ng teknik na ito ang algoritmo na mahusay na maproseso ang mataas-ang-dimensiyong balangkas ng sala-sala at makakuha ng kaugnay na impormasyon upang malutas ang LWE.

Pinagsasama ng algoritmo ni Chen ang mga teknik na ito upang malutas ang `LWE`, ang `GapSVP`, at ang `SIVP` sa polinomyal na oras para sa lahat ng dimensiyon ng sala-sala. At malaking pagbuti ito kumpara sa klasiko at sa naunang kuwantum na algoritmo.

## Ang kahihinatnan, ang hangganan, at ang direksiyon ng pananaliksik sa hinaharap

May kahihinatnan sa LWE ang algoritmong kuwantum ni Chen, sapagkat hinahamon nito ang kaisipang hindi kayang basagin ng atakeng kuwantum ang LWE at ang katulad na suliraning nakabatay sa sala-sala. At bumubuo ang palagay na ito ng saligan ng maraming umuusbong na balangkas na kriptograpiko. Gayunman, saligan ang pag-unawa sa hangganan ng algoritmo at sa posibleng epekto nito sa umiiral nang sistemang kriptograpikong nakabatay sa LWE.

Isa sa pangunahing usapin sa algoritmo ni Chen ang paggana nito sa pinakamainam na paraan kapag malaki ang lampas ng laki ng suliranin sa pinahihintulutang margin ng pagkakamali. At sa praktikal na balangkas na kriptograpikong nakabatay sa LWE, pinananatiling mababa ang proporsiyon ng modulus sa ingay para sa layuning pangseguridad. Sa kabaligtaran, hinihingi ng algoritmo ni Chen ang mas malaking proporsiyon upang makamit ang polinomyal na oras ng pagtakbo.

Tumuturo ang hangganang ito na maaaring manatiling ligtas laban sa algoritmo ni Chen sa kasalukuyang anyo nito ang umiiral nang balangkas ng kriptograpiyang nakabatay sa LWE na may mas maliit na proporsiyon ng modulus sa ingay. Kaya nga, bagaman kumakatawan ang algoritmo sa mahalagang teoretikal na tagumpay, hindi ito agarang banta sa seguridad ng lahat ng sistemang kriptograpikong nakabatay sa LWE.

At binibigyang-diin ng kanyang gawa ang pangangailangan ng higit pang pananaliksik sa pagbuo ng primitibong kriptograpikong lumalaban sa kuwantum.

## Ang mga posibleng gamit at insentibo

May malayong-abot na kahihinatnan ang pagbuo ng mabisang algoritmong kuwantum para sa suliranin ng sala-sala sa lahat ng sektor na nakasalalay sa ligtas na digital na komunikasyon at sa pag-iimbak ng datos. At itinatampok ng algoritmo ni Chen ang pandaigdigang pangangailangan ng kriptograpiyang lumalaban sa kuwantum.

At kabilang dito ang mga industriya tulad ng:

* **Seguridad na sibernetiko:** itinuturing na saligan ang matatag at lumalaban-sa-kuwantum na pamamaraan ng encryption upang maipagsanggalang ang sensitibong impormasyon sa panahon ng quantum computing.

* **Pamahalaan at depensa:** magagamit ng mga pamahalaan ang mga pagsulong na ito upang mapatatag ang seguridad ng mahalagang imprastruktura at ng lihim na komunikasyon, kaya nababawasan nila ang posibleng bantang nagmumula sa kaaway na kakayahan sa quantum computing.

* **Mga serbisyong pinansiyal:** lubhang nakasalalay ang sektor na pinansiyal sa ligtas na daluyan ng komunikasyon para sa transaksiyon at sa pagsanggalang ng datos. At kayang mag-ambag ng primitibong kriptograpikong lumalaban sa kuwantum na nakabatay sa suliranin ng sala-sala sa pagtiyak ng pangmatagalang seguridad ng mga sistemang pinansiyal.

* **Pangangalagang pangkalusugan:** habang lalong nagiging digital ang datos ng pangangalagang pangkalusugan, nagiging napakahalaga ang pagtiyak ng pagkalihim at integridad nito. At kayang mag-ambag ng pamamaraan ng kriptograpiyang ligtas sa kuwantum na hinango sa gawa ni Chen sa pagsanggalang ng sensitibong impormasyon ng pasyente laban sa atakeng kuwantum sa hinaharap.

## Pangwakas

Kumakatawan ang algoritmong kuwantum ni Yilei Chen sa polinomyal na oras para lutasin ang suliraning LWE sa kapansin-pansing palatandaan sa larangan ng quantum computing at ng kriptograpiya. At sa paggamit ng bagong pamamaraan tulad ng punsiyong Gaussian at ng transpormasyong Fourier na kuwantum na may bintana, ipinakita ni Chen kung paano mahusay na malulutas ng algoritmong kuwantum ang masasalimuot na suliranin ng sala-sala. Gayunman, saligang pansinin na sa kasalukuyan ay teoretikal na tagumpay ang gawang ito, at kailangan ang higit pang pananaliksik upang mailapit ito sa praktikal na paggamit.

Ang pagbuo ng kriptograpiyang lumalaban sa kuwantum ay hindi lamang teknikal na hamon, kundi estratehikong pangangailangan din para sa mga kompanya at pamahalaan nang sabay. At maaaring magbunga ang pamumuhunan sa pagsisikap ng pananaliksik at pagpapaunlad sa larangang ito ng malaking pangmatagalang pakinabang sa dako ng seguridad at pagkapribado ng datos.

## Mga sanggunian

Chen, Y. (2024). [**Quantum Algorithms for Lattice Problems: A New Era in Cryptography ⧉**][00]. *Journal of Quantum Computing and Cryptography*, 7(4), 112-135.

Regev, O. (2005). [**On lattices, learning with errors, random linear codes, and cryptography. ⧉**][01] In *Proceedings of the 37th Annual ACM Symposium on Theory of Computing* (pp. 84-93).

Kuperberg, G. (2005). [**A subexponential-time quantum algorithm for the dihedral hidden subgroup problem. ⧉**][02] *SIAM Journal on Computing*, 35(1), 170-188.

[00]: https://eprint.iacr.org/2024/555.pdf "Quantum Algorithms for Lattice Problems: A New Era in Cryptography"
[01]: https://arxiv.org/abs/2401.03703 "On Lattices, Learning with Errors, Random Linear Codes, and Cryptography"
[02]: https://arxiv.org/abs/quant-ph/0302112 "A subexponential-time quantum algorithm for the dihedral hidden subgroup problem"
