#!/usr/bin/env python3
"""Round-53 gate-truth counter — locators, revision notes and refusal grounds.

Test evidence for the round-52 verifier spot-check defects that the round-52 quote-truth
counter (`.ufo/waves/round-52/c52_quote_truth.py`) passes green, because its C5 only asks
whether a `## Gate` quote is a raw substring of the retained body:

  spot-check item 5  the S329 and S312 section locators (lesson `## Gate` and registry
                     anchor) name headings that do not contain the quote; the S329 note
                     "no revision printed" is false and the S312 "章节时间戳" is the
                     page-level marker.
  spot-check item 6  both refusals are stated on grounds the held entries do not carry.

Lane inputs are committed bytes at --revision (`git show`). The staged entries are read
from --staged-dir and must equal the sha256 pins in its `provenance.json`: the round-52
lane did not retain them, so the snapshot is the only fixed copy.

Heading rule: a heading is the text of an h1-h6 element or of any element carrying
`name="h2_article_titleN"` (the Baidu college pages mark in-article section headings that
way). The heading containing a quote occurrence is the last heading starting before it,
and its section runs to the next heading. A § leaf is the text after the last "→" of each
" / "-separated locator part, with the trailing parenthetical removed; it names a heading
when it is at least 4 characters long and a substring of the heading, both
whitespace-normalized.

Checks
  L1 gate_locator      every `## Gate` § leaf set names a heading containing the quote.
  L2 registry_anchor   the same for the registry row's anchor cell.
  L3 revision_notes    in either locator parenthetical: "no revision printed" is false if
                       the body prints a page-level revision marker; a 章节时间戳 / section
                       timestamp date must occur inside the quote's section; every cited
                       date must occur in the body.
  R0 staged_snapshot   each refused entry is in the snapshot and its `source:` ids are in
                       the round's retained staged-id list.
  R1 refusal_ids       the ids a refusal names as staged are the staged entry's ids.
  R2 held_ground       a held knowledge entry the refusal names must cite at least one of
                       the staged entry's source URLs, on its `source:` header or through a
                       registry id it cites; a URL written as subject matter in its prose is
                       not a source.
  R3 true_ground       each refusal has a mechanical ground: a staged id absent from the
                       registry, or a staged URL already held by a registry row.

Exit codes: 0 every check passes, 1 any check fails, 2 unevaluable input (missing lane
file, staged digest mismatch, exception) or usage error.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import subprocess
import sys

REGISTRY = "corpus/SOURCES.md"
KNOWLEDGE = "corpus/knowledge"
LESSON = "corpus/lessons/round-52.md"
SOURCES_DIR = ".ufo/waves/round-52/sources"
STAGED_IDS = ".ufo/waves/round-52/assimilation/staged-ids"
STAGED_DIR = ".ufo/waves/round-53/exec-quality-gate/staged"
HELD_FIXTURE_ENTRIES = ("field-performance-cwv.md", "pages-base-path.md")
LEAF_FLOOR = 4

GATE_RE = re.compile(r'^- (S\d{3,}) — .*?— § (.+?) — quote: "([^"]+)"')
REFUSAL_RE = re.compile(r"^- `([^`]+\.md)` \(staged, ([^)]*)\) — \*\*refused:")
HELD_RE = re.compile(r"`(?:corpus/knowledge/)?([a-z0-9-]+\.md)`")
URL_RE = re.compile(r"https?://[^\s;,)`\"'<>|]+")
ID_RE = re.compile(r"\bS\d{3,}\b")
DATE_RE = re.compile(r"\d{4}-\d{1,2}-\d{1,2}|\d{4}年\d{1,2}月\d{1,2}日")
HEADING_RES = (
    re.compile(r"<(h[1-6])\b[^>]*>(.*?)</\1\s*>", re.S | re.I),
    re.compile(r'<([a-z][a-z0-9]*)\b[^>]*\bname="h2_article_title\d+"[^>]*>(.*?)</\1\s*>',
               re.S | re.I),
)
PAGE_REV_RE = re.compile(
    r"(最新更新章节|更新日|最終更新日|最后更新|Last updated)\s*[:：]?\s*"
    r"(\d{4}-\d{1,2}-\d{1,2}|\d{4}年\d{1,2}月\d{1,2}日)"
)
NO_REV_RE = re.compile(r"no (?:revision|publication date|date) (?:printed|rendered)", re.I)
SECTION_TS_RE = re.compile(
    r"(?:章节时间戳|section timestamp)\s*(\d{4}-\d{1,2}-\d{1,2}|\d{4}年\d{1,2}月\d{1,2}日)", re.I
)


class Unevaluable(Exception):
    pass


class GitReader:
    def __init__(self, root: str, rev: str) -> None:
        self.root, self.rev = root, rev

    def read(self, path: str) -> bytes | None:
        proc = subprocess.run(
            ["git", "-C", self.root, "show", f"{self.rev}:{path}"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        return proc.stdout if proc.returncode == 0 else None


class DictReader:
    def __init__(self, files: dict[str, bytes]) -> None:
        self.files = files

    def read(self, path: str) -> bytes | None:
        return self.files.get(path)


def need_text(reader, path: str) -> str:
    raw = reader.read(path)
    if raw is None:
        raise Unevaluable(f"{path} absent at the measured revision")
    return raw.decode("utf-8")


def load_staged(staged_dir: str) -> dict[str, str]:
    """Read the staged snapshot; every file must equal its provenance pin."""
    try:
        with open(os.path.join(staged_dir, "provenance.json"), encoding="utf-8") as fh:
            pins = json.load(fh)["files"]
    except (OSError, ValueError, KeyError) as exc:
        raise Unevaluable(f"staged provenance unreadable: {exc}") from exc
    staged: dict[str, str] = {}
    for name, pin in pins.items():
        try:
            with open(os.path.join(staged_dir, name), "rb") as fh:
                raw = fh.read()
        except OSError as exc:
            raise Unevaluable(f"staged {name} unreadable: {exc}") from exc
        digest = hashlib.sha256(raw).hexdigest()
        if digest != pin.get("sha256") or len(raw) != pin.get("bytes"):
            raise Unevaluable(f"staged {name} sha256 {digest} / {len(raw)} B != provenance pin")
        staged[name] = raw.decode("utf-8")
    return staged


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(text).replace("\u3000", " ")).strip()


def parse_registry(text: str) -> dict[str, list[str]]:
    """Parse the registry table the way the census parser does: 0 to 3 leading spaces."""
    rows: dict[str, list[str]] = {}
    in_registry = False
    for line in text.splitlines():
        if line.strip().startswith("## "):
            in_registry = line.strip().lower().startswith("## registry")
            continue
        if not in_registry or not re.match(r"^ {0,3}\|", line):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 2 and re.fullmatch(r"S[0-9]{3,}", cells[0]):
            rows[cells[0]] = cells
    return rows


def urls(text: str) -> set[str]:
    return {u.rstrip(".").rstrip("/") for u in URL_RE.findall(text)}


def section(text: str, heading: str) -> list[str]:
    """Lines of one `## heading` section."""
    out: list[str] = []
    inside = False
    for line in text.splitlines():
        if line.startswith("## "):
            inside = line.strip().lower().startswith(heading.lower())
            continue
        if inside:
            out.append(line)
    return out


def split_locator(loc: str) -> tuple[list[str], str]:
    """Return (§ leaves, trailing parenthetical) of a locator."""
    loc = loc.strip()
    if loc.startswith("§"):
        loc = loc[1:].strip()
    paren = ""
    if loc.endswith(")"):
        depth = 0
        for i in range(len(loc) - 1, -1, -1):
            if loc[i] in ")）":
                depth += 1
            elif loc[i] in "(（":
                depth -= 1
                if depth == 0:
                    paren, loc = loc[i + 1:-1], loc[:i].strip()
                    break
    leaves = [norm(part.split("→")[-1]) for part in loc.split(" / ") if part.strip()]
    return leaves, paren


def headings(raw: str) -> list[tuple[int, str]]:
    found = []
    for pattern in HEADING_RES:
        for m in pattern.finditer(raw):
            found.append((m.start(), norm(re.sub(r"<[^>]+>", " ", m.group(2)))))
    return sorted(found)


def containing(raw: str, quote: str, heads: list[tuple[int, str]]) -> list[tuple[str, int, int]]:
    """(heading text, section start, section end) for every quote occurrence."""
    out = []
    start = raw.find(quote)
    while start != -1:
        before = [h for h in heads if h[0] < start]
        after = [h[0] for h in heads if h[0] > start]
        if before:
            out.append((before[-1][1], before[-1][0], after[0] if after else len(raw)))
        start = raw.find(quote, start + 1)
    return out


def leaf_names(leaves: list[str], heading: str) -> bool:
    return any(len(leaf) >= LEAF_FLOOR and leaf in heading for leaf in leaves)


def refusals(lesson: str) -> list[dict]:
    out: list[dict] = []
    for line in section(lesson, "## refused entries"):
        m = REFUSAL_RE.match(line)
        if m:
            out.append({"name": m.group(1), "claimed": ID_RE.findall(m.group(2)),
                        "text": line})
        elif out and line.startswith("  "):
            out[-1]["text"] += " " + line.strip()
    return out


def staged_sources(body: str) -> list[tuple[str, set[str]]]:
    out = []
    for line in body.splitlines()[:8]:
        m = re.match(r"^source: (S\d{3,})\b(.*)$", line)
        if m:
            out.append((m.group(1), urls(m.group(2))))
    return out


def run_checks(lane, staged: dict[str, str], lesson_path: str = LESSON,
               sources_dir: str = SOURCES_DIR, staged_ids_path: str = STAGED_IDS
               ) -> tuple[int, list[dict]]:
    results: list[dict] = []

    def add(check: str, notes: list[str], facts: dict | None = None) -> None:
        results.append({"check": check, "state": "pass" if not notes else "fail",
                        "notes": notes, "facts": facts or {}})

    try:
        lesson = need_text(lane, lesson_path)
        rows = parse_registry(need_text(lane, REGISTRY))
        gate = []
        for line in section(lesson, "## gate"):
            m = GATE_RE.match(line)
            if m:
                gate.append((m.group(1), m.group(2), m.group(3)))
        if not gate:
            raise Unevaluable(f"no `## Gate` entries parsed from {lesson_path}")

        bodies: dict[str, str] = {}
        sections: dict[str, list[tuple[str, int, int]]] = {}
        for sid, _, quote in gate:
            bodies[sid] = need_text(lane, f"{sources_dir}/{sid}.html")
            sections[sid] = containing(bodies[sid], quote, headings(bodies[sid]))

        def locator_notes(sid: str, leaves: list[str], where: str) -> list[str]:
            found = sections[sid]
            if not found:
                return [f"{sid}: {where} quote does not occur under any heading of the "
                        "retained body"]
            if any(leaf_names(leaves, h) for h, _, _ in found):
                return []
            return [f"{sid}: {where} § leaves {leaves} do not name the heading containing "
                    f"the quote; it sits under {sorted({h for h, _, _ in found})}"]

        def revision_notes(sid: str, paren: str, where: str) -> list[str]:
            raw = bodies[sid]
            notes: list[str] = []
            page = PAGE_REV_RE.search(norm(re.sub(r"<[^>]+>", " ", raw)))
            if NO_REV_RE.search(paren) and page:
                notes.append(f"{sid}: {where} says no revision is printed, but the body "
                             f"prints {page.group(1)} {page.group(2)}")
            for date in SECTION_TS_RE.findall(paren):
                spans = sections[sid]
                if spans and not any(date in raw[s:e] for _, s, e in spans):
                    where_found = (f"page-level marker {page.group(1)}"
                                   if page and page.group(2) == date else
                                   "outside the quote's section" if date in raw else "nowhere")
                    notes.append(f"{sid}: {where} cites {date} as the section timestamp, but "
                                 f"the quote's section does not carry it ({where_found})")
            for date in DATE_RE.findall(paren):
                if date not in raw:
                    notes.append(f"{sid}: {where} cites {date}, which the body does not print")
            return notes

        l1, l2, l3 = [], [], []
        for sid, loc, _ in gate:
            leaves, paren = split_locator(loc)
            l1 += locator_notes(sid, leaves, "Gate")
            l3 += revision_notes(sid, paren, "Gate")
            row = rows.get(sid)
            if row is None or len(row) < 6 or not row[5].startswith("§"):
                l2.append(f"{sid}: registry row has no § anchor cell")
                continue
            a_leaves, a_paren = split_locator(row[5])
            l2 += locator_notes(sid, a_leaves, "registry anchor")
            l3 += revision_notes(sid, a_paren, "registry anchor")
        add("L1_gate_locator", l1, {"gate_entries": [g[0] for g in gate]})
        add("L2_registry_anchor", l2)
        add("L3_revision_notes", l3)

        listed_raw = lane.read(staged_ids_path)
        listed = set(listed_raw.decode("utf-8").split()) if listed_raw is not None else set()
        refused = refusals(lesson)
        if not refused:
            raise Unevaluable(f"no refused entries parsed from {lesson_path}")
        r0, r1, r2, r3 = [], [], [], []
        facts: dict[str, dict] = {}
        for ref in refused:
            name = ref["name"]
            body = staged.get(name)
            if body is None:
                r0.append(f"{name}: staged entry not in the snapshot")
                continue
            src = staged_sources(body)
            ids = [sid for sid, _ in src]
            staged_urls = set().union(*(u for _, u in src)) if src else set()
            missing = [sid for sid in ids if sid not in listed]
            if not ids or missing:
                r0.append(f"{name}: staged source ids {missing or ids} not in {staged_ids_path}")
            if set(ref["claimed"]) != set(ids):
                r1.append(f"{name}: refusal names staged ids {ref['claimed']}, the staged "
                          f"entry's source ids are {ids}")
            for held in sorted(set(HELD_RE.findall(ref["text"])) - {name}):
                held_raw = lane.read(f"{KNOWLEDGE}/{held}")
                if held_raw is None:
                    continue
                held_text = held_raw.decode("utf-8")
                held_urls = set().union(*(urls(line) for line in held_text.splitlines()[:8]
                                          if line.startswith("source:")))
                for hid in set(ID_RE.findall(held_text)):
                    if hid in rows:
                        held_urls |= urls(rows[hid][1])
                if not held_urls & staged_urls:
                    r2.append(f"{name}: names {held} as holding the ground, but {held} cites "
                              f"none of the staged sources {sorted(staged_urls)}")
            grounds = [f"{sid} not in {REGISTRY}" for sid in ids if sid not in rows]
            for url in sorted(staged_urls):
                grounds += [f"{url} held as {rid}" for rid, row in sorted(rows.items())
                            if url in urls(row[1])]
            facts[name] = {"staged_ids": ids, "true_grounds": grounds}
            if not grounds:
                r3.append(f"{name}: no mechanical ground — every staged id is registered and "
                          "no staged URL is held")
        add("R0_staged_snapshot", r0)
        add("R1_refusal_ids", r1)
        add("R2_held_ground", r2)
        add("R3_true_ground", r3, facts)
    except (Unevaluable, UnicodeDecodeError) as exc:
        return 2, results + [{"check": "unevaluable", "state": "unevaluable",
                              "notes": [str(exc)], "facts": {}}]
    except Exception as exc:  # unevaluable evidence is exit 2, never a silent miss
        return 2, results + [{"check": "exception", "state": "unevaluable",
                              "notes": [f"{type(exc).__name__}: {exc}"], "facts": {}}]
    return (0 if all(r["state"] == "pass" for r in results) else 1), results


# --------------------------------------------------------------------------- selftest

CORRECTIONS = {
    LESSON: [
        ("§ 友好抓取 → robots写法 (no revision printed on the page)",
         "§ 友好抓取 → 如何正确识别Baiduspider移动ua (最新更新章节 2019-09-18, page-level)"),
        ("§ 移动适配 → 对应关系错误的常见原因 (章节时间戳 2020-08-14)",
         "§ 移动适配 → 如何提升移动适配效果 (最新更新章节 2020-08-14, page-level)"),
    ],
    REGISTRY: [
        ("§ 友好抓取 → robots写法 / 使用robots巧妙避免蜘蛛黑洞 (no revision printed on the page — "
         "pinned by the quoted clauses and the access date)",
         "§ 友好抓取 → 如何正确识别Baiduspider移动ua / robots写法 / 使用robots巧妙避免蜘蛛黑洞 "
         "(最新更新章节 2019-09-18, page-level)"),
        ("§ 移动适配 → 对应关系错误的常见原因 (章节时间戳 2020-08-14)",
         "§ 移动适配 → 如何提升移动适配效果 (最新更新章节 2020-08-14, page-level)"),
    ],
}
RESTATED_REFUSALS = {
    "crux-keyless-check.md":
        "- `crux-keyless-check.md` (staged, S303/S304) — **refused: sources not in the lane "
        "registry.** Neither S303 nor S304 is a row in `corpus/SOURCES.md` or in this round's "
        "receipts, so the entry cannot be written under CORPUS rule 1. Flip: open S303/S304 "
        "with a retained body and register them.",
    "jekyll-url-baseurl-options.md":
        "- `jekyll-url-baseurl-options.md` (staged, S296) — **refused: duplicate URL.** S296 "
        "cites https://jekyllrb.com/docs/configuration/options/, held as S080; a second row "
        "for that URL is an E04 duplicate. Flip: supersede S080 in place.",
}


def replace_bullet(lesson: str, name: str, new: str) -> str:
    lines = lesson.split("\n")
    start = next(i for i, line in enumerate(lines) if line.startswith(f"- `{name}` "))
    end = start + 1
    while end < len(lines) and lines[end].startswith("  "):
        end += 1
    return "\n".join(lines[:start] + [new] + lines[end:])


def selftest(root: str, rev: str, staged_dir: str) -> int:
    lane = GitReader(root, rev)
    paths = [LESSON, REGISTRY, STAGED_IDS,
             *(f"{KNOWLEDGE}/{held}" for held in HELD_FIXTURE_ENTRIES),
             *(f"{SOURCES_DIR}/{sid}.html" for sid in ("S374", "S329", "S312"))]
    base: dict[str, str] = {}
    for path in paths:
        raw = lane.read(path)
        if raw is None:
            print(f"selftest: missing round-52 input {path} at {rev}", file=sys.stderr)
            return 2
        base[path] = raw.decode("utf-8")
    try:
        staged = load_staged(staged_dir)
    except Unevaluable as exc:
        print(f"selftest: {exc}", file=sys.stderr)
        return 2

    corrected = dict(base)
    for path, pairs in CORRECTIONS.items():
        for old, new in pairs:
            if old not in corrected[path]:
                print(f"selftest: correction anchor absent from {path}: {old[:30]}",
                      file=sys.stderr)
                return 2
            corrected[path] = corrected[path].replace(old, new)
    for name, text in RESTATED_REFUSALS.items():
        corrected[LESSON] = replace_bullet(corrected[LESSON], name, text)

    def mutate(files: dict[str, str], path: str, old: str, new: str) -> dict[str, str]:
        out = dict(files)
        if old not in out[path]:
            raise KeyError(f"{path}: {old[:40]}")
        out[path] = out[path].replace(old, new, 1)
        return out

    gate_s329 = "§ 友好抓取 → 如何正确识别Baiduspider移动ua (最新更新章节 2019-09-18, page-level)"
    gate_s312 = "§ 移动适配 → 如何提升移动适配效果 (最新更新章节 2020-08-14, page-level)"
    anchor_s329 = CORRECTIONS[REGISTRY][0][1]
    s303_row = next(l for l in base[REGISTRY].split("\n") if l.startswith("| S374 |"))
    fpc = f"{KNOWLEDGE}/field-performance-cwv.md"
    held_claim = RESTATED_REFUSALS["crux-keyless-check.md"] + (
        " The lane's `field-performance-cwv.md` already carries the eligibility question.")

    # name -> (lane files, staged, expected exit, expected failing check -> note keys)
    fixtures: dict[str, tuple[dict[str, str], dict[str, str], int, dict[str, list[str]]]] = {
        "pass_corrected": (corrected, staged, 0, {}),
        "round52_as_committed": (base, staged, 1, {
            "L1_gate_locator": ["S312", "S329"],
            "L2_registry_anchor": ["S312", "S329"],
            "L3_revision_notes": ["S312", "S312", "S329", "S329"],
            "R1_refusal_ids": ["jekyll-url-baseurl-options.md"],
            "R2_held_ground": ["crux-keyless-check.md", "jekyll-url-baseurl-options.md"],
        }),
        "fail_gate_locator_s329": (mutate(corrected, LESSON, gate_s329,
            "§ 友好抓取 → robots写法 (最新更新章节 2019-09-18, page-level)"), staged, 1,
            {"L1_gate_locator": ["S329"]}),
        "fail_gate_locator_s312": (mutate(corrected, LESSON, gate_s312,
            "§ 移动适配 → 对应关系错误的常见原因 (最新更新章节 2020-08-14, page-level)"), staged, 1,
            {"L1_gate_locator": ["S312"]}),
        "fail_leaf_below_floor": (mutate(corrected, LESSON, gate_s312,
            "§ 移动适配 → 适配 (最新更新章节 2020-08-14, page-level)"), staged, 1,
            {"L1_gate_locator": ["S312"]}),
        "fail_anchor_s329": (mutate(corrected, REGISTRY, anchor_s329,
            "§ 友好抓取 → robots写法 / 使用robots巧妙避免蜘蛛黑洞 (最新更新章节 2019-09-18, page-level)"),
            staged, 1, {"L2_registry_anchor": ["S329"]}),
        "fail_no_revision_claim": (mutate(corrected, LESSON, gate_s329,
            "§ 友好抓取 → 如何正确识别Baiduspider移动ua (no revision printed on the page)"), staged, 1,
            {"L3_revision_notes": ["S329"]}),
        "fail_section_timestamp": (mutate(corrected, LESSON, gate_s312,
            "§ 移动适配 → 如何提升移动适配效果 (章节时间戳 2020-08-14)"), staged, 1,
            {"L3_revision_notes": ["S312"]}),
        "fail_date_not_printed": (mutate(corrected, LESSON, "(更新日 2010年11月24日) — quote",
            "(更新日 2011年11月24日) — quote"), staged, 1, {"L3_revision_notes": ["S374"]}),
        "fail_quote_absent": (mutate(corrected, f"{SOURCES_DIR}/S312.html",
            "手机页使用了ajax等异步加载的方法加载内容主体", "手机页使用了脚本加载内容主体"), staged, 1,
            {"L1_gate_locator": ["S312"], "L2_registry_anchor": ["S312"]}),
        "fail_refusal_ids": (mutate(corrected, LESSON, "(staged, S296)", "(staged, S041/S042)"),
            staged, 1, {"R1_refusal_ids": ["jekyll-url-baseurl-options.md"]}),
        "fail_held_ground": (mutate(corrected, LESSON,
            RESTATED_REFUSALS["crux-keyless-check.md"], held_claim), staged, 1,
            {"R2_held_ground": ["crux-keyless-check.md"]}),
        "pass_held_ground_shared_source": (mutate(mutate(corrected, LESSON,
            RESTATED_REFUSALS["crux-keyless-check.md"], held_claim), fpc,
            "https://web.dev/articles/vitals;",
            "https://web.dev/articles/vitals; https://developer.chrome.com/docs/crux/vis;"),
            staged, 0, {}),
        "fail_no_true_ground": (mutate(corrected, REGISTRY, s303_row + "\n", s303_row + "\n"
            + s303_row.replace("| S374 |", "| S303 |", 1) + "\n"
            + s303_row.replace("| S374 |", "| S304 |", 1) + "\n"), staged, 1,
            {"R3_true_ground": ["crux-keyless-check.md"]}),
        "fail_snapshot_foreign_id": (mutate(corrected, STAGED_IDS, "S296\n", ""), staged, 1,
            {"R0_staged_snapshot": ["jekyll-url-baseurl-options.md"]}),
        "fail_staged_missing": (corrected, {k: v for k, v in staged.items()
            if k != "crux-keyless-check.md"}, 1,
            {"R0_staged_snapshot": ["crux-keyless-check.md"]}),
        "unevaluable_lesson_absent": ({k: v for k, v in corrected.items() if k != LESSON},
            staged, 2, {}),
    }

    passed = 0
    lines: list[str] = []
    for name in sorted(fixtures):
        files, fixture_staged, expected, expected_fail = fixtures[name]
        reader = DictReader({k: v.encode("utf-8") for k, v in files.items()})
        code, results = run_checks(reader, fixture_staged)
        actual = {r["check"]: sorted(n.split(":")[0] for n in r["notes"])
                  for r in results if r["state"] == "fail"}
        ok = code == expected and (expected == 2 or actual == expected_fail)
        passed += ok
        lines.append(f"  {'ok  ' if ok else 'FAIL'} {name}: exit {code} (expected {expected})"
                     + ("" if ok else f"; failing {actual}, expected {expected_fail}"))
    digest = hashlib.sha256("".join(f"{p}\0{base[p]}\0" for p in sorted(base)).encode()
                            + "".join(f"{k}\0{v}\0" for k, v in sorted(staged.items())).encode()
                            ).hexdigest()
    print(f"c53 gate-truth selftest: {passed}/{len(fixtures)} (input digest {digest[:16]}, "
          f"{len(base)} lane files + {len(staged)} staged)")
    print("\n".join(lines))
    return 0 if passed == len(fixtures) else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Round-53 gate-truth counter")
    parser.add_argument("--root", default=".")
    parser.add_argument("--revision", default=None)
    parser.add_argument("--staged-dir", default=None)
    parser.add_argument("--lesson", default=LESSON)
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    staged_dir = args.staged_dir or os.path.join(args.root, STAGED_DIR)
    if args.selftest:
        return selftest(args.root, args.revision or "HEAD", staged_dir)
    if not args.revision:
        parser.error("--revision is required unless --selftest is used")
    try:
        staged = load_staged(staged_dir)
    except Unevaluable as exc:
        print(f"unevaluable: {exc}\nEXIT=2")
        return 2
    code, results = run_checks(GitReader(args.root, args.revision), staged, args.lesson)
    passed = sum(1 for r in results if r["state"] == "pass")
    if args.json:
        print(json.dumps({
            "schema": "kake-r53-gate-truth-v1",
            "revision": args.revision,
            "lesson": args.lesson,
            "checks": {r["check"]: {k: r[k] for k in ("state", "notes", "facts")}
                       for r in results},
            "checks_passed": passed,
            "met": code == 0,
        }, indent=1, ensure_ascii=False))
    else:
        print(f"gate-truth {passed}/{len(results)} met={code == 0}")
        for r in results:
            print(f"  {r['check']} {r['state'].upper()}")
            for note in r["notes"]:
                print(f"    - {note}")
            for key, value in r["facts"].items():
                print(f"    = {key}: {json.dumps(value, ensure_ascii=False)}")
        print(f"  revision: {args.revision}")
    print(f"EXIT={code}")
    return code


if __name__ == "__main__":
    sys.exit(main())
