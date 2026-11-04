# ScribeKnowledge — round 83 wave w1

**Verdict:** PASS (scribe scope). C2's knowledge entry and the `S456` registry row are written and
re-derived from bytes: 18/18 quoted spans in the entry are literal substrings of the retained RFC
9111 file, the row is eleven cells inside `## Registry`, and `sources-census.sh validate` exits 0
with no new finding. One scout-render defect and one unusable literal command form are recorded
below; neither blocks the deliverable.

## 1. Inputs and commands

| Step | Command | Exit |
|---|---|---|
| Read contract | `read .ufo/waves/round-83/contract.md` | 0 |
| Hash retained RFC | `sha256sum .ufo/waves/round-83/w1/ScoutSources/rfc9111.txt` | 0 |
| Re-derive moved headers from both capture trees | Python: load `round-81/capture/*/response.json` and `round-82/capture/*/response.json`, canonicalise, diff | 0 |
| Re-hash receipt | `sha256sum .ufo/waves/round-83/controls/after-c2-classes.txt` | 0 |
| Validate registry | `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <lane>/corpus/SOURCES.md` | **0** |
| Span audit | receipt `.ufo/waves/round-83/w1/ScribeKnowledge/span-check.txt` | 0 |

Retained source: `rfc9111.txt`, 84,477 B, sha256
`aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e`, fetched once at
`2026-11-04T13:29:41Z` by `ScoutSources` (HTTP 200, no redirect). This seat opened no socket and
confirms the digest by re-hashing the retained copy.

## 2. Entry — `corpus/knowledge/header-change-classes.md` (new)

15,184 B, 191 lines, sha256 `947c7f23831a84ea0d037181e1411d895ce0879c5216cc7514c17e0e5ef13511`.
Provenance trio on lines 1–3 (`source:` with `S456` + URL + per-section anchor lines, `verified-at:`
with 2026-11-04 and base `826b0061f233ce1dffb9bd6874abc1342a864247`, `recheck:` with the re-open
command and digest), then `ground:` and `scope:`. Sections: why a header diff needs classes; what the
source fixes (quote table); the three verdict-deciding classes (`per-request`, `validator`,
`representation`); `policy` and `unknown`; why an unknown changed header is treated as
representation-bearing; the measured record; limits.

Quote discipline. The entry quotes only raw spans: 18 single-physical-line substrings, each checked
as `span in rfc9111.txt` and as contained in the declared line range (receipt: `table spans 18
failures 0`), plus one fenced block that quotes the RFC as the exact multi-line byte slice of lines
340–342 (`raw=True occurrences=1`). The two other fenced blocks reproduce the classifier receipt's
stdout and are labelled as such. Prose that would otherwise paraphrase a hard-wrapped sentence carries a
line citation instead of quotation marks, so no collapse-rendered string is presented as a quote.

Class provenance is marked, not blurred. The entry states that RFC 9111 uses `validator` and names
its two members, that it does not use `per-request`, `representation` or `policy` as header classes,
and that the decisive treatment of `unknown` is lane policy applied to the source's storage and
merging rules; that derivation carries `[INFERENCE]`.

Measured record section quotes the receipt's own lines verbatim, including the summary
`summary surfaces=3 diffs=14 per_request=14 validator=0 representation=0 policy=0 unknown=0
verdict=same-object`, and adds an independent re-derivation I ran: the moved names are `date`,
`x-fastly-request-id`, `x-served-by`, `x-timer` on `ds4cc-primary` and those plus `x-cache` on
`ds4cc-robots` and `ds4cc-sitemap` (4+5+5=14), with all three body sha256 values equal. That matches
`corpus/knowledge/capture-drift-validators.md` §6's field set, so the two instruments agree on what
moved.

## 3. Registry — `corpus/SOURCES.md` (+1 line)

`S456` inserted after the `S455` row (old line 202) and before `## Paths`; `git diff --numstat`
reads `1 0 corpus/SOURCES.md`, and `grep -c '^| S456 |'` returns 1. Shape: 13 fields on `|`-split
(empty first/last, eleven non-empty cells), no `|` inside any cell, `kind=spec`, `tier=A`,
`status=mined`, `opened=2026-11-04`, `recheck=365d`, `used-by` is exactly
`corpus/knowledge/header-change-classes.md`. Scope cell excludes the lane's class names and bucket
membership; anchor cell names §3.1 (heading 338, quote 340–342), §3.2 (369–388), §4 (466–490), §4.2
(581–599), §4.2.3 (719–738), §4.3.1 (812–850), §4.3.4 (986–988), plus the retained-file provenance.

Census output: W04 warnings only, all pre-existing duplicate-URL pairs over `rfc9110.txt` and other
long-standing rows (`S453`, `S454`, `S455` included); the final line is
`file	ok	/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md` and the exit is 0. No E-code,
no new W04 for `rfc9111.txt`. Receipt: `.ufo/waves/round-83/w1/ScribeKnowledge/census-validate.txt`.

## 4. Findings from the scout cross-check

- **Rendered scout quotes are not raw substrings.** All nine quotes in
  `.ufo/waves/round-83/w1/ScoutSources/quotes.tsv` score `raw=False`, `collapse=True`, and each
  equals its cited line span after whitespace collapse (`span_collapse_eq=True` for 9/9). The tsv's
  `raw_occurrences=1` column therefore describes the underlying byte range, not the string as
  printed. The scout's own §3 says the one-line form cannot occur in the file, so this is a rendering
  convention, not a wrong citation — but it means its table cells cannot be pasted into an entry as
  quotes. The entry uses its own raw spans instead, and the scout's line anchors all reproduce.
- **The scout's §5 boundary is adopted.** RFC 9111 does not use the four lane class names; the
  entry says so and `[INFERENCE]`-marks the unknown treatment rather than attributing it to the RFC.
- **Item command form is unusable.** `python3 -B /home/vgpnk/Projects/shokunin/scripts/sources-census.sh
  validate …` exits 1 with `SyntaxError: unterminated string literal` at line 50: the validator is a
  Bash script. I ran `bash …/sources-census.sh validate --file …` (exit 0, recorded above) and report
  the literal form here rather than silently substituting it.

## 5. Scope, hygiene, tooling

Production writes: `corpus/knowledge/header-change-classes.md` (new) and one row in
`corpus/SOURCES.md`. Receipts: `census-validate.txt`, `span-check.txt`. Report: this file. No other
production path was touched; `git status` also shows `M corpus/QUALITY.md`, which is another seat's
D6 work, not mine. No tool installed or upgraded. Scratch
`/fast/scratch/hyaku/kake-r83/ScribeKnowledge/` was empty and has been removed; no fixture repo, no
network call, no VCS mutation.

## Verdict

**PASS.** The entry carries the required provenance trio, the three verdict-deciding classes, the
unknown-field argument with its lane-policy boundary marked, and the measured record quoting the
committed receipt; the `S456` row is the next unused id, eleven cells, inside `## Registry`, and the
census validates the file at exit 0.
