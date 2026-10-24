#!/usr/bin/env python3
"""Replay the round-23 receipt sets against one Git revision.

Usage:
  receipt_replay.py c1|c2 --root LANE --revision REV [--json]
  receipt_replay.py --selftest

c1 replays the round-23 unit receipts (measure_c1.py semantics); c2 replays the
round-23 live captures (measure_c2.py semantics). Both read the digest-pinned frozen
populations, the BASE commit, the heading, the ROUND paths and the validator at REV
exactly as the round-23 runners do. Those runners stay byte-intact as evidence.

Hardening; every rejection is a named problem:
  * REV must not start with "-" and must resolve via
    `git rev-parse --verify --end-of-options REV^{commit}`, else exit 2;
  * observedAt (c1: RFC 3339 full-date or date-time) and fetchedAt (c2: date-time) must
    be RFC 3339 section 5.6 values with real calendar and clock fields, written on or
    after 2026-10-21, and not later than REV's committer timestamp (a full-date must not
    be later than the committer's UTC date);
  * contentType is null (no header, not served) or a string parsed as an RFC 9110
    media type; other values are named problems, never string-method crashes;
  * status must be an integer and not a bool; every JSON field read is type-checked;
  * JSON must be strict RFC 8259 text: UTF-8 without a byte order mark, finite numbers,
    unique member names, bounded nesting and bounded integer length.

Exit 0 iff every unit or surface is accepted; 1 iff at least one is rejected, with named
problems; 2 when REV, a frozen population, BASE or the validator cannot be read, on usage
errors, and on any unforeseen internal error (one line on stderr, never a traceback).
"""
from __future__ import annotations

import argparse
import codecs
import contextlib
import datetime as dt
import hashlib
import io
import json
import math
import os
import random
import re
import subprocess
import sys
import tempfile
from collections import Counter
from fractions import Fraction
from typing import Callable, NamedTuple
from urllib.parse import urlsplit

ROUND = ".ufo/waves/round-23"
BASE = "b5d599e19bead54b96f589444e9ec64cdf67c28a"
HEADING = "## Live re-verification \u2014 round 23"
C1_POPULATION_SHA256 = "ffc9b3a44ee84ed827f3badc697f0ae5c8be007a50de3cafc2ccd23617697daf"
C2_POPULATION_SHA256 = "ac58c80fda73cae194fcc75bf56f62b19ea5443048ddf822fcee8d08e7c75d98"
VALIDATOR = "scripts/canonical_audit.py"
FLOOR = dt.date(2026, 10, 21)
EPOCH = dt.datetime(1970, 1, 1)
VERDICTS = ("HOLD", "STALE", "UNVERIFIABLE")
C1_FIELDS = ("id", "anchor", "claim", "surface", "method", "observation", "verdict")
FETCH_FIELDS = ("url", "method", "fetchedAt", "status", "contentType", "error",
                "truncated", "redirects", "finalUrl", "sha256", "bytes")
REDIRECT_STATUSES = frozenset({301, 302, 303, 307, 308})
MAX_REDIRECTS = 5
VALIDATOR_TIMEOUT_SECONDS = 60


class Unreadable(Exception):
    """An input the replay cannot read at all: exit 2."""


class Malformed(ValueError):
    """A value is malformed; str(exc) is the named problem."""


class Stamp(NamedTuple):
    day: dt.date              # calendar date as written
    instant: Fraction | None  # exact seconds since the epoch in UTC; None for a full-date


def show(value: object) -> str:
    """Bounded ASCII rendering of an untrusted value for a problem message."""
    text = ascii(value)
    return text if len(text) <= 60 else text[:57] + "..."


def one_line(exc: BaseException) -> str:
    text = " ".join(str(exc).split())
    return text.encode("ascii", "backslashreplace").decode("ascii")[:300]


# --- strict JSON -----------------------------------------------------------------

def _reject_constant(name: str) -> object:
    raise ValueError(f"non-standard constant {name}")


def _finite(text: str) -> float:
    number = float(text)
    if not math.isfinite(number):
        raise ValueError("number is outside the finite double range")
    return number


def _unique_members(pairs: list[tuple[str, object]]) -> dict[str, object]:
    members: dict[str, object] = {}
    for name, value in pairs:
        if name in members:
            raise ValueError(f"duplicate member name {show(name)}")
        members[name] = value
    return members


def parse_json(raw: bytes) -> object:
    """Parse strict RFC 8259 text; raise Malformed with the named problem otherwise."""
    if raw.startswith(codecs.BOM_UTF8):
        raise Malformed("starts with a UTF-8 byte order mark")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise Malformed(f"is not UTF-8 (byte {exc.start}: {exc.reason})") from None
    try:
        return json.loads(text, object_pairs_hook=_unique_members, parse_float=_finite,
                          parse_constant=_reject_constant)
    except RecursionError:
        raise Malformed("nests too deeply") from None
    except ValueError as exc:
        raise Malformed(f"is not valid JSON ({one_line(exc)})") from None


def same_json(left: object, right: object) -> bool:
    """Exact JSON equality: a bool is not an int, and an int is not a float."""
    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        return left.keys() == right.keys() and all(same_json(left[k], right[k]) for k in left)
    if isinstance(left, list):
        return len(left) == len(right) and all(same_json(a, b) for a, b in zip(left, right))
    return left == right


# --- RFC 3339 timestamps ---------------------------------------------------------

_FULL_DATE = re.compile(r"([0-9]{4})-([0-9]{2})-([0-9]{2})")
_DATE_TIME = re.compile(
    r"([0-9]{4})-([0-9]{2})-([0-9]{2})[Tt]([0-9]{2}):([0-9]{2}):([0-9]{2})"
    r"(?:\.([0-9]+))?([Zz]|[+-][0-9]{2}:[0-9]{2})")


