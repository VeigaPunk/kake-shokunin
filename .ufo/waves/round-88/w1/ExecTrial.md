# ExecTrial — round 88 w1 (actual domain trial, C2 freshness)

Status: complete. One origin GET, no second request, no production byte written,
nothing published or deployed. All receipts are in
`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-88/w1/ExecTrial/`.

## 1. The capture

| field | value |
|---|---|
| URL / method | `https://ds4cc.com/` — `GET` |
| access date (UTC) | `2026-11-04T18:52:27Z` (`date -u` immediately before; identical to the response `Date`) |
| curl | 8.23.0, `-sS --max-time 30 --retry 0`, exit `0` |
| status | `200` |
| byte count | `78897` (`size_download`, equals `content-length`) |
| body sha256 | `f2c5d2b3ab34e8e1dd6d08566147664e4dc7d21a5b01acd7943fd719e8342e93` |
| header-file sha256 | `a94ce7a4ecb62adf72496aa5563ba1463a3fb1abcaefba589429550fdde5deb8` |
| peer / redirects | `2606:50c0:8003::153` / `0` |
| credentials, cookies, auth | none sent |
| document title | `DS4CC — ship-ready agent software, distributed plainly` |

Origin requests made: **1**. The second request (`https://kimi.page/`) was
permitted only if the first response carried no `Vary` field; it did carry one,
so no second request was made and the budget was not spent.

Exact commands and exits (cwd was the scratch dir, so the relative `-D`/`-o`
paths landed there, never in the lane):

```
$ date -u +%Y-%m-%dT%H:%M:%SZ                     -> 2026-11-04T18:52:27Z
$ curl -sS --max-time 30 --retry 0 \
       -A 'kake-r88-ExecTrial/1.0 (capability observation)' \
       -D h1.txt -o b1.bin \
       -w 'http_code=%{http_code} size_download=%{size_download} remote_ip=%{remote_ip} num_redirects=%{num_redirects}\n' \
       https://ds4cc.com/
  http_code=200 size_download=78897 remote_ip=2606:50c0:8003::153 num_redirects=0
  curl_exit=0
$ wc -c < b1.bin                                  -> 78897
$ sha256sum b1.bin h1.txt
  f2c5d2b3…2e93  b1.bin
  a94ce7a4…deb8  h1.txt
$ grep -c '^content-encoding:' h1.txt             -> 0        (exit 1: no such line)
$ python3 -B loopback-capture.py                  -> curl_exit=0 http_code=204 raw_request_bytes=115
```

Retained verbatim: `response-headers.txt`, `response-body.html`, `capture.json`,
`loopback-request.txt`, `loopback-capture.py`, the four payloads, `verdicts.json`.

## 2. Observed Vary — verbatim

```
vary: Accept-Encoding
```

Extracted, not normalised:

```
$ grep -n '^vary:' response-headers.txt | od -c
0000000   2   0   :   v   a   r   y   :       A   c   c   e   p   t   -
0000020   E   n   c   o   d   i   n   g  \r  \n
```

The field value is the 15 bytes `Accept-Encoding`, with no leading or trailing
SP/HTAB — so no trimming is required before comparing it, and no other field is
nominated. Companion lines that bound the observation (all verbatim in
`capture.json`):

```
content-type: text/html; charset=utf-8
cache-control: max-age=600
date: Wed, 04 Nov 2026 18:52:27 GMT
age: 0
expires: Wed, 04 Nov 2026 11:47:14 GMT
via: 1.1 varnish
x-cache: HIT
x-cache-hits: 0
x-proxy-cache: MISS
```

`content-encoding` is **absent** (`grep -c '^content-encoding:' response-headers.txt`
= `0`, exit `1`), i.e. the representation served is identity-coded — consistent
with a request that advertised no acceptable coding (see §3).

## 3. The request side (what the client actually sent)

