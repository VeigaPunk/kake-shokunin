#!/usr/bin/env python3
"""Round-73 C2 counter — stale scratch-root citations in SKILL.md (v3 of the c72 family).

Frozen scope: `.ufo/waves/round-73/contract.md` section C2. This is a NEW numbered counter;
`.ufo/waves/round-72/c72_tmp_v2.py` stays byte-identical and is the do-nothing control.

  C2 met iff `--selftest` exits 0 with the full case count passing, every `attack` line in the
  frozen corpus is a finding, every `legit` line is clean, and SKILL.md at both the base
  revision and the measured tip yields no finding.

Detection, per token that names the scratch root (`/` + `tmp`, with a path tail):
  H1 brace   — a token inside a shell parameter default `${NAME:-...}` is a finding: the
               default word still substitutes the scratch root when the variable is unset or
               null, so the annotation cannot make it safe. General `${NAME<op>word}` forms
               (`:-`, `-`, `:=`, `=`) are read; nested defaults are handled.
  H2 command — the line carries a command segment. Segments are split on `&&`, `;`, `|` and
               backticks; `NAME=value` assignments and the `sudo`, `env`, `nohup`, `time`,
               `exec` prefixes are stripped, then the segment's first word (basename of a
               path) must be one of COMMAND_WORDS. A quoted command word is still a command
               word, and a phrase annotation never excuses a command finding — it is a
               defence against a repoint, not a licence for one. The token is a finding
               whenever its line carries such a segment: in the frozen corpus the attack
               line `run <backtick>cp<backtick> state/... <token> ...` puts the quoted
               command word in its own backtick segment and the token in the next one, so a
               token-segment-only reading would accept an attack line the corpus marks as a
               finding.
  H3 symlink — `git ls-tree <rev> SKILL.md` reporting mode 120000 is a finding (the bytes read
               are the link target, not the tracked SKILL.md), not an evaluation error.
  H4 phrase  — only the full phrase `not an executable instruction` annotates a prose token;
               truncated variants (`historical record`, `not an executable`) do not count.
  Prose lines with the full phrase and no command segment are clean. A token counts at most
  once: brace first, then command, then prose.

Reads committed bytes only (`git ls-tree`, then `git show --end-of-options <rev>:SKILL.md`);
inherited GIT_* repository pointers are scrubbed so the lane argument decides the repository.
The scratch root string is assembled at runtime: this file carries no hardcoded scratch path.
Scratch fixtures for the symlink selftest live under `--work`, else `$TMPDIR`, and are removed
before exit.

Usage:
  c73_tmp_v3.py --selftest [--work DIR]
  c73_tmp_v3.py --lane DIR --revision REV [--work DIR]
  c73_tmp_v3.py --corpus FILE [--lane DIR --revision REV] [--work DIR]
  With `--corpus` alone the corpus is classified; adding `--lane` also evaluates SKILL.md,
  and both scopes must be clean for met.

Output line:
  C2v3 revision=<rev> attack_accepted=<n>/<A> legit_rejected=<n>/<L> selftest=<p>/<t> findings=[...] met=<bool>
Exit: 0 met · 1 not met · 2 unevaluable · 64 usage.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile

PATH = "SKILL.md"
PHRASE = "not an executable instruction"
TMP_WORD = "/" + "tmp"
TOKEN_RE = re.compile(
    r"(?<![A-Za-z0-9_./])" + re.escape(TMP_WORD)
    + r"(?![A-Za-z0-9_.\-])[A-Za-z0-9_.\-/]*"
)
SEGMENT_SPLIT_RE = re.compile(r"&&|;|\||`")
PARAM_START_RE = re.compile(r"\$\{")
PARAM_WORD_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*(:?[-=])")
ASSIGNMENT_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")
PREFIX_WORDS = frozenset({"sudo", "env", "nohup", "time", "exec"})
COMMAND_WORDS = frozenset({
    "node", "python", "python3", "cp", "mv", "rm", "rsync", "tar", "dd", "cd",
    "sed", "tee", "head", "tail", "touch", "mkdir", "mktemp", "git", "curl",
    "wget", "npx", "uv", "bash", "sh", "diff", "cat", "ls", "grep", "test",
    "chmod", "chown", "ln", "install", "find", "xargs",
})
GIT_ENV_SCRUB = (
    "GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
    "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_COMMON_DIR", "GIT_PREFIX",
)
EXIT_MET, EXIT_NOT_MET, EXIT_UNEVALUABLE, EXIT_USAGE = 0, 1, 2, 64


class CorpusError(Exception):
    """The corpus is missing, unreadable or not in the frozen `<class> | <expected> | <line>` form."""


def git_env():
    env = dict(os.environ)
    for key in GIT_ENV_SCRUB:
        env.pop(key, None)
    return env


def run_git(args):
    """Run git with scrubbed repository pointers; OSError is folded into a synthetic result."""
    try:
        return subprocess.run(
            ["git", *args], capture_output=True, text=True, env=git_env(),
        )
    except OSError as exc:
        return subprocess.CompletedProcess(["git", *args], 127, "", f"{exc}")


def brace_default_ranges(line):
    """Return (start, end) offsets of shell parameter default words `${NAME<op>...}`."""
    ranges = []
    for match in PARAM_START_RE.finditer(line):
        i = match.end()
        depth = 1
        while i < len(line) and depth:
            if line.startswith("${", i):
                depth += 1
                i += 2
                continue
            if line[i] == "}":
                depth -= 1
                if depth == 0:
                    break
            i += 1
        if depth:
            continue  # unterminated parameter expansion: not a default word
        operator = PARAM_WORD_RE.match(line[match.end():i])
        if not operator:
            continue
        ranges.append((match.end() + operator.end(), i))
    return ranges


def segment_command_word(segment):
    """Return the command word of one shell segment after prefix stripping, or None."""
    text = segment.strip().lstrip("(").strip()
    words = text.split()
    while words:
        word = words[0]
        if word in PREFIX_WORDS:
            words.pop(0)
            while words and words[0].startswith("-") and words[0] != "-":
                words.pop(0)
            continue
        if ASSIGNMENT_RE.match(word):
            words.pop(0)
            continue
        break
    if not words:
        return None
    word = words[0].strip("'\"")
    base = re.sub(r".*/", "", word)
    return base if base in COMMAND_WORDS else None


def line_findings(line):
    """Return (brace, command, prose) finding counts for one line."""
    ranges = brace_default_ranges(line)
    has_command = any(
        segment_command_word(segment) is not None
        for segment in SEGMENT_SPLIT_RE.split(line)
    )
    annotated = PHRASE in line
    brace = command = prose = 0
    for match in TOKEN_RE.finditer(line):
        pos = match.start()
        if any(start <= pos < end for start, end in ranges):
            brace += 1
        elif has_command:
            command += 1
        elif not annotated:
            prose += 1
    return brace, command, prose


def mode_status(mode):
    """Classify the ls-tree mode of SKILL.md: readable regular blob, symlink, or neither."""
    if mode == "100644":
        return "ok"
    if mode == "120000":
        return "symlink"
    return "unevaluable"


def read_skill(lane, rev):
    """Read committed SKILL.md bytes. Return (status, lines, detail)."""
    if not rev or rev.startswith("-"):
        return "unevaluable", [], f"revision {rev!r} is not a safe git argument"
    tree = run_git(["-C", lane, "ls-tree", rev, PATH])
    if tree.returncode != 0:
        return "unevaluable", [], f"git ls-tree {rev} {PATH} exit {tree.returncode}: {tree.stderr.strip()}"
    listing = tree.stdout.strip()
    if not listing:
        return "missing", [], f"{PATH} absent at revision {rev}"
    mode = listing.splitlines()[0].split(None, 1)[0]
    status = mode_status(mode)
    if status == "symlink":
        return "symlink", [], f"{PATH} mode {mode} (symlink) at revision {rev}"
    if status != "ok":
        return "unevaluable", [], f"{PATH} mode {mode} is not 100644 at revision {rev}"
    shown = run_git(["-C", lane, "show", "--end-of-options", f"{rev}:{PATH}"])
    if shown.returncode != 0:
        return "unevaluable", [], f"git show {rev}:{PATH} exit {shown.returncode}: {shown.stderr.strip()}"
    return "ok", shown.stdout.splitlines(), ""


def skill_findings(lines):
    findings = []
    for number, line in enumerate(lines, 1):
        brace, command, prose = line_findings(line)
        if brace or command or prose:
            findings.append(("skill", number, brace, command, prose))
    return findings


def parse_corpus(path):
    """Parse the frozen corpus into (file line, class, expected, text) entries."""
    try:
        with open(path, "r", encoding="utf-8") as handle:
            raw = handle.read()
    except OSError as exc:
        raise CorpusError(f"cannot read corpus {path}: {exc}") from exc
    entries = []
    for number, line in enumerate(raw.splitlines(), 1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        parts = [part.strip() for part in line.split("|", 2)]
        if len(parts) != 3 or not parts[2]:
            raise CorpusError(f"corpus line {number} is not `<class> | <expected> | <line>`: {line!r}")
        cls, expected, text = parts
        if cls not in {"attack", "legit"}:
            raise CorpusError(f"corpus line {number} has unknown class {cls!r}")
        if expected not in {"finding", "clean"}:
            raise CorpusError(f"corpus line {number} has unknown expected value {expected!r}")
        if (cls == "attack") != (expected == "finding"):
            raise CorpusError(f"corpus line {number} pairs class {cls!r} with expected {expected!r}")
        entries.append((number, cls, expected, text))
    if not entries:
        raise CorpusError(f"corpus {path} has no entries")
    return entries


def classify_corpus(entries):
    """Return (attack_total, attack_accepted, legit_total, legit_rejected, findings)."""
    attack_total = attack_accepted = legit_total = legit_rejected = 0
    findings = []
    for number, cls, _expected, text in entries:
        brace, command, prose = line_findings(text)
        is_finding = (brace + command + prose) > 0
        if cls == "attack":
            attack_total += 1
            if not is_finding:
                attack_accepted += 1
                findings.append(("corpus", number, "attack", "accepted", brace, command, prose))
        else:
            legit_total += 1
            if is_finding:
                legit_rejected += 1
                findings.append(("corpus", number, "legit", "rejected", brace, command, prose))
    return attack_total, attack_accepted, legit_total, legit_rejected, findings


def scratch_dir(work):
    base = work if work else os.environ.get("TMPDIR")
    if base:
        os.makedirs(base, exist_ok=True)
    return tempfile.mkdtemp(prefix="c73-", dir=base)


def _fixture_repo(work):
    """Build one repo with a regular, a symlinked and an absent SKILL.md commit; return cases."""
    repo = tempfile.mkdtemp(prefix="c73-h3-", dir=work)
    cases = []

    def git(*args):
        return run_git(["-C", repo, *args])

    def commit(message):
        return run_git([
            "-C", repo, "-c", "user.name=kake-scratch", "-c", "user.email=kake@scratch.local",
            "commit", "-q", "-m", message,
        ])

    def record(name, ok, detail=""):
        cases.append((name, ok, detail))

    try:
        status = git("init", "-q")
        if status.returncode != 0:
            record("h3_fixture_init", False, status.stderr.strip())
            return cases
        toplevel = git("rev-parse", "--show-toplevel").stdout.strip()
        if os.path.realpath(toplevel) != os.path.realpath(repo):
            record("h3_fixture_toplevel", False, f"{toplevel!r} != {repo!r}")
            return cases
        with open(os.path.join(repo, PATH), "w", encoding="utf-8") as handle:
            handle.write("the snapshot lives here\n")
        git("add", PATH)
        commit("regular SKILL.md")
        regular = git("rev-parse", "HEAD").stdout.strip()
        os.remove(os.path.join(repo, PATH))
        with open(os.path.join(repo, "target.md"), "w", encoding="utf-8") as handle:
            handle.write("the snapshot lives here\n")
        os.symlink("target.md", os.path.join(repo, PATH))
        git("add", PATH)
        commit("symlinked SKILL.md")
        symlink = git("rev-parse", "HEAD").stdout.strip()
        git("rm", "-q", PATH)
        commit("removed SKILL.md")
        absent = git("rev-parse", "HEAD").stdout.strip()
        for name, rev, want in (
            ("h3_fixture_regular_ok", regular, "ok"),
            ("h3_fixture_symlink_finding", symlink, "symlink"),
            ("h3_fixture_absent_unevaluable", absent, "missing"),
        ):
            got, _lines, detail = read_skill(repo, rev)
            record(name, got == want, f"got={got} want={want} {detail}")
    except OSError as exc:
        record("h3_fixture_io", False, f"{exc}")
    finally:
        shutil.rmtree(repo, ignore_errors=True)
    return cases


def self_test(work, verbose):
    """Function-level fixtures for H1-H4 plus a real symlink fixture repository."""
    tok = TMP_WORD
    phrase = PHRASE
    cases = [
        # (name, line, want (brace, command, prose))
        ("h1_brace_default_bare", f'run the tool with BK="${{TMPDIR:-{tok}}}" first', (1, 0, 0)),
        ("h1_brace_default_with_path", f'repoint with BK=${{TMPDIR:-{tok}}}/kake-r12 before any write', (1, 0, 0)),
        ("h1_brace_any_name", f'BK=${{MYROOT:-{tok}/kake-r12}} then run', (1, 0, 0)),
        ("h1_brace_nested_default", f'X=${{A:-${{B:-{tok}/y}}}} is a fallback', (1, 0, 0)),
        ("h1_brace_not_double_counted", f'python3 -c "x=${{TMPDIR:-{tok}}}"', (1, 0, 0)),
        ("h2_word_rsync", f'rsync -a {tok}/kake-r12/live/ backup/ ({phrase})', (0, 1, 0)),
        ("h2_word_rm", f'rm -rf {tok}/kake-r12/ ({phrase})', (0, 1, 0)),
        ("h2_env_assignment_prefix", f'TMPDIR={tok}/kake-r12 python3 -B scripts/tool.mjs ({phrase})', (0, 1, 0)),
        ("h2_sudo_prefix", f'sudo cp state/probe-latest.json {tok}/kake-r12/live/backup.json ({phrase})', (0, 1, 0)),
        ("h2_quoted_command_word", f'run `cp` state/probe-latest.json {tok}/kake-r12/live/backup.json ({phrase})', (0, 1, 0)),
        ("h2_backticked_sudo", f'elevate first: `sudo cp state/x {tok}/kake-r12/live/x.json` ({phrase})', (0, 1, 0)),
        ("h2_cd_and_cp_chain", f'`cd {tok}/kake-r12/live && cp state/x y` ({phrase})', (0, 1, 0)),
        ("h2_env_prefix_with_assignment", f'env TMPDIR={tok}/kake-r12 python3 script.py ({phrase})', (0, 1, 0)),
        ("h2_nohup_prefix", f'nohup cp state/x {tok}/kake-r12/live/y ({phrase})', (0, 1, 0)),
        ("h2_time_prefix", f'time cp state/x {tok}/kake-r12/live/y ({phrase})', (0, 1, 0)),
        ("h2_exec_prefix", f'exec cp state/x {tok}/kake-r12/live/y ({phrase})', (0, 1, 0)),
        ("h2_plain_command", f'cp state/probe-latest.json {tok}/kake-r12/live/backup.json', (0, 1, 0)),
        ("h2_phrase_does_not_excuse", f'cp state/probe-latest.json {tok}/kake-r12/live/backup.json ({phrase})', (0, 1, 0)),
        ("legit_prose_annotated", f'the snapshot was under {tok}/kake-r12/live/ ({phrase})', (0, 0, 0)),
        ("legit_token_leads_line", f'{tok}/kake-r12/live/ absent on 2026-11-03 ({phrase})', (0, 0, 0)),
        ("legit_prose_no_command", f'the recipe that used to write under {tok}/kake-r12/ is retired ({phrase})', (0, 0, 0)),
        ("legit_token_free_recipe", 'cp state/probe-latest.json "$BK/probe-latest.backup.json" (repaired recipe; BK="$(mktemp -d)")', (0, 0, 0)),
        ("no_false_match_on_other_name", f'{tok}2/x is not the scratch root', (0, 0, 0)),
        ("no_false_match_embedded_component", f'the log at /var{tok}/x is not the scratch root', (0, 0, 0)),
        ("no_false_match_relative_component", f'a{tok}/b is not the scratch root', (0, 0, 0)),
        ("bare_root_annotated", f'the {tok} directory is not a citation ({phrase})', (0, 0, 0)),
        ("bare_root_unannotated", f'the {tok} directory is not a citation', (0, 0, 1)),
        ("h4_truncated_historical", f'the snapshot was under {tok}/k/ (historical record)', (0, 0, 1)),
        ("h4_truncated_not_executable", f'the snapshot was under {tok}/k/ (not an executable)', (0, 0, 1)),
        ("h4_full_phrase_clean", f'the snapshot was under {tok}/k/ (historical record, {phrase})', (0, 0, 0)),
        ("h3_mode_regular", "100644", "ok"),
        ("h3_mode_symlink", "120000", "symlink"),
        ("h3_mode_other", "100755", "unevaluable"),
    ]
    results = []
    for name, value, want in cases:
        if name.startswith("h3_mode_"):
            got = mode_status(value)
        else:
            got = line_findings(value)
        ok = got == want
        results.append((name, ok, f"got={got} want={want}"))
    # corpus parser: the frozen form, a malformed line, an inconsistent pairing, an empty file
    results.append(_corpus_fixture(work, "corpus_parse_valid", "attack | finding | cp x\n",
                                   [(1, "attack", "finding", "cp x")]))
    results.append(_corpus_fixture(work, "corpus_parse_malformed", "attack | finding\n", "error"))
    results.append(_corpus_fixture(work, "corpus_parse_inconsistent", "attack | clean | cp x\n", "error"))
    results.append(_corpus_fixture(work, "corpus_parse_empty", "# only comments\n\n", "error"))
    # classification counts: one accepted attack and one rejected legit line
    counts = classify_corpus([
        (1, "attack", "finding", "the snapshot was under a clean prose line"),
        (2, "legit", "clean", f"cp state/x {tok}/kake-r12/live/y"),
    ])
    results.append(_expect("corpus_counts", counts[0:4], (1, 1, 1, 1)))
    results += _fixture_repo(work)
    passed = sum(1 for _name, ok, _detail in results if ok)
    if verbose:
        for name, ok, detail in results:
            print(f"selftest {name}: {'OK' if ok else 'FAIL'} {detail}")
    return passed, len(results), results


def _corpus_fixture(work, name, text, want):
    """Write a corpus fixture under --work and compare parse_corpus against want."""
    path = os.path.join(work, f"{name}.txt")
    try:
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(text)
        got = parse_corpus(path)
    except CorpusError:
        got = "error"
    except OSError as exc:
        return (name, False, f"fixture io: {exc}")
    return _expect(name, got, want)


def _expect(name, got, want):
    return (name, got == want, f"got={got} want={want}")


def main(argv):
    lane = revision = corpus = work = None
    selftest = False
    args = list(argv)
    while args:
        arg = args.pop(0)
        if arg == "--lane" and args:
            lane = args.pop(0)
        elif arg == "--revision" and args:
            revision = args.pop(0)
        elif arg == "--corpus" and args:
            corpus = args.pop(0)
        elif arg == "--work" and args:
            work = args.pop(0)
        elif arg == "--selftest":
            selftest = True
        elif arg in ("-h", "--help"):
            print(__doc__)
            return 0
        else:
            print(__doc__, file=sys.stderr)
            return EXIT_USAGE

    findings = []
    unevaluable = None
    attack_total = attack_accepted = legit_total = legit_rejected = 0
    skill_scope = corpus is None or lane is not None
    rev_value = revision if revision is not None else ("HEAD" if skill_scope else "corpus")
    if selftest:
        rev_value = "selftest"

    passed, total, details = 0, 0, []
    try:
        scratch = scratch_dir(work)
    except OSError as exc:
        unevaluable = f"cannot create scratch dir: {exc}"
    else:
        try:
            passed, total, details = self_test(scratch, verbose=selftest)
        finally:
            shutil.rmtree(scratch, ignore_errors=True)

    findings += [("selftest", name) for name, ok, _detail in details if not ok]

    if not selftest and unevaluable is None:
        if corpus is not None:
            try:
                entries = parse_corpus(corpus)
            except CorpusError as exc:
                unevaluable = str(exc)
            else:
                attack_total, attack_accepted, legit_total, legit_rejected, corpus_findings = classify_corpus(entries)
                findings += corpus_findings
        if skill_scope:
            status, lines, detail = read_skill(lane if lane is not None else ".", revision if revision is not None else "HEAD")
            if status == "ok":
                findings += skill_findings(lines)
            elif status == "symlink":
                findings.append(("skill", "symlink", detail))
            elif status == "missing":
                unevaluable = unevaluable or detail
            else:
                unevaluable = unevaluable or detail

    if unevaluable:
        findings.append(("unevaluable", unevaluable))
        print(f"C2v3 unevaluable: {unevaluable}", file=sys.stderr)

    met = (
        unevaluable is None
        and passed == total
        and not findings
    )
    print(
        f"C2v3 revision={rev_value} attack_accepted={attack_accepted}/{attack_total} "
        f"legit_rejected={legit_rejected}/{legit_total} selftest={passed}/{total} "
        f"findings={findings} met={met}"
    )
    if unevaluable:
        return EXIT_UNEVALUABLE
    return EXIT_MET if met else EXIT_NOT_MET


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
