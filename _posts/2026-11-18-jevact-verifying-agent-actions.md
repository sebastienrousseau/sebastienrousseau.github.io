---

# Front Matter (YAML)

author: "contact@sebastienrousseau.com (Sebastien Rousseau)"
banner_alt: "Glowing blue hexagonal shapes linked across a dark background"
banner_height: "1597"
banner_width: "2584"
banner: "https://cloudcdn.pro/stocks/images/fabio-oyXis2kALVg.webp"
cdn: "https://cloudcdn.pro"
charset: "UTF-8"
cname: "sebastienrousseau.com"
copyright: "© Copyright 2025 - 2026 - Sebastien Rousseau. All rights reserved."
date: "November 18, 2026"
description: "JevAct checks selected LLM agent actions before they run. Against same-model ReAct baselines, gains were consistent on Telecom and BFCL but mixed on Airline."
format-detection: "telephone=no"
hreflang: "en"
icon: "https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/sebastienrousseau.svg"
id: "https://sebastienrousseau.com/2026-11-18-jevact-verifying-agent-actions"
image_alt: "Black and White Portrait of Sebastien Rousseau"
image_height: "162"
image_width: "162"
image: "https://cloudcdn.pro/stocks/images/sebastienrousseau.webp"
keywords: "LLM agents, agent verification, runtime verification, decision models, tool-using agents, JevAct, Kev decision model, ReAct, tau2-bench, BFCL, agent guardrails, policy compliance"
language: "en-GB"
last_reviewed: "2026-11-18"
layout: "report"
locale: "en_GB"
logo_alt: "Logo for Sebastien Rousseau"
logo_height: "44"
logo_width: "44"
logo: "https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/sebastienrousseau.svg"
menu: ""
measurementID: "G-169G4ET5HQ"
name: "Sebastien Rousseau"
permalink: "https://sebastienrousseau.com/2026-11-18-jevact-verifying-agent-actions"
rating: "general"
referrer: "no-referrer"
robots: "index, follow"
schema: "Article"
changefreq: "weekly"
revisit-after: "7 days"
site_software: "Static Site Generator, Rust"
topic_clusters: "generative-ai-llms"
seo_title: "Verifying Agent Actions Before They Run: JevAct's Decision-Model Gate"
short_name: "sebastienrousseau"
subtitle: "Most agent loops run a tool call the moment the model proposes it, and JevAct's results suggest that a cheap, probability-based checkpoint placed just before execution can make tool-using agents more reliable, though the gains vary sharply by benchmark."
tags: "AI agents, LLM agents, agent safety, runtime verification, decision models, guardrails, benchmarks, IBM"
theme-color: "0, 83, 191"
title: "Verifying Agent Actions Before They Run: JevAct's Decision-Model Gate"
url: "https://sebastienrousseau.com/2026-11-18-jevact-verifying-agent-actions"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"

# RSS - The RSS feed front matter (YAML).
atom_link: "https://sebastienrousseau.com/2026-11-18-jevact-verifying-agent-actions/rss.xml"
category: "AI"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "Static Site Generator (SSG) (version 0.0.26)"
draft_engine: "claude"
draft_model: "sonnet"
draft_version: "0.0.46"
item_description: "JevAct checks selected LLM agent actions before they run. Against same-model ReAct baselines, gains were consistent on Telecom and BFCL but mixed on Airline."
item_guid: "https://sebastienrousseau.com/2026-11-18-jevact-verifying-agent-actions/rss.xml"
item_link: "https://sebastienrousseau.com/2026-11-18-jevact-verifying-agent-actions/rss.xml"
item_pub_date: "Wed, 18 Nov 2026 00:00:00 +0000"
item_title: "Verifying Agent Actions Before They Run: JevAct's Decision-Model Gate"
last_build_date: "Wed, 18 Nov 2026 00:00:00 +0000"
managing_editor: "contact@sebastienrousseau.com (Sebastien Rousseau)"
pub_date: "Wed, 18 Nov 2026 00:00:00 +0000"
ttl: "60"
type: "article"
webmaster: "contact@sebastienrousseau.com"

# Apple - The Apple front matter (YAML).
apple_mobile_web_app_orientations: "portrait"
apple_touch_icon_sizes: "192x192"
apple-mobile-web-app-capable: "yes"
apple-mobile-web-app-status-bar-inset: "black"
apple-mobile-web-app-status-bar-style: "black-translucent"
apple-mobile-web-app-title: "Verifying Agent Actions Before They Run: JevAct's Decision-Model Gate"
apple-touch-fullscreen: "yes"

