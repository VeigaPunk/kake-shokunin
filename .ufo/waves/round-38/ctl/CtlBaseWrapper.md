# CtlBaseWrapper — round-38 C1 pre-freeze control (cheapest wrapper around the base tool)

No contact with `/fast/scratch/hyaku/kake-r38/`; the round-38 counter was not run. No tool installs
(host python 3.14.8, `/usr/bin/bwrap` already present).
## Built (two single-file stdlib tools, CLI `--manifest PATH`)
Both embed the base bytes verbatim (embedded literal sha256 `944d2f51…d3e5`, verified), `exec` them
under a non-`__main__` name (the base's own `raise SystemExit` never fires), then wrap:

| file | sha256 | bytes | lines (incl. 1 base-literal line) | wrapper lines |
|---|---|---|---|---|
| `/fast/scratch/hyaku/kake-r38ctl/CtlBaseWrapper/ctl_min.py` | `a5a5fc0bbbbdd16ec8708385a4c867db2ed6521fae882f8ed0aa3b757c223317` | 24818 | 91 | 90 |
| `/fast/scratch/hyaku/kake-r38ctl/CtlBaseWrapper/ctl_care.py` | `3215ae1a2c31538167109c1436d59597742728f381a60f621f6759cc37a9da5a` | 23322 | 73 | 72 |

`ctl_min.py` (deliberate shortcut — string-blind, no contract modelling):
- (h) `if b"NaN" in raw or b"Infinity" in raw: input_invalid`. Approximates "…outside a string are
  not JSON"; diverges on `NaN`/`Infinity` **inside a string** (must be evaluated) and does not handle
  long integers at all: json's 4300-digit `int` limit surfaces as `input_invalid` instead of
  `check_invalid`, and a long number in an unread field wrongly faults the manifest.
- (i) one regex over each parsed `url` (complement of the contract's ASCII alphabet), findings for
  those ids rewritten to one `check_invalid`. Character set exact; diverges only by rewriting by id
  (a duplicate-id check's finding can be collapsed).
- (k) `unquote(urlsplit(url).path) == "/robots.txt"` with `query == ""`; then drop `blocked` / add
  `exposed`. This is **exact**, not an approximation: no reserved escape decodes into a letter of
  `robots.txt`, so `unquote` and rule (e) normalization agree on this one target. Does not honour
  `checksEvaluated` (the judge ignores it). First version read the manifest before the base's `stat`
  guard and blocked on selftest fixture `g02-manifest-is-a-fifo` (>400 s, killed); with the guard
  restored it is 137/137.

`ctl_care.py` (same hacks, but following the sentences):
- (h) string-aware scan: raise iff `NaN`/`Infinity` occurs outside a JSON string; mask digit runs
  ≥4000 outside strings to `0`, after rejecting a leading-zero number JSON does not allow. The value
  substitution is safe because no contract-read field accepts a 4000+ digit value (a huge
  `robotsStatus`/`version` is out of range either way). 64 MiB exact-size manifest: 0.22–0.31 s.
- (i) the same character regex wired into `parse_http_url` before any parsing (base's own accounting
  and finding shapes then apply); non-ASCII kept.
- (k) `path_to_match` returns the normalized path, so the base's own `path == "/robots.txt"`
  compares normalized; query/case/kept reserved escape fall through to the rules.

## Evidence (my own contract-derived suite, not the sealed cases)
- 24-case suite in `/fast/scratch/hyaku/kake-r38ctl/CtlBaseWrapper/work/`: base 10/24, min 20/24,
  care 24/24 (min's fails: NaN-in-string; long `robotsStatus`; long number in an unread field).
- Differential fuzz, 60 random manifests × 6 checks, base vs care: 6 diffs, every one a check whose
  normalized path-to-match is exactly `/robots.txt`; no other regression. `normalize` idempotent.
- `python3 -B selftest_tip.py --tool ctl_{min,care}.py` → 137/137, exit 0 (base 137/137).
- `python3 -B .ufo/waves/round-37/sealed_count.py --root . --tool-file <ctl> --key-revision 424aa248…`
  → `passed 28, cases 28, met true`, exit 0, for both. A wrapper is invisible to both harm instruments.
- Same bwrap argv as the counter (`--clearenv`, `PATH=/usr/bin`, LC_ALL=C.UTF-8): both reports, exit 0/2.
## Expected round-38 score
- `ctl_min.py`: 17–18 of 20 (most likely 18): g/d/i/k (16) + the pure NaN/Infinity-outside cases;
  fails every j-case whose expected run holds a NaN/Infinity in a string or a long integer, and a
  64 MiB-digit run (it returns `input_invalid`). If the string-blind and long-integer failures land
  in the *same* sealed case, 19 → met, i.e. the (h) cases under-cover "outside a string" and the
  counter/target is wrong.
- `ctl_care.py`: 20 of 20 (19 at worst). **It meets the predicate while changing zero bytes of the
  tool.** Honest classification: not a work-skipping shortcut — it implements the three rules (a
  monkeypatched repair in the wrapper file). If it scores ≥19 the declaration's rule "a control that
  meets the predicate means the counter or target is wrong" fires on a control that is not a
  shortcut; the L1 must decide whether "the tool gains three rules" is behavioral (then this is a
  legitimate repair, nothing wrong) or structural (then the claim must say so — the frozen counter
  cannot see code shape: exit, verdict and findings are the whole judge).
- Impacted axes: operability (the only part text hacks cannot fake is (h) string-awareness and the
  long-integer split); freshness untouched. Declared but worth knowing: the judge does not compare
  `checksEvaluated`, so a build can meet C1 with a wrong count (min does exactly that after any
  rewrite to `check_invalid`).
## Commands (exit codes)
`git show af43a50f:scripts/robots_audit.py | sha256sum` → `944d2f51…d3e5` (0); 24-case suite runs →
as above (each under `timeout 30`); selftest 137/137 (0); round-37 counter 28/28 `met true` (0);
bwrap smoke → expected reports (0/2); 64 MiB edge → care ≤0.31 s, min ≤0.22 s. The process left by
the killed FIFO stall was killed; no strays remain.
