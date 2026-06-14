# WeasyPrint PDF render service for sebastienrousseau.com.
#
# Lives at /api/pdf/<slug>.pdf behind the lang-router Worker; the
# Worker proxies through to this Fly.io machine and caches the
# response at the Cloudflare Edge (`Cache-Control: public,
# max-age=86400, immutable`). Repeated hits never re-render — they
# come from Edge cache. First-render cost: ~600-1200ms on a Fly
# shared-cpu-1x; subsequent reads are <30ms from the user's POP.
#
# WeasyPrint produces PDF/A-quality output from HTML + CSS using
# pango/cairo, respects the @media print stylesheet shipped with
# the site (transparent inline code, sources-as-footnotes, etc.),
# and lays out left-bound RTL for AR/HE locales correctly.
#
# Image: python:3.13-slim. ~110 MB. Free-tier-friendly.

FROM python:3.13-slim

# WeasyPrint needs pango / cairo / gdk-pixbuf at the system level.
# fonts-noto-color-emoji + fonts-noto-cjk cover every locale on
# sebastienrousseau.com without bloating the image past Fly's free
# tier 8 GB shared volume limit. fonts-liberation gives a Helvetica-
# alike for headlines on locales that don't ship a serif.
RUN apt-get update && apt-get install -y --no-install-recommends \
      libpango-1.0-0 \
      libpangoft2-1.0-0 \
      libcairo2 \
      libgdk-pixbuf-2.0-0 \
      shared-mime-info \
      fonts-noto-core \
      fonts-noto-cjk \
      fonts-noto-color-emoji \
      fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /srv

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 8080
ENV PORT=8080
ENV PYTHONUNBUFFERED=1

# gunicorn — 2 sync workers (fits within Fly free-tier 256 MB).
# Each WeasyPrint render is CPU-bound but short; sync workers keep
# memory predictable. Increase to 4 if traffic justifies a larger
# Machine size.
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", \
     "--timeout", "30", "--access-logfile", "-", "app:app"]
