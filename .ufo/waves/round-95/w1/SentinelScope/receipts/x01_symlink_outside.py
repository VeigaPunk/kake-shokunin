import os; root=os.path.dirname(os.path.abspath(__file__)); os.symlink('/etc/hostname', os.path.join(root,'lnk1')); print(open(os.path.join(root,'lnk1')).read()[:40])
