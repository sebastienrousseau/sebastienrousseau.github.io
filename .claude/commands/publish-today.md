---
description: Promote today's _drafts/ article, validate voice/style, pick a banner if needed, translate 27 locale stubs with native SEO + tone, open a feat/<slug> PR, and wait for CI to land green. Invoked manually by Sebastien each evening.
---

You are publishing today's article on `sebastienrousseau.com`. Your job is to ship today's source content end-to-end as a reviewable PR — Sebastien merges it from GitHub the next morning.

**Invocation model**: Sebastien runs this slash command manually each evening so he can review the night's output before merging. There is no LaunchAgent or cloud `/schedule` cron anymore — quality bar is "all CI green on the PR", not "wall-clock latency". Don't return until step 12's CI poll confirms every required check is green (or you've surfaced a specific failure that needs Sebastien's eyes).

## Where you're running — read this first

| Marker | Local (Sebastien's Mac) | Cloud routine (Anthropic) |
|---|---|---|
| `command -v ssg` returns a path | yes | **no** |
| `git push` works | yes | **no** (proxy returns 403) |
| `git -c commit.gpgsign=true commit -S` works | yes | no (no SSH key) |
| `gh pr create` works | yes | maybe — try, fall back to GitHub MCP |
| GitHub MCP tools available | usually no | **yes** |

**Run `command -v ssg` once at the start.** If empty → cloud mode. The two flows diverge at the build step (step 9) and the push step (step 10).

## Constraints (apply in BOTH modes)

- **NEVER** put `ANTHROPIC_API_KEY` in repo secrets, env files, or CI workflows. All translation work happens here in conversation, using Sebastien's Claude subscription.
- **NEVER** force-push, **NEVER** push to `main`. Always open a PR — Sebastien merges from mobile.
- **Never stage `docs/` or `public/`.** The `docs/` snapshot is retired (2026-06-10); CI builds `public/` fresh from source and deploys it via `actions/upload-pages-artifact`. Commit source only — plus `sigstore-bundles/` when a local signed build refreshed it.
- **NEVER** invent statistics, sources, or claims the EN source doesn't make.
- **NEVER** skip a build gate — fix the root cause.

## Steps — execute in order

### 1. Locate today's source

```bash
date -u +%F
```

Find `_drafts/<today>-*.md`. If none exists, stop with: *"no draft for `<today>` — drop one into `_drafts/` first."* If `_posts/<today>-*.md` already exists (a partial earlier run), skip step 2 and resume from step 3.

### 2. Promote the draft

```bash
git mv _drafts/<today>-*.md _posts/
```

### 3. Voice / style / structure gate

Run the editorial gate **before** scaffolding 27 stubs — a defect in EN cascades through every locale and a build failure later is much more expensive than a one-second check now.

```bash
python3 scripts/editorial/check_voice.py --today
```

This script fails non-zero on any of: incomplete frontmatter (missing title/subtitle/description/banner/banner_alt/tags/twitter_*/excerpt/date/keywords); unreachable banner URL; banned filler ("delve into", "embark on", "in conclusion", "let's explore", "it is worth noting", "in today's fast-paced", "in this article", "transformative journey", "unprecedented", "game-changer", "paradigm shift", "synergy", "harness the power", "unlock the potential", …); missing lead aside or Executive Summary blockquote; fewer than three H2 sections; missing FAQ or References; H1 not exactly once; date mismatch between filename and frontmatter.

If it fails, **fix the EN draft and re-run** before proceeding. Stub generation against a broken draft wastes 27 translation slots.

### 4. Banner image (if check_voice flagged banner, OR the draft's banner is a poor semantic fit)

The legacy `pick_banner.py` scored by filename-token overlap with hand-passed hints. That capped quality at "good enough" and tended to repeat generic stock images on substantive technical pieces. Pick the banner **semantically yourself** — you have the full article in context, the model is already paid for, and image fit drives reader trust more than any other single asset choice.

**When this step runs:** always re-evaluate. If the draft already has a fitting, unique, reachable banner, leave it. If the banner is missing, unreachable, generic stock (e.g. `corporate-finance.webp` / `ai-robot.webp` on a non-AI-specific piece), or has already been used by an adjacent recent article, swap it.

```bash
# Available inventory (filename is the only metadata the CDN exposes)
ls /Users/seb/Code/Public/CDN/cloudcdn.pro/stocks/images/ | sort

# Banners already taken — exclude these for uniqueness
grep -h '^banner:' _posts/*.md | sed -E 's|.*/||; s|\.webp.*||' | sort -u
```

Read the article's frontmatter — `title`, `subtitle`, `description`, `keywords`, `tags` — and pick the inventory image whose visible subject best matches the article's semantic content. Prefer:
- **Photographer-attributed shots** (e.g. `luke-ellis-craven-yCsk1q2Eq0o.webp`, `marek-piwnicki-U6WvLJU0l6o.webp`, `riccardo-oliva-C5DLhUkEWfM.webp`) for thought-leadership pieces — editorial-looking, not stock.
- **Topic-specific imagery** (e.g. `circuit_board_cityscape.webp` for AI-as-infrastructure, `pixabay-210547.webp` for balance-sheet / stablecoins, `rustlogs.webp` for Rust libraries, `getty-images-LaU3HadwEeE-unsplash.webp` for quantum-cryptography).
- **Anything that visually answers "what is this article about" in one frame.**
- **Avoid generic-stock filenames** (`corporate-finance.webp`, `ai-robot.webp`) for substantive technical pieces — they signal AI-written content even when the writing is strong.

**URL form depends on filename shape** — the CDN transform endpoint only handles hyphenated filenames:
- Hyphenated filename (e.g. `luke-ellis-craven-yCsk1q2Eq0o.webp`) → use transform for responsive sizing:
  `https://cloudcdn.pro/api/transform?url=/stocks/images/<name>.webp&w=1200&format=webp&q=80`
- Underscored filename (e.g. `circuit_board_cityscape.webp`) → transform endpoint returns 404. Use direct URL:
  `https://cloudcdn.pro/stocks/images/<name>.webp`
- Sanity check with `curl -sI` before committing if you're not sure — `HTTP/2 200` and `content-type: image/webp` are the green signals.

Update the `banner:` line in `_posts/<slug>.md` with your chosen URL. Also update `banner_alt:` to a short concrete description of what's actually in the chosen image (this is what locale sub-agents will translate from, and what screen readers will surface). Re-run `check_voice` to confirm the URL is reachable.

> **Fallback (cloud mode only):** if you need deterministic output and don't have full article context, `python3 scripts/editorial/pick_banner.py --hint <kw>` is still available. Local-mode runs should prefer semantic selection.

### 5. Scaffold the 27 locale stubs

```bash
python3 scripts/editorial/translate_post.py <slug>          # writes 27 _posts/<lang>/<slug>.md + slug-map entries
```

`translate_post.py` is Python-only — identical in both modes. The stubs inherit the EN frontmatter (translation in step 6 also localises frontmatter title/subtitle/description/keywords for SEO).

### 6. Translate all 27 stubs — Executive Pragmatist framework

Dispatch one sub-agent per locale **in parallel batches** (7-at-a-time keeps tool budget reasonable). Each agent edits its locale's stub file via a single `Edit` tool call. The sub-agent prompt is the global Executive Pragmatist framework at `~/.claude/commands/translate.md`, instantiated with the locale code, locale name, and per-locale glossary.

Use this template — replace `<LOC>` (locale code), `<LOCALE_NAME>` (human-readable register), and `<PER_LOCALE_GLOSSARY>` (one-line key term mappings from the framework):

> Translate the body of `_posts/<LOC>/<slug>.md` into native `<LOCALE_NAME>`. Read the EN body from `_posts/<slug>.md` (lines from the H1 onwards, including the `<!-- enrich-start --> ... <!-- enrich-end -->` block at the end).
>
> You are operating as three roles in one: **Senior Technical Editor**, **Global Technical SEO Expert**, and **Master Localization Lead**. Apply the standing Executive Pragmatist framework across four pillars.
>
> **Drop** the `<!-- translation-stub -->` comment and the "Translation pending" blockquote, replace everything from there through end of file with the translation.
>
> **Pillar 1 — Style & Tone (Executive Pragmatist).** Fuse the authoritative macro-analytical rhythm of the *Financial Times* with the zero-fluff, practitioner-led pragmatism of a senior banking technologist. Direct & declarative — no passive voice, no hedged statements. Deeply technical but accessible — use `pacs.008`, `OAuth`, `SR 11-7`, `WORM logs`, `OPA`, `FIPS 203`, `ML-KEM`, `CBPR+`, `TIBER-EU` freely, contextualised around business risk and architecture. Anti-hype — eradicate "revolutionary", "game-changer", "supercharge", "delve", "tapestry", "landscape", "testament", "realm", "pivotal", "unleash", "in today's fast-paced", "furthermore", "in conclusion", "beacon", plus target-language equivalents ("plongeons dans" / "sumérgete" / "tauchen wir ein" / "vamos mergulhar" / etc.). Punchy transitions — short hard-hitting sentences between longer analytical paragraphs ("Don't.", "Two things shifted."). Frame technology as an engineering and governance problem.
>
> **Pillar 2 — Formatting & Structure (zero breakage tolerance).** Every heading (H1/H2/H3), blockquote, bullet, table row, citation link, code span, and ordered list appears at exactly the same nesting in the same order. Preserve embedded HTML — `<aside class="post-lead">`, `<aside class="author-card">`, `<figure>`, `<img>`, custom widget placeholders like `[Insert Interactive Component: …]` MUST be preserved exactly. Translate the **text inside** the tags (alt text, captions, widget prompt copy, `aria-label`) but do not break the syntax, attribute names, or class names. Preserve the contract markers verbatim: `<!-- lead-start -->`, `<!-- lead-start: manual -->`, `<!-- lead-end -->`, `<!-- enrich-start -->`, `<!-- enrich-end -->`. Preserve code-like terms verbatim: `pacs.008`, `POST /accounts/{id}/freeze`, `amount: 0`, `client_credentials`, `X25519MLKEM768`, `FIPS 203`, `ML-KEM-768`, regulatory citation IDs (`SR 11-7`, `SS1/23`, `2022/2554`), JSON keys, XML element names like `<PstlAdr>` / `<RmtInf><Strd>`.
>
> **Pillar 3 — Global SEO (frontmatter localisation).** Translate `title`, `seo_title`, `twitter_title`, `item_title`, `apple-mobile-web-app-title` idiomatically to target the equivalent high-value search intent in `<LOCALE_NAME>` — keep ≤70 chars after translation. Translate `description`, `excerpt`, `twitter_description`, `item_description` to be compelling and within 140-160 characters. Translate `subtitle` fully. Translate `keywords` and `tags` to native technical terms professionals use in the target market while preserving key English search terms that natively rank (`FIPS 203`, `ML-KEM`, `ISO 20022`, `DORA`, `SR 11-7`, `OAuth`, `Kubernetes`). Update `language` / `locale` / `hreflang` to the target code. Translate `banner_alt`, `image_alt`, `logo_alt`, `twitter_image_alt`, `thanks`. **Do not change** `id`, `permalink`, `url`, `cdn`, `cname`, `author`, `name`, `image`, `icon`, `logo`, `twitter_creator`, `twitter_site`, `measurementID`, `theme-color`, dates (`date`, `pub_date`, `item_pub_date`, `last_build_date`, `last_reviewed`), `atom_link`, `twitter_url`, `item_link`, `item_guid`.
>
> **Pillar 4 — Translation accuracy (non-negotiables).** Do not invent statistics, sources, or claims the EN source does not make. Native register, not literal translation — match the executive tone a senior banking technologist would use writing for a board / lead-architect audience in `<LOCALE_NAME>`. Apply the per-locale banking glossary: `<PER_LOCALE_GLOSSARY>`. Citation links format `[Visible text](url "title")` — translate visible text + `title` attribute, NEVER change the URL. Numbers, percentages, dates, statistics are facts — translate the surrounding sentence; never paraphrase the number itself; apply locale-correct numeric conventions. Acronyms stay canonical English with a parenthetical native expansion on first mention if a standard one exists.
>
> **Enrich block at the bottom** (`<!-- enrich-start --> ... <!-- enrich-end -->`): localise to the per-locale canonical pattern. Model on the most recent `_posts/<LOC>/2026-*.md` for the canonical "About the author" structure (aria-label + bio + credentials + "Last reviewed" line).

Dispatch in priority order (highest-traffic markets first): **fr es de it pt-br nl ja zh-hans zh-hant ko ar ru pl cs uk ro tr he hi bn id vi th fil ha yo sv** (27 total).

Per-locale glossary values (substituted into `<PER_LOCALE_GLOSSARY>`):

- **fr**: cloud-native → cloud-natif; tool-call → appel d'outil; guardrails → garde-fous; audit log → journal d'audit; kill switch → coupure d'urgence; bounded workflow → flux de travail délimité; service account → compte de service; least-privilege → moindre privilège; policy-as-code → politique en tant que code; resilience → résilience; sovereignty → souveraineté.
- **es**: agent → agente; tool-call → llamada a herramienta; guardrails → barreras de protección; audit log → registro de auditoría; kill switch → interruptor de emergencia; bounded workflow → flujo de trabajo acotado; cloud-native → nativo en la nube; resilience → resiliencia.
- **de**: agent → Agent; tool-call → Werkzeugaufruf; guardrails → Schutzmechanismen; audit log → Audit-Protokoll; kill switch → Notabschaltung; cloud-native → Cloud-nativ; resilience → Resilienz; sovereignty → Souveränität; least-privilege → Least-Privilege (kept canonical).
- **it**: agent → agente; tool-call → chiamata di strumento; guardrails → guardrail; audit log → registro di audit; kill switch → interruttore di emergenza; bounded workflow → flusso di lavoro delimitato; cloud-native → cloud-nativo; resilience → resilienza.
- **pt-br**: agent → agente; tool-call → chamada de ferramenta; guardrails → guardrails; audit log → log de auditoria; kill switch → interruptor de emergência; bounded workflow → fluxo de trabalho delimitado; cloud-native → cloud-native; outsourcing → terceirização.
- **nl**: agent → agent; tool-call → tool-aanroep; guardrails → vangrails; audit log → auditlog; kill switch → noodknop; bounded workflow → afgebakende workflow; cloud-native → cloud-native; resilience → veerkracht.
- **ja**: agent → エージェント; tool-call → ツール呼び出し; guardrails → ガードレール; audit log → 監査ログ; kill switch → キルスイッチ; cloud-native → クラウドネイティブ; least-privilege → 最小権限; policy-as-code → ポリシー・アズ・コード. Use です・ます register throughout.
- **zh-hans**: agent → 智能体; tool-call → 工具调用; guardrails → 护栏机制; audit log → 审计日志; kill switch → 紧急关停开关; cloud-native → 云原生; least-privilege → 最小权限.
- **zh-hant** (Taiwan): agent → 智能體; tool-call → 工具呼叫; guardrails → 護欄機制; audit log → 稽核日誌; kill switch → 緊急關閉開關; cloud-native → 雲端原生.
- **ko**: agent → 에이전트; tool-call → 도구 호출; guardrails → 가드레일; audit log → 감사 로그; kill switch → 킬 스위치; cloud-native → 클라우드 네이티브. Use formal 합니다체 throughout.
- **ar**: agent → وكيل; tool-call → استدعاء أداة; guardrails → حواجز حماية; audit log → سجل التدقيق; kill switch → مفتاح الإيقاف الطارئ; cloud-native → سحابي الأصل. Western Arabic numerals (66.3% not ٦٦٫٣٪).
- **ru**: agent → агент; tool-call → вызов инструмента; guardrails → защитные ограничения; audit log → журнал аудита; kill switch → аварийный выключатель; cloud-native → облачный изначально.
- **pl**: agent → agent; tool-call → wywołanie narzędzia; guardrails → mechanizmy zabezpieczające; audit log → dziennik audytu; kill switch → wyłącznik awaryjny; cloud-native → cloud-native.
- **cs**: agent → agent; tool-call → volání nástroje; guardrails → ochranné mantinely; audit log → auditní protokol; kill switch → nouzový vypínač.
- **uk**: agent → агент; tool-call → виклик інструмента; guardrails → запобіжники; audit log → журнал аудиту; kill switch → аварійний вимикач.
- **ro**: agent → agent; tool-call → apel de instrument; guardrails → bariere de siguranță; audit log → jurnal de audit; kill switch → întrerupător de urgență.
- **tr**: agent → ajan; tool-call → araç çağrısı; guardrails → güvenlik bariyerleri; audit log → denetim günlüğü; kill switch → acil durdurma düğmesi.
- **he**: agent → סוכן; tool-call → קריאה לכלי; guardrails → מעקפי בטיחות; audit log → יומן ביקורת; kill switch → מתג חירום. Western digits.
- **hi**: agent → एजेंट; tool-call → टूल कॉल; guardrails → सुरक्षा बाधाएं; audit log → ऑडिट लॉग; kill switch → आपातकालीन स्विच.
- **bn**: agent → এজেন্ট; tool-call → টুল কল; guardrails → সুরক্ষা বেড়া; audit log → অডিট লগ; kill switch → জরুরি বন্ধ সুইচ.
- **id**: agent → agen; tool-call → panggilan alat; guardrails → batas pengaman; audit log → log audit; kill switch → sakelar darurat.
- **vi**: agent → tác nhân; tool-call → lệnh gọi công cụ; guardrails → rào chắn an toàn; audit log → nhật ký kiểm toán; kill switch → công tắc dừng khẩn cấp.
- **th**: agent → เอเจนต์; tool-call → การเรียกใช้เครื่องมือ; guardrails → รั้วกันชน; audit log → บันทึกการตรวจสอบ; kill switch → สวิตช์ตัดฉุกเฉิน.
- **fil / ha / yo**: keep canonical English technical terms (tool-call, guardrails, audit log, kill switch, OAuth, OPA); translate the surrounding prose only.
- **sv**: agent → agent; tool-call → verktygsanrop; guardrails → skyddsmekanismer; audit log → revisionslogg; kill switch → nödstopp; cloud-native → molnnativ.

When the parallel batch completes, verify completeness:

```bash
python3 scripts/editorial/translate_post.py <slug> --list-stubs       # should report 'all 27 locales translated'
```

### 6b. Backfill any remaining English frontmatter

Sub-agents translate `title`, `subtitle`, `description`, `keywords`, `twitter_title`, `twitter_description`, and `excerpt`. This step covers the fields they do not touch: `seo_title`, `banner_alt`, `tags`, `item_description`, `item_title`, `twitter_title` (where missed), and `apple-mobile-web-app-title`.

```bash
python3 scripts/editorial/translate_frontmatter.py --slug <slug>
```

The script is idempotent — it only writes a field when the locale value is still byte-for-byte identical to the English source, so it never overwrites a good sub-agent translation. Run it unconditionally; a clean article produces zero writes in under a second.

### 7. Homepage card rotation

Edit `_posts/index.md`: in the `<div class="newsroom-grid feat-latest-grid">` block, **prepend** a new `<article class="newsroom-card">` for today (mirror the structure of the cards already there) and **drop the bottom card** so there are still **6 visible**. The 6-card balance fills the 3-column grid cleanly across all 28 locales (`build_translations.py` rewrites per-locale at build time).

### 8. Listings refresh

These are Python-only and run identically in both modes. `gen_articles.py` now **auto-discovers** the latest dated post — you no longer need to hand-edit the `ARTICLES` list.

```bash
python3 scripts/generators/gen_layouts.py
python3 scripts/generators/gen_articles.py    # auto-prepends today's article via _discover_latest_article()
python3 scripts/generators/gen_projects.py
python3 scripts/generators/gen_papers.py
python3 scripts/postbuild/topic_link.py
python3 scripts/postbuild/post_enrich.py
python3 scripts/generators/build_topics.py    # if today's article fits an existing cluster OR you've added it to TOPICS, the slug shows up here
python3 scripts/generators/build_lang_feeds.py
python3 scripts/generators/build_agent_api.py
```

**Topic cluster note**: if today's article belongs to an existing cluster in `scripts/generators/build_topics.py:TOPICS`, prepend its slug to that cluster's `slugs:` list. If it needs a brand-new cluster, add it (mirror the existing cluster shape — title, banner, lede, slugs). Per-locale topic clones are generated automatically by `build_translations.py`.

### 9. Validate

**Local mode (ssg present):**

```bash
./build.sh
```

Must exit 0. Surfaces i18n leakage, hreflang regression, CSP issue, RTL bug, sitemap completeness gap, news-sitemap duplicate, JSON-LD validation.

**Cloud mode (no ssg):** skip `./build.sh`. Pages-deploy CI runs it on PR merge. Best-effort Python checks:

```bash
python3 -m pytest tests/test_build_translations_smoke.py::test_parse_frontmatter_basic tests/test_translate_post.py tests/test_gen_articles_autodiscover.py -q  || true
```

### 10. Commit + open PR

**Local mode:**

Branch convention: **`feat/<slug>`** where `<slug>` is the full filename stem (already prefixed with the ISO date, e.g. `feat/2026-05-22-uk-acid-jazz-renewal-artists-concerts-albums-2026`). One branch per article — never reuse.

The PR title is `feat(content): <YYYY-MM-DD> — <title>`. The PR body is an activity log of every step this routine ran tonight (banner picked, voice gate result, locales translated, listings refreshed, build outcome, commit SHA). Sebastien reads this in the morning before merging from GitHub, so it has to be specific — not boilerplate. Fill in the placeholders below with the actual values you observed, don't leave them as `<…>`.

```bash
today=$(date -u +%F)
slug=$(basename _posts/${today}-*.md .md)
title=$(grep -oE '^title: *"[^"]+"' "_posts/${slug}.md" | head -1 | sed 's/title: *"//;s/"$//' | head -c 80)
banner_url=$(grep -oE '^banner: *"?[^" ]+' "_posts/${slug}.md" | head -1 | sed 's/banner: *"\?//;s/"\?$//')
commit_sha=  # set after `git commit` below

branch="feat/${slug}"

git checkout -b "$branch"
git add _posts/ _data/ scripts/generators/gen_articles.py scripts/generators/build_topics.py _layouts/ .claude/ 2>/dev/null || true
git commit -S -m "feat(content): ${today} — ${title} + 27 translations"
commit_sha=$(git rev-parse --short HEAD)
git push -u origin "$branch"

gh pr create --title "feat(content): ${today} — ${title}" --body "$(cat <<EOF
## Summary

**${title}** — published ${today}. EN source + 27 native-locale translations, listings + feeds refreshed.

## What ran tonight

### 1. Editorial gate
- \`check_voice.py --today\`: **passed**
- Frontmatter: title, subtitle, description, banner, banner_alt, tags, twitter_*, excerpt, date, keywords — all present
- Anti-filler scan: clean (no "delve into", "embark on", "in conclusion", "transformative journey", …)
- Structural shape: 1 H1, ≥3 H2s, lead aside present, Executive Summary blockquote present, FAQ + References present
- Date filename ↔ frontmatter \`date:\` match
<!-- If you had to fix anything before the gate passed, list it here. Delete this comment block if there was nothing. -->

### 2. Banner
- URL: \`${banner_url}\`
<!-- If you swapped the banner, add one sentence on why (e.g. "Original was \`corporate-finance.webp\` — generic stock that read as AI-written. Swapped for \`circuit_board_cityscape.webp\` which thematically matches the AI-payments-infrastructure framing."). Skip this if the draft's banner shipped as-is. -->

### 3. Translations (27 locales)
- Dispatched in parallel batches of 7 sub-agents
- Native SEO frontmatter (title / subtitle / description / keywords / twitter_* / excerpt) translated per locale
- Native register (executive / board-level tone) enforced — no hype filler in any locale
- Locales: \`fr\` \`es\` \`de\` \`it\` \`pt-br\` \`nl\` \`ja\` \`zh-hans\` \`zh-hant\` \`ko\` \`ar\` \`ru\` \`pl\` \`cs\` \`uk\` \`ro\` \`tr\` \`he\` \`hi\` \`bn\` \`id\` \`vi\` \`th\` \`fil\` \`ha\` \`yo\` \`sv\`
- \`translate_post.py --list-stubs\` confirms: **all 27 locales translated** (0 stubs remaining)

### 4. Homepage + listings
- \`_posts/index.md\` 6-card grid rotated (new card prepended, bottom card dropped)
- \`gen_articles.py\` auto-discovered the new post → \`/articles/\` featured story refreshed
- \`build_topics.py\` regenerated topic clusters (EN + 27 locale forks)
- \`build_lang_feeds.py\` regenerated 28 RSS / Atom / JSON feeds + news-sitemap
- \`build_agent_api.py\` refreshed \`/api/agents/posts.json\`
- \`postbuild.py\` refreshed \`/llms-full.txt\` + sitemap.xml + all 28 \`search-index.json\`
<!-- If a new topic cluster was added or an existing one extended, name it here. -->

### 5. Build + commit
- \`./build.sh\`: **exit 0** (i18n / hreflang / CSP / RTL / sitemap / JSON-LD all clean)
- Commit \`${commit_sha}\` signed (GPG) on branch \`${branch}\`
- Source-only commit — CI rebuilds public/ from source on merge and deploys it as the Pages artifact

## Reviewer notes
- Merge target: \`main\` — Sebastien merges from GitHub after morning review
- Required checks must all be green before merge (see Checks tab)
- If something looks off, this routine is in \`.claude/commands/publish-today.md\` — re-run after a fix lands on \`main\`

## Test plan
- [x] check_voice green
- [x] All 27 locales translated (no stubs remaining)
- [x] \`./build.sh\` exit 0
- [ ] CI: build + diff + accessibility + lighthouse all green
EOF
)"
```

**Cloud mode** (`git push` returns 403, no SSH key for signing): use the GitHub MCP server.

1. `mcp__github__create_branch` — base `main`, head `feat/<slug>`
2. For each changed file (collect via `git status --porcelain | grep -v '^?? public/'`), call `mcp__github__create_or_update_file` with the path + base64 content + branch. Source files only — CI rebuilds and deploys `public/` on merge.
3. `mcp__github__create_pull_request` — same title/body as above.

Do **not** attempt `git push` in cloud mode — it will 403.

### 11. Wait for CI to land green

The PR is not done until every required check on it is green. Poll with `gh` until all checks complete, then act on the outcome.

```bash
pr_number=$(gh pr view --json number -q .number)

# Note the field shape: `gh pr checks --json` uses `bucket` (pass/fail/pending/skipping)
# and `state` (SUCCESS/FAILURE/CANCELLED/IN_PROGRESS/QUEUED/…). There is no `status` field.
# Also: `gh pr checks` (without --json) exits non-zero if any check is failing OR pending,
# so wrap it in `|| true` if you want to log it during the poll.

# Default ceiling is 45 minutes — pa11y accessibility on a cold cache can run ~25.
deadline=$(( $(date +%s) + 2700 ))
while [[ $(date +%s) -lt $deadline ]]; do
  pending=$(gh pr checks "$pr_number" --json bucket -q '[.[] | select(.bucket == "pending")] | length')
  total=$(gh pr checks "$pr_number" --json bucket -q 'length')
  echo "[$(date -u +%H:%M:%S)] checks: $((total - pending))/$total complete"
  if [[ "$total" != "0" && "$pending" == "0" ]]; then break; fi
  sleep 30
done

# Final read: any fail / cancelled / timed-out bucket is a real problem.
failing=$(gh pr checks "$pr_number" --json bucket,name -q '[.[] | select(.bucket == "fail")] | length')
gh pr checks "$pr_number" || true   # print the human-readable table for the log
```

- If `failing == 0` **and** `pending == 0`: every check is green. Update the PR body's last test-plan checkbox (`gh pr edit "$pr_number" --body "$(...)"` re-running the same template with the checkbox flipped) and report SUCCESS to Sebastien.
- If `pending != 0` at deadline: the run took longer than 30 min. Don't fail silently — surface the still-running jobs by name and recommend Sebastien re-poll with `gh pr checks <N>` himself.
- If `failing != 0`: identify each failing job from the table, fetch its log with `gh run view --job=<job-id> --log-failed | tail -80`, and either (a) fix the root cause + push a follow-up commit to the same branch (re-triggers CI; loop back to the poll above), or (b) if the root cause needs Sebastien's judgement, leave the PR open and report the specific failure to him in the SUCCESS/FAILURE message.

The slash command does not exit cleanly until either the CI is fully green or you've reported a specific failure that needs human judgement.

### 12. Report back

Tell Sebastien:
- The PR URL
- Slug + title + commit SHA
- 28/28 locale count
- Any voice-gate defects you fixed before scaffolding
- The banner image used (URL or filename + one-line rationale if you swapped it)
- Final CI status: which checks are green, which (if any) you had to push fixes for, which (if any) still need his eyes
- Anything that needed a fix not in this checklist
- Reminder: merge from GitHub when ready — all required checks should be green

## Surfaces this routine automatically updates

After a clean run, every reference to today's article is in place across:

- `_posts/<slug>.md` (EN source)
- `_posts/<lang>/<slug>.md` × 27 (locale translations)
- `_data/i18n/<lang>/slugs.json` × 27 (slug map entries)
- `_posts/index.md` (homepage 6-card grid)
- `_posts/articles.md` (regenerated by `gen_articles.py` auto-discover)
- All 28 RSS/Atom/JSON Feed/news-sitemap files (regenerated by `build_lang_feeds.py`)
- `sitemap.xml` (ssg generates → postbuild augments with rendered topic pages)
- All 28 `search-index.json` files (regenerated by ssg + build_translations)
- `/api/agents/posts.json` (regenerated by `build_agent_api.py`)
- `/llms-full.txt` (regenerated by `postbuild.py`)
- `/topics/<cluster>/index.html` × 6 EN topic pages + 6 × 27 per-locale forks (if cluster updated)

In **both modes**, a typical daily-article commit diff is ~30 source files (EN + 27 locales + listings). If `public/` or `docs/` files appear in the diff, back them out — neither is committed (the `docs/` snapshot was retired 2026-06-10; CI deploys `public/` as a Pages artifact).
