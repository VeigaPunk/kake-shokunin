# ConnectorSibling — round 84 wave w1

Read-only scan over the fleet's 21 lane repos, the kake lane repo, and the shokuknow staged
packages. No production file was edited; no socket was opened; all scratch under
`/fast/scratch/hyaku/kake-r84/ConnectorSibling/` (deleted before yield). Receipts in
`.ufo/waves/round-84/w1/ConnectorSibling/` (`idscan.py`, `scan_kake.json`,
`collision.txt`, `ids_kake_registry_1105.txt` (194 ids, no `S457`), `ids_kake_registry_1109.txt`
(195 ids), `ids_kake_staged.txt`, `ids_S457_holders.txt`, `row_S457.txt`, `c1_base.txt`, and `RECEIPTS.md`
indexing each with its instant and one known artifact in `scan_kake.json`).

Live-state note, because it changes what "the tree" means for every row below: at 11:05 the lane
registry held **194** ids, `S001`…`S456`, with no `S457`; at 11:08 a sibling scribe appended the
`S457` row (working tree, `git diff --stat corpus/SOURCES.md` → `1 file changed, 1 insertion(+)`);
at 11:09 the tolerance-matched census reads **195** ids, max `S457`, dups 0. Both instants are
reported; the staged-package numbers are unaffected (the package is a separate file).

## 1. Sibling overlap scan

Searched `*/corpus/knowledge/` and `*/corpus/SOURCES.md` for `cache-control`, `max-age`,
`header change|header_change|header-diff|header class`, `policy`, `rfc9111`. Two sweeps: a broad
one (`policy` included) and a narrow one (`cache-control|max-age` only). The narrow terms appear in
**no sibling registry**; the broad matches in `mori`/`kumitate` `SOURCES.md` were the unrelated word
"policy" in other scopes (mori: "probe policy", "OOM policy"; kumitate: none on the narrow terms).

Real overlaps, with the exact overlap:

| sibling file / line | overlap | class |
|---|---|---|
| `kumitate-shokunin/corpus/SOURCES.md:191` (`S237`, tier A, rfc-editor `.html`, fetched 2026-11-04, scope "Age and Freshness sections — a stored artifact can carry its own age, and the consumer decides freshness against a declared lifetime") | the closest near-duplicate in the fleet. `S457`'s `teaches` cell states the same freshness-lifetime sentence; both rows are tier A, both fetched 2026-11-04, both anchored in RFC 9111 §4.2/§5.1. What `S237` does **not** carry is the value class table (directive/parameter parsing), which is `S457`'s actual addition | duplicate-of-claim, distinct capability |
| `mori-shokunin/corpus/SOURCES.md:375` (`S594`, tier A, `rfc9111.txt`, "§4.1 … the Vary-selected representation and the cache-key rule") | same document, same `.txt` URL, same tier, immediately-adjacent section. `S457` re-retains the RFC as `.html` and anchors §4.2/§5.2; the `Vary`/cache-key half of §4.1 is `S594`'s and must not be restated | same-source, different section |
| `chousa-shokunin/corpus/SOURCES.md:35` (`S025`, tier C, `rfc-editor.org/rfc/rfc9111`, anchor "section 4.2 Freshness", scope "a general rule for research-record staleness or knowledge-entry metadata policy") | `S457` grounds §4.2 at tier A for policy-field value semantics. `S025` is tier C and scoped to a research-record rule, so it does **not** cover the value classes; a reader must not read the tier-C row as prior art for `S457` | adjacent / weaker tier, not prior art |
| `kumitate-shokunin/corpus/knowledge/receipt-age-on-the-compare-path.md:40` | cites RFC 9111 §4.3.4 (a 304 replaces stored field values, `.ufo/waves/round-81/build/L1/captures/rfc9111.html:2600-2606`) and §4.2.3 `apparent_age` (`:2364`), and derives "the age counts from the later event". This is the fleet's only other reading of *header replacement in a stored response*, which is exactly the premise `C2` needs to say a changed `policy` **value** is a changed stored field rather than a per-request artifact; the same file also states the limit that a capture has no validation event | shared premise, must be cited |
| `kumitate-shokunin/corpus/knowledge/self-describing-shape-receipt.md:24,61` + `receipt-age-on-the-compare-path.md:49,58-65` | a drift gate over a **captured receipt** with an opt-in window (`--max-age DAYS` → `SHAPE_STALE age_days=45 max_age=30`, exit 1) and a **fail-closed exit 2** (`SHAPE_AGE_UNKNOWN`). Overlaps the gate *shape* (captured bytes + declared window + exit taxonomy), not header values | adjacent, reusable control design |
| `tabi-shokunin/corpus/knowledge/committed-bytes-verification-round-42.md:29,53,61` | `git show <rev>:<path>` + sha256 as a byte-drift check, and the sentence "Byte presence is not provenance". This is `C2`'s `receipts_ok` conjunct (bytes == body length, sha256 == body digest) already stated as a lane-general discipline | duplicate of the receipt conjunct only |
| `tabi-shokunin/corpus/knowledge/external-class-fixture-v2.md:299-307` | a loopback `ThreadingHTTPServer` that sets `Cache-Control: no-store` and `Location`. The only fleet occurrence of a deliberately-set `Cache-Control` value; its ground is a redirect/rate fixture, not classification | lexical only — false friend |
| `kengaku-shokunin/corpus/knowledge/extraction-policy-comparison.md:6,22,99-105` | "fixed responses can receive different verdicts" under different *extraction policies*, per-policy agreement and paired flips, "the policy that is appropriate depends on the task contract". Its "policy" is a parser policy over model answers and its verdicts are PASS/FAIL | false friend; one transferable discipline — per-policy paired flips, never a scalar |

