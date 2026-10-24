#!/usr/bin/env python3
"""Build the round-44 wave-1 spec (build + pre-freeze calibration, 36 seats).

Every item prompt leads with the bytes of /home/vgpnk/.agents/skills/godspeed/SKILL.md
(the host Godspeed binding), verbatim. Seat paths are absolute under the lane repo; the
wave `reportDir` stays lane-relative for the validator.
"""
import json
from pathlib import Path

LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
WAVE = ".ufo/waves/round-44/w1"
SCRATCH = "/fast/scratch/hyaku/kake-r44"

GODSPEED = """/skill:godspeed
You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.
"""

CONTEXT = f"""# Goal
Kake round 44, wave 1 (build + pre-freeze calibration, 36 seats). The lane is kake-shokunin (axes: operability, freshness; domain: web properties and publishing, offline sitemap/manifest auditing). Ordinary software testing of local, offline command-line tools. The L1 (agent id KakeR44) is the only writer of lane history; you are one leaf seat with one item.

Lane repo: {LANE} (read anything there). Your scratch dir: {SCRATCH}/<YourSeatName>/ (create it; keep all temporary files there, never in the lane repo unless your item names the exact file to write).

# The round's two declared claims (context only; do not score them)
- C1 (operability, capability acquisition): a witness class corpus G1-G10 plus the audit driver `c44_audit.py` makes 27 controls that met the round-43 counter v4 (`--classes v4`, blind) witnessed under v5 (`--classes v5`), while the held build (revision 020bc457, tool sha256 914ebdee...) still meets v5 and the four round-42 controls stay red. Counting command: `python3 -B .ufo/waves/round-44/c44_audit.py --classes v4|v5 ...`.
- C2 (freshness): the four r43 ledger figures routed by the round-43 verifier spot-check re-derive from committed receipts at the tip; a checker `scripts/ledger_latest_check.py` exits 0 iff the last statement of each declared figure in LOG.md / SCORECARD.md matches the receipt.

# Frozen artifacts you must not edit (the L1 freezes them after this wave returns)
- `.ufo/waves/round-44/c44_count_v5.py` (counter v5; built from the round-43 v4 by `build_v5.py`; `python3 -B .ufo/waves/round-44/build_v5.py --check` exits 0 today)
- `.ufo/waves/round-44/c44_audit.py`, `.ufo/waves/round-44/controls-27.tsv`, `.ufo/waves/round-44/controls-r43/*` (the 27 round-43 control tools)
- `.ufo/waves/round-44/c44_probe.py` (single-class probe)
Only the L1 commits. You never run git commit/jj/git push, never edit the fleet repo /home/vgpnk/Projects/shokunin, never edit a sibling lane, never touch `.ufo/state/` or the fleet `.ufo/watchdog.log`.

# Class-module contract (items that write `classes/gN_*.py`)
The counter calls `cases(rng, h)` and expects `(units, n)`:
- units are the run-F vocabulary laid out by `layout_f` in `c44_count_v5.py`: `("value", "loc"|"sitemapUrl", v)`, `("foldpair", a, b)`, `("prefixpair", a, b)`, `("pairfile", v1, v2, v3, v4, v5, v6)`; `n` is the number of generated URL values.
- `h` is the counter module itself: use `h.short_url`, `h.tok`, `h.fill`, `h.rcase`, `h.long_port`, `h.TLDS`, `h.ALNUM`, `h.COMMON_HOSTS`, `h.CASE_INVARIANT_DEFECTS`, `h.DEFECTS`, `h.xml_legal`, `h.segment_smu`.
- Deterministic from `rng` only; no I/O, no network, no environment reads, no imports of the control tools. Standard library only.
- Self-test with the probe (never run the full counter; it is 20+ minutes):
  `cd {LANE} && python3 -B .ufo/waves/round-44/c44_probe.py --root . --class G5 --tool-file .ufo/waves/round-44/controls-r43/<control>.py --seed <N>`
  Exit 1 = the control's judgement diverges from the round-41 reference on your class (a WITNESS, required); exit 0 = no witness (fix the class). Copy the probe output into your report and state the seed.
- A witness must be semantic: exit code or stdout bytes differ because the two tools judge the same generated values differently. A timing difference is not a witness.

# Report
Write your report at {LANE}/{WAVE}/<YourSeatName>.md (create the directory if missing). Every `Report:` trailer path the validator renders is relative to {LANE} — write it at {LANE}/<that path>. The report names: what you did, the exact commands you ran, their verbatim output (trimmed to the decisive lines), file paths you wrote, and any blocker. No fabricated output: an unrun check is reported as unrun.

# Bounds and rules
- Files you may write: the one lane path your item names, plus your scratch dir and your report. Nothing else.
- Read-only: the fleet repo, sibling lanes, the frozen artifacts above, all tracked lane files except the one your item names.
- Tool installs are authorized for any tool that helps (official channels only; record tool/version/channel/reason in your report). PACMAN IS PAUSED host-wide: no `pacman -S`, `-Sy`, `-Syu`, `-U`, `-R`; use `uv tool`, `npx`, or an official binary into `~/.local/bin`.
- Never message `agent://all`. Never edit `~/.omp/agent/config.yml`, `mcp.json`, or any route table.
- Report a dead end as a dead end. Do not relabel a non-witness as a witness.
"""


