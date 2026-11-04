VERDICT: C2's frozen predicate holds at the carrier, but the gate's sandbox can be forged. A pure-stdlib `_posixsubprocess.fork_exec` delegation to `scripts/cache_key.py` gets `met=true sandbox=ok`. The gate also refuses contract-conforming candidates (traceback in the refusal path, no trailing newline), and the knowledge entry and the lesson's Mistakes 5 / R90-1 contain false statements.

Seat ReviewGate (agent id ReviewGate-2), round 90 wave 1. Scope: clause-by-clause review of `scripts/cache_key_conformance.py` (sha256 `2840f32e…7591`, the same bytes at carrier `7f6c68f1` and at HEAD `79e1aac2`) against `.ufo/waves/round-89/c2-contract.md`. Receipts are in `.ufo/waves/round-90/w1/ReviewGate/`, with input hashes in `inputs.sha256`. Python 3.14.8. Tools installed: none. Network: none.


Note: at the end of my review, someone other than this seat (presumably L1) had an uncommitted working-tree edit to `scripts/cache_key_conformance.py` (now sha256 `33650406…df08c`, diff +88/−41) and to `corpus/lessons/round-90.md`. I did not review that edit. Every finding here applies to the committed bytes `2840f32e…` (carrier `7f6c68f1` = HEAD), and should be re-checked against the edit before integration.
## Findings by severity

### F1 HIGH — the sandbox can be forged: a child process escapes the audit hook
- `SANDBOX._DENY` (lines 294–298) names `subprocess.Popen`, `os.exec*`, `os.posix_spawn`, `os.fork` and others. It does not name the audit event `_posixsubprocess.fork_exec`.
- `multiprocessing.util.spawnv_passfds` (stdlib) raises only that event: `probe_audit.py` logs `['_posixsubprocess.fork_exec']` and the child ran.
- Forgery `ReviewGate/forge_forkexec.py` contains no key logic. It spawns `python3 -I -B scripts/cache_key.py` and passes through the child's exit status. The child inherits fds 0–2 and runs with no audit hook.
- Command: `python3 -B scripts/cache_key_conformance.py --candidate forge_forkexec.py --seed 923161196 --verbose` gives `clauses=6/6 hand=70/70 generated=120/120 sandbox=ok met=true`, exit 0. A random seed gives the same result (seed 167987485, exit 0). Receipt: `ReviewGate/forge-run.txt`.
- Effect: the docstring ("spawn no process"), the knowledge entry ("no process", "sandbox (exit 97, uncatchable)") and the contract's candidate rule (no importing or reading the counter/oracle) are all enforceable only against naive delegation.
- This does not falsify the frozen C2 predicate: the population is pinned and no pinned negative uses this route. It does falsify the gate's own claim to tell delegation apart from an implementation.
- The disclosed limit ("native code already loaded … not confined") misnames the gap: this is a public pure-Python stdlib call.

### F2 MEDIUM — any traceback is mislabelled as a sandbox violation, so conforming candidates are refused
- When a candidate prints a stack (an uncaught exception, or `traceback.print_stack`), `traceback`/`linecache` opens the wrapper `ckc-*/sandbox.py`. That path is neither the candidate nor stdlib, so the hook kills the process with 97 and sets the global `violation` flag.
- Evidence 1: `ctl-constant-key.py` and `ctl-naive-join.py` import only `json`/`sys`, yet `controls/after-c2-carrier.txt` reports them `sandbox=violation`. So does `adv-bad-json.py`. `--verbose` shows `SANDBOX_VIOLATION open …/ckc-*/sandbox.py` on `malformed-json`/`empty-input`.
- Evidence 2: `ReviewGate/mine_tb.py` is my conforming candidate (F-REF below). It writes `invalid_input: <reason>` and then `traceback.print_stack(file=sys.stderr)`. The gate refuses it: 73 cases die with `SANDBOX_VIOLATION open …/sandbox.py`, exit 1 (`ReviewGate/gate-variants.txt`). The contract does not forbid extra stderr after the refusal line.
- No false admit results from this, but the carrier receipt's attribution ("violation") is wrong for 3 of the 57 negatives. Those three are still refused on behaviour.

