## Verdict

C2 is **not only a rerun of round 22**: it adds a GET-only live-byte capture, response metadata and digest, a saved page/manifest/audit receipt, and a revision-pinned replay of that receipt. It therefore adds real end-to-end operability and a dated freshness observation. The canonical-policy engine is still `canonical_audit.py` (with the round-23 parser extension); C2 does not add a new source of canonical policy or establish search-engine selection.

Do not describe the evidence as “12 clean canonicals” or “12 HTML pages evaluated.” The round-23 cache has 1 `clean`, 3 `failed-policy`, 4 `could-not-evaluate` (`html_unsupported`), and 4 `not-served` results. Moreover, I found only `measure-c2-before.json` in the round-23 directory listing, with `accepted: 0`, `total: 12`, at revision `6847479d404d1dd93ecb59f99ff735bd7f010a4a`; no after-counter result was present in that listing. Thus the capture artifacts are evidence of the operation, not proof that the frozen C2 acceptance count has passed.

## Findings

### P2 — The new live path needs its own gate semantics (operability; preserve freshness meaning)

**Evidence and exact observations**

- `SKILL.md:394-407` labels the round-22 preflight offline over built HTML, says it “does not … probe live properties,” and routes live/HTTP facts outside that gate. `SKILL.md:409-411` registers only `canonical-audit`, whose entry command is `python3 scripts/canonical_audit.py --manifest <local-manifest> --json` and whose normal invocation is read-only/network-free.
- `corpus/README.md:42` likewise lists “Static canonical preflight (r22)” as source-backed policy comparison plus local fixture proof. `corpus/knowledge/static-canonical-preflight.md:53-56` states that no production artifact was available or claimed tested in round 22.
- Round-22 local proof is distinct: `.ufo/waves/round-22/domain-integrated.json:10-14` records `exit: 0`, `pagesChecked: 1`, `verdict: clean`, with the round-22 validator digest and Python version.
- The r23 capture implementation adds a separate boundary: `scripts/live_snapshot.py:53-81` issues GET and captures status, final URL, content type, bytes, SHA-256, truncation and fetch time; `:84-91` runs the validator against a generated manifest; `:114-128` saves fetch/audit receipts and stores served HTML. `.ufo/waves/round-23/measure_c2.py:63-84` verifies the stored body digest and re-runs the validator bytes from the selected Git revision, requiring exact receipt equality. This is capture plus replay, not simply rerunning r22's local manifest.
- There is also a bounded parser delta in the candidate validator: `scripts/canonical_audit.py:106-108`, `:197-224`, and `:285-295` describe/support SVG/MathML after a closed head and self-closed HTML void elements, while retaining unsupported-shape rejection.
- The cached per-surface results in `.ufo/waves/round-23/live-summary.json:4-24,44-54` include:

```json
{"id":"charter-ghp","status":200,"verdict":"clean","findings":[]}
{"id":"plazir27-kimi","status":404,"verdict":"not-served","findings":[]}
```

A further counterexample to the broad assertion “all 12 received a canonical verdict” is `plazir27-kimi`: `.ufo/waves/round-23/live/plazir27-kimi/audit.json:1-6` records `{"error":null,"exit":null,"status":404,"verdict":"not-served"}`. No canonical HTML was audited for that surface. The captured `ds4cc-primary` is a second boundary case: `.ufo/waves/round-23/live/ds4cc-primary/audit.json:1-13` records status-200 HTML as `exit: 2`, `html_unsupported`, `could-not-evaluate`.
- This limitation is aligned with the frozen scope: `contract.json:21-26` explicitly says non-served surfaces record status and describes snapshots as observations at fetch time; `c2-population.json:4-5` limits the population to public page URLs and excludes `app.ds4cc.com/mcp` because it is an API endpoint, not a page.
- Counter semantics matter: `measure_c2.py:57-62` returns a valid `not-served` result when its status receipt matches; `:82-84` treats a reproduced policy result as receipt-valid unless the receipt differs; `:101-108` counts rows with no receipt problems as `accepted`. A C2 counter pass would mean complete, reproducible receipts for the population, **not** that each policy verdict is `clean` or even evaluable.

**Impacted claim/axes:** C2 adds operability by making live served bytes auditable and revision-reproducible. The `fetchedAt`/digest support a time-bounded freshness observation, but replay alone does not refresh the live site. A reader who treats counter `accepted` as canonical health would overstate both the C2 outcome and what is fresh.

**Smallest fix / proposed move:** add one separate `canonical-live-snapshot` row to the `SKILL.md` gate registry, rather than expanding or relabeling `canonical-audit`. Give it the two-step meaning: (1) run `live_snapshot.py` for a new GET observation, recording fetchedAt/status/finalUrl/digest; (2) run `measure_c2.py --root . --revision <commit>` to reproduce the committed capture's receipt. State explicitly that the counter measures receipt completeness/reproducibility and that its per-surface verdicts remain `clean`, `failed-policy`, `could-not-evaluate`, or `not-served`. Keep r22's offline gate boundary intact.

## Checked and held

- Read the requested province, corpus README, static-canonical knowledge entry, SKILL gate registry, frozen r23 contract, C1/C2 populations, relevant scripts and the local r22/r23 round-cache artifacts.
- **Axes:** direct gain is operability (a documented repeatable live-capture/replay route); freshness is preserved by retaining per-fetch timestamps and digests, but a replay is not a new live check.
- **Risk:** without the separate row and verdict distinction, an operator could mistake a reproducible `not-served`/unsupported/policy-failure receipt for a healthy page, or mistake historical replay for a fresh GET. The 12-page population is not every owned endpoint; the API exclusion is intentional.
- **Verification to run after the planner integrates the move:** invoke the documented live snapshot capture against the frozen population, commit its fetch/body/audit artifacts, then run `python3 .ufo/waves/round-23/measure_c2.py --root . --revision <that-commit>`. Confirm the counter reproduces all 12 receipts and report the four policy/evaluability classes separately from its accepted count. A re-run of the counter alone must not be reported as fresh observation. These checks were not run by me.
- No public GET/HEAD, CLI selftest, build, lint, formatter, or install/update was performed by me. I did not edit production files or claim independent admission.

## Limits

The `live-summary.json` and per-surface records are local round-cache artifacts, not a GET I issued in this assignment; the recorded sample `fetchedAt` in `live/ds4cc-primary/fetch.json:5` is `2026-10-21T06:33:03Z`. No after-counter was observed, so the cache does not establish C2 completion. The static policy still cannot prove Google-selected canonicals, browser/JavaScript behavior, redirects beyond recorded HTTP metadata, or publishing readiness; see `corpus/knowledge/static-canonical-preflight.md:67-78,90-94` and `contract.json:26`.