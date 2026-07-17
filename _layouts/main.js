"use strict";

/**
 * Class to handle registration of a service worker.
 */
class ServiceWorkerSetup {
    /**
     * Constructor for the ServiceWorkerSetup class.
     * Checks if service workers are supported and initiates registration if they are.
     * If not, logs a warning to the console.
     */
    constructor() {
        if ("serviceWorker" in navigator) {
            // Deferring service worker registration until after the page has loaded.
            window.addEventListener('load', () => {
                this.registerServiceWorker();
            });
        } else {
            console.warn("Service workers are not supported by this browser");
        }
    }

    /**
     * Method to register a service worker.
     * Logs a success message with the registration scope if registration succeeds,
     * or an error message if registration fails.
     * Also checks for a new service worker installation and triggers an update if found.
     */
    registerServiceWorker() {
        navigator.serviceWorker.register("/sw.js", {scope: './'})
            .then(registration => {
                console.log("ServiceWorker registration successful with scope: ", registration.scope);

                // If there's no controller, this page wasn't loaded via a service worker, so they're looking at the latest version.
                // Exit early
                if (!navigator.serviceWorker.controller) return;

                // If there's a worker waiting, that means a new version has been found and the waiting worker can be updated
                if (registration.waiting) {
                    this.updateServiceWorker(registration.waiting);
                    return;
                }

                // If there's a worker installing, track its progress. If it becomes "installed", we can update the service worker.
                if (registration.installing) {
                    this.trackInstallingWorker(registration.installing);
                    return;
                }

                // If none of the above, then listen for new installing workers arriving.
                // If one arrives, track its progress.
                // If it becomes "installed", our service worker code can be updated.
                registration.addEventListener('updatefound', () => {
                    this.trackInstallingWorker(registration.installing);
                });
            })
            .catch(error => {
                console.error("ServiceWorker registration failed: ", error);
            });

        // Ensure refresh is only called once.
        // This works around a bug in "force update on reload".
        let refreshing;
        navigator.serviceWorker.addEventListener('controllerchange', () => {
            if (refreshing) return;
            window.location.reload();
            refreshing = true;
        });
    }

    /**
     * Sends a 'skipWaiting' message to a service worker indicating that it should activate immediately.
     * @param {ServiceWorker} worker - The service worker that should be updated.
     */
    updateServiceWorker(worker) {
        worker.postMessage({action: 'skipWaiting'});
    }

    /**
     * Listens for a state change on a service worker. If the state becomes 'installed',
     * this means the service worker is ready to take over from the current one.
     * Call updateServiceWorker() to trigger the new service worker to become active immediately.
     * @param {ServiceWorker} worker - The service worker that is being installed.
     */
    trackInstallingWorker(worker) {
        worker.addEventListener('statechange', () => {
            if (worker.state === 'installed') {
                this.updateServiceWorker(worker);
            }
        });
    }
}

// Create an instance of the ServiceWorkerSetup class and attach it to the global window object.
// This makes the instance accessible from anywhere in your code that has access to the global scope.
window.serviceWorkerSetup = new ServiceWorkerSetup();

/**
 * On-site search bootstrap (DX plan Phase 2, ADR-0010).
 *
 * The search runtime (/search.js + /search.css) is LAZY-LOADED on first
 * invocation only — Cmd/Ctrl-K, a click on the in-nav .ap-search button, or
 * landing on the /search page — so it adds 0 to initial LCP everywhere else.
 * Both assets are same-origin (script-src/style-src 'self'); no inline handlers,
 * no CSP change. With JS off, the nav button is inert and /search shows its
 * static fallback — progressive enhancement preserved.
 */
(function () {
    var loading = null;

    function injectOnce(tag, attrs) {
        var el = document.createElement(tag);
        for (var k in attrs) if (attrs.hasOwnProperty(k)) el.setAttribute(k, attrs[k]);
        document.head.appendChild(el);
        return el;
    }

    // Returns a promise that resolves once /search.js has booted.
    function ensureSearch() {
        if (window.SiteSearch) return Promise.resolve();
        if (loading) return loading;
        loading = new Promise(function (resolve) {
            document.addEventListener("sitesearch:ready", function () { resolve(); }, { once: true });
            injectOnce("link", { rel: "stylesheet", href: "/search.css" });
            injectOnce("script", { src: "/search.js", defer: "" });
        });
        return loading;
    }

    function openSearch() {
        if (window.SiteSearch) {
            window.SiteSearch.open();
            return;
        }
        // Remember the intent so /search.js opens as soon as it boots.
        window.__ssPendingOpen = true;
        ensureSearch().then(function () {
            if (window.__ssPendingOpen && window.SiteSearch) {
                window.__ssPendingOpen = false;
                window.SiteSearch.open();
            }
        });
    }

    // Nav search button → open the command palette.
    document.addEventListener("click", function (event) {
        var trigger = event.target.closest && event.target.closest(".ap-search");
        if (!trigger) return;
        event.preventDefault();
        openSearch();
    });

    // Cmd/Ctrl-K anywhere (except while typing into another field, where the OS
    // shortcut shouldn't be hijacked mid-entry unless it's our own input).
    document.addEventListener("keydown", function (event) {
        var k = event.key;
        if ((event.metaKey || event.ctrlKey) && (k === "k" || k === "K")) {
            event.preventDefault();
            openSearch();
        }
    });

    // The /search page self-enhances: eagerly (but idle) load the runtime so the
    // page turns into a live search box without a click. Still off the LCP path.
    if (document.getElementById("search-page")) {
        var idle = window.requestIdleCallback || function (fn) { return setTimeout(fn, 200); };
        idle(function () { ensureSearch(); });
    }
})();

