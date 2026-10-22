# Round 34 — ExecGateRejectCheck

Axes: operability and freshness. Built an offline check of committed lesson content; it reads the selected commit's lesson blob (not the worktree), includes every `## Gate` subsection, and recognizes reasoned reject decisions in source tables and source lines. Exit 0 means a match, 1 means no match, and 2 means invalid/unreadable input. Implementation: `/fast/scratch/hyaku/kake-r34/w1/ExecGateRejectCheck/gate_reject_check.py`, intended lane destination `.ufo/waves/round-34/criteria/gate_reject_check.py`. Final SHA-256: `35d0bba359ddbfaba242236cf45e5983f1add5136d1cd0c23c151e5e05972a84`.

Code evidence: committed-blob reading and input validation at script:23-65; Gate subsection extraction at :68-78; rejection/reason matching at :85-149; verdict output and exit codes at :153-171. Script is still in the sandbox; no lane implementation file was written. Only this report was written in the lane.

## Commands and results

Every check used this exact invocation form, with the listed `REV` and `LESSON` substituted: `set +e; python3 -B /fast/scratch/hyaku/kake-r34/w1/ExecGateRejectCheck/gate_reject_check.py --repo /fast/scratch/hyaku/kake-r34/w1/ExecGateRejectCheck/clone --rev REV --lesson LESSON; rc=$?; printf 'EXIT_CODE=%s\n' "$rc"; exit 0`.

Final script run set (after the last code edit):
- `--rev 93359ff0924bf622acc51eb15c2afa3cd2743022 --lesson corpus/lessons/round-33.md` → exit 1; `NO MATCH: ## Gate has no source decision beginning with reject and a non-empty reason` (expected). The committed Gate has admitted source rows, not a rejected row: clone `corpus/lessons/round-33.md:29-36`.
- `--rev a2fe31b2d1d2bf67f832b31fb994869b83dbdb9f --lesson corpus/lessons/round-28.md` → exit 1; same `NO MATCH` output.
- `--rev a2fe31b2d1d2bf67f832b31fb994869b83dbdb9f --lesson corpus/lessons/round-29.md` → exit 0; matched line M29 below (clone lesson :56; expected pass).
- `--rev a2fe31b2d1d2bf67f832b31fb994869b83dbdb9f --lesson corpus/lessons/round-30.md` → exit 0; matched line M30 below (clone lesson :55).
- `--rev a2fe31b2d1d2bf67f832b31fb994869b83dbdb9f --lesson corpus/lessons/round-31.md` → exit 1; same `NO MATCH` output; its Gate states “None this round” under Screened candidates (clone lesson :48-54).
- `--rev a2fe31b2d1d2bf67f832b31fb994869b83dbdb9f --lesson corpus/lessons/round-32.md` → exit 0; matched line M32 below (clone lesson :33).
- Bad-input check: `--rev not-a-commit --lesson corpus/lessons/round-29.md` at the same clone → exit 2; stderr `ERROR: --rev does not resolve to a commit: not-a-commit`.

Exact stdout match lines from the final run:
- M29: `MATCH: corpus/lessons/round-29.md:56: - S044 (C1) — https://mademistakes.com/mastering-jekyll/site-url-baseurl/ — accessed 2026-10-22, HTTP 200 — **rejected**: stale version claim and raw baseurl concatenation advice; quote “GitHub Pages does not use the latest version of Jekyll to build sites. It is currently locked at 3.9.0” (S016 lists Jekyll 3.10.0).`
- M30: `MATCH: corpus/lessons/round-30.md:55: - S053 (C1) — https://dev.to/stephengade/how-to-deploy-static-website-for-free-on-render-with-custom-domain-4efo — accessed 2026-10-22, HTTP 200 — **rejected**: its one durable point, the catch-all rewrite to /index.html, is already carried by S050, and its custom-domain step names an ALIAS record that S052 does not; quote “Grab your CNAME and ALIAS to add to your domain name”.`
- M32: `MATCH: corpus/lessons/round-32.md:33: | S063 | https://flueframework.com/docs/ecosystem/deploy/render/ (screened by wave-1 scribe `ScribeScreenBlueprintCandidate`, GET 200 at 2026-10-22T18:59:36Z; re-opened by the L1 at 19:01Z, quote present) | 2026-10-22 | “To auto-deploy on every push, set autoDeployTrigger: commit on the service (this replaces the deprecated autoDeploy field).” (17 words) | reject, tier C: restates fields S057 already carries; its one additive claim (`autoDeployTrigger` replacing `autoDeploy`) has no tier-A row. Flip: a Render vendor page documents `autoDeployTrigger` and the deprecation.`

Earlier invocations, retained to disclose the parser correction: the first six-case run used the same commands/commits listed above and produced the final outcomes for rounds 28-31 and 33; its round-29 and round-30 match lines were M29/M30. Round-32 initially exited 1 with `NO MATCH` because a blank line between table rows cleared the decision header. The parser was corrected to retain headers across blank lines; the subsequent six-case run (and the final run above) made round-32 exit 0 with M32. The intermediate full run also tested the bad revision and returned exit 2 with the stderr shown above.

Intermediate `sha256sum` before the last reason-normalization edit: `b44c7b9efe1c8b927a01a07bb7723f4ce20552cc116505e1baec9e5a3e5cbf11`; superseded by the final hash above. Final command: `sha256sum /fast/scratch/hyaku/kake-r34/w1/ExecGateRejectCheck/gate_reject_check.py` → `35d0bba359ddbfaba242236cf45e5983f1add5136d1cd0c23c151e5e05972a84`.

## Risks and blockers

No blocker. The matching conventions cover S-numbered source rows (`id`/`decision` tables) and explicit source-line decisions, matching the retained lesson formats. Other Markdown layouts or non-S-numbered source identifiers were not tested. No tools were installed or updated; no builds, linters, or unrelated tests were run.