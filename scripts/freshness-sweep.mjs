#!/usr/bin/env node
// freshness-sweep — kake-shokunin freshness-axis re-verification battery.
//
// One command re-executes every quantified standing claim the lane makes:
//   §paths    every cited FS path in SKILL.md + corpus/**/*.md vs the live FS
//   §history  probe-history.jsonl shape (pinned) + probe-delta event shape
//   §armed    PQ-12 charter-ghp beat pin · PQ-5 kimi dead slot · PQ-2 push
//             gate · ds4cc.com pre-push sitemap
//
// A standing claim is a PIN, not prose: pins live in
// corpus/knowledge/freshness-pins.json (loaded when present, else the
// DEFAULT_PINS constants below) so the numbers can be re-based in one diff
// instead of tracked by hand across SKILL.md.
//
// Exit contract: 0 = clean · 1 = drift · 2 = unreadable/invalid input ·
//                64 = usage error.
//
// READ-ONLY BY CONSTRUCTION: the only fs write APIs in this file live inside
// the SELFTEST-WRITES-BEGIN/END region (`--selftest` builds hermetic fixtures
// under /tmp/kake-r16/selftest). The normal path never writes, never mkdirs,
// and never touches ~/Projects. `--selftest` proves this by grepping its own
// source for write-API call sites outside that region.
//
// Usage:
//   node scripts/freshness-sweep.mjs [--json] [--offline]
//        [--section=paths|history|armed] [--repo DIR] [--selftest] [--help]
//
// Env overrides (all optional):
//   KAKE_REPO_ROOT       lane repo root (default: dirname(script)/..)
//   KAKE_FRESHNESS_PINS  pins JSON path
//   KAKE_PROBE_HISTORY   probe-history.jsonl path
//   KAKE_FLEET_CONFIG    fleet.config.json path
//   KAKE_R15_SNAPSHOT    r15 charter-ghp body snapshot (sha cross-check)
//   KAKE_FETCH_TIMEOUT   per-request timeout ms (default 15000)

'use strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import crypto from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const SELF = fileURLToPath(import.meta.url);

// ───────────────────────────────────────────────────────────────────────────
// Pins. Source of truth at runtime = corpus/knowledge/freshness-pins.json;
// these constants are the fallback when that file is absent (fresh clone /
// --repo fixture) and are byte-identical to the round-16 pin file.
// Every value here was observed live at round-16 open (2026-09-29T02:1xZ).
// ───────────────────────────────────────────────────────────────────────────
const DEFAULT_PINS = {
  schema: 'kake-freshness-pins-v1',
  updated: '2026-09-29',
  round: 16,
  pins: {
    // §history
    probeRowsFloor: 78,                               // 78 rows live (r15: 78)
    probeLastAtFloor: '2026-09-29T00:01:09.976Z',      // last row `at` >= this
    probeCadenceHours: 6,                              // webzites-probe.timer
    probeSlackMinutes: 20,                             // age ceiling = 6h20m
    probeFullSweeps: 67,                               // total>1 && total===universe
    probeSpotRows: 11,                                 // total===1
    fleetTotal: 18,
    fleetOk: 12,
    violated: ['plazir15', 'charter-ufo-fsd-kimi', 'charter-ghp', 'plazir27-kimi-pro', 'lucario'],
    errors: ['xsnapshot-app'],
    deltaPhantomMax: 0,                                // malformed + partialSweeps
    deltaEventsMax: 12,
    // §armed — PQ-12 charter-ghp
    charterGhpUrl: 'https://veigapunk.github.io/charter-ufo-fsd/',
    charterGhpPin: '2026-09-26 scribe beat',           // fleet.config.json site charter-ghp expect.marker
    charterGhpLiveSha: 'fb365e38c4eaa8842629bd0fe4f34a74568fd71360531927fa89111f53ef5293',
    charterGhpChurnAfter: '2026-09-29',
    // §armed — PQ-5 kimi dead slot
    pq5Url: 'https://charter-ufo-fsd.kimi.page/',
    pq5Status: 404,
    pq5Bytes: 13409,
    pq5Sha: '93ddca9a021664d562e698eb99d52b84d696f81485847dcfeaf6f4a5c8fca966',
    // §armed — PQ-2 push gate
    pq2Dir: '/home/vgpnk/Projects/ds4cc-marketplace',
    pq2Remote: 'e6bd071887bfaa87eff07ab03d323d5b92760fba',
    pq2Unpushed: 20,                                   // informational on its own
    sitemapUrl: 'https://ds4cc.com/sitemap.xml',
    sitemapStatus: 404,
    sitemapBytes: 9379,
    // §paths
    pathsDriftMax: 0,
  },
};

// r15's live charter-ghp body sha, per /tmp/kake-r15/charter-live.html +
// the round-15 LOG entry (live 2026-09-29T00:48:51Z: 200, 53,386B,
// sha fb365e38…). Kept as a top-level constant so the cross-check below reads
// the r15 snapshot independently of the pin file.
const R15_LIVE_SHA = 'fb365e38c4eaa8842629bd0fe4f34a74568fd71360531927fa89111f53ef5293';
const R15_SNAPSHOT_DEFAULT = '/tmp/kake-r15/charter-live.html';

// Absence vocabulary: a missing cited path is a *declared* absence (exit
// neutral) iff any citing line ±2 carries one of these words.
const ABSENT_RE = /absent|gone|vanished|emptied|no longer|dangling|no such file|never published|missing/i;

// Cited-path grammar (spec, verbatim): ~ or /home/vgpnk, then path chars.
const PATH_RE = /(?:~|\/home\/vgpnk)\/[A-Za-z0-9._@%+{},*-]*(?:\/[A-Za-z0-9._@%+{},*-]*)*/g;

// Verdict sets. DRIFT verdicts flip the exit code; steady-state verdicts do not.
const PQ12_STEADY = new Set(['EDIT-LANDED', 'PERSIST']);
const SECTIONS = ['paths', 'history', 'armed', 'plazir'];

const sha256 = (buf) => crypto.createHash('sha256').update(buf).digest('hex');
const sortedJson = (a) => JSON.stringify([...a].sort());
const hours = (ms) => +(ms / 3600000).toFixed(2);
const nowIso = () => new Date().toISOString().replace(/\.\d{3}Z$/, 'Z');

// ── CLI ────────────────────────────────────────────────────────────────────
function parseArgs(argv) {
  const o = { json: false, offline: false, section: null, repo: null, selftest: false, help: false };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--json') o.json = true;
    else if (a === '--offline') o.offline = true;
    else if (a === '--selftest') o.selftest = true;
    else if (a === '--help' || a === '-h') o.help = true;
    else if (a === '--repo') o.repo = argv[++i];
    else if (a.startsWith('--repo=')) o.repo = a.slice(7);
    else if (a.startsWith('--section=')) o.section = a.slice(10);
    else if (a === '--section') o.section = argv[++i];
    else { console.error(`freshness-sweep: unknown flag: ${a}`); return { err: 64 }; }
  }
  if (o.section === 'pq14') o.section = 'plazir';
  if (o.section !== null && !SECTIONS.includes(o.section)) {
    console.error(`freshness-sweep: unknown section: ${o.section} (know: ${SECTIONS.join(', ')})`);
    return { err: 64 };
  }
  if (o.repo === undefined) { console.error('freshness-sweep: --repo needs a directory'); return { err: 64 }; }
  return o;
}

function usage() {
  console.log(`freshness-sweep — re-verify the lane's standing claims against live surfaces.

Usage: node scripts/freshness-sweep.mjs [--json] [--offline]
       [--section=paths|history|armed] [--repo DIR] [--selftest] [--help]

  (default)        run all three sections, human lines
  --json           one JSON object: {generatedAt,node,repoRoot,ok,code,sections,pins}
  --offline        skip every fetch/ls-remote; §paths + §history still run,
                   skipped checks read 'skipped(offline)'
  --section=NAME   run one section only
  --repo DIR       lane repo root (default: script's parent dir)
  --selftest       hermetic fixtures under /tmp/kake-r16/selftest; prints a
                   case table proving declaredAbsent=exit-neutral, missing
                   without annotation=drift(1), malformed JSONL=2, bad flag=64
  --help           this text

Exit: 0 clean · 1 drift · 2 unreadable/invalid input · 64 usage error.
Read-only: no file writes outside the --selftest fixture dir.`);
}

function resolveRepoRoot(optRepo) {
  const derived = path.resolve(path.dirname(SELF), '..');
  const candidates = [
    optRepo,
    process.env.KAKE_REPO_ROOT,
    derived,
    path.join(os.homedir(), 'projects/shokunin/kake-shokunin'),
  ].filter(Boolean);
  for (const c of candidates) {
    if (fs.existsSync(path.join(c, 'SKILL.md'))) return { root: path.resolve(c), derived };
  }
  return { root: path.resolve(candidates[0]), derived };
}

