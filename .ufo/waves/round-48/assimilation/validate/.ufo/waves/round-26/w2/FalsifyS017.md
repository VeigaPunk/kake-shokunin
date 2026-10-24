# Falsify S017 — round-26 C1 freshness recheck (receipt HOLD)

Seat: `KakeR26-2.FalsifyS017` (leaf member — no subagent dispatch). Milestone `r26-recheck-falsify`. Axis: **freshness**.
Target: `.ufo/waves/round-26/rechecks/S017.json` (verdict HOLD) and the SOURCES row `corpus/SOURCES.md:25`.

Goal: try to show the receipt is WRONG — (a) the quote does not ground this row's `teaches` (page chrome / neighbouring clause instead), (b) the `anchorObserved` is mislocated in the raw bytes, (c) content or version changed in a way the receipt missed.

**Verdict: AGREE** — the receipt survives every falsification attempt I ran. Residual observations are low severity; **no change to the receipt is required**.

## What the row claims (the ground truth under attack)

`corpus/SOURCES.md:25` (identical in base `97404de4` and candidate `e28312b1`; the only `corpus/SOURCES.md` delta in this round is the appended round-26 note at line 76):

```
| S017 | Astro Docs: Deploy your Astro Site to GitHub Pages — https://docs.astro.build/en/guides/deploy/github/ | docs | C | Whether public/CNAME sets a custom domain under Actions publishing | Change your GitHub URL to a custom domain, step 2; fetched 2026-10-19 | REJECTED: Astro's public/CNAME step is contradicted by GitHub's Pages guidance for Actions; flip: GitHub docs say the CNAME file is honored under Actions | rejected | 2026-10-19 | 90d | — |
```

- teaches: *“REJECTED: Astro's public/CNAME step is contradicted by GitHub's Pages guidance for Actions; flip: GitHub docs say the CNAME file is honored under Actions”* — a **rejection** plus an explicit **flip condition**.
- anchor: *“Change your GitHub URL to a custom domain, step 2; fetched 2026-10-19”*.
- status `rejected`, `used-by` `—`.

Receipt under attack (`.ufo/waves/round-26/rechecks/S017.json:1-9`), byte-identical in the worktree and at candidate `e28312b1` (both sha256 `6a09794ae7a467b4c30773aada630b9ada90423e69d29a12a8c235d30a1abc9a`); absent at base `97404de4` (round-26 added it):

```json
{"id":"S017","verdict":"HOLD","fetchIndex":1,
 "quote":"This will deploy your site at your custom domain instead of user.github.io.",
 "anchorObserved":"Change your GitHub URL to a custom domain\" heading, step 2 'Add a ./public/CNAME record to your project.' (text view renders the inline link as 'Add a./public/CNAME'); quoted sentence immediately follows 'public/CNAME sub. example. com'",
 "reason":"The page still tells readers to 'Choose GitHub Actions as the Source of your site' and then presents the public/CNAME file as the thing that sets the domain, so the contradicted claim survives verbatim at the same anchor. GitHub's custom-domain page re-fetched this round still says 'If you are publishing from a custom GitHub Actions workflow, no CNAME file is created, and any existing CNAME file is ignored and is not required.' The flip condition ('GitHub docs say the CNAME file is honored under Actions') is not met; if anything the guidance is firmer, so the rejection and its scope hold.",
 "correction":null}
```

## Attack 1 — Does the quote ground THIS row's teaches (not page chrome, not a neighbouring clause)? → NO DEFECT

Retained bytes `fetched/S017-1.raw.gz` decompress to 187 320 B, sha256 `89cb471d86fd43f8b76420ac1c2079a52fdef21418bdf1e09a1f367b07336075` — exactly the manifest value (`.ufo/waves/round-26/fetched/manifest.json`, S017 index 1: `status 200`, `error null`, `bytes 187320`, `etag "802f3028ac2648e5c61ab4b4f5b5c6db"`, `fetchedAt 2026-10-21T15:10:41Z`) and the population pin (`population.json` S017 → same sha256, `file fetched/S017-1.raw.gz`).

