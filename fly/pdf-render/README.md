# pdf-render — WeasyPrint PDF service

Single-route Flask app behind a Fly.io free-tier machine. Renders one
article from sebastienrousseau.com into a PDF/A-quality download.

Sits behind the Cloudflare lang-router Worker at
`/api/pdf/<slug>.pdf`. The Worker proxies, the Edge caches the
response for 24h `immutable`, and repeat reads never reach Fly.

## One-time deploy

```bash
cd fly/pdf-render
fly auth login                                 # opens browser
fly launch --copy-config --name pdf-render --org personal --region lhr
# (no Postgres, no Redis, no Tigris — accept the defaults that say "no")
fly deploy
fly status                                     # should show 1 machine running
```

The free-tier app auto-stops after 5 minutes idle and auto-starts on
inbound. First render after idle pays ~600ms cold-start; subsequent
renders are ~600-1200ms. With Edge cache absorbing every repeat,
the Fly machine sees one request per article per day at most.

## Routes

```
GET /healthz                — liveness probe (Fly machine check)
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

The Worker route `/api/pdf/<slug>.pdf` is added to `workers/lang-router.js`.
It validates the slug, then `fetch(`${PDF_RENDER_BASE}/render?slug=${slug}`)`
where `PDF_RENDER_BASE = "https://pdf-render.fly.dev"` (the default Fly
hostname; set a custom domain after deploy if you prefer).

The Cloudflare Cache rule applies `Cache-Control: public, max-age=86400,
immutable` on the way out, so repeats never touch Fly.

## Free-tier budget

- Fly.io free: 3 shared-cpu-1x machines, 256 MB RAM each, auto-stop.
- The app is one machine. Auto-stops when idle. Carbon-budget conscious.
- WeasyPrint cold start: ~600ms. Render: ~600-1200ms per article.
- Bandwidth: 100 GB/mo free. Each PDF is ~80-200 KB. Easily under budget.
