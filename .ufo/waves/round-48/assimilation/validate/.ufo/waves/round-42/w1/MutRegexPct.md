MET — unicodedigit is a witnessed behavior-changing control; portpct also met but is not a control.

Axes: operability (tested); freshness (not exercised). Leaf mutation probe only; no round/admission verdict.
Aliases: R=/home/vgpnk/Projects/shokunin/kake-shokunin; S=/fast/scratch/hyaku/kake-r42w1/MutRegexPct; C=$R/.ufo/waves/round-42/c42_count.py.
Original $S/../shared is not used: reference is /fast/scratch/hyaku/kake-r42/shared/tip41.py, SHA256 50287ac6de5600ab1fca5a4cb77d9f3b8a170ad0a63f287512f9403bdb1dde7d.
Counter SHA256 7bfc32c5e76dca942208934cfbe89f166eda2776b40e69de987706b4d97dd2a6; Python 3.14.8; seed 42071 throughout.
Built rewrite.py: possessive disjoint character runs and component repetitions, preserving the original character repertoire and urlsplit checks ($S/rewrite.py:76-85).
Historical scoring command, instantiated once for each name in the table: `timeout 900 prlimit --as=8000000000 -- env TMPDIR=$S python3 -B $C --root $R --tool-file $S/NAME.py --label MutRegexPct-NAME --seed 42071 --out $S/NAME.json`.
All command exits are in the table; no counter rerolls. One additional launcher attempt for onehex was refused by the harness job cap before starting; its successful execution is the only scored onehex run.
Retained mutant tools are $S/mutants/NAME.py; historical $S/NAME.py targets have now been restored. Receipts remain $S/NAME.json. Ratios below are T1,T2,T3,T4,T5.

| NAME / changed line | One-member change | SHA256 of scored/retained bytes | Exit; equalRuns; ratios; met | Detector verdict / caught runs |
|---|---|---|---|---|
| rewrite:76-85 | pristine fast rewrite | 7b9ed1be7a1bb628ad2e6dbd19041594b1740c944869b5b610cf0a4bdffff5f3 | 0; 8/8; 1.161,1.433,1.163,1.074,1.934; true | baseline holds |
| onehex:75 | percent hex quantifier {2} → {1} | d8defa56d8cf31ae0c62f914befe3b53f134a28c208901d0ab4dfd39c4c20d1d | 1; 4/8; 1.248,1.457,1.123,1.074,1.943; false | killed: A,C,T1,T5 |
| loweronly:75 | remove uppercase A-F member from hex class | 187bebee13c5941fc07f23fa72f28c3da5617ceced86744d632013e08ef1a084 | 1; 1/8; 0.841,0.830,0.881,1.102,1.000; false | killed: A,B,C,T1,T2,T3,T5 |
| terminalpct:75 | percent hex quantifier {2} → {0,2} | c4aee456ef16a77fd8e4ce66447a51464c1003aa2968c716658109c10a2d6b41 | 1; 4/8; 1.269,1.389,1.087,1.117,1.894; false | killed: A,C,T1,T5 |
| hostpct:81 | add % to reg-name character class | b2df8a28b0e36c1987f676ed13fb146b1fed65e9a97595880569af4e4f578935 | 1; 7/8; 1.176,1.429,1.131,1.064,1.783; false | killed: A |
| portpct:82 | add % to port digit class | d1e06ba366c6253229d30948a809e14d58f1fc2306b26ea61f382802d1bfa504 | 0; 8/8; 1.177,1.444,1.102,1.106,1.734; true | survived; no behavior witness found; not a control |
| upperonly:75 | remove lowercase a-f member from hex class | 91eceae681088a65088eec17f3181a6d049add125cfd6acf16fa701d7b3958f9 | 1; 1/8; 0.819,0.847,0.844,1.089,0.949; false | killed: A,B,C,T1,T2,T3,T5 |
| unicodedigit:75 | replace 0-9 with Unicode-aware \d in percent hex class | 7498d17f310c4fa790107db7a8252097b921d815e0cf74227f6d9461de8e2a4f | 0; 8/8; 1.217,1.433,1.104,1.078,1.898; true | survived with behavior witness; none caught |
For every timing run marked caught, candRepsEqual=0/5; all other timing runs have 5/5. Both meeting mutants have A/B/C and all timing repetitions equal.

