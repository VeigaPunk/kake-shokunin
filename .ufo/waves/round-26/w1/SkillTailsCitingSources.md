# Skill tails and citing statements: freshness recheck (round 26, w1)

Lane `KakeR25.SkillTailsCitingSources-6` · milestone `r26-recheck-build` · axis: freshness. Operability is not in play: no tool or command is in scope.

Targets: `SKILL.md` and `corpus/README.md` lines that carry an `r20-correction` tail or cite S001–S013 / S020–S034. Evidence: `.ufo/waves/round-26/fetched/` (`manifest.json`, `manifest-retry.json`, text views in `fetched/text/`). Fetch times 2026-10-21T15:09:32Z to 15:10:52Z.

## 1. Result

| Verdict | Count |
|---|---|
| HOLD | 7 |
| STALE | 4 |
| UNVERIFIABLE | 0 |

- The four STALE rows (1, 3, 5, 7) are base clauses of r20 lines: `SKILL.md:16`, `SKILL.md:229`, `corpus/README.md:28`, `corpus/README.md:60`. Each base clause is wrong today. Each sits on a line whose appended `r20-correction` tail already states the correction, and every tail re-verifies (HOLD). No new correction text is required.
- No edit to `SKILL.md` or `corpus/README.md` is proposed. No original line is rewritten by this report.

## 2. Method and integrity checks

1. Raw bytes: for each of the 17 retained bodies used (S001-1, S001-2, S002-1, S002-2, S003-1, S004-1, S005-1, S006-1, S007-1, S020-1, S021-1, S022-1 (supplementary), S026-1, S027-1, S032-1, S033-1, S034-1), the sha256 of the gunzipped body equals the manifest sha256.
2. Text views: regenerating each view from its raw body with the `source_text.py` logic is byte-identical to the saved `fetched/text/<id>.txt` for the same 17 bodies.
3. Quotes: every quote below is an exact substring of its text view (exact string test), 6–25 words each.
4. Anchors: HTML and RFC anchors are headings or grammar lines located in the text view; offsets are character offsets into that view. S001 anchors are line numbers of the raw `action.yml` bodies.
5. Fetch identities: S001 index 1 = commit `7b1f4a7` (v4.0.0 `action.yml`); index 2 = commit `5f327015` (main). S002 index 1 = release v4.0.0; index 2 = release v5.0.0.
6. Duplicate bytes: S033-1 and S028-1 are the same RFC 9110 text body (sha256 `21c1cdce…`). Nothing here depends on the duplication.
7. Scope hygiene: the grep sweep returned incidental hits in round-21 and round-24 receipt files. They were not opened, used, or re-run. The full `SKILL.md` read showed round-23/24 sections; none is used as evidence here.
8. Tooling: no tool was installed or updated. Verification used the Python standard library in an in-memory kernel. Nothing was written outside this report. No site, property, browser, account or credential was used, and this lane made no network request.

## 3. Scope

- Evaluated (explicit S-ids or r20 tails): `SKILL.md:16`, `:229`, `:396`, `:540`; `corpus/README.md:28`, `:60`, `:129`.
- Not evaluated, out of range or excluded from re-fetch: `SKILL.md:381` and `corpus/README.md:112` cite S019 (own-work row, excluded from fetch). `SKILL.md:544` and `corpus/README.md:151` cite S035 (outside S001–S013/S020–S034, excluded from fetch).
- Not counted, implicit summaries with no S-id on the line: `corpus/README.md:37` (served-set summary) and `:42` (static-canonical summary). Checked against the same rows as a side note, both still hold (S001-1, S001-2, S002-1, S006-1; S021, S022, S026, S027).

## 4. Statement table

Verdict key: HOLD means the row's teaches and scope are still supported at the anchor. STALE means the statement is wrong at its anchor today. UNVERIFIABLE means the retained bytes cannot decide.

