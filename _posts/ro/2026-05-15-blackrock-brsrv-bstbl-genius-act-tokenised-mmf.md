---
title: "Stablecoin Yield by Another Name: BlackRock's BRSRV and BSTBL Filings Decoded"
subtitle: "Stablecoins cannot pay yield under the GENIUS Act. On 8 May 2026, BlackRock filed two products that are not, legally, stablecoins — and that can pay yield, in a wallet, on a public blockchain."
description: "Stablecoins cannot pay yield under the GENIUS Act. On 8 May 2026, BlackRock filed two SEC registrations for products that solve this constraint by being regulated as money market funds rather than stablecoins — while behaving, in the wallet, like yield-bearing dollars. A close reading of BRSRV, BSTBL, and the OCC rulemaking they respond to."
date: "May 15, 2026"
language: "ro-RO"
locale: "ro_RO"
banner: "https://cloudcdn.pro/stocks/images/alev-takil-7ojyp-IXW7w-unsplash.webp"
banner_alt: "BlackRock tokenised money market fund architecture diagram — BRSRV OnChain Shares and BSTBL ERC-20 share class with GENIUS Act reserve flows"
keywords: "BlackRock, BRSRV, BSTBL, BUIDL, GENIUS Act, OCC, stablecoin, tokenised money market fund, OnChain Shares, Securitize"
---

