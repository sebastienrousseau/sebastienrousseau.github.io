---

# Front Matter (YAML)

author: "contact@sebastienrousseau.com (Sebastien Rousseau)"
banner_alt: "Abstract neural network visualisation in blue and purple tones representing AI processing"
banner_height: "100vh"
banner_width: "100vw"
banner: "https://cloudcdn.pro/stocks/images/getty-images-aTWKwJllPOA.webp"
cdn: "https://cloudcdn.pro/clients"
changefreq: "weekly"
charset: "UTF-8"
cname: "sebastienrousseau.com"
copyright: "© Copyright 2007 - 2026 - Sebastien Rousseau. All rights reserved."
date: "Nov 12, 2023"
description: "How transformer models work, which 2023 models set the benchmark, where generative AI lands first in financial services, and what governance questions practitioners need answered before deploying."
format-detection: "telephone=no"
hreflang: "en"
icon: "https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/sebastienrousseau.svg"
id: "https://sebastienrousseau.com/2023-11-12-exploring-generative-ai/index.html"
image_alt: "Black and White Portrait of Sebastien Rousseau"
image_height: "161"
image_width: "161"
image: "https://cloudcdn.pro/stocks/images/sebastien-rousseau.png"
keywords: "generative AI, large language model, transformer architecture, GPT-4, financial services AI, hallucination, retrieval-augmented generation, AI governance, foundation model, fine-tuning"
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
permalink: "https://sebastienrousseau.com/2023-11-12-exploring-generative-ai/index.html"
rating: "general"
referrer: "no-referrer"
revisit-after: "7 days"
robots: "index, follow"
short_name: "sebastienrousseau"
subtitle: "Transformer mechanics, 2023 model benchmarks, financial services use cases, and the governance questions that cannot be deferred."
tags: "generative AI, large language model, GPT-4, transformer, financial services, hallucination, RAG, AI governance, foundation model, fine-tuning"
theme-color: "0, 67, 165"
title: "Generative AI in 2023: How It Works, Where It Lands"
url: "https://sebastienrousseau.com/2023-11-12-exploring-generative-ai/index.html"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"

# RSS - The RSS feed front matter (YAML).
atom_link: "https://sebastienrousseau.com/2023-11-12-exploring-generative-ai/rss.xml"
category: "AI"
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.26)"
item_description: "How transformer models work, which 2023 models set the benchmark, where generative AI lands first in financial services, and what governance questions practitioners need answered."
item_guid: "https://sebastienrousseau.com/2023-11-12-exploring-generative-ai/rss.xml"
item_link: "https://sebastienrousseau.com/2023-11-12-exploring-generative-ai/rss.xml"
item_pub_date: "Sun, 12 Nov 2023 20:30:00 +0000"
item_title: "Generative AI in 2023: How It Works, Where It Lands"
last_build_date: "Sun, 12 Nov 2023 20:30:00 +0000"
managing_editor: "contact@sebastienrousseau.com (Sebastien Rousseau)"
pub_date: "Sun, 12 Nov 2023 20:30:00 +0000"
ttl: "60"
type: "website"
webmaster: "contact@sebastienrousseau.com"

# Apple - The Apple front matter (YAML).
apple_mobile_web_app_orientations: "portrait"
apple_touch_icon_sizes: "192x192"
apple-mobile-web-app-capable: "yes"
apple-mobile-web-app-status-bar-inset: "black"
apple-mobile-web-app-status-bar-style: "black-translucent"
apple-mobile-web-app-title: "Generative AI 2023"
apple-touch-fullscreen: "yes"

# MS Application - The MS Application front matter (YAML).

msapplication-navbutton-color: "0, 67, 165"

# Twitter Card - The Twitter Card front matter (YAML).

twitter_card: "summary"
twitter_creator: "@wwdseb"
twitter_description: "Transformer mechanics, 2023 model benchmarks, financial services use cases, and the governance questions that cannot be deferred."
twitter_image: "https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/sebastienrousseau.svg"
twitter_image_alt: "Logo of Sebastien Rousseau"
twitter_site: "@wwdseb"
twitter_title: "Generative AI in 2023: How It Works, Where It Lands"
twitter_url: "https://sebastienrousseau.com/2023-11-12-exploring-generative-ai/index.html"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://sebastienrousseau.com/2023-11-12-exploring-generative-ai/index.html"
author_twitter: "@wwdseb"
author_location: "London, UK"
thanks: "Thanks for reading!"
site_last_updated: "2023-11-05"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "Kaishi, Kaishi Builder, Kaishi CLI, Kaishi Templates, Kaishi Themes"
site_software: "Static Site Generator, Rust"