| # | file:line | statement | cited rows (fetchIndex) | verdict | verbatim quote(s), text view | anchorObserved | reason | correction |
|---|---|---|---|---|---|---|---|---|
| 1 | `SKILL.md:16` (base, before tail) | "GH Actions on push to `main` (`CNAME` = ds4cc.com)": presents the repo CNAME as the domain source | none on base; same-line tail cites S005, S003, S007 (row 2) | STALE | S005-1: "If you are publishing from a custom GitHub Actions workflow, no CNAME file is created, and any existing CNAME file is ignored" | S005 "Configuring an apex domain" section, offset 3258 | Under a custom Actions workflow the repo CNAME is ignored (S005). The base implication is wrong for Actions publishing. The repository file's own bytes are not fetched by this lane and are not decided here. | None new. The same-line appended tail (row 2) is the correction; the base line is unchanged. |
| 2 | `SKILL.md:16` (tail T-CNAME, §5) | a repo CNAME sets the domain only for branch publishing; under Actions it is ignored and the domain is a Pages setting (`cname` in the REST API) | S005 (1), S003 (1), S007 (1) | HOLD | S005-1: "this will create a commit that adds a CNAME file directly to the root of your source branch." / S005-1: "Under "Custom domain", type your custom domain, then click Save." / S003-1: "A CNAME file in your repository file does not automatically add or remove a custom domain." / S007-1: "cname string or null Specify a custom domain for the repository." | S005 "Configuring an apex domain": save step at 3053, branch sentence at 3165, Actions sentence at 3258. S003 note under "Creating a custom GitHub Actions workflow" (heading 6276, note 7517). S007 "Update information about a GitHub Pages site" body parameters (heading 9163, `cname` at 10365). | Each clause still matches. Actions ignores a repo CNAME (S005). The domain is set in repository Pages settings (S005) or through the API (S003 note). `cname` is a Pages API body field (S007). "Only" for branch publishing is inferred; see §6. | None (HOLD). |
| 3 | `SKILL.md:229` (base, before tail) | GHP live-only orphans impossible by construction (deploy artifact = full tree snapshot) | none on base; same-line tail cites S001, S002, S004, S006 (row 4) | STALE | S002-1: "Potentially breaking change: hidden files (specifically dotfiles) will not be included in the artifact" | S002 v4.0.0 "What's Changed" (offset 2613); S001-1 raw lines 33–35 | The served artifact is not a full tree snapshot. The archive step passes `--exclude=.git`, `--exclude=.github` and a dotfile pattern (S001-1; S001-2 lines 37–39). v4.0.0 documents dotfiles as excluded (S002-1). | None new. The same-line tail (row 4) is the correction. |
| 4 | `SKILL.md:229` (tail T-ORPHAN, §5) | the orphan direction must be checked against the actual uploaded/deployed artifact, not the checkout; upload-pages-artifact excludes .git/.github; v4 excludes hidden paths by default (v5 adds include-hidden-files); branch builds also apply Jekyll's default exclusions | S001 (1, 2), S002 (1, 2), S004 (1), S006 (1) | HOLD | S001-2: "Include hidden files and directories (those starting with a dot) in the artifact. Excludes.git and.github regardless." / S002-1: "Potentially breaking change: hidden files (specifically dotfiles) will not be included in the artifact" / S002-2: "Changelog Update upload-artifact action to version 7 @Tom-van-Woudenberg (#139) feat: add include-hidden-files input @jonchurch (#137)" / S004-1: "The GitHub Pages artifact should be a compressed gzip archive containing a single tar file." / S006-1: "By default, Jekyll doesn't build files or folders that: Are located in a folder called /node_modules or /vendor" | S001-2 raw line 17 (`include-hidden-files:`) and lines 37–39 (Linux archive step). S002-2 "Changelog" (2623). S004 "Configuring the upload-pages-artifact action" (2617). S006 "Configuring Jekyll in your GitHub Pages site" (heading 2302; default list 2781). | Sub-claims: (a) .git/.github excluded: holds in v4.0.0 (S001-1 lines 33–35) and main (S001-2 lines 37–38). (b) v4 excludes hidden paths: holds (S002-1; the S001-1 pattern is unconditional). (c) v5 adds include-hidden-files: holds (S002-2; input at S001-2 line 17). (d) Jekyll default exclusions: holds as Jekyll's documented default (S006); the "branch builds" scope is inferred (§6). (e) artifact, not checkout: holds (S004 defines the Pages artifact as one gzip-compressed tar). | None (HOLD). |
| 5 | `corpus/README.md:28` (base, before tail) | GHP orphan impossibility proof (deploy = full-tree artifact) | none on base; same-line tail cites S001, S002, S004, S006 (row 6) | STALE | S002-1: "Potentially breaking change: hidden files (specifically dotfiles) will not be included in the artifact" | as row 3 | as row 3 | None new. Row 6 is the correction. |
| 6 | `corpus/README.md:28` (tail T-ORPHAN, §5) | as row 4 | as row 4 | HOLD | as row 4 | as row 4 | as row 4 | None (HOLD). |
| 7 | `corpus/README.md:60` (base, before tail) | GHP Pages deploys are full-tree artifacts, so the served set ≡ `origin/main` tree | none on base; same-line tail cites S001, S002, S004, S006 (row 8) | STALE | S002-1: "Potentially breaking change: hidden files (specifically dotfiles) will not be included in the artifact" | as row 3 | as row 3 | None new. Row 8 is the correction. |
| 8 | `corpus/README.md:60` (tail T-ORPHAN, §5) | as row 4 | as row 4 | HOLD | as row 4 | as row 4 | as row 4 | None (HOLD). |
| 9 | `SKILL.md:396` | "Use `corpus/knowledge/static-canonical-preflight.md` (S020/S021/S026/S027) for a source-backed offline publisher-policy check … Canonical declarations are signals, not guarantees of Google's selection." | S020 (1), S021 (1), S026 (1), S027 (1) | HOLD | S021-1: "A strong signal that the specified URL should become canonical." / S026-1: "This parser does not check that end tags match start tags" / S027-1: "Warning urlsplit() does not perform validation. See URL parsing security for details." / S020-1: "Exist on a different hostname or domain." | S021 heading "How to specify a canonical URL with rel="canonical" and other methods" (6550; signal list 6952). S026 HTMLParser class description (1546). S027 `urlsplit` "Warning" (7261). S020 §3 "The Canonical Link Relation", MAY list (heading 2925; 3605). | The cited rows still carry the taught content at their anchors. "Signal" is S021's own term. The non-guarantee clause is carried by S022 (fetchIndex 1), which this line does not cite: "Even if you explicitly designate a canonical page, Google might choose a different canonical" (offset 6540). | None (HOLD). Optional citation addition in §6. |
| 10 | `corpus/README.md:129` | Canonical signals now have a source-backed knowledge entry `knowledge/static-canonical-preflight.md` (S020/S021/S026/S027) | S020 (1), S021 (1), S026 (1), S027 (1) | HOLD | as row 9 | as row 9 | Each cited row's teaches still holds at its anchor. | None (HOLD). |
| 11 | `SKILL.md:540` | "Source rationale and exact per-field limits: … Receipt replay hardening (S032–S034)." | S032 (1), S033 (1), S034 (1) | HOLD | S032-1: "full-time = partial-time time-offset date-time = full-date "T" full-time" / S033-1: "media-type = type "/" subtype parameters type = token subtype = token" / S034-1: "The names within an object SHOULD be unique." / S034-1: "Numeric values that cannot be represented in the grammar below (such as Infinity and NaN) are not permitted." | RFC 3339 §5.6 "Internet Date/Time Format" (14397; grammar 15088), §5.7 "Restrictions" (16005). RFC 9110 §8.3.1 "Media Type" (126997; grammar 127331), §5.6.6 "Parameters" (75771). RFC 8259 §3 "Values" (8232), §4 "Objects" (8863), §6 "Numbers" (10717), §9 "Parsers" (16082). | The sections the entry cites (RFC 3339 §5.6–5.7; RFC 9110 §8.3.1 and §5.6.6; RFC 8259 §3/4/6/9) are present with the grammar and limits the entry relies on. The line's second sentence is a scope statement with no source row; it is not judged. | None (HOLD). |

