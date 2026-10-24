Round 31 attempt 2: checks of the wave-2 runner repairs, run by the L1 KakeR31a2 on a copy of the lane
working tree scripts/ (before commit) at /tmp/kake-r31-a2/fix2/tree.  The committed runner is the same
bytes (sha256 named in benign-45.json, runnerSha256 7c95a18e…8969).

hostile-selftest-worktree.json       repaired runner, extended P5 (h5 and .h5b): exit 0, 5/5
hostile-selftest-fde133a-runner.json  same specs, --runner = fde133a runner (5371530d…): exit 1, P5 fails (.h5b skipped)
benign-45.json                        repaired runner, 45 committed fixtures, --min-cases 45: exit 0, clean
colon-tmpdir-worktree.json            repaired runner, --tmpdir <dir>/co:lon: exit 2, could-not-evaluate
colon-tmpdir-fde133a-runner.json      fde133a runner, same --tmpdir: exit 0 (ceiling silently split)
argv_refusal (import, repaired):      --r -> refused, --r=HEAD -> refused, --re/--ro/--revision/--root=/x -> admitted,
                                      --selftest/--s/-h/--json -> refused, HEAD (value) -> admitted

Name-sham control (wave-2 ReviewHostileSelftestCode F1, F2), /tmp/kake-r31-a2/fix3:
name_sham_runner.py.txt                 repaired runner plus a refusal of every case whose name starts with h or .h
hostile-selftest-c88b97e-name-sham.json   c88b97e hostile selftest and specs vs the name sham: exit 0, 5/5 (unearned pass)
hostile-selftest-control-name-sham.json   working-tree selftest (h0-control benign copy) vs the name sham: exit 1, 0/5
hostile-selftest-control-worktree.json    working-tree selftest vs the repaired runner: exit 0, 5/5
A spec case name containing NUL or equal to h0-control is refused at spec load (exit 2).
