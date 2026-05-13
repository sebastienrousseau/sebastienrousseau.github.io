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
 * GA4 engagement instrumentation — three event families on top of the
 * default page_view:
 *   - scroll_depth at 25 / 50 / 75 / 100 % (once per threshold per page)
 *   - reading_time at 15 / 30 / 60 / 120 / 300 s (once per milestone)
 *   - click_outbound on any <a> whose host !== current host
 * Defers silently if gtag isn't loaded (preview / blocked-tracker case).
 */
(function ga4Engagement() {
    "use strict";
    if (typeof window === "undefined") return;

    function send(name, params) {
        if (typeof window.gtag !== "function") return;
        window.gtag("event", name, params || {});
    }

    var thresholds = [25, 50, 75, 100];
    var hit = {};
    function checkScroll() {
        var de = document.documentElement;
        var max = de.scrollHeight - window.innerHeight;
        if (max <= 0) return;
        var pct = (window.scrollY / max) * 100;
        for (var i = 0; i < thresholds.length; i++) {
            var t = thresholds[i];
            if (pct >= t && !hit[t]) {
                hit[t] = true;
                send("scroll_depth", { percent: t });
            }
        }
    }
    var scrollTicking = false;
    window.addEventListener("scroll", function () {
        if (!scrollTicking) {
            window.requestAnimationFrame(function () {
                checkScroll();
                scrollTicking = false;
            });
            scrollTicking = true;
        }
    }, { passive: true });

    [15, 30, 60, 120, 300].forEach(function (s) {
        window.setTimeout(function () {
            if (document.visibilityState !== "hidden") {
                send("reading_time", { seconds: s });
            }
        }, s * 1000);
    });

    document.addEventListener("click", function (e) {
        var a = e.target.closest("a[href]");
        if (!a) return;
        var href = a.getAttribute("href");
        if (!href || href.charAt(0) === "#" || href.charAt(0) === "/") return;
        var url;
        try {
            url = new URL(href, window.location.href);
        } catch (err) {
            return;
        }
        if (url.host === window.location.host) return;
        send("click_outbound", {
            link_url: url.href,
            link_domain: url.host,
            link_text: (a.textContent || "").trim().slice(0, 120)
        });
    }, { capture: true });
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
