Verdict: valid control — M09 breaks contract sentence 14 (as applied through 15); the contract decides the witness; the reference obeys it and the mutant does not, yet the sealed receipt scored it 24/24 (met=true), i.e. the 24-case key never exercises an xmlns="" reset child.

Axes: operability (judged), freshness (lane). Leaf seat; no subagents; no lsp device in session → diff + live-run evidence only. No tools installed.

Diff vs /fast/scratch/hyaku/kake-r39a3w1/shared/reference.py — exactly one change (single hunk, 1 line, file line 154):
-            if ns != NS:
+            if ns not in (NS, ""):
sha256: reference 663e051e10b9fca2db55fa13497b965fb19fb107b3791123769fc8534a2d69f8; mutant c41ed5268dd866a27ac8bdf73da3b034779aabaee8189a697687525dbcb35de3 (== receipt toolSha256); manifest 7896a372bde566ce3d0053cac13b025b74ef42b05b68ce85f21c4f514401d8e7; sitemap 8b3d7da61c56a908aebb8481b6eb9ce881c32b3ada36837eb82d91eb8f3df113 (both == mutants.json).

Witness sitemap.xml: <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://example.test/</loc><loc xmlns="">https://example.test/</loc></url></urlset>

Runs (each: prlimit --as=4000000000 timeout 60 python3 -B <tool> --manifest .../witnesses/M09/manifest.json; stderr empty):
reference stdout: {"version": 1, "verdict": "clean", "checks": [{"id": "witness", "status": "clean", "error": null, "findings": []}]}   REF_EXIT=0
mutant stdout:    {"version": 1, "verdict": "failed-policy", "checks": [{"id": "witness", "status": "findings", "error": null, "findings": [{"code": "loc_repeated", "entry": 1}]}]}   MUT_EXIT=1

Contract text: 14 "Elements in any other namespace, at any level, are ignored"; 15 "An entry must have exactly one loc child in the sitemap namespace: none gives loc_missing, more than one loc_repeated"; 34 any finding → failed-policy/exit 1, none → clean/exit 0. xmlns="" puts the second loc in no namespace → sentence 14 says ignore it → exactly one in-NS loc → clean/0. Reference output is the contract-determined one; the mutant counts the no-namespace loc as in-NS → loc_repeated/1 — the violation. Sentence 17 is untouched (the reset child is not "in the sitemap namespace"); the assignment's "15/17" is really "14 via 15" (mutants.json claims 14 — confirmed).

Sealed receipt read fields only (label/passed/met/toolSha256): passed=24, met=true; no rows/why/cases read; counter not run.

Conclusion: valid control. Its met status marks a sealed-key coverage gap — no case with a reset-default-namespace entry child among the 24 — so kill-rule-(1) routing to falsification fired correctly; the control itself is genuinely contract-breaking.
