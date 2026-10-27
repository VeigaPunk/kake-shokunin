# ScribeCorrectionTail

Responds to claim C3, condition C9 (append-only correction of the stale UA-only sentence in
`corpus/knowledge/crawler-identity.md`). Draft only: nothing in the lane was written except this
report and `.ufo/waves/round-59/w1/ScribeCorrectionTail.files/`; no git/jj mutation, no counter run
(C9 logic replayed with the counter's own constants and helpers, see DIFF CHECK).

Lane facts measured this seat: base `fd6303ce5c14b3f892dec586297a942ab6e4193b`, lane HEAD
`cb685273`; `git diff fd6303ce HEAD -- corpus/knowledge/crawler-identity.md` is empty and the worktree
file is clean (`sha256 2ea606a0…4661`), so base blob == HEAD blob == worktree here.
`git show <base>:corpus/knowledge/crawler-identity.md` line 31 equals the counter's `STALE_LINE`
exactly, once; the stale bullet is base lines 31-34.

## INSERT AFTER LINE 34:

13 inserted lines, no base line changed or deleted. Each S425 quotation is kept on one physical
line (the counter joins inserted lines with `" ".join`, so a quote broken at a non-space would
mismatch). The block is indented 2 columns so it stays inside the existing list item: base line 34
ends the bullet, and the correction reads as a second paragraph of that bullet. No blank line is
inserted, which keeps the list tight (see DIFF CHECK rendering counts); without the indent, or with
a leading blank line, the base list's rendered structure changes while its bytes do not.

```markdown
  **[r59-correction 2026-10-27]** The claim in the bullet above is wrong as stated: a server log
  records the requesting IP address as well as the user-agent, and Google's crawler overview gives
  three identification signals, not one [S425] — the HTTP user-agent request header,
  "The source IP address of the request." and "The reverse DNS hostname of the source IP." Its
  technical-properties section adds that the clients are distributed across many datacenters, so
  "your logs may show visits from several IP addresses" [S425]. What the bullet gets right
  survives: the user-agent header is what separates the Smartphone and Desktop subtypes quoted
  above, so a log line reading Googlebot still does not say which viewport the fetched HTML was
  produced for. What does not survive is the word *only* — verifying a claim to be Googlebot is an
  IP check (reverse DNS, then forward DNS), set out in `googlebot-verification.md` (S426); the
  fuller reading of the three signals, with the datacenter spread, is
  `crawler-identity-signals.md` (S425). The sentence above stays as historical text; this
  correction supersedes it.
```

Asserted: a server log records the requesting IP as well as the user-agent; Google's signals are
user-agent, source IP and reverse DNS; the Smartphone/Desktop point survives, `only` does not;
verification is an IP check routed to `googlebot-verification.md` (S426). Tag
`**[r59-correction 2026-10-27]**` is the first inserted line, 3 base lines after line 31; citations
`[S425]` (three) and `[S426]`; ASCII double quotes only.

Also written to `.ufo/waves/round-59/w1/ScribeCorrectionTail.files/insert.md` (same 13 lines).

## SPAN CHECKS:

Run against the retained body, verbatim output of
`python3 -B .ufo/waves/round-59/span_tools.py check S425 '<span>'`:

```
== The source IP address of the request.
{'units': 7, 'chars': 37, 'in_text_node': True, 'count_in_body': 1, 'unique': True, 'within_ceilings': True}
== The reverse DNS hostname of the source IP.
{'units': 8, 'chars': 42, 'in_text_node': True, 'count_in_body': 1, 'unique': True, 'within_ceilings': True}
== your logs may show visits from several IP addresses
{'units': 9, 'chars': 51, 'in_text_node': True, 'count_in_body': 1, 'unique': True, 'within_ceilings': True}
```

All three pass C5's mask (6..25 units, <=160 characters, inside one collapsed article text node,
page-unique against both retained bodies); two carry the row's page-named subject `IP address`, which
is what C9 requires for at least one. The S425 heading span `Google's crawlers identify themselves in
three ways:` also checks clean (7u/52c, unique) but is not quoted. No curly quote in the block.

## DIFF CHECK:

Applied in scratch (`/fast/scratch/hyaku/kake-r59/ScribeCorrectionTail`, `git clone -q --shared` of
the lane; base blob extracted with `git show <base>:corpus/knowledge/crawler-identity.md`), then
`difflib.SequenceMatcher(a=base_lines, b=patched_lines, autojunk=False).get_opcodes()`:

```
insert lines: 13 | base lines: 73 | patched lines: 86
opcodes: [('equal', 0, 34, 0, 34), ('insert', 34, 34, 34, 47), ('equal', 34, 74, 47, 87)]
delete/replace ops: []
insert-only: True
stale line base index: [30] (1-based line [31] )
op insert base_idx 34 -> 34 within-window: True      # C9: s=30 < 34 <= 30+1+8
tagged lines: 1
cites S425: True
curly: False
C9-qualifying spans (pass C5 mask and carry 'IP address'):
  ['The source IP address of the request.', 'your logs may show visits from several IP addresses']
C9_SIMULATED: pass
```

