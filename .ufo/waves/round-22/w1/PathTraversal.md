# Kake r22 w1 — PathTraversal surgical design review

Seat: `KakeR22.PathTraversal` (reviewer, read-only; leaf — no subagents). Axis: operability. Milestone: offline-canonical-capability.
Scope: file-resolution confinement of `scripts/canonical_audit.py` as specified by the frozen contract — manifest `file` fields must resolve relative to the manifest directory, regular files only, reject symlinks and traversal, no network/writes in normal mode.

## Sources read (grounding; no unseen code claimed)

- `.ufo/waves/round-22/contract.json` (frozen): `interface.fileResolution`, `interface.findingIds`, `outputs.exitMap`, matrix case list.
- `.ufo/waves/round-22/w1-spec.json` items `Implement` ("Safe regular file resolution"), `Matrix`, `Measure` (raw lines 14–24).
- `/tmp/kake-r22-Matrix/.ufo/waves/round-22/cases.json` — all 32 frozen cases; in scope: `manifest_traversal` → exit 2 / `input_invalid`, `symlink_html` → exit 2 / `input_invalid`, `missing_head` → exit 2 / `html_unsupported`.
- `/tmp/kake-r22-Matrix/.ufo/waves/round-22/matrix.py` (lines 30–75): runtime-only symlink construction and `finding_id()` comma-join.
- Fixtures: `fixtures/manifest_traversal/manifest.json` = `{"version":1,"pages":[{"url":"https://example.test/project/a.html","file":"../escape.html",...}]}`; `fixtures/symlink_html/manifest.json` points at `linked.html`, symlink created at runtime → sibling `target.html` (intra-root).
- Lane base `scripts/` contains only `corpus-contract.mjs`, `freshness-sweep.mjs`, `probe-delta.mjs`; `/tmp/kake-r22-Implement/scripts/` had no `canonical_audit.py` when this review was written. **Findings below are design requirements/falsifiers, not claims about written code.** A candidate implementation appeared afterwards; a static, non-executing inspection pass against these findings was appended at "Candidate static inspection" — nothing was run.

Godspeed axes for this seat: (a) confinement soundness, (b) deterministic ids/exits, (c) fail-loud (no false green), (d) offline purity, (e) matrix operability. No tool installs performed.

## Findings by severity

### HIGH

**H1 — Exit-code collision: uncaught exceptions exit 1, indistinguishable from "failed policy".**
Any resolution error raised outside a guard — `ValueError` on NUL in path, `UnicodeEncodeError` from JSON lone surrogates, `NotADirectoryError`/`OSError` from a trailing-slash `file` like `"a.html/"`, `PermissionError` on unreadable file — makes CPython exit 1 with a traceback. The contract exitMap reserves 1 for policy failure and 2 for could-not-evaluate. Required: every per-page resolution+read wrapped in `except (ValueError, OSError, UnicodeError)` → `input_invalid`, exit 2, JSON verdict still on stdout. This is the single cheapest way the capability silently lies.

**H2 — String containment is not confinement.**
`normpath`/`abspath` + `startswith` checks (i) pass sibling-prefix dirs (`startswith(root)` true for `root-evil/`) unless `os.path.commonpath` (never `commonprefix`) is used, and (ii) miss intermediate-component symlinks: `file: "link/b.html"` with `link → /tmp/evil` contains no `..` yet resolves outside the manifest dir. Required shape: reject any `file` value that is absolute, empty, or contains a `..` path component (textual, no normalization, no `unquote`), *then* `os.path.realpath` both sides and require `commonpath([real, realpath(manifest_dir)]) == realpath(manifest_dir)`, *then* require the final target to be a regular file and not a symlink. Defense in depth is required because no single one of these layers covers H3.

**H3 — The frozen `symlink_html` case is intra-root only; a containment-only implementation false-greens it.**
`matrix.py:30-48` builds the runtime symlink as `linked.html → target.html` inside the same temp dir. An implementation that resolves symlinks (realpath) and only checks containment reads `target.html` (contained, regular-after-resolution) and can pass policy — while remaining fully vulnerable to an escaping symlink `linked.html → ../outside.html`. The escape variant is in no frozen case. Compensating controls: falsifiers F2/F3 below; recommend a wave2 case `symlink_escape`. Acceptance must be "rejected *because* it is a symlink" (lstat), not "rejected because realpath left the room".

### MEDIUM

**M1 — Contract leaves the resolution-failure finding id unpinned; three seats must agree.**
`findingIds` contains both `input_invalid` and `html_unsupported` but the contract text maps neither to file-resolution violations. The frozen matrix already rules: `manifest_traversal`/`symlink_html` → `input_invalid`; `missing_head` → `html_unsupported`. Stable ruling to adopt everywhere (Implement selftest, cases.json, any docs): all resolution-time failures (traversal, symlink, absolute, empty, directory, missing, unreadable, NUL, bad encoding of the *path*) → `input_invalid`, exit 2; parse-shape failures of *file content* (no explicit head, undecodable bytes) → `html_unsupported`, exit 2. Any divergence between Implement's selftest and Matrix's cases.json is an L1 integration failure even if both "pass" alone.

