# Round 29 wave 1 — CriticClaimSizing (critic, leaf)

Target: the SCORECARD "Round 29 — declared claims" section (SCORECARD.md:614-637, landed at d18bbf3)
checked against the Claim sizing, Learning claim and Drift sentinel rules in
/home/vgpnk/Projects/shokunin/.scratch/goal-20261022-hyaku-12h.md:144-158 and :163-176 (read only).
Advisory input for the L1 and the non-author closure. This seat does not judge or admit the round.

## Verdict per rule

| Rule | C1 (freshness) | C2 (operability) |
|---|---|---|
| One concrete after-value | pass | pass |
| Re-derivable by one command over committed bytes | pass | risk |
| No universal wording the counter does not enumerate | risk | risk |
| Claims causally separable | pass | pass |
| Learning claim condition | risk (strongest finding) | risk |
| Drift sentinel: same axis and surface 3 rounds running | pass (risk for round 30) | pass |
| Drift sentinel: same routed defect class 3 rounds running | risk | risk |

## Findings, with the exact text that causes each one

1. **One after-value: pass.** C1 is "4/4 declared ids pass at the landed commit" (SCORECARD.md:624). C2 is "30/30 cases pass at the landed commit, with all three constant gates rejected" (:625). The C2 value has two conditions, but the counter folds them into a single exit 0 (c2_matrix_count.py:172), so one command still decides it.
2. **Re-derivable from committed bytes.** C1 passes because every input is read through `git show <rev>:<path>` (c1_quote_truth.py:46-48, 83-86). C2 is a risk. The matrix is read from the working tree next to the counter, not from the revision (`MATRIX = HERE / "c2-matrix.json"`, c2_matrix_count.py:26). The digest pin (:28) covers the matrix, but the declaration pins neither counter. The tool also runs under the host `sys.executable` (:111), which is Python 3.14.8 on this host, so the result can depend on the interpreter's HTML parser [INFERENCE: the tool has not landed, so I could not confirm it uses `html.parser`]. Smallest fix: record the counter blob ids at d18bbf3 (c1 `139ede1efbbfeed612201239a4244b43aeda855d`, c2 `58dde0628c3e40a9794c93b03c3b9f6e665173fc`) and the Python version in the after-evidence. The closure should then run the counters taken from d18bbf3.
3. **Universal or unenumerated wording, C1.** The text "grounded in four primary sources" (:624) is not checked by the counter, which ignores the kind and tier cells. Check (a) reads only cells 1, 7 and 8 (c1_quote_truth.py:100-101). The text "(round-28 routed defect 3: quote truth, not quote shape)" (:631-632) claims more than the counter measures. Its check (d) only shows that the quote appears in the lane's own extracted text (receipts `textRule`). It does not show that the quote supports the entry. Navigation text passes, and so does one quote reused for two ids (see the counterexample below). The text "the entry cites the id below its metadata header" (:629) does not match the code. The counter skips a fixed 8 lines (`entry.splitlines()[8:]`, :91), while the lane's entry header is 3 lines (field-performance-cwv.md:1-3). The code is stricter than the prose, so this is a wording mismatch, not a false pass.
4. **Universal or unenumerated wording, C2.** The text "(built HTML of a project site, declared base path, same-origin references that resolve outside it)" (:625) covers every reference, but the counter checks 30 cases. The matrix `interface` names `audio[src]` and `embed[src]`, yet no case contains `<audio` or `<embed` (grep count 0). It also names `id`, `page`, `resolved`, `pagesChecked` and `referencesChecked`, but the counter never compares them. `project()` keys only on expected keys: reason, element, attribute, value (c2_matrix_count.py:62-72). The text "all three constant gates rejected" is fully enumerated, so it passes. Note, though, that constant-clean and constant-refuse each already pass 7/30 (verification/c2-before-fe1805c.json). Smallest fix: the measured-results row says "on the 30 frozen cases" and lists the uncompared interface fields as limits.
5. **Causal separability: pass.** The two counters read disjoint inputs. C1 reads corpus/SOURCES.md, the entry, the lesson and the sources directory. C2 reads scripts/base_path_audit.py and the pinned matrix. Evidence: my sandbox commit ea8a94e changed only the three C1 files (21 insertions). It moved C1 from 0/4 to 4/4 while C2 stayed at 0/30, exit 1.
6. **Learning claim: risk. This is the strongest counterexample.** The goal file's learning claim (:144-149) needs "admitted knowledge on uncovered ground" or "a capability shown running and entered in SCORECARD's capability table".
   - C1 is the knowledge candidate, and the ground is open frontier (PROVINCE.md:27, "Jekyll/base-path build tooling"). But the C1 counter cannot tell knowledge from an empty file. My hollow commit `ea8a94ec720a2d48cf9f55f714e262c6cdf85ccd` contains:
     - an entry that is 8 lines of "h" plus "S040 S041 S042 S043";
     - registry rows of kind `blog`, tier `C`;
     - Gate quotes taken from navigation text, with S041 and S042 sharing the identical quote "Step by Step Tutorial Command Line Usage Configuration Rendering Process".

     It scores **C1 4/4, exit 0, controlBroken false**.
   - C2 is labelled "capability", but the declaration never says it enters the Capabilities table. The round-28 closure records that no capability was "added to the SCORECARD capability table (none was claimed)" (round-28-verifier-spotcheck.md:201).
   - Smallest fix, which adds a criterion and does not narrow the target: add one declaration sentence before landing. It should say that C2 at 30/30 enters a Capabilities row, and that the closure reads the C1 entry body for knowledge, because 4/4 is necessary but not sufficient. A stronger optional fix: before landing, make the counter require each id's Gate quote, or a claim citing it, inside the entry body, and reject duplicate quotes across ids.
