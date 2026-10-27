# ConnCrossPattern — round-62 counter defect scan

## Result

**Confirmed repeat: `.ufo/waves/round-47/c47_routed_count.py`.** Its `r3_fixed`, `r4_fixed`, `r5_fixed`, `r6_withdrawn`, and `r6_rerun_receipted` predicates are formed from literal substrings in committed `LOG.md`, ledger, and receipt text, and feed `fixed` → `outstanding` → `met` without replaying the claimed underlying actions. In particular, lines 145–149 accept the receipt through the marker sentence `R47 rerun only; not contemporaneous r46 verdict-time evidence`, an `exit=0`/`OFFLINE_EXIT=0` substring, and `--offline`; lines 153–155 then make `met` depend on those booleans. Exact evidence: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-47/c47_routed_count.py:133-155`.

**Related, but narrower receipt-marker variant: `.ufo/waves/round-47/c47_registry_count.py`.** Lines 118–125 accept a receipt when it contains the script-name needle, a tally regex, the literal `exit=0`, and a SHA-shaped string; they do not execute or bind that receipt to a replay. `met` is row/receipt counts at lines 128–130. Evidence: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-47/c47_registry_count.py:112-130`. This is the same marker-as-evidence weakness on the selftest-receipt leg, although it also structurally checks registry rows and the receipt's hash shape; I classify it as a related partial repeat, not as broad as c47_routed_count.

**Other observed marker weakness, different scope:** `.ufo/waves/round-32/c2_retained_count.py` has already documented substring/window defects that can produce false green. The committed review `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-32/w1/ReviewC2CounterCode.md:7-14,34-36` records fabricated-row and bare-mention attacks (`S900` substituted for `S062`, or a bare `S062` mention). This is an established related example, but it is a different marker/scope defect from c62's `resolved` components.

## Scope checked / exclusions

I scanned the committed wave Python counters and `scripts/*.py` for literal substring predicates and inspected verdict-forming logic in likely candidates. `scripts/` yielded ordinary parser/selftest field-presence checks, not a repeated counter claiming semantic resolution from markers; `scripts/quote_class.py` was not a match. Counters such as `c50_quote_class.py` derive the quote class from retained source blobs before checking ledger/lesson consistency; `c54_s374_calib.py` parses correction structure and recomputes mismatch state; `c52_gate_registry.py` pins receipt hashes and checks frozen inputs. I did not classify these as repeats based on substring checks alone.

No files other than this seat report were written. No counters or receipts were changed; no tests or commands that mutate the fleet repository were run.
