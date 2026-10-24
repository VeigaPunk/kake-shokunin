# ReviewCharterOgBlock — ledger row `d69dd22` vs LOG.md charter-ghp clause + R4 correction

- seat: ReviewCharterOgBlock (reviewer, w1, round 47)
- lane: `kake-shokunin` · lane tip read: `766f4610b64f35a0f402b37eb1d8be2d4d634c0f` · frozen base: `cd42e3c310ba442e89dde638ba6401adaefaf3e8`
- scope: one adjudication row (`d69dd22`) and the R4 correction that claims to repair it. Read-only; no lane file outside this report was written; no mutating `git`/`jj`; no sibling/fleet path read; no tool installed or updated.
- **verdict: the corrected reason correctly identifies the charter repo and the historical commit. No blocking defect on this row.** Two low-severity verification-quality notes and three scoping residuals below.

## 1. The three artifacts, verbatim

**Ledger row (original cell, still present by design)** — `corpus/quality/citation-adjudications.md:24`:

```
| `d69dd22` | LOG.md | external-repo commit | ds4cc-marketplace repo commit in the 2026-09-28 push series (external, absent). |
```

**Citing clause** — `LOG.md:47-52` (round-13 entry, which starts at `LOG.md:21`):

```
  surfaces. (4) charter-ghp: pin-lag persists BUT live is deploy-current —
  the HUMAN pushed 5 commits 18:32:06–20:43:21Z (`b74190e` bake →
  `d69dd22` og-block → `0c767c2` window sync → `b9db4b1` CORRECTION →
  `a8f1e2b` fixup), Pages served each within ~30s (live sha `0decd827…`
  == `a8f1e2b`, 53,353B); "churn paused" rescoped to the scribe automation
  only; local clone lags 5 (`61d0ce6`).
```

**R4 correction bullet** — `corpus/quality/citation-adjudications.md:43-44`:

```
- Row `d69dd22` | LOG.md — same misattribution; corrected reason: charter repo
  commit in the 2026-09-28 push series (external, absent).
```

LOG's own R4 restatement (`LOG.md:1804-1807`) agrees: the four tokens "nam[e] the charter repo's 2026-09-28 push series", and "classes were and stay correct".

## 2. Does the reason identify the repo correctly? Yes — three in-lane grounds

1. The clause is under `(4) charter-ghp` (`LOG.md:47`) and is completed by the same entry's `(6) Charter post-push subpath audit (b74190e…a8f1e2b series)` at `LOG.md:108` — LOG.md labels the series itself as **Charter**.
2. `corpus/knowledge/keeper-timer-inert.md:163-165` (r13 addendum) names the destination of the identical five hashes: "the **human pushed 5 commits directly to `origin/main`** of `~/Projects/origin-work/charter-ufo-fsd` (`b74190e` bake gold snapshot → `d69dd22` og/twitter/hreflang → `0c767c2` … )". Same hash, same order, same window.
3. `corpus/knowledge/fleet-registry.md:60` pins the surface to the repo: `| charter-ghp | veigapunk.github.io/charter-ufo-fsd | live (canonical doc) | ~/Projects/origin-work/charter-ufo-fsd |`; rows 55, 57 and 59 use `charter repo` as the lane's standard owner label for the same repo family.

The original `ds4cc-marketplace` attribution is contradicted by all three records; the `ds4cc` series is separately adjudicated (`f3d2ecd`, `e6bd071` at ledger lines 19-20). **The R4 correction is substantively right for `d69dd22`.**

## 3. Does it identify the historical commit correctly? Yes

- Series: the five human pushes `18:32:06–20:43:21Z` on 2026-09-28, `d69dd22` second (`og-block`; `og/twitter/hreflang` per keeper-timer). The reason's "in the 2026-09-28 push series" is exact and non-overclaiming.
- `external`: correct — the repo is outside the lane.
- `absent`: true in the ledger preamble's defined sense (line 5-6: "re-verified non-resolving in the lane repository (`git rev-parse -q --verify`)"). Re-checked at tip:
  - `git rev-parse -q --verify 'd69dd22^{commit}'` → nonzero (non-resolving); same for `b74190e`, `0c767c2`, `b9db4b1`.
- The class `external-repo commit` stays correct after the reason change, so the block's "classes were and stay correct" holds for this row.

## 4. Append-only claim holds

- `git diff --numstat cd42e3c310ba442e89dde638ba6401adaefaf3e8 -- corpus/quality/citation-adjudications.md` → `25	0` (insertions, deletions).
- `git show cd42e3c…:corpus/quality/citation-adjudications.md | sed -n '1,29p'` vs current lines 1-29 → no diff (`PREFIX_1_29_IDENTICAL`), so the row at line 24 keeps its original defective reason byte-for-byte; the correction is a pure tail. This is the round-20 ruling's mechanism (`corpus/QUALITY.md:31-39`).
- The block's statement that `scripts/citation_lint.py` "reads only token + file + class" is true: `scripts/citation_lint.py:121` destructures `_reason` and never uses it; the ledger's table is read only for `(token, file) → class` at `:121-123`. The ledger is not in the scanned population (`POPULATION = ("SCORECARD.md", "LOG.md")`, `:39`), so the appended block cannot create new violations.

## 5. Live behaviour reproduced (read-only)

