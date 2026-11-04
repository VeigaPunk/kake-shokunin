#!/usr/bin/env python3
"""ReviewReuse hand cases for the round-91 C2 contract.

Every expected value below was derived by hand from the contract text
(.ufo/waves/round-91/c2-contract.md) alone, BEFORE any run. The counter's
own hand cases were NOT used as sources for these inputs.

Modes:
  --reference     score against c91_reuse.reference() in-process
  --subject PATH  score a subject file as the counter would (subprocess,
                  fresh cwd, stdin JSON), with strict protocol checks
                  (raw-empty stdout on refusal, exact key set, int-not-bool).

Output: one line per case AGREE/DISAGREE/AMBIG-*, then a summary.
"""
import argparse
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile


def S(cc=None, status=200, date="1000000", age=None, expires=None, vary=None):
    h = {}
    if date is not None:
        h["Date"] = date
    if age is not None:
        h["Age"] = age
    if expires is not None:
        h["Expires"] = expires
    if vary is not None:
        h["Vary"] = vary
    if cc is not None:
        h["Cache-Control"] = cc
    return h


def I(scc=None, method="GET", rcc=None, now=1000030, shared=False,
      status=200, date="1000000", age=None, expires=None, vary=None,
      stored_headers=True, stored_extra=None, drop_request_headers=False):
    st = {"status": status}
    if stored_headers:
        st["headers"] = S(cc=scc, date=date, age=age, expires=expires, vary=vary)
    else:
        st["headers"] = {}
    if stored_extra:
        st.update(stored_extra)
    rh = {}
    if rcc is not None:
        rh["Cache-Control"] = rcc
    req = {"method": method}
    if not drop_request_headers:
        req["headers"] = rh
    inp = {"stored": st, "request": req, "now": now}
    if shared is not None:
        inp["shared"] = shared
    return inp


OK = "ok"
RF = "refuse"

