---
title: "Ang ganap na homomorphic na encryption (FHE) sa panahong quantum ng banking"
tags: "FHE, Banking, quantum computing, Data Security, Encryption, Financial Technology, Regulatory Compliance, Computational Overhead, Research, Data Privacy, ISO 20022, post-quantum cryptography, AI"
subtitle: "Kalkulasyon sa naka-encrypt na datos: ang balangkas ni Gentry, ang paglaban sa quantum sa pamamagitan ng sala-sala, at ang gamit nito sa banking."
description: "Ang ganap na homomorphic na encryption (FHE) sa banking: kung paano nagpapahintulot ng kalkulasyon sa naka-encrypt na datos, kung bakit ito lumalaban sa quantum sa pamamagitan ng SVP at CVP, at ang anim na gamit nito mula ligtas na pagsusuri hanggang naka-encrypt na LLM."
date: "Mar 25, 2024"
language: "fil-PH"
locale: "fil_PH"
banner: "https://cloudcdn.pro/stocks/images/fully-homomorphic-encryption.webp"
banner_alt: "FHE Architecture"
keywords: "FHE, ganap na homomorphic na encryption, kriptograpiya, sala-sala, Craig Gentry, post-quantum, SVP, CVP, banking, GDPR, CCPA, Zama, LLM, pagkapribado"
---
## Ang ganap na homomorphic na encryption (FHE) sa panahong quantum ng banking

Nangangako ang **ganap na homomorphic na encryption (FHE — Fully Homomorphic Encryption)** na muling bigyang-kahulugan ang seguridad ng datos sa sektor ng banking at sa industriyang pinansiyal. At sa pagbibigay-kakayahan ng pagsasagawa ng kalkulasyon sa naka-encrypt na datos, pinagsasanggalang ng FHE ang pagkapribado laban sa tradisyunal at sa kuwantum na banta nang sabay.

## Panimula

Hindi lamang teoriya ang pagpapatupad ng FHE sa sektor na pinansiyal; naging praktikal na katotohanan na itong bumabago sa pamantayan ng seguridad at pagkapribado ng datos. At tinutuklas ng artikulong ito ang praktikal na gamit, ang alalahanin sa regulasyon, ang mga posibleng kahinaan, at ang pagsulong ng pananaliksik ng ganap na homomorphic na encryption sa pinansiya at sa mga aplikasyon din ng artipisyal na katalinuhan (AI).

## Pag-unawa sa ganap na homomorphic na encryption

### Ang saligan ng encryption

Ang encryption ay pamamaraan ng pagbabago ng mababasang datos (malinaw na teksto) tungo sa anyong hindi mababasa (naka-encrypt na teksto) gamit ang algoritmo at susi ng encryption. At ang pangunahing layunin ay tiyaking ang mga awtorisadong partido lamang ang makaaabot sa orihinal na datos, sa pamamagitan ng pagbasag sa naka-encrypt na teksto gamit ang susi sa pagbasag.

### Ang tradisyunal na pamamaraan ng encryption

Nahahati ang tradisyunal na pamamaraan ng encryption sa dalawang pangunahing uri: ang simetrikong encryption at ang asimetrikong encryption. Gumagamit ang simetrikong encryption ng iisang susi para sa encryption at para sa pagbasag nito. At nakukuha ang kahusayang ito sa kapalit ng seguridad, lalo na kapag hamon ang pamamahagi ng susi. Ang asimetrikong encryption naman, na kilala rin bilang encryption sa pamamagitan ng pampublikong susi, ay gumagamit ng dalawang susi, isa para sa encryption at isa para sa pagbasag. At mas ligtas ang pamamaraang ito ngunit mas mabagal ito kaysa sa simetrikong encryption.

### Ang hangganan ng tradisyunal na encryption pagdating sa kalkulasyon

Bagaman mabisang pinagsasanggalang ng tradisyunal na pamamaraan ng encryption ang datos na nakaimbak o inililipat, nabibigo ang mga ito kapag nagsasagawa ng kalkulasyon sa naka-encrypt na datos. At karaniwan, upang maproseso o masuri ang naka-encrypt na datos, kailangan muna itong basagin, pagkatapos ay isagawa ang kinakailangang operasyon, at pagkatapos ay muli itong i-encrypt. At ang hakbang na pagbasag na ito ay malaking panganib sa pagkapribado ng datos, lalo na sa mga kapaligirang hindi mapagkakatiwalaan o sa kapaligiran ng pagkalkula sa ulap.