excerpt: "Generative AI crossed from research curiosity to production deployment in 2023. GPT-4, Claude 2, Llama 2, and Mistral demonstrated that large language models could handle legal document review, code generation, and customer dialogue at human-comparable quality — raising immediate governance questions about hallucination, data leakage, and regulatory compliance in financial services."
last_reviewed: "2026-05-24"
---


<!-- lead-start -->
<aside class="post-lead" aria-label="Article summary">
<p class="post-lead-tldr"><strong>TL;DR.</strong> Generative AI moved from research to production in 2023. The transformer architecture — specifically the self-attention mechanism — is what gave large language models their ability to handle long-range context across documents. GPT-4, Claude 2, Llama 2, and Mistral defined the 2023 benchmark landscape. Financial services saw the earliest enterprise deployments in code generation, regulatory document summarisation, and KYC automation, but production use requires confronting hallucination risk, data governance, and the regulatory expectations of supervisors who are actively watching.</p>
<p class="post-lead-heading"><strong>Key takeaways</strong></p>
<ul class="post-lead-takeaways">
  <li><strong>The transformer is the foundation.</strong> All major 2023 LLMs are built on the attention-based transformer architecture introduced in "Attention Is All You Need" (2017). The self-attention mechanism allows a model to weigh the relevance of every token against every other token in the context window — enabling coherent long-form generation across thousands of tokens.</li>
  <li><strong>Scale drove qualitative change.</strong> GPT-4 (March 2023) achieved pass-rate scores equivalent to the 90th percentile on the US Bar exam and the 99th percentile on the GRE verbal section — demonstrating that model scale produced capabilities that could not be extrapolated from smaller predecessors.</li>
  <li><strong>Open-weight models changed the access equation.</strong> Llama 2 (Meta, July 2023) and Mistral 7B (September 2023) showed that models competitive with earlier GPT-3-class systems could run on commodity hardware or private infrastructure — removing cloud dependency as a blocker for regulated industries with strict data residency requirements.</li>
  <li><strong>Financial services use cases are real but the risks are not trivial.</strong> By late 2023, major banks were running internal pilots for contract review, regulatory change summarisation, and developer productivity. The unresolved production risks — hallucination, prompt injection, audit trails, and model provenance — remained the primary barriers to broad deployment.</li>
</ul>
<p class="post-lead-related"><strong>Related reading:</strong> <a href="https://sebastienrousseau.com/2024-01-01-ai-trends-2024-insights-and-predictions-for-the-future">AI Trends 2024: Insights and Predictions</a>, <a href="https://sebastienrousseau.com/2024-01-23-advancements-in-ai-prompt-engineering">AI Prompt Engineering 2024: Techniques That Work</a>, <a href="https://sebastienrousseau.com/2024-02-13-eus-ai-act-shaping-the-future-of-global-ai-regulation">EU's AI Act: Pioneering Ethical AI Regulation Worldwide</a>.</p>
</aside>
<!-- lead-end -->

