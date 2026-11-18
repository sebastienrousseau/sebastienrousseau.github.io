---

# Front Matter (YAML)

author: "contact@sebastienrousseau.com (Sebastien Rousseau)"
banner_alt: "Blue light lines crossing in a network over a dark reflective floor"
banner_height: "1597"
banner_width: "2584"
banner: "https://cloudcdn.pro/stocks/images/johann-juraver-qyFaXDPecSQ.webp"
cdn: "https://cloudcdn.pro"
charset: "UTF-8"
cname: "sebastienrousseau.com"
copyright: "© Copyright 2025 - 2026 - Sebastien Rousseau. All rights reserved."
date: "November 24, 2026"
description: "DeepSeek Harness argues that one session per task caps parallel agent work at human attention, and proposes a Router and Worker design it calls a Super-agent."
format-detection: "telephone=no"
hreflang: "en"
icon: "https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/sebastienrousseau.svg"
id: "https://sebastienrousseau.com/2026-11-24-super-agents-one-session-per-task"
image_alt: "Black and White Portrait of Sebastien Rousseau"
image_height: "162"
image_width: "162"
image: "https://cloudcdn.pro/stocks/images/sebastienrousseau.webp"
keywords: "super-agent architecture, AI agent orchestration, multi-agent systems, agent session management, router worker architecture, DeepSeek Harness, ReAct loop, event-driven agents, agent concurrency, autonomous coding agents"
language: "en-GB"
last_reviewed: "2026-11-24"
layout: "report"
locale: "en_GB"
logo_alt: "Logo for Sebastien Rousseau"
logo_height: "44"
logo_width: "44"
logo: "https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/sebastienrousseau.svg"
menu: ""
measurementID: "G-169G4ET5HQ"
name: "Sebastien Rousseau"
permalink: "https://sebastienrousseau.com/2026-11-24-super-agents-one-session-per-task"
rating: "general"
referrer: "no-referrer"
robots: "index, follow"
schema: "Article"
seo_title: "Super-agents: why one session per task stops scaling"
short_name: "sebastienrousseau"
subtitle: "A single task is limited by model capability, but multi-tasking is limited by human attention, and the fix is an architecture rather than a better model."
tags: "super-agents, AI agents, agent architecture, multi-agent systems, DeepSeek Harness, agentic AI, concurrency, software development"
theme-color: "0, 83, 191"
title: "Super-agents: why one session per task stops scaling"
url: "https://sebastienrousseau.com/2026-11-24-super-agents-one-session-per-task"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"

# RSS - The RSS feed front matter (YAML).
atom_link: "https://sebastienrousseau.com/2026-11-24-super-agents-one-session-per-task/rss.xml"
category: "AI"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "Static Site Generator (SSG) (version 0.0.26)"
draft_engine: "claude"
draft_model: "sonnet"
draft_version: "0.0.46"
item_description: "DeepSeek Harness argues that one session per task caps parallel agent work at human attention, and proposes a Router and Worker design it calls a Super-agent."
item_guid: "https://sebastienrousseau.com/2026-11-24-super-agents-one-session-per-task/rss.xml"
item_link: "https://sebastienrousseau.com/2026-11-24-super-agents-one-session-per-task/rss.xml"
item_pub_date: "Tue, 24 Nov 2026 00:00:00 +0000"
item_title: "Super-agents: why one session per task stops scaling"
last_build_date: "Tue, 24 Nov 2026 00:00:00 +0000"
managing_editor: "contact@sebastienrousseau.com (Sebastien Rousseau)"
pub_date: "Tue, 24 Nov 2026 00:00:00 +0000"
ttl: "60"
type: "article"
webmaster: "contact@sebastienrousseau.com"

# Apple - The Apple front matter (YAML).
apple_mobile_web_app_orientations: "portrait"
apple_touch_icon_sizes: "192x192"
apple-mobile-web-app-capable: "yes"
apple-mobile-web-app-status-bar-inset: "black"
apple-mobile-web-app-status-bar-style: "black-translucent"
apple-mobile-web-app-title: "Super-agents: why one session per task stops scaling"
apple-touch-fullscreen: "yes"

