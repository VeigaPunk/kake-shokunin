#!/usr/bin/env python3
"""Seeded differential runner for the public round-35 link-preview contract.

Each trial generates focused one-page manifests for duplicate URLs, absolute
and relative URLs, and metadata inside template/svg/math, plus a manifest with
readable, non-UTF-8, and directory pages. Tool output is compared using the
round-35 projection: exit, verdict, and the multiset of (reason, page,
property); finding ids and pagesChecked are deliberately ignored.
"""
from __future__ import annotations

import argparse
import base64
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
import hashlib
import html
import json
import os
from pathlib import Path
import random
import re
import subprocess
import sys
import tempfile
from typing import Any

TIMEOUT_SECONDS = 20
MAX_MINIMIZATION_ATTEMPTS = 160
ASCII_WHITESPACE = " \t\n\r\f"
SUPPRESSED_CONTAINERS = frozenset(("template", "svg", "math"))


@dataclass(frozen=True)
class Asset:
    file: str
    url: str
    content: bytes | None = None
    directory: bool = False


@dataclass(frozen=True)
class GeneratedCase:
    name: str
    assets: tuple[Asset, ...]


def _escaped(value: str) -> str:
    return html.escape(value, quote=True)


def meta_tag(prop: str, value: str, rng: random.Random) -> str:
    attrs = [("property", prop), ("content", value)]
    rng.shuffle(attrs)
    quote = rng.choice(('"', "'"))
    return "<meta " + " ".join(f"{name}={quote}{_escaped(val)}{quote}" for name, val in attrs) + ">"


def canonical_tag(href: str, rng: random.Random) -> str:
    rel = rng.choice(("canonical", "alternate canonical", "CANONICAL"))
    attrs = [("rel", rel), ("href", href)]
    rng.shuffle(attrs)
    quote = rng.choice(('"', "'"))
    return "<link " + " ".join(f"{name}={quote}{_escaped(value)}{quote}" for name, value in attrs) + ">"


def document(head_fragments: list[str], rng: random.Random, *, shuffle: bool = True) -> bytes:
    if shuffle:
        rng.shuffle(head_fragments)
    text = "<!doctype html><html><head>" + "".join(head_fragments) + "</head><body></body></html>"
    return text.encode("utf-8")


def required_tags(token: str, page_url: str, url_value: str, rng: random.Random,
                  *, type_values: tuple[str, ...] = ("article",),
                  include_image: bool = True) -> list[str]:
    tags = [
        meta_tag("og:title", f"Round 35 {token}", rng),
        *(meta_tag("og:type", value, rng) for value in type_values),
        *( [meta_tag("og:image", f"https://images.example.test/{token}.png", rng)] if include_image else [] ),
        meta_tag("og:url", url_value, rng),
    ]
    return tags


def _url_for(seed: int, trial: int, name: str) -> str:
    return f"https://example.test/r35/{seed}/{trial}/{name}.html"


def _duplicate_url_case(seed: int, trial: int, token: str, rng: random.Random) -> GeneratedCase:
    page_url = _url_for(seed, trial, "duplicate")
    relative_one = f"../relative/{token}.html"
    relative_two = f"./second-{token}.html"
    wrong_absolute = f"https://example.test/not-canonical/{token}.html"
    first = rng.choice((page_url, relative_one, wrong_absolute))
    second = rng.choice(tuple(value for value in (page_url, relative_two, wrong_absolute)
                              if value != first))
    canonical_href = page_url if first == page_url else wrong_absolute
    fragments = required_tags(token, page_url, first, rng,
                              type_values=("article", "website"))
    fragments.append(meta_tag("og:url", second, rng))
    fragments.append(canonical_tag(canonical_href, rng))
    page = document(fragments, rng)
    return GeneratedCase(
        f"trial-{trial:04d}/duplicate_urls",
        (Asset("duplicate.html", page_url, page),),
    )