### F3 MEDIUM — `judge()` is stricter than the contract's output protocol
- The contract says: "Success: one JSON object on stdout, `{"key": <string>}`, exit 0."
- `judge()` (lines 356–358) also requires exactly one line ending in `\n`.
- `ReviewGate/mine_nonl.py` is identical to `mine.py` except that it omits the trailing newline. The gate refuses it with `clauses=1/6 hand=36/70 generated=37/120 met=false` ("stdout must be one JSON line"). Receipt: `gate-variants.txt`. Pretty-printed JSON would be refused the same way.
- In the other direction, the refusal branch (line 350) accepts a bare `invalid_input:` with no `<reason>`, which is laxer than the contract's `invalid_input: <reason>` (found by inspection, not run).
- The rest of `judge()` matches the contract exactly:
  - refusal needs rc==1, empty stdout, and stderr starting `invalid_input:`;
  - success needs rc==0, UTF-8 JSON, a dict whose only key is `key`, and the exact key string;
  - stderr is ignored on success (the contract is silent there).

### F4 MEDIUM — the lesson (Mistakes 5, R90-1) and the knowledge entry misdiagnose the non-UTF-8 behaviour
They say the positives accept `\xff` because of "Python UTF-8 mode" and that the `UnicodeDecodeError` branch is "unreachable". Both are false:
- Under the gate's environment (`-I -S -B`, `LC_ALL=C.UTF-8`), `ReviewGate/env-probe.txt` shows `utf8_mode=0 ignore_environment=1 stdin.errors=surrogateescape`. `-I` also makes the gate's `PYTHONIOENCODING=utf-8` setting dead.
- The `surrogateescape` comes from the gate's own locale choice.
- Under `LC_ALL=en_US.UTF-8`, all four frozen positives refuse `\xff` with `invalid_input:`, rc=1 (`ReviewGate/positives-probe.txt`). So the branch is reachable and the advisory failure depends on the environment.
- The positives' accepting output, `{"key": "\udcff"}`, is a lone-surrogate key.

### F5 MEDIUM — exact-duplicate header names are not covered, and every positive admits them
- The contract's refusal reads: "two header names are equal case-insensitively". Exact-equal names are equal case-insensitively.
- Input `{"uri":"u","request_headers":{"a":"1","a":"2"},"vary":"a"}` is admitted by all four positives with last-wins (`{"key": "u\u001fa\u001e2"}`, rc=0, `positives-probe.txt`). `mine.py` refuses it.
- The gate has no such case. Its `reference()` works on a decoded dict and cannot see it; `dup-header-ci` sends only `A`/`a`.
- Under the strong (raw JSON text) reading, the gate admits four non-conforming positives. Under the decoded-object reading, the contract does not decide it. Either way the case is UNCOVERED and is not disclosed in the lesson or the entry.

### F6 LOW–MEDIUM — the `raw-control` advisory contradicts text the contract actually decides
- Contract worked example 5: "the JSON input in example 5 carries them raw", with key `x%1Fb%1Ey`. The gate sends example 5 escaped (`worked-5`), and its advisory `raw-control` expects REFUSE.
- A contract-literal candidate (`mine.py`, `json.loads(strict=False)`) is therefore reported as `outside-contract-gaps=raw-control,nul-in-value`. `mine_strictjson.py` is reported with `nul-in-value` only.
- The contract contradicts itself: its Input clause and RFC 8259 §7 make raw controls "not JSON". The lesson discloses the conflict (Mistake 6, R90-3).
- Still, the decision table's line "Advisory cases: inputs the contract does not decide" is false for `raw-control`: the contract decides it, both ways. All four positives fail the literal example 5 (`cache_key.py` gives `invalid_input: input is not valid JSON`).

