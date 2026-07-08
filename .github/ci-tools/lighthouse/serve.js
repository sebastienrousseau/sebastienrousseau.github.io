// Zero-dependency static server for the Lighthouse CI fixture.
//
// The default lhci `staticDistDir` server (and a plain `http-server`) send
// assets uncompressed and un-cached, so CI scores understate production —
// Cloudflare serves this site gzipped with a long immutable cache. This server
// mirrors that: on-the-fly gzip for text assets + `Cache-Control: immutable`
// for fingerprinted static files, so the Lighthouse "text compression" and
// "efficient cache policy" audits reflect what a real visitor gets.
//
// Node built-ins only (http, fs, zlib, path) — no dependency to hash-pin.
// Usage: node serve.js [dir=public] [port=8000]
//   Prints "lighthouse-fixture listening on <port>" once ready (lhci waits on
//   this via startServerReadyPattern).

"use strict";

const http = require("http");
const fs = require("fs");
const path = require("path");
const zlib = require("zlib");

const ROOT = path.resolve(process.argv[2] || process.env.LH_SERVE_DIR || "public");
const PORT = Number(process.argv[3] || process.env.PORT || 8000);

const TYPES = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".mjs": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".webmanifest": "application/manifest+json; charset=utf-8",
  ".xml": "application/xml; charset=utf-8",
  ".txt": "text/plain; charset=utf-8",
  ".svg": "image/svg+xml",
  ".webp": "image/webp",
  ".avif": "image/avif",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".ico": "image/x-icon",
  ".woff2": "font/woff2",
  ".woff": "font/woff",
  ".map": "application/json; charset=utf-8",
};

// Text types worth gzipping; binary media (webp/png/woff2) is already compressed.
const COMPRESSIBLE = new Set([
  ".html", ".css", ".js", ".mjs", ".json", ".webmanifest", ".xml", ".txt", ".svg", ".map",
]);

function resolveFile(urlPath) {
  // Decode, strip query, prevent traversal, map dir → index.html.
  let p = decodeURIComponent(urlPath.split("?")[0].split("#")[0]);
  if (p.endsWith("/")) p += "index.html";
  const abs = path.normalize(path.join(ROOT, p));
  if (!abs.startsWith(ROOT)) return null; // traversal guard
  try {
    const st = fs.statSync(abs);
    if (st.isDirectory()) {
      const idx = path.join(abs, "index.html");
      return fs.existsSync(idx) ? idx : null;
    }
    return abs;
  } catch {
    // Extensionless path → try /index.html (clean-URL form).
    if (!path.extname(abs)) {
      const idx = abs + "/index.html";
      if (fs.existsSync(idx)) return idx;
    }
    return null;
  }
}

const server = http.createServer((req, res) => {
  const file = resolveFile(req.url || "/");
  if (!file) {
    res.writeHead(404, { "content-type": "text/plain" });
    res.end("404");
    return;
  }
  const ext = path.extname(file).toLowerCase();
  const type = TYPES[ext] || "application/octet-stream";
  // Fingerprinted assets get a long immutable cache; HTML must revalidate.
  const cache =
    ext === ".html"
      ? "public, max-age=0, must-revalidate"
      : "public, max-age=31536000, immutable";

  let body;
  try {
    body = fs.readFileSync(file);
  } catch {
    res.writeHead(500, { "content-type": "text/plain" });
    res.end("500");
    return;
  }

  const headers = { "content-type": type, "cache-control": cache, vary: "Accept-Encoding" };
  const accepts = (req.headers["accept-encoding"] || "").includes("gzip");
  if (accepts && COMPRESSIBLE.has(ext)) {
    const gz = zlib.gzipSync(body, { level: 9 });
    headers["content-encoding"] = "gzip";
    headers["content-length"] = gz.length;
    res.writeHead(200, headers);
    res.end(gz);
  } else {
    headers["content-length"] = body.length;
    res.writeHead(200, headers);
    res.end(body);
  }
});

server.listen(PORT, () => {
  // eslint-disable-next-line no-console
  console.log(`lighthouse-fixture listening on ${PORT} (root: ${ROOT})`);
});
