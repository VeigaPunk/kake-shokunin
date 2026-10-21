#!/usr/bin/env python3
"""Validate the offline publisher-side accessibility manual-review packet.

Usage: accessibility_packet.py --root ROOT [--json] [--selftest]
       accessibility_packet.py --selftest [--json]

ROOT supplies .ufo/waves/round-25/population.json and
corpus/knowledge/accessibility-review-cards.json. Normal operation reads only
those local files and emits one JSON object; --json is explicit but optional.
Quotes must be literal, case-sensitive substrings of normativeText, with at
most 25 whitespace-delimited words. No heading/text fallback or normalization
is applied. Card acceptance means packet readiness, never WCAG conformity,
criterion satisfaction, or an evaluation of any website.

--selftest ignores ROOT and uses synthetic fixtures in a temporary directory
only. Its JSON adds a selftest record identifying those fixtures. --help emits
CLI documentation instead of a packet result. Exit codes: 0 structurally clean
(or selftest passed), 1 packet findings (or selftest failed), 2 unavailable or
invalid input, 64 usage. No network access occurs in either mode.
"""

from __future__ import annotations

import argparse
import contextlib
import io
import json
import sys
import tempfile
from pathlib import Path

SCHEMA = "kake-accessibility-packet-v1"
EXPECTED = 55
POPULATION_PATH = Path(".ufo/waves/round-25/population.json")
CARDS_PATH = Path("corpus/knowledge/accessibility-review-cards.json")
METADATA_FIELDS = ("id", "title", "level", "source")
CARD_FIELDS = frozenset(
    (*METADATA_FIELDS, "sourceQuote", "publisherCheck", "evidenceNeeded",
     "failureExample", "limitation", "status")
)
EXIT_CLEAN = 0
EXIT_FAILED = 1
EXIT_INPUT = 2
EXIT_USAGE = 64


class InputProblem(ValueError):
    """A local input cannot provide an unambiguous packet inventory."""


class UsageError(ValueError):
    """The command-line shape is invalid."""


class PacketArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise UsageError(message)


class SingleRootAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None) -> None:
        if getattr(namespace, self.dest, None) is not None:
            raise UsageError("--root may be given only once")
        setattr(namespace, self.dest, values)


def _unique_members(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise InputProblem("Repeated JSON object member")
        result[key] = value
    return result


def _invalid_constant(value: str) -> None:
    raise InputProblem("Non-JSON numeric constant")


def _read_json(path: Path) -> object:
    try:
        return json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=_unique_members,
            parse_constant=_invalid_constant,
        )
    except (OSError, UnicodeError, ValueError, RecursionError) as exc:
        raise InputProblem("Input is unavailable or is not valid UTF-8 JSON") from exc


def _nonempty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _load_population(path: Path) -> list[dict]:
    document = _read_json(path)
    if not isinstance(document, dict):
        raise InputProblem("Population must be an object")
    criteria = document.get("criteria")
    if not isinstance(criteria, list) or len(criteria) != EXPECTED:
        raise InputProblem("Population must contain exactly 55 criteria")
    seen = set()
    for criterion in criteria:
        if not isinstance(criterion, dict) or any(
            not _nonempty_string(criterion.get(field))
            for field in (*METADATA_FIELDS, "normativeText")
        ):
            raise InputProblem("Population metadata and normativeText are required")
        if criterion["level"] not in ("A", "AA") or criterion["id"] in seen:
            raise InputProblem("Population levels or identities are invalid")
        seen.add(criterion["id"])
    return criteria


def _result(verdict: str, criteria: list[dict], findings: list[str]) -> dict:
    return {
        "schema": SCHEMA,
        "verdict": verdict,
        "expected": EXPECTED,
        "accepted": sum(1 for row in criteria if row["accepted"]),
        "criteria": criteria,
        "findings": findings,
        "websiteConformance": "not-assessed",
    }


def _card_findings(card: object, criterion: dict | None) -> set[str]:
    findings = set()
    if not isinstance(card, dict):
        card = {}
    if card.keys() != CARD_FIELDS:
        findings.add("fields_mismatch")
    if any(not _nonempty_string(card.get(field)) for field in CARD_FIELDS):
        findings.add("empty_field")
    if criterion is None or any(
        card.get(field) != criterion[field] for field in METADATA_FIELDS
    ):
        findings.add("metadata_mismatch")
    if card.get("status") != "not-assessed":
        findings.add("status_not_assessed")
    quote = card.get("sourceQuote")
    if _nonempty_string(quote):
        if len(quote.split()) > 25:
            findings.add("quote_too_long")
        if criterion is not None and quote not in criterion["normativeText"]:
            findings.add("quote_not_from_source")
    return findings