![divider][divider].class=\"m-10 w-100\"

## Ang malaking tagumpay ng homomorphic na encryption

Nilulutas ng **homomorphic na encryption (HE)** ang hangganan ng tradisyunal na encryption. Pinahihintulutan nito ang pagsasagawa ng ilang kalkulasyon nang tuwiran sa naka-encrypt na datos (naka-encrypt na teksto). At ang nabasag na resulta ay katulad ng orihinal na datos (malinaw na teksto) matapos isagawa ang parehong operasyon. At may tatlong pangunahing uri ang homomorphic na encryption: ang bahagyang homomorphic na encryption (PHE), ang tinatayang homomorphic na encryption (SHE), at ang ganap na homomorphic na encryption (FHE).

- **Bahagyang homomorphic na encryption (Partially Homomorphic Encryption - PHE):** sinusuportahan nito ang walang hangganang bilang ng operasyon ng iisang uri lamang (tulad ng pagdaragdag o ng pagpaparami) sa naka-encrypt na teksto.
- **Tinatayang homomorphic na encryption (Somewhat Homomorphic Encryption - SHE):** sinusuportahan nito ang limitadong bilang ng operasyon, na pinagsasama ang pagdaragdag at ang pagpaparami, ngunit hanggang sa tiyak na lalim lamang.
- **Ganap na homomorphic na encryption (Fully Homomorphic Encryption - FHE):** ang pinaka-abanteng anyo, na nagpapahintulot ng walang hangganang operasyon ng pagdaragdag at pagpaparami sa naka-encrypt na teksto.

### Ang teknikal na katalinuhan ng FHE

Nakasalalay ang FHE sa masasalimuot na balangkas na matematikal, tulad ng kriptograpiyang nakabatay sa sala-sala (lattice-based cryptography). At ang kriptograpiyang nakabatay sa sala-sala ay uri ng kriptograpiyang gumagamit ng balangkas na matematikal na tinatawag na sala-sala.

Ang sala-sala ay regular na pagkakaayos ng mga punto sa espasyo, at nakasalalay ang kriptograpiyang nakabatay sa sala-sala sa hirap ng paglutas ng ilang suliraning matematikal na kaugnay ng mga balangkas na ito. At ginagawa nitong ligtas at lumalaban sa atake ang kriptograpiyang nakabatay sa sala-sala, kabilang na ang atake mula sa mga quantum na kompyuter.

Noong 2009, bumuo si Craig Gentry ng pamamaraan, na inilarawan sa kanyang papel ng pananaliksik na [**A Fully Homomorphic Encryption Scheme ⧉**][00], upang makalikha ng sistemang kayang magsagawa ng homomorphic na pagtatasa ng sarili nitong sirkuwito ng pagbasag. At pinahihintulutan ng sarili-nitong-tinutukoy na disenyong ito ng mga balangkas na FHE ang pagsasagawa ng kahit anong kalkulasyon sa naka-encrypt na datos.

### Ang proseso ng algoritmong FHE

![FHE Operational Flow][fhe].class=\"m-10 w-100\"

Ipinapaliwanag ng diyagram sa itaas ang daloy ng operasyon ng algoritmong FHE.

- Nagsisimula ang proseso ng encryption sa malinaw na datos na ini-encrypt gamit ang susi ng encryption upang makalikha ng naka-encrypt na teksto.

- Maaaring sumailalim ang naka-encrypt na datos na ito sa maraming kalkulasyon nang tuwiran sa naka-encrypt na teksto sa pamamagitan ng prosesong kilala bilang bootstrapping.

- Pinahihintulutan ng natatanging kakayahang ito ng FHE na manatiling naka-encrypt ang datos sa buong proseso. At sa sandaling maisagawa ang kinakailangang operasyon, kayang ibalik ng proseso ng pagbasag ang binagong naka-encrypt na teksto tungo sa malinaw na teksto gamit ang balangkas na FHE.