def _calendar_day(match: re.Match[str]) -> dt.date:
    try:
        return dt.date(int(match.group(1)), int(match.group(2)), int(match.group(3)))
    except ValueError as exc:
        raise Malformed(f"is not a real calendar date ({exc})") from None


def parse_rfc3339(value: object, *, allow_full_date: bool) -> Stamp:
    """RFC 3339 section 5.6: a full-date, or a date-time with a numeric or Z offset."""
    if type(value) is not str:
        raise Malformed(f"is not a string ({type(value).__name__})")
    full = _FULL_DATE.fullmatch(value)
    if full is not None:
        if not allow_full_date:
            raise Malformed("must be a date-time with an offset, not a full-date")
        return Stamp(_calendar_day(full), None)
    match = _DATE_TIME.fullmatch(value)
    if match is None:
        raise Malformed(f"is not RFC 3339 (date-time needs T and a Z or +-HH:MM offset): {show(value)}")
    year, month, day, hour, minute, second = (int(match.group(index)) for index in range(1, 7))
    try:
        local = dt.datetime(year, month, day, hour, minute, second)
    except ValueError as exc:
        raise Malformed(f"is not a real date-time ({exc})") from None
    zone = match.group(8)
    offset = 0
    if zone not in ("Z", "z"):
        hours, minutes = int(zone[1:3]), int(zone[4:6])
        if hours > 23 or minutes > 59:
            raise Malformed(f"has an offset out of range: {zone}")
        offset = (hours * 60 + minutes) * 60 * (-1 if zone[0] == "-" else 1)
    digits = match.group(7)
    fraction = Fraction(int(digits), 10 ** len(digits)) if digits else Fraction(0)
    whole = (local - EPOCH) // dt.timedelta(seconds=1)
    return Stamp(local.date(), whole - offset + fraction)


def utc_day(stamp: Stamp) -> dt.date:
    return (EPOCH + dt.timedelta(seconds=int(stamp.instant))).date()


