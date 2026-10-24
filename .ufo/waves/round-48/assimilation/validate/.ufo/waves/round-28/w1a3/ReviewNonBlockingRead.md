# ReviewNonBlockingRead: C1 repair, WorkingTreeSource.read_document

Seat: KakeR28a3.ReviewNonBlockingRead (leaf reviewer, axis operability). Commit reviewed: b5d423fc02057f67a6f3a255808313ce40d29069 (base 22c1669c1fec83d1a0769de6b9ce686c75657e66). Only this file was written in the lane. Sandbox: /fast/scratch/hyaku/kake-r28a3/w1/ReviewNonBlockingRead (S below). Installs or upgrades: none.

## Verdict

No Critical, High or Medium defect in the assigned hunk. read_document refuses FIFO, symlink-to-FIFO, directory, device, unix socket, unreadable, missing, symlink-loop and read-error inputs with an InputInvalid (exit 2, JSON report) without blocking, and every path closes its descriptor. It does not over-reject regular files, empty regular files, symlinks to regular files inside the root, or the 26 real corpus files. F1 and F2 are Low. F3 to F6 are Info.

## Findings (severity order)

F1 Low. A device opened before refusal can become the controlling terminal.
- Code: scripts/citing_set.py:219-221. The flags omit os.O_NOCTTY, and os.open runs before the S_ISREG check at :227.
- Evidence (pty slave, child started with start_new_session=True): repaired read_document gives tty_nr 0 -> 34817 and InputInvalid document_not_regular_file. The same child opening with O_NOCTTY gives 0 -> 0. Base-style plain open() gives 0 -> 34818, so this is pre-existing and not introduced by the hunk.
- Reach: needs a device node under --root and a session-leader run with no controlling terminal. Fix: add getattr(os, "O_NOCTTY", 0) to flags. Not applied (lane is read-only for me).

F2 Low. The refusal reason drops the file type, and a socket is labelled unreadable.
- Code: :227-228 (non-regular branch carries no detail); :221-225 (ENXIO for sockets).
- Evidence (matrix, repaired): FIFO, symlink-to-FIFO, directory, ledger directory and /dev/null all give document_not_regular_file with detail None, so an operator cannot tell them apart. A unix socket gives document_unreadable with detail "No such device or address".
- Naming: the corpus side reports the same condition as not_a_regular_file (scripts/citing_set.py:284). This hunk adds document_not_regular_file, so there are two codes for one condition.
- Fix options: put the file type (stat.S_IFMT name) in detail at :228; map ENXIO or pre-stat sockets to the non-regular code.

