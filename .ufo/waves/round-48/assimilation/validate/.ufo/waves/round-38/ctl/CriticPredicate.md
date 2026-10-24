# kake r38 pre-freeze control — CriticPredicate

Seal respected: nothing under /fast/scratch/hyaku/kake-r38/ was listed, stat'ed or read (receipts name paths there; I read only committed JSON holding those strings). No lane mutation; read-only git. No installs.

## Built (stdlib, CLI `--manifest PATH`, one JSON report; `py_compile` exit 0; no key, unscored)

| Tool | Path | sha256 |
|---|---|---|
| base + (h)(i)(k) as I read the public text | `/fast/scratch/hyaku/kake-r38ctl/CriticPredicate/rulepatch.py` | `8a5712b455c3105a39f8191ec5bac7494d8f9564f5a5dde0bbe68ca242b96bc5` |
| same, RFC 3986 pct-encoded reading of (i) | `/fast/scratch/hyaku/kake-r38ctl/CriticPredicate/rulepatch_pct.py` | `b2c86c8c6e0d1d0d952621b2709248f6fa90b3254f701d67cc00137b1079b783` |

rulepatch = base bytes `944d2f51…d3e5` + (h) `parse_constant` reject and `parse_int` keeping >4000-digit tokens as text, (i) ASCII whitelist before parsing, (k) allow on `normalize(path_to_match)`. Expected 20/20; 19 if one reading is off. pct differs only on `%` without two hex digits; expected 20 if untested, 19 if one (i) case carries `%`-garbage, ≤18 otherwise. Local probes (exit): `%ZZ` → rulepatch `blocked` 1 / pct `check_invalid` 2; `/robots.txt?` → `clean` 0; duplicate `checks` key → `clean` 0; `1e999` → `check_invalid` 2; 5000-digit status → `check_invalid` + other check evaluated 2; 5000-digit unread field → evaluated 1; raw `NaN` → one `input_invalid`, 0 evaluated 2.

## Objections (quote → evidence → smallest safe fix)

1. **Wrong bullet label.** "Bullets: (g) groups and (d) rules." In the round-37 contract (g) is *manifest faults*; groups are (c). The parenthetical (substring user-agent, first-group-only, groups ended by non-record lines) describes (b)/(c); "g3" being the one case the stdlib passes fits a group case. Then "the sealed cases test (g), (d) of that contract" misnames 40% of the key. Fix: relabel to "(c) groups" before freeze (case ids may stay `g*`).
2. **Unenumerated universal clause.** "Every case of (g), (d), (i), (k) has a check whose correct outcome is a finding and one whose correct outcome is none." The counter scores runs and never inspects key shape (prompt §6.9). It is also unsatisfiable as read for (g): a (g) run is a manifest fault — one `input_invalid`, check null, "nothing is evaluated" — so no check has a finding and none has none. Fix: "each (d), (i), (k) case", and for (g) "each case has one run with non-empty expected findings and one with empty expected findings", or a key lint at freeze.
3. **Predicate is not the same string.** Plan block: `met: passed >= 19 of 20 sealed cases`. Code: `PREDICATE = "passed >= 19 of 20 sealed cases"`; receipts carry that same string without `met: `. The declaration calls the plan block "the same sentence here ... and in every receipt's `predicate` field". Fix: drop `met: ` from the plan block, or add it to `PREDICATE` and re-emit receipts (the r37 counter carries the same defect).
4. **19/20 tolerates a regression in a held rule.** 8 of 20 cases are (c)/(d), all passed by the base (`perCase`: g1–g4, d1–d4). The one tolerated failure may be one of them while all 12 new cases pass. Concrete: flip the equal-length tie-break to first-rule-wins; robots `User-agent: *` / `Allow: /a` / `Disallow: /a`, url `/a`, expect allow → one (d) case lost → 19, `met`. The r37 counter/selftest harm instruments would catch it but are "not the claim"; the predicate alone certifies a broken held rule. Fix: `passed >= 19 and 4/4 on (c) and (d)` (tolerance stays only among (h)/(i)/(k)).
5. **Routed defect 1 incomplete.** "The `## Capabilities` row ... and the 'Capabilities acquired in round 37' row carry that status." `git diff af43a50f b0ab7f60 -- SCORECARD.md` = 104 insertions, 0 deletions, all in the appended section; row 198 still reads "sealed counter 28 of 28 ... against 0 at base" with no not-admitted marker. Fix: append "(round-37 C1 not admitted at closure; see 'Round 37 — closure correction')" to both rows (append, not rewrite).
6. **(h) size bound contradicts (g).** "a manifest of up to 64 MiB of digits must still finish within the counter's 20 s" vs "larger than 64 MiB ... input_invalid": a 64 MiB digit token plus JSON syntax exceeds the cap, so it is an input fault, never an evaluated check. Fix: name the size ("a 50 MiB digit string in an unread field") inside a ≤64 MiB manifest.