- The quote is **body prose inside the row's own anchor list item**, not chrome. Raw-byte offsets (0-based, in the decompressed HTML): `<h2 id="change-your-github-url-to-a-custom-domain">` at **156 546**; step 2's `Add a <code dir="auto">./public/CNAME</code> record to your project.` at **158 082**; the quoted sentence at **158 960**; its `user.github.io` code element at **159 020**. The `<ol role="list" class="sl-steps">` under the h2 has exactly 4 `<li>`s and the quote falls **inside step 2** (verified by slicing the `ol` and testing containment per `li`: step 1 `Configure DNS for your domain provider.` → no; step 2 → **yes**; step 3 `In your Astro config, update the value for site…` → no; step 4 `If necessary, update all your page internal links…` → no).
- It is the sentence that carries the row's scope claim: the row's scope is *“Whether public/CNAME sets a custom domain under Actions publishing”*, and the quoted sentence is the assertion that the `public/CNAME` file *“will deploy your site at your custom domain instead of user.github.io.”* — i.e. exactly the claim the row rejects. It is not a neighbouring clause (step 1 is DNS configuration; step 3 is the `site` config value).
- The receipt's own prose binds the quote to the CNAME step, so the quote is not read as a free-floating sentence: `anchorObserved` states the quoted sentence *“immediately follows 'public/CNAME sub. example. com'”* — verified verbatim in the retained text view (`corpus/knowledge`-independent): `'public/CNAME sub. example. com This will deploy your site at your custom domain instead of user.github.io.' in S017-1.txt` → **True**.
- Word-bounded, row-specific, and counter-legal: `re.search(r"(?<!\w)" + re.escape(normalize(quote)) + r"(?!\w)", text)` → **match**, 1 occurrence; the same string occurs in **no other** retained text view (`grep -lF` over `.ufo/waves/round-26/fetched/text/*.txt` → only `S017-1.txt`; the loose prefix `This will deploy your site at your custom domain` likewise only in `S017-1.txt`). S017 is in no document group, so the contract-amendment row-specificity rule (`contract-amendment.json`, “a decided quote must not occur in any other population row text outside its document group”) is satisfied. `tokens = 14 ≥ 6`, `words = 12 ≤ 25` → `quote_word_count` and `quote_not_in_text` pass.
- The receipt's second cited claim is also verbatim: `'Choose GitHub Actions as the Source of your site' in S017-1.txt` → **True** (raw bytes: `Choose <strong>GitHub Actions</strong> as the <strong>Source</strong> of your site.` at offset 156 263, i.e. *before* the custom-domain h2 at 156 546 — the order the receipt asserts).
- **Flip condition test (the point of the row)**: the flip is *“GitHub docs say the CNAME file is honored under Actions”*. The re-fetched GitHub custom-domain page (S005, `fetched/text/S005-1.txt`) still contains, verbatim, `If you are publishing from a custom GitHub Actions workflow, no CNAME file is created, and any existing CNAME file is ignored and is not required.` → **True**; the re-fetched publishing-source page (S003) still contains `A CNAME file in your repository file does not automatically add or remove a custom domain.` The flip is therefore **not met** on the re-fetched bytes, so the row's `rejected` status and its `teaches` cell remain accurate and `HOLD` with `correction: null` is the correct verdict.
- **No stale adjudication is owed for this row**: `grep -rn "S017" corpus/` → `SOURCES.md:25`, `SOURCES.md:48` (chain note), `SOURCES.md:65` (round-20 gate note), `corpus/lessons/round-20.md:186`, `corpus/lessons/round-20.md:219`, `corpus/lessons/round-20-verifier-spotcheck.md:13`. The registry row's `used-by` is `—`; **no `corpus/knowledge/` entry cites S017**, and `statements.json` `pairs` has **no S017 entry** (25 pairs, all pointing at `corpus/knowledge/*.md`). So no `[r26-recheck S017 STALE]` block is required or expected, and none exists (`grep -rn "r26-recheck S017" corpus/` → no matches). Consistent with the 8 exact tags present, all on other rows: `[r26-recheck S003 STALE]`×2, `S010`×2, `S021`×1, `S026`×1, `S030`×2.

## Attack 2 — Is `anchorObserved` correct in the raw bytes? → NO DEFECT

Every locator in `anchorObserved` was checked against `fetched/S017-1.raw.gz`:

