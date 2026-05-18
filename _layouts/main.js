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
 * Forward clicks on the in-nav .ap-search button to the hidden Static Site Generator search
 * widget (#ssg-search-btn). The widget injects asynchronously, so we keep
 * trying on click rather than caching the reference.
 */
document.addEventListener("click", function (event) {
    var trigger = event.target.closest(".ap-search");
    if (!trigger) return;
    event.preventDefault();
    var ssg = document.getElementById("ssg-search-btn");
    if (ssg) {
        ssg.click();
    }
});

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
    }, { rootMargin: "0px 0px -10% 0px", threshold: 0.05 });
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
 * Mermaid renderer — lazy-loads the Mermaid library from jsdelivr only
 * when the page actually contains <pre class="mermaid"> blocks. Pages
 * without Mermaid pay no JS / no network cost; pages with Mermaid widen
 * their meta-CSP to allow the import via the postbuild patch.
 */
(async function mermaidInit() {
    "use strict";
    if (!document.querySelector("pre.mermaid")) return;
    var theme = document.documentElement.getAttribute("data-theme") === "dark" ? "dark" : "default";
    try {
        var mod = await import(
            "https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs"
        );
        mod.default.initialize({ startOnLoad: true, securityLevel: "strict", theme: theme });
    } catch (err) {
        console.warn("mermaid load failed", err);
    }
})();
