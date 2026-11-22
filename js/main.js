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
