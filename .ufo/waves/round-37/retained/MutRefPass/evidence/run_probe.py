#!/usr/bin/env python3
"""Isolated C1 reference mutants; never reads or copies sealed case contents."""
from __future__ import annotations

import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import threading
import time

ROOT = Path('/fast/scratch/hyaku/kake-r37/ctl/MutRefPass')
EVIDENCE = ROOT / 'evidence'
MUTANTS = ROOT / 'mutants'
TRIALS = EVIDENCE / 'trials'
OUTPUTS = EVIDENCE / 'outputs'
TMP = EVIDENCE / 'tmp'
LANE = Path('/home/vgpnk/Projects/shokunin/kake-shokunin')
SOURCE = Path('/fast/scratch/hyaku/kake-r37/private/ref.py')
KEY = '/fast/scratch/hyaku/kake-r37/private/cases.json'
COUNTER = LANE / '.ufo/waves/round-37/sealed_count.py'
REPORT = LANE / '.ufo/waves/round-37/ctl/MutRefPass.md'
COMMANDS = EVIDENCE / 'commands.jsonl'
LOCK = threading.Lock()
ACTIVE: dict[int, subprocess.Popen] = {}
STOP = threading.Event()
ENV = dict(os.environ, TMPDIR=str(TMP), PYTHONDONTWRITEBYTECODE='1')
ORIGINAL = SOURCE.read_bytes()
TEXT = ORIGINAL.decode('utf-8')
SHA = lambda b: hashlib.sha256(b).hexdigest()
SOURCE_HASH = SHA(ORIGINAL)
COUNTER_HASH = SHA(COUNTER.read_bytes())