def _url_form_case(seed: int, trial: int, token: str, form: str,
                   rng: random.Random) -> GeneratedCase:
    page_url = _url_for(seed, trial, form)
    if form == "absolute_url":
        url_value = page_url
        canonical_href = page_url
    else:
        url_value = f"../relative/{token}.html"
        canonical_href = url_value
    fragments = required_tags(token, page_url, url_value, rng)
    fragments.append(canonical_tag(canonical_href, rng))
    return GeneratedCase(
        f"trial-{trial:04d}/{form}",
        (Asset(f"{form}.html", page_url, document(fragments, rng)),),
    )


def _embedded_case(seed: int, trial: int, token: str, rng: random.Random) -> GeneratedCase:
    page_url = _url_for(seed, trial, "embedded")
    wrong = f"https://example.test/ignored/{token}.html"
    hidden = (
        "<template>"
        + meta_tag("og:title", f"hidden-template-{token}", rng)
        + canonical_tag(wrong, rng)
        + "<svg>"
        + meta_tag("og:type", "hidden-svg", rng)
        + "<math>"
        + meta_tag("og:url", wrong, rng)
        + canonical_tag(wrong, rng)
        + "</math></svg></template>"
        + "<svg><math>"
        + meta_tag("og:type", "hidden-math", rng)
        + canonical_tag(wrong, rng)
        + "</math></svg>"
        + "<math><template>"
        + meta_tag("og:title", f"nested-{token}", rng)
        + canonical_tag(wrong, rng)
        + "</template></math>"
    )
    fragments = [hidden]
    fragments.extend(required_tags(token, page_url, page_url, rng, include_image=False))
    # A self-closed SVG must not hide the following required property or link.
    fragments.extend(("<svg/>", meta_tag("og:image", f"https://images.example.test/{token}.png", rng)))
    fragments.append(canonical_tag(page_url, rng))
    return GeneratedCase(
        f"trial-{trial:04d}/embedded_contexts",
        (Asset("embedded.html", page_url, document(fragments, rng, shuffle=False)),),
    )


def _mixed_input_case(seed: int, trial: int, token: str, rng: random.Random) -> GeneratedCase:
    readable_url = _url_for(seed, trial, "readable-neighbor")
    readable_tags = required_tags(
        token, readable_url, f"../relative/{token}.html", rng,
        type_values=("article", "website"),
    )
    readable_tags.append(canonical_tag(f"https://example.test/wrong/{token}.html", rng))
    assets = [
        Asset("readable.html", readable_url, document(readable_tags, rng)),
        Asset("not-utf8.html", _url_for(seed, trial, "not-utf8"), b"<html><head>\xff</head></html>"),
        Asset("directory-page", _url_for(seed, trial, "directory"), directory=True),
    ]
    rng.shuffle(assets)
    return GeneratedCase(f"trial-{trial:04d}/unreadable_neighbors", tuple(assets))


def build_cases(seed: int, trial: int, rng: random.Random) -> list[GeneratedCase]:
    token = f"{rng.getrandbits(32):08x}-{trial}"
    return [
        _duplicate_url_case(seed, trial, token, rng),
        _url_form_case(seed, trial, token, "absolute_url", rng),
        _url_form_case(seed, trial, token, "relative_url", rng),
        _embedded_case(seed, trial, token, rng),
        _mixed_input_case(seed, trial, token, rng),
    ]


def manifest_value(assets: tuple[Asset, ...]) -> dict[str, Any]:
    return {
        "version": 1,
        "pages": [{"file": asset.file, "url": asset.url} for asset in assets],
    }