In-lane predecessors (the duplication that matters most, since `S457` and `C2` land in the same
registry):

- `corpus/knowledge/header-change-classes.md` (`S456`, `rfc9111.txt`, 84,477 B, anchor §4.2 at
  **lines 583-599 of the `.txt`**) — same document as `S457`, and its `scope:` line already
  disclaims "the lane's class names or … which header belongs in which class". So `S457` is a
  value-level successor, not a second class table; but the two rows now cite one RFC in **two
  coordinate spaces** (`S456`=`rfc9111.txt` line 583; `S457`=`rfc9111-httpwg.html` line 269, a
  15,327-byte line). Any citation written against one copy's line numbers is wrong against the
  other; only `S457`'s own `anchor` cell names its file.
- `corpus/knowledge/capture-drift-validators.md:31-35` — "String equality is not semantic equality.
  … a semantically equivalent re-serialization (spacing, value order within a list) reads as
  `changed`". That is precisely the limit `C2`'s `reordered` class removes, so `C2`'s entry must
  cite it as the repaired limit, not rediscover it.
- `corpus/knowledge/capture-drift-validators.md:216` (§7 erratum) already reads a `max-age` number
  out of captured headers: "`expires` is that epoch plus `max-age` (600 s) … `expires − fill = 600`
  on all six rows". `C2`'s `numeric_parameter` control is `max-age=600 → max-age=60` — the same
  figure the lane already published.
- `corpus/knowledge/response-header-expectations.md:66-67,201-202` — "the audit records presence,
  and it does not parse `max-age`". Still true of `scripts/header_audit.py`; it is *not* true of
  `scripts/policy_value_class.py`. The subject must be named, or the older sentence reads as a
  lane-level denial of `C2`.

## 2. `S457` collision check

Extractor: the lane's own tolerant rule, `scripts/id_resolver.py:21-31` (registry ids = first cell
of a table row under the exact heading `## Registry`, "0 to 3 leading spaces before the pipe (the
census parser's rule; 4 spaces is code)", fence-aware) and `:56`
`ROW_RE = ^ {0,3}\|\s*([^|]*?)\s*(?:\|(.*))?$`. Re-implemented at
`.ufo/waves/round-84/w1/ConnectorSibling/idscan.py` and cross-checked against
`grep -oE '^[ ]{0,3}\|[ ]{0,3}S[0-9]+' | sort -u`: both 194 at 11:05, both 195 at 11:09.

Id lists (full lists in `ids_kake_registry_1105.txt`, `ids_kake_registry_1109.txt`,
`ids_kake_staged.txt`):

