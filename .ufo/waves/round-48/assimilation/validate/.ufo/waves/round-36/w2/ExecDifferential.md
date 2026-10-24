# ExecDifferential — C1 differential test (lane round 36, wave 2)

Attacked: `scripts/source_recheck.py` (sha256 `577b2d7d…0d48`) against the independent
implementation `retained/independent/selftest-seat-reference.py` (sha256 `a5176fee…221f`),
plus the now-public private oracle `sealed/ref.py` (sha256 `665e8798…5298`) as tiebreaker.
Both lane files are byte-identical in the lane and in my clone at `f3a38bf`.

## What I ran (all exit 0 unless stated; sandbox `/fast/scratch/hyaku/kake-r36w2/ExecDifferential/`)

| command | result |
|---|---|
| `python3 -B diffgen.py 20261022 2000` | `cases=2000 disagreements=535 crashes=0` (broad generator: status mixes, 1-4 hop chains, relative/absolute/dot-segment/scheme-relative locations, HTML comments/script/style/template/entities/tags, NFKC + whitespace variants, 15 media types, BOMs, 36 charset labels, 37 malformed-check mutations, 12 manifest faults) |
| `python3 -B harness.py 777001 2000 compat` | `phase=compat cases=2000 disagreements=311`, `isolated disagreeing checks=330` (compat generator: inputs both tools accept, to expose semantic rather than validation divergence) |
| `python3 -B counts.py` | 4000 manifests, 2295 isolated disagreeing checks attributed to 8 causes (below) |
| `python3 -B frag.py` | 10 single-fragment HTML divergences: unterminated comment / unterminated script / unterminated style / unterminated template |
| `python3 -B oracle_probe.py` | 13 class probes through the public oracle `sealed/ref.py` |
| symlink in-place sweep (`work/m*/link.bin`) | 11 of 35 generated manifests containing a symlink-escape body diverge |

Bodies were generated, not fetched; both tools were invoked through their real `main(["--manifest", p])`;
all 12 reproducers were re-run through the CLI of all three implementations. No crashes in 4000 manifests.

## Disagreements (tool vs independent reference), counts per sweep

| class | broad | compat | reproducer | decider (SCORECARD.md) | tool / indep / oracle |
|---|---|---|---|---|---|
| charset label table | 35 | 211 | `reproducers/C1_charset_label_utf8` (`text/plain; charset=utf8`) | (f) 1639-1643: "picks the encoding by the WHATWG Encoding label table; the tool supports the labels of UTF-8, UTF-16BE, UTF-16LE and windows-1252" — `utf8`, `utf-16`, `unicode`, `cp1252`, `x-cp1252`, `iso8859-1`, `csisolatin1`, `l1`, `cp819`, `ibm819`, `iso-ir-100`, `iso_8859-1`, `ucs-2`, `iso-10646-ucs-2`, `unicodefeff`, `unicode11utf8`, `unicode20utf8` are labels of those encodings | clean / charset_unsupported / clean |
| URL scheme case | 466 | 0 | `C2_url_uppercase_scheme` (`url: HTTP://example.com/x`) | manifest rule 1606 "absolute URL, scheme `http` or `https`" with RFC 3986 §3.1 (S089): schemes are case-insensitive | clean / check_invalid / clean |
| moved target, scheme case | 24 | 68 | `C5_moved_target_scheme_case` (`location: HTTP://Upper.example/x`) | (b) 1617-1618 "RFC 3986 section 5.2 … with no further normalization" (urljoin lowercases the scheme) | `HTTP://Upper.example/x` / `http://Upper.example/x` / `http://Upper.example/x` |
| moved target, strict resolution | 0 | 36 | `C6a_moved_target_http_g` (`location: http:g`), `C6b_moved_target_after_mailto` (`mailto:a@b` then `?q=1`) | same sentence; RFC 3986 §5.2.2 strict gives `http:g` and `mailto:a@b?q=1`, urljoin does not | `http:g`, `mailto:a@b?q=1` / `http://example.com/g`, `?q=1` / same as indep |
| HTML text, unterminated | 2 | 15 | `C7a_html_unterminated_comment` (`<!-- unterminated comment`), `C7b_html_unterminated_script` (`<script>var x = 1;`) | (c) 1624-1626: "comments removed (`<!--` to the next `-->`)"; "start tag to the next end tag of the same name" — silent on a missing terminator | quote_missing / clean / quote_missing |
| empty `contentType` | 30 | 0 | `C4_empty_content_type` (`contentType: ""`) | manifest rule 1609-1611 says `contentType` "(string)" (contrast `id`, `quote`: "non-empty string"); (e) 1634-1637 "any other media type: one `unsupported_type`" | unsupported_type / check_invalid / unsupported_type |
| URL with port-only authority | 34 | 0 | `C3_url_port_only_host` (`url: http://:8080/x`) | manifest rule 1606 "non-empty host" (the host of `:8080` is empty) | check_invalid / clean / check_invalid |
| manifest `version: true` | 37 | 0 | `C8_manifest_version_true` (`{"version": true, "checks": []}`) | (g) 1646 "a non-object, `version` other than 1" — JSON `true` is not the number 1; both references accept it only because Python `True == 1` | input_invalid / clean / clean |
| body symlink escaping the manifest dir | 11/35 | — | `C9_symlink_escape` (`body: link.bin`, link → file outside the dir) | (g) 1648-1649 "a body path that is absolute, escapes the manifest directory, or is missing or not a regular file" | **clean (reads the outside file)** / check_invalid / check_invalid |

