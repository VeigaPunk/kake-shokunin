# ExecReceiptReplay — C1 counter + selftest receipt replay (round 47, w1)

Seat: `ExecReceiptReplay` (leaf executor). Mode: read-only evidence in the lane; one disposable
local sandbox clone for mutation controls. No lane file was modified by this seat.

Tip evaluated: `766f4610b64f35a0f402b37eb1d8be2d4d634c0f` (`round-47 verifier spot-check
(integrator, hyaku): non-author admit/reject`). Frozen base: `cd42e3c310ba442e89dde638ba6401adaefaf3e8`.

## Verdict

C1 operability predicate **reproduces independently at the committed tip**: counter exit 0,
`registry_rows=2/2 receipts=2/2 C1_MET`; base control exit 1, `0/2`, `C1_NOT_MET`. Both receipts
are committed, name the exact tool path, carry the *correct* 64-hex digest of the committed tool
blob, show the tally I independently reproduced (`8/8`, `23/23`) and end in `exit=0`.

Residual adversarial finding (not a falsifier of C1 as written, but a predicate-strength limit):
the counter does **not** bind the receipt's 64-hex to the tool's real digest, and does **not**
require the PASS transcript. A receipt with a wrong digest or with the PASS lines stripped still
yields `C1_MET` (mutation controls below). The facts in the committed receipts are true; the
counter alone could not have proven them so.

## 1. Independent C1 counter run (committed script, committed revision)

Script identity: `.ufo/waves/round-47/c47_registry_count.py`, worktree sha256
`4065b1cb52908102efc56e4508149842c837d24aec44883916a192983f00d3b6` — byte-identical to
`git show 766f461:.ufo/waves/round-47/c47_registry_count.py` (same hash).

```
$ python3 -B .ufo/waves/round-47/c47_registry_count.py --root . --revision 766f4610b64f35a0f402b37eb1d8be2d4d634c0f
registry_rows=2/2 receipts=2/2 C1_MET
EXIT=0
```

```
$ python3 -B .ufo/waves/round-47/c47_registry_count.py --root . --revision cd42e3c310ba442e89dde638ba6401adaefaf3e8
registry_rows=0/2 receipts=0/2 C1_NOT_MET
EXIT=1
```

`--json -` at tip returned `registry_row_detail={"citation_lint.py": true, "redirect_audit.py":
true}`, `selftest_receipt_detail={"citation_lint.py": true, "redirect_audit.py": true}`,
`verdict="C1_MET"`, exit 0.

Registry rows located at `SKILL.md:1197` (`redirect-expectation-audit`,
`scripts/redirect_audit.py`, `23/23`) and `SKILL.md:1198` (`commit-citation-lint`,
`scripts/citation_lint.py`, `8/8`); worktree `SKILL.md` sha256
`a40a37d1fa10d27d75a88e9da3fe9c54bc32ce561fc5e81d80a7189b922385e6` equals the committed blob at
`766f461`.

## 2. Receipt files — paths and sha256 (worktree == committed blob)

| receipt path | receipt sha256 (worktree; identical committed) | committed at |
|---|---|---|
| `.ufo/waves/round-47/verification/selftest-citation-lint.txt` | `b3902de66b5b0ed56af51e2b8611d5505aab1585a496194b5746881b4ea0b735` | `846138c` |
| `.ufo/waves/round-47/verification/selftest-redirect-audit.txt` | `0760b0310b166e45585794fb889431e2d5577af76e70cebfbe85d213428ef056` | `846138c` |

Committed-blob hashes recomputed via `git show <rev>:<path> | sha256sum` are identical to the
worktree hashes above, and `git status --porcelain` shows neither receipt dirty.

Per-receipt field replay (line numbers from the files):

- citation: line 1 `command: python3 -B scripts/citation_lint.py --selftest`; line 3
  `tool_path: scripts/citation_lint.py`; line 4 `tool_sha256:
  3c78a0a82f70b166776f7f7626dc7afbf9f9916a4399ae879287e4bf9662987f`; line 15
  `selftest: 8/8 passed`; line 16 `exit=0`.
