#!/usr/bin/env python3
"""Check a declaration's pre-scored tool inventory against committed summary bytes."""
import argparse
import json
import subprocess
import sys

CONTRACT_SUMMARY = ".ufo/waves/round-39/verification/pre-summary.jsonl"
POLICY = ("Only tools first scored after this declaration, other than the exact build bytes, "
          "are controls under the kill rule; the pre-declaration inventory above assigns "
          "each earlier score its class and consequence treatment.")


def class_for(label):
    if label == "sitemap_audit_ref":
        return "oracle/private reference; excluded from control consequence"
    if label.startswith("A_"):
        return "single-sentence reference ablation; control"
    return {
        "const_clean": "constant-clean control",
        "junk": "junk-output control",
        "no_reader": "manifest-only/no-reader control",
        "shallow": "shallow-reader control",
        "base": "absent-tool baseline; no bytes to hash",
    }.get(label)


def show(repo, revision, path):
    return subprocess.check_output(
        ["git", "-C", repo, "show", f"{revision}:{path}"], text=True
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True, help="repository holding the committed scorecard")
    ap.add_argument("--revision", required=True, help="scorecard commit")
    ap.add_argument("--summary-repo", help="repository holding pre-summary.jsonl (default: --repo)")
    ap.add_argument("--summary-revision", help="summary commit (default: --revision)")
    args = ap.parse_args()
    summary_repo = args.summary_repo or args.repo
    summary_revision = args.summary_revision or args.revision
    scorecard = show(args.repo, args.revision, "SCORECARD.md")
    rows = [json.loads(line) for line in show(summary_repo, summary_revision, CONTRACT_SUMMARY).splitlines() if line]
    expected = {}
    invalid_labels = []
    for row in rows:
        label = row["label"]
        klass = class_for(label)
        if klass is None or label in expected:
            invalid_labels.append(label)
            continue
        digest = row["toolSha256"]
        expected[label] = (digest if digest is not None else "—", klass)
    digest_rows = {label: pair for label, pair in expected.items() if pair[0] != "—"}

    marker = "### Pre-declaration scored-tool inventory"
    start = scorecard.find(marker)
    end = scorecard.find("- **Control classes", start) if start >= 0 else -1
    block = scorecard[start:end] if start >= 0 and end >= 0 else ""
    found = {}
    malformed = 0
    for line in block.splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 3 or cells[0] in {"Tool label", "---"} or set(cells[0]) <= {"-", ":"}:
            continue
        label, digest, klass = cells
        if label in found:
            malformed += 1
        found[label] = (digest, klass)

    missing = [label for label, pair in expected.items() if found.get(label) != pair]
    missing_sha = [label for label in digest_rows if found.get(label) != digest_rows[label]]
    extra = [label for label in found if label not in expected]
    duplicate_hashes = len([digest for digest, _ in found.values() if digest != "—"]) != len(
        {digest for digest, _ in found.values() if digest != "—"}
    )
    policy_ok = POLICY in scorecard
    if invalid_labels or malformed or missing or extra or duplicate_hashes or not policy_ok:
        print(
            "FAIL: "
            f"{len(missing_sha)} of {len(digest_rows)} byte-bearing scores missing/wrong; "
            f"{len(extra)} extra labels; {malformed} duplicate labels; "
            f"duplicate_sha256={str(duplicate_hashes).lower()}; "
            f"absent_baseline={'present' if found.get('base') == expected.get('base') else 'missing'}; "
            f"post-declaration_scope={'explicit' if policy_ok else 'missing'}"
        )
        return 1
    print(
        f"PASS: {len(digest_rows)}/{len(digest_rows)} byte-bearing pre-declaration scores "
        "SHA-pinned and classed; absent baseline explicit; post-declaration scope explicit"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