// ── pins loading ───────────────────────────────────────────────────────────
function loadPins(repoRoot) {
  const file = process.env.KAKE_FRESHNESS_PINS
    || path.join(repoRoot, 'corpus/knowledge/freshness-pins.json');
  if (fs.existsSync(file)) {
    try {
      const parsed = JSON.parse(fs.readFileSync(file, 'utf8'));
      const raw = parsed.pins || {};
      const pins = { ...DEFAULT_PINS.pins, ...raw };
      // Aliases: the landed pins file (r16) names the same quantities
      // differently than this file's defaults. Both spellings are accepted.
      const alias = (own, ...others) => { for (const n of others) if (raw[n] !== undefined) pins[own] = raw[n]; };
      alias('probeFullSweeps', 'probeFullSweepsFloor');
      alias('probeSpotRows', 'probeSpotProbes');
      alias('fleetTotal', 'probeShapeTotal');
      alias('fleetOk', 'probeShapeOk');
      alias('violated', 'probeViolated');
      alias('errors', 'probeErrors');
      const known = new Set([...Object.keys(DEFAULT_PINS.pins),
        'probeFullSweepsFloor', 'probeSpotProbes', 'probeShapeTotal', 'probeShapeOk', 'probeViolated', 'probeErrors',
        'pathsCitedSet', 'pathsMissSet', 'pathsFiles', 'deltaLastEvent', 'deltaEventsExact', 'pathsAbsenceStrictSameLine']);
      const unused = Object.keys(raw).filter((k) => !known.has(k));
      return { pins, source: 'file', file, schema: parsed.schema || null, updated: parsed.updated || null, round: parsed.round ?? null, unused };
    } catch (e) {
      return { pins: { ...DEFAULT_PINS.pins }, source: `file-invalid:${e.message}`, file, error: true, unused: [] };
    }
  }
  return { pins: { ...DEFAULT_PINS.pins }, source: 'defaults', file, schema: DEFAULT_PINS.schema, updated: DEFAULT_PINS.updated, round: DEFAULT_PINS.round, unused: [] };
}

// ── §paths ─────────────────────────────────────────────────────────────────
function listMd(dir, acc = []) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) listMd(p, acc);
    else if (e.name.endsWith('.md')) acc.push(p);
  }
  return acc;
}

// Brace/range expansion: {a,b}, {n..m}, nested groups, innermost-first. The
// alternation-body regex must allow braces in the *prefix* (nested groups), so
// it scans for the innermost {…} instead of anchoring at the first opening.
function expandBraces(tok, cap = 64) {
  let out = [tok];
  for (let pass = 0; pass < 6; pass++) {
    const next = [];
    let changed = false;
    for (const t of out) {
      const m = /\{([^{}]*)\}/.exec(t);
      if (!m) { next.push(t); continue; }
      const body = m[1];
      const rng = /^\s*(-?\d+)\s*\.\.\s*(-?\d+)\s*$/.exec(body);
      let alts;
      if (rng) {
        const [a, b] = [Number(rng[1]), Number(rng[2])];
        const step = a <= b ? 1 : -1;
        alts = [];
        for (let v = a; step > 0 ? v <= b : v >= b; v += step) alts.push(String(v));
      } else {
        alts = body.split(',').map((s) => s.replace(/\s+/g, ''));
      }
      if (alts.some((x) => !/^[A-Za-z0-9._@%+*\/-]*$/.test(x))) { next.push(t); continue; }
      changed = true;
      for (const a of alts) next.push(t.slice(0, m.index) + a + t.slice(m.index + m[0].length));
    }
    out = next;
    if (!changed) break;
    if (out.length > cap) return [tok];
  }
  return out;
}

// Normalize one raw regex hit into {kind, tokens} per the spec:
//   strip trailing ./ ,/ ;/ )/ * "where it is punctuation", strip trailing "/",
//   expand {a,b} groups. Anything still not a concrete checkable path is
//   reported as unresolved rather than as drift (see md notes).
function normalize(tok) {
  let t = tok;
  while (t.length > 1 && '.,;)*'.includes(t[t.length - 1])) t = t.slice(0, -1);
  while (t.length > 1 && t.endsWith('/')) t = t.slice(0, -1);
  const kinds = { kind: 'concrete', tokens: [] };
  const expanded = expandBraces(t);
  const placeholders = [];
  for (const e of expanded) {
    if (/[{}]/.test(e)) { placeholders.push('brace-list-not-expanded'); continue; }
    if (/(^|[^\d])\.\.([^\d]|$)/.test(e)) { placeholders.push('range-not-expanded'); continue; }
    if (/[*?]/.test(e)) { kinds.tokens.push({ token: e, kind: 'glob' }); continue; }
    if (e.endsWith('-') || e.endsWith('~')) { placeholders.push('truncated-placeholder'); continue; }
    kinds.tokens.push({ token: e, kind: 'concrete' });
  }
  if (!kinds.tokens.length && placeholders.length) kinds.kind = 'placeholder';
  else if (placeholders.length) kinds.kind = 'mixed';
  kinds.placeholders = placeholders;
  return kinds;
}

// Absence annotation over the citing line ±2. Returns {token -> evidence}.
// evidence.direct = the word sits on the citing line's own prose; otherwise
// `mentions` says whether the trigger line names the token (or a prefix of it).
// With strict=true only direct/mentioning evidence counts (see the
// pathsAbsenceStrictSameLine pin): on this corpus the prose style trails the
// annotation onto the line after the cite (SKILL.md:328→329), so strict mode is
// opt-in and its false-positive behaviour is pinned by selftest h2.
// REJECTED (r16, measured): narrowing the default further with an
// "attributable" rule (reject a window line that cites some other path) turns
// `~/Projects/ufofsdbeta-kimi-review` into a false drift — publish-queue.md:219-224
// enumerates five danglers across lines and puts the annotation word on
// :223, which cites two other paths. Collective annotations over sibling cites
// are real prose here, so the spec's ±2-line rule stays the default and the
// looseness is surfaced instead as evidence/indirect on every entry.
function annotate(lines, i, tokens, strict) {
  const blanked = (k) => lines[k].replace(PATH_RE, '\u00abcite\u00bb');
  const out = {};
  const direct = ABSENT_RE.exec(blanked(i));
  if (direct) {
    for (const t of tokens) out[t] = { word: direct[0], line: i + 1, direct: true, mentions: true };
    return out;
  }
  const lo = Math.max(0, i - 2);
  const hi = Math.min(lines.length - 1, i + 2);
  for (let k = lo; k <= hi; k++) {
    if (k === i) continue;
    const m = ABSENT_RE.exec(blanked(k));
    if (!m) continue;
    const line = lines[k];
    const segs = [...line.matchAll(PATH_RE)].map((x) => x[0]);
    for (const t of tokens) {
      if (out[t]) continue;
      const mentions = line.includes(t) || segs.some((s) => t === s || t.startsWith(`${s}/`));
      if (strict && !mentions) continue;
      out[t] = { word: m[0], line: k + 1, direct: false, mentions };
    }
  }
  return out;
}

const expandHome = (t) => (t === '~' || t.startsWith('~/') ? path.join(os.homedir(), t.slice(1)) : t);
// Dedupe canonical form: the corpus cites the same target as both `~/x` and
// `/home/vgpnk/x`, which created two keys for one path (scout r16 diff). Output
// is always the `~` spelling; resolution goes through expandHome().
const canonHome = (t) => (t.startsWith('/home/vgpnk/') ? `~${t.slice('/home/vgpnk'.length)}` : t);

