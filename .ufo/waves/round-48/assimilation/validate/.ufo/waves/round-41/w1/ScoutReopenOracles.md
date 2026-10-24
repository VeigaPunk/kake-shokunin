# ScoutReopenOracles — planned rows S118 (abnf 2.9.1), S119 (rfc3987 1.3.8)

Axes: freshness (judged), operability (named GETs completed). No tools installed. No counter run (this seat does not score a tool).

## Commands (exit 0)

- `sha256sum .ufo/waves/round-41/oracle/*.whl`
- `curl -fsSL` GET `https://pypi.org/pypi/abnf/2.9.1/json` → HTTP 200, 8215 bytes
- `curl -fsSL` GET `https://pypi.org/pypi/rfc3987/1.3.8/json` → HTTP 200, 9900 bytes
- `curl -sS -L` GET `https://github.com/declaresub/abnf` → HTTP 200, redirect_url empty

## Digests — both equal

| package | local `sha256sum` | PyPI `digests.sha256` | size |
|---|---|---|---|
| `abnf-2.9.1-py3-none-any.whl` | `cdcac127b3693ded2b00565878d8ed2b96d34b29f0ee199c06d7b40baaf60917` | same | 78103 |
| `rfc3987-1.3.8-py2.py3-none-any.whl` | `10702b1e51e5658843460b189b185c0366d2cf4cff716f13111b0ea9fd2dce53` | same | 13377 |

Lane copies `.ufo/waves/round-41/sources/pypi-abnf.json` (`d1dab17e…d10d`) and `pypi-rfc3987.json` (`f624f451…8d2e`) are byte-identical to these GETs. `sources/fetched-at.txt:1` is `2026-10-23T09:39:11Z`. Neither release is yanked.

## S118 abnf 2.9.1

- summary: "Parsers for ABNF grammars."
- author: JSON `author` is null; `author_email` `Charles Yeomans <charles@declaresub.com>`
- license: `license` and `license_expression` empty; classifier `License :: OSI Approved :: MIT License`; `license_files` `["LICENSE.txt"]`; `requires_python` `>=3.10`
- upload: wheel `2026-10-21T19:34:52.901979Z`; sdist `2026-10-21T19:34:54.472236Z` (sdist sha256 `58dfcbec…9c06`, not vendored)
- project URLs: Homepage/Source `https://github.com/declaresub/abnf`; Documentation `https://abnf.readthedocs.io/`; Changelog `…/blob/master/CHANGELOG.md`; Issues `…/issues`; `project_url` `https://pypi.org/project/abnf/`
- GitHub README (same sentence as PyPI `description` line 12): "It ships with 30+ ready-to-use grammar modules for common RFCs". Line that names them (description line 67): "the public API, the built-in core rules, the bundled grammars, and configuration knobs." The README does not name `rfc3986` in those lines.

## S119 rfc3987 1.3.8

- summary: "Parsing and validation of URIs (RFC 3986) and IRIs (RFC 3987)"
- author: `Daniel Gerber`; `author_email` `daniel.g.gerber@gmail.com`
- license: `GNU GPLv3+`; classifier `License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)`
- upload: wheel `2018-07-29T17:23:45.313143Z`; sdist `2018-07-29T17:23:47.954044Z` (sdist sha256 `d3c4d257…a733`, not vendored). Pin is stable, not a recent publish.
- project URLs: Homepage `http://pypi.python.org/pypi/rfc3987`; Download `https://github.com/dgerber/rfc3987`; `project_url` `https://pypi.org/project/rfc3987/`

## Checked statements

- `SCORECARD.md:2705-2706` abnf wheel `cdcac127…0917` = PyPI digest (S118) — **holds** (full digest above).
- `SCORECARD.md:2710-2711` rfc3987 wheel `10702b1e…ce53` = PyPI digest (S119) — **holds**.
- `c1_count.py:41` `ORACLE_SHA256` equals the file and PyPI — **holds**.
- `oracle_crosscheck.py:15` `SECOND_SHA256` equals the file and PyPI — **holds**.
- Calling the abnf *package* an RFC 3986 parser — **overstated** if read off the summary alone ("Parsers for ABNF grammars."). SCORECARD's narrower cite `abnf.grammars.rfc3986` is not checked here.

Unknown: rule-by-rule equality of `abnf/grammars/rfc3986.py` with RFC 3986 Appendix A (sibling ReviewOracleFidelity). The "30+" modules are not listed on the README lines above.
