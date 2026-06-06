---

# Front Matter (YAML)

author: "contact@sebastienrousseau.com (Sebastien Rousseau)"
banner_alt: "Giant white pillars"
banner_height: "100vh"
banner_width: "100vw"
banner: "https://cloudcdn.pro/stocks/images/tarik-haiga-3637943.webp"
cdn: "https://cloudcdn.pro/clients"
changefreq: "weekly"
charset: "UTF-8"
cname: "sebastienrousseau.com"
copyright: "© Copyright 2007 - 2026 - Sebastien Rousseau. All rights reserved."
date: "Feb 15, 2018"
description: "A technical deep-dive into how the EXTC platform was built on Ethereum ERC-223 in 2018: token architecture, multi-sig disbursements, time-locked transfers, and collateral-backed instant loans."
format-detection: "telephone=no"
hreflang: "en"
icon: "https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/sebastienrousseau.svg"
id: "https://sebastienrousseau.com/2018-02-15-the-making-of-the-express-transaction-credits-platform/index.html"
image_alt: "Black and White Portrait of Sebastien Rousseau"
image_height: "162"
image_width: "162"
image: "https://cloudcdn.pro/stocks/images/sebastien-rousseau.png"
keywords: "EXTC platform, ERC-223, Ethereum smart contracts, token architecture, multi-signature, time-locked transfer, blockchain payments, collateral-backed loans, decentralised finance, 2018 crypto"
language: "en-GB"
layout: "report"
locale: "en_GB"
logo_alt: "Logo for Sebastien Rousseau"
logo_height: "44"
logo_width: "44"
logo: "https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/sebastienrousseau.svg"
menu: "active"
measurementID: "G-169G4ET5HQ"
name: "Sebastien Rousseau"
permalink: "https://sebastienrousseau.com/2018-02-15-the-making-of-the-express-transaction-credits-platform/index.html"
rating: "general"
referrer: "no-referrer"
revisit-after: "7 days"
robots: "index, follow"
short_name: "sebastienrousseau"
subtitle: "Designing the Express Transaction Credits platform with ERC-223 smart contracts."
tags: "EXTC platform, ERC-223, Ethereum, smart contracts, token architecture, multi-signature, time-locked transfer, blockchain, decentralised finance, collateral-backed loans, ISO 20022, post-quantum cryptography, AI, stablecoins"
theme-color: "0, 67, 165"
title: "The making of the Express Transaction Credits Platform"
url: "https://sebastienrousseau.com/2018-02-15-the-making-of-the-express-transaction-credits-platform/index.html"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"

# RSS - The RSS feed front matter (YAML).
atom_link: "https://sebastienrousseau.com/2018-02-15-the-making-of-the-express-transaction-credits-platform/rss.xml"
category: "Blockchain"
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.26)"
item_description: "A technical deep-dive into the EXTC platform built on Ethereum ERC-223 in 2018: token architecture, multi-sig disbursements, time-locked transfers, and collateral-backed instant loans."
item_guid: "https://sebastienrousseau.com/2018-02-15-the-making-of-the-express-transaction-credits-platform/rss.xml"
item_link: "https://sebastienrousseau.com/2018-02-15-the-making-of-the-express-transaction-credits-platform/rss.xml"
item_pub_date: "Thu, 15 Feb 2018 18:18:18 +0000"
item_title: "The making of the Express Transaction Credits Platform"
last_build_date: "Thu, 15 Feb 2018 18:18:18 +0000"
managing_editor: "contact@sebastienrousseau.com (Sebastien Rousseau)"
pub_date: "Thu, 15 Feb 2018 18:18:18 +0000"
ttl: "60"
type: "website"
webmaster: "contact@sebastienrousseau.com"

