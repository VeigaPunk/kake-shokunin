#!/usr/bin/env node
// round-78 §paths re-pin — line-bound sidecar errata from a sweep drift dump.
//
// Adapted from `.ufo/waves/round-66/sidecar_from_drift.mjs` (round-66 contract
// §C2 part 2) for round 78. Two changes: the date is a parameter (`--date`),
// and the per-token cause is recorded instead of the round-66 hardcoded
// "Windows host migration" sentence, which is false for `~/projects`: the lane's
// recorded absence event for that token is W6 (corpus/lessons/round-17.md:9-21;
// SKILL.md:309-311), the 2026-09-29 03:13–03:14Z lowercase-tree consolidation.
//
// The freshness sidecar (`corpus/knowledge/freshness-sidecar.json`, schema
// kake-paths-sidecar-v1) is the QUALITY-r20-sanctioned way to annotate a cited
// path without editing corpus bytes: one entry per (file, line, token), bound to
// the exact line by its sha256, dated, with a note carrying the absence
// vocabulary and the phrase "historical record, not an executable instruction".
//
// Reads a `freshness-sweep.mjs --offline --json` output file, takes
// `sections.paths.drift[]` (path + unannotatedCites), and APPENDS one
// `kind:"absent"` entry per unannotated cite. Existing entries are never
// edited; an existing (file, line, token) key is left untouched (idempotent
// re-runs); a key that exists with a DIFFERENT line sha aborts without writing
// (the line moved — re-run the sweep and re-generate instead of force-annotating
// a stale line).
//
// Usage: node sidecar_from_drift.mjs --json <sweep.json> --root <repoRoot>
//        [--date YYYY-MM-DD] [--dry]
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';

const args = process.argv.slice(2);
const opt = (name) => {
  const i = args.indexOf(name);
  return i >= 0 ? args[i + 1] : undefined;
};
const jsonFile = opt('--json');
const root = opt('--root');
const dry = args.includes('--dry');
if (!jsonFile || !root) {
  console.error('usage: sidecar_from_drift.mjs --json <sweep.json> --root <repoRoot> [--date YYYY-MM-DD] [--dry]');
  process.exit(64);
}
const DATE = opt('--date') || '2026-11-03';
if (!/^\d{4}-\d{2}-\d{2}$/.test(DATE) || new Date(DATE).toISOString().slice(0, 10) !== DATE) {
  console.error('bad --date: %s', DATE);
  process.exit(64);
}
const PHRASE = 'historical record, not an executable instruction';
// Per-token recorded absence event. Anything not listed falls back to the
// measured statement only — never invent a cause.
const CAUSES = {
  '~/projects': 'the lowercase tree was consolidated into the capital root in W6, '
    + 'the 2026-09-29 03:13\u201303:14Z lowercase-tree consolidation '
    + '(corpus/lessons/round-17.md; SKILL.md:310)',
};

const drift = JSON.parse(fs.readFileSync(jsonFile, 'utf8')).sections.paths.drift;
const sidecarPath = path.join(root, 'corpus', 'knowledge', 'freshness-sidecar.json');
const sidecar = JSON.parse(fs.readFileSync(sidecarPath, 'utf8'));
if (sidecar.schema !== 'kake-paths-sidecar-v1' || !Array.isArray(sidecar.entries)) {
  console.error('sidecar schema mismatch');
  process.exit(2);
}
const lineSha = (s) => createHash('sha256').update(s, 'utf8').digest('hex');

const cache = new Map();
const linesOf = (file) => {
  if (!cache.has(file)) cache.set(file, fs.readFileSync(path.join(root, file), 'utf8').split('\n'));
  return cache.get(file);
};

const existing = new Map(sidecar.entries.map((e) => [`${e.file}:${e.line}:${e.token}`, e]));
const before = sidecar.entries.length;

let added = 0;
let skipped = 0;
const perToken = new Map();
const newEntries = [];
for (const d of drift) {
  for (const cite of d.unannotatedCites) {
    const cut = cite.lastIndexOf(':');
    const file = cite.slice(0, cut);
    const line = Number(cite.slice(cut + 1));
    if (!Number.isSafeInteger(line) || line < 1 || !/^(SKILL\.md|corpus\/.+\.md)$/.test(file)) {
      console.error('unusable cite: %s', cite);
      process.exit(2);
    }
    const lines = linesOf(file);
    const lineText = lines[line - 1];
    if (lineText === undefined) {
      console.error('line out of range: %s', cite);
      process.exit(2);
    }
    const sha = lineSha(lineText);
    const key = `${file}:${line}:${d.path}`;
    const prev = existing.get(key);
    if (prev) {
      if (prev.lineSha256 !== sha) {
        console.error('line moved under an existing entry: %s (sidecar %s, tree %s)',
          key, prev.lineSha256.slice(0, 12), sha.slice(0, 12));
        process.exit(2);
      }
      skipped += 1;
      continue;
    }
    const cause = CAUSES[d.path] || 'the target does not exist at the measured revision on this host';
    const note = `${DATE}: ${d.path} absent on this host (test -e exit 1) \u2014 ${cause}. `
      + `Citation ${file}:${line} is a ${PHRASE}.`;
    const entry = { file, line, token: d.path, lineSha256: sha, kind: 'absent', date: DATE, note };
    newEntries.push(entry);
    existing.set(key, entry);
    perToken.set(d.path, (perToken.get(d.path) || 0) + 1);
    added += 1;
  }
}

newEntries.sort((a, b) => (a.file < b.file ? -1 : a.file > b.file ? 1 : a.line - b.line));
if (!dry && newEntries.length) {
  sidecar.entries.push(...newEntries);
  fs.writeFileSync(sidecarPath, JSON.stringify(sidecar, null, 2) + '\n');
}
console.log('sidecar entries: before=%d added=%d skipped-existing=%d after=%d dry=%s',
  before, added, skipped, before + (dry ? 0 : newEntries.length), dry);
for (const [t, n] of [...perToken.entries()].sort()) console.log('  %d  %s', n, t);
for (const e of newEntries) console.log('  + %s:%d  %s', e.file, e.line, e.token);