def check_timestamp(value: object, name: str, *, allow_full_date: bool, committed: Stamp) -> list[str]:
    """Named problems for a timestamp: well-formed, on/after 2026-10-21, not after the commit."""
    try:
        stamp = parse_rfc3339(value, allow_full_date=allow_full_date)
    except Malformed as exc:
        return [f"{name} {exc}"]
    if (stamp.day < FLOOR if stamp.instant is None
            else stamp.instant < (dt.datetime.combine(FLOOR, dt.time()) - EPOCH) // dt.timedelta(seconds=1)):
        return [f"{name} is before 2026-10-21"]
    if stamp.instant is None:
        if stamp.day > utc_day(committed):
            return [f"{name} is later than the revision's committer date"]
    elif stamp.instant > committed.instant:
        return [f"{name} is later than the revision's committer timestamp"]
    return []


# --- RFC 9110 media types --------------------------------------------------------

_TCHAR = r"[!#$%&'*+\-.^_`|~0-9A-Za-z]"
_TOKEN = _TCHAR + "+"
_QUOTED = r'"(?:[\t \x21\x23-\x5b\x5d-\x7e\x80-\xff]|\\[\t \x21-\x7e\x80-\xff])*"'
_PARAMETER = _TOKEN + "=(?:" + _TOKEN + "|" + _QUOTED + ")"
# media-type = type "/" subtype parameters, with parameters = *( OWS ";" OWS [ parameter ] ).
_MEDIA_TYPE = re.compile(r"(" + _TOKEN + r")/(" + _TOKEN + r")((?:[ \t]*;(?:[ \t]*" + _PARAMETER + r")?)*)")


def parse_media_type(value: object) -> tuple[str, str]:
    """Return the lowercased (type, subtype) of an RFC 9110 media type, or raise Malformed."""
    if type(value) is not str:
        raise Malformed(f"is not a string ({type(value).__name__})")
    match = _MEDIA_TYPE.fullmatch(value.strip(" \t"))
    if match is None:
        raise Malformed(f"is not an RFC 9110 media type: {show(value)}")
    return match.group(1).lower(), match.group(2).lower()


# --- revision and blob access ----------------------------------------------------

class GitStore:
    """Blob reads at a revision. `cat-file blob` returns blobs only, never trees."""

    def __init__(self, root: str) -> None:
        self.root = root

    def git(self, *args: str) -> subprocess.CompletedProcess[bytes]:
        env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
        return subprocess.run(["git", "-c", "core.hooksPath=/dev/null", "-C", self.root, *args],
                              env=env, capture_output=True, check=False, timeout=30)

    def read(self, rev: str, path: str) -> bytes | None:
        done = self.git("cat-file", "blob", f"{rev}:{path}")
        return done.stdout if done.returncode == 0 else None

    def commit_exists(self, rev: str) -> bool:
        return self.git("cat-file", "-e", f"{rev}^{{commit}}").returncode == 0


def resolve_revision(store: GitStore, revision: str) -> tuple[str, str, Stamp]:
    """Return (full SHA, committer timestamp as written, committer Stamp) or raise Unreadable."""
    if not revision or revision.startswith("-"):
        raise Unreadable(f"revision {show(revision)} must be non-empty and must not start with '-'")
    done = store.git("rev-parse", "--verify", "--end-of-options", f"{revision}^{{commit}}")
    if done.returncode != 0:
        raise Unreadable(f"revision {show(revision)} does not resolve to a commit in the lane repository")
    sha = done.stdout.decode("ascii").strip()
    shown = store.git("show", "-s", "--format=%cI", sha)
    if shown.returncode != 0:
        raise Unreadable(f"committer timestamp of {sha} is unreadable")
    text = shown.stdout.decode("ascii").strip()
    try:
        committed = parse_rfc3339(text, allow_full_date=False)
    except Malformed as exc:
        raise Unreadable(f"committer timestamp {show(text)} {exc}") from None
    return sha, text, committed


def frozen_population(store: GitStore, rev: str, path: str, digest: str) -> object:
    raw = store.read(rev, path)
    if raw is None or hashlib.sha256(raw).hexdigest() != digest:
        raise Unreadable(f"frozen population {path} is missing or differs from its pinned digest")
    try:
        return parse_json(raw)
    except Malformed as exc:
        raise Unreadable(f"frozen population {path} {exc}") from None


def population_rows(population: object, key: str, fields: tuple[str, ...], path: str) -> list[dict]:
    rows = population.get(key) if isinstance(population, dict) else None
    if not isinstance(rows, list) or not rows or not all(
            isinstance(row, dict) and all(type(row.get(name)) is str for name in fields) for row in rows):
        raise Unreadable(f"frozen population {path} has no valid {key} list")
    return rows


# --- C1: unit receipts -----------------------------------------------------------

def check_unit(store, rev: str, unit: dict, committed: Stamp) -> tuple[list[str], dict[str, int]]:
    tally = {name: 0 for name in VERDICTS}
    raw = store.read(rev, f"{ROUND}/receipts/{unit['unit']}.json")
    if raw is None:
        return ["receipt missing"], tally
    try:
        receipt = parse_json(raw)
    except Malformed as exc:
        return [f"receipt {exc}"], tally
    if not isinstance(receipt, dict):
        return ["receipt is not a JSON object"], tally
    problems: list[str] = []
    if receipt.get("unit") != unit["unit"] or receipt.get("path") != unit["path"]:
        problems.append("unit/path mismatch")
    problems += check_timestamp(receipt.get("observedAt"), "observedAt",
                                allow_full_date=True, committed=committed)
    claims = receipt.get("claims")
    if type(claims) is not list or not claims:
        return problems + ["claims is not a non-empty list"], tally
    base_text = ""
    base_raw = store.read(BASE, unit["path"])
    if base_raw is not None:
        try:
            base_text = base_raw.decode("utf-8")
        except UnicodeDecodeError:
            problems.append("unit file at BASE is not UTF-8")
    current_raw = store.read(rev, unit["path"])
    if current_raw is None:
        return problems + ["unit file missing at revision"], tally
    try:
        current = current_raw.decode("utf-8")
    except UnicodeDecodeError:
        return problems + ["unit file at revision is not UTF-8"], tally
    position = current.find(HEADING)
    section = current[position:] if position >= 0 else ""
    if position < 0:
        problems.append("round-23 heading missing in unit file")
    seen: set[str] = set()
    for index, claim in enumerate(claims):
        if not isinstance(claim, dict):
            problems.append(f"claim {index} is not a JSON object")
            continue
        missing = [name for name in C1_FIELDS
                   if type(claim.get(name)) is not str or not claim[name].strip()]
        if missing:
            problems.append(f"claim {index}: {', '.join(missing)} missing or not a non-empty string")
            continue
        claim_id, verdict = claim["id"], claim["verdict"]
        if claim_id in seen:
            problems.append(f"claim {show(claim_id)}: duplicate id")
        seen.add(claim_id)
        if verdict not in VERDICTS:
            problems.append(f"claim {show(claim_id)}: verdict {show(verdict)} is not HOLD, STALE or UNVERIFIABLE")
            continue
        tally[verdict] += 1
        if claim["anchor"] not in base_text:
            problems.append(f"claim {show(claim_id)}: anchor not in unit at base")
        if f"[{unit['unit']}:{claim_id}]" not in section:
            problems.append(f"claim {show(claim_id)}: not cited in round-23 section")
        if verdict == "STALE":
            correction = claim.get("correction")
            if type(correction) is not str or not correction.strip():
                problems.append(f"claim {show(claim_id)}: STALE without correction")
            elif correction not in section:
                problems.append(f"claim {show(claim_id)}: correction not in round-23 section")
        if verdict == "UNVERIFIABLE":
            reason = claim.get("reason")
            if type(reason) is not str or not reason.strip():
                problems.append(f"claim {show(claim_id)}: UNVERIFIABLE without reason")
    if tally["HOLD"] + tally["STALE"] == 0:
        problems.append("no claim decided live (all UNVERIFIABLE)")
    return problems, tally


def run_c1(store, rev: str, committed: Stamp) -> dict[str, object]:
    if not store.commit_exists(BASE):
        raise Unreadable(f"frozen BASE commit {BASE} is not in the lane repository")
    population = frozen_population(store, rev, f"{ROUND}/c1-population.json", C1_POPULATION_SHA256)
    units = population_rows(population, "units", ("unit", "path"), "c1-population.json")
    rows = []
    totals = {name: 0 for name in VERDICTS}
    for unit in units:
        problems, tally = check_unit(store, rev, unit, committed)
        for name, count in tally.items():
            totals[name] += count
        rows.append({"unit": unit["unit"], "pass": not problems, "claims": tally, "problems": problems})
    return {"mode": "c1", "accepted": sum(row["pass"] for row in rows), "total": len(rows),
            "claimVerdicts": totals, "units": rows}


# --- C2: live captures -----------------------------------------------------------

def safe_http_url(value: object) -> bool:
    if type(value) is not str or any(ord(c) <= 32 or ord(c) == 127 for c in value):
        return False
    try:
        parts = urlsplit(value)
        return (parts.scheme in {"http", "https"} and bool(parts.hostname)
                and parts.username is None and parts.password is None)
    except ValueError:
        return False


def validate_fetch(fetch: dict, surface: dict, committed: Stamp) -> tuple[list[str], bool]:
    """Named problems for a fetch record, and whether it is a served 2xx text/html response."""
    problems: list[str] = []
    absent = [name for name in FETCH_FIELDS if name not in fetch]
    problems += [f"fetch.{name} is absent" for name in absent]
    if fetch.get("url") != surface["url"] or fetch.get("method") != "GET":
        problems.append("fetch url/method does not match population GET")
    if "fetchedAt" not in absent:
        problems += check_timestamp(fetch["fetchedAt"], "fetch.fetchedAt",
                                    allow_full_date=False, committed=committed)
    status = fetch.get("status")
    if "status" not in absent and (type(status) is not int or not 100 <= status <= 599):
        problems.append(f"fetch.status {show(status)} is not an integer HTTP status")
    if "error" not in absent and fetch["error"] is not None:
        problems.append("fetch.error records a failure")
    if "truncated" not in absent and type(fetch["truncated"]) is not bool:
        problems.append("fetch.truncated is not a boolean")
    media = None
    if "contentType" not in absent and fetch["contentType"] is not None:
        try:
            media = parse_media_type(fetch["contentType"])
        except Malformed as exc:
            problems.append(f"fetch.contentType {exc}")
    previous = fetch.get("url")
    if "redirects" not in absent:
        chain = fetch["redirects"]
        if type(chain) is not list or len(chain) > MAX_REDIRECTS:
            problems.append(f"fetch.redirects is not a list of at most {MAX_REDIRECTS} hops")
        else:
            for hop in chain:
                hop_status = hop.get("status") if isinstance(hop, dict) else None
                if (not isinstance(hop, dict) or hop.get("from") != previous
                        or type(hop_status) is not int or hop_status not in REDIRECT_STATUSES
                        or not safe_http_url(hop.get("to"))):
                    problems.append("fetch.redirects chain is inconsistent")
                    break
                previous = hop["to"]
    if "finalUrl" not in absent and (type(fetch["finalUrl"]) is not str or fetch["finalUrl"] != previous):
        problems.append("fetch.finalUrl differs from the redirect chain's final URL")
    if not safe_http_url(fetch.get("finalUrl")):
        problems.append("fetch.finalUrl is not a safe absolute HTTP URL")
    if "sha256" not in absent and type(fetch["sha256"]) is not str:
        problems.append("fetch.sha256 is not a string")
    if "bytes" not in absent and (type(fetch["bytes"]) is not int or fetch["bytes"] < 0):
        problems.append(f"fetch.bytes {show(fetch['bytes'])} is not a non-negative integer")
    served = (type(status) is int and 200 <= status < 300 and status not in {204, 205}
              and fetch.get("error") is None
              and fetch.get("truncated") is False and media == ("text", "html"))
    return problems, served


def judge_surface(surface: dict, fetch: dict, audit: dict, page: bytes | None,
                  committed: Stamp, reproduce: Callable) -> tuple[list[str], str | None]:
    problems, served = validate_fetch(fetch, surface, committed)
    if not served:
        if page is not None:
            problems.append("page.html is stored for a response that is not served")
        expected = {"verdict": "not-served", "status": fetch.get("status"), "exit": None, "error": None}
        if not same_json(audit, expected):
            problems.append("audit.json is not the not-served receipt for this fetch")
        return problems, "not-served"
    if page is None:
        return problems + ["page.html is missing for a served response"], None
    if hashlib.sha256(page).hexdigest() != fetch.get("sha256"):
        return problems + ["page.html digest differs from fetch.sha256"], None
    if len(page) != fetch.get("bytes"):
        problems.append("page.html length differs from fetch.bytes")
    final_url = fetch.get("finalUrl")
    if type(final_url) is not str:
        return problems + ["fetch.finalUrl is not a string"], None
    actual, failure = reproduce(final_url, page, surface["expectedCanonical"])
    if failure is not None:
        return problems + [failure], None
    if not same_json(audit, actual):
        problems.append("audit.json differs from the receipt the validator reproduces at this revision")
    result = actual["result"]
    verdict = result.get("verdict") if isinstance(result, dict) else None
    if type(verdict) is not str:
        return problems + ["validator result has no string verdict"], None
    return problems, verdict


def check_surface(store, rev: str, surface: dict, committed: Stamp,
                  reproduce: Callable) -> tuple[list[str], str | None]:
    prefix = f"{ROUND}/live/{surface['id']}"
    raw_fetch = store.read(rev, f"{prefix}/fetch.json")
    raw_audit = store.read(rev, f"{prefix}/audit.json")
    if raw_fetch is None or raw_audit is None:
        return ["fetch.json or audit.json is missing"], None
    problems: list[str] = []
    documents: list[object] = []
    for name, raw in (("fetch.json", raw_fetch), ("audit.json", raw_audit)):
        try:
            documents.append(parse_json(raw))
        except Malformed as exc:
            problems.append(f"{name} {exc}")
    if problems:
        return problems, None
    fetch, audit = documents
    if not isinstance(fetch, dict) or not isinstance(audit, dict):
        return ["fetch.json and audit.json must be JSON objects"], None
    found, verdict = judge_surface(surface, fetch, audit, store.read(rev, f"{prefix}/page.html"),
                                   committed, reproduce)
    return problems + found, verdict


def make_reproducer(validator: bytes) -> Callable[[str, bytes, str], tuple[dict | None, str | None]]:
    """Re-run the revision's validator on a fresh one-page manifest, as measure_c2 does."""

    def reproduce(final_url: str, page: bytes, expected: str) -> tuple[dict | None, str | None]:
        with tempfile.TemporaryDirectory(prefix="receipt-replay-c2-") as tmp:
            script = os.path.join(tmp, "canonical_audit.py")
            site = os.path.join(tmp, "s")
            os.mkdir(site)
            manifest = os.path.join(site, "manifest.json")
            with open(script, "wb") as handle:
                handle.write(validator)
            with open(os.path.join(site, "page.html"), "wb") as handle:
                handle.write(page)
            with open(manifest, "w", encoding="utf-8") as handle:
                json.dump({"version": 1, "pages": [{"url": final_url, "file": "page.html",
                                                    "expectedCanonical": expected}]}, handle)
            try:
                done = subprocess.run([sys.executable, "-B", script, "--manifest", manifest, "--json"],
                                      cwd=site, capture_output=True,
                                      timeout=VALIDATOR_TIMEOUT_SECONDS, check=False)
            except (OSError, subprocess.TimeoutExpired) as exc:
                return None, f"validator could not complete ({type(exc).__name__})"
        try:
            result = parse_json(done.stdout)
        except Malformed as exc:
            return None, f"validator output {exc}"
        return {"exit": done.returncode, "result": result}, None

    return reproduce


def run_c2(store, rev: str, committed: Stamp) -> dict[str, object]:
    population = frozen_population(store, rev, f"{ROUND}/c2-population.json", C2_POPULATION_SHA256)
    surfaces = population_rows(population, "surfaces", ("id", "url", "expectedCanonical"),
                               "c2-population.json")
    validator = store.read(rev, VALIDATOR)
    if validator is None:
        raise Unreadable(f"validator {VALIDATOR} is unreadable at the revision")
    reproduce = make_reproducer(validator)
    rows = []
    for surface in surfaces:
        problems, verdict = check_surface(store, rev, surface, committed, reproduce)
        rows.append({"id": surface["id"], "pass": not problems, "verdict": verdict, "problems": problems})
    verdicts = Counter(row["verdict"] for row in rows if row["verdict"] is not None)
    return {"mode": "c2", "validatorSha256": hashlib.sha256(validator).hexdigest(),
            "accepted": sum(row["pass"] for row in rows), "total": len(rows),
            "verdicts": dict(sorted(verdicts.items())), "surfaces": rows}


# --- command line ----------------------------------------------------------------

def render(result: dict[str, object]) -> str:
    if result["mode"] == "c1":
        tally = "/".join(f"{name}{result['claimVerdicts'][name]}" for name in VERDICTS)
        rows, label = result["units"], "unit"
    else:
        tally = "/".join(f"{name}{count}" for name, count in result["verdicts"].items()) or "none"
        rows, label = result["surfaces"], "surface"
    lines = [f"{result['mode']} accepted {result['accepted']}/{result['total']} {tally} "
             f"at {result['revision']} committed {result['committerTimestamp']}"]
    for row in rows:
        if not row["pass"]:
            name = row.get("unit", row.get("id"))
            lines.append(f"  REJECT {label} {name}: " + "; ".join(row["problems"]))
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Replay the round-23 receipt sets (c1 unit receipts, c2 live captures) at one Git revision.")
    parser.add_argument("mode", nargs="?", choices=("c1", "c2"), help="receipt set to replay")
    parser.add_argument("--root", help="lane Git repository")
    parser.add_argument("--revision", help="commit to replay; must not start with '-'")
    parser.add_argument("--json", action="store_true", help="print per-unit problems and verdict tallies as JSON")
    parser.add_argument("--selftest", action="store_true", help="run the built-in self-tests and exit")
    return parser


def run(argv: list[str] | None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.selftest:
        if args.mode or args.root or args.revision or args.json:
            parser.error("--selftest takes no other arguments")
        return selftest()
    if args.mode is None or args.root is None or args.revision is None:
        parser.error("expected c1|c2 with --root LANE and --revision REV, or --selftest")
    store = GitStore(args.root)
    revision, committed_text, committed = resolve_revision(store, args.revision)
    if args.mode == "c1":
        result = run_c1(store, revision, committed)
    else:
        result = run_c2(store, revision, committed)
    result.update(revision=revision, committerTimestamp=committed_text)
    if args.json:
        print(json.dumps(result, indent=1, sort_keys=True))
    else:
        print(render(result))
    return 0 if result["accepted"] == result["total"] else 1


def main(argv: list[str] | None = None) -> int:
    try:
        return run(argv)
    except Unreadable as exc:
        print(f"receipt_replay: {one_line(exc)}", file=sys.stderr)
        return 2
    except Exception as exc:  # unforeseen: exit 2 with one line; exit 1 stays a named rejection
        print(f"receipt_replay: internal error: {type(exc).__name__}: {one_line(exc)}", file=sys.stderr)
        return 2


# --- self-tests ------------------------------------------------------------------

class MemoryStore:
    """Revision store with the GitStore read interface, for self-test fixtures."""

    def __init__(self, files: dict[tuple[str, str], bytes], commits: set[str]) -> None:
        self.files = files
        self.commits = commits

    def read(self, rev: str, path: str) -> bytes | None:
        return self.files.get((rev, path))

    def commit_exists(self, rev: str) -> bool:
        return rev in self.commits


def selftest() -> int:
    failures: list[str] = []
    checked = 0

    def expect(name: str, condition: bool) -> None:
        nonlocal checked
        checked += 1
        if not condition:
            failures.append(name)

    def parses(value: object, allow_full_date: bool = True) -> bool:
        try:
            parse_rfc3339(value, allow_full_date=allow_full_date)
            return True
        except Malformed:
            return False

    def json_ok(raw: bytes) -> bool:
        try:
            parse_json(raw)
            return True
        except Malformed:
            return False

    def media(value: object) -> tuple[str, str] | None:
        try:
            return parse_media_type(value)
        except Malformed:
            return None

    committed = parse_rfc3339("2026-10-21T06:00:18-03:00", allow_full_date=False)  # 09:00:18Z
    rng = random.Random(20261021)
    crashes: list[str] = []

    for text in ("2026-10-21", "2026-10-21T09:00:18Z", "2026-10-21t09:00:18z", "2026-10-21T06:00:18-00:00",
                 "2026-10-21T06:00:18.5-03:00", "2026-10-21T06:00:18.123456789-03:00",
                 "2024-02-29T00:00:00Z", "2026-10-21T23:59:59+14:00", "2026-10-21T00:00:00-23:59"):
        expect(f"RFC 3339 accepts {text}", parses(text))
    for text in ("2026-10-21T10:00:00", "2026-10-21 09:00:18Z", "2026-10-21T24:00:00Z", "2026-10-21T09:60:00Z",
                 "2026-10-21T09:00:60Z", "2026-13-01T00:00:00Z", "2026-02-30", "2026-02-29",
                 "2026-10-21T09:00:18+24:00", "2026-10-21T09:00:18+01:60", "2026-10-21T09:00:18Zjunk",
                 "2026-10-21T09:00:18ZZ", "2026-10-21T09:00:18.Z", "2026-10-21T09:00Z", "2026-10-21Z",
                 "\n2026-10-21", "2026-10-21\n", " 2026-10-21", "\uff12\uff10\uff12\uff16-10-21",
                 "0000-01-01", "2026-10-21T09:00:18+0300", "2026-10-21T09:00:18 Z", "", "2026-10-21T9:00:18Z"):
        expect(f"RFC 3339 rejects {text!r}", not parses(text))
    expect("RFC 3339 rejects an integer", not parses(20261021))
    expect("RFC 3339 rejects a full-date where only date-time is allowed",
           not parses("2026-10-21", allow_full_date=False))

    def bound(value: object, allow_full_date: bool = True) -> list[str]:
        return check_timestamp(value, "observedAt", allow_full_date=allow_full_date, committed=committed)

    expect("full-date on the committer day is within bounds", bound("2026-10-21") == [])
    expect("full-date after the committer day is rejected", bound("2026-10-22") != [])
    expect("date before 2026-10-21 is rejected", bound("2026-10-20T23:59:59Z") != [])
    expect("instant equal to the committer timestamp is accepted",
           bound("2026-10-21T06:00:18-03:00", False) == [])
    expect("one nanosecond after the committer timestamp is rejected",
           bound("2026-10-21T06:00:18.000000001-03:00", False) != [])
    expect("date-time with written day 2026-10-21 before the commit is accepted",
           bound("2026-10-21T00:00:00-03:00", False) == [])
    expect("future date-time is rejected", bound("2099-01-01T00:00:00Z", False) != [])
    expect("full-date is rejected for fetchedAt", bound("2026-10-21", False) != [])

    for text in ("text/html", "text/html; charset=utf-8", "TEXT/HTML", " text/html ", "text/html;",
                 "text/html;;charset=utf-8", 'text/html ; charset="utf-8"', "text/html;charset=utf-8;q=0.9"):
        expect(f"media type parses {text!r}", media(text) is not None)
    expect("media type is lowercased", media("TEXT/HTML; charset=UTF-8") == ("text", "html"))
    for value in ("text/html; charset", 'text/html; charset="utf-8', "text/html/extra", "text html", "text/",
                  "/html", "", "   ", "text/html junk", "text/html;charset=utf 8", "text/html\u00a0",
                  "text/html\n", 5, None, ["text/html"], {"type": "text/html"}):
        expect(f"media type rejects {value!r}", media(value) is None)

    for raw in (b'{"a": 1}', b"[]", b'{"n": ' + b"1" * 1000 + b"}", b'{"f": 1.5e3}',
                '{"s": "\u00e9"}'.encode("utf-8")):
        expect(f"strict JSON accepts {raw[:24]!r}", json_ok(raw))
    for raw in (b"\xef\xbb\xbf{}", b'{"a": NaN}', b'{"a": Infinity}', b'{"a": -Infinity}', b'{"a": 1e400}',
                b'{"a": 1, "a": 2}', b'{"a": 1, "a": 1}', b'{"n": ' + b"1" * 5000 + b"}", b"\xff{}",
                b'{"a": 1} x', b"{", b"", "{}".encode("utf-16"), b"[" * 100000 + b"]" * 100000):
        expect(f"strict JSON rejects {raw[:24]!r}", not json_ok(raw))

    tokens = ["{", "}", "[", "]", ":", ",", '"a"', '"claims"', "1", "-", ".", "e", "+", "0", "true",
              "false", "null", "NaN", "Infinity", '"\\u00', "\\", '"', " ", "\n", "\u00e9", "\ufeff", "1" * 30]
    for _ in range(4000):
        text = "".join(rng.choice(tokens) for _ in range(rng.randint(0, 24)))
        raw = text.encode("utf-8") if rng.random() < 0.9 else bytes(rng.getrandbits(8) for _ in range(rng.randint(0, 16)))
        try:
            parse_json(raw)
        except Malformed:
            pass
        except Exception as exc:
            crashes.append(f"parse_json {type(exc).__name__}: {one_line(exc)}")
            break
    media_tokens = ["t", "e", "x", "/", ";", " ", "=", '"', "\\", "\t", "\u00e9", "\u00a0", "h", "m", "l",
                    "\x00", "charset", "utf-8", "1"]
    for _ in range(4000):
        value = "".join(rng.choice(media_tokens) for _ in range(rng.randint(0, 14)))
        try:
            parse_media_type(value)
        except Malformed:
            pass
        except Exception as exc:
            crashes.append(f"parse_media_type {type(exc).__name__}: {one_line(exc)}")
            break
    expect("random JSON and media-type inputs never raise outside Malformed", not crashes)

    surface = {"id": "s", "url": "https://example.test/", "expectedCanonical": "https://example.test/"}
    body = b"<!doctype html><title>selftest</title>"
    good = {"url": surface["url"], "method": "GET", "fetchedAt": "2026-10-21T06:33:03Z", "status": 200,
            "contentType": "text/html; charset=utf-8", "error": None, "truncated": False, "redirects": [],
            "finalUrl": surface["url"], "sha256": hashlib.sha256(body).hexdigest(), "bytes": len(body)}
    problems, served = validate_fetch(good, surface, committed)
    expect("valid served fetch is accepted", problems == [] and served)
    mutations = [None, True, False, 0, -1, 1.5, 404, 2 ** 80, "", "x", "2026-10-21", "text/html", [], [301],
                 {}, {"a": 1}, "\x00", "2026-10-21T06:33:03Z", 301, [{"from": 1}]]
    for key in list(good) + ["extra"]:
        for value in mutations:
            mutated = dict(good)
            mutated[key] = value
            try:
                validate_fetch(mutated, surface, committed)
            except Exception as exc:
                crashes.append(f"validate_fetch {key}={value!r}: {type(exc).__name__}: {one_line(exc)}")
        dropped = dict(good)
        dropped.pop(key, None)
        try:
            validate_fetch(dropped, surface, committed)
        except Exception as exc:
            crashes.append(f"validate_fetch without {key}: {type(exc).__name__}: {one_line(exc)}")
    for hop_key in ("from", "to", "status"):
        for value in mutations:
            hop = {"from": surface["url"], "to": surface["url"], "status": 301}
            hop[hop_key] = value
            try:
                validate_fetch(dict(good, redirects=[hop]), surface, committed)
            except Exception as exc:
                crashes.append(f"redirect hop {hop_key}={value!r}: {type(exc).__name__}: {one_line(exc)}")
    expect("fetch field mutations never raise", not crashes)

    def fetch_with(**changes: object) -> tuple[list[str], bool]:
        return validate_fetch(dict(good, **changes), surface, committed)

    p, s = fetch_with(contentType=5)
    expect("non-string contentType is recorded as a problem and not served", bool(p) and not s)
    p, s = fetch_with(contentType="text/html; charset")
    expect("unparsable contentType is recorded as a problem and not served", bool(p) and not s)
    p, s = fetch_with(status=True)
    expect("bool status is rejected", bool(p) and not s)
    p, s = fetch_with(error="")
    expect("empty-string error is rejected", bool(p))
    p, s = fetch_with(fetchedAt="2026-10-21")
    expect("full-date fetchedAt is rejected", bool(p))
    p, s = fetch_with(bytes=float(len(body)))
    expect("float byte count is rejected", bool(p))
    p, s = fetch_with(truncated="false")
    expect("string truncated is rejected", bool(p))
    p, s = fetch_with(redirects=[{"from": surface["url"], "to": surface["url"], "status": [301]}])
    expect("list redirect status is rejected without a crash", bool(p))

    base_text = "Alpha claim text.\nBeta claim text.\n"
    rev_text = base_text + "\n" + HEADING + "\n\n[u:c1] held. [u:c2] correction text [u:c3] no live source.\n"
    unit_path, receipt_path = "corpus/u.md", f"{ROUND}/receipts/u.json"
    good_receipt = {"unit": "u", "path": unit_path, "observedAt": "2026-10-21", "claims": [
        {"id": "c1", "anchor": "Alpha claim text.", "claim": "a", "surface": "s", "method": "m",
         "observation": "o", "verdict": "HOLD"},
        {"id": "c2", "anchor": "Beta claim text.", "claim": "b", "surface": "s", "method": "m",
         "observation": "o", "verdict": "STALE", "correction": "correction text"},
        {"id": "c3", "anchor": "Alpha claim text.", "claim": "c", "surface": "s", "method": "m",
         "observation": "o", "verdict": "UNVERIFIABLE", "reason": "no live source"}]}

    def unit_with_raw(raw_receipt: bytes) -> tuple[list[str], dict[str, int]]:
        files = {("REV", receipt_path): raw_receipt, ("REV", unit_path): rev_text.encode("utf-8"),
                 (BASE, unit_path): base_text.encode("utf-8")}
        return check_unit(MemoryStore(files, {BASE}), "REV", {"unit": "u", "path": unit_path}, committed)

    def unit_with(**changes: object) -> tuple[list[str], dict[str, int]]:
        return unit_with_raw(json.dumps(dict(good_receipt, **changes)).encode("utf-8"))

    problems, tally = unit_with()
    expect("valid unit receipt is accepted", problems == [] and tally == {"HOLD": 1, "STALE": 1, "UNVERIFIABLE": 1})
    expect("lexical-prefix observedAt is rejected", bool(unit_with(observedAt="2026-10-21T10:00:00")[0]))
    expect("observedAt with trailing text is rejected", bool(unit_with(observedAt="2026-10-21Tjunk")[0]))
    expect("claims that are not a list are rejected", bool(unit_with(claims={})[0]))
    expect("receipt that is not an object is rejected", bool(unit_with_raw(b"[]")[0]))
    expect("receipt with a byte order mark is rejected", bool(unit_with_raw(b"\xef\xbb\xbf" + json.dumps(good_receipt).encode())[0]))
    expect("receipt that is not UTF-8 is rejected", bool(unit_with_raw(b"\xff" + json.dumps(good_receipt).encode())[0]))
    mutated = json.loads(json.dumps(good_receipt))
    mutated["claims"][2]["reason"] = None
    expect("null UNVERIFIABLE reason is rejected", bool(unit_with_raw(json.dumps(mutated).encode())[0]))
    mutated = json.loads(json.dumps(good_receipt))
    mutated["claims"][2]["reason"] = 0
    expect("numeric UNVERIFIABLE reason is rejected", bool(unit_with_raw(json.dumps(mutated).encode())[0]))

    page_files = {("REV", f"{ROUND}/live/s/page.html"): body}

    def fake_reproduce(final_url: str, page: bytes, expected: str) -> tuple[dict | None, str | None]:
        return {"exit": 0, "result": {"findings": [], "pagesChecked": 1, "verdict": "clean"}}, None

    def surface_with(fetch: object, audit: object, page: bool = True) -> tuple[list[str], str | None]:
        files = dict(page_files) if page else {}
        files[("REV", f"{ROUND}/live/s/fetch.json")] = json.dumps(fetch).encode("utf-8")
        files[("REV", f"{ROUND}/live/s/audit.json")] = json.dumps(audit).encode("utf-8")
        return check_surface(MemoryStore(files, {BASE}), "REV", surface, committed, fake_reproduce)

    clean_audit = {"exit": 0, "result": {"findings": [], "pagesChecked": 1, "verdict": "clean"}}
    p, v = surface_with(good, clean_audit)
    expect("served control is accepted with its verdict", p == [] and v == "clean")
    not_served_fetch = dict(good, status=404)
    not_served_audit = {"verdict": "not-served", "status": 404, "exit": None, "error": None}
    p, v = surface_with(not_served_fetch, not_served_audit, page=False)
    expect("not-served control is accepted", p == [] and v == "not-served")
    p, v = surface_with(dict(not_served_fetch, contentType=None), not_served_audit, page=False)
    expect("null contentType without a served page is accepted", p == [] and v == "not-served")
    p, v = surface_with(dict(good, status=204), clean_audit)
    expect("body stored for 204 is rejected", bool(p) and v == "not-served")
    expect("URL control characters are rejected", not safe_http_url("https://example.test/\npath"))
    expect("timestamp lower bound compares UTC instants",
           bool(bound("2026-10-21T00:01:00+02:00", False)))
    p, v = surface_with(dict(good, contentType=5), clean_audit)
    expect("non-string contentType on a served page is rejected without a crash", bool(p) and v == "not-served")
    p, v = surface_with(not_served_fetch, dict(not_served_audit, status=404.0), page=False)
    expect("float status in a not-served receipt is rejected", bool(p))
    p, v = surface_with(good, dict(clean_audit, exit=0.0))
    expect("float exit in a served receipt is rejected", bool(p))
    p, v = surface_with(good, {"exit": 0, "result": {"findings": [], "pagesChecked": 1.0, "verdict": "clean"}})
    expect("float nested count in a served receipt is rejected", bool(p))

    with tempfile.TemporaryDirectory(prefix="receipt-replay-selftest-") as tmp:
        env = dict(os.environ, GIT_AUTHOR_NAME="selftest", GIT_AUTHOR_EMAIL="selftest@example.test",
                   GIT_COMMITTER_NAME="selftest", GIT_COMMITTER_EMAIL="selftest@example.test",
                   GIT_AUTHOR_DATE="2026-10-21T06:00:18-03:00", GIT_COMMITTER_DATE="2026-10-21T06:00:18-03:00")
        subprocess.run(["git", "init", "-q", tmp], check=True, capture_output=True, env=env)
        subprocess.run(["git", "-C", tmp, "-c", "commit.gpgsign=false", "commit", "-q", "--allow-empty",
                        "-m", "selftest"], check=True, capture_output=True, env=env)
        store = GitStore(tmp)
        sha, text, stamp = resolve_revision(store, "HEAD")
        expect("committer timestamp is read from git",
               text == "2026-10-21T06:00:18-03:00" and stamp.instant == parse_rfc3339(
                   "2026-10-21T09:00:18Z", allow_full_date=False).instant)
        for revision in ("-x", "", "no-such-revision", "HEAD^{tree}"):
            try:
                resolve_revision(store, revision)
                expect(f"revision {revision!r} is refused", False)
            except Unreadable:
                expect(f"revision {revision!r} is refused", True)
        for argv in (["c1", "--root", tmp, "--revision=-x"], ["c1", "--root", tmp, "--revision", "no-such"],
                     ["c1", "--root", tmp, "--revision", "HEAD"], ["c2", "--root", tmp, "--revision", "HEAD"],
                     ["c1", "--root", os.path.join(tmp, "missing"), "--revision", "HEAD"]):
            try:
                with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                    code = main(argv)
            except SystemExit as exc:
                code = exc.code
            expect(f"exit 2 for {' '.join(argv)}", code == 2)

    original_run = globals()["run"]

    def failing_run(argv: list[str] | None) -> int:
        raise RuntimeError("boom")

    globals()["run"] = failing_run
    try:
        captured = io.StringIO()
        with contextlib.redirect_stderr(captured):
            code = main(["c1"])
        expect("unforeseen exception exits 2", code == 2)
        expect("unforeseen exception prints one stderr line",
               captured.getvalue() == "receipt_replay: internal error: RuntimeError: boom\n")
    finally:
        globals()["run"] = original_run

    if failures:
        for name in failures:
            print(f"FAIL {name}", file=sys.stderr)
        print(f"receipt_replay selftest: {len(failures)} of {checked} checks failed", file=sys.stderr)
        return 1
    print(f"receipt_replay selftest: {checked} checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
