# MutCounters-5 — survivors (kake round 100, w1)

Mutant = single-point edit of a predicate-bearing line of a frozen counter; killed = any committed
battery command (selftest, base, committed fixtures/candidates) produced a different (rc, stdout)
than the byte-identically reproduced pristine baseline. Surviving = identical output on every
assigned command. Equivalence is judged separately: a survivor is equivalent only if NO input
distinguishes it. 11 of 32 mutants survived; 10 are separated by constructed inputs, 1 is
equivalent-in-context. Demos: `evidence/sepout-*.txt`; per-mutant table: `mutants.tsv`.

## c100_registry.py survivors (7)

### reg-m01 — `INTERP` drops `python` (line 88)
Committed battery: identical (selftest 29/29, base, pos, keepold, deleteall). Not equivalent.
Separating input: a registry row invoking a tool as `python scripts/a.py` beside the `python3` row.
Observed (demo sep-interp-python): pristine `duplicated=1 … mismatches=1 met=false`; mutant never
sees the `python` invocation → `duplicated=0 … mismatches=0 met=true` (rc 1 → 0).
Coverage gap: the committed registry tables contain no `python`-interpreter invocation, so
interpreter-set membership is untested for `python`.

### reg-m02 — `INTERP` drops `node` (line 88)
Committed battery: identical. Not equivalent.
Separating input: two rows invoking `scripts/z.mjs` as `` `node scripts/z.mjs` `` /
`` `node ./scripts/z.mjs` ``. Observed: pristine `duplicated=1 probe_mismatch=… met=false`;
mutant `duplicated=0 met=true` (rc 1 → 0). Coverage gap: no committed row invokes a tool through
`node`, so the interpreter branch for `.mjs` entry commands is untested end-to-end.

