---

# Front Matter (YAML)

author: "contact@sebastienrousseau.com (Sebastien Rousseau)"
banner_alt: "Abstract digital ledger blocks connected by light trails on dark background"
banner_height: "100vh"
banner_width: "100vw"
banner: "https://cloudcdn.pro/stocks/images/adam-smigielski-K5mPtONmpHM.webp"
cdn: "https://cloudcdn.pro/clients"
changefreq: "weekly"
charset: "UTF-8"
cname: "sebastienrousseau.com"
copyright: "© Copyright 2007 - 2026 - Sebastien Rousseau. All rights reserved."
date: "Jan 09, 2018"
description: "A technical introduction to how blockchain works: cryptographic hash chains, Merkle trees, distributed consensus, and why Ethereum's programmable layer transformed a payments ledger into a platform for smart contracts and tokenised assets."
format-detection: "telephone=no"
hreflang: "en"
icon: "https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/sebastienrousseau.svg"
id: "https://sebastienrousseau.com/2018-01-09-understanding-the-technology-behind-blockchain/index.html"
image_alt: "Black and White Portrait of Sebastien Rousseau"
image_height: "162"
image_width: "162"
image: "https://cloudcdn.pro/stocks/images/sebastien-rousseau.png"
keywords: "blockchain technology, cryptographic hash, Merkle tree, distributed consensus, proof of work, Ethereum, smart contracts, EVM, Solidity, ERC-20, distributed ledger, decentralised finance"
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
permalink: "https://sebastienrousseau.com/2018-01-09-understanding-the-technology-behind-blockchain/index.html"
rating: "general"
referrer: "no-referrer"
revisit-after: "7 days"
robots: "index, follow"
short_name: "sebastienrousseau"
subtitle: "A practical walk-through of the cryptography and consensus behind blockchain."
tags: "blockchain, Ethereum, smart contracts, cryptography, Merkle tree, consensus mechanism, proof of work, EVM, Solidity, ERC-20, decentralised finance, ISO 20022, post-quantum cryptography, AI, stablecoins, tokenised deposits"
theme-color: "0, 67, 165"
title: "Understanding the Technology behind Blockchain"
url: "https://sebastienrousseau.com/2018-01-09-understanding-the-technology-behind-blockchain/index.html"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"

# RSS - The RSS feed front matter (YAML).
atom_link: "https://sebastienrousseau.com/2018-01-09-understanding-the-technology-behind-blockchain/rss.xml"
category: "Blockchain"
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.26)"
item_description: "A technical introduction to blockchain: cryptographic hash chains, Merkle trees, distributed consensus, and how Ethereum extended a payments ledger into a programmable platform."
item_guid: "https://sebastienrousseau.com/2018-01-09-understanding-the-technology-behind-blockchain/rss.xml"
item_link: "https://sebastienrousseau.com/2018-01-09-understanding-the-technology-behind-blockchain/rss.xml"
item_pub_date: "Tue, 09 Jan 2018 09:09:00 +0000"
item_title: "Understanding the Technology behind Blockchain"
last_build_date: "Tue, 09 Jan 2018 09:09:00 +0000"
managing_editor: "contact@sebastienrousseau.com (Sebastien Rousseau)"
pub_date: "Tue, 09 Jan 2018 09:09:00 +0000"
ttl: "60"
type: "website"
webmaster: "contact@sebastienrousseau.com"

# Apple - The Apple front matter (YAML).
apple_mobile_web_app_orientations: "portrait"
apple_touch_icon_sizes: "192x192"
apple-mobile-web-app-capable: "yes"
apple-mobile-web-app-status-bar-inset: "black"
apple-mobile-web-app-status-bar-style: "black-translucent"
apple-mobile-web-app-title: "Blockchain Tech"
apple-touch-fullscreen: "yes"

# MS Application - The MS Application front matter (YAML).

msapplication-navbutton-color: "0, 67, 165"

# Twitter Card - The Twitter Card front matter (YAML).

twitter_card: "summary"
twitter_creator: "@wwdseb"
twitter_description: "How blockchain works: cryptographic hash chains, Merkle trees, consensus mechanisms, and how Ethereum turned a ledger into a programmable platform."
twitter_image: "https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/sebastienrousseau.svg"
twitter_image_alt: "Logo of Sebastien Rousseau"
twitter_site: "@wwdseb"
twitter_title: "Understanding the Technology behind Blockchain"
twitter_url: "https://sebastienrousseau.com"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://sebastienrousseau.com"
author_twitter: "@wwdseb"
author_location: "London, UK"
thanks: "Thanks for reading!"
site_last_updated: "2023-07-05"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "Kaishi, Kaishi Builder, Kaishi CLI, Kaishi Templates, Kaishi Themes"
site_software: "Static Site Generator, Rust"

