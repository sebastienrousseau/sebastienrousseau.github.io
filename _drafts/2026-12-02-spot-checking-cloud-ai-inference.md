---

# Front Matter (YAML)

author: "contact@sebastienrousseau.com (Sebastien Rousseau)"
banner_alt: "Bars of white light cutting diagonally through darkness"
banner_height: "1597"
banner_width: "2582"
banner: "https://cloudcdn.pro/stocks/images/maximalfocus-76McKuOlI5U.webp"
cdn: "https://cloudcdn.pro"
charset: "UTF-8"
cname: "sebastienrousseau.com"
copyright: "© Copyright 2025 - 2026 - Sebastien Rousseau. All rights reserved."
date: "December 2, 2026"
description: "A sampling-based protocol commits to a model's inference trace and spot-checks a few random paths, trading some soundness for proving times in milliseconds."
format-detection: "telephone=no"
hreflang: "en"
icon: "https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/sebastienrousseau.svg"
id: "https://sebastienrousseau.com/2026-12-02-spot-checking-cloud-ai-inference"
image_alt: "Black and White Portrait of Sebastien Rousseau"
image_height: "162"
image_width: "162"
image: "https://cloudcdn.pro/stocks/images/sebastienrousseau.webp"
keywords: "verifiable inference, verifiable AI, proofs of inference, SNARKs, zkLLM, Merkle tree, vector commitments, trace separation, other-model soundness, model substitution, refereed delegation, SVIP"
language: "en-GB"
last_reviewed: "2026-12-02"
layout: "report"
locale: "en_GB"
logo_alt: "Logo for Sebastien Rousseau"
logo_height: "44"
logo_width: "44"
logo: "https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/sebastienrousseau.svg"
menu: ""
measurementID: "G-169G4ET5HQ"
name: "Sebastien Rousseau"
permalink: "https://sebastienrousseau.com/2026-12-02-spot-checking-cloud-ai-inference"
rating: "general"
referrer: "no-referrer"
robots: "index, follow"
schema: "Article"
seo_title: "Spot-Checking Cloud AI: Faster Proofs of Inference, Weaker Guarantees"
short_name: "sebastienrousseau"
subtitle: "Cryptographic proofs of inference give exact guarantees but carry heavy prover overhead. A sampling-based protocol trades some soundness for proving times in milliseconds, aimed at catching a provider that serves a different model from the one it advertised."
tags: "verifiable inference, verifiable AI, proofs of inference, SNARKs, zkLLM, trace separation, other-model soundness, model substitution"
theme-color: "0, 83, 191"
title: "Spot-Checking Cloud AI: Faster Proofs of Inference, Weaker Guarantees"
url: "https://sebastienrousseau.com/2026-12-02-spot-checking-cloud-ai-inference"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"

# RSS - The RSS feed front matter (YAML).
atom_link: "https://sebastienrousseau.com/2026-12-02-spot-checking-cloud-ai-inference/rss.xml"
category: "AI"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "Static Site Generator (SSG) (version 0.0.26)"
draft_engine: "claude"
draft_model: "sonnet"
draft_version: "0.0.47"
item_description: "A sampling-based protocol commits to a model's inference trace and spot-checks a few random paths, trading some soundness for proving times in milliseconds."
item_guid: "https://sebastienrousseau.com/2026-12-02-spot-checking-cloud-ai-inference/rss.xml"
item_link: "https://sebastienrousseau.com/2026-12-02-spot-checking-cloud-ai-inference/rss.xml"
item_pub_date: "Wed, 02 Dec 2026 00:00:00 +0000"
item_title: "Spot-Checking Cloud AI: Faster Proofs of Inference, Weaker Guarantees"
last_build_date: "Wed, 02 Dec 2026 00:00:00 +0000"
managing_editor: "contact@sebastienrousseau.com (Sebastien Rousseau)"
pub_date: "Wed, 02 Dec 2026 00:00:00 +0000"
ttl: "60"
type: "article"
webmaster: "contact@sebastienrousseau.com"

