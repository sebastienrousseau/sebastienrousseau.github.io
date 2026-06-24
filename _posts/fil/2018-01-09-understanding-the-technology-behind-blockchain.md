---
author: "contact@sebastienrousseau.com (Sebastien Rousseau)"
banner_alt: "Mga abstract na digital ledger block na konektado ng mga light trail sa madilim na background"
banner_height: "100vh"
banner_width: "100vw"
banner: "https://cloudcdn.pro/stocks/images/adam-smigielski-K5mPtONmpHM.webp"
cdn: "https://cloudcdn.pro/clients"
changefreq: "weekly"
charset: "UTF-8"
cname: "sebastienrousseau.com"
copyright: "© Copyright 2007 - 2026 - Sebastien Rousseau. All rights reserved."
date: "Jan 09, 2018"
description: "Teknikal na introduksyon sa blockchain: cryptographic hash chains, Merkle trees, distributed consensus, at kung paano pinalawak ng Ethereum ang payments ledger bilang platform para sa smart contracts at tokenised assets."
format-detection: "telephone=no"
hreflang: "fil"
icon: "https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/sebastienrousseau.svg"
id: "https://sebastienrousseau.com/fil/2018-01-09-understanding-the-technology-behind-blockchain"
image_alt: "Black and White Portrait of Sebastien Rousseau"
image_height: "162"
image_width: "162"
image: "https://cloudcdn.pro/stocks/images/sebastienrousseau.webp"
keywords: "blockchain technology, cryptographic hash, Merkle tree, distributed consensus, proof of work, Ethereum, smart contracts, EVM, Solidity, ERC-20, distributed ledger, decentralised finance"
language: "fil"
layout: "report"
locale: "fil_PH"
logo_alt: "Logo for Sebastien Rousseau"
logo_height: "44"
logo_width: "44"
logo: "https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/sebastienrousseau.svg"
menu: "active"
measurementID: "G-169G4ET5HQ"
name: "Sebastien Rousseau"
permalink: "https://sebastienrousseau.com/fil/2018-01-09-understanding-the-technology-behind-blockchain"
rating: "general"
referrer: "no-referrer"
revisit-after: "7 days"
robots: "index, follow"
short_name: "sebastienrousseau"
subtitle: "Mula sa cryptographic hash chains hanggang sa programmable smart contracts: ang mekanika na gumawa ng blockchain na platform, hindi lamang ledger."
tags: "blockchain, Ethereum, smart contracts, cryptography, Merkle tree, consensus mechanism, proof of work, EVM, Solidity, ERC-20, decentralised finance, ISO 20022, post-quantum cryptography, AI, stablecoins, tokenised deposits"
theme-color: "0, 67, 165"
title: "Understanding the Technology behind Blockchain"
url: "https://sebastienrousseau.com/fil/2018-01-09-understanding-the-technology-behind-blockchain"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://sebastienrousseau.com/2018-01-09-understanding-the-technology-behind-blockchain/rss.xml"
category: "Blockchain"
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.26)"
item_description: "Teknikal na panimula sa blockchain: cryptographic hash chains, Merkle trees, distributed consensus, at kung paano pinalawak ng Ethereum ang ledger sa isang programmable platform."
item_guid: "https://sebastienrousseau.com/2018-01-09-understanding-the-technology-behind-blockchain/rss.xml"
item_link: "https://sebastienrousseau.com/2018-01-09-understanding-the-technology-behind-blockchain/rss.xml"
item_pub_date: "Tue, 09 Jan 2018 09:09:00 +0000"
item_title: "Pag-unawa sa Teknolohiya sa Likod ng Blockchain"
last_build_date: "Tue, 09 Jan 2018 09:09:00 +0000"
managing_editor: "contact@sebastienrousseau.com (Sebastien Rousseau)"
pub_date: "Tue, 09 Jan 2018 09:09:00 +0000"
ttl: "60"
type: "website"
webmaster: "contact@sebastienrousseau.com"
apple_mobile_web_app_orientations: "portrait"
apple_touch_icon_sizes: "192x192"
apple-mobile-web-app-capable: "yes"
apple-mobile-web-app-status-bar-inset: "black"
apple-mobile-web-app-status-bar-style: "black-translucent"
apple-mobile-web-app-title: "Teknolohiya ng Blockchain"
apple-touch-fullscreen: "yes"
msapplication-navbutton-color: "0, 67, 165"
twitter_card: "summary"
twitter_creator: "@wwdseb"
twitter_description: "Paano gumagana ang blockchain: hash chains, Merkle trees, consensus mechanisms, at kung paano ginawa ng Ethereum ang ledger na programmable platform."
twitter_image: "https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/sebastienrousseau.svg"
twitter_image_alt: "Logo of Sebastien Rousseau"
twitter_site: "@wwdseb"
twitter_title: "Pag-unawa sa Teknolohiya ng Blockchain"
twitter_url: "https://sebastienrousseau.com"
author_website: "https://sebastienrousseau.com"
author_twitter: "@wwdseb"
author_location: "London, UK"
thanks: "Thanks for reading!"
site_last_updated: "2023-07-05"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "Kaishi, Kaishi Builder, Kaishi CLI, Kaishi Templates, Kaishi Themes"
site_software: "Static Site Generator, Rust"
excerpt: "Ang blockchain ay isang append-only ledger na sinigurado ng cryptographic hash chains at distributed consensus — isang disenyo na ginagawang mahal sa computationally ang pakikialam at naa-audit ng sinuman. Pinalawak ng Ethereum ang pundasyon na ito ng isang programmable execution layer, ginagawang platform para sa smart contracts, tokens, at decentralised finance ang isang simpleng payments record."
last_reviewed: "2026-05-24"
---