The replay uses the counter module's own `STALE_LINE`, `STALE_WINDOW`, `CORRECTION_TAG`, `TOPIC`,
`CURLY`, `UNIT_CEILING`, `CHAR_CEILING`, `units()` and `in_content()`, and its `re.sub(r"\s+", " ")`
body collapse, against `sources/S425.html` and `sources/S426.html`; the C9 block was transcribed,
not executed by `c59_quote_truth.py` (C1-C8 need the entries and the registry append, out of this
seat). Full transcript: `.files/c9check.out`.

Rendering side effect, `cmark` over base vs patched:

```
cmark base: p=13 li=8 ul=2
cmark patched(A, no blank line): p=13 li=8 ul=2
cmark variant B (leading blank line): p=18 li=8 ul=2
```

Variant A (delivered) leaves the base rendering structurally identical (correction renders inside
the first `<li>`, no new item); variant B isolates it but turns the list loose, so it was not chosen.
Receipt `.files/render-counts.txt`.

## OTHER OCCURRENCES:

The assignment's grep `grep -rniE 'only thing a (server )?log|user-agent string is the only'` over
`corpus/`, `SKILL.md`, `README.md` returns two hits, one of them the line being corrected:

1. `corpus/knowledge/crawler-identity.md:31` — the stale sentence (corrected by the insert above).
2. `corpus/lessons/round-58-verifier-spotcheck.md:80` — the routed defect D1, verbatim:
   `- **D1 (re-flagged, carried since round 51):** \`corpus/knowledge/crawler-identity.md\` lines ~31–34 "A user-agent string is the only thing a server log records about the crawler" remains unrepaired and now sits beside DNS-verification material the lane itself holds (\`w1/ScoutLaneBaiduspider.md\`). Qualify it (UA+IP are what a log records; verification needs reverse DNS on the IP) or mark corrected in a new entry.`
   A lesson file is a round record, not corpus prose; leave it (append-only rule, and D1 becomes
   historical once the correction lands).

A wider sweep of the same phrase family
(`grep -rniE 'only (thing|record|trace)|log (records|holds|shows) (only|nothing)|ua is the only'`
over `corpus/knowledge`, `SKILL.md`, `README.md`) adds no further hit — only
`crawler-identity.md:31` again. Nothing in `SKILL.md` or `README.md` repeats the UA-only claim.

Premise-dependent text that repeats the claim's consequence rather than its wording (NOT corrected
here, no edit proposed): `crawler-identity.md:32-34` (the subtype inference, still true) and
`crawler-identity.md:35-38` ("the same page can be crawled twice … a bare Googlebot is ambiguous"),
which reads the ambiguity off the log line's UA alone. The `[INFERENCE]`-class sibling text —
`baidu-friendly-crawl-guidance.md:36-38` ("the *user-agent* string separates the subtypes") — states
the narrower true fact and needs no correction.

## FINDINGS

- A peer scout report reached a different placement conclusion for the same tail.
  `.ufo/waves/round-59/w1/ScoutLaneCrawlerIdentity.md` line "O8 correction placement" reads,
  verbatim: "original lines remain for history, so the new tail must sit after L73 and must not
  rewrite L31 (contract C9)". A tail after L73 fails C9: the counter collects only inserts whose
  base index satisfies `s < i1 <= s + 1 + STALE_WINDOW` (8), i.e. base lines 32-39. The contract and
  the counter agree; that scout line does not. Recorded for the canonical judge, not resolved by me.
- The clause "Its technical-properties section adds that the clients are distributed across many
  datacenters" is a paraphrase of the same text node that holds the quoted logs sentence
  ("… distributed across many datacenters across the world … Therefore, your logs may show visits
  from several IP addresses."); the paraphrase is unquoted by design.
- The correction names `googlebot-verification.md` and `crawler-identity-signals.md`, neither of which
  exists in the lane tree yet; C1 requires both at the measured revision. [INFERENCE] both land from
  sibling seats this wave. Tool installs: none (no pacman, no `uv tool`, nothing written outside the
  seat paths).

## ARTIFACTS

`.../w1/ScribeCorrectionTail.md` (this report) and, under `.../w1/ScribeCorrectionTail.files/`:
`insert.md` (the 13 lines), `c9check.out` (diff + C9 replay), `render-counts.txt` (cmark counts),
`base-identity.txt` (base/HEAD/worktree identity).

VERDICT: C9 insert-ready — 13 inserted lines after base line 34, insert-only per difflib, tag `[r59-correction 2026-10-27]` + S425 citation present, two quoted S425 spans pass the C5 mask and carry "IP address"; C9 replayed pass, full counter and C1-C8 unrun.