def item(name, role, axes, target, change, acceptance):
    prompt = GODSPEED + f"\n# Target\n{target}\n# Change\n{change}\n# Acceptance\n{acceptance}\n"
    return {"name": name, "role": role, "axes": axes, "prompt": prompt}


CLASS_ACCEPT = (
    "`python3 -B .ufo/waves/round-44/c44_probe.py --root . --class <G> --tool-file <control> --seed <N>` "
    "exits 1 (witness) for every control listed in your target, on at least two seeds; your report pastes "
    "the probe JSON (seed, units, values, ref41Exit/candExit, both stdout sha256) and the file path you wrote."
)

items = []

# --- 10 class modules -------------------------------------------------------
classes = [
    ("ExecG1LongPort", "G1", "g1_longport_grammar.py",
     "controls `portlen-v1-skip-grammar-6plus.py`, `portlen-v5-abbrev-window-6plus.py`, `portlen-v4-cache-portlen.py` (and the benchmark control `buildport-m6-default-branch.py` if it witnesses)",
     "Witness shape: a value whose authority carries a SIX-OR-MORE digit port that is IN RANGE when zero-padded (e.g. `:000080`, `:000443`, `:0065535`) and whose path/query carries one grammar defect (a `%` or a non-ASCII unit). The round-41 tool rejects the grammar (`loc_not_absolute`); the port-length controls skip the grammar scan for authorities with >=6 port digits and then parse a clean URL. Generate about 300 such values (mix `loc` and `sitemapUrl` units), half with the defect in a later path segment so the host lookup still sees the long port. Avoid duplicate ids/paths that would make the two tools agree by accident."),
    ("ExecG2DefaultPort", "G2", "g2_default_port.py",
     "control `buildscheme-M5-default-port-https80.py` (explicit default-port handling)",
     "Witness shape: an `https` loc with an IMPLICIT port (no `:port`) judged against an `https` sitemapUrl that carries an explicit `:443`. The round-41 tool reads both as 443 (in scope); the control maps the implicit https port to 80, so the authority tuples differ (`loc_out_of_scope`). `layout_f` derives the sitemapUrl from the first value of a pairfile: build pairfiles whose first value is `https://<host>:443/sitemap.xml` (the manifest sitemapUrl) and whose other members are clean `https://<host>/<segment>` values. Add the mirror shape (explicit `:80` on http) for completeness. About 60 pairfiles."),
    ("ExecG3EmptyPath", "G3", "g3_empty_path.py",
     "control `buildscope-m5-empty-path.py` (path = parts.path instead of `or \"/\"`)",
     "Witness shape: a clean value with NO path at all (`https://<host>`), whose derived sitemapUrl is `https://<host>/sitemap.xml`. The round-41 tool reads the loc path as `/` and the file scope prefix as `/` (clean); the control reads the path as the empty string and the prefix test fails (`loc_out_of_scope`). Emit about 120 `value`/`loc` units, plus `https://<host>:<port>` forms. The probe must witness on two seeds."),
    ("ExecG4PortScope", "G4", "g4_port_scope.py",
     "control `buildscope-m4-port-dropped.py` (scope compares parsed[:2], dropping the port)",
     "Witness shape: a pairfile whose first value (the manifest sitemapUrl) carries `:8443` and whose second value carries a DIFFERENT explicit port `:9443` on the same scheme+host. The round-41 tool compares scheme+host+port and flags `loc_out_of_scope`; the control compares scheme+host only and, with the path under the sitemapUrl directory, reports clean. About 60 pairfiles, ports varied (8443/9443, 8080/8081, 443/80)."),
    ("ExecG5Prefix", "G5", "g5_prefix_cut_45plus.py",
     "controls `headtail-V1-prefix-cache64.py`, `headtail-V2-headtail-key48.py`, `headtail-V7-prefix-cache45.py`, `prefixcache-p48-noreval.py` (an initial class file already exists; harden it, do not weaken it)",
     "Read the existing `g5_prefix_cut_45plus.py` and make it witness all four controls on at least two seeds. It currently emits 60 cut-pairs at cuts 44/45/48/64/65/80 (defect exactly at the cut) and 40 head+tail-48 pairs (defect in the middle). Report which control each unit kind catches, by running the probe once per control with two seeds. If a control needs a different shape (e.g. the key window is 45 vs 48 vs 64, or the pair order matters because the cache stores the first member), extend the class rather than editing the controls."),
    ("ExecG6Fold", "G6", "g6_fold_pairs.py",
     "controls `casememo-v3-validity-lower.py`, `casememo-v4-validity-lower-short.py`, `casememo-v7-value-lower-nonascii.py`, `casememo-v8-value-casefold-nonascii.py` (case-fold memos)",
     "Witness shape: a `foldpair` whose FIRST member is a clean value and whose SECOND member is the same value with a case-folded non-ASCII LETTER in a LATER path segment (never the first segment: the manifest sitemapUrl is case-sensitive on the first segment). Use U+212A KELVIN SIGN (`.lower()` -> `k`, `.casefold()` -> `k`) and U+017F LATIN SMALL LETTER LONG S (`.casefold()` -> `s`, but `.lower()` is unchanged) so both `value.lower()` and `value.casefold()` memos are hit. The round-41 tool rejects the non-ASCII member (`loc_not_absolute`); the memoised control answers it with the clean member's verdict (clean). Prove the fold collapse in your report: `python3 -c \"print('\\u212a'.lower(), '\\u212a'.casefold(), '\\u017f'.casefold())\"`. About 100 pairs; keep the cased position a letter, never a digit (the round-43 counter's own fold pairs degenerated on digits — this class must not repeat that)."),
    ("ExecG7Bands", "G7", "g7_band_memos.py",
     "controls `repeat-ctl_len_memo_band.py`, `repeat-ctl_depth_memo_band.py`, `repeat-ctl_defpos_memo_band.py`, `repeat-ctl_depth_memo_deep.py`, `repeat-ctl_defpos_memo_late.py` (repetition guard bands)",
     "Read each control's diff against the round-41 tool: the memo keys are (a) the value LENGTH for 6001..199999 code points, (b) the `/` COUNT for values with >=64 slashes and length <=1799, (c) the pair (LENGTH, index of the first `%`) for values with the first `%` at index >=1000 and length <=1799. Witness shape: pairs of `value` units in FIRST-SEEN order — the clean member first, then a member with the SAME key (same length / same slash count / same (length, percent index)) carrying one grammar defect. A process-global memo answers the second with the first's verdict: round-41 flags `loc_not_absolute`, the control says clean. Cover every band and both deep/late variants. Build the long values from `h.FILL`/`h.long_body` or your own filler; keep them under the counter's loc cap (2048 code points for the band memos). About 120 pairs."),
    ("ExecG8Hosts", "G8", "g8_host_tables.py",
     "controls `hosttable-A-expanded46-fixed.py`, `hosttable-B-expanded46-nogrammar.py`, `hosttable-F-provable.py` (static common-host tables)",
     "Read the host tuples out of the three controls (they differ). Witness shape: a `value`/`loc` whose HOST is in a control's table and whose PATH carries one grammar defect (a `%`, `|`, space, `<`, `>`). The round-41 tool flags `loc_not_absolute`; the table answers from the static entry and reports clean. Use hosts from all three tables, one value per host, defect varied; the derived sitemapUrl keeps the same host so scope agrees. About 120 values. Do not import the controls: copy the host strings into your class as data."),
    ("ExecG9PortDigits", "G9", "g9_port_digits.py",
     "controls `portvalue-memo-digits.py`, `portvalue-memo-digits-67.py`, `buildport-m6-default-branch.py` (port-keyed parse caches and the inverted default-port branch)",
     "Two witness shapes. (a) Port-digit cache: two separate `value` units, in order, with the SAME port digits and DIFFERENT hosts (`https://a<...>:8443/x` then `https://b<...>:8443/y`); the cache returns the first parse for the second, so the second's host differs from its own sitemapUrl host -> `loc_out_of_scope`, while round-41 is clean on both. (b) Inverted default branch: a pairfile whose first value (sitemapUrl) is `https://<host>/sitemap.xml` (implicit port) and whose second value carries an explicit `:8443`; the control rewrites the explicit port to the default, so the authority tuples agree and it reports clean while round-41 flags `loc_out_of_scope`. About 60 of each."),
    ("ExecG10Windows", "G10", "g10_headtail_windows.py",
     "controls `headtail-V4-longport-head64.py`, `headtail-V8-longport-tail64.py` (long-port values judged on a 64-code-point window)",
     "Witness shapes. (a) HEAD window: a value longer than 64 code points whose authority carries a ZERO-PADDED IN-RANGE long port (e.g. `:000080`) and whose first path segment crosses code point 64. Round-41 judges the whole value (clean); the control truncates to the first 64 code points, so the truncated path is no longer under the sitemapUrl directory -> `loc_out_of_scope`. (b) HEAD window, defect hidden: the same long-port value with one grammar defect AFTER code point 64 -> round-41 `loc_not_absolute`, control clean. (c) TAIL window: mirror (a)/(b) with the differing part in the first 64 code points and the tail clean (the control keeps only the last 64). About 120 values, each its own `value` unit so its sitemapUrl derives from itself."),
]
for name, gid, fname, target, change in classes:
    items.append(item(name, "executor", ["operability"],
                      f"{gid} class module `{LANE}/.ufo/waves/round-44/classes/{fname}`: make the round-43 controls listed here WITNESS the round-44 counter v5's class run {gid}. " + target,
                      f"Write exactly `{LANE}/.ufo/waves/round-44/classes/{fname}` exposing `cases(rng, h) -> (units, n)` (see the shared contract). " + change,
                      CLASS_ACCEPT))

