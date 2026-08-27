---
title: "CRYSTALS-Kyber: ang algoritmong nagsasanggalang sa panahong quantum"
tags: "quantum, CRYSTALS-Kyber, encryption, cybersecurity, banking, finance, data, future, post-quantum cryptography, cryptography, ISO 20022, DORA, quantum computing, AI, Rust"
subtitle: "Isang mekanismo ng pagbabalot ng susi na nakabatay sa sala-sala, hinirang ng NIST, na naghahandog ng seguridad na lumalaban sa quantum sa mas maliit na susi."
description: "Ang CRYSTALS-Kyber: isang mekanismo ng pagbabalot ng susi (KEM) na nakabatay sa suliraning Learning With Errors sa sala-sala — ang tatlong antas ng seguridad nito, ang laki ng susi nito, at kung bakit ito niyakap ng banking at ng mga serbisyong pinansiyal."
date: "Nov 19, 2023"
language: "fil-PH"
locale: "fil_PH"
banner: "https://cloudcdn.pro/stocks/images/galina-nelyubova-V70-ng4FuiA.webp"
banner_alt: "Isang makabago at eleganteng quantum na kompyuter"
keywords: "CRYSTALS-Kyber, KEM, pagbabalot ng susi, kriptograpiyang post-quantum, PQC, sala-sala, Learning With Errors, LWE, NIST, ENISA, Kyber512, Kyber768, Kyber1024, seguridad sa banking"
---
## CRYSTALS-Kyber: ang algoritmong nagsasanggalang sa panahong quantum

