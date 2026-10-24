# ExecCounterV6 — round-45 wave 1

Axes: freshness and operability (this item is judged on freshness).

## Change
Byte-copied `round-44/c44_count_v5.py` to `round-45/c45_count.py`. Corrected the provenance line to identify the following Round-42 version 3 header. Preserved the v5 predicate string as `PREDICATE_V5`, added the requested v4-only predicate as `PREDICATE_V4`, and made the receipt's `predicate` select by `a.classes`. The diff contains exactly three hunks: one docstring hunk and two predicate-text hunks; no OTHER hunks. Run lists, class loading, and scoring are unchanged.

## Named attack and evidence
C2(b) attack: **PASS at source/configuration level** — v4 mode selects `PREDICATE_V4`, which names only the eleven v4 runs, not the ten class runs. The counter was not run, so runtime receipt emission was not exercised.

Exact commands run:

```sh
mkdir -p /fast/scratch/hyaku/kake-r45/ExecCounterV6 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-45/v6diff && cp -- /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-44/c44_count_v5.py /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-45/c45_count.py
```

```sh
diff -u .ufo/waves/round-44/c44_count_v5.py .ufo/waves/round-45/c45_count.py > .ufo/waves/round-45/v6diff/v5-v6.diff; rc=$?; printf 'diff exit status: %s\n' "$rc"
```

Verbatim output:

```text
diff exit status: 1
```

Status 1 is expected for the requested changes; the resulting diff is `.ufo/waves/round-45/v6diff/v5-v6.diff`. Its three hunks are the docstring correction and predicate declaration/receipt selection changes; none is OTHER.

```sh
python3 -c 'import ast,pathlib,sys; root=pathlib.Path("."); get=lambda p,n: next(ast.literal_eval(x.value) for x in ast.walk(ast.parse((root/p).read_text())) if isinstance(x,ast.Assign) and any(isinstance(t,ast.Name) and t.id==n for t in x.targets)); old=get(".ufo/waves/round-44/c44_count_v5.py","PREDICATE"); new=get(".ufo/waves/round-45/c45_count.py","PREDICATE_V5"); ok=old.encode("utf-8")==new.encode("utf-8"); print("PREDICATE_V5 byte-identical to v5 PREDICATE: {}".format("PASS" if ok else "FAIL")); sys.exit(0 if ok else 1)'
```

Verbatim output:

```text
PREDICATE_V5 byte-identical to v5 PREDICATE: PASS
```

## Files written
- `.ufo/waves/round-45/c45_count.py`
- `.ufo/waves/round-45/v6diff/v5-v6.diff`
- `.ufo/waves/round-45/w1/ExecCounterV6.md`

Created scratch directory `/fast/scratch/hyaku/kake-r45/ExecCounterV6/`; no scratch files or tools were installed. No tests, lint, formatter, build, or counter run. No blockers. Remaining risk: runtime receipt emission was intentionally not exercised; the parent owns post-integration checks. Additional documentation risk: the unchanged opening banner on `c45_count.py` lines 2-3 still identifies this file as the Round-44 version 5 counter. I left it unchanged to honor the exact requested scope; L1 can decide whether to broaden the docstring update.
