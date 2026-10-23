# ExecCriteriaRepairs — round-36 routed defect 7 (QUALITY f, d, a)

Built three criterion checks under `/fast/scratch/hyaku/kake-r37w1/ExecCriteriaRepairs/criteria/` (to land at
`.ufo/waves/round-37/criteria/`). sha256: `control_tree_check.py` b592270e…9fc0, `polarity_check.py`
7ebc5d67…a96083, `bare_id_check.py` 8b8fe47d…adbd. Receipts+runners under `…/receipts/`:
`criterion-control-tree-v2.txt` 051f60b8, `criterion-polarity.txt` d15e9e15, `criterion-bare-id.txt` 97a3b3f2,
`run_{control_tree,polarity,bare_id}.sh` fb843c14, 9b369187, e3874143. Every command below ran `timeout 120`,
`python3 -B`, TMPDIR=sandbox; exits as observed.

## (d) control_tree_check.py v2 — root-listing false pass closed

v1 verified "a listing exists and shows no key path"; v2 fails when any listing shows (i) a component `sealed`
or basename `cases*.json` (case-insensitive), (ii) a path matching a `--pattern` key path, or (iii) a listed
directory on a key path above the key file — a non-recursive listing that stops at `.ufo` cannot certify what
it does not show. `--tree DIR` additionally walks the real tree and requires each tree be covered by a listing.
Commands/exits (receipt lines 5–47):
- `--report .ufo/waves/round-36/criteria/r35-0b7779dc-parent-tree-report.md --pattern .ufo/waves/round-35/sealed/` → FAIL on `.ufo/waves/round-35/sealed/{c1-cases,c2-probes}.json` (and round-22 `cases.json` by name), exit 1.
- `--report fixtures/report-root-key.md --pattern .ufo/waves/round-36/sealed/` → FAIL "directory '…/tree-with-key/.ufo' lies on key path", exit 1. The v1 script on the same report exits 0 (receipt line 44) — defect demonstrated.
- recursive `ls -laR` fixture → exit 1; `git ls-tree -r` fixture over round-35 key → exit 1; root listing of the lane (holds `.ufo/waves/round-37/sealed/cases.json`) → exit 1.
- `--tree fixtures/tree-with-key` run → exit 1 (`--tree` finds `.ufo/waves/round-36/sealed/cases.json` on disk).
- all 8 `.ufo/waves/round-37/ctl/*.md` with `--pattern .ufo/waves/round-37/sealed/` → exit 0; all 5 round-36 `ctl/*.md` → exit 0; constructed clean tree + `--tree` → exit 0.

## (f) polarity_check.py — the missing red-before receipt

Body-decidable check = final status 200 + body + supported media type + supported charset label; then only the
body bytes decide hold vs `quote_missing`. Per body-reading bullet (default `c,d,e,f`: HTML text, quote match,
media types, decoding) every case must carry ≥1 such finding and ≥1 such hold — kills every no-body shortcut.
- `--key .ufo/waves/round-36/sealed/cases-v1.json` → exit 1: bullets e and f have 0 body-decided findings (all
  8 cases k17–k24; their only findings are metadata-decided `unsupported_type`/`charset_unsupported`) — the
  CtlShortcut gap, now a criterion check. c,d pass.
- `--key .ufo/waves/round-36/sealed/cases.json` (v2) → exit 0: e=8 findings/12 holds, f=4/12, c=16/12, d=4/12.
- constructed metadata-only key → exit 1; constructed both-polarities key → exit 0 (receipt lines 26–34).

## (a) bare_id_check.py — bare-id negative receipt

Per entry, every cited S-id must appear in ≥1 block (paragraph/item/heading; code fences skipped) carrying ≥3
claim words after stripping ids/URLs/paths/section refs.
- `fixtures/bare-id-entry.md` (`source: S098`, `cites: S099`, `- S098`, `- S099`) → exit 1, both ids flagged.
- `corpus/knowledge/crawl-scope-per-host.md` → exit 0; full `corpus/knowledge/*.md` sweep → exit 0.

## Commands (paste-ready, from lane root)

    C=/fast/scratch/hyaku/kake-r37w1/ExecCriteriaRepairs/criteria
    python3 -B $C/control_tree_check.py --report .ufo/waves/round-36/criteria/r35-0b7779dc-parent-tree-report.md --pattern .ufo/waves/round-35/sealed/      # exit 1
    python3 -B $C/control_tree_check.py --report $PWD/../../../*.md --pattern .ufo/waves/round-37/sealed/   # ctl/*.md → exit 0
    python3 -B $C/polarity_check.py --key .ufo/waves/round-36/sealed/cases-v1.json   # exit 1
    python3 -B $C/polarity_check.py --key .ufo/waves/round-36/sealed/cases.json      # exit 0
    python3 -B $C/bare_id_check.py corpus/knowledge/render-static-sites.md           # see risk note

## Risks / not verified

- `bare_id_check.py` sweep over all 33 knowledge entries passed (v2 of the block parser). Earlier line-level
  parsing flagged `render-static-sites.md` (wrapped citations `(…, S005, S003, S007)`); block grouping removed
  the false positive — parenthetical id lists inside a claim-carrying paragraph now pass. L1 may prefer the
  stricter line-level rule; it is a one-line change (`_blocks` → per-line).
- `control_tree_check` warns (exit stays 0) when a listing names no root — MutRefPass.md's unrooted block hits
  this WARN; covered only by key-name check there. `git ls-tree` roots are repo-relative by convention.
- `polarity_check` covers polarity only; the (f) "no shared fixed label" clause and per-check label-keying are
  not tested. Unknown finding reasons → exit 2 (conservative); `--body-reason` extends the vocabulary.
- Not verified: round-37 C1 key polarity (the key is sealed; check takes `--body-bullets`/`--body-reason` and
  could run post-reveal). Exit-2 paths exercised: missing report/key/no-arg → 2.
- No installs (stdlib only); no pacman (pause honored); no lane writes except this report; sealed tree untouched.
