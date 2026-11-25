#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Builds the All Things Printed website from tools/content.py.

    python3 tools/build.py                 # production files, written into the repository
    python3 tools/build.py --preview DIR   # private preview copy (links end in index.html,
                                           # temporary photo slots shown and labelled)

Standard library only. The generated HTML is committed, so the hosting (Cloudflare
Workers static assets) needs no build step.
"""
import hashlib
import html
import json
import os
import posixpath
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import content as C  # noqa: E402

LANGS = ("fr", "en")
SVC = {s["key"]: s for s in C.SERVICES}


# ---------------------------------------------------------------- pages ----
def page_list():
    pages = [{"id": "home", "file": {"fr": "index.html", "en": "en/index.html"}}]
    for s in C.SERVICES:
        pages.append({"id": "svc:" + s["key"], "file": {
            "fr": "services/%s/index.html" % s["slug"]["fr"],
            "en": "en/services/%s/index.html" % s["slug"]["en"]}})
    pages.append({"id": "privacy", "file": {"fr": "confidentialite.html", "en": "en/privacy.html"}})
    return pages


PAGES = page_list()
FILE_OF = {(p["id"], l): p["file"][l] for p in PAGES for l in LANGS}


def url_path(f):
    """Public URL path of an output file, as Cloudflare serves it (no redirect)."""
    if f.endswith("index.html"):
        return "/" + f[: -len("index.html")]
    return "/" + f[: -len(".html")]


def abs_url(f):
    return C.SITE["domain"] + url_path(f)


class Ctx:
    def __init__(self, cur, lang, mode):
        self.cur, self.lang, self.mode = cur, lang, mode
        self.dir = posixpath.dirname(cur)

    def link(self, target_file, anchor=""):
        """Relative link from the current page to another page."""
        if self.mode == "preview":
            rel = posixpath.relpath(target_file, self.dir or ".")
        elif self.cur == "404.html":  # served at any address: use absolute paths
            rel = url_path(target_file)
        else:
            tp = url_path(target_file).lstrip("/")
            if tp == "" or tp.endswith("/"):
                rel = posixpath.relpath(tp or ".", self.dir or ".")
                rel = "./" if rel == "." else rel + "/"
            else:
                rel = posixpath.relpath(tp, self.dir or ".")
        return rel + ("#" + anchor if anchor else "")

    def page(self, pid, lang=None, anchor=""):
        return self.link(FILE_OF[(pid, lang or self.lang)], anchor)

    def here(self, anchor):
        return "#" + anchor

    def asset(self, path):
        base = ("/" + path) if (self.cur == "404.html" and self.mode != "preview") else posixpath.relpath(path, self.dir or ".")
        return base + "?v=" + VERSIONS.get(path, "1")

    def asset_plain(self, path):
        return ("/" + path) if (self.cur == "404.html" and self.mode != "preview") else posixpath.relpath(path, self.dir or ".")


VERSIONS = {}


def fingerprint():
    for rel in ["css/styles.css", "css/nojs.css", "js/main.js", "assets/images/logo.webp", "assets/images/logo.png",
                "assets/images/logo-mark-light.webp", "assets/images/logo-mark-light-2x.webp",
                "assets/images/logo-mark-light.png", "assets/images/logo-mark-light-2x.png",
                "assets/images/favicon.png", "assets/images/apple-touch-icon.png", "assets/images/og-image.jpg",
                "assets/images/logo-sm.webp"]:
        p = os.path.join(ROOT, rel)
        if os.path.exists(p):
            with open(p, "rb") as fh:
                VERSIONS[rel] = hashlib.sha256(fh.read()).hexdigest()[:10]
    for item in C.PORTFOLIO:
        p = os.path.join(ROOT, item["file"])
        if os.path.exists(p):
            with open(p, "rb") as fh:
                VERSIONS[item["file"]] = hashlib.sha256(fh.read()).hexdigest()[:10]


# ------------------------------------------------------------ strings -----
T = {
    "fr": {
        "skip": "Passer au contenu principal", "menu": "Menu", "nav_label": "Principal",
        "nav": [("services", "Services"), ("realisations", "Réalisations"), ("clientele", "Clientèle"), ("faq", "FAQ"), ("soumission", "Contact")],
        "cta": "Soumission gratuite", "cta_long": "Demander une soumission gratuite",
        "call": "Appeler", "call_long": "Appeler le " + C.SITE["phone_fr"], "text": "Texter", "text_long": "Texter le " + C.SITE["phone_fr"],
        "switch": "EN", "switch_hidden": " – English version", "switch_lang": "en-CA",
        "home": "Accueil", "services": "Services",
        "tagline": "Votre marque. Votre vision. Imprimée.",
        "brand_aria": "All Things Printed, accueil",
        "footer_services": "Services", "footer_contact": "Contact", "footer_info": "Information",
        "policy": "Politique de confidentialité", "cookies": "Paramètres des témoins", "other_lang": "English version",
        "area_line": "Au service du Grand Montréal",
    },
    "en": {
        "skip": "Skip to main content", "menu": "Menu", "nav_label": "Main",
        "nav": [("services", "Services"), ("realisations", "Our work"), ("clientele", "Who we serve"), ("faq", "FAQ"), ("soumission", "Contact")],
        "cta": "Free quote", "cta_long": "Request a free quote",
        "call": "Call", "call_long": "Call " + C.SITE["phone_en"], "text": "Text", "text_long": "Text " + C.SITE["phone_en"],
        "switch": "FR", "switch_hidden": " – Version française", "switch_lang": "fr-CA",
        "home": "Home", "services": "Services",
        "tagline": "Your Brand. Your Vision. Printed.",
        "brand_aria": "All Things Printed, home",
        "footer_services": "Services", "footer_contact": "Contact", "footer_info": "Information",
        "policy": "Privacy policy", "cookies": "Cookie settings", "other_lang": "Version française",
        "area_line": "Serving Greater Montreal",
    },
}

ICONS = {
    "apparel": ('fill', '<path d="M17 6 L8 10 L3 19 L10 23 L13 20 L13 42 L35 42 L35 20 L38 23 L45 19 L40 10 L31 6 C30 10 27 12 24 12 C21 12 18 10 17 6 Z"/>'),
    "dtf": ('stroke', '<path d="M12 6 H36 V18 M12 18 V6"/><path d="M6 18 H42 V34 H6 Z"/><path d="M12 30 H36 V42 H12 Z"/><path d="M34 24 H37"/>'),
    "embroidery": ('stroke', '<path d="M9 39 L35 13"/><path d="M33 9 L39 15"/><path d="M35 13 C40 8 44 12 40 17"/><path d="M8 44 C14 38 20 44 26 38 C32 32 38 38 44 32"/>'),
    "vinyl": ('fill', '<path d="M6 36 L30 12 L36 18 L12 42 L6 42 Z M33 9 L36 6 L42 12 L39 15 Z"/>'),
    "signage": ('stroke', '<path d="M5 9 H43 V29 H5 Z"/><path d="M14 29 V43 M34 29 V43"/><path d="M12 16 H30 M12 22 H24"/>'),
    "promo": ('stroke', '<path d="M8 18 H40 V42 H8 Z M5 11 H43 V18 H5 Z M24 11 V42 M24 11 C18 3 10 6 14 11 M24 11 C30 3 38 6 34 11"/>'),
    "events": ('fill', '<path d="M24 42 L7 25 C2 20 3 11 10 9 C15 7.5 20 10 24 15 C28 10 33 7.5 38 9 C45 11 46 20 41 25 Z"/>'),
    "design": ('stroke', '<path d="M24 4 L36 22 L28 44 H20 L12 22 Z"/><path d="M24 4 V20"/><circle cx="24" cy="23" r="3"/>'),
}


def icon(key, cls="svc-icon"):
    kind, body = ICONS[key]
    return '<svg class="%s icon-%s" viewBox="0 0 48 48" aria-hidden="true" focusable="false">%s</svg>' % (cls, kind, body)


GARMENT_SVG = {
    "tshirt": '<path d="M42 14 L26 20 L8 38 L20 52 L30 45 L30 108 L90 108 L90 45 L100 52 L112 38 L94 20 L78 14 C75 22 68 27 60 27 C52 27 45 22 42 14 Z"/>',
    "longsleeve": '<path d="M42 14 L26 20 L14 40 L6 104 L20 106 L30 52 L30 108 L90 108 L90 52 L100 106 L114 104 L106 40 L94 20 L78 14 C75 22 68 27 60 27 C52 27 45 22 42 14 Z"/>',
    "hoodie": '<path d="M44 18 C44 6 76 6 76 18 L94 22 L106 40 L114 104 L100 106 L90 56 L90 108 L30 108 L30 56 L20 106 L6 104 L14 40 L26 22 Z"/><path class="detail" d="M46 20 C48 34 72 34 74 20 M40 80 H80 V98 H40 Z"/>',
    "polo": '<path d="M42 14 L26 20 L8 38 L20 52 L30 45 L30 108 L90 108 L90 45 L100 52 L112 38 L94 20 L78 14 L60 30 Z"/><path class="detail" d="M42 14 L52 34 L60 30 L68 34 L78 14 M60 30 V52"/>',
    "workwear": '<path d="M44 14 L26 20 L14 40 L6 104 L20 106 L30 52 L30 108 L90 108 L90 52 L100 106 L114 104 L106 40 L94 20 L76 14 L60 22 Z"/><path class="detail" d="M44 14 L52 26 L60 22 L68 26 L76 14 M60 22 V108 M38 72 H52 M68 72 H82"/>',
    "team": '<path d="M42 14 L26 20 L8 38 L20 52 L30 45 L30 108 L90 108 L90 45 L100 52 L112 38 L94 20 L78 14 L60 34 Z"/><path class="detail" d="M50 56 H70 L58 88"/>',
    # Baseball cap (crown + forward bill) with a tuque behind it.
    "cap": ('<path d="M20 74 C20 50 28 38 40 38 C52 38 60 50 60 74 Z"/><circle cx="40" cy="31" r="7"/><path d="M16 68 H64 V80 H16 Z"/>'
            '<path d="M44 92 C44 70 58 58 76 58 C94 58 106 70 106 90 Z"/><path d="M100 84 C108 84 116 88 116 94 C110 98 96 98 90 94 Z"/>'
            '<path class="detail" d="M76 58 C70 68 68 80 70 92 M44 92 H106"/><circle class="detail-dot" cx="76" cy="57" r="3"/>'),
}

PHOTO_SLOT = {"fr": ("ESPACE PHOTO TEMPORAIRE", "Photo à prendre", "Aperçu seulement : non publié sur le site"),
              "en": ("TEMPORARY PHOTO SLOT", "Photo to take", "Preview only: not published on the site")}


def esc(s):
    return html.escape(s, quote=True)


def strip_tags(s):
    out, skip = [], False
    for ch in s:
        if ch == "<":
            skip = True
        elif ch == ">":
            skip = False
        elif not skip:
            out.append(ch)
    return html.unescape("".join(out))


# ------------------------------------------------------------- shared -----
def head(ctx, title, desc, pid, extra_ld=None, noindex=False):
    lang = ctx.lang
    f = ctx.cur
    alts = ""
    if pid:
        alts = "\n".join(
            '  <link rel="alternate" hreflang="%s" href="%s">' % (h, abs_url(FILE_OF[(pid, l)]))
            for h, l in (("fr-CA", "fr"), ("en-CA", "en"), ("x-default", "fr")))
    canon = '  <link rel="canonical" href="%s">\n' % abs_url(f) if pid else ""
    og_url = abs_url(f) if pid else C.SITE["domain"] + "/"
    ld = ""
    for block in (extra_ld or []):
        ld += '  <script type="application/ld+json">%s</script>\n' % json.dumps(block, ensure_ascii=False, separators=(",", ":"))
    robots = '  <meta name="robots" content="noindex">\n' if noindex else ""
    return """<!DOCTYPE html>
