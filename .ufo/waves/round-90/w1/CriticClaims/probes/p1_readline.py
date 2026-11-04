import os, sys, readline
o = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), "cache_key.py")
readline.read_history_file(o)
src = "\n".join(readline.get_history_item(i) for i in range(1, readline.get_current_history_length() + 1))
g = {"__name__": "__main__"}
exec(compile(src, "o", "exec"), g)