function scanCitations(repoRoot, pins = {}) {
  const files = [];
  const skill = path.join(repoRoot, 'SKILL.md');
  if (fs.existsSync(skill)) files.push(skill);
  const corpus = path.join(repoRoot, 'corpus');
  if (fs.existsSync(corpus)) files.push(...listMd(corpus));

  const REL_PATH_RE = /(?:^|[\s`'"([])((?:[\w.@%+-]+\/)+[\w.@%+-]+\.(?:jsonl|json|mjs|js|md|sh|html|txt|timer|service|toml))(?![A-Za-z0-9])/;

  const byToken = new Map(); // token -> {cites:Set, missingCites:Set}
  let occurrences = 0;
  let rawHits = 0;
  const relativeCites = [];   // informational: spec-regex blind spot (see below)

  for (const f of files) {
    const rel = path.relative(repoRoot, f);
    const text = fs.readFileSync(f, 'utf8');
    const lines = text.split('\n');
    const offsets = [];
    { let off = 0; for (const l of lines) { offsets.push(off); off += l.length + 1; } }
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      PATH_RE.lastIndex = 0;
      // Blind spot: PATH_RE only matches cites that start with `~` or
      // /home/vgpnk, so bare relative cites (`reports/keepers/x.md`) are
      // invisible. Count them on the line with the spec matches blanked out —
      // informational only (no base dir is knowable), but it keeps a green run
      // from hiding the part of the citation base it cannot see.
      {
        const rest = line.replace(PATH_RE, ' ');
        const rm = REL_PATH_RE.exec(rest);
        if (rm) relativeCites.push(`${rel}:${i + 1} ${rm[1]}`);
      }
      for (const m of line.matchAll(PATH_RE)) {
        occurrences++;
        rawHits++;
        let raw = m[0];
        let start = offsets[i] + m.index;
        // R1 — brace-close rescue: the cited list spans a line break
        // (`{a.md,\n b.md}`); the per-line regex stops at the space. Walk the
        // text to the brace that CLOSES the group (depth-matched, stop at a
        // backtick or 400 chars) so the whole {a,b} group can be expanded.
        if ((raw.match(/\{/g) || []).length > (raw.match(/\}/g) || []).length) {
          let depth = (raw.match(/\{/g) || []).length - (raw.match(/\}/g) || []).length;
          for (let j = 0; j < 400 && start + raw.length + j < text.length; j++) {
            const c = text[start + raw.length + j];
            if (c === '`') break;
            if (c === '{') depth++;
            else if (c === '}') { depth--; if (depth === 0) { raw = text.slice(start, start + raw.length + j + 1); break; } }
          }
        }
        // R2 — line-continuation rescue: a long path hard-wrapped by the
        // author (`.../dead-slot-` + newline + `recreate-readiness-r9.md`).
        if (/[-/]$/.test(raw) && text[start + raw.length] === '\n') {
          const nxt = /^[ \t]*([A-Za-z0-9._@%+{},*-]+)/.exec(text.slice(start + raw.length + 1, start + raw.length + 200));
          if (nxt && !nxt[1].includes('<')) raw += nxt[1];
        }
        const norm = normalize(raw);
        const cite = `${rel}:${i + 1}`;
        // Annotation window = the citing line ±2 (spec), with every *citation*
        // on the citing line blanked: the absence vocabulary must come from the
        // prose around the cite, not from the path string itself (a cite of
        // `.../selftest-gone.md` otherwise self-annotates on the word "gone").
        // The matched word + the line it came from are kept as evidence so an
        // indirect (bleed) classification is auditable rather than silent, and
        // the opt-in strict pin can require the word to sit on the citing line
        // or on a window line that names the token (or a segment-prefix of it).
        const ann = annotate(lines, i, norm.tokens.map((t) => t.token), pins.pathsAbsenceStrictSameLine === true);
        for (const tk of norm.tokens) {
          const token = canonHome(tk.token);
          const key = `${tk.kind}:${token}`;
          if (!byToken.has(key)) byToken.set(key, { token, kind: tk.kind, cites: new Set(), annotated: false, placeholders: new Set() });
          const rec = byToken.get(key);
          rec.cites.add(cite);
          if (ann[token] || ann[tk.token]) {
            rec.annotated = true;
            if (!rec.evidence) rec.evidence = { ...(ann[token] || ann[tk.token]), cite };
          }
        }
        if (norm.kind === 'placeholder' || norm.kind === 'mixed') {
          for (const ph of norm.placeholders) {
            const key = `placeholder:${raw}`;
            if (!byToken.has(key)) byToken.set(key, { token: raw, kind: 'placeholder', cites: new Set(), annotated: false, placeholders: new Set() });
            byToken.get(key).cites.add(cite);
            byToken.get(key).placeholders.add(ph);
          }
        }
      }
    }
  }

  const resolve = [], declaredAbsent = [], drift = [], unresolved = [];
  for (const rec of byToken.values()) {
    const cites = [...rec.cites].sort();
    if (rec.kind !== 'concrete') {
      unresolved.push({ path: rec.token, kind: rec.kind, cites, reason: [...rec.placeholders].join(',') || `${rec.kind} pattern (not existsSync-checkable)` });
      continue;
    }
    const abs = expandHome(rec.token);
    if (fs.existsSync(abs)) resolve.push({ path: rec.token, resolve: abs, cites });
    else if (rec.annotated) declaredAbsent.push({ path: rec.token, resolve: abs, cites, evidence: rec.evidence || null, indirect: !!(rec.evidence && !rec.evidence.direct && !rec.evidence.mentions) });
    else drift.push({ path: rec.token, resolve: abs, cites });
  }
  const byPath = (a, b) => (a.path < b.path ? -1 : a.path > b.path ? 1 : 0);
  resolve.sort(byPath); declaredAbsent.sort(byPath); drift.sort(byPath); unresolved.sort(byPath);

  // Citation-base delta vs an optional frozen set. A frozen resolve/miss table
  // can report green while the citation base grows every round (r16 scout
  // finding): the SET is the fresh surface, not the count.
  const citedSet = [...byToken.values()].map((r) => r.token).filter((t, i, a) => a.indexOf(t) === i).sort();
  const missSet = [...declaredAbsent, ...drift].map((r) => r.path).sort();
  const relFiles = files.map((f) => path.relative(repoRoot, f)).sort();
  const setDelta = { pinned: false, notes: [] };
  if (Array.isArray(pins.pathsCitedSet)) {
    setDelta.pinned = true;
    setDelta.citedAdded = citedSet.filter((t) => !pins.pathsCitedSet.includes(t));
    setDelta.citedDropped = pins.pathsCitedSet.filter((t) => !citedSet.includes(t));
    setDelta.newDrift = setDelta.citedAdded.filter((t) => drift.some((d) => d.path === t));
  }
  if (Array.isArray(pins.pathsMissSet)) {
    setDelta.pinned = true;
    // Any not-yet-pinned miss is a first-class freshness fault: a citation that
    // stopped resolving must be re-verified and then absorbed into
    // pins.pathsMissSet (annotated) or fixed (unannotated). Repetition across
    // rounds is exactly what the pin is there to prevent (r16 scout finding §3c).
    setDelta.newMissing = missSet.filter((t) => !pins.pathsMissSet.includes(t));
    setDelta.newDrift = setDelta.newMissing.filter((t) => drift.some((d) => d.path === t));
    setDelta.newDeclaredAbsent = setDelta.newMissing.filter((t) => declaredAbsent.some((d) => d.path === t));
    setDelta.recovered = pins.pathsMissSet.filter((t) => !missSet.includes(t));
  }
  if (Array.isArray(pins.pathsFiles)) {
    setDelta.pinned = true;
    setDelta.filesAdded = relFiles.filter((f) => !pins.pathsFiles.includes(f));
    setDelta.filesRemoved = pins.pathsFiles.filter((f) => !relFiles.includes(f));
  }
  if (!setDelta.pinned) setDelta.notes.push('pin pathsMissSet/pathsCitedSet (JSON emits both live) for a set-delta verdict: NEW miss = drift, recovered/added = informational; pin pathsFiles to catch corpus-file moves');
  const newDrift = setDelta.newDrift || [];
  const newMissing = setDelta.newMissing || [];

  return {
    filesScanned: files.length,
    files: relFiles,
    occurrences, rawHits, uniqueTokens: byToken.size,
    resolve: resolve.map((r) => ({ path: r.path, cites: r.cites })),
    declaredAbsent: declaredAbsent.map((r) => ({ path: r.path, cites: r.cites, evidence: r.evidence, indirect: r.indirect })),
    drift: drift.map((r) => ({ path: r.path, resolve: r.resolve, cites: r.cites })),
    unresolved,
    counts: { resolve: resolve.length, declaredAbsent: declaredAbsent.length, declaredAbsentIndirect: declaredAbsent.filter((r) => r.indirect).length, drift: drift.length, unresolved: unresolved.length, newDrift: newDrift.length, newMissing: newMissing.length },
    citedSet, missSet, setDelta,
    relativeCites: { count: relativeCites.length, sample: relativeCites.slice(0, 5), note: 'informational — cites not beginning with ~ or /home/vgpnk fall outside the spec PATH_RE (no base dir knowable); they are NOT resolve-checked' },
    ok: drift.length === 0 && newMissing.length === 0,
  };
}

// ── §history ───────────────────────────────────────────────────────────────
function parseJsonl(file) {
  const raw = fs.readFileSync(file, 'utf8');
  const rows = [];
  const malformed = [];
  raw.split('\n').forEach((line, idx) => {
    const t = line.trim();
    if (!t) return;
    try {
      const r = JSON.parse(t);
      if (typeof r.at !== 'string' || typeof r.total !== 'number' || !Array.isArray(r.violated)) throw new Error('shape');
      rows.push(r);
    } catch (e) { malformed.push({ line: idx + 1, error: e.message, text: t.slice(0, 80) }); }
  });
  return { rows, malformed };
}

function runProbeDelta(repoRoot, historyFile) {
  const script = path.join(repoRoot, 'scripts/probe-delta.mjs');
  if (!fs.existsSync(script)) return { error: `missing ${script}` };
  try {
    const out = execFileSync(process.execPath, [script, '--json', '--history', historyFile], { cwd: repoRoot, encoding: 'utf8' });
    return { json: JSON.parse(out) };
  } catch (e) {
    return { error: `probe-delta failed: ${e.message}`, stderr: String(e.stderr || '').slice(0, 300) };
  }
}

// Informational only — NEVER a drift predicate. On this host
// `systemctl --user show -p NextElapseUSecRealtime webzites-probe.timer` is
// empty even while list-timers shows the next elapse, so we read the rendered
// timer table instead (and say so).
function nextFire(repoRoot) {
  try {
    const out = execFileSync('systemctl', ['--user', 'list-timers', 'webzites-probe.timer', '--no-pager'], { encoding: 'utf8', timeout: 8000 });
    const dataLine = out.split('\n').slice(1).find((l) => l.includes('webzites-probe.timer'));
    if (!dataLine) return { source: 'systemctl --user list-timers', next: null, note: 'no timer line rendered' };
    // Non-tty output is single-space separated (column padding only on a tty),
    // so anchor the parse on the two weekday+date stamps, not on run length.
    const m = /^(\w{3} \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} \S+)\s+(.*?)\s+(\w{3} \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} \S+)\s+(.*?)\s+(webzites-probe\.timer)/.exec(dataLine.trim());
    if (!m) return { source: 'systemctl --user list-timers', next: null, raw: dataLine.trim(), note: 'timer line did not parse' };
    return { source: 'systemctl --user list-timers (NextElapseUSecRealtime is empty on this host; informational, never a predicate)', next: m[1], left: m[2], last: m[3], passed: m[4] };
  } catch (e) {
    return { source: 'systemctl --user list-timers', next: null, note: `unavailable: ${e.message}` };
  }
}

