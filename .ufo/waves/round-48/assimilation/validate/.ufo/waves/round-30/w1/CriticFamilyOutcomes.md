# KakeR30.CriticFamilyOutcomes: the declared F01-F06 outcomes against the round-27 and round-28 records

Seat: leaf critic, axis operability. Lane base `0356681`, tip `4580c78` (`scripts/citing_set.py` sha256 `d7e79ba1…9d48` at both). Sandbox `/fast/scratch/hyaku/kake-r30/w1/CriticFamilyOutcomes/` (TMPDIR there). This file is my only lane write. No network. No installs or upgrades. Python 3.14.8, system Git.

## Verdict
The declared F01-F04 behaviour should stand. It breaks no committed input and no committed caller (evidence below). There are three fixable gaps, one of them in the counter:
1. **High (F04 is open to a false pass).** argparse prefix abbreviations bypass a repeat check that scans argv for exact names (the lane's own pattern, `scripts/accessibility_packet.py:209-211`). The counter's F04 cannot see this. Fix: reject the repeat inside the parser, not by scanning tokens.
2. **Medium (F02 scope).** `1e999` parses to `inf` and is measured `clean`. That is a non-finite number reached without the `NaN`/`Infinity` tokens. Fix: also pass `parse_float` with a finite check, under `document_nonfinite_number`.
3. **Low (F03 regex anchor).** With `re.match`, the contract's `^S[0-9]{3,}$` accepts `"S001\n"`, because Python's `$` matches before a trailing newline. Fix: `re.fullmatch(r"S[0-9]{3,}", id)`.

## Q1. Is refusing `S01` right, given numeric comparison (`S001 == S0001`)?
- **Counterexample:** population `S01` with a corpus that cites `S001`. `id_key` maps both to `("n", 1)` (`citing_set.py:135,171`), so today this input is measurable: exit 1, `unadjudicated_citing_pair` row `S01` (probe P1). Under the declared rule it becomes exit 2 `population_id_unreachable` (candidate P1). So the refusal is stricter than true reachability, and for this input the label "unreachable" is not literally true.
- **Why it should still stand:** the scanner can never match the spelling `S01` itself (`_TOKEN_RE`, `citing_set.py:126`). The round-27 replay P22 (population `S01`,`S02`, corpus `See S01 and S02`) is still exit 0 `clean` at the tip (probe P2), which is the open round-27 false green (`round-27/unresolved-acceptance.json:34-41`, `round-28/w1a3/CriticCounterFaithful.md:7,39-40`). Refusal is the only rule that closes it without guessing an alias. No committed population is affected: every fed population and ledger id matches `S[0-9]{3,}` at the tip and in all 8 historical blobs (scan below). Fixtures 28 and 29 (`S0001`) still match and still pass.
- **Correction required with the change:** the docstring at `citing_set.py:33-38` still says "not `S` followed by digits". It must say three or more digits, and should state that `S01` is refused even though its key equals `S001`. Optionally add a `detail` to the finding saying the spelling is not citable.
- Ledger rows are not restricted. Ledger row `S01` still adjudicates population `S001` (`clean`, probe P3, both gates). This is consistent with the documented numeric comparison and is not a false green. Leave it as is.

## Q2. Does refusing duplicate keys (or non-finite numbers) break a committed document the lane really feeds the gate?
No. The fed inputs are the SKILL.md consumer command (`SKILL.md:609-611`: `.ufo/waves/round-26/population.json` with `.ufo/waves/round-27/complete-ledger.json`), the frozen C2 inputs (`.ufo/waves/round-27/frozen/{population,ledger}.json`, via `c2_count.py:25`) and the 29 fixtures. Round 28 committed no population or ledger document; its parity runs used the same round-26/27 files (`round-28/w1a3/RunRealInputParity.md:28,54`).
- My scan of all 696 tracked JSON files at the tip found duplicate members only in `scripts/fixtures/base-path/X01-duplicate-json-key/manifest.json` and `NaN` only in `X02`. Both are base-path fixtures and are never fed to this gate. The other flags are non-population `rows` arrays and the intentionally broken fixture 15.
- History scan (`git log --all`): 8 blobs of the fed population and ledger files plus `pairs.json` and `discovered-pairs.json` all have 0 flags.
- Behaviour: with the candidate gate the real consumer report is byte-identical to the tip's in Git mode and in working-tree mode (sha256 `93cb7fb2…` and `eb8120e6…`; exit 1, citingPairs 59, ledgerPairs 58, one `unadjudicated_citing_pair`).
- Precedent: `receipt_replay.py:98-102,123` already rejects overflow through `parse_float`, while `base_path_audit.py:231-235` does not. That is why I recommend the `parse_float` fix in gap 2.

## Q3. Does exit 64 for repeated options break a committed caller?
No. Every committed caller passes each valued option once: `citing_set_selftest.py:214-225`, `round-27/git_name_selftest.py:169-182`, `round-27/c2_count.py:25`, `round-28/c1_interface_count.py:174` (it adds `--revision` once), `round-28/verification/c1_root_env_matrix.py:52-53`, and the SKILL.md command. The gate's own `--selftest` path (`citing_set.py:665-681`) strips `--root`, so only an operator typing `--selftest --root a --root b` gets 64. I found no gate call outside the lane (fleet grep returned nothing).
- **Counterexample (High):** against the tip gate and against a token-scan variant (`gates/tokenscan.py`), `--rev no-such --revision HEAD`, `--pop missing.json --population population.json`, `--led missing.json --ledger …` and `--ro /nonexistent --root <real>` all exit 0 `clean`, with last-wins (probes R2-R5). The exact-name and `=` forms do give 64 (R1, R6, R7).
- The counter cannot tell the difference: `c1_reason_count.py` at a sandbox commit carrying the token scan (`58f3258`) scores F04 **pass**, the same as the action-based variant (`4402ef9`). Its F04 variants (`c1_reason_count.py:304-312`) use exact names only.
- Smallest correction:
  - Gate: use a store-once `argparse.Action` on the four options that calls `parser.error` when the destination is already set. With it, R1-R7 give 64 and the single-option control R8 gives 0 (`probe-cand.json`). Alternatively, use `allow_abbrev=False` plus the token scan.
  - Counter: add one abbreviated variant (for example `--rev no-such-revision --revision HEAD`) to F04, and `1e999` to F02.

## F05 and F06
These are not contested by the records: `ReviewNonBlockingRead.md:12-15` shows the missing O_NOCTTY flag (tty_nr 0 to 34817), and the counter reproduces it on both variants (F06 tty_nr 34817/34818). F05 fails at the tip with a traceback. I did not build either fix, so I make no claim about the declared fixes.

## Commands (all in the sandbox, TMPDIR set there)
- `git clone -q <lane> clone`: exit 0, HEAD `4580c78`. `sha256sum`: base and tip gate both `d7e79ba1…9d48`.
- `python3 -B scan_docs.py clone head`: exit 0, 696 scanned, 7 flagged (listed above). `… hist <8 fed paths>`: exit 0, 8 scanned, 0 flagged.
- `python3 -B probe.py gates/<g>.py work-<g>` for head, tokenscan and candidate: exit 0 each (`probe-head.json` `178a5e34…`, `probe-tok.json` `dd042fc5…`, `probe-cand.json` `6d7d4295…`).
  - Head: P1 1/failed, P2 0/clean, P4 1/failed, P5 0/clean, P6 0/clean, P7 0/clean, R1-R7 0/clean.
  - Candidate: P1, P2 and P4 give 2 `population_id_unreachable`; P5 and P6 give 2 `document_nonfinite_number`; P7 gives 2 `document_duplicate_key`; R1-R7 give 64.
- `gates/<g>.py --root clone [--revision 4580c78] --population .ufo/waves/round-26/population.json --ledger .ufo/waves/round-27/complete-ledger.json --json`: exit 1 for all four runs, and head equals candidate.
- `clone/scripts/citing_set_selftest.py --root clone --gate gates/<g>.py --tmpdir …`: exit 0, clean 29/29 for both head and candidate.
- Sandbox-clone branches `probe-candidate` (`4402ef9`) and `probe-candidate-token` (`58f3258`); only `scripts/citing_set.py` changed.
- `.ufo/waves/round-27/c2_count.py --root . --revision {4580c78,4402ef9}`: exit 0 both, detected 16/16, false positives 0.
- `.ufo/waves/round-28/c1_interface_count.py … --scratch …`: exit 0 both, 15/15.
- `.ufo/waves/round-27/git_name_selftest.py --gate gates/{head,candidate}.py`: exit 0 both, 30 cases, 0 failed.
- `.ufo/waves/round-30/c1_reason_count.py --root . --revision {4402ef9,58f3258} --scratch …`: exit 1 both, 2/14. Controls hold and both constant gates score 0. F03 and F04 pass on both. R01-R08, F01 and F02 have behaviour true but no fixture. F05 and F06 fail.

## Sandbox artifacts (absolute paths, sha256)
`/fast/scratch/hyaku/kake-r30/w1/CriticFamilyOutcomes/`: `scan_docs.py` `405231…de13`, `probe.py` `63e42d…6bcc`, `gates/candidate.py` `270e75…18ef8` (strict loader, fullmatch, store-once action; a demonstrator only, not an integration candidate: no fixtures, no F05 or F06), `gates/candidate-token.py` `6d4ad1…fca`, `gates/tokenscan.py` `7d48da…e13e`, `count-A.json` `be6b63…b311`, `count-T.json` `64419e…a09a`, `scan-head.json` `b325eb…81b1`, `scan-hist.json` `f3821f…6d546`.

## Not verified
- I did not run `round-28/verification/c1_root_env_matrix.py`, because it writes under `/fast/scratch/hyaku/kake-r28a3` and reads the lane gate. I judged it from its source only (`:52-53`, single options).
- I did not build or run the real round-30 writers' gate; I used no fixture objects with reasons and no runner changes.
- I tested no other Python version. Duplicate members deeper than a ledger pair object were not probed separately; the same hook applies at every depth.
