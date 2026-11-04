VERDICT: C1 holds; C2's counter verdict is forgeable (a pin-reading gate with no conformance logic scores met=true), but held-out probes support the gate's behaviour

# ScribeLedger — round 90, w1

Seat: scribe. Drafts are for L1 to integrate. I wrote only to this file and to `.ufo/waves/round-90/w1/ScribeLedger/`.
Every number in the drafts is copied from a committed receipt, or from a receipt in `ScribeLedger/receipts/`, and each one cites its path.

## Deliverables

| Draft | Target | Path |
|---|---|---|
| `## Round 90 — measured claims`: claim table, controls paragraph, demonstrated-repertoire row for the gate, move log, planned-after routing R90-1..R90-4 | `SCORECARD.md`, appended | `.ufo/waves/round-90/w1/ScribeLedger/scorecard-round-90.md` |
| Round-90 entry | `LOG.md`, appended | `.ufo/waves/round-90/w1/ScribeLedger/log-round-90.md` |
| One criterion, "a counter's `met` is admitted only for the refusals it has been seen to make" | `corpus/QUALITY.md`, appended | `.ufo/waves/round-90/w1/ScribeLedger/quality-round-90.md` |

**Heading collision.** `SCORECARD.md` and `LOG.md` at `79e1aac2` already end with a `## Round 90 — correction tail …` section. My headings are distinct: `## Round 90 — measured claims` and `## Round 90 — 2026-11-04, three routed round-89 defects …`. Append them after the tails.

**Uncommitted L1 QUALITY.md section.** The working tree already holds an uncommitted L1 `## Round 90 — a counter earns a met …` section. My draft is an alternative to it, not an addition. See F3.

## Findings

### F1 — C2's counter `met` can be forged (defect in the frozen `c90_gate.py`)

I built a 16-line gate with no conformance logic (`receipts/forgery-pin-reading-gate.py`). It does three things:
- strips the `\n# nonce <16hex>\n` trailer that the counter appends;
- hashes the subject;
- walks up to the `c2-population.sha256` that the counter extracts into the same work tree, and admits only the first four pinned hashes.

I committed it in a scratch fixture at `b1f19dd0`, whose parent is `79e1aac2`. Then I ran:
- `python3 -B .ufo/waves/round-90/c90_gate.py --root <fixture> --revision HEAD --work <scratch>` gave exit 0 and `C2v90 revision=b1f19dd0… gate=present positives=4/4 negatives_refused=57/57 false_admits=0 errors=0 anti_table=ok population=ok seed=1420722954 met=true`. Receipt: `receipts/forgery-c2-pin-reading-gate.txt`.

Why it works:
- The nonce can be reversed.
- The pins and labels are readable from the gate's working tree.
- `anti_table` only scans the gate's source text for hashes and stems.

**Consequence.** `controls/after-c2-carrier.txt` `met=true` alone does not show behavioural conformance. The freeze's no-positive-control disclosure is honest, but none of its controls tests a forgery that undoes the nonce. The `ctl-c2.txt` hash-table control hashed the nonce-altered bytes and failed with `false_admits=57`. The `anti_table` conjunct also has no able-to-fail witness, because no control embeds a hash or stem in the gate's source.

I folded this into the SCORECARD verdict cell, the repertoire row and the LOG entry. It is also a proposed instrument item in "Planned — after round 90". I did not assign it an R-number; L1 owns routing.

### F2 — evidence that the actual gate behaves

I ran two subjects that are not in the pins against `scripts/cache_key_conformance.py`. It is unmodified in the working tree and identical to `7f6c68f1` (`git diff --stat 7f6c68f1 79e1aac2 -- scripts/` is empty).

| Subject | Result | Receipt |
|---|---|---|
| `scripts/cache_key.py` with comments stripped and an unused function added | `clauses=6/6 hand=70/70 generated=120/120 sandbox=ok … met=true`, exit 0 | `receipts/heldout-pos-comments-stripped.txt` |
| A new mutant that trims values of SP only, against contract clause 3 | `clauses=5/6 hand=68/70 generated=118/120 … met=false`, exit 1 | `receipts/heldout-neg-value-htab-untrimmed.txt` |

Both runs printed `advisory=1/3 outside-contract-gaps=utf8-required,nul-in-value`. That line is consistent with R90-1 and R90-2.

The per-subject lines in `after-c2-carrier.txt` give every positive `6/6 70/70 120/120 sandbox=ok` and every negative `met=false`. M37 reads `clauses=5/6 hand=69/70`, which matches lesson Mistake 1.

Two samples are not a population. The gate's behaviour is supported, not proven.

### F3 — L1's uncommitted QUALITY criterion fails its own witnesses