/**
 * Listing filter — `/articles/` page <select>s update data-filter-*
 * attributes on the .tag-landing-list container. CSS in the layout
 * uses attribute selectors to hide non-matching cards. Empty value
 * means "show all". Updates a counter + empty-state marker so screen
 * readers can announce the filtered count.
 */
document.addEventListener("change", function (event) {
    var target = event.target;
    if (!target || target.tagName !== "SELECT") return;
    var which = target.getAttribute("data-filter-target");
    if (!which) return;
    // Navigate-mode selects (e.g. Year on the paged listing) jump to a
    // dedicated archive URL instead of mutating filter attributes —
    // see _render_filter_form() for why.
    if (target.getAttribute("data-filter-mode") === "navigate") {
        // Both the base path and the option value are DOM-sourced, so both are
        // validated against strict allow-lists before they reach location.href
        // — a crafted attribute or option value can never inject a URL
        // (js/xss-through-dom). Either failing its check falls back to the
        // safe default listing.
        var base = target.getAttribute("data-navigate-base") || "/articles";
        // Must be a single-slash site-relative path whose first character is
        // alphanumeric: this rejects protocol-relative ("//host") and scheme
        // ("javascript:") URLs that the previous ^\/[a-z0-9/-]+$ allowed.
        if (!/^\/[a-z0-9][a-z0-9/-]*$/.test(base)) {
            base = "/articles";
        }
        var v = target.value;
        if (v && !/^[a-z0-9-]+$/.test(v)) {
            v = "";
        }
        // base and v are both validated against strict allow-lists above and
        // encodeURIComponent-clean by construction, so the assembled path is a
        // safe same-origin relative URL (js/xss-through-dom false positive).
        var dest = v ? base + "/" + encodeURIComponent(v) + "/" : base + "/";
        window.location.assign(dest);
        return;
    }
    var list = document.querySelector(".tag-landing-list");
    if (!list) return;
    if (target.value) {
        list.setAttribute("data-filter-" + which, target.value);
    } else {
        list.removeAttribute("data-filter-" + which);
    }
    // Empty-state: after each filter change, count VISIBLE cards via
    // getBoundingClientRect (cheaper than getComputedStyle); flip a
    // marker that the CSS shows in a sibling `.listing-empty` block.
    var visible = 0;
    Array.prototype.forEach.call(list.children, function (card) {
        if (card.offsetParent !== null) visible++;
    });
    if (visible === 0) {
        list.setAttribute("data-empty", "1");
    } else {
        list.removeAttribute("data-empty");
    }
    var counter = document.getElementById("listing-count");
    if (counter) {
        counter.textContent = visible;
    }
});

/**
 * Action-rail "Save PDF" — two handlers:
 *
 *   [data-print]            — button that opens the browser print
 *                              dialog directly (no server route).
 *   [data-print-fallback]   — anchor to /api/pdf/<slug>.pdf; we let the
 *                              browser navigate by default, but if the
 *                              Worker route returns a non-PDF (e.g. 503
 *                              when the Fly.io machine is down), fall
 *                              back to window.print() so the user still
 *                              gets a PDF via the @media print stylesheet.
 *
 * Either way the PDF that drops out respects our @media print stylesheet
 * (transparent inline code, sources-as-footnotes, links shown inline).
 */
document.addEventListener("click", function (event) {
    var trigger = event.target.closest("[data-print]");
    if (!trigger) return;
    event.preventDefault();
    window.print();
});

document.addEventListener("click", function (event) {
    var trigger = event.target.closest("[data-print-fallback]");
    if (!trigger) return;
    var href = trigger.getAttribute("href");
    if (!href) {
        event.preventDefault();
        window.print();
        return;
    }
    // Probe the PDF route with HEAD; if it's a real PDF, let the
    // browser navigate. Otherwise prevent navigation and fall back.
    event.preventDefault();
    fetch(href, { method: "HEAD" })
        .then(function (res) {
            var ct = (res.headers.get("Content-Type") || "").toLowerCase();
            if (res.ok && ct.indexOf("application/pdf") !== -1) {
                window.location.href = href;
            } else {
                window.print();
            }
        })
        .catch(function () {
            window.print();
        });
});

/**
 * Copy-to-clipboard handler — single delegate for every [data-copy]
 * button inside the cite popover (BibTeX / RIS / Vancouver / Chicago /
 * APA) and the reuse / republish panel. The target is the CSS selector
 * in data-copy, typically "#cite-bibtex" or "#reuse-attribution". On
 * success we flip data-copied="1" for 2s so the CSS can render a
 * "Copied ✓" affordance; on failure (Clipboard API unavailable,
 * insecure context) we fall back to a transient textarea + execCommand.
 */
document.addEventListener("click", function (event) {
    var btn = event.target.closest("[data-copy]");
    if (!btn) return;
    event.preventDefault();
    var target = document.querySelector(btn.getAttribute("data-copy"));
    if (!target) return;
    var text = target.innerText || target.textContent || "";
    var done = function () {
        btn.setAttribute("data-copied", "1");
        setTimeout(function () { btn.removeAttribute("data-copied"); }, 2000);
    };
    if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text).then(done).catch(function () {
            fallbackCopy(text, done);
        });
    } else {
        fallbackCopy(text, done);
    }
});

/**
 * Per-card "Copy link" — every .card-share-rail emits a
 * <button data-copy-link="https://…/<slug>/"> so readers can paste the
 * canonical URL anywhere. Same Clipboard API + textarea fallback as the
 * cite popover handler above. data-copied="1" flips for 2s so CSS can
 * render a "Copied ✓" affordance on top of the icon.
 */