Nasa kakayahan nitong magsagawa ng kalkulasyon sa naka-encrypt na teksto nang hindi kailangang basagin ito ang pangunahing bentahe ng FHE, kaya tinitiyak nito ang pagpapanatili ng pagkapribado at seguridad ng datos sa buong proseso ng kalkulasyon.

### Ang paglaban ng FHE sa quantum

Madalas na marupok sa mga algoritmong kuwantum ang tradisyunal na pamamaraan ng encryption. Sapagkat kayang lutasin nang mabilis ng mga algoritmong ito ang mga suliraning tulad ng pagpapaktor ng buong bilang at ng diskretong logaritmo, na siyang saligan ng mga pamamaraang ito. Sa kabaligtaran, gumagamit ang FHE ng mga suliraning nakabatay sa sala-sala na pinaniniwalaang mahirap lutasin ng mga quantum na kompyuter. At ginagawa ng paglaban sa quantum na ito ang FHE na maaasahang pamamaraan ng encryption para sa panahong post-quantum.

Lumalaban sa atakeng kuwantum ang FHE na nakabatay sa sala-sala sapagkat ang mga saligang suliraning matematikal, tulad ng Shortest Vector Problem (SVP) at ng Closest Vector Problem (CVP), ay itinuturing na mahirap lutasin kahit ng mga quantum na kompyuter. At bagaman kayang basagin ng mga algoritmong kuwantum tulad ng algoritmo ni Shor ang tradisyunal na pamamaraan ng encryption na nakasalalay sa pagpapaktor ng malalaking bilang o sa pagkalkula ng diskretong logaritmo, hindi sila kilalang naghahandog ng malaking bentahe sa paglutas ng suliraning nakabatay sa sala-sala. At ginagawa ng katangiang ito ang FHE na nakabatay sa sala-sala na maaasahang kandidato para sa kriptograpiyang post-quantum.

![divider][divider].class=\"m-10 w-100\"

## Ang epekto ng FHE sa sektor ng banking at pinansiya

### Pagpapatibay ng pagkapribado at seguridad ng datos

Nangangako ang paggamit ng FHE sa sektor na pinansiyal ng malaking pagpapatibay sa pagkapribado ng datos. Sapagkat kaya na ngayon ng mga bangko na magsagawa ng pagtatasa ng panganib, ng pagtuklas ng pandaraya, at ng masaklaw na pagsusuri ng datos, habang tinitiyak ang ganap na pagkalihim ng impormasyon ng kliyente. At binabawasan ng teknikal na pagsulong na ito ang panganib ng paglabag sa datos, kaya pinatatatag nito ang integridad ng plataporma ng digital na banking at ng mga transaksiyong pinansiyal.

### Ang pagkalkula sa ulap at ang panlabas na pagkuha

Isa sa malalaking larangan ng paggamit ng homomorphic na encryption ang ligtas na pagproseso ng datos sa ulap. Sapagkat kayang gamitin ng mga bangko ang serbisyo ng pagkalkula sa ulap upang maproseso ang naka-encrypt na datos nang hindi isinasakripisyo ang pagkapribado nito. At pinahihintulutan nito ang mga institusyong pinansiyal na gamitin ang kakayahang lumawak at ang pagiging matipid ng pagkalkula sa ulap, habang pinananatili ang pagkalihim ng sensitibong impormasyong pinansiyal.

Binibigyang-diin ng paglipat tungo sa pagkalkula sa ulap at ng panlabas na pagkuha ng gawaing pangkalkulasyon ng mga bangko ang halaga ng FHE. Sapagkat salamat sa ligtas na pagkalkula sa ulap, kayang abutin ng mga institusyong pinansiyal ang panlabas na mapagkukunan habang pinagsasanggalang ang sensitibo at naka-encrypt na datos sa pamamagitan ng FHE. At pinahihintulutan ng FHE ang mga bangko na ligtas na gamitin ang serbisyo ng pagkalkula sa ulap, habang tinitiyak na nananatiling protektado sa lahat ng oras ang sensitibo at naka-encrypt na datos.

![divider][divider].class=\"m-10 w-100\"

## Paghahanda para sa kinabukasang kuwantum

