---
title: "Mabilis na pagkilala sa pananalita sa tunay na oras sa macOS gamit ang OpenAI Whisper"
tags: "OpenAI, Whisper, Metal, macOS, Speech, Real-Time, Transcription, GPU, Python, Silicon, ISO 20022, post-quantum cryptography, AI, open source, DORA, platform engineering, sovereign cloud, cloud native banking"
subtitle: "Ang OpenAI Whisper na pinabilis ng Metal Performance Shaders: 8 hanggang 12 beses na mas mabilis kaysa sa tunay na oras, sa mismong aparato."
description: "Ang pagsasanib ng OpenAI Whisper at ng Metal Performance Shaders sa macOS: pagsusulat na 8 hanggang 12 beses na mas mabilis kaysa sa tunay na oras, pagproseso sa mismong aparato para sa pagkapribado, at pagtuklas ng aktibidad ng tinig na 94% ang katumpakan."
date: "Mar 12, 2024"
language: "fil-PH"
locale: "fil_PH"
banner: "https://cloudcdn.pro/stocks/images/research-paper.webp"
banner_alt: "Malikhaing paglalarawan hinggil sa pagkilala sa pananalita sa macOS"
keywords: "OpenAI Whisper, Metal Performance Shaders, MPS, macOS, pagkilala sa pananalita, ASR, tunay na oras, Apple Silicon, GPU, pagproseso sa aparato, pagkapribado"
---
## Mabilis na pagkilala sa pananalita sa tunay na oras sa macOS gamit ang OpenAI Whisper

Naghahandog ang artikulong ito ng pangkalahatang tanaw sa isang [**papel ng pananaliksik**][00] na tumutuklas sa pagsasanib ng OpenAI Whisper at ng Metal Performance Shaders (MPS) sa macOS, at naghahain ito ng bagong paraan para sa pagkilala sa pananalita sa tunay na oras. At ang OpenAI Whisper ay abanteng modelo ng awtomatikong pagkilala sa pananalita (ASR) na sinanay sa malawak at sari-saring hanay ng datos na tunog, at kaya nitong isulat ang pananalita sa maraming wika. At binibigyang-kakayahan ng pagsasama ng abanteng arkitektura ng neural network ng Whisper at ng pagpapabilis ng yunit ng pagproseso ng grapika na inihahandog ng MPS ang pagpapabuti ng bilis at katumpakan sa pagproseso ng pananalita sa mismong aparato, kaya pinatatatag nito ang pagkapribado at ginhawa ng gumagamit, at sabay nitong binubuksan ang bagong posibilidad para sa mga developer na isanib ang kakayahan sa pagsasalin ng pananalita tungo sa teksto sa tunay na oras nang tuwiran sa mga aplikasyong macOS.

## Panimula

Gumaganap ang teknolohiya ng pagkilala sa pananalita ng mapagpasyang papel sa pagpapadali ng malawak na hanay ng aplikasyon, mula sa pagpapatibay ng pagiging accessible hanggang sa pagpapasimple ng pakikipag-ugnayan ng gumagamit. At ang paghahanap ng ASR na mataas ang katumpakan at mababa ang pagkaantala ay dating eksklusibo sa malalakas na serber sa ulap, kaya nagdulot ito ng hamon sa dako ng pag-abot, pagkapribado, at pagkaantala. Gayunman, naghandog ang mga kamakailang pananaliksik ng mapagbagong solusyon: ang pagsasanib ng OpenAI Whisper at ng pagpapabilis ng yunit ng pagproseso ng grapika na inihahandog ng Metal Performance Shaders (MPS) sa macOS. At kumakatawan ang pagsasanib na ito sa kapansin-pansing pagsulong sa kakayahan ng pagkilala sa pananalita sa mismong aparato, at naaayon ito sa lumalaking pagtuon sa pagkapribado ng gumagamit at sa seguridad ng datos.