<html lang="%(hl)s" class="no-js">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>%(title)s</title>
  <meta name="description" content="%(desc)s">
%(robots)s  <meta name="theme-color" content="#14161f">
%(canon)s%(alts)s
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="All Things Printed">
  <meta property="og:locale" content="%(ogl)s">
  <meta property="og:locale:alternate" content="%(ogl2)s">
  <meta property="og:title" content="%(title)s">
  <meta property="og:description" content="%(desc)s">
  <meta property="og:url" content="%(ogurl)s">
  <meta property="og:image" content="%(ogimg)s">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="All Things Printed">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="preload" href="%(font)s" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="%(css)s">
  <noscript><link rel="stylesheet" href="%(nojs)s"></noscript>
  <link rel="icon" type="image/png" href="%(fav)s">
  <link rel="apple-touch-icon" href="%(touch)s">
%(ld)s</head>
""" % {
        "hl": "fr-CA" if lang == "fr" else "en-CA", "title": esc(title), "desc": esc(desc), "robots": robots,
        "canon": canon, "alts": alts, "ogl": "fr_CA" if lang == "fr" else "en_CA", "ogl2": "en_CA" if lang == "fr" else "fr_CA",
        "ogurl": og_url, "ogimg": C.SITE["domain"] + "/assets/images/og-image.jpg",
        "font": ctx.asset_plain("assets/fonts/archivo-latin-wdth-normal.woff2"), "css": ctx.asset("css/styles.css"), "nojs": ctx.asset("css/nojs.css"),
        "fav": ctx.asset("assets/images/favicon.png"), "touch": ctx.asset("assets/images/apple-touch-icon.png"), "ld": ld,
    }


def header(ctx, pid):
    t = T[ctx.lang]
    other = "en" if ctx.lang == "fr" else "fr"
    switch_href = ctx.page(pid, other) if pid else ctx.page("home", other)
    on_home = pid == "home"
    nav = "\n".join(
        '          <li><a href="%s">%s</a></li>' % (ctx.here(a) if on_home else ctx.page("home", anchor=a), l)
        for a, l in t["nav"])
    switch = '<a class="lang-switch" href="%s" hreflang="%s" lang="%s">%s<span class="visually-hidden">%s</span></a>' % (
        switch_href, t["switch_lang"], t["switch_lang"], t["switch"], t["switch_hidden"])
    quote_href = "#soumission" if pid and pid != "privacy" else ctx.page("home", anchor="soumission")
    logo = ('<picture><source type="image/webp" srcset="%s 1x, %s 2x"><img src="%s" srcset="%s 1x, %s 2x" alt="" width="91" height="48"></picture>' % (
        ctx.asset("assets/images/logo-mark-light.webp"), ctx.asset("assets/images/logo-mark-light-2x.webp"),
        ctx.asset("assets/images/logo-mark-light.png"), ctx.asset("assets/images/logo-mark-light.png"), ctx.asset("assets/images/logo-mark-light-2x.png")))
    ribbon = ""
    if ctx.mode == "preview":
        ribbon = ('  <div class="preview-ribbon" role="note">%s</div>\n' % (
            "APERÇU DE DÉVELOPPEMENT PRIVÉ — non publié · les espaces photo sont temporaires · le formulaire n’envoie rien"
            if ctx.lang == "fr" else
            "PRIVATE DEVELOPMENT PREVIEW — not published · photo slots are temporary · the form sends nothing"))
    return """<body>
