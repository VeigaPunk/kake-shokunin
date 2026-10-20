# SourceHierarchy — round 22 w1 (connector, read-only)

Lane: `/home/vgpnk/Projects/shokunin/kake-shokunin`. Base named by the frozen contract: `7c61c8cc791bde36dd5e3688bdfea2678d90146c`.
Seat: `SourceHierarchy`. Axis judged: operability. Milestone: `offline-canonical-capability`.
Nothing in the corpus, registry, scripts, or live lane git state was edited. No package was installed. The matrix was not run. The eight official canonical documents were not opened here; scouts own those fetches. Provisional ids S020–S027 are the Knowledge seat's mapping in `.ufo/waves/round-22/w1-spec.json`, not rows in `corpus/SOURCES.md` (last mined/queued/rejected id on disk is S019).

## Axes

| Axis | Role in this proposal |
|---|---|
| operability | The only scored axis this move serves. C1 is a local runnable classifier (`scripts/canonical_audit.py`) over the frozen 32-case matrix, exits 0/1/2/64. |
| freshness | Owned by the lane and left untouched. No live property, pin, or paths-gate relabel. |
| source hierarchy | Not a kake score. Chousa owns the method. Kake already keeps a scoped A/B/C registry. This move uses that registry; it does not add a third scored axis. |

## Evidence

- Province frontier still lists canonical signals as open, and the adjacent clause gives the method away: `PROVINCE.md:22-23` (canonical/JS rendering open) and `PROVINCE.md:32-33` (`chousa` owns research method and source hierarchy; kake keeps domain findings and its own `corpus/SOURCES.md` rows). `corpus/README.md:101-103` names the same open ground.
- The registry's own fence is one sentence: tiers are scoped to the row's topic, admission stays in `corpus/QUALITY.md`, and the research method remains chousa's (`corpus/SOURCES.md:3`, pointing at `chousa-shokunin/SKILL.md`).
- Chousa's ladder is a different vocabulary and is labelled as that lane's construction: primary > secondary > aggregator > unsourced (`chousa-shokunin/PROVINCE.md:5-8`, `chousa-shokunin/SKILL.md:17-18` and `:25-33`). Kake's census accepts only tier `A|B|C` (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` around the `tier !~ /^[ABC]$/` check). Putting chousa's four names in the tier column would already fail that census.
- Pattern already used for a mechanism that must not be over-read: S009's scope is "nginx's own ETag format only; not an assertion about the GitHub Pages backend" (`corpus/SOURCES.md:17`). The knowledge entry keeps the format decode and marks backend identity as inference (`corpus/knowledge/ghp-etag-anatomy.md:30-34`). `corpus/QUALITY.md` "Validator is not identity" is the admission bar for that fence.
- Pattern already used for vendor guidance last: the crawl study path is S010 → S009 → S011 → S012 → S013, standards and a scoped mechanism before Google (`corpus/SOURCES.md:33`). `corpus/knowledge/crawl-scope-per-host.md:14-17` states the sitemap standard, then Google's Search Console exception as a second boundary, and leaves the live robots file as named debt (`:44-46`). It does not probe.
- Google canonical troubleshooting is already an unopened lead, not a mined teaching (`corpus/SOURCES.md:62`). Round-22 census-before records `sources-census.sh validate` exit 0 against the current registry. That census walks Registry table rows (field count, id, kind, A/B/C tier, status, used-by path exists, URL+scope uniqueness). It does not read the Paths bullets. A later exit 0 cannot prove study-path order or a scope non-claim.
- Round 21 already forbids treating a green structural census as source restoration, publishing readiness, or admission (`corpus/QUALITY.md:56-58`). Contract debts stay red: paths gate missSet 55; no SHONEN promotion (`contract.json` `debts`). SCORECARD's planned next move is this frontier, and it records no self-admission (`SCORECARD.md:273-276`).
- C1 limits, quoted from the frozen contract: explicit-head serialized static HTML only; policy comparison, not search-engine selection, JS rendering, HTTP headers, redirects, network freshness, or publishing readiness. Policy: exactly one canonical link in the explicit head; resolve `href` with the first head `base` href or the document URL; compare a WHATWG-like HTTP(S) normalized absolute URL to `expectedCanonical`; preserve query; reject fragments and credentials. Matrix names include `relative_same_dir` and `body_link`. Finding ids include `canonical_outside_head`, `canonical_url_invalid`, `canonical_mismatch`.

Contradiction, kept visible: the Knowledge prompt's source-list order is RFC6596, GoogleCanonical, GoogleTroubleshoot, HTMLLink, HTMLBase, HTMLTemplate, PythonParser, PythonURL. That list puts both Google documents before the HTML link type. The crawl path does the opposite with Google. Id assignment order and trust order are different sequences. Copying the prompt list into a Paths bullet would invert the pattern this lane already uses.

## Pattern to reuse

Reuse the crawl study path plus the S009 scope fence. Not a new hierarchy, and not chousa's ladder.

Trust order for the canonical preflight, using the provisional ids only as labels:

1. S023 HTML link type `canonical` — which element counts.
2. S020 RFC 6596 — relation target, including a relative IRI.
3. S024 first head `base` href — how that relative reference resolves.
4. S025 `template` inertness — what is outside the document tree the contract ignores.
5. S026 HTMLParser and S027 `urllib.parse` — bounds of this interpreter, stated as limits, not as the spec.
6. S021 Google consolidate-duplicate-urls — publisher declaration guidance, same role as S013.
7. S022 Google troubleshooting — declared versus selected. Scope fence, same shape as S009: the distinction only; not the verdict of `scripts/canonical_audit.py`.

Keep S022 mined (once opened and quoted) with that fence. Do not mark it `rejected`. S017 is rejected because a tier-A GitHub document contradicts it (`corpus/SOURCES.md:25`). S022 is not a contradiction; it is the warrant for the non-claim. Rejecting it would drop that warrant. Leaving it unfenced would let "selected canonical" leak into exit 0.

Registry ids may stay in the scout list order S020–S027. The Paths bullet must not follow that id order.

## Boundary not to absorb

- Chousa's primary/secondary/aggregator/unsourced ladder, citation-chain gate, and `research-gate`. Report method questions back; do not add those tier names or that gate to kake. `PROVINCE.md:32-33` already states this. The A/B/C column stays the only tier column.
- Google's selected canonical, live fetch, JS-rendered canonicals, HTTP `Link` headers, and redirects. Those are outside C1's limits. Crawl-scope's unprobed host robots file stays operator debt; this preflight does not close it.
- A green `sources-census.sh` or a green S019-style structural census as proof the classifier matches the policy. `corpus/QUALITY.md:56-58`.
- The red paths gate and historical lesson bytes. Contract debts. This proposal does not relabel them.

## Proposed move

One change for L1 when the canonical rows are integrated: add a Paths bullet in the trust order above, and write S022's `scope` cell as an explicit non-claim modeled on S009 ("Google's declared-versus-selected distinction only; not an assertion about `scripts/canonical_audit.py`"). Write S026 and S027's `scope` cells as interpreter limits, not WHATWG conformance and not a crawl result. Leave the tier column as A/B/C. Do not import chousa's ladder. Do not treat the Knowledge prompt's list order as the study path.

This improves operability by keeping the runnable classifier tied to the contract's resolve-then-compare rule. It does not spend freshness, does not retier old rows, and does not claim C1 admitted.

## Future falsifier

Not executed. Name: `relative_same_dir` stays a clean positive control after Google rows exist.

Contract ground: a same-directory relative `href` is resolved against the document URL, or against the first head `base` href if present, and the normalized absolute HTTP(S) URL is compared to `expectedCanonical`. The frozen case name is `relative_same_dir`. Expected observation under the contract policy: exit 0, stdout verdict `clean`, no finding id. That expectation is the contract's positive-control rule applied to this case. It is not a measured run.

The hierarchy was absorbed if any one of these is observed later:

1. `relative_same_dir` exits 1 with `canonical_url_invalid` or `canonical_mismatch` while the resolved absolute equals `expectedCanonical`. The comparator treated a non-absolute `href` as failure before resolution. That is the vendor-guidance inversion, whether or not a Google page actually says "use absolute URLs". The absolute-URL recommendation itself is [INFERENCE] until the GoogleCanonical scout returns a located quote. The contract's resolve-then-compare rule does not depend on that quote.
2. A C1 lesson, knowledge entry, or measure summary calls that exit 0 a Google-selected or indexing canonical. Selection was narrated as the operability result. Contract limit: policy comparison, not search-engine selection.
3. The new Paths bullet names S021 or S022 before both S023 and S020.

Paired rejection, so the fence is not a weakened policy: `body_link` stays a policy failure. The contract's id for a canonical link outside the explicit head is `canonical_outside_head`, exit 1. If `relative_same_dir` is green only because resolution was skipped, a green `body_link` or a green `wrong_host` is a policy hole, not a hierarchy pass.

`sources-census.sh validate` exit 0 is not this falsifier. The script does not parse Paths order or scope prose.

## Risks

- If L1 assigns different ids than S020–S027, follow the row topics, not these numbers.
- Swapping S023 and S020, or S026 and S027, does not trip the falsifier. Putting either Google id first does.
- Parser decoys (`comment_decoy`, `script_decoy`, `template_decoy`) are a neighboring hole owned by the parser review. This falsifier does not cover them.
- Scope-fence prose can be vague. The behavioral check (1) is the one that counts; the Paths-order check (3) is the cheap static twin.
- No claim that unseen `canonical_audit.py` passes. Baseline contract state is zero accepted cases until measure runs.

## Verification for L1

Do not count this report as a pass. After integration, and not before the script and fixtures exist:

- Read the new Paths bullet and confirm neither Google id precedes both the HTML link-type id and the RFC 6596 id.
- Read the Google troubleshooting row's `scope` and confirm it states the selected-canonical non-claim.
- Run the contract counter: `python3 .ufo/waves/round-22/measure.py --root . --revision <master-tip>`.
- Confirm `relative_same_dir` is accepted with exit 0 and `body_link` is rejected with `canonical_outside_head`. A clean source census beside a failed `relative_same_dir` is the hierarchy failure.

## Installs

None.