# MS Application - The MS Application front matter (YAML).

msapplication-navbutton-color: "0, 83, 191"

# Twitter Card - The Twitter Card front matter (YAML).

twitter_card: "summary_large_image"
twitter_creator: "@wwdseb"
twitter_description: "DeepSeek Harness argues that one session per task caps parallel agent work at human attention, and proposes a Router and Worker design it calls a Super-agent."
twitter_image: "https://cloudcdn.pro/stocks/images/johann-juraver-qyFaXDPecSQ.webp"
twitter_image_alt: "Blue light lines crossing in a network over a dark reflective floor"
twitter_site: "@wwdseb"
twitter_title: "Super-agents: why one session per task stops scaling"
twitter_url: "https://sebastienrousseau.com/2026-11-24-super-agents-one-session-per-task"

excerpt: "A single task is limited by model capability, but multi-tasking is limited by human attention, and the fix is an architecture rather than a better model."

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://sebastienrousseau.com"
author_twitter: "@wwdseb"
author_location: "London, UK"
thanks: "Thanks for reading!"
site_last_updated: "2026-11-24"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "Kaishi, Kaishi Builder, Kaishi CLI, Kaishi Templates, Kaishi Themes"
changefreq: "weekly"
revisit-after: "7 days"
site_software: "Static Site Generator, Rust"
topic_clusters: "generative-ai-llms"

---

# Super-agents: why one session per task stops scaling

**A single task is limited by model capability, but multi-tasking is limited by human attention, and the fix is an architecture rather than a better model.**

<!-- lead-start -->
<aside class="post-lead" aria-label="Article summary">
<p class="post-lead-tldr"><strong>TL;DR.</strong> Mainstream agents treat one isolated session as the unit of work, so a person ends up as the scheduler for parallel tasks. The authors propose a Super-agent: one continuous entity built on a two-level architecture, with a long-lived Router layer handling all human interaction and a context-isolated Worker layer running tasks concurrently.</p>
<p class="post-lead-heading"><strong>Key takeaways</strong></p>
<ul class="post-lead-takeaways">
  <li><strong>The bottleneck has moved.</strong> Models can use tools to solve complex problems with less supervision, yet sessions stay isolated and the user must remember what each one contains.</li>
  <li><strong>Four characteristics define the target.</strong> The authors believe a Super-agent is continuous, productive, proactive and persistent, and that no single ReAct loop can supply all four.</li>
  <li><strong>Sessions force a trade-off.</strong> Routing everything to one session gives the most continuous context; a new session per event gives the most throughput. Neither alone works.</li>
  <li><strong>Two levels resolve it.</strong> A Router layer keeps global continuity while isolated Worker Sessions execute tasks concurrently.</li>
</ul>
</aside>
<!-- lead-end -->

> **Executive Summary**
>
> - Coding agents and other single-task agents have shown that models can use tools to solve complex problems while needing less and less continuous monitoring and step-by-step intervention from humans.
> - Today's mainstream designs use a single session as the basic unit of work, and sessions are isolated from one another. A user running several tasks in parallel has to switch between them by hand.
> - Bolting CLIs, MCP or external connectors onto a local single-session agent lets it receive external messages, but its basic limitations remain.
> - The authors call the alternative a Super-agent. They believe it has four characteristics: continuous, productive, proactive and persistent.
> - The two-level architecture, a Router layer plus Worker Sessions, provides both continuous interaction and productive concurrency.

## The models got better; the workflow didn't

This piece reads "Exploring Super-agent Design: Towards a More Autonomous Agent System", a post published on X by DeepSeek Harness (@DeepSeekHarness) on 1 November 2026, written by Yujia Qiao on behalf of the DeepSeek Harness team and presented as a machine translation of a Chinese original.

Coding agents and other single-task agents have shown something worth stating plainly. Models can use tools to solve complex problems, and they need less and less continuous monitoring and step-by-step intervention from humans. Models have also become better at coordinating multiple agents, which makes it practical to organise and schedule work across sessions.