Ang [**Metal Performance Shaders (MPS)**][01] ay teknolohiyang binuo ng Apple na nagpapahintulot ng mataas ang bisang pagkalkula sa pamamagitan ng yunit ng pagproseso ng grapika sa mga aparatong macOS. Pinahihintulutan nito ang mga developer na gamitin ang lakas ng yunit ng pagproseso ng grapika para sa kaparalelong pagproseso, kaya nagbubunga ito ng malaking pagbuti sa bilis sa iba't ibang gawaing pangkalkulasyon, kabilang na ang machine learning at ang biswal na pagkilala ng kompyuter.

![divider][divider].class=\"m-10 w-100\"

### 1. Ang ebolusyon ng pagkilala sa pananalita sa macOS

Nakasalalay ang ebolusyon ng teknolohiya ng pagkilala sa pananalita sa mga aparatong macOS sa pagsulong ng mga modelo ng neural network at ng teknik sa pagpapabilis sa pamamagitan ng kagamitan. At ang tradisyunal na sistema ng pagkilala sa pananalita ay madalas humaharap sa hamon sa katumpakan, sa pagkaantala, at sa kahusayang pangkalkulasyon, lalo na kapag humaharap sa iba't ibang punto, sa ingay sa likuran, at sa nagbabagong kalagayan ng pagtatala. At naglatag ang pagsulpot ng OpenAI Whisper ng bagong sanggunian para sa matatag at tumpak na pagkilala sa pananalita sa malawak na hanay ng wika at diyalekto, kaya naghandog ito ng angkop na solusyon para sa mga agarang aplikasyon.

![divider][divider].class=\"m-10 w-100\"

### 2. Paggamit ng OpenAI Whisper at ng Metal Performance Shaders

Ibinubunyag ng papel ng pananaliksik ang mapanlikhang paraang pinagsasama ang abanteng kakayahan ng OpenAI Whisper at ang mataas ang bisang pagkalkula ng MPS sa macOS. At nakakamit ang pagsasanib na ito sa pamamagitan ng pagpapabuti ng modelong Whisper upang gumana ito sa yunit ng pagproseso ng grapika gamit ang balangkas na MPS, na nagbibigay-kakayahan ng mabisang kaparalelong pagproseso. At ginamit ng mga mananaliksik ang mga teknik tulad ng kuwantisasyon at pagpupungos ng modelo upang mabawasan ang laki ng modelo at ang kahingiang pangkalkulasyon nito habang pinananatili ang mataas na katumpakan. At sa paggamit ng kakayahan sa kaparalelong pagproseso ng yunit ng pagproseso ng grapika, nakakamit ng sistema ang kapansin-pansing pagbuti sa bilis, na may bilis ng pagsusulat na mas mabilis kaysa sa tunay na oras nang mga 8 hanggang 12 beses para sa karaniwang pagbigkas. At pinabubuti nito ang karanasan ng gumagamit sa pamamagitan ng pagbabawas ng oras ng paghihintay, at pinahihintulutan nito ang mas malawak na hanay ng aplikasyon sa tunay na oras, mula sa buhay na pagsasalin hanggang sa mga interaktibong sistemang pinapatnubayan ng tinig.

![divider][divider].class=\"m-10 w-100\"

### 3. Ang kahihinatnan para sa mga gumagamit at developer

May mahalagang kahihinatnan ang pagsasanib ng Whisper at ng MPS sa macOS para sa mga huling gumagamit at para sa mga developer ng aplikasyon nang sabay. Para sa mga gumagamit, naghahandog ito ng pinabuting karanasan sa pagkilala sa pananalita sa tunay na oras, sapagkat naghahandog ito ng halos agarang pagsusulat na may mataas na katumpakan habang pinananatili ang pagkapribado at seguridad ng pagproseso sa mismong aparato. At maaaring gamitin ang teknolohiyang ito sa iba't ibang senaryo sa tunay na buhay, tulad ng mga aplikasyon ng kontrol sa pamamagitan ng tinig para sa matatalinong tahanan, ng serbisyo ng pagsusulat sa tunay na oras para sa pulong at panayam, at ng tampok sa pagiging accessible para sa mga gumagamit na may kapansanan sa pandinig. At nakakakuha ang mga developer ng kasangkapan upang maisanib ang punsiyon ng pagsasalin ng pananalita tungo sa teksto sa kanilang aplikasyon, na may karagdagang pakinabang mula sa kahusayan sa enerhiya at sa maayos na pagsasanib sa Python.

