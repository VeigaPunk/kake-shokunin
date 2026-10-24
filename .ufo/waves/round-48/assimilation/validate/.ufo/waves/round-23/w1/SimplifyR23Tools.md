## Verdict

Three CLI-only scripts (~135 + ~123 + ~113 lines) with no Python importers (text search: zero `import live_snapshot` / `from measure_c` in lane). **Safe YAGNI trims** are (1) counter stdout fields not used by `contract.json` exit semantics, (2) `live_snapshot.py` stdout summary fields not written to `live/<id>/`, and (3) narrowing `check_unit`’s return type after (1). **Do not** extract shared helpers, drop redirect enforcement, drop `truncated`/`redirects` fetch metadata, or remove `main(argv=)` hooks — those either add coupling or weaken operability/security evidence. LSP references unavailable (scripts not importable modules); absence of callers verified via repository text search only.

Preserved contract: `measure_c1.py` / `measure_c2.py` exit `0` iff all units/surfaces pass, `1` on partial failure, `2` on bad revision/population; `live_snapshot.py` exit `0` after attempting all surfaces, `2` bad input, `64` usage (observed).

## Findings

### P2 — Counter stdout carries unused aggregates (operability noise)

**Command:** `python3 .ufo/waves/round-23/measure_c1.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --revision HEAD; echo exit=$?`

**Observed:** JSON includes `claimVerdicts` and per-unit `claims` histograms; `accepted=0`, `total=17`, exit `1`.

**Impacted:** C2/C1 operability — operators parsing JSON for pass/fail only; `contract.json` counts by exit code only.

**Fix:** Remove `totals`/`claimVerdicts` and per-row `claims`; keep `revision`, `accepted`, `total`, `units[].{unit,pass,problems}`.

### P2 — C2 counter emits validator digest unused by contract

**Command:** `python3 .ufo/waves/round-23/measure_c2.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --revision HEAD; echo exit=$?`

**Observed:** Top-level `validatorSha256` present; exit `1`, `accepted=0`.

**Impacted:** Operability — redundant with `git show <rev>:scripts/canonical_audit.py | sha256sum` when debugging.

**Fix:** Drop `validatorSha256` from printed JSON.

### P3 — `live_snapshot.py` stdout lists audit finding ids nobody consumes

**Command:** (static) `measure_c2.py` reads only `live/<id>/{fetch,audit,page}.json`; no lane consumer parses `live_snapshot` stdout.

**Observed:** Summary lines include `"findings": ["…"]` built from validator output.

**Impacted:** Operability — extra work per surface; findings remain in `audit.json`.

**Fix:** Omit `findings` from stdout summary; simplify verdict selection (see diff).

### P3 — `check_unit` verdict tally only fed removed stdout (measure_c1)

**Impacted:** Maintainability after P2 fix.

**Fix:** Return `list[str]` problems only; drop `{v:0 for v in VERDICTS}` tally loop.

### HOLD — Do not delete (would harm operability or security axis)

| Candidate | Reason |
|-----------|--------|
| `Redirects` handler + `redirects` in `fetch.json` | Not checked by `measure_c2`, but documents redirect chain for security/forensics (peer security task). |
| `truncated`, `method`, `error` in fetch meta | `measure_c2.served()` depends on `truncated`/`error`/content-type. |
| `not-served` `audit.json` keys `exit`/`error` | Docstring contract; harmless extra keys; `measure_c2` checks only `verdict`+`status`. |
| Temp copy of `canonical_audit.py` in `measure_c2` | Required to reproduce validator at measured revision. |
| `main(argv=None)` on all three | Needed for `counter_selftest.py` / injection without subprocess shell. |
| Shared `git_show()` module | Two call sites; new file + import is negative YAGNI. |
| Shared `served()` between snapshot and counter | Intentional duplication keeps counter independent of fetcher implementation. |

## Checked and held

**Exit semantics (error paths):**

