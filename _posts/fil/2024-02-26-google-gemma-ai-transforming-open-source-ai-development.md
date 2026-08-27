---
title: "Google Gemma: pagbabago sa pagbuo ng AI na bukas ang pinagmulan"
tags: "Gemma, Google, AI, open source, Technical, Enterprise, Integration, macOS, Data, Ethics, ISO 20022, post-quantum cryptography, Rust"
subtitle: "Ang Gemma 2B at 7B, ang pagsasanib sa Ollama sa macOS, at ang mga gamit nito sa negosyo mula chatbot hanggang katalinuhan sa kodigo."
description: "Ang Google Gemma: ang arkitektura ng mga modelong 2B at 7B, ang pagsasanay at lisensiya nito, isang patnubay sa pagpapatakbo nito nang lokal sa macOS gamit ang Ollama, at pitong gamit nito sa negosyo."
date: "Feb 26, 2024"
language: "fil-PH"
locale: "fil_PH"
banner: "https://cloudcdn.pro/stocks/images/ai-ship.webp"
banner_alt: "Google Gemma Logo - Source: Google"
keywords: "Google Gemma, AI na bukas ang pinagmulan, Gemma 2B, Gemma 7B, Ollama, macOS, malaking modelo ng wika, etikal na AI, NLP, chatbot, katalinuhan sa kodigo"
---
## Ang mapanimulang modelong AI ng Google na bukas ang pinagmulan para sa etikal at maaabot na pagbuo ng ML

Kamakailan ay inilunsad ng Google ang [**Gemma ⧉**][00], isang modelong AI na bukas ang pinagmulan na idinisenyo upang maghandog ng maaabot at etikal na saligan para sa pagbuo ng AI. At bilang modelong bukas ang pinagmulan, inihahandog ng Gemma ang buong arkitektura nito, ang pamamaraan ng pagsasanay nito, ang timbang ng modelo, at ang parametro nito sa ilalim ng mapagpahintulot na lisensiya, upang malayang maabot, matutuhan, mabuoan, at maiangkop pa nga ng mga panlabas na mananaliksik at developer ayon sa kanilang natatanging pangangailangan. Pinahihintulutan din ng malinaw na paraang ito ang pagsusuri sa gawi ng pagbuo ng Gemma upang masuportahan ang pananagutan.

Sa mga anyong tulad ng `Gemma 2B` at `7B`, sinasaklaw nito ang malawak na hanay ng aplikasyon, mula sa mga aparatong mobile hanggang sa imprastrukturang nasa ulap. At ipinamamalas ng pagpasok ng Gemma sa komunidad ng bukas na pinagmulan ang matatag na pangako ng Google sa etikal na AI, sapagkat pinatatatag nito ang inobasyon at pakikipagtulungan sa mga developer sa buong mundo.

Tinutuklas ng artikulong ito ang arkitektura ng Gemma, ang pagsasanib nito sa macOS, at ang potensiyal nitong baguhin ang mga solusyon sa negosyo at ang mas malawak na tanawin ng AI.

![Google Gemma Logo - Source: Google](https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/gemma.svg).class=\"fade-in w-25 p-5 float-end\"

## Pag-unawa sa Gemma

### Ang teknikal na arkitektura ng Gemma

Hinahango ng modelong Gemma ang inspirasyon nito sa arkitektura ng Google Gemini, at makukuha ito sa dalawang pangunahing anyo:

- Ang modelong **Gemma 2B** ay optimisado para sa kahusayan sa mismong aparato, na may mas maliit na bakas sa memorya at mas mababang pagkonsumo ng enerhiya. Kaya angkop na angkop ito sa mga aplikasyong mobile at nakapaloob tulad ng chatbot sa smartphone o ng mga aparato sa matalinong tahanan.

