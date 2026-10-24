#!/usr/bin/env node
// measure.mjs — kake round-21 frozen population measurer (kake-shokunin).
//
// Independently counts, without trusting lane scribe claims:
//   C1  provenance trio on all 21 corpus/knowledge/*.md entries —
//       each of `source:`, `verified-at:`, `recheck:` must appear as an
//       exact lowercase `field:` line with a non-empty value within the
//       FIRST 8 LINES — case-sensitive, prose `Source:` does not count;
//   C2  an exact `## Gate` heading line on every lane-authored lesson —
//       corpus/lessons/round-<N>.md and round-<N>-recensus.md only
//       (exact population regex /^round-\d+(?:-recensus)?\.md$/;
//       verifier-spotcheck / aggregator / operator files are excluded;
//       gate regex is the exact line /^## Gate$/m — suffixed headings
//       like `## Gate — ...` do not count).
//   Legacy denominator stays 15; a fresh tree may enumerate a 16th
//   lesson (round-21.md, authored this round) — extras are reported
//   and evaluated, but a complete extra never fails the run.
//
// Usage:
//   node .ufo/waves/round-21/measure.mjs                    # working tree
//   node .ufo/waves/round-21/measure.mjs --revision <commit-ish>
//   node .ufo/waves/round-21/measure.mjs --revision 5009ecaa1cce10b895617a585ddd3f7c7c923a84
//   node .ufo/waves/round-21/measure.mjs --root <repo> [--revision <commit-ish>]
//   node .ufo/waves/round-21/measure.mjs --help
//
// Output: one JSON document on stdout — mode, revision, per-file rows
// naming each missing field/gate, expected-vs-found population counts,
// and read errors. Nothing is written to the tree.
// Exit: 0 complete · 1 any missing field/gate or absent expected file ·
//       2 read errors (unreadable file, bad revision, missing dir) ·
//       64 usage error.
// Read-only by construction: working-tree mode uses fs.readFileSync/
// readdirSync only; revision mode uses argv-form `git ls-tree` /
// `git rev-parse` / `git show` subprocesses — no shell, no pipes, no writes.
// Expected population below mirrors .ufo/waves/round-21/initial.json at
// the shared baseline 5009ecaa1cce10b895617a585ddd3f7c7c923a84.

import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const DEFAULT_ROOT = path.resolve(here, '../../..');
const BASELINE = '5009ecaa1cce10b895617a585ddd3f7c7c923a84';

const KNOWLEDGE_DIR = 'corpus/knowledge';
const LESSONS_DIR = 'corpus/lessons';
const FIRST8 = 8;

const EXPECTED_KNOWLEDGE = [
  'corpus/knowledge/crawl-scope-per-host.md',
  'corpus/knowledge/drift-detection.md',
  'corpus/knowledge/fire-journal-codes.md',
  'corpus/knowledge/fleet-registry.md',
  'corpus/knowledge/free-read-verbs.md',
  'corpus/knowledge/freshness-sweep.md',
  'corpus/knowledge/ghp-custom-domain.md',
  'corpus/knowledge/ghp-etag-anatomy.md',
  'corpus/knowledge/ghp-served-set.md',
  'corpus/knowledge/ghp-subpath-spotcheck.md',
  'corpus/knowledge/keeper-timer-inert.md',
  'corpus/knowledge/kimi-subpath-audit.md',
  'corpus/knowledge/mirror-pitfalls.md',
  'corpus/knowledge/ops-automation.md',
  'corpus/knowledge/origin-repos.md',
  'corpus/knowledge/probe-delta-alerting.md',
  'corpus/knowledge/publish-channels.md',
  'corpus/knowledge/publish-queue.md',
  'corpus/knowledge/sitemap-orphan-audit.md',
  'corpus/knowledge/speedrun-pipeline.md',
  'corpus/knowledge/vault-properties.md',
];
const EXPECTED_LESSONS = [
  'corpus/lessons/round-1.md',
  'corpus/lessons/round-10.md',
  'corpus/lessons/round-12.md',
  'corpus/lessons/round-16.md',
  'corpus/lessons/round-17.md',
  'corpus/lessons/round-18.md',
  'corpus/lessons/round-19-recensus.md',
  'corpus/lessons/round-20.md',
  'corpus/lessons/round-3.md',
  'corpus/lessons/round-4.md',
  'corpus/lessons/round-5.md',
  'corpus/lessons/round-6.md',
  'corpus/lessons/round-7.md',
  'corpus/lessons/round-8.md',
  'corpus/lessons/round-9.md',
];

