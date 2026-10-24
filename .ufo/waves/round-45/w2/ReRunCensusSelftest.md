# ReRunCensusSelftest

Axes: operability, freshness.

## Attack

Re-ran the kake registry validator and round-45 audit selftest; counted the current registered source rows. No tree mutations beyond this report; no tools installed.

## Commands and decisive output

Exact commands run:

```sh
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake
python3 -B .ufo/waves/round-45/c45_audit.py --selftest
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin kake
```

The validation and selftest were also run with shell wrappers that printed their return statuses. Validation output:

```text
kake	W04	S033 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across scopes
kake	W04	S088 duplicate url www.rfc-editor.org/rfc/rfc9110.html across scopes
kake	W04	S092 duplicate url html.spec.whatwg.org/multipage/syntax.html across scopes
kake	W04	S098 duplicate url www.rfc-editor.org/rfc/rfc3986.txt across scopes
kake	W04	S099 duplicate url www.rfc-editor.org/rfc/rfc9309.html across scopes
kake	W04	S102 duplicate url www.sitemaps.org/protocol.html across scopes
kake	W04	S110 duplicate url www.w3.org/TR/xml across scopes
kake	W04	S111 duplicate url docs.python.org/3/library/urllib.parse.html across scopes
kake	W04	S115 duplicate url docs.python.org/3/library/urllib.parse.html across scopes
kake	W04	S116 duplicate url docs.python.org/3/library/urllib.parse.html across scopes
kake	W04	S117 duplicate url www.rfc-editor.org/rfc/rfc3986.txt across scopes
kake	W04	S127 duplicate url www.rfc-editor.org/rfc/rfc9844.txt across scopes
kake	ok	/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md
exit_status=0
```

Selftest output:

```text
SELFTEST PASS: v1 assertions plus timing-only, invalid receipt, error-row, build-count gates, and the end-to-end fixture cohort
exit_status=0
```

Census output (row count: 134):

```text
kake	rows	134
kake	tier.A	111
kake	tier.B	6
kake	tier.C	17
kake	status.mined	104
kake	status.queued	8
kake	status.rejected	22
FLEET	rows	134
FLEET	tier.A	111
FLEET	tier.B	6
FLEET	tier.C	17
FLEET	tier.invalid	0
FLEET	status.queued	8
FLEET	status.mined	104
FLEET	status.rejected	22
FLEET	status.invalid	0
FLEET	missing	0
exit_status=0
```

## Verdict

- **Registry conformance: PASS** — validation exited 0 and emitted no E-class rows. It reported 12 W04 duplicate-URL-across-scopes warnings; these are warnings, not conformance errors. Census reports 134 rows.
- **c45 audit selftest: PASS** — selftest exited 0.

Risk: the 12 reported W04 duplicate-URL warnings remain present in the registry. No blocker.

File written: `.ufo/waves/round-45/w2/ReRunCensusSelftest.md`.