document.addEventListener("click", function (event) {
    var btn = event.target.closest("[data-copy-link]");
    if (!btn) return;
    event.preventDefault();
    var text = btn.getAttribute("data-copy-link");
    if (!text) return;
    var done = function () {
        btn.setAttribute("data-copied", "1");
        setTimeout(function () { btn.removeAttribute("data-copied"); }, 2000);
    };
    if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text).then(done).catch(function () {
            fallbackCopy(text, done);
        });
    } else {
        fallbackCopy(text, done);
    }
});

function fallbackCopy(text, done) {
    var ta = document.createElement("textarea");
    ta.value = text;
    ta.setAttribute("readonly", "");
    ta.style.cssText = "position:fixed;top:-9999px;left:-9999px";
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand("copy"); done(); }
    catch (err) { console.warn("copy fallback failed", err); }
    document.body.removeChild(ta);
}

/**
 * Back-to-top floating button. Reveals after the user scrolls past one viewport
 * height and scrolls smoothly to the top on click.
 */
(function () {
    "use strict";
    var btn = document.querySelector(".ap-totop");
    if (!btn) return;
    btn.removeAttribute("hidden");
    var threshold = function () { return window.innerHeight; };
    var onScroll = function () {
        btn.classList.toggle("is-visible", window.scrollY > threshold());
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    btn.addEventListener("click", function () {
        var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
        window.scrollTo({ top: 0, behavior: reduced ? "auto" : "smooth" });
    });
})();

/**
 * IntersectionObserver-driven fade-up on first scroll-in for any element with
 * the .reveal class. Respects prefers-reduced-motion (the CSS handles that;
 * we still set is-in so the element is visible).
 */
(function () {
    "use strict";
    var targets = document.querySelectorAll(".reveal");
    if (!targets.length) return;
    if (typeof IntersectionObserver !== "function") {
        targets.forEach(function (el) { el.classList.add("is-in"); });
        return;
    }
    var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add("is-in");
                io.unobserve(entry.target);
            }
        });
    }, { rootMargin: ["0px", "0px", "-10%", "0px"].join(String.fromCharCode(32)), threshold: 0.05 });
    targets.forEach(function (el) { io.observe(el); });
})();

/**
 * Scroll-reveal for [data-reveal] elements (Apple-HIG primitive).
 * Fades + slides up on first intersection. Separate from .reveal so the
 * existing landing-page reveal-on-scroll behaviour stays untouched.
 */
(function () {
    "use strict";
    var targets = document.querySelectorAll("[data-reveal]");
    if (!targets.length) return;
    if (typeof IntersectionObserver !== "function") {
        targets.forEach(function (el) { el.classList.add("is-revealed"); });
        return;
    }
    var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add("is-revealed");
                io.unobserve(entry.target);
            }
        });
    }, { rootMargin: ["0px", "0px", "-8%", "0px"].join(String.fromCharCode(32)), threshold: 0.08 });
    targets.forEach(function (el) { io.observe(el); });
})();

/**
 * Light / dark theme toggle.
 * The initial theme is set in <head> by theme-init.js before paint. This handler
 * flips the data-theme attribute and persists the choice in localStorage. We
 * also sync the meta[name="theme-color"] tag so iOS/macOS Safari recolours the
 * status bar.
 */
(function () {
    "use strict";

    function announce(message) {
        var live = document.getElementById("ap-live");
        if (!live) {
            live = document.createElement("div");
            live.id = "ap-live";
            live.setAttribute("role", "status");
            live.setAttribute("aria-live", "polite");
            live.setAttribute("aria-atomic", "true");
            live.style.cssText =
                "position:absolute;left:-9999px;top:-9999px;width:1px;height:1px;" +
                "overflow:hidden;clip:rect(0 0 0 0);clip-path:inset(50%);white-space:nowrap";
            document.body.appendChild(live);
        }
        // Clear then set, so the same message is re-announced on repeat toggles.
        live.textContent = "";
        setTimeout(function () {
            live.textContent = message;
        }, 16);
    }

    function applyTheme(theme) {
        var previous = document.documentElement.getAttribute("data-theme");
        document.documentElement.setAttribute("data-theme", theme);
        var meta = document.querySelector('meta[name="theme-color"]');
        if (meta) {
            meta.setAttribute("content", theme === "dark" ? "#000000" : "#fbfbfd");
        }
        document.querySelectorAll(".theme-toggle").forEach(function (btn) {
            btn.setAttribute("aria-pressed", theme === "dark" ? "true" : "false");
            btn.setAttribute(
                "aria-label",
                theme === "dark" ? "Switch to light theme" : "Switch to dark theme"
            );
        });
        if (previous && previous !== theme) {
            announce(theme === "dark" ? "Dark theme on." : "Light theme on.");
        }
    }

    function currentTheme() {
        return document.documentElement.getAttribute("data-theme") || "light";
    }

    document.addEventListener("click", function (event) {
        var btn = event.target.closest(".theme-toggle");
        if (!btn) return;
        event.preventDefault();
        var next = currentTheme() === "dark" ? "light" : "dark";
        try {
            localStorage.setItem("theme", next);
        } catch (e) {
            /* ignore quota / disabled */
        }
        applyTheme(next);
    });

    // Sync once at boot so the toggle reflects whatever theme-init.js set.
    applyTheme(currentTheme());

    // Track OS-level changes when the user hasn't expressed a preference.
    if (window.matchMedia) {
        var media = window.matchMedia("(prefers-color-scheme: dark)");
        var handler = function (e) {
            try {
                if (localStorage.getItem("theme")) return;
            } catch (err) {
                /* ignore */
            }
            applyTheme(e.matches ? "dark" : "light");
        };
        if (media.addEventListener) {
            media.addEventListener("change", handler);
        } else if (media.addListener) {
            media.addListener(handler);
        }
    }
})();

/**
 * Reading progress bar — sticky 2px line at the top of the viewport that
 * fills as the user scrolls through the article body. Renders only on
 * pages with substantive <main.content>; nav/listing pages opt out.
 */
