#!/usr/bin/env node
// probe-delta — violated[]-delta + probe-coverage detector over probe-history.jsonl.
//
// Why: the 6h webzites-probe.timer writes silent history rows; nothing turned
// violated[] movement into an operator-visible signal (corpus/README.md r9
// known gap: "alerting on violated[] deltas … is undecided"). This is the
// runnable detection half; alert *delivery* (notify/systemd) stays with the
// webzites owner.
//
// Rules (source of truth: writer code read r10 — see
// corpus/knowledge/probe-delta-alerting.md):
//   - A row is a FULL sweep iff row.total === running max of total. Spot
//     probes (`probe <id>`) write total:1 rows and MUST NOT be diffed against
//     full sweeps — naive consecutive diffing yields ~42 events, most phantom.
//   - ENTER/EXIT = membership delta of violated[] between consecutive FULL
//     sweeps; timestamps are the two probe `at` values (enter visible at the
//     later row).
//   - UNIVERSE = total grew between consecutive full sweeps (registration):
//     newly violated/error members are listed; full membership delta is NOT
//     observable from history rows (only violated[]+errors[] are recorded).
//   - Coverage hole = gap between consecutive full sweeps > --hole-hours
//     (default 12 = 2x the 6h timer period).
//
// Usage: node scripts/probe-delta.mjs [--history PATH] [--since ISO]
//        [--hole-hours H] [--json]
// Exit 0 = parsed fine (this is a report, not a gate); 2 = unreadable input.

'use strict';
import fs from 'node:fs';
import path from 'node:path';

const DEFAULT_HISTORY = path.join(
  process.env.HOME || '', 'Projects/webzites/state/probe-history.jsonl'
);

function parseArgs(argv) {
  const out = { history: DEFAULT_HISTORY, since: null, holeHours: 12, json: false };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--history') out.history = argv[++i];
    else if (a === '--since') out.since = argv[++i];
    else if (a === '--hole-hours') out.holeHours = Number(argv[++i]);
    else if (a === '--json') out.json = true;
    else { console.error(`unknown flag: ${a}`); process.exit(64); }
  }
  if (!Number.isFinite(out.holeHours) || out.holeHours <= 0) {
    console.error('probe-delta: --hole-hours must be a positive number');
    process.exit(64);
  }
  if (out.since !== null && !Number.isFinite(Date.parse(out.since))) {
    console.error('probe-delta: --since must be an ISO date');
    process.exit(64);
  }
  return out;
}

function parseHistory(file) {
  const raw = fs.readFileSync(file, 'utf8');
  const rows = [];
  let bad = 0;
  for (const line of raw.split('\n')) {
    const t = line.trim();
    if (!t) continue;
    try {
      const r = JSON.parse(t);
      if (typeof r.at !== 'string' || !Array.isArray(r.violated) ||
          typeof r.total !== 'number') throw new Error('shape');
      rows.push(r);
    } catch { bad++; }
  }
  return { rows, bad };
}

function main() {
  const opt = parseArgs(process.argv.slice(2));
  let parsed;
  try { parsed = parseHistory(opt.history); }
  catch (e) { console.error(`probe-delta: cannot read ${opt.history}: ${e.message}`); process.exit(2); }
  const { rows, bad } = parsed;
  if (rows.length === 0) { console.error('probe-delta: zero usable rows'); process.exit(2); }

  // Classify full sweeps vs spot probes against the running universe.
  // A degenerate universe of 1 (a file that starts with spot rows) is not
  // a fleet — full sweeps require total > 1. Rows with 1 < total < universe
  // are partial sweeps: suspicious (shrunk fleet or masked spot), reported.
  let universe = 0;
  const full = [];
  let spots = 0;
  let partials = 0;
  for (const r of rows) {
    if (r.total > universe) universe = r.total;
    if (r.total > 1 && r.total === universe) full.push(r);
    else if (r.total > 1) partials++;
    else spots++;
  }

  // Diff consecutive full sweeps.
  const events = [];
  const gaps = [];
  for (let i = 1; i < full.length; i++) {
    const p = full[i - 1], c = full[i];
    gaps.push({ from: new Date(p.at), to: new Date(c.at) });
    // full[0] (the file's first full sweep) is baseline-only: never a
    // transition source — on this history its 33s bracket against full[1]
    // would emit only bootstrap phantoms (r10 reviewer rule).
    if (i === 1) continue;
    if (c.total > p.total) {
      events.push({
        type: 'UNIVERSE', site: `total ${p.total}->${c.total}`,
        detail: `new in violated[]+errors[]: ${
          c.violated.filter((x) => !p.violated.includes(x))
            .concat(c.errors.filter((x) => !p.errors.includes(x)))
            .join(',') || 'none visible'}`,
        at: c.at,
      });
    }
    for (const id of c.violated) if (!p.violated.includes(id))
      events.push({ type: 'ENTER', site: id, at: c.at, since: p.at });
    for (const id of p.violated) if (!c.violated.includes(id))
      events.push({ type: 'EXIT', site: id, at: c.at, since: p.at });
  }

  const sinceMs = opt.since ? Date.parse(opt.since) : null;
  const shown = Number.isFinite(sinceMs)
    ? events.filter((e) => Date.parse(e.at) >= sinceMs)
    : events;

  const gapMs = gaps.map((g) => g.to - g.from);
  const sorted = [...gapMs].sort((a, b) => a - b);
  const median = sorted.length ? sorted[Math.floor(sorted.length / 2)] : 0;
  const max = sorted.length ? sorted[sorted.length - 1] : 0;
  const holes = gaps
    .filter((g) => (g.to - g.from) / 3600000 > opt.holeHours)
    .map((g) => ({ from: g.from.toISOString(), to: g.to.toISOString(),
                   hours: +((g.to - g.from) / 3600000).toFixed(1) }));

  if (opt.json) {
    console.log(JSON.stringify({
      history: opt.history, rows: rows.length, malformed: bad,
      fullSweeps: full.length, spotProbesSkipped: spots, partialSweeps: partials, universe,
      events: shown, coverage: { medianGapH: +(median / 3600000).toFixed(2),
                                 maxGapH: +(max / 3600000).toFixed(2), holes },
    }, null, 2));
    return;
  }

  console.log(`probe-delta — ${opt.history}`);
  console.log(`rows ${rows.length} (malformed ${bad}) | full sweeps ${full.length} | spot probes skipped ${spots} | partial ${partials} | universe ${universe}${partials ? ' — PARTIAL SWEEPS PRESENT: verify fleet size before trusting events' : ''}`);
  console.log(`events (${shown.length}${sinceMs ? ` since ${opt.since}` : ''}):`);
  for (const e of shown) {
    const dur = e.since
      ? ` (prev sweep ${e.since})` : '';
    console.log(`  ${e.at}  ${e.type.padEnd(8)} ${e.site}${dur}${e.detail ? ` — ${e.detail}` : ''}`);
  }
  console.log(`coverage: median gap ${(median / 3600000).toFixed(2)}h, max ${(max / 3600000).toFixed(2)}h, holes >${opt.holeHours}h: ${holes.length}`);
  for (const h of holes) console.log(`  HOLE ${h.from} -> ${h.to} (${h.hours}h)`);
}

main();