function analyzeHistory({ file, pins, repoRoot, offline }) {
  const res = { file, offline };
  if (!fs.existsSync(file)) return { ...res, error: `cannot read ${file}`, code: 2 };
  let parsed;
  try { parsed = parseJsonl(file); }
  catch (e) { return { ...res, error: `cannot read ${file}: ${e.message}`, code: 2 }; }
  const { rows, malformed } = parsed;
  if (malformed.length) return { ...res, error: `malformed JSONL (${malformed.length} line(s))`, malformed, code: 2 };
  if (!rows.length) return { ...res, error: 'zero usable rows', code: 2 };

  // probe-delta's rule is the source of truth for the split: `universe` is the
  // RUNNING max of total, so a total:14 row was a full sweep at its own point
  // in history even though the fleet later grew to 18 (post-hoc universing
  // mislabels 59 full sweeps as partial — the r16 bug this rule fixes).
  let universe = 0; const full = []; let spots = 0; let partials = 0;
  for (const r of rows) {
    if (r.total > universe) universe = r.total;
    if (r.total > 1 && r.total === universe) full.push(r);
    else if (r.total > 1) partials++;
    else spots++;
  }
  const last = rows[rows.length - 1];

  const ageMs = Date.now() - Date.parse(last.at);
  const ageMaxMs = (pins.probeCadenceHours * 60 + pins.probeSlackMinutes) * 60000;
  const checks = [];
  const chk = (name, expected, actual, ok, note) => { checks.push({ name, expected, actual, ok, ...(note ? { note } : {}) }); };

  chk('rows >= floor', pins.probeRowsFloor, rows.length, rows.length >= pins.probeRowsFloor, `delta ${rows.length - pins.probeRowsFloor >= 0 ? '+' : ''}${rows.length - pins.probeRowsFloor}`);
  chk('last.at >= floor', pins.probeLastAtFloor, last.at, last.at >= pins.probeLastAtFloor);
  chk(`last.at age <= ${hours(ageMaxMs)}h`, '<= ceiling', `${hours(ageMs)}h`, ageMs <= ageMaxMs);
  chk('last.total', pins.fleetTotal, last.total, last.total === pins.fleetTotal);
  chk('last.ok', pins.fleetOk, last.ok, last.ok === pins.fleetOk);
  chk('last.violated set', sortedJson(pins.violated), sortedJson(last.violated), sortedJson(pins.violated) === sortedJson(last.violated));
  chk('last.errors set', sortedJson(pins.errors), sortedJson(last.errors), sortedJson(pins.errors) === sortedJson(last.errors));
  chk('full sweeps (total>1 && total===universe)', pins.probeFullSweeps, full.length, full.length === pins.probeFullSweeps);
  chk('spot rows (total===1)', pins.probeSpotRows, spots, spots === pins.probeSpotRows);

  const delta = runProbeDelta(repoRoot, file);
  let deltaSummary = null;
  if (delta && delta.json) {
    const d = delta.json;
    // probe-delta exposes no `phantom` field. Its own header defines phantoms
    // as noise from naive consecutive diffing (= malformed rows + partial
    // sweeps, which fabricate UNIVERSE/ENTER/EXIT events). phantom := those.
    const phantom = (d.malformed || 0) + (d.partialSweeps || 0);
    const ev = d.events || [];
    const lastEvent = ev.length ? `${ev[ev.length - 1].type} ${ev[ev.length - 1].site} @${ev[ev.length - 1].at}` : 'none';
    const deltaOk = phantom <= pins.deltaPhantomMax && ev.length <= pins.deltaEventsMax;
    checks.push({ name: 'delta phantom (malformed+partialSweeps)', expected: `<= ${pins.deltaPhantomMax}`, actual: phantom, ok: phantom <= pins.deltaPhantomMax });
    checks.push({ name: 'delta events', expected: `<= ${pins.deltaEventsMax}`, actual: ev.length, ok: ev.length <= pins.deltaEventsMax });
    if (pins.deltaEventsExact !== undefined) checks.push({ name: 'delta events (exact)', expected: pins.deltaEventsExact, actual: ev.length, ok: ev.length === pins.deltaEventsExact });
    // A count ceiling alone can absorb oscillation silently (a site flipping
    // ENTER/EXIT adds 2 events while the last-row sets stay identical), so the
    // last-event identity is pinnable (critic r16 finding 2).
    if (pins.deltaLastEvent) checks.push({ name: 'delta last event', expected: pins.deltaLastEvent, actual: lastEvent, ok: lastEvent === pins.deltaLastEvent });
    deltaSummary = {
      rows: d.rows, malformed: d.malformed, fullSweeps: d.fullSweeps,
      spotProbesSkipped: d.spotProbesSkipped, partialSweeps: d.partialSweeps, universe: d.universe,
      phantom, events: ev.length, eventsMax: pins.deltaEventsMax, lastEvent, ok: deltaOk,
      eventList: ev, coverage: d.coverage,
      // informational: the r10 baseline-only first-bracket suppression
      bootstrapSuppressed: bootstrapPhantoms(full),
      note: 'phantom := malformed + partialSweeps (probe-delta has no `phantom` field; header defines phantoms as naive-diff noise)',
    };
  } else if (delta && delta.error) {
    deltaSummary = { error: delta.error, stderr: delta.stderr || null };
    checks.push({ name: 'probe-delta', expected: 'parses', actual: delta.error, ok: false });
  }

  if (!offline) res.nextFire = nextFire(repoRoot);

  // `changed` is derived only after every check (incl. the probe-delta ones,
  // which are appended above) has been pushed — an early derivation would let
  // delta drift pass silently.
  const changed = checks.filter((c) => !c.ok);

  return {
    ...res, rows: rows.length, rowsFloor: pins.probeRowsFloor, rowsDelta: rows.length - pins.probeRowsFloor,
    universe, fullSweeps: full.length, spotRows: spots, partials, malformed: 0,
    lastAt: last.at, lastAtAgeHours: hours(ageMs), lastAtAgeMaxHours: hours(ageMaxMs),
    last: { total: last.total, ok: last.ok, violated: last.violated, errors: last.errors },
    pins: { fleetTotal: pins.fleetTotal, fleetOk: pins.fleetOk, violated: pins.violated, errors: pins.errors },
    verdict: changed.length ? 'CHANGED' : 'MATCH',
    checks, changed, delta: deltaSummary,
    ok: changed.length === 0,
  };
}

// Naive consecutive diff over the FIRST full-sweep bracket — the events
// probe-delta deliberately suppresses (r10: baseline-only, would emit
// bootstrap phantoms). Reported for transparency, never a predicate.
function bootstrapPhantoms(full) {
  if (full.length < 2) return 0;
  const [p, c] = full;
  let n = 0;
  for (const id of c.violated) if (!p.violated.includes(id)) n++;
  for (const id of p.violated) if (!c.violated.includes(id)) n++;
  if (c.total > p.total) n++;
  return n;
}

// ── §armed ─────────────────────────────────────────────────────────────────
async function fetchBody(url, timeoutMs) {
  const res = await fetch(url, { redirect: 'follow', signal: AbortSignal.timeout(timeoutMs) });
  const buf = Buffer.from(await res.arrayBuffer());
  return { status: res.status, finalUrl: res.url, bytes: buf.length, sha256: sha256(buf), body: buf.toString('utf8') };
}

// ── PQ-14: plazir-15-site push gate + live/source sitemap parity ───────────
// The r16 catch: live sitemap carries 8 <loc> (adds /tetris/) while the source
// repo's sitemap.xml has 7 → the published surface has a page the source does
// not know about. Both sub-checks are drift predicates.
async function checkPlazir({ pins, offline, timeoutMs }) {
  const out = { dir: pins.plazirSourceDir || null, offline, driftReasons: [], warnings: [] };
  const exp = { remote: pins.plazirRemote, unpushed: pins.plazirUnpushed, liveLocs: pins.plazirLiveSitemapLocs, sourceLocs: pins.plazirSourceSitemapLocs };

  const gate = { expected: { remote: exp.remote, unpushed: exp.unpushed }, skipped: null };
  if (offline) gate.verdict = 'skipped(offline)';
  else if (!out.dir) { gate.verdict = 'skipped(no-source-dir)'; out.warnings.push('pins.plazirSourceDir absent — plazir gate/source checks cannot run'); }
  else {
    try {
      const g = (args) => execFileSync('git', ['-C', out.dir, ...args], { encoding: 'utf8', timeout: 15000 }).trim();
      gate.remote = g(['ls-remote', 'origin', 'main']).split('\t')[0];
      gate.head = g(['rev-parse', 'HEAD']);
      gate.unpushed = Number(g(['rev-list', '--count', 'origin/main..HEAD']));
      if (gate.remote !== exp.remote) {
        gate.verdict = 'GATE-OPENED';
        out.driftReasons.push('plazir-gate-opened');
        gate.note = `remote moved ${exp.remote} -> ${gate.remote} (the operator pushed)`;
      } else if (gate.unpushed !== exp.unpushed) {
        gate.verdict = 'UNPUSHED-CHANGED';
        out.driftReasons.push('plazir-unpushed-changed');
        gate.note = `remote unchanged, unpushed ${gate.unpushed} != pin ${exp.unpushed} (new local commits)`;
      } else gate.verdict = 'GATE-CLOSED';
    } catch (e) { gate.verdict = 'ANOMALY'; gate.gitError = e.message; out.driftReasons.push('plazir-gate-anomaly'); }
  }

  const live = { url: process.env.KAKE_PLAZIR_LIVE_URL || pins.plazirLiveSitemapUrl, expected: exp.liveLocs };
  if (offline) live.verdict = 'skipped(offline)';
  else {
    try {
      const r = await fetchBody(live.url, timeoutMs);
      live.status = r.status;
      live.locs = (r.body.match(/<loc>/g) || []).length;
      live.verdict = r.status === 200 ? 'COUNTED' : `NOTE-${r.status}`;
    } catch (e) { live.fetchError = e.message; live.verdict = 'ERROR'; }
  }

  const source = { expected: exp.sourceLocs };
  if (!out.dir) { source.verdict = 'skipped(no-source-dir)'; source.reason = 'pins.plazirSourceDir absent'; }
  else {
    const file = path.join(out.dir, 'sitemap.xml');
    if (!fs.existsSync(file)) { source.verdict = 'skipped(no-source-file)'; source.file = file; }
    else {
      try {
        source.file = file;
        source.locs = (fs.readFileSync(file, 'utf8').match(/<loc>/g) || []).length;
        source.verdict = 'COUNTED';
      } catch (e) { source.verdict = 'ERROR'; source.error = e.message; }
    }
  }

  // Parity verdict. Under --offline the live side is unknown, so parity is not
  // evaluated (never silently passed) — the local source count still runs.
  if (offline) out.sitemapVerdict = 'skipped(offline)';
  else if (live.locs === undefined || source.locs === undefined) out.sitemapVerdict = 'NOT-EVALUATED';
  else if (live.locs !== exp.liveLocs || live.locs !== source.locs) {
    out.sitemapVerdict = 'LIVE-SOURCE-GAP';
    out.driftReasons.push('plazir-live-source-gap');
    out.gapDetail = `live ${live.locs} locs (pin ${exp.liveLocs}) vs source ${source.locs} locs (pin ${exp.sourceLocs}) — published surface has entries the source lacks`;
  } else out.sitemapVerdict = 'MATCH';

  out.gate = gate; out.live = live; out.source = source;
  out.expected = exp;
  out.verdict = [gate.verdict, `sitemap ${out.sitemapVerdict}`].join(' · ');
  out.ok = out.driftReasons.length === 0;
  if (offline) out.ok = null;                       // skipped ≠ pass
  return out;
}

