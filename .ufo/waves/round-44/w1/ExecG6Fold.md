# ExecG6Fold — G6 fold-pair attempt

Axis: operability (freshness is out of scope for this class item).

## Change

Wrote `.ufo/waves/round-44/classes/g6_fold_pairs.py`. It returns 100 `foldpair` units (200 URL values): 50 ASCII `k` → U+212A Kelvin-sign substitutions and 50 ASCII `s` → U+017F long-s substitutions. In each pair, the clean URL is first; the second differs only at that letter in the second path segment. The first path segment is unchanged. `n` is 200.

The requested witness did **not** result: all eight probes returned equal outputs. I am not reporting these as witnesses.

## Commands and evidence

Executed from `/home/vgpnk/Projects/shokunin/kake-shokunin`. Probe JSON below is trimmed to decisive fields; the probe's `ref41Tail` and `candTail` fields are omitted. Each command and its result are shown.

```sh
TMPDIR=/fast/scratch/hyaku/kake-r44/ExecG6Fold python3 -B .ufo/waves/round-44/c44_probe.py --root . --class G6 --tool-file .ufo/waves/round-44/controls-r43/casememo-v3-validity-lower.py --seed 44
```
```json
{"probe":"G6","seed":44,"units":100,"values":200,"ref41Exit":0,"candExit":0,"ref41OutSha256":"2f578c004a67e6dd1a21703a08ec43b682b5909093e5e9ff315176f77b2ede39","candOutSha256":"2f578c004a67e6dd1a21703a08ec43b682b5909093e5e9ff315176f77b2ede39","equal":true}
```

```sh
TMPDIR=/fast/scratch/hyaku/kake-r44/ExecG6Fold python3 -B .ufo/waves/round-44/c44_probe.py --root . --class G6 --tool-file .ufo/waves/round-44/controls-r43/casememo-v3-validity-lower.py --seed 440
```
```json
{"probe":"G6","seed":440,"units":100,"values":200,"ref41Exit":0,"candExit":0,"ref41OutSha256":"e062a5b0a55e3809a691e77a4ca5eac42380c0a8d636394fa19759c55b4d0aee","candOutSha256":"e062a5b0a55e3809a691e77a4ca5eac42380c0a8d636394fa19759c55b4d0aee","equal":true}
```

```sh
TMPDIR=/fast/scratch/hyaku/kake-r44/ExecG6Fold python3 -B .ufo/waves/round-44/c44_probe.py --root . --class G6 --tool-file .ufo/waves/round-44/controls-r43/casememo-v4-validity-lower-short.py --seed 44
```
```json
{"probe":"G6","seed":44,"units":100,"values":200,"ref41Exit":0,"candExit":0,"ref41OutSha256":"2f578c004a67e6dd1a21703a08ec43b682b5909093e5e9ff315176f77b2ede39","candOutSha256":"2f578c004a67e6dd1a21703a08ec43b682b5909093e5e9ff315176f77b2ede39","equal":true}
```

```sh
TMPDIR=/fast/scratch/hyaku/kake-r44/ExecG6Fold python3 -B .ufo/waves/round-44/c44_probe.py --root . --class G6 --tool-file .ufo/waves/round-44/controls-r43/casememo-v4-validity-lower-short.py --seed 440
```
```json
{"probe":"G6","seed":440,"units":100,"values":200,"ref41Exit":0,"candExit":0,"ref41OutSha256":"e062a5b0a55e3809a691e77a4ca5eac42380c0a8d636394fa19759c55b4d0aee","candOutSha256":"e062a5b0a55e3809a691e77a4ca5eac42380c0a8d636394fa19759c55b4d0aee","equal":true}
```

```sh
TMPDIR=/fast/scratch/hyaku/kake-r44/ExecG6Fold python3 -B .ufo/waves/round-44/c44_probe.py --root . --class G6 --tool-file .ufo/waves/round-44/controls-r43/casememo-v7-value-lower-nonascii.py --seed 44
```
```json
{"probe":"G6","seed":44,"units":100,"values":200,"ref41Exit":0,"candExit":0,"ref41OutSha256":"2f578c004a67e6dd1a21703a08ec43b682b5909093e5e9ff315176f77b2ede39","candOutSha256":"2f578c004a67e6dd1a21703a08ec43b682b5909093e5e9ff315176f77b2ede39","equal":true}
```

