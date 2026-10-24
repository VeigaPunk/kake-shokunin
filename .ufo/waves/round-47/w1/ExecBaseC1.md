# ExecBaseC1 — do-nothing base reproduction + instrument over-acceptance (round 47, wave 1)

Seat: executor. Claim under test: **C1** (operability — both round-46 gates have a SKILL.md
registry row and a committed selftest receipt).
Assigned target: run the counter at the frozen base and compare with
`verification/c1-before-cd42e3c.json`.
Verdict on the target: **CONFIRMED**, exactly and byte-identically.
Independent finding: the counter is a genuine discriminator, but two of its clauses are weaker
than the predicate sentence they are supposed to decide (both measured, below).
Method: read-only committed bytes; mutations only in `/fast/scratch/hyaku/kake-r47/ExecBaseC1/`.
Lane checkout, `.jj`, Git index/refs and `.ufo/state/` untouched — `git status` was never run
against the lane working tree for mutation purposes.

## Detector

`python3 -B .ufo/waves/round-47/c47_registry_count.py --root . --revision <rev>`
(0 = C1_MET, 1 = C1_NOT_MET, 2 = could-not-evaluate, 64 = usage). Key clauses:

- row: `.ufo/waves/round-47/c47_registry_count.py:114-116` — `line.lstrip().startswith("|") and needle in line`
- receipt: `:122-123` — `needle in text and tally_re.search(text) and "exit=0" in text and SHA256_RE.search(text)`
- `SHA256_RE = re.compile(r"\b[0-9a-f]{64}\b")` (`:43`) — a *token*, not a verified digest
- receipt discovery: `:105` `git ls-tree -r` of `RECEIPT_DIR` (`:42`)

## Assigned run (lane repo, lane HEAD `766f461`)

```
$ python3 -B .ufo/waves/round-47/c47_registry_count.py --root . \
    --revision cd42e3c310ba442e89dde638ba6401adaefaf3e8
registry_rows=0/2 receipts=0/2 C1_NOT_MET
```

- exit code: **1** (`EXIT=1`), stderr **0 bytes** — not a could-not-evaluate(2) masquerading as red.
- `--json -` payload vs the committed artifact:
  `diff -u .ufo/waves/round-47/verification/c1-before-cd42e3c.json <rerun>` → **IDENTICAL**;
  both sha256 `c98ff62486a90e88034c618f4a93443bfc9d4e4ac538e3aad167b290656acd13`.
- determinism: second run identical (`registry_rows=0/2 receipts=0/2 C1_NOT_MET`, exit 1).

So the do-nothing base is **0/2 registry rows, 0/2 receipts, exit 1**, and
`c1-before-cd42e3c.json` reports exactly that. Target met.

## Independent confirmation of the base state (not trusting the counter)

| probe | command | result |
|---|---|---|
| rows for either tool | `git show cd42e3c:SKILL.md \| grep -c '^|.*scripts/<tool>'` | `0` and `0`; the bare substring `scripts/<tool>` also appears **0** times anywhere in that file |
| row detector is selective, not vacuous | `git show cd42e3c:SKILL.md \| awk '/^\|/{r++} ...'` | 162 pipe rows, 16 gate rows naming a `scripts/*.py` — the base table is populated and still names neither target |
| receipt tree | `git ls-tree -r --name-only cd42e3c .ufo/waves/round-47/verification` | empty; `git ls-tree -r cd42e3c .ufo/waves/round-47/ \| wc -l` → **0** (the whole round-47 tree postdates base) |
| base identity | `git log -1 --format='%H %ci %s' cd42e3c` | `cd42e3c… 2026-10-24 03:22:36 -0300 round-46 verifier spot-check…`; `git merge-base --is-ancestor cd42e3c HEAD` → ok |
| tools exist at base | `git ls-tree -r --name-only cd42e3c -- scripts/redirect_audit.py scripts/citation_lint.py` | **both present** — base is "tools shipped, unregistered and unreceipted", not "tools missing" |

## Falsifier 1 (measured): the row clause accepts a non-registry prose row

In the scratch clone, one appended table row that is *not* a gate-registry row and carries no
kind/entry-command/verdict-map/selftest/pinned-values/owner columns:

```
| hostile note | run `scripts/redirect_audit.py` and `scripts/citation_lint.py` by hand | n/a |
```

committed, then `c47.py --root lane --revision <that commit>` →