async function sectionArmed({ pins, offline, repoRoot, timeoutMs, only = null }) {
  const out = { offline, only };
  if (only === 'plazir') {
    out.plazir = await checkPlazir({ pins, offline, timeoutMs });
    out.driftVerdicts = [...out.plazir.driftReasons];
    out.events = [];
    out.warnings = [...out.plazir.warnings];
    out.ok = offline ? null : out.plazir.ok;
    return out;
  }
  if (offline) {
    out.pq12 = { url: pins.charterGhpUrl, verdict: 'skipped(offline)' };
    out.pq5 = { url: pins.pq5Url, verdict: 'skipped(offline)' };
    out.pq2 = { dir: pins.pq2Dir, verdict: 'skipped(offline)' };
    out.sitemap = { url: pins.sitemapUrl, verdict: 'skipped(offline)' };
    out.plazir = await checkPlazir({ pins, offline, timeoutMs }); // local source count still runs
    out.counted = false;              // skipped checks are NOT passes
    out.ok = null;                    // null = not evaluated (never counted as pass)
    return out;
  }

  // ── PQ-12: charter-ghp beat pin (fleet.config.json site id charter-ghp)
  const pq12 = { url: pins.charterGhpUrl, pin: pins.charterGhpPin, pinSource: 'pins.charterGhpPin (fleet/config marker)' };
  try {
    const fleetFile = process.env.KAKE_FLEET_CONFIG || '/home/vgpnk/Projects/webzites/fleet/fleet.config.json';
    const fleet = JSON.parse(fs.readFileSync(fleetFile, 'utf8'));
    const row = (fleet.sites || []).find((s) => s.id === 'charter-ghp');
    pq12.fleetFile = fleetFile;
    pq12.fleetRow = row ? { id: row.id, url: row.url, status: row.status, expect: row.expect } : null;
    if (row && row.expect && row.expect.marker) {
      pq12.pin = row.expect.marker;
      pq12.pinSource = `${fleetFile} sites[charter-ghp].expect.marker`;
      if (row.expect.marker !== pins.charterGhpPin) pq12.pinDiffersFromPinsFile = { pinsFile: pins.charterGhpPin, fleetConfig: row.expect.marker };
    } else pq12.note = 'fleet row/marker not found — using pins file value';
  } catch (e) { pq12.fleetError = e.message; }

  try {
    const r = await fetchBody(pins.charterGhpUrl, timeoutMs);
    Object.assign(pq12, { status: r.status, bytes: r.bytes, sha256: r.sha256 });
    const lit = /scribe beat[^<]{0,80}/.exec(r.body);
    const dated = /(\d{4}-\d{2}-\d{2})[^<]{0,20}scribe beat/.exec(r.body);
    pq12.liveLiteral = lit ? lit[0] : null;
    pq12.liveDate = dated ? dated[1] : null;
    pq12.liveMarker = pq12.liveDate ? `${pq12.liveDate} scribe beat` : pq12.liveLiteral;
    pq12.shaMatchesR15 = r.sha256 === R15_LIVE_SHA;
    pq12.shaMatchesPin = r.sha256 === pins.charterGhpLiveSha;
    const editLanded = pq12.liveLiteral !== null && (pq12.pin === pq12.liveMarker || pq12.pin === pq12.liveLiteral);
    if (!pq12.liveLiteral) pq12.verdict = 'SILENT';
    else if (editLanded) pq12.verdict = 'EDIT-LANDED';
    else if (r.sha256 === pins.charterGhpLiveSha) pq12.verdict = 'PERSIST';
    else if (pq12.liveDate && pq12.liveDate > pins.charterGhpChurnAfter) pq12.verdict = 'CHURN-AGAIN';
    else pq12.verdict = 'ANOMALY';
    pq12.decisionOrder = 'SILENT > EDIT-LANDED > PERSIST > CHURN-AGAIN > ANOMALY';
    // EDIT-LANDED is a loud EVENT (the armed watch fired) but not itself drift;
    // the *sha pin* it invalidates is. Surface that so a fired watch can never
    // render as a silent green run (critic r16 finding 1/4).
    if (pq12.verdict === 'EDIT-LANDED' && r.sha256 !== pins.charterGhpLiveSha) {
      pq12.pinStale = `live sha ${r.sha256.slice(0, 8)}… != pins.charterGhpLiveSha ${String(pins.charterGhpLiveSha).slice(0, 8)}… — re-baseline the pin in the same commit as the re-pin`;
      pq12.event = 'PQ-12 EDIT-LANDED: fleet.config marker now names the live beat — re-baseline pins.charterGhpLiveSha';
    }
  } catch (e) {
    pq12.fetchError = e.message;
    pq12.verdict = 'SILENT';
  }

  // r15 snapshot cross-check: recompute the pinned body sha from the r15 file
  // and assert equality (mismatch = ANOMALY + loud warning).
  const snap = process.env.KAKE_R15_SNAPSHOT || R15_SNAPSHOT_DEFAULT;
  if (fs.existsSync(snap)) {
    const s = sha256(fs.readFileSync(snap));
    pq12.r15Snapshot = { file: snap, sha256: s, matchesConstant: s === R15_LIVE_SHA, matchesFetched: pq12.sha256 ? s === pq12.sha256 : null };
    if (s !== R15_LIVE_SHA) {
      pq12.verdict = 'ANOMALY';
      pq12.r15SnapshotMismatch = `!! ${snap} sha ${s} != R15_LIVE_SHA ${R15_LIVE_SHA}`;
    }
  } else {
    pq12.r15Snapshot = { file: snap, skipped: 'snapshot absent (expected once landed: /tmp is not durable)' };
  }

  // ── PQ-5: kimi dead slot — 404 is the expected state; any 200 is the E1 EXIT
  const pq5 = { url: pins.pq5Url, expected: { status: pins.pq5Status, bytes: pins.pq5Bytes, sha: pins.pq5Sha }, pinnedBytesShaIsInformational: true };
  try {
    const r = await fetchBody(pins.pq5Url, timeoutMs);
    Object.assign(pq5, { status: r.status, bytes: r.bytes, sha256: r.sha256 });
    if (r.status === 200) pq5.verdict = 'E1-FIRED';
    else if (r.status === pins.pq5Status) pq5.verdict = 'PENDING';
    else pq5.verdict = 'ANOMALY';
    pq5.bodyMatchesPin = r.bytes === pins.pq5Bytes && r.sha256 === pins.pq5Sha;
    if (pq5.verdict === 'PENDING' && !pq5.bodyMatchesPin) pq5.note = 'status holds, dead-slot body changed (bytes/sha vs pin) — inspect before trusting the sentinel';
  } catch (e) { pq5.fetchError = e.message; pq5.verdict = 'ANOMALY'; }

  // ── PQ-2: ds4cc-marketplace push gate (read-only git)
  const pq2 = { dir: pins.pq2Dir, expected: { remote: pins.pq2Remote, unpushed: pins.pq2Unpushed } };
  try {
    const g = (args) => execFileSync('git', ['-C', pins.pq2Dir, ...args], { encoding: 'utf8', timeout: 15000 }).trim();
    pq2.remote = g(['ls-remote', 'origin', 'main']).split('\t')[0];
    pq2.head = g(['rev-parse', 'HEAD']);
    pq2.unpushed = Number(g(['rev-list', '--count', 'origin/main..HEAD']));
    pq2.remoteMatchesPin = pq2.remote === pins.pq2Remote;
    pq2.verdict = pq2.remoteMatchesPin ? 'GATE-CLOSED' : 'GATE-OPENED';
    if (!pq2.remoteMatchesPin) pq2.warning = `!! remote moved: ${pins.pq2Remote} -> ${pq2.remote}`;
    if (pq2.unpushed !== pins.pq2Unpushed) pq2.note = `unpushed count ${pq2.unpushed} != pin ${pins.pq2Unpushed} (informational unless remote also moved)`;
  } catch (e) { pq2.gitError = e.message; pq2.verdict = 'ANOMALY'; }

  // ── sitemap: ds4cc.com listing preview (404 = pre-push, expected)
  const sitemap = { url: pins.sitemapUrl, expected: pins.sitemapStatus, pinnedBytes: pins.sitemapBytes, pinnedBytesIsInformational: true };  // status is the predicate; bytes recorded
  try {
    const r = await fetchBody(pins.sitemapUrl, timeoutMs);
    Object.assign(sitemap, { status: r.status, bytes: r.bytes });
    sitemap.verdict = r.status === pins.sitemapStatus ? 'PRE-PUSH'
      : r.status === 200 ? 'LISTED-LIVE' : `NOTE-${r.status}`;
    sitemap.ok = r.status === pins.sitemapStatus;
  } catch (e) { sitemap.fetchError = e.message; sitemap.verdict = 'ERROR'; sitemap.ok = false; }

  const plazir = await checkPlazir({ pins, offline, timeoutMs, });

  const driftVerdicts = [];
  if (!PQ12_STEADY.has(pq12.verdict)) driftVerdicts.push(`PQ-12 ${pq12.verdict}`);
  if (pq12.pinStale) driftVerdicts.push('PQ-12 EDIT-LANDED fired — sha pin re-baseline required');
  if (pq5.verdict !== 'PENDING') driftVerdicts.push(`PQ-5 ${pq5.verdict}`);
  if (pq2.verdict !== 'GATE-CLOSED') driftVerdicts.push(`PQ-2 ${pq2.verdict}`);
  if (sitemap.verdict !== 'PRE-PUSH') driftVerdicts.push(`sitemap ${sitemap.verdict}`);
  for (const r of plazir.driftReasons) driftVerdicts.push(r);

  out.pq12 = pq12; out.pq5 = pq5; out.pq2 = pq2; out.sitemap = sitemap; out.plazir = plazir;
  out.driftVerdicts = driftVerdicts;
  out.events = [pq12.event].filter(Boolean);
  out.warnings = [...plazir.warnings];
  if (pq12.r15Snapshot && pq12.r15Snapshot.skipped) out.warnings.push(`r15 charter snapshot absent (${pq12.r15Snapshot.file}) — the R15_LIVE_SHA cross-check did not run on this host; PERSIST rests on the pinned sha alone`);
  if (pq12.pinDiffersFromPinsFile) out.warnings.push(`fleet.config marker differs from the pins file (${pq12.pinDiffersFromPinsFile.pinsFile} vs ${pq12.pinDiffersFromPinsFile.fleetConfig}) — re-pin one of them`);
  out.ok = driftVerdicts.length === 0;
  return out;
}