%(ribbon)s  <a class="skip-link" href="#main">%(skip)s</a>

  <header class="site-header">
    <div class="container header-inner">
      <a class="brand" href="%(home)s" aria-label="%(brand_aria)s">
        <span class="brand-logo">%(logo)s</span>
        <span class="brand-name">All Things Printed</span>
      </a>
      <div class="header-actions">
        %(switch)s
        <a class="btn btn-sm btn-primary header-cta" href="%(quote)s">%(cta)s</a>
        <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">
          <span class="nav-toggle-bar" aria-hidden="true"></span>
          <span class="visually-hidden">%(menu)s</span>
        </button>
      </div>
      <nav id="site-nav" class="site-nav" aria-label="%(navl)s">
        <ul>
%(nav)s
        </ul>
      </nav>
    </div>
  </header>
""" % {"ribbon": ribbon, "skip": t["skip"], "home": ctx.here("top") if on_home else ctx.page("home"), "brand_aria": t["brand_aria"], "logo": logo,
       "switch": switch, "quote": quote_href, "cta": t["cta"], "menu": t["menu"], "navl": t["nav_label"], "nav": nav}


def sticky_bar(ctx, has_form):
    t = T[ctx.lang]
    quote = "#soumission" if has_form else ctx.page("home", anchor="soumission")
    return """  <nav class="mobile-bar" aria-label="%s">
    <a href="tel:%s"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.6a1 1 0 0 1-.25 1Z"/></svg>%s</a>
    <a href="sms:%s"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M4 4h16a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H8l-4 4V6a2 2 0 0 1 2-2Z"/></svg>%s</a>
    <a class="mobile-bar-cta" href="%s">%s</a>
  </nav>
""" % ("Contact rapide" if ctx.lang == "fr" else "Quick contact", C.SITE["phone_e164"], t["call"], C.SITE["phone_e164"], t["text"], quote,
       "Soumission" if ctx.lang == "fr" else "Get a quote")


def footer(ctx, pid):
    t = T[ctx.lang]
    other = "en" if ctx.lang == "fr" else "fr"
    svc_links = "\n".join('            <li><a href="%s">%s</a></li>' % (ctx.page("svc:" + s["key"]), s[ctx.lang]["name"]) for s in C.SERVICES)
    phone = C.SITE["phone_fr"] if ctx.lang == "fr" else C.SITE["phone_en"]
    return """  <footer class="site-footer">
    <div class="container footer-grid">
      <div class="footer-brand">
        <p class="footer-name">All Things Printed</p>
        <p>%(tagline)s</p>
        <p>%(area)s<br>%(hours)s</p>
      </div>
      <div>
        <h2 class="footer-title">%(fs)s</h2>
        <ul class="footer-list">
%(svc)s
        </ul>
      </div>
      <div>
        <h2 class="footer-title">%(fc)s</h2>
        <ul class="footer-list">
            <li><a href="tel:%(tel)s">%(phone)s</a></li>
            <li><a href="sms:%(tel)s">%(textl)s</a></li>
            <li><a href="mailto:%(email)s">%(email)s</a></li>
            <li><a href="%(ig)s">Instagram %(igh)s</a></li>
        </ul>
      </div>
      <div>
        <h2 class="footer-title">%(fi)s</h2>
        <ul class="footer-list">
            <li><a href="%(other)s" hreflang="%(sl)s" lang="%(sl)s">%(ol)s</a></li>
            <li><a href="%(policy_href)s" data-policy-link>%(policy)s</a></li>
            <li><button type="button" class="link-button" data-cookie-settings>%(cookies)s</button></li>
        </ul>
      </div>
    </div>
    <div class="container footer-base">
      <p>&copy; <span id="year">2026</span> All Things Printed</p>
    </div>
  </footer>
""" % {"tagline": t["tagline"], "area": t["area_line"], "hours": C.FACTS[ctx.lang]["hours"], "fs": t["footer_services"], "svc": svc_links,
       "fc": t["footer_contact"], "tel": C.SITE["phone_e164"], "phone": phone, "textl": t["text_long"], "email": C.SITE["email"],
       "ig": C.SITE["instagram"], "igh": C.SITE["instagram_handle"], "fi": t["footer_info"],
       "other": ctx.page(pid, other) if pid else ctx.page("home", other), "sl": t["switch_lang"], "ol": t["other_lang"],
       "policy_href": ctx.page("privacy"), "policy": t["policy"], "cookies": t["cookies"]}


def scripts(ctx):
    return '  <script src="%s" defer></script>\n</body>\n</html>\n' % ctx.asset("js/main.js")


# ---------------------------------------------------------- components ----
def overprint(text, cls="overprint"):
    t = esc(text)
    return '<span class="%s" data-text="%s"><span class="ov-text" data-text="%s">%s</span></span>' % (cls, t, t, t)


def hero_art(ctx, kind):
    sw = '<div class="swatch swatch-c"></div><div class="swatch swatch-m"></div><div class="swatch swatch-y"></div>'
    if kind == "shirt":
        label = "( VOTRE LOGO ICI )" if ctx.lang == "fr" else "( LOGO HERE )"
        aria = "T-shirt avec un espace pour votre logo" if ctx.lang == "fr" else "T-shirt with a space for your logo"
        art = ('<svg class="hero-shirt" viewBox="0 0 200 200" role="img" aria-label="%s">'
               '<path d="M70 22 L44 32 L14 60 L34 86 L50 74 L50 182 L150 182 L150 74 L166 86 L186 60 L156 32 L130 22 C126 36 114 44 100 44 C86 44 74 36 70 22 Z"/>'
               '<rect class="print-area" x="49" y="60" width="102" height="50" rx="3"/>'
               '<text class="print-label" x="100" y="89" text-anchor="middle">%s</text></svg>') % (aria, label)
        return '<div class="hero-art">%s%s</div>' % (sw, art)
    return '<div class="hero-art hero-art-icon" aria-hidden="true">%s<div class="hero-tile">%s</div></div>' % (sw, icon(kind, "hero-icon"))


def chips(ctx):
    f = C.FACTS[ctx.lang]
    items = (["Maquette visuelle incluse", "Délai habituel&nbsp;: " + f["turnaround"], f["area"], f["hours_short"]] if ctx.lang == "fr"
             else ["Visual mockup included", "Typical turnaround: " + f["turnaround"], f["area"], f["hours_short"]])
    return '<ul class="trust-chips" role="list">%s</ul>' % "".join("<li>%s</li>" % i for i in items)


def seasonal(ctx):
    s = C.SEASONAL
    if not s["enabled"] and ctx.mode != "preview":
        return ""
    title, text, cta = s[ctx.lang]
    note = ""
    if not s["enabled"]:
        note = '<span class="preview-flag">%s</span>' % ("EXEMPLE — désactivé en production" if ctx.lang == "fr" else "EXAMPLE — off in production")
    return """    <aside class="seasonal" aria-label="%s">
      <div class="container seasonal-inner">%s
        <p><strong>%s</strong> %s</p>
        <a class="btn btn-sm btn-yellow" href="#soumission" data-service="%s">%s</a>
      </div>
    </aside>
