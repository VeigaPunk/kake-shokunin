# ConnectorSibling — round 85, w1

## Axes and disposition

Declared axes: **C1 calibration** (registry completeness 0/3 → 3/3, score HOLD 2) and **C2 freshness** (new Referrer-Policy decoder 0/10 → 10/10, score HOLD 10). This is an author-side read-only investigation, not independent closure, admission, or a target measurement. No full D84-queue closure claim.

Read host rules first, then Godspeed, frozen contract and complete count.py before substantive investigation. Production files stayed read-only. Assimilation: none.

## Sibling overlap: bounded sweep

Searched `/home/vgpnk/Projects/shokunin/*/corpus/**/*.md`, excluding kake and corpus `live/` and `fixtures/` subtrees; case-insensitive patterns `Referrer.Policy|effective.token`, then `Referrer.Policy|effective.token|header.policy|response.header`. The registry enumeration found 21 corpus registries including kake, i.e. 20 neighboring registry-bearing lanes. These are local current bytes, not globally exhaustive ownership evidence.

**Exact Referrer-Policy/effective-token search: no matches.** The wider search returned adjacent header material, not an effective Referrer-Policy decoder:

- kama: `/home/vgpnk/Projects/shokunin/kama-shokunin/corpus/lessons/round-1-safety.md:85-87` concerns approval/redaction/credential header policy; round-48 lesson and spot-check concern HF artifact identity via `x-repo-commit`/`x-linked-etag`. Neither owns browser policy-token resolution.
- kumitate: `/home/vgpnk/Projects/shokunin/kumitate-shokunin/corpus/knowledge/self-asserted-instants.md:23-35` uses RFC 9111 Age to distinguish timestamps and elapsed age, explicitly disclosing its receipt-clock divergence. Shared HTTP substrate, different predicate.
- mori: `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md:48` owns Retry-After waiting semantics; `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/knowledge/ua-serving-normative-r79.md:40` bounds cache selection/Vary evidence, not origin negotiation or measured response policy.
- tabi: `/home/vgpnk/Projects/shokunin/tabi-shokunin/corpus/knowledge/host-published-rate-limit-headers.md:23-25` concerns host rate-limit signals; its WebDriver BiDi entries concern raw wire/status/headers and collection behavior. Capture/transport adjacency does not imply Referrer-Policy semantics ownership.
- kengaku, tameshi and tsukuroi matches concern streaming routing, header redaction and mirror Last-Modified, respectively, not this decoder.

Receipt: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-85/w1/ConnectorSibling/sweep-receipt.json` retains query scope and both tool results. An initial broader sweep included vendor JS fixtures and was narrowed to curated Markdown rather than treating vendor bytes as ownership. Limits: no code-wide, non-Markdown, hidden-live, remote or historical sweep; absence here is not universal absence.

Within kake the overlap is explicit and complementary: `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/knowledge/response-header-expectations.md:5-7` describes six generic header expectations, not Referrer-Policy token decoding. `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/knowledge/policy-value-classes.md:89-95` labels the r84 general classifier experimental and forbids using its equivalence label to waive drift or authorize publication. The new field-specific decoder must not be described as repairing or certifying that general audit.

## S458 and staged registry collisions

Ran a local Python Eval parser over both full source registries. Row recognition: `^ {0,3}\\|\\s*(S\\d+)\\s*\\|`; split cells at unescaped pipes and extract HTTP(S) URLs from the source cell only. This tolerates zero through three leading spaces and avoids treating escaped shell-pipeline pipes in staged cells as separators. Actual matched rows had zero leading spaces in both inputs.

Inputs and immutable-byte receipts:

- Current `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md`: **195 rows**, sha256 `22c7f1ceb025e17ff20b0a22fcac89567e96f232017d4b3a820eb0e4bc00201c`.
- Staged `/home/vgpnk/Projects/shokuknow/merge/kake/SOURCES.append.md`: **129 rows**, sha256 `5f0cd4c4debc647f3d1e2a85519d4ae2b000d91dad49765514871fa502e9f0cc`.
- **S458 occurs in neither registry.** No source-cell URL containing `referrer-policy` occurs in either registry. Thus the planned S458/Referrer-Policy source has no observed ID or named-spec URL collision in these snapshots; this is not source admission or proof the source was opened.
- Existing cross-registry ID collisions: **S312, S329, S367, S372, S373, S374, S390, S409**. Each same-ID pair has the same exact extracted URL set; these are identity overlap, not an observed different-URL ID conflict. This says nothing about equality of teaches/quotes/status.
- **30 URL-collision row pairs, 27 distinct exact URLs.** Full IDs, URLs and line locators are in the collision receipt. In addition to the eight same-ID pairs: current→staged S080→S296, S137→S287, S138→S288, S139→S289, S249→S399, S273→S310, S274→S311, S286→S323, S262→S299, S263→S300, S416→S329, S417→S312, S418→S380, S419→S375, S420→S376, S421→S403, S422→S408, S423→S395, S425→S398, S427→S398, S429→S415, S438→S352.

Exact URL equality only: no redirects, host aliases, trailing-slash removal or fragment canonicalization. Source-cell URLs are not equivalent merely because prose names the same subject. Receipt: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-85/w1/ConnectorSibling/collision-receipt.json`.