That second point matters more than it first appears. If coordination is practical, the interesting question is no longer whether an agent can finish a hard task. It's what happens when you hand it five of them.

Personal agents hint at the answer. They connect directly to everyday messaging, calendar, email and work platforms, monitor the feeds, and help with tasks. The post states that this always-online, event-driven way of working isn't specific to personal use and is also valuable in commercial work such as software development. It asserts that rather than measuring it, and it's worth reading it that way. But the direction is clear enough: an agent that sits inside the places where work already happens, rather than waiting for a prompt in a terminal.

## Where the single-session design breaks

Agents still use a single session as the basic unit of work, and sessions are isolated from one another. That's a tidy abstraction for one task. It becomes awkward the moment there are several.

A user running several tasks in parallel has to switch between sessions by hand and remember what each one contains. In the authors' experience, a person can usually follow only 3 to 5 active sessions at once. That figure comes from experience rather than from a controlled study, so treat it as a rule of thumb. Even so, it points at the structural problem. With these designs, a single task is limited by model capability, but multi-tasking is limited by human attention.

Read that sentence twice. It says that improving the model won't, by itself, raise the ceiling on parallel work. The ceiling is the person holding the sessions in their head. I'd argue this is the most useful framing in the whole argument, because it relocates the problem from the model, where most effort goes, to the system around it.

## Why connectors don't fix it

The obvious patch is to extend what already exists. Add CLIs, MCP or external connectors to a local single-session agent, and it can receive external messages. The authors' point is that its basic limitations remain.

They list those limitations concretely. Such a setup still runs in one synchronous session that blocks on long operations. Contexts from different tasks get mixed together. Everything stops whenever the local device goes offline. And keeping the whole arrangement running takes a lot of manual effort.

Each of those is a different kind of failure. Blocking is a throughput problem. Mixed contexts are a correctness problem. Going offline with the laptop is an availability problem. Manual upkeep is an operational one. A connector addresses none of them, because a connector only changes how messages arrive. It doesn't change what the session is.

## Decoupling the agent from the session

The post states that getting past these limits means decoupling the agent from any single, manually driven session. What follows is phrased as what the agent should be rather than as a measured result, so it's best read as the authors' design thesis.

The thesis goes like this. The agent should be one continuous entity that keeps its context across sessions and works on several complex tasks at once, without the tasks interfering with each other. The authors call this kind of agent, and its system architecture, a Super-agent.

They report a working example. Their internal Super-agent instance, which runs on DeepSeek Harness, can continue the same development task across IM and GitHub. It also monitors feedback in public group chats and, even when no one @-mentions it, finds root causes on its own and opens Pull Requests to fix them. The post doesn't give success rates or counts of Pull Requests for these two behaviours, so they are demonstrations of capability rather than benchmarks. Still, the second behaviour is striking. Nobody asked, and the agent acted.

## Four characteristics

The post states that a Super-agent has four basic characteristics: continuous, productive, proactive and persistent. The authors frame this as their belief, and each term has a specific meaning.

A continuous agent lets users interact with it directly where they already work, such as IM chats and GitHub comments, and it always feels like one agent. The post's example is a user who asks for Plan A in IM and later switches to Plan B in a GitHub Pull Request comment. The agent understands the change and adjusts what it's doing. The channel changed; the conversation didn't.

A productive agent responds quickly and completes several complex tasks in parallel, each to a high standard. It can also take the next instruction before the previous command or task has finished. That removes the blocking behaviour described earlier.

A proactive agent monitors events in its environment, acts on anything worth handling, and stays quiet otherwise. The last clause deserves attention. An agent that acts on everything is noise. Staying quiet is part of the specification.

A persistent agent is always online, connects directly to the user's real working environments, and recovers automatically from anomalies during long-running operation.

Then comes the constraint that drives the rest of the design: no single ReAct loop can provide all four characteristics at once, so they have to come from the system architecture around it. The post states this without hedging, and it's the reason this is an architecture article rather than a prompting one.