""" % ("Promotion saisonnière" if ctx.lang == "fr" else "Seasonal promotion", note, title, text, s["service"], cta)


def service_cards(ctx, keys, heading_level="h3", compact=False):
    out = []
    for k in keys:
        s = SVC[k]
        d = s[ctx.lang]
        out.append("""          <li class="svc-card ink-%(ink)s">
            <a class="svc-card-link" href="%(href)s">
              <span class="svc-icon-tile">%(icon)s</span>
              <%(h)s class="svc-card-title">%(name)s</%(h)s>
              <span class="svc-card-text">%(card)s</span>
              <span class="svc-card-more" aria-hidden="true">%(more)s <span>&rarr;</span></span>
            </a>
          </li>""" % {"ink": s["ink"], "href": ctx.page("svc:" + k), "icon": icon(s["icon"]), "h": heading_level, "name": d["name"],
                      "card": d["card"], "more": "Voir le service" if ctx.lang == "fr" else "View service"})
    return '<ul class="svc-grid%s" role="list">\n%s\n        </ul>' % (" svc-grid-compact" if compact else "", "\n".join(out))


def garment_rail(ctx, title_id="products-title", with_head=True):
    items = []
    for g in C.GARMENTS:
        svg = GARMENT_SVG[g["key"]]
        items.append("""            <li class="product %s"><a class="product-link" href="#soumission" data-product="%s" data-service="apparel">
              <svg viewBox="0 0 120 120" aria-hidden="true" focusable="false">%s</svg>
              <span class="product-name">%s</span></a>
            </li>""" % (g["ink"], esc(g[ctx.lang]), svg, g[ctx.lang]))
    head_html = ""
    if with_head:
        head_html = """        <div class="section-head">
          <h2 id="%s" class="section-title">%s</h2>
          <p class="section-intro">%s</p>
        </div>
""" % (title_id, "Choisissez un vêtement" if ctx.lang == "fr" else "Pick a garment",
       "Ajoutez votre logo ou votre design. Cliquez sur un vêtement pour le préciser dans votre demande." if ctx.lang == "fr"
       else "Add your logo or design. Click a garment to add it to your request.")
    return """    <section id="vetements" class="section section-rack" aria-labelledby="%s">
      <div class="container">
%s        <div class="rack">
          <ul class="products" role="list">
%s
          </ul>
        </div>
      </div>
    </section>
""" % (title_id, head_html, "\n".join(items))


def portfolio(ctx, shots, service=None, section_id="realisations", title=None):
    lang = ctx.lang
    real = [p for p in C.PORTFOLIO if service is None or p.get("service") == service]
    title = title or ("Nos réalisations" if lang == "fr" else "Our work")
    ig_text = ("Voyez nos projets récents sur Instagram." if lang == "fr" else "See our recent projects on Instagram.")
    ig = """<a class="ig-card" href="%s">
            <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1"/></svg>
            <span><strong>%s</strong><br>%s</span>
          </a>""" % (C.SITE["instagram"], C.SITE["instagram_handle"], ig_text)
    cards = []
    for p in real:
        cards.append('<li><figure class="work-card"><img src="%s" alt="%s" width="%d" height="%d" loading="lazy"><figcaption>%s</figcaption></figure></li>' % (
            ctx.asset(p["file"]), esc(p[lang]), p.get("width", 1200), p.get("height", 900), p[lang]))
    if not real and ctx.mode == "preview":
        badge, lbl, note = PHOTO_SLOT[lang]
        for shot in shots:
            cards.append('<li><figure class="work-card is-placeholder"><div class="work-ph" role="img" aria-label="%s: %s"><span class="ph-badge">%s</span><span class="ph-shot">%s&nbsp;: %s</span></div><figcaption>%s</figcaption></figure></li>' % (
                badge, esc(shot), badge, lbl, shot, note))
    if cards:
        body = '<ul class="work-grid" role="list">%s</ul>' % "".join(cards)
        head_extra = ig
    else:
        # No real photos yet: send visitors to Instagram, where the owner posts work.
        head_extra = ""
        body = """<div class="ig-panel">
          <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1"/></svg>
          <div><h3>%s</h3><p>%s</p></div>
          <a class="btn btn-yellow" href="%s">%s</a>
        </div>""" % (C.SITE["instagram_handle"], ig_text, C.SITE["instagram"], "Voir sur Instagram" if lang == "fr" else "View on Instagram")
    return """    <section id="%s" class="section section-work" aria-labelledby="%s-title">
      <div class="container">
        <div class="section-head section-head-row">
          <h2 id="%s-title" class="section-title">%s</h2>
          %s
        </div>
        %s
      </div>
    </section>
""" % (section_id, section_id, section_id, title, head_extra, body)


def industries(ctx, keys, title=None):
    lang = ctx.lang
    title = title or ("Avec qui nous travaillons" if lang == "fr" else "Who we work with")
    items = "\n".join('          <li><h3>%s</h3><p>%s</p></li>' % C.INDUSTRIES[k][lang] for k in keys)
    intro = ("Des petits projets personnalisés aux commandes commerciales plus importantes, selon les exigences de production." if lang == "fr"
             else "From smaller custom projects to larger commercial orders, subject to production requirements.")
    return """    <section id="clientele" class="section section-alt" aria-labelledby="clientele-title">
      <div class="container">
        <div class="section-head">
          <h2 id="clientele-title" class="section-title">%s</h2>
          <p class="section-intro">%s</p>
        </div>
        <ul class="audiences" role="list">
%s
        </ul>
      </div>
    </section>