The origin request bytes were not wire-traced (no `--trace-ascii`, and no second
request was permitted to obtain them), so the header set was established
independently on **loopback**, with the same curl flags and only the URL changed
(`loopback-request.txt`, script `loopback-capture.py`, re-run: `curl_exit=0
http_code=204 raw_request_bytes=115`):

```
GET / HTTP/1.1
Host: 127.0.0.1:39619
User-Agent: kake-r88-ExecTrial/1.0 (capability observation)
Accept: */*
```

Exactly three fields, and **no `Accept-Encoding`** (curl sends one only with
`--compressed`, which was not used). The origin GET negotiated HTTP/2, which
carries the same field set as pseudo-headers plus these three. Two corroborations
that the live request also carried no `Accept-Encoding`: the response has no
`content-encoding` (§2), and its `Vary: Accept-Encoding` is the only nomination
that could distinguish variants. This is command-derived evidence, not a capture
of the origin request itself — stated as a limit in §7.

## 4. Candidate replay — exact payloads and verdicts

Candidate: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-88/w1/ExecReader/vary_match.py`
(`sha256 51f5d7780c14cb1522c8de79cfd25c922a69242d057484d06a9a3de2d3e8adc1`,
12996 B, mtime `2026-11-04T18:55:42Z`, observed `18:57:21Z`).
Reference column is the C2 counter's own oracle (`c88_vary.reference`), not the
candidate.

### Required pair

**A — identical side** (`payload-identical.json`, sha256 `77630b77…423dff`):

```json
{
  "vary": "Accept-Encoding",
  "stored": {
    "host": "ds4cc.com",
    "user-agent": "kake-r88-ExecTrial/1.0 (capability observation)",
    "accept": "*/*"
  },
  "presented": {
    "host": "ds4cc.com",
    "user-agent": "kake-r88-ExecTrial/1.0 (capability observation)",
    "accept": "*/*"
  }
}
```

```
exit=0  stdout='match'  stderr=''      reference=match
```

**B — perturbed presented side, `accept-encoding: gzip` added** (`payload-perturbed.json`,
sha256 `5872e3ec…e21004`):

```json
{
  "vary": "Accept-Encoding",
  "stored": {
    "host": "ds4cc.com",
    "user-agent": "kake-r88-ExecTrial/1.0 (capability observation)",
    "accept": "*/*"
  },
  "presented": {
    "host": "ds4cc.com",
    "user-agent": "kake-r88-ExecTrial/1.0 (capability observation)",
    "accept": "*/*",
    "accept-encoding": "gzip"
  }
}
```

```
exit=0  stdout='mismatch'  stderr=''   reference=mismatch
```

Both verdicts equal the oracle's. `stored` is the request that selected the
representation we received (the one in §3); `presented` A is that same request
again, and B adds a coding to the **presented** side only, so the nominated field
is present on one side and absent on the other.

### Supplementary (not required by the seat, run because they bear on readability of the pair)

| payload | difference | exit | stdout | stderr | reference |
|---|---|---|---|---|---|
| `payload-supplementary-ua.json` | presented `user-agent` changed, nothing nominated touched | 0 | `match` | `` | `match` |
| `payload-probe-dupkey.json` | stored map carries `Accept-Encoding` **and** `accept-encoding` | 1 | `` | `invalid_input: stored field name 'accept-encoding' is an ambiguous case-variant duplicate` | `invalid` |

The first shows the verdict is driven by the nominated field only — a request that
differs in a field the origin did not nominate still matches, which is the
behaviour §4.1 requires and the one thing the required identical pair cannot show
by itself.

### Candidate volatility (honest)

The candidate was under active revision while this trial ran. Two snapshots were
scored:

| sha256 | size | mtime (local, -0300) | required pair |
|---|---|---|---|
| `286c32f3…ddcdf3` | 13195 | 15:55:28 | `match` / `mismatch` |
| `51f5d778…3e8adc1` | 12996 | 15:55:42 | `match` / `mismatch` |

Verdict details in `verdicts.json` bind to `51f5d778`. `replay.md` holds the four
byte-stable commands; **L1 must re-run them at carry time**, because a later
revision is not covered by these receipts.

## 5. What the trial proves and does not prove

**Proves.** On 2026-11-04T18:52:27Z the live surface `https://ds4cc.com/` emitted
`Vary: Accept-Encoding` — a real nomination, not a constructed one — so the C2
capability has at least one live target, and the reader returns `match` for the
captured request re-presented and `mismatch` when a coding is added to the
presented side, both agreeing with the counter's oracle, with an empty stderr and
exit 0 in both cases. It also proves the reader ignores a difference in a field
the response did not nominate.

