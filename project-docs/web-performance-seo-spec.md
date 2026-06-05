# Web Design, Core Vitals, and SEO Guide

> Last Updated: June 4, 2026

This guide provides the code, settings, and setup details to achieve perfect web speed and search scores.
We build the Sebastien Rousseau web site using vanilla HTML, CSS, and JS, compiled with the Shokunin static site builder and delivered via Cloudflare Workers.

## Contents

This guide covers speed metrics, asset rules, edge cache headers, user click delay, access rules, sitemaps, and language routing.

## 1: Speed & Core Vitals (PSI & Lighthouse 100%)

We optimize speed metrics by removing render blocks, styling key CSS, and deferring script loads.

### Key Paint Path & Render-blocking Cures

To achieve fast page loads on mobile devices, all render-blocking scripts and styles must be removed.

We structure our head tags to render top page content at once.

#### A: Inlining Key CSS & Async CSS

We inline the minimal top styles in the page head to speed up initial painting.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">

  <!-- 1. Inline Critical CSS -->
  <style>
    body{margin:0;font-family:'Inter',system-ui,-apple-system,sans-serif;color:#111;background-color:#fff}
    .skip-link{position:absolute;top:-40px;left:0;background:#000;color:#fff;padding:8px;z-index:100}
    .skip-link:focus-visible{top:0}
    header{display:flex;justify-content:between;padding:1rem 2rem;border-bottom:1px solid #eee}
    main{max-width:80ch;margin:2rem auto;padding:0 1rem}
  </style>

  <!-- 2. Async Load Non-Critical CSS (Preload -> Stylesheet swap) -->
  <link rel="preload" href="/assets/css/main.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
  <noscript><link rel="stylesheet" href="/assets/css/main.css"></noscript>
</head>
```

Non-critical styles load in the background and apply later.

#### B: Code-Splitting & Deferral

We defer all key script loads to keep the browser main thread quick during load.

```html
  <!-- Modern JS deferred (non-blocking) -->
  <script type="module" src="/assets/js/main.js" defer></script>

  <!-- Dynamic Import inside main.js (Code-Splitting) -->
  <script type="module">
    // Load heavy interactive libraries only when needed
    document.querySelector('.interactive-btn')?.addEventListener('click', async () => {
      const { runInteractiveTask } = await import('/assets/js/modules/heavy-interactive.js');
      runInteractiveTask();
    });
  </script>
```

This ensures the page responds immediately to user clicks while heavy tools load.

### Asset Setup

Our asset setup strategy compresses images into modern formats and self-hosts key variable font subsets.

This reduces file sizes and prevents layout shifts during load.

#### A: Next-Gen Images & Layout Shift Prevention

We prevent layout shifts by declaring explicit sizes and aspect ratios on all responsive image elements.

```html
<!-- Responsive Picture Element with Next-Gen Formats and Layout-shift prevention -->
<picture class="article-hero-picture">
  <!-- AVIF for modern browsers (smallest bytes) -->
  <source srcset="/images/hero-400.avif 400w, /images/hero-800.avif 800w, /images/hero-1200.avif 1200w"
          sizes="(max-width: 600px) 400px, (max-width: 1200px) 800px, 1200px"
          type="image/avif">
  <!-- WebP Fallback -->
  <source srcset="/images/hero-400.webp 400w, /images/hero-800.webp 800w, /images/hero-1200.webp 1200w"
          sizes="(max-width: 600px) 400px, (max-width: 1200px) 800px, 1200px"
          type="image/webp">
  <!-- Standard Img Fallback with layout dimensions -->
  <img src="/images/hero-800.jpg"
       alt="Illustration representing post-quantum cryptographic key distributions"
       width="800"
       height="450"
       loading="eager"
       fetchpriority="high"
       decoding="async"
       class="img-responsive">
</picture>
```

We map these sizes in our CSS style rules to preserve the correct aspect ratio.

```css
.img-responsive {
  display: block;
  max-width: 100%;
  height: auto;
  aspect-ratio: 16 / 9;
}
```

The browser reserves layout space for the image to prevent content from jumping.

#### B: Web Fonts Setup (FOIT/FOUT Cure)

We avoid invisible text phases during font download by using variable fonts and font swap rules.

```css
@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 100 900;
  font-display: swap;
  src: url('/fonts/inter-variable-latin.woff2') format('woff2');
  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+2000-206F, U+2074, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
}
```

We preload key font files in the header to ensure they are available at once.

```html
<link rel="preload" href="/fonts/inter-variable-latin.woff2" as="font" type="font/woff2" crossorigin="anonymous">
```

This balances loading speeds with visual stability for our readers.

### Cache-Control & Edge Setup

The edge server uses a Cloudflare Worker to set cache rules and compress assets by default.

```javascript
export async function handleRequest(request) {
  const url = new URL(request.url);
  const response = await fetch(request);
  const headers = new Headers(response.headers);

  headers.set("X-Frame-Options", "DENY");
  headers.set("X-Content-Type-Options", "nosniff");
  headers.set("Referrer-Policy", "strict-origin-when-cross-origin");
  headers.set("Content-Security-Policy", "default-src 'self'; object-src 'none'; base-uri 'self';");

  if (url.pathname.startsWith("/assets/") || url.pathname.startsWith("/fonts/") || url.pathname.startsWith("/images/")) {
    headers.set("Cache-Control", "public, max-age=31536000, immutable");
  } else {
    headers.set("Cache-Control", "public, max-age=0, must-revalidate");
  }

  return new Response(response.body, {
    status: response.status,
    statusText: response.statusText,
    headers
  });
}
```

Static assets are saved for one year, while pages are checked on every request.

### Click to Paint Setup

We improve input delay by breaking up long script tasks and yielding running to the browser paint loop.

```javascript
export function yieldToMain() {
  if (globalThis.scheduler?.yield) {
    return scheduler.yield();
  }
  return new Promise(resolve => setTimeout(resolve, 0));
}

async function processHugeDataSet(items) {
  let count = 0;
  for (const item of items) {
    doHeavyMath(item);
    count++;

    if (count % 50 === 0) {
      await yieldToMain();
    }
  }
}
```

Yielding to the paint loop prevents long scripts from blocking user input.

## 2: WAVE & Access (100% WCAG 2.2 Rules)

Our access checklist guarantees full WCAG compliance across color levels, labels, and focus states.

We test these features quickly in the build pipeline.

### Structured DOM Layout

We build a clean DOM tree using standard elements to ensure screen readers can parse the page.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <title>Post-Quantum Payments Security — Sebastien Rousseau</title>
</head>
<body>
  <a href="#main-content" class="skip-link">Skip to main content</a>
  <header>
    <nav aria-label="Main Navigation">
      <ul>
        <li><a href="/" aria-current="page">Home</a></li>
        <li><a href="/articles/">Articles</a></li>
      </ul>
    </nav>
  </header>
  <main id="main-content">
    <article>
      <h1>Post-Quantum Payments Security</h1>
      <p>Content goes here.</p>
    </article>
  </main>
  <footer>
    <p>&copy; 2026 Sebastien Rousseau</p>
  </footer>
</body>
</html>
```

This outline provides a logical flow for keyboards and screen readers.

### Contrast & Visible Focus Lines

We guarantee clear viewing by meeting contrast levels and adding visible focus outlines to links.

```css
:focus-visible {
  outline: 3px solid #005a9c;
  outline-offset: 2px;
}

body {
  color: #1a1a1a;
  background-color: #ffffff;
}

a {
  color: #005a9c;
  text-decoration: underline;
}

a:hover {
  color: #003a6c;
}
```

This ensures that all page content is readable and links are easy to navigate.

### Aria Labels & Forms

All interactive forms and inputs use clear label elements to pass access checks.

```html
<form action="https://formspree.io/f/project" method="POST" aria-label="Contact Form">
  <div class="form-group">
    <label for="user-email">Email Address</label>
    <input type="email" id="user-email" name="email" required aria-describedby="email-helper">
    <span id="email-helper" class="helper-text">We will never share your email address.</span>
  </div>
  <button type="submit">Submit Form</button>
</form>
```

This prevents input confusion and assists helper tools.

## 3: Google News & Technical SEO

Our search optimization steps ensure fast indexing and complete news coverage across all locales.

We publish feeds and schemas that follow search engine standards.

### Google News XML Sitemap

We publish a news site map XML containing details for articles released in the last two days.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:news="http://www.google.com/schemas/sitemap-news/0.9">
  <url>
    <loc>https://sebastienrousseau.com/2026-05-20-quantum-payments-2026/</loc>
    <news:news>
      <news:publication>
        <news:name>Sebastien Rousseau Web Platform</news:name>
        <news:language>en</news:language>
      </news:publication>
      <news:publication_date>2026-05-20T06:30:00Z</news:publication_date>
      <news:title>Post-Quantum Payments Security and Financial Technology</news:title>
    </news:news>
  </url>
</urlset>
```

This file lists post names, dates, languages, and titles for search tools.

### Schema.org JSON-LD structured data

We embed structured data block elements to provide rich contextual metadata for search crawlers.

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "TechArticle",
  "@id": "https://sebastienrousseau.com/2026-05-20-quantum-payments-2026/#article",
  "headline": "Post-Quantum Payments Security",
  "datePublished": "2026-05-20T06:30:00Z",
  "dateModified": "2026-05-20T06:30:00Z",
  "author": {
    "@type": "Person",
    "name": "Sebastien Rousseau",
    "url": "https://sebastienrousseau.com"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Sebastien Rousseau Web Platform",
    "logo": {
      "@type": "ImageObject",
      "url": "https://sebastienrousseau.com/logo.png"
    }
  },
  "description": "An analysis of post-quantum cryptography in retail banking systems."
}
</script>
```

This allows tools to parse the content author and type details plainly.

### Multi-Language Router (Cloudflare Worker)

The edge router parses locale headers and routes users to their own language versions.

```javascript
// Edge Language Router redirect logic
export async function routeLanguage(request) {
  const url = new URL(request.url);

  // Skip route if cookie is set or path is asset
  if (url.pathname.includes(".") || request.headers.get("Cookie")?.includes("lang=")) {
    return fetch(request);
  }

  const acceptLang = request.headers.get("Accept-Language") || "";
  const preferredLang = parseAcceptLanguage(acceptLang); // Returns 'fr', 'es', etc.

  if (preferredLang && preferredLang !== 'en') {
    return Response.redirect(`https://sebastienrousseau.com/${preferredLang}${url.pathname}`, 302);
  }

  return fetch(request);
}
```

This ensures visitors land on the translated version of the page.