// Exact per-field patterns: lowercase `field:` at column 0 with a non-empty
// value ([ \t]* then non-space), matched against each of the first 8 lines.
// Case-sensitive so prose `Source:` in legacy entries does not count —
// only the declared metadata trio does.
const FIELDS = [
  ['source', /^source:[ \t]*\S/],
  ['verified-at', /^verified-at:[ \t]*\S/],
  ['recheck', /^recheck:[ \t]*\S/],
];
const FIELD_NAMES = FIELDS.map(([name]) => name);
const LESSON_NAME_RE = /^round-\d+(?:-recensus)?\.md$/;
const GATE_RE = /^## Gate$/m;

const USAGE = `usage: node .ufo/waves/round-21/measure.mjs [--root <repo>] [--revision <commit-ish>] [--help]
  --root <repo>       repository root (default: two levels above this script)
  --revision <ish>    measure a git commit instead of the working tree;
                      shared baseline is ${BASELINE}
  --help              print this text`;

function usageError(message) {
  console.error(`measure.mjs: ${message}\n${USAGE}`);
  process.exit(64);
}

function parseArgs(argv) {
  const opts = { root: DEFAULT_ROOT, revision: null };
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === '--help' || arg === '-h') {
      console.log(USAGE);
      process.exit(0);
    } else if (arg === '--root') {
      if (i + 1 >= argv.length) usageError('--root requires a value');
      opts.root = argv[++i];
    } else if (arg.startsWith('--root=')) {
      opts.root = arg.slice('--root='.length);
    } else if (arg === '--revision') {
      if (i + 1 >= argv.length) usageError('--revision requires a value');
      opts.revision = argv[++i];
    } else if (arg.startsWith('--revision=')) {
      opts.revision = arg.slice('--revision='.length);
    } else {
      usageError(`unknown argument: ${arg}`);
    }
  }
  if (opts.revision !== null && opts.revision.length === 0) {
    usageError('--revision requires a non-empty commit-ish');
  }
  opts.root = path.resolve(opts.root);
  return opts;
}

function git(root, args) {
  // argv-form execFile: no shell, no pipes, read-only subcommands only.
  return execFileSync('git', ['-C', root, ...args], {
    encoding: 'utf8',
    maxBuffer: 64 * 1024 * 1024,
  });
}

function makeSource(root, revision) {
  if (revision === null) {
    return {
      mode: 'working-tree',
      revision: null,
      list() {
        const out = [];
        for (const [dir, nameRe] of [
          [KNOWLEDGE_DIR, /\.md$/],
          [LESSONS_DIR, LESSON_NAME_RE],
        ]) {
          let names;
          try {
            names = fs.readdirSync(path.join(root, dir));
          } catch (error) {
            throw new Error(`cannot list ${dir}: ${error.message}`);
          }
          for (const name of names) {
            if (nameRe.test(name)) out.push(`${dir}/${name}`);
          }
        }
        return out.sort();
      },
      read(rel) {
        return fs.readFileSync(path.join(root, rel), 'utf8');
      },
    };
  }
  let resolved;
  try {
    resolved = git(root, ['rev-parse', '--verify', `${revision}^{commit}`]).trim();
  } catch (error) {
    throw new Error(`cannot resolve revision '${revision}': ${error.message}`);
  }
  return {
    mode: 'revision',
    revision: resolved,
    list() {
      const out = git(root, [
        'ls-tree', '-r', '--name-only', resolved, '--', KNOWLEDGE_DIR, LESSONS_DIR,
      ]).split('\n').filter((line) => line.length > 0);
      return out.filter((rel) => {
        const base = rel.slice(rel.lastIndexOf('/') + 1);
        if (rel.startsWith(`${KNOWLEDGE_DIR}/`)) return base.endsWith('.md');
        if (rel.startsWith(`${LESSONS_DIR}/`)) return LESSON_NAME_RE.test(base);
        return false;
      }).sort();
    },
    read(rel) {
      return git(root, ['show', `${resolved}:${rel}`]);
    },
  };
}

function evalKnowledge(rel, text) {
  const head = text.split(/\r?\n/, FIRST8);
  const fields = {};
  const missing = [];
  for (const [name, re] of FIELDS) {
    const present = head.some((line) => re.test(line));
    fields[name] = present;
    if (!present) missing.push(name);
  }
  return { file: rel, fields, missing };
}

function evalLesson(rel, text) {
  const gate = GATE_RE.test(text);
  return { file: rel, gate, missing: gate ? [] : ['## Gate'] };
}

