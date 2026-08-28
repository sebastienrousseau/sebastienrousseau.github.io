---
title: "Ciyar da AI gaba da LLM multimodal: darussa daga MM1"
tags: "Multimodal, LLM, AI, MM1, pre-training, gane hoto, NLP, gaba, learning, bincike, ISO 20022, post-quantum cryptography, quantum computing"
subtitle: "Yadda binciken MM1 na Apple ke bayyana gine-gine, bayanan pre-training, da ikon multimodal"
description: "Nazari kan binciken MM1 na Apple: LLM multimodal, gine-gine, dabarun pre-training, ingancin hoto, da ikon few-shot."
date: "March 18, 2024"
language: "ha-NG"
locale: "ha_NG"
banner: "https://cloudcdn.pro/stocks/images/mm1-visual.webp"
banner_alt: "Tutar Apple MM1"
keywords: "LLM multimodal, binciken MM1, ci gaban AI, dabarun pre-training, gane hoto, sarrafa harshe na halitta, aikace-aikacen AI, makomar AI, multimodal learning, binciken AI"
---

![Tutar Apple MM1](https://cloudcdn.pro/stocks/images/mm1-visual.webp).class="img-fluid clearfix"

<!-- lead-start -->
<aside class="post-lead" aria-label="Taƙaitaccen labari">
<p class="post-lead-tldr"><strong>Takaitawa.</strong> MM1 ya nuna yadda Apple ya gina model da ke haɗa fahimtar hoto da harshe. Darasin injiniya shi ne: cakuda bayanai, resolution na hoto, image encoder, da vision-language connector su ne ke ɗaukar nauyin inganci.</p>
<p class="post-lead-heading"><strong>Mahimman darussa</strong></p>
<ul class="post-lead-takeaways">
  <li><strong>Multimodal AI ya zama batun gine-gine.</strong> Model ba zai tsaya kan rubutu kawai ba; dole ya haɗa hoto, harshe, da mahalli.</li>
  <li><strong>MM1 ya nuna muhimmancin cakuda data.</strong> Image-caption, interleaved image-text, da text-only data suna aiki tare.</li>
  <li><strong>Resolution na hoto yana da nauyi.</strong> Kyakkyawan visual input na iya fi ƙarin parameters tasiri.</li>
  <li><strong>Vision-language connector shi ne gada.</strong> Cross-attention da multi-head attention suna mayar da visual features zuwa amfani ga language model.</li>
</ul>
<p class="post-lead-related"><strong>Karin karatu:</strong> <a href="https://sebastienrousseau.com/2023-11-12-exploring-generative-ai/index.html">Generative AI a 2023: yadda yake aiki da inda ake amfani da shi</a>, <a href="https://sebastienrousseau.com/2026-05-11-lucy-besson-knowledge-transfer-ai-quantum/index.html">Lucy’s Flash Drive: AI, quantum da ilimi</a>, <a href="https://sebastienrousseau.com/2024-04-15-quantum-algorithm-challenges-lattice-based-cryptography/index.html">Quantum algorithm da lattice cryptography</a>.</p>
</aside>
<!-- lead-end -->

## Gabatarwa

Haɗin sarrafa harshe na halitta da gane hoto ya samar da LLM multimodal. A paper ɗin MM1, Apple ya gabatar da jerin model na AI da ke haɗa fahimtar gani da fahimtar harshe. Binciken ya gwada zaɓin architecture, cakuda pre-training data, da abubuwan da ke ƙayyade performance.

Muhimmancin MM1 ba wai demo ba ne. Muhimmancinsa shi ne ya nuna wane ɓangare na tsarin model ne ke da tasiri, yadda ake shirya data, da wane trade-off injiniya ya kamata a auna.

![divider][divider].class=\"m-10 w-100\"

## Tasowar AI multimodal

AI ya ci gaba a manyan hanyoyi biyu: fahimtar harshe da fahimtar hoto. LLM sun sauya yadda machine ke fahimta da rubuta harshe. Computer vision kuma ya inganta yadda machine ke fitar da ma’ana daga hoto. LLM multimodal yana haɗa waɗannan abubuwa biyu domin model ya yi aiki da rubutu da hoto a lokaci guda.

Wannan ya buɗe hanya ga assistants masu fahimtar allo, nazarin takardu, kayan koyarwa, visual search, da ƙirƙirar abun multimedia. Amma matsalar ba wai karɓar hoto kawai ba ce. Matsalar ita ce haɗa visual representation da language model cikin hanyar da za ta ba da sakamako mai ma’ana.

![divider][divider].class=\"m-10 w-100\"

## Binciken MM1: muhimmin mataki a AI multimodal

Binciken [**MM1: Methods Analysis & Insights from Multimodal LLM Pre-training ⧉**][00] ya zama muhimmin abin dubawa wajen fahimtar MLLM pre-training. Masu binciken Apple sun gwada image encoder, vision-language connector, image resolution, da data composition.

### Hanya da manufofi

MM1 ya yi amfani da gwaji mai tsauri. Masu binciken sun gwada architecture daban-daban da cakuda data daban-daban, sannan suka auna tasirinsu kan few-shot learning. Wannan yana da muhimmanci saboda a amfani na zahiri ba koyaushe ake da manyan labelled examples ba.

Manufar ita ce gano design da zai ba model damar koyo daga ƙaramin misali, ya tsaya daidai, kuma ya haɗa visual context da umarnin harshe.

![divider][divider].class=\"m-10 w-100\"

## Sakamako da darussa

Darasi na farko shi ne data mix yana da muhimmanci. Haɗa image-caption data, interleaved image-text data, da text-only data ya ba da sakamako mafi kyau. Model yana bukatar nau’in data daban-daban domin ya koyi alaƙa tsakanin abu a hoto, mahallin takarda, da umarnin harshe.

Darasi na biyu shi ne scale ba parameter count kawai ba ne. MM1 ya gwada dense models har zuwa 30B parameters da mixture-of-experts variants. Amma binciken ya nuna image resolution na iya yin tasiri fiye da girman model. A multimodal AI, ingancin visual input wani ɓangare ne na performance.

Image encoder ma yana da nauyi. ResNet ko ViT suna shafar yadda model ke fitar da visual features. Vision-language connector kuma yana haɗa features ɗin da language model domin su zama context mai amfani.

![divider][divider].class=\"m-10 w-100\"

## Gine-ginen MM1 da tsarin multimodal learning

![Gine-ginen model MM1][architecture].class=\"m-10 w-100\"

Diagram ɗin yana nuna tsarin MM1. Image input yana shiga Image Encoder. Text input yana shiga pre-trained LLM transformer. Visual features suna wucewa zuwa VL Connector, wanda ke haɗa su da textual representation. Wannan multimodal fusion yana ba model damar yin visual question answering da captioning bayan supervised fine-tuning.

Pre-training data ya ƙunshi 45% interleaved data, 45% captions, da 10% text-only data. Wannan ya nuna cewa multimodal learning ba ƙara hoto ga language model kawai ba ne; tsara data yana cikin architecture.

![divider][divider].class=\"m-10 w-100\"

## MM1 a matsayin benchmark na AI multimodal

MM1 benchmark ne saboda yana gwada shawarar architecture da ta dace da amfani na gaske. Model ɗin ya nuna ƙarfi a visual question answering, image captioning, da aikin da ke buƙatar fahimtar hoto tare da harshe.

Ƙarfinsa shi ne samar da rubutu mai ma’ana daga visual input. Idan aka ba shi hoton titi mai cunkoso, zai iya bayyana yanayi, gine-gine, mutane, da ayyuka. Wannan shi ne ainihin darajar multimodal AI: fahimtar context, ba gane object kaɗai ba.

### Tasiri da gaba

MM1 ya ba da tushe ga MLLM architecture mafi ƙarfi. A gaba, ana bukatar connector mai daidaitawa, attention mai inganci, da evaluation mafi tsauri don yanayin amfani na zahiri.

> Mu ƙirƙiri gobe maimakon damuwa da jiya. — **Steve Jobs**

Aikace-aikace sun haɗa da assistants masu fahimtar allo, kayan koyarwa, nazarin takardu, da ƙirƙirar abun ciki. Amma model multimodal ya fi wahalar tantancewa. Ƙarin modality yana nufin ƙarin aikin validation.

> Babban mataki na gaba a AI shi ne machine da ke fahimtar duniya a kusa da su sosai, har ma su iya yin reasoning kan data da ba su taɓa gani ba. — **Yann LeCun**

![divider][divider].class=\"m-10 w-100\"

## Kammalawa

MM1 muhimmin bincike ne a ci gaban LLM multimodal. Ya nuna architecture, data quality, image resolution, da vision-language connector suna ƙayyade ikon model. Ba girman model kaɗai ne amsa ba; dole a auna data pipeline da haɗin modalities.

Model irin MM1 na iya sa hulɗar mutum da machine ta zama mafi halitta. Amma hakan yana bukatar injiniya mai tsari, evaluation, da governance.

Don karanta asalin paper, duba: [**MM1: Methods Analysis & Insights from Multimodal LLM Pre-training ⧉**][00]

[00]: https://arxiv.org/abs/2403.09611 "MM1: Methods Analysis & Insights from Multimodal LLM Pre-training"

[divider]: https://cloudcdn.pro/clients/common/images/elements/divider.svg "Divider"
[architecture]: https://cloudcdn.pro/stocks/diagrams/mm1_model_architecture.svg "Gine-ginen model MM1"
