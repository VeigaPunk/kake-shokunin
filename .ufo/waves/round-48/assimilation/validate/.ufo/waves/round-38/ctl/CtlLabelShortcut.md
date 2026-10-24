# kake-r38-ctl / CtlLabelShortcut — label-keyed shortcut and delegation ceiling
No contact with /fast/scratch/hyaku/kake-r38/ (sealed tree); the round-38 counter was never run; no
lane file written except this report; no tool installed. Impacted axis: operability (C1's surface).
## Files
A. `/fast/scratch/hyaku/kake-r38ctl/CtlLabelShortcut/ctl_label_shortcut.py`
   sha256 `69affa2d6e3b5d306d26191c8251145a11fa8f6b39b29314443e9b1861457fbd` (375 lines) — the
   shortcut control. Decides from surface labels only: no user-agent group parsing. Every
   `allow:`/`disallow:` record after the first `user-agent:` line is pooled and applied to every
   check; matching is raw-value globbing (prefix, final `$`, `*`, longest value wins, allow wins
   ties) over the round-37 normalization used as a plain string transform. The three round-38 edge
   rules are string predicates, so they are exact: `parse_constant` rejects NaN/Infinity,
   `parse_int` returns a sentinel above 1000 digits (nothing converted), the ASCII URL character
   set is scanned, the implicit allow compares `normalize(path)` with `/robots.txt`. Framing
   (usage, manifest shape, check faults, status ranges, verdict, exit) is present because no case
   can pass without it.
B. `/fast/scratch/hyaku/kake-r38ctl/CtlLabelShortcut/ctl_delegate_ceiling.py`
   sha256 `5c80fb01a5714450dfc3678368136c715a6e3796f1bb25d62fd3e5ee5364f0f2` (180 lines) — the
   whole base bytes (zlib+base64, asserted at load to sha256 `944d2f51…d3e5`) exec'd into a private
   namespace, plus three overlays: `json.loads` wrapped (constant reject + digit-length hook),
   `parse_http_url` wrapped (character set), `path_to_match` wrapped to return the normalized path
   so the base's own `path == "/robots.txt"` sentence fires as (k) requires.
## Expected scores and why
A: **14–16 of 20, not met.** j 4/4 ((h) is literal/grammar; 60 MiB of digits is a length test); r
4/4 (the declaration's four examples behave as written in my synthetic run); u 3–4/4 (character set
exact; one companion check may sit in a multi-group file); d 3–4/4 (value-length specificity,
tie-to-allow, final `$`, `*` all agree with (d)); g 0–2/4 (group selection is the one rule that is
not a label: pooling the Alpha group with `*` flips the decision). `synth.py`'s `g_group_conflict`
reproduces it — A reports clean where (c)/(g) says `blocked`; if u/r companions live in multi-group
files, A falls to 11–12.
B: **20 of 20.** B is base + exactly the three amendments, the declaration's own description of the
private reference (`reference.json`, 20/20). A lower score would mean the reference implements
something other than the three rules.
## Counterexample and the round rule it touches
B is the "cheapest wrapper around the base tool" arm, and it meets by construction: base + the three
amendments ≡ the reference. Read with "a control that meets the predicate means this counter or
target is wrong; no reclassification of the control is an option", that arm would force C1's
withdrawal while implementing every rule the claim adds. The rule cannot distinguish a wrapper that
skips work from one that does it. The skipping wrapper is bounded from public receipts: A1 (no
constant reject) 18 fails j1,j2; A2 (no long int) 18 fails j3,j4 — disjoint — so base + (i)+(k) only
is ≤16. Smallest safe correction: define the wrapper arm as "base plus at most two amendments", or
qualify the rule to controls that skip a declared rule; record B as the reference re-measurement,
not a control. The discriminating control is A.
## Which label keys survive the counter
Survive: URL path/query text, userAgent tokens, robots file contents, robotsStatus values, expect
strings, manifest raw bytes (NaN/Infinity, digit-run length, field names), manifest size — sealed
data, not labels about it. Defeated: check ids (fresh `c`+12 hex per run), robots and manifest file
names (fresh 32-hex UUID per file), directory names, and the original-id→fresh-id map; `@ID:`/
`@FILE:` tokens never reach the tool. The fresh-id shape `^c[0-9a-f]{12}$` identifies a counter run
but carries no case information. Consequence: the only label keys that decide correctly are the
three syntactic rules themselves (JSON number grammar, URL character class, `/robots.txt` after
unreserved-escape decoding) — cheap, but implementing them is the claim, not a bypass.
## Counter robustness note
`materialize`'s structured path calls `json.dumps(manifest)`, which raises for integer literals above
4300 digits, and `load_key` parses the key under the same limit; a (h) run carrying a long literal
must be a `raw`/`rawTemplate` run. `reference.json` 20/20 shows the key is materializable today; a
note for the next key edit, not a defect.
## Commands (exit codes)
- `sha256sum .ufo/waves/round-38/sealed_count.py` → `52daff55…6e7b`, the declared pin (0)
- `git show af43a50f:scripts/robots_audit.py | sha256sum` → `944d2f51…d3e5`, the declared base (0)
- `python3 -B synth.py` (10 synthetic contract cases, both tools) → A 9/10, B 10/10 (0)
- `python3 -B ctl_delegate_ceiling.py` (no args) → 64; `ctl_label_shortcut.py --bogus` → 64
- 60 MiB of digits (unread field / robotsStatus): rc 0 / rc 2, 0.09–0.11 s per tool (inside 20 s)
