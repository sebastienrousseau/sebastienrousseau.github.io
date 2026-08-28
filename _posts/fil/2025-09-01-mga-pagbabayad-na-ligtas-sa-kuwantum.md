---
title: "Mga pagbabayad na ligtas sa kuwantum: bakit dapat kumilos na ang industriya"
tags: "quantum-safe payments, post-quantum cryptography, payments, EPAA, ISO 20022, SWIFT, SEPA, DORA, quantum computing, AI, cross-border payments, stablecoins"
subtitle: "Ang panganib ng anihin-ngayon-i-decrypt-mamaya sa SWIFT, SEPA at FedNow — at ang gawain ng pangkat ng EPAA."
description: "Ang bantang kuwantum sa imprastruktura ng pagbabayad: ang panganib ng harvest-now decrypt-later, ang epekto sa SWIFT, SEPA, FedNow at ISO 20022, ang pamantayang FIPS 203/204/205 ng NIST, at ang puting papel ng EPAA."
date: "September 01, 2025"
language: "fil-PH"
locale: "fil_PH"
banner: "https://cloudcdn.pro/stocks/images/digital-nodes.webp"
banner_alt: "Malikhaing paglalarawan hinggil sa mga pagbabayad na ligtas sa kuwantum"
keywords: "mga pagbabayad na ligtas sa kuwantum, EPAA, harvest-now decrypt-later, HNDL, SWIFT, SEPA, FedNow, ISO 20022, NIST, FIPS 203, ML-KEM, ML-DSA, DORA, MAS, APRA"
---
## Ang bantang kuwantum sa mga sistema ng pagbabayad

Nakasalalay ang makabagong imprastruktura ng pagbabayad sa encryption sa pamamagitan ng pampublikong susi — RSA, ECC at Diffie-Hellman — sa pagpapatunay ng transaksiyon, sa pagsanggalang ng datos ng may hawak ng kard, at sa pagtiyak ng seguridad ng palitan ng mensahe sa pagitan ng mga institusyong pinansiyal. Bumubuo ang mga algoritmong ito ng saligang kinatatayuan ng SWIFT, ng SEPA, at ng mga sistema ng kabuuang pag-aayos sa tunay na oras, at ng halos bawat umiiral na scheme ng kard ngayon.

Ang mga quantum na kompyuter na nagpapatakbo ng algoritmo ni Shor ay magiging kayang basagin ang mga primitibong kriptograpikong ito. At bagaman hindi pa makukuha ang mga makinang kuwantum na matiisin sa pagkakamali sa kinakailangang laki, ginagawa ng landas ng pag-unlad ng kagamitan — gaya ng pinatunayan ng IBM, ng Google, at ng iba pa — na usapin ito ng iskedyul sa inhinyeriya at hindi ng teoriya. At kinumpleto ng National Institute of Standards and Technology (NIST) ang unang hanay ng pamantayan ng kriptograpiyang post-quantum (FIPS 203, 204 at 205) bilang tugon dito.

## Ang panganib ng "anihin ngayon, i-decrypt mamaya"

Hindi limitado ang banta sa isang petsa sa hinaharap kung kailan magiging sapat na ang kakayahan ng mga quantum na kompyuter. Sapagkat sinasalo at iniimbak ng mga aktor sa antas ng estado at ng mga sopistikadong kalaban ang naka-encrypt na datos ngayon, na may layuning basagin ito sa sandaling maging makukuha ang mapagkukunang kuwantum. At ang estratehiyang ito na kilala bilang harvest-now decrypt-later (HNDL) ay nangangahulugang anumang datos ng pagbabayad na may pangmatagalang sensitibidad — ang talaang pangregulasyon, ang arkibo ng pagsunod, ang obligasyong pangkontrata — ay nasa panganib na.

