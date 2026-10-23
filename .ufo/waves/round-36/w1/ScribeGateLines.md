# Round 36 wave 1 — Gate source-opening draft

Axis: freshness.

## Behavior
- Drafted one source-opening line each for S088–S094 at `/fast/scratch/hyaku/kake-r36w1/ScribeGateLines/gate.md` (7 lines; SHA-256 `17547ce544698e38a262b8e0747b975162605b5d7403321fdf4d9ddd278634f4`).
- Each line carries the receipt URL, UTC access time and HTTP status, admit/reject, tier, kind, status, a reason, a located quote (≤25 words), and the exact whitespace-normalizing verifier command.
- Decisions: S088–S092 admit / A / spec / mined; S093 reject / C / community / rejected; S094 admit / B / docs / mined. S093 is the located reject.

## Gates and commands
- `timeout 10s mkdir -p /fast/scratch/hyaku/kake-r36w1/ScribeGateLines/tmp` — exit 0, no output.
- The exact quote-check commands are pasted on `gate.md:1-7`; each was run verbatim from the sandbox. All exited 0 and printed, respectively: `PASS S088`, `PASS S089`, `PASS S090`, `PASS S091`, `PASS S092`, `PASS S093`, `PASS S094`.
- `timeout 10s wc -l gate.md` — exit 0; output `7 gate.md`.
- `timeout 10s sha256sum gate.md` — exit 0; output `17547ce544698e38a262b8e0747b975162605b5d7403321fdf4d9ddd278634f4  gate.md`.

## Provenance and findings
- URLs, access times, HTTP statuses, and text hashes were taken from `kake-shokunin/.ufo/waves/round-36/sources/receipts.json:2-84`; retained snapshots are `.../sources/S088.txt` through `S094.txt`. Receipt text SHA-256s: S088 `81c7197438672559e2e6ba2d7cc23ccaccbfc4f5f68ec3be0972238120d0b07a`; S089 `656b0d769d8f5446cee8ad984e39f1db2089697fd373898dae95d7d0e9054ba7`; S090 `a137086931ac8720d6c3adacd2242a18231c3e1bb96b83eaae8820b938f9399b`; S091 `517c1892ef8f657b4d240d5779404e660753b1c713dcee0138d05f9ec8d23e96`; S092 `2fb98770463f89d127d4f02bc92c9306164a530498bc78db61e8875f4496adb3`; S093 `5ddaebd8fed49b544e990e1b0b46154c76e8f70bb1fe1214bddfb8478d8a7cbd`; S094 `458c6cc943e3e507b09275982afaadde180f765f2f928aee7a357632b8911208`.
- The line shape follows `corpus/lessons/round-35.md:44-53`; tier/kind/status terms follow `/home/vgpnk/Projects/shokunin/CORPUS.md:86-115`; the cited C1 rules are in `SCORECARD.md:1597-1644`.
- Quote checks confirm each quoted substring in the retained `.txt` snapshot after collapsing whitespace. No live source request was made.

## Touched surfaces and limits
- Wrote the sandbox draft above and this requested report only. No product code, `corpus/SOURCES.md`, lesson, Git state, or other tracked lane file was changed; no tools were installed.
- Did not access `/fast/scratch/hyaku/kake-r36/`, search for or run sealed cases, run the counter, fetch sources, or evaluate the implementation/admission verdict.
- Source decisions/statuses are this author-side draft only; no registry row has been written and no independent re-open or non-author verification is claimed. The C1 tool behavior, sealed predicate, and live freshness remain unverified here.

## Artifact paths
- Draft: `/fast/scratch/hyaku/kake-r36w1/ScribeGateLines/gate.md` — SHA-256 `17547ce544698e38a262b8e0747b975162605b5d7403321fdf4d9ddd278634f4`.
- Report: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-36/w1/ScribeGateLines.md`.
