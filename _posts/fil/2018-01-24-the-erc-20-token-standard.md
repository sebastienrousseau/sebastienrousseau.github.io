---
title: "Ang pamantayang token na ERC-20"
tags: "Ethereum, erc20, eip, tokens, contracts, blockchain, cryptocurrencies, smart-token, Solidity, ISO 20022, post-quantum cryptography, AI, stablecoins"
subtitle: "Paano pinag-isa ng ERC-20 ang arkitektura ng token sa Ethereum, at kung bakit ito naging katalista ng desentralisadong pinansiya."
description: "Ang pamantayang ERC-20: ang anim na pangunahing punsiyon at dalawang pangyayaring tinutukoy nito, kung paano nito inalis ang pagkakawatak-watak ng arkitektura ng token sa Ethereum, at ang epekto nito sa DeFi at sa seguridad."
date: "January 24, 2018"
language: "fil-PH"
locale: "fil_PH"
banner: "https://cloudcdn.pro/stocks/images/m-ZzOa5G8hSPI.webp"
banner_alt: "Isang nakapatay na laptop sa ibabaw ng kayumangging mesang kahoy"
keywords: "ERC-20, Ethereum, pamantayang token, smart contract, DeFi, desentralisadong pinansiya, interoperabilidad, DApps, seguridad ng token, blockchain"
---
![Isang nakapatay na laptop sa ibabaw ng kayumangging mesang kahoy](https://cloudcdn.pro/stocks/images/m-ZzOa5G8hSPI.webp).class=\"img-fluid clearfix\"

## Ang pamantayang token na ERC-20

### Ang pangangailangan ng isang pinag-isang interface ng token

Bago sumulpot ang pamantayang ERC-20 (Ethereum Request for Comments 20), ang blockchain ng Ethereum ay tila lupang walang batas pagdating sa arkitektura ng token. Ang bawat bagong token ay may sarili nitong hanay ng patakaran, punsiyon, at interface. Hindi lamang nito ipinapasan sa mga developer ang mabigat na kurba ng pagkatuto, kundi hinahadlangan din nito ang interoperabilidad ng mga token. Sa esensiya, ang bawat bagong token ay parang isang bagong wikang kailangang pag-aralan, unawain, at ipatupad. Napigil ng pagkakawatak-watak na ito ang kakayahang lumawak at ang malawakang pagtanggap sa mga token sa plataporma ng Ethereum.

Ang pagsulpot ng pamantayang ERC-20 ay gumanap na tila isang pinag-isang wika, sapagkat naglatag ito ng magkakabahaging hanay ng patakaran at punsiyon na sinusunod ng lahat ng token sa Ethereum. Ngayon ay may isa nang magkatugmang interface ang mga developer na mapagtatrabahuhan, anuman ang tokeng tinutukoy. Pinasimple ng pagsasapamantayang ito ang pakikipag-ugnayan sa mga token, kaya naging mas maayos ang pagsasanib nito sa iba't ibang aplikasyon at serbisyo. Bunga nito, mas mabisa nang natatrato ng mga developer ang mga token, na naghahanda ng kapaligirang kaaya-aya sa inobasyon at paglago sa loob ng ekosistema ng Ethereum.

#### Ang lupang walang batas ng arkitektura ng token

Ang blockchain ng Ethereum ay orihinal na idinisenyo upang suportahan ang iisang uri ng token: ang ETH. Gayunman, habang lumalago ang katanyagan ng plataporma, sinimulan ng mga developer na lumikha ng sarili nilang token upang katawanin ang iba't ibang ari-arian at konsepto. Nagbunga ito ng pagdami ng magkakaibang arkitektura ng token, bawat isa ay may sariling hanay ng patakaran at punsiyon.

Dahil sa pagkakawatak-watak na ito, naging mahirap para sa mga developer ang lumikha ng aplikasyong nakikipag-ugnayan sa maraming token. Naging mahirap din para sa mga gumagamit ang pangasiwaan ang kanilang mga ari-ariang token sa iba't ibang plataporma.

#### Ang pamantayang ERC-20

Inilunsad ang pamantayang ERC-20 noong 2015 upang harapin ang mga hamong dulot ng lupang walang batas ng arkitektura ng token. Tinutukoy ng pamantayan ang magkakabahaging hanay ng patakaran at punsiyon na sinusunod ng lahat ng token sa Ethereum. Pinadadali ng pagsasapamantayang ito sa mga developer ang paglikha ng aplikasyong kayang makipag-ugnayan sa alinmang tokeng ERC-20, at pinadadali rin nito sa mga gumagamit ang pangangasiwa ng kanilang ari-arian.

Malawakang tinanggap ng komunidad ng Ethereum ang pamantayang ERC-20. Sa kasalukuyan, mahigit 200,000 na ang bilang ng umiiral na tokeng ERC-20, at ginagamit ang pamantayan sa malawak na hanay ng aplikasyon, kabilang na ang mga desentralisadong palitan, ang mga plataporma ng pagpapautang, at ang mga desentralisadong aplikasyon sa paglalaro.

## Ang ideya

### Isang magkakabahaging hanay ng punsiyon at katangian para sa lahat ng token

Tinutukoy ng pamantayang ERC-20 ang anim na pangunahing punsiyong dapat ipatupad ng lahat ng tugmang token. Ang mga punsiyong ito ay:

- `transfer(address to, uint256 amount)`: naglilipat ng dami ng token mula sa adres ng tumatawag tungo sa tinukoy na adres.
- `approve(address spender, uint256 amount)`: pinahihintulutan ang tinukoy na adres na gumastos ng dami ng token sa ngalan ng tumatawag.
- `allowance(address owner, address spender)`: ibinabalik ang dami ng tokeng pinapayagang gastusin ng tinukoy na `spender` sa ngalan ng tinukoy na `owner`.
- `totalSupply()`: ibinabalik ang kabuuang bilang ng tokeng nasa sirkulasyon.
- `balanceOf(address owner)`: ibinabalik ang bilang ng tokeng pag-aari ng tinukoy na adres.
- `name()`: ibinabalik ang pangalan ng token.
- `symbol()`: ibinabalik ang simbolo ng token.

Tinutukoy din ng pamantayan ang dalawang pangyayaring dapat ilabas kapag matagumpay na naisagawa ang katumbas na punsiyon:

- `Transfer(address from, address to, uint256 amount)`: inilalabas kapag naglipat ng dami ng token mula sa isang adres tungo sa iba.
- `Approval(address owner, address spender, uint256 amount)`: inilalabas kapag binigyan ang tinukoy na adres ng pahintulot na gumastos ng dami ng token sa ngalan ng tinukoy na `owner`.

## Ang epekto

### Ang paglago ng desentralisadong pinansiya (DeFi) at ang pagdami ng gumagamit ng Ethereum

Nagdulot ang pamantayang ERC-20 ng nadaramang epekto sa ekosistema ng Ethereum. Naging mahalaga itong katalista ng kilusang desentralisadong pinansiya (DeFi), at nag-ambag din ito sa paglawak ng pagtanggap sa Ethereum.

Ang mga plataporma ng desentralisadong pinansiya, na naghahandog ng hanay ng serbisyong pinansiyal mula pagpapautang hanggang pangangasiwa ng ari-arian, ay lubhang umaasa sa mga token upang mapadali ang mga transaksiyon. Sa paggampan ng ERC-20 bilang pandaigdigang konektor, naging higit na madali para sa mga aplikasyong DeFi ang isanib ang malawak na hanay ng token nang hindi kailangang iangkop ang kanilang kodigo sa bawat token.

Pinadali rin ng pamantayan sa mga gumagamit ang pangangasiwa ng kanilang mga ari-ariang token. Dahil sumusunod ang mga token sa iisang saligang patakaran, mas madali nang nailulipat, nagagastos, at napangangasiwaan ng mga gumagamit ang kanilang ari-arian sa iba't ibang plataporma. Ang pagbuting ito sa karanasan ng gumagamit ang naging pampasigla sa mas mataas na antas ng pagtanggap sa Ethereum.

## Ang mga insentibo

### Pagbaba ng gastos sa pagpapaunlad at pagtibay ng seguridad

Ang pagsasapamantayang dala ng protokol na ERC-20 ay nag-iwan din ng tuwirang epektong pang-ekonomiya. Sa paglalaan ng isang nasubok at kinikilala ng komunidad na balangkas para sa paglikha ng token, malaki ang ibinaba ng pamantayan sa hadlang sa pagpasok ng mga developer. Kaya na nilang lumikha ngayon ng bagong token nang may mas mababang gastos sa pagpapaunlad at mas mabilis na pagpasok sa pamilihan, nang hindi na kailangang muling likhain ang gulong. Hinihikayat din ng pamantayan, sa di-tuwirang paraan, ang paglikha ng mga desentralisadong aplikasyon (DApps) at serbisyong kayang makipag-ugnayan sa pandaigdigang saklaw sa alinmang tokeng ERC-20, na nagpapasigla naman sa isang lalong masiglang ekosistema.

Isa pang kapansin-pansing bentahe ang pagtibay ng seguridad. Sumailalim ang pamantayang ERC-20 sa mahigpit na pagsusuri ng komunidad ng Ethereum, kaya naging matatag at ligtas itong modelo para sa pagpapatupad ng token. Ang pagsunod sa pamantayang ito ay nangangahulugang sinusunod ng mga pangunahing bahagi ng smart contract ng token ang pinakamahusay na kasanayang tinatanggap ng komunidad. Binabawasan nito ang panganib ng butas sa seguridad na maaaring idulot ng isang kulang sa disenyong modelo ng token. Bagaman hindi ito garantiya laban sa lahat ng uri ng kahinaan, isa itong mahalagang hakbang tungo sa pagtiyak ng pangkalahatang seguridad ng mga token, at samakatwid ng mga proyektong gumagamit ng mga ito.