(function readingProgress() {
    "use strict";
    var main = document.querySelector("main.content");
    if (!main) return;
    var minHeight = window.innerHeight * 1.5;
    if (main.offsetHeight < minHeight) return;

    var bar = document.createElement("div");
    bar.className = "reading-progress";
    bar.setAttribute("role", "progressbar");
    bar.setAttribute("aria-label", "Reading progress");
    bar.setAttribute("aria-valuemin", "0");
    bar.setAttribute("aria-valuemax", "100");
    bar.setAttribute("aria-valuenow", "0");
    document.body.appendChild(bar);

    var ticking = false;
    function update() {
        var rect = main.getBoundingClientRect();
        var totalScroll = rect.height - window.innerHeight;
        var current = Math.min(Math.max(-rect.top, 0), totalScroll);
        var pct = totalScroll > 0 ? (current / totalScroll) * 100 : 0;
        bar.style.transform = "scaleX(" + (pct / 100) + ")";
        bar.setAttribute("aria-valuenow", Math.round(pct));
        ticking = false;
    }
    function schedule() {
        if (!ticking) {
            window.requestAnimationFrame(update);
            ticking = true;
        }
    }
    window.addEventListener("scroll", schedule, { passive: true });
    window.addEventListener("resize", schedule, { passive: true });
    update();
})();

/**
 * Language selector — wires up the .ap-lang button + flag-grid menu in
 * the nav.
 *   - Reflects the current language on the toggle (globe + code).
 *   - Marks the current language item with aria-current="true".
 *   - Active live languages (those with real /{lang}/ routes) get their
 *     hrefs rewired to the per-page hreflang alternate when one exists.
 *   - Disabled placeholder languages stay non-clickable.
 *   - Toggle: button click + outside-click close + Escape close.
 */
(function langSelector() {
    "use strict";
    var box = document.querySelector(".ap-lang");
    if (!box) return;
    var toggle = box.querySelector(".ap-lang-toggle");
    var menu = box.querySelector(".ap-lang-menu");
    if (!toggle || !menu) return;

    var current = (document.documentElement.getAttribute("lang") || "en").slice(0, 2).toLowerCase();
    var items = box.querySelectorAll(".ap-lang-item");
    items.forEach(function (a) {
        var lang = a.getAttribute("data-lang");
        if (lang === current || lang.indexOf(current + "-") === 0) {
            a.setAttribute("aria-current", "true");
            a.classList.add("active");
        }
        // Per-page hreflang override (live links only — placeholders
        // are <span> with no href and aria-disabled, skipped here).
        // Extract just the pathname so the link is origin-relative —
        // a localhost click shouldn't navigate to prod.
        if (a.tagName !== "A") return;
        var alt = document.querySelector(
            'link[rel="alternate"][hreflang="' + lang + '"]'
        );
        if (!alt) return;
        try {
            var url = new URL(alt.getAttribute("href"), window.location.href);
            a.setAttribute("href", url.pathname + url.search + url.hash);
        } catch (err) {
            a.setAttribute("href", alt.getAttribute("href"));
        }
    });
    // Visible label + aria-label come from the SSR + chrome patches —
    // JS leaves them alone.

    function setOpen(open) {
        if (open) {
            menu.removeAttribute("hidden");
            toggle.setAttribute("aria-expanded", "true");
        } else {
            menu.setAttribute("hidden", "");
            toggle.setAttribute("aria-expanded", "false");
        }
    }

    toggle.addEventListener("click", function (e) {
        e.stopPropagation();
        setOpen(toggle.getAttribute("aria-expanded") !== "true");
    });
    document.addEventListener("click", function (e) {
        if (toggle.getAttribute("aria-expanded") !== "true") return;
        if (!box.contains(e.target)) setOpen(false);
    });
    document.addEventListener("keydown", function (e) {
        if (e.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") {
            setOpen(false);
            toggle.focus();
        }
    });
})();

/**
 * Pre-fill the contact form from URL query parameters. The footer
 * newsletter widget submits as GET to /contact/?email=…&subject=newsletter
 * &message=…, so on arrival we pull those values into the matching
 * form fields and focus the Name field (the only one not pre-filled).
 * The contact form's own reCAPTCHA flow then takes over from there —
 * no AJAX shenanigans, no formspree interstitial, no tracker-blocker
 * conflicts. Acts only on the contact page (or any page hosting the
 * full ap-form contact form); silently no-ops elsewhere.
 */
(function contactPrefill() {
    "use strict";
    var form = document.querySelector("form.ap-form");
    if (!form) return;
    var params = new URLSearchParams(window.location.search);
    var email = params.get("email");
    var subject = params.get("subject");
    var message = params.get("message");
    if (!email && !subject && !message) return;
    if (email) {
        var emailEl = form.querySelector('input[name="email"]');
        if (emailEl) emailEl.value = email;
    }
    if (subject) {
        var subjectEl = form.querySelector('select[name="subject"]');
        if (subjectEl) {
            var match = Array.prototype.find.call(
                subjectEl.options,
                function (opt) { return opt.value === subject; }
            );
            if (match) subjectEl.value = subject;
        }
    }
    if (message) {
        var messageEl = form.querySelector('textarea[name="message"]');
        if (messageEl && !messageEl.value) messageEl.value = message;
    }
    var nameEl = form.querySelector('input[name="name"]');
    if (nameEl) nameEl.focus();
    // Strip the query string from the address bar so a refresh doesn't
    // re-prefill and the URL stays canonical.
    if (history && typeof history.replaceState === "function") {
        history.replaceState({}, "", window.location.pathname + window.location.hash);
    }
})();