// ── reporting ──────────────────────────────────────────────────────────────
function printPaths(p) {
  console.log(`§paths  ${p.filesScanned} files · ${p.occurrences} occurrences · ${p.uniqueTokens} unique tokens`);
  console.log(`  resolve ${p.counts.resolve} · declaredAbsent ${p.counts.declaredAbsent} · drift ${p.counts.drift} · unresolved ${p.counts.unresolved}`);
  if (p.counts.drift) {
    console.log(`  !! DRIFT ${p.counts.drift} cited path(s) missing with no absent-annotation:`);
    for (const d of p.drift) console.log(`     ${d.path}  (${d.cites.length} cite(s): ${d.cites.slice(0, 3).join(', ')}${d.cites.length > 3 ? ', …' : ''})`);
  }
  for (const d of p.declaredAbsent) console.log(`  declaredAbsent  ${d.path}  ${d.cites[0]}${d.cites.length > 1 ? ` (+${d.cites.length - 1})` : ''}${d.indirect ? ` [indirect: "${d.evidence.word}" @${d.evidence.line}, no token mention]` : ''}`);
  if (p.counts.unresolved) console.log(`  unresolved (not existsSync-checkable): ${p.unresolved.map((u) => `${u.path} [${u.kind}]`).join(' · ')}`);
  console.log(`  citation base: ${p.citedSet.length} targets · missSet ${p.missSet.length} · files ${p.files.length}`);
  console.log(`  relative-form cites (outside PATH_RE, not resolve-checked): ${p.relativeCites.count}${p.relativeCites.count ? ` — e.g. ${p.relativeCites.sample.join(' · ')}` : ''}`);
  const sd = p.setDelta;
  if (sd.pinned) {
    if (sd.citedAdded) console.log(`  set-delta cited: +${sd.citedAdded.length} new / -${sd.citedDropped.length} dropped${sd.citedAdded.length ? ` — new: ${sd.citedAdded.join(' · ')}` : ''}${sd.citedDropped.length ? ` — dropped: ${sd.citedDropped.join(' · ')}` : ''}`);
    if (sd.newMissing) console.log(`  set-delta miss: ${sd.newMissing.length ? '!! NEW MISS ' + sd.newMissing.join(' · ') : 'no new miss'}${sd.recovered && sd.recovered.length ? ` · recovered: ${sd.recovered.join(' · ')}` : ''}`);
    if (sd.filesAdded) console.log(`  set-delta files: +${sd.filesAdded.length} / -${sd.filesRemoved.length}${sd.filesAdded.length ? ` — added: ${sd.filesAdded.join(' · ')}` : ''}${sd.filesRemoved.length ? ` — removed: ${sd.filesRemoved.join(' · ')}` : ''}`);
  } else if (sd.notes.length) console.log(`  set-delta: unpinned — ${sd.notes[0]}`);
}

function printHistory(h) {
  if (h.error) { console.log(`§history  !! ERROR ${h.error}`); return; }
  console.log(`§history  ${h.file}`);
  console.log(`  rows ${h.rows} (floor ${h.rowsFloor}, delta ${h.rowsDelta >= 0 ? '+' : ''}${h.rowsDelta}) · full ${h.fullSweeps} · spot ${h.spotRows} · partial ${h.partials} · universe ${h.universe} · malformed 0`);
  console.log(`  last ${h.lastAt} (age ${h.lastAtAgeHours}h, ceiling ${h.lastAtAgeMaxHours}h) total=${h.last.total} ok=${h.last.ok}`);
  console.log(`  violated [${h.last.violated.join(',')}]  errors [${h.last.errors.join(',')}]`);
  console.log(`  verdict ${h.verdict}${h.changed.length ? ' — CHANGED (drift); expected vs actual:' : ''}`);
  for (const c of h.changed) console.log(`    !! ${c.name}: expected ${JSON.stringify(c.expected)} · actual ${JSON.stringify(c.actual)}${c.note ? ` (${c.note})` : ''}`);
  if (h.delta && h.delta.events !== undefined) {
    console.log(`  probe-delta: ${h.delta.events} event(s) (max ${h.delta.eventsMax}) · phantom ${h.delta.phantom} · bootstrap-suppressed ${h.delta.bootstrapSuppressed} · median gap ${h.delta.coverage.medianGapH}h · last ${h.delta.lastEvent}`);
    for (const e of h.delta.eventList) console.log(`    ${e.at}  ${e.type.padEnd(8)} ${e.site}${e.detail ? ` — ${e.detail}` : ''}`);
  } else if (h.delta && h.delta.error) console.log(`  !! probe-delta: ${h.delta.error}`);
  if (h.nextFire) console.log(`  next fire (informational): ${h.nextFire.next || 'n/a'}${h.nextFire.left ? ` (in ${h.nextFire.left})` : ''} — source: ${h.nextFire.source}`);
}

function printArmed(a) {
  console.log('§armed');
  if (a.offline) { console.log('  all remote checks skipped(offline) — NOT counted as pass (complete=false)'); return; }
  const p12 = a.pq12;
  console.log(`  PQ-12 charter-ghp  ${p12.verdict}${PQ12_STEADY.has(p12.verdict) ? '' : '  !! DRIFT'}`);
  console.log(`    pin      ${JSON.stringify(p12.pin)}  (${p12.pinSource})`);
  console.log(`    live     ${JSON.stringify(p12.liveMarker)}  status ${p12.status} bytes ${p12.bytes} sha ${String(p12.sha256).slice(0, 8)}…`);
  console.log(`    sha: pin ${p12.shaMatchesPin ? 'match' : 'DIFFER'} · r15 ${p12.shaMatchesR15 ? 'match' : 'DIFFER'} · order ${p12.decisionOrder}`);
  if (p12.r15Snapshot && p12.r15Snapshot.skipped) console.log(`    r15 snapshot: ${p12.r15Snapshot.skipped}`);
  else if (p12.r15Snapshot) console.log(`    r15 snapshot ${p12.r15Snapshot.file}: ${p12.r15Snapshot.matchesConstant ? 'sha == R15_LIVE_SHA ✓' : '!! MISMATCH'}`);
  if (p12.r15SnapshotMismatch) console.log(`    ${p12.r15SnapshotMismatch}`);
  if (p12.pinDiffersFromPinsFile) console.log(`    !! fleet.config marker != pins file: ${JSON.stringify(p12.pinDiffersFromPinsFile)}`);
  if (p12.event) console.log(`    !! EVENT: ${p12.event}`);
  if (p12.pinStale) console.log(`    !! ${p12.pinStale}`);
  const p5 = a.pq5;
  console.log(`  PQ-5 kimi dead slot  ${p5.verdict}${p5.verdict === 'PENDING' ? '' : '  !! DRIFT (E1 EXIT event)'}`);
  console.log(`    expected ${p5.expected.status}/${p5.expected.bytes}B/${p5.expected.sha.slice(0, 8)}… · live ${p5.status}/${p5.bytes}B/${String(p5.sha256).slice(0, 8)}…${p5.bodyMatchesPin ? ' (body matches pin)' : ''}`);
  if (p5.note) console.log(`    note: ${p5.note}`);
  const p2 = a.pq2;
  console.log(`  PQ-2 push gate  ${p2.verdict}${p2.verdict === 'GATE-CLOSED' ? '' : '  !! DRIFT (loud)'}`);
  console.log(`    remote ${p2.remote} (pin ${p2.expected.remote}) · HEAD ${String(p2.head).slice(0, 8)} · unpushed ${p2.unpushed} (pin ${p2.expected.unpushed})`);
  if (p2.warning) console.log(`    ${p2.warning}`);
  if (p2.note) console.log(`    note: ${p2.note}`);
  const sm = a.sitemap;
  console.log(`  ds4cc sitemap  ${sm.verdict}${sm.verdict === 'PRE-PUSH' ? '' : '  (listing changed)'} — status ${sm.status}${sm.bytes !== undefined ? `/${sm.bytes}B` : ''}`);
  if (a.driftVerdicts && a.driftVerdicts.length) console.log(`  !! DRIFT verdicts: ${a.driftVerdicts.join(' · ')}`);
  if (a.plazir) printPlazir(a.plazir);
}

