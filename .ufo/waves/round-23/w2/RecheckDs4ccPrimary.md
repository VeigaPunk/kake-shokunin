# RecheckDs4ccPrimary — round 23 wave 2 falsification (C2 surface `ds4cc-primary`)

Lane: /home/vgpnk/Projects/shokunin/kake-shokunin — frozen candidate 5e5afb9e4d8ee18831b9b35b35e8a34e47aceecd (base b5d599e19bead54b96f589444e9ec64cdf67c28a). Scratch: /tmp/kake-r23w2-Ds4cc-AZkS. Read-only on the lane except this report. No tools installed or updated (none needed).

## Verdict

**No counterexample found.** Every attack on the `expectedCanonical` choice and on the audit receipt's served/not-served classification failed against evidence; the counter reproduces this surface (12/12 overall, exit 0); the fresh GET is byte-identical to the committed snapshot (zero drift).

## Findings

No P0–P2 findings. Two P3 robustness notes on the reproduction machinery (neither invalidates the claim for this surface; both observed by code reading, not exercised as failures):

- **P3 — uncaught validator timeout in measure_c2.py.** `check()` runs `subprocess.run([... canonical_audit.py ...], timeout=60)` (measure_c2.py:71) without catching `subprocess.TimeoutExpired`; a hung validator crashes the counter with a traceback instead of a typed exit 2 ("inputs cannot be read") or a per-surface problem row. Impacted axis: C2 reproduction robustness. Smallest fix: wrap the `subprocess.run` in `try/except subprocess.TimeoutExpired` and append a problem row (`"validator timed out"`). The frozen validator is a bounded static parser (2 MiB HTML cap), so a hang is unlikely; ds4cc-primary reproduces fine.
- **P3 (informational) — the committed `live/ds4cc-primary/manifest.json` is never read by the counter.** measure_c2.py rebuilds its own manifest from `fetch.finalUrl` + population `expectedCanonical` (measure_c2.py:65-68). For this surface the committed manifest (sha256 6cf2d4efbf45e7d2824a020d83cb22d044a1c16d405f30bdf2b55b0ed4659835) agrees content-wise (`url=https://ds4cc.com/`, `file=page.html`, `expectedCanonical=https://ds4cc.com/`), so nothing is masked; noted only because manifest drift would be invisible to the counter by design.

## Checked and held

### 0. Committed snapshot identity with the frozen revision

`cd /home/vgpnk/Projects/shokunin/kake-shokunin && for f in …; do cmp working-tree sha256 vs git show 5e5afb9e:$f sha256; done` → **MATCH for all five** inputs (`fetch.json`, `audit.json`, `page.html`, `manifest.json`, `c2-population.json`). `c2-population.json` digest `ac58c80fda73cae194fcc75bf56f62b19ea5443048ddf822fcee8d08e7c75d98` equals the frozen `POPULATION_SHA256` constant; revision `5e5afb9e…` resolves via `git rev-parse --verify 5e5afb9e…^{commit}`. So all eyeball derivations below are about exactly the measured bytes.

### 1. Fresh read-only GET vs committed fetch.json

Command: `curl -sSL --max-time 60 -o fresh.html -w 'status=%{http_code} finalUrl=%{url_effective} contentType=%{content_type} bytes=%{size_download} numRedirects=%{num_redirects}\n' https://ds4cc.com/ && sha256sum fresh.html` (2026-10-21, one GET, no auth/forms).

| field | committed fetch.json | fresh GET | match |
|---|---|---|---|
| status | 200 | 200 | yes |
| finalUrl | https://ds4cc.com/ | https://ds4cc.com/ | yes |
| content-type | text/html; charset=utf-8 | text/html; charset=utf-8 | yes |
| sha256 | ccb3f46eda1ce3270df1e3373d49c4034025c4f475a6999142279e03b00b2bb8 | ccb3f46eda1ce3270df1e3373d49c4034025c4f475a6999142279e03b00b2bb8 | yes |
| bytes | 76159 | 76159 | yes |
| redirects | [] | numRedirects=0 | yes |

**Zero drift** — the live body is byte-identical to the committed `page.html`. No drift statement needed beyond this line.

### 2. By-eye policy derivation from committed page.html head

