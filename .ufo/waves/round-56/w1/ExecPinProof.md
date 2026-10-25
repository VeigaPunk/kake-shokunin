# ExecPinProof

Round-56 W1, lane `kake-shokunin`. Question: do the two revision-pinned quote-truth selftests keep passing
after later commits change the tree, and what must a `SKILL.md` registry row carry so its documented
command reproduces the tally?

Method: throwaway clone `D=/tmp/tmp.Bqxq2sLwwK`, `git clone -q --no-checkout` of the lane, `checkout -q
e48354b7c26bb6dc544ab6bbdc534fabe0daf7b6`; `git -C "$D/kake" rev-parse --show-toplevel` = `/tmp/tmp.Bqxq2sLwwK/kake`.
Then one commit on top, `5454be9b534dbc4793fb53738023c4d48421cada` (identity `-c user.name=selftest -c
user.email=selftest@local`), 4 files / +21 lines: two registry rows appended after S418 in
`corpus/SOURCES.md` (fixture S419/S420, text marked "not a landed claim"), two entries under
`corpus/knowledge/` (`yahoo-japan-deleted-url-recrawl.md`, `yahoo-japan-nonexistent-url-recrawl.md`), and
two rows added to the `corpus/README.md` coverage map. No lane file, lane jj state or Git index touched;
the fixture lives only inside `$D`.

## RUNS:

All runs from the clone root, `python3 -B`, serial (one at a time). Tallies are the printed `A/B`.

| selftest | pin | HEAD | result |
|---|---|---|---|
| `c52_quote_truth.py --selftest` | `KAKE_R52_SELFTEST_REV=1ae8de5d4dee` | `e48354b` (base) | **18/18, exit 0 — PASS** |
| `c52_quote_truth.py --selftest` | none | `e48354b` (base) | 17/18, exit 1 — FAIL (`pass: expected 0, got 1`: C5 S374 line-72 quote; C8 `registry rows 156 != mirror rows 145 + 3`) |
| `c55_quote_truth.py --selftest` | `KAKE_R55_SELFTEST_REV=64c0ce12ffe3ca4d6d1891a3e3e33933a95380f6` | `e48354b` (base) | **54/54, exit 0 — PASS** |
| `c55_quote_truth.py --selftest` | none | `e48354b` (base) | **54/54, exit 0 — PASS** |
| `c52_quote_truth.py --selftest` | `KAKE_R52_SELFTEST_REV=1ae8de5d4dee` | `5454be9` (fixture) | **18/18, exit 0 — PASS** |
| `c52_quote_truth.py --selftest` | none | `5454be9` (fixture) | 17/18, exit 1 — FAIL (same two C5/C8 notes, now `registry rows 158 != mirror rows 145 + 3`) |
| `c55_quote_truth.py --selftest` | `KAKE_R55_SELFTEST_REV=64c0ce12ffe3ca4d6d1891a3e3e33933a95380f6` | `5454be9` (fixture) | **54/54, exit 0 — PASS** |
| `c55_quote_truth.py --selftest` | none | `5454be9` (fixture) | 51/54, exit 1 — FAIL (3 fixtures: `pass`, `pass_census_relative_argv`, `pass_gate_extra_short_quote`; each with C7 `validated scratch registry is not byte-equal to the landed registry`, C8 `registry rows 158 != mirror rows 155 + 1`, C8 `append-only: ... != mirror bytes`) |
| `c55_readme_index.py --selftest` | none | `5454be9` (fixture) | **44/44, exit 0 — PASS** |
| `c52_wave_ledger.py --selftest` | none | `5454be9` (fixture) | **19/19, exit 0 — PASS** |

Both pins resolve in the clone and are ancestors of the fixture HEAD (`1ae8de5d4dee8300624b0db2a94497ff905942c5`,
`64c0ce12ffe3ca4d6d1891a3e3e33933a95380f6`). Pinned runs print `(fixture revision 1ae8de5d4dee)` /
`(fixture revision 64c0ce12ffe3)`; unpinned runs print the HEAD sha they resolved.