""" % (title, intro, items)


def process(ctx):
    if ctx.lang == "fr":
        steps = [("Envoyez votre demande", "Formulaire, appel ou texto. Joignez votre logo par courriel."),
                 ("Recevez votre soumission", "Nous recommandons les produits et la technique, puis vous envoyons la soumission."),
                 ("Approuvez la maquette", "La maquette visuelle est incluse et envoyée une fois la soumission approuvée. Un dépôt de 50&nbsp;% confirme la commande."),
                 ("Production et livraison", "Délai habituel de 10 à 15 jours ouvrables. Solde de 50&nbsp;% à la fin. Des frais de livraison peuvent s’appliquer.")]
        title = "Comment ça fonctionne"
    else:
        steps = [("Send your request", "Form, call or text. Email us your logo."),
                 ("Receive your quote", "We recommend the products and method, then send you a quote."),
                 ("Approve the mockup", "The visual mockup is included and sent once your quote is approved. A 50% deposit confirms the order."),
                 ("Production and delivery", "Typical turnaround of 10 to 15 business days. Remaining 50% on completion. Delivery fees may apply.")]
        title = "How it works"
    items = "\n".join('          <li><h3>%s</h3><p>%s</p></li>' % s for s in steps)
    return """    <section id="processus" class="section" aria-labelledby="processus-title">
      <div class="container">
        <div class="section-head">
          <h2 id="processus-title" class="section-title">%s</h2>
        </div>
        <ol class="steps">
%s
        </ol>
      </div>
    </section>
""" % (title, items)


def faq(ctx, keys, title=None, extra=None):
    lang = ctx.lang
    title = title or ("Questions fréquentes" if lang == "fr" else "Frequently asked questions")
    qa = [C.FAQ_BANK[k][lang] for k in keys] + (extra or [])
    items = "\n".join("""          <details>
            <summary>%s</summary>
            <p>%s</p>
          </details>""" % q for q in qa)
    return """    <section id="faq" class="section" aria-labelledby="faq-title">
      <div class="container faq-wrap">
        <h2 id="faq-title" class="section-title">%s</h2>
        <div class="faq">
%s
        </div>
      </div>
    </section>
""" % (title, items)


def quote_section(ctx, default_service=None):
    lang = ctx.lang
    fr = lang == "fr"
    f = C.FACTS[lang]
    phone = C.SITE["phone_fr"] if fr else C.SITE["phone_en"]
    opts = "\n".join('                  <option value="%s" data-key="%s"%s>%s</option>' % (
        esc(SVC[k][lang]["name"]), k, " selected" if k == default_service else "", SVC[k][lang]["name"]) for k in C.FORM_SERVICES)
    other_opt = "Autre / je ne sais pas" if fr else "Other / not sure"
    mail_subject = ("Visuel pour ma demande de soumission" if fr else "Artwork for my quote request")
    page_url = abs_url(ctx.cur)
    L = {
        "title": "Demandez votre soumission" if fr else "Request your quote",
        "intro": ("Appelez, textez ou remplissez le formulaire. Pas besoin de connaître le matériau, la technique ou le format de fichier&nbsp;: nous vous guidons."
                  if fr else "Call, text or fill in the form. You don’t need to know the material, method or file format: we’ll guide you."),
        "form_title": "Soumission gratuite" if fr else "Free quote",
        "form_intro": "Votre demande nous est envoyée directement." if fr else "Your request is sent to us directly.",
        "type": "Type de demande" if fr else "Request type", "n_type": "Type de demande" if fr else "Request type",
        "type_new": "Nouvelle demande" if fr else "New request", "type_re": "Recommande" if fr else "Reorder",
        "name": "Nom" if fr else "Name", "phone": "Téléphone" if fr else "Phone", "email": "Courriel" if fr else "Email",
        "service": "Service", "art": "Votre visuel" if fr else "Your artwork", "n_art": "Visuel" if fr else "Artwork",
        "art_opts": (["J’ai un fichier vectoriel (AI, EPS, SVG, PDF)", "J’ai un autre fichier (JPG, PNG…)", "J’ai besoin d’aide pour créer un design", "Pas encore de visuel"] if fr
                     else ["I have a vector file (AI, EPS, SVG, PDF)", "I have another file (JPG, PNG…)", "I need help creating a design", "No artwork yet"]),
        "details": "Détails du projet" if fr else "Project details", "n_details": "Détails" if fr else "Details",
        "details_ph": ("Produit, quantité, tailles, couleurs, date souhaitée. Pour une recommande, décrivez la commande précédente."
                       if fr else "Product, quantity, sizes, colours, date needed. For a reorder, describe the previous order."),
        "privacy": ("Vos renseignements servent uniquement à répondre à votre demande." if fr else "Your information is used only to respond to your request."),
        "policy": "Politique de confidentialité" if fr else "Privacy policy",
        "send": "Envoyer ma demande" if fr else "Send my request",
        "hp": "Ne pas remplir ce champ" if fr else "Leave this field empty",
        "lang_field": "Langue" if fr else "Language", "lang_value": "Français" if fr else "English",
        "page_field": "Page",
        "subject": "Nouveau lead - site Web All Things Printed" if fr else "New lead - All Things Printed website",
        "art_title": "Envoyer votre logo" if fr else "Sending your logo",
        "art_steps": (["Envoyez d’abord le formulaire.", "Écrivez-nous ensuite à " + C.SITE["email"] + " avec votre fichier en pièce jointe et votre nom en objet.",
                       "Idéal&nbsp;: fichier vectoriel (AI, EPS, SVG, PDF). Les autres fichiers peuvent être ajustés moyennant des frais."] if fr else
                      ["Send the form first.", "Then email " + C.SITE["email"] + " with your file attached and your name in the subject.",
                       "Best: a vector file (AI, EPS, SVG, PDF). Other files can be adjusted for a fee."]),
        "art_btn": "Envoyer mon logo par courriel" if fr else "Email my logo",
        "reorder": ("<strong>Déjà client&nbsp;?</strong> Choisissez «&nbsp;Recommande&nbsp;» et décrivez votre commande précédente."
                    if fr else "<strong>Already a customer?</strong> Choose “Reorder” and describe your previous order."),
    }
    rows = [("Téléphone" if fr else "Phone", '<a href="tel:%s">%s</a>' % (C.SITE["phone_e164"], phone)),
            ("Texto" if fr else "Text", '<a href="sms:%s">%s</a>' % (C.SITE["phone_e164"], phone)),
            ("Courriel" if fr else "Email", '<a href="mailto:%s">%s</a>' % (C.SITE["email"], C.SITE["email"])),
            ("Territoire" if fr else "Service area", f["area"]),
            ("Heures" if fr else "Hours", f["hours"]),
            ("Instagram", '<a href="%s">%s</a>' % (C.SITE["instagram"], C.SITE["instagram_handle"]))]
    contact = "\n".join('            <div><dt>%s</dt><dd>%s</dd></div>' % r for r in rows)
    art_steps = "\n".join("              <li>%s</li>" % s for s in L["art_steps"])
    art_opts = "\n".join('                <option>%s</option>' % o for o in L["art_opts"])
    from urllib.parse import quote as q
    mailto = "mailto:%s?subject=%s" % (C.SITE["email"], q(mail_subject))
    return """    <section id="soumission" class="section section-dark" aria-labelledby="soumission-title">
      <div class="container contact">
        <div class="contact-info">
          <h2 id="soumission-title" class="section-title">%(title)s</h2>
          <p>%(intro)s</p>
          <dl class="contact-list">
%(contact)s
          </dl>
          <div class="contact-buttons">
            <a class="btn btn-outline-light" href="tel:%(tel)s">%(call)s</a>
            <a class="btn btn-outline-light" href="sms:%(tel)s">%(textb)s</a>
          </div>
          <div class="artwork-box">
            <h3>%(art_title)s</h3>
            <ol>