| command | observed |
|---|---|
| `python3 -B .ufo/waves/round-47/c47_r4_mutation_check.py --root . --revision 766f4610…` | `R4_REASON_FIDELITY base=pass mutants=5/5_rejected PASS`, exit 0 |
| `python3 -B scripts/citation_lint.py --root .` | exit 0, `violations: 0`; `adjudicated` contains `{"class":"external-repo commit","file":"LOG.md","line":49,"token":"d69dd22"}` |
| `sha256sum .ufo/waves/round-47/verification/c2-r4-mutation.txt` | `1e7636ecb023b2d2fa61d5bb6904166ebe84337514beed175c8010675cd507c3` — equals LOG/report claim |
| `git show 714e707…:corpus/quality/citation-adjudications.md \| sha256sum` | `e75bc3a746539d86651f4b31f578480702fc325cbe1e1555cd76aa38d5058669` — equals receipt's `ledger_sha256_at_revision`; also equal at HEAD and worktree |
| `git show 714e707…:.ufo/waves/round-47/c47_routed_count.py \| sha256sum` | `9be35ef2452aaff0757a0c2839c17cb58e08a7a59f6a217a3489598c19a8359e` — equals receipt |
| `sha256sum .ufo/waves/round-47/c47_r4_mutation_check.py` (HEAD and `714e707`) | `0c8aa7a4357e836e0011871900d0e26bbb4f4c426b91ea2634538405c482ada2` — equals receipt |

The r46 pre-state also keys the same row correctly: `.ufo/waves/round-46/verification/c2-before-7cdbaefd.json` `violations[16]` = `{"file":"LOG.md","line":49,"reason":"dead_citation","token":"d69dd22"}`.

## 6. Findings

### Low-1 — the committed "able-to-fail" control is phrase-presence, not reason fidelity
`c47_routed_count.py:100-113` (`r4_reasons_fixed`) takes **only the ledger text** and asserts `R4_EXPECTED` phrases appear under the matching `- Row \`<token>\``; it never reads `LOG.md`. `c47_r4_mutation_check.py:64-71` mutates only inside the ledger (`charter repo commit` → `ds4cc-marketplace repo commit`, `CriticProbeLeniency` → `CriticC2Sufficiency`). Hence `R4_REASON_FIDELITY … PASS` (reproduced, exit 0) proves the correction block was *written as intended*, not that it *matches the citing line*. The new QUALITY criterion (`corpus/QUALITY.md:1072`, "Citation reason fidelity") is therefore grounded only by independent reading — this report's §2/§3 — not by any committed control. Advisory, not a row defect: for `d69dd22` the independent check passes.
Reproduction limits of this claim: structural, from the cited source lines plus one PASS run; I did not build a counter-mutant that keeps the phrase while contradicting LOG (the function has no LOG input, so no such mutant can be killed).

### Low-2 — the four charter bullets are non-uniform and `d69dd22` carries no superseded-reason quote
`b74190e`'s bullet quotes its old reason (`:38-42`); the `d69dd22`/`0c767c2`/`b9db4b1` bullets say only "same misattribution" (`:43-47`). They cite their rows by token, which satisfies the round-20 ruling's "correction blocks citing the old line" as written, and the corrected reason is stated in full — but a reader of row 24 alone gets no forward pointer, and the justification for the row is one hop away in the `b74190e` bullet. Documentation-quality only; the substantive reason is unambiguous.

### Info-1 — "charter repo" is lane shorthand, not the canonical path
The lane's canonical name for the repo is `~/Projects/origin-work/charter-ufo-fsd` (`fleet-registry.md:60`, `keeper-timer-inert.md:163`). "charter repo" is established corpus vocabulary (`fleet-registry.md:55,57,59`), so it is not ambiguous to a corpus reader; but a future correction could name the path and the commit role (`og-block`) to make the row self-describing.

### Info-2 — `absent` is scoped, not host-wide
The r18 annotation on the same knowledge lines says only the `origin-work` clone is gone (2026-10-12 prune); `corpus/knowledge/origin-repos.md:24` maps the same Pages site to `repos/charter-ufo-fsd`, whose presence I did not inspect (sibling/fleet paths out of bounds). The ledger's own definition of "absent" is lane-object-store non-resolution, which is verified above. Do not cite this row as proof the repo vanished from the host.

### Info-3 — the defective cell survives by design
Row 24 still reads `ds4cc-marketplace …`; only §Round-47 corrections supersedes it. No current consumer reads the reason (`citation_lint.py:121` ignores it), so nothing breaks today; any future reason-reading consumer must parse the correction block, not the table.

## 7. Residual risk and verification gaps

- No sibling/fleet checkout of `charter-ufo-fsd` was inspected (lane bounds), so I could not confirm the five hashes against the repo's own object store; repo attribution rests on three independent in-lane records (`LOG.md:47-51,108`; `keeper-timer-inert.md:163-165`; `fleet-registry.md:60`).
- No network call; the series' live-Pages claim (`a8f1e2b` == live sha) is taken from committed records, not re-probed.
- I did not execute `c47_registry_count.py`, the freshness selftest, or any write-bearing harness — out of this row's scope.
- Nothing in this report changes contract, axes, routes or judgment; it is one advisory input.

## 8. SHONEN

- [x] Row `d69dd22` corrected reason checked against the exact `LOG.md:47-52` clause: repo = charter (`charter-ghp` → `origin-work/charter-ufo-fsd`), series = 2026-09-28 human pushes, commit = 2nd (`og-block`) — match confirmed by three independent in-lane records.
- [x] Append-only mechanism verified byte-level (`25/0`; prefix 1-29 identical), and the appended block cannot create lint violations.
- [x] Receipt identity independently recomputed (file sha256 and all three internal shas equal); helper reproduction PASS, exit 0.
- [ ] Lane control proving reason-vs-citing-line fidelity (Low-1) does not exist; the criterion currently depends on manual review.