<!-- lead-start -->
<aside class="post-lead" aria-label="Buod ng artikulo">
<p class="post-lead-tldr"><strong>TL;DR.</strong> Ang blockchain ay isang distributed ledger kung saan ang bawat talaan (bloke) ay cryptographically na naka-link sa nauna. Ang pagbabago ng anumang makasaysayang talaan ay nagpapawalang-bisa sa bawat kasunod na bloke — isang katangian na ipinapatupad hindi ng isang sentral na awtoridad kundi ng isang network ng mga independiyenteng validator na nagpapatakbo ng parehong mga panuntunan. Pinalawak ng Ethereum ang disenyo na ito gamit ang isang Turing-complete execution layer, na ginagawang programmable ang ledger at binubuksan ang pinto para sa mga smart contract, digital token, at desentralisadong pananalapi.</p>
<p class="post-lead-heading"><strong>Mga pangunahing punto</strong></p>
<ul class="post-lead-takeaways">
  <li><strong>Ang pangunahing problemang nalutas.</strong> Tinutugunan ng blockchain ng Bitcoin ang problema ng double-spend nang walang pinagkakatiwalaang ikatlong partido sa pamamagitan ng paggawa ng kasaysayan ng transaksyon na tamper-evident at kolektibong pinapanatili. Ang solusyon ay hinarap ang 30 taon ng naunang trabaho sa cryptographic hash function at distributed system.</li>
  <li><strong>Paano nagkakakonekta ang mga bloke.</strong> Ang bawat bloke ay naglalaman ng SHA-256 hash ng header ng nakaraang bloke. Ang pagbabago ng isang bloke ay sinisira ang bawat kasunod na hash, na nangangailangan sa isang umaatake na gawin muli ang lahat ng kasunod na proof-of-work — hindi maaasahang magawa sa computational na paraan pagkatapos ng ilang unang bloke sa isang mature na chain.</li>
  <li><strong>Programmable layer ng Ethereum.</strong> Idinagdag ng Ethereum ang Ethereum Virtual Machine (EVM), isang deterministic execution environment na nagpapatakbo ng Solidity bytecode sa bawat full node nang sabay-sabay. Ang mga smart contract — code na na-deploy sa chain — ay nagpapatakbo nang atomically: alinman sa kumpleto nang buo o nagbabalik, nang walang partial state.</li>
  <li><strong>Mula sa ledger hanggang sa platform.</strong> Ang ERC-20 token standard, na tinukoy noong 2015, ay nagpakita kung paano maaaring mag-host ang EVM ng mga fungible token nang hindi binabago ang base protocol. Daan-daang payment token, stablecoin, at governance token ang itinayo dito sa pagitan ng 2017 at 2020 — kabilang ang EXTC token na inilarawan sa mga kasamang artikulo sa site na ito.</li>
