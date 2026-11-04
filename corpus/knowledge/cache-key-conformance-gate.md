source: S466 — RFC 9110 §5.5 Field Values — https://www.rfc-editor.org/rfc/rfc9110.txt; S467 — RFC 9111 §2 and §4.1 (supersedes S463 for construction ground) — https://www.rfc-editor.org/rfc/rfc9111.txt; S468 — RFC 8259 §7 and §8.1 — https://www.rfc-editor.org/rfc/rfc8259.txt. Bodies retained at `.ufo/waves/round-90/L1/src/` (rfc9110.txt 502941 bytes sha256 21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a; rfc9111.txt 84477 bytes sha256 aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e; rfc8259.txt 28360 bytes sha256 61a5378f4255c720beb2a4b4a63b29540147c140f36988bf086291989b4cd2d7).
verified-at: 2026-11-04 — all three plain-text bodies fetched by the round-90 L1 at 22:01:10Z and 22:07:31Z (HTTP 200); the two RFC 9110/9111 digests equal the round-89 retained copies byte for byte.
recheck: 180d, due 2027-05-03, or sooner after an RFC erratum on these sections. Re-fetch into a scratch directory, compare the three sha256 values, and re-locate RFC 9110 lines 1606–1612, RFC 9111 lines 251–262 and RFC 8259 lines 424–431 and 483–486.
ground: operability — round-90 C2, a capability acquisition: a behavioural gate that decides whether a cache-key constructor implements the lane's key contract.
scope: conformance of a stdin/stdout key constructor to `.ufo/waves/round-89/c2-contract.md`. Not storability, freshness, revalidation, reuse or serving; not what any cache does.

# Deciding whether a cache-key constructor conforms

Round 89 shipped `scripts/cache_key.py` and a counter that could not tell it apart from
seven non-conforming stubs (`.ufo/waves/round-89/w1/ExecControls/scoring-receipt.txt`):
every one of its cases left a contract clause unexercised. This entry is the instrument
that does tell them apart: `scripts/cache_key_conformance.py --candidate <script>`.

## Located quotes

RFC 9110 §5.5, lines 1606–1609 (S466):

> Field values containing CR, LF, or NUL characters are invalid and dangerous

RFC 9111 §2, line 251 (S467):

> The "cache key" is the information a cache uses to choose a response

RFC 8259 §8.1, lines 485–486 (S468):

> JSON text exchanged between systems that are not part of a closed ecosystem MUST be encoded using UTF-8

## Decision table — what the gate scores

| Population | How it is built | Scored into `met` | Why |
|---|---|---|---|
| Hand cases (70) | One or more per contract clause: members, names, values, escaping, layout, refusals | yes | each clause has a case a one-clause shortcut fails |
| Generated cases (120) | From a seed chosen at run time (printed) and decided by the gate's own reference | yes | a table over committed cases cannot pass |
| Advisory cases (3) | Inputs the contract does not decide but a source does: non-UTF-8 bytes, raw control in a JSON string (S468), NUL in a value (S466) | no — own line `advisory=X/Y` | surfaces contract gaps without silently widening the contract |
| Sandbox | Audit hook around the candidate: stdlib imports only; open only itself and stdlib; no process, socket, ctypes, listing outside stdlib | yes (any violation fails) | an oracle import or an exec of a counter file is not an implementation |

## Error patterns

| Pattern | Seen in | What catches it |
|---|---|---|
| Sorting `Vary` members by raw text, then lowercasing | `adv-raw-sort` | `sort-lowered-a-B`, `sort-lowered-B-a` |
| Escaping values but not names (`%` is a tchar) | `adv-no-name-escape`, MutKey M37 | `name-percent-present`, `name-percent-absent` |
| Refusing only LF, or only nominated fields | `adv-cr-only`, M23/M24 | `cr-only`, `cr-unnominated`, `lf-unnominated-novary` |
| Treating a missing `request_headers` as `{}` | `adv-missing-headers` | `headers-missing`, `headers-missing-vary` |
| Crashing on malformed JSON (exit 1 without `invalid_input:`) | `adv-bad-json` | `malformed-json`, `empty-input` |
| Delegating to the counter's reference | round-90 `neg-oracle-path-import`, `neg-exec-source` | sandbox (exit 97, uncatchable) |
| Calling M37 "equivalent" because names "cannot contain `%`" | round-89 MutKey §5.2 | `name-percent-absent` kills it |

## Limits (what this gate does not show)

- The shipped candidate fails two advisory cases: non-UTF-8 input is accepted (Python's
  UTF-8 mode decodes stdin with `surrogateescape`, so the `UnicodeDecodeError` branch is
  unreachable) and a NUL inside a value is kept. Both are outside the contract as written;
  they are routed as contract gaps, not scored.
- The contract's worked example 5 says the separators are carried raw inside the JSON
  string; RFC 8259 §7 requires them escaped, and the candidate refuses the raw form.
  The gate sends them escaped; the wording is a routed contract defect.
- RFC 9111 §2 composes the key from at least the method and the target URI; the
  contract's key omits the method (adapter limit, recorded on S467).
- The sandbox is an in-process audit hook; native code already loaded by the stdlib is
  not confined. It is evidence against delegation, not a security boundary.

## Runnable checklist

```sh
cd /home/vgpnk/Projects/shokunin/kake-shokunin
S=$(mktemp -d "${TMPDIR:-/fast/scratch}/ckc.XXXXXX") && trap 'rm -rf -- "$S"' EXIT
python3 -B scripts/cache_key_conformance.py --candidate scripts/cache_key.py --work "$S"
# expect: advisory=1/3 outside-contract-gaps=utf8-required,nul-in-value
#         clauses=6/6 hand=70/70 generated=120/120 sandbox=ok seed=<S> met=true ; exit 0
python3 -B scripts/cache_key_conformance.py --candidate .ufo/waves/round-89/w1/ExecControls/adv-cr-only.py --work "$S"
# expect: met=false ; exit 1
python3 -B scripts/cache_key_conformance.py --candidate .ufo/waves/round-90/frozen/neg-exec-source.py --work "$S"
# expect: sandbox=violation met=false ; exit 1
```