# --- C2 ledger checker -----------------------------------------------------
items.append(item(
    "ExecLedgerCheck", "executor", ["freshness"],
    f"C2 checker `{LANE}/scripts/ledger_latest_check.py` and its spec `{LANE}/.ufo/waves/round-44/ledger-quotes.json`: prove, per declared figure, that the LAST statement about it in the lane's ledgers matches the committed receipt.",
    f"""Write `{LANE}/scripts/ledger_latest_check.py` (Python 3 standard library, no network) and `{LANE}/.ufo/waves/round-44/ledger-quotes.json`. The checker reads the spec, and for each entry:
- `file` (lane-relative), `pattern` (a Python regex whose group 1 is the number or range), `receipt` (a committed artifact under `.ufo/waves/round-43/`), `derive` (how the expected value is read from that artifact).
Resolve the expected value from the receipt bytes: (1) `verification/l1-rescores/*.json` -> count of distinct `toolSha256` values; (2) `verification/freeze/ref41-base.json` -> `ratios.T1` and `ratios.T5`; (3) `verification/freeze/build-{1,2,3}.json` -> min/max of `ratios.T1` and `ratios.T5`; (4) the round-43 wave composition -> count of `.ufo/waves/round-43/w1/*.md` files plus the settle line of `.ufo/waves/round-43/w1-dispatch-log.txt`.
The declared figures and their committed receipts are, verbatim: SCORECARD "L1 re-scored 18 of 27" vs 14 receipts; LOG "T1 4.27, T5 8.68" vs 4.207/7.047; LOG "T1 1.00-1.02, T5 1.13-1.18" vs 1.004-1.009/1.105-1.215; SCORECARD/LOG "47 reports, 15 dead, 4 live-at-settle" vs 50 reports/15 dead/1 live.
Rule: for each spec entry, take the LAST line in the named file matching the pattern (append-only ledgers put corrections last; `git show master:<path>` if the worktree copy is unavailable) and compare its group 1 to the derived value; print one line per entry (`id verdict quoted=... derived=... path:line`) and a final `ledger-quotes: N figures, M mismatches`; exit 0 iff M==0, 1 if any mismatch, 2 on unreadable input. Add `--selftest` that feeds two synthetic fixtures (one matching, one mismatching) and proves the checker can fail.
Run it before any repair: the four declared entries must show 4 mismatches and exit 1 (that is the C2 "before" receipt — paste the verbatim output and write the receipt to `{LANE}/.ufo/waves/round-44/verification/ledger-before.txt` with a `.exit` companion file holding the exit code).
Do NOT edit LOG.md, SCORECARD.md, the lesson or the receipts: the repair is the L1's."""
    ,
    "`scripts/ledger_latest_check.py` and `.ufo/waves/round-44/ledger-quotes.json` exist; `--selftest` exits 0 and its mismatching fixture is shown red; the before run prints `4 mismatches` and exits 1; `verification/ledger-before.txt` + `.exit` are written; the report pastes the command and output."))