def audit_packet(root: str | Path) -> tuple[dict, int]:
    """Return packet readiness and exit code without network access or writes."""
    root = Path(root)
    try:
        population = _load_population(root / POPULATION_PATH)
    except InputProblem:
        return _result("could-not-evaluate", [], ["input_invalid"]), EXIT_INPUT
    try:
        cards = _read_json(root / CARDS_PATH)
        if not isinstance(cards, list):
            raise InputProblem("Cards must be a JSON list")
    except InputProblem:
        rows = [
            {"id": item["id"], "accepted": False, "findings": ["input_invalid"]}
            for item in population
        ]
        return _result("could-not-evaluate", rows, ["input_invalid"]), EXIT_INPUT

    expected = {item["id"]: item for item in population}
    grouped = {identity: [] for identity in expected}
    findings = set()
    for card in cards:
        identity = card.get("id") if isinstance(card, dict) else None
        criterion = expected.get(identity) if isinstance(identity, str) else None
        card_findings = _card_findings(card, criterion)
        findings.update(card_findings)
        if criterion is not None:
            grouped[identity].append(card_findings)

    rows = []
    for criterion in population:
        matches = grouped[criterion["id"]]
        row_findings = set()
        if not matches:
            row_findings.add("missing_id")
        else:
            for issues in matches:
                row_findings.update(issues)
            if len(matches) != 1:
                row_findings.add("duplicate_id")
        findings.update(row_findings)
        rows.append({
            "id": criterion["id"],
            "accepted": not row_findings,
            "findings": sorted(row_findings),
        })
    verdict = "failed" if findings else "clean"
    return _result(verdict, rows, sorted(findings)), EXIT_FAILED if findings else EXIT_CLEAN


def parse_cli(argv: list[str]) -> argparse.Namespace:
    parser = PacketArgumentParser(
        prog="accessibility_packet.py",
        allow_abbrev=False,
        description="Offline packet readiness only; no website or WCAG conformity assessment.",
    )
    parser.add_argument("--root", metavar="ROOT", action=SingleRootAction,
                        help="root containing the pinned population and review-card list")
    parser.add_argument("--json", action="store_true", help="emit JSON (the default)")
    parser.add_argument("--selftest", action="store_true",
                        help="use synthetic temporary fixtures only; ROOT is not read")
    args = parser.parse_args(argv)
    if args.root is not None and not args.root.strip():
        parser.error("--root must be nonempty")
    if not args.selftest and args.root is None:
        parser.error("--root ROOT is required unless --selftest is selected")
    return args