- Ang modelong **Gemma 7B** ay may higit na mataas na kapasidad, na inihanda para sa mas masalimuot na gawain tulad ng pagsusuri ng malalaking hanay ng datos at dokumento. Ang larangan nito ay ang mga sentro ng datos at ang imprastrukturang nasa ulap na nagpapatakbo ng inperensiya sa buong base ng datos.

Naghahandog ang dalawang modelo ng mga bloke ng gusaling AI na sari-sari ang gamit, mula sa personal na proyekto hanggang sa solusyon sa negosyo.

### Ang pagsasanay at kakayahan ng Gemma

Batay sa [**teknikal na ulat ⧉**][01], abante ang mga modelong Gemma (2B at 7B), at sinanay ang mga ito sa napakalaking hanay ng datos na nagbibigay-diin sa nilalaman sa web, sa matematika, at sa pagpoprograma. Ang mga modelong ito, hindi tulad ng hinalinhan nitong Gemini, ay hindi nagbibigay-prayoridad sa mga tampok na maraming wika o maraming anyo. At isinasanib ng mga ito ang masaklaw na talasalitaan at ginagamit nila ang mapanlikhang paraan ng tokenisation, kaya pinatatatag nito ang paghawak sa iba't ibang uri ng datos. At ang pag-aayos ng tagubilin sa mga ito, na pinagsasama ang superbisadong pagkatuto at ang pinatibay na pagkatuto mula sa puna ng tao, ay nakatuon lamang sa Ingles, sapagkat pinabubuti nito ang masusing pag-unawa at paglikha ng teksto. Binibigyang-diin ng mapanlikhang pamamaraang ito ang potensiyal ng mga ito sa mga espesyalisadong larangan, kaya itinatampok nito ang umuunlad na tanawin ng pagsasanay ng modelong pangwika.

### Ang Gemma at ang komunidad ng bukas na pinagmulan

Bilang paglabas na bukas ang pinagmulan sa ilalim ng [**mapagpahintulot na lisensiya ⧉**][03], kumakatawan din ang Gemma sa pangako ng Google na patatagin ang etikal na pakikipagtulungan sa AI. Kaya na ngayon ng mga panlabas na developer na bumuo sa ibabaw ng Gemma, suriin ito, at iangkop ito sa malinaw na paraan upang mapabilis ang pag-abot at matiyak ang pananagutan.

![divider][divider].class=\"m-10 w-100\"

![Ollama Logo - Source: Ollama](https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/ollama.svg).class=\"fade-in w-25 p-5 float-start\"

## Pagsasanib ng Google Gemma sa Ollama sa macOS

Ang [**Ollama ⧉**][02] ay interface na nagpapahintulot ng lokal na pagtuklas sa mga katulong na AI sa sistemang macOS. Gagamitin natin ito upang ihanda ang mga modelong Gemma 2B at 7B sa mga kompyuter ng Apple na serye M. Gagabayan ka ng patnubay na ito sa proseso ng pagsasanib ng Gemma sa Ollama sa macOS.

Magagamit mo ang utos na uname upang mailimbag ang arkitektura ng prosesor ng kompyuter. Buksan ang Terminal at patakbuhin:

```bash
uname -m
```

Kung `arm64` ang lumabas, mayroon kang Mac na serye M. At kung `x86_64` naman, mayroon kang Mac na Intel. Ang patnubay na ito ay para sa mga aparatong Mac na serye M.

### Paghahanda ng kapaligiran

#### 1. Tiyaking naka-install ang Python 3.8+, ang pip, at ang venv

Bago magsimula, tiyaking mayroong [**Python 3.8 ⧉**][04] o mas bago sa iyong Mac, kasama ang mga kasangkapang `pip` at `venv`. Masusuri mo ang bersiyon ng Python at ng pip at mapapa-upgrade mo ang pip sa pamamagitan ng pagpapatakbo ng sumusunod na utos sa Terminal:

```bash
python3 --version
pip3 --version
pip3 install --upgrade pip
```