Nagbabadya ang nalalapit na pagdating ng quantum computing ng posibleng krisis para sa tradisyunal na pamamaraan ng kriptograpiya. At likas na lumalaban sa atakeng kuwantum ang FHE na nakabatay sa sala-sala, kaya naghahandog ito ng matatag na depensa laban sa bantang dulot ng quantum computing sa seguridad ng datos.

### Ang kriptograpiyang lumalaban sa quantum

Naghahandog ang FHE ng napakalakas na layer ng proteksiyon laban sa banta ng quantum computing. At sa paggamit ng mga teknik sa encryption na nakabatay sa sala-sala, tinitiyak ng FHE na mananatiling ligtas ang datos at ari-ariang pinansiyal kahit sa harap ng mga kalabang kuwantum.

Nagmumula ang paglaban sa quantum ng FHE sa masasalimuot na saligang suliraning matematikal tulad ng Shortest Vector Problem (SVP) at ng Closest Vector Problem (CVP). At pinaniniwalaang mahirap lutasin ang mga suliraning ito kahit ng mga quantum na kompyuter, kaya ginagawa nitong angkop na angkop na kandidato ang FHE na nakabatay sa sala-sala para sa kriptograpiyang post-quantum.

Ang paggamit ng kriptograpiyang lumalaban sa quantum, tulad ng FHE, ay saligan hindi lamang sa pagsanggalang ng ari-ariang pinansiyal, kundi sa pagpapanatili rin ng tiwala ng kliyente sa panahong digital. At habang sumusulong ang quantum computing, mas nasa mabuting katayuan ang mga institusyong pinansiyal na nagbibigay-prayoridad sa matatag na encryption upang maglayag sa hamon at pagkakataon sa hinaharap.

![divider][divider].class=\"m-10 w-100\"

## Ang kinabukasan ng FHE sa sektor ng banking at pinansiya

Maaasahan ang landas ng FHE sa sektor na pinansiyal, ngunit humaharap pa rin ito sa hamon. At magagamit ng industriya ng banking ang buong potensiyal ng FHE sa pamamagitan ng pagpapatibay ng teknolohiya, ng pagsasanib nito sa pang-araw-araw na operasyong pinansiyal, at ng pakikipagtulungan sa mga katawang pangregulasyon.

Magagamit ang FHE sa iba't ibang aplikasyong pambangko at pinansiyal, tulad ng:

- **Ligtas na pagsusuri ng datos na pinansiyal**: pinahihintulutan ng FHE ang mga bangko na suriin ang naka-encrypt na datos na pinansiyal tulad ng transaksiyon, marka ng utang, at portfolio ng pamumuhunan, nang hindi isinasakripisyo ang pagkapribado ng kliyente, kaya tinitiyak nito ang ligtas na pagproseso ng sensitibong impormasyon.

- **Machine learning na nagpapanatili ng pagkapribado**: pinahihintulutan ng FHE ang mga bangko na sanayin at ilunsad ang modelo ng machine learning sa naka-encrypt na datos, kaya binibigyang-kakayahan nila ang sarili na gamitin ang AI sa pagtuklas ng pandaraya, sa pagtatasa ng panganib, at sa paghahati-hati ng kliyente, habang pinananatili ang pagkalihim ng datos.

- **Ligtas na kalkulasyong maraming partido**: pinahihintulutan ng FHE ang ligtas na pakikipagtulungan sa pagitan ng maraming institusyong pinansiyal, kaya nagagawa nilang magsagawa ng pinagsasaluhang kalkulasyon sa naka-encrypt na datos nang hindi ibinabahagi ang sensitibong impormasyon, kaya pinadadali nito ang ligtas na transaksiyon sa pagitan ng mga bangko at ang pagsunod.

- **Seguridad ng interface sa pagpoprograma ng aplikasyon (API)**: kayang tiyakin ng FHE ang seguridad ng mga API sa pamamagitan ng pag-encrypt ng sensitibong datos bago ito ilipat, upang matiyak na mananatiling lihim ang impormasyon ng kliyente sa panahon ng palitan ng datos sa pagitan ng mga bangko at ng panlabas na serbisyo.

