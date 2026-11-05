#!/usr/bin/env python3
"""Round-97 C1 repair builder: emits the `## Coverage index — round 97` table.

Two row kinds, both written by the L1 and judged row-by-row by review seats:
  * corrected rows: an entry whose existing index row omits source ids from
    the entry's own `source:` line. The row keeps the existing Area and
    Coverage text verbatim and its Entry cell names every id the entry cites
    (the correction is the id set; the older row stays as filed history).
  * new rows: an entry with no index row at all; Area and Coverage are
    authored from the entry's H1, `ground:` and `scope:` lines.
Usage: gen_index_rows.py --root LANE --revision REV  (reads committed bytes)
"""
import argparse
import importlib.util
import os
import sys

here = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("c97i", os.path.join(here, "c97_index.py"))
c97i = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c97i)

NEW = {
    "cache-key-conformance-gate.md": (
        "Cache-key constructor conformance gate (r90)",
        "A behavioural gate that decides whether a stdin/stdout cache-key constructor "
        "conforms to the lane's round-89 key contract; not storability, freshness, "
        "revalidation, reuse or serving"),
    "cache-key-construction.md": (
        "Vary cache-key construction (r89)",
        "Constructing the stored-response key a presented request maps to from a "
        "supplied URI, request header map and Vary value; no server, CDN or browser "
        "behaviour claimed"),
    "conditional-list-membership.md": (
        "Conditional-request contract v2 semantics (r95)",
        "What the RFCs decide for the evaluator's v2 clauses: empty list elements, "
        "obs-text inside an opaque-tag, duplicate JSON member names and the GET/HEAD "
        "304/412 split, separated from lane conventions"),
    "conditional-request-evaluation.md": (
        "Conditional request evaluation (r93)",
        "Deciding which status (200, 304 or 412) a recipient would answer a "
        "conditional request with, and the deciding precondition, over supplied "
        "values under contract v1; no live CDN or Pages front claimed"),
    "gate-agreement-metadata.md": (
        "Gate-agreement ledger provenance (r88)",
        "Provenance companion for the JSON gate-agreement ledger: the ledger digest, "
        "per-row snapshot provenance from the verifier spot-checks, and the recheck "
        "trigger when a spot-check re-decides a row"),
    "gate-status-ledger.md": (
        "Historical and host-bound gate status (r66)",
        "Dated list of lane gates that go red by design on later trees or on a "
        "migrated host, adopted from the considerthese proposal, with re-runnable "
        "counter receipts behind each adjudication"),
    "heuristic-freshness.md": (
        "Heuristic freshness decision (r92)",
        "When a cache may assign a heuristic expiration time to a stored response and "
        "what lifetime it carries, one decision per stored response; no clock, "
        "storage or revalidation"),
    "http-list-and-method-grammar.md": (
        "Conditional-request grammar (r94)",
        "The method-token case rule and the list-member whitespace rule for If-Match "
        "and If-None-Match as RFC 9110 states them; entity-tag grammar and contract "
        "decisions stay out of scope"),
    "revalidation-exchange.md": (
        "Revalidation exchange (r96)",
        "Which precondition validators a cache sends for a stored response and how it "
        "handles the validation reply (304 update, 5xx reuse, full-response "
        "replacement), decided over supplied values under contract v1; no live cache"),
    "sitemap-formats.md": (
        "Sitemap containers and formats (r77)",
        "The container and format rules an offline sitemap audit decides: the XML "
        "schema form, the gzip container, plain-text sitemaps and RSS 2.0 or Atom 1.0 "
        "feeds, each attributed to its source row; no property fetched"),
    "stored-response-reuse.md": (
        "Stored-response reuse decision (r91)",
        "What one stored response may be used for under contract v1: the reuse "
        "decision over supplied status, header and request maps with first-match "
        "freshness lifetime and current age; no live property"),
    "vary-matching.md": (
        "Conservative Vary matching (r88)",
        "The RFC 9111 section 4.1 match rule as this reader applies it offline to two "
        "supplied request-header maps; not cache-key construction, storage, "
        "revalidation, freshness or serving"),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--revision", required=True)
    a = ap.parse_args()
    sha, readme, entries = c97i.load(os.path.abspath(a.root), a.revision)
    d = c97i.audit(readme, entries)
    rows = c97i.index_rows(readme)
    out = ["| Area | Entry | Coverage |", "|---|---|---|"]
    for name in sorted(d["unindexed"]):
        ids = sorted(c97i.source_ids(entries[name]))
        idtxt = (" (" + ", ".join(ids) + ")") if ids else " (own-work; no SOURCES row)"
        if name in NEW:
            area, cov = NEW[name]
            out.append("| %s | `knowledge/%s`%s | %s |" % (area, name, idtxt, cov))
            continue
        prior = [r for r in rows if name in c97i.TOKEN.findall(r[0])
                 and len(c97i.split_cells(r[2])) == 3]
        if not prior:
            sys.exit("no prior row and no authored row for %s" % name)
        cells = c97i.split_cells(prior[0][2])
        area, cov = cells[0], cells[-1]
        out.append("| %s | `knowledge/%s`%s | %s |" % (area, name, idtxt, cov))
    print("\n".join(out))


if __name__ == "__main__":
    main()
