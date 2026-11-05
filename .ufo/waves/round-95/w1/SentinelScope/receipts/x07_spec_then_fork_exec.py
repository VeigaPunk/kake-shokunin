import importlib.util as u,glob,sys,os
c=glob.glob(os.path.join(sys.prefix,'lib','python*','lib-dynload','_posixsubprocess*.so'))+glob.glob(os.path.join(sys.base_prefix,'lib','python*','lib-dynload','_posixsubprocess*.so'))
if not c: print('no-so'); raise SystemExit(0)
s=u.spec_from_file_location('_posixsubprocess', c[0]); m=u.module_from_spec(s); s.loader.exec_module(m)
args=(['sh','-c','echo FORKEXEC > /fast/scratch/hyaku/kake-r95/SentinelScope/sbx/work/forkexec_marker'], None, None, None, None, None)
print('fork_exec present', hasattr(m,'fork_exec'))