- redirect: line 1 `command: python3 -B scripts/redirect_audit.py --selftest`; line 3
  `tool_path: scripts/redirect_audit.py`; line 4 `tool_sha256:
  1e1dff18030c9028d833ab108bff140102343f4c5198c35984e7838e54bb748a`; line 30
  `selftest: 23/23 passed`; line 31 `exit=0`.
- Exactly one 64-hex token per receipt (`grep -oE '\b[0-9a-f]{64}\b'`), exactly one `exit=` line
  per receipt (line 16 / line 31). Sizes: 16 and 31 lines.

## 3. Digest binding checked independently (counter does not do this)

```
$ git show 766f461:scripts/citation_lint.py | sha256sum
3c78a0a82f70b166776f7f7626dc7afbf9f9916a4399ae879287e4bf9662987f
$ git show 766f461:scripts/redirect_audit.py | sha256sum
1e1dff18030c9028d833ab108bff140102343f4c5198c35984e7838e54bb748a
```

Same two digests at the receipt commit `846138c`; both tools last changed at `ee43e66`, so the
receipts were not stale at commit time or at tip. Worktree tool files hash identically to the
committed blobs.

## 4. Independent re-run of both selftests (observed tally)

```
$ python3 -B scripts/citation_lint.py --selftest
... 8 PASS lines ...
selftest: 8/8 passed            EXIT_CITATION=0
$ python3 -B scripts/redirect_audit.py --selftest
... 23 PASS lines ...
selftest: 23/23 passed          EXIT_REDIRECT=0
```

Both transcripts match the receipt bodies line-for-line, including mutant controls (F/G/H/E and
the six `mutant …`/`cli …` cases respectively).

## 5. Mutation controls (disposable clone, local only, never pushed)

Sandbox: `/fast/scratch/hyaku/kake-r47/ExecReceiptReplay/sandbox`, cloned from the lane, `origin`
removed after cloning; all mutations are local commits on top of `766f461`.

| mutation commit | change | counter result | exit |
|---|---|---|---|
| `97c4295` | citation `tool_sha256` replaced with 64 zeros | `2/2 2/2 C1_MET` | 0 |
| `13adf0f` | redirect receipt: all `  PASS` lines stripped, tally kept | `2/2 2/2 C1_MET` | 0 |
| `9bc195c` | redirect tally `23/23` → `22/23` | `2/2 1/2 C1_NOT_MET` | 1 |
| `4860764` | citation receipt deleted | `2/2 1/2 C1_NOT_MET` | 1 |

Reading: presence and tally bindings work; digest and transcript-detail bindings are absent.
Because facts were verified out-of-band in §3–§4, this is a predicate-hardening note, not a C1
falsification.

## 6. Risks / limits

- Counter weakness as tabulated in §5: a forged 64-hex or a token-only stub receipt is accepted.
  Anyone relying on the counter without the §3 digest check and §4 selftest re-run gets a weaker
  guarantee than "names the tool sha256" suggests.
- The counter matches any `|`-leading SKILL.md line containing the tool path; the two hits here
  are genuine gate-registry rows (`SKILL.md:1197-1198`), but the check does not inspect the
  gate's command/exit column.
- `run_at_utc: 2026-10-24T06:46:10Z` is identical in both receipts; consistent with one batched
  run, unverifiable as wall-clock evidence by replay.
- Unrelated worktree noise observed, untouched: `M .ufo/waves/round-47/w1/swarm-registry.json`,
  `?? .ufo/waves/round-46/residual/`.

## 7. Files changed

- `.ufo/waves/round-47/w1/ExecReceiptReplay.md` (this report; only write).
- Scratch: `/fast/scratch/hyaku/kake-r47/ExecReceiptReplay/sandbox` (local clone with four mutation
  commits, `origin` removed, nothing pushed).

Tooling installs/updates: none (git 2.x and system python3 sufficed; no pacman invoked).
Blockers: none.