## 5. Exact tail texts (verbatim, for reference)

T-CNAME, `SKILL.md:16`:

`**[r20-correction 2026-10-19: a repo CNAME sets the domain only for branch publishing; under Actions it is ignored and the domain is a Pages setting (`cname` in the REST API) — S005, S003, S007]**`

T-ORPHAN, `SKILL.md:229`, `corpus/README.md:28` and `corpus/README.md:60` (identical text):

`**[r20-correction 2026-10-19: the orphan direction must be checked against the actual uploaded/deployed artifact or build output, not inferred from the checkout; upload-pages-artifact excludes .git/.github and v4 excludes hidden paths by default (v5 adds include-hidden-files); branch builds also apply Jekyll's default exclusions — S001, S002, S004, S006]**`

## 6. Precision notes (no verdict change)

- Row 2: the rows never say "only" for branch publishing. S005 says branch publishing "will create a commit that adds a CNAME file", and S003 says a repo CNAME "does not automatically add or remove a custom domain". The exclusivity is an inference from that contrast.
- Row 4(b): "by default" understates v4.0.0. Its `action.yml` has no override input, so the dotfile exclusion is unconditional there. Not stale.
- Row 4(d): the S006 default-exclusion sentence names Jekyll builds, not "branch builds". The branch scope is inferred from the page's Jekyll and branch wording.
- Row 9: the explicit non-guarantee wording is in S022, and S022 says "might" where the registry paraphrases "may". Optional citation addition for L1, not a correction: S022 could be added to the `SKILL.md:396` citation list.
- Row 10: S026 and S027 text reads "Python 3.15.1"; the registry row says "Python 3.15 documentation". Version wording only.
- Row 1: this lane did not fetch the ds4cc repository file. The verdict rests on the documented mechanism. Live Pages settings (custom-domain state, `build_type`) were not observed; only the documented mechanism was re-checked.
- Row 2: the registry's "step 4" numbering does not appear in the S005 text view. The anchor is the section, not the step number.

## 7. Summary

```json
{"statements":11,"hold":7,"stale":4}
```
