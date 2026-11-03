import html, re, sys, pathlib
src, dst = sys.argv[1], sys.argv[2]
s = pathlib.Path(src).read_text(encoding='utf-8', errors='replace')
s = re.sub(r'(?is)<script\b.*?</script\s*>', '', s)
s = re.sub(r'(?is)<style\b.*?</style\s*>', '', s)
s = re.sub(r'(?s)<[^>]*>', '', s)
s = html.unescape(s)
pathlib.Path(dst).write_text(s, encoding='utf-8')