```
measure_c1.py NOTACOMMIT exit 2 expect 2 ok
measure_c2.py NOTACOMMIT exit 2 expect 2 ok
measure_c1.py HEAD exit 1 expect 1 ok
live_snapshot bad pop exit 2 out {"error": "Expecting value: line 1 column 1 (char 0)"}
live_snapshot usage exit 64
```

**Trimmed `measure_c1` mutant in scratch** (`/tmp/kake-r23-SimplifyR23Tools-QyIX/measure_c1.py`, lane unchanged): `mutant_c1_exit=1` matches `orig_c1_exit=1` on HEAD.

**Lane HEAD at probe:** `4e7dd1d4e52dcbdce249dd3dbc8485bc4e23cf4b` (target scripts match candidate `4d95d2e9` for these paths).

**Tooling:** No installs or updates (system `python3` only).

## Limits

- Did not run full `live_snapshot.py` against C2 population (live GETs) or mutation matrix; stdout/diagnostic trims validated by static consumer analysis + exit-code probe only.
- No committed `live/<id>/` receipts at HEAD — cannot exercise `measure_c2` pass path on lane; served-path equality logic held unchanged in proposed diffs.
- Semantic reference proof: text grep only (no Python LSP in scope).

## Proposed diff (integrator applies in clone; not applied to lane)

### `.ufo/waves/round-23/measure_c1.py`

```diff
--- a/.ufo/waves/round-23/measure_c1.py
+++ b/.ufo/waves/round-23/measure_c1.py
@@ -36,7 +36,7 @@ def show(root: str, revision: str, path: str) -> str | None:
     return done.stdout.decode("utf-8") if done.returncode == 0 else None
 
 
-def check_unit(root: str, revision: str, unit: dict[str, str]) -> tuple[list[str], dict[str, int]]:
+def check_unit(root: str, revision: str, unit: dict[str, str]) -> list[str]:
     problems: list[str] = []
-    verdicts = {v: 0 for v in VERDICTS}
     raw = show(root, revision, f"{ROUND}/receipts/{unit['unit']}.json")
     if raw is None:
-        return ["receipt missing"], verdicts
+        return ["receipt missing"]
     try:
         receipt = json.loads(raw)
     except json.JSONDecodeError as exc:
-        return [f"receipt is not JSON: {exc}"], verdicts
+        return [f"receipt is not JSON: {exc}"]
     if not isinstance(receipt, dict):
-        return ["receipt is not an object"], verdicts
+        return ["receipt is not an object"]
     if receipt.get("unit") != unit["unit"] or receipt.get("path") != unit["path"]:
         problems.append("unit/path mismatch")
     if not isinstance(receipt.get("observedAt"), str) or receipt["observedAt"][:10] < "2026-10-21":
         problems.append("observedAt missing or before 2026-10-21")
     claims = receipt.get("claims")
     if not isinstance(claims, list) or not claims:
-        return problems + ["no claims"], verdicts
+        return problems + ["no claims"]
     base_text = show(root, BASE, unit["path"]) or ""
     current = show(root, revision, unit["path"])
     if current is None:
-        return problems + ["unit file missing at revision"], verdicts
+        return problems + ["unit file missing at revision"]
     position = current.find(HEADING)
     section = current[position:] if position >= 0 else ""
     if position < 0:
@@ -75,7 +75,6 @@ def check_unit(root: str, revision: str, unit: dict[str, str]) -> tuple[list[s
         if verdict not in VERDICTS:
             problems.append(f"claim {claim['id']}: verdict {verdict!r}")
             continue
-        verdicts[verdict] += 1
         if claim["anchor"] not in base_text:
             problems.append(f"claim {claim['id']}: anchor not in unit at base")
         if f"[{unit['unit']}:{claim['id']}]" not in section:
@@ -88,7 +87,7 @@ def check_unit(root: str, revision: str, unit: dict[str, str]) -> tuple[list[s
                 problems.append(f"claim {claim['id']}: correction not in round-23 section")
         if verdict == "UNVERIFIABLE" and not str(claim.get("reason", "")).strip():
             problems.append(f"claim {claim['id']}: UNVERIFIABLE without reason")
-    return problems, verdicts
+    return problems
 
 
 def main(argv: list[str] | None = None) -> int:
@@ -106,15 +105,12 @@ def main(argv: list[str] | None = None) -> int:
         return 2
     revision = resolved.stdout.strip()
     units = json.loads(population_raw)["units"]
-    rows, totals = [], {v: 0 for v in VERDICTS}
+    rows = []
     for unit in units:
-        problems, verdicts = check_unit(args.root, revision, unit)
-        for key, value in verdicts.items():
-            totals[key] += value
-        rows.append({"unit": unit["unit"], "pass": not problems, "claims": verdicts, "problems": problems})
+        problems = check_unit(args.root, revision, unit)
+        rows.append({"unit": unit["unit"], "pass": not problems, "problems": problems})
     accepted = sum(row["pass"] for row in rows)
-    print(json.dumps({"revision": revision, "accepted": accepted, "total": len(units), "claimVerdicts": totals,
-                      "units": rows}, indent=1, sort_keys=True))
+    print(json.dumps({"revision": revision, "accepted": accepted, "total": len(units), "units": rows}, indent=1, sort_keys=True))
     return 0 if accepted == len(units) else 1
```

