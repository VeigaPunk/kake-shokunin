# MetadataSafety — kake round 21 w1 (sentinel)

Scope: `corpus/knowledge/fire-journal-codes.md` and `corpus/knowledge/publish-queue.md`.
Question: which source/recheck text can be used without credentials and behind an operator gate.
Writes: this report only. Tools installed: none. No command quoted in either entry was run.

## Observation timeline (honest)

1. I first read both files at their base form (`fire-journal-codes.md#88F8` matches
   `.ufo/waves/round-21/frozen/before/`; neither had a provenance trio).
2. During this audit, scribes Knowledge03 and Knowledge18 landed prefixes. `git diff 5009ecaa -- <both>`
   shows **4 insertions, 0 deletions per file**: a pure prefix of three trio lines plus a blank line.
   Every original line is now shifted +4. The line numbers below are **current** (post-prefix).
3. Commands I ran myself (none were taken from the entries):
   - a `test -e` loop over the cited roots;
   - `git diff`/`git status` on the two targets;
   - `grep -c S019 corpus/SOURCES.md`;
   - `test -e` on S019's canonical input.

   Disclosure: one path in my stat loop is the same as the first clause of the new fire-journal recheck,
   `test -e ~/Projects/webzites/scripts/kimi-surface.mjs`. I ran it before that prefix existed, as my own
   existence check. I did not execute it from the entry.

Existence results (2026-10-20, stat only, no content read):

| Path | Status |
|---|---|
| `~/Projects/webzites` and its `scripts/kimi-surface.mjs`, `state`, `fleet`, `reports` | ABSENT |
| `~/Projects/plazir-15-site` | ABSENT |
| `~/Projects/origin-work` | ABSENT |
| `~/Projects/origin-work/charter-ufo-fsd` | ABSENT |
| `~/Projects/ds4cc-marketplace` | ABSENT |
| `/tmp/kake-r14` | ABSENT |
| `/tmp/kake-r16` | PRESENT (scratch) |
| Lane `state/`, `fleet/`, `reports/`, `src/` | ABSENT |
| `corpus/CORPUS.md` | ABSENT |
| `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/CORPUS.md` (S019 canonical input) | PRESENT |
| `corpus/SOURCES.md` S019 row | present; file uncommitted-modified by L1 |

The whole `~/Projects/webzites` root is gone. The in-entry absence flags (r20 at fire-journal:8; r18
at publish-queue:7, :192, :250; r20 at publish-queue:267) are therefore an under-count, not wrong.
The prefixes' "sources absent" generalization is grounded by this stat.

## Verdict on landed metadata

| Field | fire-journal-codes.md (L1–3) | publish-queue.md (L1–3) |
|---|---|---|
| source | SAFE. Pure citation, no command. Defect F2. | SAFE as a citation. Defects F1 and F4. |
| verified-at | SAFE and honest: historical-not-live-reverified, no today-as-domain-recheck. Defect F3a. | SAFE and honest; states "no live domain recheck performed this round". Defect F3b. |
| recheck | **SAFE for credential-free, operator-gated use**: `test -e` stat plus `grep -lE '"fire": *true'` over the narrow glob `~/Projects/webzites/state/recreate-plazir15-*.json`. Local only, no network, no metered or mutating verb. `-l` prints filenames, never journal content. Restore-or-retire gate present. | **SAFE for credential-free, operator-gated use**: `for … test -e` stat loop over two paths. Local, no network, no content read. Restore-or-retire gate present. |

Neither recheck touches the network, a browser session, a git remote, credential or auth files, or a
metered kimi verb. If the sources stay absent, both are harmless: they print "absent", or grep errors
because the glob doesn't expand.

## Findings

### F1 — Low-Medium: wrong S019 provenance path in publish-queue `source:` (fabricated readiness)

- **Evidence:** publish-queue.md:1 reads `S019 (metadata contract only, corpus/CORPUS.md registered by L1 this round; …)`.
  Per the lane rule, `corpus/CORPUS.md` resolves to `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/CORPUS.md`,
  and that file is ABSENT.
- **What S019 actually names:** SOURCES.md:27 gives the canonical input as
  `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/CORPUS.md`, which is PRESENT.
- **Exploit path:** a reader or verifier that follows the source path gets ENOENT. Worse, a later round
  could create a lane-local `corpus/CORPUS.md` that was never the S019 contract, and the field would
  silently bind to it.
- **Smallest fix:** replace that parenthetical with `S019 (corpus/SOURCES.md; metadata contract only, not platform authority)`.
  Don't name a path, or name S019's canonical input exactly. This is a prefix-line-only edit and stays
  a pure prefix versus base. Owner: Knowledge18 / L1.

### F2 — Low: bare webzites-relative path in fire-journal `source:`

- **Evidence:** fire-journal-codes.md:1 has `… + state/rebuild-charter-fire.log (own-work; …)`. The two
  sibling paths are anchored to `~/Projects/webzites/`; this one is bare. Under the lane rule it resolves
  to `kake-shokunin/state/rebuild-charter-fire.log` (lane `state/` is ABSENT), not the real
  `~/Projects/webzites/state/…`.
- **Note:** the body's line 10 has the same bare form, but that is a preserved historical line. Don't touch it.
- **Fix:** write `~/Projects/webzites/state/rebuild-charter-fire.log` in the prefix.

### F3 — Low: verified-at slightly understates the latest evidence round (honesty, not safety)