excerpt: "Blockchain is an append-only ledger secured by cryptographic hash chains and distributed consensus — a design that makes tampering computationally expensive and auditable by anyone. Ethereum extended this foundation with a programmable execution layer, turning a simple payments record into a platform for smart contracts, tokens, and decentralised finance."
last_reviewed: "2026-05-24"
---


<!-- lead-start -->
<aside class="post-lead" aria-label="Article summary">
<p class="post-lead-tldr"><strong>TL;DR.</strong> A technical introduction to how blockchain works: cryptographic hash chains, Merkle trees, distributed consensus, and why Ethereum's programmable layer transformed a payments ledger into a platform for smart contracts and tokenised assets.</p>
<p class="post-lead-heading"><strong>Key takeaways</strong></p>
<ul class="post-lead-takeaways">
  <li><strong>The Problem Blockchain Solved.</strong> Before Bitcoin, digital payments required a trusted intermediary — a bank, payment processor, or clearing house — to prevent double-spending.</li>
  <li><strong>The Cryptographic Building Blocks.</strong> Blockchain technology assembles three pre-existing cryptographic primitives into a new architecture:.</li>
  <li><strong>How the Bitcoin Blockchain Works.</strong> A Bitcoin block contains three logical components:.</li>
  <li><strong>Ethereum's Programmable Layer.</strong> Ethereum generalised Bitcoin's transaction model from "transfer value" to "execute code." The key additions:.</li>
</ul>
<p class="post-lead-related"><strong>Related reading:</strong> <a href="https://sebastienrousseau.com/2018-02-15-the-making-of-the-express-transaction-credits-platform/index.html">The making of the Express Transaction Credits Platform</a>, <a href="https://sebastienrousseau.com/2018-02-04-unveiling-a-new-cryptocurrency-and-offering-future-faster-payment-solution/index.html">Unveiling a new Cryptocurrency and Faster Payment Solution</a>, <a href="https://sebastienrousseau.com/2018-01-24-the-erc-20-token-standard/index.html">ERC-20: The Ethereum Token Interface That Changed the World</a>.</p>
</aside>
<!-- lead-end -->