# MS Application - The MS Application front matter (YAML).

msapplication-navbutton-color: "0, 83, 191"

# Twitter Card - The Twitter Card front matter (YAML).

twitter_card: "summary_large_image"
twitter_creator: "@wwdseb"
twitter_description: "JevAct checks selected LLM agent actions before they run. Against same-model ReAct baselines, gains were consistent on Telecom and BFCL but mixed on Airline."
twitter_image: "https://cloudcdn.pro/stocks/images/fabio-oyXis2kALVg.webp"
twitter_image_alt: "Glowing blue hexagonal shapes linked across a dark background"
twitter_site: "@wwdseb"
twitter_title: "Verifying Agent Actions Before They Run: JevAct's Decision-Model Gate"
twitter_url: "https://sebastienrousseau.com/2026-11-18-jevact-verifying-agent-actions"

excerpt: "Most agent loops run a tool call the moment the model proposes it, and JevAct's results suggest that a cheap, probability-based checkpoint placed just before execution can make tool-using agents more reliable, though the gains vary sharply by benchmark."

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://sebastienrousseau.com"
author_twitter: "@wwdseb"
author_location: "London, UK"
thanks: "Thanks for reading!"
site_last_updated: "2026-11-18"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "Kaishi, Kaishi Builder, Kaishi CLI, Kaishi Templates, Kaishi Themes"

---

# Verifying Agent Actions Before They Run: JevAct's Decision-Model Gate

**Most agent loops run a tool call the moment the model proposes it, and JevAct's results suggest that a cheap, probability-based checkpoint placed just before execution can make tool-using agents more reliable, though the gains vary sharply by benchmark.**

<!-- lead-start -->
<aside class="post-lead" aria-label="Article summary">
<p class="post-lead-tldr"><strong>TL;DR.</strong> JevAct is a runtime verification framework that intercepts selected agent actions before execution and returns targeted feedback for bounded revision. It combines executable checks over tool state with a prefill-only decision model called Kev. Against a ReAct harness using the same agent LLM, all eight agents tested on Telecom improved on both at-least-once and three-run success, and all nine on BFCL improved in three-run success, though their at-least-once results were mixed; Airline effects were smaller and varied by agent.</p>
<p class="post-lead-heading"><strong>Key takeaways</strong></p>
<ul class="post-lead-takeaways">
  <li><strong>The gap is real.</strong> Proposed actions are often executed without independent verification of policy compliance or task completion.</li>
  <li><strong>Two kinds of check.</strong> Deterministic code verifies tool-state facts; a decision model assesses conversational context probabilistically.</li>
  <li><strong>Nothing about the agent changes.</strong> The agent's LLM, base prompt and tools stay as they were.</li>
  <li><strong>Results are uneven.</strong> Telecom gains are uniform across agents, BFCL at-least-once results are mixed, and Airline varies by agent.</li>
  <li><strong>The evidence covers the whole harness.</strong> The comparisons evaluate the full system, not the judge in isolation.</li>
</ul>
</aside>
<!-- lead-end -->

> **Executive Summary**
>
> - LLM agents increasingly take consequential actions through external tools, yet those actions are often executed without independent verification of policy compliance or task completion.
> - JevAct compiles a domain policy offline into questions, rules, executable state checks and, where needed, a hand-off checklist.
> - At runtime, code checks facts in tool records while Kev, an open-sourced Jev-like decision model, answers questions that depend on the conversation.
> - Compared with a ReAct harness on τ²-bench (Airline, Telecom) and BFCL, gains are consistent on Telecom and BFCL's three-run success, and more mixed on Airline.
> - The authors' own framing is cautious: the findings suggest that structured decision models combined with executable verification can improve reliability.

## The problem: execution follows proposal

An agent that books a flight, cancels an order or changes an account setting is doing something that can't be quietly undone. The uncomfortable part is how little stands between the model's suggestion and the effect. Many agent loops execute a proposed tool call as soon as the model produces it. Nobody independently checks whether the action complies with the domain's policy, or whether a task that the agent considers finished is actually finished.

That gap is the starting point of "Think Before You Act: Decision Gate for LLM Agents", a 2026 arXiv preprint by Iftach Shoham, Yuval David and colleagues at IBM, which introduces JevAct. This isn't a new observation, but it's worth stating plainly because so much agent tooling focuses on making the proposer better. ReAct agents interleave reasoning with tool use, and that pattern has become a common baseline. Reflection methods such as Self-Refine and Reflexion add critique and feedback to improve later proposals or trials, without updating model weights. Useful as that is, those methods don't by themselves verify a particular action against a domain policy immediately before execution. The check JevAct cares about sits at a different point in the loop: after a proposal exists and before it commits.

