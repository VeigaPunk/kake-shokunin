#!/usr/bin/env python3
"""CHEAT DEMO (c61 cheat 5): disclosure matching with wrong-case path/commit.
Contract C1: event disclosed when disclosures JSON 'holds an entry with equal
path and commit'. Case semantics of 'equal' are NOT frozen; no L-fixture
exercises a case-twisted entry. A tool matching case-insensitively treats a
wrong-case entry as covering -> silent false-negative on the real lane."""
P = ".ufo/waves/r63-s101/controls/receipt-929.txt"
C = "062908f5977833449b93bce05edd23dd02e09a3f"

def covers(entry, ci_path=False, ci_commit=False):
    ep, ec = entry["path"], entry["commit"]
    p, c = P, C
    if ci_path: ep, p = ep.lower(), p.lower()
    if ci_commit: ec, c = ec.lower(), c.lower()
    return ep == p and ec == c

variants = [
    ("clean entry (L3 shape)",            {"path": P, "commit": C}),
    ("path dir case-twisted",             {"path": ".ufo/WAVES/r63-s101/controls/receipt-929.txt", "commit": C}),
    ("path Controls-twisted",             {"path": ".ufo/waves/r63-s101/CONTROLS/receipt-929.txt", "commit": C}),
    ("commit hex upper-cased",            {"path": P, "commit": C.upper()}),
    ("path + commit both twisted",        {"path": ".ufo/waves/r63-s101/controls/RECEIPT-929.txt", "commit": C.upper()}),
]
for name, entry in variants:
    strict = covers(entry)
    loose  = covers(entry, ci_path=True, ci_commit=True)
    print(f"{name:30s} strict_equal={strict}  case_insensitive={loose}")

print()
print("All five entries name the SAME real rewrite event.")
print("No frozen L-fixture feeds a twisted entry, so a case-insensitive tool")
print("still scores 18/18 while silently covering twisted disclosures -> hole.")