%(art_steps)s
            </ol>
            <a class="btn btn-sm btn-yellow" href="%(mailto)s">%(art_btn)s</a>
          </div>
        </div>

        <div class="quote-card">
          <span class="crop crop-tl" aria-hidden="true"></span>
          <span class="crop crop-tr" aria-hidden="true"></span>
          <span class="crop crop-bl" aria-hidden="true"></span>
          <span class="crop crop-br" aria-hidden="true"></span>
          <h3>%(form_title)s</h3>
          <p class="form-intro">%(form_intro)s</p>
          <form id="lead-form" class="quote-form" action="%(action)s" method="POST" novalidate%(preview_attr)s>
            <input type="hidden" name="_subject" value="%(subject)s">
            <input type="hidden" name="_cc" value="%(cc)s">
            <input type="hidden" name="_template" value="table">
            <input type="hidden" name="_captcha" value="false">
            <input type="hidden" name="%(lang_field)s" value="%(lang_value)s">
            <input type="hidden" name="%(page_field)s" value="%(page_url)s">
            <div class="hp-field" aria-hidden="true">
              <label for="q-honey">%(hp)s</label>
              <input id="q-honey" name="_honey" type="text" tabindex="-1" autocomplete="off">
            </div>
            <fieldset class="field segmented">
              <legend>%(type)s</legend>
              <label><input type="radio" name="%(n_type)s" value="%(type_new)s" checked> <span>%(type_new)s</span></label>
              <label><input type="radio" name="%(n_type)s" value="%(type_re)s"> <span>%(type_re)s</span></label>
            </fieldset>
            <div class="field">
              <label for="q-name">%(name)s <span aria-hidden="true">*</span></label>
              <input id="q-name" name="%(name)s" type="text" autocomplete="name" required>
            </div>
            <div class="field-row">
              <div class="field">
                <label for="q-phone">%(phone)s <span aria-hidden="true">*</span></label>
                <input id="q-phone" name="%(phone)s" type="tel" autocomplete="tel" required>
              </div>
              <div class="field">
                <label for="q-email">%(email)s <span aria-hidden="true">*</span></label>
                <input id="q-email" name="email" type="email" autocomplete="email" required>
              </div>
            </div>
            <div class="field">
              <label for="q-service">%(service)s</label>
              <select id="q-service" name="Service">
%(opts)s
                <option value="%(other_opt)s" data-key="other">%(other_opt)s</option>
              </select>
            </div>
            <div class="field">
              <label for="q-artwork">%(art)s</label>
              <select id="q-artwork" name="%(n_art)s">
%(art_opts)s
              </select>
            </div>
            <div class="field">
              <label for="q-details">%(details)s <span aria-hidden="true">*</span></label>
              <textarea id="q-details" name="%(n_details)s" rows="5" required placeholder="%(details_ph)s"></textarea>
            </div>
            <p class="hint">%(reorder)s</p>
            <p class="hint">%(privacy)s <a href="%(policy_href)s">%(policy)s</a></p>
            <div id="form-status" class="form-status" role="status" aria-live="polite"></div>
            <button class="btn btn-primary btn-lg btn-block" type="submit">%(send)s</button>
          </form>
        </div>
      </div>
    </section>
""" % dict(L, contact=contact, tel=C.SITE["phone_e164"], call=T[lang]["call_long"], textb=T[lang]["text_long"],
           art_steps=art_steps, mailto=esc(mailto), action=C.SITE["form_action"], cc=C.SITE["form_sms_cc"],
           page_url=page_url, opts=opts, other_opt=other_opt, art_opts=art_opts, policy_href=ctx.page("privacy"),
           preview_attr=' data-preview="true"' if ctx.mode == "preview" else "")


# ------------------------------------------------------------- schema -----
def ld_business(lang):
    d = C.SITE["domain"]
    return {
        "@context": "https://schema.org", "@type": "LocalBusiness", "@id": d + "/#business",
        "name": "All Things Printed",
        "slogan": T[lang]["tagline"],
        "url": d + ("/" if lang == "fr" else "/en/"),
        "logo": d + "/assets/images/logo.png", "image": d + "/assets/images/og-image.jpg",
        "telephone": "+1-514-815-1829", "email": C.SITE["email"],
        "address": {"@type": "PostalAddress", "addressRegion": "QC", "addressCountry": "CA"},
        "areaServed": {"@type": "AdministrativeArea", "name": "Grand Montréal" if lang == "fr" else "Greater Montreal"},
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification",
                                       "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
                                       "opens": "09:00", "closes": "17:00"}],
        "sameAs": [C.SITE["instagram"]],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Services", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s[lang]["name"],
                                                "url": abs_url(FILE_OF[("svc:" + s["key"], lang)])}} for s in C.SERVICES]},
    }


def ld_website(lang):
    d = C.SITE["domain"]
    return {"@context": "https://schema.org", "@type": "WebSite", "@id": d + "/#website", "name": "All Things Printed",
            "url": d + "/", "inLanguage": ["fr-CA", "en-CA"], "publisher": {"@id": d + "/#business"}}


def ld_service(s, lang):
    d = s[lang]
    url = abs_url(FILE_OF[("svc:" + s["key"], lang)])
    return [
        {"@context": "https://schema.org", "@type": "Service", "name": d["name"], "serviceType": d["name"],
         "description": strip_tags(d["lead"]), "url": url, "inLanguage": "fr-CA" if lang == "fr" else "en-CA",
         "areaServed": {"@type": "AdministrativeArea", "name": C.FACTS[lang]["area"]},
         "provider": {"@id": C.SITE["domain"] + "/#business"}},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": T[lang]["home"], "item": abs_url(FILE_OF[("home", lang)])},
            {"@type": "ListItem", "position": 2, "name": T[lang]["services"], "item": abs_url(FILE_OF[("home", lang)]) + "#services"},
            {"@type": "ListItem", "position": 3, "name": d["name"], "item": url}]},
    ]


# -------------------------------------------------------------- pages -----
def render_home(ctx):
    lang = ctx.lang
    fr = lang == "fr"
    title = "Impression personnalisée à Montréal | All Things Printed" if fr else "Custom Printing in Montreal | All Things Printed"
    desc = ("T-shirts, kangourous, broderie, lettrage vinyle, enseignes et produits promotionnels pour entreprises et événements du Grand Montréal. Soumission gratuite."
            if fr else "Custom T-shirts, hoodies, embroidery, vinyl lettering, signage and promotional products for Greater Montreal businesses and events. Free quote.")
    slogan = "Vos idées, imprimées avec audace." if fr else "Your ideas, printed bold."
    kicker = "Impression personnalisée · Grand Montréal" if fr else "Custom printing · Greater Montreal"
    lead = ("Vêtements personnalisés, broderie, lettrage en vinyle, enseignes, produits promotionnels et impression pour événements, pour les entreprises, les organismes et les particuliers."
            if fr else "Custom apparel, embroidery, vinyl lettering, signage, promotional products and event printing for businesses, organizations and individuals.")
    about = ("All Things Printed est une entreprise d’impression personnalisée et d’image de marque du Grand Montréal. Nous transformons vos logos, vos designs et vos idées en produits de qualité.",
             "Nous travaillons avec des entreprises de toutes tailles, des entrepreneurs locaux aux organisations établies, ainsi qu’avec les particuliers. Chaque produit imprimé représente le client qui se trouve derrière&nbsp;: nous misons sur la qualité, le souci du détail et une présentation professionnelle, et nous vous aidons à choisir les bons matériaux et les bonnes techniques.")
    if not fr:
        about = ("All Things Printed is a custom printing and branding company in Greater Montreal. We turn your logos, designs and ideas into quality products.",
                 "We work with businesses of all sizes, from local entrepreneurs to established organizations, and with individuals. Every printed piece represents the customer behind it: we focus on quality, attention to detail and professional presentation, and we help you choose the right materials and methods.")
    creds = (["Une seule adresse pour les vêtements, le vinyle, les enseignes, les articles promotionnels et les événements",
              "Maquette visuelle incluse dans le prix", "Aide à la préparation et à la vectorisation de votre logo", "Dépôt de 50&nbsp;%, solde à la fin"] if fr else
             ["One shop for apparel, vinyl, signage, promotional items and events", "Visual mockup included in the price",
              "Help preparing and vectorizing your logo", "50% deposit, balance on completion"])
    logo = ('<picture><source type="image/webp" srcset="%s 380w, %s 760w" sizes="(max-width: 760px) 70vw, 360px"><img class="about-logo" src="%s" alt="%s" width="760" height="450" loading="lazy"></picture>' % (
        ctx.asset("assets/images/logo-sm.webp"), ctx.asset("assets/images/logo.webp"), ctx.asset("assets/images/logo.png"),
        "Logo d’ATP Inc. All Things Printed" if fr else "ATP Inc. All Things Printed logo"))
    body = []
    body.append(head(ctx, title, desc, "home", [ld_business(lang), ld_website(lang)]))
    body.append(header(ctx, "home"))
    body.append("""  <main id="main">
    <section id="top" class="hero" aria-labelledby="hero-title">
      <div class="container">
        <div class="proof-sheet">
          <span class="crop crop-tl" aria-hidden="true"></span>
          <span class="crop crop-tr" aria-hidden="true"></span>
          <span class="crop crop-bl" aria-hidden="true"></span>
          <span class="crop crop-br" aria-hidden="true"></span>
          <div class="hero-grid">
            <div class="hero-copy">
              <h1 id="hero-title"><span class="eyebrow">%(kicker)s</span> %(slogan)s</h1>
              <p class="lead"><strong class="tagline">%(tagline)s</strong> %(lead)s</p>
              <div class="hero-actions">
                <a class="btn btn-primary btn-lg" href="#soumission">%(cta)s</a>
                <a class="btn btn-outline btn-lg" href="tel:%(tel)s">%(call)s</a>
              </div>
              %(chips)s
            </div>
            %(art)s
          </div>
          <div class="colour-bar" aria-hidden="true">
            <span class="cb-c"></span><span class="cb-m"></span><span class="cb-y"></span><span class="cb-k"></span>
            <span class="cb-cm"></span><span class="cb-my"></span><span class="cb-cy"></span>
            <span class="cb-t1"></span><span class="cb-t2"></span><span class="cb-t3"></span>
            <span class="reg-mark"></span>
          </div>
        </div>
      </div>
    </section>
