---
title: "Pagsanggalang sa datos sa panahong quantum: ang aklatang hash (HSH)"
tags: "post-quantum cryptography, hash library, HSH, password hashing, key derivation, Argon2i, Bcrypt, Scrypt, quantum computing, ISO 20022, AI, Rust, open source"
subtitle: "Kriptograpiyang lumalaban sa quantum sa Rust: Argon2i, BScrypt at Scrypt sa isang magaan na aklatan para sa pag-hash at pagpapatunay ng password."
description: "Paano binabanta ng quantum computing ang tradisyunal na encryption, at paano naghahandog ang aklatang hash (HSH) na nakabatay sa Rust ng mga punsiyong PBKDF na lumalaban sa quantum — Argon2i, BScrypt, Scrypt — para sa pag-hash at pagpapatunay ng password."
date: "Oct 16, 2023"
language: "fil-PH"
locale: "fil_PH"
banner: "https://cloudcdn.pro/stocks/images/galina-nelyubova-7ej8VWfwFsg.webp"
banner_alt: "Malikhaing paglalarawan hinggil sa paksa ng quantum computing"
keywords: "HSH, aklatang hash, Rust, kriptograpiyang post-quantum, PQC, quantum computing, Argon2i, BScrypt, Scrypt, PBKDF, QKD, NIST, seguridad ng password"
---
## Pagsanggalang sa datos sa panahong quantum: ang aklatang hash (HSH)

