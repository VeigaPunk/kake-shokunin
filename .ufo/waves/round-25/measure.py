#!/usr/bin/env python3
"""Measure round-25 packet readiness at one immutable Git revision."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from typing import Any

SCHEMA = "kake-accessibility-packet-v1"
EXPECTED = 55
POPULATION = ".ufo/waves/round-25/population.json"
SOURCE = ".ufo/waves/round-25/source-wcag22.html"
CARDS = "corpus/knowledge/accessibility-review-cards.json"
PACKET_TOOL = "scripts/accessibility_packet.py"
POPULATION_SHA256 = "4751dc24db2e3698c2b276bb81bff57412c8fbf6c1c0a62f1aa2ad9e0f903058"
SOURCE_SHA256 = "6e3c5fe397257cae509a2fb4752b73062cf8cbeb92c2cec618989b17e4cf7057"
FIELDS = frozenset({
    "id", "title", "level", "source", "sourceQuote", "publisherCheck",
    "evidenceNeeded", "failureExample", "limitation", "status",
})
PROSE = ("publisherCheck", "evidenceNeeded", "failureExample", "limitation")
REVISION_RE = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})\Z", re.IGNORECASE)


class InputFailure(Exception):
    """An unavailable or invalid measurement input, named by a stable finding."""

    def __init__(self, finding: str):
        self.finding = finding
        super().__init__(finding)


class UsageError(Exception):
    pass


class Parser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise UsageError(message)


def packet_result(verdict: str, accepted: int = 0,
                  criteria: list[dict[str, Any]] | None = None,
                  findings: list[str] | None = None) -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "verdict": verdict,
        "expected": EXPECTED,
        "accepted": accepted,
        "criteria": criteria or [],
        "findings": findings or [],
        "websiteConformance": "not-assessed",
    }


def strict_json(raw: bytes) -> Any:
    def reject_constant(value: str) -> None:
        raise ValueError(f"non-standard JSON constant: {value}")

    def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate JSON object member")
            result[key] = value
        return result

    return json.loads(
        raw.decode("utf-8"),
        parse_constant=reject_constant,
        object_pairs_hook=unique_object,
    )


class GitStore:
    """Read commit objects without consulting user Git configuration."""

    def __init__(self, root: Path):
        self.root = root

    def git(self, *args: str) -> subprocess.CompletedProcess[bytes]:
        env = {key: value for key, value in os.environ.items()
               if not key.startswith("GIT_")}
        env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
        return subprocess.run(
            ["git", "-c", "core.hooksPath=/dev/null", "-C", str(self.root), *args],
            env=env,
            capture_output=True,
            check=False,
            timeout=30,
        )

    def resolve(self, revision: str) -> str:
        if not REVISION_RE.fullmatch(revision):
            raise InputFailure("input_invalid")
        done = self.git("rev-parse", "--verify", "--end-of-options",
                        f"{revision}^{{commit}}")
        if done.returncode != 0:
            raise InputFailure("input_invalid")
        try:
            return done.stdout.decode("ascii").strip()
        except UnicodeError:
            raise InputFailure("input_invalid") from None

    def read(self, revision: str, path: str) -> bytes | None:
        done = self.git("cat-file", "blob", f"{revision}:{path}")
        return done.stdout if done.returncode == 0 else None


def pinned_bytes(root: Path, store: GitStore, revision: str,
                 path: str, expected_sha256: str) -> bytes:
    raw = store.read(revision, path)
    if raw is not None:
        if hashlib.sha256(raw).hexdigest() != expected_sha256:
            raise InputFailure("snapshot_tampered")
        return raw

    # The pinned source inputs are immutable fixtures, not candidate deliverables.
    # The baseline predates their round-25 paths, so use an exact local copy only
    # when that revision has no blob for the fixture.
    candidates = [root / path]
    candidates.extend(parent / path for parent in root.parents)
    candidates.extend(parent / path for parent in Path(__file__).resolve().parents)
    seen: set[Path] = set()
    for candidate_path in candidates:
        try:
            candidate_path = candidate_path.resolve(strict=True)
        except OSError:
            continue
        if candidate_path in seen:
            continue
        seen.add(candidate_path)
        try:
            candidate = candidate_path.read_bytes()
        except OSError:
            continue
        if hashlib.sha256(candidate).hexdigest() != expected_sha256:
            raise InputFailure("snapshot_tampered")
        return candidate
    raise InputFailure("input_invalid")


def pinned_population_bytes(root: Path, store: GitStore, revision: str) -> bytes:
    return pinned_bytes(root, store, revision, POPULATION, POPULATION_SHA256)


def pinned_source_bytes(root: Path, store: GitStore, revision: str) -> bytes:
    return pinned_bytes(root, store, revision, SOURCE, SOURCE_SHA256)


def population_rows(raw: bytes) -> list[dict[str, str]]:
    try:
        population = strict_json(raw)
    except (UnicodeError, ValueError):
        raise InputFailure("population_invalid") from None
    if (not isinstance(population, dict)
            or population.get("sourceSha256") != SOURCE_SHA256):
        raise InputFailure("population_invalid")
    rows = population.get("criteria")
    if not isinstance(rows, list) or len(rows) != EXPECTED:
        raise InputFailure("population_invalid")
    required = ("id", "title", "level", "source", "normativeText")
    seen: set[str] = set()
    for row in rows:
        if (not isinstance(row, dict)
                or any(type(row.get(key)) is not str or not row[key].strip()
                       for key in required)
                or row["level"] not in ("A", "AA")
                or row["id"] in seen):
            raise InputFailure("population_invalid")
        seen.add(row["id"])
    return rows

def normalized(text: str) -> str:
    text = " ".join(text.split())
    return re.sub(r"(\()\s+", r"\1", re.sub(r"\s+([,.;:)])", r"\1", text))



def derive_packet(rows: list[dict[str, str]], cards: Any) -> dict[str, Any]:
    if not isinstance(cards, list):
        raise InputFailure("input_invalid")

    reference = {row["id"]: row for row in rows}
    buckets: dict[str, list[dict[str, Any]]] = {}
    global_findings: list[str] = []
    for card in cards:
        if not isinstance(card, dict) or not isinstance(card.get("id"), str):
            global_findings.append("input_invalid")
            continue
        criterion_id = card["id"]
        if criterion_id not in reference:
            global_findings.append("metadata_mismatch")
        buckets.setdefault(criterion_id, []).append(card)

    criteria: list[dict[str, Any]] = []
    for criterion_id, reference_row in reference.items():
        found = buckets.get(criterion_id, [])
        findings: list[str] = []
        if not found:
            findings.append("missing_id")
        elif len(found) != 1:
            findings.append("duplicate_id")
        else:
            card = found[0]
            if set(card) != FIELDS:
                findings.append("fields_mismatch")
            if any(card.get(key) != reference_row[key]
                   for key in ("id", "title", "level", "source")):
                findings.append("metadata_mismatch")
            if any(type(card.get(key)) is not str or not card[key].strip()
                   for key in PROSE):
                findings.append("empty_field")
            quote = card.get("sourceQuote")
            if type(quote) is not str or not quote.strip():
                findings.append("empty_field")
            else:
                quote = normalized(quote)
                if len(quote.split()) < 6:
                    findings.append("quote_too_short")
                if len(quote.split()) > 25:
                    findings.append("quote_too_long")
                if re.search(r"(?<!\w)" + re.escape(quote) + r"(?!\w)",
                             normalized(reference_row["normativeText"])) is None:
                    findings.append("quote_not_from_source")
            if card.get("status") != "not-assessed":
                findings.append("status_not_assessed")
        criteria.append({
            "id": criterion_id,
            "accepted": not findings,
            "findings": sorted(set(findings)),
        })

    accepted = sum(row["accepted"] for row in criteria)
    findings = sorted(set(global_findings + [
        finding for row in criteria for finding in row["findings"]
    ]))
    clean = accepted == EXPECTED and not findings and len(cards) == EXPECTED
    return packet_result("clean" if clean else "failed", accepted,
                         criteria, findings)


def strict_equal(left: Any, right: Any) -> bool:
    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        return (left.keys() == right.keys()
                and all(strict_equal(left[key], right[key]) for key in left))
    if isinstance(left, list):
        return len(left) == len(right) and all(
            strict_equal(a, b) for a, b in zip(left, right))
    return left == right


def parse_tool_result(proc: subprocess.CompletedProcess[bytes]) -> dict[str, Any]:
    if proc.stderr:
        raise InputFailure("input_invalid")
    try:
        result = strict_json(proc.stdout)
    except (UnicodeError, ValueError):
        raise InputFailure("input_invalid") from None
    if not isinstance(result, dict):
        raise InputFailure("input_invalid")
    return result


def invoke_candidate(tool: bytes, cards: bytes | None, population: bytes,
                     source: bytes) -> tuple[dict[str, Any], int]:
    try:
        with tempfile.TemporaryDirectory(prefix="kake-r25-measure-") as directory:
            snapshot = Path(directory)
            tool_path = snapshot / PACKET_TOOL
            tool_path.parent.mkdir(parents=True, exist_ok=True)
            tool_path.write_bytes(tool)
            card_path = snapshot / CARDS
            if cards is not None:
                card_path.parent.mkdir(parents=True, exist_ok=True)
                card_path.write_bytes(cards)
            for relative_path, contents in ((POPULATION, population),
                                            (SOURCE, source)):
                fixture_path = snapshot / relative_path
                fixture_path.parent.mkdir(parents=True, exist_ok=True)
                fixture_path.write_bytes(contents)
            env = {key: os.environ[key] for key in ("PATH", "SYSTEMROOT", "WINDIR")
                   if key in os.environ}
            env.update(PYTHONIOENCODING="utf-8", PYTHONUTF8="1",
                       PYTHONDONTWRITEBYTECODE="1")
            proc = subprocess.run(
                [sys.executable, "-I", "-B", str(tool_path),
                 "--root", str(snapshot), "--json"],
                cwd=snapshot,
                env=env,
                capture_output=True,
                check=False,
                timeout=60,
            )
            return parse_tool_result(proc), proc.returncode
    except (OSError, subprocess.TimeoutExpired):
        raise InputFailure("input_invalid") from None




def capability_absent(rows: list[dict[str, str]]) -> dict[str, Any]:
    criteria = [{"id": row["id"], "accepted": False,
                 "findings": ["input_invalid"]} for row in rows]
    return packet_result("failed", 0, criteria, ["input_invalid"])


def input_invalid_rows(rows: list[dict[str, str]]) -> dict[str, Any]:
    return packet_result("could-not-evaluate", 0, [], ["input_invalid"])


def invalid_input(finding: str) -> dict[str, Any]:
    return packet_result("could-not-evaluate", 0, [], [finding])


def evaluate(root: Path, revision: str) -> tuple[dict[str, Any], int]:
    try:
        store = GitStore(root)
        resolved = store.resolve(revision)
        population = pinned_population_bytes(root, store, resolved)
        source = pinned_source_bytes(root, store, resolved)
        rows = population_rows(population)
        tool = store.read(resolved, PACKET_TOOL)
        cards_raw = store.read(resolved, CARDS)
    except InputFailure as exc:
        return invalid_input(exc.finding), 2
    except (OSError, subprocess.SubprocessError):
        return invalid_input("input_invalid"), 2

    if tool is None:
        return capability_absent(rows), 1

    try:
        tool_result, tool_exit = invoke_candidate(
            tool, cards_raw, population, source)
    except InputFailure as exc:
        return invalid_input(exc.finding), 2

    try:
        cards = strict_json(cards_raw) if cards_raw is not None else None
        expected_result = derive_packet(rows, cards)
    except (UnicodeError, ValueError):
        expected_result = input_invalid_rows(rows)
        expected_exit = 2
    except InputFailure:
        expected_result = input_invalid_rows(rows)
        expected_exit = 2
    else:
        expected_exit = 0 if expected_result["verdict"] == "clean" else 1
        if cards_raw is None:
            expected_result = input_invalid_rows(rows)
            expected_exit = 2

    if tool_exit != expected_exit or not strict_equal(tool_result, expected_result):
        return invalid_input("input_invalid"), 2
    return expected_result, expected_exit


def main(argv: list[str] | None = None) -> int:
    parser = Parser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--revision", required=True)
    try:
        args = parser.parse_args(argv)
    except UsageError:
        output, exit_code = invalid_input("usage"), 64
    else:
        try:
            root = args.root.resolve(strict=True)
            output, exit_code = evaluate(root, args.revision)
        except OSError:
            output, exit_code = invalid_input("input_invalid"), 2
    print(json.dumps(output, ensure_ascii=False, sort_keys=True))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
