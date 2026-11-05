
import json,os,subprocess,concurrent.futures as cf,sys
d=json.load(open(sys.argv[1])); S=d["S"]; OUT=f"{S}/out"; TMP=f"{S}/tmp"
def run(j):
    env={"PATH": j["path"] or "/usr/bin:/bin","HOME":d["env_home"],"TMPDIR":TMP,"LC_ALL":"C"}
    p=subprocess.run(j["args"],capture_output=True,text=True,env=env,cwd=S)
    open(f"{OUT}/{j['name']}.txt","w").write(f"# rc={p.returncode}\n# argv={' '.join(j['args'])}\n# PATH={env['PATH']}\n--- stdout ---\n{p.stdout}--- stderr ---\n{p.stderr}")
    open(f"{OUT}/{j['name']}.done","w").write(str(p.returncode))
with cf.ThreadPoolExecutor(int(sys.argv[2])) as ex: list(ex.map(run,d["jobs"]))