```sh
TMPDIR=/fast/scratch/hyaku/kake-r44/ExecG6Fold python3 -B .ufo/waves/round-44/c44_probe.py --root . --class G6 --tool-file .ufo/waves/round-44/controls-r43/casememo-v7-value-lower-nonascii.py --seed 440
```
```json
{"probe":"G6","seed":440,"units":100,"values":200,"ref41Exit":0,"candExit":0,"ref41OutSha256":"e062a5b0a55e3809a691e77a4ca5eac42380c0a8d636394fa19759c55b4d0aee","candOutSha256":"e062a5b0a55e3809a691e77a4ca5eac42380c0a8d636394fa19759c55b4d0aee","equal":true}
```

```sh
TMPDIR=/fast/scratch/hyaku/kake-r44/ExecG6Fold python3 -B .ufo/waves/round-44/c44_probe.py --root . --class G6 --tool-file .ufo/waves/round-44/controls-r43/casememo-v8-value-casefold-nonascii.py --seed 44
```
```json
{"probe":"G6","seed":44,"units":100,"values":200,"ref41Exit":0,"candExit":0,"ref41OutSha256":"2f578c004a67e6dd1a21703a08ec43b682b5909093e5e9ff315176f77b2ede39","candOutSha256":"2f578c004a67e6dd1a21703a08ec43b682b5909093e5e9ff315176f77b2ede39","equal":true}
```

```sh
TMPDIR=/fast/scratch/hyaku/kake-r44/ExecG6Fold python3 -B .ufo/waves/round-44/c44_probe.py --root . --class G6 --tool-file .ufo/waves/round-44/controls-r43/casememo-v8-value-casefold-nonascii.py --seed 440
```
```json
{"probe":"G6","seed":440,"units":100,"values":200,"ref41Exit":0,"candExit":0,"ref41OutSha256":"e062a5b0a55e3809a691e77a4ca5eac42380c0a8d636394fa19759c55b4d0aee","candOutSha256":"e062a5b0a55e3809a691e77a4ca5eac42380c0a8d636394fa19759c55b4d0aee","equal":true}
```

Fold-collapse command and output:

```sh
python3 -c "print('\u212a'.lower(), '\u212a'.casefold(), '\u017f'.casefold())"
```
```text
k k s
```

Reference investigation (read-only): materialized the pinned round-41 tool under scratch with:

```sh
git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 1ef7a0e95f6884dd113fe583a997c633fe330ddd:scripts/sitemap_audit.py > /fast/scratch/hyaku/kake-r44/ExecG6Fold/ref41_sitemap_audit.py
```

Command output: none. The pinned source has `_UNRESERVED` including `\u0080-\U0010ffff` at line 73, uses that in `_PCHAR` at line 76, and permits repeated `/<PCHAR>*` path segments in `_URI_RE` at lines 83-85. Thus U+212A and U+017F in a path are accepted by the round-41 grammar; they do not produce the claimed `loc_not_absolute` finding. This matches the probe results (both exits 0 and identical stdout hashes).

Also ran `mkdir -p /fast/scratch/hyaku/kake-r44/ExecG6Fold` and `mkdir -p .ufo/waves/round-44/w1`; both produced no output. No tools were installed. No build, full counter, lint, formatter, or separate test suite was run.

## Blocker

Acceptance is unmet: the required controls did not witness on either requested seed. The specified witness shape and Unicode letters are legal under the actual pinned round-41 path grammar, and the candidate/reference results are identical, so repeating or reshaping these pairs within the stated constraints cannot create the asserted `loc_not_absolute` difference. Missing prerequisite is a reference behavior that rejects these Unicode path members (or an updated assignment that names a genuinely rejectable semantic difference); no frozen reference/control artifact was changed. LSP tooling was not exposed in the supplied tool inventory, and this new module required no symbol refactor.