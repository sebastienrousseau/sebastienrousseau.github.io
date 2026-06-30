"use strict";

/**
 * Service worker for sebastienrousseau.com
 *
 * Caching strategy:
 *   - HTML (navigation requests):  network-first, fall back to cache, then offline page.
 *   - Static assets (/_csp/*, /main.*.js, /sw.*.js, /highlight.*.css, /theme-init.*.js
 *     and same-origin SVG / WebP / WOFF2): stale-while-revalidate.
 *   - Third-party origins: pass-through (no caching) to honour CSP and analytics opt-outs.
 */

const CACHE = "ap-v8";
const OFFLINE_URL = "/offline/index.html";
const PRECACHE = [
  "/",
  "/index.html",
  "/main.js",
  "/theme-init.js",
  "/highlight.css",
  OFFLINE_URL,
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE).then((c) => c.addAll(PRECACHE).catch(() => null))
  );
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener("message", (event) => {
  // Only honour messages from same-origin clients (js/missing-origin-check).
  if (event.origin && event.origin !== self.location.origin) return;
  if (event.data && event.data.action === "skipWaiting") {
    self.skipWaiting();
  }
});

function isStaticAsset(url) {
  if (url.origin !== self.location.origin) return false;
  return (
    url.pathname.startsWith("/_csp/") ||
    /\/main\.[a-z0-9]+\.js$/.test(url.pathname) ||
    /\/sw\.[a-z0-9]+\.js$/.test(url.pathname) ||
    /\/highlight\.[a-z0-9]+\.css$/.test(url.pathname) ||
    /\/theme-init\.[a-z0-9]+\.js$/.test(url.pathname) ||
    /\.(svg|webp|png|jpg|jpeg|gif|woff2)$/.test(url.pathname)
  );
}

function staleWhileRevalidate(request) {
  return caches.open(CACHE).then((cache) =>
    cache.match(request).then((cached) => {
      const network = fetch(request)
        .then((response) => {
          if (response.ok || response.type === "opaque") {
            cache.put(request, response.clone()).catch(() => {});
          }
          return response;
        })
        .catch(() => cached);
      return cached || network;
    })
  );
}

function networkFirst(request) {
  return fetch(request)
    .then((response) => {
      if (response.ok) {
        const clone = response.clone();
        caches.open(CACHE).then((c) => c.put(request, clone)).catch(() => {});
      }
      return response;
    })
    .catch(() =>
      caches.match(request).then((cached) => cached || caches.match(OFFLINE_URL))
    );
}

self.addEventListener("fetch", (event) => {
  const { request } = event;
  if (request.method !== "GET") return;

  const url = new URL(request.url);

  // Cross-origin: don't intervene.
  if (url.origin !== self.location.origin) return;

  if (request.mode === "navigate" || request.headers.get("accept")?.includes("text/html")) {
    event.respondWith(networkFirst(request));
    return;
  }
  if (isStaticAsset(url)) {
    event.respondWith(staleWhileRevalidate(request));
  }
});