## What JevAct is

JevAct is a harness that checks selected proposals before execution. It's described as a runtime verification framework that intercepts selected agent actions and enables feedback-driven correction. It operates independently of the underlying agent model and requires no modifications to the model's parameters or tools. In the evaluated setup, the agent's LLM, base prompt and tools remain unchanged.

Architecturally, JevAct augments the harness of a ReAct agent by inserting a selective checking stage between message proposal and execution. The word "selective" matters. The framework doesn't inspect every message; it targets particular kinds of action. Two are defined in the paper. A write call changes the environment, for example by booking, cancelling or changing a setting. A hand-off ends the agent's attempt, either by transferring the user to a human or by telling the user that nothing more can be done. Writes are where a policy violation does damage; hand-offs are where an agent can give up too early. The framework's stated aim of identifying potentially invalid actions and premature task termination maps onto those two categories.

When a check fails, the proposal isn't simply blocked. The checks can defer execution and request a revised proposal from the LLM with temporary feedback, subject to a fixed revision budget. A passing proposal proceeds. A flagged one goes back to the agent with targeted feedback and a bounded chance to revise. And the division of labour stays clear: the agent still proposes actions, and Kev doesn't choose them.

## Two kinds of evidence, one gate

The design rests on a split between what can be verified deterministically and what can't. JevAct combines deterministic verification of tool-state facts with probabilistic assessment of conversational context. At runtime, code checks facts available in tool records, and Kev answers the questions that depend on the conversation.

That split is sensible. Some policy conditions are facts sitting in a tool's records, and a program can read them without any model's opinion. Other conditions live in what the user and agent said to each other, which no database lookup will settle. Handing the first kind to code and the second to a model means the model is only asked about things code can't answer.

The offline half is what makes this practical to describe. A compiler turns a domain policy into questions, rules, executable checks over tool state, and where needed, a hand-off checklist. In other words, JevAct compiles domain policies into executable state checks and structured questions evaluated by a prefill-only decision model. The authors say they lay the foundation for a workflow that compiles domain policies into questions, decision rules, executable state checks and hand-off checklists for a decision-model gate. That's a modest way to put it, and I'd take it at face value: the claim is about a workflow's foundation, not a finished product.

## Why a decision model instead of an LLM judge

The obvious alternative is an LLM judge reading the proposal and writing a verdict. The paper's objection is practical. Free-form explanations from such a judge must still be interpreted before a gate can act on them, and making this decision with a frontier model is costly. A gate needs a decision, not an essay.

Decision models are built for that. Jev introduced decision models that return typed choices, scores and probabilities rather than generated text. They return choices and probabilities for fixed questions, which makes threshold-based checks straightforward. The model JevAct uses is prefill-only and produces probability-based judgments without relying on LLM generation. Kev is an open-source Jev-type decision model, placed in a separate verification step before selected actions commit.

There's a catch, and the authors state it themselves. Decision-model probabilities aren't guaranteed to be calibrated or correct, so their value has to be tested in the agent loop rather than assumed. That sentence frames the whole empirical section. The central question is whether a decision model can serve as a probability-thresholded verifier alongside executable tool-state checks. It's a question to be answered by experiment, and the experiment is where the interesting detail lies.

Related work on decision models gives a mixed picture of why that testing matters. Li et al. report competitive results on preference and evidence-grounded factuality but weaker performance when derivation is required. Rao and Callison-Burch report mixed rubric results and overlapping errors with LLM judges. A decision model that's strong at some judgement tasks and weaker at others is precisely the kind of component you'd want to pair with deterministic checks rather than trust alone.

## How the comparison was run

JevAct is compared with a ReAct harness using the same agent LLM in both arms. The tasks span Airline and Telecom in τ²-bench and multi-turn function-calling tasks in BFCL. Holding the agent LLM fixed across both arms is the right control for the question being asked: any difference comes from the harness, not from a stronger or weaker proposer.

The paper reports its results using pass^3 figures, taken from Table 2, along with at-least-once success. Those two measures pull in different directions, and the contrast between them turns out to be informative. Success across all three runs rewards an agent that gets it right every time. At-least-once success rewards an agent that gets it right on any attempt. A verifier that catches bad actions should help the first more reliably than the second, and the results fit that reading, though the paper says only that the BFCL pattern is consistent with more repeatable performance on some tasks, so I'll flag the rest as interpretation rather than finding.

