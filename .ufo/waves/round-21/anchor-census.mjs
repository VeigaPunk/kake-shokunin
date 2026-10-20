#!/usr/bin/env node
// anchor-census.mjs — round-21 moved-reference register and byte-preservation audit.
//
// Compares every corpus/knowledge/*.md and every lane-authored corpus/lessons
// file (round-N.md / round-N-recensus.md — aggregator, verifier, spotcheck and
// round-21 lessons excluded) against the frozen base
// 5009ecaa1cce10b895617a585ddd3f7c7c923a84 via `git show <base>:<path>`.
//
// The round-21 contract permits only pure provenance prefixes and pure
// end-of-file Gate suffixes: every original byte must remain contiguous and
// every addition must sit on clean line boundaries. Any changed original byte
// is flagged as a preservation violation. For compliant files the tool emits a
// complete old-line -> new-line map (uniform offset).
//
// It then scans every tracked text source file — including the targets
// themselves, since lessons cite each other — for literal
// `filename:line[-end]` references that name a census target basename and
// reports each with: source location, cited (old) line range, resolved new
// line range, byte equality over the referenced ranges, and citation
// staleness. All anomalies are collected into `mismatches` for the L1
// correction register.
//
// Read-only: no writes, no temp files. Git is invoked as `git show`,
// `git ls-files` and `git rev-parse` only. JSON goes to stdout. Exit code is
// 1 when any violation or mismatch is found, else 0.
//
// Usage: node .ufo/waves/round-21/anchor-census.mjs [--root DIR] [--base REV]

