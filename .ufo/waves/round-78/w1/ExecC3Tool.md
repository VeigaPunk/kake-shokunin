# ExecC3Tool — C3 offline meta-robots audit tool (round 78, w1)

Seat: `ExecC3Tool`, kake lane round 78, attempt 1, wave w1.
**Verdict: delivered.** `scripts/meta_robots_audit.py` implements frozen §C3 as
corrected by amendments 1–4, selftest `selftest: 94/94 passed` (exit 0), and the
tool scores 36/36 on the matrix's rebuilt frozen cases; the real-input run over the
8 retained served pages exits 0 with every page matching its declared effective set.

## 0. Deliverables

| Path (relative to lane root) | sha256 |
|---|---|
| `scripts/meta_robots_audit.py` | `886e88618f7064fb32b95f469ce825bd405b5ae943ba3e100bc0c645cf560ba3` (59,428 B) |
| `.ufo/waves/round-78/w1/ExecC3Tool/real-manifest.json` | `b1d2314e06aa063313f9c229300fa65ce550adbb8456c9cac7c54dff97c0f1b2` |
| `.ufo/waves/round-78/w1/ExecC3Tool/realrun.txt` | `5ab71927d8eaed7789c375f93e06601a0598d18b0e1e044f20def7c1ed27c3e5` |

Nothing else in `scripts/` changed; no commit/push/stash/checkout was run; no tool
was installed or upgraded. Interface points were coordinated with `ExecC3Matrix`
over `agent://` (interface note + amendment deltas + final digest) and with L1
`KakeR78` (amendments 1–4 blockers, final summary).

## 1. CLI

```
meta_robots_audit.py --manifest PATH [--root DIR] [--json] | meta_robots_audit.py --selftest [--work DIR]
```

- Manifest `kake-meta-robots-manifest/v1`: `{"schema", "agents" (optional,
  default `["robots"]`), "checks": [{"id", "path", "url"}]}` — no `expect`
  (amendment 2 B1; an `expect` key, if present, is never read — selftest case
  `p18_expect_key_never_read` proves the label leak is closed).
- `--root` defaults to the manifest's directory; `path` resolves under `--root`
  (with a manifest-dir fallback) and must not escape it.
- `--json` prints exactly one object: success
  `{"version":1,"checks":[{"id","effective","findings"}]}`, fault
  `{"version":1,"error":"<code>"}`. Human summary without `--json`; only the
  JSON form is compared (B2).
- Exit: 0 no findings in any processed check · 1 any finding (amendment 4) · 2
  input/check fault with code `missing_file` / `duplicate_check_id` /
  `bad_manifest` · 64 usage. Repeated options are usage errors; `--selftest`
  rejects `--manifest`/`--root`/`--json`; `--work` is additive house style
  (defaults to the system temp dir, honours `TMPDIR`).

## 2. Selftest

```
$ cd /home/vgpnk/Projects/shokunin/kake-shokunin && TMPDIR=$HYAKU_SCRATCH/kake-r78/ExecC3Tool \
    python3 -B scripts/meta_robots_audit.py --selftest --work $HYAKU_SCRATCH/kake-r78/ExecC3Tool/work
selftest: 94/94 passed
exit=0
```

94 = 91 fixture cases + 3 harness checks (byte-identical repeat run; exact
`{"version","checks"}` shape; ≥40 floor). The 91 fixtures cover all 36 frozen ids
of amendment 3 §C4 (in table order, exit/effective/findings verbatim) plus parser
corners (comments, script raw text, attribute order/unquoted/duplicated values,
noscript-in-head, `http-equiv`-only meta, unterminated tag at EOF), merge corners
(`all`+`noindex`, `none`+`index`, earliest `unavailable_after` across offsets,
RFC 822 weekday/numeric zones, RFC 850 rejection), every finding id, and the three
fault codes. Corrections made during convergence after L1 review: RFC 822 weekday
comma merged across the content comma-split (m23); RFC 850 yields
`invalid_value` plus `unknown_directive` for the orphan fragment (m25); p18
manifest id aligned with the case name. No production behaviour changed for any
frozen case.