/**
 * Lazy-load Google reCAPTCHA only when the visitor engages the contact
 * form. api.js is ~800 KB of third-party JS that otherwise loads on every
 * /contact/ view, pushing LCP to ~2.7 s (Lighthouse 0.75). Injecting it on
 * first focus/pointer keeps the widget ready before submit while removing it
 * from the initial load. api.js auto-renders any .g-recaptcha element once it
 * boots; same www.google.com script-src the eager tag used, so no CSP change.
 */
(function recaptchaLazy() {
    "use strict";
    var box = document.querySelector(".g-recaptcha");
    if (!box) return;
    var form = box.closest("form") || document;
    var loaded = false;
    var load = function () {
        if (loaded) return;
        loaded = true;
        var s = document.createElement("script");
        s.src = "https://www.google.com/recaptcha/api.js";
        s.async = true;
        s.defer = true;
        document.head.appendChild(s);
    };
    form.addEventListener("focusin", load, { once: true });
    form.addEventListener("pointerdown", load, { once: true });
})();

/**
 * Mermaid renderer — lazy-loads the Mermaid library from jsdelivr only
 * when the page actually contains <pre class="mermaid"> blocks. Pages
 * without Mermaid pay no JS / no network cost; pages with Mermaid widen
 * their meta-CSP to allow the import via the postbuild patch.
 */