%(seasonal)s
    <section id="services" class="section" aria-labelledby="services-title">
      <div class="container">
        <div class="section-head">
          <h2 id="services-title" class="section-title">%(svc_title)s</h2>
          <p class="section-intro">%(svc_intro)s</p>
        </div>
        %(cards)s
      </div>
    </section>
""" % {"kicker": kicker, "slogan": overprint(slogan), "tagline": T[lang]["tagline"], "lead": lead, "cta": T[lang]["cta_long"],
       "tel": C.SITE["phone_e164"], "call": T[lang]["call_long"], "chips": chips(ctx), "art": hero_art(ctx, "shirt"),
       "seasonal": seasonal(ctx), "svc_title": "Nos services" if fr else "Our services",
       "svc_intro": ("Choisissez un service pour voir les options, les questions fréquentes et demander une soumission." if fr
                     else "Choose a service to see the options, common questions and request a quote."),
       "cards": service_cards(ctx, [s["key"] for s in C.SERVICES])})
    body.append(garment_rail(ctx))
    body.append(portfolio(ctx, C.HOME_SHOTS[lang]))
    body.append(industries(ctx, list(C.INDUSTRIES)))
    body.append(process(ctx))
    body.append("""    <section id="apropos" class="section section-alt" aria-labelledby="apropos-title">
      <div class="container about">
        <div class="about-head">
          <h2 id="apropos-title" class="section-title">%s</h2>
          %s
        </div>
        <div class="about-copy">
          <p class="about-lede">%s</p>
          <p>%s</p>
          <ul class="check-list" role="list">%s</ul>
          <p class="about-tagline">%s</p>
        </div>
      </div>
    </section>
""" % ("À propos" if fr else "About us", logo, about[0], about[1], "".join("<li>%s</li>" % c for c in creds), T[lang]["tagline"]))
    body.append(faq(ctx, ["turnaround", "files", "mockup", "payment", "delivery", "artwork", "reorder"]))
    body.append(quote_section(ctx))
    body.append("  </main>\n\n")
    body.append(footer(ctx, "home"))
    body.append(sticky_bar(ctx, True))
    body.append(cookie_and_scripts(ctx))
    return "".join(body)


def cookie_and_scripts(ctx):
    return scripts(ctx)


def render_service(ctx, s):
    lang = ctx.lang
    fr = lang == "fr"
    d = s[lang]
    pid = "svc:" + s["key"]
    body = [head(ctx, d["title"], d["desc"], pid, ld_service(s, lang)), header(ctx, pid)]
    intro = "\n".join("          <p>%s</p>" % p for p in d["intro"])
    options = "".join("<li>%s</li>" % o for o in d["options"])
    apps = "".join("<li>%s</li>" % a for a in d["apps"])
    art = hero_art(ctx, "shirt") if s["key"] == "apparel" else hero_art(ctx, s["icon"])
    crumbs = '<nav class="breadcrumb" aria-label="%s"><ol><li><a href="%s">%s</a></li><li><a href="%s">%s</a></li><li aria-current="page">%s</li></ol></nav>' % (
        "Fil d’Ariane" if fr else "Breadcrumb", ctx.page("home"), T[lang]["home"], ctx.page("home", anchor="services"), T[lang]["services"], d["name"])
    body.append("""  <main id="main">
    <section class="hero hero-service" aria-labelledby="hero-title">
      <div class="container">
        <div class="proof-sheet">
          <span class="crop crop-tl" aria-hidden="true"></span>
          <span class="crop crop-tr" aria-hidden="true"></span>
          <span class="crop crop-bl" aria-hidden="true"></span>
          <span class="crop crop-br" aria-hidden="true"></span>
          %(crumbs)s
          <div class="hero-grid">
            <div class="hero-copy">
              <h1 id="hero-title" class="service-h1">%(h1)s</h1>
              <p class="lead">%(lead)s</p>
              <div class="hero-actions">
                <a class="btn btn-primary btn-lg" href="#soumission" data-service="%(key)s">%(cta)s</a>
                <a class="btn btn-outline btn-lg" href="tel:%(tel)s">%(call)s</a>
              </div>
              %(chips)s
            </div>
            %(art)s
          </div>
          <div class="colour-bar" aria-hidden="true">
            <span class="cb-c"></span><span class="cb-m"></span><span class="cb-y"></span><span class="cb-k"></span>
            <span class="cb-cm"></span><span class="cb-my"></span><span class="cb-cy"></span>
            <span class="cb-t1"></span><span class="cb-t2"></span><span class="cb-t3"></span>
            <span class="reg-mark"></span>
          </div>
        </div>
      </div>
    </section>

    <section id="details" class="section" aria-labelledby="details-title">
      <div class="container svc-detail">
        <div class="svc-detail-copy">
          <h2 id="details-title" class="section-title">%(about_title)s</h2>