## What the numbers show

On Telecom, all eight agents improve both at-least-once success and success across all three runs. That's the cleanest result in the paper: no exceptions among the agents tested, on either measure.

On BFCL, all nine agents improve in three-run success, but at-least-once results are mixed. Read that carefully. On BFCL, the stricter measure rises for every agent tested, by 0.1 to 9.6 points; the lenient measure improves for four agents and declines for five. If you care about an agent behaving correctly every time, that's the favourable direction. If you care about whether a retry might eventually succeed, the benefit isn't established here.

Airline is the weak spot. Airline effects are smaller and vary by agent. The summary of results puts it as particularly consistent gains on Telecom and BFCL, while performance on Airline is more mixed. A founder reading this shouldn't round that up to "improves everything". The authors report improvements in agent reliability across multiple models and benchmarks, but on Airline gains are smaller and mixed, and they say their findings do not establish uniform gains. The paper cautions that with 50 Airline tasks a single task moves a score by 2 percentage points, so small differences should be read cautiously; beyond that, I won't guess why Airline behaves differently.

The overall reading is hedged by the authors themselves: the findings suggest that combining structured decision models with executable verification can improve the reliability of tool-using LLM agents. "Suggest" is the right verb. It's a promising result, not a proof.

## What the comparison does and doesn't isolate

One limitation deserves more weight than it usually gets. Because JevAct adds compiled checks and revision opportunities, the comparisons evaluate the full harness, not the judge in isolation. That's a significant caveat for anyone hoping to conclude that the decision model is doing the heavy lifting. The gains could come from Kev's probabilities, from the executable state checks, from the extra chances to revise, or from some combination. The main comparisons don't separate them.

I'd argue that's not a flaw so much as an honest description of what a system paper can show. The question the authors pose, whether a decision model can serve as a probability-thresholded verifier alongside executable tool-state checks, is answered at the level of the pair, since "alongside" is in the question itself. But a reader deciding where to invest effort should keep it in mind. If you're building something similar, you can't infer from this evidence that the decision model alone would carry the improvement, nor that the code checks alone would.

It also means the calibration caveat still stands. The probabilities aren't guaranteed to be calibrated or correct, and the harness-level result doesn't remove that uncertainty. It shows that the arrangement as a whole helped on the benchmarks tested.

## Where this sits among other guard designs

JevAct joins a crowded set of approaches to guarding agent actions, and the differences are instructive. GuardAgent uses a separate agent to generate and execute verification code from user-defined guard requirements. Zwerdling et al. compile company policies into executable guards that check compliance before tool actions. AgentSpec represents runtime constraints as triggers, predicates and enforcement actions. ShieldAgent derives verifiable rules from policy documents.

Others lean on models for the verification itself. ToolSafe uses a learned guardrail to assess proposed tool calls and return feedback, while PolicyGuard and PolicyGuide use model-based verifiers for policy adherence and workflow guidance. CaMeL takes a different route, enforcing security through separation of trusted control flow and untrusted data.

Against that background, JevAct's distinguishing choice is its particular pairing. Like the compile-to-executable-guards line of work, it turns policy into checks over tool state. Like the model-based verifiers, it uses a model for judgements code can't make. What it adds is a decision model that returns fixed-choice probabilities, used online before selected actions execute, with feedback for revision. It leaves proposals to the ReAct LLM and puts Kev in a separate verification step before selected actions commit.

## Why this design is worth watching

My view is that the most useful idea here isn't Kev itself but the discipline of the split. Ask code what code can answer. Ask a model only what depends on conversation. Keep the proposer and the verifier separate, so that the model checking an action isn't the one that suggested it. And make the verifier's output a probability against a threshold, so the gate is a comparison rather than a piece of text someone has to parse.

That design also makes the weak points legible. If a check misfires, you can ask whether it was a state check or a conversational question. If the thresholds are wrong, they're numbers you can examine. The paper's own caution that probabilities need testing in the loop is the correct instinct, and it's a better posture than assuming a verifier works because it sounds sensible.

The uneven results are, if anything, reassuring about the honesty of the reporting. A framework claiming uniform gains everywhere would deserve more suspicion than one that shows eight of eight on Telecom, nine of nine on BFCL three-run success, mixed at-least-once results on BFCL, and variable effects on Airline. The pattern gives practitioners something to plan around: the strongest evidence is for reliability across repeated runs, and the weakest is in the domain where effects vary by agent.