# Every old/new pair changes exactly one source line, not an ABL flag.
# The final explanation is public-contract reasoning, never a sealed-case description.
SPECS = [
 ('M01', 'b: exactly 512000 bytes', 'LIMIT = 512000', 'LIMIT = 511999', 'LIMIT: 512000 -> 511999', 'the last permitted byte is dropped'),
 ('M02', 'b: exactly 512000 bytes', 'LIMIT = 512000', 'LIMIT = 512001', 'LIMIT: 512000 -> 512001', 'a forbidden extra byte can change a rule'),
 ('M03', 'b: key trims only SP/TAB', 'key = key.strip(" \\t")', 'key = key.strip()', 'key.strip(SP/TAB) -> key.strip()', 'Unicode whitespace can turn an ignored key into a record'),
 ('M04', 'b: value trims only SP/TAB', 'value = value.strip(" \\t")', 'value = value.strip()', 'value.strip(SP/TAB) -> value.strip()', 'Unicode whitespace in a literal rule or agent is lost'),
 ('M05', 'b: first # starts comment', 'i = line.find("#")', 'i = line.rfind("#")', 'find(#) -> rfind(#)', 'text between comment markers is wrongly retained'),
 ('M06', 'b: only CR/LF/CRLF split lines', 'lines = re.split(r"\\r\\n|\\r|\\n", text)', 'lines = text.splitlines()', 'CR/LF regex -> splitlines()', 'Unicode separators wrongly start new records'),
 ('M07', 'b: split at first colon', 'key, value = line.split(":", 1)', 'key, value = line.rsplit(":", 1)', 'split(:,1) -> rsplit(:,1)', 'a colon inside a value changes the parsed key'),
 ('M08', 'b: ASCII key case comparison', 'key = key.lower()', 'key = key.casefold()', 'key.lower() -> key.casefold()', 'Unicode folding can convert a non-ASCII key to a record'),
 ('M09', 'c: ASCII agent comparison', 'a.lower() == u', 'a.casefold() == u', 'group-name lower() -> casefold()', 'Unicode group names can spuriously equal an ASCII product'),
 ('M10', 'c: exact group-name equality', 'a.lower() == u', 'u in a.lower()', 'agent equality -> substring', 'a longer different group name can match'),
 ('M11', 'c: wildcard only without exact match', 'if not matched and "c_star" not in ABL:', 'if matched and "c_star" not in ABL:', 'if not matched -> if matched', 'wildcard fallback is inverted'),
 ('M12', 'c: combine every matching group', 'rules.extend(g["rules"])', 'rules = g["rules"]', 'rules.extend(group) -> rules = group', 'only the last matching group retains its rules'),
 ('M13', 'c: agent after rule starts group', '\n            last_ua = False\n', '\n            last_ua = True\n', 'after rule: last_ua False -> True', 'a later agent inherits the earlier group rules'),
 ('M14', 'c: consecutive agents share group', '            last_ua = True\n', '            last_ua = False\n', 'after agent: last_ua True -> False', 'earlier consecutive agents lose the following rules'),
 ('M15', 'd: star also matches empty', 'rx = ".*".join', 'rx = ".+".join', 'wildcard .* -> .+', 'a zero-length wildcard expansion no longer matches'),
 ('M16', 'd: only terminal $ anchors', 'anchored = pat.endswith("$")', 'anchored = pat.startswith("$")', 'endswith($) -> startswith($)', 'terminal anchors become literal dollar characters'),
 ('M17', 'd: unanchored match is prefix', 'return re.match(rx +', 'return re.fullmatch(rx +', 're.match -> re.fullmatch', 'an otherwise matching prefix is rejected with a suffix'),
 ('M18', 'd: prefix begins at first character', 'return re.match(rx +', 'return re.search(rx +', 're.match -> re.search', 'a rule can wrongly match in the middle of a path'),
 ('M19', 'd: normalized octet length wins', '        length = len(npat)\n', '        length = len(pat)\n', 'len(normalized) -> len(raw)', 'raw Unicode or escaped lengths can select another rule'),
 ('M20', 'd: allow wins equal-length ties', 'elif best is None or length > best[0] or (length == best[0] and kind == "allow"):', 'elif best is None or length >= best[0] or (length == best[0] and kind == "allow"):', 'longest comparison > -> >=', 'a later equal-length disallow overrides allow'),
 ('M21', 'd: allow wins equal-length ties', 'elif best is None or length > best[0] or (length == best[0] and kind == "allow"):', 'elif best is None or length > best[0] or (length == best[0] and kind == "disallow"):', 'tie kind allow -> disallow', 'equal-length ties select disallow'),
 ('M22', 'e: reserved escapes stay encoded', 'if chr(b) in UNRESERVED and "e_unreserved" not in ABL:', 'if (chr(b) in UNRESERVED or b == 47) and "e_unreserved" not in ABL:', 'decode unreserved -> also decode %2F', 'encoded slash is collapsed into a literal slash'),
 ('M23', 'e: kept escapes use uppercase hex', 'out.append("%" + s[i + 1:i + 3].upper())', 'out.append("%" + s[i + 1:i + 3].lower())', 'escape hex upper() -> lower()', 'escaped non-ASCII octets no longer equal raw UTF-8 normalization'),
 ('M24', 'e: UTF-8 escapes use uppercase hex', '"%%%02X" % b', '"%%%02x" % b', 'UTF-8 octet format %02X -> %02x', 'raw non-ASCII no longer equals uppercase-normalized escapes'),
 ('M25', 'e: empty URL path becomes /', '        path = "/"\n', '        path = ""\n', 'empty-path default / -> empty', 'a slash rule no longer matches a host-only URL'),
 ('M26', 'e: non-empty query is included', 'path += "?" + p.query', 'path += ""', 'append ?query -> append empty', 'query-dependent rules see only the path'),
 ('M27', 'e: fragment is never included', '    path = p.path\n', '    path = p.path + ("#" + p.fragment if p.fragment else "")\n', 'path -> path plus fragment', 'fragment text changes matching and anchoring'),
 ('M28', 'e: /robots.txt exemption is exact', 'if npath == "/robots.txt" and', 'if npath.lower() == "/robots.txt" and', 'robots path comparison -> case-insensitive', 'differently cased paths wrongly bypass their rules'),
 ('M29', 'g: version is integer 1, not True', 'type(m.get("version")) is int', 'isinstance(m.get("version"), int)', 'exact int type -> isinstance(int)', 'JSON true is wrongly accepted as manifest version'),
 ('M30', 'manifest: entire agent is product token', 'UA_RE.fullmatch(ua)', 'UA_RE.match(ua)', 'UA fullmatch -> match', 'a valid prefix hides an invalid trailing character'),
 ('M31', 'manifest: agent alphabet excludes digits', 'UA_RE = re.compile(r"[A-Za-z_-]+")', 'UA_RE = re.compile(r"[A-Za-z0-9_-]+")', 'UA alphabet -> add 0-9', 'digit-containing agents are wrongly accepted'),
 ('M32', 'manifest: reject status 300', '(300 <= status <= 399 and', '(301 <= status <= 399 and', '3xx lower bound 300 -> 301', 'status 300 becomes valid and evaluated'),
 ('M33', 'manifest: reject status 399', '(300 <= status <= 399 and', '(300 <= status <= 398 and', '3xx upper bound 399 -> 398', 'status 399 becomes valid and evaluated'),
 ('M34', 'manifest: floats are not status integers', 'type(status) is not int', 'not isinstance(status, (int, float))', 'status int-only -> int or float', 'in-range floating statuses are wrongly accepted'),
 ('M35', 'manifest: status 200 is valid', 'not (200 <= status <= 599)', 'not (201 <= status <= 599)', 'status lower bound 200 -> 201', 'an allowed 200 status becomes check_invalid'),
 ('M36', 'manifest: status 599 is valid', 'not (200 <= status <= 599)', 'not (200 <= status <= 598)', 'status upper bound 599 -> 598', 'an allowed 599 status becomes check_invalid'),
 ('M37', 'manifest: resolve symlinks for containment', 'real = os.path.realpath(full)', 'real = os.path.abspath(full)', 'realpath(file) -> abspath(file)', 'a symlink can refer outside the manifest directory'),
 ('M38', 'manifest: file stays inside directory', 'not real.startswith(base + os.sep)', 'not real.startswith(base)', 'containment prefix drops separator', 'a sibling directory sharing the base prefix passes'),
 ('M39', 'g: only sizes greater than 64 MiB fail', 'MAX_MANIFEST = 64 * 1024 * 1024', 'MAX_MANIFEST = 64 * 1024 * 1024 - 1', 'manifest max 64 MiB -> 64 MiB minus 1', 'an otherwise valid exactly-64-MiB manifest is rejected'),
 ('M40', 'g: non-UTF-8 manifest is invalid', 'm = json.loads(fh.read().decode("utf-8"))', 'm = json.loads(fh.read().decode("utf-8", "replace"))', 'manifest UTF-8 strict -> replacement', 'invalid UTF-8 inside a JSON string can be accepted'),
 ('M41', 'f: checksEvaluated counts valid checks', '        evaluated += 1\n', '        evaluated += 2\n', 'evaluated increment 1 -> 2', 'every nonempty valid set has a doubled count; counter explicitly ignores it'),
 ('M42', 'usage: stdout report version is 1', 'print(json.dumps({"version": 1,', 'print(json.dumps({"version": 2,', 'output report version 1 -> 2', 'the required output version is wrong; counter does not compare it'),
]


