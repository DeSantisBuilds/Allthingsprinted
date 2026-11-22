/* All Things Printed — small site script (no dependencies) */
(function () {
  "use strict";

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

  // ----- Placeholder social links: don't jump to top of page -----
  document.querySelectorAll("[data-placeholder-link]").forEach(function (a) {
    a.addEventListener("click", function (e) { e.preventDefault(); });
  });

  // ----- Quote form → pre-filled email (no server needed) -----
  var form = document.getElementById("quote-form");
  if (!form) return;
  var status = document.getElementById("quote-status");
  var PLACEHOLDER_EMAIL = "you@example.com";

  function showStatus(message, type) {
    status.className = "form-status is-" + type;
    status.textContent = message;
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
      showStatus("Please fill in your name, a valid email, and your project details.", "error");
      firstInvalid.focus();
      return;
    }

    var to = (form.getAttribute("data-quote-email") || "").trim();
    if (!to || to === PLACEHOLDER_EMAIL) {
      showStatus(
        "Online quote requests aren't set up yet, so nothing was sent. " +
        "Please contact us directly using the details on this page.",
        "warning"
      );
      return;
    }

    var v = function (name) { return (form.elements[name].value || "").trim(); };
    var lines = [
      "Name: " + v("name"),
      "Email: " + v("email"),
      "Phone: " + (v("phone") || "-"),
      "Service: " + v("service"),
      "Product: " + (v("product") || "-"),
      "Approx. quantity: " + (v("quantity") || "-"),
      "Needed by: " + (v("needed_by") || "-"),
      "",
      "Project details:",
      v("details")
    ];
    var subject = "Quote request: " + v("service") + " - " + v("name");
    var href = "mailto:" + to +
      "?subject=" + encodeURIComponent(subject) +
      "&body=" + encodeURIComponent(lines.join("\n"));

    showStatus(
      "Your email app should now open with your request filled in. Remember to press Send there. " +
      "If nothing opened, email us at " + to + ".",
      "success"
    );
    window.location.href = href;
  });
})();