# --- audit hardening -------------------------------------------------------
items.append(item(
    "ExecAudit", "executor", ["operability"],
    f"Harden `{LANE}/.ufo/waves/round-44/c44_audit.py`: `witnessed` must mean a SEMANTIC witness, not `met=false` for any reason.",
    """Change the witnessed criterion to: `met is False` AND `caughtBy` non-empty AND every key in `caughtBy` starts with `G` (a class run), so a timing-bound failure or a v4-run divergence cannot be counted as a class witness. When `--classes v4` is used, print `witnessed` as `0` by construction (there are no class runs) and state it. Keep `--expect blind` / `--expect witnessed` semantics and the receipt layout. Add `--selftest`: two synthetic control rows, one that passes every run and one that diverges on one class run, asserting `witnessed` is 0 and 1 respectively; prove the selftest is able to fail by temporarily breaking the criterion in a scratch copy (report the red run).
Also make the audit record `classKeys` and, for each witnessed control, the exact `caughtBy` class keys in the summary line.
Do not change `c44_count_v5.py`, the class modules or the controls.""",
    "The selftest exits 0 and its red-mode scratch run is pasted in the report; the audit's source shows the semantic criterion; `python3 -B .ufo/waves/round-44/c44_audit.py --root . --controls .ufo/waves/round-44/controls-27.tsv --counter .ufo/waves/round-44/c44_count_v5.py --classes v4 --expect blind --workers 2 --out .ufo/waves/round-44/verification/smoke-v4.json` exits 0 (all 27 blind under the v4 corpus)."))

# --- scouts ----------------------------------------------------------------
scout_plan = [
    ("ScoutPortFamily", "port family (portlen-v1/v4/v5, portvalue-digits/-67, buildport-m6)",
     ["portlen-v1-skip-grammar-6plus.py", "portlen-v5-abbrev-window-6plus.py", "portlen-v4-cache-portlen.py", "portvalue-memo-digits.py", "portvalue-memo-digits-67.py", "buildport-m6-default-branch.py"]),
    ("ScoutFoldFamily", "case-fold family (casememo-v3/v4/v7/v8)",
     ["casememo-v3-validity-lower.py", "casememo-v4-validity-lower-short.py", "casememo-v7-value-lower-nonascii.py", "casememo-v8-value-casefold-nonascii.py"]),
    ("ScoutBandFamily", "repetition-band family (repeat-ctl_len/depth/defpos band, depth-deep, defpos-late)",
     ["repeat-ctl_len_memo_band.py", "repeat-ctl_depth_memo_band.py", "repeat-ctl_defpos_memo_band.py", "repeat-ctl_depth_memo_deep.py", "repeat-ctl_defpos_memo_late.py"]),
    ("ScoutHostFamily", "host-table family (hosttable-A/B/F)",
     ["hosttable-A-expanded46-fixed.py", "hosttable-B-expanded46-nogrammar.py", "hosttable-F-provable.py"]),
    ("ScoutWindowFamily", "head/tail-window family (headtail-V1/V2/V4/V7/V8, prefixcache-p48)",
     ["headtail-V1-prefix-cache64.py", "headtail-V2-headtail-key48.py", "headtail-V4-longport-head64.py", "headtail-V7-prefix-cache45.py", "headtail-V8-longport-tail64.py", "prefixcache-p48-noreval.py"]),
    ("ScoutBuildMutants", "build-mutant family (buildscope-m4/m5, buildscheme-M5, buildport-m6)",
     ["buildscope-m4-port-dropped.py", "buildscope-m5-empty-path.py", "buildscheme-M5-default-port-https80.py", "buildport-m6-default-branch.py"]),
]
for name, family, controls in scout_plan:
    paths = ", ".join(f"`{LANE}/.ufo/waves/round-44/controls-r43/{c}`" for c in controls)
    items.append(item(
        name, "scout", ["operability"],
        f"Independent witness blueprint for the {family}: confirm from the control source what each shortcut does, then produce and RUN a hand-made witness fixture against the round-41 tool and the control.",
        f"""For each control {paths}:
1. Diff it against the round-41 tool (`git -C {LANE} show <REF41_REV>:scripts/sitemap_audit.py`, see `REF41_REV` in `{LANE}/.ufo/waves/round-44/c44_count_v5.py`) and quote the injected lines.
2. State the shortcut in one sentence and the exact value shape that must expose it.
3. Build a tiny v1 manifest by hand in your scratch dir (`{SCRATCH}/<YourSeatName>/`): one XML file plus a JSON manifest with `file`/`sitemapUrl`, and run BOTH tools under the same interpreter (`python3 -B <tool> <manifest>`), copying the tool bytes out with `git show`. Paste both stdout documents verbatim and name the first differing finding.
4. State whether the G-class blueprint named in the wave context (see the executor item for your family) can witness it, and what must be added.
Do not write any file under the lane repo except your report.""",
        "Your report quotes the injected control lines, pastes both tools' verbatim stdout for at least one hand-made witness per control, and states for each whether the planned class shape witnesses it."))