### `.ufo/waves/round-23/measure_c2.py`

```diff
--- a/.ufo/waves/round-23/measure_c2.py
+++ b/.ufo/waves/round-23/measure_c2.py
@@ -103,8 +103,7 @@ def main(argv: list[str] | None = None) -> int:
         problems, verdict = check(args.root, revision, validator, surface)
         rows.append({"id": surface["id"], "pass": not problems, "verdict": verdict, "problems": problems})
     accepted = sum(row["pass"] for row in rows)
-    print(json.dumps({"revision": revision, "validatorSha256": hashlib.sha256(validator).hexdigest(),
-                      "accepted": accepted, "total": len(rows), "surfaces": rows}, indent=1, sort_keys=True))
+    print(json.dumps({"revision": revision, "accepted": accepted, "total": len(rows), "surfaces": rows}, indent=1, sort_keys=True))
     return 0 if accepted == len(rows) else 1
```

Optional further trim (same exit semantics): drop `"verdict"` from each surface row when `"pass": false` (always `null` today).

### `scripts/live_snapshot.py`

```diff
--- a/scripts/live_snapshot.py
+++ b/scripts/live_snapshot.py
@@ -123,9 +123,8 @@ def main(argv: list[str] | None = None) -> int:
             receipt = audit(args.validator, directory, str(meta["finalUrl"]), surface["expectedCanonical"])
         with open(os.path.join(directory, "audit.json"), "w", encoding="utf-8") as stream:
             json.dump(receipt, stream, indent=1, sort_keys=True)
-        verdict = receipt.get("verdict") or receipt["result"]["verdict"]
-        summary.append({"id": surface["id"], "status": meta["status"], "verdict": verdict,
-                        "findings": [f["id"] for f in receipt.get("result", {}).get("findings", [])]})
+        verdict = receipt["verdict"] if "verdict" in receipt else receipt["result"]["verdict"]
+        summary.append({"id": surface["id"], "status": meta["status"], "verdict": verdict})
     print(json.dumps({"surfaces": summary}, indent=1))
     return 0
```

On-disk artifacts (`fetch.json`, `audit.json`, `page.html`, `manifest.json`) unchanged by this hunk — **C2 reproduction unchanged**.

## Deletion candidates rejected (evidence)

- **`fetch.json` `redirects` array:** no `measure_c2` read; kept for audit trail (security review scope in `w1-dispatch.json`).
- **Extract `round23_git_show` helper:** 2 call sites; grep shows no third consumer at r23-build.
- **Drop `-B` on validator subprocess:** avoids `.pyc` writes in temp checkouts; zero functional gain.

Report: `.ufo/waves/round-23/w1/SimplifyR23Tools.md`