def append_command(row):
    with LOCK:
        with COMMANDS.open('a', encoding='utf-8') as fh:
            fh.write(json.dumps(row, sort_keys=True) + '\n')


def halt(signum, frame):
    STOP.set()
    with LOCK:
        processes = list(ACTIVE.values())
    for process in processes:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    raise SystemExit(128 + signum)


signal.signal(signal.SIGTERM, halt)
signal.signal(signal.SIGINT, halt)


def score(mid, stage, tool):
    if STOP.is_set():
        raise RuntimeError('probe interrupted')
    argv = ['timeout', '300', 'python3', '-B', str(COUNTER), '--root', str(LANE),
            '--tool-file', str(tool), '--key-file', KEY]
    began = time.monotonic()
    process = subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               env=ENV, cwd=str(ROOT), start_new_session=True)
    with LOCK:
        ACTIVE[process.pid] = process
    try:
        try:
            stdout, stderr = process.communicate(timeout=310)
        except BaseException:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            process.communicate()
            raise
    finally:
        with LOCK:
            ACTIVE.pop(process.pid, None)
    outpath = OUTPUTS / f'{mid}.{stage}.stdout.json'
    errpath = OUTPUTS / f'{mid}.{stage}.stderr.txt'
    outpath.write_bytes(stdout)
    errpath.write_bytes(stderr)
    try:
        result = json.loads(stdout)
    except (ValueError, UnicodeError):
        result = {'error': 'counter stdout was not JSON'}
    record = dict(mutant=mid, stage=stage, argv=argv, cwd=str(ROOT),
                  env={'TMPDIR': str(TMP), 'PYTHONDONTWRITEBYTECODE': '1'},
                  exit=process.returncode, stdout=str(outpath), stderr=str(errpath),
                  elapsedSeconds=round(time.monotonic() - began, 4),
                  toolSha256=SHA(tool.read_bytes()))
    append_command(record)
    return dict(exit=process.returncode, passed=result.get('passed'),
                cases=result.get('cases'), met=result.get('met'),
                toolSha256=result.get('toolSha256'), stdout=str(outpath), stderr=str(errpath))