## WHY:

Both scripts read committed bytes only, and every evidence read is `git show <rev>:<path>` where `rev` is
the env pin or, when the pin is absent, `git rev-parse HEAD` of the working directory:

- `c52_quote_truth.py:466-472` — `rev = os.environ.get("KAKE_R52_SELFTEST_REV")`; else `git(os.getcwd(), "rev-parse", "HEAD")`; `root = os.getcwd()`.
- `c55_quote_truth.py:593-597` — `git(os.getcwd(), "rev-parse", "HEAD")`, then `rev = os.environ.get("KAKE_R55_SELFTEST_REV") or head`.

The fixed evidence list includes `corpus/SOURCES.md` (REGISTRY), the pre-append mirror and its pin, the
receipts, the census/validate scratch, and the `ADOPTED` entries. `corpus/README.md` is **not** read by
either script (zero `README` references in both) and the knowledge reads are fixed `ADOPTED` paths, so the
two new entries and the README rows are inert; the registry blob is the one surface that moved.

Row arithmetic, measured with the same census parser (`## Registry`, 0–3 leading spaces, `S[0-9]{3,}`):

| revision | registry rows | subject |
|---|---|---|
| `1ae8de5d4dee` (r52 pin) | 148 | round 52: frozen baselines and the seven measurement receipts |
| `64c0ce12ffe3` (r55 pin) | 156 | round-55: content revision — reviewer repairs, lesson caveat, validation receipts |
| `fcaf4b85ce32` (r55 hardcoded `BASE_REV`) | 155 | round-54 verifier spot-check (integrator, hyaku): non-author admit/reject |
| `e48354b7c26b` (round-56 base) | 156 | round-55 verifier spot-check (integrator, hyaku): non-author admit/reject |
| `5454be9b534d` (this fixture) | 158 | round-56 fixture: two registry rows, two entries, README rows |

- **r52 C8** requires `len(rows) == mirror_rows + len(ADOPTED)` with `mirror-pin.json` `rows=145` and three
  adopted rows → 148. `1ae8de5d4dee` has exactly 148; base tip already had 156 (hence the known 17/18),
  the fixture has 158. C8 also requires the measured registry minus the three adopted rows to equal the
  mirror bytes, which any later append breaks.
- **r52 C5** fails unpinned because later commits edited `corpus/knowledge/yahoo-japan-rel-nofollow-semantics.md`
  (`fd91527` round-53 re-grounding, `8e408e0` round-54 S374 repair, `faf9abe` round-55 wave-2 repairs): line
  72's quote is no longer a raw substring of the retained body. The pin reads the pre-edit blob, so the
  fixture commit — which does not touch that entry — leaves the failure count unchanged at 17/18.
- **r55 C8** requires `len(rows) == mirror_rows(155) + len(NEW_ROWS=("S418",))` → 156, plus append-only
  equality after restoring `used-by` on S372/S373. `64c0ce12` has 156; base tip also had 156 (no registry
  commit between the pin and base tip: `git log 64c0ce12..e48354b -- corpus/SOURCES.md` is empty), which is
  why r55 unpinned passed at base and fails at 158.
- **r55 C7** additionally compares the measured registry byte-for-byte with the frozen validated scratch
  `.ufo/waves/round-55/assimilation/validate/corpus/SOURCES.md` (sha256 `cc402e4b559528170fe71ba09b6ad3be663a8f9d5ce9f36caeaed5ea45e6c50e`, 156 rows, identical at `64c0ce12` and at `e48354b`). At 158 rows
  that equality dies, so three `pass*` fixtures flip — 54 → 51.

Conclusion: the pins are load-bearing, not decoration. A pinned run is invariant under any later commit
(the fixture HEAD proves it for both scripts); an unpinned run is a function of the registry and entry
bytes at HEAD and breaks as soon as the round appends rows. Neither the new entries nor the README edit can
flip either selftest — only `corpus/SOURCES.md` (and, for r52, the S374 entry) can.