### F7 LOW — false or loose statements in `corpus/knowledge/cache-key-conformance-gate.md`
- (a) "Sandbox … no process" and "Delegating to the counter's reference … sandbox (exit 97, uncatchable)" are false (F1).
- (b) "Python's UTF-8 mode decodes stdin with `surrogateescape`, so the `UnicodeDecodeError` branch is unreachable" is false (F4).
- (c) "Advisory … inputs the contract does not decide" is false for `raw-control` (F6).
- (d) Error-pattern row "Crashing on malformed JSON … caught by `malformed-json`, `empty-input`": at the carrier the observed mechanism is the sandbox false positive (F2). The cases would still fail on behaviour without it, but the receipt reads `sandbox=violation`.
- (e) The RFC 9110 quote is cited at "lines 1606–1609" but sits on lines 1606–1607, as the lesson says. Cosmetic.
- Verified true:
  - the RFC 9111 line-251 quote and the RFC 8259 lines 485–486 quote;
  - the retained body sha256 values (all three match);
  - "Hand cases (70)";
  - the expected checklist lines for `cache_key.py`;
  - the round-89 instrument's false admits on stubs (`scoring-receipt.txt`, 7 `cand_met=true`).

## Reference check (F-REF): `reference()` agrees with the contract
- I wrote an independent implementation from the contract text only: `ReviewGate/mine.py`, with ASCII-only lowercasing, explicit token set and `strip(" \t")`.
- Command: `python3 -B compare.py` (`ReviewGate/compare.txt`). Results:
  - **58 constructed inputs**, each labelled and covering every clause and edge I could build (ows-only vary, comma-only, sort order of `0 _ a ~`, Kelvin sign U+212A in names and members, NBSP, VT/FF, NUL kept, CR in URI accepted, bool/object/list values, top-level null/number/list, extra keys, absent vs empty in both positions, `%`-names present and absent): 0 disagreements.
  - Wide fuzz: 20,000 inputs, seed 90, with an alphabet including CR/LF/NUL/non-token names: 0 disagreements.
  - The gate's own `gen_case` at seed 923161196, n=2000: 0 disagreements.
- `mine.py` scored by the gate: `clauses=6/6 hand=70/70 generated=120/120 met=true`, exit 0.
- Limit: the comparison runs on decoded objects. Raw-text issues (F5, F6, encoding) are outside `reference()`'s reach by construction.

## Clause-by-clause coverage (contract sentence → deciding hand cases)
| Contract sentence | Hand cases | Status |
|---|---|---|
| Input: one JSON object on stdin | array, string, malformed-json, empty-input | covered; encoding not decided (advisory utf8-required) |
| `vary` absent ≡ `""` | vary-absent, vary-empty | covered |
| Output success protocol | judge on every key case | covered, but stricter than the contract (F3) |
| Output refusal protocol | judge on every REFUSE case | covered; `<reason>` not checked (F3) |
| Exactly three ingredients (unnominated headers ignored) | vary-absent, vary-empty (header present, key = URI) | covered |
| 1 split on `,` | worked-3, tab-trim, three-pairs | covered |
| 1 trim SP/HTAB only | tab-trim, worked-3; lf-not-ows, vt-not-ows | covered |
| 1 member must be a token | inner-space, non-ascii, lf-not-ows, vt-not-ows; star-in-token (positive) | covered |
| 1 case-insensitive compare and sort | sort-lowered-a-B, sort-lowered-B-a, sort-lowered-Zb | covered |
| 1 duplicate member refused | dup-member-case, dup-member-exact | covered |
| 2 name lowercased, ASCII A–Z only | member-name-lowered | "ASCII only" cannot be observed (names must be tokens; M33 casefold is equivalent) |
| 2 case-insensitive lookup | lookup-ci, worked-3 | covered |
| 2 header names differing only in case refused | dup-header-ci, dup-header-unnominated | covered; exact duplicates UNCOVERED (F5) |
| 3 value trim SP/HTAB, otherwise byte-exact | edge-ows, all-ows-is-empty, vt-kept, nbsp-kept, case-kept, inner-ws-kept | covered |
| 4 `%`→`%25` in URI, names, values | uri-percent, name-percent-present, name-percent-absent, worked-4, value-percent-escape-literal | covered |
| 4 four separators → `%1C…%1F` (and escape `%` first) | value-each-sep, uri-seps, uri-seps-with-pair, value-sep-not-ows, worked-5 | covered (separators cannot occur in names) |
| 5 layout, pairs sorted by lowercased name | worked-1…7, three-pairs, uri-seps-with-pair, sort-* | covered |
| 5 no member → `ESC(uri)` alone | worked-1, vary-empty, vary-absent, uri-percent | covered |
| absent → GS; present-empty → empty; the two differ | worked-6, worked-7, present-empty, absent | covered |
| R: not object; `uri` missing or not a string | array, string, malformed-json, empty-input, uri-missing, uri-number, uri-null | covered |
| R: `request_headers` missing or not an object | headers-missing, headers-missing-vary, headers-list, headers-null | covered |
| R: header name not a string / empty / not a token | name-empty, name-not-token ("not a string" cannot occur in JSON) | covered |
| R: value not a string / CR / LF | value-number, value-null, cr-only, lf-only, cr-unnominated, lf-unnominated-novary | covered |
| R: `vary` not a string | vary-number, vary-null, vary-list | covered |
| R: `*` member | wildcard, wildcard-listed, wildcard-ows | covered |
| R: empty after trim, or not a token | trailing-comma, leading-comma, only-ows, inner-space | covered |
| R: duplicate members / duplicate header names | dup-member-*, dup-header-* | covered except exact duplicates (F5) |
| Worked examples 1–7 | worked-1…7 + self_check | 1–4, 6, 7 covered; literal ex. 5 (raw) UNCOVERED, advisory expects the opposite (F6) |
| Scope | — | not behavioural |
| Candidate rules (no counter import, no `.ufo/waves` reads, no table) | sandbox + seeded generated cases | table rule covered; import/read rule forgeable (F1) |