#### 2. Lumikha ng birtuwal na kapaligiran upang maihiwalay ang mga dependency

Buksan ang Terminal at lumikha ng birtuwal na kapaligiran upang maiwasan ang salungatan sa mga pakete sa antas ng sistema.

```bash
python3 -m venv gemma_env
source gemma_env/bin/activate
```

#### 3. I-install ang pinakabagong bersiyon ng Ollama para sa macOS

I-download ang [**pinakabagong bersiyon ng Ollama ⧉**][05] para sa macOS mula sa opisyal na sayt. I-extract at ilipat ang aplikasyong Ollama sa folder na Applications. Buksan ito at sundin ang tagubilin sa paghahanda.

#### 4. Tiyaking matagumpay ang pag-install ng Ollama

Suriin kung tama ang pagkaka-install ng Ollama sa pamamagitan ng pagpapatakbo ng:

```bash
ollama --version
```

Dapat mong makita ang bersiyon ng Ollama na nakalimbag.

### Rekomendasyon para sa sistema

Para sa pinakamainam na bisa ng Gemma 2B, kakailanganin mo ang:

- **Prosesor**: Intel i5 na maraming núcleo o mas mataas
- **Memorya**: 16 GB na RAM (32 GB para sa Gemma 7B)
- **Imbakan**: 50 GB na bakante sa SSD
- **macOS**: napapanahon (Monterey o mas bago)

Sa naihandang Ollama, handa ka nang ihanda at makipag-ugnayan sa mga modelong Gemma nang lokal.

![divider][divider].class=\"m-10 w-100\"

## Paghahanda ng lokal na kopya ng Gemma

### 1. Pagpapatakbo ng modelong Gemma sa pamamagitan ng CLI ng Ollama

Piliin ang modelong Gemma na nais mong patakbuhin:

- Gemma 2B (mas maliit na modelo): `ollama run gemma:2b`
- Gemma 7B (mas malaking modelo): `ollama run gemma:7b`

### 2. Ida-download ng unang pagpapatakbo ang mga ari-arian ng modelo (maaaring tumagal)

Ida-download ng unang pagpapatakbo ang piniling modelong Gemma, at maaari itong tumagal nang kaunti. At sa sandaling matapos, maihahanda na ang Gemma para gamitin.

#### Halimbawa ng usapang tanong

```bash
>>> Hello Gemma. How are you today?
```

Tutugon ang Gemma ng sagot sa likas na wika.

```bash
>>> Hello Gemma. How are you today?
Hello! It's a lovely day to be alive. Thank you for asking. How are you doing today? 😊
```

### Pagpatay sa birtuwal na kapaligiran

```bash
deactivate
```

Ibabalik ka nito sa nakatakdang kapaligiran ng Python ng iyong sistema.

