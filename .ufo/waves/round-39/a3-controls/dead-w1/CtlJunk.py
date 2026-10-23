#!/usr/bin/env python3
"""Round-39 C1 CONTROL: junk output (deliberately skips the audit work).

Shape (frozen control class "junk output"):
  * reads NOTHING from disk -- the manifest, the sitemap files and the case
    directory are never opened;
  * prints one plausible-looking but WRONG JSON document on stdout: wrong key
    names (aliases "results"/"outcome"/"state"/"err"/"problems") and findings
    rendered as STRINGS ("loc_missing@3") instead of {"code": ..., "entry": ...}
    pairs;
  * chooses one of the contract's exit codes at random per run, and shapes the
    document consistently with it (0 -> clean, 1 -> failed-policy,
    2 -> could-not-evaluate), so the document is internally plausible.

Deliberately skipped: every rule (a)-(k) of
.ufo/waves/round-39/c1-contract.md -- encoding, well-formedness, doctype,
root, entries, entry children, size/entry limits, loc form, scope, lastmod,
changefreq, priority -- and all file reading.

The one piece of contract knowledge kept is the argument-shape rule
(sentence 2): an argument list that is not exactly "--manifest <path>" is a
usage error, exit 64, stdout ignored.  That is argument-shape detection, not
audit work, and it is what makes the control strong: the sealed counter's
judge returns True on an exit-only expectation without ever inspecting stdout.

Standard library only; no network; writes nothing but the stdout document.
"""
import json
import os
import random
import sys

# Contract sentence 34: the three exit codes that carry a verdict.
EXIT_CODES = (0, 1, 2)
VERDICT_FOR_EXIT = {0: "clean", 1: "failed-policy", 2: "could-not-evaluate"}
USAGE_EXIT = 64

ERROR_CODES = ("input_invalid", "check_invalid", "file_unreadable")
FINDING_CODES = (
    "encoding_invalid",
    "xml_malformed",
    "doctype_present",
    "root_invalid",
    "no_entries",
    "element_unexpected",
    "loc_missing",
    "loc_repeated",
    "field_repeated",
    "loc_not_absolute",
    "loc_too_long",
    "loc_out_of_scope",
    "lastmod_invalid",
    "changefreq_invalid",
    "priority_invalid",
    "too_large",
    "too_many_entries",
)
# Ids a hand-written manifest might plausibly use -- fabricated, not read.
FAKE_IDS = ("c1", "c2", "check-1", "case-1", "s1", "id1", "a1", "t1", "chk1")


def junk_document(rnd):
    """One plausible-looking but wrong JSON document."""
    code = rnd.choice(EXIT_CODES)
    verdict = VERDICT_FOR_EXIT[code]
    checks = []

    if code == 0:
        # "clean": no findings anywhere
        checks.append({"id": rnd.choice(FAKE_IDS), "status": "clean", "error": None,
                       "findings": []})
        if rnd.random() < 0.15:
            checks.append({"id": rnd.choice(FAKE_IDS), "status": "clean", "error": None,
                           "findings": []})
    elif code == 1:
        # "failed-policy": findings as STRINGS, not {"code","entry"} pairs
        findings = ["%s@%d" % (rnd.choice(FINDING_CODES), rnd.randint(1, 9))
                    for _ in range(rnd.randint(1, 2))]
        checks.append({"id": rnd.choice(FAKE_IDS), "status": "findings", "error": None,
                       "findings": findings})
    else:
        # "could-not-evaluate": either the manifest-level error shape
        # (contract sentence 3) or a per-check error
        if rnd.random() < 0.6:
            doc = {
                "version": 1,
                "verdict": verdict,
                "error": "input_invalid",
                "checks": [],
                # wrong key names
                "results": [],
                "outcome": verdict,
                "generated_by": "sitemap-audit",
            }
            return code, doc
        checks.append({"id": rnd.choice(FAKE_IDS), "status": "error",
                       "error": rnd.choice(ERROR_CODES), "findings": []})

    for c in checks:
        # wrong key names, the way a plausible-but-wrong tool would write them
        c["state"] = c["status"]
        c["err"] = c["error"]
        c["problems"] = c["findings"]

    doc = {
        "version": 1,
        "verdict": verdict,
        "checks": checks,
        # wrong key names at the top level too
        "results": checks,
        "outcome": verdict,
        "generated_by": "sitemap-audit",
    }
    return code, doc


def main(argv):
    # Contract sentence 2: only "--manifest <path>" is a usage; anything else
    # is a usage error (exit 64, stdout ignored).  No file is ever opened.
    if len(argv) != 2 or argv[0] != "--manifest" or not argv[1]:
        return USAGE_EXIT
    rnd = random.Random(os.urandom(16))
    code, doc = junk_document(rnd)
    sys.stdout.write(json.dumps(doc) + "\n")
    sys.stdout.flush()
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
