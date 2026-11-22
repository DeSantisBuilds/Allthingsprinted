/* All Things Printed — small site script (no dependencies) */
(function () {
  "use strict";

  /* ========================================================================
     SITE SETTINGS — the only part of this file you normally need to edit.
     ======================================================================== */
  var CONFIG = {
    // Online quote form with Cloudflare Turnstile. Paste your Turnstile SITE key
    // (the public one, it starts with "0x") to switch the form from "open the
    // visitor's email app" to "send online with file uploads". The SECRET key
    // never goes here: it is stored in Cloudflare (see README).
    turnstileSiteKey: "",
    // Address of the Worker that receives the form. "/api/quote" works when the
    // site itself runs on the Worker. If the site is on GitHub Pages, use the
    // Worker's full address, e.g. "https://allthingsprinted.<account>.workers.dev/api/quote".
    quoteEndpoint: "/api/quote",
    // Optional analytics. Leave empty to use none. When one is set, the cookie
    // banner asks visitors for consent and loads it only if they accept.
    cloudflareAnalyticsToken: "",
    googleAnalyticsId: ""
  };

  document.documentElement.classList.remove("no-js");

  // ----- Mobile navigation -----
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");
  if (toggle && nav) {
    var setOpen = function (open) {
      toggle.setAttribute("aria-expanded", String(open));
      nav.classList.toggle("is-open", open);
    };
    toggle.addEventListener("click", function () {
      setOpen(toggle.getAttribute("aria-expanded") !== "true");
    });
    nav.addEventListener("click", function (e) {
      if (e.target.closest("a")) setOpen(false);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("is-open")) {
        setOpen(false);
        toggle.focus();
      }
    });
  }

  // ----- Hero: one-time three-colour motion -----
  // The cyan, magenta and yellow circles behind the T-shirt drift, orbit and
  // breathe for 12 seconds, slow down, and land back exactly where the CSS puts
  // them. Each motion is a mix of sine waves multiplied by an envelope that is
  // zero (with zero speed) at 0s and at 12s, so the start and the landing are
  // seamless. Only transforms change (GPU-friendly, no layout shifts). At 12s
  // every inline style is removed, so the hero is the original static design.
  (function heroMotion() {
    var art = document.querySelector(".hero-art");
    if (!art || !window.requestAnimationFrame) return;
    if (window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

    var DURATION = 12000;
    var TAU = Math.PI * 2;
    // Per circle: orbit around the art's centre (deg), drift (fraction of the
    // art's size) and scale, each as amplitude / frequency (Hz) / phase.
    var layers = [
      { sel: ".swatch-c", rot: [58, 0.19, 0.4], x: [0.07, 0.31, 0.0], y: [0.06, 0.27, 1.3], s: [0.08, 0.23, 0.0] },
      { sel: ".swatch-m", rot: [-66, 0.17, 1.1], x: [0.06, 0.29, 2.0], y: [0.07, 0.33, 0.6], s: [0.07, 0.26, 0.8] },
      { sel: ".swatch-y", rot: [50, 0.22, 2.2], x: [0.05, 0.35, 0.5], y: [0.06, 0.24, 2.6], s: [0.09, 0.20, 1.7] }
    ].map(function (l) {
      l.el = art.querySelector(l.sel);
      return l;
    }).filter(function (l) { return l.el; });
    if (!layers.length) return;

    var size = 0;
    function measure() {
      size = art.clientWidth;
      layers.forEach(function (l) {
        // Pivot every circle around the centre of the artwork (behind the shirt).
        var ox = art.clientWidth / 2 - l.el.offsetLeft;
        var oy = art.clientHeight / 2 - l.el.offsetTop;
        l.el.style.transformOrigin = ox + "px " + oy + "px";
      });
    }

    function wave(p, t) { return p[0] * Math.sin(TAU * p[1] * t + p[2]); }

    // 0 at the start and the end, with zero speed at both, so motion eases in
    // quickly, then decays smoothly into the final pose.
    function envelope(ms) {
      var r = Math.min(ms / 900, 1);
      var rise = r * r * (3 - 2 * r);
      var fall = 1 - ms / DURATION;
      return rise * fall * fall;
    }

    function finish() {
      layers.forEach(function (l) {
        l.el.style.transform = "";
        l.el.style.transformOrigin = "";
        l.el.style.willChange = "";
      });
      window.removeEventListener("resize", measure);
    }

    layers.forEach(function (l) { l.el.style.willChange = "transform"; });
    measure();
    window.addEventListener("resize", measure);

    var start = null;
    function frame(now) {
      if (start === null) start = now;
      var ms = now - start;
      if (ms >= DURATION) { finish(); return; }
      var e = envelope(ms);
      var t = ms / 1000;
      layers.forEach(function (l) {
        var dx = wave(l.x, t) * e * size;
        var dy = wave(l.y, t) * e * size;
        var rot = wave(l.rot, t) * e;
        var sc = 1 + wave(l.s, t) * e;
        l.el.style.transform =
          "translate3d(" + dx.toFixed(2) + "px," + dy.toFixed(2) + "px,0) " +
          "rotate(" + rot.toFixed(3) + "deg) scale(" + sc.toFixed(4) + ")";
      });
      requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  })();

  // ----- Footer year -----
  var year = document.getElementById("year");
  if (year) year.textContent = new Date().getFullYear();

  // ----- Language: French is the main page, English lives at /en/ -----
  var FR = (document.documentElement.lang || "").toLowerCase().indexOf("fr") === 0;
  var T = FR ? {
    invalid: "Veuillez indiquer votre nom, un courriel valide et les détails de votre projet.",
    notSet: "Les demandes de soumission en ligne ne sont pas encore configurées; rien n'a été envoyé. Communiquez avec nous directement.",
    opened: function (to) { return "Votre application de courriel devrait s'ouvrir avec votre demande. Joignez votre visuel, puis appuyez sur Envoyer. Si rien ne s'est ouvert, écrivez-nous à " + to + "."; },
    subject: "Demande de soumission",
    labels: { name: "Nom", email: "Courriel", phone: "Téléphone", service: "Service", product: "Produit",
      quantity: "Quantité approx.", needed_by: "Date souhaitée", sizes: "Tailles", colours: "Couleurs",
      locations: "Emplacements d'impression", artwork: "Visuel", details: "Détails du projet" },
    attach: "(Joignez votre visuel ou votre logo à ce courriel.)",
    sending: "Envoi en cours…",
    sent: "Merci! Votre demande a bien été envoyée. Nous vous répondrons par courriel.",
    captcha: "Veuillez compléter la vérification de sécurité, puis réessayer.",
    captchaLoad: "La vérification de sécurité n'a pas pu se charger. Rechargez la page ou écrivez-nous à info@allthingsprinted.ca.",
    fileType: "Un des fichiers n'est pas d'un format accepté (PNG, JPG, PDF, SVG, AI, EPS, PSD, TIFF ou WEBP).",
    fileSize: "Les fichiers sont trop volumineux : 5 fichiers et 15 Mo au total au maximum.",
    failed: "La demande n'a pas pu être envoyée. Réessayez, ou écrivez-nous à info@allthingsprinted.ca ou appelez le 514 815-1829.",
    cookie: {
      region: "Témoins et confidentialité",
      title: "Témoins et confidentialité",
      notice: "Ce site n'utilise aucun témoin publicitaire ni de suivi. Il utilise seulement ce qui est nécessaire à son fonctionnement, comme la mémorisation de ce choix et une vérification de sécurité Cloudflare qui protège le formulaire de soumission contre le pourriel.",
      ask: "Nous utilisons ce qui est nécessaire au fonctionnement du site, comme une vérification de sécurité Cloudflare sur le formulaire. Avec votre permission, nous utilisons aussi des outils de mesure d'audience pour comprendre comment le site est utilisé.",
      ok: "J'ai compris", accept: "Tout accepter", refuse: "Refuser", customize: "Personnaliser", save: "Enregistrer mes choix",
      necessary: "Nécessaires (toujours actifs)", necessaryDesc: "Fonctionnement du site, mémorisation de vos choix et protection du formulaire.",
      analytics: "Mesure d'audience", analyticsDesc: "Statistiques de visite pour améliorer le site.",
      policy: "Politique de confidentialité", policyHref: "confidentialite.html"
    }
  } : {
    invalid: "Please fill in your name, a valid email, and your project details.",
    notSet: "Online quote requests aren't set up yet, so nothing was sent. Please contact us directly.",
    opened: function (to) { return "Your email app should now open with your request filled in. Attach your artwork, then press Send. If nothing opened, email us at " + to + "."; },
    subject: "Quote request",
    labels: { name: "Name", email: "Email", phone: "Phone", service: "Service", product: "Product",
      quantity: "Approx. quantity", needed_by: "Needed by", sizes: "Sizes", colours: "Colours",
      locations: "Print locations", artwork: "Artwork", details: "Project details" },
    attach: "(Please attach your artwork or logo to this email.)",
    sending: "Sending…",
    sent: "Thank you! Your request was sent. We'll reply by email.",
    captcha: "Please complete the security check, then try again.",
    captchaLoad: "The security check couldn't load. Reload the page or email us at info@allthingsprinted.ca.",
    fileType: "One of the files isn't an accepted format (PNG, JPG, PDF, SVG, AI, EPS, PSD, TIFF or WEBP).",
    fileSize: "The files are too large: up to 5 files and 15 MB in total.",
    failed: "Your request couldn't be sent. Please try again, or email info@allthingsprinted.ca or call (514) 815-1829.",
    cookie: {
      region: "Cookies and privacy",
      title: "Cookies and privacy",
      notice: "This site uses no advertising or tracking cookies. It only uses what it needs to work, such as remembering this choice and a Cloudflare security check that protects the quote form from spam.",
      ask: "We use what the site needs to work, such as a Cloudflare security check on the quote form. With your permission, we also use analytics to understand how the site is used.",
      ok: "Got it", accept: "Accept all", refuse: "Decline", customize: "Customize", save: "Save my choices",
      necessary: "Necessary (always on)", necessaryDesc: "Site operation, remembering your choices and protecting the form.",
      analytics: "Analytics", analyticsDesc: "Visit statistics to improve the site.",
      policy: "Privacy policy", policyHref: "privacy.html"
    }
  };

  // ----- Cookie consent (Quebec Law 25: nothing optional runs before consent) -----
  (function cookieConsent() {
    var KEY = "atp-consent-v1";
    var C = T.cookie;
    var hasAnalytics = !!(CONFIG.cloudflareAnalyticsToken || CONFIG.googleAnalyticsId);

    function read() {
      try { return JSON.parse(localStorage.getItem(KEY) || "null"); } catch (e) { return null; }
    }
    function write(choice) {
      choice.date = new Date().toISOString();
      try { localStorage.setItem(KEY, JSON.stringify(choice)); } catch (e) { /* private mode: ask again next visit */ }
    }

    var analyticsLoaded = false;
    function loadAnalytics() {
      if (analyticsLoaded) return;
      analyticsLoaded = true;
      if (CONFIG.cloudflareAnalyticsToken) {
        var cf = document.createElement("script");
        cf.defer = true;
        cf.src = "https://static.cloudflareinsights.com/beacon.min.js";
        cf.setAttribute("data-cf-beacon", JSON.stringify({ token: CONFIG.cloudflareAnalyticsToken }));
        document.head.appendChild(cf);
      }
      if (CONFIG.googleAnalyticsId) {
        var ga = document.createElement("script");
        ga.async = true;
        ga.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(CONFIG.googleAnalyticsId);
        document.head.appendChild(ga);
        window.dataLayer = window.dataLayer || [];
        window.gtag = function () { window.dataLayer.push(arguments); };
        window.gtag("js", new Date());
        window.gtag("config", CONFIG.googleAnalyticsId);
      }
    }

    var banner = null;
    function close() { if (banner) { banner.remove(); banner = null; } }
    function decide(analytics) {
      write({ analytics: !!analytics });
      close();
      if (analytics && hasAnalytics) loadAnalytics();
      else if (analyticsLoaded) location.reload(); // consent withdrawn: reload without the scripts
    }

    function button(label, cls, onClick) {
      var b = document.createElement("button");
      b.type = "button";
      b.className = "btn btn-sm " + cls;
      b.textContent = label;
      b.addEventListener("click", onClick);
      return b;
    }

    function open(showDetails) {
      close();
      var saved = read();
      banner = document.createElement("section");
      banner.className = "cookie-banner";
      banner.setAttribute("aria-label", C.region);
      var inner = document.createElement("div");
      inner.className = "cookie-inner";
      var h = document.createElement("h2");
      h.className = "cookie-title";
      h.textContent = C.title;
      var p = document.createElement("p");
      p.textContent = hasAnalytics ? C.ask : C.notice;
      var link = document.createElement("a");
      link.href = C.policyHref;
      link.textContent = C.policy;
      p.appendChild(document.createTextNode(" "));
      p.appendChild(link);
      inner.appendChild(h);
      inner.appendChild(p);

      var actions = document.createElement("div");
      actions.className = "cookie-actions";
      if (!hasAnalytics) {
        actions.appendChild(button(C.ok, "btn-primary", function () { decide(false); }));
      } else {
        var details = document.createElement("div");
        details.className = "cookie-details";
        details.hidden = !showDetails;
        details.innerHTML =
          '<label class="cookie-option"><input type="checkbox" checked disabled> <span><strong></strong><br><span class="cookie-desc"></span></span></label>' +
          '<label class="cookie-option"><input type="checkbox" data-analytics> <span><strong></strong><br><span class="cookie-desc"></span></span></label>';
        var strongs = details.querySelectorAll("strong"), descs = details.querySelectorAll(".cookie-desc");
        strongs[0].textContent = C.necessary; descs[0].textContent = C.necessaryDesc;
        strongs[1].textContent = C.analytics; descs[1].textContent = C.analyticsDesc;
        var box = details.querySelector("[data-analytics]");
        box.checked = !!(saved && saved.analytics);
        inner.appendChild(details);

        actions.appendChild(button(C.accept, "btn-primary", function () { decide(true); }));
        actions.appendChild(button(C.refuse, "btn-outline-light", function () { decide(false); }));
        var custom = button(showDetails ? C.save : C.customize, "btn-outline-light", function () {
          if (details.hidden) { details.hidden = false; custom.textContent = C.save; box.focus(); }
          else decide(box.checked);
        });
        actions.appendChild(custom);
      }
      inner.appendChild(actions);
      banner.appendChild(inner);
      document.body.appendChild(banner);
      return banner;
    }

    document.querySelectorAll("[data-cookie-settings]").forEach(function (b) {
      b.addEventListener("click", function () {
        var el = open(true);
        var first = el.querySelector("input:not([disabled]), button");
        if (first) first.focus();
      });
    });

    var saved = read();
    if (!saved) open(false);
    else if (saved.analytics && hasAnalytics) loadAnalytics();
  })();

  // ----- Quote form -----
  var form = document.getElementById("quote-form");
  if (!form) return;
  var status = document.getElementById("quote-status");
  var submitBtn = form.querySelector('button[type="submit"]');
  var PLACEHOLDER_EMAIL = "you@example.com";
  // "online": Turnstile + Worker with file uploads. "email": opens the visitor's email app.
  var ONLINE = !!(CONFIG.turnstileSiteKey && CONFIG.quoteEndpoint);

  function showStatus(message, type) {
    status.className = "form-status is-" + type;
    status.textContent = message;
  }

  document.querySelectorAll("[data-mode]").forEach(function (el) {
    el.hidden = el.getAttribute("data-mode") !== (ONLINE ? "online" : "email");
  });
  if (submitBtn) submitBtn.textContent = submitBtn.getAttribute(ONLINE ? "data-label-online" : "data-label-email") || submitBtn.textContent;

  // Garment cards and service links pre-select the matching option in the form.
  function preselect(selectName, value) {
    var select = form.elements[selectName];
    if (!select || !value) return;
    for (var i = 0; i < select.options.length; i++) {
      if (select.options[i].text === value || select.options[i].value === value) {
        select.selectedIndex = i;
        return;
      }
    }
  }
  document.querySelectorAll("[data-product], [data-service]").forEach(function (link) {
    link.addEventListener("click", function () {
      if (link.dataset.product) {
        preselect("product", link.dataset.product);
        preselect("service", form.elements.service.options[0].text);
      }
      if (link.dataset.service) preselect("service", link.dataset.service);
    });
  });

  // Cloudflare Turnstile: loaded only in online mode, when the form comes near the screen.
  var widgetId = null, turnstileState = "idle";
  function loadTurnstile() {
    if (!ONLINE || turnstileState !== "idle") return;
    turnstileState = "loading";
    window.atpTurnstileReady = function () {
      try {
        widgetId = window.turnstile.render("#turnstile", {
          sitekey: CONFIG.turnstileSiteKey,
          language: FR ? "fr" : "en",
          theme: "light"
        });
        turnstileState = "ready";
      } catch (e) { turnstileState = "error"; }
    };
    var s = document.createElement("script");
    s.src = "https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit&onload=atpTurnstileReady";
    s.async = true; s.defer = true;
    s.onerror = function () { turnstileState = "error"; showStatus(T.captchaLoad, "error"); };
    document.head.appendChild(s);
  }
  if (ONLINE) {
    if ("IntersectionObserver" in window) {
      var io = new IntersectionObserver(function (entries) {
        if (entries.some(function (en) { return en.isIntersecting; })) { loadTurnstile(); io.disconnect(); }
      }, { rootMargin: "600px 0px" });
      io.observe(form);
    } else {
      loadTurnstile();
    }
    form.addEventListener("focusin", loadTurnstile);
  }

  var ALLOWED_EXT = ["png", "jpg", "jpeg", "pdf", "svg", "ai", "eps", "psd", "tif", "tiff", "webp"];
  function checkFiles() {
    var input = form.elements.artwork_files;
    if (!input || !input.files) return null;
    var total = 0;
    if (input.files.length > 5) return T.fileSize;
    for (var i = 0; i < input.files.length; i++) {
      var ext = input.files[i].name.split(".").pop().toLowerCase();
      if (ALLOWED_EXT.indexOf(ext) === -1) return T.fileType;
      total += input.files[i].size;
    }
    return total > 15 * 1024 * 1024 ? T.fileSize : null;
  }

  function sendOnline() {
    var fileProblem = checkFiles();
    if (fileProblem) { showStatus(fileProblem, "error"); form.elements.artwork_files.focus(); return; }
    var token = window.turnstile && widgetId !== null ? window.turnstile.getResponse(widgetId) : "";
    if (!token) { showStatus(turnstileState === "error" ? T.captchaLoad : T.captcha, "error"); return; }

    var label = submitBtn.textContent;
    submitBtn.disabled = true;
    submitBtn.textContent = T.sending;
    showStatus(T.sending, "info");
    var data = new FormData(form);
    if (!data.get("cf-turnstile-response")) data.set("cf-turnstile-response", token);

    fetch(CONFIG.quoteEndpoint, { method: "POST", body: data })
      .then(function (r) { return r.json().catch(function () { return { ok: false, error: "send" }; }); })
      .then(function (res) {
        if (res && res.ok) {
          form.reset();
          showStatus(T.sent, "success");
        } else {
          var code = res && res.error;
          showStatus(code === "captcha" ? T.captcha : code === "file_type" ? T.fileType :
            (code === "file_size" || code === "too_many_files") ? T.fileSize :
            code === "invalid" ? T.invalid : T.failed, "error");
        }
      })
      .catch(function () { showStatus(T.failed, "error"); })
      .then(function () {
        submitBtn.disabled = false;
        submitBtn.textContent = label;
        if (window.turnstile && widgetId !== null) window.turnstile.reset(widgetId);
      });
  }

  function sendByEmailApp() {
    var to = (form.getAttribute("data-quote-email") || "").trim();
    if (!to || to === PLACEHOLDER_EMAIL) {
      showStatus(T.notSet, "warning");
      return;
    }

    var v = function (name) {
      var el = form.elements[name];
      return el ? (el.value || "").trim() : "";
    };
    var locations = Array.prototype.map.call(
      form.querySelectorAll('input[name="locations"]:checked'),
      function (box) { return box.value; }
    ).join(", ");
    var L = T.labels;
    var lines = [
      L.name + ": " + v("name"),
      L.email + ": " + v("email"),
      L.phone + ": " + (v("phone") || "-"),
      L.service + ": " + v("service"),
      L.product + ": " + (v("product") || "-"),
      L.quantity + ": " + (v("quantity") || "-"),
      L.needed_by + ": " + (v("needed_by") || "-"),
      L.sizes + ": " + (v("sizes") || "-"),
      L.colours + ": " + (v("colours") || "-"),
      L.locations + ": " + (locations || "-"),
      L.artwork + ": " + v("artwork"),
      "",
      L.details + ":",
      v("details"),
      "",
      T.attach
    ];
    var subject = T.subject + ": " + v("service") + " - " + v("name");
    var href = "mailto:" + to +
      "?subject=" + encodeURIComponent(subject) +
      "&body=" + encodeURIComponent(lines.join("\n"));

    showStatus(T.opened(to), "success");
    window.location.href = href;
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    // Basic validation
    var firstInvalid = null;
    form.querySelectorAll("[required]").forEach(function (el) {
      var ok = el.value.trim() !== "" && el.checkValidity();
      el.setAttribute("aria-invalid", ok ? "false" : "true");
      if (!ok && !firstInvalid) firstInvalid = el;
    });
    if (firstInvalid) {
      showStatus(T.invalid, "error");
      firstInvalid.focus();
      return;
    }

    if (ONLINE) sendOnline();
    else sendByEmailApp();
  });
})();
