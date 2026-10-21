## Verdict

No actionable operability defect found in the assigned checks against `scripts/canonical_audit.py` at `4d95d2e9a7fa41735b064ebfd92ce1a25e84b0cc`. This is a scoped author-side observation, not independent admission.

## Findings

None (P0–P3).

## Checked and held

Target: extracted `git show 4d95d2e9a7fa41735b064ebfd92ce1a25e84b0cc:scripts/canonical_audit.py`; SHA-256 `d8acf75062ab61006a5fdf786d04deb0d54d0d15f19e11be09a80b57aa74ecac`. Lane HEAD observed as `4e7dd1d4e52dcbdce249dd3dbc8485bc4e23cf4b`; `git diff --stat 4d95d2e9a7fa41735b064ebfd92ce1a25e84b0cc -- scripts/canonical_audit.py` emitted no lines. Interpreter: `Python 3.14.8`. All fixtures and the extracted script were under `/tmp/kake-r23-BoundaryReadOnly-LyYM`; no lane production file was changed.

### Positive control: valid, actually checked clean fixture

Command:

```text
python3 /tmp/kake-r23-BoundaryReadOnly-LyYM/canonical_audit.4d95d2e.py --manifest /tmp/kake-r23-BoundaryReadOnly-LyYM/clean/manifest.json --json
```

Exact CLI output and status:

```text
{"findings":[],"pagesChecked":1,"verdict":"clean"}
exit_code=0
```

The manifest and explicit, closed-head page contained one canonical equal to the expected URL; `pagesChecked: 1` distinguishes evaluated-clean from unsupported/skipped.

Inventory command used before and after the CLI: `stat -c '%n mode=%a size=%s mtime=%y ctime=%z inode=%i uid=%u gid=%g' /tmp/kake-r23-BoundaryReadOnly-LyYM/clean/manifest.json /tmp/kake-r23-BoundaryReadOnly-LyYM/clean/page.html` and `sha256sum --` on those same paths. Exact before and after records were identical:

```text
/tmp/kake-r23-BoundaryReadOnly-LyYM/clean/manifest.json mode=644 size=131 mtime=2026-10-21 04:02:57.546079588 -0300 ctime=2026-10-21 04:02:57.546079588 -0300 inode=173157070 uid=1000 gid=1000
/tmp/kake-r23-BoundaryReadOnly-LyYM/clean/page.html mode=644 size=114 mtime=2026-10-21 04:02:57.547010920 -0300 ctime=2026-10-21 04:02:57.547010920 -0300 inode=173157071 uid=1000 gid=1000
6fc36e5d69f5265c6f4fbac812158edce87efecb0421bc479ee813005ebd2f6d  /tmp/kake-r23-BoundaryReadOnly-LyYM/clean/manifest.json
7d9c0e16814d4d099a5a9456caf88f392c563cb9807c99299f83da5cf97e7528  /tmp/kake-r23-BoundaryReadOnly-LyYM/clean/page.html
```

### Negative control: real policy failure

Command:

```text
python3 /tmp/kake-r23-BoundaryReadOnly-LyYM/canonical_audit.4d95d2e.py --manifest /tmp/kake-r23-BoundaryReadOnly-LyYM/red/manifest.json --json
```

Exact CLI output and status:

```text
{"findings":[{"id":"canonical_mismatch","page":"https://example.test/a.html"}],"pagesChecked":1,"verdict":"failed-policy"}
exit_code=1
```

The page's canonical deliberately used `https://other.example/a.html`, so this is a checked policy mismatch, not an unsupported input. `stat -c` with the same format and `sha256sum --` on the red manifest and page were run before and after; the exact records matched:

```text
/tmp/kake-r23-BoundaryReadOnly-LyYM/red/manifest.json mode=644 size=131 mtime=2026-10-21 04:02:57.547350800 -0300 ctime=2026-10-21 04:02:57.547350800 -0300 inode=181357199 uid=1000 gid=1000
/tmp/kake-r23-BoundaryReadOnly-LyYM/red/page.html mode=644 size=121 mtime=2026-10-21 04:02:57.547783880 -0300 ctime=2026-10-21 04:02:57.547783880 -0300 inode=181357200 uid=1000 gid=1000
6fc36e5d69f5265c6f4fbac812158edce87efecb0421bc479ee813005ebd2f6d  /tmp/kake-r23-BoundaryReadOnly-LyYM/red/manifest.json
7d30ab22f8d214352b6f4c81c548c44874ac99d5b0e91c9daffdc489af0e7719  /tmp/kake-r23-BoundaryReadOnly-LyYM/red/page.html
```

### Unsupported is distinct from clean

A third fixture with SVG inside the still-open head produced:

```text
{"findings":[{"id":"html_unsupported","page":"https://example.test/a.html"}],"pagesChecked":1,"verdict":"could-not-evaluate"}
exit_code=2
```

Its before/after SHA-256 values also matched: manifest `6fc36e5d69f5265c6f4fbac812158edce87efecb0421bc479ee813005ebd2f6d`; page `8e50f2a7e099e4cfff8408398bf96b1a8bef7826ca72ad805ba051cb07f55d77`.

### Import and runtime network-surface checks

An AST walk over every `Import` and `ImportFrom` in the target file returned exactly:

```json
{"imports":["__future__","argparse","html.parser","ipaddress","json","ntpath","os","re","stat","subprocess","sys","tempfile","urllib.parse"],"network_capable_direct_imports":[]}
```

A Python audit-hook wrapper executing the target as `__main__` with the clean and red manifest arguments emitted the same respective CLI JSON above and, on stderr in each case, exactly:

```json
{"network_imports":[],"network_events":[]}
```

The hook watched imports of socket/SSL/HTTP/urllib request and common network-client modules, socket/SSL/HTTP client events, `urllib.Request`, and process/system execution events. In source, `urllib.parse` is used for URL parsing; `subprocess.run` is confined to `_run_cli`/selftest (lines 835–847), which re-invokes this script using a fixed Python executable/path. No such process or network event occurred in either manifest invocation.

## Limits

- The immutability inventory covered the two regular fixture files per clean/red case (mode, size, mtime, ctime, inode, uid/gid, SHA-256), not adversarial concurrent replacement or every possible filesystem object.
- The import result means no direct network-client imports were present and no watched network/process events were observed in these invocations. `subprocess` is a generic process-launch module imported for selftest; if “network-capable import” is defined to include any generic process launcher regardless of reachable command, this narrower direct-network-import interpretation does not settle that broader policy.
- No selftest/build/lint, external HTTP request, or publishing action was run. No tooling was installed or updated.
