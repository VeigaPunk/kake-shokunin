# Round 37 W2 — RevengerToolReadings: the 12 open-point readings vs L1 ref and independent

Attacked: wave-1 `ExecRobotsTool`'s 11 numbered open-point choices (`.ufo/waves/round-37/w1/ExecRobotsTool.md`,
"Open-point choices") against the L1 reference and the independent implementation, per reading with a
distinguishing input. The w1 list has 11 items; the assignment says 12 — choice 2 holds two independent
readings, split here into 2a/2b. Method: sandbox `/fast/scratch/hyaku/kake-r37w2/RevengerToolReadings`
(clone of 79d3c780, checkout verified); landed tool sha256 `5eb767ec…cabae` = w1 deliverable, unedited.
Harness `harness.py` (retained in sandbox) ran `python3 <tool> --manifest <m>` for each of 15 constructs ×
3 tools; outputs projected to (exit, verdict, checksEvaluated, multiset(check,reason)); KAKE_ABLATE unset.
Run 1 exit 0; after fixing an R1a harness bug (dangling symlink), rerun printed all 15 blocks, summary
section raised TypeError (cosmetic, after data). TMPDIR pointed into the sandbox; no lane file written but
this report; no tool installs (stdlib only). Contract text: SCORECARD.md:1795-1858.

Per-reading results (L=landed, R=ref, I=independent; exit/V/E/findings):

1. Manifest stat follows symlinks; FIFO/device input_invalid, never opened.
   R1a symlink→regular: L 0/clean/1/[]; R same; I same. R1b FIFO: all 2/input_invalid/0, instant (no block).
   Bonus: dangling symlink → all three 2/input_invalid ("not a regular file", SCORECARD.md:1854).
   Text: stat semantics; contract says only "not a regular file". HOLDS (all three agree).
2a. Manifest directory = dirname(realpath(manifest)). Construct: dirB/link.json → dirA/real.json, robots
   "r.txt" only in dirA. L 0/clean/1; **R 2/check_invalid (c1)**; I 0/clean/1. Ref resolves robots relative to
   `realpath(dirname(abspath))` (ref.py:180) — the symlink's dir, not the target's. Text: "inside the
   manifest's directory (after resolving symlinks and `..`)" (SCORECARD.md:1809-1810) — resolving the
   manifest's own symlinks is the supported reading. Landed reading HOLDS; ref.py deviates on this input.
2b. 64 MiB inclusive. Exactly 67108864 B: all 0/clean/1; +1 B: all 2/input_invalid. Text: "larger than
   64 MiB" is the fault (SCORECARD.md:1854). HOLDS.
3. BOM manifest. `\xef\xbb\xbf`+valid JSON: all 2/input_invalid. Text: fault list has "not JSON"
   (1855); json.loads rejects a leading U+FEFF, and BOM removal is granted only in (b) to the robots
   file (1819-1820). HOLDS.
4. Product token `[A-Za-z_-]+`. ua "-" evaluated (c1 blocked, robots `Disallow: /p`), ua "Agent1"
   check_invalid: identical in all three (L=R=I: 2/[(c1,blocked),(c2,check_invalid)]/E=1). Text: "one or
   more ASCII letters, `_` or `-`" (1807) — digits rejected, lone "-" accepted. HOLDS.
5. URL validity = scheme+non-empty host only. "ftp://h/p" check_invalid; "http://h:zzz/p" evaluated
   (blocked); "HTTP://H/p" evaluated — identical in all three (2/[(u1,check_invalid),(u2,blocked)]/E=2).
   Text: contract lists exactly scheme+host (1807-1808); port/userinfo unjudged. HOLDS.
6. Implicit `/robots.txt` compared raw, before normalization. robots `User-agent: *\nDisallow: /`.
   L: i1 `/robots%2Etxt` blocked, i2 `/robots.txt?x=1` blocked. **R: i1 NOT blocked** (allowed implicitly:
   `npath == "/robots.txt"` after normalize, ref.py:137); i2 blocked. I: like L. So R accepts a
   percent-encoded spelling the raw-path reading rejects. Text: "The path `/robots.txt` is always allowed"
   (SCORECARD.md:1841) precedes "Before comparison both … are normalized" (1842) — the exemption is on the
   constructed path, pre-normalization. Landed reading HOLDS; ref.py is over-broad here (yet scored 28/28
   sealed — the sealed cases do not pin this edge, as SCORECARD's follow-up section itself states).
7. Validated robots file unreadable at open time (chmod 000). All three 2/[(c1,check_invalid)]/E=1
   (c2 404 still evaluated). Text: (f) fault list (1848-1851) omits "unreadable"; "unreadable" appears only
   in (g) for the manifest (1855); check_invalid is the only bucket that keeps the other check evaluated.
   Supported-by-analogy [INFERENCE]; all three implementations chose it. HOLDS (w1 flagged this as a bare
   choice — confirmed: not text-pinned, but not wrong either).
8. Matching group with no rules still suppresses `*`. robots `*\nDisallow: /\nUser-agent: bot`; ua "bot",
   expect allow → all 0/clean/1. Text: fallback only "if no group matches" (SCORECARD.md (c), ~1817-1819).
   HOLDS.
9. Lone surrogate URL (`http://h/a\ud800b`, JSON escape). L: 0/clean/1 (decided; with expect=allow →
   1/[(c1,blocked)] probe — the path was encoded and matched `Disallow: /a`). **R and I crash**:
   UnicodeEncodeError "can't encode character '\ud800'… surrogates not allowed", exit 1, no JSON
   (ref.py:106, independent:64 — plain `encode("utf-8")`). Landed encodes surrogatepass
   (robots_audit.py:157). Text: the check satisfies every (f) rule, so the tool must report a decision; a
   crash produces no report at all. "Always reports rather than crashing" HOLDS for the landed tool; the
   exact encoding of an ill-formed scalar is text-open, both references fail the report obligation.
10. Ids case-sensitive; earlier invalid id counts; id kept on check_invalid. checks A(600), a(valid), A(dup):
    all three 2/[(A,ci),(a,blocked),(A,ci)]/E=1. Text: id "not equal to the id of an earlier check in the
    list" (1805-1806, positional regardless of validity); string equality case-sensitive; (f) 1851. HOLDS.
11. Extra top-level manifest fields; trim = spaces/tabs only. Extra "note" accepted by all; NBSP key
    `\u00a0allow\u00a0: /p` ignored by all → c1 blocked (1/[(c1,blocked)]/E=1) — a `str.strip()` tool would
    have allowed. Text: "with spaces and tabs trimmed" (1821-1822); (g) fault list has no extra-field rule.
    HOLDS.

Verdict: all 12 landed readings hold on their distinguishing inputs; 9 of 12 show three-way agreement, 3
show defects — all in the reference implementations, none in the landed tool: (i) ref.py manifest-dir
reading (2a); (ii) ref.py implicit-allow after normalization (6); (iii) ref.py and independent crash on a
lone surrogate instead of reporting (9). Consequences: none touch the C1 counter result (sealed cases
contain none of these constructs; the ref scored 28/28 anyway). But the independent implementation is the
selftest's second oracle: it is not crash-proof beyond the 131 fixtures, so future selftest fixtures using
surrogate URLs would kill the oracle, not the tool. Reproduce: `cd /fast/scratch/hyaku/kake-r37w2/RevengerToolReadings
&& python3 harness.py` (cases/R6, cases/R9 kept on disk).