# Apple - The Apple front matter (YAML).
apple_mobile_web_app_orientations: "portrait"
apple_touch_icon_sizes: "192x192"
apple-mobile-web-app-capable: "yes"
apple-mobile-web-app-status-bar-inset: "black"
apple-mobile-web-app-status-bar-style: "black-translucent"
apple-mobile-web-app-title: "EXTC Platform 2018"
apple-touch-fullscreen: "yes"

# MS Application - The MS Application front matter (YAML).

msapplication-navbutton-color: "0, 67, 165"

# Twitter Card - The Twitter Card front matter (YAML).

twitter_card: "summary"
twitter_creator: "@wwdseb"
twitter_description: "A technical deep-dive into the EXTC platform built on Ethereum ERC-223 in 2018: token architecture, multi-sig disbursements, and collateral-backed instant loans."
twitter_image: "https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/sebastienrousseau.svg"
twitter_image_alt: "Logo of Sebastien Rousseau"
twitter_site: "@wwdseb"
twitter_title: "The making of the Express Transaction Credits Platform"
twitter_url: "https://sebastienrousseau.com/2018-02-15-the-making-of-the-express-transaction-credits-platform/index.html"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://sebastienrousseau.com/2018-02-15-the-making-of-the-express-transaction-credits-platform/index.html"
author_twitter: "@wwdseb"
author_location: "London, UK"
thanks: "Thanks for reading!"
site_last_updated: "2023-07-05"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "Kaishi, Kaishi Builder, Kaishi CLI, Kaishi Templates, Kaishi Themes"
site_software: "Static Site Generator, Rust"

excerpt: "A hands-on account of building the EXTC platform on Ethereum ERC-223 in early 2018: how the token contract was structured, what the multi-signature and time-lock primitives were designed to do, and what the experiment revealed about blockchain's practical limits for payment networks."
last_reviewed: "2026-05-24"
---


<!-- lead-start -->
<aside class="post-lead" aria-label="Article summary">
<p class="post-lead-tldr"><strong>TL;DR.</strong> A technical deep-dive into how the EXTC platform was built on Ethereum ERC-223 in 2018: token architecture, multi-sig disbursements, time-locked transfers, and collateral-backed instant loans.</p>
<p class="post-lead-heading"><strong>Key takeaways</strong></p>
<ul class="post-lead-takeaways">
  <li><strong>The Design Problem: Why ERC-20 Was Insufficient.</strong> The ERC-20 standard, proposed in 2015 and formalised in Ethereum Improvement Proposal 20, defined the canonical fungible token interface that powered the ICO boom of 2017–2018.</li>
  <li><strong>The ERC-223 Solution: Atomic Transfer with Notification.</strong> ERC-223, proposed on the Ethereum EIPs GitHub issue tracker, addressed the silent-loss problem by changing what a token transfer was required to do.</li>
  <li><strong>The EXTC Contract Architecture.</strong> The EXTC token contract was a Solidity implementation structured around five modules:.</li>
  <li><strong>The Collateral-Backed Instant Loan Mechanism.</strong> The EXTC lending primitive was the most complex component.</li>
</ul>
<p class="post-lead-related"><strong>Related reading:</strong> <a href="https://sebastienrousseau.com/2018-02-04-unveiling-a-new-cryptocurrency-and-offering-future-faster-payment-solution/index.html">Unveiling a new Cryptocurrency and Faster Payment Solution</a>, <a href="https://sebastienrousseau.com/2018-01-09-understanding-the-technology-behind-blockchain/index.html">Understanding the Technology behind Blockchain</a>, <a href="https://sebastienrousseau.com/2026-05-15-blackrock-brsrv-bstbl-genius-act-tokenised-mmf">Stablecoin Yield by Another Name: BlackRock's BRSRV and BSTBL Filings Decoded</a>.</p>
</aside>
<!-- lead-end -->