# (name, kind, input, expected)  kind: ok/refuse
# AMBIG_* marks a genuinely contract-ambiguous input; exp = strict-contract
# reading, alt = the competing reading.
CASES = [
    # --- my item's named inputs -------------------------------------------
    ("cc-ows-around-equals", OK,
     I(scc="max-age = 60", now=1000030),
     {"exp": ("heuristic-undecided", None, 30), "alt": ("reuse", 60, 30),
      "why": "clause 4 trims the directive, not the name; 'max-age ' is unknown -> ignored"},
    ),
    ("no-cache-quoted-field-request", OK,
     I(scc="max-age=60", rcc='no-cache="Set-Cookie"', now=1000030),
     {"exp": ("revalidate", 60, 30)},
    ),
    ("stored-cc-empty-value", RF,
     I(scc="", now=1000030),
     {"exp": None, "alt": ("heuristic-undecided", None, 30),
      "why": "''.split(',') is [''] -> one empty directive -> clause 4 refusal; zero-directive reading would decide"},
    ),
    ("max-stale-quoted", RF,
     I(scc="max-age=60", rcc='max-stale="10"', now=1000065),
     {"exp": None},
    ),
    ("age-leading-zeros", OK,
     I(scc="max-age=60", age="007", now=1000010),
     {"exp": ("reuse", 60, 17)},
    ),
    ("date-far-future", OK,
     I(scc="max-age=60", date="2000000", now=1000000),
     {"exp": ("reuse", 60, 0)},
    ),
    ("expires-equals-date", OK,
     I(expires="1000000", now=1000000, scc=None),
     {"exp": ("revalidate", 0, 0)},
    ),
    ("vary-trailing-comma", OK,
     I(scc="max-age=60", vary="Accept,", now=1000030),
     {"exp": ("reuse", 60, 30)},
    ),
    ("vary-star-member", OK,
     I(scc="max-age=60", vary="Accept, *", now=1000030),
     {"exp": ("not-storable", None, None)},
    ),
    ("head-request-no-cache", OK,
     I(scc="max-age=60", method="HEAD", rcc="no-cache", now=1000030),
     {"exp": ("revalidate", 60, 30)},
    ),
    ("head-stored-no-store", OK,
     I(scc="no-store, max-age=60", method="HEAD", now=1000030),
     {"exp": ("not-storable", None, None)},
    ),
    ("smaxage-only-not-shared", OK,
     I(scc="s-maxage=100", now=1000050),
     {"exp": ("heuristic-undecided", None, 50)},
    ),
    ("smaxage-only-shared", OK,
     I(scc="s-maxage=100", now=1000050, shared=True),
     {"exp": ("reuse", 100, 50)},
    ),
    ("precedence-all-three", OK,
     I(scc="s-maxage=100, max-age=10", expires="999999", now=1000050, shared=True),
     {"exp": ("reuse", 100, 50)},
    ),
    ("private-quoted-shared", OK,
     I(scc='private="Authorization", max-age=60', now=1000030, shared=True),
     {"exp": ("not-storable", None, None)},
    ),
    ("private-quoted-not-shared", OK,
     I(scc='private="Authorization", max-age=60', now=1000030, shared=False),
     {"exp": ("reuse", 60, 30)},
    ),
    ("dup-directive-same-arg", OK,
     I(scc="max-age=60, max-age=60", now=1000030),
     {"exp": ("reuse", 60, 30)},
    ),
    ("dup-directive-case-differs", RF,
     I(scc="max-age=60, MAX-AGE=30", now=1000030),
     {"exp": None},
    ),
    ("max-age-signed-plus", RF,
     I(scc="max-age=+60", now=1000030), {"exp": None},
    ),
    ("max-age-signed-neg-zero", RF,
     I(scc="max-age=-0", now=1000030), {"exp": None},
    ),
    ("uppercase-directive", OK,
     I(scc="MAX-AGE=60", now=1000030),
     {"exp": ("reuse", 60, 30)},
    ),
    ("tab-padded-cc", OK,
     I(scc="\tmax-age=60 ", now=1000030),
     {"exp": ("reuse", 60, 30)},
    ),
    ("directive-empty-name", RF,
     I(scc="=60", now=1000030),
     {"exp": None, "alt": ("heuristic-undecided", None, 30),
      "why": "contract has no nameless-directive clause; refusal is the reference posture"},
    ),
    ("quoted-arg-with-comma", OK,
     I(scc='private="a, b", max-age=60', now=1000030, shared=True),
     {"exp": ("not-storable", None, None),
     "why": "clause 4 splits on ',' inside the quoted arg; 'private=\"a' still names private"},
    ),
    ("request-max-age-stale-by-one", OK,
     I(scc="max-age=60", rcc="max-age=30", now=1000031),
     {"exp": ("revalidate", 60, 31)},
    ),
    ("request-max-age-zero-boundary", OK,
     I(scc="max-age=60", rcc="max-age=0", now=1000000),
     {"exp": ("reuse", 60, 0)},
    ),
    ("min-fresh-precedes-max-stale", OK,
     I(scc="max-age=60", rcc="max-stale=100, min-fresh=10", now=1000065),
     {"exp": ("revalidate", 60, 65)},
    ),
    ("only-if-cached-serve-stale", OK,
     I(scc="max-age=60", rcc="max-stale=10, only-if-cached", now=1000065),
     {"exp": ("only-if-cached-miss", 60, 65)},
    ),
    ("only-if-cached-heuristic", OK,
     I(rcc="only-if-cached", now=1000010),
     {"exp": ("only-if-cached-miss", None, 10)},
    ),
    ("min-fresh-heuristic-order", OK,
     I(rcc="min-fresh=10", now=1000010),
     {"exp": ("heuristic-undecided", None, 10)},
    ),
    ("negative-lifetime-max-stale", OK,
     I(expires="999900", rcc="max-stale", now=1000000, scc=None),
     {"exp": ("serve-stale", -100, 0)},
    ),
    ("method-lowercase-head", OK,
     I(scc="max-age=60", method="head", now=1000030),
     {"exp": ("not-storable", None, None)},
    ),
    ("method-trailing-space", OK,
     I(scc="max-age=60", method="GET ", now=1000030),
     {"exp": ("not-storable", None, None)},
    ),
    ("now-zero-fresh", OK,
     I(scc="max-age=60", date="0", now=0),
     {"exp": ("reuse", 60, 0)},
    ),
    ("request-headers-absent", OK,
     I(scc="max-age=60", now=1000030, drop_request_headers=True),
     {"exp": ("reuse", 60, 30)},
    ),
    ("unknown-directive-quoted-arg", OK,
     I(scc='foo="bar", max-age=60', now=1000030),
     {"exp": ("reuse", 60, 30)},
    ),
    # --- refusals from validation clauses ---------------------------------
    ("lf-in-value", RF,
     I(scc="max-age=60", now=1000030), {"exp": None},
    ),
    ("nul-in-value", RF,
     I(scc="max-age=60", now=1000030), {"exp": None},
    ),
    ("status-99", RF,
     I(scc="max-age=60", status=99, now=1000030), {"exp": None},
    ),
    ("status-600", RF,
     I(scc="max-age=60", status=600, now=1000030), {"exp": None},
    ),
    ("shared-as-string", RF,
     I(scc="max-age=60", now=1000030, shared="true"), {"exp": None},
    ),
    ("missing-stored", RF,
     {"request": {"method": "GET", "headers": {}}, "now": 1000030}, {"exp": None},
    ),
    ("extra-stored-key", RF,
     I(scc="max-age=60", now=1000030, stored_extra={"ttl": 5}),
     {"exp": None, "alt": ("reuse", 60, 30),
      "why": "contract says 'exactly these keys' for the top level only; stored shape is shown, not declared exact"},
    ),
    ("stored-headers-absent", RF,
     I(scc="max-age=60", now=1000030, stored_headers=False), {"exp": None},
    ),
    ("date-non-integer", RF,
     I(scc="max-age=60", date="abc", now=1000030), {"exp": None},
    ),
    ("min-fresh-quoted", RF,
     I(scc="max-age=60", rcc='min-fresh="20"', now=1000030), {"exp": None},
    ),
    ("smaxage-quoted-shared", RF,
     I(scc='s-maxage="100"', now=1000050, shared=True), {"exp": None},
    ),
    ("date-ows-trimmed", OK,
     I(scc="max-age=60", date=" 1000000 ", now=1000030),
     {"exp": ("reuse", 60, 30)},
    ),
    ("shared-absent-default", OK,
     {"stored": {"status": 200, "headers": {"Date": "1000000",
                                            "Cache-Control": "max-age=60"}},
      "request": {"method": "GET", "headers": {}}, "now": 1000030},
     {"exp": ("reuse", 60, 30)},
    ),
    ("shared-absent-smaxage-untaken", OK,
     {"stored": {"status": 200, "headers": {"Date": "1000000",
                                            "Cache-Control": "s-maxage=100"}},
      "request": {"method": "GET", "headers": {}}, "now": 1000050},
     {"exp": ("heuristic-undecided", None, 50)},
    ),
    ("header-value-json-number", RF,
     {"stored": {"status": 200, "headers": {"Date": "1000000",
                                            "Cache-Control": "max-age=60",
                                            "X-Note": 5}},
      "request": {"method": "GET", "headers": {}}, "now": 1000030},
     {"exp": None},
    ),
    ("header-value-bool", RF,
     {"stored": {"status": 200, "headers": {"Date": "1000000",
                                            "Cache-Control": "max-age=60",
                                            "X-Note": True}},
      "request": {"method": "GET", "headers": {}}, "now": 1000030},
     {"exp": None},
    ),
    ("header-value-null", RF,
     {"stored": {"status": 200, "headers": {"Date": "1000000",
                                            "Cache-Control": "max-age=60",
                                            "X-Note": None}},
      "request": {"method": "GET", "headers": {}}, "now": 1000030},
     {"exp": None},
    ),
]

