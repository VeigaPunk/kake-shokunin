#!/usr/bin/env node
// corpus-contract — kake-shokunin corpus shape gate (S019 metadata/gate contract).
//
// Two read-only contract checks over the lane corpus, both intentionally
// syntactic (shape, not truth — field honesty and gate-content review belong
// to other seats):
//
//   missing_metadata  corpus/knowledge/*.md — the provenance trio
//                     (source: / verified-at: / recheck:, one line each, any
//                     case, ≤3 leading spaces) must appear with a non-empty
//                     value inside the FIRST 8 lines. Basenames containing
//                     verifier/aggregator/operator are excluded (not lane-
//                     authored knowledge entries). One finding per missing
//                     field; the id embeds path and field:
//                     missing_metadata:<file>:<field>
//   missing_gate      corpus/lessons/<name>.md where the basename matches the
//                     exact lane-author regex /^round-\d+(?:-recensus)?\.md$/
//                     must contain a non-empty level-2 "## Gate" ATX section
//                     (a "## Gate — …" suffix variant counts; "### Gate",
//                     "## Gatekeeping", and headings inside fenced code do
//                     not). Every other lessons basename — aggregator audits,
//                     verifier spot-checks, operator notes — is excluded.
//                     Exactly one finding per offending lesson, id
//                     missing_gate:<file>; detail is no-gate-section or
//                     empty-gate-section.
//
// Exit contract: 0 = clean · 1 = findings · 2 = could-not-evaluate
//                (unreadable/missing corpus dirs or files) · 64 = usage error.
//                Exit 2 outranks exit 1 when both apply.
//
// READ-ONLY BY CONSTRUCTION: the only fs write calls in this file sit inside
// SELFTEST-WRITES-BEGIN/END marker pairs in selftest(), which builds hermetic
// fixtures under an fs.mkdtempSync dir in os.tmpdir(). The normal path never
// writes. --selftest proves this by scanning its own source with
// writeConfinement() (residual bypasses are listed above that function).
//
// Usage:
//   node scripts/corpus-contract.mjs [--json] [--root DIR] [--selftest] [--help]
//
//   (default)   human lines, one per finding/skip/error, then a result line
//   --json      one JSON object:
//               {tool,contract,root,ok,code,counts,findings,skipped,errors}
//   --root DIR  lane repo root (default: this script's parent directory — the
//               lane checkout). The corpus is <root>/corpus/{knowledge,lessons}.
//   --selftest  hermetic fixtures + self-source read-only assertion; prints a
//               case table, exits 0 when every case passes else 1 (2 when the
//               selftest itself cannot run)
//   --help      this text
//
// Output is deterministic: sorted findings/skips, no timestamps.

'use strict';
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const SELF = fileURLToPath(import.meta.url);