items.append(item(
    "ScoutRegistry", "scout", ["operability"],
    f"Verify the 27-control registry `{LANE}/.ufo/waves/round-44/controls-27.tsv`: every sha256 matches its file, every path exists, every named round-43 seat report exists under `.ufo/waves/round-43/w1/`, and the family tallies sum to 27.",
    "Run `sha256sum` over each listed file and compare to column 5; check existence of the seat reports in column 6; tabulate rows by family and class and state the arithmetic (`5+3+4+5+3+2+1+4=27` or the true decomposition). Report any mismatch as a defect with the exact row. Also confirm no row points at a file that differs byte-wise from the round-43 evidence (compare against `.ufo/waves/round-43/verification/l1-rescores/*.json` `toolSha256` values where present).",
    "The report carries a 27-row table (name, sha match yes/no, seat report yes/no, class) and the exact family arithmetic; every mismatch is named."))

items.append(item(
    "ScoutRef41Semantics", "scout", ["operability"],
    "Establish the round-41 reference tool's exact finding semantics for the six defect shapes the new classes rely on, by running it on hand-made manifests.",
    f"""The reference tool is `git -C {LANE} show <REF41_REV>:scripts/sitemap_audit.py` (REF41_REV/REF41_SHA in `{LANE}/.ufo/waves/round-44/c44_count_v5.py`; verify the sha). In your scratch dir, build one manifest per shape and run it:
(a) a loc with a `%`/non-ASCII grammar defect in the path; (b) a loc with a zero-padded 6-digit in-range port (`:000080`) and a clean path; (c) a loc with an out-of-range 6-digit port (`:123456`); (d) a loc with no path and its sitemapUrl one level up; (e) a loc whose port differs from the sitemapUrl port; (f) a loc with an implicit https port against a sitemapUrl with `:443`.
Paste each manifest's values and the tool's verbatim stdout (`{{"id":..,"status":..,"findings":[..]}}`), and state the finding code each shape produces (`loc_not_absolute`, `loc_out_of_scope`, `clean`, `check_invalid`, ...). This is the oracle the class blueprints assume; name any assumption that is falsified.""",
    "The report pastes the six manifests' decisive values and the tool's verbatim stdout per shape, with the finding code named for each."))

# --- reviewers / critics / etc. -------------------------------------------
items.append(item(
    "ReviewCounterContract", "reviewer", ["operability"],
    f"Review the frozen counter v5 `{LANE}/.ufo/waves/round-44/c44_count_v5.py` (uncommitted, built by `build_v5.py`) against the round-43 v4 it derives from.",
    f"""Verify: (1) `python3 -B .ufo/waves/round-44/build_v5.py --check` exits 0 and the built bytes equal the committed-in-workspace file; (2) the diff from `{LANE}/.ufo/waves/round-43/c43_count_v4.py` contains ONLY the header, PREDICATE, the class-run wiring (`load_classes`, CLASS_DIR/CLASS_MODULES, the `--classes` flag, the runs list) and nothing that changes the equality/timing semantics of runs A-F or T1-T5; (3) the v5 predicate sentence matches the code it describes (the eleven v4 runs and the ten class runs; the ratio bound 2.0; the round-40 baseline); (4) the run denominator: 21 runs in v5 mode (A-F=6, G1-G10=10, T1-T5=5) and 11 in v4 mode; (5) `--classes v4` genuinely generates no class runs and cannot load a class module. Quote line numbers. Name every discrepancy; a clean review states the commands it ran.""",
    "The report shows the diff hunks with line numbers, the `--check` output, the two denominators derived from the code, and a verdict (`sound` / `defect: ...`) per item."))