(async function mermaidInit() {
    "use strict";
    if (!document.querySelector("pre.mermaid")) return;
    try {
        var mod = await import(
            "https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs"
        );
        var isDark = document.documentElement.getAttribute("data-theme") === "dark";
        if (!document.documentElement.getAttribute("data-theme")) {
            isDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
        }
        mod.default.initialize({
            startOnLoad: false,
            securityLevel: "antiscript",
            theme: isDark ? "dark" : "base",
            themeVariables: isDark ? {
                fontFamily: "var(--type-mono), ui-monospace, monospace",
                fontSize: "14px",
                primaryColor: "#161617",
                primaryTextColor: "#f5f5f7",
                primaryBorderColor: "#3a3a3c",
                lineColor: "#b0b0b8",
                textColor: "#f5f5f7",
                actorBorder: "#3a3a3c",
                actorBkg: "#161617",
                actorTextColor: "#f5f5f7",
                actorLineColor: "#3a3a3c",
                labelBoxBkgColor: "#161617",
                labelBoxBorderColor: "#3a3a3c",
                labelTextBkgColor: "#161617",
                labelTextColor: "#f5f5f7",
                loopTextColor: "#f5f5f7",
                noteBorderColor: "#3a3a3c",
                noteBkgColor: "#1d1d1f",
                noteTextColor: "#f5f5f7",
                activationBorderColor: "#3a3a3c",
                activationBkgColor: "#1d1d1f",
                sequenceNumberColor: "#f5f5f7",
            } : {
                fontFamily: "var(--type-mono), ui-monospace, monospace",
                fontSize: "14px",
                primaryColor: "#ffffff",
                primaryTextColor: "#111111",
                primaryBorderColor: "#d2d2d7",
                lineColor: "#505058",
                textColor: "#1d1d1f",
                actorBorder: "#d2d2d7",
                actorBkg: "#fafafc",
                actorTextColor: "#1d1d1f",
                actorLineColor: "#d2d2d7",
                labelBoxBkgColor: "#ffffff",
                labelBoxBorderColor: "#d2d2d7",
                labelTextBkgColor: "#ffffff",
                labelTextColor: "#1d1d1f",
                loopTextColor: "#1d1d1f",
                noteBorderColor: "#d2d2d7",
                noteBkgColor: "#f1f1f3",
                noteTextColor: "#1d1d1f",
                activationBorderColor: "#d2d2d7",
                activationBkgColor: "#f1f1f3",
                sequenceNumberColor: "#1d1d1f",
            },
            flowchart: { htmlLabels: true, useMaxWidth: true, curve: "basis" },
        });

        // Inject dynamic CSS overrides using variables so SVGs update cleanly on theme toggles
        var style = document.createElement("style");
        style.textContent = [
            // Container — the layout's generic `main.content pre` rule paints
            // a grey card background + padding meant for code blocks. Override
            // for Mermaid so the SVG sits flush on the page background, and
            // widen to the banner / page max width so the diagram is legible.
            // Match the site's existing wide-content pattern (used by tables
            // and .article-banner) — max-width: var(--max-wide) with auto
            // margins. The site's <main> doesn't actually constrain to a
            // narrow column for everything; only paragraphs have max-width:65ch.
            // pre.mermaid as block-level can therefore go to the full
            // --max-wide alongside tables and banner figures.
            "pre.mermaid { background: transparent !important; border: 0 !important; padding: 0 !important; margin: 24px auto !important; width: 100% !important; max-width: var(--max-wide, 1440px) !important; overflow-x: auto; text-align: center; }",
            "pre.mermaid svg { max-width: 100%; height: auto; }",
            // Dark mode: Mermaid's themeVariables are baked into the SVG at
            // render time, so toggling the site theme post-render leaves the
            // SVG with stale colors. CSS overrides using --ink / --bg-alt /
            // --border / --card / --accent follow the theme variable
            // switching at paint time and stay readable in either mode.
            "[data-theme='dark'] pre.mermaid svg .actor rect, html:not([data-theme='light']) pre.mermaid svg .actor rect { fill: #161617 !important; stroke: #3a3a3c !important; }",
            "[data-theme='dark'] pre.mermaid svg .actor text, [data-theme='dark'] pre.mermaid svg .actor tspan, html:not([data-theme='light']) pre.mermaid svg .actor text, html:not([data-theme='light']) pre.mermaid svg .actor tspan { fill: #f5f5f7 !important; }",
            "[data-theme='dark'] pre.mermaid svg .actor-line, html:not([data-theme='light']) pre.mermaid svg .actor-line { stroke: #3a3a3c !important; }",
            "[data-theme='dark'] pre.mermaid svg .messageLine0, [data-theme='dark'] pre.mermaid svg .messageLine1, html:not([data-theme='light']) pre.mermaid svg .messageLine0, html:not([data-theme='light']) pre.mermaid svg .messageLine1 { stroke: #b0b0b8 !important; fill: none !important; }",
            "[data-theme='dark'] pre.mermaid svg .messageText, html:not([data-theme='light']) pre.mermaid svg .messageText { fill: #f5f5f7 !important; }",
            "[data-theme='dark'] pre.mermaid svg .labelBox, html:not([data-theme='light']) pre.mermaid svg .labelBox { fill: #161617 !important; stroke: #3a3a3c !important; }",
            "[data-theme='dark'] pre.mermaid svg .labelText, [data-theme='dark'] pre.mermaid svg .labelText tspan, html:not([data-theme='light']) pre.mermaid svg .labelText, html:not([data-theme='light']) pre.mermaid svg .labelText tspan { fill: #f5f5f7 !important; }",
            "[data-theme='dark'] pre.mermaid svg .note rect, html:not([data-theme='light']) pre.mermaid svg .note rect { fill: #1d1d1f !important; stroke: #3a3a3c !important; }",
            "[data-theme='dark'] pre.mermaid svg .note text, [data-theme='dark'] pre.mermaid svg .note tspan, html:not([data-theme='light']) pre.mermaid svg .note text, html:not([data-theme='light']) pre.mermaid svg .note tspan { fill: #f5f5f7 !important; }",
            "[data-theme='dark'] pre.mermaid svg marker path, [data-theme='dark'] pre.mermaid svg marker polygon, html:not([data-theme='light']) pre.mermaid svg marker path, html:not([data-theme='light']) pre.mermaid svg marker polygon { fill: #b0b0b8 !important; stroke: #b0b0b8 !important; }",
            "@media (prefers-color-scheme: dark) { html:not([data-theme='light']) pre.mermaid svg .actor rect { fill: #161617 !important; stroke: #3a3a3c !important; } html:not([data-theme='light']) pre.mermaid svg .actor text, html:not([data-theme='light']) pre.mermaid svg .actor tspan { fill: #f5f5f7 !important; } html:not([data-theme='light']) pre.mermaid svg .messageText { fill: #f5f5f7 !important; } html:not([data-theme='light']) pre.mermaid svg .note rect { fill: #1d1d1f !important; stroke: #3a3a3c !important; } html:not([data-theme='light']) pre.mermaid svg .note text, html:not([data-theme='light']) pre.mermaid svg .note tspan { fill: #f5f5f7 !important; } html:not([data-theme='light']) pre.mermaid svg marker path { fill: #b0b0b8 !important; stroke: #b0b0b8 !important; } html:not([data-theme='light']) pre.mermaid svg .messageLine0, html:not([data-theme='light']) pre.mermaid svg .messageLine1 { stroke: #b0b0b8 !important; fill: none !important; } }",
            "pre.mermaid svg .actor rect { fill: var(--bg-alt, #fafafc) !important; stroke: var(--border, #3a3a3e) !important; }",
            "pre.mermaid svg .actor text, pre.mermaid svg .actor tspan { fill: var(--ink, #111111) !important; }",
            "pre.mermaid svg .actor-line { stroke: var(--border, #3a3a3e) !important; }",
            "pre.mermaid svg .messageLine0, pre.mermaid svg .messageLine1 { stroke: var(--ink-mute, #3a3a3e) !important; }",
            "pre.mermaid svg .messageText { fill: var(--ink, #111111) !important; stroke: none !important; }",
            "pre.mermaid svg .labelBox { fill: var(--card, #ffffff) !important; stroke: var(--border, #3a3a3e) !important; }",
            "pre.mermaid svg .labelText, pre.mermaid svg .labelText tspan { fill: var(--ink, #111111) !important; }",
            "pre.mermaid svg .note rect { fill: var(--bg-alt, #fafafc) !important; stroke: var(--border, #3a3a3e) !important; }",
            "pre.mermaid svg .note text, pre.mermaid svg .note tspan { fill: var(--ink, #111111) !important; }",
            "pre.mermaid svg .loopText, pre.mermaid svg .loopText tspan { fill: var(--ink, #111111) !important; }",
            "pre.mermaid svg .loopLine { stroke: var(--border, #3a3a3e) !important; fill: none !important; }",
            "pre.mermaid svg .active { fill: var(--bg-alt, #fafafc) !important; stroke: var(--border, #3a3a3e) !important; }",
            "pre.mermaid svg circle.sequenceNumber { fill: var(--accent, #0043a5) !important; stroke: var(--accent, #0043a5) !important; }",
            "pre.mermaid svg text.sequenceNumber { fill: #ffffff !important; stroke: none !important; font-weight: bold !important; }",
            "pre.mermaid svg .edgePath .path { stroke: var(--ink-mute, #3a3a3e) !important; }",
            "pre.mermaid svg .edgeLabel rect { fill: var(--card, #ffffff) !important; }",
            "pre.mermaid svg .edgeLabel text, pre.mermaid svg .edgeLabel tspan { fill: var(--ink, #111111) !important; }",
            // Mermaid v10 renders edge labels through <foreignObject> with
            // HTML <span>s that inherit a default mid-gray colour (≈ 6.5:1
            // contrast vs the white edge-label rect). Force the same dark
            // ink as the SVG-targeted rule so the labels clear WCAG 2.2
            // AAA on every Mermaid diagram on the site. The ``\x20`` escape
            // preserves the descendant-combinator space through the SSG's
            // CSS-aware string minifier, which otherwise collapses spaces
            // between selectors and class tokens.
            ".edgeLabel\x20span,.edgeLabel\x20div,.edgeLabel\x20p,.edgeLabel{color:var(--ink,#111111)!important;background-color:var(--card,#ffffff)!important;}",
            "pre.mermaid svg marker { fill: var(--ink-mute, #3a3a3e) !important; stroke: none !important; }"
        ].join("\n");
        document.head.appendChild(style);

        await mod.default.run({ querySelector: "pre.mermaid" });

        // Dedupe duplicate id attributes across multiple Mermaid SVGs on
        // the same page. Mermaid 10 emits stable IDs (`arrowhead`,
        // `crosshead`, `filled-head`, `sequencenumber`, `computer`,
        // `database`, `clock`, …) in each diagram's <defs>, which
        // collide when more than one diagram lives on the page and
        // produce a WCAG 2.2 AAA Principle 4.1.1 F77 duplicate-id
        // failure under pa11y. Walk every rendered SVG, prefix any
        // duplicate ID with the diagram index, and rewrite same-SVG
        // url(#…) and href="#…" references so the renamed markers
        // still resolve.
        try {
            var seen = Object.create(null);
            var svgs = document.querySelectorAll("pre.mermaid svg");
            svgs.forEach(function (svg, idx) {
                var rename = Object.create(null);
                var nodes = svg.querySelectorAll("[id]");
                nodes.forEach(function (n) {
                    var orig = n.getAttribute("id");
                    if (!orig) return;
                    if (!seen[orig]) { seen[orig] = true; return; }
                    var fresh = "m" + idx + "-" + orig;
                    n.setAttribute("id", fresh);
                    rename[orig] = fresh;
                });
                if (Object.keys(rename).length === 0) return;
                // Fix up url(#orig) / #orig / xlink:href="#orig" inside
                // this SVG so renamed markers keep resolving.
                svg.querySelectorAll("*").forEach(function (el) {
                    for (var i = 0; i < el.attributes.length; i++) {
                        var attr = el.attributes[i];
                        var v = attr.value;
                        if (!v) continue;
                        Object.keys(rename).forEach(function (orig) {
                            var fresh = rename[orig];
                            if (v.indexOf("url(#" + orig + ")") !== -1) {
                                v = v.split("url(#" + orig + ")").join("url(#" + fresh + ")");
                            }
                            if (v === "#" + orig) {
                                v = "#" + fresh;
                            }
                        });
                        if (v !== attr.value) attr.value = v;
                    }
                });
            });
        } catch (dedupErr) {
            console.warn("mermaid id dedup failed", dedupErr);
        }
    } catch (err) {
        console.warn("mermaid load failed", err);
    }
})();