F3 Info. Intended change in measured output: a FIFO with a live writer.
- Evidence: base exits 0 clean (it read the writer's JSON). Repaired exits 2 refused in 0.03 s.
- Basis: the module docstring says a FIFO or device is refused without blocking; round-27 .ufo/waves/round-27/w1/BuildGate.md item 6 rejects fifo, socket and device entries. This hunk extends that to input documents. The L1 should record it, because measured output changes for this input class.
- Label shifts, exit 2 unchanged: directory and ledger directory move from document_unreadable to document_not_regular_file; /dev/null moves from document_not_json to document_not_regular_file.

F4 Info. Double close: not reproduced in a real failure.
- The finally at :236-238 closes the fd if os.fdopen raised. An injected fault that closes the fd and then raises leaks a raw OSError [Errno 9] past InputInvalid (fdopen probe, case injected-fdopen).
- A real CPython failure before FileIO creation (buffering=1 under warnings-as-errors) leaves the fd open, so the finally closes it correctly. A failure after FileIO creation could not be reproduced. No action required.

F5 Info. Pre-existing residuals outside C1, unchanged by this hunk, not exercised.
- Containment is checked by realpath (is_inside, :215) and the file is opened later by path (:221). A swap between the two is possible. The new fstat checks type, not containment.
- handle.read() (:231) has no size bound.

F6 Info. The C1 counter covers this hunk narrowly.
- c1_interface_count.py exercises read_document only through U1 and U2 (FIFO population and ledger, lines 176-182). It does not cover symlink-to-FIFO, directory, socket, unreadable, read error, device, live writer, or descriptor counts. My matrix and fd probe cover those, and all pass.

Docs: b5d423f touches scripts/citing_set.py and two verification JSON files only (git show --stat). The SKILL.md:616 exit row (0/1/2/64) is still accurate. The lane has no CHANGELOG file; LOG.md was not touched by this commit.

## Commands and exit codes

LANE=/home/vgpnk/Projects/shokunin/kake-shokunin; S as above.
1. git -C $LANE diff 22c1669 b5d423f -- scripts/citing_set.py -> exit 0 (+60/-13).
2. git clone -q $LANE $S/clone -> exit 0; git -C $S/clone log -1 b5d423f -> exit 0.
3. git show b5d423f:scripts/citing_set.py > $S/citing_set.py -> exit 0; git show 22c1669:scripts/citing_set.py > $S/citing_set.base.py -> exit 0 (24856 bytes).
4. git -C $S/clone checkout -q --detach b5d423f; sha256sum clone copy and sandbox copy -> both 28ba9965...f415; exit 0.
5. python3 -B $LANE/.ufo/waves/round-28/c1_interface_count.py --root $S/clone --revision b5d423f... --scratch $S/counter-fix -> exit 0; 15/15 (defect 11/11, control 4/4). Matches c1-after-b5d423f.json.
6. Same counter, --revision 22c1669... -> exit 1; 4/15 (defect 0/11, control 4/4); U1 and U2 timed out at 20 s. Matches c1-before.json.
7. timeout 90 python3 -B $S/probes/fdprobe.py $S/citing_set.py $S/fd-probe-root -> exit 0 (results below).
8. timeout 280 python3 -B $S/probes/matrix.py $S/citing_set.base.py $S/citing_set.py $S/matrix-work -> exit 0 (16 cases, 12 s timeout each).
9. Real corpus copy ($S/realcorpus-root: 26 corpus/knowledge files, population S001-S999, empty ledger), both gates -> exit 1 each, identical reports (citingPairs 76, corpusFiles 26, only unadjudicated_citing_pair, zero input_invalid).
10. pty controlling-terminal probe (F1) -> child rc 0 for each mode.
11. Symlink loop read_document -> document_unreadable "Too many levels of symbolic links"; no hang.
12. CPython fdopen probe (F4) -> rc 0; "fd still open after failed fdopen".
13. git -C $S/clone show --stat b5d423f -> exit 0; 3 files.

## Results

fd probe (in-process, repaired hunk): nine paths (regular, empty, symlink-to-regular, FIFO, symlink-to-FIFO, directory, mode 000, missing, unix socket), each called 200 times. Descriptor delta 0 on every path. Symlink-to-/proc/self/mem (EIO on read) refused, delta 0. issubclass(InputInvalid, OSError) is False.

CLI matrix (base -> repaired):
- valid-control: 0 clean -> 0 clean
- population-fifo: TIMEOUT at 12 s -> 2 document_not_regular_file in 0.03 s
- ledger-fifo: TIMEOUT -> 2 document_not_regular_file
- population-symlink-to-fifo: TIMEOUT -> 2 document_not_regular_file
- population-directory: 2 document_unreadable (Is a directory) -> 2 document_not_regular_file
- population-unix-socket: 2 document_unreadable (ENXIO) -> same
- population-mode-000: 2 document_unreadable (EACCES) -> same
- population-missing: 2 document_unreadable (ENOENT) -> same
- population-symlink-regular-inside: 0 clean -> 0 clean (no over-rejection)
- population-empty-regular: 2 document_not_json -> same
- ledger-directory: 2 document_unreadable -> 2 document_not_regular_file
- population-symlink-outside-root: 2 path_escapes_root -> same
- corpus-entry-fifo: 2 not_a_regular_file -> same (refused in _walk, no open)
- population-fifo-live-writer: 0 clean -> 2 document_not_regular_file (F3)
- population-dev-null (root /dev): 2 document_not_json -> 2 document_not_regular_file
- population-dev-zero (root /dev): base not run (would read /dev/zero without bound); repaired 2 document_not_regular_file in 0.03 s, no read

Counter reproduction: base 4/15 and repaired 15/15 both match the lane's recorded before and after files.

## Residual risk and gaps

- Not verified: device nodes other than /dev/null, /dev/zero and the pty slave; O_NONBLOCK on FUSE or NFS regular files; a real failure after FileIO creation in fdopen; the containment race (F5); GitSource, which this hunk does not touch and which I ran only through the counter.
- I did not run citing_set_selftest.py directly. The counter ran it (K4, exit 0).
- No installs or upgrades. Used system git and Python 3.14.8 only.