`c55_readme_index.py --selftest` builds its own synthetic fixtures (`N=46`, `_fixture()` sandbox repos) and
never reads the lane HEAD; `c52_wave_ledger.py --selftest` builds fixtures under its own `SELFTEST_DIR` and
resolves each fixture repo's own HEAD. Both are HEAD-invariant by construction — 44/44 and 19/19 at the
fixture HEAD confirm it.

Operational note (observed, not a claim about the gate): `c52_quote_truth.py` keeps its scratch at
`<repo>/.ufo/waves/round-52/selftest/quote/work` (gitignored, `shutil.rmtree` at start). Two concurrent
invocations in the same clone collide — I hit `fatal: cannot copy '/usr/share/git-core/templates/hooks/commit-msg.sample' to '.../work/fail_bad_receipts/.git/hooks/commit-msg.sample': File exists` once and reran serially; the 18/18 above is the serial rerun.

## RECOMMENDATION:

The registry row's self-test cell must carry the pinned command as one backticked span, because
`c56_selftally.py` (`documented_command`, `run_command`) takes the first backticked span that names the
script and carries `--selftest`, splits leading `VAR=value` words into the environment, and runs the rest in
a clean clone of the measured revision. Without the pin the command fails at any post-append revision.

Row `quote-truth-counter` — exact cell text:

    `KAKE_R52_SELFTEST_REV=1ae8de5d4dee python3 -B .ufo/waves/round-52/c52_quote_truth.py --selftest` (18 fixtures, sandbox repos; receipt `.ufo/waves/round-52/control/c2-quote-selftest.txt`)

Row `yahoo-robots-quote-truth-counter` — exact cell text:

    `KAKE_R55_SELFTEST_REV=64c0ce12ffe3ca4d6d1891a3e3e33933a95380f6 python3 -B .ufo/waves/round-55/c55_quote_truth.py --selftest` (54 fixtures, sandbox repos; receipt `.ufo/waves/round-55/controls/c2-selftest.txt`)

Constraints that make those cells parse as C1 expects:

- The claim integer must equal the printed **total**, and the cell must contain exactly one integer the row
  regex `\((\d+) (?:sandbox-repo )?(?:fixtures|checks)` matches: `18` for r52, `54` for r55. The current
  r55 cell's `47 sandbox-repo fixtures` is why the base row reads as a mismatch against 54; a second
  matching integer elsewhere in the cell (e.g. `(54 fixtures ... plus 47 sandbox-repo fixtures)`) would sum
  to 101 and re-break the row. Non-matching numeric prose (`plus 3 unit-rule checks`) is safe.
- Keep the `VAR=value` word first and unquoted inside the span; `shlex.split` then hands it to `env`.
- Pin to a **pre-append** revision (`1ae8de5d4dee` = `1ae8de5d4dee8300624b0db2a94497ff905942c5` for r52,
  `64c0ce12ffe3ca4d6d1891a3e3e33933a95380f6` for r55). The pin names the *fixture* revision; the row's gate
  command (`--root . --revision <commit>`) still measures the round's own revision. Pinning to the round-56
  final revision would reintroduce exactly the failure this seat measured.
- No pin is needed for `readme-index-counter` (44/44) or `wave-evidence-ledger` (19/19) — both selftests
  generate their own fixtures. Their claims are separate C1 items; note that the readme-index row currently
  claims 35 against an observed 44 (out of this seat's scope, reported as observed).

Risks / limits: the fixture commit is throwaway (`/tmp/tmp.Bqxq2sLwwK`, may vanish); the real round-56
append will produce the same 156→158 (or 156→157/159) row movement and therefore the same unpinned
failure. I did not run `c56_selftally.py` (it clones the lane at a measured revision; not this seat's
command surface) and did not measure the SKILL.md rows themselves.

VERDICT: Pinned runs are HEAD-invariant (r52 18/18, r55 54/54 at base and at a post-append fixture HEAD); unpinned r52 is 17/18 and unpinned r55 drops 54/54 → 51/54 after the registry append, so both registry rows must document the `KAKE_R5x_SELFTEST_REV` pin with claim 18 and 54.