7. **Drift sentinel, same axis and surface: pass for round 29.**
   - Operability was worked on scripts/citing_set.py in round 27 (C2) and round 28 (C1). Round 29 moves to scripts/base_path_audit.py, which breaks that run.
   - Freshness was citing-pair adjudication in round 27. In rounds 28 and 29 it is a new knowledge entry from four sources with Gate quote lines (round 28 C2, round 29 C1). That makes two rounds in a row. A round-30 freshness claim of the same shape is the risk to watch.
8. **Drift sentinel, same routed defect class: risk.**
   - Routing so far: round 27 routed counter granularity ("the runner compares exit plus finding-id multiset only", round-27-verifier-spotcheck.md item 3). Round 28 routed the same class ("checks finding ids, not reason codes … quote shape, not quote truth", round-28-verifier-spotcheck.md:225).
   - Round 29 declares both counters as fixes for that class (:631-633). Each still has granularity gaps, listed in findings 3 and 4.
   - If the round-29 closure routes a counter-granularity defect again, the class has been routed three rounds running, and the sentinel requires a different frontier area next round.
   - Round-28 routed defect 4 (record at least one screened-and-rejected source candidate) applies directly to C1's source step, but the declaration does not mention it. Neither does the corpus/SOURCES.md at e58b66c, which is unchanged since base (verification/census-before.txt).
9. **Provenance note (not one of the sizing rules).** The declaration names S040 "GitHub Docs About GitHub Pages". Its receipt redirects to `what-is-github-pages` (sources/receipts.json, S040 `finalUrl`). The registry row should name the page actually served.

## Commands run (sandbox /fast/scratch/hyaku/kake-r29/w1/CriticClaimSizing/, TMPDIR inside it)

- `git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin …/clone` (exit 0; tip e58b66c)
- `python3 -B .ufo/waves/round-29/c1_quote_truth.py --root . --revision e58b66c` gave "C1 0/4", exit 1 (output: `c1-e58b66c.json`).
- `python3 -B .ufo/waves/round-29/c2_matrix_count.py --root . --revision e58b66c` gave "C2 0/30", exit 1. The constant gates scored 7/30, 0/30 and 7/30, all rejected (output: `c2-e58b66c.json`).
- `python3 -B …/hollow.py`, then a sandbox-only commit gave ea8a94e (exit 0).
- `python3 -B .ufo/waves/round-29/c1_quote_truth.py --root . --revision HEAD` gave "C1 4/4 at ea8a94e…", exit 0 (output: `c1-hollow.json`, sha256 f460ec88044aa44ef545add4b00fc981304bb0ea8c2c0b24a0f1bdc70e76ded5).
- `python3 -B .ufo/waves/round-29/c2_matrix_count.py --root . --revision ea8a94e` gave "C2 0/30", exit 1 (output: `c2-hollow.json`).
- `sha256sum c2-matrix.json` gave 75c08f64…e84a, which equals the pin. `python3 --version` gave Python 3.14.8.

Evidence files: /fast/scratch/hyaku/kake-r29/w1/CriticClaimSizing/{hollow.py,c1-hollow.json,c2-hollow.json,c1-e58b66c.json,c2-e58b66c.json}.

## Not verified

- I did not check the landed tool or the landed entry, because neither exists yet.
- I did not reopen the source pages and made no network fetch.
- I did not build a C2 gaming tool; that belongs to CriticC2CounterGameable. The C2 granularity claims above come from reading the code.
- I did not read the canonical PROTOCOL or AXES texts for the drift rule beyond the goal file.

No installs. I wrote nothing in the lane except this report.