Para sa tulong sa paglutas ng suliranin o para sa karagdagang detalye hinggil sa paghahanda, sumangguni sa [Ollama Documentation ⧉](https://ollama.com/docs) at sa [Gemma Documentation ⧉](https://github.com/google-deepmind/gemma).

![divider][divider].class=\"m-10 w-100\"

## Ang epekto ng Gemma na bukas ang pinagmulan

Mula nang ilunsad ito, mabilis na pinabilis ng Gemma ang inobasyon salamat sa maaabot at kolaboratibo nitong paraang bukas ang pinagmulan.

Pinahihintulutan din ng mapagpahintulot na lisensiya ang pagsusuri sa mismong arkitektura ng Gemma para sa layuning pampananaliksik at ang paggawa ng napakadetalyadong pagbabago. At ibinahagi na ng mga developer ang kanilang pagbabago, pag-aangkop, at ganap na bagong kakayahan sa mga plataporma ng kolaborasyon sa software.

Patuloy na pinabubuti ng pagsisikap na ito ng komunidad ang kakayahan ng Gemma upang makabuo ng mga sistemang AI na etikal at responsable, na naaayon sa mga umuusbong na pinakamahusay na kasanayan.

At sa paglipas ng panahon, maaaring umusbong ang isang ekosistema ng kasangkapan, pagsasanib, at maging ng ganap na bagong aplikasyon para sa Gemma salamat sa kalikasan nito bilang plataporma na bukas ang pinagmulan.

![divider][divider].class=\"m-10 w-100\"

## Mga gamit ng Gemma para sa mga solusyon sa negosyo

Naghahandog ang modelong AI ng Google na Gemma ng iba't ibang solusyon sa negosyo sa pamamagitan ng teknikal nitong arkitektura at ng kalikasan nitong bukas ang pinagmulan, upang matugunan ang tiyak na pangangailangan ng negosyo.

### 1. Mga chatbot at katulong na pang-usap

Ang mas maliit na modelong Gemma 2B ay optimisado para sa kahusayan sa mismong aparato, kaya angkop na angkop ito sa pagbuo ng **chatbot** at ng **birtuwal na katulong**. Kayang ilunsad ng mga organisasyon ang mga katulong na pinapagana ng AI na ito sa mga aparatong mobile o sa mga nakapaloob na sistema upang mapatatag ang serbisyo sa kliyente, ang suporta, at ang pag-akit nang hindi nangangailangan ng malawak na mapagkukunang pangkalkulasyon.

At bagaman kalalabas pa lamang ng Gemma, naaayon nang mabuti ang kakayahan nito sa umiiral nang aplikasyon ng chatbot at ng birtuwal na katulong na tumutulong sa mga kliyente. At habang gumugulang ang Gemma, inaasahan nating makakita ng tuwirang pagsasanib na magbibigay-daan sa mga interface na pang-usap ng susunod na henerasyon.

### 2. Pagsusuri ng datos at kabatiran

Ang mas malaking modelong Gemma 7B, sa mas mataas nitong kapasidad para sa masasalimuot na gawain, ay angkop na angkop sa pagsusuri ng malalaking hanay ng datos at dokumento. Magagamit ng mga organisasyon ang modelong ito upang kumuha ng kabatiran, uso, at huwaran mula sa napakaraming datos, kaya nakatutulong ito sa proseso ng paggawa ng pasya at sa estratehikong pagpaplano.

### 3. Paglikha at pagbubuod ng nilalaman

Kayang tumulong ng mga modelong Gemma sa paglikha at pagbubuod ng nilalaman, tulad ng ulat, artikulo, at materyal sa marketing. Malaki ang maibababa ng kakayahang ito sa panahon at pagod na kailangan upang makalikha ng mataas ang kalidad na nilalaman, kaya pinahihintulutan nito ang mga negosyo na tumuon sa pagkamalikhain at estratehiya.

### 4. Naaangkop na elektronikong marketing at pagtutok ng anunsiyo

Sa pag-unawa at paglikha nito ng likas na wika, kayang tulungan ng Gemma ang mga organisasyon na makalikha ng mas naaangkop at mas mabisang kampanya sa elektronikong marketing at estratehiya sa pagtutok ng anunsiyo. Maaaring humantong ang gamit na ito sa pinabuting pag-akit sa kliyente at sa mas mataas na antas ng conversion.

### 5. Pagproseso ng likas na wika (NLP) para sa mga aparato sa gilid

Ginagawa ng optimisasyon ng Gemma na angkop ang modelo para patakbuhin ang mga gawaing NLP nang tuwiran sa mga aparato sa gilid. Pinahihintulutan ng kakayahang ito ang paggawa ng pasya sa negosyo sa tunay na oras at ang mas maayos na pagsasanib sa tunay na mundo, gaya ng sa mga aplikasyon sa tingian, sa pagmamanupaktura, at sa internet ng mga bagay.

### 6. Katalinuhan sa kodigo para sa mga developer

Kayang patatagin ng Gemma ang produktibidad ng developer sa pamamagitan ng paghahandog ng interface sa likas na wika para sa gawain sa pag-edit ng kodigo at sa pagbuo. Halimbawa, magagamit ng mga developer ang usapang tanong upang makakuha ng rekomendasyon ng kodigo, ng paglalarawan ng punsiyon, ng tulong sa pagwawasto, at ng pagsusuri ng kodigo. At susuriin ng Gemma ang konteksto at ang kahulugan upang maghandog ng angkop na mungkahi. At kayang tumulong ng "kapareha sa pagpoprogramang AI" na ito na pasimplehin ang daloy ng trabaho, bawasan ang pagkakamali, at pabilisin ang pagbuo ng mga produktong pinapagana ng AI.

### 7. Mga aplikasyong maraming anyo

Sa kakayahan nitong magproseso ng impormasyon sa larangan ng teksto, tunog, at paningin, nagiging sari-sari ang gamit ng Gemma para sa mga gamit na maraming anyo. Partikular na kapaki-pakinabang ang tampok na ito para sa mga aplikasyong nangangailangan ng pakikipag-ugnayan sa mga gumagamit sa mas likas at mas maayos na paraan, tulad ng karanasan sa birtuwal na realidad (VR) at sa pinatatatag na realidad (AR).

Ginagawang mahalagang kasangkapan ng kalikasan ng Gemma na bukas ang pinagmulan at ng teknikal nitong sari-saring gamit ito para sa mga organisasyong naghahangad gamitin ang AI sa kanilang pangangailangan sa operasyon. Magaling ang Gemma sa paglikha ng birtuwal na katulong at ng chatbot na nagpapatatag ng karanasan ng kliyente, at kaya nitong hawakan ang malaking dami ng pagsusuri ng datos. At hinihikayat din ng modelo nitong bukas ang pinagmulan ang inobasyon at pakikipagtulungan, kaya pinahihintulutan nito ang mga organisasyon na iangkop ang Gemma upang matugunan ang kanilang pangangailangan.

![divider][divider].class=\"m-10 w-100\"

## Ano ang naghihintay sa hinaharap?

Sa pagtingin sa darating, nakatayo ang Gemma sa bingit ng karagdagang paglago at pagpapaunlad. May mga pagsisikap upang mapatatag ang pagkakatugma nito sa iba't ibang kapaligiran ng kagamitan, mapatatag ang suporta sa karagdagang wika, at mapalawak ang saklaw ng aplikasyon nito. At itinatakda ng Google at ng Gemma ang layunin nilang tugunan ang mga hamon kaugnay ng katumpakan, ng pagtuklas ng kiling, at ng ligtas na paggamit ng datos, kaya inilalagay nila ang Gemma bilang lider sa etikal na pagbuo ng AI.

![divider][divider].class=\"m-10 w-100\"

## Pangwakas

Itinuturing na mapagpasyang sandali sa larangan ng AI ang paglulunsad ng Gemma, sapagkat binibigyang-liwanag nito ang paglipat tungo sa mas maaabot, mas etikal, at mas kolaboratibong gawi ng pagbuo. At habang patuloy itong umuunlad, naghahanda ang Gemma na gumanap ng mahalagang papel sa paghubog ng kinabukasan ng AI, sapagkat naghahandog ito ng balangkas kung paano maitutulak ng mga proyektong bukas ang pinagmulan ang inobasyon habang sumusunod sa etikal na pamantayan.

[00]: https://ai.google.dev/gemma "Google Gemma AI"
[01]: https://storage.googleapis.com/deepmind-media/gemma/gemma-report.pdf "Gemma Technical Report"
[02]: https://ollama.com "Ollama"
[03]: https://ai.google.dev/gemma/terms "Gemma Licensing"
[04]: https://www.python.org/downloads/release/python-380/ "Python 3.8"
[05]: https://ollama.com/download "Ollama Download"

[divider]: https://cloudcdn.pro/clients/common/images/elements/divider.svg "Divider"