### reg-m05 — escaped-pipe split `re.split(r"\\\||\|")` → `re.split(r"\|")` (line 108)
Committed battery: identical. Not equivalent — and subtler than intended: both regexes split at
every pipe position; they differ only in whether the preceding backslash is consumed, so the
committed `printf x \| python3 …` case (space-separated) cannot distinguish them.
Separating input: an escaped pipe immediately after the path with no space — entry cell
`` `python3 -B scripts/a.py\|cat` ``. Pristine consumes `\|` as a separator and finds first word
`scripts/a.py`; mutant leaves first word `scripts/a.py\` → invocation missed. Observed: pristine
`duplicated=1 … mismatches=2 met=false` (rc 1), mutant `duplicated=0 … mismatches=1` (rc 0) — the
mutant would accept a registry the frozen counter rejects.

### reg-m10 — `PROBE_ARG = "--zz-bogus-r100"` → `"--zz-bogus-r99"` (line 89)
Committed battery: identical — every committed invoked tool treats any unknown flag alike, so the
constant's exact value is untested. Not equivalent.
Separating input: a tool that exits 2 only for the exact argument list
`['--zz-bogus-r100']`, in a row whose verdict map names only `` `2` `` (row nonconformant on R3 but
still probe-checked: D2 applies to every invoking row). Observed: pristine probe rc=2 ∈ codes → no
`probe_mismatch` line; mutant probe rc=0 ∉ codes → `probe_mismatch 1 scripts/a.py rc=0 codes=2`.

### reg-m11 — sandbox `--unshare-all` → `--unshare-net` (line 95)
Committed battery: identical — every committed probe and self-test span behaves the same whether
or not PID/IPC/UTS namespaces are unshared; network isolation is kept by the mutant, so even the
`v2-probe-sandbox-no-network` selftest case passes. Not equivalent.
Separating input: a tool that introspects `/proc` (counts digit-named entries) and exits 0 when
isolated (≤5 pids) else 7, with a verdict map naming only `` `7` ``. Observed: pristine probe sees
pid ns `[1, 2]` → rc 0 → `probe_mismatch 3 … rc=0 codes=7`; mutant shares the host PID space → rc 7
→ no mismatch line. Note: on this host the committed network probe is degenerate — outbound
1.1.1.1:53 is unreachable, so that control passes with or without `--unshare-net`. Host-level
observation, routed not repaired.

### reg-m13 — `names_path` boundary classes dropped (line 213)
Committed battery: identical — no committed cell names a scripts path only as a substring of a
longer token. Not equivalent.
Separating input: entry cell `` `python3 -B scripts/a.py.bak` `` with a working self-test cell
naming `scripts/a.py`. Pristine: R2 boundary requires the path to end at `[\s'\"$]` → row
nonconformant → `unlisted=1`; mutant: substring match → row conformant → `unlisted=0` (rc unchanged,
first line flips `listed`).

### reg-m14 — fence length `m.group(1)[:3]` → `m.group(1)` (line 162)
Committed battery: identical — no committed SKILL.md uses a >3-char fence. Not equivalent.
Separating input: a block opened with 4 backticks containing a registry table, an inner 3-backtick
line, the 4-backtick close, then a second table. Pristine truncates the fence marker to 3 chars,
closes at the inner line, then re-opens a fence at the closer → `rows=0`; mutant keeps the
4-backtick fence intact → second table live → `rows=1`. The mutant is the CommonMark-correct
behavior, i.e. the committed parser mis-parses long fences (coverage finding on the counter;
frozen instrument — routed, not patched).

## c100_fresh304.py survivors (4)

### fr-m08 — output trim OWS set `.strip(OWS)` → `.strip()` (line 228)
Committed battery: identical (every committed case value contains only SP/HTAB). Not equivalent.
Separating input: any header value containing whitespace outside `" \t"`, e.g. `x-v: "\x0bv\x0b"`.
Observed (module-level `decide_bytes`): pristine `updated[0].headers.x_v = "\u000bv\u000b"`;
mutant `"v"` — the stored/updated value differs although both trim, because RFC 9110 OWS is
exactly SP/HTAB.

### fr-m12 — `decide_bytes` error set → `except ValueError` (line 236)
Committed battery: identical. Two reasons stacked: `UnicodeDecodeError` is a `ValueError` subclass,
so dropping it changes nothing; and `RecursionError` is unreachable at committed input depths.
Not equivalent.
Separating input: RAW JSON with a 60000-deep array (`{"pad": [[[…]]], "stored": [], …}`). Observed:
pristine catches `RecursionError` → clean `Refuse` (refusal); mutant propagates → `CRASH
RecursionError` (the counter would abort mid-drift-check). Depth 5000/20000 do not separate — the
committed grammar cannot produce such inputs.

### fr-m14 — judge drops whitespace strictness `if s != s.strip() or not s:` → `if not s:` (line 522)
Committed battery: identical. The `neg-e4-wsstdout` forgery exercises only the refusal-emptiness
clause (its failure mass is `refusals=0/119`); no committed candidate emits a success object with
surrounding whitespace, and `json.loads` tolerates leading/trailing spaces itself. Not equivalent —
and this is the highest-value finding of the seat:
Separating input: a candidate semantically equal to the positive oracle that prints
`"   " + json + "   \n"`. Observed: pristine `hand=43/91 generated=76/300 … met=false` (rc 1);
mutant `hand=91/91 generated=300/300 met=true` (rc 0) — **the frozen C2 target predicate is
reachable by a whitespace-padded candidate under this mutant**. The whitespace clause of the
success judge is uncovered by the committed forgery set. Routed to the L1; the instruments are
frozen, so this is a coverage admission, not a repair.

### fr-m15 — `sandbox_ok` drops the pid assertions → `return rc == 0` (line 512)
Committed battery: identical (`--selftest` never reaches `sandbox_ok`; every candidate run still
passes the weakened gate because the committed `SANDBOX` argv itself still isolates the PID
namespace). Equivalent-in-context: the check re-asserts a property the argv it precedes already
guarantees on this host, so no constructable input distinguishes them without sabotaging bwrap —
a host-level change the bounds forbid. Defense-in-depth redundancy, documented not exercised.

## Summary

| counter | mutants | killed | survived | separated | equivalent |
|---|---|---|---|---|---|
| c100_registry.py | 15 | 8 | 7 | 7 | 0 |
| c100_fresh304.py | 17 | 13 | 4 | 3 | 1 |
| total | 32 | 21 | 11 | 10 | 1 |
