# round-5 aggregator mirror — PATH-less CLI invocation & undeclared binary prerequisite

- **Repo:** `kake-shokunin` (owner of the file cited below).
- **Filed by:** kotoba round-5 report (2026-09-28), `kotoba-shokunin@4002b9f` §"Cross-domain observations to relay" (item "kake L46"); artifact `kotoba-shokunin/corpus/knowledge/fleet-skill-audit-round5.md` (defect row "kake L46").
- **Mirrored by:** aggregator round-5 (main-repo lane, `m_qwen`) per `PROTOCOL.md` integrator step 2. Aggregator-owned file; the owning lane corrects `SKILL.md`.
- **Pointer provenance:** kotoba's L46/L161 match kake's *round-4* blob (`git -C kake-shokunin show 6b1cd07:SKILL.md | wc -l` → 179; bare `webzites probe --all` at L46; `bin/webzites.mjs` at L161) — the revision current when the audit ran.
- **Safety:** read-only audit; no publish, no probe, no fire, no `git push`.

## Claim — `webzites` invoked bare, bin absent from PATH

`SKILL.md:46` (`6b1cd07`) opens the checklist with `` `webzites probe --all` `` — invoked as a bare command; the CLI's real location is named only in the "Cited paths" trailer (`~/Projects/webzites/bin/webzites.mjs`), with no step declaring it on `PATH` and no prerequisite row for it.

Host verification (2026-09-28): `command -v webzites` → empty (exit 1); `ls ~/.local/bin | grep -i webzites` → no match; `ls -la ~/Projects/webzites/bin/webzites.mjs` → `-rwxr-xr-x 1 vgpnk vgpnk 410 Sep 20 22:42`; `ls ~/Projects/webzites/package.json` → No such file (no root manifest to install a `bin` link from). So every pasted `webzites …` command in this file is non-runnable as written for a reader whose shell lacks the mission root's `bin/` on `PATH`.

## Current-state verification — still open

At **HEAD `9544914`** (round-8, 2026-09-28 16:49:59 -0300; tree clean) the file is 211 lines and the bare invocations remain at L46, L64, L100, L120, L124; the CLI path is named only at L188. Absence sweep for a precedence rule: `grep -n 'PATH' kake-shokunin/SKILL.md` → no match (no `export PATH=…`, no `node <abs-path>` invocation form).

Queue: open routed-defects row in the aggregator ledger (`AGGREGATE.md`) until kake's next steered round lands the correction.

## Falsifiable next check

```
command -v webzites                                  # after the fix: resolves (shim on PATH) — today: empty, exit 1
grep -n 'webzites' kake-shokunin/SKILL.md | head     # L46/L64/L100/L120/L124 bare; L188 names bin/webzites.mjs only
```
