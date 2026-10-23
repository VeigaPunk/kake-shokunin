# Round-38 C2 real-run inputs (12 retained live robots.txt files)

Owner: `KakeR38.ExecRealRunPrep` (leaf seat, wave 1). Advisory input for the L1 and the
non-author closure; not a claim, not a verdict, not a sealed counter.

## What this is

The round-37 real-run manifest (55 checks over 12 hosts whose `/robots.txt` bodies were
fetched once in round 37 and retained) extended with 36 checks that exercise the round-38
C2 contract rules **(h)**, **(i)** and **(k)** on the same retained bodies, plus six (h)
fault manifests. No new fetch was made; the robots bodies are byte copies of
`.ufo/waves/round-37/realrun/robots/*.txt` and their sha256 values were re-checked against
the round-37 fetch receipts (`robots/receipts.json`) at build time.

- `manifest.json` — 91 checks: the 55 round-37 checks kept verbatim (only `robots` is
  re-pointed at `robots/…`) plus 36 new checks (3 per host).
- `manifest.strict.json` — the contract-field-only projection of `manifest.json`.
- `manifest.h-*.json` — six (h) fault manifests, each referencing the same retained files.
- `expectations.json` — the declared oracle, hand-written from the public contract text:
  exact expected exit, verdict, `checksEvaluated`, findings per manifest, and the per-check
  declared outcome with its quoted deciding lines. No sealed case was read, listed, copied
  or run; these expectations come from SCORECARD.md's round-38 text only.
- `justifications.md` — one human-readable justification block per new check (rendered from
  `expectations.json` by `render_justifications.py`).
- `build_r38_manifest.py` — builds the manifests and the oracle; asserts every quote
  verbatim at its line in the retained body and every body sha256 against the receipts.
- `run_realrun.py` — runs any `robots_audit.py` over every manifest and compares its report
  exactly (exit, verdict, `checksEvaluated`, finding multiset) with the oracle.
- `base/` — the base-tool run (`af43a50f`, tool sha256 `944d2f51…d3e5`): one receipt per
  manifest plus `summary.json`.

## New checks (36)

Per host, 3 checks. Eleven hosts get one implicit-allow check (k) on `/robots%2Etxt` or
`/%72obots.txt`, one URL carrying an excluded ASCII character (i) whose correct outcome is a
check fault, and one ordinary percent-encoded path decided by a quoted rule line (e).
en.wikipedia.org gets both escape forms (`%2E` and `%72`), under `UbiCrawler`, plus its
excluded-character check — those two are the (k) checks where a raw-path comparison and the
contract disagree. On the other eleven hosts the file's rules already allow `/robots.txt`, so
those (k) checks pin the implicit allow without discriminating against the base tool. 36 new
checks in all, 3 per host.

Excluded characters used by (i), one per host: space U+0020, `"`, `\`, `{`, `|`, `^`,
`` ` ``, `}`, `>`, `<`, U+0001 (control), U+007F (DEL).

## Declared reports

| manifest | exit | verdict | checksEvaluated | findings |
|---|---|---|---|---|
| `manifest.json` | 2 | `could-not-evaluate` | 79 | the 12 (i) checks, `check_invalid` |
| `manifest.h-long-status.json` | 2 | `could-not-evaluate` | 1 | `h-long-status-5000` `check_invalid` |
| `manifest.h-unused-bigint.json` | 0 | `clean` | 2 | none |
| `manifest.h-nan-unused.json` | 2 | `could-not-evaluate` | 0 | `{null, input_invalid}` |
| `manifest.h-infinity-status.json` | 2 | `could-not-evaluate` | 0 | `{null, input_invalid}` |
| `manifest.h-neginfinity-status.json` | 2 | `could-not-evaluate` | 0 | `{null, input_invalid}` |
| `manifest.h-float-status.json` | 2 | `could-not-evaluate` | 1 | `h-float-status-1e400` `check_invalid` |

`manifest.json`'s 13 (k) checks and 11 percent-path checks are allowed by their `expect`
field and must produce no finding. The 12 (i) checks keep `expect: "allow"` because that
field's domain is unchanged by the round-38 amendments (`"allow"`/`"disallow"`; round-37
rule (f)); their declared outcome is the check fault, and `expectations.json`
(`newChecks.<id>.declaredOutcome`) is the oracle. Writing `"expect": "check_invalid"` would
itself be a check fault under (f), so both the base and any built tool would emit
`check_invalid` for the wrong reason and the divergence would disappear; the fault here is
decided by the URL characters alone.

## Running the built tool (L1)

```
cd /fast/scratch/hyaku/kake-r38w1/ExecRealRunPrep/realrun
TMPDIR=… python3 -B run_realrun.py --tool <path-to-built>/scripts/robots_audit.py --out after
```

Exit 0 = every declared report matched; 1 = at least one mismatch; 2 = a run could not be
evaluated (missing tool, timeout, unparseable stdout). Every receipt records the tool's
sha256, the manifest's sha256, the exact command, exit, stdout, stderr, observed report,
declared report and the differences. A same-tool rerun replaces the receipts in `--out`.

## Base-tool result (already run)

Tool: `af43a50fa399881eead9381d835b78a015e277a6:scripts/robots_audit.py`, sha256
`944d2f51f396fb6e1ba3c7cf07112eb3f55d011e9bbc16bb1a59af517be1d3e5`. Command:

```
python3 -B run_realrun.py --tool ../base-tool/robots_audit.py --out base   # exit 1
```

6 of 7 manifests mismatch, 1 matches. On `manifest.json` the base evaluates all 91 checks
and reports only the two `UbiCrawler` (k) checks as `blocked` (raw path compared before
normalization): verdict `failed-policy`, exit 1, `checksEvaluated` 91, and none of the 12
(i) `check_invalid` findings. (h): the base reads `NaN`/`Infinity`/`-Infinity` as floats,
fails a manifest holding a 5,000-digit integer (Python's 4,300-digit conversion limit) as
`input_invalid` with nothing evaluated, and gets the `1e400` float-status case right.

## Limits

- The only network use in this directory's provenance was round 37's fetch; this seat made
  no request. The retained bodies are as recorded there, not re-verified against the live
  hosts in round 38.
- The checks are synthetic URLs over live files: they test the tool's manifest/check
  handling and implicit-allow comparison, not crawling behaviour.
- The harness is not part of the tool and is not a sealed counter; it compares declared
  reports and says nothing about admission.
- The 5,000-digit probes are a JSON-number length probe, not the contract's 64 MiB bound.