Matrix cross-check (this seat, read-only, working-tree tool vs
`.ufo/waves/round-78/cases`): `cases=36 correct=36 wrong=0` comparing exit code,
`effective`, and `findings` against each `expect.json` (g34/g35 compare the
`error` string).

## 3. Real-input run (round 76 population)

Command (exit 0):

```
$ cd /home/vgpnk/Projects/shokunin/kake-shokunin && python3 -B \
    scripts/meta_robots_audit.py \
    --manifest .ufo/waves/round-78/w1/ExecC3Tool/real-manifest.json \
    --root /home/vgpnk/Projects/shokunin/kake-shokunin --json
```

Population honesty: 12 named surfaces under `.ufo/waves/round-23/live/`; **8**
retain served `page.html` (`fetch.json` status 200, sha256 verified 8/8 against
`fetch.json`). The other 4 — `charter-kimi`, `lucario-kimi`, `plazir15-kimi`,
`plazir27-kimi` — retain only `audit.json` + `fetch.json` (404, 13,409 B
placeholder body, no HTML bytes) and are reported not retained, never counted
clean or as an error (same population round 76 amendment 1 fixed).

Declared expectation per page (derived from the retained bytes by this seat, not
by the tool): 7 pages declare no `<meta name="robots">` at all → default
`["follow","index"]`; `plazir15-ghp` declares
`<meta name="robots" content="index,follow" />` in `<head>` → `["follow","index"]`.

Observed (`realrun.txt`, both JSON and text forms, both exit 0): all 8 pages
`effective=["follow","index"]`, `findings=[]`. Every page's audit output matches
what it declares — the real-run smoke. Findings are data, not defects: there are
none, and no retained page was edited.

## 4. Amendments applied (frozen corrections, implemented in order)

- **A1** body-section matching metas join the effective set and are also
  reported `meta_robots_tag_outside_head`.
- **A2/B6** `unavailable_after` accepts RFC 3339 full-date, RFC 3339 date-time
  (lowercase `t`/`z` permitted) and RFC 822-style `[EEE,] D Mon YYYY HH:MM:SS
  ZONE` with the B6 zone list or `±HHMM`; RFC 850 is not implemented →
  `invalid_value`.
- **A3** `noarchive`/`nocache`/`nositelinkssearchbox` are ignored rules →
  `meta_robots_ignored_rule`; `indexifembedded` is an effective, non-collapsing
  token.
- **B1–B4** the tool never reads `expect`; `meta_robots_expected_mismatch` was
  removed from the vocabulary (closed set of five ids); stdout schema is frozen;
  correctness is exit+effective+findings vs the matrix's `expect.json`.
- **B5** selftest is scored: final line `selftest: P/T passed`, P==T≥40, exit 0.
- **C2** declared-after-collapse merge; default pair whenever no valid rule
  survives (so `g11/g13/g16/g32` and empty/missing content all render
  `["follow","index"]` with their finding); `max-snippet:0` renders `nosnippet`
  and suppresses the snippet family only — a declared `max-video-preview:-1`
  survives (frozen g26 = `["max-video-preview:-1","nosnippet"]`).
