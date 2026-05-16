
      (function () {
        var loaded = false;
        function load() {
          if (loaded) return;
          loaded = true;
          var s = document.createElement('script');
          s.src = 'https://www.google.com/recaptcha/api.js';
          s.async = true;
          s.defer = true;
          document.head.appendChild(s);
        }
        var form = document.querySelector('form.ap-form');
        if (!form) return;
        ['focusin', 'click', 'touchstart'].forEach(function (ev) {
          form.addEventListener(ev, load, { once: true, passive: true });
        });
        // Fallback: if the page sits idle on /contact/ for 4s, load anyway
        // so the widget renders before the user reaches the submit button.
        setTimeout(load, 4000);
      })();
    