# Apple - The Apple front matter (YAML).
apple_mobile_web_app_orientations: "portrait"
apple_touch_icon_sizes: "192x192"
apple-mobile-web-app-capable: "yes"
apple-mobile-web-app-status-bar-inset: "black"
apple-mobile-web-app-status-bar-style: "black-translucent"
apple-mobile-web-app-title: "Spot-Checking Cloud AI: Faster Proofs of Inference, Weaker Guarantees"
apple-touch-fullscreen: "yes"

# MS Application - The MS Application front matter (YAML).

msapplication-navbutton-color: "0, 83, 191"

# Twitter Card - The Twitter Card front matter (YAML).

twitter_card: "summary_large_image"
twitter_creator: "@wwdseb"
twitter_description: "A sampling-based protocol commits to a model's inference trace and spot-checks a few random paths, trading some soundness for proving times in milliseconds."
twitter_image: "https://cloudcdn.pro/stocks/images/maximalfocus-76McKuOlI5U.webp"
twitter_image_alt: "Bars of white light cutting diagonally through darkness"
twitter_site: "@wwdseb"
twitter_title: "Spot-Checking Cloud AI: Faster Proofs of Inference, Weaker Guarantees"
twitter_url: "https://sebastienrousseau.com/2026-12-02-spot-checking-cloud-ai-inference"

changefreq: "weekly"
revisit-after: "7 days"
site_software: "Static Site Generator, Rust"
excerpt: "Cryptographic proofs of inference give exact guarantees but carry heavy prover overhead. A sampling-based protocol trades some soundness for proving times in milliseconds, aimed at catching a provider that serves a different model from the one it advertised."

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://sebastienrousseau.com"
author_twitter: "@wwdseb"
author_location: "London, UK"
thanks: "Thanks for reading!"
site_last_updated: "2026-12-02"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "Kaishi, Kaishi Builder, Kaishi CLI, Kaishi Templates, Kaishi Themes"

---

# Spot-Checking Cloud AI: Faster Proofs of Inference, Weaker Guarantees

**Cryptographic proofs of inference give exact guarantees but carry heavy prover overhead. A sampling-based protocol trades some soundness for proving times in milliseconds, aimed at catching a provider that serves a different model from the one it advertised.**

<!-- lead-start -->
<aside class="post-lead" aria-label="Article summary">
<p class="post-lead-tldr"><strong>TL;DR.</strong> Clients of cloud-hosted AI models have no guarantee that responses are correct or came from the intended model. SNARK-based proofs can provide that guarantee, but the authors call their prover overhead prohibitive. Anchuri and co-authors propose a protocol in which the server commits to the inference trace with Merkle-tree-based vector commitments and opens only a few entries along randomly sampled paths. On Llama-2-7B, committing to the trace took 5.8 milliseconds, against 388.3 seconds of proving for zkLLM on the same machine, with a larger proof and a weaker, explicitly stated security guarantee.</p>
<p class="post-lead-heading"><strong>Key takeaways</strong></p>
<ul class="post-lead-takeaways">
  <li><strong>The problem is trust.</strong> A client of these models receives an answer from an untrusted, possibly corrupted, server and cannot rerun a large model locally.</li>
  <li><strong>Exact proofs are slow to produce.</strong> SNARKs carry proof-generation overhead the paper puts at typically 1000× or larger; zkLLM takes around 15 minutes for a model of up to 13B parameters.</li>
  <li><strong>Sampling changes the cost.</strong> The prover commits to the whole execution trace, and the verifier checks a few random paths from output to input.</li>
  <li><strong>The trade is explicit.</strong> The formal guarantee is other-model soundness: detecting a server that ran a model whose behaviour differs substantially from the intended one. Full soundness for LLMs is left open.</li>
  <li><strong>The proof is not private.</strong> Opened values reveal information about the underlying model; the protocol is not zero-knowledge.</li>
