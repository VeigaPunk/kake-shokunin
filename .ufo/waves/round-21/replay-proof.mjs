#!/usr/bin/env node
// replay-proof.mjs — kake round-21 frozen-snapshot replay (kake-shokunin).
//
// Wraps scripts/corpus-contract.mjs against the frozen "before" snapshot
// (.ufo/waves/round-21/frozen/before), pinned by per-file SHA-256 digests
// in frozen/before/expected.json (baseline 5009ecaa1cce10b895617a585ddd3f7c7c923a84).
//
// Contract under test (lane-authored gate, not this file):
//   node scripts/corpus-contract.mjs --root <frozen> --json
//     → exit 1 on the untouched baseline corpus, emitting stable
//       missing_metadata and missing_gate IDs.
//
// Proof order:
//   1. verify EVERY input digest before any execution — any mismatch is
//      snapshot_tampered (exit 2), and the gate is never run;
//   2. run the gate TWICE on the unchanged snapshot — exit must equal
//      expected_exit and both runs must produce byte-identical stdout
//      (stable ID set, no ordering drift);
//   3. extract missing_metadata:* and missing_gate:* IDs from raw stdout
//      and check counts: ≥1 metadata ID in each of (knowledge −
//      metadata_complete) files, and exactly (lessons − gates_complete)
//      gate IDs — one per un-gated lane lesson;
//   4. re-verify every input digest after execution — the snapshot must
//      be byte-identical (the gate is read-only; this proof must not
//      mutate it either).
//
// Semantics: missing_metadata/missing_gate report absent provenance
// metadata and absent retrospective gate sections — historical record
// gaps. They are NOT live-freshness or domain-verification findings;
// this proof performs no domain reads and claims no live state.
//
// Usage: node .ufo/waves/round-21/replay-proof.mjs
// Exit: 0 PASS · 1 FAIL (contract assertion) ·
//       2 could_not_evaluate / snapshot_tampered.
// Read-only: fs reads + argv-form spawnSync only — no shell, no pipes,
// no writes to the tree or snapshot.

