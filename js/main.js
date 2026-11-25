/* All Things Printed — small site script (no dependencies) */
(function () {
  "use strict";

  /* ========================================================================
     SITE SETTINGS — the only part of this file you normally need to edit.
     ======================================================================== */
  var CONFIG = {
    // Optional analytics. Leave empty to use none. When one is set, the cookie
    // notice asks visitors for consent and loads it only if they accept.
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
    invalid: "Veuillez indiquer votre nom, votre téléphone, un courriel valide et les détails de votre projet.",
    sending: "Envoi en cours…",
    sent: "Merci! Votre demande a bien été envoyée. Nous vous contacterons rapidement.",
    preview: "Aperçu seulement : ce formulaire n'envoie rien dans l'aperçu de développement.",
    failed: "La demande n'a pas pu être envoyée. Réessayez, ou appelez-nous au 514 815-1829 ou écrivez à info@allthingsprinted.ca.",
    subject: "Nouveau lead",
    product: "Produit",
    cookie: {
      region: "Témoins et confidentialité",
      title: "Témoins et confidentialité",
      notice: "Ce site n'utilise aucun témoin publicitaire ni de suivi. Il enregistre seulement ce choix dans votre navigateur.",
      ask: "Ce site n'utilise aucun témoin publicitaire. Avec votre permission, nous utilisons des outils de mesure d'audience pour comprendre comment le site est utilisé.",
      ok: "J'ai compris", accept: "Tout accepter", refuse: "Refuser", customize: "Personnaliser", save: "Enregistrer mes choix",
      necessary: "Nécessaires (toujours actifs)", necessaryDesc: "Fonctionnement du site et mémorisation de vos choix.",
      analytics: "Mesure d'audience", analyticsDesc: "Statistiques de visite pour améliorer le site.",
      policy: "Politique de confidentialité", policyHref: "confidentialite.html"
    }
  } : {
    invalid: "Please fill in your name, phone, a valid email and your project details.",
    sending: "Sending…",
    sent: "Thank you! Your request was sent. We'll contact you shortly.",
    preview: "Preview only: this form sends nothing in the development preview.",
    failed: "Your request couldn't be sent. Please try again, or call (514) 815-1829 or email info@allthingsprinted.ca.",
    subject: "New lead",
    product: "Product",
    cookie: {
      region: "Cookies and privacy",
      title: "Cookies and privacy",
      notice: "This site uses no advertising or tracking cookies. It only stores this choice in your browser.",
      ask: "This site uses no advertising cookies. With your permission, we use analytics to understand how the site is used.",
      ok: "Got it", accept: "Accept all", refuse: "Decline", customize: "Customize", save: "Save my choices",
      necessary: "Necessary (always on)", necessaryDesc: "Site operation and remembering your choices.",
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
      var h = document.createElement("p");
      h.className = "cookie-title";
      h.textContent = C.title;
      var p = document.createElement("p");
      p.textContent = hasAnalytics ? C.ask : C.notice;
      var link = document.createElement("a");
      var footerPolicy = document.querySelector("[data-policy-link]");
      link.href = footerPolicy ? footerPolicy.getAttribute("href") : C.policyHref;
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

  // ----- Forms: sent straight to the business email by FormSubmit -----
  // Each form's "action" is the FormSubmit address. With JavaScript we send it in
  // the background (FormSubmit's /ajax/ address) and show a message on the page;
  // without JavaScript the browser posts it normally.
  function setupForm(form, opts) {
    var status = form.querySelector("[data-status]") || document.getElementById("form-status");
    var submitBtn = form.querySelector('button[type="submit"]');

    function showStatus(message, type) {
      status.className = "form-status is-" + type;
      status.textContent = message;
    }

    // Clear an error message as soon as the visitor edits the form again.
    form.addEventListener("input", function () {
      if (status.classList.contains("is-error")) { status.className = "form-status"; status.textContent = ""; }
    });

    form.addEventListener("submit", function (e) {
      e.preventDefault();
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
      if (opts.validate) {
        var problem = opts.validate();
        if (problem) { showStatus(problem.message, "error"); if (problem.focus) problem.focus.focus(); return; }
      }

      // Development preview: never send anything.
      if (form.getAttribute("data-preview") === "true") { showStatus(T.preview, "info"); return; }

      // The subject carries the key facts (it is what shows in a text-message alert).
      form.querySelector('input[name="_subject"]').value = opts.subject();
      var data = new FormData(form);
      if (opts.prepare) opts.prepare(data);

      var label = submitBtn.textContent;
      submitBtn.disabled = true;
      submitBtn.textContent = T.sending;
      showStatus(T.sending, "info");

      fetch(form.action.replace("formsubmit.co/", "formsubmit.co/ajax/"), {
        method: "POST",
        headers: { "Accept": "application/json" },
        body: data
      })
        .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { return { ok: r.ok, body: j }; }); })
        .then(function (res) {
          var success = res.ok && res.body && (res.body.success === true || res.body.success === "true");
          if (success) {
            form.reset();
            if (opts.afterReset) opts.afterReset();
            showStatus(opts.sent, "success");
          } else {
            showStatus(T.failed, "error");
          }
        })
        .catch(function () { showStatus(T.failed, "error"); })
        .then(function () {
          submitBtn.disabled = false;
          submitBtn.textContent = label;
        });
    });
  }

  function val(form, selector) {
    var el = form.querySelector(selector);
    return el ? el.value.trim() : "";
  }

  // Quote / lead form
  var lead = document.getElementById("lead-form");
  if (lead) {
    var serviceSelect = lead.querySelector("#q-service");
    var details = lead.querySelector("#q-details");

    var requestType = function () {
      var checked = lead.querySelector('.segmented input:checked');
      return checked ? checked.value : "";
    };

    setupForm(lead, {
      sent: T.sent,
      subject: function () {
        var type = requestType();
        var isReorder = lead.querySelector('.segmented input:checked') !== lead.querySelector('.segmented input');
        return T.subject + ": " + val(lead, "#q-name") + " - " + val(lead, "#q-phone") + " - " +
          (serviceSelect ? serviceSelect.value : "") + (isReorder ? " - " + type : "");
      }
    });

    // Buttons and cards that name a service pre-select it in the form;
    // garments also add "Product: …" to the project details.
    var selectService = function (key) {
      if (!serviceSelect || !key) return;
      for (var i = 0; i < serviceSelect.options.length; i++) {
        if (serviceSelect.options[i].getAttribute("data-key") === key) { serviceSelect.selectedIndex = i; return; }
      }
    };
    document.querySelectorAll("[data-service]").forEach(function (link) {
      link.addEventListener("click", function () {
        selectService(link.getAttribute("data-service"));
        var product = link.getAttribute("data-product");
        if (product && details) {
          var line = T.product + ": " + product;
          if (details.value.indexOf(line) === -1) details.value = line + (details.value ? "\n" + details.value : "\n");
        }
      });
    });
  }
})();