L1's draft (working tree, `corpus/QUALITY.md` after line 1761) requires "(2) at least one forgery per conjunct". `controls/ctl-c1.txt` does not meet that. I enumerated the conjuncts in `c90_defects.py` against the reason strings in the receipt. These conjuncts have no forgery:
- `baseclean.out` tracked at the lane root;
- the correction receipt untracked (the message "receipt … not tracked" never appears);
- the `LOG.md` prefix (D2c rewrites `SCORECARD.md` only);
- the retained RFC 9111 digest;
- the individual conditions on the superseding row (rfc9111 URL, `mined`, scope cell).

Read literally, L1's text would reject the round's own C1 `met`.

My draft instead requires one forgery per item, refused for its stated reason. Unwitnessed conjuncts must be listed as limits.

The draft uses `ctl-c1-v0-before-parse-fix.txt` as a second witness. In v0 the D2b forgery was refused for the wrong reason: "receipt first line disagrees" instead of the c89 re-run. In `ctl-c1.txt` it reads "re-run at 93475f7e gives open=1 closed=5". This shows that checking the reason is what makes a forgery a witness.

### F4 — C1 re-reads met at the receipts commit, and appending the drafts does no harm

- `c90_defects.py --revision 79e1aac2` gave exit 0, `open=0 closed=3 met=true`. Receipt: `receipts/c1-at-79e1aac2.txt`.
- `c90_gate.py --revision 79e1aac2` gave exit 0, `positives=4/4 negatives_refused=57/57 … seed=970713380 met=true`. Receipt: `receipts/c2-at-79e1aac2.txt`.
- I appended all three drafts to `SCORECARD.md`, `LOG.md` and `corpus/QUALITY.md` in a fixture (commit `4993644e`, parent `79e1aac2`). The C1 counter then gave exit 0, `open=0 closed=3 met=true`. Receipt: `receipts/noharm-c1-drafts-appended.txt`.

The drafts never contain the token `D89-2 correction:`, so they cannot become D2 candidate lines.

### F5 — smaller limits (reported, not fixed)

- **D1 live conjunct.** It uses `git status --untracked-files=normal`, so a lane-root file matched by `.gitignore` is invisible to it. The relevant patterns are `__pycache__/` and `*.pyc` (`.gitignore`). This does not matter for `baseclean.out`.
- **D2 verifies the count, not the item list.** D89-2's substantive defect was "items B, C, D, E, F closed" contradicting `closed=1`. The counter checks only `open=N closed=M` and the receipt. The item-list correction exists in the appended tail (`SCORECARD.md:5555`, `LOG.md:3089`), but no conjunct measures it.
- **The C1 reading is time-bound.** D1 is live, so `after-c1-carrier.txt` holds for the working tree at the time it was run. The freeze discloses this.
- **Positive M36 (dedupe).** It is admitted as conforming, consistent with round-89 `w1/MutKey.md:108`: the dedupe is unreachable behind the duplicate-member refusal.

## Counts I verified

| Item | Value | Source |
|---|---|---|
| Registry rows | 202 at `209027f4` → 205 at `e50c9566` and `79e1aac2` | `git show <rev>:corpus/SOURCES.md \| grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` |
| Knowledge entries | 77 → 78 | `git ls-tree -r --name-only <rev> -- corpus/knowledge \| grep -c '\.md$'` |
| W04 lines | 26 → 29 | `grep -c W04` on `controls/census-before.txt` and `controls/census-after.txt` |
| Counter and pin sha256 | match the freeze | `sha256sum` |
| Counter, pin and frozen-negative bytes, `4ee62b18`..`79e1aac2` | unchanged | `git diff --stat` empty |
| Seats | 13 | `w1-spec.json` |
| Attack share | mutation-tester 2 + reviewer 2 + critic 1 = 5/13 | `w1-spec.json` |
| Dispatch | `2026-11-04T19:14:24` | `w1.ready.dispatched` |
| Freeze commit | `18:54:29 -0300` | `git show 4ee62b18` |

I assumed the dispatch stamp is local time, like the commit dates. The stamp itself carries no timezone.

## Not checked by me

- The LOG line "no network beyond the three named RFC GETs" is copied from L1's lesson §Gate. It is L1's statement to confirm.
- The `assimilation/` directory (untracked) is L1's. I did not read it, and the LOG draft makes no assimilation statement.

## Hygiene

- **Tools:** none installed or upgraded. No network.
- **Fixture:** one clone, `/fast/scratch/hyaku/kake-r90/ScribeLedger/fx.*`, toplevel asserted. Fixture commits only, with `-c user.name=fixture -c user.email=fixture@scratch.invalid`.
- **Lane and fleet:** no mutating git command in LANE or the fleet repo.
- **Scratch:** deleted before yield. Commands are in `receipts/commands.txt`.
- **Tool issue:** I filed a QA note for a bash tool call that returned no output.