/**
 * "Read as…" audience path selector (homepage, Phase 8; extended to the
 * /iso20022-mcp/ hub, whose generator tags every section the same way).
 *
 * Progressive enhancement: the control ships [hidden] in static HTML,
 * so a JS-off reader gets the full page in document order and no
 * inert widget. On load we reveal it, then re-order the tagged sections
 * so the ones tagged for the chosen audience (boards / engineers /
 * regulators) lead — nothing is ever removed, so it's a lens, not a
 * destructive filter.
 *
 * The preference is cookie-free: `?read=<audience>` in the URL (a
 * shareable, bookmarkable permalink) plus `localStorage`. URL wins on
 * load so a shared link always reflects its author's lens. Reorders
 * announce via a polite `role="status"` live region. No inline handlers
 * or styles — CSP-hash-clean, same-origin script only.
 */
(function () {
    var root = document.querySelector(".read-as");
    if (!root) return;
    // The sections container: the homepage content wrap, or the ISO 20022
    // MCP hub wrapper (the only other page whose sections carry
    // [data-audience] tags). Any other page has neither, and bails.
    var home =
        document.querySelector(".home-content") ||
        document.querySelector(".iso20022-mcp-page");
    if (!home) return;

    // Only these three lenses are honoured — everything else (including a
    // crafted ?read= value) falls back to the authored "Everyone" order,
    // so a hostile query string can never drive the DOM.
    var ALLOWED = ["boards", "engineers", "regulators"];
    var STORE_KEY = "read-as";
    var buttons = Array.prototype.slice.call(root.querySelectorAll(".read-as-btn"));
    var status = root.querySelector("[data-read-status]");
    var announce = root.getAttribute("data-announce") || "";

    // Snapshot the authored section order once so "Everyone" restores it.
    // Not `:scope >`: the build can wrap the authored sections in an extra
    // container (e.g. a lang="en" div injected on the homepage), so find
    // them anywhere under the wrap and reorder within their real parent.
    var sections = Array.prototype.slice.call(
        home.querySelectorAll("section[data-audience]")
    );
    if (!sections.length) return;
    var container = sections[0].parentNode;
    // One shared parent only: a split container would make appendChild
    // teleport sections between wrappers, so bail to the authored order.
    for (var si = 1; si < sections.length; si++) {
        if (sections[si].parentNode !== container) return;
    }

    function sanitize(v) {
        return ALLOWED.indexOf(v) !== -1 ? v : "";
    }

    // Stable partition: sections tagged for `aud` keep their relative
    // order and move to the front; the rest follow in their original
    // order. `aud === ""` leaves the authored order untouched.
    function reorder(aud) {
        var lead = [];
        var rest = [];
        sections.forEach(function (sec) {
            var tags = (sec.getAttribute("data-audience") || "").split(/\s+/);
            if (aud && tags.indexOf(aud) !== -1) {
                lead.push(sec);
            } else {
                rest.push(sec);
            }
        });
        lead.concat(rest).forEach(function (sec) {
            container.appendChild(sec);
        });
    }

    function labelFor(aud) {
        for (var i = 0; i < buttons.length; i++) {
            if ((buttons[i].getAttribute("data-read") || "") === aud) {
                return buttons[i].textContent.trim();
            }
        }
        return "";
    }

    function apply(aud, opts) {
        aud = sanitize(aud);
        opts = opts || {};
        reorder(aud);
        buttons.forEach(function (b) {
            var on = (b.getAttribute("data-read") || "") === aud;
            b.setAttribute("aria-pressed", on ? "true" : "false");
        });
        if (status && opts.speak) {
            status.textContent = (announce ? announce + ": " : "") + labelFor(aud);
        }
        if (opts.persist) {
            try {
                if (aud) localStorage.setItem(STORE_KEY, aud);
                else localStorage.removeItem(STORE_KEY);
            } catch (e) { /* private mode — non-fatal */ }
            try {
                var url = new URL(window.location.href);
                if (aud) url.searchParams.set("read", aud);
                else url.searchParams.delete("read");
                window.history.replaceState(null, "", url.toString());
            } catch (e2) { /* older engine — non-fatal */ }
        }
    }

    // Reveal the control now that it's wired (was [hidden] for JS-off).
    root.removeAttribute("hidden");

    buttons.forEach(function (b) {
        b.addEventListener("click", function () {
            apply(b.getAttribute("data-read") || "", { persist: true, speak: true });
        });
    });

    // Initial lens: URL param wins (shared link), else stored preference.
    var initial = "";
    try {
        initial = new URL(window.location.href).searchParams.get("read") || "";
    } catch (e) { /* no URL support — stays "" */ }
    if (!initial) {
        try { initial = localStorage.getItem(STORE_KEY) || ""; } catch (e3) {}
    }
    // Only announce on load when a non-default lens is actually applied,
    // so the default homepage doesn't fire a spurious live-region update.
    apply(initial, { persist: false, speak: sanitize(initial) !== "" });
})();