- **Ligtas na pagkalkula sa ulap**: pinahihintulutan ng FHE ang mga bangko na kumuha ng ligtas na panlabas na mapagkukunan sa ulap para sa kalkulasyon at pag-iimbak ng datos nang hindi isinasakripisyo ang pagkapribado nito, sapagkat nananatiling naka-encrypt ang datos sa buong proseso, kaya pinalalawak nito ang paggamit ng matipid at kayang lumawak na serbisyo sa ulap.

- **Pagsunod sa regulasyon na nagpapanatili ng pagkapribado**: pinahihintulutan ng FHE ang mga bangko na ligtas na maibahagi ang naka-encrypt na datos sa mga awtoridad na pangregulasyon, kaya binibigyang-kakayahan nila ang sarili na sumunod sa kahingian sa pag-uulat nang hindi ibinubunyag ang sensitibong impormasyon ng kliyente, kaya pinasisimple nito ang proseso ng pagsunod habang pinananatili ang pagkapribado.

Ibinubunyag ng mga aplikasyong ito ang mapagbagong lakas ng FHE sa sektor ng banking at pinansiya, at itinatampok nila ang potensiyal nitong baguhin ang pamantayan ng seguridad at pagkapribado ng datos.

![divider][divider].class=\"m-10 w-100\"

## Paglampas sa hamon ng pagyakap sa FHE

### Ang hamon sa bisa at ang pagpapabuti nito

Nananatiling mahalagang hamon ang pagtugon sa bigat na pangkalkulasyon na likas sa FHE. At pinaliliit ng kamakailang pagsulong sa pagpapabuti ng algoritmo at ng pagbuo ng espesyalisadong tagapabilis na kagamitan ang agwat sa bisa sa pagitan ng tradisyunal na pagkalkula at ng FHE.

### Ang pagsasapamantayan at ang pakikipagtulungan

Nakasalalay ang landas tungo sa malawakang pagyakap sa FHE sa pagsasapamantayan ng protokol at sa pagpapatibay ng pakikipagtulungan sa pagitan ng mga may kinalaman sa ekosistemang pinansiyal. At kayang malaki ang mapabilis ng nagkakaisang paraan ng pagyakap sa FHE ang pagsasanib nito sa pangunahing serbisyong pinansiyal.

### Ang regulasyon at ang pagsunod

Gumaganap ang mga katawang pangregulasyon ng mapagpasyang papel sa pagyakap sa FHE, sapagkat ipinapataw ng umuunlad na batas sa pagkapribado ng datos ang paggamit nito. At maaaring maging katalista ang pagtulak na pangregulasyon para sa malawakang pagyakap sa FHE sa industriya ng sektor ng banking at pinansiya, kasabay ng pagtiyak ng pagsunod sa alituntunin sa pagsanggalang ng datos.

Gumaganap ang tanawing pangregulasyon sa paligid ng pagkapribado at seguridad ng datos ng mahalagang papel sa pagyakap sa FHE sa industriya ng mga bangko. Sapagkat inaatasan ng mahigpit na alituntunin tulad ng pangkalahatang alituntunin sa pagsanggalang ng datos (GDPR) at ng batas sa pagkapribado ng mamimili sa California (CCPA) ang matatag na hakbang sa pagsanggalang ng datos, at binibigyang-diin nila ang karapatan ng indibidwal sa pagkapribado. At ang FHE, sa kakayahan nitong magproseso ng naka-encrypt na datos nang hindi binabasag ito, ay naaayon nang mabuti sa pagtuon na nakasentro sa pagkapribado ng mga alituntuning ito. At habang lalong humihigpit ang batas sa pagkapribado ng datos, naghahandog ang FHE ng nakakukumbinsing solusyong nagpapahintulot sa mga bangko na magsagawa ng kinakailangang kalkulasyon at pagsusuri habang sumusunod sa kahingian sa pagsunod.

![divider][divider].class=\"m-10 w-100\"

## Pagtiyak ng seguridad ng malalaking modelo ng wika sa pamamagitan ng ganap na homomorphic na encryption (FHE)