**Does not prove.** One identical-side observation is not a discriminator: `match`
in case A is entailed by any implementation that equates two equal maps, and case
B only shows the reader refuses to equate a request that advertises a coding with
one that does not. Nothing here shows that ds4cc.com actually returns a *different
representation* per `Accept-Encoding` — that would need a second live request with
a coding, which the seat's budget and the presence of `Vary` in the first response
foreclosed. Likewise not proven: that any intermediary honours `Vary` on this
surface (the only nearby evidence is `x-cache: HIT` with `x-cache-hits: 0` and
`age: 0`, which is consistent with a just-stored object, and `x-proxy-cache: MISS`
alongside `x-cache: HIT`, i.e. two layers labelling the same response
differently); cache-key construction, storage, revalidation, freshness, serving or
any browser behaviour; anything at all about `kimi.page` (never requested); and no
claim that any surface is clean.

## 6. Defects found in the round's own material

**D-a (C2 profile under-declared; the counter cannot see it).** The counter's
reference refuses an *ambiguous case-variant duplicate field name in a request
map* (`c88_vary.py:75`, `return None  # ambiguous duplicate name, refused`), but
`contract.md:87`'s declared profile lists no such rule — it states case-insensitive
*field-name* comparison, `, ` combination, OWS trimming, absence rules and `*`,
and nothing about duplicate keys inside `stored`/`presented`. The frozen cases do
not exercise it either: case 13 is duplicate *Vary members*
(`vary-cases.json:14`), and `generate()` builds request keys from the
lowercase-only `NAMES` list, so no seeded case can contain both `Accept-Encoding`
and `accept-encoding` as keys.

Evidence that the rule is invisible to the scoring surface — a mutant of the
candidate with only the refusal deleted (`probe-var-dup-accept.py`, retained,
sha256 `980c57d1f57770a720200171d524df0077b85933bb31e2e22e07f433ab5f40c1`)
accepts the duplicate-key payload (`od -c` on its stdout: `m a t c h`, 5 bytes, no
newline; exit `0`; the oracle says `invalid`) and still scores full marks:

```
$ python3 -B c88_vary.py --tool .../w1/ExecTrial/probe-var-dup-accept.py --work …/work-base
{"claim": "C2", "frozen": 20, "frozen_total": 20, "random": 200, "random_total": 200,
 "met": true, "cases_sha256": "c461cbd8…b0802d", "random_sha256": "004a8eb7…bc2b50",
 "tool_sha256": "980c57d1…5f40c1", "details": []}          exit=0
```

