# Round 36 w2 — ReviewToolCode seat report

Seat: KakeR36.ReviewToolCode. Axes: **freshness** (is C1's tool what the contract says) and
**operability** (usage/exit/output behavior). Attack: line-by-line review of
`scripts/source_recheck.py` at build commit 4d5b3d5 against the C1 contract
(SCORECARD.md:1599-1624), hunting case-specific code, extra file reads, network, env,
subprocess. Verdict: **contract-faithful; no case-specific code; one low finding.**

## Provenance and commands (all exit 0)

- Sandbox clone at f3a38bf: `git clone -q <lane> /fast/scratch/hyaku/kake-r36w2/ReviewToolCode/clone && git checkout -q f3a38bf`.
- `git diff 4d5b3d5 f3a38bf -- scripts/source_recheck.py | wc -l` → `0`; landed file byte-identical
  to the build commit; sha256 `577b2d7d028964e06152f5a7b792141e586045eaa8ec9262ee7f416ba5510d48`
  (matches SCORECARD "measured results" and w1/ExecToolBuild.md).
- Case-specificity scan: extracted all 436 strings from `.ufo/waves/round-36/sealed/cases.json`
  (revealed key v2) and substring-tested each against the tool source. Overlaps: 32, all generic
  contract vocabulary (`reason`, `gone`, `text/html`, field names, verdict words). **0 case ids,
  0 body file names, 0 URLs, 0 quotes, 0 hex literals ≥16** in the tool.
- IO-surface grep: imports only `json os re sys unicodedata html.unescape` (L27-32). File opens
  exactly two, both `'rb'`: manifest L538, body L513. Only output: stdout L577, usage stderr L611.
  No `environ|getenv|subprocess|popen|socket|urllib|http.client|requests|system|spawn|exec`,
  no write-mode opens, no makedirs/remove/rename/chmod/listdir. Docstring claim L6-8 matches code.

## Sentence → lines (script lines = `scripts/source_recheck.py`)

| Contract sentence | Implementing lines | Note |
|---|---|---|
| usage `--manifest PATH`; one JSON report; exit 0/1/2/64 | L10-16, parse_args L585-605, main L608-627, emit L570-582 | P7/P8: dup flag & no args → 64, stdout empty; G16 → 0 |
| finding shape `{check,reason,target}` | finding L374-375; target set only for `moved` L498-499 | |
| manifest UTF-8 JSON, version 1, checks list | load_manifest L535-558 (decode L543, version L552-554, checks L555-557) | G12: BOM → input_invalid (open pt 7) |
| check object: id/url/quote/hops rules | validate_check L418-469 (id L422-424, url L425-431, quote L433-435, hops L436-438) | |
| status int 100-599, bool rejected | L443-447 | P1: `true` → check_invalid; P14a/b: 600/99 → check_invalid |
| redirect hop needs location; all but last redirect; last not redirect | L448-461 | |
| 200 ⇒ contentType+body (relative, regular file, inside dir) | L462-468, body_path L393-407 | P5 abs, P6 `../` → check_invalid; F4 symlink (finding F1) |
| (a) last hop decides; 404/410 gone; else http_error; no quote unless 200 | evaluate_check L502-532 (gone L528-529, http_error L530-531); body opened only in 200 branch L513 | P15: moved+gone both present |
| (b) 301/308 permanent, 302/303/307 temporary; RFC 3986 §5.2 resolution, no further normalization | sets L36-37; moved_target L477-490; resolve_reference L159-180 (§5.2.2 branches L167-179, dot-segments L98-131, merge L134-141) | P9a strict `g:h`→`g:h`; P9b `g`→`/a/g`; P9c `../c`→`/c`; F9e 302-first → no moved |
| (b) moved target = last hop of leading permanent run; in addition to final status | L480-484 (run scan), L486-489 (chain), L496-499 (both) | P15 ✓ |
| (b) no fragment inheritance | base fragment discarded L162 parse `_`, reference fragment kept L180 | |
| (c) comments→raw elements→tags→references; title kept | html_text L341-346; remove_comments L278-292; remove_raw_elements L294-313 (regexes L271-275); strip_tags L315-339; unescape L346 | P10 unterminated comment → quote_missing; P11 uppercase tags/type → clean |
| (d) NFKC then isspace deleted; substring; case-sensitive | normalize L361-368 (table L356-358); match L525-526 | |
| (e) media type before `;`, trimmed, ASCII-case-insensitive; params case-insensitive | parse_content_type L378-390; branch L504-510 | |
| (e) text/plain raw, no HTML processing; else unsupported_type, no quote check | mode plain skips html_text L523-524; unsupported early return L508-510 | |
| (f) BOM wins over charset, mark dropped | BOMS L241-244; pick_encoding L252-254 | |
| (f) charset trimmed, dequoted, ASCII-case-insensitive label; 4 encoding families; else charset_unsupported | L255-263; table L202-238 (latin1/ascii/us-ascii→cp1252 present) | G3b: 0x81 under `us-ascii` → U+FFFD, clean |
| (f) no BOM no charset → UTF-8; invalid bytes → U+FFFD | L255-256; decode errors="replace" L522 | |
| (g) input_invalid cases, check null, nothing evaluated | main L613-615 + load_manifest None paths | G12 ✓ |
| (g) check_invalid per rule; id when non-empty string; others still evaluated | L620-622, check_id_of L410-415 | P1/P5/P6/P13/P14 ✓ |
| (g) checksEvaluated = non-check_invalid | main L618/L621 → emit L574 | |
| verdict rule: blocking→could-not-evaluate; else findings→failed-policy; else clean | BLOCKING_REASONS L52; decide_verdict L561-567; exit map L578-582 | G16 clean→0 |

## Findings

- **F1 (low, advisory)** — `body_path` L393-407 enforces containment lexically (normpath +
  prefix, L399-402) and accepts the body via `os.path.isfile` (L404-406), which follows symlinks.
  A body name inside the manifest dir that symlinks **outside** it is accepted and read (L513).
  Observed: F4 probe — manifest dir with `esc.txt` → outside file containing `OUTSIDE-MARK`,
  quote `OUTSIDE-MARK` → exit 0 clean; the tool read a file outside the manifest directory.
  Contract says "a relative path to a regular file inside the manifest's directory" — the *path*
  is inside and isfile() calls it a regular file, so this is a defensible reading (builder's open
  point 8 declares it), and real exposure is nil: the counter writes the manifest itself with
  fresh random names and jails the tool in bwrap (SCORECARD counter v2 note), and the tool has no
  write/network sink. A readlink-resolved containment check would be stricter.
- **F2 (info)** — `--manifest --manifest` consumes the flag as the value (parse_args L591-595) →
  exit 2 input_invalid, not 64. Contract fixes only the documented invocation; all judge-relevant
  usage errors (missing trailing value, extra positional, duplicate flag, empty `--manifest=`)
  correctly exit 64 with empty stdout (P7/P8/G17).
- **F3 (info)** — BOM'd manifest → `input_invalid` (strict UTF-8 decode L543). RFC 8259 lets an
  implementation ignore a BOM; the contract's "(UTF-8 JSON)" doesn't decide. Consistent with the
  reference (28/28), documented open point 7.
- **F4 (info)** — windows-1252 via Python `cp1252` + errors="replace" (L522) sends the 5 bytes
  WHATWG defines as C1 controls (0x81 8D 8F 90 9D) to U+FFFD. The contract's own sentence "bytes
  invalid in the chosen encoding decode to U+FFFD" supports the tool's reading; divergence is
  confined to those bytes; open point 4.
- **F5 (info)** — `version` 1.0 accepted (L553 `version != 1` numeric compare; F2 probe → clean
  exit 0). "Other than 1" is satisfied numerically; documented open point 7.

## Case-specific code: none found

The scan above is the attack the claim most needs to survive (counter randomizes ids/body names
per run — SCORECARD:1594-1597): the tool contains no id, body-name, URL, quote, label or hash
literal from the revealed key, and its only constants are the contract's own vocabulary (L36-52,
L202-244). Logic reads ids solely to echo them in findings (L410-415, L496).