![Abstract digital ledger blocks connected by light trails on dark background](https://cloudcdn.pro/stocks/images/adam-smigielski-K5mPtONmpHM.webp).class=\"img-fluid clearfix\"

> **Executive Summary / Key Takeaways**
>
> - **The problem.** Digital cash requires solving the double-spend problem: preventing the same unit from being spent twice without a trusted clearinghouse. Bitcoin's 2008 whitepaper solved this by replacing trusted intermediaries with cryptographic proof and distributed consensus ([Nakamoto, 2008](https://bitcoin.org/bitcoin.pdf "Bitcoin: A Peer-to-Peer Electronic Cash System")).
> - **The data structure.** A blockchain is a linked list of blocks where each block header contains the SHA-256 hash of the previous header. The hash chain makes history append-only: altering any past block invalidates every subsequent hash, forcing an attacker to redo all subsequent proof-of-work.
> - **Merkle trees.** Transactions within a block are hashed into a binary Merkle tree. The root hash, stored in the block header, allows efficient verification of any individual transaction without downloading the full block — the basis for lightweight SPV clients.
> - **Ethereum's extension.** Ethereum's Yellow Paper (2014) introduced the EVM — a deterministic stack machine running on every full node. Smart contracts are bytecode deployed to the chain; they execute identically on all nodes and settle atomically, replacing trusted intermediaries with self-enforcing code ([Wood, 2014](https://ethereum.github.io/yellowpaper/paper.pdf "Ethereum Yellow Paper")).
> - **Practical significance.** Every tokenised asset, stablecoin, and DeFi protocol deployed since 2017 runs on these foundations. Understanding the hash chain, the Merkle tree, and the EVM execution model is the prerequisite for working with any Ethereum-based system.

---

## The Problem Blockchain Solved

Before Bitcoin, digital payments required a trusted intermediary — a bank, payment processor, or clearing house — to prevent double-spending. If Alice sent a digital file representing £10 to Bob, nothing in the file itself stopped her from sending an identical copy to Carol. The solution in every existing system was centralised record-keeping: the bank's ledger said the money was spent, so it could not be spent again.

Bitcoin's contribution was to replace that trusted ledger with a distributed one in which the record of all transactions is replicated across thousands of independent nodes. Mutual distrust between nodes was converted into security through two mechanisms:

1. **Cryptographic linking.** Each block of transactions contains the hash of the previous block. A hash function is a one-way deterministic mapping: given any input, the function produces a fixed-length output, and changing even one bit of the input produces a completely different output. This means any alteration to a historical block invalidates every block after it.

2. **Proof-of-work consensus.** Adding a new block requires finding a nonce value such that the block's hash falls below a target threshold — computationally expensive to find, trivially cheap to verify. This makes rewriting history proportionally expensive to the depth of the block being altered, because an attacker must redo all the proof-of-work from that block to the chain tip.

The combination means that the longest chain with the most cumulative proof-of-work is, by construction, the one maintained by honest participants spending real resources.

## The Cryptographic Building Blocks

Blockchain technology assembles three pre-existing cryptographic primitives into a new architecture:

### SHA-256 Hash Functions

SHA-256 (Secure Hash Algorithm 256-bit) is a member of the SHA-2 family standardised by NIST. It takes an arbitrary-length input and produces a 256-bit output. Key properties for blockchain use:

- **Deterministic.** The same input always produces the same output.
- **Pre-image resistance.** Given a hash output, it is computationally infeasible to reconstruct the input.
- **Avalanche effect.** Changing one bit of input changes roughly half the output bits, making brute-force search inefficient.
- **Collision resistance.** It is computationally infeasible to find two different inputs that produce the same hash.

Bitcoin applies SHA-256 twice (SHA-256d) for added security against length-extension attacks. Ethereum uses Keccak-256, a SHA-3 finalist variant.

### Merkle Trees

A Merkle tree is a binary tree of hashes. Each leaf node is the hash of a transaction. Each internal node is the hash of its two children. The root — the Merkle root — summarises all transactions in the block in a single 32-byte value stored in the block header.

The practical consequence: to verify that a specific transaction is included in a block, you only need `log₂(n)` hashes, not all `n` transactions. For a block with 2,000 transactions, verification requires 11 hashes rather than 2,000 — the basis for Simplified Payment Verification (SPV) in lightweight clients.

### Digital Signatures (ECDSA)

Transaction authorisation in Bitcoin and Ethereum uses the Elliptic Curve Digital Signature Algorithm (ECDSA) over the secp256k1 curve. A private key signs a transaction; any node can verify the signature using the corresponding public key without knowing the private key. This ensures that only the holder of the private key can authorise a spend from an address.

Ethereum addresses are the last 20 bytes of the Keccak-256 hash of the public key — a derivation that makes addresses compact and portable while remaining cryptographically tied to the key pair.

## How the Bitcoin Blockchain Works

A Bitcoin block contains three logical components:

**The block header** — 80 bytes comprising: the protocol version, the hash of the previous block header, the Merkle root of transactions, a Unix timestamp, the current difficulty target, and the nonce. Miners iterate the nonce (and sometimes the timestamp or extra-nonce in the coinbase transaction) until the double-SHA-256 hash of the header falls below the difficulty target.

**The transaction list** — the ordered set of transactions included in the block. The coinbase transaction (the first) assigns the block reward and transaction fees to the miner's address.

**The chain** — the linkage of headers. The cumulative proof-of-work in the chain (the sum of all work done to produce every block) determines which fork is the canonical chain. Nodes always follow the chain with the most cumulative work.

Block time is targeted at 10 minutes for Bitcoin. Difficulty adjusts every 2,016 blocks (approximately two weeks) to maintain that target as total network hash rate changes.

## Ethereum's Programmable Layer

Ethereum generalised Bitcoin's transaction model from "transfer value" to "execute code." The key additions:

**The Ethereum Virtual Machine (EVM).** A 256-bit word, stack-based virtual machine that executes deterministically on all full nodes. Every opcode has an explicit gas cost. Computation is bounded by the block gas limit, preventing infinite loops from halting the network. All nodes executing the same bytecode on the same state must produce the same output — this consensus on execution is what makes smart contracts trustless.

**Accounts.** Ethereum has two account types: Externally Owned Accounts (EOAs) controlled by private keys, and Contract Accounts whose code is stored on-chain. A transaction sent to a contract address triggers the contract's bytecode execution.

**State.** Ethereum's global state is a mapping of addresses to account states (nonce, balance, storage, code hash). The state root — a Merkle Patricia trie of all account states — is included in each block header, allowing efficient proof of any account's state at any block height.

**Gas.** Users pay gas (in ETH) for every EVM operation. Gas serves two functions: it compensates miners/validators for computation, and it caps the resources any single transaction can consume, preventing denial-of-service attacks via expensive operations.

## Writing Smart Contracts in Solidity

Solidity is a statically-typed, contract-oriented language that compiles to EVM bytecode. A minimal token contract illustrates the core concepts:

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

Key observations: `mapping(address => uint256)` is an EVM storage layout, not an in-memory data structure — reads and writes cost gas. `require` reverts the entire transaction on failure, returning unused gas. `event Transfer` emits a log that off-chain indexers use to track transfers without re-reading full state. The `constructor` runs once at deployment; subsequent calls go to the named functions.

The ERC-20 standard formalised a common interface for fungible tokens — `transfer`, `transferFrom`, `approve`, `allowance`, `balanceOf`, `totalSupply` — allowing any ERC-20-compliant token to work with any ERC-20-aware exchange or wallet without custom integration.

## From Ledger to Financial Infrastructure

The blockchain primitives described here — hash chains, Merkle trees, the EVM, and ERC-20 — became the foundation for a broader set of financial applications between 2018 and 2026:

**Decentralised Finance (DeFi).** Lending protocols (Compound, Aave), automated market makers (Uniswap), and yield aggregators all run as EVM smart contracts. They replace the clearing, custody, and settlement functions of traditional financial intermediaries with self-executing code and on-chain liquidity pools.

**Tokenised Assets.** Central banks and commercial banks are piloting tokenised deposits, tokenised bonds, and tokenised money market funds on permissioned variants of EVM-compatible chains. The underlying mechanics — hash-secured state transitions, atomic settlement, programmable transfer rules — are direct descendants of the 2014 Ethereum architecture.

**Central Bank Digital Currencies.** The Bank of England's wholesale CBDC research, the ECB's digital euro programme, and Project Agorá all explore DLT architectures derived from or compatible with the foundational designs in Bitcoin and Ethereum. The consensus and hash-chain structures remain relevant even where the permissioning and governance model differs entirely from public blockchains.

The journey from the 2008 Bitcoin whitepaper to 2026 tokenised finance spans two decades, but it runs on a coherent technical lineage. Understanding how a SHA-256 hash chain enforces immutability, how a Merkle tree enables efficient verification, and how the EVM executes smart contracts atomically is the prerequisite for evaluating any claim about what blockchain can and cannot do in regulated financial services.

## Frequently Asked Questions

**What is the difference between a blockchain and a distributed database?**

A traditional distributed database replicates data across nodes for availability and performance, but trust is centralised — an administrator can modify records. A blockchain makes tampering computationally expensive through hash chaining and consensus: modifying any historical record requires redoing all subsequent proof-of-work or proof-of-stake, and convincing the network to accept the altered fork. The distinguishing property is tamper-evidence enforced by cryptography and incentive design rather than by access controls.

**Why does Ethereum use Keccak-256 rather than SHA-256?**

Ethereum adopted Keccak-256 (the SHA-3 finalist before NIST standardisation adjustments) partly because its designers wanted independence from the SHA-2 lineage that Bitcoin already depended on. Keccak also has different algebraic properties that made it attractive for certain EVM operations. The practical effect for developers is that Ethereum address derivation and storage slot hashing use Keccak-256, not SHA-256d as in Bitcoin.

**What does "gas" prevent in the EVM?**

Gas prevents two categories of attack. First, it prevents denial-of-service via computationally expensive operations: every opcode costs gas, so an attacker cannot force the network to execute infinite loops at no cost. Second, the block gas limit caps total computation per block, ensuring that block validation time remains bounded and predictable for full nodes. Without gas, a single contract call could halt the network by executing unbounded computation.

**How does proof-of-stake change the security model compared to proof-of-work?**

In proof-of-work, security is provided by energy expenditure: attacking the chain requires controlling more than 50% of the network's hash rate, which means controlling more than 50% of its physical hardware and power. In proof-of-stake (used by Ethereum since the Merge in 2022), security is provided by economic stake: validators lock ETH as collateral, which is slashed if they sign conflicting blocks. A 51% attack requires acquiring and risking more than 50% of all staked ETH — a capital cost rather than a hardware and energy cost. The security model is different but mathematically comparable in economic terms under the assumption that rational validators prefer fee income to capital destruction.

## References

- Nakamoto, S., (2008). [Bitcoin: A Peer-to-Peer Electronic Cash System ⧉](https://bitcoin.org/bitcoin.pdf "Bitcoin Whitepaper").
- Buterin, V., (2014). [Ethereum: A Next-Generation Smart Contract and Decentralised Application Platform ⧉](https://ethereum.org/whitepaper "Ethereum Whitepaper").
- Wood, G., (2014). [Ethereum: A Secure Decentralised Generalised Transaction Ledger ⧉](https://ethereum.github.io/yellowpaper/paper.pdf "Ethereum Yellow Paper").
- NIST, (2015). [SHA-3 Standard: Permutation-Based Hash and Extendable-Output Functions ⧉](https://www.nist.gov/publications/sha-3-standard-permutation-based-hash-and-extendable-output-functions "NIST FIPS 202").

<!-- enrich-start -->
<aside class="author-card" aria-label="About the author"><img alt="Portrait of Sebastien Rousseau" src="https://cloudcdn.pro/stocks/images/sebastien-rousseau.png" width="64" height="64" loading="lazy" decoding="async" /><span class="author-card-body"><strong class="author-card-name"><a href="/about/index.html">Sebastien Rousseau</a></strong><span class="author-card-bio">Senior banking technologist writing on applied AI, ISO 20022 migration, post-quantum cryptography for financial services, and the structural transformation of wholesale payments.</span><span class="author-credentials">20+ years across HSBC Commercial &amp; Investment Bank, PayPal, Barclays, Shazam, AKQA, Virgin Group. <a href="/about/index.html">Full profile</a> &middot; <a href="https://www.linkedin.com/in/sebastienrousseau/" rel="external noopener">LinkedIn</a> &middot; <a href="https://github.com/sebastienrousseau" rel="external noopener">GitHub</a></span></span></aside>
<p class="post-reviewed">Last reviewed <time datetime="2026-06-06">2026-06-06</time>.</p>
<aside class="related-posts" aria-labelledby="related-heading">
<h2 id="related-heading" class="related-heading">Related reading</h2>
<div class="related-grid">
<article class="related-card"><a href="https://sebastienrousseau.com/2018-02-15-the-making-of-the-express-transaction-credits-platform/index.html" class="related-media" aria-label="The making of the Express Transaction Credits Platform" tabindex="-1"><img alt="Giant white pillars" src="https://cloudcdn.pro/stocks/images/tarik-haiga-3637943.webp" loading="lazy" decoding="async" width="600" height="400" /></a><footer class="related-body"><h3><a href="https://sebastienrousseau.com/2018-02-15-the-making-of-the-express-transaction-credits-platform/index.html">The making of the Express Transaction Credits Platform</a></h3><p><time datetime="2018-02-15">2018-02-15</time></p></footer></article>
<article class="related-card"><a href="https://sebastienrousseau.com/2018-02-04-unveiling-a-new-cryptocurrency-and-offering-future-faster-payment-solution/index.html" class="related-media" aria-label="Unveiling a new Cryptocurrency and Faster Payment Solution" tabindex="-1"><img alt="Turned off laptop computer on top of brown wooden table" src="https://cloudcdn.pro/stocks/images/laureen-missaire-DBbuhMbAIsQ.webp" loading="lazy" decoding="async" width="600" height="400" /></a><footer class="related-body"><h3><a href="https://sebastienrousseau.com/2018-02-04-unveiling-a-new-cryptocurrency-and-offering-future-faster-payment-solution/index.html">Unveiling a new Cryptocurrency and Faster Payment Solution</a></h3><p><time datetime="2018-02-04">2018-02-04</time></p></footer></article>
<article class="related-card"><a href="https://sebastienrousseau.com/2018-01-24-the-erc-20-token-standard/index.html" class="related-media" aria-label="ERC-20: The Ethereum Token Interface That Changed the World" tabindex="-1"><img alt="Turned off laptop computer on top of brown wooden table" src="https://cloudcdn.pro/stocks/images/m-ZzOa5G8hSPI.webp" loading="lazy" decoding="async" width="600" height="400" /></a><footer class="related-body"><h3><a href="https://sebastienrousseau.com/2018-01-24-the-erc-20-token-standard/index.html">ERC-20: The Ethereum Token Interface That Changed the World</a></h3><p><time datetime="2018-01-24">2018-01-24</time></p></footer></article>
</div>
</aside>
<!-- enrich-end -->
