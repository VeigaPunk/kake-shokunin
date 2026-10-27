# SentinelSources

Safety review of the C3 evidence surface, round 58, 2026-10-26. Read-only: retained bodies
`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-58/sources/{S423,S424}.html` + `receipts.json`,
` .../round-58/fetch_sources.py`, and the planned entry/recheck commands in
`.../round-58/w1-spec.json` / `w1-dispatch.json`. Lane git read-only (`git show fff3eea:…`). No file in the
lane was modified except this report; scratch lived in `/fast/scratch/hyaku/kake-r58/SentinelSources`.

## FINDINGS:

**F1 — MEDIUM (evidence integrity, not secrecy). The overwrite refusal is keyed on `receipts.json` alone.**
`fetch_sources.py:7` refuses only when `<dir>/receipts.json` exists; `:12` writes `S423.html`/`S424.html`
unconditionally. A dir that already holds retained bodies but no receipts (interrupted run, pre-populated dir,
stale copy) is silently overwritten — demonstrated with a stubbed `curl` on PATH: run 1 wrote both bodies +
receipts; run 2 exited 1 with the usage message; run 3 into a dir containing `ORIGINAL-RETAINED-BODY` as
`S423.html` exited 0 and replaced it (`STUB-BODY-…`). Impact: the sha256 pin is written *after* the bytes, so a
replacement body cannot be detected by the receipts it invalidates; a later "verified" recheck then attests the
replacement. Smallest remediation: refuse when any `*.html` exists in the target dir, or write each receipt
immediately after its own fetch (`os.O_EXCL`).

**F2 — LOW (provenance blind spot). Redirects are followed, the effective URL is not recorded.**
`fetch_sources.py:12` uses `-sL` and `-w "%{http_code}"` only; `:17` stores `url`, `httpStatus`, bytes, sha256,
`fetchedAt`, UA — no `%{url_effective}`, no `%{content_type}`, no `--proto`. Checked live today (2 GETs):
`code=200 redirects=0 final=<requested url>` for both rows, so nothing leaks today; a future off-host redirect
(e.g. to a login/consent page) would still be receipted as HTTP 200 against the original URL. Remediation:
`-w '%{http_code} %{url_effective} %{content_type}'`, add `--proto '=https'`.

**F3 — LOW (evidence). Full-body bytes are not stable across fetches; the article text nodes are.**
Fresh anonymous fetch today, same flags as the script: live sha256 `ee5f8b2b…` (S423, 29007 B) and `7f91b990…`
(S424, 22476 B) differ from the pinned `8b8aef60…` / `3ef1275b…` (byte counts identical), while
`c58_quote_truth.text_segments` is node-for-node identical retained vs live (S423 155/155, S424 30/30).
Consequence for safety review: a recheck that pins full-body sha256 will false-alarm; the `grep -F -c` shape is
the correct one. (Stability is a sibling seat's claim — stated here only as the fact my review turns on.)

**F4 — MEDIUM (latent command-injection surface in future rechecks). Page-derived text is embedded in a shell
command.** The stored form is `curl -fsSL --compressed '<url>' | grep -F -c '<quote>'` (w1-spec items 0/1/2/3/…).
The quote comes from third-party page text; a `'` inside it closes the single-quoted string and the remainder is
re-parsed by the shell, so `;`, `$(…)`, backticks or `|` smuggled via the page would execute when a later agent
runs the recheck. Today safe: across all 185 article text nodes the only shell metacharacter present is `'`, in
exactly one node per page — the page's own inline `curl --head --user-agent '…' --request GET 'xxxxxxx'` example,
which is ~40 units and therefore unselectable under the ≤25-unit ceiling; zero hits for `` ` ``, `$`, `\`, `!`,
and zero newlines. Smallest remediation: reject any quote containing `'` (or pass it through `grep -F -c -- "$q"`
via `printf %s`), and keep the rule "a quote never contains a shell metacharacter".

**F5 — LOW (operability/hang). The recheck line carries no `--max-time`.** `fetch_sources.py:12` uses
`--max-time 60`; the stored recheck (`curl -fsSL --compressed '<url>'`) has no timeout, so a stalled connection
hangs a verification run with no retry/abort path. Remediation: append `--max-time 60`.

**F6 — INFO (the copied `curl --head …` recipe: semantics verified, safe as printed).** The planned S424 entry
describes the page's UA check as `curl --head --user-agent '<Baiduspider UA>' --request GET '<site>'`. Probed on a
local server (`127.0.0.1:8931`, one GET): curl sends **`GET`**, not HEAD, with the spoofed
`…Baiduspider/2.0; +http://www.baidu.com/search/spider.html` UA, discards the response body, and writes the
*header block* to the output stream (`got.out` = 5 header lines; the 10-byte body was not saved). Run verbatim
with the page's placeholders it fails closed: `curl: (6) Could not resolve host: xxxxxxx`, exit 6 — no egress,
no state change, no credentials, idempotent read. Residual risk is editorial: substituting a real host turns it
into a forged-crawler-UA probe of a site we may not own (the page's own example is the third-party
`abc.com.cn`). Keep `'xxxxxxx'` / `'<site>'` verbatim in the entry, state "run only against your own domain",
and do not present it as copy-paste-ready (the `--head` + `--request GET` pairing is misleading).