# value-level CR/LF/NUL payloads are built here so the JSON stays readable
for name in ("lf-in-value", "nul-in-value"):
    for i, (n, k, inp, exp) in enumerate(CASES):
        if n == name:
            payload = "a\nb" if name == "lf-in-value" else "a\x00b"
            h = inp["stored"]["headers"]
            h["X-Note"] = payload
            inp["stored"]["headers"] = h


VOCAB = {"reuse", "revalidate", "serve-stale", "must-revalidate-fail",
         "not-storable", "heuristic-undecided", "only-if-cached-miss"}


def check_success(got, exp_triple):
    problems = []
    if not isinstance(got, dict):
        return ["stdout is not a JSON object: %r" % (type(got).__name__,)]
    if set(got) != {"decision", "freshness_lifetime", "current_age"}:
        problems.append("key set %r" % (sorted(got),))
    d = got.get("decision")
    if not isinstance(d, str) or d not in VOCAB:
        problems.append("decision %r not in vocabulary" % (d,))
    for k in ("freshness_lifetime", "current_age"):
        v = got.get(k)
        absent = k not in got
        if isinstance(v, bool) or (v is not None and not isinstance(v, int)):
            problems.append("%s type %s (bool-or-not-int)" % (k, type(v).__name__))
    if not problems and (got["decision"], got["freshness_lifetime"],
                         got["current_age"]) != exp_triple:
        problems.append("triple %r != hand %r" % (
            (got["decision"], got["freshness_lifetime"], got["current_age"]),
            exp_triple))
    return problems


