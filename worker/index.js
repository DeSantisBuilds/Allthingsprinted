/**
 * All Things Printed — Cloudflare Worker
 *
 * 1. Serves the static website (index.html, en/, css/, js/, assets/).
 * 2. Handles quote requests at POST /api/quote:
 *    - rejects bots with a hidden "honeypot" field,
 *    - verifies the Cloudflare Turnstile token with Cloudflare (server side),
 *    - checks the fields and the uploaded artwork files,
 *    - emails the request, with the files attached, through Resend.
 *
 * Settings (see README, "Online quote form"):
 *   Secrets (never commit these): TURNSTILE_SECRET, RESEND_API_KEY
 *   Variables (wrangler.toml):     QUOTE_TO, QUOTE_FROM, ALLOWED_ORIGINS
 */

const MAX_FILES = 5;
const MAX_TOTAL_BYTES = 15 * 1024 * 1024; // 15 MB for all files together
const ALLOWED_EXT = ["png", "jpg", "jpeg", "pdf", "svg", "ai", "eps", "psd", "tif", "tiff", "webp"];
const LIMITS = { name: 120, email: 200, phone: 40, service: 120, product: 120, quantity: 60,
  needed_by: 20, sizes: 300, colours: 300, locations: 200, artwork: 120, details: 5000, lang: 5 };

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/api/quote") return handleQuote(request, env);
    if (env.ASSETS) return env.ASSETS.fetch(request);
    return new Response("Not found", { status: 404 });
  },
};

function corsHeaders(request, env) {
  const origin = request.headers.get("Origin");
  const allowed = (env.ALLOWED_ORIGINS || "").split(",").map((s) => s.trim()).filter(Boolean);
  if (origin && allowed.includes(origin)) {
    return { "Access-Control-Allow-Origin": origin, "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type", "Vary": "Origin" };
  }
  return {};
}

function json(body, status, extra) {
  return new Response(JSON.stringify(body), {
    status, headers: { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store", ...extra },
  });
}

export async function handleQuote(request, env) {
  const cors = corsHeaders(request, env);
  if (request.method === "OPTIONS") return new Response(null, { status: 204, headers: cors });
  if (request.method !== "POST") return json({ ok: false, error: "method" }, 405, cors);
  if (!env.TURNSTILE_SECRET || !env.RESEND_API_KEY || !env.QUOTE_TO || !env.QUOTE_FROM) {
    return json({ ok: false, error: "not_configured" }, 503, cors);
  }

  let form;
  try { form = await request.formData(); } catch { return json({ ok: false, error: "bad_request" }, 400, cors); }

  // Honeypot: real visitors never see or fill this field.
  if (String(form.get("website") || "").trim() !== "") return json({ ok: true }, 200, cors);

  // Turnstile check (must happen on the server; the widget alone does not stop bots).
  const token = String(form.get("cf-turnstile-response") || "");
  if (!token) return json({ ok: false, error: "captcha" }, 400, cors);
  const verify = new FormData();
  verify.append("secret", env.TURNSTILE_SECRET);
  verify.append("response", token);
  const ip = request.headers.get("CF-Connecting-IP");
  if (ip) verify.append("remoteip", ip);
  let outcome;
  try {
    const r = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", { method: "POST", body: verify });
    outcome = await r.json();
  } catch { return json({ ok: false, error: "captcha_unavailable" }, 502, cors); }
  if (!outcome || !outcome.success) return json({ ok: false, error: "captcha" }, 400, cors);

  // Fields
  const f = {};
  for (const key of Object.keys(LIMITS)) {
    const value = key === "locations" ? form.getAll("locations").map(String).join(", ") : String(form.get(key) || "");
    f[key] = value.trim().slice(0, LIMITS[key]);
  }
  if (!f.name || !f.details || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(f.email)) {
    return json({ ok: false, error: "invalid" }, 400, cors);
  }

  // Files
  const files = form.getAll("artwork_files").filter((x) => x && typeof x === "object" && x.size > 0);
  if (files.length > MAX_FILES) return json({ ok: false, error: "too_many_files" }, 400, cors);
  let total = 0;
  const attachments = [];
  for (const file of files) {
    const ext = String(file.name || "").split(".").pop().toLowerCase();
    if (!ALLOWED_EXT.includes(ext)) return json({ ok: false, error: "file_type" }, 400, cors);
    total += file.size;
    if (total > MAX_TOTAL_BYTES) return json({ ok: false, error: "file_size" }, 400, cors);
    attachments.push({ filename: safeName(file.name), content: toBase64(await file.arrayBuffer()) });
  }

  const fr = f.lang.startsWith("fr");
  const L = fr
    ? { name: "Nom", email: "Courriel", phone: "Téléphone", service: "Service", product: "Produit", quantity: "Quantité approx.",
        needed_by: "Date souhaitée", sizes: "Tailles", colours: "Couleurs", locations: "Emplacements d'impression",
        artwork: "Visuel", files: "Fichiers joints", details: "Détails du projet", subject: "Demande de soumission" }
    : { name: "Name", email: "Email", phone: "Phone", service: "Service", product: "Product", quantity: "Approx. quantity",
        needed_by: "Needed by", sizes: "Sizes", colours: "Colours", locations: "Print locations",
        artwork: "Artwork", files: "Attached files", details: "Project details", subject: "Quote request" };
  const rows = ["name", "email", "phone", "service", "product", "quantity", "needed_by", "sizes", "colours", "locations", "artwork"]
    .map((k) => `${L[k]}: ${f[k] || "-"}`);
  rows.push(`${L.files}: ${attachments.length ? attachments.map((a) => a.filename).join(", ") : "-"}`);
  const text = [
    rows.join("\n"), "", `${L.details}:`, f.details, "",
    `— ${fr ? "Envoyé depuis le formulaire du site (français)" : "Sent from the website form (English)"}`,
  ].join("\n");

  let sent;
  try {
    sent = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: { "Authorization": `Bearer ${env.RESEND_API_KEY}`, "Content-Type": "application/json" },
      body: JSON.stringify({
        from: env.QUOTE_FROM,
        to: env.QUOTE_TO.split(",").map((s) => s.trim()),
        reply_to: f.email,
        subject: `${L.subject}: ${f.service || "-"} - ${f.name}`.slice(0, 200),
        text,
        attachments,
      }),
    });
  } catch { return json({ ok: false, error: "send" }, 502, cors); }
  if (!sent.ok) return json({ ok: false, error: "send" }, 502, cors);
  return json({ ok: true }, 200, cors);
}

function safeName(name) {
  const cleaned = String(name || "file").replace(/[\\/:*?"<>|\r\n]+/g, "_").slice(-120);
  return cleaned || "file";
}

function toBase64(buffer) {
  const bytes = new Uint8Array(buffer);
  let binary = "";
  const chunk = 0x8000;
  for (let i = 0; i < bytes.length; i += chunk) binary += String.fromCharCode.apply(null, bytes.subarray(i, i + chunk));
  return btoa(binary);
}