- kake registry, 11:05 — n=194, dups=0, runs
  `S001-S139, S249, S262-S263, S273-S274, S286, S312, S329, S367, S372-S374, S390, S409, S416-S456`.
  `S457` absent. Next free id = **S457**.
- kake registry, 11:09 (after the scribe's write) — n=195, dups=0, max `S457`, so the id is unique
  in-lane by the census's own rule.
- kake staged package `/home/vgpnk/Projects/shokuknow/merge/kake/SOURCES.append.md` — n=129,
  `S287`…`S415`, contiguous. `S457` absent.
- Registry ∩ staged = **8** ids (`S312, S329, S367, S372, S373, S374, S390, S409`), and each of the
  eight is the same document as the staged row at that id (identical source title **and** URL, e.g.
  `S390` = 百度Spider新增渲染抓取UA公告 / `https://ziyuan.baidu.com/wiki/990` on both sides). These are
  already-landed rows, not conflicts; the other 121 staged ids are unlanded.

Collision count: **0** in the kake registry, **0** in the kake staged package.

Fleet-side `S457` holders (21 registries scanned; **2** before the lane's own write — `mado-shokunin`
(max `S483`) and `revenger-shokunin` (max `S479`) — and 3 after it, counting kake): plus
`merge/kama/SOURCES.append.md`, whose block is `S330`…`S471`
and does contain `S457`. This is **not** a collision, and the measurement that settles it is that
the two staged packages themselves overlap by **86 ids** (`merge/kake` ∩ `merge/kama` =
`S330`…`S415`). Two "staged" packages sharing 86 ids prove each package continues its own lane's
S-space; ids are lane-local. A fleet-wide "`S457` is taken" reading is therefore wrong, and so is
the inverse inference that a lane append must skip siblings' ids.

URL dimension: `S456` = `https://www.rfc-editor.org/rfc/rfc9111.txt`, `S457` =
`https://httpwg.org/specs/rfc9111.html` — different URLs for the same document in two renderings.
The lane file already carries a *third* pointer to the same document: `corpus/SOURCES.md:267` lists
`RFC 9111 HTTP Caching — https://www.rfc-editor.org/rfc/rfc9111.html` as an unopened lead bullet,
which is kumitate `S237`'s URL. So after `S457` the fleet holds three renderings of RFC 9111
(`rfc-editor .txt` in kake/mori, `rfc-editor .html` in kumitate and in kake's lead list,
`httpwg .html` in kake), and no registry row collides on a URL.
The census normalization (scheme stripped, host lowercased, fragment and one trailing slash
stripped) keeps them distinct, so no URL collision; the document duplication is the `S456` row
above. Precedent for a second row on one document at a distinct scope is in the lane itself:
`S028` says "distinct section and scope from S010" on the same `rfc9110.txt`. The one live check I
made on the landed row rather than trusting the write: its anchor's coordinate space is real —
`rfc9111-httpwg.html` line 269 is a 15,327-byte line containing `rfc.section.4.2`, `Freshness`,
`rfc.section.4.2.p.1` and `…p.3`; line 279 contains `rfc.section.5.2` + `Cache-Control`; line 282
contains `rfc.section.5.2.2.1` (receipt `row_S457.txt`). The row's `source` URL matches the round's
own retained copy (`ScoutSources/fetch-meta-httpwg.txt`: `http_code=200`,
`url_effective=https://httpwg.org/specs/rfc9111.html`, `size_download=178573`).

Residual risk, not a collision: the reservation `S287`…`S415` is invisible from inside the lane, and
`S457` is above it, so append-at-max+1 is safe this round only because the lane's own `S416`…`S456`
block already sits above the reserved block.

## 3. Cross-claim pattern

The `C1` repair pattern is: *a routed-defect queue whose closure is re-derived from tree bytes by
conjuncts, with one line per item and a single `met` summary whose exit code is the decision.*

- **Implements it — kasegi.** `kasegi-shokunin/corpus/instruments/r47-routed-defects.py:32-36` —
  "Each limb is `fixed` only when the substantive evidence is present in the tree under `--root`;
  the counter is READ-ONLY over the tree it grades"; `:48-49` the output contract
  (`limb L<n> fixed=0|1 read=<token>` then `routed-defects total=11 fixed=<k> unresolved=<m> exit=0|1`);
  `:346` `print(… exit=%d) % (…, 0 if fixed == total else 1)`. Same shape as `c84_defect_queue.py`,
  plus a `read=<token>` per item that kake does not print.
- **Implements it — kumitate, in ledger form.** `kumitate-shokunin/scripts/routed-ledger.mjs:33`
  (`ROUTED_LEDGER: CLEAN spotchecks=<n> sections=<s> items=<i> rows=<r> open=<o> closed=<c>
  wontfix=<w>`), `:16` a closed row binds its answer by `path:line` **plus a quote located at that
  exact line**, `:19`/`:343` `ROW_CONTRADICTED` refuses a second non-open row on one
  `(round,item)`, `:37` exit 0 clean / 1 drift / 2 fail-closed / 64 usage.
- **Does not implement it — mado.** `mado-shokunin/corpus/lessons/round-80-verifier-spotcheck.md:133`
  opens `## Routed defects (lane fixes next round; status-neutral)` and lists `D1`…`D7` as prose
  bullets `:135`…`:156`; `test -d mado-shokunin/scripts` → exit 1, so there is no script directory;
  the only two non-`.ufo` hits for `routed-defects|defect_queue|routed-ledger` under the whole lane
  are prose (`corpus/QUALITY.md:328`, a rule that a predicate and its counter share one population,
  and `corpus/lessons/round-77.md:194`, "the round-78 report's routed-defects section") — so mado
  routes defects in reports but has no instrument to decide them; and the two following lessons
  carry no closure row —
  `grep -n 'D[1-7]' mado-shokunin/corpus/lessons/round-81.md mado-shokunin/corpus/lessons/round-82.md`
  → 0 hits. The queue is prose with no closure record at all.
- **kake's own instantiation, and a divergence.** `c84_defect_queue.py:204-210` prints
  `item=<n> closed= state= row= <detail>` then `C1v1 … open= closed= met=`; the selftest at `:281-300`
  mutates one item per case. But two items' contract row conjuncts are **not prose reads**:
  `item_d3` (`:161-179`) returns `row = len(settled) >= 1`, and `item_d4` (`:180-201`) returns
  `row = len(claimed) == len(derived) and len(derived) > 0` — both are the state expression again,
  while contract §C1 says `D3`'s row conjunct is "the round lesson or `SCORECARD.md` names the
  connector seat" and `D4`'s is "the round lesson names `controls/census-before.txt`". The freeze's
  own receipt proves it is dead: `.ufo/waves/round-84/controls/base-c84-defect-queue.txt:4` prints
  `item=D4 closed=1 state=1 row=1 receipt_w04=22 derived_w04=22` while `corpus/lessons/round-84.md`
  does not exist — the path is absent at both the base `fe42ad11` and the freeze `f358022`
  (`git show <rev>:corpus/lessons/round-84.md` exits **128** at each), and the frozen receipt is
  byte-identical to the tree's copy (`git diff --stat f358022 -- …/base-c84-defect-queue.txt` empty,
  exit 0). My independent run at the worktree
  reproduces the four item lines and `C1v1 revision=worktree items=4 open=3 closed=1 met=false`,
  **exit 1** (`c1_base.txt`). `D1`'s row conjunct is a genuine prose test but only token-membership
  (`"round-83.md" in line and "Gate" in line`), which a sentence can satisfy while naming nothing.