// ---------------------------------------------------------------------------
// Primary-nav submenu disclosure — drives the per-item .ap-sub-toggle
// buttons (About / Library / Research / Suite Overview). Progressive
// enhancement on top of the CSS-only fallback:
//   - With JS off, html has no .has-js class, so the stylesheet's
//     :hover / :focus-within rules open the panels on their own.
//   - With JS on, .has-js scopes the :focus-within fallback out and the
//     buttons take over: click (and native Enter/Space on <button>)
//     toggles aria-expanded, which the CSS maps to panel visibility.
//     Escape closes the open panel and returns focus to its button;
//     clicking or focusing outside closes everything. Hover stays as a
//     pure-CSS enhancement for mouse users. Same-origin, CSP-safe.
// ---------------------------------------------------------------------------
(function () {
    "use strict";
    // ``\x20`` preserves the descendant-combinator space through the SSG's
    // CSS-aware string minifier (same workaround as the Mermaid styles).
    var SUB_SEL = ".ap-menu\x20.has-sub";
    var items = document.querySelectorAll(SUB_SEL);
    if (!items.length) return;
    document.documentElement.classList.add("has-js");

    var pairs = [];
    items.forEach(function (li) {
        var btn = li.querySelector("button.ap-sub-toggle[aria-controls]");
        if (!btn) return;
        var panel = document.getElementById(btn.getAttribute("aria-controls"));
        if (!panel) return;
        pairs.push({ li: li, btn: btn });
    });
    if (!pairs.length) return;

    function closeAll(except) {
        pairs.forEach(function (p) {
            if (p.btn !== except) p.btn.setAttribute("aria-expanded", "false");
        });
    }

    pairs.forEach(function (p) {
        p.btn.addEventListener("click", function () {
            var open = p.btn.getAttribute("aria-expanded") === "true";
            closeAll(p.btn);
            p.btn.setAttribute("aria-expanded", open ? "false" : "true");
        });
        // Escape inside the item: close the panel, hand focus back to
        // the button so keyboard users don't lose their place.
        p.li.addEventListener("keydown", function (e) {
            if (e.key !== "Escape" && e.key !== "Esc") return;
            if (p.btn.getAttribute("aria-expanded") !== "true") return;
            e.stopPropagation();
            p.btn.setAttribute("aria-expanded", "false");
            p.btn.focus();
        });
        // Tabbing out of the item closes its panel.
        p.li.addEventListener("focusout", function (e) {
            if (e.relatedTarget && p.li.contains(e.relatedTarget)) return;
            p.btn.setAttribute("aria-expanded", "false");
        });
    });

    // Click anywhere outside the nav items closes every open panel.
    document.addEventListener("click", function (e) {
        var inside = e.target.closest && e.target.closest(SUB_SEL);
        if (!inside) closeAll(null);
    });
})();

// ---------------------------------------------------------------------------
// Mobile nav toggle — expose disclosure state to assistive technology.
// The menu itself is a CSS `:has(.ap-toggle:checked)` disclosure that works
// with JavaScript disabled; this pass only mirrors the checkbox state into
// `aria-expanded` (valid on role=checkbox per WAI-ARIA 1.2) and wires
// `aria-controls`, so screen readers announce expanded / collapsed without
// changing the no-JS behaviour.
// ---------------------------------------------------------------------------
(function () {
    "use strict";
    var toggle = document.getElementById("ap-menu-toggle");
    if (!toggle) return;
    var nav = document.querySelector('.ap-nav nav[aria-label="Primary navigation"]');
    if (nav && !nav.id) nav.id = "ap-primary-nav";
    if (nav) toggle.setAttribute("aria-controls", nav.id);
    var sync = function () {
        toggle.setAttribute("aria-expanded", toggle.checked ? "true" : "false");
    };
    sync();
    toggle.addEventListener("change", sync);
})();