def run_reference(counter_path):
    spec = importlib.util.spec_from_file_location("c91r", counter_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    agree = disagree = 0
    lines = []
    for name, kind, inp, exp in CASES:
        try:
            got = mod.reference(inp)
            got_triple = (got["decision"], got["freshness_lifetime"], got["current_age"])
        except mod.Invalid as exc:
            got_triple = ("refusal: %s" % exc,)
        if "alt" in exp:
            strict_refusal = got_triple[0].startswith("refusal:")
            if exp["exp"] is None and strict_refusal:
                state = "AMBIG-strict-agree(refusal)"
                agree += 1
            elif got_triple == exp["exp"]:
                state = "AMBIG-strict-agree"
                agree += 1
            elif got_triple == exp["alt"]:
                state = "AMBIG-alt-agree"
                agree += 1
            else:
                state = "AMBIG-neither"
                disagree += 1
            lines.append("%-34s %s got=%r strict=%r alt=%r" % (
                name, state, got_triple, exp["exp"], exp["alt"]))
        elif kind == OK:
            if got_triple == exp["exp"]:
                state = "AGREE"
                agree += 1
            else:
                state = "DISAGREE"
                disagree += 1
            lines.append("%-34s %s got=%r hand=%r" % (name, state, got_triple, exp["exp"]))
        else:
            if got_triple[0].startswith("refusal:"):
                state = "AGREE-refusal"
                agree += 1
                lines.append("%-34s %s got=%r" % (name, state, got_triple))
            else:
                state = "DISAGREE-decided"
                disagree += 1
                lines.append("%-34s %s got=%r hand=refusal" % (name, state, got_triple))
    return agree, disagree, lines


def run_subject(path, work):
    agree = disagree = protocol_notes = 0
    lines = []
    for name, kind, inp, exp in CASES:
        d = tempfile.mkdtemp(prefix="rr-", dir=work)
        try:
            p = subprocess.run([sys.executable, "-B", path],
                               input=json.dumps(inp).encode(), cwd=d,
                               capture_output=True, timeout=60)
        finally:
            shutil.rmtree(d, ignore_errors=True)
        out = p.stdout.decode("utf-8", "replace")
        err = p.stderr.decode("utf-8", "replace")
        if "alt" in exp:
            strict_refusal = p.returncode == 1 and out == "" and err.startswith("invalid_input:")
            if exp["exp"] is None:
                if strict_refusal:
                    agree += 1
                    lines.append("%-34s AMBIG-strict-agree(refusal)" % name)
                else:
                    try:
                        got = json.loads(out)
                        got_triple = (got.get("decision"), got.get("freshness_lifetime"),
                                      got.get("current_age"))
                    except ValueError:
                        got_triple = ("unparseable",)
                    if got_triple == exp["alt"]:
                        agree += 1
                        lines.append("%-34s AMBIG-alt-agree" % name)
                    else:
                        disagree += 1
                        lines.append("%-34s AMBIG-neither got=%r" % (name, got_triple))
            else:
                problems = []
                if p.returncode != 0:
                    problems.append("rc=%d" % p.returncode)
                else:
                    try:
                        got = json.loads(out)
                    except ValueError:
                        problems.append("stdout not JSON: %r" % out[:60])
                        got = None
                    if got is not None:
                        problems += check_success(got, exp["exp"])
                if problems:
                    try:
                        got = json.loads(out)
                        alt_triple = (got.get("decision"), got.get("freshness_lifetime"),
                                      got.get("current_age"))
                    except ValueError:
                        alt_triple = None
                    if alt_triple == exp["alt"]:
                        agree += 1
                        lines.append("%-34s AMBIG-alt-agree" % name)
                    else:
                        disagree += 1
                        lines.append("%-34s AMBIG-neither %s" % (name, "; ".join(problems)))
                else:
                    agree += 1
                    lines.append("%-34s AMBIG-strict-agree" % name)
            continue
        if kind == RF:
            problems = []
            if p.returncode != 1:
                problems.append("rc=%d" % p.returncode)
            if out != "":
                problems.append("stdout not empty: %r" % out[:60])
            if not err.startswith("invalid_input:"):
                problems.append("stderr %r" % err[:60])
            elif err.strip() == "invalid_input:":
                problems.append("note: empty reason after prefix (counter-tolerated)")
            if problems:
                disagree += 1
                lines.append("%-34s DISAGREE %s" % (name, "; ".join(problems)))
            else:
                agree += 1
                lines.append("%-34s AGREE-refusal reason=%r" % (name, err.strip()[:80]))
        else:
            problems = []
            if p.returncode != 0:
                problems.append("rc=%d stderr=%r" % (p.returncode, err.strip()[:80]))
            else:
                try:
                    got = json.loads(out)
                except ValueError:
                    problems.append("stdout not JSON: %r" % out[:60])
                    got = None
                if got is not None:
                    problems += check_success(got, exp["exp"])
            if problems:
                disagree += 1
                lines.append("%-34s DISAGREE %s" % (name, "; ".join(problems)))
            else:
                agree += 1
                lines.append("%-34s AGREE %r" % (name, exp["exp"]))
    return agree, disagree, protocol_notes, lines


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["reference", "subject"], required=True)
    ap.add_argument("--counter", default=None)
    ap.add_argument("--subject", default=None)
    ap.add_argument("--work", default=None)
    a = ap.parse_args()
    if a.mode == "reference":
        agree, disagree, lines = run_reference(a.counter)
        for ln in lines:
            print(ln)
        print("SUMMARY reference agree=%d disagree=%d of %d" % (agree, disagree, len(CASES)))
        return 0 if disagree == 0 else 1
    agree, disagree, notes, lines = run_subject(a.subject, a.work)
    for ln in lines:
        print(ln)
    print("SUMMARY subject agree=%d disagree=%d protocol_notes=%d of %d"
          % (agree, disagree, notes, len(CASES)))
    return 0 if disagree == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