function measure(opts) {
  const errors = [];
  let source;
  try {
    source = makeSource(opts.root, opts.revision);
  } catch (error) {
    errors.push({ file: null, message: error.message });
    return { source: { mode: opts.revision === null ? 'working-tree' : 'revision', revision: opts.revision }, errors };
  }
  let listed = [];
  try {
    listed = source.list();
  } catch (error) {
    errors.push({ file: null, message: error.message });
    return { source: { mode: source.mode, revision: source.revision }, errors };
  }
  const listedSet = new Set(listed);
  const knowledgeFiles = listed.filter((rel) => rel.startsWith(`${KNOWLEDGE_DIR}/`));
  const lessonFiles = listed.filter((rel) => rel.startsWith(`${LESSONS_DIR}/`));
  // Population contract: the legacy lane-authored lesson denominator stays
  // fixed at 15. A fresh working tree may legitimately enumerate a 16th
  // (round-21.md, authored this round); extras are reported AND evaluated
  // like any member, so their own missing gates still fail — but a
  // complete extra never does.

  const population = {
    knowledge: {
      expected: EXPECTED_KNOWLEDGE.length,
      found: knowledgeFiles.length,
      absent: EXPECTED_KNOWLEDGE.filter((rel) => !listedSet.has(rel)),
      extra: knowledgeFiles.filter((rel) => !EXPECTED_KNOWLEDGE.includes(rel)),
    },
    lessons: {
      expected: EXPECTED_LESSONS.length,
      found: lessonFiles.length,
      absent: EXPECTED_LESSONS.filter((rel) => !listedSet.has(rel)),
      extra: lessonFiles.filter((rel) => !EXPECTED_LESSONS.includes(rel)),
    },
  };

  const evalSet = (files, evaluator) => files.map((rel) => {
    let text;
    try {
      text = source.read(rel);
    } catch (error) {
      errors.push({ file: rel, message: error.message });
      return { file: rel, readError: true, missing: [] };
    }
    return evaluator(rel, text);
  });

  const knowledgeRows = evalSet(knowledgeFiles, evalKnowledge);
  const lessonRows = evalSet(lessonFiles, evalLesson);
  // Absent expected members surface as rows so filenames stay visible.
  for (const rel of population.knowledge.absent) {
    knowledgeRows.push({ file: rel, absent: true, missing: [...FIELD_NAMES, 'file-absent'] });
  }
  for (const rel of population.lessons.absent) {
    lessonRows.push({ file: rel, absent: true, missing: ['## Gate', 'file-absent'] });
  }
  knowledgeRows.sort((a, b) => a.file.localeCompare(b.file));
  lessonRows.sort((a, b) => a.file.localeCompare(b.file));

  const missing = [];
  for (const row of knowledgeRows) {
    for (const what of row.missing) missing.push(`${row.file}: ${what}`);
  }
  for (const row of lessonRows) {
    for (const what of row.missing) missing.push(`${row.file}: ${what}`);
  }
  const populationDeviation =
    population.knowledge.absent.length > 0 || population.knowledge.extra.length > 0 ||
    population.lessons.absent.length > 0 || population.lessons.extra.length > 0;

  return {
    source: { mode: source.mode, revision: source.revision },
    criteria: {
      knowledge: { fields: FIELD_NAMES, window: `first-${FIRST8}-lines`, fieldRegex: 'exact lowercase field name at column 0, [ \\t]* then non-empty value' },
      lessons: { populationRegex: String(LESSON_NAME_RE), gateRegex: String(GATE_RE) },
    },
    semantics: 'missing source:/verified-at:/recheck: flags absent provenance metadata (historical record); it is not evidence of absent live verification — this run performs no domain reads',
    population,
    populationDeviation,
    knowledge: {
      expected: EXPECTED_KNOWLEDGE.length,
      complete: knowledgeRows.filter((r) => !r.readError && !r.absent && r.missing.length === 0).length,
      files: knowledgeRows,
    },
    lessons: {
      expected: EXPECTED_LESSONS.length,
      complete: lessonRows.filter((r) => !r.readError && !r.absent && r.missing.length === 0).length,
      files: lessonRows,
    },
    missing,
    errors,
  };
}

function main() {
  const opts = parseArgs(process.argv.slice(2));
  const result = measure(opts);
  let exitCode;
  if (result.errors.length > 0) {
    exitCode = 2;
  } else if (result.missing.length > 0) {
    // Any missing field, gate, or absent expected file. Population extras
    // alone do not fail; their own missing entries do.
    exitCode = 1;
  } else {
    exitCode = 0;
  }
  result.exitCode = exitCode;
  console.log(JSON.stringify(result, null, 2));
  process.exit(exitCode);
}

main();