// PQ-14 plazir-15-site: push gate + live/source sitemap parity.
function printPlazir(p) {
  const g = p.gate || {}, live = p.live || {}, src = p.source || {};
  console.log(`  PQ-14 plazir-15-site  ${p.verdict}${p.ok === false ? '  !! DRIFT' : p.ok === null ? '  (not evaluated — offline)' : ''}`);
  console.log(`    gate ${g.verdict}${g.skipped ? ` (${g.skipped})` : ''} — remote ${g.remote || 'n/a'} (pin ${g.expected.remote}) · HEAD ${String(g.head || '').slice(0, 8)} · unpushed ${g.unpushed !== undefined ? g.unpushed : 'n/a'} (pin ${g.expected.unpushed})`);
  if (g.note) console.log(`      ${g.note}`);
  console.log(`    sitemap ${p.sitemapVerdict} — live ${live.locs !== undefined ? `${live.locs} locs` : live.verdict} (pin ${p.expected.liveLocs}) · source ${src.locs !== undefined ? `${src.locs} locs` : src.verdict} (pin ${p.expected.sourceLocs})${src.file ? ` · ${src.file}` : ''}${src.reason ? ` · ${src.reason}` : ''}`);
  if (p.gapDetail) console.log(`    !! ${p.gapDetail}`);
  if (p.dir) console.log(`    dir ${p.dir}`);
}

// ── orchestration ──────────────────────────────────────────────────────────
async function runSections({ repoRoot, pinsFile, sections, offline, timeoutMs }) {
  const pins = pinsFile.pins;
  const out = { sections: {}, notes: [] };
  if (sections.includes('paths')) out.sections.paths = scanCitations(repoRoot, pins);
  if (sections.includes('history')) out.sections.history = analyzeHistory({
    file: process.env.KAKE_PROBE_HISTORY || path.join(os.homedir(), 'Projects/webzites/state/probe-history.jsonl'),
    pins, repoRoot, offline: false,
  });
  if (offline && sections.includes('history')) {
    out.sections.history.offline = true;
    out.sections.history.notes = ['probe-delta is a local child process — still run under --offline'];
  }
  if (sections.includes('armed')) out.sections.armed = await sectionArmed({ pins, offline, repoRoot, timeoutMs });
  // `plazir` is a sub-section of §armed; standalone only when armed was not
  // requested, so `(default)`/`--section=armed` never run it twice.
  if (sections.includes('plazir') && !sections.includes('armed')) {
    out.sections.plazir = await sectionArmed({ pins, offline, repoRoot, timeoutMs, only: 'plazir' });
  }
  // Gate pins: without them the set-delta / last-event / exact-count verdicts
  // are inert (they cannot fail), so their absence is reported loudly rather
  // than silently absorbed (critic r16 finding A).
  const GATE_KEYS = ['pathsMissSet', 'pathsFiles', 'deltaLastEvent', 'deltaEventsExact'];
  const inertGates = GATE_KEYS.filter((k) => pins[k] === undefined);
  if (inertGates.length) {
    out.gateWarnings = [`gate pins absent from ${pinsFile.file}: ${inertGates.join(', ')} — these verdicts are inert (cannot fail) until pinned`];
  }
  return out;
}

function verdictOf(sections) {
  let code = 0; const reasons = [];
  const p = sections.paths;
  if (p && !p.ok) { code = Math.max(code, 1); reasons.push(`§paths: ${p.counts.drift} unannotated miss · ${p.counts.newMissing} NOT in pins.pathsMissSet`); }
  const h = sections.history;
  if (h && h.error) { code = Math.max(code, h.code || 2); reasons.push(`§history ${h.error}`); }
  else if (h && !h.ok) { code = Math.max(code, 1); reasons.push(`§history CHANGED (${h.changed.length} check(s))`); }
  const a = sections.armed || sections.plazir;
  if (a && a.ok === false) { code = Math.max(code, 1); reasons.push(`§armed: ${a.driftVerdicts.join(', ')}`); }
  const skipped = a && a.offline ? ['§armed (all remote checks)'] : [];
  return { code, reasons, skipped };
}

async function main() {
  const opt = parseArgs(process.argv.slice(2));
  if (opt.err) process.exit(opt.err);
  if (opt.help) { usage(); process.exit(0); }
  if (opt.selftest) { process.exit(await selftest()); }

  const { root: repoRoot, derived } = resolveRepoRoot(opt.repo);
  const pinsFile = loadPins(repoRoot);
  const sections = opt.section ? [opt.section] : SECTIONS;
  const timeoutMs = Number(process.env.KAKE_FETCH_TIMEOUT || 15000);
  const result = await runSections({ repoRoot, pinsFile, sections, offline: opt.offline, timeoutMs });
  const v = verdictOf(result.sections, sections);
  const ok = v.code === 0;

  if (opt.json) {
    console.log(JSON.stringify({
      generatedAt: nowIso(),
      node: process.version,
      repoRoot,
      complete: !opt.offline,
      ok,
      code: v.code,
      sections: result.sections,
      pins: { ...pinsFile.pins, _source: pinsFile.source, _file: pinsFile.file, _schema: pinsFile.schema, _updated: pinsFile.updated, _round: pinsFile.round, _unused: pinsFile.unused },
      reasons: v.reasons,
      skipped: v.skipped,
      ...(result.gateWarnings ? { gateWarnings: result.gateWarnings } : {}),
      ...(repoRoot !== derived ? { note: `repoRoot via override (script-derived: ${derived})` } : {}),
    }, null, 2));
    process.exit(v.code);
  }

  console.log(`freshness-sweep — kake-shokunin freshness axis`);
  console.log(`generated ${nowIso()} · node ${process.version} · repo ${repoRoot}${repoRoot !== derived ? ' (override)' : ''}${opt.offline ? ' · OFFLINE' : ''}`);
  console.log(`pins: ${pinsFile.source} ${pinsFile.file} (round ${pinsFile.round}, updated ${pinsFile.updated})`);
  if (pinsFile.unused && pinsFile.unused.length) console.log(`pins not evaluated by this instrument (informational): ${pinsFile.unused.join(', ')}`);
  if (result.sections.paths) printPaths(result.sections.paths);
  if (result.sections.history) printHistory(result.sections.history);
  if (result.sections.armed) printArmed(result.sections.armed);
  if (result.gateWarnings) for (const w of result.gateWarnings) console.log(`!! ${w}`);
  if (result.sections.armed && result.sections.armed.warnings) for (const w of result.sections.armed.warnings) console.log(`!! WARN ${w}`);
  if (v.skipped.length) console.log(`skipped(offline): ${v.skipped.join(' · ')} — complete=false, never counted as pass`);
  console.log(`VERDICT: ${ok ? 'OK' : 'DRIFT'}${v.reasons.length ? ` — ${v.reasons.join(' · ')}` : ''}${result.sections.armed && result.sections.armed.events && result.sections.armed.events.length ? ` — EVENT: ${result.sections.armed.events.join(' · ')}` : ''} (exit ${v.code}${opt.offline ? ', partial: offline' : ''}${result.gateWarnings ? ', gates inert' : ''})`);
  process.exit(v.code);
}

