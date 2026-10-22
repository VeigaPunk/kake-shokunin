# RerunC1Sealed — C1 measured values attack (round 35, wave 2)

Attack: re-ran the sealed C1 counter on the five measured revisions to try to falsify the
landed values (14/24 pre-repair, 24/24 post-repair, 4c6be2bd exit 2). **No falsification:
all five runs reproduce the receipts exactly** (only cosmetic `keySource` label differs).

## Method
Fresh clone at measured revision 7deacc4629c1d05a34fb919d8095e99efc7b712f:
```
git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin /fast/scratch/hyaku/kake-r35/w2/RerunC1Sealed/clone
git -C <clone> checkout -q 7deacc4629c1d05a34fb919d8095e99efc7b712f
```
For each revision (GIT_* env unset; TMPDIR=/fast/scratch/hyaku/kake-r35/w2/RerunC1Sealed/tmp):
```
python3 -B <clone>/.ufo/waves/round-35/sealed_count.py c1 --root <clone> \
  --revision <rev> --key-revision 4c6be2bdec5630166c4013e53c226b1119ec63cc
```

## Results
| rev | exit | passed | met | matches receipt |
|---|---|---|---|---|
| 16a6b8b8 | 1 | 14/24 | false | yes (semantically —) |
| bd14096a | 1 | 14/24 | false | yes (semantically) |
| b1cbbc39 | 0 | 24/24 | true | yes (semantically) |
| 95abec21 | 0 | 24/24 | true | yes (semantically) |
| 4c6be2bd | 2 | — | — | yes (semantically) |

Field-by-field JSON comparison (dict keys order-normalized; perCase compared both in-order and
by id) shows the ONLY difference on all five runs is:
- `keySource`: mine "revision 4c6be2bdec5630166c4013e53c226b1119ec63cc" (full hash passed on
  CLI) vs receipt "revision 4c6be2bd" (short form wave-1 used). Pure verbatim echo of the
  `--key-revision` argument (sealed_count.py:299); not a behavior difference.
Identical fields in every run: `counterSha256` 1b4d9d590b70f82c72e257006b77dc7232c43d7ccf1e5df51e892da2efb3469b,
`revision` (full hash), `toolPresent`, `toolSha256`, `cases` 24, `passed`, `target` 22,
`met`, and the full `perCase` list.

## Independent cross-checks
- Counter script sha256 at 7deacc46 = 1b4d9d590b70f82c72e257006b77dc7232c43d7ccf1e5df51e892da2efb3469b = receipt `counterSha256` (verified via `git show 7deacc46:.ufo/waves/round-35/sealed_count.py | sha256sum`).
- Key c1-cases.json sha256 at reveal 4c6be2bd = a861dccdf63c21b2f731b5845ec016e216bee8bd7ad62df646d5e47e8bc1a391 = `C1_KEY_SHA256` pin (sealed_count.py:57).
- Tool sha256: cccc3a17256aa4387a57e55b039257f8b3a3d0a9f34dd925f62f4c73bd33a4db at 16a6b8b8/bd14096a (matches receipts); 1a8b27243a00cede1b93f8d3e95201476c75b70a3bcaa59a7e51f2220e5f5ef4 at b1cbbc39/95abec21 (matches receipts).
- Exit 2 at 4c6be2bd carries error "key visible at the measured revision" (sealed_count.py:300-302), identical to receipt c1-at-4c6be2bd.json apart from keySource label.

## Evidence pointers
- My outputs: /fast/scratch/hyaku/kake-r35/w2/RerunC1Sealed/out-c1-at-{16a6b8b8,bd14096a,b1cbbc39,95abec21,4c6be2bd}.json (sha256: cd07e700…, c4bcddff…, 982eb349…, 16d632df…, a28a41e0…); stderr files empty.
- Receipts: .ufo/waves/round-35/verification/c1-at-{16a6b8b8,bd14096a,b1cbbc39,95abec21,4c6be2bd}.json.
- Counter: .ufo/waves/round-35/sealed_count.py (pin at :57, key-visible exit at :300-302, head fields at :298-299).

Not verified: nothing outstanding — all five specified runs executed; no network, no tools installed (none needed). Verdict evidence: C1 landed values stand. `