![BlackRock tokenised money market fund architecture diagram — BRSRV OnChain Shares and BSTBL ERC-20 share class with GENIUS Act reserve flows](https://cloudcdn.pro/stocks/images/alev-takil-7ojyp-IXW7w-unsplash.webp).class="img-fluid clearfix"

---

> **TL;DR.** Stablecoins cannot pay yield under the GENIUS Act. On 8 May 2026, BlackRock filed two SEC registrations for products that solve this constraint by being regulated as money market funds rather than stablecoins — while behaving, in the wallet, like yield-bearing dollars. A close reading of BRSRV, BSTBL, and the OCC rulemaking they respond to.
>
> **Concluzii cheie**
>
> - DRAFT translation: this article is a Română stub generated from the English source. Body text is intentionally left in English until a native reviewer signs off.
> - Source title: *Stablecoin Yield by Another Name: BlackRock's BRSRV and BSTBL Filings Decoded*.
> - Source subtitle: *Stablecoins cannot pay yield under the GENIUS Act. On 8 May 2026, BlackRock filed two products that are not, legally, stablecoins — and that can pay yield, in a wallet, on a public blockchain.*.
> - Editorial note: replace this block with hand-translated copy before flipping `active=True` for ro in `scripts/_lang_registry.py`.

---

Stablecoins cannot pay yield under the GENIUS Act. On 8 May 2026, BlackRock filed two SEC registrations for products that solve this constraint by being regulated as money market funds rather than stablecoins — while behaving, in the wallet, like yield-bearing dollars on a public blockchain.

---

> **Key Takeaways**
>
> - The **GENIUS Act**, signed in July 2025 and now in the final months of its rulemaking, prohibits payment stablecoin issuers from paying interest or yield to holders simply for holding, using, or keeping a stablecoin. The OCC's March 2026 proposal hardened this further with a rebuttable presumption that affiliate and third-party yield arrangements also violate the ban.
> - The economic problem this creates is straightforward. With approximately **$281 billion in payment stablecoins outstanding** and Treasury yields at multi-year highs, the gap between what a wallet holder receives (zero) and what the underlying reserves earn (~4–5%) is now in the tens of billions of dollars annually.
> - On **8 May 2026, BlackRock filed two SEC registration statements** that capture this gap without violating the yield prohibition — because neither product is, legally, a stablecoin.
> - **BRSRV** (BlackRock Daily Reinvestment Stablecoin Reserve Vehicle) is a new money market fund holding cash, sub-93-day Treasuries, and overnight Treasury repos. It issues "OnChain Shares" through a permissioned multi-chain framework with Securitize Transfer Agent LLC as the legal record of ownership. Minimum investment: $3 million. It is engineered to qualify as an eligible reserve asset under the GENIUS Act.
> - **BSTBL** is the more architecturally significant filing. It bolts an ERC-20 share class onto BlackRock's existing **$6–7 billion Select Treasury Based Liquidity Fund**, with BNY Mellon Investment Servicing as transfer agent, recording shareholders on Ethereum. It is the first time a public-Ethereum share class has been added to an existing BlackRock money-market product.
> - The pattern is now visible across the industry. **Tokenised money market funds are the architecture that the GENIUS Act, by prohibiting yield on stablecoins, made inevitable.** The $14 billion tokenised Treasury market — led by BlackRock's BUIDL at roughly 40% share — is the early read on where the next wave of "wallet dollars" sits.

---

## A Filing That Is Also a Policy Position

The two BlackRock filings of 8 May 2026 did not arrive in a vacuum. They arrived one week after BlackRock submitted a [seventeen-page comment letter ⧉](https://www.theblock.co/post/399812/blackrock-urges-occ-to-drop-tokenized-reserve-cap-idea-expand-eligible-assets-in-genius-act-comment-letter "BlackRock urges OCC to drop tokenized reserve cap idea, expand eligible assets in GENIUS Act comment letter") to the Office of the Comptroller of the Currency on the final day of the comment window for its GENIUS Act implementing rules — and four days after [BlackRock published a public summary on X ⧉](https://beincrypto.com/blackrock-occ-stablecoin-genius-act-comment/ "BlackRock Backs OCC Stablecoin Rules Under GENIUS Act") of its seven core recommendations to the agency.

The recommendations and the new filings are best read as one document in two parts. The comment letter argued that the OCC should drop its proposed 20% cap on tokenised reserve assets, confirm that qualifying ETFs receive the same treatment as government money market funds, and allow same-day-settling GMMFs to count toward the weekly liquidity floor. The filings, four days later, registered the exact instruments that benefit from those positions: a new fund (BRSRV) explicitly engineered to qualify as an eligible reserve under the GENIUS Act, and a tokenised share class (BSTBL) on top of the firm's existing $6–7 billion Treasury liquidity fund. Whether or not the OCC adopts BlackRock's positions in the final rule, the firm has now placed its products in the policy debate with the kind of specificity that is hard for a regulator to ignore.

This is the strategic backdrop for what, at first read, looks like a clever piece of legal engineering. It is more accurately read as the largest asset manager in the world declaring where the line between a "stablecoin" and a "tokenised security" should sit in US law — and registering the products that will live on either side of that line.

## Why Stablecoins Cannot Pay Yield

The GENIUS Act, signed in July 2025 and now the basis of overlapping OCC, FDIC, and Federal Reserve rulemakings, draws an unusually clean conceptual distinction. A "payment stablecoin" under the Act is a digital asset designed to maintain a stable value relative to a fiat currency, backed by high-quality reserves, redeemable at par. A "permitted payment stablecoin issuer" (PPSI) is a federally or state-chartered entity authorised to issue such a token. And the [Act's section 4(a)(11) ⧉](https://www.lw.com/en/insights/occ-issues-proposal-to-implement-the-genius-act "OCC Issues Proposal to Implement the GENIUS Act") prohibits any PPSI from paying interest or yield to holders solely for holding, using, or keeping the stablecoin.

The OCC's March 2026 [proposed rule ⧉](https://www.nixonpeabody.com/insights/alerts/2026/04/02/proposed-occ-regulations-for-payment-stablecoins-under-the-genius-act "Proposed OCC regulations for payment stablecoins under the GENIUS Act") extended this prohibition operationally. It established a rebuttable presumption that arrangements routing yield through an affiliate or related third party — for example, a crypto exchange paying "loyalty rewards" to holders of a particular stablecoin — also violate the ban, with the burden on the issuer to demonstrate otherwise. White-label arrangements, in which a PPSI issues digital assets branded by a partner that then pays yield, are explicitly treated as presumptively evasive. The Office of the Comptroller [signalled in early 2026 ⧉](https://www.compliancecorylated.com/news/us-occ-closes-genius-act-loophole-allowing-yield-bearing-stablecoins/ "US OCC closes GENIUS Act loophole allowing yield-bearing stablecoins") that the "loophole" framing of the issuer-pays-via-affiliate model would not survive final rulemaking in any permissive form.

The economic rationale for this prohibition is contested. Banking-industry submissions to the OCC argued for the strict prohibition on the basis that yield-bearing stablecoins would drain transactional bank deposits — a market estimated by the [US Treasury advisory council at approximately $6.6 trillion ⧉](https://www.congress.gov/crs-product/IF13174 "The Stablecoin Yield Debate — Congressional Research Service"), of which a meaningful share is "at risk" from competition with yield-bearing dollar-substitutes. Crypto-industry submissions, led by Coinbase, argued the opposite: that incentives are central to competition in payments, and that a broad ban would impose net welfare costs without materially affecting bank lending.

Whichever side has the better policy argument, the legal result for now is settled: a stablecoin in the regulatory sense of the GENIUS Act cannot pay its holder yield. What it cannot do, however, is define what a holder can do with their money next. And here the architecture diverges.

## The Architecture of BRSRV

The BlackRock Daily Reinvestment Stablecoin Reserve Vehicle is, in its plumbing, an unremarkable money market fund. It holds cash, US Treasury securities with maturities of 93 days or less, and overnight repurchase agreements backed by Treasuries. It is aligned with Rule 2a-7 under the Investment Company Act of 1940 — the same regulatory architecture that has governed institutional money market funds for four decades. Its yield, like every other government MMF, derives from the prevailing short-Treasury rate.

What is novel is the share class. BRSRV shares are issued as ["OnChain Shares" through a permissioned framework ⧉](https://unchainedcrypto.com/blackrock-files-for-two-new-tokenized-money-market-funds-targeting-stablecoin-capital/ "BlackRock Files for Two New Tokenized Money-Market Funds Targeting Stablecoin Capital") that connects to multiple public blockchains, with [Securitize Transfer Agent LLC serving as the official transfer agent ⧉](https://www.crowdfundinsider.com/2026/05/278346-blackrock-focuses-on-tokenization-initiatives-with-blockchain-enabled-funds/ "BlackRock Focuses On Tokenization Initiatives With Blockchain Enabled Funds"). Off-chain identity systems — the same kind of KYC infrastructure that backs BlackRock's existing $2.9 billion [BUIDL fund ⧉](https://stablecoininsider.org/top-10-tokenized-treasury-funds-in-2026-buidl-benji-and-the-highest-yielding-on-chain-options/ "Top 10 Tokenized Treasury Funds in 2026") — link wallet addresses to verified investors. Minimum investment: $3 million. The filing does not yet name which blockchains the fund will support at launch.

The product is explicitly engineered, [as multiple sources have noted ⧉](https://cryptobriefing.com/blackrock-tokenized-money-market-funds-stablecoins/ "BlackRock doubles down on tokenization with new stablecoin reserve funds"), to qualify as an eligible reserve asset under the GENIUS Act. The target buyer is not a retail wallet user. It is a stablecoin issuer (or a treasury operation that holds stablecoins as part of a working-capital strategy) that needs a Treasury-yielding instrument it can hold programmatically on the same blockchain rails as the stablecoins themselves. The pitch, simplified to a single sentence, is: keep your reserves on chain, earn the Treasury yield, satisfy the regulator.

For BlackRock, the strategic position is sharper than it appears. Its existing BUIDL fund already backs more than 90% of the reserves of two of the largest "yield-bearing" stablecoin-adjacent products — Ethena's USDtb and Solana-based Jupiter's JupUSD. BRSRV is the dedicated, GENIUS-aware extension of that role: the wholesale Treasury-yield product purpose-built for the reserve-management workflow of every PPSI that will exist under the new regime.

## The Architecture of BSTBL

The second filing is operationally more interesting and architecturally more important. BSTBL — the on-chain share class for the existing BlackRock Select Treasury Based Liquidity Fund — is not a new fund. It is a new share class layered onto a money market product that already manages approximately $6–7 billion in assets, was [retooled in October 2025 into a GENIUS-compliant configuration ⧉](https://www.theblock.co/post/399812/blackrock-urges-occ-to-drop-tokenized-reserve-cap-idea-expand-eligible-assets-in-genius-act-comment-letter "BlackRock urges OCC to drop tokenized reserve cap idea") with a 5 p.m. ET trading deadline and a Treasury-heavy mandate, and is now being extended onto Ethereum as an ERC-20 token.

The transfer agent for this share class is [BNY Mellon Investment Servicing ⧉](https://www.mexc.com/news/1080472 "BlackRock files for two new tokenized funds with the U.S. SEC on Ethereum"), which will maintain the official shareholder records on Ethereum using the ERC-20 standard. Off-chain KYC infrastructure links wallets to investor identity records, as it does for BUIDL and for every other compliant tokenised fund in the market today. The substantive distinction from BRSRV is the chain (Ethereum, public, with the ERC-20 token as the share representation) and the transfer agent (BNY rather than Securitize) — and the fact that this is the first time a public-Ethereum share class has been bolted onto an existing BlackRock money-market fund.

That last detail is the one worth dwelling on. BlackRock's prior tokenised products — BUIDL most prominently — were structured as new funds with on-chain native architecture. BSTBL takes a different and arguably more consequential approach: tokenise an existing, large, conventional money market product by adding a new share class, rather than building a parallel structure. The implication is that any existing BlackRock MMF could, in principle, follow the same pattern. So could any existing competitor MMF — Vanguard's, Fidelity's, JPMorgan's, State Street's. The architectural barrier to tokenising the conventional money market fund industry is, after BSTBL, lower than it has ever been.

For an industry context: tokenised US Treasuries have grown from approximately $2 billion to [$14 billion as of May 2026 ⧉](https://www.mexc.com/news/1080472 "BlackRock files for two new tokenized funds with the U.S. SEC on Ethereum"), with BlackRock's BUIDL at roughly 40% market share, Franklin Templeton's BENJI/FOBXX at $850 million, and Ondo Finance's combined OUSG and USDY products in the second position. The next $50–100 billion is plausibly already in motion through filings like BSTBL.

## Payment Stablecoin vs Tokenised Money Market Fund: The Distinction That Matters

For a non-specialist reader, the distinction between a "stablecoin" and a "tokenised money market fund share" can look like a regulatory technicality. It is not. The two instruments occupy genuinely different positions in US securities law and the consequences flow through the entire product design.

| Dimension | Payment Stablecoin (under GENIUS Act) | Tokenised MMF Share (BRSRV / BSTBL pattern) |
|---|---|---|
| Legal status | Payment instrument | Security (fund share) |
| Governing regime | GENIUS Act; OCC/FDIC/Fed rulemakings | Investment Company Act 1940; Rule 2a-7 |
| Issuer | Permitted Payment Stablecoin Issuer (PPSI) | SEC-registered fund (and transfer agent) |
| Reserve requirements | Cash, short Treasuries, repos — strict | Cash, short Treasuries, repos — Rule 2a-7 |
| Can pay yield to holder | **No** (Section 4(a)(11)) | **Yes** (the yield is the return on the share) |
| Redemption | At par, on demand | At NAV, typically T+0 or T+1 |
| Record of ownership | Issuer wallet / on-chain | Transfer agent (legal); blockchain (operational) |
| Minimum investment | None (retail typical) | Substantial ($3M for BRSRV; institutional for BSTBL) |
| Composability with DeFi | High | High (BUIDL is precedent) |
| User experience in a wallet | Token that holds $1 | Token whose value accrues toward yield |
| Bank-deposit substitution risk | The central regulatory concern | Materially lower (security, not deposit-like) |

*Source: Synthesis of GENIUS Act text, OCC March 2026 NPRM, BlackRock filings of 8 May 2026, and Rule 2a-7 framework.*

The bottom row is the one that explains the regulatory architecture. A payment stablecoin that pays yield looks, to a bank regulator, like a deposit substitute. A tokenised money market fund share that pays yield looks like a security — and securities competing with deposits is not a new concern, because conventional money market funds have done exactly that for forty years. The GENIUS Act draws its line at the deposit-substitute concern. Everything that sits clearly on the security side of that line is, by construction, outside the Act's yield prohibition.

## Is This a Loophole?

It is tempting — and the framing has surfaced widely on LinkedIn and crypto-Twitter since the filing — to call this a "loophole" in the GENIUS Act: stablecoins cannot pay yield, so BlackRock filed something that legally isn't a stablecoin. The framing captures the headline cleverly. As legal characterisation it understates the substance.

The yield prohibition in the GENIUS Act was a specific policy choice with a specific target: the deposit-substitution risk to the banking sector from a class of instrument designed to function as money. Tokenised money market funds are not designed to function as money; they are designed to function as fund shares, with all the regulatory weight (Rule 2a-7, audited reserves, NAV disclosure, transfer-agent legal records of ownership) that has applied to that category for decades. That those fund shares now happen to settle on Ethereum or another public chain does not change what they are in securities law. The OCC's own [proposed rule ⧉](https://www.morganlewis.com/pubs/2026/04/occs-genius-act-proposal-what-prospective-issuers-need-to-know "Stablecoin Regulation: OCC Proposal Under the GENIUS Act") explicitly contemplates tokenised reserves as a legitimate category — the open debate is the 20% cap, not the existence of the asset class.

What is genuinely novel is the user experience. A holder of a tokenised MMF share, in a wallet on a public chain, has something that *looks* like a stablecoin (a fungible token, transferable peer-to-peer, composable with DeFi infrastructure) but that *behaves* like a security (the NAV accrues, the holder is on a KYC list, the transfer agent's records are legally controlling). The headline framing — "legally isn't a stablecoin" — is correct as far as it goes. The deeper observation is that the GENIUS Act, by prohibiting yield on the payment-stablecoin category, effectively *required* the industry to converge on tokenised MMFs as the carrier for yield-bearing on-chain dollars. The Act drew a line; the industry, predictably, structured products that sit on the more favourable side of it. That is not a loophole. It is the design of the regulatory architecture working roughly as intended — even if the velocity at which it is producing institutional products is faster than most participants expected.

## What This Means by Sector

The implications of the 8 May filings are not uniform. The strategic response varies materially depending on where an institution sits in the value chain.

### Stablecoin Issuers (PPSIs)

For Circle, Tether, PayPal, and the next generation of bank-issued payment stablecoins, BRSRV is the operational answer to a question that has only had ad-hoc answers up to now: where do reserves sit when they need to be both Treasury-yielding and natively on the same chain as the issued stablecoin? Direct holding of T-bills works at issuance scale but is operationally heavy. Holding BUIDL works, but BUIDL's structure was not designed specifically around the GENIUS Act reserve framework. BRSRV is. The competitive consequence is that Circle, Tether, and bank-issued PPSIs now have a credible, GENIUS-engineered wholesale product to plug into their reserve management — and the marginal cost of switching reserves into a BlackRock product is, structurally, lower than it has ever been.

### Banks and Money Market Fund Operators

For banks that operate large money market fund franchises — JPMorgan, State Street, BNY Mellon, Northern Trust, Vanguard, Fidelity — BSTBL is the operational template for what their own products will likely have to do. The architectural pattern is now visible: take an existing MMF, register a new on-chain share class with the SEC, appoint a transfer agent to maintain shareholder records on Ethereum (or another major public chain), and gate access through off-chain KYC. The barrier to entry for a tokenised share class on an existing $10–50 billion MMF is, in the BSTBL pattern, principally regulatory and operational rather than technical. BNY Mellon's role as the transfer agent for BSTBL — recording shareholders on Ethereum using ERC-20 — is itself a signal that traditional transfer-agent infrastructure is being extended onto public chains by precisely the institutions that have managed the legal record of fund ownership for decades.

### DeFi Protocols and On-Chain Treasury

For DeFi protocols, BRSRV and BSTBL extend a pattern that BUIDL began: the migration of high-quality Treasury collateral from off-chain custodial accounts into on-chain instruments that can be composed with lending, derivatives, and structured products. Ethena's USDtb and Jupiter's JupUSD are the early-mover examples; the design space behind them is now substantially larger. The risk consideration — and it is non-trivial — is that the underlying instruments are KYC-gated and permissioned, which limits the degree of "permissionless" composition that DeFi-native systems can rely on. The integration patterns that emerge in the next twelve months will determine how cleanly tokenised MMFs become a primary collateral layer of the on-chain economy.

### Regulators

For the OCC, the FDIC, and the Federal Reserve, the 8 May filings clarify what the regulatory perimeter is being asked to accommodate. The yield prohibition in the GENIUS Act has clearly not stopped on-chain yield from reaching wallet holders; it has migrated the architecture for delivering that yield from the payment-stablecoin category (which the regulators directly supervise) into the registered-fund category (which the SEC supervises). This is not necessarily a bad outcome — registered funds are a well-understood regulatory category — but it does mean that the cross-agency coordination question becomes operationally sharper. The OCC's final rule, due by January 2027, will determine whether the 20% cap on tokenised reserves survives in any form, and whether the line between "payment stablecoin" and "tokenised MMF share" is held at the issuer level or is allowed to blur further at the wallet level.

## Conclusion

The 8 May 2026 filings are not, by themselves, a paradigm shift. They are individual products from a single asset manager, filed in the specific regulatory window that the OCC's rulemaking opened. What they capture, however, is the shape of an industry-level transition that has been visible since BlackRock launched BUIDL in March 2024 and that the GENIUS Act has now accelerated rather than constrained.

Stablecoins, in the GENIUS Act sense, will continue to do what stablecoins were always good at: efficient settlement, near-instant cross-border payment, programmable money for use cases that need a stable unit of account. They will not, under current and proposed rules, pay yield to their holders. The yield-bearing dollar in a wallet — the product that takes the same form factor as a stablecoin but that accrues Treasury yield to its holder — will be a tokenised money market fund share, issued by a registered fund, with a transfer agent (Securitize, BNY Mellon, and likely several others) as the legal record of ownership. BRSRV and BSTBL are the early, institutional expressions of that pattern. They will not be the last.

For prior context on this site, the [January 2018 piece on the Ethereum technology stack ⧉](https://sebastienrousseau.com/2018-01-09-understanding-the-technology-behind-blockchain/index.html "Understanding the Technology behind Blockchain") covered the substrate on which BSTBL now sits, the [January 2018 article on the ERC-20 standard ⧉](https://sebastienrousseau.com/2018-01-24-the-erc-20-token-standard/index.html "ERC-20: The Ethereum Token Interface That Changed the World") covered the share-class representation BlackRock has chosen, the [February 2018 analysis of faster-payment cryptocurrencies ⧉](https://sebastienrousseau.com/2018-02-04-unveiling-a-new-cryptocurrency-and-offering-future-faster-payment-solution/index.html "Unveiling a New Cryptocurrency and Faster Payment Solution") covered the user experience problem that yield-bearing on-chain instruments are now partly solving, and the [recent piece on the SWIFT CBPR+ structured-address deadline](https://sebastienrousseau.com/2026-05-12-iso-20022-pacs008-structured-address-deadline/index.html "The November 2026 pacs.008 Structured-Address Deadline") sits adjacent in the wider payments-modernisation conversation that BlackRock's filings are also part of. The point of triangulating these is not to claim that any single architecture has won. It is that the institutional and the on-chain financial systems are, in 2026, converging on shared primitives faster than either of them anticipated even a year ago.

## Frequently Asked Questions

**What is the actual difference between BRSRV/BSTBL and a stablecoin like USDC?**

In the wallet, the difference is mostly invisible. Each is a fungible token on a public blockchain, redeemable for dollars (or for the underlying fund share value), composable with DeFi. In law, the difference is substantial. USDC is a payment stablecoin under the GENIUS Act, issued by a Permitted Payment Stablecoin Issuer, prohibited from paying yield to holders. BRSRV and BSTBL are share classes of registered money market funds under the Investment Company Act of 1940, regulated under Rule 2a-7, where the yield is the natural return on the share. A holder of BRSRV is, legally, a shareholder of a fund. A holder of USDC is, legally, a holder of a payment instrument.

**Why is BSTBL different from BUIDL if both are tokenised BlackRock funds on Ethereum?**

BUIDL, launched in March 2024, was structured as a new fund with on-chain architecture from inception, with Securitize as the partner and the design native to the digital-asset workflow. BSTBL, by contrast, is a new on-chain share class added to an existing $6–7 billion conventional money market fund — the Select Treasury Based Liquidity Fund. BNY Mellon serves as the transfer agent. The architectural significance is that BSTBL demonstrates how to bring an existing, large, traditional money-market product on-chain without rebuilding it as a new fund. That template, if it works, is portable to any conventional MMF in the industry.

**Why is the OCC's 20% cap on tokenised reserves controversial?**

The OCC's March 2026 proposal floated a potential 20% limit on how much of a stablecoin issuer's reserves could be held in tokenised form. BlackRock's comment letter argued that this would be "extraneous" to the OCC's supervisory objectives, because the risk profile of a reserve asset is driven by credit quality, duration, and liquidity — not by whether it is held or transferred on a distributed ledger. Operationally, the cap would constrain BUIDL's role as the primary reserve backing of products like Ethena's USDtb and Jupiter's JupUSD, both of which currently rely on BUIDL for more than 90% of their reserves. The OCC's final rule, due by January 2027, will determine whether the cap survives, is raised, or is dropped.

**What does it mean that the BRSRV filing does not name the blockchains it will support?**

It is a routine feature of early-stage SEC filings rather than a strategic ambiguity. The filing establishes the legal structure (a registered fund issuing OnChain Shares through a permissioned framework with Securitize as transfer agent) without committing to specific chains, which BlackRock will likely announce closer to launch. BUIDL itself was launched on Ethereum and subsequently expanded to Polygon, Avalanche, Optimism, Aptos, and Arbitrum; BRSRV is most plausibly going to follow a similar multi-chain pattern given the explicit reference to "multiple public blockchains" in the filing.

**Is this the end of yield-bearing stablecoins as a product category?**

It is the end of yield-bearing payment stablecoins as a category, at least under US federal law, unless Congress amends the GENIUS Act. It is not the end of yield-bearing on-chain dollars as a product category, which is what users actually want. That category is now migrating to tokenised money market fund shares — BUIDL, BENJI, BRSRV, BSTBL, Ondo's products, and the wave of competing tokenised MMFs that the BSTBL pattern is likely to catalyse. The instruments will look slightly different in the wallet (the value of the token will reflect accumulated yield rather than holding $1.00 flat), but the economic function — dollar-equivalent exposure with Treasury yield, settled on a public chain — is being preserved through a different regulatory pathway.

## References

- Sebastien Rousseau, (2026). [The November 2026 pacs.008 Structured-Address Deadline: A Six-Month View](https://sebastienrousseau.com/2026-05-12-iso-20022-pacs008-structured-address-deadline/index.html "The November 2026 pacs.008 Structured-Address Deadline").
- Sebastien Rousseau, (2018). [ERC-20: The Ethereum Token Interface That Changed the World](https://sebastienrousseau.com/2018-01-24-the-erc-20-token-standard/index.html "ERC-20: The Ethereum Token Interface That Changed the World").
- Sebastien Rousseau, (2018). [Understanding the Technology behind Blockchain](https://sebastienrousseau.com/2018-01-09-understanding-the-technology-behind-blockchain/index.html "Understanding the Technology behind Blockchain").
- Sebastien Rousseau, (2018). [Unveiling a New Cryptocurrency and Faster Payment Solution](https://sebastienrousseau.com/2018-02-04-unveiling-a-new-cryptocurrency-and-offering-future-faster-payment-solution/index.html "Unveiling a New Cryptocurrency and Faster Payment Solution").
- Unchained, (2026). [BlackRock Files for Two New Tokenized Money-Market Funds Targeting Stablecoin Capital ⧉](https://unchainedcrypto.com/blackrock-files-for-two-new-tokenized-money-market-funds-targeting-stablecoin-capital/ "BlackRock Files for Two New Tokenized Money-Market Funds Targeting Stablecoin Capital"). Unchained.
- The Block, (2026). [BlackRock urges OCC to drop tokenized reserve cap idea, expand eligible assets in GENIUS Act comment letter ⧉](https://www.theblock.co/post/399812/blackrock-urges-occ-to-drop-tokenized-reserve-cap-idea-expand-eligible-assets-in-genius-act-comment-letter "BlackRock urges OCC to drop tokenized reserve cap idea"). The Block.
- BeInCrypto, (2026). [BlackRock Backs OCC Stablecoin Rules Under GENIUS Act ⧉](https://beincrypto.com/blackrock-occ-stablecoin-genius-act-comment/ "BlackRock Backs OCC Stablecoin Rules Under GENIUS Act"). BeInCrypto.
- Markets Media, (2026). [BlackRock Fires 'Starting Gun for a New Financial Era' ⧉](https://www.marketsmedia.com/blackrock-fires-starting-gun-for-a-new-financial-era/ "BlackRock Fires 'Starting Gun for a New Financial Era'"). Markets Media.
- Crowdfund Insider, (2026). [BlackRock Focuses On Tokenization Initiatives With Blockchain Enabled Funds ⧉](https://www.crowdfundinsider.com/2026/05/278346-blackrock-focuses-on-tokenization-initiatives-with-blockchain-enabled-funds/ "BlackRock Focuses On Tokenization Initiatives With Blockchain Enabled Funds"). Crowdfund Insider.
- CoinDesk, (2026). [BlackRock Deepens Tokenization Push with New Onchain Fund Offerings ⧉](https://www.coindesk.com/business/2026/05/09/blackrock-deepens-tokenization-push-with-new-onchain-fund-offerings "BlackRock Deepens Tokenization Push with New Onchain Fund Offerings"). CoinDesk.
- Crypto Briefing, (2026). [BlackRock doubles down on tokenization with new stablecoin reserve funds ⧉](https://cryptobriefing.com/blackrock-tokenized-money-market-funds-stablecoins/ "BlackRock doubles down on tokenization with new stablecoin reserve funds"). Crypto Briefing.
- Latham & Watkins, (2026). [OCC Issues Proposal to Implement the GENIUS Act ⧉](https://www.lw.com/en/insights/occ-issues-proposal-to-implement-the-genius-act "OCC Issues Proposal to Implement the GENIUS Act"). Latham & Watkins.
- Nixon Peabody, (2026). [Proposed OCC Regulations for Payment Stablecoins Under the GENIUS Act ⧉](https://www.nixonpeabody.com/insights/alerts/2026/04/02/proposed-occ-regulations-for-payment-stablecoins-under-the-genius-act "Proposed OCC regulations for payment stablecoins under the GENIUS Act"). Nixon Peabody LLP.
- Morgan Lewis, (2026). [Stablecoin Regulation: OCC Proposal Under the GENIUS Act ⧉](https://www.morganlewis.com/pubs/2026/04/occs-genius-act-proposal-what-prospective-issuers-need-to-know "Stablecoin Regulation: OCC Proposal Under the GENIUS Act"). Morgan Lewis.
- American Banker, (2026). [Stablecoin yield debate dominates GENIUS rule comments ⧉](https://www.americanbanker.com/news/stablecoin-yield-debate-dominates-genius-rule-comments "Stablecoin yield debate dominates GENIUS rule comments"). American Banker.
- Congressional Research Service, (2026). [The Stablecoin Yield Debate ⧉](https://www.congress.gov/crs-product/IF13174 "The Stablecoin Yield Debate"). Congress.gov.
- Compliance Corylated, (2026). [US OCC closes GENIUS Act loophole allowing yield-bearing stablecoins ⧉](https://www.compliancecorylated.com/news/us-occ-closes-genius-act-loophole-allowing-yield-bearing-stablecoins/ "US OCC closes GENIUS Act loophole allowing yield-bearing stablecoins"). Compliance Corylated.
- CryptoSlate, (2025). [Tokenized US Treasuries just broke DeFi's most sacred rule ⧉](https://cryptoslate.com/tokenized-us-treasuries-silently-replaced-defis-foundation-and-you-missed-the-critical-9-billion-shift/ "Tokenized US Treasuries — CryptoSlate"). CryptoSlate.
- MEXC News, (2026). [BlackRock files for two new tokenized funds with the U.S. SEC on Ethereum ⧉](https://www.mexc.com/news/1080472 "BlackRock files for two new tokenized funds with the U.S. SEC on Ethereum"). MEXC News.
- Stellar Foundation, (2026). [Franklin Templeton, Stellar Development Foundation Mark Five Years of BENJI ⧉](https://stellar.org/press/franklin-templeton-stellar-development-foundation-mark-five-years-of-benji-the-first-u-s-registered-tokenized-money-market-fund "Five Years of BENJI"). Stellar Development Foundation.

<!-- enrich-start -->
<aside class="author-card" aria-label="About the author"><img alt="Portrait of Sebastien Rousseau" src="https://cloudcdn.pro/stocks/images/sebastien-rousseau.png" width="64" height="64" loading="lazy" decoding="async" /><span class="author-card-body"><strong class="author-card-name"><a href="/about/index.html">Sebastien Rousseau</a></strong><span class="author-card-bio">Senior banking technologist writing on applied AI, ISO 20022 migration, post-quantum cryptography for financial services, and the structural transformation of wholesale payments.</span><span class="author-credentials">20+ years across HSBC Commercial &amp; Investment Bank, PayPal, Barclays, Shazam, AKQA, Virgin Group. <a href="/about/index.html">Full profile</a> &middot; <a href="https://www.linkedin.com/in/sebastienrousseau/" rel="external noopener">LinkedIn</a> &middot; <a href="https://github.com/sebastienrousseau" rel="external noopener">GitHub</a></span></span></aside>
<p class="post-reviewed">Last reviewed <time datetime="2026-05-15">2026-05-15</time>.</p>
<aside class="related-posts" aria-labelledby="related-heading">
<h2 id="related-heading" class="related-heading">Related reading</h2>
<div class="related-grid">
<article class="related-card"><a href="https://sebastienrousseau.com/2024-02-13-eus-ai-act-shaping-the-future-of-global-ai-regulation/index.html" class="related-media" aria-label="EU's AI Act: Pioneering Ethical AI Regulation Worldwide" tabindex="-1"><img alt="A person sitting on black bench reading newspaper" src="https://cloudcdn.pro/stocks/images/ryoji-iwata-a-qsFZimp1M.webp" loading="lazy" decoding="async" width="600" height="400" /></a><footer class="related-body"><h3><a href="https://sebastienrousseau.com/2024-02-13-eus-ai-act-shaping-the-future-of-global-ai-regulation/index.html">EU's AI Act: Pioneering Ethical AI Regulation Worldwide</a></h3><p><time datetime="2024-02-13">2024-02-13</time></p></footer></article>
<article class="related-card"><a href="https://sebastienrousseau.com/2018-01-24-the-erc-20-token-standard/index.html" class="related-media" aria-label="ERC-20: The Ethereum Token Interface That Changed the World" tabindex="-1"><img alt="Turned off laptop computer on top of brown wooden table" src="https://cloudcdn.pro/stocks/images/m-ZzOa5G8hSPI.webp" loading="lazy" decoding="async" width="600" height="400" /></a><footer class="related-body"><h3><a href="https://sebastienrousseau.com/2018-01-24-the-erc-20-token-standard/index.html">ERC-20: The Ethereum Token Interface That Changed the World</a></h3><p><time datetime="2018-01-24">2018-01-24</time></p></footer></article>
</div>
</aside>
<!-- enrich-end -->
