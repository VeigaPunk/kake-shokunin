# Draft — SCORECARD capabilities row for C1 (round 46)

Status: **DRAFT, not an entry claim.** Written in wave 1 at HEAD
`ded938d2f23aba265d1acf1fdd4b3ab028020037`, before the C1 tool, matrix,
fixtures or selftest existed. Every `⟨…⟩` below is unmeasured and must be
filled from the committed bytes/receipts; the row enters `SCORECARD.md`
`## Capabilities` only if the after stage meets the frozen predicate. Per
`AXES.md` §Capabilities: “Rows enter only through a round that demonstrates
the capability running; a capability without a passing demonstration in the
round report is pre-claiming and does not enter the table.”

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| Offline static-host redirect/rewrite audit | Reads a version-1 manifest of static-host redirect/rewrite checks — local `_redirects`-form rule files, existing-resource path lists, request paths and the expected decision for each check — and reports, read-only and network-free, every check whose decided outcome differs from its expectation, with the decided outcome, status and resolved target beside the expectation (rule parsing for splats, `:placeholder` segments and the force and rewrite flags; first-match order; no rule applied where a resource exists at the request path; 301/302/307/308 status and target; relative targets resolved (S088); rewrite pass-through at the original path (S050); malformed-rule faults; stable finding ids; exits 0/1/2/64); no fetch, live host, DNS, response-header, rendered-DOM or engine-acceptance claim; the matrix certifies its ⟨N⟩ planted witness classes, not every contract sentence | `scripts/redirect_audit.py` (sha256 `⟨tool sha256⟩`); selftest `python3 -B scripts/redirect_audit.py --selftest` → ⟨N⟩/⟨N⟩ exit 0 (receipt `⟨path⟩`, sha256 `⟨…⟩`); after: `python3 -B .ufo/waves/round-46/c46_matrix.py --root . --revision ⟨round-46 tip commit⟩ --stage after` → `witnesses_caught` ⟨N⟩/⟨N⟩, do-nothing/constant/junk controls rejected, exit 0 (receipt `⟨path⟩`, sha256 `⟨…⟩`; pins `toolSha256` and `selftestSha256`); before: same command `--stage before` → ⟨at least one planted witness uncaught or one do-nothing/constant/junk control accepted⟩ (receipt `⟨path⟩`, sha256 `⟨…⟩`) | 46 |

## Fill-at-integration

1. Tool identity: `sha256sum scripts/redirect_audit.py`; confirm the
   committed blob equals the measured blob.
2. Selftest: `python3 -B scripts/redirect_audit.py --selftest`; record the
   verbatim tally and exit, and the receipt path + sha256 (criterion (l),
   `corpus/QUALITY.md`, requires `toolRevision`, `toolSha256`,
   `selftestSha256` on a post-measurement receipt).
3. Matrix after: `python3 -B .ufo/waves/round-46/c46_matrix.py --root .
   --revision ⟨tip⟩ --stage after`. Fill `witnesses_caught` /
   `witnesses_total`, the control verdicts (all of do-nothing, constant and
   junk must read `rejected`), `exit` and `wall_s` (routed defect 4: under
   120 s), and the receipt path + sha256.
4. Matrix before: the same command `--stage before`. The scratch baseline
   tool (`.ufo/waves/round-46/controls/before-tool.py`) must leave at least
   one planted witness uncaught, or one of the three controls accepted;
   fill the actual result and receipt path + sha256.
5. Reconcile the behaviour list against the landed tool: keep only rule
   classes the tool actually decides, and replace the generic “decided
   outcome” wording with the tool's own outcome vocabulary. Drop any class
   the matrix does not witness.
6. Paste the filled row only after the after receipt is committed and
   re-derivable from the named revision; every filed count in the row cites
   its receipt path + sha256.

## Provenance at draft time

- `git ls-tree -r --name-only HEAD scripts/ | grep -c '^scripts/redirect_audit.py$'` → `0`.
- `git ls-tree -r --name-only HEAD .ufo/waves/round-46/ | grep -c 'c46_matrix.py'` → `0`.
- `python3 -B .ufo/waves/round-46/c46_matrix.py --root . --revision ded938d2… --stage after` → `can't open file ... [Errno 2] No such file or directory`, exit 2.
- `python3 -B scripts/redirect_audit.py --selftest` → `can't open file ... [Errno 2] No such file or directory`, exit 2.
- Wave-1 seat `ExecRedirectSelftest` recorded the same absence and left all
  six mutant probes unrun (`.ufo/waves/round-46/build/redirect-selftest.md`).
