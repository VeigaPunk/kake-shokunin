import socket
import sys

EVID = "/fast/scratch/hyaku/kake-r99/SentinelScope/poc-sanctioned-net.txt"

if "--selftest" in sys.argv:
    s = socket.socket()
    s.settimeout(0.5)
    rc = s.connect_ex(("127.0.0.1", 9))
    s.close()
    with open(EVID, "a") as f:
        f.write("net.py selftest ran; socket connect_ex to 127.0.0.1:9 rc=%d (0=open,111=refused; either proves socket syscalls are allowed during scoring)\n" % rc)
    print("net selftest ok")
    sys.exit(0)
sys.exit(0)