## One bounded proposed move: scope-and-authority distinction in C1 registry notes

Proposal 5 at `/home/vgpnk/Projects/shokunin/kake-shokunin/considerthese/2026-10-26.md:33` suggests distinguishing deliberately historical red gates from regressions (its example is c56_quote_truth.py 6/8). It is historical proposal data, **not source truth or authority to repin gates**.

Propose that L1's already-required C1 registry entries use their existing scope/limit text to distinguish **frozen structural witness** from **semantic approval authority**, and cross-reference the existing r84 experimental correction and the new field-specific decoder. Keep commands, verdict mappings, fixtures, historical results and the frozen count.py oracle unchanged. No separate framework or new runtime is needed.

Crucial contradiction: a historical red caused by a fixed population and an experimentally false-green semantic classifier are **different failure modes**. Proposal 5 cannot justify calling the r84 semantic counterexample an expected-red exemption, nor can a 3/3 registry score grant semantic approval. Preserve r84's unprovable status and all open D84-2..4 defects. The C2 decoder answers only “last recognized token”; it does not assess policy suitability, arbitrary field equivalence or permission to publish.

Second-order surfaces:

- Runtime: no changes to r84 tool behavior or callers; preserve Referrer-Policy field/token ordering when supplying input to the separate decoder. Sorting would destroy the witness.
- Contract: C1 stays discoverability-only and C2 stays the ten frozen cases plus separate retained-control trial; no numerator expansion, oracle editing or full-queue closure.
- Substrate: share recorded header evidence, not generic grammar or multiset equivalence. The 20-lane Markdown sweep finds adjacent capture/HTTP concepts but no conflicting effective-token owner.
- Verification: separate labels for frozen historical scope and semantic non-approval prevent a green selftest from laundering the false-green example. Retain opposite-order evidence rather than reclassifying it away.

Affected axes: **calibration** improves interpretability of the required discoverable rows; **freshness** retains the decoder's narrowly justified field-specific capability. No-harm is a proposal-level inference, not a measured verdict: scope notes must not weaken fail conditions or authorize exceptions.

Risks: vague “historical” wording could hide a real regression; overbroad “effective” wording could imply browser conformance or deployment approval; byte-level URL comparison can miss aliases; current registries can change after this snapshot. Mitigation is explicit non-approval wording, unchanged oracle/fixtures and a collision re-read by L1 at integration time, not bulk staged assimilation.

## Verification handoff and execution limits

Only assigned read-only overlap/collision work was exercised. Tool calls: `read`, `glob`, `grep`, and local Python Eval for registry parsing/receipt serialization. All completed without reported execution error; Eval ran in-process and did not supply a subprocess exit status (none invented). No shell commands, tests, counter runs, decoder runs, build/lint, git/jj mutation, network requests or installs were performed. No scratch directory was created or used, so no scratch residue exists to remove.

L1, not this seat, should execute the frozen C1/C2 counter commands and retained opposite-order trial after integration, check source-seat S458 reopening evidence, and confirm eight-cell registry rows retain explicit experimental limits. Green count.py CASES alone do not exercise malformed input or usage exit behavior, which remain separate contract obligations.

Report: .ufo/waves/round-85/w1/ConnectorSibling.md