## Convergence, and an old set of problems

The post expects personal agents and agents for commercial work such as software development to end up with similar designs when the goal is an always-online system that responds to environmental events concurrently. It's an expectation, hedged accordingly. If it holds, the people building a personal assistant and the people building a development agent are solving the same problem, and they could share a good deal of design.

There's a second observation that I find reassuring. Building such a system raises many problems much like those long studied in computer systems, so many classic design ideas from that field apply here too. The authors don't say which ideas, and I won't guess. But the implication for founders is practical: you aren't facing an entirely unmapped problem. Scheduling, isolation and recovery already have long histories.

The authors think five modules form the basic framework that supports the four characteristics, while implementations will vary. Again, that's their judgement rather than a proven decomposition. Four of the modules are mapped to the characteristics as follows.

The two-level architecture (Section 2) provides both continuous interaction and productive concurrency. The event-driven design (Section 3) makes the agent proactive. Full-duplex multi-channel interaction (Section 4) keeps each exchange with users both continuous and productive. Separating compute, state and environments (Section 5), together with a Watchdog (Section 6), keeps the agent persistently online across devices and lets it recover from anomalies on its own.

The rest of this piece concentrates on the first of those, the two-level architecture.

## The trade-off between continuity and throughput

Supporting both continuous interaction across channels and productive concurrency across tasks forces a fundamental trade-off between continuity and throughput in how the system organises its sessions. There are two obvious ways to organise them, and each fails in a predictable way.

The first is to route every event to one session. That gives the most continuous context, because that session sees everything. The cost is speed. A ReAct loop runs one step at a time, which caps how fast a single session can work: tasks take a long time and throughput stays low. The intermediate details of different tasks also end up interleaved in one context, which degrades the results. So the session that knows the most also reasons the worst, since it's reading a jumble.

The second is to give every event its own new session. That maximises concurrent throughput, but when tasks aren't fully independent, the lack of a shared global context leaves their results disconnected. Several sessions replying to the user separately also make the interaction confusing. The user gets five voices where they wanted one.

Neither extreme is acceptable, and the trade-off is real rather than a matter of tuning. A system that wants both continuity and throughput has to separate the two jobs.

## One session, two jobs

The post identifies why the jobs are tangled in the first place. In existing designs, a session does two jobs: it manages the model's context, and it is the user's unit of project management. One object carries both responsibilities, so improving one degrades the other. Give the user a single session to follow, and the context gets polluted. Give the model clean, isolated contexts, and the user has to juggle them.

This is the reason the 3 to 5 session figure bites. The user's unit of project management is the session, so the number of sessions they can track becomes the number of projects they can run.

## The two-level architecture

The proposal splits the responsibilities. A long-lived Router layer (Section 2.1) maintains global continuity by handling all human interaction and global coordination. A context-isolated Worker layer (Section 2.2) runs tasks with high concurrency. Put together: the Router layer handles all routing and external interaction, while multiple isolated Worker Sessions execute tasks concurrently.

The Router layer is a long-lived global routing layer that receives human interaction from every entry point. That's why the agent always feels like one agent. Whatever channel a message arrives on, it lands in the same place. The Workers, meanwhile, keep their contexts isolated, so the interleaving problem from the single-session design doesn't arise inside them.

The authors add a clarification that's easy to miss. The two levels are a logical division of responsibilities, and neither layer has to be implemented as a single session. The Router isn't necessarily one process holding one context, and the Worker layer isn't necessarily one pool. The architecture describes who's responsible for what, not how many sessions exist.

The practical consequence is stated directly: the system takes over context management and concurrent execution, so users seldom have to think about sessions. This is what addresses the attention ceiling. If the person no longer needs to remember what each session contains, the 3 to 5 limit stops being the limit on how many tasks can run. The post doesn't say how many tasks its internal instance runs concurrently, so I can't say where the new limit sits.

## What the post supports, and what it doesn't

It's worth being honest about the evidence here. The strong claims are structural. Sessions are isolated, a single ReAct loop runs one step at a time, a single shared session interleaves contexts, and a session per event disconnects results. The post states those without hedging.