```
registry_rows=2/2 receipts=0/2 C1_NOT_MET
```

One stray mention row flips **both** tools. `SKILL.md` already contains rows of exactly this
shape at base (e.g. base line 944, an advice row naming `scripts/canonical_audit.py`), so this is
a reachable state, not a contrived one. The predicate sentence says "SKILL.md gate-registry row";
the detector tests only `startswith("|") and needle in line` (`:114-116`).

## Falsifier 2 (measured): the receipt clause accepts a fabricated sha256

Fabricated receipt committed under `verification/`, with an **all-zero** digest and no command
ever run:

```
tool_path: scripts/redirect_audit.py
tool_sha256: 0000000000000000000000000000000000000000000000000000000000000000
selftest: 23/23 passed
exit=0
```

→ `registry_rows=2/2 receipts=1/2` with `redirect_audit.py: true`. The receipt counts.
Control on the same axis: the same receipt minus any 64-hex stays `false`, so the clause enforces
digest *presence* only, never equality with the tool blob.

This is the variant `w1/MutationC1Receipt.md` recorded under "Adversarial note (static, not
exercised)". It is now exercised: the note is a live gap, not a suspicion. (Their digest-*strip*
mutation correctly killed the receipt; a digest-*substitution* does not.)

## What still holds for C1 (so the falsifiers are bounded)

- The two genuine receipts at `714e707` name the **correct** blobs: `tool_sha256: 1e1dff18…bb748a`
  and `3c78a0a8…9662987f` equal `git show <rev>:scripts/<tool> | sha256sum` at both `cd42e3c` and
  `714e707` (tool bytes are unchanged across the round; only rows and receipts were added).
- Per-file attribution at `714e707` over all committed `verification/` files — only
  `selftest-redirect-audit.txt` and `selftest-citation-lint.txt` satisfy tally+hex+exit=0. The
  sweep log, census files and `c1-before-*.json` do **not**, so the green is not an accidental
  self-quote of a receipt by a log file inside the receipt directory.
- Non-constancy (the reason the 0/2 red is evidential): same binary at `714e707` →
  `registry_rows=2/2 receipts=2/2 C1_MET`, exit **0**; at `846138c` the same, exit 0. A
  constant-false instrument would have matched the base artifact too.
- Exit taxonomy exercised: bogus revision →
  `could-not-evaluate: no SKILL.md at 0000000000000000…` exit **2**; missing `--root` → exit **64**.

## Caveats / risks

1. **The before-side receipt half is vacuous.** The entire `.ufo/waves/round-47/` tree is absent at
   base, so `git ls-tree` returns empty and `receipts=0/2` is guaranteed by history rather than by
   receipt content. The base run cannot distinguish "no receipt" from "no receipt directory"; only
   the after-side run exercises `:122-123`. Recommend the before claim be stated as "unreceipted"
   (which is true) rather than as a measured receipt search.
2. **Predicate wording stronger than the instrument** on both clauses (rows: any pipe-row mention;
   receipts: any 64-hex). C1_MET at tip is factually correct per the digests above, but a future
   run could reach `C1_MET` from a prose mention plus a placeholder digest. If the SCORECARD
   sentence is quoted as the C1 evidence standard, the counter should verify the digest against
   `git show <rev>:scripts/<tool>` and require a registry-table row.
3. `--json PATH` (`:146`) writes a file; the docstring's "Read-only" holds only for the default
   stdout form. Reproducing the artifact therefore requires `--json -` or stdout redirection.
4. `parse_cli` de-duplicates `--root` but not `--revision` (last wins silently).

## Not done (stated, not claimed)

- I did **not** execute `scripts/redirect_audit.py --selftest` or `scripts/citation_lint.py --selftest`.
  The 23/23 and 8/8 tallies are read from committed receipts; their truth is bounded by digest
  provenance above, not by re-execution. Test execution belongs to the parent's post-integration gate.
- No lane mutation, no `jj`/`git` write in the lane, no push from the scratch clone, no sibling-repo
  or fleet-root reads.
- No tools installed or updated in this seat (no package operations attempted; host pacman pause
  irrelevant here).

## Files changed

- `.ufo/waves/round-47/w1/ExecBaseC1.md` (this report) — only write in the lane.
- Scratch only: `/fast/scratch/hyaku/kake-r47/ExecBaseC1/{c47.py,lane/}` (local clone + mutation
  commits; never pushed).
