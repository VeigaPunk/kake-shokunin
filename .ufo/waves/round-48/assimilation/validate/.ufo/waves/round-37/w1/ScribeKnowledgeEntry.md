# ScribeKnowledgeEntry — scoped report

- Axes: operability and freshness (publisher web properties).
- Behavior: drafted an offline robots.txt rule reference in the sandbox, with RFC 9309 rules separated from explicit Round-37 lane readings, Google-specific notes, and limits. No product code or lane knowledge file was changed.
- Artifact: `/fast/scratch/hyaku/kake-r37w1/ScribeKnowledgeEntry/robots-txt-rules.md` — 83 lines (under 120); SHA-256 `07c20e6b4ef8c0511ee708583a37735ca3814b2839451adc361dbe4ff9cebb36`.
- The substantive rules cite S011/S095/S096 with section headings; lane readings are explicitly labeled and point to the public C1 contract. Shape follows `corpus/knowledge/crawl-scope-per-host.md:1-3` and `link-preview-metadata.md:1-9`; content is grounded in `SCORECARD.md:1795-1857` and retained sources.
- Provenance: `.ufo/waves/round-37/sources/receipts.json:2-36` records S011 text SHA-256 `8e632e483ba4c6c9808a1436d3912079b1856e77d52ba2ca7245dc8d39259cf3`, S095 `a90948534ca17e54196115163fb9a5f6afbb0b347f97a44b01a3a1d636ddbbc6`, and S096 `d17aa81d51ba5fa3e030f24697a95bc50b864545bd90ba9db5228008a8615574`.
- Finding: the opened `corpus/SOURCES.md` snapshot ends with S094 at line 102 and did not yet show S095/S096 rows; those ids are used per assignment and the round-37 receipts exist. Confirm the source rows before copying the draft into the corpus.

## Commands and outcomes

- `timeout 30s mkdir -p /fast/scratch/hyaku/kake-r37w1/ScribeKnowledgeEntry` — exit 0; no output.
- `timeout 30s wc -l /fast/scratch/hyaku/kake-r37w1/ScribeKnowledgeEntry/robots-txt-rules.md && timeout 30s sha256sum /fast/scratch/hyaku/kake-r37w1/ScribeKnowledgeEntry/robots-txt-rules.md` — exit 0; output `83 .../robots-txt-rules.md` and the hash above.
- File reads used the read tool; the draft was written in the sandbox and this scoped report is the only lane write.

## Gates and limits

- No C1 counter or sealed cases accessed; no C1 implementation, build, test, lint, or live fetch was run. Draft is domain guidance, not execution evidence or a round verdict.
- Not verified: that S095/S096 registry rows have since landed, and no functional checker was exercised. No tools installed or updated.
- Out of scope: C1 implementation/integration, crawler-specific behavior beyond S095, fetching/redirects/cache, and all live operator properties.

## Touched surfaces

- Sandbox artifact: `/fast/scratch/hyaku/kake-r37w1/ScribeKnowledgeEntry/robots-txt-rules.md`.
- Report: `.ufo/waves/round-37/w1/ScribeKnowledgeEntry.md`.