## 4. What the lane can learn only across lanes

1. **Closure can be bound to a located quote instead of a token.** kumitate's ledger requires each
   closed row to name a `path:line` and to carry a quote that is found at *that* line, and refuses a
   second non-open row per `(round,item)` (`routed-ledger.mjs:16,19,343`). kake's `D1` row conjunct
   accepts the mere presence of two words on a line, and `D3`/`D4` read no prose at all — a defect
   marked closed by an unrelated sentence is undetectable here, and kumitate's guard is the reason
   it is detectable there. Nothing in kake's repo states this rule; `corpus/knowledge/gate-status-ledger.md`
   is a historical-gate list, not a per-item closure ledger.
2. **Keep "unevaluable" out of "open".** kumitate exits 2 for fail-closed and 1 for drift
   (`routed-ledger.mjs:37`), and `c84_…` does not: the C1 selftest asserts
   `missing-tree-reopens-all — open=4 expect=4` (`controls/c84-selftest-c1.txt`), i.e. an unreadable
   tree and four live defects print the same `open=4` and the same exit. Under the round's kill rule
   ("a claim whose counting command exits non-zero at the after-state reports `unprovable`") the
   receipt cannot distinguish a miss from an unreadable tree without reading the free-text `detail`.
   That distinction exists in a sibling lane and in none of kake's counters.
