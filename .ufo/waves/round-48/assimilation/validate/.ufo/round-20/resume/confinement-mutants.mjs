#!/usr/bin/env node
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync, execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const L = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');
const write = "  fs.writeFileSync('/dev/null', '');";

function markerScan(lines) {
  const allowed = new Set(), gapsAllowed = new Set(), marks = [], errors = [];
  let open = null;
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();
    const begin = /^\/\/ SELFTEST-WRITES-BEGIN(?: \(.+\))?$/.test(line);
    const end = line === '// SELFTEST-WRITES-END';
    if (begin) {
      if (open !== null) errors.push('nested');
      else { open = i; marks.push(`B${i + 1}`); }
    }
    if (open !== null) allowed.add(i);
    if (end) {
      if (open === null) errors.push('unbalanced');
      else { allowed.add(i); open = null; marks.push(`E${i + 1}`); }
    }
    if (open !== null) gapsAllowed.add(i + 1);
  }
  if (open !== null) errors.push('unterminated');
  return { allowed, gapsAllowed, marks, errors };
}
function functionSites(source) {
  const lines = source.split('\n'), regions = markerScan(lines), sites = [];
  for (let i = 0; i < lines.length; i++) {
    const declaration = /^(?:async\s+)?function\s+([A-Za-z_$][\w$]*)\s*\(/.exec(lines[i]);
    if (!declaration) continue;
    let depth = 0, quote = null, escaped = false, afterParams = false, bodyLine = -1;
    for (let line = i; line < lines.length && bodyLine < 0; line++) {
      const text = lines[line];
      const from = line === i ? declaration[0].lastIndexOf('(') + declaration.index : 0;
      for (let col = from; col < text.length; col++) {
        const ch = text[col];
        if (quote) {
          if (escaped) escaped = false;
          else if (ch === '\\') escaped = true;
          else if (ch === quote) quote = null;
          continue;
        }
        if (ch === "'" || ch === '"' || ch === '`') { quote = ch; continue; }
        if (ch === '(') depth++;
        else if (ch === ')' && --depth === 0) afterParams = true;
        else if (afterParams && ch === '{') { bodyLine = line; break; }
      }
    }
    const gap = bodyLine + 1;
    if (bodyLine >= 0 && !regions.errors.length && !regions.gapsAllowed.has(gap)) {
      sites.push({ name: declaration[1], bodyLine });
    }
  }
  return sites;
}

function runMutant(source, name) {
  const sites = functionSites(source), site = sites.find((candidate) => candidate.name === name);
  const lines = source.split('\n');
  lines.splice(site.bodyLine + 1, 0, write);
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'kake-confinement-'));
  try {
    const home = path.join(root, 'home'), selftest = path.join(root, 'selftest');
    fs.mkdirSync(home);
    fs.mkdirSync(selftest);
    const script = path.join(root, 'freshness-sweep.mjs');
    fs.writeFileSync(script, lines.join('\n'));
    const result = spawnSync(process.execPath, [script, '--selftest'], {
      env: { ...process.env, HOME: home, KAKE_SELFTEST_DIR: selftest, KAKE_REPO_ROOT: L },
      stdio: 'ignore', timeout: 60000,
    });
    if (result.error || result.status === null) throw new Error('mutant process failed to complete');
    return result.status === 0;
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
}

try {
  const oldSource = execFileSync('git', ['-C', L, 'show', 'cb807bc:scripts/freshness-sweep.mjs'], { encoding: 'utf8' });
  const newSource = fs.readFileSync(path.join(L, 'scripts/freshness-sweep.mjs'), 'utf8');
  const oldNames = functionSites(oldSource).map((site) => site.name);
  const newNames = new Set(functionSites(newSource).map((site) => site.name));
  const names = [...new Set(oldNames.filter((name) => newNames.has(name)))];
  if (!names.length) throw new Error('no shared out-of-region function sites');
  const counts = [];
  for (const [revision, source] of [['cb807bc', oldSource], ['working-tree', newSource]]) {
    let killed = 0, survived = 0;
    for (const name of names) {
      if (runMutant(source, name)) survived++;
      else killed++;
    }
    counts.push({ revision, killed, survived, total: names.length });
    console.log(`MUTANTS ${revision}: killed ${killed}/${names.length} survived ${survived}/${names.length}`);
  }
  const old = counts[0], current = counts[1];
  if (old.survived < 1 || current.survived !== 0) process.exitCode = 1;
} catch {
  console.error('MUTANTS replay: ERROR');
  process.exitCode = 1;
}
