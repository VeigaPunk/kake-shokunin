# Real-run summary

- tool: `/fast/scratch/hyaku/kake-r38w1/ExecRealRunPrep/base-tool/robots_audit.py`
- tool sha256: `944d2f51f396fb6e1ba3c7cf07112eb3f55d011e9bbc16bb1a59af517be1d3e5`
- timeout: 20.0 s per manifest
- all declared reports matched: **False**

| manifest | match | expected exit/verdict/evaluated | observed exit/verdict/evaluated |
|---|---|---|---|
| `manifest.h-float-status.json` | True | 2/could-not-evaluate/1 | 2/could-not-evaluate/1 |
| `manifest.h-infinity-status.json` | False | 2/could-not-evaluate/0 | 2/could-not-evaluate/1 |
| `manifest.h-long-status.json` | False | 2/could-not-evaluate/1 | 2/could-not-evaluate/0 |
| `manifest.h-nan-unused.json` | False | 2/could-not-evaluate/0 | 0/clean/2 |
| `manifest.h-neginfinity-status.json` | False | 2/could-not-evaluate/0 | 2/could-not-evaluate/1 |
| `manifest.h-unused-bigint.json` | False | 0/clean/2 | 2/could-not-evaluate/0 |
| `manifest.json` | False | 2/could-not-evaluate/79 | 1/failed-policy/91 |

## `manifest.h-infinity-status.json` differences

- checksEvaluated: expected 0, observed 1
- findings missing: [[null, "input_invalid"]]
- findings extra: [["h-infinity-status", "check_invalid"]]

## `manifest.h-long-status.json` differences

- checksEvaluated: expected 1, observed 0
- findings missing: [["h-long-status-5000", "check_invalid"]]
- findings extra: [[null, "input_invalid"]]

## `manifest.h-nan-unused.json` differences

- exit: expected 2, observed 0
- verdict: expected 'could-not-evaluate', observed 'clean'
- checksEvaluated: expected 0, observed 2
- findings missing: [[null, "input_invalid"]]

## `manifest.h-neginfinity-status.json` differences

- checksEvaluated: expected 0, observed 1
- findings missing: [[null, "input_invalid"]]
- findings extra: [["h-neginfinity-status", "check_invalid"]]

## `manifest.h-unused-bigint.json` differences

- exit: expected 0, observed 2
- verdict: expected 'clean', observed 'could-not-evaluate'
- checksEvaluated: expected 2, observed 0
- findings extra: [[null, "input_invalid"]]

## `manifest.json` differences

- exit: expected 2, observed 1
- verdict: expected 'could-not-evaluate', observed 'failed-policy'
- checksEvaluated: expected 79, observed 91
- findings missing: [["r38-i-developer_mozilla_org-del", "check_invalid"], ["r38-i-developers_google_com-quote", "check_invalid"], ["r38-i-docs_github_com-backslash", "check_invalid"], ["r38-i-ds4cc_com-braceopen", "check_invalid"], ["r38-i-en_wikipedia_org-pipe", "check_invalid"], ["r38-i-github_com-caret", "check_invalid"], ["r38-i-html_spec_whatwg_org-backtick", "check_invalid"], ["r38-i-pages_github_com-braceclose", "check_invalid"], ["r38-i-veigapunk_github_io-gt", "check_invalid"], ["r38-i-www_rfc-editor_org-space", "check_invalid"], ["r38-i-www_robotstxt_org-lt", "check_invalid"], ["r38-i-www_sitemaps_org-ctl", "check_invalid"]]
- findings extra: [["r38-k-en_wikipedia_org-pct2e", "blocked"], ["r38-k-en_wikipedia_org-pct72", "blocked"]]

