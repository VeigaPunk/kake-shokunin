import importlib.util
import re

COUNTER = "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-60/c60_gate_status.py"
spec = importlib.util.spec_from_file_location("c60_probe", COUNTER)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
member = ".ufo/waves/round-48/c48_lint_count.py"
head = (
    "| Name | Kind | Entry command | Verdict map | Self-test | Proof | Scope | Owner |\n"
    "|---|---|---|---|---|---|---|---|\n"
)

# A rendered table row whose Entry command is present only inside a same-line HTML comment.
comment_row = (
    f"| fake | gate | <!-- `python3 -B {member} --root . --revision <commit>` --> | "
    "`0=met`; `1=not met` | n | n | n | n |"
)
comment_skill = head + comment_row + "\n"
module.run_member = lambda *args: 0
comment_result = module.eval_member(
    member, module.md_tables(comment_skill), comment_skill, "unused", "a" * 40, "unused"
)

# A valid row plus a path mention inside a fenced block. The invalid ```python closer
# causes _mask() to treat the later hidden line as an extra rendered-row mention.
visible_row = (
    f"| c48_lint_count | gate | `python3 -B {member} --root . --revision <commit>` | "
    "`0=met`; `1=not met` | n | n | n | n |"
)
fenced_skill = (
    head + visible_row + "\n```text\n```python\n| hidden | note | " + member + " |\n```\n"
)
fenced_mentions = module.rows_mentioning(fenced_skill, member)
fenced_tables = module.md_tables(fenced_skill)
fenced_result = module.eval_member(
    member, fenced_tables, fenced_skill, "unused", "c" * 40, "unused"
)

# A never-met observation with one valid green exit and one non-verdict exit.
kind = "never met 0123456789abcdef0123456789abcdef01234567"
never_row = (
    f"| x | {kind} | `python3 -B {member} --root . --revision <commit>` | "
    "`0=met`; `1=not met` | n | n | n | n |"
)
never_skill = head + never_row + "\n"
module.is_ancestor = lambda *args, **kwargs: True
module.entry_exists = lambda *args, **kwargs: True
codes = iter((0, 2))
module.run_member = lambda *args: next(codes)
never_result = module.eval_member(
    member, module.md_tables(never_skill), never_skill, "unused", "b" * 40, "unused"
)

print(
    "HTML-comment-only row:",
    "candidate row accepted", bool(comment_result["argv"]),
    "label=", comment_result["label"],
    "e_T=", comment_result["e_T"],
    "classes=", comment_result["classes"],
)
print(
    "fence case:",
    "parsed_table_rows=", sum(len(rows) for _, rows in fenced_tables),
    "rendered_mentions=", fenced_mentions,
    "mentions_count=", len(fenced_mentions),
    "canonical_vs_hidden=", len(fenced_mentions) > sum(len(rows) for _, rows in fenced_tables),
)
print("fence row classification:", fenced_result["classes"])
print("never-met e_T=0,e_P=2:", "classes=", never_result["classes"])