items.append(item(
    "ReviewAuditDriver", "reviewer", ["operability"],
    f"Review `{LANE}/.ufo/waves/round-44/c44_audit.py` as the C1 counting command's driver.",
    """Check: the `--expect blind` and `--expect witnessed` predicates match the claim sentences (blind = 0 witnessed, exit 0; witnessed = all witnessed AND every build receipt met, exit 0); the receipt keeps every per-control counter receipt under `<receipt-dir>/tools/` so the tally re-derives; errors (missing file, sha mismatch, counter exit 2) are reported and cannot be silently counted as witnessed; `--workers` cannot interleave two tools' receipts (unique output names); the summary records the counter sha256, the seed of each receipt, `caughtBy` keys and the build receipts. Then attack it: create a scratch copy where one control is replaced by the pristine round-41 tool (must be NOT witnessed) and another by a tool with one deliberate semantic change (must be witnessed) and run the audit on that two-row TSV with `--classes v5`. Paste both runs. Do not edit the real file; the driver's owner is seat ExecAudit.""",
    "The report lists the checks with line numbers, pastes the two scratch-audit runs (pristine -> not witnessed; changed -> witnessed), and names any way to fool the driver."))

items.append(item(
    "ReviewInheritedLineage", "reviewer", ["operability"],
    "Re-verify the INHERITED round-44 artifacts that attempt 1 left uncommitted (this round's attempt 2 inherits them): `build_v5.py`, `c44_count_v5.py`, `c44_audit.py`, `controls-27.tsv`, `controls-r43/`, `verification/freeze/control-v4blind.json`.",
    f"""For each: state what it is, whether it re-derives (`python3 -B .ufo/waves/round-44/build_v5.py --check`; sha256 of every control against the TSV; the class modules: which exist and which are missing), and whether it can be trusted for the claim. Read `{LANE}/.ufo/waves/round-44/verification/freeze/control-v4blind.json` and say what it proves and what it does NOT prove (it predates this attempt's freeze and its `tools/` dir is empty). Check the r43 counter bytes it derives from: `sha256sum {LANE}/.ufo/waves/round-43/c43_count_v4.py` must equal `1c3b96610873301b1ea17d123677dd76a86f77edf26020c1ff5ef38221fe8eab`. Name exactly which inherited artifacts this attempt may reuse and which it must discard, with reasons.""",
    "The report has one row per inherited artifact: path, sha256, re-derivation command + result, verdict (reuse / discard with reason)."))

items.append(item(
    "ReviewLedgerCheck", "reviewer", ["freshness"],
    f"Review the C2 checker `{LANE}/scripts/ledger_latest_check.py` and spec `{LANE}/.ufo/waves/round-44/ledger-quotes.json` (owner seat ExecLedgerCheck; if the files do not exist yet, review the declared design and say so).",
    """Attack the rule "the last matching line in an append-only ledger is the current statement": enumerate ways it can be fooled (a later unrelated line matching the pattern; a correction that quotes the stale value; a file whose last line is a historical table). For each, state whether the spec's patterns exclude it. Then run the checker: `python3 -B scripts/ledger_latest_check.py --selftest` and the before run; paste outputs. Re-derive ONE expected value yourself from the receipt bytes (e.g. the count of distinct `toolSha256` under `.ufo/waves/round-43/verification/l1-rescores/`) with an independent `python3 -c` one-liner and compare. Do not edit the tool.""",
    "The report lists the fooling shapes, runs the selftest and the before run verbatim, and re-derives at least one expected value independently."))

items.append(item(
    "CriticClaimC1", "critic", ["operability"],
    "Falsify the C1 claim design BEFORE any claim data is scored: find a way the declared count can be met without the claimed work, or a way the claim overstates what it shows.",
    f"""The claim: under the frozen counter v5, the 27 round-43 controls that met v4 (`--classes v4`: 27/27 blind) are witnessed (`--classes v5`, semantic class-run divergence) AND the held build (rev 020bc457) is met on 3 fresh seeds AND the four round-42 controls plus a junk control stay not met. The skip-work control is `--classes v4` on the same counter bytes: if that already witnesses the 27, the counters are wrong. Attack: (a) is "witnessed" the right observable, or can a control be witnessed for a reason unrelated to the class it was designed to expose (state which `caughtBy` key would have to carry it); (b) does the 27 denominator omit a control the round-43 tally really contained, or include one that is not in `controls-27.tsv`; (c) can the class modules be overfit to the control FILES (reading their source) rather than to a real shortcut class — and does that make the capability claim circular; (d) is the held build usable as harm evidence when it is the same build whose C1 was rejected in r42/r43. Name each attack with the exact command or code line that would decide it. Do not run the full counter.""",
    "The report lists each attack as `attack / how it would be decided / what the L1 must add to the claim text or evidence`; at least one attack must be a concrete falsifier, not a concern."))

items.append(item(
    "CriticClaimC2", "critic", ["freshness"],
    "Falsify the C2 claim design: can the declared four-figure freshness count reach 0 without repairing the actual staleness?",
    """The claim: four r43 ledger figures (re-score tally, do-nothing ratios, build ratio range, wave composition) each re-derive from committed receipts at the tip, counted by `scripts/ledger_latest_check.py` (4 mismatches -> 0). Attack: (a) appending a bare correction line that satisfies the regex without naming the receipt — is that repaired staleness or cosmetic; (b) a spec that reads its expected value from a file the L1 also edits; (c) a "last line" rule that silently changes meaning when the ledger gains unrelated later lines; (d) whether the four figures are the whole routed set (spot-check §8.1,3,4,5,7,8) and which routed defects are excluded because they live in the closed fleet report; (e) whether the LOG's superseded ratios can be corrected at all without a rewrite (append-only). Name the minimum strengthening (extra assertions, receipt pointer in the same line, a fifth figure) that makes the claim non-gameable. Do not edit anything.""",
    "The report names each attack, the minimum strengthening it demands, and whether the current design would survive it."))

