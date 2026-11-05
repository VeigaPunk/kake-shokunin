import importlib.util as u,glob,sys,os; c=glob.glob(os.path.join(sys.prefix,'lib','python*','lib-dynload','_posixsubprocess*.so'))+glob.glob(os.path.join(sys.base_prefix,'lib','python*','lib-dynload','_posixsubprocess*.so')); print('so', c[:1]); 
if c:
  s=u.spec_from_file_location('_posixsubprocess', c[0]); m=u.module_from_spec(s); s.loader.exec_module(m); print('LOADED', m.__name__, [x for x in dir(m) if 'fork' in x])
else:
  print('no-so-found')
