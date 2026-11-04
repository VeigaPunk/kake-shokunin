import sys
ev=[]
sys.addaudithook(lambda e,a: ev.append(e) if not e.startswith(("open","import","compile","exec","object.","sys._getframe","os.listdir","os.scandir","marshal","builtins")) else None)
import os, multiprocessing.util as mu
r,w=os.pipe()
pid=mu.spawnv_passfds(os.fsencode(sys.executable),[os.fsencode(sys.executable),b"-c",b"import os;os.write(%d,b'child-ran')"%w],[w])
os.close(w); print(os.read(r,100)); os.waitpid(pid,0)
print(ev)