3. **A second allocator holds `S287`–`S415` and lives outside the lane repo.** The lane's whole
   visibility into id space is `max(registry)+1`; the staged block is only in
   `/home/vgpnk/Projects/shokuknow/merge/kake/`, and its continued existence is provable only by
   comparing it against `merge/kama/` (86 shared ids). Kake's own repo cannot tell the lane that a
   reservation exists, that 121 of its ids are still unlanded, or that `S457` is safe *because* it is
   above `S415` rather than because it is the next integer.

## Commands and exit codes

```
cwd=kake-shokunin
python3 -B .ufo/waves/round-84/c84_defect_queue.py --root .
  -> exit 1; item=D1..D4 closed=0,0,0,1 ; C1v1 revision=worktree items=4 open=3 closed=1 met=false
python3 <receipts>/idscan.py corpus/SOURCES.md          (11:05 then 11:09)
  -> exit 0 both times; n=194 then n=195; dups=0; max S456 then S457
grep -oE '^[ ]{0,3}\|[ ]{0,3}S[0-9]+' corpus/SOURCES.md | tr -d ' |' | sort -u | wc -l
  -> exit 0; 195 (cross-check of the tolerant extractor)
grep -cE '^ {0,3}\| {0,3}S457' corpus/SOURCES.md
  -> 0 before the scribe's write, 1 after
git diff --stat corpus/SOURCES.md
  -> exit 0; 1 file changed, 1 insertion(+)
git show fe42ad11eb1084ad2ea68d12c5bbb2922a089868:corpus/lessons/round-84.md
  -> exit 128 (path absent at base); the same at f358022 (path absent at freeze)
git diff --stat f358022 -- .ufo/waves/round-84/controls/base-c84-defect-queue.txt
  -> exit 0, empty: the frozen receipt equals the tree's copy

cwd=fleet root
python3 <receipts>/idscan.py */corpus/SOURCES.md        (21 registries)
  -> exit 0; S457 holders: 2 before the write (mado, revenger), 3 after
grep -rn 'rfc9111' --include=SOURCES.md . | grep -v '/\.ufo/'
  -> exit 0; 6 lines: kake S456, kake S457, kake :267 (an unopened-lead bullet), kumitate S237,
     mori S594, chousa S025
grep -n 'D[1-7]' mado-shokunin/corpus/lessons/round-81.md mado-shokunin/corpus/lessons/round-82.md
  -> exit 1; no matches
test -d mado-shokunin/scripts                          -> exit 1; absent
grep -rln -E 'routed-defects|defect_queue|routed-ledger' mado-shokunin/ | grep -v '/\.ufo/' | wc -l
  -> exit 0; 2 (prose only)
grep -nE '^- \*\*D[1-7]' mado-shokunin/corpus/lessons/round-80-verifier-spotcheck.md
  -> exit 0; bullets at 135,139,142,144,146,150,153
grep -n 'rfc.section.4.2' kake-shokunin/.ufo/waves/round-84/w1/ScoutSources/rfc9111-httpwg.html
  -> exit 0; first prose hit line 269 (line 261 is the nav)
rm -rf -- /fast/scratch/hyaku/kake-r84/ConnectorSibling
  -> exit 0; scratch removed, receipts kept under w1/ConnectorSibling/
```

## Verdict

`CONNECTOR-SIBLING: CLEAN — 0 id collisions (kake registry 0, kake staged package 0; the 3 fleet
S457 rows are lane-local, proven by the two staged packages sharing 86 ids); overlap scan complete
over 21 lane repos with 8 cross-lane overlaps named and 2 false friends named; 1 contract-vs-instrument
divergence reported, not patched (C1 `D3`/`D4` row conjuncts are state expressions, and the frozen
base receipt shows `D4 closed=1` with no round lesson); 3 cross-lane lessons named that kake's own
repo cannot supply.`
