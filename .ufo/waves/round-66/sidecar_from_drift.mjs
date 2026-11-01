#!/usr/bin/env node
// round-66 §paths re-pin — generate line-bound sidecar errata from a sweep drift dump.
//
// Contract: `.ufo/waves/round-66/contract.md` §C2 part 2. The freshness sidecar
// (`corpus/knowledge/freshness-sidecar.json`, schema kake-paths-sidecar-v1) is the
// QUALITY-r20-sanctioned way to annotate a cited path without editing corpus bytes:
// one entry per (file, line, token), bound to the exact line by its sha256, dated,
// with the note carrying the absence vocabulary and the phrase
// "historical record, not an executable instruction".
//
// This tool reads a `freshness-sweep.mjs --offline --json` output file, takes
// `sections.paths.drift[]` (path + unannotatedCites), and APPENDS one entry per
// unannotated cite to the sidecar. Existing entries are never edited; an existing
// (file, line, token) key is left untouched (idempotent re-runs); a key that exists
// with a DIFFERENT line sha aborts without writing (the line moved — re-run the sweep
// and re-generate instead of force-annotating a stale line).
//
// Usage: node sidecar_from_drift.mjs --json <sweep.json> --root <repoRoot> [--dry]
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
  console.error('usage: sidecar_from_drift.mjs --json <sweep.json> --root <repoRoot> [--dry]');
  process.exit(64);
}
const DATE = '2026-10-31';
const PHRASE = 'historical record, not an executable instruction';

const drift = JSON.parse(fs.readFileSync(jsonFile, 'utf8')).sections.paths.drift;
const sidecarPath = path.join(root, 'corpus', 'knowledge', 'freshness-sidecar.json');
const sidecar = JSON.parse(fs.readFileSync(sidecarPath, 'utf8'));
if (sidecar.schema !== 'kake-paths-sidecar-v1' || !Array.isArray(sidecar.entries)) {
  console.error('sidecar schema mismatch');
  process.exit(2);
}
const lineSha = (s) => createHash('sha256').update(s, 'utf8').digest('hex');
const existing = new Map(sidecar.entries.map((e) => [`${e.file}:${e.line}:${e.token}`, e]));

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
    const key = `${file}:${line}:${d.path}`;
    const prev = existing.get(key);
    if (prev) {
      const sha = lineSha(fs.readFileSync(path.join(root, file), 'utf8').split('\n')[line - 1]);
      if (prev.lineSha256 !== sha) {
        console.error('line moved under an existing entry: %s (sidecar %s, tree %s)', key, prev.lineSha256.slice(0, 12), sha.slice(0, 12));
        process.exit(2);
      }
      skipped += 1;
      continue;
    }
    const lineText = fs.readFileSync(path.join(root, file), 'utf8').split('\n')[line - 1];
    if (lineText === undefined) {
      console.error('line out of range: %s', key);
      process.exit(2);
    }
    const note = `${DATE}: ${d.path} absent on this host — an old-host home path; the `
      + `Windows host migration removed every former home tree, so this target does not `
      + `exist on the current machine. Citation ${file}:${line} is a ${PHRASE}.`;
    newEntries.push({
      file,
      line,
      token: d.path,
      lineSha256: lineSha(lineText),
      kind: 'absent',
      date: DATE,
      note,
    });
    existing.set(key, newEntries[newEntries.length - 1]);
    perToken.set(d.path, (perToken.get(d.path) || 0) + 1);
    added += 1;
  }
}
if (!dry) {
  sidecar.entries.push(...newEntries);
  fs.writeFileSync(sidecarPath, JSON.stringify(sidecar, null, 2) + '\n');
}
console.log('sidecar entries: added=%d skipped-existing=%d drift-tokens=%d dry=%s',
  added, skipped, drift.length, dry);
for (const [t, n] of [...perToken.entries()].sort()) console.log('  %d  %s', n, t);
