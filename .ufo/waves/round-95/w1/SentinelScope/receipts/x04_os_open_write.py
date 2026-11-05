import os; fd=os.open('/fast/scratch/hyaku/kake-r95/SentinelScope/sbx/work/osopen_marker', os.O_CREAT|os.O_WRONLY); os.write(fd,b'x'); os.close(fd)
