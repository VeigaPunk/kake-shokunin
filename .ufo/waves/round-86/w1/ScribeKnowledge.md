# ScribeKnowledge — round 86 w1 scoped findings

Report-root: /home/vgpnk/Projects/shokunin/kake-shokunin
Report: .ufo/waves/round-86/w1/ScribeKnowledge.md
Seat: author-side source-grounded draft; not independent closure.

## Axes and behavior

Axes: source fidelity; bounded field-specific semantics; auditable provenance; production/scratch confinement. Drafted the requested effective-freshness knowledge entry and README frontier-move block. Kept the first-occurrence-vs-minimum witness while correcting false historical attribution. No production file, registry row, counter, VCS state, or sibling artifact was modified.

## Deliverables and touched surfaces

All paths below are relative to Report-root:

- `.ufo/waves/round-86/w1/ScribeKnowledge/corpus/knowledge/cache-control-effective.md` — substantive integration draft; provenance trio first; shared s-maxage > max-age > Expires−Date; duplicates/conflict; no-store; case/quoted arguments; overflow convention; RP contrast; planned interface; explicit limitations.
- `.ufo/waves/round-86/w1/ScribeKnowledge/readme-frontier-move.md` — README coverage/frontier draft, conditional on integration; retains D84-2/3 and denies whole-queue closure.
- `.ufo/waves/round-86/w1/ScribeKnowledge/s457-rfc9111.html` and `s457-rfc9111.headers` — independent GET body/headers.
- `.ufo/waves/round-86/w1/ScribeKnowledge/rfc7234-contrast.txt` and `rfc7234-contrast.headers` — independent historical contrast body/headers.
- This report.

The final draft proposes S461 per L1's source-scope correction, explicitly pending the guarded append. It does not claim that row exists or that append gates passed. S457 supports only its existing max-age/freshness scope; S456 does not supply directive argument syntax.

## Source receipts and commands

Prerequisites read: `/home/vgpnk/.omp/agent/RULES.md`, godspeed skill, frozen round-86 contract, round-86 count.py declarations and frozen CASES (lines 154–250), existing RP knowledge entry, README coverage/frontier sections, source registry rows S456–S458. No counter was executed.

Executed GET command (exit 0):

```sh
mkdir -p /fast/scratch/hyaku/kake-r86/ScribeKnowledge && curl -sS -D /fast/scratch/hyaku/kake-r86/ScribeKnowledge/rfc9111.headers -o /fast/scratch/hyaku/kake-r86/ScribeKnowledge/rfc9111.html -w 'code=%{http_code} url=%{url_effective}\n' https://httpwg.org/specs/rfc9111.html && date -u '+%Y-%m-%dT%H:%M:%SZ' && wc -c /fast/scratch/hyaku/kake-r86/ScribeKnowledge/rfc9111.html && sha256sum /fast/scratch/hyaku/kake-r86/ScribeKnowledge/rfc9111.html
```

Outcome: HTTP 200; 2026-11-04T15:36:38Z; 178573 bytes; SHA-256 `999f401328ed8991d172aeb1cd4ab048630928437af2401d3e39552c4a073f64`.

Executed contrast GET (exit 0):

```sh
curl -sS -D /fast/scratch/hyaku/kake-r86/ScribeKnowledge/rfc7234.headers -o /fast/scratch/hyaku/kake-r86/ScribeKnowledge/rfc7234.txt -w 'code=%{http_code} url=%{url_effective}\n' https://www.rfc-editor.org/rfc/rfc7234.txt && date -u '+%Y-%m-%dT%H:%M:%SZ' && wc -c /fast/scratch/hyaku/kake-r86/ScribeKnowledge/rfc7234.txt && sha256sum /fast/scratch/hyaku/kake-r86/ScribeKnowledge/rfc7234.txt
```

Outcome: HTTP 200; 2026-11-04T15:37:12Z; 90647 bytes; SHA-256 `1d084238ae6692d1e3322fa0850dbb9596812332d92b76d9a815c5ed9b600dea`.