// ── --selftest: hermetic fixtures + self-source read-only assertion ─────────
async function selftest() {
  const dir = process.env.KAKE_SELFTEST_DIR || '/tmp/kake-r16/selftest';
  const cases = [];
  const run = (args, env) => {
    try {
      const stdout = execFileSync(process.execPath, [SELF, ...args], { encoding: 'utf8', env: { ...process.env, ...env }, stdio: ['ignore', 'pipe', 'pipe'] });
      return { code: 0, stdout };
    } catch (e) { return { code: e.status === undefined ? -1 : e.status, stdout: String(e.stdout || ''), stderr: String(e.stderr || '') }; }
  };

  // SELFTEST-WRITES-BEGIN (only writes in this file live here)
  const annotated = path.join(dir, 'annotated-only');
  const unannotated = path.join(dir, 'unannotated');
  fs.mkdirSync(path.join(annotated, 'corpus/knowledge'), { recursive: true });
  fs.mkdirSync(path.join(unannotated, 'corpus/knowledge'), { recursive: true });
  fs.writeFileSync(path.join(annotated, 'SKILL.md'),
    '# fixture A\n\n'
    + 'Known miss: `~/Projects/webzites/selftest-missing.md` (fixture, deliberately not created).\n'
    + 'That path is **absent since 2026-09-28** (fixture annotation).\n');
  fs.writeFileSync(path.join(annotated, 'corpus/knowledge/note.md'), 'See `~/Projects/webzites/fleet` (fixture, resolves).\n');
  fs.writeFileSync(path.join(unannotated, 'SKILL.md'),
    '# fixture B\n\nCite `~/Projects/webzites/selftest-gone.md` here (fixture; no annotation anywhere).\n');
  fs.writeFileSync(path.join(unannotated, 'corpus/knowledge/note.md'), 'no paths here\n');
  // fixture F documents the spec's ±2-line window semantics: a missing path whose
  // window merely mentions "missing" for an unrelated reason is declaredAbsent.
  const loose = path.join(dir, 'loose-window');
  fs.mkdirSync(path.join(loose, 'corpus'), { recursive: true });
  fs.writeFileSync(path.join(loose, 'SKILL.md'),
    '# fixture F\n\nThe roster is missing one row.\n\nCite `~/Projects/webzites/selftest-unrelated.md` (fixture).\n');
  const pins = path.join(dir, 'pins.json');
  fs.writeFileSync(pins, JSON.stringify({ schema: 'kake-freshness-pins-v1', round: 0, pins: { pathsDriftMax: 0 } }, null, 2));
  const pinsSetDelta = path.join(dir, 'pins-setdelta.json');
  fs.writeFileSync(pinsSetDelta, JSON.stringify({ schema: 'kake-freshness-pins-v1', round: 0, pins: { pathsMissSet: [] } }, null, 2));
  const pinsStrict = path.join(dir, 'pins-strict.json');
  fs.writeFileSync(pinsStrict, JSON.stringify({ schema: 'kake-freshness-pins-v1', round: 0, pins: { pathsAbsenceStrictSameLine: true } }, null, 2));
  // fixture H — the corpus prose style: annotation trails the cite onto the
  // next line without repeating the path. Spec-literal window => declaredAbsent;
  // strict pin => drift (this is why strict is opt-in, not the default).
  const strictRoot = path.join(dir, 'strict-window');
  fs.mkdirSync(path.join(strictRoot, 'corpus'), { recursive: true });
  fs.writeFileSync(path.join(strictRoot, 'SKILL.md'),
    '# fixture H\n\n'
    + 'Cite `~/Projects/webzites/selftest-trailing.md`.\n'
    + 'That path is absent since 2026-09-28 (annotation names no path).\n\n'
    + 'Cite `~/Projects/webzites/selftest-named.md`.\n'
    + 'Note: `~/Projects/webzites/selftest-named.md` is absent (annotation names the path).\n');
  const badHistory = path.join(dir, 'bad-history.jsonl');
  fs.writeFileSync(badHistory, '{"at":"2026-09-29T00:00:00.000Z","total":1,"ok":1,"violated":[],"errors":[]}\n{"at": "broken\n');
  // SELFTEST-WRITES-END

  const envA = { KAKE_REPO_ROOT: annotated, KAKE_FRESHNESS_PINS: pins, KAKE_FETCH_TIMEOUT: '2000' };
  let r = run(['--section=paths', '--json', '--offline'], envA);
  let j = null; try { j = JSON.parse(r.stdout); } catch { /* fall through */ }
  cases.push({
    id: 'a annotated-missing -> declaredAbsent, exit-neutral',
    expect: 'exit 0 · declaredAbsent contains selftest-missing.md · drift []',
    got: `exit ${r.code} · declaredAbsent ${JSON.stringify(j && j.sections.paths.declaredAbsent.map((d) => d.path))} · drift ${JSON.stringify(j && j.sections.paths.drift.map((d) => d.path))} · resolve ${JSON.stringify(j && j.sections.paths.resolve.map((d) => d.path))}`,
    pass: r.code === 0 && !!j && j.sections.paths.drift.length === 0
      && j.sections.paths.declaredAbsent.some((d) => d.path.endsWith('selftest-missing.md'))
      && !j.sections.paths.declaredAbsent.some((d) => d.path.endsWith('selftest-present.md'))
      && j.sections.paths.resolve.some((d) => d.path.endsWith('fleet')),
  });

  const envB = { KAKE_REPO_ROOT: unannotated, KAKE_FRESHNESS_PINS: pins, KAKE_FETCH_TIMEOUT: '2000' };
  r = run(['--section=paths', '--json'], envB);
  j = null; try { j = JSON.parse(r.stdout); } catch { /* fall through */ }
  cases.push({
    id: 'b unannotated-missing -> drift, exit 1',
    expect: 'exit 1 · drift contains selftest-gone.md',
    got: `exit ${r.code} · drift ${JSON.stringify(j && j.sections.paths.drift.map((d) => d.path))}`,
    pass: r.code === 1 && !!j && j.sections.paths.drift.some((d) => d.path.endsWith('selftest-gone.md')),
  });

  // Case F is a documented limitation, asserted so it can never rot silently:
  // the spec's ±2-line window is word-based, so an unrelated "missing" in the
  // window marks a truly-missing cite as declaredAbsent (exit-neutral).
  r = run(['--section=paths', '--json'], { KAKE_REPO_ROOT: loose, KAKE_FRESHNESS_PINS: pins });
  j = null; try { j = JSON.parse(r.stdout); } catch { /* fall through */ }
  cases.push({
    id: 'f (documented limitation) unrelated absent-word in ±2 lines -> declaredAbsent',
    expect: 'exit 0 · declaredAbsent contains selftest-unrelated.md · drift [] — spec-mandated window semantics',
    got: `exit ${r.code} · declaredAbsent ${JSON.stringify(j && j.sections.paths.declaredAbsent.map((d) => d.path))} · drift ${JSON.stringify(j && j.sections.paths.drift.map((d) => d.path))}`,
    pass: r.code === 0 && !!j && j.sections.paths.declaredAbsent.some((d) => d.path.endsWith('selftest-unrelated.md')) && j.sections.paths.drift.length === 0,
  });

  // Case G: the same annotated-missing fixture, but with pathsMissSet pinned
// empty — the first-seen miss must now FAIL (set-delta is a verdict, not a
// report), proving case A's green came from the pin, not from a can-only-pass.
  r = run(['--section=paths', '--json'], { KAKE_REPO_ROOT: annotated, KAKE_FRESHNESS_PINS: pinsSetDelta });
  j = null; try { j = JSON.parse(r.stdout); } catch { /* fall through */ }
  cases.push({
    id: 'g pinned-empty pathsMissSet -> first-seen miss fails (set-delta verdict)',
    expect: 'exit 1 · setDelta.newMissing contains selftest-missing.md · drift []',
    got: `exit ${r.code} · newMissing ${JSON.stringify(j && j.sections.paths.setDelta.newMissing)} · drift ${JSON.stringify(j && j.sections.paths.drift.map((d) => d.path))}`,
    pass: r.code === 1 && !!j && j.sections.paths.setDelta.newMissing.includes('~/Projects/webzites/selftest-missing.md') && j.sections.paths.drift.length === 0,
  });

  // Cases H1/H2: the same trailing-annotation fixture under the spec-literal
// window and under the opt-in strict pin.
  r = run(['--section=paths', '--json'], { KAKE_REPO_ROOT: strictRoot, KAKE_FRESHNESS_PINS: pins });
  j = null; try { j = JSON.parse(r.stdout); } catch { /* fall through */ }
  cases.push({
    id: 'h1 spec-literal ±2 window: trailing annotation -> declaredAbsent, exit 0',
    expect: 'exit 0 · declaredAbsent has trailing+named · drift []',
    got: `exit ${r.code} · declaredAbsent ${JSON.stringify(j && j.sections.paths.declaredAbsent.map((d) => d.path))} · drift ${JSON.stringify(j && j.sections.paths.drift.map((d) => d.path))}`,
    pass: r.code === 0 && !!j
      && j.sections.paths.declaredAbsent.some((d) => d.path.endsWith('selftest-trailing.md'))
      && j.sections.paths.declaredAbsent.some((d) => d.path.endsWith('selftest-named.md'))
      && j.sections.paths.drift.length === 0,
  });
  r = run(['--section=paths', '--json'], { KAKE_REPO_ROOT: strictRoot, KAKE_FRESHNESS_PINS: pinsStrict });
  j = null; try { j = JSON.parse(r.stdout); } catch { /* fall through */ }
  cases.push({
    id: 'h2 strict pin (pathsAbsenceStrictSameLine): unnamed trailing annotation -> drift, exit 1',
    expect: 'exit 1 · drift has trailing · declaredAbsent has named · evidence.direct/mentions recorded',
    got: `exit ${r.code} · drift ${JSON.stringify(j && j.sections.paths.drift.map((d) => d.path))} · declaredAbsent ${JSON.stringify(j && j.sections.paths.declaredAbsent.map((d) => d.path))}`,
    pass: r.code === 1 && !!j
      && j.sections.paths.drift.some((d) => d.path.endsWith('selftest-trailing.md'))
      && j.sections.paths.declaredAbsent.some((d) => d.path.endsWith('selftest-named.md'))
      && j.sections.paths.declaredAbsent.every((d) => d.evidence && d.evidence.mentions === true),
  });

  r = run(['--section=history', '--json'], { KAKE_FRESHNESS_PINS: pins, KAKE_PROBE_HISTORY: badHistory });
  cases.push({
    id: 'c malformed JSONL -> exit 2',
    expect: 'exit 2 · error names malformed JSONL',
    got: `exit ${r.code} · stderr/stdout ${JSON.stringify((r.stdout || r.stderr || '').slice(0, 120))}`,
    pass: r.code === 2 && /malformed/.test(r.stdout || r.stderr || ''),
  });

  r = run(['--bogus-flag'], {});
  cases.push({
    id: 'd unknown flag -> exit 64',
    expect: 'exit 64',
    got: `exit ${r.code} · ${JSON.stringify((r.stderr || '').trim().slice(0, 80))}`,
    pass: r.code === 64,
  });

  // Self-source read-only assertion: every write-API call site must sit inside
  // the SELFTEST-WRITES region. Names are assembled so the checker's own
  // source cannot self-match.
  const WRITE_APIS = ['writeFile', 'mkdir', 'appendFile', 'rm', 'unlink', 'rmdir'].map((s) => s + 'Sync').concat(['createWriteStream', 'writeFile', 'mkdir']);
  const src = fs.readFileSync(SELF, 'utf8').split('\n');
  const begin = src.findIndex((l) => l.includes('SELFTEST-WRITES-BEGIN'));
  const end = src.findIndex((l) => l.includes('SELFTEST-WRITES-END'));
  const re = new RegExp(`(?:^|[^A-Za-z0-9_$])(${WRITE_APIS.join('|')})\\s*\\(`);
  const violations = [];
  src.forEach((l, i) => {
    if (l.trim().startsWith('//')) return;
    if (re.test(l) && (i < begin || i > end)) violations.push(`${i + 1}: ${l.trim().slice(0, 70)}`);
  });
  cases.push({
    id: 'e write-API call sites confined to SELFTEST-WRITES region',
    expect: '0 call sites outside the region',
    got: `${violations.length} outside${violations.length ? `: ${violations.join(' | ')}` : ''} (region lines ${begin + 1}-${end + 1})`,
    pass: violations.length === 0,
  });

  const failed = cases.filter((c) => !c.pass);
  console.log('freshness-sweep --selftest');
  console.log(`fixtures: ${dir} (hermetic; re-runnable)`);
  for (const c of cases) console.log(`  ${c.pass ? 'PASS' : 'FAIL'}  ${c.id}\n        expect: ${c.expect}\n        got:    ${c.got}`);
  console.log(`selftest: ${cases.length - failed.length}/${cases.length} passed`);
  return failed.length ? 1 : 0;
}

main().catch((e) => { console.error(`freshness-sweep: ${e && e.stack || e}`); process.exit(2); });