The softer claims are the ones that carry the ambition. The Super-agent definition, the four characteristics, the five-module framework and the expected convergence of personal and commercial designs are all hedged in the post. The authors believe, think and expect them. None is presented as a measured outcome.

The internal instance on DeepSeek Harness is described through behaviours: continuing one development task across IM and GitHub, and spotting root causes in public group chats before anyone asks. It's an existence proof, not a performance study. The post does report preliminary experiments, but the authors say they use synthetic workloads and simplified environments and that the results are indicative only. In that ablation, Super-agent completed tasks in 12.4 minutes at p50 and 15.7 minutes at p95, faster than a single session with a subagent tool, while using more cache-read tokens per run. For a technical reader, that's the right level of confidence to carry away: the design is coherent and the failure modes of the alternatives are well described, but the numbers come from simulated work, not from the instance in daily use.

## What a founder should take from this

If you're building an agent product, the first lesson is to stop treating the session as the product. A session is an implementation detail of context management that has been promoted to a user interface. The authors' argument is that this promotion is what caps parallel work, and I think they're right to put the problem there.

The second lesson concerns where you place your effort. A single task is limited by model capability, so a better model helps a single task. Multi-tasking is limited by human attention, so a better model doesn't obviously help it. Architecture does. A Router that absorbs every entry point and Workers that keep contexts apart are the kind of structure that moves the ceiling.

The third is about scope. Personal agents that sit in messaging, calendar, email and work platforms and the commercial development agents that answer a group chat with a Pull Request look like different products. The authors expect them to converge on similar designs, so a team building one shouldn't ignore progress on the other.

None of that makes the build easy. Persistence alone asks for compute, state and environments to be separated, plus a Watchdog so the agent recovers from anomalies by itself. Proactivity asks for an event-driven design. Full-duplex multi-channel interaction has its own section. The two-level architecture is one of five modules, not the entire answer.

## An open question

The post leaves one thing open, and it's the one I'd most want answered. The Router handles all human interaction and global coordination, and the Workers are isolated by design. The post says the trade-off between continuity and throughput is fundamental, and that the two-level split provides both. For tasks that touch the same environment, it says Workers subscribed to that environment's Thread receive the same event notifications, and the Router relays the few cases that need coordination across tasks. It also says that once tasks grow larger and more tightly coupled than one Router Session can handle, the right structure for each layer is not yet settled. The session-per-event failure was disconnected results from tasks that weren't independent. How the Router passes just enough global context down, without reintroducing the interleaving it was meant to prevent, is where the design will be tested.

## Frequently Asked Questions

**What is a Super-agent?**
It's the post's name for an agent, and its system architecture, that is decoupled from any single, manually driven session. The agent is one continuous entity that keeps its context across sessions and works on several complex tasks at once without the tasks interfering with each other.

**Why does one session per task stop scaling?**
Sessions are isolated, so a user running several tasks in parallel has to switch between them by hand and remember what each one contains. In the authors' experience a person can usually follow only 3 to 5 active sessions at once, so multi-tasking is limited by human attention rather than model capability.

**Why don't CLIs, MCP or connectors solve the problem?**
They let a local single-session agent receive external messages, but its basic limitations remain. It still blocks on long operations in one synchronous session, mixes contexts from different tasks, stops when the local device goes offline and takes a lot of manual effort to keep running.

**How does the two-level architecture work?**
A long-lived Router layer handles all human interaction and global coordination, while a context-isolated Worker layer runs tasks with high concurrency. The two levels are a logical division of responsibilities, and neither layer has to be implemented as a single session.

**How strong is the evidence for the design?**
The post describes an internal Super-agent instance running on DeepSeek Harness and reports preliminary experiments. The authors say those experiments use synthetic workloads and simplified environments, so the results are indicative only.

## References

- Qiao, Y., (2026). Exploring Super-agent Design: Towards a More Autonomous Agent System. DeepSeek Harness (@DeepSeekHarness) on X.
