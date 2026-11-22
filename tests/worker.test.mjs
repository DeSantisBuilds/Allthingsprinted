// Run with: npm test
import test from "node:test";
import assert from "node:assert/strict";
import worker, { handleQuote } from "../worker/index.js";

const env = { TURNSTILE_SECRET: "s", RESEND_API_KEY: "k", QUOTE_TO: "info@allthingsprinted.ca",
  QUOTE_FROM: "ATP <soumissions@allthingsprinted.ca>", ALLOWED_ORIGINS: "https://desantisbuilds.github.io" };

function mockFetch({ captcha = true, send = true } = {}) {
  const calls = [];
  globalThis.fetch = async (url, init) => {
    calls.push({ url: String(url), init });
    if (String(url).includes("siteverify")) return new Response(JSON.stringify({ success: captcha }));
    if (String(url).includes("resend")) return new Response("{}", { status: send ? 200 : 500 });
    throw new Error("unexpected " + url);
  };
  return calls;
}
function form(extra = {}, files = []) {
  const fd = new FormData();
  const base = { name: "Marie", email: "marie@example.com", details: "50 t-shirts", service: "Impression", lang: "fr-CA",
    "cf-turnstile-response": "tok", ...extra };
  for (const [k, v] of Object.entries(base)) fd.append(k, v);
  for (const f of files) fd.append("artwork_files", f);
  return fd;
}
const req = (fd, headers = {}) => new Request("https://x/api/quote", { method: "POST", body: fd, headers });

test("valid request is verified and emailed with attachment", async () => {
  const calls = mockFetch();
  const fd = form({ locations: "Devant" }, [new File([new Uint8Array([1, 2, 3])], "logo.pdf")]);
  fd.append("locations", "Dos");
  const r = await handleQuote(req(fd, { "CF-Connecting-IP": "1.2.3.4" }), env);
  assert.equal(r.status, 200);
  assert.equal(calls.length, 2);
  const mail = JSON.parse(calls[1].init.body);
  assert.deepEqual(mail.to, ["info@allthingsprinted.ca"]);
  assert.equal(mail.reply_to, "marie@example.com");
  assert.match(mail.subject, /^Demande de soumission/);
  assert.match(mail.text, /Emplacements d'impression: Devant, Dos/);
  assert.equal(mail.attachments[0].filename, "logo.pdf");
  assert.equal(mail.attachments[0].content, "AQID");
});
test("failed captcha is rejected and nothing is emailed", async () => {
  const calls = mockFetch({ captcha: false });
  const r = await handleQuote(req(form()), env);
  assert.equal(r.status, 400); assert.equal((await r.json()).error, "captcha");
  assert.equal(calls.length, 1);
});
test("missing token is rejected without calling Cloudflare", async () => {
  const calls = mockFetch();
  const r = await handleQuote(req(form({ "cf-turnstile-response": "" })), env);
  assert.equal((await r.json()).error, "captcha"); assert.equal(calls.length, 0);
});
test("honeypot silently drops bots", async () => {
  const calls = mockFetch();
  const r = await handleQuote(req(form({ website: "spam.example" })), env);
  assert.equal(r.status, 200); assert.equal(calls.length, 0);
});
test("invalid email is rejected", async () => {
  mockFetch();
  const r = await handleQuote(req(form({ email: "nope" })), env);
  assert.equal((await r.json()).error, "invalid");
});
test("disallowed file type is rejected", async () => {
  mockFetch();
  const r = await handleQuote(req(form({}, [new File(["x"], "virus.exe")])), env);
  assert.equal((await r.json()).error, "file_type");
});
test("too many files are rejected", async () => {
  mockFetch();
  const files = Array.from({ length: 6 }, (_, i) => new File(["x"], `a${i}.png`));
  const r = await handleQuote(req(form({}, files)), env);
  assert.equal((await r.json()).error, "too_many_files");
});
test("oversized files are rejected", async () => {
  mockFetch();
  const big = new File([new Uint8Array(16 * 1024 * 1024)], "big.png");
  const r = await handleQuote(req(form({}, [big])), env);
  assert.equal((await r.json()).error, "file_size");
});
test("missing secrets report not_configured", async () => {
  mockFetch();
  const r = await handleQuote(req(form()), { ...env, RESEND_API_KEY: "" });
  assert.equal(r.status, 503); assert.equal((await r.json()).error, "not_configured");
});
test("email provider failure is reported", async () => {
  mockFetch({ send: false });
  const r = await handleQuote(req(form()), env);
  assert.equal(r.status, 502); assert.equal((await r.json()).error, "send");
});
test("GET is refused; CORS only for allowed origins", async () => {
  const g = await handleQuote(new Request("https://x/api/quote"), env);
  assert.equal(g.status, 405);
  const ok = await handleQuote(new Request("https://x/api/quote", { method: "OPTIONS", headers: { Origin: "https://desantisbuilds.github.io" } }), env);
  assert.equal(ok.headers.get("Access-Control-Allow-Origin"), "https://desantisbuilds.github.io");
  const bad = await handleQuote(new Request("https://x/api/quote", { method: "OPTIONS", headers: { Origin: "https://evil.example" } }), env);
  assert.equal(bad.headers.get("Access-Control-Allow-Origin"), null);
});
test("other paths are served from static assets", async () => {
  const r = await worker.fetch(new Request("https://x/en/"), { ASSETS: { fetch: async () => new Response("page") } });
  assert.equal(await r.text(), "page");
});