%(intro)s
          <a class="btn btn-primary" href="#soumission" data-service="%(key)s">%(cta_svc)s</a>
        </div>
        <div class="svc-lists">
          <div class="svc-list-card ink-%(ink)s">
            <h3>%(opt_title)s</h3>
            <ul class="check-list" role="list">%(options)s</ul>
          </div>
          <div class="svc-list-card">
            <h3>%(apps_title)s</h3>
            <ul class="dot-list" role="list">%(apps)s</ul>
          </div>
        </div>
      </div>
    </section>
""" % {"crumbs": crumbs, "h1": overprint(d["h1"], "overprint overprint-sm"), "lead": d["lead"], "key": s["key"], "cta": T[lang]["cta_long"],
       "tel": C.SITE["phone_e164"], "call": T[lang]["call_long"], "chips": chips(ctx), "art": art,
       "about_title": ("Le service en bref" if fr else "The service at a glance"), "intro": intro,
       "cta_svc": "Obtenir une soumission pour ce service" if fr else "Get a quote for this service",
       "ink": s["ink"], "opt_title": d["options_title"], "options": options, "apps_title": d["apps_title"], "apps": apps})
    if s.get("garments"):
        body.append(garment_rail(ctx))
    body.append(portfolio(ctx, s["shots"][lang], service=s["key"], title=("Réalisations" if fr else "Our work")))
    body.append(industries(ctx, s["industries"], title=("Pour qui" if fr else "Who it’s for")))
    body.append(faq(ctx, s["faq"] + ["payment"]))
    body.append("""    <section class="section section-alt" aria-labelledby="related-title">
      <div class="container">
        <div class="section-head">
          <h2 id="related-title" class="section-title">%s</h2>
        </div>
        %s
      </div>
    </section>
""" % ("Services complémentaires" if fr else "Related services", service_cards(ctx, s["related"], compact=True)))
    body.append(quote_section(ctx, default_service=s["key"]))
    body.append("  </main>\n\n")
    body.append(footer(ctx, pid))
    body.append(sticky_bar(ctx, True))
    body.append(scripts(ctx))
    return "".join(body)


def render_privacy(ctx):
    lang = ctx.lang
    fr = lang == "fr"
    with open(os.path.join(ROOT, "tools", "policy_%s.html" % lang), encoding="utf-8") as fh:
        frag = fh.read()
    title = "Politique de confidentialité | All Things Printed" if fr else "Privacy policy | All Things Printed"
    desc = ("Comment All Things Printed recueille, utilise et protège vos renseignements personnels, et comment exercer vos droits selon la Loi 25 du Québec." if fr
            else "How All Things Printed collects, uses and protects your personal information, and how to exercise your rights under Quebec’s Law 25.")
    out = [head(ctx, title, desc, "privacy"), header(ctx, "privacy")]
    out.append("""  <main id="main" class="section policy">
    <div class="container policy-inner">
      <p><a href="%s">&larr; %s</a></p>
      %s
    </div>
  </main>

""" % (ctx.page("home"), "Retour à l’accueil" if fr else "Back to home", frag))
    out.append(footer(ctx, "privacy"))
    out.append(sticky_bar(ctx, False))
    out.append(scripts(ctx))
    return "".join(out)


def render_404(ctx):
    out = [head(ctx, "Page introuvable / Page not found | All Things Printed",
                "Cette page n’existe pas. This page does not exist.", None, noindex=True)]
    out.append(header(ctx, None))
    out.append("""  <main id="main" class="section policy">
    <div class="container policy-inner not-found">
      <p class="eyebrow-dark">404</p>
      <h1 class="page-title">Page introuvable</h1>
      <p>Cette page n’existe pas ou a été déplacée.</p>
      <p><a class="btn btn-primary" href="%s">Retour à l’accueil</a></p>
      <hr>
      <p lang="en-CA"><strong>Page not found.</strong> This page doesn’t exist or has moved. <a href="%s">Go to the English home page</a>.</p>
    </div>
  </main>

""" % (ctx.page("home", "fr"), ctx.page("home", "en")))
    out.append(footer(ctx, None))
    out.append(sticky_bar(ctx, False))
    out.append(scripts(ctx))
    return "".join(out)


# ------------------------------------------------------------- extras -----
def sitemap():
    rows = []
    for p in PAGES:
        for l in LANGS:
            alts = "".join('\n    <xhtml:link rel="alternate" hreflang="%s" href="%s"/>' % (h, abs_url(p["file"][ll]))
                           for h, ll in (("fr-CA", "fr"), ("en-CA", "en"), ("x-default", "fr")))
            rows.append("  <url>\n    <loc>%s</loc>%s\n  </url>" % (abs_url(p["file"][l]), alts))
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
            'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n%s\n</urlset>\n' % "\n".join(rows))


def robots():
    return "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % C.SITE["domain"]


def write(base, rel, text):
    path = os.path.join(base, rel)
    os.makedirs(os.path.dirname(path) or base, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def build(base, mode):
    fingerprint()
    out = []
    for p in PAGES:
        for l in LANGS:
            f = p["file"][l]
            ctx = Ctx(f, l, mode)
            if p["id"] == "home":
                txt = render_home(ctx)
            elif p["id"] == "privacy":
                txt = render_privacy(ctx)
            else:
                txt = render_service(ctx, SVC[p["id"][4:]])
            write(base, f, txt)
            out.append(f)
    write(base, "404.html", render_404(Ctx("404.html", "fr", mode)))
    out.append("404.html")
    write(base, "sitemap.xml", sitemap())
    write(base, "robots.txt", robots())
    return out


def main():
    if len(sys.argv) >= 3 and sys.argv[1] == "--preview":
        dest = os.path.abspath(sys.argv[2])
        if os.path.exists(dest):
            shutil.rmtree(dest)
        for d in ("css", "js", "assets"):
            shutil.copytree(os.path.join(ROOT, d), os.path.join(dest, d))
        files = build(dest, "preview")
        print("preview: %d pages in %s" % (len(files), dest))
    else:
        files = build(ROOT, "production")
        print("production: %d pages" % len(files))


if __name__ == "__main__":
    main()