items.append(item(
    "ConnectorSibling", "connector", ["operability", "freshness"],
    "Sibling-overlap scan: does another lane already own the witness-class / counter-hardening method or the ledger-freshness checker this round builds?",
    f"""Search sibling lanes under /home/vgpnk/Projects/shokunin/*-shokunin (read-only; start with tameshi, kama, kaidoku, kumitate, chousa, mado, tabi, mori) for: a control-class corpus scored against a frozen counter; a "witnessed" notion distinct from "met"; an append-only ledger freshness checker. Use `grep`/`git log --oneline` read-only. Report the nearest prior art with paths and commit hashes, whether kake's round duplicates it, and what kake should cite instead of re-inventing. If kake's work is genuinely new, say which rows of its corpus/SOURCES.md should record the adjacency import and why.""",
    "The report names each nearest prior art with a resolvable path + commit, states duplicate/not-duplicate per item, and names any SOURCES row kake should add."))

items.append(item(
    "SentinelScope", "sentinel", ["operability"],
    "Adversarial scope and safety review of the wave's own plan: can any seat in this wave mutate history, the fleet repo, a sibling lane, or leak credentials?",
    f"""Read the wave prompt text as delivered (it is in this context) and the write bounds. Enumerate: (1) every file path the wave's items may write; (2) whether any item can run `git commit`/`jj`/`git push`, edit `/home/vgpnk/Projects/shokunin` (fleet) or a sibling, or write `.ufo/state/`; (3) whether any item runs a network call or embeds a credential; (4) whether the class modules' generated values can escape the sandbox (`{SCRATCH}` / tmpdir) or fill the disk (state the caps in the counter); (5) whether the probe or audit can overwrite evidence receipts. Name each gap with the exact prompt sentence that permits it, and the minimum additional bound. Do not edit files.""",
    "The report has a matrix (item -> writable paths -> verdict) and a named list of gaps with the sentence that permits each, or states `no gap found` per category with the evidence read."))

items.append(item(
    "RevengerControls", "revenger", ["operability"],
    "Reverse-engineer three of the round-43 controls from their bytes alone and reconstruct the intent of their authors — then judge whether the planned class shape is the one the author would have had to defeat.",
    f"""Pick `{LANE}/.ufo/waves/round-44/controls-r43/headtail-V2-headtail-key48.py`, `{LANE}/.ufo/waves/round-44/controls-r43/portvalue-memo-digits.py`, `{LANE}/.ufo/waves/round-44/controls-r43/repeat-ctl_defpos_memo_band.py`. For each: reconstruct the injected block, the cache key, what the author believed the counter could not generate (quote the control's own comment), and the value shape that defeats it. Then state whether the planned G-class (G5/G9/G7) contains that shape, and whether the author's control would still meet v5 after the class lands (it must not). Report the control's own claims vs your reconstruction where they disagree.""",
    "The report reconstructs key + blind-spot claim + defeating shape per control, and gives a verdict `class covers it` / `class misses it` with the shape named."))

items.append(item(
    "MutationTesterAudit", "mutation-tester", ["operability"],
    f"Mutation-test the audit driver `{LANE}/.ufo/waves/round-44/c44_audit.py` and the claim's counting command: prove the command is able to fail and cannot be fooled by a degenerate control set.",
    """In scratch: (1) run the audit on a 2-row TSV with the pristine round-41 tool and a semantically changed tool under `--classes v5` — expect 0 witnessed and 1 witnessed respectively (paste). (2) Mutate the driver one member at a time in a scratch copy: make `witnessed` count `met is None`; make it count errors as witnessed; make `--expect witnessed` ignore the build receipts; drop the sha check. For each mutant, show the mutant's output on the same 2-row TSV and state whether the mutant would still produce the claim's verdict (ok=true). A mutant that still passes is a hole in the driver, not in the counter. (3) Confirm the count of controls (27) is enforced: a TSV missing one row must not silently report `ok=true` under `--expect witnessed` (`witnessed == total` would still hold) — name the fix. Do not edit the real driver.""",
    "The report has two tables: two-row audit runs; mutant -> output -> passes-yes/no. At least one mutant must be shown to pass (a real hole) or the report states that none did, with the mutants listed."))

items.append(item(
    "LabratKelvin", "scout", ["operability"],
    "Hypothesis: case-fold memos can be defeated by a non-ASCII letter whose `.lower()`/`.casefold()` maps to an ASCII letter, without making the whole value fold-degenerate.",
    """Verify with Python only: `'\\u212a'.lower()`, `'\\u212a'.casefold()`, `'\\u017f'.casefold()`, `'\\u017f'.lower()`, `'\\u0130'.lower()`; then build two VALUES differing only by U+212A vs `k` in a later path segment, and confirm `b.lower() == a.lower()` and `b.casefold() == a.casefold()`. Confirm the round-41 tool's judgement differs on the pair (run it on a hand-made manifest: non-ASCII value is `loc_not_absolute`, ASCII one clean). Report the shortest pair that works and any code point that fails to fold (e.g. digits) so the class cannot degenerate. State the exact expected divergence for `casememo-v3/v4/v7/v8`.""",
    "The report pastes the Python one-liners' output, the identical-folded-keys check, and the reference tool's verbatim stdout on the pair."))