</ul>
<p class="post-lead-related"><strong>Kaugnay na pagbabasa:</strong> <a href="https://sebastienrousseau.com/2018-01-24-the-erc-20-token-standard">ERC-20: Ang Ethereum Token Interface na Nagbago ng Mundo</a>, <a href="https://sebastienrousseau.com/2018-02-04-unveiling-a-new-cryptocurrency-and-offering-future-faster-payment-solution">Pagbubunyag ng Bagong Cryptocurrency at Mas Mabilis na Solusyon sa Pagbabayad</a>, <a href="https://sebastienrousseau.com/2018-02-15-the-making-of-the-express-transaction-credits-platform">Ang Paglikha ng Express Transaction Credits Platform</a>.</p>
</aside>
<!-- lead-end -->

![Abstract digital ledger blocks connected by light trails on dark background](https://cloudcdn.pro/stocks/images/adam-smigielski-K5mPtONmpHM.webp).class=\"img-fluid clearfix\"

> **Buod / Mga Pangunahing Punto**
>
> - **Ang problema.** Ang digital cash ay nangangailangan ng paglutas ng problema ng double-spend: pag-iwas sa paggastos ng parehong yunit nang dalawang beses nang walang pinagkakatiwalaang clearinghouse. Nalutas ito ng 2008 whitepaper ng Bitcoin sa pamamagitan ng pagpapalit ng mga pinagkakatiwalaang intermediary ng cryptographic proof at distributed consensus ([Nakamoto, 2008](https://bitcoin.org/bitcoin.pdf "Bitcoin: A Peer-to-Peer Electronic Cash System")).
> - **Ang data structure.** Ang blockchain ay isang linked list ng mga bloke kung saan ang bawat block header ay naglalaman ng SHA-256 hash ng nakaraang header. Ginagawa ng hash chain ang kasaysayan na append-only: ang pagbabago ng anumang nakaraang bloke ay nagpapawalang-bisa sa bawat kasunod na hash, na pinipilit ang isang umaatake na gawin muli ang lahat ng kasunod na proof-of-work.
> - **Merkle trees.** Ang mga transaksyon sa loob ng isang bloke ay naka-hash sa isang binary Merkle tree. Ang root hash, na nakaimbak sa block header, ay nagbibigay-daan sa mahusay na pag-verify ng anumang indibidwal na transaksyon nang hindi dina-download ang buong bloke — ang batayan para sa magagaang SPV client.
> - **Pagpapalawak ng Ethereum.** Ipinakilala ng Yellow Paper ng Ethereum (2014) ang EVM — isang deterministic stack machine na tumatakbo sa bawat full node. Ang mga smart contract ay bytecode na na-deploy sa chain; nagpapatakbo sila nang magkapareho sa lahat ng node at nagse-settle nang atomically, pinapalitan ang mga pinagkakatiwalaang intermediary ng self-enforcing code ([Wood, 2014](https://ethereum.github.io/yellowpaper/paper.pdf "Ethereum Yellow Paper")).
> - **Praktikal na kahalagahan.** Ang bawat tokenised asset, stablecoin, at DeFi protocol na na-deploy mula 2017 ay tumatakbo sa mga pundasyon na ito. Ang pag-unawa sa hash chain, ang Merkle tree, at ang EVM execution model ay kinakailangan bago magtrabaho sa anumang Ethereum-based na sistema.

---

## Ang Problemang Nalutas ng Blockchain

Bago ang Bitcoin, ang mga digital na pagbabayad ay nangangailangan ng isang pinagkakatiwalaang intermediary — isang bangko, payment processor, o clearing house — upang maiwasan ang double-spending. Kung magpadala si Alice ng digital na file na kumakatawan sa £10 kay Bob, walang nasa file mismo ang pumigil sa kanya na magpadala ng magkaparehong kopya kay Carol. Ang solusyon sa bawat umiiral na sistema ay sentralisadong pagpapanatili ng talaan: sinabi ng ledger ng bangko na nagastos na ang pera, kaya hindi na ito maaaring gastusin muli.

Ang kontribusyon ng Bitcoin ay palitan ang pinagkakatiwalaang ledger na iyon ng isang distributed na ledger kung saan ang talaan ng lahat ng transaksyon ay na-replicate sa libu-libong independiyenteng node. Ang mutual na kawalan ng tiwala sa pagitan ng mga node ay na-convert sa seguridad sa pamamagitan ng dalawang mekanismo:

1. **Cryptographic linking.** Ang bawat bloke ng mga transaksyon ay naglalaman ng hash ng nakaraang bloke. Ang hash function ay isang one-way deterministic mapping: para sa anumang input, ang function ay gumagawa ng fixed-length output, at ang pagbabago kahit isang bit ng input ay gumagawa ng ganap na naiibang output. Nangangahulugang ang anumang pagbabago sa isang makasaysayang bloke ay nagpapawalang-bisa sa bawat bloke pagkatapos nito.

2. **Proof-of-work consensus.** Ang pagdaragdag ng bagong bloke ay nangangailangan ng paghahanap ng nonce value na ang hash ng bloke ay mas mababa sa isang target threshold — mahal sa computational na paraan na mahanap, mura naman na i-verify. Ginagawa nitong proporsyonal na mahal ang muling pagsulat ng kasaysayan sa lalim ng blokeng binabago, dahil dapat gawin muli ng umaatake ang lahat ng proof-of-work mula sa blokeng iyon hanggang sa dulo ng chain.

Ang kombinasyon ay nangangahulugan na ang pinakamahabang chain na may pinakamaraming cumulative proof-of-work ay, sa pamamagitan ng konstruksyon, ang isa na pinapanatili ng mga tapat na kalahok na gumagugol ng tunay na mapagkukunan.

## Ang Mga Cryptographic Building Block

Ang teknolohiya ng blockchain ay nag-aasemble ng tatlong pre-existing na cryptographic primitive sa isang bagong arkitektura:

### Mga Hash Function ng SHA-256

Ang SHA-256 (Secure Hash Algorithm 256-bit) ay isang miyembro ng pamilyang SHA-2 na na-standardize ng NIST. Tumatanggap ito ng input na may arbitrary na haba at gumagawa ng 256-bit na output. Mga pangunahing katangian para sa paggamit ng blockchain:

- **Deterministic.** Ang parehong input ay laging gumagawa ng parehong output.
- **Pre-image resistance.** Dahil sa isang hash output, hindi maaasahang maibalik ang input sa computational na paraan.
- **Avalanche effect.** Ang pagbabago ng isang bit ng input ay nagbabago ng halos kalahati ng mga output bit, na ginagawang hindi mahusay ang brute-force search.
- **Collision resistance.** Hindi maaasahang mahanap ang dalawang magkaibang input na gumagawa ng parehong hash sa computational na paraan.

Inilalapat ng Bitcoin ang SHA-256 nang dalawang beses (SHA-256d) para sa karagdagang seguridad laban sa mga length-extension attack. Gumagamit ang Ethereum ng Keccak-256, isang SHA-3 finalist variant.

### Merkle Trees

Ang Merkle tree ay isang binary tree ng mga hash. Ang bawat leaf node ay ang hash ng isang transaksyon. Ang bawat internal node ay ang hash ng dalawang anak nito. Ang ugat — ang Merkle root — ay nagbubuod ng lahat ng transaksyon sa bloke sa isang solong 32-byte na halaga na nakaimbak sa block header.

Ang praktikal na kahihinatnan: upang i-verify na ang isang partikular na transaksyon ay kasama sa isang bloke, kailangan mo lamang ng `log₂(n)` na hash, hindi lahat ng `n` na transaksyon. Para sa isang bloke na may 2,000 transaksyon, ang pag-verify ay nangangailangan ng 11 hash sa halip na 2,000 — ang batayan para sa Simplified Payment Verification (SPV) sa mga magagaang client.

### Mga Digital Signature (ECDSA)

Gumagamit ang awtorisasyon ng transaksyon sa Bitcoin at Ethereum ng Elliptic Curve Digital Signature Algorithm (ECDSA) sa ibabaw ng secp256k1 curve. Ang isang private key ay pumipirma ng transaksyon; ang sinumang node ay maaaring i-verify ang pirma gamit ang kaukulang public key nang hindi alam ang private key. Tinitiyak nito na ang humahawak lamang ng private key ang maaaring mag-authorize ng gastos mula sa isang address.

Ang mga address ng Ethereum ay ang huling 20 byte ng Keccak-256 hash ng public key — isang derivation na ginagawang compact at portable ang mga address habang nananatiling cryptographically na nakatali sa key pair.

## Paano Gumagana ang Bitcoin Blockchain

Ang isang Bitcoin block ay naglalaman ng tatlong lohikal na bahagi:

**Ang block header** — 80 byte na binubuo ng: ang bersyon ng protocol, ang hash ng nakaraang block header, ang Merkle root ng mga transaksyon, isang Unix timestamp, ang kasalukuyang difficulty target, at ang nonce. Ino-iterate ng mga miner ang nonce (at minsan ang timestamp o extra-nonce sa coinbase transaction) hanggang ang double-SHA-256 hash ng header ay mas mababa sa difficulty target.

**Ang listahan ng transaksyon** — ang ordered set ng mga transaksyon na kasama sa bloke. Ang coinbase transaction (ang una) ay nagtatalaga ng block reward at mga bayad sa transaksyon sa address ng miner.

**Ang chain** — ang pagkakakonekta ng mga header. Ang cumulative proof-of-work sa chain (ang kabuuan ng lahat ng trabahong ginawa upang makagawa ng bawat bloke) ay tinutukoy kung aling fork ang canonical chain. Laging sumusunod ang mga node sa chain na may pinakamaraming cumulative work.

Ang oras ng bloke ay naglalayong 10 minuto para sa Bitcoin. Nag-a-adjust ang difficulty tuwing 2,016 na bloke (humigit-kumulang dalawang linggo) upang mapanatili ang target na iyon habang nagbabago ang kabuuang hash rate ng network.

## Programmable Layer ng Ethereum

Pinag-generalize ng Ethereum ang transaction model ng Bitcoin mula sa "transfer value" hanggang sa "execute code." Ang mga pangunahing karagdagan:

**Ang Ethereum Virtual Machine (EVM).** Isang 256-bit na salita, stack-based virtual machine na nagpapatakbo nang deterministically sa lahat ng full node. Ang bawat opcode ay may explicit na gas cost. Ang computation ay limitado ng block gas limit, pinipigilan ang mga infinite loop mula sa pagpigil sa network. Ang lahat ng node na nagpapatakbo ng parehong bytecode sa parehong estado ay dapat gumawa ng parehong output — ang consensus na ito sa execution ang nagpapaging trustless ng mga smart contract.

**Mga Account.** Ang Ethereum ay may dalawang uri ng account: Externally Owned Accounts (EOA) na kinokontrol ng mga private key, at Contract Accounts na ang code ay nakaimbak sa chain. Ang isang transaksyon na ipinadala sa isang contract address ay nag-trigger ng bytecode execution ng contract.

**Estado.** Ang global state ng Ethereum ay isang mapping ng mga address sa mga account state (nonce, balanse, storage, code hash). Ang state root — isang Merkle Patricia trie ng lahat ng account state — ay kasama sa bawat block header, na nagbibigay-daan sa mahusay na patunay ng estado ng anumang account sa anumang block height.

**Gas.** Nagbabayad ang mga gumagamit ng gas (sa ETH) para sa bawat EVM operation. Nagsisilbi ang gas ng dalawang function: binibigyan nito ng kabayaran ang mga miner/validator para sa computation, at nililimitahan nito ang mga mapagkukunan na maaaring gamitin ng anumang solong transaksyon, pinipigilan ang mga denial-of-service attack sa pamamagitan ng mga mahal na operasyon.

## Pagsulat ng Mga Smart Contract sa Solidity

Ang Solidity ay isang statically-typed, contract-oriented na wika na nag-compile sa EVM bytecode. Isang minimal na token contract ang naglalarawan ng mga pangunahing konsepto:

```solidity
pragma solidity ^0.8.0;

contract MyToken {
    string public name;
    string public symbol;
    uint8 public decimals;
    uint256 public totalSupply;
    mapping(address => uint256) public balanceOf;

    event Transfer(address indexed from, address indexed to, uint256 value);

    constructor(
        string memory _name,
        string memory _symbol,
        uint8 _decimals,
        uint256 _totalSupply
    ) {
        name = _name;
        symbol = _symbol;
        decimals = _decimals;
        totalSupply = _totalSupply;
        balanceOf[msg.sender] = _totalSupply;
    }

    function transfer(address _to, uint256 _value) external returns (bool) {
        require(balanceOf[msg.sender] >= _value, "Insufficient balance");
        balanceOf[msg.sender] -= _value;
        balanceOf[_to] += _value;
        emit Transfer(msg.sender, _to, _value);
        return true;
    }
}
```

Mga pangunahing obserbasyon: ang `mapping(address => uint256)` ay isang EVM storage layout, hindi isang in-memory data structure — ang mga pagbabasa at pagsulat ay nagkakahalaga ng gas. Binabawi ng `require` ang buong transaksyon sa kabiguan, ibinabalik ang hindi nagamit na gas. Ang `event Transfer` ay nag-e-emit ng log na ginagamit ng mga off-chain indexer upang subaybayan ang mga transfer nang hindi muling binabasa ang buong estado. Ang `constructor` ay tumatakbo nang isang beses sa pag-deploy; ang mga kasunod na tawag ay pupunta sa mga pinangalanang function.

Pina-formalize ng ERC-20 standard ang isang karaniwang interface para sa mga fungible token — `transfer`, `transferFrom`, `approve`, `allowance`, `balanceOf`, `totalSupply` — na nagbibigay-daan sa anumang ERC-20-compliant na token na gumana sa anumang ERC-20-aware na palitan o wallet nang walang custom integration.

## Mula sa Ledger hanggang sa Financial Infrastructure

Ang mga blockchain primitive na inilarawan dito — mga hash chain, Merkle tree, ang EVM, at ERC-20 — ay naging pundasyon para sa mas malawak na hanay ng mga aplikasyong pinansyal sa pagitan ng 2018 at 2026:

**Desentralisadong Pananalapi (DeFi).** Ang mga lending protocol (Compound, Aave), mga automated market maker (Uniswap), at mga yield aggregator ay lahat tumatakbo bilang mga EVM smart contract. Pinapalitan nila ang mga function ng clearing, custody, at settlement ng tradisyonal na mga pinansyal na intermediary ng self-executing code at mga on-chain liquidity pool.

**Mga Tokenised Asset.** Ang mga sentral na bangko at komersyal na bangko ay nag-pi-pilot ng mga tokenised deposit, tokenised bond, at tokenised money market fund sa mga permissioned na variant ng mga EVM-compatible na chain. Ang pinagbabatayan na mekaniko — mga hash-secured state transition, atomic settlement, mga programmable transfer rule — ay mga direktang inapo ng 2014 Ethereum architecture.

**Mga Central Bank Digital Currency.** Ang wholesale CBDC research ng Bank of England, ang digital euro programme ng ECB, at Project Agorá ay lahat nag-eeksplora ng mga DLT architecture na nagmula sa o katugma ng mga pundasyon na disenyo sa Bitcoin at Ethereum. Ang mga istruktura ng consensus at hash-chain ay nananatiling may kaugnayan kahit saan ang permissioning at modelo ng pamamahala ay ganap na naiiba mula sa mga public blockchain.

Ang paglalakbay mula sa 2008 Bitcoin whitepaper hanggang sa 2026 tokenised finance ay sumasaklaw ng dalawang dekada, ngunit tumatakbo ito sa isang magkakaugnay na teknikal na linya. Ang pag-unawa kung paano nagpapatupad ng immutability ang isang SHA-256 hash chain, kung paano nagbibigay-daan ang isang Merkle tree sa mahusay na pag-verify, at kung paano nag-e-execute ang EVM ng mga smart contract nang atomically ay kinakailangan bago masuri ang anumang pahayag tungkol sa kung ano ang kaya at hindi kaya ng blockchain sa mga regulated na serbisyong pinansyal.

## Mga Madalas Itanong

**Ano ang pagkakaiba ng blockchain at distributed database?**

Ang tradisyonal na distributed database ay nag-re-replicate ng data sa mga node para sa availability at performance, ngunit ang tiwala ay sentralisado — maaaring baguhin ng isang administrator ang mga talaan. Ginagawa ng blockchain ang pag-tamper na mahal sa computational na paraan sa pamamagitan ng hash chaining at consensus: ang pagbabago ng anumang makasaysayang talaan ay nangangailangan ng pag-redo ng lahat ng kasunod na proof-of-work o proof-of-stake, at ng paghikayat sa network na tanggapin ang binagong fork. Ang pagkakaibang katangian ay tamper-evidence na ipinapatupad ng cryptography at disenyo ng insentibo sa halip na mga kontrol sa pag-access.

**Bakit gumagamit ang Ethereum ng Keccak-256 sa halip na SHA-256?**

Pinagtibay ng Ethereum ang Keccak-256 (ang SHA-3 finalist bago ang mga pagsasaayos sa standardisasyon ng NIST) bahagyang dahil gusto ng mga designer nito ang kalayaan mula sa linya ng SHA-2 na umaasa na ang Bitcoin. Mayroon ding iba't ibang algebraic na katangian ang Keccak na ginawa itong kaakit-akit para sa ilang mga operasyon ng EVM. Ang praktikal na epekto para sa mga developer ay ang Ethereum address derivation at storage slot hashing ay gumagamit ng Keccak-256, hindi SHA-256d tulad ng sa Bitcoin.

**Ano ang pinipigilan ng "gas" sa EVM?**

Pinipigilan ng gas ang dalawang kategorya ng atake. Una, pinipigilan nito ang denial-of-service sa pamamagitan ng mga operasyong mahal sa computational na paraan: ang bawat opcode ay nagkakahalaga ng gas, kaya hindi maaaring pilitin ng isang umaatake ang network na mag-execute ng mga infinite loop nang walang bayad. Pangalawa, nililimitahan ng block gas limit ang kabuuang computation sa bawat bloke, tinitiyak na ang oras ng pag-validate ng bloke ay nananatiling limitado at predictable para sa mga full node. Nang walang gas, ang isang solong contract call ay maaaring mapigilan ang network sa pamamagitan ng pag-execute ng walang limitasyong computation.

**Paano binabago ng proof-of-stake ang modelo ng seguridad kumpara sa proof-of-work?**

Sa proof-of-work, ang seguridad ay ibinibigay ng paggugol ng enerhiya: ang pag-atake sa chain ay nangangailangan ng pagkontrol sa mahigit 50% ng hash rate ng network, na nangangahulugang pagkontrol sa mahigit 50% ng pisikal na hardware at kapangyarihan nito. Sa proof-of-stake (ginagamit ng Ethereum mula noong Merge noong 2022), ang seguridad ay ibinibigay ng economic stake: nagla-lock ang mga validator ng ETH bilang collateral, na sini-slash kung pumirma sila ng mga nagtatagisang bloke. Ang isang 51% na atake ay nangangailangan ng pagkuha at pag-aaksaya ng mahigit 50% ng lahat ng naka-stake na ETH — isang capital cost sa halip na hardware at energy cost. Ang modelo ng seguridad ay naiiba ngunit mathematically na maihahambing sa mga tuntunin ng ekonomiya sa ilalim ng pagpapalagay na mas gusto ng mga makatwirang validator ang kita ng bayad kaysa pagkasira ng kapital.

## Mga Sanggunian

- Nakamoto, S., (2008). [Bitcoin: A Peer-to-Peer Electronic Cash System ⧉](https://bitcoin.org/bitcoin.pdf "Bitcoin Whitepaper").
- Buterin, V., (2014). [Ethereum: A Next-Generation Smart Contract and Decentralised Application Platform ⧉](https://ethereum.org/whitepaper "Ethereum Whitepaper").
- Wood, G., (2014). [Ethereum: A Secure Decentralised Generalised Transaction Ledger ⧉](https://ethereum.github.io/yellowpaper/paper.pdf "Ethereum Yellow Paper").
- NIST, (2015). [SHA-3 Standard: Permutation-Based Hash and Extendable-Output Functions ⧉](https://www.nist.gov/publications/sha-3-standard-permutation-based-hash-and-extendable-output-functions "NIST FIPS 202").

<!-- enrich-start -->
<aside class="author-card" aria-label="About the author"><img alt="Portrait of Sebastien Rousseau" src="https://cloudcdn.pro/stocks/images/sebastienrousseau.webp" width="64" height="64" loading="lazy" decoding="async" /><span class="author-card-body"><strong class="author-card-name"><a href="/about/index.html">Sebastien Rousseau</a></strong><span class="author-card-bio">Senior banking technologist writing on applied AI, ISO 20022 migration, post-quantum cryptography for financial services, and the structural transformation of wholesale payments.</span><span class="author-credentials">20+ years across HSBC Commercial &amp; Investment Bank, PayPal, Barclays, Shazam, AKQA, Virgin Group. <a href="/about/index.html">Full profile</a> &middot; <a href="https://www.linkedin.com/in/sebastienrousseau/" rel="external noopener">LinkedIn</a> &middot; <a href="https://github.com/sebastienrousseau" rel="external noopener">GitHub</a></span></span></aside>
<p class="post-reviewed">Last reviewed <time datetime="2026-05-24">2026-05-24</time>.</p>
<aside class="related-posts" aria-labelledby="related-heading">
<h2 id="related-heading" class="related-heading">Related reading</h2>
<div class="related-grid">
<article class="related-card"><a href="https://sebastienrousseau.com/2018-01-24-the-erc-20-token-standard" class="related-media" aria-label="ERC-20: The Ethereum Token Interface That Changed the World" tabindex="-1"><img alt="Giant white pillars" src="https://cloudcdn.pro/stocks/images/tarik-haiga-3637943.webp" loading="lazy" decoding="async" width="600" height="400" /></a><footer class="related-body"><h3><a href="https://sebastienrousseau.com/2018-01-24-the-erc-20-token-standard">ERC-20: The Ethereum Token Interface That Changed the World</a></h3><p><time datetime="2018-01-24">2018-01-24</time></p></footer></article>
<article class="related-card"><a href="https://sebastienrousseau.com/2018-02-04-unveiling-a-new-cryptocurrency-and-offering-future-faster-payment-solution" class="related-media" aria-label="Unveiling a New Cryptocurrency and Faster Payment Solution" tabindex="-1"><img alt="A very tall building with a lot of holes in it" src="https://cloudcdn.pro/stocks/images/laureen-missaire-DBbuhMbAIsQ.webp" loading="lazy" decoding="async" width="600" height="400" /></a><footer class="related-body"><h3><a href="https://sebastienrousseau.com/2018-02-04-unveiling-a-new-cryptocurrency-and-offering-future-faster-payment-solution">Unveiling a New Cryptocurrency and Faster Payment Solution</a></h3><p><time datetime="2018-02-04">2018-02-04</time></p></footer></article>
<article class="related-card"><a href="https://sebastienrousseau.com/2018-02-15-the-making-of-the-express-transaction-credits-platform" class="related-media" aria-label="The Making of the Express Transaction Credits Platform" tabindex="-1"><img alt="Giant white pillars" src="https://cloudcdn.pro/stocks/images/tarik-haiga-3637943.webp" loading="lazy" decoding="async" width="600" height="400" /></a><footer class="related-body"><h3><a href="https://sebastienrousseau.com/2018-02-15-the-making-of-the-express-transaction-credits-platform">The Making of the Express Transaction Credits Platform</a></h3><p><time datetime="2018-02-15">2018-02-15</time></p></footer></article>
</div>
</aside>
<!-- enrich-end -->