Read ScoutCache metadata/headers and ran `sha256sum /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-86/w1/ScoutCache/s457.body.html` (exit 0). Its re-open metadata records HTTP 200 at 15:37:19Z, same body size and SHA-256. The own quote does not depend on another seat's extraction.

Extraction used Python Eval with HTML unescaping/tag removal over the retained source: §1.2.2 line 267; §4.2 line 269; §4.2.1 line 270; §5.2 line 279; §5.2.2 directive bodies line 282; §5.3 line 283; Appendix B line 304. Own quote, 14 words: “either the first occurrence should be used or the response should be considered stale.” Location: §4.2.1 paragraph 4, line 270.

Receipt retention command used `mkdir -p` for the owned draft path and four `cp` operations from own scratch to the four retained files listed above; exit 0. Scratch cleanup command `rm -r /fast/scratch/hyaku/kake-r86/ScribeKnowledge` exited 0 after retention. No installs or updates.

## Findings and exact conflicts

1. Frozen wording: “first occurrence wins on duplicate values (§4.2.1 SHOULD — NOT RFC 7234's most-restrictive rule)”. Source correction: RFC7234 §4.2.1 lines 691–695 declares duplicate values invalid, encouraging stale treatment; it does not prescribe minimum selection. RFC9111 clarifies first-occurrence-or-stale and separately advises most-restrictive handling for conflicting directives. Draft records that distinction rather than changing the frozen case population.
2. Assignment wording: “RP order matters, Cache-Control order does not for these directives”. Correct bounded reading: no-store/max-age positions commute for the no-store result; duplicate max-age values do not commute under first-occurrence selection. No arbitrary-header equivalence follows.
3. L1's source-scope correction: S457 excludes directive-list ordering and S456 excludes directive argument syntax. Draft switched to proposed S461, explicitly pending guarded append/mirror census; old source scopes remain intact.
4. Exact 2147483648 cap is a local profile: RFC9111 permits that overflow value or the greatest conveniently representable positive integer. Null and clamp conventions likewise are not RFC quotations.
5. §5.2.2.5 no-store and §5.2.2.10 s-maxage numbering agree with the contract; §5.2 case/argument paragraph independently located. `storable=true` is not full cacheability proof.

## Defects in this seat's execution

- First fetch invocation failed before running because its requested cwd did not exist. Retried with an existing cwd; GET then succeeded. No HTTP failure inferred from that setup error.
- Supplying a name to the first successful bash fetch made the harness classify it as a service; it exited 0 in 373ms. No intentional persistent/background work was commissioned. Receipt copy was also auto-backgrounded briefly by an incoming interrupt and subsequently completed successfully.
- First extraction Eval timed out after 60 seconds because the submitted extraction code contained a non-advancing loop. Kernel reset; replacement extraction succeeded. No product code was involved.
- Initial quote-count edit targeted the wrong line and replaced a paragraph. Re-read affected lines, restored the paragraph and corrected the quote count to 14. Final edit tool output records the restored paragraph.
- An inspection used shell listings/cat instead of preferred read/glob tools. No writes resulted.

## Gates, out-of-scope and limits

No builds, tests, selftests, reader runs, counter runs, mutation trials, VCS mutations, live property requests, POSTs, publishing, deploys, accounts or credentials. A read-only listing at 15:40:54Z found the production reader absent then; that is not a failure verdict on another seat's candidate.

C1 open=4→0, C2 cases=15/15, independent closure, guard proof, mirror census and assimilation adoption/reject are not established by this seat. L1 owns integration after WAVE-DONE and all corresponding measurements/gates. The draft names no browser cache model, Vary/Age/Pragma implementation, must-understand store-permission, or live property measurement. D84-2 and D84-3 stay retained-open. No full D84-queue closure claim.

Recommended integrator action: use the draft after the new source row's guarded admission, preserve source-scope correction in the lesson, and apply the frozen fifteen-case measurement through L1; this report supplies source evidence, not a green gate.