## Builder open points judged against source

1. RFC §5.2 strict — contract bullet (b) names §5.2 verbatim; L167-179; P9a-d pass. **Sound.**
2. moved = last hop of leading permanent run — contract sentence verbatim; L480-490. **Sound.**
3. media-type before charset — bullet (e) says unsupported type → "no quote check", and (f) rules
   only gate the quote check; early return L508-510 is consistent. **Sound.**
4. cp1252 replace — see F4. **Defensible, contract-literal.**
5. Unterminated comment/raw element runs to end; tag without `>` kept as text — contract text is
   "up to the next `>`" which is undefined when none exists; L285-291, L306-311, L331-334;
   linear-time under hostile input. **Defensible.**
6. location rules (both directions enforced; last-hop location string-or-null, unread) — matches
   the manifest paragraph read as a whole; L448-461. **Sound.**
7. version 1.0 ok, BOM manifest rejected — see F3/F5. **Defensible, documented.**
8. lexical containment, symlinks followed — see F1. **Defensible; strictest open point.**
9. checksEvaluated semantics — contract (g) last sentence; L618/L621. **Sound.**

## Not verified (outside this seat)

- The sealed counter run itself (28/28 receipts) and the control/ablation receipts — RerunC1Sealed
  / RerunControls own reruns; I did not execute `sealed_count.py` nor the 28 cases.
- RFC 3986 §5.4.1's 23 normal examples were validated by the builder, not re-run by me; I probed
  resolution with 5 fixtures of my own (all pass, P9a-c, F9e, plus §5.4.1's `g:h` behavior).
- Performance/DoS claims (builder's 5 MB timings) not re-measured; code inspection shows linear
  `str.find`/regex loops (L278-339), no quadratic scans.
- Tooling installed: none.