**M2 — The traversal fixture can be passed for the wrong reason (absence, not policy).**
`file: "../escape.html"` resolves to `fixtures/escape.html`, which does not exist. An implementation that normalizes `..` away and then reports any missing file as `input_invalid`/2 passes the frozen case while enforcing zero confinement. Discriminator: F1 below (make the escape target exist and be valid).

**M3 — Ungated resolution edges, each `input_invalid`/2, none in the matrix:** absolute `file` (`/etc/passwd`), empty string (normalizes to the manifest directory itself — a directory, must not be "clean"), `"."`/`".."`, trailing slash, NUL byte, directory-as-file, unreadable file, percent-encoded names (must stay literal — see M5), case-sensitive POSIX matching (never `lower()` a path). Cheap wave2 matrix extension; today the contract's word "reject" is the only guard.

**M4 — Fail-fast vs collect-all is unpinned and the matrix masks it.**
`matrix.py:50-72` joins multiple finding ids with `","`, and every fixture is single-page — so an implementation that continues past a resolution failure and emits `input_invalid` plus other pages' policy findings would still be single-id today but unstable on any multi-page manifest. Ruling adopted (Implement seat, 2026-10-20): collect one finding per page and continue; any `input_invalid` in the run ⇒ verdict could-not-evaluate with exit-2 precedence. Contract- and matrix-compatible: single-page frozen fixtures keep the `finding_id()` comma-join unreachable, and multi-page manifests may legitimately emit multiple ids.

**M5 — Never decode the `file` field.** It is a filesystem path, not a URL: `urllib.parse.unquote("%2e%2e%2fsecret")` manufactures a traversal the manifest author never wrote, and `urljoin` on paths invites the same. Literal bytes only; percent-encoded names simply won't exist → missing → `input_invalid`.

### LOW

**L1 — TOCTOU residual:** lstat-then-open is racy in principle; out of scope for an offline, operator-owned tree. Strict hardening (not a gate): `os.open(path, O_RDONLY | O_NOFOLLOW)` + `fstat` `S_ISREG`, or a `dir_fd` component walk with `O_NOFOLLOW|O_DIRECTORY` for intermediates. Record as hardening, do not gate r22 on it.

**L2 — Manifest path itself is operator input:** `--manifest` may legitimately be a symlink or live anywhere; the confinement rule scopes page `file` fields only. State that explicitly to avoid an overbroad implementation rejecting its own entry point.

**L3 — `pages: []`:** a preflight that reports `clean`/exit 0 on zero pages is a typo-away-from-publish false green. Ruled `input_invalid`/2 by the Implement seat (2026-10-20); not represented in the frozen matrix.

**L4 — Hardlink aliasing:** a hardlink inside the root pointing at outside content is a regular contained file; contract is silent. Offline preflight reading it is harmless; note only, no gate.

**L5 — Measure/materialization interplay:** fixtures commit no symlinks (Matrix builds them at runtime), so git-blob materialization cannot silently downgrade the symlink case to a regular-file case *today*. If that invariant ever changes, `symlink_html` becomes non-probative at measure time. Also flag to Measure: set `PYTHONDONTWRITEBYTECODE=1` so runs in read-only or hash-verified trees don't create `__pycache__` (offline-purity axis).

## Expected stable finding ids (this seat's scope)

| Input condition | finding id | exit |
|---|---|---|
| `file` escapes manifest dir (`../…`, absolute, or realpath escape) | `input_invalid` | 2 |
| `file` names a symlink (final component — frozen `symlink_html`) | `input_invalid` | 2 |
| intermediate-component symlink (ungated; pin strict-reject) | `input_invalid` | 2 |
| missing file / directory / empty `file` / NUL / unreadable / bad path encoding (ungated) | `input_invalid` | 2 |
| content-shape failures (no explicit head, undecodable bytes) — boundary with HeadBoundary | `html_unsupported` | 2 |

## Minimum acceptance / rejection pair

- **ACCEPT:** temp root with regular `a.html` whose head carries `rel=canonical https://example.test/project/a.html`; manifest `{"version":1,"pages":[{"url":"https://example.test/project/a.html","file":"a.html","expectedCanonical":"https://example.test/project/a.html"}]}` → exit 0, verdict clean, `pagesChecked` 1, `findings` empty.
- **REJECT:** same root; copy a fully valid canonical page to `parent/escape.html`; manifest page `"file": "../escape.html"` → exit 2, `findings` contains `{"id":"input_invalid"}` naming that page's url, and the escape file's canonical marker never appears in stdout (proves it was not read).

## Bounded falsification recipe (post-integration; temp dirs, no network, minutes)