## Was moving non-UTF-8 to the advisory line legitimate? (lesson Mistakes 5)
- **For legitimacy:**
  - The contract never names bytes or an encoding.
  - RFC 8259 §8.1's UTF-8 MUST applies to "systems that are not part of a closed ecosystem", and a lane stdin/stdout adapter is arguably a closed ecosystem.
  - The refusal "input is not a JSON object" can be read either way, so a scored clause would have added a rule.
  - The move was disclosed before the carrier, routed as R90-1, not hidden, and the counter, predicate, pins and labels were not changed.
- **For weakening:**
  - It was decided after seeing all four frozen positives fail. That is a gate fitted to the labels.
  - The natural reading of "one JSON object" plus the RFC definition of JSON text points to refusal.
  - The positives' accepting output (a key containing `\udcff`) is not a meaningful key.
- **Verdict: a legitimate reading reached with a wrong diagnosis. It was not a weakening that was needed to admit the positives.**
  - The failure was caused by the gate's own `LC_ALL=C.UTF-8` environment (F4). Under `en_US.UTF-8` the positives already refuse `\xff`.
  - A gate with a strict stdin locale could have kept the case scored and still admitted 4/4.
  - Two residual defects remain:
    1. The positives' conformance on this input depends on the locale.
    2. The disclosed mechanism, "UTF-8 mode / unreachable", is false and should be corrected.

## Residual risk and verification gaps
- I did not re-run `c90_gate.py` over all 61 subjects. I did reproduce `cache_key.py` at seed 923161196 (`met=true`, matching the carrier line in `forge-run.txt`) and read the per-subject lines in `controls/after-c2-carrier.txt`.
- Other sandbox routes I reasoned about but did not test: `os.open(dir_fd=…)`, `sqlite3.connect`, and reads via `zipimport`. File-existence leaks via `os.stat` are allowed by design.
- A candidate could detect the gate (cwd `ckc-*/cwd`, `-I -S`, scrubbed env) and behave differently outside it. Behavioural gates have this limit inherently, and the entry does not disclose it.
- Scratch `/fast/scratch/hyaku/kake-r90/ReviewGate/` is deleted before yield. No git mutation was made, and nothing was written outside my two paths.