import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createHash } from 'node:crypto';
import { spawnSync } from 'node:child_process';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '../../..');
const frozen = path.join(here, 'frozen/before');
const manifestFile = path.join(frozen, 'expected.json');
const gate = path.join(root, 'scripts/corpus-contract.mjs');
const sha = (bytes) => createHash('sha256').update(bytes).digest('hex');
const ID_RE = /\b(?:missing_metadata|missing_gate)[^\s"',\]]*/g;
const PATH_IN_ID_RE = /corpus\/(?:knowledge|lessons)\/[^\s"',:\]]+\.md/g;

function verifyInputs(inputs, label) {
  const bad = [];
  for (const [rel, digest] of Object.entries(inputs)) {
    const file = path.join(frozen, rel);
    let actual;
    try {
      actual = sha(fs.readFileSync(file));
    } catch (error) {
      bad.push(`${rel}: unreadable (${error.message})`);
      continue;
    }
    if (actual !== digest) bad.push(`${rel}: sha256 ${actual} != ${digest}`);
  }
  if (bad.length > 0) {
    for (const line of bad) console.error(`REPLAY_PROOF: snapshot_tampered (${label}) ${line}`);
    process.exit(2);
  }
  return Object.keys(inputs).length;
}

function extractIds(stdout) {
  const ids = stdout.match(ID_RE) ?? [];
  const metadata = ids.filter((id) => id.startsWith('missing_metadata'));
  const gates = ids.filter((id) => id.startsWith('missing_gate'));
  const metadataFiles = new Set(metadata.flatMap((id) => id.match(PATH_IN_ID_RE) ?? []));
  const gateFiles = new Set(gates.flatMap((id) => id.match(PATH_IN_ID_RE) ?? []));
  return { metadata, gates, metadataFiles, gateFiles };
}

let failures = 0;
const fail = (message) => {
  failures += 1;
  console.error(`REPLAY_PROOF: FAIL — ${message}`);
};

try {
  const expected = JSON.parse(fs.readFileSync(manifestFile, 'utf8'));
  const n = verifyInputs(expected.inputs, 'before-run');
  assert.equal(
    Object.keys(expected.inputs).length,
    expected.knowledge + expected.lessons,
    'manifest inputs must cover knowledge + lessons',
  );
  console.log(`PROOF inputs digest ok (files=${n}, revision=${expected.revision})`);

  if (!fs.existsSync(gate)) {
    console.error(`REPLAY_PROOF: could_not_evaluate — gate not found: ${gate}`);
    process.exit(2);
  }

  // Two runs on the unchanged snapshot: same exit, byte-identical stdout.
  const runs = [1, 2].map((i) => {
    const result = spawnSync(process.execPath, [gate, '--root', frozen, '--json'], {
      cwd: root,
      encoding: 'utf8',
    });
    if (result.error) {
      console.error(`REPLAY_PROOF: could_not_evaluate — gate spawn failed: ${result.error.message}`);
      process.exit(2);
    }
    return { run: i, status: result.status, stdout: result.stdout, stderr: result.stderr };
  });
  try {
    assert.equal(runs[0].status, expected.expected_exit,
      `run1 exit ${runs[0].status} != expected ${expected.expected_exit}`);
    assert.equal(runs[1].status, expected.expected_exit,
      `run2 exit ${runs[1].status} != expected ${expected.expected_exit}`);
    assert.equal(runs[1].stdout, runs[0].stdout, 'run2 stdout differs from run1 (unstable IDs/ordering)');
    console.log(`PROOF gate stable across 2 runs (exit=${runs[0].status})`);
  } catch (error) {
    fail(error.message);
  }

  try {
    JSON.parse(runs[0].stdout);
  } catch (error) {
    fail(`gate --json output unparseable: ${error.message}`);
  }

  const { metadata, gates, metadataFiles, gateFiles } = extractIds(runs[0].stdout);
  const expectedMissingMetadataFiles = expected.knowledge - expected.metadata_complete;
  const expectedMissingGateFiles = expected.lessons - expected.gates_complete;
  try {
    assert(metadata.length > 0, 'no missing_metadata IDs emitted');
    assert(gates.length > 0, 'no missing_gate IDs emitted');
    // IDs must carry corpus/... paths so missing members are named.
    assert.equal(metadataFiles.size, expectedMissingMetadataFiles,
      `missing_metadata covers ${metadataFiles.size} files, expected ${expectedMissingMetadataFiles}`);
    assert.equal(gateFiles.size, expectedMissingGateFiles,
      `missing_gate covers ${gateFiles.size} files, expected ${expectedMissingGateFiles}`);
    // Gate IDs are one per un-gated lesson.
    assert.equal(gates.length, expectedMissingGateFiles,
      `missing_gate ids ${gates.length}, expected ${expectedMissingGateFiles}`);
    // No ID may point outside the frozen corpus populations.
    for (const file of [...metadataFiles]) {
      assert(file.startsWith('corpus/knowledge/'), `missing_metadata path outside corpus/knowledge: ${file}`);
    }
    for (const file of [...gateFiles]) {
      assert(/^corpus\/lessons\/round-\d+(?:-recensus)?\.md$/.test(file),
        `missing_gate path outside lane-lesson population: ${file}`);
    }
    console.log(`PROOF ids: ${metadata.length} missing_metadata (${metadataFiles.size} files), ${gates.length} missing_gate (${gateFiles.size} files)`);
  } catch (error) {
    fail(error.message);
  }

  // Snapshot must be byte-identical after both runs — gate and proof are read-only.
  verifyInputs(expected.inputs, 'after-run');
  console.log('PROOF snapshot unchanged after execution');

  console.log(`REPLAY_PROOF: ${failures ? 'FAIL' : 'PASS'} (files=${n}, runs=2, failures=${failures})`);
  process.exitCode = failures ? 1 : 0;
} catch (error) {
  console.error(`REPLAY_PROOF: could_not_evaluate — ${error.message}`);
  process.exitCode = 2;
}
