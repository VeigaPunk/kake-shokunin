import json,subprocess,sys
SW="max-age=600, stale-if-error=1200"
P=[("N1",{"response_cc":SW,"freshness_lifetime":600,"current_age":900,"event":"error","error":100},("not-an-error",300)),
("N2",{"response_cc":SW,"freshness_lifetime":600,"current_age":900,"event":"error","error":599},("not-an-error",300)),
("N3",{"response_cc":SW,"freshness_lifetime":600,"current_age":900,"event":"error","error":"500"},"REFUSE"),
("N4",{"response_cc":"max-age=600, stale-while-revalidate=3\u00e9","freshness_lifetime":600,"current_age":615,"event":"request"},"REFUSE"),
("N5",{"response_cc":'foo="\u0100", stale-while-revalidate=30',"freshness_lifetime":600,"current_age":615,"event":"request"},"REFUSE"),
("N6",{"response_cc":"stale-while-revalidate=99999999999","freshness_lifetime":0,"current_age":2147483648,"event":"request"},("serve-stale-revalidate",2147483648)),
("N6b",{"response_cc":"stale-while-revalidate=99999999999","freshness_lifetime":0,"current_age":2147483649,"event":"request"},("revalidate",2147483649)),
("N7",{"response_cc":"max-age=600","request_cc":"stale-if-error=5, stale-if-error=60","freshness_lifetime":600,"current_age":640,"event":"error","error":500},("error-through",40)),
("N8",{"response_cc":"max-age=600, stale-if-error=300","freshness_lifetime":600,"current_age":900,"event":"error","error":504,"shared":True},("serve-stale-error",300)),
("A1",{"response_cc":"stale-while-revalidate="+"9"*5000,"freshness_lifetime":0,"current_age":2147483649,"event":"request"},("revalidate",2147483649)),
("A3",{"response_cc":"stale-while-revalidate="+"0"*5000+"5","freshness_lifetime":0,"current_age":5,"event":"request"},("serve-stale-revalidate",5)),
("SN",{"response_cc":"max-age=600","freshness_lifetime":600,"current_age":615,"event":"request","shared":None},"REFUSE"),
]
cand=sys.argv[1]; ok=0
for n,i,w in P:
    p=subprocess.run([sys.executable,"-I","-B",cand],input=json.dumps(i).encode(),capture_output=True)
    if w=="REFUSE": g= p.returncode==1 and p.stdout==b"" and p.stderr.startswith(b"invalid_input:")
    else:
        try: o=json.loads(p.stdout); g= p.returncode==0 and o=={"decision":w[0],"staleness":w[1]}
        except Exception: g=False
    ok+=g; print(n,"ok" if g else "FAIL",p.returncode,p.stdout[:80],p.stderr[:100])
print(f"probe {ok}/{len(P)}")