Sinimulan nang tumugon ng mga tagapagregula sa pinansiya. Naglabas ang Monetary Authority of Singapore (MAS) ng gabay hinggil sa kahandaang kuwantum. At tinukoy ng Australian Prudential Regulation Authority (APRA) ang panganib na kriptograpiko sa loob ng balangkas nito ng teknikal na katatagan. At ipinapataw ng Digital Operational Resilience Act (DORA) ng Unyong Europeo ang pangangasiwa ng panganib sa teknolohiya ng impormasyon at komunikasyon na isinasaalang-alang ang mga umuusbong na banta, kabilang na ang quantum computing.

## Ang epekto sa buong daluyan ng pagbabayad

Umaabot ang kahihinatnan sa buong lawak ng imprastruktura ng pagbabayad:

**Ang mensaherong SWIFT:** nakasalalay ang anyo ng mensaheng MT at MX sa TLS at sa digital na lagda upang matiyak ang integridad at ang pagpapatunay. At anumang paglabag sa balangkas ng susi ay nagpapahina sa modelo ng tiwalang nag-uugnay sa mahigit 11,000 institusyon sa buong mundo.

**Ang SEPA at ang mga agarang pagbabayad:** pinoproseso ng sistemang SEPA Instant Credit Transfer ng European Payments Council ang mga transaksiyong hindi na maaaring bawiin sa loob ng wala pang sampung segundo. At ang paglabag na kriptograpiko sa ganitong bilis ay hindi nag-iiwan ng anumang bintana para sa pakikialam ng tao o para sa mano-manong pagsusuri.

**Ang mga sistema ng agarang pagbabayad:** ang Faster Payments (Reyno Unido), ang FedNow (Estados Unidos) at ang NPP (Australya) ay lahat magkakasaluhan sa pagsalalay sa klasikong primitibong kriptograpiko para sa pagpapatunay ng mensahe at para sa pagsusuri ng kalahok.

**Ang pagsunod at ang datos na mahaba ang buhay:** ang talaan ng pagbabayad na iniingatan para sa layuning pangregulasyon — madalas na sapilitan sa loob ng lima hanggang sampung taon o higit pa — ay mabubuhay nang mas matagal kaysa sa katiyakan ng seguridad na inihahandog ng encryption na nagsanggalang sa mga ito noong sandaling nalikha ang mga ito. At dapat isaalang-alang ng programa ng paglipat tungo sa [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) ang kriptograpikong haba ng buhay ng datos na nililikha ng mga ito.

**Ang blockchain at ang teknolohiya ng ipinamahaging talaan:** humaharap ang mga plataporma ng digital na ari-arian at ang mga kasangkapan sa tokenisadong pagbabayad na nakasalalay sa kriptograpiya ng elliptic curve sa tuwiran at mahusay-nang-nauunawaang banta mula sa mga algoritmong kuwantum.

## Ano ang dapat gawin ngayon ng mga institusyon

Ang paglipat tungo sa kriptograpiyang lumalaban sa quantum computing ay hindi iisang pag-upgrade kundi programang tumatagal ng maraming taon na nangangailangan ng maayos na paghahanda:

**Ang imbentaryong kriptograpiko:** dapat ikatalogo ng mga institusyon ang bawat sistema, protokol, at imbakan ng datos na nakasalalay sa klasikong encryption sa pamamagitan ng pampublikong susi. At kabilang dito ang sertipikong TLS, ang pagpapatunay ng interface sa pagpoprograma ng aplikasyon, ang anyo ng HSM, ang sistema ng pangangasiwa ng susi, at ang encryption ng datos na nakahimpil.

**Ang pagyakap sa algoritmong post-quantum:** naglabas ang NIST ng pamantayan para sa ML-KEM (FIPS 203) para sa pagbabalot ng susi, at para sa ML-DSA (FIPS 204) para sa digital na lagda. At dapat simulan ng mga institusyon ang pagsubok sa mga algoritmong ito sa kapaligirang hindi pamproduksiyon at ang pagbuo ng mapa ng paglipat sa mahahalagang sistema.

