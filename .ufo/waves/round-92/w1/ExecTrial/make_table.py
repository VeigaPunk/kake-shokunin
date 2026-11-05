#!/usr/bin/env python3
"""ExecTrial-6: render trial.txt from inputs.index.json + outputs/summary.json.

EXPECTED below is the hand derivation from the frozen contract text
(.ufo/waves/round-92/c2-contract.md, decision order clauses 9-13, first match
wins), written down BEFORE the instrument ran. It is a trial cross-check, not
a second oracle: any disagreement is reported, never reconciled by editing
either side.
"""
import hashlib
import json
import os

LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
SEAT = os.path.join(LANE, ".ufo/waves/round-92/w1/ExecTrial")

EXPECTED = {
    "r61-burnerchrome-kimi": ("not-storable", None, False, "c9 no-store"),
    "r61-charter-ghp": ("explicit", 600, False, "c10 max-age=600 (shadows Expires)"),
    "r61-charter-kimi": ("heuristic-undecided", None, False, "c11 404 cacheable, no explicit; c13 Last-Modified absent"),
    "r61-ds4cc-kimi": ("not-storable", None, False, "c9 no-store"),
    "r61-ds4cc-primary": ("explicit", 600, False, "c10 max-age=600 (shadows Expires)"),
    "r61-lucario-ghp": ("explicit", 600, False, "c10 max-age=600 (shadows Expires)"),
    "r61-lucario-kimi": ("heuristic-undecided", None, False, "c11 404 cacheable, no explicit; c13 Last-Modified absent"),
    "r61-plazir15-ghp": ("explicit", 600, False, "c10 max-age=600 (shadows Expires)"),
    "r61-plazir15-kimi": ("heuristic-undecided", None, False, "c11 404 cacheable, no explicit; c13 Last-Modified absent"),
    "r61-plazir27-kimi": ("heuristic-undecided", None, False, "c11 404 cacheable, no explicit; c13 Last-Modified absent"),
    "r61-ufo-fsd-kimi-pro": ("not-storable", None, False, "c9 no-store"),
    "r61-vault-index-kimi": ("not-storable", None, False, "c9 no-store"),
    "r81-ds4cc-primary": ("explicit", 600, False, "c10 max-age=600 (shadows Expires)"),
    "r81-ds4cc-robots": ("explicit", 600, False, "c10 max-age=600 (shadows Expires)"),
    "r81-ds4cc-sitemap": ("explicit", 600, False, "c10 max-age=600 (shadows Expires)"),
    "r82-ds4cc-primary": ("explicit", 600, False, "c10 max-age=600 (shadows Expires)"),
    "r82-ds4cc-robots": ("explicit", 600, False, "c10 max-age=600 (shadows Expires)"),
    "r82-ds4cc-sitemap": ("explicit", 600, False, "c10 max-age=600 (shadows Expires)"),
}


def main():
    idx = {r["surface"]: r for r in json.load(open(os.path.join(SEAT, "inputs.index.json")))}
    summ = json.load(open(os.path.join(SEAT, "outputs", "summary.json")))
    env = dict(line.split("=", 1) for line in
               open(os.path.join(SEAT, "trial.env")).read().splitlines() if "=" in line)
    instr_digest = summ["summary"]["instrument_sha256"]
    lines = []
    a = lines.append
    a("kake round 92 w1 / seat ExecTrial-6 -- heuristic freshness instrument trial on recorded domain bytes")
    a("trial, not a claim: exercises the delivered instrument; admits nothing about any live cache")
    a("")
    a("lane head           : %s" % env.get("lane_head"))
    a("freeze revision     : %s" % env.get("freeze_rev"))
    a("instrument          : scripts/heuristic_freshness.py")
    a("instrument sha256   : %s (%d bytes)" % (instr_digest, summ["summary"]["instrument_bytes"]))
    a("instrument committed: %s" % (env.get("instrument_committed") or "no (worktree bytes during wave, bound by digest above)"))
    a("python              : %s" % env.get("python"))
    a("run at (UTC)        : %s" % env.get("utc"))
    a("population          : %d recorded surfaces = 12 x round-61/capture + 3 x round-81/capture + 3 x round-82/capture" % summ["summary"]["surfaces"])
    a("")
    a("Replay (from LANE=/home/vgpnk/Projects/shokunin/kake-shokunin, stdlib-only, no network):")
    a("  python3 -B .ufo/waves/round-92/w1/ExecTrial/build_inputs.py   # rebuilds inputs/ from the capture trees")
    a("  python3 -B .ufo/waves/round-92/w1/ExecTrial/run_trial.py      # runs the instrument once per input, captures outputs/")
    a("")
    a("Per-surface: decision | lifetime | heuristic | recorded headers the decision rests on (as recorded;")
    a("HTTP-dates shown verbatim, epoch in inputs.index.json). EXP = hand-derived from the frozen")
    a("contract before the run; AGREE = instrument vs EXP.")
    a("")
    hdr = "{:<22} {:>5} {:<26} {:>8} {:<5} {:<5} {}".format(
        "surface", "st", "decision", "lifetime", "heur", "agree", "basis (recorded headers) / EXP clause")
    a(hdr)
    a("-" * len(hdr))
    agree_n = 0
    for row in sorted(summ["rows"], key=lambda r: r["surface"]):
        sid = row["surface"]
        r = idx[sid]
        rt = r["recorded_tracked"]
        if row["exit"] == 0:
            d = row["decision"]
            dec, life, heur = d["decision"], d["lifetime"], d["heuristic"]
        else:
            dec, life, heur = "REFUSAL", None, None
        exp_dec, exp_life, exp_heur, exp_why = EXPECTED[sid]
        agree = (dec == exp_dec and life == exp_life and heur == exp_heur)
        agree_n += agree
        basis = "; ".join(
            "%s: %s" % (k, ", ".join("%s" % v for v in rt[k]))
            for k in ("cache-control", "expires", "last-modified", "vary", "date")
            if k in rt)
        a("{:<22} {:>5} {:<26} {:>8} {:<5} {:<5} {}".format(
            sid, r["status"], dec, "-" if life is None else life,
            "-" if heur is None else str(heur).lower(), "yes" if agree else "NO",
            basis))
        a("{:<22} {:>5} {:<26} {:>8} {:<5} {:<5} EXP: {} -> {}, {}, {}".format(
            "", "", "", "", "", "", exp_why, exp_dec,
            "-" if exp_life is None else exp_life, str(exp_heur).lower()))
        if row["exit"] != 0:
            a("{:<22} stderr: {}".format("", row.get("stderr", "")))
    a("")
    a("totals: surfaces=%d exit0=%d refused=%d agree_with_pre_run_contract_derivation=%d/%d"
      % (summ["summary"]["surfaces"], summ["summary"]["exit0"], summ["summary"]["refused"],
         agree_n, len(EXPECTED)))
    open(os.path.join(SEAT, "trial.txt"), "w").write("\n".join(lines) + "\n")
    print("wrote trial.txt agree=%d/%d refused=%d" % (agree_n, len(EXPECTED), summ["summary"]["refused"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
