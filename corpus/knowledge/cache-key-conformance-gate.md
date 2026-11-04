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

RFC 9110 §5.5, lines 1606–1607 (S466):

> Field values containing CR, LF, or NUL characters are invalid and dangerous

RFC 9111 §2, line 251 (S467):

> The "cache key" is the information a cache uses to choose a response

RFC 8259 §8.1, lines 485–486 (S468):

> JSON text exchanged between systems that are not part of a closed ecosystem MUST be encoded using UTF-8

## Decision table — what the gate scores

| Population | How it is built | Scored into `met` | Why |
|---|---|---|---|
| Hand cases (92) | One or more per contract clause: members, names, values, escaping, layout, refusals; 70 at the carrier `7f6c68f1`, 22 added from the round-90 wave's false admits (ExecStubs S01–S08, S10–S14, S23; CriticClaims H1–H7) | yes | each clause has a case a one-clause shortcut fails |
| Generated cases (120) | From a seed chosen at run time (printed) and decided by the gate's own reference | yes | a table over committed cases cannot pass |
| Advisory cases (4) | Inputs the contract leaves undecided or decides two ways, and a source decides: non-UTF-8 bytes and raw control in a JSON string (S468; the contract's example 5 says raw, its Input clause says JSON), NUL in a value (S466), two JSON members with one header name (round-89 routed definition) | no — own line `advisory=X/Y` | surfaces contract gaps without silently widening the contract |
| Output protocol | success: stdout is one JSON object with exactly one member `key` (duplicate members visible), any whitespace layout; refusal: exit 1, empty stdout, a stderr line `invalid_input: <reason>` | yes | the contract's Output section, no stricter (ReviewGate F3) |
| Sandbox | Audit hook around the candidate, its state bound at install time: stdlib imports only, minus modules that spawn processes or load native code (`_posixsubprocess`, `ctypes`, `socket`, sub-interpreters, …); open only itself, the wrapper and stdlib, checked both textually and by `realpath`; exact `str`/`bytes` paths only; no process, socket, `gc` object walk or audit-hook change; stdin decoded as strict UTF-8 | yes (any violation fails) | an oracle import, a counter-file read or a child process is not an implementation |

## Error patterns

| Pattern | Seen in | What catches it |
|---|---|---|
| Sorting `Vary` members by raw text, then lowercasing | `adv-raw-sort` | `sort-lowered-a-B`, `sort-lowered-B-a` |
| Escaping values but not names (`%` is a tchar) | `adv-no-name-escape`, MutKey M37 | `name-percent-present`, `name-percent-absent` |
| Refusing only LF, or only nominated fields | `adv-cr-only`, M23/M24 | `cr-only`, `cr-unnominated`, `lf-unnominated-novary` |
| Treating a missing `request_headers` as `{}` | `adv-missing-headers` | `headers-missing`, `headers-missing-vary` |
| Crashing on malformed JSON (exit 1 without `invalid_input:`) | `adv-bad-json` | `malformed-json`, `empty-input` (at the carrier the traceback also tripped the sandbox; after the wave a traceback is an ordinary failure) |
| Delegating to the counter's reference | round-90 `neg-oracle-path-import`, `neg-exec-source`; wave probes (ExecSandbox c01–c21, ScoutGround and ReviewGate `fork_exec`, CriticClaims `readline`) | sandbox (exit 97, uncatchable) |
| Delegating through a child process (`_posixsubprocess.fork_exec` raises no audit event) | ScoutGround F1, ReviewGate F1, ExecSandbox c11 | the module is denied at import |
| Rebinding the hook's state through frame globals, `gc`, or a spoofed `os.path.realpath` | ExecSandbox c05, c13, c18, c20, c21 | state lives in the hook's bound arguments; `gc.get_*` denied; textual path check |
| Sorting members in a non-code-point order, truncating long lists, dropping tchars | ExecStubs S03, S16; CriticClaims H1, H2 | `codepoint-order`, `nine-members`, `every-tchar` |
| Normalising or case-folding non-ASCII values or URIs; trimming the URI | ExecStubs S07, S08, S10, S11, S23; CriticClaims H3 | `non-ascii-case-kept`, `no-normalisation`, `uri-*-kept` |
| Duplicate `key` members in the output | ExecStubs S13 | member-list judge |
| Calling M37 "equivalent" because names "cannot contain `%`" | round-89 MutKey §5.2 | `name-percent-absent` kills it |

## Limits (what this gate does not show)

- The shipped candidate fails two advisory cases: a NUL inside a value is kept, and two
  JSON members with one header name collapse to the last one. Both are routed (R90-2,
  R90-5), not scored. Non-UTF-8 input is refused once stdin is strict (the carrier's
  advisory failure came from the gate's own C-family locale, ReviewGate F4).
- A stub that refuses NUL (ExecStubs S09) is admitted: the contract is silent and the RFC
  allows rejection, so the gate cannot call it non-conforming.
- The contract's worked example 5 says the separators are carried raw inside the JSON
  string; RFC 8259 §7 requires them escaped, and the candidate refuses the raw form.
  The gate sends them escaped; the wording is a routed contract defect (R90-3).
- RFC 9111 §2 composes the key from at least the method and the target URI; the
  contract's key omits the method (adapter limit, recorded on S467).
- The sandbox is an in-process audit hook; native code already loaded by the stdlib is
  not confined, and a candidate can detect the gate's environment and behave differently
  outside it. It is evidence against delegation, not a security boundary.

## Runnable checklist

```sh
cd /home/vgpnk/Projects/shokunin/kake-shokunin
S=$(mktemp -d "${TMPDIR:-/fast/scratch}/ckc.XXXXXX") && trap 'rm -rf -- "$S"' EXIT
python3 -B scripts/cache_key_conformance.py --candidate scripts/cache_key.py --work "$S"
# expect: advisory=2/4 outside-contract-gaps=nul-in-value,dup-json-member
#         clauses=6/6 hand=92/92 generated=120/120 sandbox=ok seed=<S> met=true ; exit 0
python3 -B scripts/cache_key_conformance.py --candidate .ufo/waves/round-89/w1/ExecControls/adv-cr-only.py --work "$S"
# expect: met=false ; exit 1
python3 -B scripts/cache_key_conformance.py --candidate .ufo/waves/round-90/frozen/neg-exec-source.py --work "$S"
# expect: sandbox=violation met=false ; exit 1
```
