<h1 align="center">Site build tools</h1>

<p align="center">
  Python tooling that compiles, validates, and stages sebastienrousseau.com.
</p>

---

## Layout

Tools are grouped by domain so each concern stays isolated:

| Folder | Responsibility |
| :--- | :--- |
| `cron/` | Local daily-publish scheduling + installers |
| `dev/` | Lint, naming, and complexity helpers |
| `editorial/` | Translation + frontmatter automation |
| `generators/` | Template, listing, feed, and topic builders |
| `lib/` | Shared helpers (frontmatter, slug, locale registry) |
| `postbuild/` | HTML rewrites, CSP/SRI, search index, sitemaps |
| `security/` | Sigstore signing + SBOM |
| `seo_and_audit/` | Link audit, JSON-LD validation, readability |

## License

Licensed under [Apache-2.0](../LICENSE).

<p align="right"><a href="#site-build-tools">Back to Top</a></p>