| claim | raw evidence | verdict |
|---|---|---|
| heading “Change your GitHub URL to a custom domain” | `<h2 id="change-your-github-url-to-a-custom-domain">Change your GitHub URL to a custom domain</h2>` at 156 546 | ✓ |
| “step 2 ‘Add a ./public/CNAME record to your project.’” | `<p>Add a <code dir="auto">./public/CNAME</code> record to your project.</p>` at 158 082, inside the 2nd `<li>` of the section’s `sl-steps` `<ol>` (4 `<li>`s total) | ✓ |
| “text view renders the inline link as ‘Add a./public/CNAME’” | the text view joins `<code>` content without a space and `source_text.normalize()` strips whitespace before `.` → `Add a./public/CNAME` | ✓ (rendering; element type misnamed — see R1) |
| “quoted sentence immediately follows ‘public/CNAME sub. example. com’” | text view: `public/CNAME sub. example. com This will deploy your site at your custom domain instead of user.github.io.` | ✓ |

The SOURCES row’s own anchor cell *“Change your GitHub URL to a custom domain, step 2”* still resolves: the h2 text is unchanged and step 2 of that list is still the CNAME step. The round-20 ledger record (`corpus/lessons/round-20.md:219`) quotes the same two sources — Astro *“Add a `./public/CNAME` record to your project.”* and GitHub *“any existing `CNAME` file is ignored and is not required.”* — and both are still present in the 2026-10-21 bytes (`'Add a./public/CNAME record to your project.' in S017-1.txt` → True; `'any existing CNAME file is ignored and is not required' in S005-1.txt` → True).

## Attack 3 — Did content or version change in a way the receipt missed? → NO DEFECT

1. **Independent live GET of the row URL** (one plain GET of `https://docs.astro.build/en/guides/deploy/github/`, already listed in `corpus/SOURCES.md`; `curl 8.23.0`, 2026-10-21): body **187 320 B, sha256 `89cb471d86fd43f8b76420ac1c2079a52fdef21418bdf1e09a1f367b07336075`, etag `"802f3028ac2648e5c61ab4b4f5b5c6db"`** — **byte-identical to the retained wave bytes**, and the etag matches the manifest’s. There is no drift window at all: the same bytes, the same validator, the same content. (The GET was piped in memory for digest/length comparison only; nothing was saved.)
2. **The corroborating witness also holds.** One further plain GET of the already-listed documentation URL for row S005 (`…/managing-a-custom-domain-for-your-github-pages-site`) yields 240 439 B with **108 differing bytes** against the retained `fetched/S005-1.raw.gz` — but the differences are **entirely Next.js asset-chunk hashes** (e.g. `webpack-091b7f339815a268.js` vs `webpack-5e180f68666d859a.js`; first diff at byte 7 769, last at 240 228), and the **extracted text is identical** (14 697 chars both; `text equal: True`). The sentence the receipt relies on is present in the live text as well as in the retained text. So the contradiction witness is current, not a stale cached reading.
3. **Committed bytes agree with the worktree**: `git show e28312b1:.ufo/waves/round-26/fetched/S017-1.raw.gz | sha256sum` = `7cf007f1c3218766ed6fd5639d64621258b00e86bed405d8c9fd9ce6a07807c6` = the worktree file; same for `rechecks/S017.json` (`6a09794a…`). `fetchIndex: 1` is the row’s only population fetch.
4. **Receipt shape and counter verdict**: exactly the 7 required keys (`id, verdict, fetchIndex, quote, anchorObserved, reason, correction`), `id == "S017"`, `verdict == "HOLD"`, non-empty `reason` and `anchorObserved`, `correction: null` (required for HOLD). Running the committed counter at the candidate revision: `python3 -B .ufo/waves/round-26/measure.py --root . --revision e28312b14b076584fedd696fae2a684e460bd11e` → `{"decided": 32, "expected": 32, "findings": [], "hold": 32, "stale": 0, "unverifiable": 0, "statements": 276, "statementsStale": 8, "statementCorrections": 8, "schema": "kake-source-recheck-v1"}`, **exit 0**. Row-level verdicts: HOLD 32 / STALE 0 / UNVERIFIABLE 0, matching the round-26 note at `corpus/SOURCES.md:76`.
5. **Seat report ≡ receipt**: the JSON block in `w1/RowS017.md` parses to a dict **identical** to `rechecks/S017.json` (all 7 keys, no differences) — the receipt is the seat report unchanged, as `corpus/lessons/round-26.md` claims.

## Residual observations (low severity; none requires changing the receipt)