![Malikhaing paglalarawan hinggil sa paksa ng quantum computing](https://cloudcdn.pro/stocks/images/galina-nelyubova-7ej8VWfwFsg.webp).class=\"img-fluid clearfix\"

Sa artikulong ito ay tatalakayin ko ang mga gamit ng kriptograpiyang lumalaban sa quantum computing, na nakatuon partikular sa aklatang hash sa wikang Rust (HSH) na aking binuo. Ang aklatang ito ay ganap na optimisado para sa mga punsiyong kriptograpiko ng pag-hash at pagpapatunay.

## Malalim na pagtingin

### Ang umuusbong na banta ng quantum computing

Habang umuunlad ang tanawing digital, kailangang yakapin ng mga institusyong nagbibigay ng serbisyong pinansiyal ang mga bagong teknolohiya upang manatiling mapagkumpitensiya. Ang kabiguang gawin ito ay maaaring magdulot ng pagkakaiwan, sapagkat umaabot ang pagbabagong digital sa bawat sektor.

Naghahatid ang quantum computing ng radikal na pagbabagong nangangako ng pagpapabilis sa pagsulong sa iba't ibang sektor, kabilang na ang banking at ang mga serbisyong pinansiyal. Gayunman, kasama nito ang malalaking panganib sa seguridad na digital, dahil sa kakayahan nitong basagin ang pinakamasalimuot na kodigo.

Ginagawang lipas ng quantum computing ang ilang tradisyunal na teknik sa pag-encrypt, sapagkat kaya nitong lutasin ang mga suliraning matematikal na hindi kayang lutasin ng karaniwang kompyuter.

Sa kasalukuyang kalagayan, kayang makipag-usap nang ligtas nina Alice at Bob gamit ang mga susing kriptograpiko, kaya napipigilan si Eve na basahin ang mga mensahe. Ngunit hindi ganap na masisiguro ang lubusang seguridad ng pamamahagi at pag-iimbak ng susi. Bunga nito, kumakatawan ang mga quantum na kompyuter sa saligang banta sa kriptograpiya at sa seguridad na digital.

#### Ligtas ngunit marupok: paglampas sa mga hamong kriptograpiko sa panahong quantum

![Diyagram ng pagkakasunod-sunod][01].class=\"img-fluid clearfix\"

##### Paliwanag

* *Alice tungo kay Eve — nagpapadala si Alice ng naka-encrypt na mensahe*
* *Sinasalo ni Eve — sinasalo ni Eve ang mensahe ni Alice*
* *Sinusubukang basagin ni Eve — sinusubukan ni Eve ngunit nabibigo siyang basagin ang encryption*
* *Eve tungo kay Bob — nagpapadala si Eve ng naka-encrypt na mensahe kay Bob*
* *Bob tungo kay Eve — nagpapadala si Bob ng naka-encrypt na tugon kay Eve*
* *Sinasalo ni Eve — sinasalo ni Eve ang tugon ni Bob*
* *Sinusubukang basagin ni Eve — muling nabibigo si Eve na basagin ang encryption*
* *Eve tungo kay Alice — nagpapadala si Eve ng naka-encrypt na mensahe kay Alice*

##### Pagpapaliwanag

###### Ang kasalukuyang encryption

Ang kasalukuyang mga algoritmo ng encryption na ginagamit nina Alice at Bob ay mabisa sa pagpigil kay Eve na basagin ang encryption ng kanilang mensahe. Gayunman, kumakatawan ang quantum computing sa posibleng banta sa seguridad ng mga algoritmong ito.

###### Ang mga posibleng panganib na quantum

Ang mga quantum na kompyuter ay higit na mabilis kaysa sa karaniwang kompyuter sa pagsasagawa ng ilang uri ng kalkulasyon, kabilang na ang mga ginagamit upang basagin ang ilang algoritmo ng encryption. Kung magkaroon si Eve ng quantum na kompyuter, maaaring mabasag niya ang encryption at mabasa ang mga mensahe nina Alice at Bob.

###### Ang panganib sa pamamahagi at pag-iimbak ng susi

Kahit gumamit sina Alice at Bob ng matibay na encryption, maaaring mapasok ang kanilang mensahe kung mapasok ang mga susing ginamit sa pag-encrypt at pagbasag nito. Maaaring mapasok ang mga susi sa iba't ibang paraan tulad ng pagnanakaw, ng pag-hack, at ng mga atake sa panlipunang inhinyeriya.

###### Ang pangangailangan ng kriptograpiyang post-quantum

Ang kriptograpiyang post-quantum ay bagong larangan ng kriptograpiyang idinisenyo upang lumaban sa mga atakeng quantum. Nasa yugto pa rin ng pagbuo ang mga algoritmo ng kriptograpiyang post-quantum, ngunit may tunay na potensiyal ang mga ito upang ipagsanggalang ang datos laban sa mga atakeng quantum.

### Pagpapakilala sa kriptograpiyang lumalaban sa quantum computing

Ang kriptograpiyang lumalaban sa quantum computing, na kilala rin bilang kriptograpiyang post-quantum (PQC) o kriptograpiyang ligtas sa quantum, ay tumutukoy sa mga algoritmong kriptograpiko na pinaniniwalaang ligtas laban sa atake ng mga quantum na kompyuter.

Kailangang gawin ng mga institusyon ang mga nararapat na pag-iingat upang ipagsanggalang ang kanilang datos laban sa panganib ng quantum computing. Maaaring maghandog sa mga kompanya ng serbisyong pinansiyal ng karagdagang layer ng seguridad ang pagpapatupad ng kriptograpiyang lumalaban sa quantum at ng mga estratehiya sa quantum entanglement.

* **Ang kriptograpiyang lumalaban sa quantum computing** ay bagong uri ng kriptograpiyang kayang labanan ang atake ng mga quantum na kompyuter. Kayang pabilisin ng mga algoritmo nito ang pagproseso ng datos at mapataas ang katumpakan, kaya nagiging mas mahusay itong pagpipilian.

* **Ang quantum entanglement** ay maaaring gamitin upang lumikha ng mga sistema ng [quantum na pamamahagi ng susi](/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html) ([QKD](/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html)), na kayang lumikha at mamahagi ng ligtas na susing kriptograpiko sa malalayong distansiya. Ang mga sistemang QKD ay hindi tinatablan ng atake mula sa quantum na kompyuter, kaya angkop na angkop ang mga ito sa pagsanggalang sa sensitibong datos na pinansiyal.

## Ang ideya

### Ang aklatang hash (HSH): pagpapanguna sa interoperabilidad sa kriptograpiyang lumalaban sa quantum

Naghahandog ang aklatang hash (HSH) ng magaan, mabisa, at madaling gamiting solusyon sa pagsanggalang sa datos gamit ang kriptograpiyang lumalaban sa quantum computing. Binibigyang-kakayahan nito ang mga developer na gumamit ng mga algoritmong lumalaban sa quantum sa kanilang aplikasyon nang hindi kailangan ang detalyadong pag-unawa sa saligang algoritmong kriptograpiko.

Ginawa ang aklatan sa wikang pamprograma na Rust, na kilala sa bilis at kahusayan nito, at angkop na angkop sa kriptograpiya at sa pangmatagalang pagiging maaasahan.

## Ang epekto

### Ang mga pakinabang ng aklatang hash na lumalaban sa quantum computing

Naghahandog ang [aklatang hash (HSH) ⧉][00] ng kayamanan ng makabagong primitibong kriptograpiko, at bumubuo ito ng matatag na harang laban sa mga suliranin ng panahong quantum. Nasa pagsanggalang sa sensitibong datos ang halaga nito, sa panahong kumakatawan ang quantum computing sa saligang panganib sa seguridad na digital.

Naghahandog ang aklatan sa mga organisasyon at institusyong pinansiyal ng pinakamataas na antas ng proteksiyong makukuha sa internet, sa pamamagitan ng piling hanay ng algoritmo, kabilang ang Argon2i, BScrypt, at Scrypt. Ang mga ito ay ligtas na punsiyon ng paghango ng susi na nakabatay sa password (PBKDFs). Ginagamit ang mga punsiyong PBKDF upang gawing susing kriptograpiko ang mga password. Idinisenyo ang mga ito upang maging mabagal at masinsin sa memorya, kaya nagiging mahirap basagin ang mga ito sa pamamagitan ng brute-force na atake.

Bukod dito, tinitiyak ng aklatan na ang mga resulta ay hindi lamang ligtas at mabisa, kundi angkop na angkop din sa mga aplikasyon sa antas ng negosyo, kayang lumawak, at madaling gamitin.

## Ang mga insentibo

### Ligtas na paglalayag sa tanawin ng quantum computing

* **Katiyakan ng seguridad**: nagbibigay sa mga organisasyon ang paggamit ng aklatang hash (HSH) ng katiyakang mananatiling ligtas ang kanilang datos.

* **Paghahanda sa hinaharap**: ang pagyakap ngayon sa mga algoritmong lumalaban sa quantum ay nagsasanggalang sa mga organisasyon laban sa posibleng kahinaan sa hinaharap.

* **Kahusayan sa gastos**: ang aklatang hash (HSH) ay bukas ang pinagmulan at magagamit nang hindi kailangan ng mamahaling lisensiya o bayad sa suskripsiyon. Kaya nagiging kaakit-akit itong pagpipilian sa mga organisasyong naghahangad panatilihing mababa ang gastos habang nakakamit ang ligtas na quantum computing.

### Pagpapanatili ng tiwala ng mamimili

* **Pagsanggalang sa datos ng kliyente**: pinatatatag ng pagpapanatiling ligtas ng datos ng kliyente laban sa atake ng quantum na kompyuter ang tiwala ng kliyente sa kakayahan ng mga organisasyong ipagsanggalang ang kanilang impormasyon.

* **Pagsunod at obligasyong pangregulasyon**: nakatutulong ang paggamit ng mga abanteng pamamaraang kriptograpiko sa pagsunod sa mahihigpit na batas at alituntunin sa pagsanggalang ng datos, kaya naiiwasan ang mga legal na kahihinatnan at multa.

### HSH: ang pinakamahusay na aklatang hash na lumalaban sa quantum

* **Mataas na bisa**: ang paggamit ng [aklatang hash (HSH) ⧉][00] na nakabatay sa Rust ay nagbubunga ng seguridad, kahusayan, at bisa.
Pagkakatugma sa iba't ibang plataporma: pinagsasanggalang ng aklatang hash (HSH) ang datos sa iba't ibang plataporma at aplikasyon.

* **Kadalian ng pagpapatupad**: naghahandog ang aklatang hash (HSH) sa mga developer ng kasangkapang madaling ipatupad, kaya bumababa ang hadlang sa pagyakap sa mga algoritmong lumalaban sa quantum.

## Pangwakas

Naghahandog ang [aklatang hash (HSH) ⧉][00] ng magaan, mabisa, at madaling gamiting solusyon sa pagsanggalang sa datos gamit ang kriptograpiyang lumalaban sa quantum computing. Pinadadali nito sa mga developer ang pag-upgrade ng kanilang protokol na kriptograpiko upang maging lumalaban sa quantum nang hindi kailangan ang malalim na pag-unawa sa mga algoritmo.

Ang kriptograpiyang lumalaban sa quantum computing ay larangang mabilis umunlad, at nakatuon ang aklatang HSH na manatili sa unahan nito. Regular itong ina-update ng bagong algoritmo at tampok upang magsanggalang laban sa mga umuusbong na banta.

Kasalukuyang tinutukoy ng [National Institute of Standards and Technology (NIST) ⧉][02] ang hanay ng pamantayan para sa mga algoritmong kriptograpikong post-quantum sa pamamagitan ng [proyektong kriptograpiyang post-quantum (PQC) ⧉][03].

Mahalaga sa alinmang organisasyong humahawak ng sensitibong datos ang pagsanggalang sa inyong datos laban sa atake ng quantum computing. At ang [aklatang hash (HSH) ⧉][00] ay malakas na kasangkapang makatutulong sa inyo na ipagsanggalang ang inyong datos laban sa umuusbong na bantang ito.

[00]: https://crates.io/crates/hsh "The Hash Library (HSH) - Quantum-Resistant Cryptographic Hash Library for Password Hashing and Verification"
[01]: https://cloudcdn.pro/stocks/diagrams/alice-bob-eve-encryption.svg "Ligtas ngunit marupok: paglampas sa mga hamong kriptograpiko sa panahong quantum"
[02]: https://www.nist.gov/ "National Institute of Standards and Technology"
[03]: https://csrc.nist.gov/projects/post-quantum-cryptography "Post-Quantum Cryptography PQC"
