# RevengerSurvivors — why M07/M08/M09/M11/M24 survived the round-36 selftest

Seat: KakeR37.RevengerSurvivors (leaf). Scope: reverse-engineer the five round-36 tool mutants
that survive the round-36 selftest fixture set (C2 base 27 of 32) and name the contract sentence
each breaks. Sandbox: /fast/scratch/hyaku/kake-r37w1/RevengerSurvivors/ (no lane writes except
this report; no tool installs; no sealed-tree contact).

## Baseline reproduced (public C2 counter, my sandbox clone at 4b089da6)

`python3 -B <lane>/.ufo/waves/round-37/c2_mutkill.py --root <clone> --revision 4b089da6… --jobs 8`
→ exit 1, `fixtures: 101, validFixtures: 101, failedOnE1: [], failedOnE2: [], killed: 27,
survivors: ["M07","M08","M09","M11","M24"]` (counter.json sha256 8decc585…). E1 = 4d5b3d55
tool (sha 577b2d7d…), E2 = 1a16b8e3 independent reference (sha a5176fee…), mutant shas match
MutTool-manifest.json pins.

## Per-mutant findings (probe.py sha 31e84d25…, results b3f274bb…)

Each: mutation site in E1, contract sentence (quoted from the round-36 selftest CONTRACT, which
quotes SCORECARD round-36 C1), smallest input, observed outputs. E2 agrees with E1 on all five →
all five are valid C2 killer candidates. Runner: `python3 -B probe.py` → exit 0.

**M07** (bullet b; MutTool "each redirect resolved from original URL"). E1.py:488
`resolve_reference(base, …)` → mutant `resolve_reference(check["url"], …)`: hop ≥2 locations are
resolved against the check URL, not the previous resolved location.
Breaks (b): "Each location is resolved against the URL that hop answered (the check url for the
first hop, then the previous resolved location) by RFC 3986 section 5.2".
Input: url `https://a.example/dir/page`; hops 301 `/two`, 308 `three`, 404; quote `PAYLOAD`.
E1=E2: exit 1, moved target `https://a.example/three` + gone. M07: moved target
`https://a.example/dir/three` (hop 2 rebased on `/dir/page`). Killed on target projection.
Survival: dump of the selftest's 101 FIXTURES has **0 fixtures with a relative (non-`/`, non-
scheme) location on hop ≥ 2** — the chain-rule sentence is never exercised past hop 1.

**M08** (bullet b; "relative redirects retain dot segments"). E1.py:178
`remove_dot_segments(_merge(...))` → mutant `_merge(...)` only: relative-path references keep
`.`/`..` segments (RFC 3986 §5.2.4 skipped after §5.2.3 merge).
Breaks (b): resolution "by RFC 3986 section 5.2" (§5.2.2 target path = RDS(merge(path))).
Input: url `https://a.example/dir/page`; hops 301 `../top`, 404; quote `PAYLOAD`.
E1=E2: exit 1, moved target `https://a.example/top`. M08: `https://a.example/dir/../top`.
Survival: the only `../` in the fixture set is the body *path* of `g09-body-path-escapes-manifest-
directory`; **no fixture resolves a dot-segment hop location**, so RDS-after-merge is never tested.

**M09** (bullet c; "retain HTML comments"). E1.py:343 `text = remove_comments(text)` deleted from
`html_text`. strip_tags still eats `<!--…-->` spans that contain `>`, so only a comment with an
inner `>` before the quote leaks text.
Breaks (c): "comments removed (`<!--` to the next `-->`)".
Input: contentType text/html; body `<!-- >PAYLOAD -->`; quote `PAYLOAD`.
E1=E2: exit 1 quote_missing (comment gone). M09: exit 0 clean (strip_tags removes only `<!-- >`,
leaving `PAYLOAD -->`). Caution for whoever seals this: the natural fixture `<!--PAYLOAD-->` is a
**false killer** — M09 passes it too (strip_tags removes the whole span); verified, then replaced.
Survival: exactly one fixture carries a comment (`c04-comment-removed`: `<!-- hidden note -->`
after `<p>hi</p>` — no inner `>`, no quote inside), so remove_comments is observationally dead.

**M11** (bullet c; "retain ordinary HTML tags"). E1.py:345 `text = strip_tags(text)` deleted.
Breaks (c): "every remaining tag removed (`<` followed by an ASCII letter, / or !, up to the
next `>`)". A tag merely *adjacent* to the quote still matches; it must **split** the quote.
Input: contentType text/html; body `PA<b>YLOAD`; quote `PAYLOAD`.
E1=E2: exit 0 clean. M11: exit 1 quote_missing (text stays `PA<b>YLOAD`). 55 fixtures contain
tags; none puts a tag between quote characters — wrapping `<b>PAYLOAD</b>` does NOT kill it
(verified pass before I sharpened the probe).

**M24** (bullet f; "decode BOM but do not drop its mark"). E1.py:255 `return codec,
data[len(mark):]` → mutant `return codec, data`: the BOM survives decoding as a leading U+FEFF.
Breaks (f): "A body starting with a byte order mark … is decoded in that encoding with the mark
dropped, whatever charset says".
Deep reason it survives: (d) is *substring* matching, `'\ufeff'.isspace()` is False and NFKC
leaves it, so a retained leading BOM is invisible unless the quote itself contains U+FEFF.
Input: contentType text/plain (no charset); body bytes `EF BB BF` + `PAYLOAD`; quote
`U+FEFF PAYLOAD`.
E1=E2: exit 1 quote_missing (mark dropped). M24: exit 0 clean. The 3 BOM fixtures (f01, f12,
f13) all use U+FEFF-free quotes → all pass on both implementations.

## Cross-checks and limits

- All probes judged exactly like the counter (exit among accepted, report shape, findings
  projected on (check, reason, target-for-moved), checksEvaluated); each mutant fails only its
  own fixture and passes the other four — inputs are minimal and specific.
- Manifest rule discovered en route: a check requires a non-empty string `quote` even when the
  final hop is 404 (E1.py:431); quote-less 404-tail manifests are `check_invalid` on E1 *and* E2
  (both rejected my first shrunk fixtures — no E1/E2 disagreement there).
- M24's distinguishing input is contract-legal but pathological (U+FEFF in the quote); every
  ordinary input is observationally invariant under the report schema — worth a limit line if
  the L1 wants M24 killable by sealed cases (fix must either anchor the match or expose text).
- Did not verify: the five probes run through the counter's bwrap jail (they run direct with
  clean env), and nothing was added to the selftest — sealed/selftest changes are L1 work.

Report: .ufo/waves/round-37/w1/RevengerSurvivors.md