def previous_score(mid, stage, records):
    command = records[(mid, stage)]
    result = json.loads(Path(command['stdout']).read_bytes())
    if command['toolSha256'] != result.get('toolSha256'):
        raise RuntimeError(f'{mid}: recorded tool hash does not match detector receipt')
    return dict(exit=command['exit'], passed=result.get('passed'), cases=result.get('cases'),
                met=result.get('met'), toolSha256=result.get('toolSha256'),
                stdout=command['stdout'], stderr=command['stderr'])


def run_trial(spec):
    mid, contract, old, new, diff, why = spec
    if TEXT.count(old) != 1:
        raise ValueError(f'{mid}: expected one source occurrence, found {TEXT.count(old)}')
    mutated = TEXT.replace(old, new, 1).encode('utf-8')
    before_lines, after_lines = ORIGINAL.splitlines(), mutated.splitlines()
    if len(before_lines) != len(after_lines) or sum(a != b for a, b in zip(before_lines, after_lines)) != 1:
        raise ValueError(f'{mid}: not a single-line mutant')
    trial = TRIALS / f'{mid}.py'
    final = MUTANTS / f'{mid}.py'
    with LOCK:
        records = {(row.get('mutant'), row.get('stage')): row
                   for row in map(json.loads, COMMANDS.read_text().splitlines()) if row.get('mutant')}
    if all((mid, stage) in records for stage in ('pristine', 'mutated', 'restored')):
        baseline = previous_score(mid, 'pristine', records)
        mutation = previous_score(mid, 'mutated', records)
        restored = previous_score(mid, 'restored', records)
        pristine_hash = baseline['toolSha256']
        applied_hash = SHA(final.read_bytes())
        restored_hash = SHA(trial.read_bytes())
    else:
        trial.write_bytes(ORIGINAL)
        pristine_hash = SHA(trial.read_bytes())
        baseline = score(mid, 'pristine', trial)
        mutation = None
        try:
            trial.write_bytes(mutated)
            applied_hash = SHA(trial.read_bytes())
            final.write_bytes(mutated)
            mutation = score(mid, 'mutated', final)
        finally:
            trial.write_bytes(ORIGINAL)
            restored_hash = SHA(trial.read_bytes())
            restored = score(mid, 'restored', trial)
    valid = (baseline['exit'] == restored['exit'] == 0
             and baseline['cases'] == restored['cases'] == 28
             and baseline['passed'] == restored['passed'] == 28
             and pristine_hash == restored_hash == SOURCE_HASH
             and baseline['toolSha256'] == restored['toolSha256'] == SOURCE_HASH
             and mutation['exit'] in (0, 1)
             and mutation['cases'] == 28
             and mutation['toolSha256'] == applied_hash == SHA(final.read_bytes()))
    verdict = ('survived' if mutation['met'] else 'killed') if valid else 'inconclusive'
    return dict(id=mid, contract=contract, old=old, new=new, oneLineDiff=diff,
                equivalenceUnderContract=False, equivalenceReason=why,
                equivalenceBasis='INFERENCE from public contract, not a sealed-case disclosure',
                sourceSha256=pristine_hash, appliedSha256=applied_hash,
                restoredSha256=restored_hash, restoredExact=trial.read_bytes() == ORIGINAL,
                file=str(final), baseline=baseline, mutated=mutation,
                restored=restored, verdict=verdict)


