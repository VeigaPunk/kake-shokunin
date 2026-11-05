#!/usr/bin/env python3
"""Supplementary probes for the five survivors (scratch only; NOT the frozen selftest).

Each probe builds a fixture repo in scratch, runs the PRISTINE counter and the
survivor mutant through the public CLI, and records whether the mutant's output
differs. Probes explain why a survivor survived; they do not change the verdict.
"""
import importlib.util
import os
import subprocess
import sys

SCRATCH = "/fast/scratch/hyaku/kake-r97/MutIndex"
PRISTINE = os.path.join(SCRATCH, "pristine", "c97_index.py")
MUT = os.path.join(SCRATCH, "mutants")
PY = sys.executable

spec = importlib.util.spec_from_file_location("pristine_c97", PRISTINE)
P = importlib.util.module_from_spec(spec)
spec.loader.exec_module(P)

ENTRY_A, ENTRY_B = P.ENTRY_A, P.ENTRY_B
HEAD, ROW_A, ROW_B = P.HEAD, P.ROW_A, P.ROW_B
ENTRIES = {"a.md": ENTRY_A, "b.md": ENTRY_B}
WORK = os.path.join(SCRATCH, "probe-work")
os.makedirs(WORK, exist_ok=True)


def cli(script, root, rev="HEAD", env=None):
    p = subprocess.run([PY, "-B", script, "--root", root, "--revision", rev,
                        "--work", WORK], capture_output=True, text=True,
                       env=env)
    return p.returncode, (p.stdout.splitlines() or [""])[0]


def mk(name, readme, entries=ENTRIES):
    d = os.path.join(WORK, name)
    if os.path.exists(d):
        subprocess.run(["rm", "-rf", d], check=True)
    P.make_repo(d, readme, entries)
    top = subprocess.run(["/usr/bin/git", "-C", d, "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True).stdout.strip()
    assert os.path.realpath(top) == os.path.realpath(d), top
    return d


PROBES = [
    # (probe id, mutant id, fixture readme, extra fixture notes)
    ("PR-M01a", "M01-no-fence-skip",
     HEAD + ROW_A + "```\n" + ROW_B + "```\n",
     "frozen selftest fenced row (no header): fenced row is consumed as a table header"),
    ("PR-M01b", "M01-no-fence-skip",
     HEAD + ROW_A + "```\n" + HEAD + ROW_B + "```\n",
     "fenced block carrying its own header + data row"),
    ("PR-M02a", "M02-no-comment-skip",
     HEAD + ROW_A + "<!--\n" + ROW_B + "-->\n",
     "frozen selftest commented row (no header): comment-body row consumed as header"),
    ("PR-M02b", "M02-no-comment-skip",
     HEAD + ROW_A + "<!--\n" + HEAD + ROW_B + "-->\n",
     "comment carrying its own header + data row"),
    ("PR-M06", "M06-min-words-8to1",
     HEAD + ROW_A + "| Sitemaps | `knowledge/b.md` (S902–S904) | sitemap containers "
     "location scoping |\n",
     "row with ids, 5 words (<8), 2+ shared long words with entry"),
]


def m12_probe():
    d = mk("m12-replace", HEAD + ROW_A, ENTRIES)
    # replace the committed README blob with one that indexes b.md
    blob_old = subprocess.run(["/usr/bin/git", "-C", d, "rev-parse", "HEAD:corpus/README.md"],
                              capture_output=True, text=True).stdout.strip()
    alt = os.path.join(WORK, "m12-alt-README.md")
    with open(alt, "w") as fh:
        fh.write(HEAD + ROW_A + ROW_B)
    blob_new = subprocess.run(["/usr/bin/git", "-C", d, "-c", "user.name=probe",
                               "-c", "user.email=probe@mutindex.invalid",
                               "hash-object", "-w", alt],
                              capture_output=True, text=True).stdout.strip()
    subprocess.run(["/usr/bin/git", "-C", d, "-c", "user.name=probe",
                    "-c", "user.email=probe@mutindex.invalid",
                    "replace", blob_old, blob_new], check=True)
    return d


def pathshadow_probe():
    """M13: PATH-shadowed git wrapper. Pristine vs mutant, parent PATH shadowed."""
    d = mk("m13-shadow", HEAD + ROW_A + ROW_B, ENTRIES)
    shadow = os.path.join(WORK, "shadow-bin")
    os.makedirs(shadow, exist_ok=True)
    marker = os.path.join(WORK, "shadow-fired.txt")
    wrapper = os.path.join(shadow, "git")
    with open(wrapper, "w") as fh:
        fh.write('#!/bin/sh\necho fired >> "%s"\nexec /usr/bin/git "$@"\n' % marker)
    os.chmod(wrapper, 0o755)
    env = dict(os.environ)
    env["PATH"] = shadow + ":" + env.get("PATH", "")
    if os.path.exists(marker):
        os.remove(marker)
    rp = cli(PRISTINE, d, env=env)
    rm = cli(os.path.join(MUT, "M13-git-from-path.py"), d, env=env)
    fired = os.path.exists(marker)
    return {"pristine": rp, "mutant": rm, "shadow_fired": fired,
            "same": rp == rm}


def main():
    print("PROBE  pristine(rc,line) | mutant(rc,line) | differs")
    results = []
    for pid, mid, readme, note in PROBES:
        d = mk(pid, readme, ENTRIES)
        mscript = os.path.join(MUT, mid + ".py")
        rp = cli(PRISTINE, d)
        rm = cli(mscript, d)
        differs = rp != rm
        results.append((pid, mid, rp, rm, differs, note))
        print("%s  %s | %s | differs=%s  [%s]" % (pid, rp, rm, differs, note))

    d12 = m12_probe()
    p12 = cli(PRISTINE, d12)
    m12 = cli(os.path.join(MUT, "M12-no-git-no-replace-objects.py"), d12)
    results.append(("PR-M12", "M12-no-git-no-replace-objects", p12, m12, p12 != m12,
                    "git replace ref on README blob"))
    print("PR-M12  %s | %s | differs=%s" % (p12, m12, p12 != m12))

    sh = pathshadow_probe()
    print("PR-M13  pristine=%s mutant=%s shadow_fired=%s same=%s"
          % (sh["pristine"], sh["mutant"], sh["shadow_fired"], sh["same"]))
    with open(os.path.join(SCRATCH, "probe-results.txt"), "w") as fh:
        for pid, mid, rp, rm, dif, note in results:
            fh.write("%s\t%s\tpristine=%s\tmutant=%s\tdiffers=%s\t%s\n"
                     % (pid, mid, rp, rm, dif, note))
        fh.write("PR-M13\tM13-git-from-path\tpristine=%s\tmutant=%s\tshadow_fired=%s\tsame=%s\n"
                 % (sh["pristine"], sh["mutant"], sh["shadow_fired"], sh["same"]))


if __name__ == "__main__":
    main()
