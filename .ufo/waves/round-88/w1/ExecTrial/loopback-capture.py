#!/usr/bin/env python3
"""ExecTrial round 88 — capture the client's own request headers on loopback.

No origin and no network is contacted: the socket binds 127.0.0.1 on an
ephemeral port and curl is pointed at it with the same flags as the live GET.
Run: python3 -B loopback-capture.py
"""
import socket
import subprocess
import sys
import threading

srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srv.bind(('127.0.0.1', 0))
srv.listen(1)
port = srv.getsockname()[1]
got = {}


def serve():
    conn, _ = srv.accept()
    conn.settimeout(5)
    data = b''
    while b'\r\n\r\n' not in data:
        chunk = conn.recv(4096)
        if not chunk:
            break
        data += chunk
    got['raw'] = data
    conn.sendall(b'HTTP/1.1 204 No Content\r\nvary: Accept-Encoding\r\ncontent-length: 0\r\n\r\n')
    conn.close()


t = threading.Thread(target=serve)
t.start()
p = subprocess.run(['curl', '-sS', '--max-time', '5',
                    '-A', 'kake-r88-ExecTrial/1.0 (capability observation)',
                    '-o', '/dev/null', '-w', '%{http_code}',
                    f'http://127.0.0.1:{port}/'], capture_output=True, text=True)
t.join(10)
srv.close()

print('curl_exit=%d http_code=%s stderr=%r' % (p.returncode, p.stdout, p.stderr))
print('raw_request_bytes=%d' % len(got.get('raw', b'')))
sys.stdout.write(got.get('raw', b'').decode('utf-8', 'replace'))