</ul>
</aside>
<!-- lead-end -->

> **Executive Summary**
>
> - The source is "Towards Verifiable AI with Lightweight Cryptographic Proofs of Inference" by Anchuri, Campanelli, Cesaretti, Gennaro, Jois, Kayman and Ozdemir, posted to the IACR Cryptology ePrint Archive (2026/541); an earlier version is to appear at IEEE SaTML 2026.
> - Most proposals for verifiable AI use SNARKs, which verify cheaply but incur proof-generation overhead the paper puts at typically 1000× or larger.
> - The framework replaces full cryptographic proofs with a sampling-based approach grounded in statistical properties of neural networks, which the authors formalise as trace separation.
> - In the authors' benchmark on Llama-2-7B, proving fell from 388.3 seconds (zkLLM) to milliseconds, verification fell from 2.36 seconds to 12.44 milliseconds, and the proof grew from 183 kB to about 3.4 MB.
> - The protocol trades soundness for efficiency. The authors position it for auditing, high-volume deployments where repeated queries amplify detection, and providers who face penalties if caught.
> - Experiments on ResNet-18 and Llama-2-7B, and three attack strategies, support the design; the authors state that formal guarantees of trace separation are still needed.

## The client who cannot check the answer

Large AI models are increasingly offered as cloud services, and the paper opens on a plain weakness of that arrangement: clients have no guarantee that responses are correct or were produced by the intended model. In the authors' words, a client of these models "will only receive an answer from an untrusted, possibly corrupted, server who could provide incorrect responses."

The obvious workaround does not hold up. A client could, in principle, download the model from a verified site and run the query on their own device. The paper calls this "clearly infeasible", because the computing resources these networks need are too large for the average user's systems. If the client could run the model, they would not need the service.

So the question the authors pose is whether a client can efficiently verify a computation performed by an untrusted server, using fewer resources than running the model would take. That is the problem of verifiable inference.

## What exact proofs cost

Most proposals to build verifiable AI systems use cryptographic proofs, in particular SNARKs (Succinct Non-interactive Arguments of Knowledge). Their appeal is on the verifier's side. A SNARK lets a client verify an arbitrary computation from a short proof, and the paper describes verification as remarkably efficient, giving constant-size proofs and verification time, regardless of the size of the computation, as an example.

The difficulty sits with the prover. The paper puts SNARK proof-generation overhead at "typically 1000× or larger", citing Justin Thaler's analysis of SNARK performance. The reason is structural: SNARKs introduce expensive cryptographic operations for every elementary computation step, such as a gate in a circuit representation, and a large neural network has a great many steps.

The paper gives two reference points. For zkLLM, producing a proof of correct inference for a large language model with up to 13B parameters takes around 15 minutes. The abstract also describes existing proof systems as introducing prohibitive prover overhead, "e.g., hundreds of seconds per query for billion-parameter models".

The authors explain why that matters. Verifiable inference must run at almost zero overhead, because predictions are computed many times and are usually fast to produce, so the proof has to be comparably fast. They note that this may not hold for verifiable training, which is infrequent and can tolerate slower proofs, and the paper deals only with inference from an already correctly trained model. Their conclusion is measured: while work is ongoing to reduce the burden, full proofs on machine learning models using these approaches "still appear to be infeasible".

## Why cheap proofs matter beyond outsourcing

It would be easy to treat this as a narrow concern about whether a cloud provider is honest about its compute. The paper argues for a wider reach.

One application is model transparency: proving that an AI system that has been "certified" as trained correctly over "legal" data is the one actually used to compute predictions. Another is fairwashing, where a provider uses a biased model for users but substitutes an unbiased one when under audit. An appendix adds three motivating scenarios: a provider quietly serving a cheaper, smaller or heavily quantized model; a provider swapping a safety-aligned model for a dealigned variant; and a provider serving a model trained on data it had no right to use, in place of one audited for licensed data.

