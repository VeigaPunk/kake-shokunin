#!/usr/bin/env node
// Round-20 evidence replay: verify frozen inputs, then exercise both real CLIs.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createHash } from 'node:crypto';
import { execFileSync, spawnSync } from 'node:child_process';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '../..');
const frozen = path.join(here, 'frozen/citation-locality');
const sha = (bytes) => createHash('sha256').update(bytes).digest('hex');
let scratch;
try {
  const expected = JSON.parse(fs.readFileSync(path.join(frozen, 'expected.json'), 'utf8'));
  for (const [relative, digest] of Object.entries(expected.inputs)) {
    if (sha(fs.readFileSync(path.join(frozen, relative))) !== digest) {
      console.error(`CITATION_LOCALITY_PROOF: snapshot_tampered (${relative})`);
      process.exitCode = 2;
      break;
    }
  }
  if (!process.exitCode) {
    const baseline = execFileSync('git', ['show', `${expected.baselineRevision}:scripts/freshness-sweep.mjs`], { cwd: root });
    assert.equal(sha(baseline), expected.baselineScriptSha256, 'baseline program digest');
    scratch = fs.mkdtempSync(path.join(here, '.replay-'));
    const baselineFile = path.join(scratch, 'baseline.mjs');
    fs.writeFileSync(baselineFile, baseline);
    const candidateFile = path.join(root, 'scripts/freshness-sweep.mjs');
    let failures = 0;
    for (const [name, finding] of Object.entries(expected.cases)) {
      const fixture = path.join(frozen, name);
      for (const [stage, program] of [['baseline', baselineFile], ['candidate', candidateFile]]) {
        const result = spawnSync(process.execPath, [program, '--section=paths', '--json'], {
          cwd: root,
          encoding: 'utf8',
          env: { ...process.env, HOME: path.join(fixture, 'home'), KAKE_REPO_ROOT: path.join(fixture, 'repo'), KAKE_FRESHNESS_PINS: path.join(fixture, 'pins.json') },
        });
        try {
          if (result.error) throw result.error;
          assert.equal(result.status, stage === 'baseline' ? finding.beforeExit : finding.afterExit, result.stderr);
          const paths = JSON.parse(result.stdout).sections.paths;
          assert.deepEqual(paths.drift.map((d) => d.path), stage === 'baseline' ? [] : finding.afterDrift);
          if (stage === 'candidate') {
            assert.deepEqual(Object.fromEntries(paths.drift.map((d) => [d.path, d.unannotatedCites])), finding.afterUnannotatedCites);
            if (finding.present) assert(paths.resolve.some((d) => d.path === '~/publish/source.md'));
            if (name === 'all-annotated') assert(paths.declaredAbsent.some((d) => d.path === '~/publish/source.md'));
            if (name === 'mixed' || name === 'alias') assert.deepEqual(paths.setDelta.newMissing, []);
          }
          console.log(`PROOF ${stage} ${name}: exit ${result.status}, findings match`);
        } catch (error) {
          failures++;
          console.error(`PROOF ${stage} ${name}: FAIL — ${error.message}`);
        }
      }
    }
    console.log(`CITATION_LOCALITY_PROOF: ${failures ? 'FAIL' : 'PASS'} (cases=${Object.keys(expected.cases).length}, failures=${failures})`);
    process.exitCode = failures ? 1 : 0;
  }
} catch (error) {
  console.error(`CITATION_LOCALITY_PROOF: could_not_evaluate — ${error.message}`);
  process.exitCode = 2;
} finally {
  if (scratch) fs.rmSync(scratch, { recursive: true, force: true });
}
