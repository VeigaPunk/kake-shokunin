# ExecC2RealRun — round-79 w1 seat report

**Verdict:** real-input run complete — `realrun/manifest.json` built from the 12 recorded round-61 captures; `scripts/x_robots_tag_audit.py` (sha256 `f06c47b5cdd38bccf3dd1c0f381fbd560f6622bdf9d25443a02a2e2c23a24de8`) ran over it with **rc=0 in both `--json` and text mode, `XRTv1 checks=12 findings=0 exit=0`**; population at base rev recorded (20 paths, rc=0). The receipt covers the **recorded 2026-10-27 header sets only — it makes no statement about the live hosts today**.

## 1. Manifest built (`x-robots-tag-manifest/v1`)

- File: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-79/realrun/manifest.json` — 20584 bytes, sha256 `096503668786bed5d9ede122c76568e95018b49b67c76cbd41f67453b43a1e44`.
- Built from all 12 `capture/*/response.json` (`.ufo/waves/round-61/capture/`): `id` = capture dir name, `url` = `finalUrl`, `headers` = the recorded `{name, value}` list **unchanged** (verified: every header entry has exactly keys `name`,`value`; per-check header count equals the capture's `headerCount` for all 12).
- Checks (12): burnerchrome-kimi, charter-ghp, charter-kimi, ds4cc-kimi, ds4cc-primary, lucario-ghp, lucario-kimi, plazir15-ghp, plazir15-kimi, plazir27-kimi, ufo-fsd-kimi-pro, vault-index-kimi.
- **None of the 12 recorded header sets declares `X-Robots-Tag`** (0 of 22+23+14+16+22+23+14+23+14+14+12+16 recorded fields). Per the frozen contract this is a valid check with empty sets, so `exit 0 / checks=12` is the expected carrier outcome — measured, and it matches.
- All 12 captures `fetchedAt` on **2026-10-27** (census: `{'2026-10-27': 12}`).

## 2. Tool wait and bytes

- Poll: file absent at 2026-11-04T09:59:55Z; **found at attempt 3, 2026-11-04T10:04:27Z** (`sleep 60` between checks; well inside the 25-minute budget).
- Bytes run: 18053 bytes, sha256 `f06c47b5cdd38bccf3dd1c0f381fbd560f6622bdf9d25443a02a2e2c23a24de8`, re-hashed identical **after** both runs (byte-stable during measurement). I did not touch the file (concurrently authored by ExecC2Tool); if the carrier lands different bytes, re-run this receipt against them.

## 3. Runs (verbatim commands, cwd = lane root)

```
python3 -B scripts/x_robots_tag_audit.py --manifest /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-79/realrun/manifest.json --json   → rc=0, stderr empty
python3 -B scripts/x_robots_tag_audit.py --manifest /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-79/realrun/manifest.json          → rc=0, stderr empty
```

- Text mode final line: `XRTv1 checks=12 findings=0 exit=0`; 12 `check <id> directives=[] effective=[] bots={} findings=[]` lines.
- JSON mode: exactly one object, `{"schema": "x-robots-tag-report/v1", ...}`; top keys `checks/findings/exit/schema`; `checks`=12; union findings `[]`; total per-check findings 0.
- Surface count: **checks=12** (matches the contract's carrier statement).
- **Scope statement:** this receipt judges the recorded 2026-10-27 header sets of the 12 round-61 surfaces, read-only and network-free. It claims nothing about the live hosts as of today or any later date, no crawler behaviour, and no header inheritance across redirect hops.

## 4. Population receipt (`--emit-population`, base revision)

Command: `python3 -B scripts/instrument_receipts.py --root . --revision 0898085450ee1b65d910f1dcb7a0efc20b413b88 --emit-population` → **rc=0**, 20 paths (run twice, identical; verbatim copy retained). This is the population **at the base revision** — the SKILL.md registry will need these 20 plus the two new rows (`scripts/x_robots_tag_audit.py`, `.ufo/waves/round-79/c79_xrt_matrix.py`) once they land:

```
.ufo/waves/round-52/c52_wave_ledger.py
.ufo/waves/round-57/c57_idresolver_gate.py
.ufo/waves/round-58/c58_receipt_rewrites.py
.ufo/waves/round-58/c58_resolver_cases.py
.ufo/waves/round-59/c59_axis_evidence.py
.ufo/waves/round-59/c59_resolver_cases.py
.ufo/waves/round-66/c66_gate_status_hostportable.py
.ufo/waves/round-69/c69_recorded_counts.py
.ufo/waves/round-69/c69_tmp_honour.py
.ufo/waves/round-72/c72_tmp_v2.py
.ufo/waves/round-73/c73_tmp_v3.py
.ufo/waves/round-73/c73_wave_pointers.py
.ufo/waves/round-74/c74_registry_gap.py
.ufo/waves/round-75/c75_row_truth.py
scripts/citation_lint.py
scripts/doc_quote_truth.py
scripts/hreflang_audit.py
scripts/id_resolver.py
scripts/instrument_receipts.py
scripts/redirect_audit.py
```

## 5. Retained receipts (`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-79/w1/ExecC2RealRun/`)

| File | Bytes | sha256 |
|---|---|---|
| `digests.txt` | 504 | `3dca927d5d71390dce58be40be07189ed181b59b0c134cc6c816d27291d7b454` |
| `population_r0898085.txt` | 728 | `f80f052f5d910af3976d3b9e90226abc7fd3bdf1a84ec49b0bcb46c14ea7aaf3` |
| `realrun_json.json` | 1627 | `f4bb732f9039a8dc2bdc6761aeef97902f37e358f4cc580ed86ef382abefe95a` |
| `realrun_text.txt` | 838 | `a11d87f89a39ceda1b26de9caec7e773ad7ac3ed4e148c4589962219f3147428` |

No stderr receipts: both runs wrote empty stderr.

## 6. Notes, risks, tooling

- No tools installed or upgraded for this seat (none needed); pacman pause respected.
- Scratch `/fast/scratch/hyaku/kake-r79/ExecC2RealRun/` was created per protocol, used for the poll loop cwd only, and deleted before this report was finalized.
- Risk: the tool is under concurrent authorship; the digests above pin the exact bytes measured. Frozen artifacts untouched; no other seat's files modified.
- Defects in my scope: none observed. The manifest exercises only the zero-X-Robots-Tag path of the grammar (a property of the recorded captures, not of the tool).
