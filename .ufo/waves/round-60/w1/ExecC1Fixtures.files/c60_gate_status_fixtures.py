#!/usr/bin/env python3
"""c60_gate_status_fixtures.py - independent fixture harness for the round-60 C1 gate.

Builds small fixture *lanes* (git repos) in scratch and runs ANY candidate C1
counter against them:

    python3 -B <counter> --root <fixture> --revision <tip-sha> --work <dir>

Each fixture reproduces the round-60 contract Claim-C1 surface:

  * a committed population of round 48-59 member counters
    (regex  ^\\.ufo/waves/round-(N)/(?:[a-z0-9-]+/)?c(N)_[a-z0-9_]+\\.py$  - the
    optional inner segment is ONE directory component without slashes; the two
    Ns must agree and satisfy 48 <= N <= 59),
  * a SKILL.md whose qualifying registry table has the header
    | Name | Kind | Entry command | Verdict map | Self-test | Pinned values / frozen proof | Write scope | Owner |
    (first three cells Name/Kind/Entry command as the contract requires, 8
    non-empty cells per row, `Verdict map` cell carrying `0=` and `1=`),
  * a SCORECARD.md axis table | Axis | Score | Evidence pointer | Last change |
    with operability 10 / freshness 10 / calibration 2.

Fixture history model: two commits on `main`. Commit 1 (the PIN commit) holds
every member file at its pin-time body. Commit 2 (the TIP commit, measured)
holds the registry, the scorecard and every member whose tip body differs.
Members labelled historical / never-met carry a Kind cell whose first 40-hex
is the PIN commit sha - a real ancestor of the tip. e_P semantics: per the
contract, the same entry command runs "with the pin substituted", i.e. the
TIP-tree counter file is invoked with the pin revision in its arguments (the
clone is always detached at the measured revision). Toy bodies are written so
that BOTH this reading and the weaker "run the pin-tree file" reading give the
intended exit wherever the two can be made to agree; where they cannot, the
contract reading is used.

Expected contract output (checked by the harness):
  * exit 0 iff met, 1 iff at least one mismatch, 2 iff unevaluable, 64 usage,
  * every mismatch line carries one of the contract's class tokens verbatim:
    unregistered, duplicate_row, row_incomplete, unpinned, pin_not_ancestor,
    command_unparsable, live_not_green, historical_but_green,
    historical_not_green_at_pin, never_met_but_green - or `scores_held` when an
    axis-table score differs from 10/10/2.

Usage:
    python3 -B c60_gate_status_fixtures.py --counter <path> [--work <scratch>]
                                         [--timeout 300] [--json]
    python3 -B c60_gate_status_fixtures.py --selfcheck [--work <scratch>]
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

PER_MEMBER_CLASSES = [
    "unregistered", "duplicate_row", "row_incomplete", "unpinned",
    "pin_not_ancestor", "command_unparsable",
    "live_not_green", "historical_but_green", "historical_not_green_at_pin",
    "never_met_but_green",
]
ALL_CLASSES = PER_MEMBER_CLASSES + ["scores_held"]

FLEET_ROOT = "/home/vgpnk/Projects/shokunin"

# The real round 48-59 population at the round-60 base (paths mirrored).
POPULATION = [
    ".ufo/waves/round-48/c48_lint_count.py",
    ".ufo/waves/round-48/c48_quote_truth.py",
    ".ufo/waves/round-49/c49_order.py",
    ".ufo/waves/round-49/c49_quote_truth.py",
    ".ufo/waves/round-50/c50_durable.py",
    ".ufo/waves/round-50/c50_quote_class.py",
    ".ufo/waves/round-51/c51_quote_truth.py",
    ".ufo/waves/round-51/c51_wave_ledger.py",
    ".ufo/waves/round-52/c52_gate_registry.py",
    ".ufo/waves/round-52/c52_mutation_ladder.py",
    ".ufo/waves/round-52/c52_quote_truth.py",
    ".ufo/waves/round-52/c52_wave_ledger.py",
    ".ufo/waves/round-53/exec-quality-gate/c53_gate_truth.py",
    ".ufo/waves/round-54/c54_ops_debt.py",
    ".ufo/waves/round-54/c54_s374_calib.py",
    ".ufo/waves/round-55/c55_quote_truth.py",
    ".ufo/waves/round-55/c55_readme_index.py",
    ".ufo/waves/round-56/c56_quote_truth.py",
    ".ufo/waves/round-56/c56_selftally.py",
    ".ufo/waves/round-57/c57_idresolver_gate.py",
    ".ufo/waves/round-57/c57_quote_truth.py",
    ".ufo/waves/round-57/c57_receipt_pins.py",
    ".ufo/waves/round-58/c58_quote_truth.py",
    ".ufo/waves/round-58/c58_receipt_rewrites.py",
    ".ufo/waves/round-58/c58_resolver_cases.py",
    ".ufo/waves/round-59/c59_axis_evidence.py",
    ".ufo/waves/round-59/c59_quote_truth.py",
    ".ufo/waves/round-59/c59_resolver_cases.py",
]

# Toy member bodies -----------------------------------------------------------

B_EXIT0 = "import sys\nsys.exit(0)\n"
B_EXIT1 = "import sys\nsys.exit(1)\n"
B_EXIT2 = "import sys\nsys.exit(2)\n"
B_EXIT124 = "import sys\nsys.exit(124)\n"

# Green iff an argument equal to the clone's HEAD (the substituted revision) is
# present. Used for every placeholder / env probe.
B_HEAD_ARG = (
    "import subprocess,sys\n"
    "head=subprocess.check_output(['git','rev-parse','HEAD']).decode().strip()\n"
    "sys.exit(0 if head in sys.argv[1:] else 1)\n"
)

# Green iff the pin sha arrives among argv (tip-tree body; {pin} substituted at
# write time). e_P -> 0, e_T -> 1 under the contract reading.
B_PIN_OK = "import sys\nsys.exit(0 if '{pin}' in sys.argv[1:] else 1)\n"

# Green iff substituted <rev> arrives as `--rev <sha>` and that sha is HEAD.
B_BRACKET_KEPT = (
    "import subprocess,sys\n"
    "head=subprocess.check_output(['git','rev-parse','HEAD']).decode().strip()\n"
    "sys.exit(0 if len(sys.argv)==3 and sys.argv[1]=='--rev' "
    "and sys.argv[2]==head else 1)\n"
)

# Green iff an env word arrived AND its substituted value is HEAD.
B_ENV_HEAD = (
    "import os,subprocess,sys\n"
    "head=subprocess.check_output(['git','rev-parse','HEAD']).decode().strip()\n"
    "sys.exit(0 if os.environ.get('GATE_FIX_FLAG')==head else 1)\n"
)

B_ENV_LITERAL = (
    "import os,sys\n"
    "sys.exit(0 if os.environ.get('GATE_FIX_ENV')=='1' "
    "and os.environ.get('GATE_FIX_FLAG')=='ok' else 1)\n"
)

# Green iff a scratch dir argument that is an absolute existing dir arrives.
B_SCRATCH_ARG = (
    "import os,sys\n"
    "sys.exit(0 if any(os.path.isabs(a) and os.path.isdir(a) "
    "for a in sys.argv[1:]) else 1)\n"
)

# Green iff the literal fleet-root path is passed through untouched.
B_FLEET_ARG = (
    "import sys\n"
    f"sys.exit(0 if '{FLEET_ROOT}' in sys.argv[1:] else 1)\n"
)

SKILL_TABLE_HEADER = (
    "| Name | Kind | Entry command | Verdict map | Self-test | "
    "Pinned values / frozen proof | Write scope | Owner |\n"
    "|---|---|---|---|---|---|---|---|\n"
)
VMAP = "`0=met`; `1=not met`; `2=unevaluable`; `64=usage`"
SELFTEST = "`python3 -B {path} --selftest`"
PINNED = "fixture pin"
SCOPE = "read-only"
OWNER = "kake"

SCORECARD_HEAD = (
    "# fixture-shokunin - Scorecard\n\n"
    "| Axis | Score | Evidence pointer | Last change |\n"
    "|---|---|---|---|\n"
)


def scrub_env():
    env = dict(os.environ)
    for k in list(env):
        if k.startswith("GIT_"):
            env.pop(k)
    return env


def git(repo, *args, check=True):
    r = subprocess.run(["git", "-C", str(repo), *args],
                       capture_output=True, text=True, env=scrub_env())
    if check and r.returncode != 0:
        raise RuntimeError(f"git {args} -> {r.returncode}: {r.stderr.strip()}")
    return r


def commit_all(repo, msg):
    git(repo, "add", "-A")
    git(repo, "-c", "user.name=selftest", "-c", "user.email=selftest@local",
        "commit", "-q", "--allow-empty", "-m", msg)


def write_file(repo, relpath, content):
    p = Path(repo) / relpath
    p.parent.mkdir(parents=True, exist_ok=True)
    if p.is_symlink():
        p.unlink()
    p.write_text(content)
    p.chmod(0o755)


def write_symlink(repo, relpath, target):
    p = Path(repo) / relpath
    if p.exists() or p.is_symlink():
        p.unlink()
    p.parent.mkdir(parents=True, exist_ok=True)
    os.symlink(target, p)


def fmt_cell(text, pin, tip, side):
    return (text.replace("{pin}", pin).replace("{tip}", tip)
                .replace("{side}", side))


class Member:
    """One population counter in a fixture lane.

    body     file content at the TIP commit ({pin}/{tip}/{side} substituted)
    pin_body file content at the PIN commit (must be brace-free; None -> body,
             which then must also be brace-free)
    kind     Kind cell text ({pin}/{tip}/{side} substituted)
    cmd      Entry command cell; None -> `python3 -B <path> --root . --revision <commit>`
    """

    def __init__(self, path, body=B_EXIT0, pin_body=None, kind="gate",
                 cmd=None, name=None):
        self.path = path
        self.body = body
        self.pin_body = pin_body
        self.kind = kind
        self.cmd = cmd
        self.name = name or Path(path).name

    def effective_pin_body(self):
        pb = self.pin_body if self.pin_body is not None else self.body
        assert "{" not in pb, f"{self.path}: pin-time body cannot embed {{}}"
        return pb


def default_cmd(path):
    return f"`python3 -B {path} --root . --revision <commit>`"


def registry_row(path, kind, cmd, pin, tip, side, vmap=VMAP, cells8=True):
    cells = [Path(path).name,
             fmt_cell(kind, pin, tip, side),
             fmt_cell(cmd if cmd is not None else default_cmd(path),
                      pin, tip, side),
             vmap,
             SELFTEST.format(path=path), PINNED, SCOPE, OWNER]
    if not cells8:
        cells = cells[:6]
    return "| " + " | ".join(cells) + " |"


def row(path, kind="gate", cmd=None, vmap=VMAP, cells8=True):
    """Row template (returns a thunk evaluated with known shas)."""
    def make(pin, tip, side):
        return registry_row(path, kind, cmd, pin, tip, side,
                            vmap=vmap, cells8=cells8)
    return make


def scorecard_md(spec):
    rows = spec.get("score_rows")
    if rows is None:
        s = {"op": 10, "fr": 10, "cal": 2}
        s.update(spec.get("scores", {}))
        rows = [("operability", s["op"]), ("freshness", s["fr"]),
                ("calibration", s["cal"])]
    out = [SCORECARD_HEAD]
    for axis, score in rows:
        out.append(f"| {axis} | {score} | evidence | r59 |\n")
    return "".join(out)


def skill_md(spec, pin, tip, side):
    members = spec["members"]
    drop = set(spec.get("drop_rows", []))
    rows = spec.get("rows", {})
    out = ["# fixture-shokunin - SKILL\n\n",
           "### Round 48-59 gate registry\n\n", SKILL_TABLE_HEADER]
    for m in members:
        if m.path in drop:
            continue
        if m.path in rows:
            for thunk in rows[m.path]:
                out.append(thunk(pin, tip, side) + "\n")
        else:
            out.append(registry_row(m.path, m.kind, m.cmd, pin, tip, side)
                       + "\n")
    for thunk in spec.get("extra_rows", []):
        out.append(thunk(pin, tip, side) + "\n")
    out.append("\n")
    for header, table_rows in spec.get("extra_tables", []):
        out.append(header + "\n")
        for thunk in table_rows:
            out.append(thunk(pin, tip, side) + "\n")
        out.append("\n")
    if spec.get("extra_md"):
        out.append(fmt_cell(spec["extra_md"], pin, tip, side) + "\n")
    return "".join(out)


def build_fixture(spec, repo):
    """Build a fixture lane; return (repo, tip, pin, side)."""
    repo = Path(repo)
    repo.mkdir(parents=True, exist_ok=True)
    git(repo, "init", "-q", "-b", "main")
    top = git(repo, "rev-parse", "--show-toplevel").stdout.strip()
    assert top == str(repo), f"toplevel {top} != {repo}"

    # Side commit guaranteed NOT to be an ancestor of the tip: a dangling
    # empty-tree commit with no parent and no branch.
    side = git(repo, "-c", "user.name=selftest",
               "-c", "user.email=selftest@local", "commit-tree",
               "4b825dc642cb6eb9a060e54bf8d69288fbee4904", "-m",
               "side").stdout.strip()

    members = spec.get("members") or [Member(p) for p in POPULATION]
    spec["members"] = members

    # ---- pin commit: every member file at its pin body + noise
    for m in members:
        write_file(repo, m.path, m.effective_pin_body())
    for path, body in spec.get("noise", []):
        write_file(repo, path, body)
    commit_all(repo, "pin")
    pin = git(repo, "rev-parse", "HEAD").stdout.strip()

    # ---- tip commit: differing bodies, registry, scorecard, links, edits
    for m in members:
        if m.body != m.effective_pin_body():
            write_file(repo, m.path, fmt_cell(m.body, pin, tip="0" * 40,
                                              side=side))
    for path, body in spec.get("tip_edits", {}).items():
        write_file(repo, path, fmt_cell(body, pin, "0" * 40, side))
    for path, target in spec.get("tip_links", {}).items():
        write_symlink(repo, path, target)
    for path in spec.get("deletions", []):
        p = repo / path
        if p.exists() or p.is_symlink():
            p.unlink()
    if not spec.get("skill_absent"):
        write_file(repo, "SKILL.md",
                   spec.get("skill") or skill_md(spec, pin, "0" * 40, side))
    if not spec.get("scorecard_absent"):
        write_file(repo, "SCORECARD.md", scorecard_md(spec))
    commit_all(repo, "tip")
    tip = git(repo, "rev-parse", "HEAD").stdout.strip()
    return str(repo), tip, pin, side

# --- case table ---------------------------------------------------------------
# (id, spec_fn, expect_exit, expect_classes, allow_classes, note)
# expect_classes must appear in stdout+stderr; every other class token is
# forbidden unless listed in allow_classes. expect_exit 2/64 need no classes.

CASES = []


def case(cid, spec_fn, expect_exit, expect=(), allow=(), note=""):
    CASES.append(dict(id=cid, spec_fn=spec_fn, expect_exit=expect_exit,
                      expect=list(expect), allow=list(allow), note=note))


def S(**kw):
    return kw


def members_swap(path_out, member_in):
    return [member_in if p == path_out else Member(p) for p in POPULATION]


HIST = ".ufo/waves/round-48/c48_lint_count.py"
NM = ".ufo/waves/round-49/c49_order.py"
M50 = ".ufo/waves/round-50/c50_durable.py"


def hist(kind_hist="gate (historical: green at its measured revision `{pin}` "
                  "only; red on later trees by design)",
         body=B_PIN_OK, pin_body=B_EXIT0, path=HIST, **kw):
    return Member(path, body=body, pin_body=pin_body, kind=kind_hist, **kw)


def nm(kind_nm="gate (never met: red at its measured revision `{pin}` and at "
              "every later tree)",
       body=B_EXIT1, pin_body=B_EXIT1, path=NM, **kw):
    return Member(path, body=body, pin_body=pin_body, kind=kind_nm, **kw)


def spec_replace(*overrides):
    over = {m.path: m for m in overrides}
    return S(members=[over.get(p, Member(p)) for p in POPULATION])


# ---- population / boundary ---------------------------------------------------

case("met_baseline", lambda: S(), 0,
     note="28 live members, all registered, all green -> met")

case("met_subdir_member",
     lambda: S(members=members_swap(
         ".ufo/waves/round-53/exec-quality-gate/c53_gate_truth.py",
         Member(".ufo/waves/round-53/sub/c53_gate_truth.py"))),
     0, note="one-level [a-z0-9-]+ subdir member must count (28 total)")

case("met_boundary_noise",
     lambda: S(noise=[
        (".ufo/waves/round-47/c47_old.py", B_EXIT0),
        (".ufo/waves/round-47/sub/c47_x.py", B_EXIT0),
        (".ufo/waves/round-60/c60_gate_status.py", B_EXIT0),
        (".ufo/waves/round-60/c60_x.py", B_EXIT0),
        (".ufo/waves/round-60/sub/c60_x.py", B_EXIT0),
        (".ufo/waves/round-53/a/b/c53_x.py", B_EXIT0),
        (".ufo/waves/round-53/under_score/c53_x.py", B_EXIT0),
        (".ufo/waves/round-53/c53_UPPER.py", B_EXIT0),
        (".ufo/waves/round-53/c53_tool.PY", B_EXIT0),
        (".ufo/waves/round-53/c53_.py", B_EXIT0),
        ("scripts/c53_not_a_counter.py", B_EXIT0),
        (".ufo/waves/round-5/c5_x.py", B_EXIT0),
     ]),
     0,
     note="28 members + 12 committed non-member paths; counting any noise "
          "breaks members==28 or adds unregistered rows")

case("met_phantom_row",
     lambda: S(extra_rows=[row(".ufo/waves/round-53/c53_ghost.py")]),
     0, note="registry row for an UNCOMMITTED member-shaped path is ignored "
             "(population is committed paths, not rows)")

case("member_symlink",
     lambda: S(noise=[(".ufo/waves/round-53/c53_link_target.py", B_EXIT0)],
               tip_links={".ufo/waves/round-53/exec-quality-gate/"
                          "c53_gate_truth.py": "../c53_link_target.py"}),
     0, note="member path is a committed symlink -> still a committed path; "
             "python3 resolves it at run time. [contract-silent: non-blob "
             "members]")

# ---- structural row classes --------------------------------------------------

case("unregistered",
     lambda: S(drop_rows={".ufo/waves/round-51/c51_wave_ledger.py"}),
     1, expect=("unregistered",))

case("duplicate_row",
     lambda: S(extra_rows=[row(M50)]),
     1, expect=("duplicate_row",))

case("row_incomplete_cells",
     lambda: S(rows={M50: [row(M50, cells8=False)]}),
     1, expect=("row_incomplete",),
     note="row with 6 cells < 8 non-empty -> row_incomplete")

case("row_incomplete_vmap",
     lambda: S(rows={M50: [row(M50, vmap="`0:met`; `1:not met`")]}),
     1, expect=("row_incomplete",),
     note="8 cells but Verdict map lacks `0=`/`1=`")

case("met_vmap_control",
     lambda: S(rows={M50: [row(M50)]}),
     0, note="control: literal 0=/1= verdict map stays green")

case("fenced_row_unregistered",
     lambda: S(drop_rows={M50},
               extra_md="```\n" +
               "| c50_durable.py | gate | `python3 -B " + M50 + "` | "
               "`0=met`; `1=not met` | s | p | r | k |\n```\n"),
     1, expect=("unregistered",),
     note="row inside a fenced code block does not count")

case("commented_row_unregistered",
     lambda: S(drop_rows={M50},
               extra_md="<!--\n" +
               "| c50_durable.py | gate | `python3 -B " + M50 + "` | "
               "`0=met`; `1=not met` | s | p | r | k |\n-->\n"),
     1, expect=("unregistered",),
     note="row inside an HTML comment does not count")

case("indented_row_unregistered",
     lambda: S(drop_rows={M50},
               extra_md="    | c50_durable.py | gate | `python3 -B " + M50 +
               "` | `0=met`; `1=not met` | s | p | r | k |\n"),
     1, expect=("unregistered",),
     note="4-space indented row = indented code block")

case("wrong_table_unregistered",
     lambda: S(drop_rows={M50},
               extra_tables=[("| A | B | C |\n|---|---|---|",
                              [row3 := (lambda p, t, s:
                               "| n | k | `python3 -B " + M50 + "` |")])]),
     1, expect=("unregistered",),
     note="row in a table whose first three cells are not Name/Kind/Entry "
          "command does not count")

case("wrong_cell_unregistered",
     lambda: S(rows={M50: [row(M50,
                     cmd="`python3 -B .ufo/waves/round-99/c99_ghost.py`")]}),
     1, expect=("unregistered",),
     note="row exists but its Entry command names a non-member path")

# ---- label parsing -----------------------------------------------------------

case("label_default_live",
     lambda: S(rows={M50: [row(M50, kind="gate")]}),
     0, note="Kind with neither word -> live; member green -> met")

case("label_nevermet_hyphen",
     lambda: S(rows={M50: [row(M50, kind="gate (never-met hyphen variant)")]}),
     0, note="'never-met' (hyphen) is not 'never met' -> live")

case("kind_both_words_hist_wins",
     lambda: spec_replace(hist(
         kind_hist="gate (historical `{pin}` and also never met)")),
     0,
     note="Kind carrying BOTH words: contract order puts 'historical' first; "
          "a never-met reading sees e_P==0 -> never_met_but_green -> exit 1",
     allow=("never_met_but_green",))

# ---- live observations -------------------------------------------------------

case("live_not_green",
     lambda: spec_replace(Member(".ufo/waves/round-51/c51_quote_truth.py",
                                 body=B_EXIT1)),
     1, expect=("live_not_green",))

case("live_exit2_not_green",
     lambda: spec_replace(Member(".ufo/waves/round-51/c51_quote_truth.py",
                                 body=B_EXIT2)),
     1, expect=("live_not_green",),
     note="member itself exiting 2 still counts as e_T != 0 -> live_not_green")

case("live_timeout_not_green",
     lambda: spec_replace(Member(".ufo/waves/round-51/c51_quote_truth.py",
                                 body=B_EXIT124)),
     1, expect=("live_not_green",),
     note="member exit 124 simulates the counter-side 1800s timeout path")

# ---- historical --------------------------------------------------------------

case("historical_met",
     lambda: spec_replace(hist()),
     0, note="historical: red at tip (argv lacks pin), green at pin")

case("historical_first_hex_pin",
     lambda: spec_replace(hist(
         kind_hist="gate (historical `{pin}` then `{side}`)")),
     0, allow=("pin_not_ancestor", "historical_not_green_at_pin"),
     note="Kind carries TWO 40-hex: 'the first one is the pin'; a last-hex "
          "reader picks a non-ancestor pin")

case("historical_but_green",
     lambda: spec_replace(hist(body=B_EXIT0, pin_body=B_EXIT0)),
     1, expect=("historical_but_green",),
     note="do-nothing control: relabelled a still-green counter historical")

case("historical_not_green_at_pin",
     lambda: spec_replace(hist(body=B_EXIT1, pin_body=B_EXIT1)),
     1, expect=("historical_not_green_at_pin",),
     note="fake pin: counter red at the pinned revision too")

case("unpinned_historical",
     lambda: spec_replace(hist(
         kind_hist="gate (historical: green at its old measured revision "
                   "only; red on later trees by design)",
         body=B_EXIT1, pin_body=B_EXIT1)),
     1, expect=("unpinned",),
     allow=("historical_not_green_at_pin", "pin_not_ancestor"),
     note="historical with no 40-hex in Kind -> unpinned")

case("pin_not_ancestor",
     lambda: spec_replace(hist(
         kind_hist="gate (historical: green at `{side}` only)",
         body="import sys\nsys.exit(0 if '{side}' in sys.argv[1:] else 1)\n",
         pin_body=B_EXIT1)),
     1, expect=("pin_not_ancestor",),
     allow=("historical_not_green_at_pin",),
     note="pin is a real 40-hex commit that is NOT an ancestor of the "
          "measured tip (unrelated orphan commit)")

# ---- never-met ---------------------------------------------------------------

case("never_met_clean",
     lambda: spec_replace(nm()),
     0, note="never met: red at tip and at pin -> consistent label")

case("never_met_but_green_tip",
     lambda: spec_replace(nm(body=B_EXIT0)),
     1, expect=("never_met_but_green",),
     note="e_T == 0 -> never_met_but_green")

case("never_met_but_green_pin",
     lambda: spec_replace(nm(body=B_PIN_OK, pin_body=B_EXIT0)),
     1, expect=("never_met_but_green",),
     note="e_P == 0 -> never_met_but_green")

case("unpinned_never_met",
     lambda: spec_replace(nm(
         kind_nm="gate (never met: red at its measured revision and at every "
                 "later tree)")),
     1, expect=("unpinned",),
     note="never met with no 40-hex in Kind -> unpinned")

# ---- command parsing ---------------------------------------------------------

case("command_unparsable_quote",
     lambda: S(rows={M50: [row(M50,
        cmd="`python3 -B .ufo/waves/round-50/c50_durable.py 'unbalanced`")]}),
     1, expect=("command_unparsable",),
     note="unbalanced quote -> not shlex-parsable")

case("command_unparsable_sh",
     lambda: S(rows={M50: [row(M50, cmd="`sh " + M50 + "`")]}),
     1, expect=("command_unparsable",),
     note="not run with python3")

case("command_unparsable_bashwrap",
     lambda: S(rows={M50: [row(M50,
        cmd="`bash -c 'python3 " + M50 + "'`")]}),
     1, expect=("command_unparsable",),
     note="python3 buried inside a bash -c wrapper is not 'runs m with python3'")

case("command_no_backtick",
     lambda: S(rows={M50: [row(M50,
        cmd="python3 -B .ufo/waves/round-50/c50_durable.py --root .")]}),
     1, expect=("command_unparsable",), allow=("unregistered",),
     note="no backtick span contains the path [contract-silent: which class]")

case("command_echo_span",
     lambda: S(rows={M50: [row(M50,
        cmd="`echo " + M50 + "` then `python3 -B " + M50 + "`")]}),
     1, expect=("command_unparsable",),
     note="first backtick span containing the path does not run it with python3")

# ---- placeholder substitution ------------------------------------------------

for tag in ("commit", "rev", "revision", "tip"):
    case(f"placeholder_{tag}",
         lambda tag=tag: S(
             rows={M50: [row(M50,
                   cmd=f"`python3 -B {M50} <{tag}>`")]},
             tip_edits={M50: B_HEAD_ARG}),
         0, note=f"<{tag}> -> measured revision; body asserts argv==HEAD")

case("placeholder_scratch",
     lambda: S(rows={M50: [row(M50,
                   cmd=f"`python3 -B {M50} --work <scratch>`")]},
               tip_edits={M50: B_SCRATCH_ARG}),
     0, note="<scratch> -> a fresh scratch dir (absolute, exists)")

case("placeholder_fleet_root",
     lambda: S(rows={M50: [row(M50,
                   cmd=f"`python3 -B {M50} --fleet <fleet root>`")]},
               tip_edits={M50: B_FLEET_ARG}),
     0, note="<fleet root> -> literal /home/vgpnk/Projects/shokunin")

case("bracket_kept",
     lambda: S(rows={M50: [row(M50,
                   cmd=f"`python3 -B {M50} [--rev <rev>]`")]},
               tip_edits={M50: B_BRACKET_KEPT}),
     0, note="[--rev <rev>] all-placeholder -> kept, brackets stripped")

case("bracket_dropped",
     lambda: S(rows={M50: [row(M50,
                   cmd=f"`python3 -B {M50} [--bogus]`")]},
               tip_edits={M50: B_EXIT0}),
     0, note="[--bogus] -> dropped entirely, no argv")

case("bracket_dropped_partial",
     lambda: S(rows={M50: [row(M50,
                   cmd=f"`python3 -B {M50} [--rev <rev> --bogus]`")]},
               tip_edits={M50: B_EXIT0}),
     0, note="one unknown <...> inside [] drops the whole segment")

case("env_words_literal",
     lambda: S(rows={M50: [row(M50,
                   cmd=f"`GATE_FIX_ENV=1 GATE_FIX_FLAG=ok python3 -B {M50}`")]},
               tip_edits={M50: B_ENV_LITERAL}),
     0, note="leading NAME=value words are env assignments")

case("env_words_substituted",
     lambda: S(rows={M50: [row(M50,
                   cmd=f"`GATE_FIX_FLAG=<rev> python3 -B {M50}`")]},
               tip_edits={M50: B_ENV_HEAD}),
     0, allow=("command_unparsable",),
     note="placeholder inside an env value [contract-silent: substitution "
          "scope]; reading A substitutes it")

case("extra_args_ok",
     lambda: S(rows={M50: [row(M50,
                   cmd=f"`python3 -B {M50} --root . --jobs 2 --json`")]}),
     0, note="extra plain flags pass through unchanged")

# ---- scores ------------------------------------------------------------------

case("score_cal_mutant",
     lambda: S(scores={"cal": 10}), 1, expect=("scores_held",),
     note="R59-D2 routed defect: calibration 2 -> 10 must fail")

case("score_op_mutant",
     lambda: S(scores={"op": 9}), 1, expect=("scores_held",),
     note="operability 10 -> 9 must fail")

case("score_row_missing",
     lambda: S(score_rows=[("operability", 10), ("freshness", 10)]),
     1, expect=("scores_held",), allow=("unevaluable",),
     note="calibration row absent -> scores_held == 2 -> not met")

# ---- unevaluable -------------------------------------------------------------

case("unevaluable_no_skill",
     lambda: S(skill_absent=True), 2,
     note="SKILL.md absent at the measured revision -> exit 2")

case("unevaluable_no_scorecard",
     lambda: S(scorecard_absent=True), 2,
     note="SCORECARD.md absent -> exit 2")

case("unevaluable_bad_rev",
     lambda: S(revision="0" * 40), 2,
     note="--revision names a commit the fixture does not contain -> exit 2")


# -----------------------------------------------------------------------------

def run_counter(counter, repo, rev, work, timeout):
    env = scrub_env()
    env["TMPDIR"] = str(work)
    cmd = [sys.executable, "-B", str(counter),
           "--root", str(repo), "--revision", rev, "--work", str(work)]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True,
                           timeout=timeout, env=env)
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except subprocess.TimeoutExpired as e:
        out = ""
        for part in (e.stdout, e.stderr):
            if part:
                out += part if isinstance(part, str) else part.decode("replace")
        return 137, f"HARNESS TIMEOUT after {timeout}s\n{out}"


def check_case(cs, counter, base_work, timeout):
    work = Path(tempfile.mkdtemp(prefix=cs["id"] + "-", dir=base_work))
    (work / "w").mkdir(parents=True)
    spec = cs["spec_fn"]()
    try:
        repo, tip, pin, side = build_fixture(spec, work / "lane")
    except Exception as e:
        return dict(id=cs["id"], ok=False, error=f"fixture-build: {e}")
    rev = spec.get("revision") or tip
    rc, out = run_counter(counter, repo, rev, work / "w", timeout)
    forbidden = [c for c in ALL_CLASSES
                 if c not in cs["expect"] and c not in cs["allow"]]
    missing = [c for c in cs["expect"] if c not in out]
    hit = [c for c in forbidden if c in out]
    ok = (rc == cs["expect_exit"] and not missing and not hit)
    return dict(id=cs["id"], ok=ok, exit=rc, expect_exit=cs["expect_exit"],
                missing=missing, forbidden=hit, note=cs["note"], tip=tip,
                pin=pin,
                tail=out.strip().splitlines()[-3:] if out.strip() else [])


def run_all(counter, base_work, timeout):
    results = []
    for cs in CASES:
        r = check_case(cs, counter, base_work, timeout)
        results.append(r)
        if "error" in r:
            status = "ERR"
        else:
            status = "PASS" if r["ok"] else "FAIL"
        print(f"{status} {r['id']}: exit={r.get('exit')} "
              f"expect={r.get('expect_exit')} miss={r.get('missing')} "
              f"forbidden={r.get('forbidden')}"
              + (f" ({r['error']})" if "error" in r else ""))
    passed = sum(1 for r in results if r.get("ok"))
    print(f"tally: {passed}/{len(CASES)} cases passed")
    return results, passed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--counter")
    ap.add_argument("--work", default=None)
    ap.add_argument("--timeout", type=int, default=300)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selfcheck", action="store_true")
    args = ap.parse_args()

    if args.selfcheck:
        base = Path(args.work or tempfile.mkdtemp(prefix="c60fix-sc-"))
        fx = base / "fx"
        fx.mkdir(parents=True, exist_ok=True)
        c0 = base / "counter_always0.py"
        c1 = base / "counter_always1.py"
        c0.write_text("import sys\nsys.exit(0)\n")
        c1.write_text("import sys\nsys.exit(1)\n")
        grand_ok = True
        for c in (c0, c1):
            results, passed = run_all(c, fx, args.timeout)
            print(f"SELFCHECK {c.name}: {passed}/{len(CASES)}")
            if c.name.endswith("always1.py") and passed != 0:
                grand_ok = False
            if c.name.endswith("always0.py") and passed == len(CASES):
                grand_ok = False
        return 0 if grand_ok else 1

    if not args.counter:
        ap.error("--counter required (or --selfcheck)")
    counter = Path(args.counter).resolve()
    base = Path(args.work or tempfile.mkdtemp(prefix="c60fix-"))
    fx = base / "fx"
    fx.mkdir(parents=True, exist_ok=True)
    results, passed = run_all(counter, fx, args.timeout)
    if args.json:
        print(json.dumps(results, indent=1))
    return 0 if passed == len(CASES) else 1


if __name__ == "__main__":
    sys.exit(main())