import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { existsSync, readFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const BASE_DEFAULT = '5009ecaa1cce10b895617a585ddd3f7c7c923a84';
const SCRIPT_DIR = dirname(fileURLToPath(import.meta.url));
// .ufo/waves/round-21/anchor-census.mjs -> repo root is three levels up.
const DEFAULT_ROOT = resolve(SCRIPT_DIR, '..', '..', '..');

// Paths that look like credential/auth material are never read or scanned.
const SENSITIVE_RE =
  /(?:^|[\/._-])(?:credentials?|secrets?|tokens?|oauth|passw(?:or)?ds?|id_rsa|id_dsa|id_ecdsa|id_ed25519|agent\.db)(?:[\/._-]|$)|(?:^|[\/])\.env(?:\.|\/)|\.(?:pem|key|p12|pfx|netrc|kubeconfig)$/i;

const KNOWLEDGE_RE = /^corpus\/knowledge\/[^/]+\.md$/;
const LANE_LESSON_RE = /^corpus\/lessons\/round-\d+(?:-recensus)?\.md$/;

// Side cache of buffers/line tables so large payloads never enter JSON.
const BUFFER_CACHE = new Map();

function fail(message, code = 2) {
  process.stderr.write(`anchor-census: ${message}\n`);
  process.exit(code);
}

function parseArgs(argv) {
  const args = { root: DEFAULT_ROOT, base: BASE_DEFAULT };
  for (let i = 0; i < argv.length; i += 1) {
    const a = argv[i];
    if (a === '--root') {
      const v = argv[++i];
      if (!v) fail('--root needs a value');
      args.root = resolve(v);
    } else if (a === '--base') {
      const v = argv[++i];
      if (!v) fail('--base needs a value');
      args.base = v;
    } else if (a === '--help' || a === '-h') {
      process.stdout.write(
        'Usage: node anchor-census.mjs [--root DIR] [--base REV]\n' +
          'Read-only. Emits the moved-reference register as JSON on stdout.\n',
      );
      process.exit(0);
    } else {
      fail(`unknown argument: ${a}`);
    }
  }
  return args;
}

function git(root, gitArgs) {
  try {
    return execFileSync('git', gitArgs, {
      cwd: root,
      encoding: 'buffer',
      maxBuffer: 256 * 1024 * 1024,
      stdio: ['ignore', 'pipe', 'pipe'],
    });
  } catch (err) {
    const stderr = err.stderr ? err.stderr.toString('utf8') : String(err);
    fail(`git ${gitArgs.join(' ')} failed: ${stderr.trim()}`);
  }
}

// `git show <base>:<path>` returning null when the path is absent at base.
// The base revision itself is verified once in main() before this runs.
function gitShowOrNull(root, base, relPath) {
  try {
    return execFileSync('git', ['show', `${base}:${relPath}`], {
      cwd: root,
      encoding: 'buffer',
      maxBuffer: 256 * 1024 * 1024,
      stdio: ['ignore', 'pipe', 'ignore'],
    });
  } catch {
    return null;
  }
}

const sha256 = (buf) => createHash('sha256').update(buf).digest('hex');

// Byte offset of the start of each 1-based line; lineByte[i-1] is line i.
// An empty buffer yields []. A trailing "\n" does not spawn a phantom line.
function lineByteOffsets(buf) {
  const offs = [0];
  for (let i = 0; i < buf.length; i += 1) {
    if (buf[i] === 0x0a && i + 1 < buf.length) offs.push(i + 1);
  }
  return offs;
}

// 1-based inclusive line range -> byte slice. Caller guards range validity.
function lineSlice(buf, offs, start, end) {
  return buf.subarray(offs[start - 1], end < offs.length ? offs[end] : buf.length);
}

// Number of lines a buffer occupies: "\n" count, plus one for an unterminated
// trailing line.
function countLines(buf) {
  if (buf.length === 0) return 0;
  let n = 0;
  for (let i = 0; i < buf.length; i += 1) if (buf[i] === 0x0a) n += 1;
  return buf[buf.length - 1] === 0x0a ? n : n + 1;
}

// Compare referenced line-range bytes with a single trailing line terminator
// normalized away: when the base file had no final LF and the wave added one,
// a citation ending on the last original line still compares equal — the LF
// is a boundary addition, not a byte change to the referenced content.
function rangeBytesEqual(a, b) {
  const strip = (buf) =>
    buf.length > 0 && buf[buf.length - 1] === 0x0a
      ? buf.subarray(0, buf.length - 1)
      : buf;
  return strip(a).equals(strip(b));
}

// Greedy monotonic line alignment used ONLY for violation diagnostics.
// Returns array indexed by old line (0-based) -> new line (1-based) or null.
function greedyLineMap(oldLines, newLines) {
  const map = new Array(oldLines.length).fill(null);
  let j = 0;
  for (let i = 0; i < oldLines.length && j < newLines.length; i += 1) {
    while (j < newLines.length && !newLines[j].equals(oldLines[i])) j += 1;
    if (j < newLines.length) {
      map[i] = j + 1;
      j += 1;
    }
  }
  return map;
}

function analyzeTarget(root, base, relPath, currentBuf) {
  const rec = {
    file: relPath,
    kind: relPath.startsWith('corpus/knowledge/') ? 'knowledge' : 'lesson',
    presentAtBase: true,
    presentInTree: currentBuf !== null,
    preserved: null, // null until both sides are present
    map: null,
    additions: null,
    violation: null,
  };

  const baseBuf = gitShowOrNull(root, base, relPath);

  if (baseBuf === null) {
    rec.presentAtBase = false;
    rec.map = { type: 'new-file', lines: [] };
    return rec;
  }
  if (currentBuf === null) {
    rec.preserved = false;
    rec.violation = { type: 'deleted-in-tree' };
    return rec;
  }

  rec.base = { bytes: baseBuf.length, sha256: sha256(baseBuf) };
  rec.current = { bytes: currentBuf.length, sha256: sha256(currentBuf) };

  const baseOffs = lineByteOffsets(baseBuf);
  const curOffs = lineByteOffsets(currentBuf);
  const oldLineCount = baseOffs.length;
  const newLineCount = curOffs.length;

  BUFFER_CACHE.set(relPath, { baseBuf, currentBuf, baseOffs, curOffs });

  if (baseBuf.equals(currentBuf)) {
    rec.preserved = true;
    rec.map = {
      type: 'offset',
      offset: 0,
      firstOriginalNewLine: 1,
      lastOriginalNewLine: oldLineCount,
      oldLineCount,
      newLineCount,
      sameBytes: true,
    };
    rec.additions = { prefixLines: 0, suffixLines: 0 };
    return rec;
  }

  // Whole-original-byte containment: current = prefix + old + suffix.
  const idx = currentBuf.indexOf(baseBuf);
  if (idx < 0) {
    // Some original byte was changed, deleted or reordered. Build the greedy
    // diagnostic map and count changed original lines.
    const oldLines = baseOffs.map((_o, i) =>
      lineSlice(baseBuf, baseOffs, i + 1, i + 1),
    );
    const newLines = curOffs.map((_o, i) =>
      lineSlice(currentBuf, curOffs, i + 1, i + 1),
    );
    const mapArr = greedyLineMap(oldLines, newLines);
    let firstChanged = null;
    let changed = 0;
    for (let i = 0; i < mapArr.length; i += 1) {
      const at = mapArr[i];
      if (at === null || !newLines[at - 1].equals(oldLines[i])) {
        changed += 1;
        if (firstChanged === null) firstChanged = i + 1;
      }
    }
    rec.preserved = false;
    rec.violation = {
      type: 'original-bytes-changed',
      changedOriginalLines: changed,
      firstChangedOriginalLine: firstChanged,
      baseSha256: sha256(baseBuf),
      currentSha256: sha256(currentBuf),
    };
    rec.map = {
      type: 'greedy',
      offset: null,
      oldLineCount,
      newLineCount,
      lines: mapArr.map((n, i) => ({ old: i + 1, new: n })),
      sameBytes: false,
    };
    rec.additions = null;
    return rec;
  }

  // Contiguous containment found. Detect degenerate ambiguous placement.
  let occurrenceCount = 1;
  for (let p = idx + 1; ; ) {
    const n = currentBuf.indexOf(baseBuf, p);
    if (n < 0) break;
    occurrenceCount += 1;
    p = n + 1;
  }

  const prefixBuf = currentBuf.subarray(0, idx);
  const suffixBuf = currentBuf.subarray(idx + baseBuf.length);

  // Line-boundary contract: a clean prefix ends at a newline (or is empty).
  // A clean suffix normally requires the original to end with a newline.
  // Special case (round-16 shape): if the base has NO final LF, a suffix may
  // begin with a newly added LF that terminates the last original line.
  // That LF is a boundary-only addition — original bytes stay contiguous —
  // and it does not count as a new line or a changed original byte.
  const prefixClean = idx === 0 || currentBuf[idx - 1] === 0x0a;
  const baseEndsLf = baseBuf[baseBuf.length - 1] === 0x0a;
  const terminatingLfAdded =
    !baseEndsLf && suffixBuf.length > 0 && suffixBuf[0] === 0x0a;
  const suffixClean =
    suffixBuf.length === 0 || baseEndsLf || terminatingLfAdded;
  const boundaryClean =
    prefixClean && suffixClean && occurrenceCount === 1;

  rec.preserved = boundaryClean;
  rec.additions = {
    prefixLines: countLines(prefixBuf),
    // The added LF that terminates the old last line is a boundary byte,
    // not a new line of its own.
    suffixLines: countLines(suffixBuf) - (terminatingLfAdded ? 1 : 0),
    ...(terminatingLfAdded ? { terminatingLfAdded: true } : {}),
  };
  rec.map = {
    type: 'offset',
    offset: rec.additions.prefixLines,
    firstOriginalNewLine: rec.additions.prefixLines + 1,
    lastOriginalNewLine: rec.additions.prefixLines + oldLineCount,
    oldLineCount,
    newLineCount,
    sameBytes: true,
    ...(occurrenceCount > 1 ? { ambiguousPlacement: true } : {}),
    ...(boundaryClean ? {} : { misalignedBoundary: true }),
  };
  if (!boundaryClean) {
    rec.violation = {
      type:
        occurrenceCount > 1 ? 'ambiguous-placement' : 'misaligned-boundary',
      detail:
        'original bytes are contiguous but additions do not sit on clean line boundaries',
      occurrences: occurrenceCount,
      prefixBoundaryClean: prefixClean,
      suffixBoundaryClean: suffixClean,
    };
  }
  return rec;
}

function buildBasenameIndex(targets) {
  const index = new Map();
  for (const t of targets) {
    const base = t.slice(t.lastIndexOf('/') + 1);
    if (!index.has(base)) index.set(base, []);
    index.get(base).push(t);
  }
  return index;
}

function escapeRe(s) {
  return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function scanReferences({ root, scanFiles, targets, targetData }) {
  const basenameIndex = buildBasenameIndex(targets);
  const basenames = [...basenameIndex.keys()]
    .sort((a, b) => b.length - a.length)
    .map(escapeRe)
    .join('|');
  // Optional relative path prefix + basename + :line + optional -end range.
  const refRe = new RegExp(
    `(?<![\\w.\\-/])(?:([\\w.\\-~/]*)/)?(${basenames}):(\\d+)(?:-(\\d+))?`,
    'g',
  );

  const register = [];
  const mismatches = [];
  let scanned = 0;
  let skippedSensitive = 0;
  let skippedBinary = 0;

  for (const rel of scanFiles) {
    if (SENSITIVE_RE.test(rel)) {
      skippedSensitive += 1;
      continue;
    }
    const abs = join(root, rel);
    let buf;
    try {
      buf = readFileSync(abs);
    } catch {
      continue; // vanished mid-run; wave still in flight
    }
    if (buf.includes(0x00)) {
      skippedBinary += 1;
      continue;
    }
    scanned += 1;
    const srcLines = buf.toString('utf8').split('\n');
    if (srcLines.length > 0 && srcLines[srcLines.length - 1] === '') {
      srcLines.pop();
    }
    for (let ln = 0; ln < srcLines.length; ln += 1) {
      const line = srcLines[ln];
      refRe.lastIndex = 0;
      let m;
      while ((m = refRe.exec(line)) !== null) {
        const [, pathPrefix, baseName, sStart, sEnd] = m;
        const citedStart = Number(sStart);
        const citedEnd = sEnd === undefined ? citedStart : Number(sEnd);
        const candidates = basenameIndex.get(baseName) ?? [];
        const entry = {
          source: { file: rel, line: ln + 1, text: m[0] },
          cited: {
            basename: baseName,
            pathPrefix: pathPrefix ?? null,
            start: citedStart,
            end: citedEnd,
          },
        };

        if (candidates.length === 0) continue; // unreachable; defensive
        if (candidates.length > 1) {
          entry.status = 'ambiguous-target';
          entry.candidates = candidates;
          mismatches.push({ type: 'ambiguous-target', ...entry });
          register.push(entry);
          continue;
        }

        const target = candidates[0];
        const data = targetData.get(target);
        entry.target = { file: target };

        // A stated path prefix must be a directory-suffix of the real target
        // path (bare basename, `knowledge/x.md` and `corpus/knowledge/x.md`
        // all resolve; contradictory directories flag).
        if (
          pathPrefix &&
          target !== `${pathPrefix}/${baseName}` &&
          !target.endsWith(`/${pathPrefix}/${baseName}`)
        ) {
          entry.status = 'path-mismatch';
          mismatches.push({ type: 'path-mismatch', ...entry });
          register.push(entry);
          continue;
        }

        if (!data || !data.presentAtBase) {
          entry.status = 'target-not-at-base';
          mismatches.push({ type: 'target-not-at-base', ...entry });
          register.push(entry);
          continue;
        }
        if (!data.preserved) {
          entry.status = 'unresolvable-target-violation';
          mismatches.push({ type: 'unresolvable-target-violation', ...entry });
          register.push(entry);
          continue;
        }

        const { offset, oldLineCount } = data.map;
        if (citedStart < 1 || citedEnd < citedStart || citedEnd > oldLineCount) {
          entry.status = 'out-of-range';
          entry.target.oldLineCount = oldLineCount;
          mismatches.push({ type: 'out-of-range', ...entry });
          register.push(entry);
          continue;
        }

        const newStart = citedStart + offset;
        const newEnd = citedEnd + offset;
        const { baseBuf, currentBuf, baseOffs, curOffs } =
          BUFFER_CACHE.get(target);
        const sameBytes = rangeBytesEqual(
          lineSlice(baseBuf, baseOffs, citedStart, citedEnd),
          lineSlice(currentBuf, curOffs, newStart, newEnd),
        );

        entry.resolved = {
          oldRange: [citedStart, citedEnd],
          newRange: [newStart, newEnd],
        };
        entry.sameBytes = sameBytes;
        entry.staleCitation = offset !== 0;
        entry.status =
          offset === 0 ? 'current' : sameBytes ? 'moved' : 'moved-bytes-differ';
        if (!sameBytes) {
          mismatches.push({ type: 'moved-bytes-differ', ...entry });
        }
        register.push(entry);
      }
    }
  }

  return {
    register,
    mismatches,
    scanStats: { scanned, skippedSensitive, skippedBinary },
  };
}

function main() {
  const { root, base } = parseArgs(process.argv.slice(2));
  if (!existsSync(join(root, '.git'))) {
    fail(`--root ${root} does not look like a git work tree`);
  }
  // Verify the base revision resolves before treating per-path `git show`
  // failures as absent-at-base.
  git(root, ['rev-parse', '--verify', '--quiet', `${base}^{commit}`]);

  const lsOut = git(root, ['ls-files', '-z']).toString('latin1');
  const trackedFiles = lsOut.split('\0').filter(Boolean).sort();

  const targets = trackedFiles.filter(
    (p) => KNOWLEDGE_RE.test(p) || LANE_LESSON_RE.test(p),
  );

  const targetData = new Map();
  const fileReports = [];
  const violations = [];
  for (const rel of targets) {
    const abs = join(root, rel);
    const curBuf = existsSync(abs) ? readFileSync(abs) : null;
    const rec = analyzeTarget(root, base, rel, curBuf);
    targetData.set(rel, rec);
    fileReports.push(rec);
    if (rec.violation) violations.push({ file: rel, ...rec.violation });
  }

  // Scan ALL tracked files, targets included — lessons cite each other.
  const { register, mismatches, scanStats } = scanReferences({
    root,
    scanFiles: trackedFiles,
    targets,
    targetData,
  });

  const added = (r, key) => (r.preserved && r.additions ? r.additions[key] : 0);
  const out = {
    tool: 'anchor-census',
    base,
    root,
    summary: {
      targets: targets.length,
      unchanged: fileReports.filter(
        (r) =>
          r.preserved &&
          added(r, 'prefixLines') === 0 &&
          added(r, 'suffixLines') === 0,
      ).length,
      prefixAdded: fileReports.filter(
        (r) => r.preserved && added(r, 'prefixLines') > 0,
      ).length,
      suffixAdded: fileReports.filter(
        (r) => r.preserved && added(r, 'suffixLines') > 0,
      ).length,
      newFiles: fileReports.filter((r) => !r.presentAtBase).length,
      violations: violations.length,
      references: register.length,
      referencesMoved: register.filter((r) => r.status === 'moved').length,
      referencesStaleCitation: register.filter(
        (r) => r.staleCitation === true,
      ).length,
      mismatches: mismatches.length,
      scanned: scanStats.scanned,
      skippedSensitive: scanStats.skippedSensitive,
      skippedBinary: scanStats.skippedBinary,
    },
    ok: violations.length === 0 && mismatches.length === 0,
    violations,
    files: fileReports,
    register,
    mismatches,
  };

  process.stdout.write(`${JSON.stringify(out, null, 2)}\n`);
  process.exit(out.ok ? 0 : 1);
}

main();
