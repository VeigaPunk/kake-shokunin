# ResidReviewRecords — round-41 records vs lane state b9bf1a3 (final tool 50287ac6…1dde7d verified)

Checked SKILL.md:1157-1172 (small-manifest tests of each sentence), corpus/lessons/round-41.md (pointer
sweep + fix-able-to-fail reruns), corpus/QUALITY.md (s)(t)(u) vs scripts at criteria/. Sandbox
/fast/scratch/hyaku/kake-r41resid/KakeR41.ResidReviewRecords/ (harness.py, sweep.py, cases/, outputs).
No tools installed. All runs `timeout`+`prlimit --as=4000000000`.

## Commands (all in /home/vgpnk/Projects/shokunin/kake-shokunin, exit codes recorded)
- `git rev-parse HEAD` → b9bf1a3… ✓; `sha256sum scripts/sitemap_audit.py` → 50287ac6de5600ab…1dde7d ✓.
- `python3 -B .ufo/waves/round-41/criteria/live_tally_check.py --dispatch-log .ufo/waves/round-41/w1-dispatch-log.txt --receipts .ufo/waves/round-41/verification/w1` → "141 receipts, dead-seat 0", exit 0.
- Same with round-40 log/receipts → 4 `CtlUTabOnly-dead__*` listed, exit 1 (re-derived from round-40 bytes).
- `fresh_review_check.py --tool-sha 50287ac6… --reports .ufo/waves/round-41/w2` → 1 hit `w2/ReviewSkillAmendment.md`, exit 0; `--tool-sha 4de35f8c… --reports .ufo/waves/round-40/w1` → 0, exit 1 (re-derived).
- `sitemap_audit_selftest.py --tool scripts/sitemap_audit.py` → `PASS 225/225` exit 0; on extracted base `git show 8eb121c8:…` (4de35f8c…1460e ✓) → `PASS 196/225`, 29 FAIL lines, all `r41_*`; selftest sha 18752057…01bf8 ✓.
- `sitemap_audit.py --manifest .ufo/waves/round-41/realrun/manifest.json | jq -S . | sha256sum` → fd985a41867…8a5 ✓ (byte-equal claim reproduced).
- Harness: 52 checks (35 sitemapUrl + 17 loc) run on final, base 4de35f8c, and first build `git show eae5ae2c:…` (0b485431… ✓): PROBLEMS none; per-case table in sandbox.
- Pointer sweep over round-41.md: 23/23 path:line pointers resolve (incl. c1_count.py:117-119 read: `insert` = `randint(1, len-1)`, interior-only; single IP-literal template ✓).
- Receipts: w1 141 files, 15 met; w1v2 141, 10 met; w2 33 reports; `CtlNoPct__terminal_pct`/`CtlGeneratorShape__v1_shape` met:true 1434/1434 under v1, met:false (1433, 1365) under v2 ✓.
- Sources: `sha256sum -c sources/SHA256SUMS` exit 0; rfc3986.txt 3102dae4…d683 ✓; oracle wheels cdcac127…0917, 10702b1e…ce53 ✓; oracle-crosscheck 14340 cases/0 disagreements (v1+v2 receipts; counter sha 2acc443a…67b4 ✓).

## Per-statement verdicts
- SKILL S1 (sha; TAB/LF/CR in IP literal invalid): holds. Final `check_invalid`/`loc_not_absolute`;
  first build 0b485431 passed them (`loc_out_of_scope` — regression corroborated); base rejected.
- S2 (RFC 3986-first; sentence-21 strip for loc): holds (`lo_pad` clean; `su_space_path` base clean →
  final check_invalid, i.e. urlsplit-accepts/RFC-rejects is now judged by the grammar first).
- S3 (char classes): holds for sitemapUrl — all 24 listed classes `check_invalid`, base accepted the
  path/query/fragment ones; loc classes `loc_not_absolute`; C0 char-ref → `xml_malformed`.
  Overstated (see findings 1–2).
- S4 (U+0080+ and urlsplit carve-outs unchanged): holds in behavior (non-ASCII path clean both;
  port>65535, zone-id, IP-host codes identical final vs base). Overstated wording (finding 3).
- S5 (exploratory; 15/141; counter is information): holds (recounted).
- Lesson Mistakes 1–3 fixes "shown able to fail": holds — receipts and both criteria scripts re-derived
  red on round 40 / green on round 41 exactly as the lesson states.
- Lesson Mistake 4 ((r) green on this counter): receipts exist (`verification/r40standing/`) but I did
  not re-run the counter; not independently re-verified.

## Findings (severity, path:line)
1. LOW SKILL.md:1162-1163 — DEL in a `loc` gives `xml_malformed` (final AND round-40 base; XML layer,
   observed), not `loc_not_absolute`; the sentence lists DEL among loc_not_absolute givers and says the
   round-40 tool accepted them — wrong for DEL-in-loc on both counts (DEL-in-`sitemapUrl` is
   `check_invalid` as claimed). Suggest "DEL (in `sitemapUrl`; a `loc` with DEL gives `xml_malformed`)".
2. LOW SKILL.md:1162-1163 — "a space … where the round-40 tool accepted them" holds for space in
   path/query/fragment (base clean → rejected now) but a space in the host was already rejected by the
   round-40 tool (`loc_out_of_scope`, my su_space/lo_space). Per-position truth, positional wording.
3. LOW SKILL.md:1166 — "U+0080 and above are still accepted wherever RFC 3986 allows `unreserved`":
   true in path (U+0085, NEL clean both rounds) but non-ASCII in the host gives `loc_out_of_scope` on
   both rounds (unchanged scope rule); "wherever" overstates.
4. INFO `.ufo/waves/round-41/resid/` absent at check time (2026-10-23T~11:20Z): the only seat report
   naming the final sha is w2/ReviewSkillAmendment.md, and it is a genuine review of the final bytes
   (~70 manifests, base+first-build diffs), not a mere sha quotation — so (t) is green on real review;
   residual fresh reviews still pending should land in resid/.

## Residual risk / gaps
- (r)/Mistake-4 standing-control scores and counter/v2 seeds taken from committed receipts, not re-run.
- ReviewSkillAmendment reviewed SKILL text at 204 fixtures (pre-extension); I re-verified against the
  landed 225-fixture state — all re-checked sentences hold.
- First build only spot-checked on the 4 IP-literal/whitespace cases, not the full 52-case matrix.