- **F0** Run the acceptance/rejection pair above verbatim.
- **F1 (policy vs absence):** create the traversal target: next to `fixtures/manifest_traversal/` place `escape.html` containing a *fully valid* canonical page; rerun the case (or CLI on that manifest). Policy implementation: still exit 2 `input_invalid`. Normalize-first implementation: reads it and emits 0/1 → false green proven.
- **F2 (escaping symlink):** temp `root/{manifest.json, outside.html(valid)}`, `os.symlink("../outside.html", "root/link.html")`, page `"file": "link.html"` → expect exit 2 `input_invalid`; a realpath-containment-only implementation fails this.
- **F3 (intermediate symlink):** `root/sub/a.html` (valid, real dir); `root/link → /tmp/evil-dir` containing `b.html` (valid); page `"file": "link/b.html"` → strict pin expects `input_invalid`; containment-only yields a policy verdict — escalate to L1 for the ruling, don't silently accept either.
- **F4 (exception collision):** page `"file": "a.html/"` and `"file": "\u0000.html"` → both must print the JSON verdict and exit 2; any traceback + exit 1 = H1 confirmed.
- **F5 (no writes):** `find root -exec sha256sum {} + > before`; run; diff after; plus `PYTHONDONTWRITEBYTECODE=1`. Byte-identical tree required.

## Residual risk and verification gaps

- Design review preceded the candidate; the post-review static inspection (below) checked resolution code as written, without executing it. Untested and unintegrated — falsifiers F0–F5 remain L1's acceptance probes.
- M1 and L3 are pinned and now statically confirmed in the candidate (selftest maps traversal/symlink to `input_invalid`/2; empty `pages` rejected). M3's edges are statically rejected in the candidate (absolute/ntpath/drive/backslash, empty/dot/dot-dot components, non-regular files, oversize → `html_unsupported`) but remain absent from the frozen matrix — wave2 extension candidates. Final integration pin rests with L1; Implement and Matrix can still each be internally consistent and mutually wrong until L1 compares them.
- TOCTOU and hardlink aliasing remain ungated by design (offline threat model); F2/F3 cover the deterministic symlink attacks, not races.
- Falsifiers are specified, not executed (read-only seat, "no tests yet"); L1 should run F0–F5 after integration and record results in the wave report.

## Candidate static inspection (post-review, non-executing, 2026-10-20)

Candidate `/tmp/kake-r22-Implement/scripts/canonical_audit.py` (824 lines) inspected statically against the findings above. Line cites are that file.

| Finding | Status in candidate | Evidence |
|---|---|---|
| H1 exception collision | Addressed | Per-page guard `except (InputProblem, OSError, UnicodeError, ValueError)` → `input_invalid`; input findings force could-not-evaluate/exit 2 (`audit_manifest`, 612–641); `main` prints JSON only (809–821) |
| H2 containment | Addressed, stronger than required | Textual layer rejects absolute/ntpath-abs/drive/backslash (478–486) and empty/dot/dot-dot components (487–489); then dirfd walk `O_DIRECTORY\|O_NOFOLLOW` per component + `dir_fd` (491–502) — links are never followed, so `realpath`/`commonpath` layers are unnecessary by construction |
| H3 symlink escape | Addressed | Final open `O_NOFOLLOW\|O_NONBLOCK` (504–509); ELOOP → `input_invalid`; `fstat` S_ISREG (511–513); fifo selftest case present |
| M2 policy-vs-absence | Addressed by construction | Component check fires before any stat/read; selftest additionally plants a real `../outside.html` (733–736) — F1's discriminator is embedded |
| M4 fail semantics | Ruling implemented | Loop collects one finding per page and continues; exit-2 precedence (612–641) |
| M5 no decode | Addressed | Resolution is pure string split + `os.open`; no `unquote`/`urljoin` in the path layer |
| L1 hardening | Adopted | Full dirfd no-follow chain; bounded reads 2 MiB HTML / 1 MiB manifest (`read_bounded_fd` 445–457) |
| L2 manifest scope | Addressed | Manifest opened without `O_NOFOLLOW` (461) but must fstat-regular (463–464) — symlinked manifest allowed by design |
| L3 empty pages | Ruled + implemented | `_validate_manifest` 581–582 → `input_invalid`/2; selftest asserts it (775–791) |
| M1 id mapping | Matches frozen matrix | `../escape.html` → `input_invalid`/2; final symlink → `input_invalid`/2 — both as `cases.json` pins |

**New finding (LOW, H1-class residue):** the manifest-load guard (607–615) does not catch `RecursionError`; `json.loads` on a ≤1 MiB deeply nested manifest raises it uncaught → traceback + exit 1, colliding with failed-policy — the exact H1 class, narrow trigger (offline operator-owned input). Cheap fix: add `RecursionError` to that except tuple. MemoryError left out of scope.

**Definitional note (not a defect):** `pagesChecked` counts only pages that reached evaluation (manifest-level failure → 0). Contract does not define it and the matrix does not assert it; L1 should record the semantics.

Falsifier status: F0–F5 remain unexecuted; selftest already embeds F1/F2/F3-equivalents (planted outside file, `alias→real` parent-dir symlink, final-component symlink, fifo) and F4's trailing-slash case is rejected at component level. Static inspection is not execution — L1 still runs F0–F5 plus the frozen matrix.

Report trailer: `.ufo/waves/round-22/w1/PathTraversal.md`
