# ReopenS118Fresh — row S118 (abnf 2.9.1)

Axes: freshness. No tools installed. No wheel re-download (the named check is the PyPI JSON digest vs local `sha256sum`).

## Commands (exit codes)

- `curl -fsSL -D headers.txt -o pypi-abnf-2.9.1.json -w http:%{http_code} https://pypi.org/pypi/abnf/2.9.1/json` — exit 0; `HTTP/2 200`; `date: Fri, 23 Oct 2026 10:08:52 GMT`; `x-pypi-last-serial: 42558633`; body sha256 `d1dab17e48793e9e3921679ef8e2672b2a71557c024482b931eef4d934a6d10d`.
- `cmp` that body vs `.ufo/waves/round-41/sources/pypi-abnf.json` — exit 0 (byte-equal). `sources/fetched-at.txt` is `2026-10-23T09:39:11Z`.
- `sha256sum .ufo/waves/round-41/oracle/abnf-2.9.1-py3-none-any.whl` — exit 0; `cdcac127b3693ded2b00565878d8ed2b96d34b29f0ee199c06d7b40baaf60917`.
- Zip member `abnf/grammars/rfc3986.py` present. `prlimit --as=4000000000 python3` import of that wheel: `rfc3986.Rule("URI").parse_all("https://example.com/a?b=1#c")` returns node `URI`; leftover and space hosts raise `ParseError` — exit 0.

## Clauses (`corpus/SOURCES.md:126`)

- `info.summary` "Parsers for ABNF grammars." — **holds** (live JSON, period included).
- README "validate a whole string against a rule (raises ParseError otherwise)" — **holds** as a verbatim substring of `info.description` (a `#` comment in the Quick start fence, not a prose sentence). The row does not call it a sentence.
- `urls[]` wheel `abnf-2.9.1-py3-none-any.whl` sha256 `cdcac127…0917` — **holds**. Same digest as the local file, `c1_count.py:41` `ORACLE_SHA256`, and SCORECARD.md:2705-2706 (`cdcac127…0917` = the PyPI digest). File size 78103, upload `2026-10-21T19:34:52.901979Z`, `yanked: false`. Owner `declaresub`.
- fetched `2026-10-23T09:39:11Z`, HTTP 200, retained JSON sha256 `d1dab17e…d10d` — **holds**. Today's GET is still those bytes.
- Wheel contains `abnf/grammars/rfc3986.py` — **holds** (module docstring: collected rules from RFC 3986 Appendix A).
- Teaches, byte-equal to the wheel PyPI publishes — **holds** (published sha256 equals `sha256sum`; the wheel bytes were not fetched again).
- Teaches, `abnf.grammars.rfc3986.Rule("URI").parse_all` accepts a whole string or raises `ParseError` — **holds**. Method is inherited (`abnf/_parser_python.py` `Rule.parse_all`: return the node, or `ParseError` if the source is not fully consumed). Docstring also names `GrammarError` when a rule is undefined; `URI` is defined, and the two probes raised `ParseError` only.
- Teaches, "which the counter reads as valid or invalid" — **overstated** (low). `c1_count.py:82-85` maps `ParseError` to invalid, but a returned node is still invalid unless the scheme is `http`/`https` and an authority has a non-empty host (`c1_count.py:86-93`). Parse success is not the counter's valid.

No wrong clause. Freshness of the quoted summary, README fragment, digest, and grammar member holds as of 2026-10-23T10:08:52Z.