items.append(item(
    "LabratScopeSmu", "scout", ["operability"],
    "Hypothesis: `layout_f`'s derived/segment sitemapUrl makes some planned witnesses scope-only (the divergence is `loc_out_of_scope` regardless of the intended grammar defect), which weakens the class.",
    f"""Read `layout_f`, `derived_smu` and `segment_smu` in `{LANE}/.ufo/waves/round-44/c44_count_v5.py`. For the planned shapes of G1 (long port + grammar defect), G2 (implicit https port), G8 (tabled host + path defect) and G10 (long-port window), compute by hand what sitemapUrl `layout_f` derives for the value, and whether the value is IN scope for the round-41 tool. Then run one hand-made manifest per shape through the reference tool and confirm. Report which shapes are safe (the divergence is the intended finding) and which are scope-only, with the exact derived sitemapUrl string and the tool's stdout. Recommend the minimal layout fix that is NOT allowed (the counter is frozen) versus the value-side fix the class must use.""",
    "The report shows, per shape, the derived sitemapUrl string, the reference tool's verbatim stdout, and a verdict `intended-code` / `scope-only` with the value-side fix."))

items.append(item(
    "SimplifierInherited", "simplifier", ["operability"],
    "YAGNI pass over the inherited round-44 artifacts and the planned new files: name dead weight that should be deleted before the freeze, and dead weight that must stay as evidence.",
    f"""Inspect `{LANE}/.ufo/waves/round-44/` (build_v5.py, c44_count_v5.py, c44_audit.py, c44_probe.py, controls-27.tsv, controls-r43/, verification/freeze/). For each: is it load-bearing for C1/C2, or dead weight (superseded, duplicated, never referenced)? Check especially `verification/freeze/control-v4blind.json` (does any command read it?) and the empty `verification/freeze/tools/` dir. Do NOT delete anything: produce a list `path -> keep (reason) / delete-before-freeze (reason)`, and state which deletions would change the claim's evidence (those must stay). Also check the new class files' size and helper duplication: name one concrete simplification that does not change behavior.""",
    "The report lists every path with keep/delete and a reason, and names at most three concrete simplifications with the lines they touch."))

items.append(item(
    "ScribeSources", "scribe", ["freshness"],
    "Open the two SOURCES rows the round-43 spot-check routed for a locator erratum (S129, S130) and write the Gate + the two superseding rows, without rewriting history.",
    f"""Read `{LANE}/corpus/SOURCES.md` rows S129 and S130 and the cited files (`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-33/w1/CtlDoNothing.md` §Verdict and `ReviewFreeze.md`; `/home/vgpnk/Projects/shokunin/kama-shokunin/corpus/knowledge/self-assessment-at-writing.md` §Checking self-assessment statements at writing). Re-open both files this round and record the access date (2026-10-23) and a ≤25-word verbatim quote with its TRUE location under section-prose counting (the section's first paragraph for both, per the appended erratum in `{LANE}/corpus/lessons/round-43.md`).
Then write `{LANE}/corpus/lessons/round-44.md` with: (1) a `## Gate` section whose table records the two re-opened rows, the URL/path, access date, the quote, and the decision; (2) a note that S131 and S132 are the superseding rows (contract rule 2: a correction is a new row whose `teaches` opens `supersedes S0NN — `), with the exact new anchor text for each; (3) a `## Mistakes` heading (the L1 fills the mined mistake later). Do NOT edit the S129/S130 rows in place and do NOT edit any other lesson.""",
    "`corpus/lessons/round-44.md` exists with a `## Gate` table quoting both rows verbatim (≤25 words each), the access date, the true paragraph, the assessed decision, and the exact S131/S132 row text; the report pastes the quotes and the `wc -w` count of each quote."))

items.append(item(
    "CriticMathDenominator", "critic", ["operability"],
    "Audit the C1 arithmetic independently: 27 controls, 10 class runs, 4 r42 canaries, 1 junk control, 1 held build; and the denominator the audit prints.",
    f"""From `{LANE}/.ufo/waves/round-44/controls-27.tsv` and `{LANE}/.ufo/waves/round-43/w1/` (the seat reports) re-derive: the 27 controls by family/class, the mapping control -> expected G-class (check the TSV's class column against each control's source), and the four r42 canaries named in `{LANE}/.ufo/waves/round-44/verification/freeze/control-v4blind.json` (or in the r43 SCORECARD/lesson if absent). State the exact expected summary lines the audit must print for before (27/27 blind, exit 0) and after (witnessed 27/27, build met 3/3, exit 0), including the `caughtBy` keys per control that would satisfy the claim. Name any control whose expected `caughtBy` key is NOT the class the TSV assigns (a mapping defect). Do not edit anything.""",
    "The report has a 27-row table with `expected class -> caughtBy key that must carry it`, the four canary names, and the two exact expected summary lines; mapping defects are named."))

spec = {
    "wave": "kake-r44-w1",
    "milestone": "r44-build",
    "maxLanes": 64,
    "axes": ["operability", "freshness"],
    "reportDir": WAVE,
    "context": CONTEXT,
    "items": items,
}
out = Path(__file__).resolve()
(spec_path := out.parent / "w1-spec.json").write_text(json.dumps(spec, indent=1) + "\n")
print("items:", len(items))
from collections import Counter
print("roles:", dict(Counter(i["role"] for i in items)))
print("wrote", spec_path)