I'd argue this is the strongest reason to care. Audit and certification regimes are only as good as the link between the thing inspected and the thing deployed. A check cheap enough to run on live traffic does more to hold that link than a stronger one that is too slow to run.

## Spot checks in place of full proofs

The authors take a different path from circuit-based proofs. Their starting observation comes from AI research on representational similarity: two models that produce sufficiently different outputs must also differ in their internal activation traces. The paper quotes a survey by Klabunde and co-authors: "When functional similarity measures indicate dissimilarity, representations must be dissimilar at some layer."

They formalise this as a trace separation property and show that, combined with a suitable testing mechanism, it is sufficient to guarantee security under the notion they call other-model soundness. The authors say their technical approach has not been used in this setting before.

The concrete scheme detects cheating through a small number of checks on random parts of the computation. That is a deliberate contrast with cryptographic proofs, which check every step and give a proof of exact rather than approximate correctness.

## How the protocol works

The prover commits to the execution trace of inference using Merkle-tree-based vector commitments, then opens only a small number of entries along randomly sampled paths from output to input. A commitment to the correct model's weights, published after training, serves as the ground truth.

The verifier starts at a random output neuron. It reads that neuron's claimed activation, the activations of all its parent neurons and the corresponding weights, and checks that the neuron's value is consistent with them. It then picks one of the parents at random and repeats, layer by layer, until it reaches the input. If every check on the path passes, it accepts the output.

The path matters. The authors report that a simpler test, checking one random neuron anywhere in the network, failed because discrepancies typically show up only in late layers, so an early-layer check would usually pass even when the output was wrong. Tracing a whole path anchors the check at the input layer, which the adversary cannot change. Vector commitments bind the server to unique values, so it cannot change the trace after seeing which entries are requested, and the openings are much smaller than the network.

The paper contrasts this with SVIP, an earlier verifiable inference protocol that trains a secret-dependent proxy task, with a trusted intermediary distributing secrets to users. The authors list two overheads: SVIP needs model-specific training that can be resource-intensive, and its security relies on actively refreshing secrets against recovery attacks, in which the provider poses as a user to steal them. Their own protocol runs directly between prover and verifier, needs no intermediary or proxy task, and, the authors say, "naturally" applies to a wide class of deep neural networks beyond LLMs. The experiments cover a ResNet-18 classifier and Llama-2-7B, and the conclusion lists extending the protocol to architectures with different data flows, such as graph neural networks, as future work.

## The speed result, in numbers

The authors benchmarked on a single machine (an AMD Ryzen 9 9900X CPU, 32 GB of RAM and an NVIDIA GeForce RTX 3090 GPU) using Llama-2-7B. They ran zkLLM's public implementation for timings and took zkLLM's proof size from its paper, noting that zkLLM's original hardware differed.

For zkLLM, proving the whole inference took 388.3 seconds, the proof was 183 kB, and verification took 2.36 seconds. For the new protocol, committing to the entire trace took 5.8 milliseconds, and generating a single Merkle opening took 0.007 milliseconds on average with the tensors in device memory. Verification took 12.44 milliseconds.

The proof is larger. The activation values on the path come to 3.14 MB, or 1.6 MB with Brotli compression; the Merkle openings add about 100 KB that cannot be compressed. Because the client holds only a commitment to the model rather than its weights, the proof must also carry the relevant weights and their openings, which roughly doubles the payload to about 3.4 MB. The authors describe this as "moderately larger proofs". Whether 3.4 MB per query is moderate depends on the deployment.

The paper attributes much of the speed to a hybrid commitment scheme: for matrix multiplication layers it commits only to the input activation matrix, and for element-wise layers to the output tensor, so it does not serialise the entire computation.

## Evidence that the statistics hold

A protocol built on statistical properties is only as good as those properties, and the authors tested them directly.