- **A4** finding-bearing cases exit 1 (supersedes amendment 3 §C4's exit column).

No deviation from the frozen contract beyond the amendments was needed; where the
frozen grammar left a case undecidable I stopped and asked (g27's four-token list
and the exit column were L1-corrected in amendments 3–4, not silently guessed).

## 5. Decisions where the frozen grammar was ambiguous

Each is implemented once and documented in the module docstring:

1. **Schema strictness** — the manifest `schema` must be exactly
   `kake-meta-robots-manifest/v1`; no `version` alias (a `version: 1` manifest is
   `bad_manifest`).
2. **Path resolution** — `path` is relative; absolute paths are `bad_manifest`;
   resolution is realpath-containment-checked against `--root` with a manifest-dir
   fallback (the matrix invokes with `--root <case>`, which alone suffices).
3. **Head scope** — only an explicit `<head>` element scopes placement; a
   `<body>` start tag closes the head; documents omitting `<head>` have no implied
   head (their metas are outside-head findings that still join, per A1).
4. **Scanner tolerance** — comments, doctypes, CDATA and processing instructions
   are skipped, as is the raw text of `script`/`style`/`textarea`/`title`;
   attribute values are HTML-unescaped; the first occurrence of a repeated
   attribute wins; a `<meta>` unterminated at EOF is not an element.
   `template`/`svg`/`math` subtrees are not specially skipped (the contract
   states none).
5. **Missing `content`** is identical to empty content → `empty_content` (B6).
6. **Integer grammar** — `-1|[0-9]+`; leading zeros accepted and normalised to
   decimal; `+5`, `-2`, embedded spaces are `invalid_value`.
7. **`nosnippet` domination** — the literal token drops both numeric families;
   `max-snippet:0` drops only the snippet family (frozen g26); `max-image-preview`
   is never dropped by `nosnippet`.
8. **`all`/`none` expansion** — kept per the frozen contract (`all` →
   index,follow even though the source calls it a no-op), so `all`+`noindex`
   yields `["follow","noindex"]` and `none`+`index` yields `["nofollow","noindex"]`.
9. **`unavailable_after` details** — the value is trimmed after the first colon;
   a date-only value is midnight UTC; B6 named zones use their real UTC offsets
   (`EST=-5h` … `PDT=-7h`) and `±HHMM` is honoured; the earliest instant wins with
   ties broken by the lexicographically smallest literal; because content splits
   on commas, an RFC 822 weekday is merged with one following fragment before
   parsing, and a failed merge reports `invalid_value` on the directive token
   while orphan fragments are processed normally (RFC 850 therefore yields
   `invalid_value` + `unknown_directive`).
10. **Default rule** — the pair `["follow","index"]` is emitted whenever the
    collapsed set is empty (no matching element, empty/missing content, or only
    invalid/unknown/ignored tokens); a matching element with only non-effective
    tokens is never silently dropped (the reason is a finding).
11. **Findings granularity** — one finding per offending element/token;
    per-check lists are sorted and de-duplicated; exit 1 if any check reports any
    finding.
12. **Faults** — structural validation (ids, paths, urls, duplicates) runs before
    any file read; the first fault short-circuits to the error object with its
    code; `bad_manifest` covers JSON/schema/shape faults, `missing_file` an
    unreadable page, `duplicate_check_id` a repeated id.
13. **`agents`** — non-empty strings; duplicates collapse; an empty list matches
    nothing (every page defaults); matching is ASCII case-insensitive with no
    whitespace trimming of the `name` value.
14. **`url`** — must be a string, otherwise `bad_manifest`; it is carried through
    and never fetched (offline guarantee).
15. **Empty `checks`** — a valid manifest with zero checks prints
    `{"version":1,"checks":[]}` and exits 0.
16. **Determinism** — JSON is emitted compact with sorted keys and a trailing
    newline; repeated runs are byte-identical (harness-verified).

## 6. Blockers raised and closed

- g27's four-token expected list (amendment 2 B6) was unreachable under the
  frozen merge; L1 corrected it to `["indexifembedded","noindex"]` (amendment 3).
- Exit codes for finding cases (amendment 3 §C4 said 0) were corrected to 1 by
  amendment 4; implemented.
- Fault `error` codes were unnamed in B2; L1 froze `missing_file` /
  `duplicate_check_id` / `bad_manifest` (amendment 3 C3); the matrix uses the same
  strings.

## 7. Scratch

All fixtures, the selftest `--work` tree and the debug dirs lived under
`/fast/scratch/hyaku/kake-r78/ExecC3Tool/` and were removed before this report;
receipts are copied into `.ufo/waves/round-78/w1/ExecC3Tool/`. Nothing was written
outside the lane and the seat's scratch.