![divider][divider].class=\"m-10 w-100\"

### 4. Pagpapasigla ng pagyakap at inobasyon

Pinadadali ng modular na balangkas at ng pagpapatupad ng sistema sa Python ang pagsasanib sa umiiral nang aplikasyon at binabawasan nito ang hadlang sa pagpasok para sa mga developer na nais isama ang kakayahan sa pagkilala sa pananalita. Gayunman, maaaring humarap ang mga developer sa hamon sa pag-aangkop ng modelo at sa pagbagay nito sa tiyak na gamit, gayundin sa pagpapabuti ng bisa para sa iba't ibang anyo ng kagamitan. At naghahandog ang papel ng pananaliksik ng gabay upang matugunan ang mga hamong ito, tulad ng maingat na pag-aayos ng modelo sa datos na tiyak sa larangan at ng pagpapatupad ng estratehiya sa dinamikong paglalaan ng mapagkukunan. Bukod dito, tinitiyak ng sistemang nagtitipid ng enerhiya sa pagtuklas ng aktibidad ng tinig, na nakakamit ang katumpakang 94% at pagbawi na 96%, na mananatiling mabilis tumugon at tumpak ang mga aplikasyon nang hindi inuubos ang mapagkukunan ng aparato. At taglay ng kombinasyong ito ng tampok ang potensiyal na pasiglahin ang pagyakap ng mga developer at pukawin ang higit pang inobasyon sa larangan ng pagkilala sa pananalita sa tunay na oras.

![divider][divider].class=\"m-10 w-100\"

## Pangwakas

Kumakatawan ang pagsasanib ng OpenAI Whisper at ng Metal Performance Shaders sa macOS sa kapansin-pansing pagsulong sa teknolohiya ng pagkilala sa pananalita sa tunay na oras. At sa paghahandog ng pinabuting bilis, katumpakan, at kahusayan, pinatatatag ng inobasyong ito ang karanasan ng gumagamit at binubuksan nito ang bagong posibilidad para sa pagbuo ng aplikasyon. At nag-aambag ang pananaliksik na ito sa patuloy na pagsulong ng mga teknolohiyang AI, at taglay nito ang kakayahang magbigay-inspirasyon sa karagdagang pag-unlad sa pagproseso ng pananalita sa mismong aparato sa iba't ibang plataporma. At habang patuloy na umuunlad ang teknolohiyang ito, taglay nito ang kakayahang baguhin kung paano nakikipag-ugnayan ang mga gumagamit sa kanilang aparato, kaya ginagawa nitong mas maayos at mas maaabot ang digital na komunikasyon.

### Pag-abot sa papel ng pananaliksik

.class=\"card bg-light p-3 me-3 w-100\"
Upang matuto pa hinggil sa pagsasanib ng OpenAI Whisper at ng Metal Performance Shaders sa macOS para sa pagkilala sa pananalita sa tunay na oras, hinihikayat ang mga mambabasa na abutin ang buong papel ng pananaliksik. Naghahandog ang papel ng malalim na teknikal na detalye, ng resulta ng eksperimento, at ng karagdagang kabatiran hinggil sa posibleng aplikasyon at sa mga direksiyon sa hinaharap ng teknolohiyang ito. At sa pag-abot sa buong papel ng pananaliksik, makakakuha ang mga mambabasa ng masaklaw na pag-unawa sa pamamaraan, sa pagpapatupad, at sa kahihinatnan ng mapanlikhang paraang ito sa pagkilala sa pananalita sa tunay na oras sa mga aparatong macOS. [**Basahin ang buong papel ngayon! ❯**][00]

[00]: /papers/index.html "Mga publikasyon ng pananaliksik at puting papel mula kay Sebastien Rousseau"
[01]: https://developer.apple.com/documentation/metalperformanceshaders "Metal Performance Shaders - Apple Developer Documentation"

[divider]: https://cloudcdn.pro/clients/common/images/elements/divider.svg "Divider"