Witness: `https://example.test/%\u06610` (literal U+0661 ARABIC-INDIC DIGIT ONE, followed by ASCII zero).
Tip41 _parse_url returns None; unicodedigit returns (https, example.test, 443, /%\u06610). Full CLI: tip41 exit 1 with loc_not_absolute; mutant exit 0 with clean/empty findings.
Exact CLI command template: `timeout 30 prlimit --as=8000000000 -- python3 -B TOOL --manifest $S/witnesses/NAME/manifest.json`, TOOL=/fast/scratch/hyaku/kake-r42/shared/tip41.py and $S/mutants/NAME.py; complete argv/stdout/stderr/exits for all seven pairs are in $S/witnesses.json.
Witness driver command: `timeout 180 prlimit --as=8000000000 -- python3 -B witness_probe.py` (cwd $S), exit 0.
Other concrete witnesses: onehex /%2 (1→0); loweronly /%AF (0→1); terminalpct /a% (1→0); hostpct https://a%z.test/a (1→1, loc_not_absolute→loc_out_of_scope); upperonly /%af (0→1). Paths without an explicit host use https://example.test.
Port witness https://example.test:80%/a: regex false→true, but _parse_url is None in both and CLI output identical. The existing parts.port ValueError guard rejects the added percent forms ($S/mutants/portpct.py:102-104).

Expected bounded behavioral detector: compare exact _parse_url tuples with tip41 on 107,931 independently generated values; regex equality is diagnostic only. Inputs include exhaustive ASCII percent pairs, component insertions, bracket edits, random values and long values; fixed seed 42071.
Detector $S/own_diff.py SHA256 322f199b5834c429584c400bb567c148b274d316b28a292b46895c719505ce17; exact per-file command: `timeout 120 prlimit --as=8000000000 -- python3 -B $S/own_diff.py $S/NAME.py $S/NAME-PHASE-diff.json`.
Driver commands (cwd $S), each exit 0: `timeout 150 prlimit --as=8000000000 -- python3 -B run_diff.py pristine rewrite`; `timeout 180 prlimit --as=8000000000 -- python3 -B run_diff.py mutated onehex loweronly terminalpct hostpct portpct upperonly`; `timeout 180 prlimit --as=8000000000 -- python3 -B run_diff.py mutatedExtra unicodedigit`; `timeout 240 prlimit --as=8000000000 -- python3 -B run_diff.py restored onehex loweronly terminalpct hostpct portpct upperonly unicodedigit`.
Actual parse mismatches / child exits: pristine rewrite 0/0; mutated onehex 6687/1, loweronly 1215/1, terminalpct 32216/1, hostpct 6614/1, portpct 0/0, upperonly 1208/1, unicodedigit 0/0; every restored target 0/0. Portpct had seven diagnostic regex-only differences. The independent generator also missed Unicode digits; the concrete CLI witness supplies the missing disproof.
Restoration evidence: each working target followed rewrite SHA256 → its table mutant SHA256 → rewrite SHA256 7b9ed1be7a1bb628ad2e6dbd19041594b1740c944869b5b610cf0a4bdffff5f3. All seven restored files have that exact hash before and after the unchanged bounded detector. No baseline failure; no inconclusive mutants.
Full detector commands, actual output, detector hashes and input before/after hashes: $S/diff-pristine.json, diff-mutated.json, diff-mutatedExtra.json, diff-restored.json. Archived mutants are intentional evidence copies, not unrestored working targets.

Checked statements: fast rewrite equality holds on the exercised independent and counter inputs (not an exhaustive proof); obvious one-/zero-hex, case and host-percent defects are caught — holds for the five killed mutants.
`met` as sufficient evidence for “keeps EVERY judgment” — overstated: $S/mutants/unicodedigit.py:75 changes a judgment while meeting. The generated-run predicate itself holds on this receipt; this is a coverage finding, not a changed contract or round verdict.
Generator gap: $C:71,74,81 restrict percent units/hex generation and non-ASCII samples without Unicode decimal digits, so the plausible 0-9→\d defect is not exercised.
Bounds: maximum two own counter processes concurrently; TMPDIR stayed under $S; all started commands terminated; counter temporary directories cleaned. Retained sandbox size: 308,749 bytes (`timeout 30 prlimit --as=8000000000 -- du -sb $S`, exit 0). No installs/updates, network requests, lane source edits, or Git/jj mutations.