## What to do with this

For technical readers, the takeaway is architectural. The agent's LLM, base prompt and tools remain unchanged in JevAct, so the verification layer is something you add around an agent rather than something you train into it. For founders, the practical reading is narrower than the headline. The paper reports improved reliability across multiple models and benchmarks, with Airline more mixed, and its comparisons evaluate the full harness rather than the judge in isolation. The main comparisons don't establish which component earns the improvement, though the paper's Airline ablation suggests that programmatic verification accounts for much of it in that setting.

The open question is the paper's own central one: whether a decision model can serve as a probability-thresholded verifier alongside executable tool-state checks, when, as the authors note, its probabilities are not guaranteed to be calibrated or correct. The Airline results, where effects are smaller and vary by agent, are the place to look first. Whether that variation traces to the checks, the thresholds or the policies being compiled is something the reported results leave open, and it's the experiment I'd most want to see next.

## Frequently Asked Questions

**What is JevAct?**
JevAct is a runtime verification framework from IBM researchers that intercepts selected agent actions, namely write calls and hand-offs, before execution. A flagged proposal goes back to the agent with targeted feedback and a bounded chance to revise. The agent's LLM, base prompt and tools stay unchanged.

**What does Kev do in JevAct?**
Kev is an open-source Jev-like decision model that answers fixed questions with probabilities rather than generated text. In JevAct it answers the questions that depend on the conversation, while code checks facts available in tool records. Kev does not choose actions; the agent still proposes them.

**How was JevAct evaluated?**
The paper compares JevAct with a ReAct harness using the same agent LLM in both arms. The tasks span Airline and Telecom in τ²-bench and multi-turn function-calling tasks in BFCL, with success reported both as at-least-once over three runs and as success in all three runs.

**Did JevAct improve every agent on every benchmark?**
No. On Telecom, all eight agents improved on both measures, and on BFCL all nine improved in three-run success while at-least-once results were mixed. Airline effects were smaller and varied by agent, and the authors say the findings do not establish uniform gains.

**Does the paper show that the decision model alone drives the gains?**
No. Because JevAct adds compiled checks and revision opportunities, the main comparisons evaluate the full harness, not the judge in isolation. The authors also note that decision-model probabilities are not guaranteed to be calibrated or correct.

## References

- Shoham, I., David, Y., Akrabi, O., Bilgory, E., Levy, I., Marreed, S., Zeltyn, S. and Shlomov, S., (2026). [Think Before You Act: Decision Gate for LLM Agents ⧉](https://arxiv.org/abs/2610.38620 "Think Before You Act"). arXiv.
- Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K. and Cao, Y., (2022). [ReAct: Synergizing Reasoning and Acting in Language Models ⧉](https://arxiv.org/abs/2210.03629 "ReAct"). arXiv.
- Barres, V., Dong, H., Ray, S., Si, X. and Narasimhan, K., (2025). [τ²-bench: Evaluating Conversational Agents in a Dual-Control Environment ⧉](https://arxiv.org/abs/2506.07982 "τ²-bench"). arXiv.
- TypeSafe AI, (2026). [Introducing System One Models and Jev ⧉](https://typesafe.ai/blog/introducing-system-one-models-and-jev "Introducing Jev"). TypeSafe AI.
- Palmer, J., (2026). [KEV: Prefill-only Decision Models ⧉](https://github.com/jaredpalmer/kev "KEV"). GitHub.
- Xiang, Z. et al., (2024). [GuardAgent: Safeguard LLM Agents by a Guard Agent via Knowledge-Enabled Reasoning ⧉](https://arxiv.org/abs/2406.09187 "GuardAgent"). arXiv.
- Chen, Z., Kang, M. and Li, B., (2025). [ShieldAgent: Shielding Agents via Verifiable Safety Policy Reasoning ⧉](https://arxiv.org/abs/2503.22738 "ShieldAgent"). arXiv.
- Li, Y., Miao, Y., Krishnan, R. and Padman, R., (2026). [Jev-as-a-Judge: Accept When Confident, Escalate When Unsure ⧉](https://arxiv.org/abs/2609.26550 "Jev-as-a-Judge"). arXiv.
- Rao, D. and Callison-Burch, C., (2026). [Jev vs. LLMs as Rubric Judges: Cheaper, Faster, and Wrong in the Same Places ⧉](https://arxiv.org/abs/2609.29769 "Jev vs. LLMs as Rubric Judges"). arXiv.