For classifiers, they trained two ResNet-18 models, one for dogs versus cats and one for dogs versus squirrels, and compared their internal activations on dog images, the class both share. For LLMs, they compared Llama-2-7b-chat-hf with its base model, Llama-2-7b-hf: a fine-tuned model against the version it came from, which the authors describe as closer to a real deployment. The weights were closely aligned, with a mean relative Frobenius norm of 0.052 across 291 weight matrices, yet the path test still distinguished the two. The paper reports that when comparing models with very different behaviour, the test never failed in their experiments, and the authors believe the probability of failure is negligible.

Then comes the adversarial question. A cheating server need not submit an honest trace from another model; it might try to forge one. The authors tried gradient-descent reconstruction, on a small three-layer network trained on the iris dataset and on Llama-2-7B-chat, and an inverse transform attack on the small network. On Llama-2-7B-chat, across about 3.5 million path evaluations, no reconstruction achieved a separation value below 0.373.

The hardest test was a logit swap attack, which sits closer to full soundness: the adversary takes the true model's output, swaps the highest- and lowest-probability tokens, and optimises intermediate activations to match. It did far better than reconstruction, with a minimum separation of 0.031, an order of magnitude smaller, though the authors report that every attempt still left measurable deviations.

The wording matters here. The conclusion says the experiments "provide evidence" that the protocol resists natural attack strategies, "for the specific strategies we tested". That is evidence about three attacks, not a proof that no attack exists.

## What the protocol does not promise

The authors are direct that the protocol "trades soundness for efficiency", and that sentence deserves weight.

The formal framework covers what the paper calls a relatively limited, though still practically useful, notion: other-model soundness. Under it, the client can detect a server that used a model whose behaviour differs substantially from the intended one. That speaks directly to model substitution. It is not exact correctness. Full soundness, where the server may produce an arbitrary output and forge a trace without restriction, escapes the formal treatment. The authors note that the analysis does extend to binary classifiers, where an adversary can only flip the output, but that LLMs are harder: an adversary can tinker with the output in ways that make the random-path test's detection probability "very low". They leave full soundness for LLMs as an open problem, and point out that any single-path sampling strategy faces a detection bound of 1/N, where N is the maximum layer width.

The paper also lists other limits. The protocol is not zero-knowledge: opening values in the clear reveals information about the model, which matters to a provider whose weights are proprietary. The authors sketch ways to add zero-knowledge on the sampled path only. A non-interactive version is an open problem. Quantized models need study, because an adversary could exploit their rounding errors. And while trace separation is widely accepted in machine learning, "more formal theoretical guarantees of trace separation are needed to prove security."

The authors argue that low per-query detection can still be enough. When inference runs at scale, a provider that routinely substitutes models will on average be caught after a moderate number of queries. Auditors can send many test queries against a committed model. And providers who face severe penalties have reason not to cheat even when the chance of detection per query is low, which the paper links to usage-based pricing such as per-token billing for LLM APIs.

## A second protocol: two servers and a referee

The paper also presents a protocol in the refereed delegation model of Canetti, Riva and Rothblum. Two servers compute the inference, and at least one is assumed honest. If their claims differ, a bisection over the hashed execution trace narrows the dispute until a referee needs to check only a single step. The number of rounds is logarithmic in the size of the model.

This is a different bargain. It needs a second server and an assumption that one of the two is honest, and in return it identifies the correct output rather than detecting a different model. The authors note that the same bisection blueprint underpins optimistic rollups on Ethereum, such as Arbitrum and Optimism, and that applying the refereed model to AI was first proposed in earlier work on optimistic machine learning, which did not provide experimental validation.

## Where this leaves a technical team

The results sketch a division of labour. Exact cryptographic proofs give the strongest guarantee and cost the most to produce: 388.3 seconds for Llama-2-7B in the authors' benchmark. The sampling protocol gives a narrower guarantee, other-model soundness, with proving in milliseconds and a proof of a few megabytes.

My view is that the narrower guarantee is the one more likely to be deployed. A check cheap enough to run routinely can sit in front of real traffic; one that takes minutes per query mostly cannot. The substitution cases the paper raises (a cheaper model, a dealigned model, a model trained on data the provider had no right to use) all come down to whether the deployed model is the committed one, which is the question other-model soundness answers.

