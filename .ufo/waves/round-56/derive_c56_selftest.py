#!/usr/bin/env python3
"""Version 1.1 of c56_quote_truth.py: port the round-55 selftest (fixture mutations of the REAL committed evidence) to the
round-56 rows and add fixtures for this round's new risks. The conditions C1..C8 and the predicate are NOT touched; only the
`--selftest` block is replaced (the version-1 file ships a stub). Idempotent: run on the version-1 file."""
import re, subprocess
LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
src55 = subprocess.run(["git", "-C", LANE, "show", "e48354b7c26bb6dc544ab6bbdc534fabe0daf7b6:.ufo/waves/round-55/c55_quote_truth.py"],
                       capture_output=True, text=True, check=True).stdout
a = src55.index("# --------------------------------------------------------------------------- selftest")
b = src55.index("def main() -> int:")
block = src55[a:b]
MAP = {"S372": "S367", "S373": "S419", "S418": "S420"}
block = re.sub(r"S372|S373|S418", lambda m: MAP[m.group(0)], block)
def rep(old, new):
    global block
    assert old in block, old
    block = block.replace(old, new)
rep('set_used_by(row(f, "S419"), ADOPTED["S419"])', 'set_used_by(row(f, "S367"), ADOPTED["S367"])')
rep('.replace("002885", "002886")', '.replace("002857", "002858")')
rep('f[REGISTRY] = f[REGISTRY].replace("§ robots.txtとは？ (h2)", "§ 存在しない見出し (h2)")',
    'f[REGISTRY] = f[REGISTRY].replace(row(f, "S420"), re.sub(r"§ [^|]*? \\(更新日", "§ 存在しない見出し (更新日", row(f, "S420"), count=1))')
rep("KAKE_R55_SELFTEST_REV", "KAKE_R56_SELFTEST_REV")
rep("c55-qt-", "c56-qt-")
rep("missing round-55 evidence", "missing round-56 evidence")
rep("c55 quote-truth selftest", "c56 quote-truth selftest")
new_cases = '''
    SHARED = "サーバーが「HTTP 404 Not Found」のステータスを返すように"  # occurs in both sibling bodies (S419 and S420)

    @case("fail_gate_quote_shared_with_sibling")
    def _(f):
        g = gate_line_of(f, "S420")
        q = re.findall(r'"([^"]+)"', g)[-1]
        f[LESSON] = f[LESSON].replace(g, g.replace(q, SHARED))

    @case("fail_entry_only_sibling_shared_spans")
    def _(f):
        body = f[ADOPTED["S420"]].split("\\n")
        keep = [ln for ln in body if '"' not in ln]
        f[ADOPTED["S420"]] = "\\n".join(keep) + "".join(f'\\n> "{SHARED}{t}"' for t in ("", "設定", "設定を行って"))

    @case("pass_entity_span_raw", 0)
    def _(f): f[ADOPTED["S367"]] += '\\n> "rel=&quot;nofollow&quot;属性を使った指定方法"\\n'

    @case("fail_entity_span_decoded")
    def _(f): f[ADOPTED["S367"]] += '\\n> "HTMLの<head>内に次のような記述をします"\\n'

    @case("fail_new_row_already_in_base")
    def _(f): f["__base_registry__"] = f["__base_registry__"] + row(f, "S419") + "\\n"
'''
marker = '    unit_checks = {'
assert marker in block
block = block.replace(marker, new_cases + "\n" + marker, 1)
cur = open("c56_quote_truth.py").read()
i = cur.index("# --------------------------------------------------------------------------- selftest")
j = cur.index("def main() -> int:")
cur = cur[:i] + block + cur[j:]
cur = cur.replace('Version 1 (frozen before any seat scored).', 'Version 1 (frozen before any seat scored); version 1.1 replaces the `--selftest` stub with the ported selftest\n(`derive_c56_selftest.py`) — conditions and predicate unchanged.', 1)
open("c56_quote_truth.py", "w").write(cur)