![Abstract neural network visualisation in blue and purple tones representing AI processing](https://cloudcdn.pro/stocks/images/getty-images-aTWKwJllPOA.webp).class=\"img-fluid clearfix\"

> **Executive Summary / Key Takeaways**
>
> - **The architecture that changed everything.** The 2017 transformer paper introduced self-attention: a mechanism that computes relevance weights between every pair of tokens in the input, replacing the sequential processing of RNNs with parallelisable matrix operations. Every major language model in 2023 is a transformer variant ([Vaswani et al., 2017](https://arxiv.org/abs/1706.03762 "Attention Is All You Need")).
> - **GPT-4 as the 2023 benchmark.** Released March 2023, GPT-4 scored in the 90th percentile on the US Bar exam, 99th on GRE Verbal, and demonstrated multi-step reasoning across long documents. It set the capability benchmark that subsequent models aimed to meet or exceed ([OpenAI, 2023](https://arxiv.org/abs/2303.08774 "GPT-4 Technical Report")).
> - **Open-weight models democratised access.** Meta's Llama 2 (July 2023) and Mistral AI's Mistral 7B (September 2023) showed that models competitive with GPT-3.5-class capability could run on private infrastructure — addressing the data residency requirements of regulated industries.
> - **Financial services pilots in 2023.** Broad deployments by late 2023 included legal contract review (JPMorgan's DocLLM research), regulatory change monitoring, and developer productivity tools. Goldman Sachs reported internal use of AI coding assistants across 10,000 developers.
> - **Hallucination is a production blocker.** LLMs generate plausible-sounding but factually incorrect outputs at non-trivial rates. In regulated use cases — credit decisions, compliance opinions, customer disclosures — hallucination is not a cosmetic flaw; it is a regulatory and liability risk requiring architectural mitigations such as retrieval-augmented generation (RAG).

---

## How the Transformer Architecture Works

Every significant language model deployed in 2023 — GPT-4, Claude 2, Llama 2, Mistral, Falcon — is built on the transformer architecture introduced in the 2017 paper "Attention Is All You Need." Understanding the core mechanism explains both why these models work and where they fail.

**Tokens and embeddings.** The model begins by splitting input text into sub-word tokens (typically using byte-pair encoding). Each token is mapped to a high-dimensional vector (an embedding) that encodes its semantic relationships with other tokens, learned during pre-training.

**Self-attention.** For each token, the model computes three vectors: a Query (what this token is looking for), a Key (what this token offers), and a Value (what this token contributes). Attention scores are computed by taking the dot product of each Query against all Keys, applying softmax to produce weights, and summing the Values weighted by those scores. This means every token attends to every other token in the context window simultaneously — the mechanism that gives transformers their ability to handle long-range dependencies.

**Multi-head attention.** Multiple attention heads run in parallel, each learning different types of relationships (syntactic, semantic, positional). Their outputs are concatenated and linearly projected.

**Feed-forward layers.** After attention, each position passes through two linear transformations with a non-linear activation. This layer performs per-token computation independently, capturing local feature transformations.

**Scale.** GPT-4 is estimated at over one trillion parameters (unconfirmed by OpenAI). Llama 2 70B uses 70 billion. Mistral 7B uses 7 billion, with grouped-query attention and sliding window attention for efficiency. Larger models generally exhibit better zero-shot and few-shot reasoning — the emergent capabilities that make them useful for tasks they were not explicitly trained on.

## The 2023 Model Landscape

2023 produced more significant model releases than any prior year:

**GPT-4 (OpenAI, March 2023).** Multimodal (text + image input), context window up to 128,000 tokens in later GPT-4 Turbo variant, strong multi-step reasoning. Set the benchmark for professional-domain tasks.

**Claude 2 (Anthropic, July 2023).** 100,000-token context window (longest at launch), strong performance on long-document tasks such as contract review and regulatory analysis. Constitutional AI training for reduced harmful outputs.

**Llama 2 (Meta, July 2023).** Open-weight release at 7B, 13B, 34B, and 70B parameter variants. Commercial use permitted. Enabled on-premise deployment for regulated industries. Spawned hundreds of fine-tuned variants (Code Llama, Vicuna, WizardLM).

**Mistral 7B (Mistral AI, September 2023).** 7 billion parameters outperforming Llama 2 13B on most benchmarks. Grouped-query attention and sliding window attention reduce inference cost. The first significant European frontier model, relevant given GDPR and EU AI Act context.

**Falcon 180B (TII, September 2023).** 180 billion parameter open-weight model, trained on 3.5 trillion tokens of RefinedWeb data. Demonstrated that open-weight models could approach GPT-4-class scale.

## Where Generative AI Landed First in Financial Services

By late 2023, financial institutions had moved from internal experimentation to structured pilot programmes in several distinct use cases:

**Developer productivity.** Code generation tools (GitHub Copilot, Amazon CodeWhisperer, internally fine-tuned models) became the most broadly deployed category. Goldman Sachs reported that 10,000 developers had access to AI coding assistance. Morgan Stanley deployed GPT-4 internally to help financial advisers retrieve information from a 100,000-document knowledge base.

**Legal and regulatory document processing.** Contract clause extraction, regulatory change monitoring, and compliance mapping were the highest-value pilots. JPMorgan's research on DocLLM demonstrated that document-layout-aware language models outperformed generic LLMs on financial document understanding tasks.

**Customer service augmentation.** Banks deployed LLM-powered assistants for first-line customer queries, with human escalation for regulated advice. Key constraints: the model cannot give regulated advice, must not hallucinate product terms, and must be auditable.

**KYC and AML narrative generation.** Summarising complex transaction patterns and customer profiles for analyst review — replacing what had been manual write-up work — emerged as a credible use case with lower hallucination risk because the model summarises provided data rather than generating novel claims.

## The Risks That Production Exposed

Moving from demo to production in financial services surfaced a set of risks that required architectural responses:

**Hallucination.** LLMs generate confident-sounding incorrect outputs at rates that vary by task type and model. On factual recall tasks, even GPT-4 hallucinates at rates that are unacceptable for compliance opinions or credit disclosures. The primary mitigation is retrieval-augmented generation (RAG): ground the model's output in retrieved, verifiable documents rather than relying on parametric knowledge alone.

**Prompt injection.** Adversarial inputs embedded in documents or user messages can redirect model behaviour. In financial services, where LLMs process untrusted documents (contracts, emails, customer submissions), prompt injection is a production security risk, not a theoretical one.

**Data leakage.** Models fine-tuned or prompted on confidential data can reproduce that data in output — a material risk for PII, trading positions, and client information. Architectural controls (private deployment, data-in-context management, output filtering) are required, not optional.

**Model provenance and auditability.** Regulators expect financial institutions to explain automated decisions. An LLM that produces a credit assessment without an auditable reasoning trail fails the explainability requirements of GDPR Article 22, the EU AI Act's high-risk AI provisions, and existing FCA model risk guidance.

**Stale knowledge.** LLMs have training cutoffs. A model trained on data through early 2023 does not know about regulatory changes, rate decisions, or market events after that date — a significant limitation for real-time compliance or market commentary use cases without RAG or real-time retrieval.

## Governance Requirements Before Deployment

Financial services practitioners operating in 2023 were not waiting for regulatory certainty before deploying — but leading institutions adopted model risk management (MRM) frameworks adapted from SR 11-7 and SS3/18 guidance:

**Model inventory and documentation.** LLMs deployed for business functions require documentation of training data provenance, fine-tuning methodology, known failure modes, and performance on domain-specific validation sets.

**Human-in-the-loop checkpoints.** For regulated outputs (credit decisions, compliance opinions, customer disclosures), human review remained mandatory in 2023. Automation was applied to drafting and summarisation; final sign-off remained human.

**Vendor risk.** Using a third-party model API (OpenAI, Anthropic, Google) introduces vendor concentration risk, data residency risk, and model change risk (providers can update models silently). Enterprise agreements and private deployments partially mitigate these.

**Regulatory engagement.** The FCA, PRA, ECB, and FINRA all issued papers or speeches on AI governance in 2023. The consistent message: existing model risk frameworks apply to AI, and firms should be proactive in documenting their governance approach ahead of formal guidance.

## Frequently Asked Questions

**What is the difference between a large language model and a foundation model?**

A large language model (LLM) is a model trained on text data at scale to predict and generate language. A foundation model is a broader term for any large pre-trained model that can be adapted (fine-tuned or prompted) for multiple downstream tasks — including LLMs but also vision models, code models, and multimodal models. GPT-4 is both an LLM and a foundation model. DALL-E 3 is a foundation model but not an LLM. In practice, the terms are often used interchangeably when referring to text-generation systems.

**What is retrieval-augmented generation and why does it matter for financial services?**

RAG combines a language model with a retrieval system: rather than relying solely on the model's parametric knowledge (what it learned during training), RAG fetches relevant documents at inference time and provides them as context. This significantly reduces hallucination on factual tasks because the model is synthesising provided text rather than recalling learned facts. For financial services, RAG enables use cases like regulatory change monitoring (always retrieves current rules) and contract review (grounds the model in the actual contract text) that would be too hallucination-prone with a pure generation approach.

**How should financial institutions handle the EU AI Act in relation to generative AI deployments in 2023?**

The EU AI Act was still in legislative process in 2023 (passed by the European Parliament in March 2024, entered into force August 2024). However, institutions with EU operations or EU customers were already assessing their pipelines. High-risk AI systems in credit scoring, employment decisions, and critical infrastructure require conformity assessments, human oversight mechanisms, and audit logging. General-purpose AI (GPAI) models — which includes foundation models like GPT-4 — have their own tier of requirements around transparency and systemic risk. Firms that began documentation and governance work in 2023 were better positioned for the implementation deadlines.

**What is the practical difference between fine-tuning and prompt engineering for enterprise LLM deployments?**

Fine-tuning modifies the model's weights by continuing training on domain-specific data — it teaches the model new knowledge and behavioural patterns. It requires labelled training data, compute budget, and ongoing maintenance as base models are updated. Prompt engineering (including few-shot examples and system prompts) shapes behaviour at inference time without changing weights — faster to implement and update, but bounded by what the base model already knows. For most 2023 financial services deployments, RAG plus prompt engineering was the preferred starting point; fine-tuning was reserved for cases where the model needed to learn proprietary terminology or adopt strict output formats.

## References

- Vaswani, A., et al., (2017). [Attention Is All You Need ⧉](https://arxiv.org/abs/1706.03762 "Attention Is All You Need").
- OpenAI, (2023). [GPT-4 Technical Report ⧉](https://arxiv.org/abs/2303.08774 "GPT-4 Technical Report").
- Touvron, H., et al., Meta AI, (2023). [Llama 2: Open Foundation and Fine-Tuned Chat Models ⧉](https://arxiv.org/abs/2307.09288 "Llama 2").
- Jiang, A., et al., Mistral AI, (2023). [Mistral 7B ⧉](https://arxiv.org/abs/2310.06825 "Mistral 7B").

<!-- enrich-start -->
<aside class="author-card" aria-label="About the author"><img alt="Portrait of Sebastien Rousseau" src="https://cloudcdn.pro/stocks/images/sebastien-rousseau.png" width="64" height="64" loading="lazy" decoding="async" /><span class="author-card-body"><strong class="author-card-name"><a href="/about/index.html">Sebastien Rousseau</a></strong><span class="author-card-bio">Senior banking technologist writing on applied AI, ISO 20022 migration, post-quantum cryptography for financial services, and the structural transformation of wholesale payments.</span><span class="author-credentials">20+ years across HSBC Commercial &amp; Investment Bank, PayPal, Barclays, Shazam, AKQA, Virgin Group. <a href="/about/index.html">Full profile</a> &middot; <a href="https://www.linkedin.com/in/sebastienrousseau/" rel="external noopener">LinkedIn</a> &middot; <a href="https://github.com/sebastienrousseau" rel="external noopener">GitHub</a></span></span></aside>
<p class="post-reviewed">Last reviewed <time datetime="2026-05-24">2026-05-24</time>.</p>
<aside class="related-posts" aria-labelledby="related-heading">
<h2 id="related-heading" class="related-heading">Related reading</h2>
<div class="related-grid">
<article class="related-card"><a href="https://sebastienrousseau.com/2024-01-01-ai-trends-2024-insights-and-predictions-for-the-future" class="related-media" aria-label="AI Trends 2024: Insights and Predictions for the Future" tabindex="-1"><img alt="Drone View of London" src="https://cloudcdn.pro/stocks/images/drone-view-of-london.webp" loading="lazy" decoding="async" width="600" height="400" /></a><footer class="related-body"><h3><a href="https://sebastienrousseau.com/2024-01-01-ai-trends-2024-insights-and-predictions-for-the-future">AI Trends 2024: Insights and Predictions for the Future</a></h3><p><time datetime="2024-01-01">2024-01-01</time></p></footer></article>
<article class="related-card"><a href="https://sebastienrousseau.com/2024-01-23-advancements-in-ai-prompt-engineering" class="related-media" aria-label="AI Prompt Engineering 2024: Techniques That Work" tabindex="-1"><img alt="A man analysing data on screens" src="https://cloudcdn.pro/stocks/images/ai-prompt-engineering-modern-office.webp" loading="lazy" decoding="async" width="600" height="400" /></a><footer class="related-body"><h3><a href="https://sebastienrousseau.com/2024-01-23-advancements-in-ai-prompt-engineering">AI Prompt Engineering 2024: Techniques That Work</a></h3><p><time datetime="2024-01-23">2024-01-23</time></p></footer></article>
<article class="related-card"><a href="https://sebastienrousseau.com/2024-02-13-eus-ai-act-shaping-the-future-of-global-ai-regulation" class="related-media" aria-label="EU's AI Act: Pioneering Ethical AI Regulation Worldwide" tabindex="-1"><img alt="A person sitting on black bench reading newspaper" src="https://cloudcdn.pro/stocks/images/ryoji-iwata-a-qsFZimp1M.webp" loading="lazy" decoding="async" width="600" height="400" /></a><footer class="related-body"><h3><a href="https://sebastienrousseau.com/2024-02-13-eus-ai-act-shaping-the-future-of-global-ai-regulation">EU's AI Act: Pioneering Ethical AI Regulation Worldwide</a></h3><p><time datetime="2024-02-13">2024-02-13</time></p></footer></article>
</div>
</aside>
<!-- enrich-end -->