## Ambiguities (two careful implementers differ; input → reading A vs B, observed)

| # | Rule | Input | A vs B |
|---|---|---|---|
| A1 | (i) | url `http://h/%ZZ`, robots `Disallow: /`, expect allow | list-literal: `blocked` 1; pct-encoded: `check_invalid` 2 |
| A2 | (k) | url `http://h/robots.txt?`, robots `Disallow: /`, expect allow | empty query dropped: `clean` 0; `?` present = "with a query": `blocked` 1 |
| A3 | (h) | `{"version":1,"checks":[<valid>],"checks":[]}` | last-wins: `clean` 0; duplicate names not JSON / first-wins: `input_invalid` or `blocked` |
| A4 | (h) | `"robotsStatus": 1e999` | finite syntax: `check_invalid` 2; infinite value = rejected literal: `input_invalid` 2 |
| A5 | (h) | 5000-digit number in an unread field | contract: evaluate; default `json.loads` raises → `input_invalid` |
| A6 | (k) | robots `Disallow: /robots.txt`, url `/robots.txt`, expect allow | "is allowed": `clean`; rules decide: `blocked` (base overrides; text does not say so) |
| A7 | (h)/(g) | manifest of 64 MiB of digits | evaluate per (h); `input_invalid` per the 64 MiB cap |

One sentence each fixes all: `%` need not be followed by hex; a trailing empty `?` does not change the path to match; duplicate member names: last wins; only the three literal tokens are non-JSON; long integers are `check_invalid` regardless of field; the /robots.txt allow overrides rules; the digit bound sits inside a ≤64 MiB manifest.

## Sound (measured from committed bytes)

- Counter file sha256 `52daff55…6e7b` = the declared pin (`sha256sum` exit 0); `met` line is `len(rows) == CASES and passed >= TARGET`; key pin `8b3fac55…2941`; before receipt 8/20, met false, exit 1, toolSha256 `944d2f51…` = base bytes (`git show | sha256sum` exit 0).
- Routed defect 2 holds: r37 key at `424aa248` sha256 `93ad9ee6…` = its pin; r37 counter unchanged.
- No whole-rule skip reaches 19: base 8 + the other two rules' 8 = 16; 19 needs 11 of 12 new cases. Stdlib shortcut 7 and ablations ≤18 (pre receipts) reproduce by reading, so the target separates them; base is 8, not a do-nothing 19; ids/file names are fresh per run and the jail binds only /usr and its scratch dir.
- Residual: `checksEvaluated` is not compared (declared), so a report may violate that contract field and still read 19+; the counter alone does not certify it.

Commands (all exit 0 unless noted): `sha256sum` on both tools; `python3 -B rulepatch.py --manifest t/mN.json` for N∈{7,8,9,10} (exits 1,0,0,2 as above); `git diff af43a50f b0ab7f60 --stat`; `git cat-file -e 424aa248:.ufo/waves/round-37/sealed/cases.json`. No process left running.
