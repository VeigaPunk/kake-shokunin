# Round 37 W1 — ExecRobotsTool (C1 build)

DISCLOSURE: while checking the boundary I ran `test -e /fast/scratch/hyaku/kake-r37/`,
a stat of the sealed directory itself only. Nothing under it was listed, read,
stat'ed, searched or opened; the C1 counter was not run (no key).

Built C1's tool to the round-37 C1 contract. No lane file was written except this report; no installs needed.

## Deliverables (sandbox; L1 copies after review)
- /fast/scratch/hyaku/kake-r37w1/ExecRobotsTool/robots_audit.py — 578 lines,
  sha256 5eb767ec68a649145102619ed13754428bef489e432ed50eb20e9e50542cabae,
  stdlib only (json, os, re, stat, sys, urllib.parse); no urllib.robotparser.
- /fast/scratch/hyaku/kake-r37w1/ExecRobotsTool/robots_audit.patch — 584 lines,
  new file mode 100755, against 4b089da699cfaaf5ebeb6a0746b7e4238602e20a,
  sha256 72befdae0e47951752bf6eeeb047aba079ddd5954b227c0f49cc28b1f87564b2.
- Scaffolding: cases/ (15 manifests + 14 (g) runs, expected.json), make_cases.py,
  run_cases.py, run_cases.log, usage.log, perf/, clone/, applycheck/.
## Behavior
Usage is exactly `--manifest PATH`; any other argument list prints one stderr
line and exits 64. The manifest is stat'ed before opening (FIFO/device =>
input_invalid, never opened), size-checked at 64 MiB inclusive, decoded strict
UTF-8, parsed as JSON. Report: {"version":1,"verdict":V,"checksEvaluated":N,
"findings":[{"check":id|null,"reason":R}]}; exit 0/1/2 for clean/failed-policy/
could-not-evaluate. (a) 2xx parses, 4xx allows, 5xx disallows incl. /robots.txt;
(b) 512000 bytes, BOM drop, U+FFFD replace, CR/LF/CRLF, first-# comment,
space/tab trim, ASCII key case, orphan rules ignored, other keys never end a
group; (c) group start/continuation over blank/comment/ignored lines, exact
ASCII case-insensitive token match, matching groups merged, * only if none
matched, empty matching group suppresses *; (d) empty value never matches, * any
run, trailing $ anchors, prefix match, longest normalized octets, allow on tie;
(e) path+query, no fragment, raw /robots.txt implicit allow, non-ASCII UTF-8
%-encoding, unreserved escapes decoded, other escapes uppercased, reserved kept
(%2F != /); (f) one check_invalid per faulty check (id when non-empty str),
other checks still evaluated; (g) one input_invalid, nothing evaluated; verdict
precedence as declared.
## Open-point choices (contract silent; S011-closest reading)
1. Manifest stat follows symlinks (symlink-to-regular is regular); FIFO/device is
   input_invalid and never opened, so it cannot block.
2. Manifest directory = dirname(realpath(manifest)); 64 MiB is inclusive.
3. A UTF-8 BOM on the manifest is input_invalid (strict JSON on decoded text);
   BOM removal is granted only to the robots file.
4. Product token = [A-Za-z_-]+ (RFC 2.2.1 ABNF): digits and * rejected; a lone
   "-" or "_" accepted.
5. URL validity = scheme http/https (urlsplit lowercases) + non-empty hostname;
   port, userinfo and host syntax beyond non-emptiness are not judged.
6. Implicit /robots.txt allow compares the raw path-to-match before
   normalization, so /robots.txt?x=1 and /robots%2Etxt are rule-decided.
7. A robots file that passed validation but cannot be opened is check_invalid.
8. A matching group with no rules still suppresses the * fallback.
9. Lone surrogates (JSON \uD800) percent-encode via surrogatepass; no crash.
10. Ids compare case-sensitively; an earlier id counts even when that check is
    otherwise invalid; check_invalid uses the id when it is a non-empty string.
11. Extra top-level manifest fields are allowed. Values/keys trim only spaces and
    tabs, not str.strip().
## Evidence (all run in the sandbox; logs retained)
$ python3 robots_audit.py --manifest cases/m08.json
{"version":1,"verdict":"failed-policy","checksEvaluated":10,"findings":[{"check":"i1","reason":"blocked"},{"check":"i3","reason":"blocked"},{"check":"i5","reason":"exposed"},{"check":"i8","reason":"blocked"},{"check":"i10","reason":"exposed"}]}
exit=1
$ python3 run_cases.py -> 29/29 cases passed, exit=0. Coverage: m01,m02 (a);
  m03,m04,m05 (b); m06,m07 (c); m08 (d); m09,m10,m10b,m14 (e); m11,m12 (f);
  g01..g15 (g); usage.log (usage errors).
$ usage: no args / --manifest alone / --manifest M extra / --manifest=M / --help -> stderr usage line each, exits 64 64 64 64 64.
$ bwrap --unshare-all --ro-bind /usr /usr --ro-bind <sandbox> /work --proc /proc
  --dev /dev --tmpfs /tmp python3 /work/robots_audit.py --manifest <m>: m08
  exit=1 (same findings); FIFO manifest exit=2 input_invalid, no block;
  exactly-64-MiB manifest exit=0 clean.
$ bash time: 50k plain rules + 200 checks 0.43s; 42k wildcard rules + 200 checks 0.85s;
  64 MiB manifest with 550000 404 checks 1.50s; exact 64 MiB, one check 0.08s.
$ git -C applycheck apply --check ../robots_audit.patch -> exit 0; after apply sha256
  equals 5eb767ec...; applied tool on cases/m08.json exit=1, same findings.

Not verified: the sealed counter and reference behavior (no key); the C1 predicate
is the L1's to run at the integration commit.
## Risks
- Highest: the silent readings the sealed cases could pin against me — the raw
  /robots.txt comparison (6) and BOM manifest as input_invalid (3).
- Robots-file unreadability (7) is not in the contract fault list; that behavior is
  a choice, not measured against any reference.
- URL validity beyond scheme+host (5) follows only the contract parenthetical.