![Isang makabago at eleganteng quantum na kompyuter](https://cloudcdn.pro/stocks/images/galina-nelyubova-V70-ng4FuiA.webp).class=\"img-fluid clearfix\"

## Malalim na pagtingin

### Paglalayag sa bantang quantum: ang pagsilang ng CRYSTALS-Kyber

Sa naunang artikulo ko, [Pagsanggalang sa datos sa panahong quantum ⧉][03], tinalakay ko nang malalim ang nalalapit na banta ng quantum computing sa seguridad na digital, at tiningnan ko kung paano tinutugunan ng kriptograpiyang lumalaban sa quantum (QRC) ang bantang ito. Tutuklasin ko naman ngayon ang `CRYSTALS-Kyber`, isang mapanimulang algoritmong QRC na bumabago sa tanawin ng seguridad.

Ang mga quantum na kompyuter, sa kakayahan nilang magsagawa ng ilang kalkulasyon nang higit na mabilis kaysa sa karaniwang kompyuter, ay kumakatawan sa saligang panganib sa kasalukuyang algoritmo ng encryption. Nagbubunsod ito ng alalahanin hinggil sa seguridad ng sensitibong impormasyon, kabilang na ang mga transaksiyong pinansiyal, ang mga talaang medikal, at ang mga personal na komunikasyon.

Upang mabawasan ang bantang ito, bumuo ang mga kriptograpo ng mga algoritmong QRC, tulad ng `CRYSTALS-Kyber`. Ang algoritmong ito ay isang mekanismo ng pagbabalot ng susi (KEM) na idinisenyo upang ligtas na maipagpalit ang lihim na susi sa pagitan ng mga partido.

Sa kasalukuyan, namumukod ang `CRYSTALS-Kyber` bilang nangunguna sa proseso ng pagsasapamantayan ng kriptograpiyang post-quantum ng [National Institute of Standards and Technology (NIST) ⧉][05], na nagpapamalas ng potensiyal nito bilang matatag na solusyong pangseguridad para sa panahong digital.

### CRYSTALS-Kyber: seguridad na nakatindig laban sa quantum computing

Nakasalalay ang seguridad ng `CRYSTALS-Kyber` sa hirap ng paglutas sa suliraning `Learning With Errors (LWE)` sa ibabaw ng mga sala-salang (lattice) ng yunit. Ang masalimuot na hamong matematikal na ito, na itinuturing na hindi malulutas sa pagkalkula kahit ng mga quantum na kompyuter, ang haligi ng katatagan ng `CRYSTALS-Kyber` laban sa mga atakeng quantum.

### CRYSTALS-Kyber: isang radikal na pagbabago sa seguridad na digital

Kabilang ang `CRYSTALS-Kyber` sa pangkat ng mga algoritmong CRYSTALS (Cryptographic Suite for Algebraic Lattices), at buong-pagmamalaking taglay nito ang katangiang algoritmong ligtas sa quantum (QSA).

Bagaman hindi ganap na bago ang konsepto ng paggamit ng suliraning sala-sala para sa layuning kriptograpiko, itinataas ng `CRYSTALS-Kyber` ang konseptong ito sa antas ng kahusayang walang katulad. Ang kakayahan nitong lumikha ng susing kriptograpiko na mas maliit ang laki at may mas mabilis na pag-encrypt at pagbasag ay ginagawa itong angkop na angkop na pagpipilian sa mga aplikasyon sa tunay na buhay, lalo na sa mahigpit na mundo ng pinansiya.

![Divider][01].class=\"m-10 w-100\"

## Ang ideya

### Pag-unawa sa mekanismo ng CRYSTALS-Kyber: ang pagbabalot ng susi sa gitna

Nasa kaibuturan ng mapanimulang disenyo ng `CRYSTALS-Kyber` ang mapanlikha nitong paraan ng pagbabalot ng susi, isang saligang sangkap ng ligtas na komunikasyon. Ginagamit nito ang lakas ng kriptograpiyang nakabatay sa sala-sala, isang pamamaraang kilala sa katatagan nito laban sa mga atakeng quantum. Ginagamit ng abanteng teknik na ito ang mga balangkas na heometriko sa isang espasyong maraming dimensiyon upang lumikha ng susing kriptograpiko.

Gumagamit ang `CRYSTALS-Kyber` ng tiyak na uri ng suliraning sala-sala, na kilala sa katangian nito sa kahusayan at seguridad, upang lumikha ng susing kriptograpiko. Tinitiyak nito ang pagsanggalang sa sensitibong datos kahit sa harap ng pag-unlad ng quantum computing.

#### Ligtas na pagbabalot ng susi: ang kaibuturan ng CRYSTALS-Kyber

Ang pagbabalot ng susi ay tulad ng ligtas na pagsasara ng mensahe sa loob ng isang kahon, na ang tanging may susi upang buksan ito ay ang nilalayong tatanggap. Sa mundo ng kriptograpiya, kasangkot sa prosesong ito ang paglikha ng magkapares na susi: isang pampublikong susi na maaaring ibahagi nang hayagan, at isang pribadong susi na kailangang manatiling lihim. Nasa kakayahan nitong likhain at gamitin ang dalawang susing ito sa paraang tumitiyak ng walang katulad na seguridad ang katalinuhan ng `CRYSTALS-Kyber`.

Tingnan natin kung paano ginagamit ng `CRYSTALS-Kyber` ang pagbabalot ng susi upang magtatag ng ligtas na komunikasyon sa pagitan ng dalawang partido, sina Alice at Bob. Ipinapakita ng diyagram ng pagkakasunod-sunod sa ibaba ang mga hakbang sa pagtatatag ng ligtas na komunikasyon nina Alice at Bob gamit ang `CRYSTALS-Kyber`, isang mekanismong KEM na idinisenyo upang tiyakin ang ligtas na palitan ng susi para sa mga protokol ng encryption. Gumaganap dito ng mahalagang papel ang KyberServer, sapagkat ito ang lumilikha at namamahagi ng susing kriptograpiko.

![Ang mekanismo ng pagbabalot ng susi (KEM) sa CRYSTALS-Kyber][04].class=\"img-fluid clearfix\"

##### Paliwanag

- Alice: ang nagpapadala ng mensahe.
- Bob: ang tumatanggap ng mensahe.
- KyberServer: ang serber na lumilikha at namamahagi ng susing kriptograpiko.

##### Pagpapaliwanag

###### Ang palitan ng pampublikong susi

- Sinisimulan ni Alice ang proseso sa paghiling ng kanyang pampublikong susi mula sa KyberServer.
- Tumutugon ang KyberServer sa pagpapadala ng pampublikong susi ni Alice, na isang halagang matematikal na maaaring ibahagi nang hayagan nang hindi nasasakripisyo ang seguridad ng pribadong susi ni Alice.
- Ibinabahagi naman ni Alice ang kanyang pampublikong susi kay Bob, kaya nagagawa nitong mag-encrypt ng mensaheng siya lamang ang makababasag.

###### Ang pagbabalot at pagbubukas ng balot

- Humihiling si Bob ng susi sa pagbabalot mula sa KyberServer. Gagamitin ang pansamantalang susing ito upang i-encrypt ang pinagsasaluhang lihim na susi bago ito ipadala kay Alice.
- Ipinadadala ng KyberServer ang susi sa pagbabalot kay Bob.
- Ginagamit ni Bob ang pampublikong susi ni Alice at ang susi sa pagbabalot upang i-encrypt ang pinagsasaluhang lihim na susi, kaya nakalilikha siya ng naka-encrypt na kapsula.
- Ipinadadala ni Bob ang naka-encrypt na kapsula kay Alice.
- Humihiling si Alice ng susi sa pagbubukas mula sa KyberServer. Gagamitin ang pansamantalang susing ito upang buksan ang naka-encrypt na kapsula at ibunyag ang pinagsasaluhang lihim na susi.
- Ipinadadala ng KyberServer ang susi sa pagbubukas kay Alice.

###### Ang palitan ng pinagsasaluhang lihim na susi

- Ginagamit ni Alice ang kanyang pribadong susi at ang susi sa pagbubukas upang buksan ang kapsula, kaya nabubunyag ang pinagsasaluhang lihim na susi.
- Ibinabahagi ni Alice ang pinagsasaluhang lihim na susi kay Bob, kaya nagagawa nitong basagin ang mga mensaheng naka-encrypt sa susing ito.

###### Ang ligtas na komunikasyon

Mabisang ipinapakita ng diyagram ang masasalimuot na hakbang sa pagtatatag ng ligtas na daluyan ng komunikasyon, at itinatampok nito ang mapagpasyang papel ng KyberServer sa paglikha at pamamahagi ng susing kriptograpiko. Sa paggamit ng KEM na `CRYSTALS-Kyber`, kayang ipagsanggalang nina Alice at Bob ang kanilang sensitibong impormasyon at mapanatili ang ligtas na komunikasyon kahit sa harap ng mga posibleng kalaban.

### Ang kriptograpiyang nakabatay sa sala-sala: matatag na saligan ng paglaban sa quantum

Gumagamit ang `CRYSTALS-Kyber` ng paraang nakabatay sa sala-sala, isang pamamaraang kilala sa posibleng paglaban nito sa mga atakeng quantum. Ang prinsipyong nasa likod ng kriptograpiyang nakabatay sa sala-sala ay may kinalaman sa mga balangkas na heometriko sa espasyong maraming dimensiyon. Bagaman maaaring mukhang mabigat ang paglalayag sa masasalimuot na balangkas na ito, pinasisimple ito ng `CRYSTALS-Kyber`. Gumagamit ito ng tiyak na uri ng suliraning sala-sala, na kilala sa katangian nito sa kahusayan at seguridad, upang lumikha ng susing kriptograpiko.

#### Mabisang laki ng susi: balanse ng seguridad at bisa

Isa sa mga pangunahing tampok ng `CRYSTALS-Kyber` ang laki ng susi nito. Kumpara sa ibang algoritmo ng kriptograpiyang post-quantum (PQC), naghahandog ang `CRYSTALS-Kyber` ng laki ng susing higit na maliit, kaya nagiging higit itong praktikal sa mga aplikasyon sa tunay na buhay. Naghahandog ang `CRYSTALS-Kyber` ng tatlong antas ng seguridad, na ang bawat isa ay may sariling laki ng susi:

- **Kyber512**: naghahandog ang antas na ito ng seguridad na 128 bit, at gumagamit ito ng laki ng susing 1,632 byte para sa lihim na susi, 800 byte para sa pampublikong susi, at 768 byte para sa naka-encrypt na teksto.
- **Kyber768**: naghahandog ito ng seguridad na 192 bit, at gumagamit ito ng laki ng susing 2,400 byte para sa lihim na susi, 1,184 byte para sa pampublikong susi, at 1,088 byte para sa naka-encrypt na teksto.
- **Kyber1024**: naghahandog ito ng seguridad na 256 bit, at gumagamit ito ng laki ng susing 3,168 byte para sa lihim na susi, 1,568 byte para sa pampublikong susi, at 1,568 byte para sa naka-encrypt na teksto.

Ginagawa ng medyo maliliit na lakíng ito ang `CRYSTALS-Kyber` na kaakit-akit na pagpipilian para sa mga aparatong limitado ang mapagkukunan, tulad ng smartphone at ng aparatong IoT. Binabawasan din nito ang bandwidth na kailangan sa paglilipat ng susing kriptograpiko, na maaaring makatulong sa mga aplikasyong limitado ang koneksiyon sa network.

#### Hindi natitinag na bilis: isang parola sa mabilis na tanawing pinansiyal

Isa pang bagay na nagpapaakit sa `CRYSTALS-Kyber` ang bilis nito. Sa mabilis na sektor ng banking at ng mga serbisyong pinansiyal, kasinghalaga ng seguridad ang bilis. Tinitiyak ng disenyo ng algoritmo na gumagana ito nang mahusay, kaya napadadali ang mabilis na pag-encrypt at pagbasag. Hindi nakukuha ang kahusayang ito sa kapalit ng seguridad; tuwiran itong bunga ng abanteng saligang matematikal ng algoritmo.

### CRYSTALS-Kyber: ang pagsasanib ng seguridad, kahusayan, at bilis

Sumulpot ang `CRYSTALS-Kyber` bilang nangunguna sa paghahanap ng kriptograpiyang lumalaban sa quantum computing, at naghahandog ito ng natatanging halo ng seguridad, kahusayan, at bilis. Ang mapanlikha nitong paraang nakabatay sa sala-sala, ang mas maliit na laki ng susi nito, at ang optimisadong disenyo nito ay ginagawa itong angkop na angkop na pagpipilian sa pagsanggalang ng sensitibong impormasyon sa industriya ng banking at ng mga serbisyong pinansiyal. At habang patuloy na niyayakap ng mundo ang mga teknolohiyang digital, nakahanda ang `CRYSTALS-Kyber` na gumanap ng mahalagang papel sa pagsanggalang ng ating datos sa mga darating na taon.

![Divider][01].class=\"m-10 w-100\"

## Ang epekto

### CRYSTALS-Kyber: mga bentahe para sa banking at mga serbisyong pinansiyal

Nakikipagkarera nang walang tigil ang industriya ng banking at ng mga serbisyong pinansiyal upang manatiling nangunguna laban sa mga bantang sibernetikong lalong nagiging sopistikado. Sa kalagayang ito, namumukod ang `CRYSTALS-Kyber` hindi lamang dahil sa katangian nitong lumalaban sa quantum (QR), kundi dahil din sa nadaramang pakinabang na inihahandog nito sa industriyang ito. Tinatalakay ng bahaging ito ang mga praktikal na tampok ng `CRYSTALS-Kyber`, at itinatampok kung bakit partikular itong angkop sa natatanging pangangailangan ng mga institusyong pinansiyal.

- **Pinatatag na seguridad gamit ang mas maliliit na susi**: isa sa pangunahing bentahe ng `CRYSTALS-Kyber` ang kakayahan nitong lumikha ng mas maliit na susi ng encryption nang hindi isinasakripisyo ang seguridad. Sa isang sektor na maaaring maging mapaminsala ang bunga ng paglabag sa datos, hindi napag-uusapan ang matatag na seguridad. Pinasisimple ng mas maliit na laki ng susing inihahandog ng `CRYSTALS-Kyber` ang pangangasiwa ng susi, na mapagpasyang salik sa malalaking sistemang pambangko kung saan libu-libong susi ang nasa sirkulasyon. Hindi lamang nito pinatatatag ang seguridad, kundi pinabubuti rin nito ang kahusayan ng pag-iimbak at pagpapadala, na napakahalagang salik sa panahong mahalaga ang bilis at ang espasyo.

- **Bilis at kahusayan**: sa mga serbisyong pinansiyal, kung saan nagaganap ang mga transaksiyon sa loob ng milisegundo, mapagpasya ang bilis ng operasyong kriptograpiko. Nangingibabaw ang `CRYSTALS-Kyber` sa bahaging ito, at naghahandog ito ng mabilis na operasyon sa paglikha ng susi, sa pagbabalot, at sa pagbubukas ng balot. Tinitiyak ng bilis na ito na hindi nagiging sagabal ang mga hakbang na pangseguridad sa kapaligiran ng mataas na dalas na kalakalan o sa panahon ng malalaking transaksiyon. Bukod dito, ang kahusayan ng `CRYSTALS-Kyber` ay nauuwi sa mas kaunting mapagkukunang pangkalkulasyon, kaya nakatutulong ito sa pagtitipid sa gastos at sa mas maunlad-sa-kapaligirang operasyon.

- **Paghahanda sa hinaharap laban sa mga bantang quantum**: sa pagdating ng quantum computing, humaharap ang industriya sa kinabukasang maaaring maging lipas na ang tradisyunal na pamamaraang kriptograpiko. Sa pagyakap sa `CRYSTALS-Kyber`, hindi lamang tinitiyak ng mga institusyong pinansiyal ang kanilang kasalukuyan, kundi inihahanda rin nila ang kanilang sarili para sa mundong post-quantum. Ipinamamalas ng maagap na paraang ito sa seguridad na sibernetiko ang kanilang pangako sa pangmatagalang pagsanggalang ng datos, isang saligang pagsasaalang-alang para sa mga may kinalaman at sa mga kliyenteng nagbibigay-prayoridad sa seguridad ng datos.

- **Pagsunod sa regulasyon at mapagkumpitensiyang bentahe**: habang sinisimulan ng mga tagapagregula sa buong mundo na kilalanin ang bantang quantum, malamang na iaatas nila ang pagyakap sa mga algoritmong lumalaban sa quantum. Ang maagang pagyakap sa `CRYSTALS-Kyber` ay naglalagay sa mga institusyong pinansiyal bilang nangunguna sa pagsunod at sa seguridad. Naghahandog din ito ng mapagkumpitensiyang bentahe, sapagkat nagbibigay ito ng katiwasayan sa mga kliyente at katuwang hinggil sa pangako ng institusyon sa abanteng kasanayang pangseguridad.

![Divider][01].class=\"m-10 w-100\"

## Ang mga insentibo

### Ang argumento para sa pagyakap sa CRYSTALS-Kyber

Sa isang tanawing hindi lamang pangangailangan kundi mapagkumpitensiyang pagkakaiba rin ang seguridad na sibernetiko, nakatayo ang industriya ng banking at ng mga serbisyong pinansiyal sa isang mapagpasyang sangandaan. Ang pagyakap sa `CRYSTALS-Kyber` ay kumakatawan sa estratehikong hakbang na naaayon sa kasalukuyang pangangailangan sa seguridad at sa mga darating na pagbabagong teknikal nang sabay. Tinatalakay ng huling bahaging ito ang mga nakakukumbinsing insentibo sa pagsasanib ng `CRYSTALS-Kyber` sa balangkas na kriptograpiko ng mga serbisyong pinansiyal.

- **Pananatili sa unahan ng mga usong pangseguridad**: kumakatawan ang pag-angat ng quantum computing sa saligang banta sa tradisyunal na algoritmo ng encryption, sapagkat ginagawa nitong mababasag ng mga darating na quantum na kompyuter ang mga ito. Sa pagyakap sa `CRYSTALS-Kyber`, kayang ipagsanggalang ng mga institusyong pinansiyal ang kanilang sensitibong datos at ang kanilang mahalagang imprastruktura laban sa mga umuusbong na bantang ito.

- **Kahusayan sa operasyon at pagiging matipid**: ang siksik na laki ng susi at ang mabisang algoritmo ng `CRYSTALS-Kyber` ay nauuwi sa malaking pagtitipid sa gastos. Kumpara sa tradisyunal na algoritmo ng encryption, binabawasan ng `CRYSTALS-Kyber` ang pangangailangan sa imbakan nang hanggang 50% at ang pagkonsumo ng bandwidth nang hanggang 30%, kaya nagbubunga ito ng malaking pagtitipid para sa mga institusyong pinansiyal na may napakalaking dami ng datos.

- **Pagkakaayon sa regulasyon at pangangasiwa ng panganib**: sa pagrerekomenda ng ilang katawang pangregulasyon, kabilang na ang National Institute of Standards and Technology (NIST) at ang European Union Agency for Cybersecurity (ENISA), ng pagyakap sa solusyong kriptograpikong lumalaban sa quantum, mapapabuti ang katayuan ng mga maagang gumamit ng `CRYSTALS-Kyber` upang sumunod sa mga darating na kahingiang pangregulasyon at mabawasan ang posibleng legal na panganib.

- **Pagpapatibay ng tiwala ng kliyente at ng reputasyon ng institusyon**: niyakap ng mga nangungunang institusyong pinansiyal tulad ng Barclays at Deutsche Bank ang `CRYSTALS-Kyber` upang ipagsanggalang ang datos ng kanilang kliyente at tiyakin ang seguridad ng kanilang mahahalagang transaksiyong pinansiyal. Hindi lamang pinangalagaan ng pangakong ito sa abanteng seguridad ang mga institusyong ito laban sa posibleng atakeng sibernetiko, kundi pinatibay din nito ang kanilang reputasyon bilang mapagkakatiwalaang tagapangalaga ng sensitibong impormasyon.

![Divider][01].class=\"m-10 w-100\"

## Pangwakas

### Pagtiyak ng seguridad ng kinabukasang pinansiyal gamit ang CRYSTALS-Kyber

Sa harap ng umuunlad na bantang sibernetiko, humaharap ang industriya ng banking at ng mga serbisyong pinansiyal sa isang mapagpasyang pagpipilian. Ang tradisyunal na algoritmo ng encryption, na dating itinuring na ligtas, ay marupok na ngayon sa harap ng umuusbong na lakas ng quantum computing. Namumukod ang `CRYSTALS-Kyber` bilang parola ng seguridad, at naghahandog ito ng matatag, mabisa, at napapanatiling solusyon sa pagsanggalang ng mga digital na ari-arian ng sektor na pinansiyal.

Sa natatanging halo nito ng katangiang lumalaban sa quantum, ng kahusayan sa operasyon, at ng mas maliit na laki ng susi, kumakatawan ang `CRYSTALS-Kyber` sa isang punto ng pagbabago sa seguridad na pinansiyal. Sa pagyakap sa `CRYSTALS-Kyber`, hindi lamang tinitiyak ng mga institusyon ang seguridad ng kanilang kasalukuyang operasyon, kundi inihahanda rin nila ang sarili sa kinabukasang muling bibigyang-kahulugan ng quantum computing ang seguridad na sibernetiko. Ipinamamalas ng maagap na paraang ito ang kanilang pangako sa pinakamataas na pamantayan ng seguridad, na nagpapatibay sa tiwala ng kliyente at sumusuporta sa katatagan ng industriya laban sa mga umuunlad na banta.

Sa isang mundong lalong nagkakaugnay at nagiging digital, nakatayo ang `CRYSTALS-Kyber` bilang patotoo sa lakas ng mapanlikha at malayong-tanaw na solusyon. Ang pagyakap dito ng mga nangungunang institusyong pinansiyal tulad ng Barclays at Deutsche Bank ay malakas na pagsang-ayon sa kakayahan nito at malinaw na hudyat sa industriya na yakapin ang solusyong kriptograpikong lumalaban sa quantum na ito.

![Divider][01].class=\"m-10 w-100\"

Sa pagtatapos, umaasa akong naliwanagan ng pagtuklas na ito sa `CRYSTALS-Kyber` ang malalim na epekto ng kriptograpiyang lumalaban sa quantum computing sa sektor na pinansiyal. At kung nais ninyong lumalim pa sa mapanimulang teknolohiyang ito o kung mayroon kayong anumang katanungan, inaanyayahan ko kayong makipag-ugnayan sa akin sa [LinkedIn ⧉][02] o sa pamamagitan ng [pahina ng pakikipag-ugnayan][00].

Maraming salamat muli sa inyong panahon, at inaasahan kong makarinig mula sa inyo.

[00]: /contact/index.html "Contact"
[01]: https://cloudcdn.pro/clients/common/images/elements/divider.svg "Divider"
[02]: https://www.linkedin.com/in/sebastienrousseau/ "Sebastien Rousseau on LinkedIn"
[03]: /2023-10-16-protecting-data-in-the-quantum-age-the-hash-library-hsh/index.html "Protecting Data in the Quantum Age: The Hash Library (HSH)"
[04]: https://cloudcdn.pro/stocks/diagrams/alice-bob-eve-kyber.svg "CRYSTALS-Kyber Key Encapsulation Mechanism (KEM)"
[05]: https://www.nist.gov/ "The National Institute of Standards and Technology (NIST)"
