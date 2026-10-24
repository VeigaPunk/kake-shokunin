# CtlPrintableOnly — KILLED (1212/1434; met=false)
Axes: operability (assigned measurement); freshness (not independently measured). No round judgment.

## Mutant and artifacts
Sandbox: `/fast/scratch/hyaku/kake-r41w1/CtlPrintableOnly/` (all receipt names below relative to this directory).
Retained tool: `/fast/scratch/hyaku/kake-r41w1/CtlPrintableOnly/printable_only.py`.
SHA-256: `127ff731ff2f2b41c0bcccbeacf98e3c91e79d5d1bb02f486b2394944a1ebe02`.
Mutation: `printable_only.py:113` adds `value = re.sub(r"[\x00-\x1f\x7f]", "", value)` before the unchanged reference grammar and URL parser.
It deliberately lets every C0 control and DEL pass by deleting them; it retains the reference's space, forbidden-printable, delimiter-position and percent-triplet checks. No seed/template/output shortcut was added.
`probe.py` received the identical one-line mutation and was then restored exactly; the retained mutant is a separate artifact.
Pristine/restored probe SHA-256: `e9dc25b6e398b222387e608685e54218dff9a9accd75599934dc8290f11999a7`.
Read-only reference SHA-256: `6d7c2dd445fc7d3b2df7c3307d18f05c7f2cf6154830430dbc15dd372509010a`.
The pristine scratch copy differs from the reference only by its omitted terminal LF: `cmp -l` reported EOF at byte 15658, and adding LF to the copied bytes hashes to the reference SHA above.
Counter SHA-256: `2acc443af33466796ad178d8c1ad8350d36250b29e7383bba4ba10d2e4fe67b4`.

## Exact behavioral commands and exits
```sh
timeout 900 prlimit --as=4000000000 -- env TMPDIR=/fast/scratch/hyaku/kake-r41w1/CtlPrintableOnly/tmp python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-41/c1_count.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --tool-file /fast/scratch/hyaku/kake-r41w1/CtlPrintableOnly/probe.py --label CtlPrintableOnly-pristine --seed 41001 --out /fast/scratch/hyaku/kake-r41w1/CtlPrintableOnly/pristine.json
# exit 0
timeout 900 prlimit --as=4000000000 -- env TMPDIR=/fast/scratch/hyaku/kake-r41w1/CtlPrintableOnly/tmp python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-41/c1_count.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --tool-file /fast/scratch/hyaku/kake-r41w1/CtlPrintableOnly/probe.py --label CtlPrintableOnly-mutated --seed 41001 --out /fast/scratch/hyaku/kake-r41w1/CtlPrintableOnly/mutated.json
# exit 1
timeout 900 prlimit --as=4000000000 -- env TMPDIR=/fast/scratch/hyaku/kake-r41w1/CtlPrintableOnly/tmp python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-41/c1_count.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --tool-file /fast/scratch/hyaku/kake-r41w1/CtlPrintableOnly/probe.py --label CtlPrintableOnly-restored --seed 41001 --out /fast/scratch/hyaku/kake-r41w1/CtlPrintableOnly/restored.json
# exit 0
timeout 900 prlimit --as=4000000000 -- env TMPDIR=/fast/scratch/hyaku/kake-r41w1/CtlPrintableOnly/tmp python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-41/c1_count.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --tool-file /fast/scratch/hyaku/kake-r41w1/CtlPrintableOnly/printable_only.py --label CtlPrintableOnly-printable-only --seed 41001 --out /fast/scratch/hyaku/kake-r41w1/CtlPrintableOnly/printable-only.json
# exit 1
```
Expected detector: pristine met; mutant not met because raw C0/DEL remain RFC-invalid; restored met on the identical seed.
Actual stdout summaries: pristine/restored passed=1434, met=true; mutated/retained passed=1212, met=false; note=null throughout. Each underlying audit tool exited 2, which is distinct from the counter exits above.

## Receipts (all four actual runs)
| Receipt | passed | byField (loc; sitemapUrl) | byComponent | met |
|---|---:|---|---|---|
| pristine.json | 1434/1434 | 630/630; 804/804 | fragment,host,path,port,query,userinfo each 239/239 | true |
| mutated.json | 1212/1434 | 606/630; 606/804 | fragment,host,path,port,query,userinfo each 202/239 | false |
| restored.json | 1434/1434 | 630/630; 804/804 | fragment,host,path,port,query,userinfo each 239/239 | true |
| printable-only.json | 1212/1434 | 606/630; 606/804 | fragment,host,path,port,query,userinfo each 202/239 | false |

## Findings and statement dispositions
- **holds:** `printable_only.py:113` / mutated `probe.py:113` skip C0+DEL; the counter catches 222 cases (24 loc, 198 sitemapUrl), 37 per component. The skipped units are loc TAB/LF/CR/DEL and sitemapUrl U+0000–U+001F/DEL, inserted in each of the six components (`c1_count.py:45-47,177-179`).
- **holds:** all 200 recorded misses are C0/DEL and oracle-invalid; the receipt cap is 200, not 222 (`c1_count.py:361-363`). Concrete catches: manifest host U+0002 at `printable-only.json:30-34`, loc host DEL at `:37-41`.
- **holds:** this strongest-reference-minus-controls partial repair scores below 1434 on seed 41001; it was killed, not inconclusive. No passing control was found in this assigned class.
- **holds:** pristine/restored `probe.py` skip no URL-validation work and have no mismatches; receipts pin identical before/after SHA-256, and a post-restoration `sha256sum` returned that same hash (exit 0). Mutant bytes hash identically in the mutation receipt and retained artifact.
- Scope: one mutant, one seed, four runs; no other control class or seed is claimed checked. No fleet/shared source was edited; only this report and the seat sandbox were written. No installs, network requests, services, or background jobs; every bounded detector invocation returned.