Tool ↔ oracle only (independent reference agrees with the tool): `C7c_html_endtag_with_attribute`
(`<script>x</script foo>tail`) — tool and indep keep `tail` (clean), oracle drops to EOF
(`quote_missing`); decider (c) 1625 "the next end tag of the same name" is ambiguous for an end tag
with attributes.

## Findings

1. **Tool defect, contract-decided: symlink body escape.** `body_path` textually `normpath`s the
   body string and calls `os.path.isfile`, so a link inside the manifest directory that resolves
   outside passes validation; the tool then reads those bytes. Bullet (g) says such a check is
   `check_invalid`, and both references report it. Reproducer `C9_symlink_escape`; 11 of 35 generated
   instances diverge. This also weakens the "reads only the manifest and the body files it names"
   docstring line for a symlinked body.
2. **Tool ↔ oracle gaps that the 28-case key does not cover.** `moved` targets (scheme case,
   `http:g`, relative ref after a non-hierarchical base), `version: true` and `</script attr>`
   differ between the tool and the L1's own `sealed/ref.py`, yet both score 28/28. The contract text
   favors the tool on moved-target ("no further normalization", RFC 3986 §5.2.2 strict) and on
   `version` (JSON type), so the oracle is the weaker side — but the current "reference 28/28 and
   tool 28/28" evidence does not pin these edges, and a future key that does would fail the tool.
3. **Independent reference is narrower than the contract** on charset labels, URL scheme case,
   empty host, empty `contentType` and unterminated HTML; it also uses `urljoin` instead of RFC 3986
   §5.2 strict. Its 28/28 score therefore does not certify the tool on those rows; it certifies only
   the 28 sampled behaviours.
4. No differential disagreement on media-type parsing: 12 content-type shape variants (spacing,
   duplicate `charset`, quoted label, parameter-with-semicolon, casing, empty label) gave identical
   output in all three implementations.

## Evidence pointers

Sandbox `/fast/scratch/hyaku/kake-r36w2/ExecDifferential/`: `diffgen.py`, `harness.py`, `counts.py`,
`counts.json`, `groups.json`, `per_sweep.json`, `frag_diffs.json`, `html_min.json`,
`oracle_probe.json`, `reproducer_table.json`, `reproducers/<case>/manifest.json` (+ body files).
Lane never written except this report. No tools installed or upgraded.

Not verified: live fetches (offline generator only); commits/PRs/branches; any behaviour outside the
contract bullets I generated (e.g. `hops` entries with extra keys, non-UTF-8 manifest encodings
beyond one probe, path-traversal forms other than `../`); the sealed counter itself was not run.