- **F3a, fire-journal:2:** says `2026-09-28 … journals 2026-09-26/09-27`. But the body's top-level key
  list (:12–18) and the plazir15 `×3` re-count (:60) are explicitly **r16** measurements. The r16 date
  (2026-09-29T02:1x–02:3xZ) appears only in publish-queue.md:243, not in this entry.
  - Fix: append `; r16 re-count of key list and ×3 fires (r16 = 2026-09-29 per publish-queue.md)`.
- **F3b, publish-queue:2:** calls r16 the `latest in-entry live read`. But :261–262 record a later
  **r17** ETag sampler (`6ab49126-1365d` in 8/8 fetches). r17 is undated in-entry.
  - Fix: `r16 … (r17 ETag sampler later, undated in-entry)`. Or drop "latest".

### F4 — Low: publish-queue `source:` omits the entry's primary "Source queue"

- **Evidence:** :7 names `~/Projects/webzites/fleet/fleet.dedupe-report.md` (r1 lines 46–57, r2 lines 89–106)
  as the source queue. The prefix lists config, reports and kimi-map, but not this file.
- **Fix:** add `fleet/fleet.dedupe-report.md (r1 46–57, r2 89–106)` to the `under ~/Projects/webzites:` list.
- **[INFERENCE]** A comma-splitting parser (for example a citation scanner) may read the prefix's
  `fleet/…`, `reports/…`, `state/…` items as lane-relative. Spelling each one with `~/Projects/webzites/`
  avoids that. I did not read the scanner.

## Body text that must never be promoted into `source:`/`recheck:`

Each entry below fails credential-free, operator-gated use. It is preserved history: leave it in the body,
but never lift it into metadata or run it from metadata.

| Class | Locations (current lines) | Why unsafe |
|---|---|---|
| Metered or mutating retries | fire-journal:26–33 (`retry`, `retry freely`, `retry once`, `refire`); :62–63 (`safe to re-run`); :67–70 | Re-invokes `recreate`/`rebuild`/`update`, which can spend a metered fire. Codes 4, 6 and 7 may already have consumed one. |
| Browser and auth session | fire-journal:27 (`browser ensure`); :32 (`operator re-login` + `browser status`); publish-queue:29 and :131 (CDP :9222) | Needs a logged-in kimi session over CDP, i.e. credential-bearing state. |
| Authenticated kimi RPC / map sweep | fire-journal:28, :75 (`kimi-map`, `GetWebsiteByChatID`); publish-queue:25, 27, 28, 69, 130–132 | Session-authenticated RPC. The entry itself (:132–133) forbids gating on E5. |
| Vanished-tool verbs | publish-queue:26, :75, :124 (`sync-check`) | `kimi-surface.mjs` is absent, so whether it needs auth can't be checked. Exclude it. |
| Operator-owned publish actions | publish-queue:28–29 (Publish click, `SetWebsiteSlug`); :38 (`git push origin main`); PQ-12 `fleet.config.json:256` edit | Publishing and deploys are operator-owned under the contract. |
| Git network operations | publish-queue:171 (`git pull`/`fetch`); r15 and r16 `ls-remote`; :178 (GitHub trees API) | They can invoke a git credential helper or gh token. The pulls also write, which the entry itself gates at :171–172. |
| Domain network reads | publish-queue:153 (`curl` + `grep -o 'scribe beat[^<]*'`); :170 (raw.githubusercontent); every "live GET" | Credential-free, but this round forbids domain network reads. Usable later only behind an explicit operator gate. |
| Local but stale or absent | publish-queue:27 (`git status -sb`); :38 (`git rev-list --count origin/main..HEAD`, `git show origin/main:<path>`); :94 (`git ls-tree origin/main`); :160 (`systemctl --user list-timers webzites-probe.timer`) | Credential-free and read-only, but every target repo is ABSENT. Remote-tracking refs are frozen without a fetch, so these give historical comparison only, never freshness. |
| Scratch, not provenance | publish-queue:26 (`/tmp/kake-r14/pq2-root.html`, ABSENT); :274 (`/tmp/kake-r16/scout-claims.md`, PRESENT but declared non-repo) | Not citable sources. |

Identifiers: chat UUIDs at publish-queue:26–29 and the site-id pin at :34 are binding identifiers, not
secrets. Neither prefix copies them. Keep it that way.

## Safe metadata pattern (for L1/scribes)

- `source:` cites only. Use absolute `~/Projects/webzites/...` paths and keep an absence clause.
  Identify S019 by id, or by its exact canonical input; never `corpus/CORPUS.md`.
- `verified-at:` is the original evidence date and round, plus `historical-not-live-reverified`.
- `recheck:` allows only `test -e`/`ls -d` stat or `grep -l`/`grep -c` over named local files with
  narrow globs. Never `state/*`: unknown siblings could be session or auth material [INFERENCE].
  Add `operator must restore or retire`. No network, no browser, no git remote, no `kimi-surface`
  verb, no `retry`.

Both landed rechecks already fit this pattern. F1–F4 are fixes to source and verified-at only.

## Limitations

- I read no file except the two targets, plus single-line greps of SOURCES.md:27 for S019 and existence stats.
- Whether `sync-check` or the journals carry auth material can't be checked: the sources are gone.
- Line numbers will shift if anyone edits the prefixes again.
- I made no edits to either target, and I sent no peer messages: none of this blocks the wave.
