# ReviewAblationDesign — do the 36 ablation receipts show every contract bullet moves the target?

Scope: read all 37 JSONs in `.ufo/waves/round-36/verification/ablations/` (36 ablations +
reference) and the C1 contract at `cd321279:SCORECARD.md`. No sealed paths touched. Counter on
disk `sealed_count.py` sha256 `88ec5914…` matches every receipt's `counterSha256` (v3).

## Case layout recovered from receipts
Each home ablation fails exactly its bullet's four ids, so the block map is:
k01–k04 (a), k05–k08 (b), k09–k12 (c), k13–k16 (d), k17–k20 (e), k21–k24 (f), k25–k28 (g).
Cross-block failures reveal case design, noted below.

## Ablation → contract sentence map (score, fails)
- a_204ok 24, a_410err 22(+k26,k28 → two g cases contain 410 checks), a_none 16(+all b,all g
  → b/g cases exercise status decisions): bullet (a) final-status rules — 200→quote, 404/410→
  `gone`, other→`http_error`, no quote check unless 200.
- b_none/b_noresolve/b_firstonly/b_anywhere/b_final 24 each: bullet (b) — permanent-vs-temporary
  leading run, RFC 3986 resolution base, `moved` target = last leading-permanent location.
- c_keepcomment/c_keepstyle/c_keeptemplate/c_nohead 24, c_keepscript 20(+k17–20 → e cases carry
  script text), c_noentity 19(+k13,k17–20), c_raw 16(+all d,all e): bullet (c) — comments,
  script/style/template removal (S025), tag stripping, entity decode, title kept.
- d_casefold (case-sensitivity), d_collapse (isspace-delete vs collapse), d_nonfkc (NFKC),
  d_exact 23(+k11): bullet (d) — NFKC + delete-isspace + case-sensitive substring.
- e_allhtml/e_alltext/e_noxhtml 22(+k10,k12 → two c cases are xhtml), e_casesens 17(+c,d minus
  k16): bullet (e) — media-type split, text/plain raw, xhtml HTML-rules, case-insensitive match.
- f_nobom (BOM beats charset), f_pylatin (latin1→windows-1252 label table), f_noquote (trim +
  strip quotes), f_utf8only (label whitelist→`charset_unsupported`), f_nounsupported,
  f_labelcase 14(+c,d,e cases → charset labels across non-f cases): bullet (f) decoding.
- g_abort (input_invalid path), g_noescape (path escape), g_noloc (redirect sans location),
  g_nourlcheck (URL scheme/host), g_skip (continue after bad check): bullet (g) input faults.
- s_ctkey 13, s_unsure 24: shortcut probes, not rule ablations (scorecard names them as such).

## Support for the claim
Declared: "each of the 34 rule ablations fails at least the four cases of its bullet (at most
24 of 28)". Observed: every rule ablation fails all four home cases; none met (13–24). Each
bullet is therefore load-bearing — no bullet's rules can be wholly skipped for free. Cross-block
failures (a_410err, c_keepscript, e_casesens, f_labelcase, s_ctkey) show key-v2 checks bind
bullets together, so label-keyed shortcuts cannot pick off bullets e/f as the old key allowed.

## Uncovered rules — could a tool skipping one still reach 25?
Free (no case exercises them; bounded risk noted):
1. Exit 64 usage error — no case calls without `--manifest`. FREE.
2. `checksEvaluated` counting (g) — contract: not compared. FREE by design.
3. Output `version:1`, field order, extra fields — not compared. FREE by design.
4. `target` on non-`moved` findings — ignored. FREE by design.
5. `check` = null vs id on `input_invalid` — fixed null; covered only if a g case is a
   manifest-level fault AND g_abort shows it is. Covered.
6. Fragment inheritance — declared out of scope. N/A.

Bounded (at most the 4 home cases; skip is free only if no g case carries that fault):
7. `hops` non-empty; last-hop-is-not-redirect / mid-hops-are-redirect validity; hop status
   100–599 range; last-200 requires contentType+body — no dedicated ablation. If a g case uses
   a redirect-final or out-of-range hop the skip is caught; otherwise FREE (≤4 cases at stake).
8. `id` non-object/empty → `check:null` — only covered if a g case has such a check; else FREE.
9. `quote`/`contentType` non-string faults — same bound: caught iff present in k25–k28.
10. Missing/empty `location` IS covered (g_noloc); URL validity IS covered (g_nourlcheck);
    manifest-level faults ARE covered (g_abort); continue-after-fault IS covered (g_skip).

Implicitly covered by multiset equality (no ablation needed): "no other finding for a
check_invalid check" and "one finding per rule" — extra/missing findings fail the multiset.
Verdict mapping is enforced transitively: `could-not-evaluate` on g/f cases, `failed-policy`
elsewhere; a wrong verdict loses whole blocks (≥8 cases), so skipping it cannot reach 25.
Caveat: if zero cases expect `clean`/exit 0, the clean-path exit code is untested — cannot
confirm case verdict mix from receipts alone (findings not in receipts). [INFERENCE — low risk:
a clean-expecting case would be unusual for this design, but unverified.]

Narrower-than-ablation skips (e.g. hex refs only within entity decode, UTF-16BE BOM only) are
not proven caught — each home case would have to exercise that exact sub-rule. Bound: a
coincidentally-right narrow skip could pass all 28. Same residual the s_ctkey redesign addressed.

## Verdict on the receipts (advisory)
Supported: every bullet moves the target; no bullet is skippable for free; all ablations fail
≥4 cases including their entire home block. Gaps are per-sub-rule, not per-bullet: worst case a
sub-rule inside one bullet is unguarded (≤4 cases) plus untested usage-exit/clean-path edges.
Nothing found that lets a 25-of-28 tool omit a whole contract bullet.

Not verified: case contents, per-case expected verdicts/findings, ablation source code (paths
redacted), whether g cases cover each manifest fault type above.