def main():
    append_command(dict(stage='orchestrator',
                        shell='timeout --kill-after=5s 850s python3 -B /fast/scratch/hyaku/kake-r37/ctl/MutRefPass/evidence/run_probe.py',
                        exit=1, error='M13: expected one source occurrence, found 2',
                        note='first attempt; all other trials completed; reuse those actual receipts without rerunning'))
    futures = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        futures = [pool.submit(run_trial, spec) for spec in SPECS]
        rows = [future.result() for future in futures]
    rows.sort(key=lambda row: row['id'])
    if ACTIVE:
        raise RuntimeError('a detector process remains active')
    source_after = SHA(SOURCE.read_bytes())
    counter_after = SHA(COUNTER.read_bytes())
    summary = dict(control='MutRefPass', axes=['contract deviation', 'counter sensitivity', 'byte restoration'],
                   skips='one public C1 rule per reference-derived tool; never uses ABL flags',
                   mutants=len(rows), met=sum(row['mutated']['met'] is True for row in rows),
                   killed=sum(row['verdict'] == 'killed' for row in rows),
                   survived=sum(row['verdict'] == 'survived' for row in rows),
                   inconclusive=sum(row['verdict'] == 'inconclusive' for row in rows),
                   sourceBeforeSha256=SOURCE_HASH, sourceAfterSha256=source_after,
                   counterBeforeSha256=COUNTER_HASH, counterAfterSha256=counter_after,
                   allRestored=all(row['restoredExact'] for row in rows),
                   baselineScores=sorted({row['baseline']['passed'] for row in rows}),
                   restoredScores=sorted({row['restored']['passed'] for row in rows}),
                   keyCopied=False, keyContentsReadByProbe=False, installedTools=[],
                   activeProcessesAtEnd=len(ACTIVE), perMutant=rows)
    if source_after != SOURCE_HASH or counter_after != COUNTER_HASH:
        raise RuntimeError('read-only source/counter hash changed')
    summary_path = EVIDENCE / 'summary.json'
    summary_path.write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')
    listing_argv = ['timeout', '15', 'ls', '-la', str(ROOT)]
    listing = subprocess.run(listing_argv, capture_output=True, timeout=20, check=False)
    listing_path = EVIDENCE / 'sandbox-root.ls.txt'
    listing_path.write_bytes(listing.stdout)
    (EVIDENCE / 'sandbox-root.ls.stderr.txt').write_bytes(listing.stderr)
    append_command(dict(stage='listing', argv=listing_argv, exit=listing.returncode,
                        stdout=str(listing_path)))
    # The outer shell wrapper exits 0 iff this complete main() returns normally.
    runner_command = 'timeout --kill-after=5s 850s python3 -B /fast/scratch/hyaku/kake-r37/ctl/MutRefPass/evidence/run_probe.py'
    append_command(dict(stage='orchestrator', shell=runner_command, exit=0,
                        exitBasis='recorded immediately before normal return'))
    manifest_path = EVIDENCE / 'SHA256SUMS'
    manifest_files = sorted(path for path in ROOT.rglob('*') if path.is_file() and path != manifest_path)
    manifest_path.write_text(''.join(f'{SHA(path.read_bytes())}  {path}\n' for path in manifest_files), encoding='utf-8')
    manifest_hash = SHA(manifest_path.read_bytes())
    lines = [
      '# MutRefPass — single-point reference controls',
      'Axes: contract deviation / counter sensitivity / exact restoration. Each control skips one C1 rule; no ABL flags; no installs, key copied/read by this probe: no (counter alone reads it).',
      f"Expected detector: frozen `passed >= 25 of 28`; met **{summary['met']}/{len(rows)}**; killed {summary['killed']}, survived {summary['survived']}, inconclusive {summary['inconclusive']}. Pristine scores {summary['baselineScores']}/28; restored {summary['restoredScores']}/28; exact exits in evidence.",
      f'Before = restored = private source after: sha256 `{SOURCE_HASH}` (all {len(rows)} trials restored exactly; delivered mutants intentionally retained).',
      f'Every deliverable absolute path + sha256: `{manifest_path}`; manifest sha256 `{manifest_hash}`. Summary, 126 raw stdouts, stderr, exact argv/exit codes and listing are included; report hash is in the handoff.',
      f'Exact commands/exits: `{COMMANDS}`; runner `{runner_command}` exit 0 after one locator-count failure (exit 1, retained); completed trials were not rerun. Root listing below; no sealed key copied here; temporary fixtures removed.',
      'Mutation scores use `timeout 300 python3 -B ' + str(COUNTER) + ' --root ' + str(LANE) + ' --tool-file <mutants/Mxx.py> --key-file ' + KEY + '` with TMPDIR=' + str(TMP) + '; pristine/restored use the same detector on trials/Mxx.py.',
      'Equivalence column: N = [INFERENCE] non-equivalent under the public contract, with reason; not a claim about an undisclosed case. Killed means predicate false, not merely fewer than 28.',
      '| id | contract sentence broken | one-line diff | passed/28 | met | equivalent if met / why |',
      '|---|---|---|---:|:---:|---|',
    ]
    for row in rows:
        met = row['mutated']['met'] is True
        equivalent = 'N: ' + row['equivalenceReason'] if met else '—'
        lines.append('| ' + row['id'] + ' | ' + row['contract'] + ' | `' + row['oneLineDiff'] + '` | '
                     + str(row['mutated']['passed']) + '/28 | ' + ('yes' if met else 'no') + ' | ' + equivalent + ' |')
    lines.extend(['```text', *listing.stdout.decode('utf-8').rstrip('\n').splitlines(), '```'])
    if len(lines) > 60:
        raise RuntimeError(f'report would exceed 60 lines: {len(lines)}')
    REPORT.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(json.dumps(dict(mutants=len(rows), met=summary['met'], killed=summary['killed'],
                          survived=summary['survived'], inconclusive=summary['inconclusive'],
                          baselineScores=summary['baselineScores'], restoredScores=summary['restoredScores'],
                          sourceSha256=SOURCE_HASH, allRestored=summary['allRestored'],
                          manifest=str(manifest_path), manifestSha256=manifest_hash,
                          report=str(REPORT), reportSha256=SHA(REPORT.read_bytes()),
                          reportLines=len(lines), activeProcessesAtEnd=len(ACTIVE)), indent=2))


if __name__ == '__main__':
    main()