def materialize(case_dir: Path, assets: tuple[Asset, ...]) -> Path:
    case_dir.mkdir(parents=True, exist_ok=True)
    for asset in assets:
        path = case_dir / asset.file
        if asset.directory:
            path.mkdir(parents=True, exist_ok=True)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(asset.content or b"")
    manifest = case_dir / "manifest.json"
    manifest.write_text(json.dumps(manifest_value(assets), sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return manifest


def tool_environment() -> dict[str, str]:
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env.setdefault("LC_ALL", "C.UTF-8")
    return env


def run_tool(tool: Path, case_dir: Path) -> dict[str, Any]:
    command = [sys.executable, "-B", str(tool), "--manifest", "manifest.json"]
    try:
        proc = subprocess.run(
            command,
            cwd=str(case_dir),
            capture_output=True,
            timeout=TIMEOUT_SECONDS,
            env=tool_environment(),
        )
    except subprocess.TimeoutExpired:
        return {"tool": str(tool), "runnerError": f"timed out after {TIMEOUT_SECONDS}s"}
    except OSError as exc:
        return {"tool": str(tool), "runnerError": f"could not start tool: {exc}"}

    observation: dict[str, Any] = {"tool": str(tool), "exitCode": proc.returncode}
    if proc.returncode in (0, 1, 2):
        try:
            payload = json.loads(proc.stdout.decode("utf-8"))
        except (UnicodeError, json.JSONDecodeError) as exc:
            observation["contractError"] = f"expected one UTF-8 JSON object: {exc}"
            observation["stdoutPreview"] = proc.stdout.decode("utf-8", errors="replace")[:1000]
            observation["stdoutSha256"] = hashlib.sha256(proc.stdout).hexdigest()
            return observation
        if not isinstance(payload, dict):
            observation["contractError"] = "JSON stdout is not an object"
            observation["stdoutPreview"] = proc.stdout.decode("utf-8", errors="replace")[:1000]
            observation["stdoutSha256"] = hashlib.sha256(proc.stdout).hexdigest()
            return observation
        findings = payload.get("findings")
        if not isinstance(findings, list):
            observation["contractError"] = "JSON findings is not a list"
            observation["stdoutPreview"] = proc.stdout.decode("utf-8", errors="replace")[:1000]
            observation["stdoutSha256"] = hashlib.sha256(proc.stdout).hexdigest()
            return observation
        observation["verdict"] = payload.get("verdict")
        observation["findings"] = [
            {key: finding.get(key) for key in ("reason", "page", "property")}
            if isinstance(finding, dict) else {"invalidFinding": finding}
            for finding in findings
        ]
    elif proc.returncode not in (64,):
        observation["contractError"] = "exit code is outside the public interface"
        observation["stdoutPreview"] = proc.stdout.decode("utf-8", errors="replace")[:1000]
        observation["stderrPreview"] = proc.stderr.decode("utf-8", errors="replace")[:1000]
        observation["stdoutSha256"] = hashlib.sha256(proc.stdout).hexdigest()
    return observation


def run_pair(tool_a: Path, tool_b: Path, case_dir: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    with ThreadPoolExecutor(max_workers=2) as pool:
        future_a = pool.submit(run_tool, tool_a, case_dir)
        future_b = pool.submit(run_tool, tool_b, case_dir)
        return future_a.result(), future_b.result()


def _field_key(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def semantic_key(observation: dict[str, Any]) -> tuple[Any, ...]:
    if "runnerError" in observation:
        return ("runnerError", observation.get("runnerError"))
    code = observation.get("exitCode")
    if code == 64:
        return (64,)
    if "contractError" in observation:
        return ("contractError", code, observation.get("stdoutSha256"))
    findings = tuple(sorted(
        (_field_key(item.get("reason")), _field_key(item.get("page")), _field_key(item.get("property")))
        for item in observation.get("findings", [])
    ))
    return (code, _field_key(observation.get("verdict")), findings)


def difference_key(left: dict[str, Any], right: dict[str, Any]) -> dict[str, Any]:
    if "contractError" in left or "contractError" in right or "runnerError" in left or "runnerError" in right:
        return {"nonContractResults": [semantic_key(left), semantic_key(right)]}
    if left.get("exitCode") not in (0, 1, 2) or right.get("exitCode") not in (0, 1, 2):
        return {"nonContractResults": [semantic_key(left), semantic_key(right)]}
    left_findings = Counter(
        (_field_key(item.get("reason")), _field_key(item.get("page")), _field_key(item.get("property")))
        for item in left.get("findings", [])
    )
    right_findings = Counter(
        (_field_key(item.get("reason")), _field_key(item.get("page")), _field_key(item.get("property")))
        for item in right.get("findings", [])
    )
    def expand(counts: Counter[tuple[str, str, str]]) -> list[dict[str, Any]]:
        output: list[dict[str, Any]] = []
        for signature, count in sorted(counts.items()):
            item = {"reason": json.loads(signature[0]), "page": json.loads(signature[1]),
                    "property": json.loads(signature[2])}
            output.extend([item] * count)
        return output
    verdict_a = left.get("verdict")
    verdict_b = right.get("verdict")
    return {
        "exitCodes": [left.get("exitCode"), right.get("exitCode")],
        "verdicts": [verdict_a, verdict_b],
        "findingsOnlyInA": expand(left_findings - right_findings),
        "findingsOnlyInB": expand(right_findings - left_findings),
    }


def _write_candidate(root: Path, assets: tuple[Asset, ...], tag: str) -> Path:
    case_dir = root / tag
    return materialize(case_dir, assets).parent


def minimize_case(case: GeneratedCase, root: Path, tool_a: Path, tool_b: Path,
                  target_delta: dict[str, Any]) -> tuple[tuple[Asset, ...], bool, int]:
    assets = list(case.assets)
    attempts = 0
    complete = True
    target = _field_key(target_delta)

    def preserves(candidate: list[Asset]) -> bool:
        nonlocal attempts, complete
        if attempts >= MAX_MINIMIZATION_ATTEMPTS:
            complete = False
            return False
        attempts += 1
        with tempfile.TemporaryDirectory(prefix="difftest-min-", dir=str(root)) as temp:
            case_dir = _write_candidate(Path(temp), tuple(candidate), "case")
            left, right = run_pair(tool_a, tool_b, case_dir)
        return _field_key(difference_key(left, right)) == target

    changed = True
    while changed and len(assets) > 1 and attempts < MAX_MINIMIZATION_ATTEMPTS:
        changed = False
        for index in range(len(assets)):
            candidate = assets[:index] + assets[index + 1:]
            if candidate and preserves(candidate):
                assets = candidate
                changed = True
                break

    for asset_index in range(len(assets)):
        asset = assets[asset_index]
        if asset.directory or asset.content is None:
            continue
        try:
            parts = re.findall(r"<[^>]*>|[^<]+", asset.content.decode("utf-8"), flags=re.DOTALL)
        except UnicodeError:
            continue
        granularity = 2
        while parts and attempts < MAX_MINIMIZATION_ATTEMPTS:
            chunk_size = (len(parts) + granularity - 1) // granularity
            reduced = False
            for start in range(0, len(parts), chunk_size):
                candidate_parts = parts[:start] + parts[start + chunk_size:]
                candidate_assets = list(assets)
                candidate_assets[asset_index] = Asset(
                    asset.file, asset.url, "".join(candidate_parts).encode("utf-8"), False
                )
                if preserves(candidate_assets):
                    parts = candidate_parts
                    assets = candidate_assets
                    granularity = max(2, granularity - 1)
                    reduced = True
                    break
            if reduced:
                continue
            if granularity >= len(parts):
                break
            granularity = min(len(parts), granularity * 2)
    if attempts >= MAX_MINIMIZATION_ATTEMPTS:
        complete = False
    return tuple(assets), complete, attempts


def asset_reproducer(asset: Asset) -> dict[str, Any]:
    result: dict[str, Any] = {"file": asset.file, "url": asset.url}
    if asset.directory:
        result["kind"] = "directory"
    else:
        content = asset.content or b""
        try:
            text = content.decode("utf-8")
        except UnicodeError:
            result["kind"] = "file"
            result["encoding"] = "base64"
            result["content"] = base64.b64encode(content).decode("ascii")
        else:
            result["kind"] = "file"
            result["encoding"] = "utf-8"
            result["content"] = text
    return result


def public_observation(observation: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in observation.items() if key != "tool"}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tool-a", required=True, metavar="PATH")
    parser.add_argument("--tool-b", required=True, metavar="PATH")
    parser.add_argument("--seed", required=True, type=int, metavar="N")
    parser.add_argument("--count", required=True, type=int, metavar="K")
    args = parser.parse_args(argv)

    tool_a = Path(args.tool_a).expanduser().resolve()
    tool_b = Path(args.tool_b).expanduser().resolve()
    summary: dict[str, Any] = {
        "runner": "kake-r35-difftest",
        "seed": args.seed,
        "count": args.count,
        "toolA": str(tool_a),
        "toolB": str(tool_b),
        "casesCompared": 0,
        "disagreementCount": 0,
        "disagreements": [],
    }
    if args.count < 1:
        summary["error"] = "--count must be at least 1"
        print(json.dumps(summary, sort_keys=True, separators=(",", ":")))
        return 64
    for label, tool in (("tool-a", tool_a), ("tool-b", tool_b)):
        if not tool.is_file():
            summary["error"] = f"{label} is not a file: {tool}"
            print(json.dumps(summary, sort_keys=True, separators=(",", ":")))
            return 2
    tmp_value = os.environ.get("TMPDIR")
    if not tmp_value or not Path(tmp_value).is_dir():
        summary["error"] = "TMPDIR must name an existing sandbox directory"
        print(json.dumps(summary, sort_keys=True, separators=(",", ":")))
        return 2

    rng = random.Random(args.seed)
    run_errors = 0
    contract_errors = 0
    with tempfile.TemporaryDirectory(prefix="kake-r35-difftest-", dir=tmp_value) as tmp:
        root = Path(tmp)
        for trial in range(args.count):
            for case in build_cases(args.seed, trial, rng):
                with tempfile.TemporaryDirectory(prefix="difftest-case-", dir=str(root)) as case_tmp:
                    case_dir = _write_candidate(Path(case_tmp), case.assets, "case")
                    left, right = run_pair(tool_a, tool_b, case_dir)
                summary["casesCompared"] += 1
                run_errors += int("runnerError" in left or "runnerError" in right)
                contract_errors += int("contractError" in left or "contractError" in right)
                if semantic_key(left) == semantic_key(right):
                    continue
                delta = difference_key(left, right)
                minimized_assets, minimization_complete, minimization_attempts = minimize_case(
                    case, root, tool_a, tool_b, delta
                )
                repro_assets = [asset_reproducer(asset) for asset in minimized_assets]
                summary["disagreements"].append({
                    "case": case.name,
                    "toolA": public_observation(left),
                    "toolB": public_observation(right),
                    "difference": delta,
                    "minimalReproducer": {
                        "manifest": manifest_value(minimized_assets),
                        "assets": repro_assets,
                        "minimization": {
                            "method": "page-entry and HTML-token deletion while preserving the same output delta",
                            "complete": minimization_complete,
                            "toolPairRuns": minimization_attempts,
                        },
                    },
                })
    summary["disagreementCount"] = len(summary["disagreements"])
    if run_errors:
        summary["runnerErrors"] = run_errors
        summary["status"] = "could-not-evaluate"
    elif contract_errors:
        summary["contractErrors"] = contract_errors
        summary["status"] = "could-not-evaluate"
    elif summary["disagreementCount"]:
        summary["status"] = "different"
    else:
        summary["status"] = "same"
    print(json.dumps(summary, sort_keys=True, separators=(",", ":"), ensure_ascii=False))
    if run_errors or contract_errors:
        return 2
    return 1 if summary["disagreementCount"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