Head spans lines 2–497 (`</head>` at 497). Grep over the whole page for `<base|rel="canonical"|rel='canonical'|rel=canonical` finds exactly one canonical link — line 496, inside the head: `<link rel="canonical" href="https://ds4cc.com/" />` — and **no `<base>` anywhere**; no svg/math before the head closes. Policy ("one head canonical equal to expectedCanonical; mirrors declare their primary") therefore implies: exactly one head canonical, href `https://ds4cc.com/` == expectedCanonical → **verdict clean, exit 0, findings [], pagesChecked 1**. Committed audit.json is exactly `{"exit": 0, "result": {"findings": [], "pagesChecked": 1, "verdict": "clean"}}`. Derivation and receipt agree. (`og:url` at line 10 says the same URL; the validator ignores og:url, correctly per policy.)

### 3. Counter reproduction

`python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --revision 5e5afb9e4d8ee18831b9b35b35e8a34e47aceecd` → exit 0; `"accepted": 12, "total": 12`; the ds4cc-primary row is `{"id": "ds4cc-primary", "pass": true, "problems": [], "verdict": "clean"}`. `validatorSha256` = `062ccc4db6ab506ecb274ac0da4e4c4e9041462562e23cc586a0168cc8e44387`, which equals the sha256 of `git show 5e5afb9e:scripts/canonical_audit.py` (verified by digest), and that frozen validator's `--selftest` exits 0 (all cases ok, incl. `absolute_match`, `selfclosing_link`, `title_text_decoy`). The claim that the validator now evaluates body SVG/MathML and void self-closing tags but rejects any base after the head is consistent with its code (`scripts/canonical_audit.py:212-308` head-boundary handling, `:633-682` evaluate_page) and its passing selftest.

### 4. Attack: expectedCanonical choice (`https://ds4cc.com/`, basis "primary self-canonical")

Failed to break. The choice is forced, not merely defensible:
1. The served page's only head canonical is exactly `https://ds4cc.com/` (fresh GET byte-identical to committed, so live agrees too).
2. The page's `og:url` (line 10) says the same.
3. The property map designates `ds4cc.com (primary) | https://ds4cc.com/` (receipt `property-map.json` c22 and c26, both HOLD; anchor SKILL.md:16) — the primary designation is on record, and the mirror `ds4cc-kimi` in the same population declares `expectedCanonical=https://ds4cc.com/`, consistent with ds4cc.com being the primary.
4. `fetch.url == fetch.finalUrl == https://ds4cc.com/` (no redirect), so no normalization gap (www/http/apex/trailing-slash variants) exists between fetched and expected. No competing candidate has any on-record support.

### 5. Attack: the receipt's served / not-served classification

Failed to break. Clarification first: `.ufo/waves/round-23/receipts/` contains 18 files covering the 17 C1 units — **no `ds4cc-primary.json` exists there, by design**; for C2 the "canonical-policy receipt" is `live/<id>/audit.json` (measure_c2.py docstring). Attacks on that classification:
- *Served branch taken correctly?* `served()` (measure_c2.py:38-41) needs int 2xx status (200 ✓), `error is None` (✓), `not truncated` (false ✓), ctype `text/html` after `;`-split/lower (✓). All four hold, so the served branch is mandatory — the counter cannot misclassify this surface as not-served.
- *Page digest gate:* `sha256(page.html) == fetch.sha256` → `ccb3f46e…` both sides ✓.
- *Receipt equality gate:* the counter re-runs the frozen validator on a rebuilt manifest in a temp dir and requires `audit.json == {"exit": done.returncode, "result": json.loads(stdout)}` exactly → holds (findings §3); dict compare is key-order-insensitive, and `public_result` emits exactly `{verdict, pagesChecked, findings}` (canonical_audit.py:766+), so no extra-key mismatch.
- *Not-served branch soundness (by code reading):* a non-served fetch requires `verdict=="not-served"` + `status==fetch.status` + **no page.html stored**; a 2xx-but-error-flagged or truncated capture also falls to not-served, and `isinstance(status, int)` cannot be spoofed by `true` (True==1 < 200). For ds4cc-primary none of these paths are reachable, and none was found wrongly reachable for a 2xx-text/html surface.
- *Other gates:* `fetchedAt` `"2026-10-21T06:33:03Z"[:10]` is not `< "2026-10-21"` ✓; `url`/`method` match the population GET ✓.

## Limits

- Fresh GET is one instant, one vantage (curl 8.x, `-L`), from this workstation; drift after 2026-10-21 ~fetch time is unobservable from here. Zero drift was observed at check time.
- The other 11 surfaces were accepted only via the single aggregate counter run (out of my scope); I verified counter mechanics and the validator snapshot, not their individual pages.
- The two P3 notes are code-reading findings on the reproduction machinery; the timeout path was not exercised (would require a hanging validator).
- C1 (17 receipts) was not in scope; I only confirmed the receipts directory layout to resolve the "receipt" naming (C2 receipts are the per-surface audit.json files).
