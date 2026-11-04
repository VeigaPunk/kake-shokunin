# kake round-79 — contract amendment 1 (terms-only, before any after-state)

Frozen contract `.ufo/waves/round-79/contract.md` at `e1a9a897`. No tool existed and no case
had been scored when this amendment was written; the frozen case set, oracle, counters and
predicates are unchanged.

**A1 — directive vocabulary.** The known-name list gains `noarchive` as a value-less
directive. Grounding: the S449 row's `teaches` records that Google's historical section names
`noarchive` (retained S449 text lines 1223-1236); the audit judges declarations and claims no
current crawler effect. The frozen list is therefore `all, index, noindex, follow, nofollow,
none, nosnippet, indexifembedded, max-snippet, max-image-preview, max-video-preview,
notranslate, noimageindex, unavailable_after, noarchive`.

**A2 — normalization wording.** `none` is replaced by `noindex` and `nofollow` and is not
itself kept; `all` contributes nothing and is not kept; `index` and `follow` are kept as
positive tokens and are removed only from `effective`. This is the reading cases c03 (none ->
noindex+nofollow), c04 (all -> empty) and c09/c10 (index/follow kept) already encode.

**A3 — why.** A scratch L1 reference implementation run against the frozen oracle exposed
exactly these three readings (c03 `none` kept, c04 `all` kept, c26 `noarchive` unknown) before
any tool existed; A1/A2 settle them in favour of the frozen expectations. No data was scored
before this amendment, and no case, oracle byte or predicate changes.

Commit: the amendment lands with `controls/ctl-c2-oracle-cheat.txt` and this file, before the
tool exists.
