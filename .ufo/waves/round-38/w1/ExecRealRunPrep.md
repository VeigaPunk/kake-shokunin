# Round-38 w1 — ExecRealRunPrep (complete)

Leaf seat; no subagents, no tool installs, no network request, no Git/jj mutation. I never listed,
read, stat'ed or searched `/fast/scratch/hyaku/kake-r38/` or `kake-r38ctl/`, and ran no round-38
counter. The only lane write is this report; deliverables live under
`/fast/scratch/hyaku/kake-r38w1/ExecRealRunPrep/realrun/` (12 retained round-37 robots bodies; no
new fetch; each body's sha256 re-checked against the round-37 fetch receipts at build time).

**Manifest.** `manifest.json` (sha256 `9e683943…989a9`): 91 checks = the 55 round-37 checks
verbatim (only `robots` re-pointed at `robots/…`; 55/55 byte-identical otherwise) + 36 new, 3/host:
- 13 (k): `/robots%2Etxt` or `/%72obots.txt`, expected allow on the normalized `/robots.txt`. Both
  forms on en.wikipedia.org under `UbiCrawler` (group `Disallow: /`, lines 27–28) — the two checks
  where a raw-path comparison and (k) disagree; on the other 11 hosts the rules already allow
  `/robots.txt` (anchors).
- 12 (i): one URL per host with an excluded ASCII character (space, `"`, `\`, `{`, `|`, `^`, `` ` ``,
  `}`, `>`, `<`, U+0001, U+007F), expected check_invalid.
- 11 (e): ordinary percent-encoded paths — `%61`/`%70`/`%4D` decoded (disallow where a quoted rule
  covers the decoded path), `%2F` kept (allow where decoding would wrongly disallow, e.g.
  `/api%2Fv1` vs `Disallow: /api/`).

**Faults.** Six (h) manifests over the same files: 5,000-digit out-of-range status; 5,000-digit
integer in an unread field; `NaN` in an unread field; `Infinity` and `-Infinity` as status; `1e400`
as status. Separate files because a manifest `input_invalid` (or the base's integer-digit parse
failure) would void the shared manifest.

**Oracle and evidence.** `expectations.json`: exact exit, verdict, `checksEvaluated` and finding
multiset per manifest, plus per-check declared outcome and quotes; declared main report exit 2,
`could-not-evaluate`, 79 evaluated, the 12 (i) `check_invalid` findings. `justifications.md`:
per-check deciding line(s) + why (hosts at :15–158; the two Wikipedia (k) checks at :77/:80,
quoting L27 `User-agent: UbiCrawler`, L28 `Disallow: /`; (h) at :159–190). `run_realrun.py`
(exact-report comparer, records tool sha256), `build_r38_manifest.py` (asserts every quote and body
hash), `verify_inputs.py`, `summarize_run.py`, `README.md`.

## Commands, exits, observed

    python3 -B build_r38_manifest.py                            exit 0  91 checks, 36 new, 12 faults
    python3 -B <lane>/.ufo/waves/round-37/realrun/validate_manifest.py manifest.json --evidence
                                                                exit 0  faults [], checks 91, quotes 121
    python3 -B verify_inputs.py                                 exit 0  87 self-checks, ok true
    python3 -B run_realrun.py --tool ../base-tool/robots_audit.py --out base
                                                                exit 1  6 of 7 mismatch, 1 matches
    python3 -B ../base-tool/robots_audit.py --manifest manifest.json
                                                                exit 1  base/direct-main.txt

Base tool `af43a50fa399881eead9381d835b78a015e277a6:scripts/robots_audit.py`, sha256
`944d2f51f396fb6e1ba3c7cf07112eb3f55d011e9bbc16bb1a59af517be1d3e5`; Python 3.14.8 recorded in
every receipt. Observed vs declared (`base/`): `manifest.json` failed-policy/exit 1/91 evaluated/2
blocked (`r38-k-en_wikipedia_org-pct2e`, `-pct72`) vs could-not-evaluate/exit 2/79 evaluated/12
check_invalid — the base has no (i) rule (the 12 (i) checks evaluate as allow, no finding) and
compares the implicit allow on the raw path. `h-long-status` input_invalid/0 vs check_invalid/1
(Python's 4,300-digit int limit); `h-unused-bigint` input_invalid/0 vs clean/2 (same limit);
`h-nan-unused` clean/2 vs input_invalid/0 (`json.loads` accepts NaN); `h-infinity`/`h-neginfinity`
check_invalid/1 vs input_invalid/0; `h-float-status` (1e400) matches check_invalid/1 (anchor).

## Evidence and hashes (full list in `realrun/MANIFEST.sha256`)

`manifest.json` `9e683943476eb918f499b3337066b347409046979338f2670049ff6d16b898a9`; `expectations.json` `4c5eb911f861677d1073f910fb219401bb1b79c0a59a94f8fad5c13eef3d5dee`
`justifications.md` `f6950772e39735a98ae7a862dd375996be5f001e187dc85a80348e84df7a8f81`; `run_realrun.py` `f8c8db361b8f892e3adb0f37587f41461d74fdf1a1ba50d288b64bec262a2d80`
`build_r38_manifest.py` `c89fc2aff28dd66583547604acf6e76346cdc935563e897efd10deefe9d9a867`; `README.md` `1633d03796835c799ec38b7217f9d9f8f08011bf0387ffb63776ef4efb0f0708`
`base/summary.json` `8259476327901490f8b290efd8f1a2fc360ac6d081c46f058d1e4305e1397b41`; `base/SUMMARY.md` `83709fc50fdb2ab80956e1993504dda27817e0d196ba381c37ba53c69fec92a3`
`base/direct-main.txt` `52e4215ca1fac1076a4cc6a64602972e95b055632d6ff95826aa024d0faf81c8`; `base/receipt-manifest.json` `7c6b309c7ae23ed1df18206f0f862825fc07a7152c8532490d6169a071d20dfb`.

## For the L1

`cd /fast/scratch/hyaku/kake-r38w1/ExecRealRunPrep/realrun && TMPDIR=<tmp> python3 -B run_realrun.py`
`--tool <lane>/scripts/robots_audit.py --out after` — exit 0 = all seven declared reports matched;
receipts name the built tool's sha256. The 12 (i) checks keep `expect: "allow"` because that field's
domain is unchanged; writing `check_invalid` there would itself be a check fault and make base and
built tools agree for the wrong reason. Oracle: `expectations.json` → `newChecks.<id>.declaredOutcome`.

## Limits / not verified

- (k) discriminates against the base on 2 of 13 checks (Wikipedia/UbiCrawler); 11 pin the allow
  where rules already allow `/robots.txt`. The 5,000-digit probes test JSON-number length, not (h)'s
  64 MiB/20 s bound. Robots bodies are round-37 copies, not re-fetched; synthetic URLs over live
  files; this harness is evidence, not a sealed counter; no admission.
- Not run: the built tool; `robots_audit_selftest.py` 137/137 and the round-37 counter 28/28 harm
  instruments (L1's gate); any sealed round-38 counter.