I'd hold that view with the same care the authors show. The experiments cover two model families and three attack strategies. The protocol exposes model internals in its proofs. And the SNARK side is not standing still, so the comparison point may move.

The open question is the one the authors name themselves. The defence was tested against gradient-descent reconstruction, inverse transforms and logit swapping, and the swap attack came an order of magnitude closer than the others. The authors invite analysis against more adaptive adversaries, such as generative adversarial networks trained to produce consistent, honest-looking activation paths. How the protocol holds up against those is what a team adopting it would most want to know.

## Frequently Asked Questions

**What problem does verifiable inference solve?**
It lets a client check that a cloud-hosted model's answer was computed correctly by the intended model, without rerunning the model. The paper notes that rerunning a large model locally is infeasible for most users, and that clients otherwise have no guarantee that responses are correct or came from the intended model.

**How is the sampling-based protocol different from a SNARK?**
A SNARK checks every step of the computation and yields a proof of exact correctness, at proof-generation overhead the paper puts at typically 1000× or larger. The sampling protocol commits to the execution trace with Merkle-tree-based vector commitments and checks only a few randomly sampled paths from output to input, giving approximate rather than exact correctness.

**How fast is it?**
In the authors' benchmark on Llama-2-7B, zkLLM took 388.3 seconds to prove and 2.36 seconds to verify, with a 183 kB proof. The new protocol committed to the trace in 5.8 milliseconds and verified in 12.44 milliseconds, with a proof of about 3.4 MB.

**What does other-model soundness guarantee?**
It guarantees that the client can detect a server that used a model whose behaviour differs substantially from the intended one. It does not cover every cheating strategy: full soundness for LLMs, where a server may forge an arbitrary output and trace, is left as an open problem.

**Does the protocol keep the model's weights private?**
No. The authors state that the protocol is not zero-knowledge and that opening values in the clear reveals information about the underlying model. They discuss adding zero-knowledge to the sampled path as future work.

## References

- Pranay Anchuri, Matteo Campanelli, Paul Cesaretti, Rosario Gennaro, Tushar M. Jois, Hasan S. Kayman and Tugce Ozdemir, (2026). [Towards Verifiable AI with Lightweight Cryptographic Proofs of Inference ⧉](https://eprint.iacr.org/2026/541 "Towards Verifiable AI with Lightweight Cryptographic Proofs of Inference"). IACR Cryptology ePrint Archive, Paper 2026/541.
- Justin Thaler, (2022). [Measuring SNARK performance: Frontends & backends ⧉](https://a16zcrypto.com/posts/article/measuring-snark-performance-frontends-backends-and-the-future/ "Measuring SNARK performance"). a16z.
- Haochen Sun, Jason Li and Hongyang Zhang, (2024). [zkLLM: Zero Knowledge Proofs for Large Language Models, public implementation ⧉](https://github.com/jvhs0706/zkllm-ccs2024 "zkLLM implementation"). GitHub.
- Yifan Sun, Yuhang Li, Yue Zhang, Yuchen Jin and Huan Zhang, (2025). [SVIP: Towards Verifiable Inference of Open-source Large Language Models ⧉](https://arxiv.org/abs/2410.22307 "SVIP"). arXiv.
- Ulrich Aïvodji, Hiromi Arai, Olivier Fortineau, Sébastien Gambs, Satoshi Hara and Alain Tapp, (2019). [Fairwashing: the risk of rationalization ⧉](https://proceedings.mlr.press/v97/aivodji19a.html "Fairwashing: the risk of rationalization"). Proceedings of the 36th International Conference on Machine Learning, PMLR 97.
- KD Conway, Cathie So, Xiaohang Yu and Kartin Wong, (2024). [opML: Optimistic Machine Learning on Blockchain ⧉](https://arxiv.org/abs/2401.17555 "opML"). arXiv.