**F7 — LOW (evidence quality). No content check on what was fetched.** `fetch_sources.py` accepts any HTTP 200
body; a WAF challenge or login shell would be pinned and cited as a page. Add a body assertion (the article block
`class="article-info"` is present in both retained bodies) or record `%{content_type}`.

**F8 — INFO. `argv[1]` is caller-controlled** (`os.makedirs(exist_ok=True)`, then writes under it) — harness
called, no injection into the arg list (`ROWS` is constant; `-o <path>` consumes the value, so a leading `-`
cannot be reinterpreted as a curl option), but a symlinked target dir writes outside the intended tree.

**F9 — INFO. UA `kake-shokunin-round58` (`:6`) is a durable self-identifier** in Baidu's access logs; no secret
in it, and it is recorded in the receipts (good provenance). Only note if the fleet later objects to
fingerprinting the harness.

## REDACTION NEEDED: no

- Token-shaped values in the retained bodies: exactly one — `…imcswebchat/roulette/in?id=16606&token=<32-char
  [a-z0-9]>&domainID=zhanzhang&type=2`, at **`S423.html:244` col 68** and **`S424.html:244` col 68** (same
  line/col in both; `token=` occurrences per body: 1). It is a Baidu-hosted chat-widget handle, and the evidence
  says it is static and public, not session-scoped: identical value in (a) both rows, (b) a fresh anonymous
  re-fetch today with no cookie jar, (c) **10** retained bodies across rounds 52/53/57/58 (S312, S329,
  S312-reread, S329-reread, S390, S409, S421, S422, S423, S424). It grants nothing of ours.
- Already committed: `git show fff3eea:.ufo/waves/round-58/sources/S423.html` contains it (1 occurrence), and the
  round-52/53/57 bodies precede it. Redaction is therefore not free: history rewrite **plus** re-pinned sha256
  for both bodies (their bytes change, so `receipts.json` and every downstream quote check follow). Given the
  static-widget evidence, that cost buys nothing.
- No cookies: the anonymous response does set `BAIDUID` and `PHPSESSID` (names only; header dump kept in scratch,
  never committed), and `fetch_sources.py` retains no headers at all (`-o` body only, no `-D`, no `-b`/`-c`).
  The bodies contain **0** occurrences of `BAIDUID`, `BDUSS`, `STOKEN`, `PHPSESSID`, `sessionid`, `csrf*`.
- Analytics id `hm.baidu.com/hm.js?<32-hex>` — site-wide public id, same in all 10 bodies; not a credential.
- No personal data: 0 email addresses, 0 phone numbers (0 eleven-digit runs), 0 15/18-digit ID-like strings,
  0 IPv4 literals, 0 `user@host` URLs, 0 NUL bytes, both bodies valid UTF-8. Template chrome only
  (`usercfg/editaccount`, `消息提醒`, `管理员设置`, `联系我们`) — nav links, no account identifiers.

## NON-ISSUES:

- Overwrite refusal works in the intended case: second run on a dir with `receipts.json` exits 1 with the pinned-
  evidence message (stub-verified).
- `--max-time 60` per URL, 2 URLs, no retry loop; default TLS verification; no `--insecure`; no auth headers, no
  cookie jar, no proxy config.
- `receipts.json` carries no token/cookie material; `fetchedAt` is UTC with explicit `+00:00`; byte counts match
  the files on disk (29007 / 22476).
- Article text nodes are raw substrings of the body (155/155 and 30/30) and contain no newline, so a text-node
  quote yields `grep -F -c` = 1; a ~25-unit sample Chinese span checked out on the retained body.
- The recheck's fetch surface is the page and nothing else: one GET to `ziyuan.baidu.com/college/articleinfo?id=…`,
  0 redirects today, no subresources (curl does not parse HTML), no cookies or credentials sent.
- Retaining public pages fetched anonymously is consistent with the lane's existing practice (260 files under
  `.ufo/waves/*/sources/`); opening them in a browser would contact baidu subdomains
  (hm/passport/zhiqiu/tongji/su/smartprogram) — a reviewer note, not a repo risk.

VERDICT: No secret or personal data in the C3 evidence; the widget `token=` is a static public Baidu handle already committed in fff3eea, so no redaction — fix the receipts-keyed overwrite refusal (F1) and harden the stored recheck quoting/timeout (F4/F5) before the entry text is frozen.
