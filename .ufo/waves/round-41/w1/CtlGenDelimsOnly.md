# CtlGenDelimsOnly — KILLED: delimiter-only control scores 1068/1434
Axes: operability measured; freshness unchanged/unmeasured. One assigned mutation probe, no round judgment.
Mutant: replace the reference RFC repertoire/percent validator with a complete gen-delimiter-placement regex; retain the base tool's whitespace guard, urlsplit, scheme, nonempty-host and port checks. No character allow-list, percent-triplet validation, case-label reading or generator-template matching was added.
Expected detector: the unchanged C1 counter must return exit 1 / met=false for this cheaper validator, while pristine and restored reference bytes return exit 0 / met=true; all runs use seed 41001.

## Tools and hashes
- Returned control: `/fast/scratch/hyaku/kake-r41w1/CtlGenDelimsOnly/delims_only.py`, sha256 `5964074c8bca566b29dfcef776d21712e0932555bce4a0b573e4a1ec05f32bab`.
- Restored probe: `/fast/scratch/hyaku/kake-r41w1/CtlGenDelimsOnly/probe.py`, pristine and restored sha256 `6d7c2dd445fc7d3b2df7c3307d18f05c7f2cf6154830430dbc15dd372509010a`; during mutation its hash was the returned control hash above.
- Counter sha256 `2acc443af33466796ad178d8c1ad8350d36250b29e7383bba4ba10d2e4fe67b4`; oracle sha256 `cdcac127b3693ded2b00565878d8ed2b96d34b29f0ee199c06d7b40baaf60917`.

## Exact detector commands and actual outputs
All commands ran from `/fast/scratch/hyaku/kake-r41w1/CtlGenDelimsOnly`; receipts are absolute paths below.
`timeout 900 prlimit --as=4000000000 -- env TMPDIR=/fast/scratch/hyaku/kake-r41w1/CtlGenDelimsOnly/tmp python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-41/c1_count.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --tool-file /fast/scratch/hyaku/kake-r41w1/CtlGenDelimsOnly/probe.py --seed 41001 --label CtlGenDelimsOnly-pristine --out /fast/scratch/hyaku/kake-r41w1/CtlGenDelimsOnly/pristine.json` — exit 0.
Pristine receipt: passed=1434/1434; byField={loc:630/630,sitemapUrl:804/804}; byComponent={fragment:239/239,host:239/239,path:239/239,port:239/239,query:239/239,userinfo:239/239}; met=true; note=null.
`timeout 900 prlimit --as=4000000000 -- env TMPDIR=/fast/scratch/hyaku/kake-r41w1/CtlGenDelimsOnly/tmp python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-41/c1_count.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --tool-file /fast/scratch/hyaku/kake-r41w1/CtlGenDelimsOnly/delims_only.py --seed 41001 --label CtlGenDelimsOnly-mutant --out /fast/scratch/hyaku/kake-r41w1/CtlGenDelimsOnly/mutant.json` — exit 1.
Mutant receipt: passed=1068/1434; byField={loc:519/630,sitemapUrl:549/804}; byComponent={fragment:163/239,host:165/239,path:172/239,port:239/239,query:158/239,userinfo:171/239}; met=false; note=null.
`timeout 900 prlimit --as=4000000000 -- env TMPDIR=/fast/scratch/hyaku/kake-r41w1/CtlGenDelimsOnly/tmp python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-41/c1_count.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --tool-file /fast/scratch/hyaku/kake-r41w1/CtlGenDelimsOnly/probe.py --seed 41001 --label CtlGenDelimsOnly-restored --out /fast/scratch/hyaku/kake-r41w1/CtlGenDelimsOnly/restored.json` — exit 0.
Restored receipt: passed=1434/1434; byField={loc:630/630,sitemapUrl:804/804}; byComponent={fragment:239/239,host:239/239,path:239/239,port:239/239,query:239/239,userinfo:239/239}; met=true; note=null.
All three receipts report toolExit=2, distinct from the detector exits above; generated invalid manifest URL checks produce tool errors.

## Findings / checked statements
- HOLDS: the control skips non-delimiter repertoire and percent-triplet checks (`/fast/scratch/hyaku/kake-r41w1/CtlGenDelimsOnly/delims_only.py:69-84`); 366 cases catch it: 111 loc and 255 sitemapUrl, across every component except port.
- HOLDS: the counter separates this control from the reference on seed 41001. Examples in `mutant.json:29-76`: malformed fragment `%`, host U+0002, path backtick, fragment caret, host DEL and host `%4G` all have oracleValid=false yet are accepted.
- WRONG for this control: full RFC 3986 agreement. It scores 1068, not 1434. No claim about unrun seeds or other delimiter-only implementations is made.
- HOLDS: pristine and restored behavior agree exactly on all generated judgments; `pristine.json:4-28` and `restored.json:4-28`.

## Restoration evidence and bounds
`timeout 10 prlimit --as=4000000000 -- cp /fast/scratch/hyaku/kake-r41/shared/ref_fix.py /fast/scratch/hyaku/kake-r41w1/CtlGenDelimsOnly/probe.py && timeout 10 prlimit --as=4000000000 -- cmp /fast/scratch/hyaku/kake-r41/shared/ref_fix.py /fast/scratch/hyaku/kake-r41w1/CtlGenDelimsOnly/probe.py && timeout 10 prlimit --as=4000000000 -- sha256sum /fast/scratch/hyaku/kake-r41w1/CtlGenDelimsOnly/probe.py /fast/scratch/hyaku/kake-r41w1/CtlGenDelimsOnly/delims_only.py` — exit 0; cmp emitted nothing; hashes were respectively `6d7c2dd445fc7d3b2df7c3307d18f05c7f2cf6154830430dbc15dd372509010a` and `5964074c8bca566b29dfcef776d21712e0932555bce4a0b573e4a1ec05f32bab`.
The first edit encountered copied read-only permissions (EACCES); bounded `chmod u+w` exited 0, the file was reopened, and the mutation then applied. No detector failure was concealed.
Verdict: KILLED, not baseline-inconclusive. Exact probe bytes restored; the separately preserved control is intentionally returned for L1 re-scoring. Shared files and lane code were never modified; no network, installations, subagents, background jobs, or checks beyond this probe. All started command trees exited.