Ang malalaking modelo ng wika (LLMs) ay malalakas na kasangkapang AI. Gayunman, nagbubunsod ang paggamit ng mga ito ng alalahanin hinggil sa pagkapribado, lalo na kapag humaharap sa sensitibong datos ng gumagamit. At naghahandog ang ganap na homomorphic na encryption (FHE) ng solusyong nagsasanggalang sa pagkapribado ng gumagamit at nagpapanatili sa intelektuwal na pag-aari ng mga may-ari ng modelo, sa pamamagitan ng pagbibigay-kakayahan ng pagsasagawa ng kalkulasyon sa naka-encrypt na datos.

### Ang hamon sa pagkapribado ng malalaking modelo ng wika

Kasangkot sa paglulunsad ng malaking modelo ng wika sa mismong lugar upang mapanatili ang pagkapribado ng datos ang mga hamon tulad ng mataas na gastos at ng posibleng pagbubunyag ng mahalagang intelektuwal na pag-aari. At tinutugunan ng FHE ang mga hamong ito sa pamamagitan ng pagbibigay-kakayahan sa malalaking modelo ng wika na gumana sa naka-encrypt na datos ng gumagamit, kaya tinitiyak nito ang pagkapribado at ang seguridad ng modelo nang sabay.

### Ang paraan ng Zama para sa naka-encrypt na malaking modelo ng wika

Ang [**Zama ⧉**][01], isang kompanya ng teknolohiya para sa pagkapribado, ay nagpatunay ng pagiging posible ng pagbuo ng naka-encrypt na malaking modelo ng wika gamit ang FHE. At nakakamit ng paraan nito, na pinagsasama ang FHE at ang iba pang teknik na nagpapatibay ng pagkapribado, ang bisang katulad ng sa mga di-naka-encrypt na modelo na may katamtamang pagtaas lamang sa bigat na pangkalkulasyon.

### Pagpapabuti ng pagkapribado ng gumagamit sa pamamagitan ng naka-encrypt na malalaking modelo ng wika

Taglay ng pagsasanib ng FHE sa malalaking modelo ng wika ang posibilidad na baguhin ang pagkapribado ng gumagamit, lalo na sa mga aplikasyong humaharap sa sensitibong personal o pangkalakalang impormasyon. At habang lalong nagtutuon ang AI sa pagkapribado, mahalagang makipagtulungan ang mga developer, gumagamit, at katawang pangregulasyon. At ang pakikipagtulungang ito ang susi sa pagtatayo ng ekosistemang AI na nagbibigay-prayoridad sa seguridad at pagkapribado.

![divider][divider].class=\"m-10 w-100\"

## Pangwakas

Ang **ganap na homomorphic na encryption (FHE)** ay mapanimulang teknolohiya ng seguridad ng datos na naghahandog ng pambihirang pagkapribado at seguridad sa sektor ng banking at sa industriyang pinansiyal.

At habang sumusulong ang quantum computing, lalo pang nagiging mahalaga ang FHE. At muling huhubugin ng pagyakap dito ang seguridad na sibernetiko sa mga serbisyong pinansiyal, kaya gagawin nitong mas mapagkakatiwalaan at mas ligtas ang digital na banking sa ating mundong lalong nagkakaugnay.

Binuksan din ng pagsulpot ng FHE ang bagong posibilidad para sa ligtas at pribadong paggamit ng malalaking modelo ng wika. Sapagkat sa pagbibigay-kakayahan ng naka-encrypt na malalaking modelo ng wika, tinitiyak ng FHE na mananatiling lihim ang datos ng gumagamit habang ginagamit ang abanteng kakayahan ng mga modelong ito.

Papalapit na ang panahon ng quantum computing. At dapat maagap na tasahin ng mga bangko ang kanilang imprastruktura ng kriptograpiya, tukuyin ang mga posibleng butas, at bumuo ng malinaw na mapa para sa pagyakap sa FHE upang maipagsanggalang ang datos at mapanatili ang tiwala ng kliyente.

[00]: https://crypto.stanford.edu/craig/ "The original paper by Craig Gentry on Fully Homomorphic Encryption"
[01]: https://zama.ai/ "Zama - Fully Homomorphic Encryption"

[divider]: https://cloudcdn.pro/clients/common/images/elements/divider.svg "Divider"
[fhe]: https://cloudcdn.pro/stocks/diagrams/fhe_algorithm_diagram.webp "FHE Architecture"