// ── contract constants ─────────────────────────────────────────────────────
const FIRST_N = 8;
const TRIO_FIELDS = ['source', 'verified-at', 'recheck'];
// A trio field is a line-start label (≤3 leading spaces), a colon, then a
// non-empty value on THE SAME LINE — per-line matching only, [ \t] whitespace
// never crosses a line break. `source:` / `source:   ` / `source` alone are
// all absent, even when the next line is another field's key.
const TRIO_RE = /^[ \t]{0,3}(source|verified-at|recheck)[ \t]*:(.*)$/i;
// Basename exclusion shared by both checks (lesson filenames are additionally
// constrained by the exact lane-author regex below, which already excludes
// every -aggregator-* / -verifier-* name; the basename test stays so the
// exclusion is explicit rather than an accident of the regex).
const EXCLUDE_RE = /verifier|aggregator|operator/i;
const LANE_LESSON_RE = /^round-\d+(?:-recensus)?\.md$/;
// "## Gate" = ATX level 2, exact word Gate (suffix subtitles allowed);
// "##Gate" is not a heading, "### Gate" is the wrong level, "## Gatekeeping"
// is a different word.
const GATE_WORD_RE = /^Gate\b/;
const ATX_RE = /^(#{1,6})(?:\s|$)/;
const FENCE_RE = /^\s{0,3}(`{3,}|~{3,})/;

const ID_METADATA = 'missing_metadata';
const ID_GATE = 'missing_gate';

// ── CLI ────────────────────────────────────────────────────────────────────
function parseArgs(argv) {
  const o = { json: false, root: null, selftest: false, help: false };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--json') o.json = true;
    else if (a === '--selftest') o.selftest = true;
    else if (a === '--help' || a === '-h') o.help = true;
    else if (a === '--root') o.root = argv[++i];
    else if (a.startsWith('--root=')) o.root = a.slice(7);
    else { console.error(`corpus-contract: unknown flag: ${a}`); return { err: 64 }; }
  }
  if (o.root === undefined || o.root === '') {
    console.error('corpus-contract: --root needs a directory');
    return { err: 64 };
  }
  return o;
}

function usage() {
  console.log(`corpus-contract — S019 corpus shape gate (provenance trio + lesson Gate sections).

Usage: node scripts/corpus-contract.mjs [--json] [--root DIR] [--selftest] [--help]

  (default)   human lines, one per finding/skip/error, then a result line
  --json      one JSON object:
              {tool,contract,root,ok,code,counts,findings,skipped,errors}
  --root DIR  lane repo root (default: this script's parent directory)
  --selftest  hermetic fixture battery under the OS temp dir; exit 0 on all-pass
  --help      this text

Checks:
  corpus/knowledge/*.md     source:/verified-at:/recheck: non-empty in first
                            ${FIRST_N} lines; verifier/aggregator/operator basenames excluded
  corpus/lessons/round-N.md every exact /^round-\\d+(?:-recensus)?\\.md$/ basename
                            carries a non-empty level-2 "## Gate" section

Finding ids embed the path: missing_metadata:<file>:<field> · missing_gate:<file>
Exit: 0 clean · 1 findings · 2 could-not-evaluate · 64 usage error.
Read-only: no file writes outside the --selftest fixture dir.`);
}

// ── checks ─────────────────────────────────────────────────────────────────
// Returns the sorted trio-field names absent (or empty-valued) in the first
// FIRST_N lines of file.
function missingTrio(file) {
  const head = fs.readFileSync(file, 'utf8').split(/\r?\n/, FIRST_N);
  const seen = new Set();
  for (const line of head) {
    const m = TRIO_RE.exec(line);
    if (m && /\S/.test(m[2])) seen.add(m[1].toLowerCase());
  }
  return TRIO_FIELDS.filter((f) => !seen.has(f));
}

// Returns 'ok' | 'empty-gate-section' | 'no-gate-section' for one lesson.
// Fence-aware: a "## Gate" inside ```/~~~ fenced code is not a section. A
// section is non-empty when it holds at least one non-blank line (a deeper
// heading like "### Candidates" counts as content) before the next level-1/2
// heading or EOF. A repeated "## Gate" restarts the section, so "exists a
// non-empty Gate section" is the verdict.
function gateStatus(file) {
  const lines = fs.readFileSync(file, 'utf8').split(/\r?\n/);
  let fence = null; // '`' | '~' | null
  let inGate = false;
  let hasContent = false;
  for (const raw of lines) {
    const t = raw.trim();
    const f = FENCE_RE.exec(raw);
    if (f) {
      const mark = f[1][0];
      if (fence === null) fence = mark;
      else if (fence === mark) fence = null;
      if (inGate) hasContent = true;
      continue;
    }
    if (fence) { if (inGate && t) hasContent = true; continue; }
    const h = ATX_RE.exec(t);
    if (h) {
      if (h[1].length === 2 && GATE_WORD_RE.test(t.slice(h[1].length).trimStart())) {
        inGate = true;
        hasContent = false;
        continue;
      }
      if (inGate && h[1].length <= 2) return hasContent ? 'ok' : 'empty-gate-section';
      if (inGate) hasContent = true; // deeper heading = section content
      continue;
    }
    if (inGate && t) hasContent = true;
  }
  if (inGate) return hasContent ? 'ok' : 'empty-gate-section';
  return 'no-gate-section';
}

// ── evaluation ─────────────────────────────────────────────────────────────
function listMd(dir) {
  return fs.readdirSync(dir, { withFileTypes: true })
    .filter((d) => d.isFile() && d.name.endsWith('.md'))
    .map((d) => d.name)
    .sort();
}

function evaluate(root) {
  const findings = [];
  const skipped = [];
  const errors = [];
  const counts = { knowledgeChecked: 0, lessonsChecked: 0, skipped: 0 };

  const rel = (...p) => path.join('corpus', ...p);

  // knowledge: every *.md not excluded by basename must carry the trio.
  const kdir = path.join(root, 'corpus', 'knowledge');
  let names;
  try { names = listMd(kdir); } catch (e) {
    names = null;
    errors.push({ file: rel('knowledge'), error: `unreadable: ${e.code || e.message}` });
  }
  if (names) {
    for (const name of names) {
      const file = rel('knowledge', name);
      if (EXCLUDE_RE.test(name)) { skipped.push({ file, reason: 'excluded-name' }); continue; }
      counts.knowledgeChecked++;
      try {
        const missing = missingTrio(path.join(kdir, name));
        for (const field of missing) findings.push({ id: `${ID_METADATA}:${file}:${field}`, file, field });
      } catch (e) {
        errors.push({ file, error: `unreadable: ${e.code || e.message}` });
      }
    }
  }

  // lessons: only the exact lane-author regex is gated.
  const ldir = path.join(root, 'corpus', 'lessons');
  try { names = listMd(ldir); } catch (e) {
    names = null;
    errors.push({ file: rel('lessons'), error: `unreadable: ${e.code || e.message}` });
  }
  if (names) {
    for (const name of names) {
      const file = rel('lessons', name);
      if (!LANE_LESSON_RE.test(name)) { skipped.push({ file, reason: 'not-lane-author' }); continue; }
      if (EXCLUDE_RE.test(name)) { skipped.push({ file, reason: 'excluded-name' }); continue; }
      counts.lessonsChecked++;
      try {
        const status = gateStatus(path.join(ldir, name));
        if (status !== 'ok') findings.push({ id: `${ID_GATE}:${file}`, file, detail: status });
      } catch (e) {
        errors.push({ file, error: `unreadable: ${e.code || e.message}` });
      }
    }
  }

  const fieldRank = (f) => (f.field ? TRIO_FIELDS.indexOf(f.field) : 0);
  findings.sort((a, b) => (a.file === b.file ? fieldRank(a) - fieldRank(b) : (a.file < b.file ? -1 : 1)));
  skipped.sort((a, b) => (a.file < b.file ? -1 : 1));
  errors.sort((a, b) => (a.file < b.file ? -1 : 1));
  counts.skipped = skipped.length;

  const code = errors.length ? 2 : findings.length ? 1 : 0;
  return { code, counts, findings, skipped, errors };
}

// ── reporting ──────────────────────────────────────────────────────────────
function emit(root, result, json) {
  if (json) {
    console.log(JSON.stringify({
      tool: 'corpus-contract',
      contract: 'S019',
      root,
      ok: result.code === 0,
      code: result.code,
      counts: result.counts,
      findings: result.findings,
      skipped: result.skipped,
      errors: result.errors,
    }));
    return;
  }
  console.log('corpus-contract — corpus/knowledge trio(first 8 lines) + corpus/lessons lane-author ## Gate');
  console.log(`root: ${root}`);
  for (const f of result.findings) {
    console.log(`FAIL ${f.id}${f.detail ? `  ${f.detail}` : ''}`);
  }
  for (const s of result.skipped) console.log(`SKIP ${s.reason}  ${s.file}`);
  for (const e of result.errors) console.log(`ERROR ${e.file}: ${e.error}`);
  const c = result.counts;
  console.log(`result: ${result.findings.length} findings · ${c.knowledgeChecked} knowledge entries · ${c.lessonsChecked} lane lessons · ${c.skipped} skipped · ${result.errors.length} errors — exit ${result.code}`);
}

// ── --selftest: hermetic fixtures + self-source read-only assertion ────────
// Static read-only proof: every fs write-API call in this file must sit inside
// a // SELFTEST-WRITES-BEGIN … // SELFTEST-WRITES-END line pair.
function writeConfinement(lines) {
  const syncNames = [
    'writeFile', 'mkdir', 'appendFile', 'rm', 'unlink', 'rmdir', 'copyFile',
    'rename', 'cp', 'truncate', 'symlink', 'link', 'write', 'open', 'mkdtemp',
  ].map((name) => `${name}Sync`);
  const directNames = [
    'createWriteStream', 'writeFile', 'mkdir', 'appendFile', 'copyFile',
    'rename', 'cp', 'truncate', 'symlink', 'link', 'write', 'open', 'rm',
    'unlink', 'rmdir', 'mkdtemp',
  ];
  const apis = [...syncNames, ...directNames];
  const re = new RegExp(`(?:^|[^A-Za-z0-9_$])(${apis.join('|')})\\s*\\(`);
  const violations = [];
  const regions = [];
  const errors = [];
  const allowed = new Array(lines.length).fill(false);
  let open = false;
  let openLine = null;
  for (let i = 0; i < lines.length; i++) {
    const t = lines[i].trim();
    if (/^\/\/ SELFTEST-WRITES-BEGIN(?: \(.+\))?$/.test(t)) {
      if (open) errors.push(`nested BEGIN at ${i + 1}`);
      else { open = true; openLine = i + 1; regions.push(`B${i + 1}`); }
    }
    if (open) allowed[i] = true;
    if (t === '// SELFTEST-WRITES-END') {
      if (!open) errors.push(`unbalanced END at ${i + 1}`);
      else { open = false; openLine = null; regions.push(`E${i + 1}`); }
    }
  }
  if (open) errors.push(`unterminated BEGIN at ${openLine}`);
  for (let i = 0; i < lines.length; i++) {
    if (lines[i].trim().startsWith('//')) continue;
    if (re.test(lines[i]) && !allowed[i]) violations.push(`${i + 1}: ${lines[i].trim().slice(0, 70)}`);
  }
  return { violations, regions, errors };
}
// Covered: writeFileSync, mkdirSync, appendFileSync, rmSync, unlinkSync,
// rmdirSync, copyFileSync, renameSync, cpSync, truncateSync, symlinkSync,
// linkSync, writeSync, openSync, mkdtempSync, createWriteStream, plus direct
// calls named writeFile, mkdir, appendFile, copyFile, rename, cp, truncate,
// symlink, link, write, open, rm, unlink, rmdir, mkdtemp.
// Residual bypasses (not covered): aliases, bracket access, a call split
// across lines, metadata/fd writes (chmod, chown, utimes, ftruncate, writev,
// fsync), and execFileSync/child-process side effects — selftest children are
// invoked only in --root/--json read-only mode.

// ── pinned fixture expectations ────────────────────────────────────────────
// These literals are the stable contract: child runs below are compared
// byte-for-byte (JSON.stringify) against them.
const EXPECTED_CLEAN = {
  code: 0,
  counts: { knowledgeChecked: 5, lessonsChecked: 3, skipped: 5 },
  findings: [],
  skipped: [
    { file: 'corpus/knowledge/verifier-notes.md', reason: 'excluded-name' },
    { file: 'corpus/lessons/operator-notes.md', reason: 'not-lane-author' },
    { file: 'corpus/lessons/round-2-extra.md', reason: 'not-lane-author' },
    { file: 'corpus/lessons/round-20-verifier-spotcheck.md', reason: 'not-lane-author' },
    { file: 'corpus/lessons/round-4-aggregator-audit.md', reason: 'not-lane-author' },
  ],
  errors: [],
};
const EXPECTED_FAIL = {
  code: 1,
  counts: { knowledgeChecked: 5, lessonsChecked: 7, skipped: 2 },
  findings: [
    { id: 'missing_metadata:corpus/knowledge/bare-then-key.md:source', file: 'corpus/knowledge/bare-then-key.md', field: 'source' },
    { id: 'missing_metadata:corpus/knowledge/empty-fields.md:source', file: 'corpus/knowledge/empty-fields.md', field: 'source' },
    { id: 'missing_metadata:corpus/knowledge/empty-fields.md:verified-at', file: 'corpus/knowledge/empty-fields.md', field: 'verified-at' },
    { id: 'missing_metadata:corpus/knowledge/empty-fields.md:recheck', file: 'corpus/knowledge/empty-fields.md', field: 'recheck' },
    { id: 'missing_metadata:corpus/knowledge/late-trio.md:source', file: 'corpus/knowledge/late-trio.md', field: 'source' },
    { id: 'missing_metadata:corpus/knowledge/late-trio.md:verified-at', file: 'corpus/knowledge/late-trio.md', field: 'verified-at' },
    { id: 'missing_metadata:corpus/knowledge/late-trio.md:recheck', file: 'corpus/knowledge/late-trio.md', field: 'recheck' },
    { id: 'missing_metadata:corpus/knowledge/no-trio.md:source', file: 'corpus/knowledge/no-trio.md', field: 'source' },
    { id: 'missing_metadata:corpus/knowledge/no-trio.md:verified-at', file: 'corpus/knowledge/no-trio.md', field: 'verified-at' },
    { id: 'missing_metadata:corpus/knowledge/no-trio.md:recheck', file: 'corpus/knowledge/no-trio.md', field: 'recheck' },
    { id: 'missing_metadata:corpus/knowledge/partial.md:verified-at', file: 'corpus/knowledge/partial.md', field: 'verified-at' },
    { id: 'missing_metadata:corpus/knowledge/partial.md:recheck', file: 'corpus/knowledge/partial.md', field: 'recheck' },
    { id: 'missing_gate:corpus/lessons/round-2-recensus.md', file: 'corpus/lessons/round-2-recensus.md', detail: 'empty-gate-section' },
    { id: 'missing_gate:corpus/lessons/round-2.md', file: 'corpus/lessons/round-2.md', detail: 'no-gate-section' },
    { id: 'missing_gate:corpus/lessons/round-3.md', file: 'corpus/lessons/round-3.md', detail: 'empty-gate-section' },
    { id: 'missing_gate:corpus/lessons/round-4.md', file: 'corpus/lessons/round-4.md', detail: 'no-gate-section' },
    { id: 'missing_gate:corpus/lessons/round-5.md', file: 'corpus/lessons/round-5.md', detail: 'no-gate-section' },
    { id: 'missing_gate:corpus/lessons/round-6.md', file: 'corpus/lessons/round-6.md', detail: 'no-gate-section' },
  ],
  skipped: [
    { file: 'corpus/knowledge/aggregator-log.md', reason: 'excluded-name' },
    { file: 'corpus/lessons/round-8-aggregator-coldrun.md', reason: 'not-lane-author' },
  ],
  errors: [],
};
const EXPECTED_BARE = {
  code: 0,
  counts: { knowledgeChecked: 0, lessonsChecked: 0, skipped: 0 },
  findings: [],
  skipped: [],
  errors: [],
};

async function selftest() {
  const cases = [];
  const run = (args) => {
    try {
      const stdout = execFileSync(process.execPath, [SELF, ...args], {
        encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'],
      });
      return { code: 0, stdout };
    } catch (e) {
      return { code: e.status === undefined ? -1 : e.status, stdout: String(e.stdout || ''), stderr: String(e.stderr || '') };
    }
  };
  const project = (r) => {
    let parsed = null;
    try { parsed = JSON.parse(r.stdout); } catch { /* non-JSON stdout */ }
    if (!parsed) return { exit: r.code, parse: 'non-json' };
    return {
      exit: r.code,
      code: parsed.code,
      counts: parsed.counts,
      findings: parsed.findings,
      skipped: parsed.skipped,
      errors: parsed.errors,
    };
  };
  const eq = (a, b) => JSON.stringify(a) === JSON.stringify(b);
  const FENCE = '`'.repeat(3);

  // SELFTEST-WRITES-BEGIN (hermetic fixture build — every write in this file)
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'kake-corpus-contract-'));
  const okRoot = path.join(tmp, 'ok');
  const badRoot = path.join(tmp, 'bad');
  const bareRoot = path.join(tmp, 'bare');
  for (const root of [okRoot, badRoot, bareRoot]) {
    fs.mkdirSync(path.join(root, 'corpus', 'knowledge'), { recursive: true });
    fs.mkdirSync(path.join(root, 'corpus', 'lessons'), { recursive: true });
  }
  const put = (root, rel, text) => fs.writeFileSync(path.join(root, rel), text);

  // clean corpus: trio variants (case, spacing, indent, line-8 boundary),
  // gate variants (suffix subtitle, subheading-only content), exclusions.
  put(okRoot, 'corpus/knowledge/good.md',
    'source: fixture S001\nverified-at: 2026-10-20 fixture\nrecheck: fixture command\n\n# Good entry\n');
  put(okRoot, 'corpus/knowledge/case-variant.md',
    'Source: x\nVERIFIED-AT: y\nRecheck: z\n\n# Case variant\n');
  put(okRoot, 'corpus/knowledge/spaced-colon.md',
    'source : x\nverified-at : y\nrecheck : z\n\n# Spaced colons\n');
  put(okRoot, 'corpus/knowledge/indented.md',
    '  source: x\n   verified-at: y\n\trecheck: z\n\n# Indented trio\n');
  put(okRoot, 'corpus/knowledge/line8.md',
    '# Late start\n\n- a\n- b\n- c\nsource: x\nverified-at: y\nrecheck: z\n\n# Body\n');
  put(okRoot, 'corpus/knowledge/verifier-notes.md',
    '# Verifier notes\n\nno trio — excluded by basename\n');
  put(okRoot, 'corpus/knowledge/freshness-pins.json',
    '{"pins":{}}\n');
  put(okRoot, 'corpus/lessons/round-1.md',
    '# Lesson — round 1\n\n## Learned\n\n- x\n\n## Gate\n\n- admitted: x\n');
  put(okRoot, 'corpus/lessons/round-19-recensus.md',
    '# Lesson — round 19 recensus\n\n## Learned\n\n- x\n\n## Gate — round-21 retrospective reconstruction\n\n### Candidates\n\n- a\n');
  put(okRoot, 'corpus/lessons/round-7.md',
    '# Lesson — round 7\n\n## Learned\n\n- x\n\n## Gate\n### Verdict\n- ok\n');
  put(okRoot, 'corpus/lessons/round-4-aggregator-audit.md',
    '# Aggregator audit\n\nno gate — excluded by lane-author regex\n');
  put(okRoot, 'corpus/lessons/round-20-verifier-spotcheck.md',
    '# Verifier spotcheck\n\nno gate — excluded\n');
  put(okRoot, 'corpus/lessons/round-2-extra.md',
    '# Round 2 extra\n\nno gate — excluded\n');
  put(okRoot, 'corpus/lessons/operator-notes.md',
    '# Operator notes\n\nno gate — excluded\n');

  // failing corpus: malformed/empty trio fields, trio past the window,
  // empty/fenced/wrong-level gate sections, exclusions.
  put(badRoot, 'corpus/knowledge/empty-fields.md',
    'source:\nverified-at:   \nrecheck:\n# Empty fields\n');
  // Reviewer-driven negative: a bare `source:` label must not satisfy the
  // field by absorbing the next line's key — matching is strictly per-line.
  put(badRoot, 'corpus/knowledge/bare-then-key.md',
    'source:\nverified-at: y\nrecheck: z\n\n# Bare source label\n');
  put(badRoot, 'corpus/knowledge/late-trio.md',
    '# Late trio\n\nfiller\nfiller\nfiller\nfiller\nfiller\nfiller\nsource: x\nverified-at: y\nrecheck: z\n');
  put(badRoot, 'corpus/knowledge/no-trio.md',
    '# No trio\n\nJust prose.\n');
  put(badRoot, 'corpus/knowledge/partial.md',
    'source: fixture S999\nverified-at:\n# Partial\n');
  put(badRoot, 'corpus/knowledge/aggregator-log.md',
    '# Aggregator log\n\nno trio — excluded by basename\n');
  put(badRoot, 'corpus/lessons/round-2-recensus.md',
    '# Lesson — round 2 recensus\n\n## Learned\n\n- x\n\n## Gate\n\n## Open\n\n- y\n');
  put(badRoot, 'corpus/lessons/round-2.md',
    '# Lesson — round 2\n\n## Learned\n\n- x\n\n## Open\n\n- y\n');
  put(badRoot, 'corpus/lessons/round-3.md',
    '# Lesson — round 3\n\n## Learned\n\n- x\n\n## Gate\n');
  put(badRoot, 'corpus/lessons/round-4.md',
    '# Lesson — round 4\n\n' + FENCE + 'markdown\n## Gate\n\n- looks like a gate but is fenced\n' + FENCE + '\n\n## Open\n\n- y\n');
  put(badRoot, 'corpus/lessons/round-5.md',
    '# Lesson — round 5\n\n## Gatekeeping notes\n\n- x\n');
  put(badRoot, 'corpus/lessons/round-6.md',
    '# Lesson — round 6\n\n### Gate\n\n- wrong level\n');
  put(badRoot, 'corpus/lessons/round-7.md',
    '# Lesson — round 7\n\n## Learned\n\n- x\n\n## Gate\n\n- admitted: x\n');
  put(badRoot, 'corpus/lessons/round-8-aggregator-coldrun.md',
    '# Cold run\n\nno gate — excluded\n');
  // SELFTEST-WRITES-END

  // c1 — clean corpus: exit 0 and the exact pinned projection.
  {
    const r = run(['--json', '--root', okRoot]);
    const got = project(r);
    const want = { exit: 0, ...EXPECTED_CLEAN };
    cases.push({
      id: 'c1 clean corpus — exit 0, zero findings, exclusions pinned',
      expect: JSON.stringify(want),
      got: JSON.stringify(got),
      pass: eq(got, want),
    });
  }

  // c2 — failing corpus: exit 1 and every pinned finding id/file/detail.
  {
    const r = run(['--json', '--root', badRoot]);
    const got = project(r);
    const want = { exit: 1, ...EXPECTED_FAIL };
    cases.push({
      id: 'c2 failing corpus — exit 1, pinned missing_metadata/missing_gate ids',
      expect: JSON.stringify(want),
      got: JSON.stringify(got),
      pass: eq(got, want),
    });
  }

  // c3 — non-JSON mode still exits 1 on the failing corpus (exit contract
  // independent of output mode).
  {
    const r = run(['--root', badRoot]);
    cases.push({
      id: 'c3 human output mode — same exit contract (1)',
      expect: 'exit 1',
      got: `exit ${r.code}`,
      pass: r.code === 1,
    });
  }

  // c4 — bare corpus (empty knowledge/ + lessons/ dirs): vacuously clean.
  {
    const r = run(['--json', '--root', bareRoot]);
    const got = project(r);
    const want = { exit: 0, ...EXPECTED_BARE };
    cases.push({
      id: 'c4 bare corpus — exit 0, zero checked',
      expect: JSON.stringify(want),
      got: JSON.stringify(got),
      pass: eq(got, want),
    });
  }

  // c5 — absent root: both corpus dirs unreadable → could-not-evaluate.
  {
    const r = run(['--json', '--root', path.join(tmp, 'absent')]);
    const got = project(r);
    const errs = Array.isArray(got.errors) ? got.errors : [];
    const pass = got.exit === 2 && got.code === 2 && errs.length === 2
      && errs[0].file === 'corpus/knowledge' && errs[1].file === 'corpus/lessons'
      && Array.isArray(got.findings) && got.findings.length === 0;
    cases.push({
      id: 'c5 absent root — exit 2, two unreadable-dir errors, no findings',
      expect: 'exit 2 · errors=[corpus/knowledge, corpus/lessons] · findings=[]',
      got: `exit ${got.exit} · errors=${JSON.stringify(errs.map((e) => e.file))} · findings=${JSON.stringify(got.findings)}`,
      pass,
    });
  }

  // c6 — usage errors: unknown flag, bare --root, empty --root=.
  {
    const a = run(['--bogus']);
    const b = run(['--root']);
    const c = run(['--root=']);
    cases.push({
      id: 'c6 usage — unknown flag, bare --root, empty --root= all exit 64',
      expect: 'exit 64 · exit 64 · exit 64',
      got: `exit ${a.code} · exit ${b.code} · exit ${c.code}`,
      pass: a.code === 64 && b.code === 64 && c.code === 64,
    });
  }

  // e1 — static read-only proof over this file's own source, plus synthetic
  // positive/negative controls for the scanner itself. probeWrite is built by
  // concatenation so these control lines stay invisible to the scanner.
  {
    const src = fs.readFileSync(SELF, 'utf8').split('\n');
    const report = writeConfinement(src);
    const probeWrite = '  fs.writeFile' + 'Sync(p, t);';
    const positive = writeConfinement(['const x = 1;', probeWrite]).violations.length === 1;
    const negative = writeConfinement([
      'const x = 1;',
      '// SELFTEST-WRITES-BEGIN (control)',
      probeWrite,
      '// SELFTEST-WRITES-END',
    ]).violations.length === 0;
    const decl = src.findIndex((l) => l.startsWith('async function selftest()')) + 1;
    const inside = decl > 0 && report.regions.length >= 2
      && report.regions.every((r) => Number(r.slice(1)) > decl);
    cases.push({
      id: 'e1 write confinement — no fs write outside selftest markers',
      expect: '0 violations · 0 errors · regions inside selftest() · controls pass',
      got: `${report.violations.length} violations [${report.violations.join(' | ')}] · errors [${report.errors.join(' | ')}] · regions ${report.regions.join(',')} inside=${inside ? 'yes' : 'NO'} · controls positive=${positive ? 'PASS' : 'FAIL'} negative=${negative ? 'PASS' : 'FAIL'}`,
      pass: report.violations.length === 0 && report.errors.length === 0
        && inside && positive && negative,
    });
  }

  // SELFTEST-WRITES-BEGIN (fixture cleanup)
  fs.rmSync(tmp, { recursive: true, force: true });
  // SELFTEST-WRITES-END

  const failed = cases.filter((c) => !c.pass);
  console.log('corpus-contract --selftest');
  for (const c of cases) console.log(`  ${c.pass ? 'PASS' : 'FAIL'}  ${c.id}\n        expect: ${c.expect}\n        got:    ${c.got}`);
  console.log(`selftest: ${cases.length - failed.length}/${cases.length} passed`);
  return failed.length ? 1 : 0;
}

// ── main ───────────────────────────────────────────────────────────────────
async function main() {
  const o = parseArgs(process.argv.slice(2));
  if (o.err) { process.exit(o.err); return; }
  if (o.help) { usage(); return; }
  if (o.selftest) { process.exit(await selftest()); return; }
  const root = o.root ? path.resolve(o.root) : path.resolve(path.dirname(SELF), '..');
  const result = evaluate(root);
  emit(root, result, o.json);
  process.exit(result.code);
}

main().catch((e) => { console.error(`corpus-contract: ${e && e.stack || e}`); process.exit(2); });