![Giant white pillars](https://cloudcdn.pro/stocks/images/tarik-haiga-3637943.webp).class=\"img-fluid clearfix\"

> **Executive Summary / Key Takeaways**
>
> - **The root problem.** ERC-20, the dominant Ethereum token standard in 2018, had a structural flaw: tokens transferred directly to a smart contract address were silently destroyed if the contract lacked a handler. Any payment platform built on ERC-20 inherited that risk ([Ethereum EIPs](https://eips.ethereum.org/EIPS/eip-20 "EIP-20: Token Standard")).
> - **ERC-223 as the fix.** ERC-223 required recipient contracts to implement a `tokenFallback(address, uint, bytes)` function. If absent, the transfer reverted atomically. No tokens could be silently lost ([Ethereum EIPs GitHub](https://github.com/ethereum/EIPs/issues/223 "ERC-223 Token Standard Proposal")).
> - **EXTC's five contract primitives.** Token identity (name, symbol, 18-decimal precision), fixed supply, ERC-223-compliant transfer, multi-signature corporate disbursement, and block-height time-locked standing orders.
> - **The collateral loan mechanism.** Borrowers locked EXTC tokens in a contract escrow; the contract released loan proceeds atomically upon receipt of collateral, without underwriting delay or credit-committee approval.
> - **What the experiment revealed about Ethereum limits.** At mainnet throughput of ~15 TPS and gas costs of $0.10–$1.00 per transaction at the January 2018 peak, a payment network processing even remittance-scale volume was economically and technically infeasible on public Ethereum without Layer-2 infrastructure.

---

## The Design Problem: Why ERC-20 Was Insufficient

The ERC-20 standard, proposed in 2015 and formalised in Ethereum Improvement Proposal 20, defined the canonical fungible token interface that powered the ICO boom of 2017–2018. Its six core functions — `totalSupply`, `balanceOf`, `transfer`, `transferFrom`, `approve`, and `allowance` — were sufficient for simple token issuance and exchange.

For a payment platform, however, ERC-20 had a production-critical flaw. The `transfer(address _to, uint256 _value)` function moved tokens to any address, including contract addresses, without triggering any code in the receiving contract. A contract that was not specifically programmed to track incoming ERC-20 transfers had no way to detect them. Tokens sent this way were trapped permanently, with no mechanism for recovery.

The Ethereum community estimated that tens of millions of dollars in ERC-20 tokens had been permanently lost by mid-2018 through this mechanism. Building a payment platform where transfers could silently fail and destroy user funds was not acceptable.

## The ERC-223 Solution: Atomic Transfer with Notification

ERC-223, proposed on the Ethereum EIPs GitHub issue tracker, addressed the silent-loss problem by changing what a token transfer was required to do. Under ERC-223, `transfer(address _to, uint256 _value, bytes _data)` checked whether the recipient address contained contract code. If it did, the transfer called `_to.tokenFallback(address _from, uint256 _value, bytes _data)`.

The critical property: if the recipient contract did not implement `tokenFallback`, the entire transfer transaction reverted. No tokens left the sender's balance. No tokens were trapped. The transfer was atomic — it either completed with the recipient's code executing, or it failed entirely with the state unchanged.

For EXTC, this meant:

- **Payment to smart contracts was safe by construction.** Escrow contracts, multi-sig wallets, and lending contracts could receive EXTC tokens without any risk of funds being irreversibly lost.
- **The `_data` field enabled rich payment metadata.** The bytes payload could carry invoice references, routing codes, or compliance attestations — information a simple ERC-20 transfer could not convey.
- **Gas costs were marginally higher.** Calling `tokenFallback` added approximately 2,000–5,000 gas per transfer, a minor overhead at 2018 gas prices.

## The EXTC Contract Architecture

The EXTC token contract was a Solidity implementation structured around five modules:

### 1. Token Identity

```
string public name = "Express Transaction Credits";
string public symbol = "EXTC";
uint8 public decimals = 18;
```

Eighteen decimal places gave EXTC sub-cent precision, matching the granularity required for micro-payment and micro-loan use cases. The symbol `EXTC` was the on-chain identifier registered in the token contract.

### 2. Fixed Total Supply

Total supply was set at contract deployment and could not be inflated by subsequent mints. This design choice made EXTC deflationary: any tokens permanently removed from circulation — through irreversible burn operations — reduced supply without replacement. The fixed-supply model was standard in 2018 payment token designs, reflecting the Bitcoin-influenced assumption that deflationary pressure was a feature for a medium of exchange.

### 3. ERC-223 Compliant Balance and Transfer

The core transfer function implemented the full ERC-223 interface. Internal balance mappings tracked each address's holdings. The `isContract(address)` helper distinguished EOA (externally owned account) addresses from contract addresses to determine whether `tokenFallback` needed to be called.

### 4. Multi-Signature Corporate Disbursements

Corporate payment workflows required co-authorisation: no single signer could unilaterally initiate a disbursement above a defined threshold. The EXTC contract implemented a two-of-N multi-signature scheme:

1. A designated initiator proposed a transfer, specifying recipient, amount, and a nonce.
2. A co-signer confirmed the nonce.
3. Only after both signatures were recorded on-chain did the transfer execute.

This eliminated single-point-of-failure risk for corporate accounts while keeping the entire authorisation flow on-chain and auditable without a clearing house intermediary.

### 5. Block-Height Time-Locked Standing Orders

Recurring payments — salaries, subscriptions, scheduled loan repayments — required a standing-order primitive. EXTC implemented this as a time-lock: a transfer record was stored in the contract with a `releaseBlock` parameter. The transfer could not execute until the Ethereum block height reached `releaseBlock`.

Block height as a time proxy was a pragmatic choice in 2018. Ethereum targeted a 15-second block interval, making block height a reasonably reliable proxy for wall-clock time within a range of minutes. Absolute timestamps (`block.timestamp`) were available but susceptible to miner manipulation within a ±900-second window, making block height the safer reference for financial contracts.

## The Collateral-Backed Instant Loan Mechanism

The EXTC lending primitive was the most complex component. The design:

1. **Borrower locks collateral.** The borrower called `lockCollateral(uint256 _collateralAmount)`, transferring EXTC tokens to the lending contract escrow via an ERC-223 `tokenFallback`.
2. **Loan-to-value ratio check.** The contract read a pre-configured LTV ratio (e.g. 50%) and calculated the maximum loan amount against the locked collateral.
3. **Atomic loan disbursement.** If the collateral met the minimum threshold, the contract immediately transferred the loan amount to the borrower's address. No underwriting queue, no credit committee, no settlement delay.
4. **Repayment and release.** On repayment — principal plus a fixed interest rate — the contract released the collateral back to the borrower. Failure to repay by `releaseBlock` triggered automatic liquidation: the contract transferred the collateral to the lender's designated address.

The entire flow was enforced by contract code. Neither party needed to trust the other or rely on an intermediary to enforce terms.

## What the Experiment Revealed

The EXTC contract architecture was technically coherent. ERC-223 resolved ERC-20's most serious safety flaw. The multi-signature and time-lock primitives mapped directly to real corporate payment workflows. The collateral loan mechanism demonstrated that secured lending could be fully automated and self-enforcing on-chain.

Two constraints revealed themselves in practice:

**Gas costs.** At the January 2018 peak, Ethereum gas prices reached 50–100 gwei, making a single ERC-223 token transfer cost $0.50–$2.00. For micro-payments or remittances of $10–$50, those fees were prohibitive.

**Throughput.** The Ethereum mainnet block gas limit in early 2018 was approximately 8 million gas. An ERC-223 transfer consumed roughly 50,000–80,000 gas. The network could therefore process approximately 100–160 EXTC token transfers per block, or roughly 7–11 per second at the 15-second block interval. Payment network scale — hundreds or thousands of transactions per second — was not achievable on public Ethereum without Layer-2 infrastructure that did not yet exist in production form.

These were infrastructure constraints, not design flaws in EXTC. The contract logic was correct. The underlying blockchain could not yet support payment volume at financial-industry scale.

## The Ideas That Reached Production

Several design patterns from EXTC were validated by subsequent development:

**Atomic token transfer with receiver notification** — the core ERC-223 property — became the basis for ERC-777 (2019), which extended the notification model and was later incorporated into DeFi lending protocols. The `tokenFallback` pattern appears throughout modern DeFi architecture.

**Multi-signature authorisation for corporate disbursements** — the pattern of requiring multiple on-chain signatures before execution — became the standard model for DAO treasury management and institutional custody solutions. Gnosis Safe, launched in 2018, popularised this pattern at scale.

**Collateral-backed instant loans without intermediaries** — the mechanism of locking collateral in escrow and releasing loan proceeds atomically — is the fundamental design of DeFi lending protocols such as Compound (2018) and Aave (2020).

**Block-height time locks for scheduled payments** — the pattern of encoding future execution timing in the contract — appears in token vesting contracts, delayed governance proposals, and time-weighted average price (TWAP) oracle designs across the DeFi ecosystem.

The EXTC experiment did not reach production scale. The infrastructure required to make the design viable took three to five more years to mature. The design questions it asked were the right ones for 2018.

## Frequently Asked Questions

**Why was ERC-223 never adopted as the dominant token standard despite fixing ERC-20's flaw?**

ERC-223 required recipient contracts to implement `tokenFallback`, breaking backwards compatibility with the thousands of contracts already deployed for ERC-20 tokens. The existing ERC-20 ecosystem was too large to migrate. Subsequent proposals — notably ERC-777 and ERC-1363 — addressed the same problem with different compatibility trade-offs, but ERC-20 remained dominant through a combination of network effects and the introduction of wrapped token patterns that avoided the silent-loss scenario.

**What happened to the EXTC token and platform?**

EXTC was a proof-of-concept and early research project from 2018. The wider ICO and payment token market contracted sharply through 2018–2019 as Ethereum scalability limits and regulatory uncertainty became clear. The ideas embedded in the EXTC design resurfaced in later protocols that had access to Layer-2 infrastructure, better tooling, and clearer regulatory frameworks.

**How does EXTC's collateral loan model compare to modern DeFi protocols like Aave?**

The core mechanism is the same: lock collateral, receive a loan sized against an LTV ratio, repay or face liquidation. The differences are: (1) modern DeFi protocols use oracle price feeds for dynamic LTV rather than fixed ratios; (2) they use algorithmic interest rates that respond to pool utilisation; (3) they operate on Layer-2 networks with gas costs 10–100 times lower than 2018 mainnet; (4) Aave and Compound have undergone formal security audits and held billions of dollars in liquidity, providing empirical validation that the basic model is sound.

**What were the Solidity version constraints in early 2018?**

The EXTC contract was written for Solidity 0.4.x, the dominant version in early 2018. Solidity 0.4 lacked many safety features introduced in later versions: integer overflow checking (added automatically in 0.8.0), `require`/`revert` with error messages (limited in 0.4), and explicit function visibility (default was public in 0.4). The contract relied on OpenZeppelin's SafeMath library to guard against overflow, a common pattern before the compiler enforced this natively.

## References

- Ethereum Foundation, (2015). [EIP-20: Token Standard ⧉](https://eips.ethereum.org/EIPS/eip-20 "EIP-20 Token Standard").
- Dexaran, Ethereum GitHub, (2017). [ERC-223 Token Standard Proposal ⧉](https://github.com/ethereum/EIPs/issues/223 "ERC-223 discussion").
- OpenZeppelin, (2018). [OpenZeppelin Contracts — SafeMath ⧉](https://github.com/OpenZeppelin/openzeppelin-contracts "OpenZeppelin Contracts").
- Ethereum Foundation, (2014). [Ethereum Whitepaper ⧉](https://ethereum.org/whitepaper "Ethereum Whitepaper").

<!-- enrich-start -->
<aside class="author-card" aria-label="About the author"><img alt="Portrait of Sebastien Rousseau" src="https://cloudcdn.pro/stocks/images/sebastien-rousseau.png" width="64" height="64" loading="lazy" decoding="async" /><span class="author-card-body"><strong class="author-card-name"><a href="/about/index.html">Sebastien Rousseau</a></strong><span class="author-card-bio">Senior banking technologist writing on applied AI, ISO 20022 migration, post-quantum cryptography for financial services, and the structural transformation of wholesale payments.</span><span class="author-credentials">20+ years across HSBC Commercial &amp; Investment Bank, PayPal, Barclays, Shazam, AKQA, Virgin Group. <a href="/about/index.html">Full profile</a> &middot; <a href="https://www.linkedin.com/in/sebastienrousseau/" rel="external noopener">LinkedIn</a> &middot; <a href="https://github.com/sebastienrousseau" rel="external noopener">GitHub</a></span></span></aside>
<p class="post-reviewed">Last reviewed <time datetime="2026-06-06">2026-06-06</time>.</p>
<aside class="related-posts" aria-labelledby="related-heading">
<h2 id="related-heading" class="related-heading">Related reading</h2>
<div class="related-grid">
<article class="related-card"><a href="https://sebastienrousseau.com/2018-02-04-unveiling-a-new-cryptocurrency-and-offering-future-faster-payment-solution/index.html" class="related-media" aria-label="Unveiling a new Cryptocurrency and Faster Payment Solution" tabindex="-1"><img alt="Turned off laptop computer on top of brown wooden table" src="https://cloudcdn.pro/stocks/images/laureen-missaire-DBbuhMbAIsQ.webp" loading="lazy" decoding="async" width="600" height="400" /></a><footer class="related-body"><h3><a href="https://sebastienrousseau.com/2018-02-04-unveiling-a-new-cryptocurrency-and-offering-future-faster-payment-solution/index.html">Unveiling a new Cryptocurrency and Faster Payment Solution</a></h3><p><time datetime="2018-02-04">2018-02-04</time></p></footer></article>
<article class="related-card"><a href="https://sebastienrousseau.com/2018-01-09-understanding-the-technology-behind-blockchain/index.html" class="related-media" aria-label="Understanding the Technology behind Blockchain" tabindex="-1"><img alt="Abstract digital ledger blocks connected by light trails on dark background" src="https://cloudcdn.pro/stocks/images/adam-smigielski-K5mPtONmpHM.webp" loading="lazy" decoding="async" width="600" height="400" /></a><footer class="related-body"><h3><a href="https://sebastienrousseau.com/2018-01-09-understanding-the-technology-behind-blockchain/index.html">Understanding the Technology behind Blockchain</a></h3><p><time datetime="2018-01-09">2018-01-09</time></p></footer></article>
<article class="related-card"><a href="https://sebastienrousseau.com/2026-05-15-blackrock-brsrv-bstbl-genius-act-tokenised-mmf" class="related-media" aria-label="Stablecoin Yield by Another Name: BlackRock's BRSRV and BSTBL Filings Decoded" tabindex="-1"><img alt="BlackRock tokenised money market fund architecture diagram — BRSRV OnChain Shares and BSTBL ERC-20 share class with GENIUS Act reserve flows" src="https://cloudcdn.pro/stocks/images/alev-takil-7ojyp-IXW7w-unsplash.webp" loading="lazy" decoding="async" width="600" height="400" /></a><footer class="related-body"><h3><a href="https://sebastienrousseau.com/2026-05-15-blackrock-brsrv-bstbl-genius-act-tokenised-mmf">Stablecoin Yield by Another Name: BlackRock's BRSRV and BSTBL Filings Decoded</a></h3><p><time datetime="2026-05-15">2026-05-15</time></p></footer></article>
</div>
</aside>
<!-- enrich-end -->