So C2's 220 scored cases discriminate neither the presence nor the absence of a
rule the reference enforces. Either the profile text should state the refusal or
the reference should drop it; as it stands, a candidate that follows
`contract.md` exactly and a candidate that follows the reference disagree on an
input class no scored case covers. (Same command on the shipped bytes:
`frozen=20/20 random=200/200 met=true exit=0` at `51f5d778` — an observation at a
moving sha, **not** the carried gate; that remains L1's `--root/--revision` run.)

**D-b (surface header inconsistency, observed, bounded).** On the single response
captured, `expires: Wed, 04 Nov 2026 11:47:14 GMT` is 7 h 05 m 13 s **earlier**
than `date: Wed, 04 Nov 2026 18:52:27 GMT`, while `cache-control: max-age=600`
and `age: 0` make the response fresh for 600 s. `max-age` overrides `Expires`
(RFC 9111 §5.3), so this is a stale-looking `Expires` coexisting with a fresh
`max-age`, not a violation — but it is a configuration smell worth recording, and
it means `Expires` alone would give the wrong answer on this surface.

**D-c (label mismatch, observed).** `x-proxy-cache: MISS` and `x-cache: HIT` on the
same response, with `x-cache-hits: 0`. Both cannot describe the same cache; they
describe two layers (GitHub's proxy front and the Fastly edge, `via: 1.1 varnish`,
`x-served-by: cache-gig2250045-GIG`). Recorded as observed, with no inference
about which layer served the bytes.

No defect was found in the frozen 20-case set's labels: my two required payloads
and both supplementary probes agree with the oracle on every point they touch, and
the case-file sha printed by the counter (`c461cbd8…b0802d`) matches
`sha256sum vary-cases.json` independently.

## 7. Limits

- **Request side is command-derived.** The origin request bytes were not traced;
  the header set comes from a loopback run of the same curl flags. If a future
  curl changed a default header, only non-nominated fields could differ, and the
  nominated field's absence is fixed by not passing `--compressed` — but the
  claim "the origin saw exactly these three fields" is inference, not capture.
- **Single shot.** One response on one access date, 78 897 bytes, no repetition,
  no retry for a prettier result. Header values such as `x-cache` are per-response
  and say nothing about the steady state.
- **Body is a moving target.** The sha256 binds the bytes retained here; the site
  may change without notice, so the hash is a receipt, not a reproducibility
  guarantee.
- **Candidate moved during the trial** (§4); verdicts bind to one sha, and the
  replay is the transferable artifact.
- **Freshness is untouched.** Nothing here measures age, revalidation or serving;
  the C2 claim's 10 HOLD status is not moved by this seat, and the kimi.page
  surface was never contacted.
- Environment: linux 7.2.11-arch1-1, python 3.14, curl 8.23.0. **No tool was
  installed or upgraded** for this seat, so there is no tool/version/channel entry
  to record; `pacman` was not invoked.

## 8. Files and digests

```
a94ce7a4ecb62adf72496aa5563ba1463a3fb1abcaefba589429550fdde5deb8  response-headers.txt      (654 B)
f2c5d2b3ab34e8e1dd6d08566147664e4dc7d21a5b01acd7943fd719e8342e93  response-body.html        (78897 B)
77630b7797c2052104ae302976ca9fb7af9e80c2e0a5db331cb3560464423dff  payload-identical.json    (301 B)
5872e3ec63dc4d6723b5f5c032584de2b2c09099bbf871c5db127f87a0e21004  payload-perturbed.json    (332 B)
65873044070d1444ed0fe09a4056e8418dee92489cc44fbfc795fc95a15dd3a7  payload-supplementary-ua.json
8a816d44ec6ee42fe2dec8ac782aa7997be1f5a85a851ef8776dd972dafff884  payload-probe-dupkey.json
51f5d7780c14cb1522c8de79cfd25c922a69242d057484d06a9a3de2d3e8adc1  candidate-snapshot-51f5d778.py  (12996 B)
980c57d1f57770a720200171d524df0077b85933bb31e2e22e07f433ab5f40c1  probe-var-dup-accept.py   (12847 B)
```

`capture.json` (metadata + verbatim header lines), `verdicts.json` (four probes,
candidate sha/size/mtime, oracle column), `loopback-request.txt`,
`loopback-capture.py`, `replay.md` (byte-stable re-run commands for L1). The two
`.py` files are receipts, not candidates: `candidate-snapshot-51f5d778.py` is the
exact candidate byte string my verdicts bind to (ExecReader may revise it), and
`probe-var-dup-accept.py` is the D-a fixture. Neither is a production path and
neither is imported by anything.