**R1 — `anchorObserved` misnames an HTML element type.** It says *“text view renders the inline link as ‘Add a./public/CNAME’”*, but in the raw bytes `./public/CNAME` is an inline **`<code dir="auto">`** element (`<p>Add a <code dir="auto">./public/CNAME</code> record to your project.</p>`, offset 158 082). The only real link in that list is step 1’s `Configure DNS for your domain provider` → `docs.github.com/...`. The rendered-string claim itself is right (the missing space comes from `source_text.normalize()`’s whitespace-before-`.` rule, not from the markup). The located text and the quote’s position are exact, so this is wording, not mislocation.

**R2 — `anchorObserved` opens with an unbalanced quote.** The string begins `Change your GitHub URL to a custom domain" heading` — a stray closing double-quote with no opener. Cosmetic JSON-string formatting; the intended heading text is unambiguous and matches the raw bytes.

**R3 — the receipt’s `reason` cites GitHub’s wording without naming the source row or its digest.** The sentence *“If you are publishing from a custom GitHub Actions workflow, no CNAME file is created, and any existing CNAME file is ignored and is not required.”* is S005’s text, not S017’s. The claim is grounded (S005 was re-fetched this round and its own receipt `rechecks/S005.json` re-verifies the identical sentence, HOLD), and `w1/RowS017.md` discloses the cross-reference (“quoted from this round’s `fetched/text/S005-1.txt` … this row only uses it as the contradiction witness its teaches names”) — but the disclosure is in the seat report, not in the receipt itself, so the receipt is not self-contained on that point.

**R4 — scope note on the flip condition (not a defect).** The flip is written at the documentation level (*“GitHub docs say the CNAME file is honored under Actions”*). The re-fetched GitHub pages in this wave’s population (S003, S005) both still deny it, so the flip is unmet on the evidence this wave retains, and HOLD is correct on the row’s own terms. A *behavioural* proposition (whether a CNAME file in the **published artifact root** is honoured by Pages under Actions, as opposed to a CNAME in the **repository**) is a different claim; it is not what the flip says, it is not stated by the re-fetched docs, and I did not probe it — that would be property probing, outside the lane bounds, and the “Setting up a custom domain” / “About custom domains” pages are not in `corpus/SOURCES.md` (no occurrence of `setting-up-a-custom-domain` in `corpus/`), so they were not fetched either.

## Verification gaps / limits of this attack

- No 2026-10-19 bytes are retained for S017, so “the contradicted claim survives at the same anchor” is established against (a) the corpus’s own 2026-10-19 record (`corpus/lessons/round-20.md:219`, whose two quotes are still present verbatim in the 2026-10-21 bytes), and (b) the 2026-10-21 re-fetch, which is byte-identical to this round’s retained bytes and to a live GET taken now. There is no residual drift window to close.
- I did not fetch any URL outside `corpus/SOURCES.md`; no property, browser, account, credential, publication or security probe was performed; no round-24 material was read, run, retried, rephrased or re-routed.
- I did not modify the corpus, scripts, the fleet repo, sibling lanes, or the lane Git index/jj. `git status --porcelain -- corpus/ scripts/ .ufo/waves/round-26/rechecks/ .ufo/waves/round-26/fetched/` → empty (only untracked wave scratch directories exist in the lane). The only file I wrote is this report.

## Process note / bound compliance

- Tools used, none installed or updated: `curl 8.23.0` (system package, OpenSSL 3.6.5), `python3 3.14.8`, `git 2.56.0`, `gzip`, `sha256sum`, `grep`. No pacman/uv/cargo/npm transaction was performed; the host-wide pacman pause was untouched.
- Two plain public GETs, both of documentation URLs already listed in `corpus/SOURCES.md` (the row's own URL, and the S005 URL used as the contradiction witness), both piped in memory for digest/length/text comparison and neither saved to disk.
- Files written by me: this report only (`.ufo/waves/round-26/w2/FalsifyS017.md`).
- Disclosure: importing the committed helper `.ufo/waves/round-26/source_text.py` through `importlib` caused CPython to emit an untracked bytecode cache (`.ufo/waves/round-26/__pycache__/source_text.cpython-314.pyc`; a matching `before/__pycache__/` entry was present in the lane at the same moment, from a concurrent peer). These are regenerable caches of a committed wave helper, are untracked (`git status` shows them as `??`), and touch no corpus file, script, fleet repo, sibling lane, or the lane Git index/jj; I left them in place rather than delete files a concurrently running peer may be using.

```json
{"target":".ufo/waves/round-26/rechecks/S017.json","verdict":"AGREE","severity":"low"}
```