def selftest() -> tuple[dict, int]:
    """Exercise the public CLI against temporary synthetic inputs, never ROOT."""
    records = []
    baseline = None
    normative = " ".join(f"token{index}" for index in range(1, 31)) + "."
    population = {
        "criteria": [
            {
                "id": f"fixture.{index:02d}",
                "title": f"Synthetic criterion {index}",
                "level": "AA" if index % 2 == 0 else "A",
                "source": f"https://example.invalid/packet-fixture/#criterion-{index}",
                "normativeText": normative,
                "text": f"Synthetic heading {index}. {normative} Supplemental note only.",
            }
            for index in range(1, EXPECTED + 1)
        ]
    }
    pristine = [
        {
            **{field: item[field] for field in METADATA_FIELDS},
            "sourceQuote": "token1 token2 token3 token4 token5",
            "publisherCheck": "Record the relevant manual publisher review scope.",
            "evidenceNeeded": "Retain the manual review observations and their scope.",
            "failureExample": "A documented requirement is omitted from the review plan.",
            "limitation": "Synthetic fixture only; no website has been assessed.",
            "status": "not-assessed",
        }
        for item in population["criteria"]
    ]
    fixture_ids = [item["id"] for item in population["criteria"]]

    try:
        with tempfile.TemporaryDirectory(prefix="kake-accessibility-packet-") as directory:
            root = Path(directory)
            population_path = root / POPULATION_PATH
            cards_path = root / CARDS_PATH
            population_path.parent.mkdir(parents=True)
            cards_path.parent.mkdir(parents=True)

            def store(path: Path, document: object) -> None:
                path.write_text(json.dumps(document), encoding="utf-8")

            def check(name: str, expected_exit: int, accepted: int,
                      findings: list[str], argv: list[str] | None = None,
                      expected_rows: int = EXPECTED) -> dict | None:
                stdout, stderr = io.StringIO(), io.StringIO()
                arguments = ["--root", str(root), "--json"] if argv is None else argv
                try:
                    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                        exit_code = main(arguments)
                    payload = json.loads(stdout.getvalue())
                    assert exit_code == expected_exit, "exit code"
                    assert set(payload) == {
                        "schema", "verdict", "expected", "accepted", "criteria",
                        "findings", "websiteConformance",
                    }, "result fields"
                    assert payload["schema"] == SCHEMA, "schema"
                    assert payload["verdict"] == {
                        EXIT_CLEAN: "clean", EXIT_FAILED: "failed",
                        EXIT_INPUT: "could-not-evaluate", EXIT_USAGE: "could-not-evaluate",
                    }[expected_exit], "verdict"
                    assert payload["expected"] == EXPECTED, "fixed population size"
                    assert type(payload["accepted"]) is int, "accepted type"
                    assert payload["accepted"] == accepted, "accepted count"
                    assert payload["findings"] == sorted(findings), "stable findings"
                    assert payload["websiteConformance"] == "not-assessed", "conformance boundary"
                    rows = payload["criteria"]
                    assert isinstance(rows, list) and len(rows) == expected_rows, "row count"
                    assert [row["id"] for row in rows] == (
                        fixture_ids if expected_rows == EXPECTED else []
                    ), "row identities/order"
                    for row in rows:
                        assert set(row) == {"id", "accepted", "findings"}, "row fields"
                        assert type(row["accepted"]) is bool, "row accepted type"
                        assert row["findings"] == sorted(set(row["findings"])), "row findings"
                        assert row["accepted"] == (not row["findings"]), "row acceptance"
                        assert set(row["findings"]).issubset(payload["findings"]), "findings union"
                    assert sum(row["accepted"] for row in rows) == accepted, "row total"
                except Exception as exc:
                    records.append({"id": name, "ok": False,
                                    "detail": f"{type(exc).__name__}: {exc}"})
                    return None
                records.append({"id": name, "ok": True})
                return payload

            def change(field: str, value: object) -> None:
                cards = [dict(card) for card in pristine]
                cards[0][field] = value
                store(cards_path, cards)

            store(population_path, population)
            store(cards_path, pristine)
            baseline = check("pristine55", EXIT_CLEAN, EXPECTED, [])
            check("json_is_default", EXIT_CLEAN, EXPECTED, [], ["--root", str(root)])
            store(cards_path, list(reversed(pristine)))
            check("card_order_is_not_identity", EXIT_CLEAN, EXPECTED, [])
            change("sourceQuote", " ".join(normative.split()[:25]))
            check("quote25", EXIT_CLEAN, EXPECTED, [])
            change("sourceQuote", " ".join(normative.split()[:26]))
            check("quote26", EXIT_FAILED, EXPECTED - 1, ["quote_too_long"])
            change("sourceQuote", "Synthetic heading 1.")
            check("heading_is_not_normative", EXIT_FAILED, EXPECTED - 1, ["quote_not_from_source"])
            change("sourceQuote", "Supplemental note only.")
            check("note_is_not_normative", EXIT_FAILED, EXPECTED - 1, ["quote_not_from_source"])
            change("sourceQuote", "TOKEN1")
            check("quote_case_is_literal", EXIT_FAILED, EXPECTED - 1, ["quote_not_from_source"])
            change("sourceQuote", "token1  token2")
            check("quote_spacing_is_literal", EXIT_FAILED, EXPECTED - 1, ["quote_not_from_source"])
            store(cards_path, pristine[:-1])
            check("missing_card", EXIT_FAILED, EXPECTED - 1, ["missing_id"])
            store(cards_path, [])
            check("empty_packet", EXIT_FAILED, 0, ["missing_id"])
            store(cards_path, pristine + [dict(pristine[0])])
            check("duplicate_card", EXIT_FAILED, EXPECTED - 1, ["duplicate_id"])
            change("id", "fixture.unknown")
            check("changed_id", EXIT_FAILED, EXPECTED - 1, ["metadata_mismatch", "missing_id"])
            change("id", pristine[1]["id"])
            check("changed_to_known_id", EXIT_FAILED, EXPECTED - 2,
                  ["duplicate_id", "metadata_mismatch", "missing_id"])
            store(cards_path, pristine + [{**pristine[0], "id": "fixture.extra"}])
            check("unexpected_extra_id", EXIT_FAILED, EXPECTED, ["metadata_mismatch"])
            for field in METADATA_FIELDS[1:]:
                change(field, pristine[0][field] + " changed")
                check(f"changed_{field}", EXIT_FAILED, EXPECTED - 1, ["metadata_mismatch"])
            for field in ("sourceQuote", "publisherCheck", "evidenceNeeded", "failureExample", "limitation"):
                change(field, " \n ")
                check(f"empty_{field}", EXIT_FAILED, EXPECTED - 1, ["empty_field"])
            for value in (None, [], 0):
                change("publisherCheck", value)
                check(f"nonstring_{type(value).__name__}", EXIT_FAILED, EXPECTED - 1, ["empty_field"])
            for status in ("passed", "failed", "inapplicable", "conformant", "not-assessed "):
                change("status", status)
                check(f"false_status_{status.strip()}", EXIT_FAILED, EXPECTED - 1, ["status_not_assessed"])
            cards = [dict(card) for card in pristine]
            del cards[0]["publisherCheck"]
            store(cards_path, cards)
            check("missing_field", EXIT_FAILED, EXPECTED - 1, ["empty_field", "fields_mismatch"])
            cards = [dict(card) for card in pristine]
            cards[0]["extra"] = "not part of a card"
            store(cards_path, cards)
            check("extra_field", EXIT_FAILED, EXPECTED - 1, ["fields_mismatch"])
            store(cards_path, [None, *pristine[1:]])
            check("nonobject_card", EXIT_FAILED, EXPECTED - 1,
                  ["empty_field", "fields_mismatch", "metadata_mismatch", "missing_id", "status_not_assessed"])
            cards_path.unlink()
            check("absent_cards", EXIT_INPUT, 0, ["input_invalid"])
            for name, content in (
                ("invalid_cards_json", "{"),
                ("cards_not_list", "{}"),
                ("duplicate_json_member", '[{"id":"a","id":"b"}]'),
                ("non_json_constant", "[NaN]"),
            ):
                cards_path.write_text(content, encoding="utf-8")
                check(name, EXIT_INPUT, 0, ["input_invalid"])
            cards_path.write_bytes(b"\xff")
            check("non_utf8_cards", EXIT_INPUT, 0, ["input_invalid"])
            store(cards_path, pristine)
            population_path.unlink()
            check("absent_population", EXIT_INPUT, 0, ["input_invalid"], expected_rows=0)
            population_path.write_text("{", encoding="utf-8")
            check("invalid_population_json", EXIT_INPUT, 0, ["input_invalid"], expected_rows=0)
            store(population_path, {"criteria": population["criteria"][:-1]})
            check("population_must_be55", EXIT_INPUT, 0, ["input_invalid"], expected_rows=0)
            store(population_path, {"criteria": [population["criteria"][0]] * EXPECTED})
            check("population_ids_unique", EXIT_INPUT, 0, ["input_invalid"], expected_rows=0)
            criteria = [dict(item) for item in population["criteria"]]
            del criteria[0]["normativeText"]
            store(population_path, {"criteria": criteria})
            check("no_text_fallback", EXIT_INPUT, 0, ["input_invalid"], expected_rows=0)
            store(population_path, population)
            for name, arguments in (
                ("usage_no_root", []),
                ("usage_missing_root_value", ["--root"]),
                ("usage_empty_root", ["--root", ""]),
                ("usage_unknown_option", ["--unknown"]),
                ("usage_abbreviated_option", ["--ro", str(root)]),
                ("usage_repeated_root", ["--root", str(root), "--root", str(root)]),
            ):
                check(name, EXIT_USAGE, 0, [], arguments, expected_rows=0)
    except OSError:
        result = _result("could-not-evaluate", [], ["input_invalid"])
        result["selftest"] = {"passed": False, "fixture": "synthetic-temporary-only", "cases": records}
        return result, EXIT_INPUT

    passed = baseline is not None and all(record["ok"] for record in records)
    result = _result(
        "clean" if passed else "failed",
        baseline["criteria"] if passed else [],
        [] if passed else ["selftest_failed"],
    )
    result["selftest"] = {"passed": passed, "fixture": "synthetic-temporary-only", "cases": records}
    return result, EXIT_CLEAN if passed else EXIT_FAILED


def main(argv: list[str] | None = None) -> int:
    try:
        args = parse_cli(sys.argv[1:] if argv is None else argv)
    except UsageError as exc:
        print(f"accessibility_packet.py: {exc}", file=sys.stderr)
        result, exit_code = _result("could-not-evaluate", [], []), EXIT_USAGE
    else:
        result, exit_code = selftest() if args.selftest else audit_packet(args.root)
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