**Ang kakayahang umangkop na kriptograpiko:** dapat idisenyo ang mga sistema — o muling ayusin ang balangkas ng mga ito — upang maaaring mapalitan ang algoritmong kriptograpiko nang hindi nangangailangan ng ganap na muling pagdidisenyo ng aplikasyon. At nalalapat ang prinsipyong ito sa tarangkahan ng pagbabayad, sa gitnang software para sa palitan ng mensahe, at sa interface sa pagpoprograma ng aplikasyon na nakaharap sa kliyente nang pantay-pantay.

**Ang mga hibridong paraan:** sa panahon ng transisyon, naghahandog ng malalim na depensa ang mga hibridong balangkas na kriptograpikong pinagsasama ang klasiko at ang post-quantum na algoritmo. At pinananatili ng paraang ito ang pabalik na pagkakatugma habang ipinapasok ang paglaban sa kuwantum.

## Ang pangkat na tagapagtrabaho ng EPAA at ang pakikipagtulungan sa industriya

Nagtatag ang Emerging Payments Association Asia (EPAA) ng pangkat na tagapagtrabaho sa Quantum Safe Cryptography upang tugunan ang mga hamong ito sa pamamagitan ng magkakaugnay na gawain sa industriya. At tinitipon ng pangkat ang mga kalahok mula sa buong ekosistema ng pagbabayad, kabilang na ang IBM, ang HSBC, ang KPMG, ang JPMorgan Chase, ang PayPal, at iba pa.

Sa pamamagitan ng mga workshop na ginanap sa Sydney, Hong Kong at Singapore, bumuo ang pangkat na tagapagtrabaho ng magkakabahaging balangkas upang tasahin ang panganib na kuwantum sa mga sistema ng pagbabayad at upang tukuyin ang praktikal na landas ng paglipat. At kumakatawan ang nabuong puting papel — [Quantum-Safe Payments: Why the Payments Industry Must Act Now][epaa] — sa posisyong pinagkasunduan hinggil sa pagkaapurahan at laki ng hamong ito.

Ipinapasya ng pagsusuri ng pangkat na tagapagtrabaho na ang kahandaang lumaban sa quantum computing ay pasyang may kinalaman sa kasalukuyang imprastruktura, at hindi sa imprastruktura sa hinaharap. At ang mga institusyong nag-aatubili ay nanganganib na hindi matugunan ang inaasahan ng regulasyon, o hindi maipagsanggalang ang datos na mahaba ang buhay, o hindi mapanatili ang interoperabilidad sa mga katuwang na nauna nang lumipat.

## Tungkol sa may-akda

Si Sebastien Rousseau ay Senior Digital Product Manager sa HSBC Bank plc, kung saan pinamumunuan niya ang mga produktong interface sa pagpoprograma ng aplikasyon para sa pagbabayad ng negosyo sa loob ng Commercial & Investment Bank ng HSBC. Nag-ambag siya sa EPAA Quantum Safe Cryptography Working Group at sinasaliksik niya ang paggamit ng kriptograpiyang post-quantum sa mga serbisyong pinansiyal. [Magbasa pa hinggil kay Sebastien ❯][00]

## Mga kaugnay na artikulo

- [[Ang quantum na pamamahagi ng susi](/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html): pagbabago sa seguridad ng mga bangko][rel1]
- [[CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html): ang algoritmong nagsasanggalang sa panahong kuwantum][rel2]

[00]: /about/index.html "Tungkol kay Sebastien Rousseau"
[epaa]: https://emergingpaymentsasia.org/wp-content/uploads/2025/09/Quantum-Safe-Payments-Why-the-Payments-Industry-Must-Act-Now.pdf "Ang puting papel ng EPAA Quantum-Safe Payments"
[rel1]: /2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html "Quantum Key Distribution: Revolutionising Security in Banking"
[rel2]: /2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html "CRYSTALS-Kyber: The Safeguarding Algorithm in a Quantum Age"
