<h1 align="center">pdf-render</h1>

<p align="center">
  A single-route Flask + WeasyPrint service on a Fly.io free-tier machine that
  renders one sebastienrousseau.com article into a PDF/A-quality download.
</p>

---

## Contents

- [Overview](#overview)
- [One-time deploy](#one-time-deploy)
- [Routes](#routes)
- [Local smoke test](#local-smoke-test)
- [Wiring with the Worker](#wiring-with-the-worker)
- [Free-tier budget](#free-tier-budget)
- [License](#license)

## Overview

Sits behind the Cloudflare `lang-router` Worker at `/api/pdf/<slug>.pdf`. The Worker proxies, the edge caches the response for 24h `immutable`, and repeat reads never reach Fly.

## One-time deploy

```bash
cd fly/pdf-render
fly auth login                                 # opens browser
fly launch --copy-config --name pdf-render --org personal --region lhr
# (no Postgres, no Redis, no Tigris — accept the "no" defaults)
fly deploy
fly status                                     # should show 1 machine running
```

The app auto-stops after 5 minutes idle and auto-starts on inbound. First render after idle pays ~600ms cold-start; subsequent renders are ~600–1200ms. With the edge cache absorbing repeats, the machine sees at most one request per article per day.

## Routes

```text
GET /healthz                 — liveness probe (Fly machine check)
GET /render?slug=<slug>      — render one article to PDF
```

## Local smoke test

```bash
cd fly/pdf-render
pip install -r requirements.txt
ORIGIN_BASE=https://sebastienrousseau.com python app.py
# in another shell:
curl 'http://localhost:8080/render?slug=2026-06-08-banking-resilience-index-ai-cloud-quantum-payments-third-party-risk-2026' \
  -o /tmp/test.pdf && open /tmp/test.pdf
```

## Wiring with the Worker

The route `/api/pdf/<slug>.pdf` lives in `workers/lang-router.js`. It validates the slug, then calls `fetch(${PDF_RENDER_BASE}/render?slug=${slug})` where `PDF_RENDER_BASE = "https://pdf-render.fly.dev"` (the default Fly hostname; set a custom domain after deploy if you prefer). The Cloudflare cache rule applies `Cache-Control: public, max-age=86400, immutable`, so repeats never touch Fly.

## Free-tier budget

- Fly.io free: 3 shared-cpu-1x machines, 256 MB RAM each, auto-stop.
- The app is one machine; it auto-stops when idle.
- WeasyPrint cold start ~600ms; render ~600–1200ms per article.
- Bandwidth: 100 GB/mo free; each PDF is ~80–200 KB — easily under budget.

## License

Licensed under [Apache-2.0](../../LICENSE).

<p align="right"><a href="#pdf-render">Back to Top</a></p>
