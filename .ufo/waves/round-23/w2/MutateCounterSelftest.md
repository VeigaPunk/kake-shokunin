# Round 23 wave 2 — counter selftest mutation probe

## Verdict

**Counterexample found: the selftest does not detect many individual counter-check weakenings.** This is a coverage finding, not a finding that the frozen production receipts are invalid, and not an admission/integration verdict.

At frozen candidate `5e5afb9e4d8ee18831b9b35b35e8a34e47aceecd`, tested **71 one-at-a-time structural mutants: 13 killed, 58 survived, 0 inconclusive**.

| Counter / judged axis | Mutants | Killed | Survived | Inconclusive |
| --- | ---: | ---: | ---: | ---: |
| C1 / freshness | 41 | 5 | 36 | 0 |
| C2 / operability | 30 | 8 | 22 | 0 |
| Total | 71 | 13 | 58 | 0 |

## Findings

### P2 — C1 selftest leaves freshness, receipt integrity, and correction checks mutation-survivable

**Impacted claim/axis:** C1 / freshness. Examples: `C1-08` disables the observedAt date cutoff; `C1-14` disables required-field validation; `C1-25` disables claim citations in the round-23 section; `C1-26` disables the entire STALE-correction branch; `C1-29` disables correction inclusion; `C1-31` disables UNVERIFIABLE reasons; `C1-34` disables the frozen-population digest. Each mutant returned selftest exit 0 with `selftest: passed`, all seven cases passed, and empty stderr. Each had a passing pristine run and a passing byte-exact restored run.

Other surviving C1 mutations cover receipt existence/JSON/object handling, population unit/path matching, date type, claims array shape/nonemptiness, missing current unit, claim object/type/nonblank and each of the seven required field names, duplicate IDs, allowed verdicts, frozen-population dispatch/readability, revision resolution, and heading-dependent section selection. The complete matrix below distinguishes these checks.

**Smallest fix:** add isolated synthetic invalid-receipt fixtures for these checks to the existing selftest, including STALE-without-correction, STALE-correction-outside-section, missing citation, missing UNVERIFIABLE reason, pre-cutoff timestamp, and modified population. Keep the counter contract unchanged. For guards protected by another guard or a later exception, assert the intended structured rejection rather than assuming guard removal necessarily accepts invalid data.

### P2 — C2 selftest leaves snapshot identity, freshness, body digest, and replay-exit checks mutation-survivable

**Impacted claim/axis:** C2 / operability. `C2-11` removes URL matching while leaving the tested GET-method check active. `C2-14` removes the fetchedAt cutoff. `C2-20` removes comparison of stored page SHA-256 with fetch.sha256. `C2-29` compares audit results only, ignoring the reproduced validator exit. All survived: exit 0, `selftest: passed`, all seven cases passed, stderr empty, with passing pristine/restored controls.

Further C2 survivors remove served-status type/lower bound, error/truncation/Content-Type guards; fetch/audit presence and JSON rejection; fetchedAt type; non-served page absence, verdict and status matching; served page presence; validator JSON rejection; revision/population/validator readability; and the frozen-population digest. In particular, the existing non-GET case kills method removal, not URL removal; the existing changed-audit-verdict case kills result comparison removal, not exit comparison removal.

**Smallest fix:** add negative fixtures changing only URL, timestamp, digest, audit exit, non-served status/verdict/page presence, each served-classification atom, population digest, and unreadable/invalid inputs. Preserve the existing production checks and GET-only contract.

### Exact detector command and mutation propagation

Every detector invocation used the following exact argv from the working directory shown (no network):

Working directory: `/tmp/kake-r23w2-MutateCounterSelftest-htuV/clone`

```text
python3 .ufo/waves/round-23/counter_selftest.py
```

Clone setup actually run:

```text
git clone --no-hardlinks /home/vgpnk/Projects/shokunin/kake-shokunin /tmp/kake-r23w2-MutateCounterSelftest-htuV/clone
git -C /tmp/kake-r23w2-MutateCounterSelftest-htuV/clone checkout --detach 5e5afb9e4d8ee18831b9b35b35e8a34e47aceecd
```

Each mutant was applied through a single-node `xd://ast_edit` proposal and `xd://resolve`, then committed **only in the scratch clone**. This matters: counter_selftest.py clones its own ROOT, so an uncommitted mutation would not reach the detector. The committed source blob SHA-256 was required to equal the mutated working-file SHA-256 before each run. The original file was restored in a finally block, committed, hashed, and subjected to the same detector. The prior restored run serves as the next mutant’s pristine control; the first mutant has a separate initial pristine run. Thus 143 detector invocations = 1 initial pristine + 71 mutated + 71 restored. There were no baseline/restoration failures or timeouts.

Expected outcomes were recorded before the probes in `/tmp/kake-r23w2-MutateCounterSelftest-htuV/expectations.json`. Expected 12 kills and 59 survivors; observed 13 kills and 58 survivors. The sole mismatch was C2-01: ignoring git-show failure turns the deliberately absent non-served page into empty bytes, so the valid 404 fixture detects `page.html stored for a non-served response`.

### Complete mutation matrix

“0; all 7 pass” means the actual selftest stdout parses to `selftest: passed` and seven passed cases, with stderr empty. Failure entries name the exact failing case; verbatim stdout/stderr for every invocation, including pristine and restored controls, are embedded in the evidence appendix. Mutations are individual; overlapping aggregate/atomic variants are not independent semantic obligations.

| ID | Counter check | Exact AST pattern → replacement | Expected | Actual output / verdict | Mutated file SHA-256 |
| --- | --- | --- | --- | --- | --- |
| C1-01 | Git show return code | `done.returncode == 0` → `True` | survived | exit 0; all 7 pass; **survived** | `6af416858f5584ba95aa3e9e924f9a7b9bfec118c585877e41de200a876f7d7f` |
| C1-02 | Missing receipt rejection | `return ["receipt missing"], verdicts` → `return [], verdicts` | survived | exit 0; all 7 pass; **survived** | `7c49761665d34746311b599fc0449120ee5a2137fe1323ae91b279b9e15ad2cd` |
| C1-03 | Invalid receipt JSON rejection | `return [f"receipt is not JSON: {exc}"], verdicts` → `return [], verdicts` | survived | exit 0; all 7 pass; **survived** | `31cdb0fce41bb064a44949b5a692fd2d97141636099e9b5dcb0bef5a99444436` |
| C1-04 | Receipt object rejection | `return ["receipt is not an object"], verdicts` → `return [], verdicts` | survived | exit 0; all 7 pass; **survived** | `b5dd527ec2a4d7b1801b4a943a7333873d73e58d84d2d53ada23fb1271249488` |
| C1-05 | Receipt unit matches population | `receipt.get("unit") != unit["unit"]` → `False` | survived | exit 0; all 7 pass; **survived** | `2b55608cf1628abbe20a1bf7302900150dbe0ad290bf3a826e48b023ddefbbdb` |
| C1-06 | Receipt path matches population | `receipt.get("path") != unit["path"]` → `False` | survived | exit 0; all 7 pass; **survived** | `dcb8a6c9e711cd35eaa5aa9b66045b3e817fef9dda0d8c859e3d4c10a622b601` |
| C1-07 | observedAt is a string | `not isinstance(receipt.get("observedAt"), str)` → `False` | survived | exit 0; all 7 pass; **survived** | `40f377ea41c946e03b5be9a281939755076b4daa9c8b0e633dff11705f014c8e` |
| C1-08 | observedAt date cutoff | `receipt["observedAt"][:10] < "2026-10-21"` → `False` | survived | exit 0; all 7 pass; **survived** | `451c0b5a69d52bc362bb91e52de66b4dec2f5a2900d384b3ef5526b21a9115ee` |
| C1-09 | Claims array type | `not isinstance(claims, list)` → `False` | survived | exit 0; all 7 pass; **survived** | `71637c4534b1f4b577220b93c5910f8cc00834bebc110352309c106c89c21753` |
| C1-10 | Claims array nonempty | `not claims` → `False` | survived | exit 0; all 7 pass; **survived** | `4cf4887cd4a861c6a813d3efc2077a3bc1aa1acb0f0ce9e91123f91f67e0da4e` |
| C1-11 | Missing current unit rejection | `return problems + ["unit file missing at revision"], verdicts` → `return problems, verdicts` | survived | exit 0; all 7 pass; **survived** | `d53c382179c5157e952c56fbddf244eed33b2c62c86b418b20f8016263b1d193` |
| C1-12 | Round-23 heading diagnostic | `position < 0` → `False` | killed | exit 1; C1 missing heading rejected with diagnostic; **killed** | `5a795942b82d1acb85dcae9609ff6ee3f4826da4c758504c18607f21c2ca8d54` |
| C1-13 | Claim row object type | `not isinstance(claim, dict)` → `False` | survived | exit 0; all 7 pass; **survived** | `27590fb579067b6b039c7ad8bd41c020382efa794022ab132d0890e4b169812e` |
| C1-14 | Required claim fields guard | `any(not isinstance(claim.get(k), str) or not claim[k].strip() for k in FIELDS)` → `False` | survived | exit 0; all 7 pass; **survived** | `9350f3344d4be91500020306369559648c6cff14f164fe6dd7c2d621843d97a5` |
| C1-15 | Required claim field id | `FIELDS = ("id", "anchor", "claim", "surface", "method", "observation", "verdict")` → `FIELDS = ('anchor', 'claim', 'surface', 'method', 'observation', 'verdict')` | survived | exit 0; all 7 pass; **survived** | `239087d32817f4d094183860ee84291158a0c99536755f8503cf46c88f3f7b08` |
| C1-16 | Required claim field anchor | `FIELDS = ("id", "anchor", "claim", "surface", "method", "observation", "verdict")` → `FIELDS = ('id', 'claim', 'surface', 'method', 'observation', 'verdict')` | survived | exit 0; all 7 pass; **survived** | `2402d63f34c434c113ae850f156969ee96d48ebb1998231e27bfbdca40385881` |
| C1-17 | Required claim field claim | `FIELDS = ("id", "anchor", "claim", "surface", "method", "observation", "verdict")` → `FIELDS = ('id', 'anchor', 'surface', 'method', 'observation', 'verdict')` | survived | exit 0; all 7 pass; **survived** | `525442da1d79644df0e01afa8285d1fba8d4b0b7c9389bda0ec6a2c1810b1304` |
| C1-18 | Required claim field surface | `FIELDS = ("id", "anchor", "claim", "surface", "method", "observation", "verdict")` → `FIELDS = ('id', 'anchor', 'claim', 'method', 'observation', 'verdict')` | survived | exit 0; all 7 pass; **survived** | `034e3e9ad721bd56dde7ee390a9426cf97e8c47e0785034c9133076edbe66cac` |
| C1-19 | Required claim field method | `FIELDS = ("id", "anchor", "claim", "surface", "method", "observation", "verdict")` → `FIELDS = ('id', 'anchor', 'claim', 'surface', 'observation', 'verdict')` | survived | exit 0; all 7 pass; **survived** | `a3d3f2a18a180be15416fdeb014e9e2c3b233bc5246262e626623aa7f1c9795a` |
| C1-20 | Required claim field observation | `FIELDS = ("id", "anchor", "claim", "surface", "method", "observation", "verdict")` → `FIELDS = ('id', 'anchor', 'claim', 'surface', 'method', 'verdict')` | survived | exit 0; all 7 pass; **survived** | `bbc857e9011e1f6da4d091a118cc294e16be98bad674a35d72cd9881f082818f` |
| C1-21 | Required claim field verdict | `FIELDS = ("id", "anchor", "claim", "surface", "method", "observation", "verdict")` → `FIELDS = ('id', 'anchor', 'claim', 'surface', 'method', 'observation')` | survived | exit 0; all 7 pass; **survived** | `33731cf2555b2dba5fdd865ec719fb11700f885591b1ce66307f79de0c9e31f6` |
| C1-22 | Duplicate claim IDs | `claim["id"] in seen` → `False` | survived | exit 0; all 7 pass; **survived** | `d527b7fa022a74d1254fe2966bd22624ee8da021213e91d760a60cfa0ad6757d` |
| C1-23 | Allowed verdict membership | `verdict not in VERDICTS` → `False` | survived | exit 0; all 7 pass; **survived** | `9b63107cbe0285040c79ddc7eaf6c26db3bb096f8c61fb39302ea78d2d4958e8` |
| C1-24 | Anchor belongs to base unit | `claim["anchor"] not in base_text` → `False` | killed | exit 1; C1 invalid receipt rejected; **killed** | `911420b5e807cbcdfd4634c9b9e6f1449b8764bc9d5de648318ca59560d7d3a6` |
| C1-25 | Claim cited after heading | `f"[{unit['unit']}:{claim['id']}]" not in section` → `False` | survived | exit 0; all 7 pass; **survived** | `aee8e79ea50c5f1a7ca710bc9401520d091bbda45cb37aa73216f988d819876b` |
| C1-26 | STALE correction dispatch | `verdict == "STALE"` → `False` | survived | exit 0; all 7 pass; **survived** | `b62798a0016352fa08a141caa6c54469fa6f0f969a1a833aa94db01a35e52855` |
| C1-27 | Correction string type | `not isinstance(correction, str)` → `False` | survived | exit 0; all 7 pass; **survived** | `d37d6c6ee6d46d37fa52371f6fbb20c0eb5e04f6ee8a195e4bcf1615c961620a` |
| C1-28 | Correction nonblank | `not correction.strip()` → `False` | survived | exit 0; all 7 pass; **survived** | `28860cd7d4e5d1c79cbfbd28db6123a845ea7fbdf10802cd82c03b4098966f5d` |
| C1-29 | Correction in appended section | `correction not in section` → `False` | survived | exit 0; all 7 pass; **survived** | `24071c6c09aa59cc5a6eb4c4824ddba8f002e26b07848fed5298c03138aaab96` |
| C1-30 | UNVERIFIABLE reason dispatch | `verdict == "UNVERIFIABLE"` → `False` | survived | exit 0; all 7 pass; **survived** | `3be799e9818b274752fc6913cb466b36fcb0356e08e6224fc0da2990c5560ee5` |
| C1-31 | UNVERIFIABLE reason nonblank | `not str(claim.get("reason", "")).strip()` → `False` | survived | exit 0; all 7 pass; **survived** | `210d84a5c6a05056ad8f26a83ac1c6de9898cbfcf74df1d0ac507d335c3eab05` |
| C1-32 | At least one live-decided claim | `verdicts["HOLD"] + verdicts["STALE"] == 0` → `False` | killed | exit 1; C1 all-UNVERIFIABLE receipt rejected; **killed** | `f03a73b8eccfef62e92944341119c735de5682dcab47d931f26e4ac1ffcd1658` |
| C1-33 | Frozen population guard dispatch | `population_raw is not None` → `False` | survived | exit 0; all 7 pass; **survived** | `3adf6a11f8e2e87d6dcbb890d025a8641b44474fdff6751dbb795fe6c409532b` |
| C1-34 | Frozen population digest | `hashlib.sha256(population_raw.encode("utf-8")).hexdigest() != POPULATION_SHA256` → `False` | survived | exit 0; all 7 pass; **survived** | `3ed8765cb4b12f110034bff4df7417a9233042841f9cc9fcd4eb9927efdce410` |
| C1-35 | Revision resolves to a commit | `resolved.returncode != 0` → `False` | survived | exit 0; all 7 pass; **survived** | `b1876666fc5f4c3aef3684f6adc7db8d0e8d02acc123caaf97fee91d85bc11e7` |
| C1-36 | Population readable | `population_raw is None` → `False` | survived | exit 0; all 7 pass; **survived** | `fcc08f6a44b7e64ea082049b49c7ac791a2b3a8f8800283ad404fc5a7cacdd35` |
| C1-37 | Per-unit acceptance uses problems | `not problems` → `True` | killed | exit 1; C1 invalid receipt rejected; **killed** | `d1f5796e08f61bc6dca3b231141fc1226c43404f5386fa44cd546744c167ebde` |
| C1-38 | Overall exit rejects any failed unit | `accepted == len(units)` → `True` | killed | exit 1; C1 invalid receipt rejected; **killed** | `701829e0d4e79d7b95734b563cf3b0023f03aaf63e83d092013f37ab6d7b5f75` |
| C1-39 | Section is gated on heading presence | `position >= 0` → `True` | survived | exit 0; all 7 pass; **survived** | `23b09bde38c46c439bfa548c226b2d4643ca6b93e92c82d3ef46bef95c9866a2` |
| C1-40 | Required field string type | `not isinstance(claim.get(k), str)` → `False` | survived | exit 0; all 7 pass; **survived** | `d1664e99ae799318b7cf7fc859553458f990f4386c38ef45a5b4693618fdd234` |
| C1-41 | Required field nonblank | `not claim[k].strip()` → `False` | survived | exit 0; all 7 pass; **survived** | `05a8c2b1b97c89e89fc5f0bb560638a0ac472eb99f68b1413654a807dde54aaa` |
| C2-01 | Git show return code | `done.returncode == 0` → `True` | survived | exit 1; C2 valid live receipts; **killed** | `7b584d3f77f46369b9dfb3b98ee12e89f5c2dcaba12646428cdc7a04b00b4c3c` |
| C2-02 | Served status integer type | `isinstance(status, int)` → `True` | survived | exit 0; all 7 pass; **survived** | `e833e8da38441bc42fe246f21ce13362e42df8401e92c8b66b014cb07309a25a` |
| C2-03 | Served status lower bound | `200 <= status < 300` → `status < 300` | survived | exit 0; all 7 pass; **survived** | `be7d3088a440bfdffb9ab062c55d86bce4e02b9010a1639d90733944dcec4645` |
| C2-04 | Served status upper bound | `200 <= status < 300` → `200 <= status` | killed | exit 1; C2 valid live receipts; **killed** | `565871a6442449a227d547edad5abe985f885b020aa17c3cce025d94c963f781` |
| C2-05 | Served fetch has no error | `fetch.get("error") is None` → `True` | survived | exit 0; all 7 pass; **survived** | `977e339df3a532e831fe862ccb661073ad5cd2c3c3b2e58161c7087fea580ca0` |
| C2-06 | Served fetch is not truncated | `not fetch.get("truncated")` → `True` | survived | exit 0; all 7 pass; **survived** | `da3483fc4f6667590484d1a75ac57145a7bb9b3517c528fe3e040182d0b3cb5c` |
| C2-07 | Served Content-Type HTML | `ctype.split(";")[0].strip().lower() == "text/html"` → `True` | survived | exit 0; all 7 pass; **survived** | `0b389fa0624eeb489378bd27506f6113662af8483317934fbfc2e1b8d47fa46c` |
| C2-08 | Fetch metadata present | `raw_fetch is None` → `False` | survived | exit 0; all 7 pass; **survived** | `bac59a78cd75404b5c8739ef6819b224bc91d975bba98d22b14572abad694adf` |
| C2-09 | Audit receipt present | `raw_audit is None` → `False` | survived | exit 0; all 7 pass; **survived** | `547dd95df3cf773d2a6c97e11981b122b671590e604470e21ad95f26eeb74156` |
| C2-10 | Receipt JSON parsing rejection | `return [f"receipt JSON invalid: {exc}"], None` → `return [], None` | survived | exit 0; all 7 pass; **survived** | `61d7eefea8b6a37f509205eca57bffb143cd05affc59c88e9cb8ce06e0e6fde0` |
| C2-11 | Fetch URL matches population | `fetch.get("url") != surface["url"]` → `False` | survived | exit 0; all 7 pass; **survived** | `a0df21c9627a1e0c97376dec43e4e7e9f07b3c8c7f1d4f36073ae9911707dea7` |
| C2-12 | Fetch method GET | `fetch.get("method") != "GET"` → `False` | killed | exit 1; C2 non-GET fetch rejected; **killed** | `4d44aa70c821cc3da7f94b1b12764c8ef6c4c39a44b993dee014fce429df587f` |
| C2-13 | fetchedAt is a string | `not isinstance(fetch.get("fetchedAt"), str)` → `False` | survived | exit 0; all 7 pass; **survived** | `4079d5507ead65ad465919f66bf6c9f3a8576f95eed3c3a93f73115bab059990` |
| C2-14 | fetchedAt date cutoff | `fetch["fetchedAt"][:10] < "2026-10-21"` → `False` | survived | exit 0; all 7 pass; **survived** | `ec72ece7fb0d9ec2abdf9b73e821f05606a2646395c203637f6dabc7d0b88062` |
| C2-15 | Non-served branch dispatch | `not served(fetch)` → `False` | killed | exit 1; C2 valid live receipts; **killed** | `8524505132739c8fd3f53ce50b3aaaad3ca267deb0d25a722a97b31d9c5b7cfb` |
| C2-16 | Non-served response has no page | `page is not None` → `False` | survived | exit 0; all 7 pass; **survived** | `af5821f85d28e85cb0df26077993ff1183cb3b9f6ba5b189a8338e9e8e6f92f2` |
| C2-17 | Non-served receipt verdict | `receipt.get("verdict") != "not-served"` → `False` | survived | exit 0; all 7 pass; **survived** | `0ef6a6bb65489648beff33d201a1510b554d25bfc558e55a8b891d2feaf13c4e` |
| C2-18 | Non-served receipt status matches | `receipt.get("status") != fetch.get("status")` → `False` | survived | exit 0; all 7 pass; **survived** | `88e7c5bd07b10c66f591e607419ceee39f266632c825be5ead167c0f315b093e` |
| C2-19 | Served page bytes present | `page is None` → `False` | survived | exit 0; all 7 pass; **survived** | `3e1227ad22740a111d46f26bbaedb34e8e2742fe1435db194b526f86ab7d5e77` |
| C2-20 | Served page digest matches fetch | `hashlib.sha256(page).hexdigest() != fetch.get("sha256")` → `False` | survived | exit 0; all 7 pass; **survived** | `3de1d7594b4af741237aff1f2f61b9bb971bf27059b1673b8b8f1e3aa4ef20d5` |
| C2-21 | Validator emits JSON rejection | `return problems + ["validator did not emit JSON"], None` → `return problems, None` | survived | exit 0; all 7 pass; **survived** | `74962a273f5ca34698b83adf6c6e65178bad87c4e9c2065efa12816e0c61c8a4` |
| C2-22 | Stored audit equals reproduced audit | `receipt != actual` → `False` | killed | exit 1; C2 unreproducible receipt rejected; **killed** | `bb20d6dc24917cfdb910e5d41ad0899b0d49b6d38f0477b9d9f4baa13b764ff6` |
| C2-23 | Revision resolves to a commit | `resolved.returncode != 0` → `False` | survived | exit 0; all 7 pass; **survived** | `4583401ed50aafa316a978038e587c2f74824e6645a8de8d0564943cd41a7a2b` |
| C2-24 | Population readable | `population is None` → `False` | survived | exit 0; all 7 pass; **survived** | `ae40f2d34e99497f6710192773588b829a8f46af3fbe101a30917363c960a46e` |
| C2-25 | Validator readable | `validator is None` → `False` | survived | exit 0; all 7 pass; **survived** | `71e74fc44cbe5b446bb6a6787bc3e045e8544c775134ef44724a4cf9234ccbcf` |
| C2-26 | Frozen population digest | `hashlib.sha256(population).hexdigest() != POPULATION_SHA256` → `False` | survived | exit 0; all 7 pass; **survived** | `aac57bcce8f277d7a1e1b5a8a3d16c92035e05b07b3b0dc97246f4711895cc3f` |
| C2-27 | Per-surface acceptance uses problems | `not problems` → `True` | killed | exit 1; C2 unreproducible receipt rejected; **killed** | `106411a335788b52460c35673256bf5230c046795581b885d1980f0da794c8af` |
| C2-28 | Overall exit rejects any failed surface | `accepted == len(rows)` → `True` | killed | exit 1; C2 unreproducible receipt rejected; **killed** | `3da86d0e539e02045127ad2f22605ea3d9d5b4115adf210331910473b0f2f7c1` |
| C2-29 | Stored audit exit equals reproduced exit | `receipt != actual` → `receipt.get("result") != actual.get("result")` | survived | exit 0; all 7 pass; **survived** | `2e5bb253b9d4d7e801869bc86df1ac94f4328f6841fc5f0cf7adc802f503847c` |
| C2-30 | Stored audit result equals reproduced result | `receipt != actual` → `receipt.get("exit") != actual.get("exit")` | killed | exit 1; C2 unreproducible receipt rejected; **killed** | `d80b0c39d7a893e74b890930ecffe2b999f81a0567f741902ac1b73a651a0bcb` |

## Checked and held

### Detector kills

- **C1:** C1-12 heading diagnostic; C1-24 base anchor; C1-32 at least one live-decided claim; C1-37 failed-unit acceptance propagation; C1-38 overall failure exit.
- **C2:** C2-01 git-show failure handling (caught by the valid non-served fixture); C2-04 status upper bound; C2-12 GET method; C2-15 non-served branch selection; C2-22 complete audit equality; C2-27 failed-surface acceptance propagation; C2-28 overall failure exit; C2-30 audit result comparison.
- C1-12 is killed by the required **diagnostic**, not by a changed accepted count: citations still reject the missing-heading unit. C2-01/C2-04/C2-15 are killed by the valid 404 fixture. These distinctions are retained rather than overstating independent negative coverage.

### Pristine/restored detector cases

All seven cases passed on the initial pristine run and each of 71 restored runs:

| Case | Counter exit | Accepted / total | Selftest case passed |
| --- | ---: | --- | --- |
| C1 valid receipts | 0 | 17/17 | true |
| C2 valid live receipts | 0 | 12/12 | true |
| C1 invalid receipt rejected | 1 | 16/17 | true |
| C1 missing heading rejected with diagnostic | 1 | 16/17 | true |
| C2 unreproducible receipt rejected | 1 | 11/12 | true |
| C1 all-UNVERIFIABLE receipt rejected | 1 | 16/17 | true |
| C2 non-GET fetch rejected | 1 | 11/12 | true |

### Exact-byte restoration

Before every mutation and after every restoration, the following SHA-256 values held. Only the selected counter changed during each mutated run; the other counter and detector stayed unchanged. The appendix records before/mutated/restored hashes and committed blob hashes for all 71 probes.

| File beneath `/tmp/kake-r23w2-MutateCounterSelftest-htuV/clone/.ufo/waves/round-23` | Original and final restored SHA-256 |
| --- | --- |
| `measure_c1.py` | `c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5` |
| `measure_c2.py` | `ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c` |
| `counter_selftest.py` | `5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d` |

Final scratch restored commit: `eefc66d36656c43cfd352f27559fa3fad5ae9093`. This is a scratch-history descendant containing exact candidate counter/detector bytes, not a production revision or integrated change.

## Limits

- This probe examines the committed selftest as a bounded detector, not the actual live truth of 17 units or 12 surfaces. It does not independently re-fetch web properties or rerun the production counters against the frozen live receipts.
- “Each check” is enumerated as every explicit counter validation predicate/error-return, independent compound atoms, both acceptance/exit gates, the shared required-field guard plus all seven declared fields, heading section selection, and separate audit exit/result comparison. It does not mutate parser invocation plumbing, loop structure, CLI argument declarations, or Python’s `__main__` guard. There are no claims of exhaustive mutation-operator coverage.
- A survivor means this selected mutation passed this detector. Some structural guard-removal mutants can remain protected by another validation or raise later on malformed inputs; no invalid-input acceptance witness is claimed for every survivor. The date-cutoff, correction-branch, body-digest, and audit-exit mutants still establish concrete detector blind spots without changing the contract.
- Expected outcomes were derived before execution; the C2-01 mismatch is disclosed. No failures were relabelled as baseline failures, and no failed baseline was counted as a kill.
- No production edits, lane git/index/jj writes, sibling-source edits, network actions, builds, lint, formatters, host service changes, or subagent dispatch. Only this report was written in the lane. Scratch-only Git commits preserve every mutant and exact restoration.
- Runtime used: Python 3.14.8 (observed `python3 --version`; interpreter path in detector output `/usr/bin/python3`). No tool installations or updates.

## Evidence appendix — exact actual outputs and hashes

Complete machine-readable ledger follows. stdout/stderr are JSON-escaped verbatim captured strings, including final newlines; no output is normalized or elided. Each record contains its predeclared mutation/expectation, local commit identities, before/mutated/restored hashes, committed blob hash, and pristine/mutated/restored detector results. The same bytes are also retained at `/tmp/kake-r23w2-MutateCounterSelftest-htuV/mutation-ledger.json`.

```json
{
  "protocol": {
    "axes": [
      "freshness",
      "operability"
    ],
    "revision": "5e5afb9e4d8ee18831b9b35b35e8a34e47aceecd",
    "command": [
      "python3",
      ".ufo/waves/round-23/counter_selftest.py"
    ],
    "sourceSha256": {
      "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
      "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
      "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
    },
    "mutants": [
      {
        "id": "C1-01",
        "script": "measure_c1.py",
        "check": "Git show return code",
        "pattern": "done.returncode == 0",
        "replacement": "True",
        "expected": "survived",
        "expectationReason": "No selftest fixture invalidates this check."
      },
      {
        "id": "C1-02",
        "script": "measure_c1.py",
        "check": "Missing receipt rejection",
        "pattern": "return [\"receipt missing\"], verdicts",
        "replacement": "return [], verdicts",
        "expected": "survived",
        "expectationReason": "No selftest fixture invalidates this check."
      },
      {
        "id": "C1-03",
        "script": "measure_c1.py",
        "check": "Invalid receipt JSON rejection",
        "pattern": "return [f\"receipt is not JSON: {exc}\"], verdicts",
        "replacement": "return [], verdicts",
        "expected": "survived",
        "expectationReason": "No selftest fixture invalidates this check."
      },
      {
        "id": "C1-04",
        "script": "measure_c1.py",
        "check": "Receipt object rejection",
        "pattern": "return [\"receipt is not an object\"], verdicts",
        "replacement": "return [], verdicts",
        "expected": "survived",
        "expectationReason": "No selftest fixture invalidates this check."
      },
      {
        "id": "C1-05",
        "script": "measure_c1.py",
        "check": "Receipt unit matches population",
        "pattern": "receipt.get(\"unit\") != unit[\"unit\"]",
        "replacement": "False",
        "expected": "survived",
        "expectationReason": "No selftest fixture invalidates this check."
      },
      {
        "id": "C1-06",
        "script": "measure_c1.py",
        "check": "Receipt path matches population",
        "pattern": "receipt.get(\"path\") != unit[\"path\"]",
        "replacement": "False",
        "expected": "survived",
        "expectationReason": "No selftest fixture invalidates this check."
      },
      {
        "id": "C1-07",
        "script": "measure_c1.py",
        "check": "observedAt is a string",
        "pattern": "not isinstance(receipt.get(\"observedAt\"), str)",
        "replacement": "False",
        "expected": "survived",
        "expectationReason": "No selftest fixture invalidates this check."
      },
      {
        "id": "C1-08",
        "script": "measure_c1.py",
        "check": "observedAt date cutoff",
        "pattern": "receipt[\"observedAt\"][:10] < \"2026-10-21\"",
        "replacement": "False",
        "expected": "survived",
        "expectationReason": "No selftest fixture invalidates this check."
      },
      {
        "id": "C1-09",
        "script": "measure_c1.py",
        "check": "Claims array type",
        "pattern": "not isinstance(claims, list)",
        "replacement": "False",
        "expected": "survived",
        "expectationReason": "No selftest fixture invalidates this check."
      },
      {
        "id": "C1-10",
        "script": "measure_c1.py",
        "check": "Claims array nonempty",
        "pattern": "not claims",
        "replacement": "False",
        "expected": "survived",
        "expectationReason": "No selftest fixture invalidates this check."
      },
      {
        "id": "C1-11",
        "script": "measure_c1.py",
        "check": "Missing current unit rejection",
        "pattern": "return problems + [\"unit file missing at revision\"], verdicts",
        "replacement": "return problems, verdicts",
        "expected": "survived",
        "expectationReason": "No selftest fixture invalidates this check."
      },
      {
        "id": "C1-12",
        "script": "measure_c1.py",
        "check": "Round-23 heading diagnostic",
        "pattern": "position < 0",
        "replacement": "False",
        "expected": "killed",
        "expectationReason": "Missing-heading fixture requires the explicit heading diagnostic, even though citation checks also fail."
      },
      {
        "id": "C1-13",
        "script": "measure_c1.py",
        "check": "Claim row object type",
        "pattern": "not isinstance(claim, dict)",
        "replacement": "False",
        "expected": "survived",
        "expectationReason": "No selftest fixture invalidates this check."
      },
      {
        "id": "C1-14",
        "script": "measure_c1.py",
        "check": "Required claim fields guard",
        "pattern": "any(not isinstance(claim.get(k), str) or not claim[k].strip() for k in FIELDS)",
        "replacement": "False",
        "expected": "survived",
        "expectationReason": "No selftest fixture invalidates this check."
      },
      {
        "id": "C1-15",
        "script": "measure_c1.py",
        "check": "Required claim field id",
        "pattern": "FIELDS = (\"id\", \"anchor\", \"claim\", \"surface\", \"method\", \"observation\", \"verdict\")",
        "replacement": "FIELDS = ('anchor', 'claim', 'surface', 'method', 'observation', 'verdict')",
        "expected": "survived",
        "expectationReason": "No selftest fixture invalidates this check."
      },
      {
        "id": "C1-16",
        "script": "measure_c1.py",
        "check": "Required claim field anchor",
        "pattern": "FIELDS = (\"id\", \"anchor\", \"claim\", \"surface\", \"method\", \"observation\", \"verdict\")",
        "replacement": "FIELDS = ('id', 'claim', 'surface', 'method', 'observation', 'verdict')",
        "expected": "survived",
        "expectationReason": "No selftest fixture invalidates this check."
      },
      {
        "id": "C1-17",
        "script": "measure_c1.py",
        "check": "Required claim field claim",
        "pattern": "FIELDS = (\"id\", \"anchor\", \"claim\", \"surface\", \"method\", \"observation\", \"verdict\")",
        "replacement": "FIELDS = ('id', 'anchor', 'surface', 'method', 'observation', 'verdict')",
        "expected": "survived",
        "expectationReason": "No selftest fixture invalidates this check."
      },
      {
        "id": "C1-18",
        "script": "measure_c1.py",
        "check": "Required claim field surface",
        "pattern": "FIELDS = (\"id\", \"anchor\", \"claim\", \"surface\", \"method\", \"observation\", \"verdict\")",
        "replacement": "FIELDS = ('id', 'anchor', 'claim', 'method', 'observation', 'verdict')",
        "expected": "survived",
        "expectationReason": "No selftest fixture invalidates this check."
      },
      {
        "id": "C1-19",
        "script": "measure_c1.py",
        "check": "Required claim field method",
        "pattern": "FIELDS = (\"id\", \"anchor\", \"claim\", \"surface\", \"method\", \"observation\", \"verdict\")",
        "replacement": "FIELDS = ('id', 'anchor', 'claim', 'surface', 'observation', 'verdict')",
        "expected": "survived",
        "expectationReason": "No selftest fixture invalidates this check."
      },
      {
        "id": "C1-20",
        "script": "measure_c1.py",
        "check": "Required claim field observation",
        "pattern": "FIELDS = (\"id\", \"anchor\", \"claim\", \"surface\", \"method\", \"observation\", \"verdict\")",
        "replacement": "FIELDS = ('id', 'anchor', 'claim', 'surface', 'method', 'verdict')",
        "expected": "survived",
        "expectationReason": "No selftest fixture invalidates this check."
      },
      {
        "id": "C1-21",
        "script": "measure_c1.py",
        "check": "Required claim field verdict",
        "pattern": "FIELDS = (\"id\", \"anchor\", \"claim\", \"surface\", \"method\", \"observation\", \"verdict\")",
        "replacement": "FIELDS = ('id', 'anchor', 'claim', 'surface', 'method', 'observation')",
        "expected": "survived",
        "expectationReason": "No selftest fixture invalidates this check."
      },
      {
        "id": "C1-22",
        "script": "measure_c1.py",
        "check": "Duplicate claim IDs",
        "pattern": "claim[\"id\"] in seen",
        "replacement": "False",
        "expected": "survived",
        "expectationReason": "No selftest fixture invalidates this check."
      },
      {
        "id": "C1-23",
        "script": "measure_c1.py",
        "check": "Allowed verdict membership",
        "pattern": "verdict not in VERDICTS",
        "replacement": "False",
        "expected": "survived",
        "expectationReason": "No selftest fixture invalidates this check."
      },
      {
        "id": "C1-24",
        "script": "measure_c1.py",
        "check": "Anchor belongs to base unit",
        "pattern": "claim[\"anchor\"] not in base_text",
        "replacement": "False",
        "expected": "killed",
        "expectationReason": "Invalid-anchor fixture expects one rejected unit and the anchor diagnostic."
      },
      {
        "id": "C1-25",
        "script": "measure_c1.py",
        "check": "Claim cited after heading",
        "pattern": "f\"[{unit['unit']}:{claim['id']}]\" not in section",
        "replacement": "False",
        "expected": "survived",
        "expectationReason": "No selftest fixture invalidates this check."
      },
      {
        "id": "C1-26",
        "script": "measure_c1.py",
        "check": "STALE correction dispatch",
        "pattern": "verdict == \"STALE\"",
        "replacement": "False",
        "expected": "survived",
        "expectationReason": "No selftest fixture invalidates this check."
      },
      {
        "id": "C1-27",
        "script": "measure_c1.py",
        "check": "Correction string type",
        "pattern": "not isinstance(correction, str)",
        "replacement": "False",
        "expected": "survived",
        "expectationReason": "No selftest fixture invalidates this check."
      },
      {
        "id": "C1-28",
        "script": "measure_c1.py",
        "check": "Correction nonblank",
        "pattern": "not correction.strip()",
        "replacement": "False",
        "expected": "survived",
        "expectationReason": "No selftest fixture invalidates this check."
      },
      {
        "id": "C1-29",
        "script": "measure_c1.py",
        "check": "Correction in appended section",
        "pattern": "correction not in section",
        "replacement": "False",
        "expected": "survived",
        "expectationReason": "No selftest fixture invalidates this check."
      },
      {
        "id": "C1-30",
        "script": "measure_c1.py",
        "check": "UNVERIFIABLE reason dispatch",
        "pattern": "verdict == \"UNVERIFIABLE\"",
        "replacement": "False",
        "expected": "survived",
        "expectationReason": "No selftest fixture invalidates this check."
      },
      {
        "id": "C1-31",
        "script": "measure_c1.py",
        "check": "UNVERIFIABLE reason nonblank",
        "pattern": "not str(claim.get(\"reason\", \"\")).strip()",
        "replacement": "False",
        "expected": "survived",
        "expectationReason": "No selftest fixture invalidates this check."
      },
      {
        "id": "C1-32",
        "script": "measure_c1.py",
        "check": "At least one live-decided claim",
        "pattern": "verdicts[\"HOLD\"] + verdicts[\"STALE\"] == 0",
        "replacement": "False",
        "expected": "killed",
        "expectationReason": "All-UNVERIFIABLE fixture expects one rejected unit with the live-decision diagnostic."
      },
      {
        "id": "C1-33",
        "script": "measure_c1.py",
        "check": "Frozen population guard dispatch",
        "pattern": "population_raw is not None",
        "replacement": "False",
        "expected": "survived",
        "expectationReason": "No selftest fixture invalidates this check."
      },
      {
        "id": "C1-34",
        "script": "measure_c1.py",
        "check": "Frozen population digest",
        "pattern": "hashlib.sha256(population_raw.encode(\"utf-8\")).hexdigest() != POPULATION_SHA256",
        "replacement": "False",
        "expected": "survived",
        "expectationReason": "No selftest fixture invalidates this check."
      },
      {
        "id": "C1-35",
        "script": "measure_c1.py",
        "check": "Revision resolves to a commit",
        "pattern": "resolved.returncode != 0",
        "replacement": "False",
        "expected": "survived",
        "expectationReason": "No selftest fixture invalidates this check."
      },
      {
        "id": "C1-36",
        "script": "measure_c1.py",
        "check": "Population readable",
        "pattern": "population_raw is None",
        "replacement": "False",
        "expected": "survived",
        "expectationReason": "No selftest fixture invalidates this check."
      },
      {
        "id": "C1-37",
        "script": "measure_c1.py",
        "check": "Per-unit acceptance uses problems",
        "pattern": "not problems",
        "replacement": "True",
        "expected": "killed",
        "expectationReason": "Invalid-anchor fixture must mark the targeted unit failed and decrement accepted."
      },
      {
        "id": "C1-38",
        "script": "measure_c1.py",
        "check": "Overall exit rejects any failed unit",
        "pattern": "accepted == len(units)",
        "replacement": "True",
        "expected": "killed",
        "expectationReason": "Invalid-anchor fixture expects exit 1, not 0."
      },
      {
        "id": "C1-39",
        "script": "measure_c1.py",
        "check": "Section is gated on heading presence",
        "pattern": "position >= 0",
        "replacement": "True",
        "expected": "survived",
        "expectationReason": "No selftest fixture invalidates this check."
      },
      {
        "id": "C1-40",
        "script": "measure_c1.py",
        "check": "Required field string type",
        "pattern": "not isinstance(claim.get(k), str)",
        "replacement": "False",
        "expected": "survived",
        "expectationReason": "No selftest fixture invalidates this check."
      },
      {
        "id": "C1-41",
        "script": "measure_c1.py",
        "check": "Required field nonblank",
        "pattern": "not claim[k].strip()",
        "replacement": "False",
        "expected": "survived",
        "expectationReason": "No selftest fixture invalidates this check."
      },
      {
        "id": "C2-01",
        "script": "measure_c2.py",
        "check": "Git show return code",
        "pattern": "done.returncode == 0",
        "replacement": "True",
        "expected": "survived",
        "expectationReason": "No selftest fixture invalidates this check."
      },
      {
        "id": "C2-02",
        "script": "measure_c2.py",
        "check": "Served status integer type",
        "pattern": "isinstance(status, int)",
        "replacement": "True",
        "expected": "survived",
        "expectationReason": "No selftest fixture invalidates this check."
      },
      {
        "id": "C2-03",
        "script": "measure_c2.py",
        "check": "Served status lower bound",
        "pattern": "200 <= status < 300",
        "replacement": "status < 300",
        "expected": "survived",
        "expectationReason": "No selftest fixture invalidates this check."
      },
      {
        "id": "C2-04",
        "script": "measure_c2.py",
        "check": "Served status upper bound",
        "pattern": "200 <= status < 300",
        "replacement": "200 <= status",
        "expected": "killed",
        "expectationReason": "The valid 404 non-served fixture would be misclassified as served, then lack page bytes."
      },
      {
        "id": "C2-05",
        "script": "measure_c2.py",
        "check": "Served fetch has no error",
        "pattern": "fetch.get(\"error\") is None",
        "replacement": "True",
        "expected": "survived",
        "expectationReason": "No selftest fixture invalidates this check."
      },
      {
        "id": "C2-06",
        "script": "measure_c2.py",
        "check": "Served fetch is not truncated",
        "pattern": "not fetch.get(\"truncated\")",
        "replacement": "True",
        "expected": "survived",
        "expectationReason": "No selftest fixture invalidates this check."
      },
      {
        "id": "C2-07",
        "script": "measure_c2.py",
        "check": "Served Content-Type HTML",
        "pattern": "ctype.split(\";\")[0].strip().lower() == \"text/html\"",
        "replacement": "True",
        "expected": "survived",
        "expectationReason": "No selftest fixture invalidates this check."
      },
      {
        "id": "C2-08",
        "script": "measure_c2.py",
        "check": "Fetch metadata present",
        "pattern": "raw_fetch is None",
        "replacement": "False",
        "expected": "survived",
        "expectationReason": "No selftest fixture invalidates this check."
      },
      {
        "id": "C2-09",
        "script": "measure_c2.py",
        "check": "Audit receipt present",
        "pattern": "raw_audit is None",
        "replacement": "False",
        "expected": "survived",
        "expectationReason": "No selftest fixture invalidates this check."
      },
      {
        "id": "C2-10",
        "script": "measure_c2.py",
        "check": "Receipt JSON parsing rejection",
        "pattern": "return [f\"receipt JSON invalid: {exc}\"], None",
        "replacement": "return [], None",
        "expected": "survived",
        "expectationReason": "No selftest fixture invalidates this check."
      },
      {
        "id": "C2-11",
        "script": "measure_c2.py",
        "check": "Fetch URL matches population",
        "pattern": "fetch.get(\"url\") != surface[\"url\"]",
        "replacement": "False",
        "expected": "survived",
        "expectationReason": "No selftest fixture invalidates this check."
      },
      {
        "id": "C2-12",
        "script": "measure_c2.py",
        "check": "Fetch method GET",
        "pattern": "fetch.get(\"method\") != \"GET\"",
        "replacement": "False",
        "expected": "killed",
        "expectationReason": "The non-GET fixture changes method to HEAD and expects rejection with a GET diagnostic."
      },
      {
        "id": "C2-13",
        "script": "measure_c2.py",
        "check": "fetchedAt is a string",
        "pattern": "not isinstance(fetch.get(\"fetchedAt\"), str)",
        "replacement": "False",
        "expected": "survived",
        "expectationReason": "No selftest fixture invalidates this check."
      },
      {
        "id": "C2-14",
        "script": "measure_c2.py",
        "check": "fetchedAt date cutoff",
        "pattern": "fetch[\"fetchedAt\"][:10] < \"2026-10-21\"",
        "replacement": "False",
        "expected": "survived",
        "expectationReason": "No selftest fixture invalidates this check."
      },
      {
        "id": "C2-15",
        "script": "measure_c2.py",
        "check": "Non-served branch dispatch",
        "pattern": "not served(fetch)",
        "replacement": "False",
        "expected": "killed",
        "expectationReason": "The valid 404 fixture would fall through to missing page/digest rejection."
      },
      {
        "id": "C2-16",
        "script": "measure_c2.py",
        "check": "Non-served response has no page",
        "pattern": "page is not None",
        "replacement": "False",
        "expected": "survived",
        "expectationReason": "No selftest fixture invalidates this check."
      },
      {
        "id": "C2-17",
        "script": "measure_c2.py",
        "check": "Non-served receipt verdict",
        "pattern": "receipt.get(\"verdict\") != \"not-served\"",
        "replacement": "False",
        "expected": "survived",
        "expectationReason": "No selftest fixture invalidates this check."
      },
      {
        "id": "C2-18",
        "script": "measure_c2.py",
        "check": "Non-served receipt status matches",
        "pattern": "receipt.get(\"status\") != fetch.get(\"status\")",
        "replacement": "False",
        "expected": "survived",
        "expectationReason": "No selftest fixture invalidates this check."
      },
      {
        "id": "C2-19",
        "script": "measure_c2.py",
        "check": "Served page bytes present",
        "pattern": "page is None",
        "replacement": "False",
        "expected": "survived",
        "expectationReason": "No selftest fixture invalidates this check."
      },
      {
        "id": "C2-20",
        "script": "measure_c2.py",
        "check": "Served page digest matches fetch",
        "pattern": "hashlib.sha256(page).hexdigest() != fetch.get(\"sha256\")",
        "replacement": "False",
        "expected": "survived",
        "expectationReason": "No selftest fixture invalidates this check."
      },
      {
        "id": "C2-21",
        "script": "measure_c2.py",
        "check": "Validator emits JSON rejection",
        "pattern": "return problems + [\"validator did not emit JSON\"], None",
        "replacement": "return problems, None",
        "expected": "survived",
        "expectationReason": "No selftest fixture invalidates this check."
      },
      {
        "id": "C2-22",
        "script": "measure_c2.py",
        "check": "Stored audit equals reproduced audit",
        "pattern": "receipt != actual",
        "replacement": "False",
        "expected": "killed",
        "expectationReason": "The unreproducible-audit fixture changes verdict and expects one rejected surface."
      },
      {
        "id": "C2-23",
        "script": "measure_c2.py",
        "check": "Revision resolves to a commit",
        "pattern": "resolved.returncode != 0",
        "replacement": "False",
        "expected": "survived",
        "expectationReason": "No selftest fixture invalidates this check."
      },
      {
        "id": "C2-24",
        "script": "measure_c2.py",
        "check": "Population readable",
        "pattern": "population is None",
        "replacement": "False",
        "expected": "survived",
        "expectationReason": "No selftest fixture invalidates this check."
      },
      {
        "id": "C2-25",
        "script": "measure_c2.py",
        "check": "Validator readable",
        "pattern": "validator is None",
        "replacement": "False",
        "expected": "survived",
        "expectationReason": "No selftest fixture invalidates this check."
      },
      {
        "id": "C2-26",
        "script": "measure_c2.py",
        "check": "Frozen population digest",
        "pattern": "hashlib.sha256(population).hexdigest() != POPULATION_SHA256",
        "replacement": "False",
        "expected": "survived",
        "expectationReason": "No selftest fixture invalidates this check."
      },
      {
        "id": "C2-27",
        "script": "measure_c2.py",
        "check": "Per-surface acceptance uses problems",
        "pattern": "not problems",
        "replacement": "True",
        "expected": "killed",
        "expectationReason": "The unreproducible-audit fixture must mark the targeted surface failed and decrement accepted."
      },
      {
        "id": "C2-28",
        "script": "measure_c2.py",
        "check": "Overall exit rejects any failed surface",
        "pattern": "accepted == len(rows)",
        "replacement": "True",
        "expected": "killed",
        "expectationReason": "The unreproducible-audit fixture expects exit 1, not 0."
      },
      {
        "id": "C2-29",
        "script": "measure_c2.py",
        "check": "Stored audit exit equals reproduced exit",
        "pattern": "receipt != actual",
        "replacement": "receipt.get(\"result\") != actual.get(\"result\")",
        "expected": "survived",
        "expectationReason": "No selftest fixture invalidates this check."
      },
      {
        "id": "C2-30",
        "script": "measure_c2.py",
        "check": "Stored audit result equals reproduced result",
        "pattern": "receipt != actual",
        "replacement": "receipt.get(\"exit\") != actual.get(\"exit\")",
        "expected": "killed",
        "expectationReason": "The unreproducible-audit fixture changes result verdict only; ignoring results accepts it."
      }
    ]
  },
  "pristine": {
    "exit": 0,
    "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-x6mvp_v_/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-x6mvp_v_/repo\", \"--revision\", \"2a8432e95c3cc8d8a178ca9d23cafd123618a872\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-x6mvp_v_/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-x6mvp_v_/repo\", \"--revision\", \"2a8432e95c3cc8d8a178ca9d23cafd123618a872\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-x6mvp_v_/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-x6mvp_v_/repo\", \"--revision\", \"e68930d532846646f09db28285816df60682434e\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-x6mvp_v_/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-x6mvp_v_/repo\", \"--revision\", \"21c56cd2bdcef7112fa27b3aadf60b13ac489228\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-x6mvp_v_/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-x6mvp_v_/repo\", \"--revision\", \"60a00e5054fbdc028c5d2a8a1d87856af6b434bd\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-x6mvp_v_/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-x6mvp_v_/repo\", \"--revision\", \"5a1eb5277f82f592e1a91622aef007a17e28a1e5\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-x6mvp_v_/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-x6mvp_v_/repo\", \"--revision\", \"49b9b20a0304b3c19ea95c1b0fd33561c093faf3\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
    "stderr": "",
    "elapsedSeconds": 2.146
  },
  "runs": [
    {
      "id": "C1-01",
      "script": "measure_c1.py",
      "check": "Git show return code",
      "pattern": "done.returncode == 0",
      "replacement": "True",
      "expected": "survived",
      "expectationReason": "No selftest fixture invalidates this check.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-x6mvp_v_/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-x6mvp_v_/repo\", \"--revision\", \"2a8432e95c3cc8d8a178ca9d23cafd123618a872\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-x6mvp_v_/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-x6mvp_v_/repo\", \"--revision\", \"2a8432e95c3cc8d8a178ca9d23cafd123618a872\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-x6mvp_v_/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-x6mvp_v_/repo\", \"--revision\", \"e68930d532846646f09db28285816df60682434e\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-x6mvp_v_/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-x6mvp_v_/repo\", \"--revision\", \"21c56cd2bdcef7112fa27b3aadf60b13ac489228\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-x6mvp_v_/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-x6mvp_v_/repo\", \"--revision\", \"60a00e5054fbdc028c5d2a8a1d87856af6b434bd\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-x6mvp_v_/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-x6mvp_v_/repo\", \"--revision\", \"5a1eb5277f82f592e1a91622aef007a17e28a1e5\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-x6mvp_v_/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-x6mvp_v_/repo\", \"--revision\", \"49b9b20a0304b3c19ea95c1b0fd33561c093faf3\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.146
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "5e5afb9e4d8ee18831b9b35b35e8a34e47aceecd",
      "mutatedSha256": {
        "measure_c1.py": "6af416858f5584ba95aa3e9e924f9a7b9bfec118c585877e41de200a876f7d7f",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "d654ae5def77b111a320a98ef7c9d2a69ed881d3",
      "committedMutationSha256": "6af416858f5584ba95aa3e9e924f9a7b9bfec118c585877e41de200a876f7d7f",
      "mutated": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-exoj2ci6/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-exoj2ci6/repo\", \"--revision\", \"7a54eaa1f7c47599cb217a7df7ff334b855f873c\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-exoj2ci6/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-exoj2ci6/repo\", \"--revision\", \"7a54eaa1f7c47599cb217a7df7ff334b855f873c\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-exoj2ci6/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-exoj2ci6/repo\", \"--revision\", \"87c8aca0f5c4fea1eafbf2eb9a294874ae4d1136\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-exoj2ci6/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-exoj2ci6/repo\", \"--revision\", \"221b8fe81cdae79392bad2126e5be5ba0cb57de2\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-exoj2ci6/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-exoj2ci6/repo\", \"--revision\", \"0fc7a059b60df3391ccb01bebc41164f7e9e9445\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-exoj2ci6/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-exoj2ci6/repo\", \"--revision\", \"d41b1bdbbc47a135f48236f87026ee3eae821e64\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-exoj2ci6/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-exoj2ci6/repo\", \"--revision\", \"8dbbc5322bb197bad511cbcdcfd1b8533698d368\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.048
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "e8ecf353b29da7bbb623c62ab91f8cbcb5a3fcf3",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-h2fmd6mo/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-h2fmd6mo/repo\", \"--revision\", \"ef6c7b7debaac48b3c172b5a0d313f22e3acfa67\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-h2fmd6mo/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-h2fmd6mo/repo\", \"--revision\", \"ef6c7b7debaac48b3c172b5a0d313f22e3acfa67\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-h2fmd6mo/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-h2fmd6mo/repo\", \"--revision\", \"9c02a108608e5fea7ab2a15275e41f9919b9ccf2\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-h2fmd6mo/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-h2fmd6mo/repo\", \"--revision\", \"e9f1588fb9f081e580ac13cf1a8da781b5b59d65\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-h2fmd6mo/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-h2fmd6mo/repo\", \"--revision\", \"4deee02be71ccaa47a6365aaf3c3ff98d8a019c8\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-h2fmd6mo/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-h2fmd6mo/repo\", \"--revision\", \"06bebe6e67e7c1f263f7da002adb097d892b9c58\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-h2fmd6mo/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-h2fmd6mo/repo\", \"--revision\", \"e4e2f6a27720ace40b7ec2a3a0c006c0944326a4\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.021
      },
      "verdict": "survived"
    },
    {
      "id": "C1-02",
      "script": "measure_c1.py",
      "check": "Missing receipt rejection",
      "pattern": "return [\"receipt missing\"], verdicts",
      "replacement": "return [], verdicts",
      "expected": "survived",
      "expectationReason": "No selftest fixture invalidates this check.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-h2fmd6mo/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-h2fmd6mo/repo\", \"--revision\", \"ef6c7b7debaac48b3c172b5a0d313f22e3acfa67\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-h2fmd6mo/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-h2fmd6mo/repo\", \"--revision\", \"ef6c7b7debaac48b3c172b5a0d313f22e3acfa67\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-h2fmd6mo/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-h2fmd6mo/repo\", \"--revision\", \"9c02a108608e5fea7ab2a15275e41f9919b9ccf2\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-h2fmd6mo/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-h2fmd6mo/repo\", \"--revision\", \"e9f1588fb9f081e580ac13cf1a8da781b5b59d65\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-h2fmd6mo/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-h2fmd6mo/repo\", \"--revision\", \"4deee02be71ccaa47a6365aaf3c3ff98d8a019c8\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-h2fmd6mo/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-h2fmd6mo/repo\", \"--revision\", \"06bebe6e67e7c1f263f7da002adb097d892b9c58\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-h2fmd6mo/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-h2fmd6mo/repo\", \"--revision\", \"e4e2f6a27720ace40b7ec2a3a0c006c0944326a4\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.021
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "e8ecf353b29da7bbb623c62ab91f8cbcb5a3fcf3",
      "mutatedSha256": {
        "measure_c1.py": "7c49761665d34746311b599fc0449120ee5a2137fe1323ae91b279b9e15ad2cd",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "d0a32eb101025f6af56052afd5d42861f672dc3d",
      "committedMutationSha256": "7c49761665d34746311b599fc0449120ee5a2137fe1323ae91b279b9e15ad2cd",
      "mutated": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-vf73x20m/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-vf73x20m/repo\", \"--revision\", \"91ab2de8aedc1c7dbc4aecd725a133b23da12dfa\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-vf73x20m/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-vf73x20m/repo\", \"--revision\", \"91ab2de8aedc1c7dbc4aecd725a133b23da12dfa\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-vf73x20m/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-vf73x20m/repo\", \"--revision\", \"2d8d777d89bd1cbebc7f94720c0df98f43baf1d9\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-vf73x20m/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-vf73x20m/repo\", \"--revision\", \"03e59d1136e7928f5e01c672620380d7705535af\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-vf73x20m/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-vf73x20m/repo\", \"--revision\", \"410cb931bf168514c8582a48ee969627c89a0a5e\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-vf73x20m/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-vf73x20m/repo\", \"--revision\", \"0971586d09bd69880d1cb2fd266b1fe76a8750b0\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-vf73x20m/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-vf73x20m/repo\", \"--revision\", \"5f94ad8a70d0f448dca705f5b3f17831f05f9cd8\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.062
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "8ac0f705350d894adfc589f70d0a12b85603ab36",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-jmb6oc_g/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-jmb6oc_g/repo\", \"--revision\", \"6d9ece44785176592a00d773aeab3349bee7a5f9\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-jmb6oc_g/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-jmb6oc_g/repo\", \"--revision\", \"6d9ece44785176592a00d773aeab3349bee7a5f9\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-jmb6oc_g/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-jmb6oc_g/repo\", \"--revision\", \"12d457d64b983bc09f9c6f0eae0bb7b286a2d323\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-jmb6oc_g/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-jmb6oc_g/repo\", \"--revision\", \"e48c5b85ec39dbdf9d7a0900c6c3205707b12f8a\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-jmb6oc_g/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-jmb6oc_g/repo\", \"--revision\", \"85e750a01eac8ab35f6023fcbadd38c02584e8c3\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-jmb6oc_g/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-jmb6oc_g/repo\", \"--revision\", \"5ac06e4e50926d9f0330495f6a641f297a6c1dc3\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-jmb6oc_g/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-jmb6oc_g/repo\", \"--revision\", \"36e722b4c33497b81d691e3bae17588fb94e9f9f\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.136
      },
      "verdict": "survived"
    },
    {
      "id": "C1-03",
      "script": "measure_c1.py",
      "check": "Invalid receipt JSON rejection",
      "pattern": "return [f\"receipt is not JSON: {exc}\"], verdicts",
      "replacement": "return [], verdicts",
      "expected": "survived",
      "expectationReason": "No selftest fixture invalidates this check.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-jmb6oc_g/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-jmb6oc_g/repo\", \"--revision\", \"6d9ece44785176592a00d773aeab3349bee7a5f9\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-jmb6oc_g/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-jmb6oc_g/repo\", \"--revision\", \"6d9ece44785176592a00d773aeab3349bee7a5f9\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-jmb6oc_g/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-jmb6oc_g/repo\", \"--revision\", \"12d457d64b983bc09f9c6f0eae0bb7b286a2d323\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-jmb6oc_g/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-jmb6oc_g/repo\", \"--revision\", \"e48c5b85ec39dbdf9d7a0900c6c3205707b12f8a\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-jmb6oc_g/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-jmb6oc_g/repo\", \"--revision\", \"85e750a01eac8ab35f6023fcbadd38c02584e8c3\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-jmb6oc_g/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-jmb6oc_g/repo\", \"--revision\", \"5ac06e4e50926d9f0330495f6a641f297a6c1dc3\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-jmb6oc_g/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-jmb6oc_g/repo\", \"--revision\", \"36e722b4c33497b81d691e3bae17588fb94e9f9f\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.136
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "8ac0f705350d894adfc589f70d0a12b85603ab36",
      "mutatedSha256": {
        "measure_c1.py": "31cdb0fce41bb064a44949b5a692fd2d97141636099e9b5dcb0bef5a99444436",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "e985ea682a597334d3ce38f5f8cb80466b7a4e4d",
      "committedMutationSha256": "31cdb0fce41bb064a44949b5a692fd2d97141636099e9b5dcb0bef5a99444436",
      "mutated": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-18g5ly6j/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-18g5ly6j/repo\", \"--revision\", \"4d0f6d60aa771dd7f6f64a5711fcea40e9361076\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-18g5ly6j/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-18g5ly6j/repo\", \"--revision\", \"4d0f6d60aa771dd7f6f64a5711fcea40e9361076\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-18g5ly6j/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-18g5ly6j/repo\", \"--revision\", \"ccc70f36058482ce624f8e0a0546387e947dc3ca\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-18g5ly6j/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-18g5ly6j/repo\", \"--revision\", \"c08cce10c065cc4466e3e32fb6d4a403302f180e\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-18g5ly6j/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-18g5ly6j/repo\", \"--revision\", \"509f82b1163a71d94d38cb40e63b1488ab0f27b0\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-18g5ly6j/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-18g5ly6j/repo\", \"--revision\", \"9c60a3bea2a20272a19dca48e042fc10cc146b90\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-18g5ly6j/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-18g5ly6j/repo\", \"--revision\", \"462b7129ac976bc2bce7c70b9da0677e61ad67b8\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.156
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "bad6c9347ea7fe6009071ea3e0b2c43bfede6346",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-50iajvrd/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-50iajvrd/repo\", \"--revision\", \"c16e9a0ca13a83797278d5e496c4da9092ede907\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-50iajvrd/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-50iajvrd/repo\", \"--revision\", \"c16e9a0ca13a83797278d5e496c4da9092ede907\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-50iajvrd/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-50iajvrd/repo\", \"--revision\", \"443945f1eb3330191f50357076931cb37a552163\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-50iajvrd/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-50iajvrd/repo\", \"--revision\", \"7c69d896ee43eb7169546564053a08b1e567e2d3\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-50iajvrd/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-50iajvrd/repo\", \"--revision\", \"d924b1c22daeb12a0a5496e3290799a1e465a351\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-50iajvrd/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-50iajvrd/repo\", \"--revision\", \"c14e8d2766432ddfe4ea896c35dc17baf52ad82a\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-50iajvrd/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-50iajvrd/repo\", \"--revision\", \"e544ec999d2ecbc63dc32e32ee8dfbafcb40a7bd\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.143
      },
      "verdict": "survived"
    },
    {
      "id": "C1-04",
      "script": "measure_c1.py",
      "check": "Receipt object rejection",
      "pattern": "return [\"receipt is not an object\"], verdicts",
      "replacement": "return [], verdicts",
      "expected": "survived",
      "expectationReason": "No selftest fixture invalidates this check.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-50iajvrd/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-50iajvrd/repo\", \"--revision\", \"c16e9a0ca13a83797278d5e496c4da9092ede907\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-50iajvrd/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-50iajvrd/repo\", \"--revision\", \"c16e9a0ca13a83797278d5e496c4da9092ede907\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-50iajvrd/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-50iajvrd/repo\", \"--revision\", \"443945f1eb3330191f50357076931cb37a552163\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-50iajvrd/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-50iajvrd/repo\", \"--revision\", \"7c69d896ee43eb7169546564053a08b1e567e2d3\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-50iajvrd/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-50iajvrd/repo\", \"--revision\", \"d924b1c22daeb12a0a5496e3290799a1e465a351\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-50iajvrd/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-50iajvrd/repo\", \"--revision\", \"c14e8d2766432ddfe4ea896c35dc17baf52ad82a\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-50iajvrd/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-50iajvrd/repo\", \"--revision\", \"e544ec999d2ecbc63dc32e32ee8dfbafcb40a7bd\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.143
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "bad6c9347ea7fe6009071ea3e0b2c43bfede6346",
      "mutatedSha256": {
        "measure_c1.py": "b5dd527ec2a4d7b1801b4a943a7333873d73e58d84d2d53ada23fb1271249488",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "11fd3839286b16828129274b6f5a33d2305310f6",
      "committedMutationSha256": "b5dd527ec2a4d7b1801b4a943a7333873d73e58d84d2d53ada23fb1271249488",
      "mutated": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-li_tu1ox/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-li_tu1ox/repo\", \"--revision\", \"b07d3fd5125c77d30782443696cd99afaac24cc8\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-li_tu1ox/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-li_tu1ox/repo\", \"--revision\", \"b07d3fd5125c77d30782443696cd99afaac24cc8\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-li_tu1ox/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-li_tu1ox/repo\", \"--revision\", \"bf9c67bff8564c5533895c16bf96e01bb02eec62\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-li_tu1ox/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-li_tu1ox/repo\", \"--revision\", \"343c76938a9b3cd9f2ab6bc8d4929e0b257d81ac\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-li_tu1ox/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-li_tu1ox/repo\", \"--revision\", \"ff50bd165aaf4730ae3e940ff698dd30bcab3de9\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-li_tu1ox/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-li_tu1ox/repo\", \"--revision\", \"eea2cc9cf03528b825671c9d5b6fbd4ee7a9c898\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-li_tu1ox/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-li_tu1ox/repo\", \"--revision\", \"4a0c7f16fdf90852267045fddfe680fe2c95e920\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.126
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "d883c1d73eb6bbeb0e157d087292bd9c193a7a9d",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-2sqjjuak/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-2sqjjuak/repo\", \"--revision\", \"934e9fe6c68f98ca02ee9dcaf7fecf8aaf49a907\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-2sqjjuak/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-2sqjjuak/repo\", \"--revision\", \"934e9fe6c68f98ca02ee9dcaf7fecf8aaf49a907\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-2sqjjuak/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-2sqjjuak/repo\", \"--revision\", \"f57a643b5b9b7faf2e165b6ee428637f739414b6\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-2sqjjuak/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-2sqjjuak/repo\", \"--revision\", \"9a1918fe5036e3d94b79a3f1bad771abf39521ca\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-2sqjjuak/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-2sqjjuak/repo\", \"--revision\", \"32834f392ddde0c18f688b56c2b88f2c33eecb6a\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-2sqjjuak/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-2sqjjuak/repo\", \"--revision\", \"301d5e051cc4d2cb9ddd80832aa35bb78727591c\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-2sqjjuak/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-2sqjjuak/repo\", \"--revision\", \"fecd956e801842dd9b9e156273fed400a671bd87\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.07
      },
      "verdict": "survived"
    },
    {
      "id": "C1-05",
      "script": "measure_c1.py",
      "check": "Receipt unit matches population",
      "pattern": "receipt.get(\"unit\") != unit[\"unit\"]",
      "replacement": "False",
      "expected": "survived",
      "expectationReason": "No selftest fixture invalidates this check.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-2sqjjuak/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-2sqjjuak/repo\", \"--revision\", \"934e9fe6c68f98ca02ee9dcaf7fecf8aaf49a907\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-2sqjjuak/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-2sqjjuak/repo\", \"--revision\", \"934e9fe6c68f98ca02ee9dcaf7fecf8aaf49a907\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-2sqjjuak/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-2sqjjuak/repo\", \"--revision\", \"f57a643b5b9b7faf2e165b6ee428637f739414b6\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-2sqjjuak/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-2sqjjuak/repo\", \"--revision\", \"9a1918fe5036e3d94b79a3f1bad771abf39521ca\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-2sqjjuak/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-2sqjjuak/repo\", \"--revision\", \"32834f392ddde0c18f688b56c2b88f2c33eecb6a\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-2sqjjuak/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-2sqjjuak/repo\", \"--revision\", \"301d5e051cc4d2cb9ddd80832aa35bb78727591c\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-2sqjjuak/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-2sqjjuak/repo\", \"--revision\", \"fecd956e801842dd9b9e156273fed400a671bd87\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.07
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "d883c1d73eb6bbeb0e157d087292bd9c193a7a9d",
      "mutatedSha256": {
        "measure_c1.py": "2b55608cf1628abbe20a1bf7302900150dbe0ad290bf3a826e48b023ddefbbdb",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "3b3a0b682cc07857f1772662622766b05174fa15",
      "committedMutationSha256": "2b55608cf1628abbe20a1bf7302900150dbe0ad290bf3a826e48b023ddefbbdb",
      "mutated": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-1agb1o5n/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-1agb1o5n/repo\", \"--revision\", \"6e8aae9be06a29ddb1b7541e0ade91d749a4e0ab\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-1agb1o5n/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-1agb1o5n/repo\", \"--revision\", \"6e8aae9be06a29ddb1b7541e0ade91d749a4e0ab\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-1agb1o5n/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-1agb1o5n/repo\", \"--revision\", \"f9e21923dc9fa100cc5dc58dea6681c2315c4237\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-1agb1o5n/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-1agb1o5n/repo\", \"--revision\", \"0d97c10c71ae8f2f7d90a54a1442d6e7fed4e1b7\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-1agb1o5n/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-1agb1o5n/repo\", \"--revision\", \"7fdabf5c03e7e791ba7220cc31b9cd840a30fb58\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-1agb1o5n/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-1agb1o5n/repo\", \"--revision\", \"03a17b38baaac509abdbbf44d5198dcc96cd8c53\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-1agb1o5n/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-1agb1o5n/repo\", \"--revision\", \"938b6bbb903146dabbfe4170dafcb773508e01aa\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.074
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "24c05385dfb3fc1074c7cbc48e29147013e3524e",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-rxbfep0r/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-rxbfep0r/repo\", \"--revision\", \"5f833c54d09d1622bed62f4f66998333ec97611f\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-rxbfep0r/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-rxbfep0r/repo\", \"--revision\", \"5f833c54d09d1622bed62f4f66998333ec97611f\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-rxbfep0r/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-rxbfep0r/repo\", \"--revision\", \"7f4f00a64ac5877d000b8d0abb0474e3afae2eee\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-rxbfep0r/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-rxbfep0r/repo\", \"--revision\", \"1dd7615244bfad8cddb5ec910e9382c4bc4ed0e1\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-rxbfep0r/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-rxbfep0r/repo\", \"--revision\", \"42bd28ae8bca26b60c0313b1d67f1d4752356a8b\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-rxbfep0r/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-rxbfep0r/repo\", \"--revision\", \"818977be1a335306a004adaa48129a958ac23a25\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-rxbfep0r/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-rxbfep0r/repo\", \"--revision\", \"9e59a3c288a4eb0183eee763b49c401cc85076a4\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.039
      },
      "verdict": "survived"
    },
    {
      "id": "C1-06",
      "script": "measure_c1.py",
      "check": "Receipt path matches population",
      "pattern": "receipt.get(\"path\") != unit[\"path\"]",
      "replacement": "False",
      "expected": "survived",
      "expectationReason": "No selftest fixture invalidates this check.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-rxbfep0r/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-rxbfep0r/repo\", \"--revision\", \"5f833c54d09d1622bed62f4f66998333ec97611f\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-rxbfep0r/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-rxbfep0r/repo\", \"--revision\", \"5f833c54d09d1622bed62f4f66998333ec97611f\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-rxbfep0r/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-rxbfep0r/repo\", \"--revision\", \"7f4f00a64ac5877d000b8d0abb0474e3afae2eee\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-rxbfep0r/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-rxbfep0r/repo\", \"--revision\", \"1dd7615244bfad8cddb5ec910e9382c4bc4ed0e1\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-rxbfep0r/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-rxbfep0r/repo\", \"--revision\", \"42bd28ae8bca26b60c0313b1d67f1d4752356a8b\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-rxbfep0r/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-rxbfep0r/repo\", \"--revision\", \"818977be1a335306a004adaa48129a958ac23a25\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-rxbfep0r/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-rxbfep0r/repo\", \"--revision\", \"9e59a3c288a4eb0183eee763b49c401cc85076a4\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.039
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "24c05385dfb3fc1074c7cbc48e29147013e3524e",
      "mutatedSha256": {
        "measure_c1.py": "dcb8a6c9e711cd35eaa5aa9b66045b3e817fef9dda0d8c859e3d4c10a622b601",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "e38d8b0477eaaeae7aa81793fb6e9e851baf76f4",
      "committedMutationSha256": "dcb8a6c9e711cd35eaa5aa9b66045b3e817fef9dda0d8c859e3d4c10a622b601",
      "mutated": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-q4a6maa0/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-q4a6maa0/repo\", \"--revision\", \"e29c504afdc24200adfda486b80cc936e6e9463b\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-q4a6maa0/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-q4a6maa0/repo\", \"--revision\", \"e29c504afdc24200adfda486b80cc936e6e9463b\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-q4a6maa0/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-q4a6maa0/repo\", \"--revision\", \"d25b56c7af817e4af06a03e7ed5337640aed541e\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-q4a6maa0/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-q4a6maa0/repo\", \"--revision\", \"3e77c1c7456038755ccd8d4e2ce9e4858cb7d4d0\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-q4a6maa0/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-q4a6maa0/repo\", \"--revision\", \"b5351ca7e04810f69e3e83bb43b89b8a630849c1\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-q4a6maa0/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-q4a6maa0/repo\", \"--revision\", \"63c69ff80dee5ee4bd03bbc1f4b3233532fe8e85\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-q4a6maa0/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-q4a6maa0/repo\", \"--revision\", \"f1704226e5501a5050710e1771fa2c9f5153d89e\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.075
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "6d97a95bed6c8f6bf703aff17b129fb9d38864b7",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-2y9jjgjh/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-2y9jjgjh/repo\", \"--revision\", \"8bd77bef313f325d9a6db45c16f0167e0eb7573f\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-2y9jjgjh/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-2y9jjgjh/repo\", \"--revision\", \"8bd77bef313f325d9a6db45c16f0167e0eb7573f\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-2y9jjgjh/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-2y9jjgjh/repo\", \"--revision\", \"356694a70cbfd48f5fd4d1b1955f8dc6deef776e\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-2y9jjgjh/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-2y9jjgjh/repo\", \"--revision\", \"7e31d5269d07714bcb2c593c073a5f5ea2124e97\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-2y9jjgjh/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-2y9jjgjh/repo\", \"--revision\", \"8d7d8f4101692ba59832bc56436a12a807fdc894\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-2y9jjgjh/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-2y9jjgjh/repo\", \"--revision\", \"a55368e78e0dbaa87f903a34916da8a0d8166e6a\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-2y9jjgjh/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-2y9jjgjh/repo\", \"--revision\", \"eafb58732e5363ca94a1a8a56e324e638fb547c7\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.116
      },
      "verdict": "survived"
    },
    {
      "id": "C1-07",
      "script": "measure_c1.py",
      "check": "observedAt is a string",
      "pattern": "not isinstance(receipt.get(\"observedAt\"), str)",
      "replacement": "False",
      "expected": "survived",
      "expectationReason": "No selftest fixture invalidates this check.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-2y9jjgjh/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-2y9jjgjh/repo\", \"--revision\", \"8bd77bef313f325d9a6db45c16f0167e0eb7573f\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-2y9jjgjh/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-2y9jjgjh/repo\", \"--revision\", \"8bd77bef313f325d9a6db45c16f0167e0eb7573f\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-2y9jjgjh/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-2y9jjgjh/repo\", \"--revision\", \"356694a70cbfd48f5fd4d1b1955f8dc6deef776e\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-2y9jjgjh/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-2y9jjgjh/repo\", \"--revision\", \"7e31d5269d07714bcb2c593c073a5f5ea2124e97\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-2y9jjgjh/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-2y9jjgjh/repo\", \"--revision\", \"8d7d8f4101692ba59832bc56436a12a807fdc894\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-2y9jjgjh/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-2y9jjgjh/repo\", \"--revision\", \"a55368e78e0dbaa87f903a34916da8a0d8166e6a\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-2y9jjgjh/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-2y9jjgjh/repo\", \"--revision\", \"eafb58732e5363ca94a1a8a56e324e638fb547c7\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.116
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "6d97a95bed6c8f6bf703aff17b129fb9d38864b7",
      "mutatedSha256": {
        "measure_c1.py": "40f377ea41c946e03b5be9a281939755076b4daa9c8b0e633dff11705f014c8e",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "156ee0c79e36104b94ed22141d7f5dc8c80fc113",
      "committedMutationSha256": "40f377ea41c946e03b5be9a281939755076b4daa9c8b0e633dff11705f014c8e",
      "mutated": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-91yxj1vq/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-91yxj1vq/repo\", \"--revision\", \"6dac90e82d5408c70614e20a5bf684fdbf93ef4f\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-91yxj1vq/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-91yxj1vq/repo\", \"--revision\", \"6dac90e82d5408c70614e20a5bf684fdbf93ef4f\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-91yxj1vq/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-91yxj1vq/repo\", \"--revision\", \"f5e79975093014f3db8617d624ffb3838d969092\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-91yxj1vq/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-91yxj1vq/repo\", \"--revision\", \"92bdd4be3d3cb89b89b24e8ee745eba86f2c1925\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-91yxj1vq/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-91yxj1vq/repo\", \"--revision\", \"05b3015601aff21a3ca1ca780f475dbe74a308e3\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-91yxj1vq/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-91yxj1vq/repo\", \"--revision\", \"1ba9c672158b79b99100fae67acc23f47b81f95e\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-91yxj1vq/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-91yxj1vq/repo\", \"--revision\", \"70052960903924350ec039df0480c63fd4642a18\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.096
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "9db8f0c0b67b22dc8e77afda86740baf536e89f3",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-dm2ux6ne/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-dm2ux6ne/repo\", \"--revision\", \"4e632d45f5baf1f9d8c0be616c4142c351ea22c7\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-dm2ux6ne/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-dm2ux6ne/repo\", \"--revision\", \"4e632d45f5baf1f9d8c0be616c4142c351ea22c7\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-dm2ux6ne/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-dm2ux6ne/repo\", \"--revision\", \"dd99c31a36617fa7f67a9c39d2c7cef2b13b5a88\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-dm2ux6ne/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-dm2ux6ne/repo\", \"--revision\", \"bd19590ded86dc825bff5da63243bf20f915922b\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-dm2ux6ne/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-dm2ux6ne/repo\", \"--revision\", \"7a41f3619e494726df5c27835e53d7cb8f7ea47b\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-dm2ux6ne/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-dm2ux6ne/repo\", \"--revision\", \"a1b44421539c7a32fdaed599787a5c1957359686\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-dm2ux6ne/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-dm2ux6ne/repo\", \"--revision\", \"f461bb4478bf2b92dea2a5928b5bcb56a3fa3d70\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.061
      },
      "verdict": "survived"
    },
    {
      "id": "C1-08",
      "script": "measure_c1.py",
      "check": "observedAt date cutoff",
      "pattern": "receipt[\"observedAt\"][:10] < \"2026-10-21\"",
      "replacement": "False",
      "expected": "survived",
      "expectationReason": "No selftest fixture invalidates this check.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-dm2ux6ne/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-dm2ux6ne/repo\", \"--revision\", \"4e632d45f5baf1f9d8c0be616c4142c351ea22c7\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-dm2ux6ne/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-dm2ux6ne/repo\", \"--revision\", \"4e632d45f5baf1f9d8c0be616c4142c351ea22c7\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-dm2ux6ne/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-dm2ux6ne/repo\", \"--revision\", \"dd99c31a36617fa7f67a9c39d2c7cef2b13b5a88\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-dm2ux6ne/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-dm2ux6ne/repo\", \"--revision\", \"bd19590ded86dc825bff5da63243bf20f915922b\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-dm2ux6ne/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-dm2ux6ne/repo\", \"--revision\", \"7a41f3619e494726df5c27835e53d7cb8f7ea47b\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-dm2ux6ne/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-dm2ux6ne/repo\", \"--revision\", \"a1b44421539c7a32fdaed599787a5c1957359686\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-dm2ux6ne/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-dm2ux6ne/repo\", \"--revision\", \"f461bb4478bf2b92dea2a5928b5bcb56a3fa3d70\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.061
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "9db8f0c0b67b22dc8e77afda86740baf536e89f3",
      "mutatedSha256": {
        "measure_c1.py": "451c0b5a69d52bc362bb91e52de66b4dec2f5a2900d384b3ef5526b21a9115ee",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "b89f54683895f5737d14e888c450e1542cde341f",
      "committedMutationSha256": "451c0b5a69d52bc362bb91e52de66b4dec2f5a2900d384b3ef5526b21a9115ee",
      "mutated": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-id4e9k_d/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-id4e9k_d/repo\", \"--revision\", \"87c9bd41c544537877a1d70c3c3a05f6d7f8c2b2\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-id4e9k_d/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-id4e9k_d/repo\", \"--revision\", \"87c9bd41c544537877a1d70c3c3a05f6d7f8c2b2\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-id4e9k_d/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-id4e9k_d/repo\", \"--revision\", \"314170ff978584a98a0ea87531e53b51f72581ef\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-id4e9k_d/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-id4e9k_d/repo\", \"--revision\", \"0221b1c4bf7ce31c71bf7aada7fd90d5f24aeaed\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-id4e9k_d/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-id4e9k_d/repo\", \"--revision\", \"974994c1c4373fd3527499794e4f1da56c18df2d\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-id4e9k_d/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-id4e9k_d/repo\", \"--revision\", \"d3eaafef5113de7e8f3eb2a1ea363e9973ca4726\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-id4e9k_d/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-id4e9k_d/repo\", \"--revision\", \"5c2c76265f4381912e4a52e8097be4b3aeec0248\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.084
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "027647291fc44b169a31cf3137ed97ca80447e9d",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-yj1f6m14/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-yj1f6m14/repo\", \"--revision\", \"9744d09e3968d1f9a9162010f82e08c5b215495f\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-yj1f6m14/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-yj1f6m14/repo\", \"--revision\", \"9744d09e3968d1f9a9162010f82e08c5b215495f\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-yj1f6m14/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-yj1f6m14/repo\", \"--revision\", \"0f10f6512fd92ca57ce83bce3689cf78d94aad4e\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-yj1f6m14/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-yj1f6m14/repo\", \"--revision\", \"db6b50e3ac108797e74ae12e1aaecfaf9d80a61c\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-yj1f6m14/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-yj1f6m14/repo\", \"--revision\", \"aecccdab871d1cf414aecfe56cbbc5951ea857fa\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-yj1f6m14/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-yj1f6m14/repo\", \"--revision\", \"a4683b9248265be7101e2b0e4ac69871c863779b\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-yj1f6m14/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-yj1f6m14/repo\", \"--revision\", \"103e9dfb7a2c5afe2544402021967819d56a9fca\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.092
      },
      "verdict": "survived"
    },
    {
      "id": "C1-09",
      "script": "measure_c1.py",
      "check": "Claims array type",
      "pattern": "not isinstance(claims, list)",
      "replacement": "False",
      "expected": "survived",
      "expectationReason": "No selftest fixture invalidates this check.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-yj1f6m14/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-yj1f6m14/repo\", \"--revision\", \"9744d09e3968d1f9a9162010f82e08c5b215495f\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-yj1f6m14/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-yj1f6m14/repo\", \"--revision\", \"9744d09e3968d1f9a9162010f82e08c5b215495f\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-yj1f6m14/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-yj1f6m14/repo\", \"--revision\", \"0f10f6512fd92ca57ce83bce3689cf78d94aad4e\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-yj1f6m14/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-yj1f6m14/repo\", \"--revision\", \"db6b50e3ac108797e74ae12e1aaecfaf9d80a61c\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-yj1f6m14/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-yj1f6m14/repo\", \"--revision\", \"aecccdab871d1cf414aecfe56cbbc5951ea857fa\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-yj1f6m14/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-yj1f6m14/repo\", \"--revision\", \"a4683b9248265be7101e2b0e4ac69871c863779b\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-yj1f6m14/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-yj1f6m14/repo\", \"--revision\", \"103e9dfb7a2c5afe2544402021967819d56a9fca\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.092
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "027647291fc44b169a31cf3137ed97ca80447e9d",
      "mutatedSha256": {
        "measure_c1.py": "71637c4534b1f4b577220b93c5910f8cc00834bebc110352309c106c89c21753",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "4a77100d714a3eb87056276573f48cb02d2274f1",
      "committedMutationSha256": "71637c4534b1f4b577220b93c5910f8cc00834bebc110352309c106c89c21753",
      "mutated": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-th5q5fjh/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-th5q5fjh/repo\", \"--revision\", \"7950a8aba4398a7687c28ad360b3009032b5dfc6\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-th5q5fjh/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-th5q5fjh/repo\", \"--revision\", \"7950a8aba4398a7687c28ad360b3009032b5dfc6\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-th5q5fjh/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-th5q5fjh/repo\", \"--revision\", \"e885cae8a7e8d92d2ccd25c49abdb5e260d751e5\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-th5q5fjh/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-th5q5fjh/repo\", \"--revision\", \"53d69f9a883d86e54931c8d777f1c5d25de2f498\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-th5q5fjh/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-th5q5fjh/repo\", \"--revision\", \"4bcd80dfc728241634e1200fe672019276bcd307\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-th5q5fjh/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-th5q5fjh/repo\", \"--revision\", \"482b7a12b50389947599f45da454f918adc6d62f\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-th5q5fjh/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-th5q5fjh/repo\", \"--revision\", \"138c69995b81306942a2cf06eab394b954b7fac5\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.087
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "35fee7dcefcb40811842d1bb78a6e0c23654c7f3",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-6z1f5xx7/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-6z1f5xx7/repo\", \"--revision\", \"70525a415728c6f4c31e20e44720d3fe25503ab3\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-6z1f5xx7/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-6z1f5xx7/repo\", \"--revision\", \"70525a415728c6f4c31e20e44720d3fe25503ab3\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-6z1f5xx7/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-6z1f5xx7/repo\", \"--revision\", \"b503bf94412db22df2e5783c5d04feafd4fb2167\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-6z1f5xx7/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-6z1f5xx7/repo\", \"--revision\", \"a9e7ee43fd5bbc43ee7e84736f7694704da03fb2\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-6z1f5xx7/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-6z1f5xx7/repo\", \"--revision\", \"3dc10baffcadb196dcd1b5011f4f07bbfa92f8c0\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-6z1f5xx7/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-6z1f5xx7/repo\", \"--revision\", \"41bc4ff7e8de3c88d744963ad23f595c98674374\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-6z1f5xx7/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-6z1f5xx7/repo\", \"--revision\", \"ee7f28e61a7a1e9dec609df9ab940c4c838c27a7\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.111
      },
      "verdict": "survived"
    },
    {
      "id": "C1-10",
      "script": "measure_c1.py",
      "check": "Claims array nonempty",
      "pattern": "not claims",
      "replacement": "False",
      "expected": "survived",
      "expectationReason": "No selftest fixture invalidates this check.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-6z1f5xx7/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-6z1f5xx7/repo\", \"--revision\", \"70525a415728c6f4c31e20e44720d3fe25503ab3\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-6z1f5xx7/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-6z1f5xx7/repo\", \"--revision\", \"70525a415728c6f4c31e20e44720d3fe25503ab3\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-6z1f5xx7/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-6z1f5xx7/repo\", \"--revision\", \"b503bf94412db22df2e5783c5d04feafd4fb2167\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-6z1f5xx7/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-6z1f5xx7/repo\", \"--revision\", \"a9e7ee43fd5bbc43ee7e84736f7694704da03fb2\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-6z1f5xx7/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-6z1f5xx7/repo\", \"--revision\", \"3dc10baffcadb196dcd1b5011f4f07bbfa92f8c0\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-6z1f5xx7/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-6z1f5xx7/repo\", \"--revision\", \"41bc4ff7e8de3c88d744963ad23f595c98674374\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-6z1f5xx7/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-6z1f5xx7/repo\", \"--revision\", \"ee7f28e61a7a1e9dec609df9ab940c4c838c27a7\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.111
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "35fee7dcefcb40811842d1bb78a6e0c23654c7f3",
      "mutatedSha256": {
        "measure_c1.py": "4cf4887cd4a861c6a813d3efc2077a3bc1aa1acb0f0ce9e91123f91f67e0da4e",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "d2463fb03c3003232cbac4b977a64f8a2939c306",
      "committedMutationSha256": "4cf4887cd4a861c6a813d3efc2077a3bc1aa1acb0f0ce9e91123f91f67e0da4e",
      "mutated": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ldwuweho/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ldwuweho/repo\", \"--revision\", \"d24b273a14619e5ec91750567bc41031e7c59e58\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ldwuweho/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ldwuweho/repo\", \"--revision\", \"d24b273a14619e5ec91750567bc41031e7c59e58\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ldwuweho/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ldwuweho/repo\", \"--revision\", \"cd051de175553c52f9368b303819842b7364fb4d\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ldwuweho/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ldwuweho/repo\", \"--revision\", \"91e6a1d15d4d9f6382c117cf7bc203989b235083\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ldwuweho/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ldwuweho/repo\", \"--revision\", \"c061506e4631c02fa8bbf1aa6e1f8fb917a66ba3\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ldwuweho/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ldwuweho/repo\", \"--revision\", \"550942546fe5900ece5c2799d31b1749590b514b\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ldwuweho/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ldwuweho/repo\", \"--revision\", \"be83e6cd259b0c240e683a5fafab2813f96a2fa1\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.16
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "ada21c4ff326dbf615482d0ab354572c97da8c37",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-dr83a3er/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-dr83a3er/repo\", \"--revision\", \"edfd1dded2d5d311f54ff14f942c90639422b0d4\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-dr83a3er/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-dr83a3er/repo\", \"--revision\", \"edfd1dded2d5d311f54ff14f942c90639422b0d4\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-dr83a3er/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-dr83a3er/repo\", \"--revision\", \"5eed45dd13976970733cc7c0b793556b581a98e3\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-dr83a3er/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-dr83a3er/repo\", \"--revision\", \"789e2e47b088e419d8bfb395696f1d7edea68e7d\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-dr83a3er/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-dr83a3er/repo\", \"--revision\", \"756ad65241bbca98a0dc949ef28cd7808ca58b5b\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-dr83a3er/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-dr83a3er/repo\", \"--revision\", \"eef3557aaefe3a7cb6be5419170a0ad52e2f3652\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-dr83a3er/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-dr83a3er/repo\", \"--revision\", \"e8d459a58925bb4f14ba6b2473e721e633ed7555\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.102
      },
      "verdict": "survived"
    },
    {
      "id": "C1-11",
      "script": "measure_c1.py",
      "check": "Missing current unit rejection",
      "pattern": "return problems + [\"unit file missing at revision\"], verdicts",
      "replacement": "return problems, verdicts",
      "expected": "survived",
      "expectationReason": "No selftest fixture invalidates this check.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-dr83a3er/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-dr83a3er/repo\", \"--revision\", \"edfd1dded2d5d311f54ff14f942c90639422b0d4\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-dr83a3er/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-dr83a3er/repo\", \"--revision\", \"edfd1dded2d5d311f54ff14f942c90639422b0d4\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-dr83a3er/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-dr83a3er/repo\", \"--revision\", \"5eed45dd13976970733cc7c0b793556b581a98e3\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-dr83a3er/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-dr83a3er/repo\", \"--revision\", \"789e2e47b088e419d8bfb395696f1d7edea68e7d\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-dr83a3er/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-dr83a3er/repo\", \"--revision\", \"756ad65241bbca98a0dc949ef28cd7808ca58b5b\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-dr83a3er/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-dr83a3er/repo\", \"--revision\", \"eef3557aaefe3a7cb6be5419170a0ad52e2f3652\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-dr83a3er/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-dr83a3er/repo\", \"--revision\", \"e8d459a58925bb4f14ba6b2473e721e633ed7555\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.102
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "ada21c4ff326dbf615482d0ab354572c97da8c37",
      "mutatedSha256": {
        "measure_c1.py": "d53c382179c5157e952c56fbddf244eed33b2c62c86b418b20f8016263b1d193",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "8584936b85ad2677d4af360adca559dcb2a440a9",
      "committedMutationSha256": "d53c382179c5157e952c56fbddf244eed33b2c62c86b418b20f8016263b1d193",
      "mutated": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ucygg_9i/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ucygg_9i/repo\", \"--revision\", \"db8c78748aa112974970d01088bc92130550ff23\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ucygg_9i/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ucygg_9i/repo\", \"--revision\", \"db8c78748aa112974970d01088bc92130550ff23\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ucygg_9i/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ucygg_9i/repo\", \"--revision\", \"0e79c47bf16da388027ebaf277a4dafe9817c045\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ucygg_9i/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ucygg_9i/repo\", \"--revision\", \"bf472b0fbbb8332157d06987caf3313f74f00742\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ucygg_9i/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ucygg_9i/repo\", \"--revision\", \"3c44df6ea4dd3e2a9dafaba244df2b7bac89152d\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ucygg_9i/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ucygg_9i/repo\", \"--revision\", \"727908e6d062c6a432c086960287b68194b75168\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ucygg_9i/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ucygg_9i/repo\", \"--revision\", \"cecfd601bdfb2e5b73f73a57da9dffbd262266b1\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.135
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "dc4856b8e55054be9af2d5a07f23897ea231766f",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-sdirsk9t/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-sdirsk9t/repo\", \"--revision\", \"8b99520ca38dc8e2ab30e0fd92be5d481507b7fa\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-sdirsk9t/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-sdirsk9t/repo\", \"--revision\", \"8b99520ca38dc8e2ab30e0fd92be5d481507b7fa\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-sdirsk9t/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-sdirsk9t/repo\", \"--revision\", \"d45dc49dd29925b105938d9927737f498c0577a3\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-sdirsk9t/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-sdirsk9t/repo\", \"--revision\", \"3444b401bc4db2bddd76042fed877fd915d0e204\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-sdirsk9t/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-sdirsk9t/repo\", \"--revision\", \"948c7eac9ed235422b89a72aed8593d72ca63a5f\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-sdirsk9t/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-sdirsk9t/repo\", \"--revision\", \"ac66af4ef582f4b43236e8f5bc684c72181f5cf6\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-sdirsk9t/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-sdirsk9t/repo\", \"--revision\", \"46215d2e65e1942eba599a8885e9e6f80001a03b\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.087
      },
      "verdict": "survived"
    },
    {
      "id": "C1-12",
      "script": "measure_c1.py",
      "check": "Round-23 heading diagnostic",
      "pattern": "position < 0",
      "replacement": "False",
      "expected": "killed",
      "expectationReason": "Missing-heading fixture requires the explicit heading diagnostic, even though citation checks also fail.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-sdirsk9t/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-sdirsk9t/repo\", \"--revision\", \"8b99520ca38dc8e2ab30e0fd92be5d481507b7fa\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-sdirsk9t/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-sdirsk9t/repo\", \"--revision\", \"8b99520ca38dc8e2ab30e0fd92be5d481507b7fa\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-sdirsk9t/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-sdirsk9t/repo\", \"--revision\", \"d45dc49dd29925b105938d9927737f498c0577a3\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-sdirsk9t/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-sdirsk9t/repo\", \"--revision\", \"3444b401bc4db2bddd76042fed877fd915d0e204\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-sdirsk9t/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-sdirsk9t/repo\", \"--revision\", \"948c7eac9ed235422b89a72aed8593d72ca63a5f\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-sdirsk9t/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-sdirsk9t/repo\", \"--revision\", \"ac66af4ef582f4b43236e8f5bc684c72181f5cf6\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-sdirsk9t/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-sdirsk9t/repo\", \"--revision\", \"46215d2e65e1942eba599a8885e9e6f80001a03b\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.087
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "dc4856b8e55054be9af2d5a07f23897ea231766f",
      "mutatedSha256": {
        "measure_c1.py": "5a795942b82d1acb85dcae9609ff6ee3f4826da4c758504c18607f21c2ca8d54",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "02169c85664df70fe08e209e146941284eac08ed",
      "committedMutationSha256": "5a795942b82d1acb85dcae9609ff6ee3f4826da4c758504c18607f21c2ca8d54",
      "mutated": {
        "exit": 1,
        "stdout": "",
        "stderr": "counter_selftest: {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-qxf9_8qd/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-qxf9_8qd/repo\", \"--revision\", \"a633c7d0d6b67668d5747db1ba9a3d2f2857d8ac\"], \"errors\": [\"target 'fire-journal-codes' lacks problem 'round-23 heading missing in unit file'\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"output\": {\"accepted\": 16, \"claimVerdicts\": {\"HOLD\": 17, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"revision\": \"a633c7d0d6b67668d5747db1ba9a3d2f2857d8ac\", \"total\": 17, \"units\": [{\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"drift-detection\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": false, \"problems\": [\"claim fixture: not cited in round-23 section\"], \"unit\": \"fire-journal-codes\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"fleet-registry\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"free-read-verbs\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"ghp-subpath-spotcheck\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"keeper-timer-inert\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"kimi-subpath-audit\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"mirror-pitfalls\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"ops-automation\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"origin-repos\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"probe-delta-alerting\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"publish-channels\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"publish-queue\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"sitemap-orphan-audit\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"speedrun-pipeline\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"vault-properties\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"property-map\"}]}, \"passed\": false, \"stderr\": \"\", \"total\": 17}\n",
        "elapsedSeconds": 1.151
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "363fa2aa2f0d6b8abe6ed43fc7e495047871a783",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-g57md89q/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-g57md89q/repo\", \"--revision\", \"344267396abe2fc1c7cb1ed00262531177a832d1\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-g57md89q/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-g57md89q/repo\", \"--revision\", \"344267396abe2fc1c7cb1ed00262531177a832d1\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-g57md89q/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-g57md89q/repo\", \"--revision\", \"a08155904761469c016187b2d98ac5e7f6dd922d\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-g57md89q/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-g57md89q/repo\", \"--revision\", \"44dd05cb3e3c6dd019956dff56a9e3e82a1ce53a\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-g57md89q/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-g57md89q/repo\", \"--revision\", \"b20bb5daa16db476f74e48357b25caf3de22dedb\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-g57md89q/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-g57md89q/repo\", \"--revision\", \"27e14ee70ab23419998bbfa1f23a54efc26cddd9\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-g57md89q/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-g57md89q/repo\", \"--revision\", \"7a29ae9fdf24e30c5df6edc071024991920e7f8c\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.133
      },
      "verdict": "killed"
    },
    {
      "id": "C1-13",
      "script": "measure_c1.py",
      "check": "Claim row object type",
      "pattern": "not isinstance(claim, dict)",
      "replacement": "False",
      "expected": "survived",
      "expectationReason": "No selftest fixture invalidates this check.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-g57md89q/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-g57md89q/repo\", \"--revision\", \"344267396abe2fc1c7cb1ed00262531177a832d1\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-g57md89q/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-g57md89q/repo\", \"--revision\", \"344267396abe2fc1c7cb1ed00262531177a832d1\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-g57md89q/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-g57md89q/repo\", \"--revision\", \"a08155904761469c016187b2d98ac5e7f6dd922d\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-g57md89q/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-g57md89q/repo\", \"--revision\", \"44dd05cb3e3c6dd019956dff56a9e3e82a1ce53a\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-g57md89q/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-g57md89q/repo\", \"--revision\", \"b20bb5daa16db476f74e48357b25caf3de22dedb\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-g57md89q/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-g57md89q/repo\", \"--revision\", \"27e14ee70ab23419998bbfa1f23a54efc26cddd9\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-g57md89q/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-g57md89q/repo\", \"--revision\", \"7a29ae9fdf24e30c5df6edc071024991920e7f8c\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.133
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "363fa2aa2f0d6b8abe6ed43fc7e495047871a783",
      "mutatedSha256": {
        "measure_c1.py": "27590fb579067b6b039c7ad8bd41c020382efa794022ab132d0890e4b169812e",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "35d5a1da810a022632a71492c873f1c946574e9b",
      "committedMutationSha256": "27590fb579067b6b039c7ad8bd41c020382efa794022ab132d0890e4b169812e",
      "mutated": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-h99rtgrt/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-h99rtgrt/repo\", \"--revision\", \"b4c724cb6b5ba5040b793f4c0495f9b5ea80ed89\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-h99rtgrt/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-h99rtgrt/repo\", \"--revision\", \"b4c724cb6b5ba5040b793f4c0495f9b5ea80ed89\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-h99rtgrt/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-h99rtgrt/repo\", \"--revision\", \"83b459de9e2d44b39e1c570d801d9bcac4f96301\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-h99rtgrt/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-h99rtgrt/repo\", \"--revision\", \"a674b521ac88a98cb21585befbd5d94961b0a67a\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-h99rtgrt/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-h99rtgrt/repo\", \"--revision\", \"b1c522c47d759fd95080ce6bfc840e4b8f616ffe\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-h99rtgrt/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-h99rtgrt/repo\", \"--revision\", \"dec88a7c8b10779b15ff9ec92c1cabc74202a6d5\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-h99rtgrt/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-h99rtgrt/repo\", \"--revision\", \"a7df347fb6dea3b30b4b8da3f2168f1bbfdf13f4\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.099
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "3f1a8ae6dd9dcfcccc2dc3a6fc770131429c8cfe",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-dg8g1d_7/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-dg8g1d_7/repo\", \"--revision\", \"f636f04e949e4c0047efd25fd0914f44b55b7aac\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-dg8g1d_7/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-dg8g1d_7/repo\", \"--revision\", \"f636f04e949e4c0047efd25fd0914f44b55b7aac\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-dg8g1d_7/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-dg8g1d_7/repo\", \"--revision\", \"a884eae3f60cdba7e5693d2ea8edece1fb18eea7\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-dg8g1d_7/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-dg8g1d_7/repo\", \"--revision\", \"b4dbaa6595711f4f7565fc258eca13e69ca26be5\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-dg8g1d_7/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-dg8g1d_7/repo\", \"--revision\", \"f9a97854d0b19c1d60cb0205282b2db36c0c1ec3\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-dg8g1d_7/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-dg8g1d_7/repo\", \"--revision\", \"6c9954038ca9adee8f26bab43d78a320adf367be\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-dg8g1d_7/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-dg8g1d_7/repo\", \"--revision\", \"4aaaf408e0a8657bd6dbbb5a080b11e885563db0\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.056
      },
      "verdict": "survived"
    },
    {
      "id": "C1-14",
      "script": "measure_c1.py",
      "check": "Required claim fields guard",
      "pattern": "any(not isinstance(claim.get(k), str) or not claim[k].strip() for k in FIELDS)",
      "replacement": "False",
      "expected": "survived",
      "expectationReason": "No selftest fixture invalidates this check.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-dg8g1d_7/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-dg8g1d_7/repo\", \"--revision\", \"f636f04e949e4c0047efd25fd0914f44b55b7aac\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-dg8g1d_7/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-dg8g1d_7/repo\", \"--revision\", \"f636f04e949e4c0047efd25fd0914f44b55b7aac\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-dg8g1d_7/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-dg8g1d_7/repo\", \"--revision\", \"a884eae3f60cdba7e5693d2ea8edece1fb18eea7\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-dg8g1d_7/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-dg8g1d_7/repo\", \"--revision\", \"b4dbaa6595711f4f7565fc258eca13e69ca26be5\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-dg8g1d_7/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-dg8g1d_7/repo\", \"--revision\", \"f9a97854d0b19c1d60cb0205282b2db36c0c1ec3\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-dg8g1d_7/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-dg8g1d_7/repo\", \"--revision\", \"6c9954038ca9adee8f26bab43d78a320adf367be\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-dg8g1d_7/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-dg8g1d_7/repo\", \"--revision\", \"4aaaf408e0a8657bd6dbbb5a080b11e885563db0\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.056
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "3f1a8ae6dd9dcfcccc2dc3a6fc770131429c8cfe",
      "mutatedSha256": {
        "measure_c1.py": "9350f3344d4be91500020306369559648c6cff14f164fe6dd7c2d621843d97a5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "8d99f35aa1c400b1ef9bf909445c519b23f63817",
      "committedMutationSha256": "9350f3344d4be91500020306369559648c6cff14f164fe6dd7c2d621843d97a5",
      "mutated": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-fat7mxc3/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-fat7mxc3/repo\", \"--revision\", \"6e61a5bb72c736755ba7b35f357d9815ae57f112\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-fat7mxc3/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-fat7mxc3/repo\", \"--revision\", \"6e61a5bb72c736755ba7b35f357d9815ae57f112\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-fat7mxc3/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-fat7mxc3/repo\", \"--revision\", \"460a7d52fe8cbd2b3311638a5a37e0a648a79183\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-fat7mxc3/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-fat7mxc3/repo\", \"--revision\", \"57077fc002109a419aacdc63503a7c5ab953b3eb\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-fat7mxc3/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-fat7mxc3/repo\", \"--revision\", \"6de095d1ce5cf08ede2c1bd3348dd76769a4a0a4\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-fat7mxc3/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-fat7mxc3/repo\", \"--revision\", \"793e2e6b36ac450a5c5afa6660fd7ed1efa79333\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-fat7mxc3/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-fat7mxc3/repo\", \"--revision\", \"d4109eddf13308b46e0dfc73f7c1b720cc65ab70\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.037
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "6736ea9570ba7704d9fb4f100ffbda2453f8b755",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-x6m_fy8y/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-x6m_fy8y/repo\", \"--revision\", \"b9cc0944b6fd506f702bf8b979dd6de3d1daeaa2\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-x6m_fy8y/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-x6m_fy8y/repo\", \"--revision\", \"b9cc0944b6fd506f702bf8b979dd6de3d1daeaa2\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-x6m_fy8y/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-x6m_fy8y/repo\", \"--revision\", \"c2cbef3fc51bb2330c248ef2a717091044541ea0\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-x6m_fy8y/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-x6m_fy8y/repo\", \"--revision\", \"d363170e550428ca925da5bb5db6f140f3131850\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-x6m_fy8y/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-x6m_fy8y/repo\", \"--revision\", \"c49434a30a2281cc69f6788ce88bbe36f0f26448\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-x6m_fy8y/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-x6m_fy8y/repo\", \"--revision\", \"0f49f5312804a298fe972be559929475380f439e\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-x6m_fy8y/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-x6m_fy8y/repo\", \"--revision\", \"9e2e9c0bf50668f176edf30ba9a295d1a7ba3448\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.07
      },
      "verdict": "survived"
    },
    {
      "id": "C1-15",
      "script": "measure_c1.py",
      "check": "Required claim field id",
      "pattern": "FIELDS = (\"id\", \"anchor\", \"claim\", \"surface\", \"method\", \"observation\", \"verdict\")",
      "replacement": "FIELDS = ('anchor', 'claim', 'surface', 'method', 'observation', 'verdict')",
      "expected": "survived",
      "expectationReason": "No selftest fixture invalidates this check.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-x6m_fy8y/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-x6m_fy8y/repo\", \"--revision\", \"b9cc0944b6fd506f702bf8b979dd6de3d1daeaa2\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-x6m_fy8y/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-x6m_fy8y/repo\", \"--revision\", \"b9cc0944b6fd506f702bf8b979dd6de3d1daeaa2\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-x6m_fy8y/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-x6m_fy8y/repo\", \"--revision\", \"c2cbef3fc51bb2330c248ef2a717091044541ea0\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-x6m_fy8y/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-x6m_fy8y/repo\", \"--revision\", \"d363170e550428ca925da5bb5db6f140f3131850\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-x6m_fy8y/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-x6m_fy8y/repo\", \"--revision\", \"c49434a30a2281cc69f6788ce88bbe36f0f26448\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-x6m_fy8y/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-x6m_fy8y/repo\", \"--revision\", \"0f49f5312804a298fe972be559929475380f439e\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-x6m_fy8y/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-x6m_fy8y/repo\", \"--revision\", \"9e2e9c0bf50668f176edf30ba9a295d1a7ba3448\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.07
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "6736ea9570ba7704d9fb4f100ffbda2453f8b755",
      "mutatedSha256": {
        "measure_c1.py": "239087d32817f4d094183860ee84291158a0c99536755f8503cf46c88f3f7b08",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "72a6a0ca556e3d51525cbb872346b0a8e0008528",
      "committedMutationSha256": "239087d32817f4d094183860ee84291158a0c99536755f8503cf46c88f3f7b08",
      "mutated": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ibk4ha47/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ibk4ha47/repo\", \"--revision\", \"aec871aeb6b44ddaa23e737f41a8cfec30e2fa6a\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ibk4ha47/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ibk4ha47/repo\", \"--revision\", \"aec871aeb6b44ddaa23e737f41a8cfec30e2fa6a\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ibk4ha47/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ibk4ha47/repo\", \"--revision\", \"bed4d93c0f8a482ad81d5764289ced2617f2037c\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ibk4ha47/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ibk4ha47/repo\", \"--revision\", \"5e1c31c7923e37e5ce903a61a6a83cacd886885d\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ibk4ha47/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ibk4ha47/repo\", \"--revision\", \"2da4857cac5b200b5b01bebdc0e92b685e6fbe90\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ibk4ha47/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ibk4ha47/repo\", \"--revision\", \"e32aa1f1dd58509b7cefd910404e2fe1a0cf75ef\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ibk4ha47/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ibk4ha47/repo\", \"--revision\", \"4cad01caa155f6573826b722fb45f4d02a387d2b\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.085
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "dead865b7cc8dfd1b975c49276d837c51f4927fd",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-4_jvkp7h/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-4_jvkp7h/repo\", \"--revision\", \"96e18116d029e2ae79247857e0f17ac613573bf2\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-4_jvkp7h/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-4_jvkp7h/repo\", \"--revision\", \"96e18116d029e2ae79247857e0f17ac613573bf2\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-4_jvkp7h/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-4_jvkp7h/repo\", \"--revision\", \"84d7c299c394d48e7e0405b56ae76ff9300049d6\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-4_jvkp7h/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-4_jvkp7h/repo\", \"--revision\", \"97bd627620e27869f9186807e23dface6d7b0dd7\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-4_jvkp7h/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-4_jvkp7h/repo\", \"--revision\", \"4ade3b7bce0db2e41e8ce8592f0b5ce8e0aa127f\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-4_jvkp7h/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-4_jvkp7h/repo\", \"--revision\", \"534d78334e19d4a29b7b0fab00f63ab5d5714fa2\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-4_jvkp7h/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-4_jvkp7h/repo\", \"--revision\", \"6ceecc5ab5a307099b9b7426e18b16559676a354\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.101
      },
      "verdict": "survived"
    },
    {
      "id": "C1-16",
      "script": "measure_c1.py",
      "check": "Required claim field anchor",
      "pattern": "FIELDS = (\"id\", \"anchor\", \"claim\", \"surface\", \"method\", \"observation\", \"verdict\")",
      "replacement": "FIELDS = ('id', 'claim', 'surface', 'method', 'observation', 'verdict')",
      "expected": "survived",
      "expectationReason": "No selftest fixture invalidates this check.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-4_jvkp7h/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-4_jvkp7h/repo\", \"--revision\", \"96e18116d029e2ae79247857e0f17ac613573bf2\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-4_jvkp7h/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-4_jvkp7h/repo\", \"--revision\", \"96e18116d029e2ae79247857e0f17ac613573bf2\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-4_jvkp7h/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-4_jvkp7h/repo\", \"--revision\", \"84d7c299c394d48e7e0405b56ae76ff9300049d6\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-4_jvkp7h/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-4_jvkp7h/repo\", \"--revision\", \"97bd627620e27869f9186807e23dface6d7b0dd7\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-4_jvkp7h/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-4_jvkp7h/repo\", \"--revision\", \"4ade3b7bce0db2e41e8ce8592f0b5ce8e0aa127f\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-4_jvkp7h/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-4_jvkp7h/repo\", \"--revision\", \"534d78334e19d4a29b7b0fab00f63ab5d5714fa2\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-4_jvkp7h/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-4_jvkp7h/repo\", \"--revision\", \"6ceecc5ab5a307099b9b7426e18b16559676a354\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.101
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "dead865b7cc8dfd1b975c49276d837c51f4927fd",
      "mutatedSha256": {
        "measure_c1.py": "2402d63f34c434c113ae850f156969ee96d48ebb1998231e27bfbdca40385881",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "19e36c6867867ae83a59998f93e2df3bc0247566",
      "committedMutationSha256": "2402d63f34c434c113ae850f156969ee96d48ebb1998231e27bfbdca40385881",
      "mutated": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-bh7aqayr/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-bh7aqayr/repo\", \"--revision\", \"1392142073ceb7522c3624a6c57a892270860b7e\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-bh7aqayr/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-bh7aqayr/repo\", \"--revision\", \"1392142073ceb7522c3624a6c57a892270860b7e\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-bh7aqayr/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-bh7aqayr/repo\", \"--revision\", \"7343add98406198ce0ebf880ecfc804cbff244b2\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-bh7aqayr/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-bh7aqayr/repo\", \"--revision\", \"694d9f96d0c2d367d1326dae8130a545508f09cd\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-bh7aqayr/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-bh7aqayr/repo\", \"--revision\", \"61857ccc2c83b2976fdc70486a3075b0b61dfebe\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-bh7aqayr/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-bh7aqayr/repo\", \"--revision\", \"4d3dd902436bc626c7f85398cc6f39e4c79cc515\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-bh7aqayr/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-bh7aqayr/repo\", \"--revision\", \"6835f1f38483c672b9904dfff049261547cedd39\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.14
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "94e559571df5e7499e2bba07bb1d8e345cd82df5",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-uq_t82l1/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-uq_t82l1/repo\", \"--revision\", \"35e7ba673c1ce84c9cf3e46aced87827c262d577\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-uq_t82l1/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-uq_t82l1/repo\", \"--revision\", \"35e7ba673c1ce84c9cf3e46aced87827c262d577\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-uq_t82l1/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-uq_t82l1/repo\", \"--revision\", \"8f4e5fcd8371c8b5a073f3301b08390c0955ab1b\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-uq_t82l1/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-uq_t82l1/repo\", \"--revision\", \"0e426f7edac4f48e9d4dc5435558fb1b0e9d9b77\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-uq_t82l1/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-uq_t82l1/repo\", \"--revision\", \"af059be0e76ad03ab7f866909a5b7b57d10f6bd4\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-uq_t82l1/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-uq_t82l1/repo\", \"--revision\", \"9e0cefeefc8ec520244949664cb325cd05f7efdb\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-uq_t82l1/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-uq_t82l1/repo\", \"--revision\", \"69a874260a3279aec910bc8e21a2c4eb716ebb0b\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.064
      },
      "verdict": "survived"
    },
    {
      "id": "C1-17",
      "script": "measure_c1.py",
      "check": "Required claim field claim",
      "pattern": "FIELDS = (\"id\", \"anchor\", \"claim\", \"surface\", \"method\", \"observation\", \"verdict\")",
      "replacement": "FIELDS = ('id', 'anchor', 'surface', 'method', 'observation', 'verdict')",
      "expected": "survived",
      "expectationReason": "No selftest fixture invalidates this check.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-uq_t82l1/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-uq_t82l1/repo\", \"--revision\", \"35e7ba673c1ce84c9cf3e46aced87827c262d577\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-uq_t82l1/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-uq_t82l1/repo\", \"--revision\", \"35e7ba673c1ce84c9cf3e46aced87827c262d577\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-uq_t82l1/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-uq_t82l1/repo\", \"--revision\", \"8f4e5fcd8371c8b5a073f3301b08390c0955ab1b\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-uq_t82l1/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-uq_t82l1/repo\", \"--revision\", \"0e426f7edac4f48e9d4dc5435558fb1b0e9d9b77\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-uq_t82l1/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-uq_t82l1/repo\", \"--revision\", \"af059be0e76ad03ab7f866909a5b7b57d10f6bd4\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-uq_t82l1/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-uq_t82l1/repo\", \"--revision\", \"9e0cefeefc8ec520244949664cb325cd05f7efdb\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-uq_t82l1/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-uq_t82l1/repo\", \"--revision\", \"69a874260a3279aec910bc8e21a2c4eb716ebb0b\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.064
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "94e559571df5e7499e2bba07bb1d8e345cd82df5",
      "mutatedSha256": {
        "measure_c1.py": "525442da1d79644df0e01afa8285d1fba8d4b0b7c9389bda0ec6a2c1810b1304",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "51389dfbae59b4b58b4b7ac7c56d0ed9b899ef1f",
      "committedMutationSha256": "525442da1d79644df0e01afa8285d1fba8d4b0b7c9389bda0ec6a2c1810b1304",
      "mutated": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-4rrzyzzu/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-4rrzyzzu/repo\", \"--revision\", \"33f47689e997f6729d55867303410eb43c4e7620\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-4rrzyzzu/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-4rrzyzzu/repo\", \"--revision\", \"33f47689e997f6729d55867303410eb43c4e7620\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-4rrzyzzu/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-4rrzyzzu/repo\", \"--revision\", \"dfaabe22023b5ebdecb07ddc68890cf97624f6be\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-4rrzyzzu/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-4rrzyzzu/repo\", \"--revision\", \"9253226327cb09c8da5d66086470adf97c9f1c81\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-4rrzyzzu/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-4rrzyzzu/repo\", \"--revision\", \"ede3f4fa46a0cbcea050b1cdc44d4522b83405c8\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-4rrzyzzu/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-4rrzyzzu/repo\", \"--revision\", \"a10196e8053c22ce7ee214248fd6925801bd7fb4\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-4rrzyzzu/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-4rrzyzzu/repo\", \"--revision\", \"1f8a8bb2c2750ad80d28c22697ef7bfd0c951e1c\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.033
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "77bf71472fb2e1cf8cdcad198a0c5d21bcd650eb",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-632_d333/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-632_d333/repo\", \"--revision\", \"69b820a0eef5b6c3d8408dbcf827f32f58bbc3bd\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-632_d333/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-632_d333/repo\", \"--revision\", \"69b820a0eef5b6c3d8408dbcf827f32f58bbc3bd\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-632_d333/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-632_d333/repo\", \"--revision\", \"119120dd9cfd0932970377ae4444882ea399b2f5\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-632_d333/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-632_d333/repo\", \"--revision\", \"dceeb2a0a2fda0cdf379fb8ee33e0d7595323e8f\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-632_d333/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-632_d333/repo\", \"--revision\", \"03d9a60aba604bde35d1f624620349ec0bb35858\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-632_d333/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-632_d333/repo\", \"--revision\", \"b557f76d17b665fcd1f719eca9201959f953d724\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-632_d333/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-632_d333/repo\", \"--revision\", \"f18562c02ff7628b9bb5d780bc2f0b53cc363ae2\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.016
      },
      "verdict": "survived"
    },
    {
      "id": "C1-18",
      "script": "measure_c1.py",
      "check": "Required claim field surface",
      "pattern": "FIELDS = (\"id\", \"anchor\", \"claim\", \"surface\", \"method\", \"observation\", \"verdict\")",
      "replacement": "FIELDS = ('id', 'anchor', 'claim', 'method', 'observation', 'verdict')",
      "expected": "survived",
      "expectationReason": "No selftest fixture invalidates this check.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-632_d333/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-632_d333/repo\", \"--revision\", \"69b820a0eef5b6c3d8408dbcf827f32f58bbc3bd\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-632_d333/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-632_d333/repo\", \"--revision\", \"69b820a0eef5b6c3d8408dbcf827f32f58bbc3bd\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-632_d333/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-632_d333/repo\", \"--revision\", \"119120dd9cfd0932970377ae4444882ea399b2f5\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-632_d333/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-632_d333/repo\", \"--revision\", \"dceeb2a0a2fda0cdf379fb8ee33e0d7595323e8f\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-632_d333/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-632_d333/repo\", \"--revision\", \"03d9a60aba604bde35d1f624620349ec0bb35858\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-632_d333/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-632_d333/repo\", \"--revision\", \"b557f76d17b665fcd1f719eca9201959f953d724\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-632_d333/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-632_d333/repo\", \"--revision\", \"f18562c02ff7628b9bb5d780bc2f0b53cc363ae2\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.016
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "77bf71472fb2e1cf8cdcad198a0c5d21bcd650eb",
      "mutatedSha256": {
        "measure_c1.py": "034e3e9ad721bd56dde7ee390a9426cf97e8c47e0785034c9133076edbe66cac",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "69a0b074f0dd9b2373d3faf5244b39ecfc018fc0",
      "committedMutationSha256": "034e3e9ad721bd56dde7ee390a9426cf97e8c47e0785034c9133076edbe66cac",
      "mutated": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-g1hc80wf/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-g1hc80wf/repo\", \"--revision\", \"da1d55389999d5b51e5a2cbc13a34563a465ba0d\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-g1hc80wf/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-g1hc80wf/repo\", \"--revision\", \"da1d55389999d5b51e5a2cbc13a34563a465ba0d\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-g1hc80wf/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-g1hc80wf/repo\", \"--revision\", \"3319d890b7d9100d43bf74edee525119b8b0a1ad\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-g1hc80wf/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-g1hc80wf/repo\", \"--revision\", \"e973e378d39637fd04bdb61b17994d780e9c3c72\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-g1hc80wf/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-g1hc80wf/repo\", \"--revision\", \"ceec21126c0d599f567a459877fff4dd80d86964\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-g1hc80wf/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-g1hc80wf/repo\", \"--revision\", \"61aff102890a8315694bb3e4a5022cbe6f02af09\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-g1hc80wf/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-g1hc80wf/repo\", \"--revision\", \"406e4386470be7862d07420ff53f3f03ebba676e\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.035
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "bbc152daaba7a4bfb1698cf3afdb564b32ec6d3d",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-6n6t_95q/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-6n6t_95q/repo\", \"--revision\", \"0278ecd84d2a320554e59ebf2c95a2e615ab0132\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-6n6t_95q/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-6n6t_95q/repo\", \"--revision\", \"0278ecd84d2a320554e59ebf2c95a2e615ab0132\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-6n6t_95q/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-6n6t_95q/repo\", \"--revision\", \"a933328e6829a25fe0dde7352cea867b5fb3f7bd\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-6n6t_95q/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-6n6t_95q/repo\", \"--revision\", \"08b54333158c82a76da3013d4d28400d89a7023b\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-6n6t_95q/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-6n6t_95q/repo\", \"--revision\", \"12022df276593f66e4c056eba64bc0fb3db955fc\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-6n6t_95q/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-6n6t_95q/repo\", \"--revision\", \"cc70455c4601b87d2c9b656cd1b8e7646a20eb7b\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-6n6t_95q/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-6n6t_95q/repo\", \"--revision\", \"1e1162b5c05d55617bcd28fb9fd0df588b62c148\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.021
      },
      "verdict": "survived"
    },
    {
      "id": "C1-19",
      "script": "measure_c1.py",
      "check": "Required claim field method",
      "pattern": "FIELDS = (\"id\", \"anchor\", \"claim\", \"surface\", \"method\", \"observation\", \"verdict\")",
      "replacement": "FIELDS = ('id', 'anchor', 'claim', 'surface', 'observation', 'verdict')",
      "expected": "survived",
      "expectationReason": "No selftest fixture invalidates this check.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-6n6t_95q/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-6n6t_95q/repo\", \"--revision\", \"0278ecd84d2a320554e59ebf2c95a2e615ab0132\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-6n6t_95q/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-6n6t_95q/repo\", \"--revision\", \"0278ecd84d2a320554e59ebf2c95a2e615ab0132\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-6n6t_95q/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-6n6t_95q/repo\", \"--revision\", \"a933328e6829a25fe0dde7352cea867b5fb3f7bd\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-6n6t_95q/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-6n6t_95q/repo\", \"--revision\", \"08b54333158c82a76da3013d4d28400d89a7023b\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-6n6t_95q/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-6n6t_95q/repo\", \"--revision\", \"12022df276593f66e4c056eba64bc0fb3db955fc\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-6n6t_95q/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-6n6t_95q/repo\", \"--revision\", \"cc70455c4601b87d2c9b656cd1b8e7646a20eb7b\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-6n6t_95q/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-6n6t_95q/repo\", \"--revision\", \"1e1162b5c05d55617bcd28fb9fd0df588b62c148\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.021
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "bbc152daaba7a4bfb1698cf3afdb564b32ec6d3d",
      "mutatedSha256": {
        "measure_c1.py": "a3d3f2a18a180be15416fdeb014e9e2c3b233bc5246262e626623aa7f1c9795a",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "7f0ee6c85b47f3610b176a48bc5087451d819cd8",
      "committedMutationSha256": "a3d3f2a18a180be15416fdeb014e9e2c3b233bc5246262e626623aa7f1c9795a",
      "mutated": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ej0j_pr3/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ej0j_pr3/repo\", \"--revision\", \"22fb9fd82e66a10b3639068fe7fd393bcb2a350d\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ej0j_pr3/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ej0j_pr3/repo\", \"--revision\", \"22fb9fd82e66a10b3639068fe7fd393bcb2a350d\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ej0j_pr3/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ej0j_pr3/repo\", \"--revision\", \"187afb6de4ec0bbcd4e8b82644da2e681b18d065\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ej0j_pr3/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ej0j_pr3/repo\", \"--revision\", \"74ad32ac035ee209f266115905d08ff44f81f559\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ej0j_pr3/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ej0j_pr3/repo\", \"--revision\", \"f6f0913c7c72d6ea3abbf6d72417990d12821002\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ej0j_pr3/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ej0j_pr3/repo\", \"--revision\", \"fe8a68cedbf2882d9d26cd1f9f4e582337f04e32\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ej0j_pr3/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ej0j_pr3/repo\", \"--revision\", \"3f7d3acd8f733c6b1a83c1808dbecc165b354252\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.037
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "e0b54c8b78892fa525af9c97249cedb781389c56",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xi6xodpu/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xi6xodpu/repo\", \"--revision\", \"43394d11b6d67b4a3e57fe42a5cbde9bc10c71c5\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xi6xodpu/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xi6xodpu/repo\", \"--revision\", \"43394d11b6d67b4a3e57fe42a5cbde9bc10c71c5\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xi6xodpu/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xi6xodpu/repo\", \"--revision\", \"feacc61a48847ea9a46570058c9abe3563f94ba2\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xi6xodpu/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xi6xodpu/repo\", \"--revision\", \"bb2e4c83b35251c14e85142285ee4dcb499bcd61\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xi6xodpu/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xi6xodpu/repo\", \"--revision\", \"4b2f2567e6603c17221dffa2457b8bf2c8c53e25\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xi6xodpu/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xi6xodpu/repo\", \"--revision\", \"7dc4cbea02c216fdd5e8fd529b24a0548121971b\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xi6xodpu/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xi6xodpu/repo\", \"--revision\", \"70d6f395f7aaa5ef59740267e9bf9e62682041f3\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.121
      },
      "verdict": "survived"
    },
    {
      "id": "C1-20",
      "script": "measure_c1.py",
      "check": "Required claim field observation",
      "pattern": "FIELDS = (\"id\", \"anchor\", \"claim\", \"surface\", \"method\", \"observation\", \"verdict\")",
      "replacement": "FIELDS = ('id', 'anchor', 'claim', 'surface', 'method', 'verdict')",
      "expected": "survived",
      "expectationReason": "No selftest fixture invalidates this check.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xi6xodpu/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xi6xodpu/repo\", \"--revision\", \"43394d11b6d67b4a3e57fe42a5cbde9bc10c71c5\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xi6xodpu/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xi6xodpu/repo\", \"--revision\", \"43394d11b6d67b4a3e57fe42a5cbde9bc10c71c5\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xi6xodpu/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xi6xodpu/repo\", \"--revision\", \"feacc61a48847ea9a46570058c9abe3563f94ba2\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xi6xodpu/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xi6xodpu/repo\", \"--revision\", \"bb2e4c83b35251c14e85142285ee4dcb499bcd61\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xi6xodpu/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xi6xodpu/repo\", \"--revision\", \"4b2f2567e6603c17221dffa2457b8bf2c8c53e25\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xi6xodpu/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xi6xodpu/repo\", \"--revision\", \"7dc4cbea02c216fdd5e8fd529b24a0548121971b\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xi6xodpu/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xi6xodpu/repo\", \"--revision\", \"70d6f395f7aaa5ef59740267e9bf9e62682041f3\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.121
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "e0b54c8b78892fa525af9c97249cedb781389c56",
      "mutatedSha256": {
        "measure_c1.py": "bbc857e9011e1f6da4d091a118cc294e16be98bad674a35d72cd9881f082818f",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "49920d582ccd27cca9ebe5749a4ac066528f53b4",
      "committedMutationSha256": "bbc857e9011e1f6da4d091a118cc294e16be98bad674a35d72cd9881f082818f",
      "mutated": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-goal_ebe/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-goal_ebe/repo\", \"--revision\", \"2c1defb80b8323f29b1d6ad75c2e4b65380a164e\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-goal_ebe/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-goal_ebe/repo\", \"--revision\", \"2c1defb80b8323f29b1d6ad75c2e4b65380a164e\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-goal_ebe/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-goal_ebe/repo\", \"--revision\", \"ebffb3230687cf25d505df75aa2d8234a52248cc\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-goal_ebe/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-goal_ebe/repo\", \"--revision\", \"34e0f797e9a214c27f6a1035f6fd543ff1d011bb\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-goal_ebe/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-goal_ebe/repo\", \"--revision\", \"b1e4fb1c69e4eb531ab6560ad72e063f7d2454cf\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-goal_ebe/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-goal_ebe/repo\", \"--revision\", \"16862a50e212d007ee034ee1fd81320491d56b2b\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-goal_ebe/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-goal_ebe/repo\", \"--revision\", \"6c8de1273f08055fa8622b5b90199e93f0c14d5c\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.105
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "1144b0bbd97dc6e421ce66796cad88ab34000192",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-adndmt9h/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-adndmt9h/repo\", \"--revision\", \"19f0c68741a132808343ff03e19d43c3667bf9f1\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-adndmt9h/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-adndmt9h/repo\", \"--revision\", \"19f0c68741a132808343ff03e19d43c3667bf9f1\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-adndmt9h/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-adndmt9h/repo\", \"--revision\", \"46b254c2b765f4c98fecb85dd099e0e7b5d67d05\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-adndmt9h/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-adndmt9h/repo\", \"--revision\", \"1baf7b28e8de5240611f0e1b433ada56ef1a8ac4\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-adndmt9h/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-adndmt9h/repo\", \"--revision\", \"6eddfb2ba7a2aea585c1206b1ddc5e34424e9b66\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-adndmt9h/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-adndmt9h/repo\", \"--revision\", \"37fc5fc3934321113d5367b17e1d3f84f0235fa3\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-adndmt9h/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-adndmt9h/repo\", \"--revision\", \"2a7197301988f065daa8ac77347d39d3594c7922\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.037
      },
      "verdict": "survived"
    },
    {
      "id": "C1-21",
      "script": "measure_c1.py",
      "check": "Required claim field verdict",
      "pattern": "FIELDS = (\"id\", \"anchor\", \"claim\", \"surface\", \"method\", \"observation\", \"verdict\")",
      "replacement": "FIELDS = ('id', 'anchor', 'claim', 'surface', 'method', 'observation')",
      "expected": "survived",
      "expectationReason": "No selftest fixture invalidates this check.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-adndmt9h/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-adndmt9h/repo\", \"--revision\", \"19f0c68741a132808343ff03e19d43c3667bf9f1\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-adndmt9h/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-adndmt9h/repo\", \"--revision\", \"19f0c68741a132808343ff03e19d43c3667bf9f1\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-adndmt9h/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-adndmt9h/repo\", \"--revision\", \"46b254c2b765f4c98fecb85dd099e0e7b5d67d05\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-adndmt9h/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-adndmt9h/repo\", \"--revision\", \"1baf7b28e8de5240611f0e1b433ada56ef1a8ac4\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-adndmt9h/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-adndmt9h/repo\", \"--revision\", \"6eddfb2ba7a2aea585c1206b1ddc5e34424e9b66\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-adndmt9h/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-adndmt9h/repo\", \"--revision\", \"37fc5fc3934321113d5367b17e1d3f84f0235fa3\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-adndmt9h/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-adndmt9h/repo\", \"--revision\", \"2a7197301988f065daa8ac77347d39d3594c7922\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.037
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "1144b0bbd97dc6e421ce66796cad88ab34000192",
      "mutatedSha256": {
        "measure_c1.py": "33731cf2555b2dba5fdd865ec719fb11700f885591b1ce66307f79de0c9e31f6",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "794c022d2dd2de47eeee353a0a70a419de754ff8",
      "committedMutationSha256": "33731cf2555b2dba5fdd865ec719fb11700f885591b1ce66307f79de0c9e31f6",
      "mutated": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-rsdwq9jc/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-rsdwq9jc/repo\", \"--revision\", \"6be948af65d4df3c4b1f78fc0d9dbbc0f42e80fa\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-rsdwq9jc/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-rsdwq9jc/repo\", \"--revision\", \"6be948af65d4df3c4b1f78fc0d9dbbc0f42e80fa\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-rsdwq9jc/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-rsdwq9jc/repo\", \"--revision\", \"5ddd2db24275350f230fcda8398c72cdbabc01a8\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-rsdwq9jc/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-rsdwq9jc/repo\", \"--revision\", \"6c5884ea876093548354e47b7cddde033db7dd5c\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-rsdwq9jc/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-rsdwq9jc/repo\", \"--revision\", \"136eb84be377197127a9af8455f203d76a53febb\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-rsdwq9jc/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-rsdwq9jc/repo\", \"--revision\", \"3a8c8c7ebc15bf8e3149e4468593dc856f87cdda\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-rsdwq9jc/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-rsdwq9jc/repo\", \"--revision\", \"94f19b6bf498f2e48f09e01355568443aa3bda98\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.029
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "897b6b2cc04bdaa6c584808936f1027f3e84032f",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-7_5vhxjw/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-7_5vhxjw/repo\", \"--revision\", \"39f754bcd51d569a4f1261da8706971fccf1a31f\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-7_5vhxjw/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-7_5vhxjw/repo\", \"--revision\", \"39f754bcd51d569a4f1261da8706971fccf1a31f\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-7_5vhxjw/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-7_5vhxjw/repo\", \"--revision\", \"444fd2bf1ee8d6e739ce0ade466d3c02ffe1fb91\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-7_5vhxjw/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-7_5vhxjw/repo\", \"--revision\", \"929c95312d58b129a06e232e7641d9792dd250d5\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-7_5vhxjw/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-7_5vhxjw/repo\", \"--revision\", \"34b19060cdae1145624e42b28d425c9b8213aecc\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-7_5vhxjw/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-7_5vhxjw/repo\", \"--revision\", \"bab277610cd20f4ccf74f25a81c9be16d20e2a0a\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-7_5vhxjw/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-7_5vhxjw/repo\", \"--revision\", \"067f4cf4d32b9ea7084a2e38ec9a6ab932c6ea0c\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.058
      },
      "verdict": "survived"
    },
    {
      "id": "C1-22",
      "script": "measure_c1.py",
      "check": "Duplicate claim IDs",
      "pattern": "claim[\"id\"] in seen",
      "replacement": "False",
      "expected": "survived",
      "expectationReason": "No selftest fixture invalidates this check.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-7_5vhxjw/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-7_5vhxjw/repo\", \"--revision\", \"39f754bcd51d569a4f1261da8706971fccf1a31f\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-7_5vhxjw/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-7_5vhxjw/repo\", \"--revision\", \"39f754bcd51d569a4f1261da8706971fccf1a31f\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-7_5vhxjw/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-7_5vhxjw/repo\", \"--revision\", \"444fd2bf1ee8d6e739ce0ade466d3c02ffe1fb91\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-7_5vhxjw/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-7_5vhxjw/repo\", \"--revision\", \"929c95312d58b129a06e232e7641d9792dd250d5\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-7_5vhxjw/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-7_5vhxjw/repo\", \"--revision\", \"34b19060cdae1145624e42b28d425c9b8213aecc\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-7_5vhxjw/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-7_5vhxjw/repo\", \"--revision\", \"bab277610cd20f4ccf74f25a81c9be16d20e2a0a\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-7_5vhxjw/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-7_5vhxjw/repo\", \"--revision\", \"067f4cf4d32b9ea7084a2e38ec9a6ab932c6ea0c\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.058
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "897b6b2cc04bdaa6c584808936f1027f3e84032f",
      "mutatedSha256": {
        "measure_c1.py": "d527b7fa022a74d1254fe2966bd22624ee8da021213e91d760a60cfa0ad6757d",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "9deb4ace2a28f7fe3c9cce911fdeb303daefffec",
      "committedMutationSha256": "d527b7fa022a74d1254fe2966bd22624ee8da021213e91d760a60cfa0ad6757d",
      "mutated": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-6l0tq4to/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-6l0tq4to/repo\", \"--revision\", \"831cfb9224e1f0f0869eab22b183f826b0a56800\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-6l0tq4to/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-6l0tq4to/repo\", \"--revision\", \"831cfb9224e1f0f0869eab22b183f826b0a56800\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-6l0tq4to/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-6l0tq4to/repo\", \"--revision\", \"852cbb84f520e982b7f6849375865e0021d43bd5\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-6l0tq4to/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-6l0tq4to/repo\", \"--revision\", \"be32a5dc86c1dd1b58f102588daab0cf5786ce26\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-6l0tq4to/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-6l0tq4to/repo\", \"--revision\", \"fd333d52439be551872dbcd2dfcde239375ba97b\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-6l0tq4to/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-6l0tq4to/repo\", \"--revision\", \"4f07d1c5ce591faeced5710947fdbdd341f5e556\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-6l0tq4to/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-6l0tq4to/repo\", \"--revision\", \"28f46319841fc1cff095d86dcd539b629f4aae4f\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.063
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "46606e5ddd09cc0f51e260157219e108b301fa38",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ln2b4342/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ln2b4342/repo\", \"--revision\", \"a50597bedd3cd6c6d7acd064665603bc22fb44fc\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ln2b4342/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ln2b4342/repo\", \"--revision\", \"a50597bedd3cd6c6d7acd064665603bc22fb44fc\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ln2b4342/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ln2b4342/repo\", \"--revision\", \"3d209b0e9e90d497d3f7c707f262c32bf32d1243\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ln2b4342/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ln2b4342/repo\", \"--revision\", \"4d4170eb87795c94abceda3d0515709de04b6f2d\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ln2b4342/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ln2b4342/repo\", \"--revision\", \"1f670964b8cbe6aaff5c3456a94e26fb8a2d07ef\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ln2b4342/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ln2b4342/repo\", \"--revision\", \"b9485cf3d6e921b9a78e43836c6b9e1e74d971ad\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ln2b4342/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ln2b4342/repo\", \"--revision\", \"cc4f6343eee44ffce8890a6a5a596ff3e3f8484f\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.068
      },
      "verdict": "survived"
    },
    {
      "id": "C1-23",
      "script": "measure_c1.py",
      "check": "Allowed verdict membership",
      "pattern": "verdict not in VERDICTS",
      "replacement": "False",
      "expected": "survived",
      "expectationReason": "No selftest fixture invalidates this check.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ln2b4342/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ln2b4342/repo\", \"--revision\", \"a50597bedd3cd6c6d7acd064665603bc22fb44fc\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ln2b4342/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ln2b4342/repo\", \"--revision\", \"a50597bedd3cd6c6d7acd064665603bc22fb44fc\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ln2b4342/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ln2b4342/repo\", \"--revision\", \"3d209b0e9e90d497d3f7c707f262c32bf32d1243\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ln2b4342/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ln2b4342/repo\", \"--revision\", \"4d4170eb87795c94abceda3d0515709de04b6f2d\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ln2b4342/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ln2b4342/repo\", \"--revision\", \"1f670964b8cbe6aaff5c3456a94e26fb8a2d07ef\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ln2b4342/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ln2b4342/repo\", \"--revision\", \"b9485cf3d6e921b9a78e43836c6b9e1e74d971ad\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ln2b4342/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ln2b4342/repo\", \"--revision\", \"cc4f6343eee44ffce8890a6a5a596ff3e3f8484f\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.068
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "46606e5ddd09cc0f51e260157219e108b301fa38",
      "mutatedSha256": {
        "measure_c1.py": "9b63107cbe0285040c79ddc7eaf6c26db3bb096f8c61fb39302ea78d2d4958e8",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "5b36b5a4bdea98e03c2fefddcabc3f7f715dc4bd",
      "committedMutationSha256": "9b63107cbe0285040c79ddc7eaf6c26db3bb096f8c61fb39302ea78d2d4958e8",
      "mutated": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-49tulxvl/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-49tulxvl/repo\", \"--revision\", \"c87e1535db937e7dcbdb5a226c736b0aa34d71da\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-49tulxvl/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-49tulxvl/repo\", \"--revision\", \"c87e1535db937e7dcbdb5a226c736b0aa34d71da\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-49tulxvl/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-49tulxvl/repo\", \"--revision\", \"4fefd533432ced555966d6682e9da4cb180899ba\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-49tulxvl/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-49tulxvl/repo\", \"--revision\", \"ec72bc7de10524affcc0e49a68bdcefc1512dbe6\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-49tulxvl/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-49tulxvl/repo\", \"--revision\", \"cd1c510b217bc099375bb80f9c41ed58c137809f\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-49tulxvl/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-49tulxvl/repo\", \"--revision\", \"7a4efa59b6c8924be387875e6bed3e00534047a0\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-49tulxvl/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-49tulxvl/repo\", \"--revision\", \"be854f489bc1c02973f0cfbed95ea1670834f028\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.07
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "1cc3f21c42e602802c04605ab8321f3f5887177b",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-rb17fm9u/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-rb17fm9u/repo\", \"--revision\", \"05a0b03b521c91937d52fb2ca7e9ca680bedddf4\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-rb17fm9u/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-rb17fm9u/repo\", \"--revision\", \"05a0b03b521c91937d52fb2ca7e9ca680bedddf4\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-rb17fm9u/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-rb17fm9u/repo\", \"--revision\", \"35798a1f233ceef7dd44593c3f6e4408e8dcc451\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-rb17fm9u/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-rb17fm9u/repo\", \"--revision\", \"86b29bf8a4fa82468044c6cc0e83b2c34257f80c\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-rb17fm9u/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-rb17fm9u/repo\", \"--revision\", \"8b1dae8a231eb0701d44c5a96e08dd3a7f5117be\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-rb17fm9u/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-rb17fm9u/repo\", \"--revision\", \"350d36988380cdf4368767cf904daef58d1fad09\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-rb17fm9u/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-rb17fm9u/repo\", \"--revision\", \"4b4ea64fdf8033926a0f6cf919bcc9e1d03ff540\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.03
      },
      "verdict": "survived"
    },
    {
      "id": "C1-24",
      "script": "measure_c1.py",
      "check": "Anchor belongs to base unit",
      "pattern": "claim[\"anchor\"] not in base_text",
      "replacement": "False",
      "expected": "killed",
      "expectationReason": "Invalid-anchor fixture expects one rejected unit and the anchor diagnostic.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-rb17fm9u/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-rb17fm9u/repo\", \"--revision\", \"05a0b03b521c91937d52fb2ca7e9ca680bedddf4\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-rb17fm9u/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-rb17fm9u/repo\", \"--revision\", \"05a0b03b521c91937d52fb2ca7e9ca680bedddf4\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-rb17fm9u/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-rb17fm9u/repo\", \"--revision\", \"35798a1f233ceef7dd44593c3f6e4408e8dcc451\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-rb17fm9u/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-rb17fm9u/repo\", \"--revision\", \"86b29bf8a4fa82468044c6cc0e83b2c34257f80c\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-rb17fm9u/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-rb17fm9u/repo\", \"--revision\", \"8b1dae8a231eb0701d44c5a96e08dd3a7f5117be\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-rb17fm9u/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-rb17fm9u/repo\", \"--revision\", \"350d36988380cdf4368767cf904daef58d1fad09\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-rb17fm9u/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-rb17fm9u/repo\", \"--revision\", \"4b4ea64fdf8033926a0f6cf919bcc9e1d03ff540\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.03
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "1cc3f21c42e602802c04605ab8321f3f5887177b",
      "mutatedSha256": {
        "measure_c1.py": "911420b5e807cbcdfd4634c9b9e6f1449b8764bc9d5de648318ca59560d7d3a6",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "638011cdcd54caffa3fd5e2cd6816c3f942544d7",
      "committedMutationSha256": "911420b5e807cbcdfd4634c9b9e6f1449b8764bc9d5de648318ca59560d7d3a6",
      "mutated": {
        "exit": 1,
        "stdout": "",
        "stderr": "counter_selftest: {\"accepted\": 17, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-l0tse_9z/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-l0tse_9z/repo\", \"--revision\", \"6277478ac399caae83b57234318386e8c7995d20\"], \"errors\": [\"exit 0, expected 1\", \"accepted 17, expected 16\", \"failed rows [], expected ['drift-detection']\", \"target 'drift-detection' lacks problem 'anchor not in unit at base'\"], \"exit\": 0, \"expectedAccepted\": 16, \"expectedExit\": 1, \"output\": {\"accepted\": 17, \"claimVerdicts\": {\"HOLD\": 17, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"revision\": \"6277478ac399caae83b57234318386e8c7995d20\", \"total\": 17, \"units\": [{\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"drift-detection\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"fire-journal-codes\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"fleet-registry\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"free-read-verbs\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"ghp-subpath-spotcheck\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"keeper-timer-inert\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"kimi-subpath-audit\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"mirror-pitfalls\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"ops-automation\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"origin-repos\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"probe-delta-alerting\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"publish-channels\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"publish-queue\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"sitemap-orphan-audit\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"speedrun-pipeline\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"vault-properties\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"property-map\"}]}, \"passed\": false, \"stderr\": \"\", \"total\": 17}\n",
        "elapsedSeconds": 1.028
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "9b839d96caa3fcbf3289f50ba935df1bbba1ab29",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-5qydyhm9/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-5qydyhm9/repo\", \"--revision\", \"b4d180fb7e0f0899e18649dc31ab60250cc1002f\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-5qydyhm9/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-5qydyhm9/repo\", \"--revision\", \"b4d180fb7e0f0899e18649dc31ab60250cc1002f\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-5qydyhm9/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-5qydyhm9/repo\", \"--revision\", \"78bc3ca67d1398afc96bbe78b9be091c25ca3c91\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-5qydyhm9/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-5qydyhm9/repo\", \"--revision\", \"10495a9304407770509528b5ad97545b5d825df6\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-5qydyhm9/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-5qydyhm9/repo\", \"--revision\", \"22874e67159a74ea03162a65c91985f2f97b349a\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-5qydyhm9/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-5qydyhm9/repo\", \"--revision\", \"4efbf738bd11a3634089343ee7b6dac58541f0b1\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-5qydyhm9/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-5qydyhm9/repo\", \"--revision\", \"47f4df99dd802450def2c666364b6161fb7191a9\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.082
      },
      "verdict": "killed"
    },
    {
      "id": "C1-25",
      "script": "measure_c1.py",
      "check": "Claim cited after heading",
      "pattern": "f\"[{unit['unit']}:{claim['id']}]\" not in section",
      "replacement": "False",
      "expected": "survived",
      "expectationReason": "No selftest fixture invalidates this check.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-5qydyhm9/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-5qydyhm9/repo\", \"--revision\", \"b4d180fb7e0f0899e18649dc31ab60250cc1002f\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-5qydyhm9/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-5qydyhm9/repo\", \"--revision\", \"b4d180fb7e0f0899e18649dc31ab60250cc1002f\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-5qydyhm9/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-5qydyhm9/repo\", \"--revision\", \"78bc3ca67d1398afc96bbe78b9be091c25ca3c91\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-5qydyhm9/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-5qydyhm9/repo\", \"--revision\", \"10495a9304407770509528b5ad97545b5d825df6\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-5qydyhm9/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-5qydyhm9/repo\", \"--revision\", \"22874e67159a74ea03162a65c91985f2f97b349a\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-5qydyhm9/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-5qydyhm9/repo\", \"--revision\", \"4efbf738bd11a3634089343ee7b6dac58541f0b1\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-5qydyhm9/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-5qydyhm9/repo\", \"--revision\", \"47f4df99dd802450def2c666364b6161fb7191a9\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.082
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "9b839d96caa3fcbf3289f50ba935df1bbba1ab29",
      "mutatedSha256": {
        "measure_c1.py": "aee8e79ea50c5f1a7ca710bc9401520d091bbda45cb37aa73216f988d819876b",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "cea85857668aadf43f35b7f592236fbb30b367a6",
      "committedMutationSha256": "aee8e79ea50c5f1a7ca710bc9401520d091bbda45cb37aa73216f988d819876b",
      "mutated": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-v2n6wfp5/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-v2n6wfp5/repo\", \"--revision\", \"4961787ed31005ccb9b644cb13e9e2e49d36b03f\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-v2n6wfp5/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-v2n6wfp5/repo\", \"--revision\", \"4961787ed31005ccb9b644cb13e9e2e49d36b03f\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-v2n6wfp5/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-v2n6wfp5/repo\", \"--revision\", \"fae04cb9829637da686299779bcd447a2e2efdc0\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-v2n6wfp5/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-v2n6wfp5/repo\", \"--revision\", \"d331899394ec10ffaa0875454efc71b849f79b9b\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-v2n6wfp5/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-v2n6wfp5/repo\", \"--revision\", \"1cc9fd53b9277c144ccb08e86a3c310a6229f205\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-v2n6wfp5/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-v2n6wfp5/repo\", \"--revision\", \"f7cdaff7c465a2b1266fd9b587894f890f68927a\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-v2n6wfp5/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-v2n6wfp5/repo\", \"--revision\", \"a220d9904561938ef74514fc92b472418f3c20ff\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.243
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "918494186669f38dfb1af9c5b485d40c2dbb9a8c",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-zvflr144/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-zvflr144/repo\", \"--revision\", \"29db0aa242c6dfa12e32f05a94d7e564c341d15c\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-zvflr144/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-zvflr144/repo\", \"--revision\", \"29db0aa242c6dfa12e32f05a94d7e564c341d15c\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-zvflr144/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-zvflr144/repo\", \"--revision\", \"57afe1abeb2c1a97a412843dd89a9f379171bb4b\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-zvflr144/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-zvflr144/repo\", \"--revision\", \"59de35c02692c2f3377453768c79a12a9344f056\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-zvflr144/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-zvflr144/repo\", \"--revision\", \"d39067a384b9eb64b53b2336ff0cbcdfd141ba9e\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-zvflr144/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-zvflr144/repo\", \"--revision\", \"ec06bce00f1741f18627ce75fc3b1276eba0a83d\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-zvflr144/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-zvflr144/repo\", \"--revision\", \"b8ceb64e848df59acf2174806b8b3d7e2f84c8ce\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.33
      },
      "verdict": "survived"
    },
    {
      "id": "C1-26",
      "script": "measure_c1.py",
      "check": "STALE correction dispatch",
      "pattern": "verdict == \"STALE\"",
      "replacement": "False",
      "expected": "survived",
      "expectationReason": "No selftest fixture invalidates this check.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-zvflr144/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-zvflr144/repo\", \"--revision\", \"29db0aa242c6dfa12e32f05a94d7e564c341d15c\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-zvflr144/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-zvflr144/repo\", \"--revision\", \"29db0aa242c6dfa12e32f05a94d7e564c341d15c\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-zvflr144/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-zvflr144/repo\", \"--revision\", \"57afe1abeb2c1a97a412843dd89a9f379171bb4b\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-zvflr144/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-zvflr144/repo\", \"--revision\", \"59de35c02692c2f3377453768c79a12a9344f056\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-zvflr144/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-zvflr144/repo\", \"--revision\", \"d39067a384b9eb64b53b2336ff0cbcdfd141ba9e\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-zvflr144/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-zvflr144/repo\", \"--revision\", \"ec06bce00f1741f18627ce75fc3b1276eba0a83d\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-zvflr144/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-zvflr144/repo\", \"--revision\", \"b8ceb64e848df59acf2174806b8b3d7e2f84c8ce\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.33
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "918494186669f38dfb1af9c5b485d40c2dbb9a8c",
      "mutatedSha256": {
        "measure_c1.py": "b62798a0016352fa08a141caa6c54469fa6f0f969a1a833aa94db01a35e52855",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "8a78a59590fd3724312acb30121feb549d092c82",
      "committedMutationSha256": "b62798a0016352fa08a141caa6c54469fa6f0f969a1a833aa94db01a35e52855",
      "mutated": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-_zwcr14w/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-_zwcr14w/repo\", \"--revision\", \"da9b2ff1839f8309ea3d18bf1769057c158e6350\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-_zwcr14w/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-_zwcr14w/repo\", \"--revision\", \"da9b2ff1839f8309ea3d18bf1769057c158e6350\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-_zwcr14w/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-_zwcr14w/repo\", \"--revision\", \"0529fc2b6e0f09dd9c65541d81373f075878aae3\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-_zwcr14w/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-_zwcr14w/repo\", \"--revision\", \"6412f3cb3b02ceb7b26c8f9624286a3a39bcb9ec\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-_zwcr14w/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-_zwcr14w/repo\", \"--revision\", \"c53f96c5f1bd002f079cab9f4ead9594693ff344\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-_zwcr14w/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-_zwcr14w/repo\", \"--revision\", \"c15db523f8c8b0bcdcf682c57ee0a5a1e49a8495\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-_zwcr14w/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-_zwcr14w/repo\", \"--revision\", \"2a2708cebef14ac2f2363f0d838c22c4645e253d\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.177
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "027d719f21aeb3e5411a6ba1ffc37522f80e9c38",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-s6_s75f9/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-s6_s75f9/repo\", \"--revision\", \"213a64a2c41061ded35fadce97a0974becb43a14\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-s6_s75f9/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-s6_s75f9/repo\", \"--revision\", \"213a64a2c41061ded35fadce97a0974becb43a14\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-s6_s75f9/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-s6_s75f9/repo\", \"--revision\", \"f4a3c85ef1e6f770801743279fa7b37b0e3ae4b9\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-s6_s75f9/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-s6_s75f9/repo\", \"--revision\", \"423d55d13a992c90db3dcecde3c645aec969cbe3\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-s6_s75f9/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-s6_s75f9/repo\", \"--revision\", \"6c98f529716d85907d104bb4449e1f57573c6161\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-s6_s75f9/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-s6_s75f9/repo\", \"--revision\", \"795ec1c63cd6e56fb50d5fb96d70b041acbc1671\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-s6_s75f9/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-s6_s75f9/repo\", \"--revision\", \"5f792edb932c1e873790fa9f2d6ab883986678ab\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.209
      },
      "verdict": "survived"
    },
    {
      "id": "C1-27",
      "script": "measure_c1.py",
      "check": "Correction string type",
      "pattern": "not isinstance(correction, str)",
      "replacement": "False",
      "expected": "survived",
      "expectationReason": "No selftest fixture invalidates this check.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-s6_s75f9/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-s6_s75f9/repo\", \"--revision\", \"213a64a2c41061ded35fadce97a0974becb43a14\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-s6_s75f9/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-s6_s75f9/repo\", \"--revision\", \"213a64a2c41061ded35fadce97a0974becb43a14\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-s6_s75f9/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-s6_s75f9/repo\", \"--revision\", \"f4a3c85ef1e6f770801743279fa7b37b0e3ae4b9\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-s6_s75f9/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-s6_s75f9/repo\", \"--revision\", \"423d55d13a992c90db3dcecde3c645aec969cbe3\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-s6_s75f9/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-s6_s75f9/repo\", \"--revision\", \"6c98f529716d85907d104bb4449e1f57573c6161\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-s6_s75f9/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-s6_s75f9/repo\", \"--revision\", \"795ec1c63cd6e56fb50d5fb96d70b041acbc1671\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-s6_s75f9/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-s6_s75f9/repo\", \"--revision\", \"5f792edb932c1e873790fa9f2d6ab883986678ab\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.209
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "027d719f21aeb3e5411a6ba1ffc37522f80e9c38",
      "mutatedSha256": {
        "measure_c1.py": "d37d6c6ee6d46d37fa52371f6fbb20c0eb5e04f6ee8a195e4bcf1615c961620a",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "972d1de6641b462c6c95197cfb81b5b2cc1bd01c",
      "committedMutationSha256": "d37d6c6ee6d46d37fa52371f6fbb20c0eb5e04f6ee8a195e4bcf1615c961620a",
      "mutated": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-80k7h_ri/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-80k7h_ri/repo\", \"--revision\", \"27d3eb1ae168cd03d7cc46a43597eeb2fc295ce7\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-80k7h_ri/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-80k7h_ri/repo\", \"--revision\", \"27d3eb1ae168cd03d7cc46a43597eeb2fc295ce7\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-80k7h_ri/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-80k7h_ri/repo\", \"--revision\", \"33bc067f15af6bb335a841c3e7d7743029625cda\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-80k7h_ri/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-80k7h_ri/repo\", \"--revision\", \"1c848fd13aedda84c316026f3c78f74cea90d410\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-80k7h_ri/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-80k7h_ri/repo\", \"--revision\", \"90e44a8637899c4c6fb0deab68bca6c3808c9390\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-80k7h_ri/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-80k7h_ri/repo\", \"--revision\", \"9d5ac20772e69e9cade6cf4d353e97d46242cf36\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-80k7h_ri/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-80k7h_ri/repo\", \"--revision\", \"364260bad7b7809e9e709de94a4226a0e711db97\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.259
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "3f08a0fdffbfb5affee93d637dfbc6fc1efa56d1",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-568dkzi_/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-568dkzi_/repo\", \"--revision\", \"87c456d8235658830363981638687ee40b0a6394\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-568dkzi_/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-568dkzi_/repo\", \"--revision\", \"87c456d8235658830363981638687ee40b0a6394\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-568dkzi_/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-568dkzi_/repo\", \"--revision\", \"b35b90162d5c7f3da9d7026fea57a94816dd8b72\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-568dkzi_/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-568dkzi_/repo\", \"--revision\", \"51908efe865f47722a5ca4d9e2ee4224dc795d0e\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-568dkzi_/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-568dkzi_/repo\", \"--revision\", \"3f2046b02ed48206a61009d84b0a29ca5a280a12\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-568dkzi_/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-568dkzi_/repo\", \"--revision\", \"06dab98a60a3dbd6d881af5e1ae271d6bfcfce5b\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-568dkzi_/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-568dkzi_/repo\", \"--revision\", \"d6bc3b1cdc9e69c55848e3de9c049f98c5196388\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.396
      },
      "verdict": "survived"
    },
    {
      "id": "C1-28",
      "script": "measure_c1.py",
      "check": "Correction nonblank",
      "pattern": "not correction.strip()",
      "replacement": "False",
      "expected": "survived",
      "expectationReason": "No selftest fixture invalidates this check.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-568dkzi_/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-568dkzi_/repo\", \"--revision\", \"87c456d8235658830363981638687ee40b0a6394\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-568dkzi_/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-568dkzi_/repo\", \"--revision\", \"87c456d8235658830363981638687ee40b0a6394\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-568dkzi_/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-568dkzi_/repo\", \"--revision\", \"b35b90162d5c7f3da9d7026fea57a94816dd8b72\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-568dkzi_/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-568dkzi_/repo\", \"--revision\", \"51908efe865f47722a5ca4d9e2ee4224dc795d0e\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-568dkzi_/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-568dkzi_/repo\", \"--revision\", \"3f2046b02ed48206a61009d84b0a29ca5a280a12\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-568dkzi_/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-568dkzi_/repo\", \"--revision\", \"06dab98a60a3dbd6d881af5e1ae271d6bfcfce5b\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-568dkzi_/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-568dkzi_/repo\", \"--revision\", \"d6bc3b1cdc9e69c55848e3de9c049f98c5196388\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.396
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "3f08a0fdffbfb5affee93d637dfbc6fc1efa56d1",
      "mutatedSha256": {
        "measure_c1.py": "28860cd7d4e5d1c79cbfbd28db6123a845ea7fbdf10802cd82c03b4098966f5d",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "661712c318b912e20058b392eea3466b10eba274",
      "committedMutationSha256": "28860cd7d4e5d1c79cbfbd28db6123a845ea7fbdf10802cd82c03b4098966f5d",
      "mutated": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-hc32g3tr/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-hc32g3tr/repo\", \"--revision\", \"0e26751a6f0a91d4af24953533b638ff3422c9e3\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-hc32g3tr/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-hc32g3tr/repo\", \"--revision\", \"0e26751a6f0a91d4af24953533b638ff3422c9e3\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-hc32g3tr/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-hc32g3tr/repo\", \"--revision\", \"bc66fad51852322f2fe58ea47f465a7872d22b81\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-hc32g3tr/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-hc32g3tr/repo\", \"--revision\", \"a32264530d9bf8acc2c668c624e320e1c0e65fa6\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-hc32g3tr/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-hc32g3tr/repo\", \"--revision\", \"82646705ed8af6a95fae8614b8deb43c2670b3f6\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-hc32g3tr/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-hc32g3tr/repo\", \"--revision\", \"b178116e9ec6741b7913494acbca4495febe2977\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-hc32g3tr/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-hc32g3tr/repo\", \"--revision\", \"6c313e92a3146c7ad45eccd45954ff30eb5898bc\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.277
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "0d316aa145fcaa6ce6e6cec85eb9d7530d78a7c0",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-58lvc5_y/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-58lvc5_y/repo\", \"--revision\", \"2abdae763b2df794c75efda557c1d0eb0915b4b9\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-58lvc5_y/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-58lvc5_y/repo\", \"--revision\", \"2abdae763b2df794c75efda557c1d0eb0915b4b9\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-58lvc5_y/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-58lvc5_y/repo\", \"--revision\", \"2f06b93a787b3cf7036acad6e1fcbc3598b7e364\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-58lvc5_y/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-58lvc5_y/repo\", \"--revision\", \"aa00b4d128d50afb98b6e8b331e730b083534605\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-58lvc5_y/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-58lvc5_y/repo\", \"--revision\", \"015e3f4a8a2f908c6936ab71357acb5583152a85\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-58lvc5_y/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-58lvc5_y/repo\", \"--revision\", \"0143a4a5c7712e3d9689d928d1bffb9354575b65\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-58lvc5_y/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-58lvc5_y/repo\", \"--revision\", \"d7f7234054f798c5f5dad335c4f9c7fe47277d35\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.26
      },
      "verdict": "survived"
    },
    {
      "id": "C1-29",
      "script": "measure_c1.py",
      "check": "Correction in appended section",
      "pattern": "correction not in section",
      "replacement": "False",
      "expected": "survived",
      "expectationReason": "No selftest fixture invalidates this check.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-58lvc5_y/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-58lvc5_y/repo\", \"--revision\", \"2abdae763b2df794c75efda557c1d0eb0915b4b9\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-58lvc5_y/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-58lvc5_y/repo\", \"--revision\", \"2abdae763b2df794c75efda557c1d0eb0915b4b9\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-58lvc5_y/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-58lvc5_y/repo\", \"--revision\", \"2f06b93a787b3cf7036acad6e1fcbc3598b7e364\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-58lvc5_y/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-58lvc5_y/repo\", \"--revision\", \"aa00b4d128d50afb98b6e8b331e730b083534605\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-58lvc5_y/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-58lvc5_y/repo\", \"--revision\", \"015e3f4a8a2f908c6936ab71357acb5583152a85\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-58lvc5_y/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-58lvc5_y/repo\", \"--revision\", \"0143a4a5c7712e3d9689d928d1bffb9354575b65\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-58lvc5_y/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-58lvc5_y/repo\", \"--revision\", \"d7f7234054f798c5f5dad335c4f9c7fe47277d35\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.26
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "0d316aa145fcaa6ce6e6cec85eb9d7530d78a7c0",
      "mutatedSha256": {
        "measure_c1.py": "24071c6c09aa59cc5a6eb4c4824ddba8f002e26b07848fed5298c03138aaab96",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "f6e5766606f1f5a5630ea980db68b3cba2115624",
      "committedMutationSha256": "24071c6c09aa59cc5a6eb4c4824ddba8f002e26b07848fed5298c03138aaab96",
      "mutated": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-nbzo49nn/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-nbzo49nn/repo\", \"--revision\", \"ae5ca7801b74b7c9309354b5f2828611a3e04dc7\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-nbzo49nn/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-nbzo49nn/repo\", \"--revision\", \"ae5ca7801b74b7c9309354b5f2828611a3e04dc7\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-nbzo49nn/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-nbzo49nn/repo\", \"--revision\", \"828b25181f746e0f932e82283ab905408c905066\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-nbzo49nn/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-nbzo49nn/repo\", \"--revision\", \"db82fdf1fcf01343cbcafd71ffb8527b26db7553\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-nbzo49nn/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-nbzo49nn/repo\", \"--revision\", \"ac9377ddc00d4000c9000ffea9a2f0c7bdc9cb59\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-nbzo49nn/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-nbzo49nn/repo\", \"--revision\", \"143b25c55f4d2e5a08d0dc2f292178a127503105\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-nbzo49nn/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-nbzo49nn/repo\", \"--revision\", \"3d3b4a032c7ad0da1724aa48d459386117e4b3ca\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.202
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "bae87ee302b838bd7916abfd8533d86023b01548",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xg4rwshd/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xg4rwshd/repo\", \"--revision\", \"4abebe678177b5e5c64bfb0eb6da5953cdf8a081\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xg4rwshd/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xg4rwshd/repo\", \"--revision\", \"4abebe678177b5e5c64bfb0eb6da5953cdf8a081\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xg4rwshd/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xg4rwshd/repo\", \"--revision\", \"5109e08fa338e3299c0d446c5406315b6d3df7ba\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xg4rwshd/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xg4rwshd/repo\", \"--revision\", \"5de1b1680c3f318cb025436fc6aefe0ae32ac3d1\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xg4rwshd/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xg4rwshd/repo\", \"--revision\", \"f57366e0d6469a529807a2f3dc5424ed4dd7482e\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xg4rwshd/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xg4rwshd/repo\", \"--revision\", \"415a938248b65f9fa52f9ec9cd2bc1b90390245f\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xg4rwshd/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xg4rwshd/repo\", \"--revision\", \"e2c3bbf90615e0ca3e585641c5a2be8e3a4ec84d\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.192
      },
      "verdict": "survived"
    },
    {
      "id": "C1-30",
      "script": "measure_c1.py",
      "check": "UNVERIFIABLE reason dispatch",
      "pattern": "verdict == \"UNVERIFIABLE\"",
      "replacement": "False",
      "expected": "survived",
      "expectationReason": "No selftest fixture invalidates this check.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xg4rwshd/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xg4rwshd/repo\", \"--revision\", \"4abebe678177b5e5c64bfb0eb6da5953cdf8a081\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xg4rwshd/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xg4rwshd/repo\", \"--revision\", \"4abebe678177b5e5c64bfb0eb6da5953cdf8a081\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xg4rwshd/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xg4rwshd/repo\", \"--revision\", \"5109e08fa338e3299c0d446c5406315b6d3df7ba\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xg4rwshd/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xg4rwshd/repo\", \"--revision\", \"5de1b1680c3f318cb025436fc6aefe0ae32ac3d1\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xg4rwshd/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xg4rwshd/repo\", \"--revision\", \"f57366e0d6469a529807a2f3dc5424ed4dd7482e\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xg4rwshd/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xg4rwshd/repo\", \"--revision\", \"415a938248b65f9fa52f9ec9cd2bc1b90390245f\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xg4rwshd/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xg4rwshd/repo\", \"--revision\", \"e2c3bbf90615e0ca3e585641c5a2be8e3a4ec84d\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.192
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "bae87ee302b838bd7916abfd8533d86023b01548",
      "mutatedSha256": {
        "measure_c1.py": "3be799e9818b274752fc6913cb466b36fcb0356e08e6224fc0da2990c5560ee5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "b302060f8aa7ccdd6836d76fadb4192253523e53",
      "committedMutationSha256": "3be799e9818b274752fc6913cb466b36fcb0356e08e6224fc0da2990c5560ee5",
      "mutated": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-17bv1e7e/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-17bv1e7e/repo\", \"--revision\", \"4e73ea508c86149873c0626b74b02de9915124d6\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-17bv1e7e/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-17bv1e7e/repo\", \"--revision\", \"4e73ea508c86149873c0626b74b02de9915124d6\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-17bv1e7e/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-17bv1e7e/repo\", \"--revision\", \"2b1e109fe9d266c0e1b7916d57914b414d472688\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-17bv1e7e/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-17bv1e7e/repo\", \"--revision\", \"fe2f44191dbbed712d96e14193fb17eeee94dbbe\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-17bv1e7e/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-17bv1e7e/repo\", \"--revision\", \"25f7602519f60f12b45ae910669fd838d9db7f51\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-17bv1e7e/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-17bv1e7e/repo\", \"--revision\", \"335c6123302ec9a9f1e10b1581a67812bae72bd2\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-17bv1e7e/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-17bv1e7e/repo\", \"--revision\", \"a63c3f409fdca4334f0906c87b09594f9d79be4e\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.184
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "d482abd8cfb8d7f1f61b48ceee10932595d92079",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xfbkfpuv/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xfbkfpuv/repo\", \"--revision\", \"350d312d28fe69fc731fd1bec5c82c4e160ac1a3\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xfbkfpuv/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xfbkfpuv/repo\", \"--revision\", \"350d312d28fe69fc731fd1bec5c82c4e160ac1a3\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xfbkfpuv/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xfbkfpuv/repo\", \"--revision\", \"adb6deee61e9f256631c46247c3f5feba9942ecb\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xfbkfpuv/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xfbkfpuv/repo\", \"--revision\", \"d9d59d44c984ac24580ca35a1ae3aeb14b70b997\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xfbkfpuv/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xfbkfpuv/repo\", \"--revision\", \"250338ed1fbcca67b8e51e89be6b1d409831c8ad\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xfbkfpuv/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xfbkfpuv/repo\", \"--revision\", \"b3470cbcd604a1e61c8f10bccad8187e61cce094\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xfbkfpuv/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xfbkfpuv/repo\", \"--revision\", \"464301ca8d6828e2a7ef75a819b8f04157c21326\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.225
      },
      "verdict": "survived"
    },
    {
      "id": "C1-31",
      "script": "measure_c1.py",
      "check": "UNVERIFIABLE reason nonblank",
      "pattern": "not str(claim.get(\"reason\", \"\")).strip()",
      "replacement": "False",
      "expected": "survived",
      "expectationReason": "No selftest fixture invalidates this check.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xfbkfpuv/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xfbkfpuv/repo\", \"--revision\", \"350d312d28fe69fc731fd1bec5c82c4e160ac1a3\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xfbkfpuv/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xfbkfpuv/repo\", \"--revision\", \"350d312d28fe69fc731fd1bec5c82c4e160ac1a3\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xfbkfpuv/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xfbkfpuv/repo\", \"--revision\", \"adb6deee61e9f256631c46247c3f5feba9942ecb\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xfbkfpuv/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xfbkfpuv/repo\", \"--revision\", \"d9d59d44c984ac24580ca35a1ae3aeb14b70b997\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xfbkfpuv/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xfbkfpuv/repo\", \"--revision\", \"250338ed1fbcca67b8e51e89be6b1d409831c8ad\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xfbkfpuv/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xfbkfpuv/repo\", \"--revision\", \"b3470cbcd604a1e61c8f10bccad8187e61cce094\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xfbkfpuv/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xfbkfpuv/repo\", \"--revision\", \"464301ca8d6828e2a7ef75a819b8f04157c21326\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.225
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "d482abd8cfb8d7f1f61b48ceee10932595d92079",
      "mutatedSha256": {
        "measure_c1.py": "210d84a5c6a05056ad8f26a83ac1c6de9898cbfcf74df1d0ac507d335c3eab05",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "aca54e75e4f290d667957b172c05fc7bc8886d59",
      "committedMutationSha256": "210d84a5c6a05056ad8f26a83ac1c6de9898cbfcf74df1d0ac507d335c3eab05",
      "mutated": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-oavdkvaj/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-oavdkvaj/repo\", \"--revision\", \"4c4987129f160b660ed779d13f8c8c4ff44a1433\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-oavdkvaj/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-oavdkvaj/repo\", \"--revision\", \"4c4987129f160b660ed779d13f8c8c4ff44a1433\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-oavdkvaj/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-oavdkvaj/repo\", \"--revision\", \"7fe94ef60373916ac2135c19a9d02f5a6f5940e4\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-oavdkvaj/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-oavdkvaj/repo\", \"--revision\", \"866969aeea41e672cd930765df83fcf467456526\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-oavdkvaj/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-oavdkvaj/repo\", \"--revision\", \"72bd11c253b9683c6be48040adf1c17f7791e4bb\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-oavdkvaj/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-oavdkvaj/repo\", \"--revision\", \"3fb7bdc4850b0ad7bae5c49856cfd8b157108fb3\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-oavdkvaj/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-oavdkvaj/repo\", \"--revision\", \"75ed183332cc61c0e3c63c21da6982519ea165b0\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.247
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "1681d362152d4505637768d9f40f5b84cb81ef51",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-l75vtty6/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-l75vtty6/repo\", \"--revision\", \"6a5f9ecd001f2e60262e96eacad2c674b1f848e0\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-l75vtty6/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-l75vtty6/repo\", \"--revision\", \"6a5f9ecd001f2e60262e96eacad2c674b1f848e0\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-l75vtty6/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-l75vtty6/repo\", \"--revision\", \"b87457ab500dfedd81131467dd712cdb858d81d4\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-l75vtty6/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-l75vtty6/repo\", \"--revision\", \"6fbd456a4d452be45f1e5f93df57978e18969b11\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-l75vtty6/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-l75vtty6/repo\", \"--revision\", \"4b2e7826eeccd42d149127078d83bf3bd2a4f7d3\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-l75vtty6/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-l75vtty6/repo\", \"--revision\", \"c3fb60e07687e9a4a4873f4e333bbbcae2dc2eb8\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-l75vtty6/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-l75vtty6/repo\", \"--revision\", \"e43596b479bd2bd3abd2e17c513cf118fd70f6e6\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.154
      },
      "verdict": "survived"
    },
    {
      "id": "C1-32",
      "script": "measure_c1.py",
      "check": "At least one live-decided claim",
      "pattern": "verdicts[\"HOLD\"] + verdicts[\"STALE\"] == 0",
      "replacement": "False",
      "expected": "killed",
      "expectationReason": "All-UNVERIFIABLE fixture expects one rejected unit with the live-decision diagnostic.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-l75vtty6/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-l75vtty6/repo\", \"--revision\", \"6a5f9ecd001f2e60262e96eacad2c674b1f848e0\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-l75vtty6/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-l75vtty6/repo\", \"--revision\", \"6a5f9ecd001f2e60262e96eacad2c674b1f848e0\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-l75vtty6/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-l75vtty6/repo\", \"--revision\", \"b87457ab500dfedd81131467dd712cdb858d81d4\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-l75vtty6/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-l75vtty6/repo\", \"--revision\", \"6fbd456a4d452be45f1e5f93df57978e18969b11\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-l75vtty6/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-l75vtty6/repo\", \"--revision\", \"4b2e7826eeccd42d149127078d83bf3bd2a4f7d3\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-l75vtty6/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-l75vtty6/repo\", \"--revision\", \"c3fb60e07687e9a4a4873f4e333bbbcae2dc2eb8\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-l75vtty6/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-l75vtty6/repo\", \"--revision\", \"e43596b479bd2bd3abd2e17c513cf118fd70f6e6\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.154
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "1681d362152d4505637768d9f40f5b84cb81ef51",
      "mutatedSha256": {
        "measure_c1.py": "f03a73b8eccfef62e92944341119c735de5682dcab47d931f26e4ac1ffcd1658",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "9989aa3d2650b36488ab2003e57b059938f772eb",
      "committedMutationSha256": "f03a73b8eccfef62e92944341119c735de5682dcab47d931f26e4ac1ffcd1658",
      "mutated": {
        "exit": 1,
        "stdout": "",
        "stderr": "counter_selftest: {\"accepted\": 17, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-eruab_rm/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-eruab_rm/repo\", \"--revision\", \"07f8efe7120a2d0283023f147c3d33306840dd0c\"], \"errors\": [\"exit 0, expected 1\", \"accepted 17, expected 16\", \"failed rows [], expected ['fleet-registry']\", \"target 'fleet-registry' lacks problem 'no claim decided live'\"], \"exit\": 0, \"expectedAccepted\": 16, \"expectedExit\": 1, \"output\": {\"accepted\": 17, \"claimVerdicts\": {\"HOLD\": 16, \"STALE\": 0, \"UNVERIFIABLE\": 1}, \"revision\": \"07f8efe7120a2d0283023f147c3d33306840dd0c\", \"total\": 17, \"units\": [{\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"drift-detection\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"fire-journal-codes\"}, {\"claims\": {\"HOLD\": 0, \"STALE\": 0, \"UNVERIFIABLE\": 1}, \"pass\": true, \"problems\": [], \"unit\": \"fleet-registry\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"free-read-verbs\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"ghp-subpath-spotcheck\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"keeper-timer-inert\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"kimi-subpath-audit\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"mirror-pitfalls\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"ops-automation\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"origin-repos\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"probe-delta-alerting\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"publish-channels\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"publish-queue\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"sitemap-orphan-audit\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"speedrun-pipeline\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"vault-properties\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"property-map\"}]}, \"passed\": false, \"stderr\": \"\", \"total\": 17}\n",
        "elapsedSeconds": 1.679
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "5d3f4d36b304b3bd1e4532efc41dfc15a0c6fdef",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-8xt85hxl/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-8xt85hxl/repo\", \"--revision\", \"2b46030fb07a33123b399daa00ab93eb0f4158ff\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-8xt85hxl/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-8xt85hxl/repo\", \"--revision\", \"2b46030fb07a33123b399daa00ab93eb0f4158ff\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-8xt85hxl/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-8xt85hxl/repo\", \"--revision\", \"f4655314476bd3b05d141464ed209c9a835d704e\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-8xt85hxl/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-8xt85hxl/repo\", \"--revision\", \"7ea9f1a14b3497e78a9be27a13791ab2e0acecba\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-8xt85hxl/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-8xt85hxl/repo\", \"--revision\", \"e956ff7a3ca4161f38e456c403ce0bf91a4976af\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-8xt85hxl/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-8xt85hxl/repo\", \"--revision\", \"a298c2ca712a87f5f3c8ef680ac61bab143383fe\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-8xt85hxl/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-8xt85hxl/repo\", \"--revision\", \"00eb679a588622016b86b93ad6139489b1e8b52c\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.195
      },
      "verdict": "killed"
    },
    {
      "id": "C1-33",
      "script": "measure_c1.py",
      "check": "Frozen population guard dispatch",
      "pattern": "population_raw is not None",
      "replacement": "False",
      "expected": "survived",
      "expectationReason": "No selftest fixture invalidates this check.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-8xt85hxl/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-8xt85hxl/repo\", \"--revision\", \"2b46030fb07a33123b399daa00ab93eb0f4158ff\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-8xt85hxl/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-8xt85hxl/repo\", \"--revision\", \"2b46030fb07a33123b399daa00ab93eb0f4158ff\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-8xt85hxl/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-8xt85hxl/repo\", \"--revision\", \"f4655314476bd3b05d141464ed209c9a835d704e\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-8xt85hxl/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-8xt85hxl/repo\", \"--revision\", \"7ea9f1a14b3497e78a9be27a13791ab2e0acecba\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-8xt85hxl/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-8xt85hxl/repo\", \"--revision\", \"e956ff7a3ca4161f38e456c403ce0bf91a4976af\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-8xt85hxl/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-8xt85hxl/repo\", \"--revision\", \"a298c2ca712a87f5f3c8ef680ac61bab143383fe\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-8xt85hxl/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-8xt85hxl/repo\", \"--revision\", \"00eb679a588622016b86b93ad6139489b1e8b52c\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.195
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "5d3f4d36b304b3bd1e4532efc41dfc15a0c6fdef",
      "mutatedSha256": {
        "measure_c1.py": "3adf6a11f8e2e87d6dcbb890d025a8641b44474fdff6751dbb795fe6c409532b",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "44639111ecf8d7692684a464c0bb0e6848fd7b22",
      "committedMutationSha256": "3adf6a11f8e2e87d6dcbb890d025a8641b44474fdff6751dbb795fe6c409532b",
      "mutated": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-dwq_j9gv/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-dwq_j9gv/repo\", \"--revision\", \"18e024d5af09f068770b0d44f132d4087be22d9a\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-dwq_j9gv/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-dwq_j9gv/repo\", \"--revision\", \"18e024d5af09f068770b0d44f132d4087be22d9a\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-dwq_j9gv/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-dwq_j9gv/repo\", \"--revision\", \"de18e4318639df8d49a44c71a762530590f157b8\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-dwq_j9gv/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-dwq_j9gv/repo\", \"--revision\", \"2cf9564498cbca26e7ec9d3982dd05f3c22217d1\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-dwq_j9gv/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-dwq_j9gv/repo\", \"--revision\", \"9196fe91202ea83e5fc0d50ad2432d117fdce1cd\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-dwq_j9gv/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-dwq_j9gv/repo\", \"--revision\", \"238ca0ded95768b4e021db33d33662d0ac5ae91e\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-dwq_j9gv/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-dwq_j9gv/repo\", \"--revision\", \"36df480e0340391985b5e00244c8c274196bffc7\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.144
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "40720a3516eb035249d3a4e67b296aa4f84aae94",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-2m8f1ydg/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-2m8f1ydg/repo\", \"--revision\", \"1a1a33a2ffb1983010df6caa3eb254386d4a2393\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-2m8f1ydg/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-2m8f1ydg/repo\", \"--revision\", \"1a1a33a2ffb1983010df6caa3eb254386d4a2393\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-2m8f1ydg/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-2m8f1ydg/repo\", \"--revision\", \"4dc0fb73b1dd7e984f4df3880e4ac78a8419a65a\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-2m8f1ydg/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-2m8f1ydg/repo\", \"--revision\", \"bcd4b03f087d0708d0114176f7aedcf569dcf5cb\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-2m8f1ydg/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-2m8f1ydg/repo\", \"--revision\", \"f1c0fc58951b9515a19ab98cc9294ec0c2e59fc8\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-2m8f1ydg/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-2m8f1ydg/repo\", \"--revision\", \"b75a10713f3d77ad62ee9860cd5fb82380483097\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-2m8f1ydg/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-2m8f1ydg/repo\", \"--revision\", \"03245a465abeced32ed46c664fef388f5746b840\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.138
      },
      "verdict": "survived"
    },
    {
      "id": "C1-34",
      "script": "measure_c1.py",
      "check": "Frozen population digest",
      "pattern": "hashlib.sha256(population_raw.encode(\"utf-8\")).hexdigest() != POPULATION_SHA256",
      "replacement": "False",
      "expected": "survived",
      "expectationReason": "No selftest fixture invalidates this check.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-2m8f1ydg/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-2m8f1ydg/repo\", \"--revision\", \"1a1a33a2ffb1983010df6caa3eb254386d4a2393\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-2m8f1ydg/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-2m8f1ydg/repo\", \"--revision\", \"1a1a33a2ffb1983010df6caa3eb254386d4a2393\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-2m8f1ydg/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-2m8f1ydg/repo\", \"--revision\", \"4dc0fb73b1dd7e984f4df3880e4ac78a8419a65a\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-2m8f1ydg/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-2m8f1ydg/repo\", \"--revision\", \"bcd4b03f087d0708d0114176f7aedcf569dcf5cb\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-2m8f1ydg/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-2m8f1ydg/repo\", \"--revision\", \"f1c0fc58951b9515a19ab98cc9294ec0c2e59fc8\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-2m8f1ydg/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-2m8f1ydg/repo\", \"--revision\", \"b75a10713f3d77ad62ee9860cd5fb82380483097\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-2m8f1ydg/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-2m8f1ydg/repo\", \"--revision\", \"03245a465abeced32ed46c664fef388f5746b840\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.138
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "40720a3516eb035249d3a4e67b296aa4f84aae94",
      "mutatedSha256": {
        "measure_c1.py": "3ed8765cb4b12f110034bff4df7417a9233042841f9cc9fcd4eb9927efdce410",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "f65171e6e9e80f295de166951383df28128a5a6a",
      "committedMutationSha256": "3ed8765cb4b12f110034bff4df7417a9233042841f9cc9fcd4eb9927efdce410",
      "mutated": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-c3pwlu_7/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-c3pwlu_7/repo\", \"--revision\", \"a03a5f9a67dc05a0b00d15d7538b3e673d2c82e4\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-c3pwlu_7/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-c3pwlu_7/repo\", \"--revision\", \"a03a5f9a67dc05a0b00d15d7538b3e673d2c82e4\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-c3pwlu_7/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-c3pwlu_7/repo\", \"--revision\", \"46d8932920a792ac0de4597994d88c6c90d5b7d0\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-c3pwlu_7/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-c3pwlu_7/repo\", \"--revision\", \"4aacacb1b496a117f4775cf4f0027ec206b1b32e\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-c3pwlu_7/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-c3pwlu_7/repo\", \"--revision\", \"0366f7b2871fa92e7786f571aead9338d0574496\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-c3pwlu_7/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-c3pwlu_7/repo\", \"--revision\", \"a7f0c20b89df14d775c8b86ad36fb5d8f20f96ab\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-c3pwlu_7/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-c3pwlu_7/repo\", \"--revision\", \"eb51de0a66f95a9380ab7c2af62268896a5b57a0\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.183
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "22cbed3a4e09214cafba444e2fd6172da3100ca9",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-hcb_t465/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-hcb_t465/repo\", \"--revision\", \"9e7aec2198c2daddb560aa61c04afbc9a3a511a6\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-hcb_t465/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-hcb_t465/repo\", \"--revision\", \"9e7aec2198c2daddb560aa61c04afbc9a3a511a6\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-hcb_t465/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-hcb_t465/repo\", \"--revision\", \"f34fe864bc7cf9c86682b503a391dd4ac3f1566e\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-hcb_t465/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-hcb_t465/repo\", \"--revision\", \"14d0f6dbccc562d75c24c2304ccfcc04f12455a9\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-hcb_t465/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-hcb_t465/repo\", \"--revision\", \"20f129c667c26ad1acae2176a85fe7e8bf1e5c2c\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-hcb_t465/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-hcb_t465/repo\", \"--revision\", \"3a21018782c6f9e4f0c048d99f11c3efb431448f\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-hcb_t465/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-hcb_t465/repo\", \"--revision\", \"7a9419cca51820ab252f3fe1984400f160401c57\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.264
      },
      "verdict": "survived"
    },
    {
      "id": "C1-35",
      "script": "measure_c1.py",
      "check": "Revision resolves to a commit",
      "pattern": "resolved.returncode != 0",
      "replacement": "False",
      "expected": "survived",
      "expectationReason": "No selftest fixture invalidates this check.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-hcb_t465/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-hcb_t465/repo\", \"--revision\", \"9e7aec2198c2daddb560aa61c04afbc9a3a511a6\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-hcb_t465/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-hcb_t465/repo\", \"--revision\", \"9e7aec2198c2daddb560aa61c04afbc9a3a511a6\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-hcb_t465/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-hcb_t465/repo\", \"--revision\", \"f34fe864bc7cf9c86682b503a391dd4ac3f1566e\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-hcb_t465/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-hcb_t465/repo\", \"--revision\", \"14d0f6dbccc562d75c24c2304ccfcc04f12455a9\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-hcb_t465/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-hcb_t465/repo\", \"--revision\", \"20f129c667c26ad1acae2176a85fe7e8bf1e5c2c\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-hcb_t465/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-hcb_t465/repo\", \"--revision\", \"3a21018782c6f9e4f0c048d99f11c3efb431448f\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-hcb_t465/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-hcb_t465/repo\", \"--revision\", \"7a9419cca51820ab252f3fe1984400f160401c57\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.264
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "22cbed3a4e09214cafba444e2fd6172da3100ca9",
      "mutatedSha256": {
        "measure_c1.py": "b1876666fc5f4c3aef3684f6adc7db8d0e8d02acc123caaf97fee91d85bc11e7",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "7d550f2be1b429933deb09c08ba71aff55b06ee4",
      "committedMutationSha256": "b1876666fc5f4c3aef3684f6adc7db8d0e8d02acc123caaf97fee91d85bc11e7",
      "mutated": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-hcrxo_1u/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-hcrxo_1u/repo\", \"--revision\", \"58a3312c27c1291c30f6a6965cc1f7de3344f2e2\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-hcrxo_1u/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-hcrxo_1u/repo\", \"--revision\", \"58a3312c27c1291c30f6a6965cc1f7de3344f2e2\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-hcrxo_1u/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-hcrxo_1u/repo\", \"--revision\", \"a1707981ec33efa65bf3646aae6a3adb4095cbb7\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-hcrxo_1u/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-hcrxo_1u/repo\", \"--revision\", \"4e0ce355a14d7fef7e4208d426101bde1763ee0f\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-hcrxo_1u/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-hcrxo_1u/repo\", \"--revision\", \"d684d91b82105979b12497255086207dd180138e\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-hcrxo_1u/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-hcrxo_1u/repo\", \"--revision\", \"62e715ba8f7f1f620557efc05e4fc711ec6a29a2\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-hcrxo_1u/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-hcrxo_1u/repo\", \"--revision\", \"f1daa82fdb532dbfb1c94bccb5ad552510f15816\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.098
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "981dac2ab0f6a85867daebb696e14bbb1631dc52",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-21888xek/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-21888xek/repo\", \"--revision\", \"7b36d8d4a42bf5c9c4a47b569f72fbf1644c76fc\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-21888xek/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-21888xek/repo\", \"--revision\", \"7b36d8d4a42bf5c9c4a47b569f72fbf1644c76fc\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-21888xek/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-21888xek/repo\", \"--revision\", \"643a7b50d17025e524b166a2e2747af1098586aa\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-21888xek/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-21888xek/repo\", \"--revision\", \"f9cb8b84dda91f489a96f33b42738041eca1e93a\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-21888xek/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-21888xek/repo\", \"--revision\", \"7e9662fa31bda7e8212e340e4b9f72109441c844\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-21888xek/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-21888xek/repo\", \"--revision\", \"48acf15beec27a10732c17468aef0bf9b3076167\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-21888xek/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-21888xek/repo\", \"--revision\", \"a82b8c705691cf9a6da760e157fe32780c034e2a\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.062
      },
      "verdict": "survived"
    },
    {
      "id": "C1-36",
      "script": "measure_c1.py",
      "check": "Population readable",
      "pattern": "population_raw is None",
      "replacement": "False",
      "expected": "survived",
      "expectationReason": "No selftest fixture invalidates this check.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-21888xek/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-21888xek/repo\", \"--revision\", \"7b36d8d4a42bf5c9c4a47b569f72fbf1644c76fc\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-21888xek/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-21888xek/repo\", \"--revision\", \"7b36d8d4a42bf5c9c4a47b569f72fbf1644c76fc\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-21888xek/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-21888xek/repo\", \"--revision\", \"643a7b50d17025e524b166a2e2747af1098586aa\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-21888xek/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-21888xek/repo\", \"--revision\", \"f9cb8b84dda91f489a96f33b42738041eca1e93a\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-21888xek/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-21888xek/repo\", \"--revision\", \"7e9662fa31bda7e8212e340e4b9f72109441c844\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-21888xek/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-21888xek/repo\", \"--revision\", \"48acf15beec27a10732c17468aef0bf9b3076167\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-21888xek/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-21888xek/repo\", \"--revision\", \"a82b8c705691cf9a6da760e157fe32780c034e2a\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.062
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "981dac2ab0f6a85867daebb696e14bbb1631dc52",
      "mutatedSha256": {
        "measure_c1.py": "fcc08f6a44b7e64ea082049b49c7ac791a2b3a8f8800283ad404fc5a7cacdd35",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "3dd95cb315de83e66b4b8b9c4f22bcce48fbc7af",
      "committedMutationSha256": "fcc08f6a44b7e64ea082049b49c7ac791a2b3a8f8800283ad404fc5a7cacdd35",
      "mutated": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-zuv672in/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-zuv672in/repo\", \"--revision\", \"1f3a6fa24bf388ebf00f5bbebc4e3973ba5cfed5\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-zuv672in/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-zuv672in/repo\", \"--revision\", \"1f3a6fa24bf388ebf00f5bbebc4e3973ba5cfed5\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-zuv672in/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-zuv672in/repo\", \"--revision\", \"5a2da221164e3fe6f8e61e865f3ef8388029855a\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-zuv672in/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-zuv672in/repo\", \"--revision\", \"eb67accbe816bf2c57f213bbaa7c2b584bb9a9e4\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-zuv672in/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-zuv672in/repo\", \"--revision\", \"46d04c9a86c1225ffb1f9d858bd4a6e95b479570\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-zuv672in/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-zuv672in/repo\", \"--revision\", \"4b268a874c7ee96e569adf077a2505932a7804eb\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-zuv672in/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-zuv672in/repo\", \"--revision\", \"27c6cf4f89b8ef6ea71eadee1e1c5e4cb6da902f\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.06
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "850c921347d0072145c15e60c45fc6aec719d7e1",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-82p5khuh/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-82p5khuh/repo\", \"--revision\", \"1e2e60f4ad2b1df61249c4ace79516caf9428512\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-82p5khuh/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-82p5khuh/repo\", \"--revision\", \"1e2e60f4ad2b1df61249c4ace79516caf9428512\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-82p5khuh/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-82p5khuh/repo\", \"--revision\", \"af1980b6f3e36e3db71c2b3f18dcc82ecda0304e\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-82p5khuh/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-82p5khuh/repo\", \"--revision\", \"22a9c589c89b44f72825625ec4ac7ffd5c5fe3ff\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-82p5khuh/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-82p5khuh/repo\", \"--revision\", \"0b6ef34ef137fe0237488fc840825135588a646e\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-82p5khuh/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-82p5khuh/repo\", \"--revision\", \"2b2a831a844802d083fbf438b0e21710ac9d7f16\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-82p5khuh/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-82p5khuh/repo\", \"--revision\", \"ae0314ada4c1d5269fe9d3d0fe432dcc55726fda\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.055
      },
      "verdict": "survived"
    },
    {
      "id": "C1-37",
      "script": "measure_c1.py",
      "check": "Per-unit acceptance uses problems",
      "pattern": "not problems",
      "replacement": "True",
      "expected": "killed",
      "expectationReason": "Invalid-anchor fixture must mark the targeted unit failed and decrement accepted.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-82p5khuh/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-82p5khuh/repo\", \"--revision\", \"1e2e60f4ad2b1df61249c4ace79516caf9428512\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-82p5khuh/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-82p5khuh/repo\", \"--revision\", \"1e2e60f4ad2b1df61249c4ace79516caf9428512\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-82p5khuh/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-82p5khuh/repo\", \"--revision\", \"af1980b6f3e36e3db71c2b3f18dcc82ecda0304e\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-82p5khuh/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-82p5khuh/repo\", \"--revision\", \"22a9c589c89b44f72825625ec4ac7ffd5c5fe3ff\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-82p5khuh/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-82p5khuh/repo\", \"--revision\", \"0b6ef34ef137fe0237488fc840825135588a646e\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-82p5khuh/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-82p5khuh/repo\", \"--revision\", \"2b2a831a844802d083fbf438b0e21710ac9d7f16\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-82p5khuh/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-82p5khuh/repo\", \"--revision\", \"ae0314ada4c1d5269fe9d3d0fe432dcc55726fda\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.055
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "850c921347d0072145c15e60c45fc6aec719d7e1",
      "mutatedSha256": {
        "measure_c1.py": "d1f5796e08f61bc6dca3b231141fc1226c43404f5386fa44cd546744c167ebde",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "5dee6af94cc368603078bd1052463c8e1bc163ff",
      "committedMutationSha256": "d1f5796e08f61bc6dca3b231141fc1226c43404f5386fa44cd546744c167ebde",
      "mutated": {
        "exit": 1,
        "stdout": "",
        "stderr": "counter_selftest: {\"accepted\": 17, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-h4t75fie/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-h4t75fie/repo\", \"--revision\", \"c8087258f9978ca4802ab2a2304b2bccba30482c\"], \"errors\": [\"exit 0, expected 1\", \"accepted 17, expected 16\", \"failed rows [], expected ['drift-detection']\"], \"exit\": 0, \"expectedAccepted\": 16, \"expectedExit\": 1, \"output\": {\"accepted\": 17, \"claimVerdicts\": {\"HOLD\": 17, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"revision\": \"c8087258f9978ca4802ab2a2304b2bccba30482c\", \"total\": 17, \"units\": [{\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [\"claim fixture: anchor not in unit at base\"], \"unit\": \"drift-detection\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"fire-journal-codes\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"fleet-registry\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"free-read-verbs\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"ghp-subpath-spotcheck\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"keeper-timer-inert\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"kimi-subpath-audit\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"mirror-pitfalls\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"ops-automation\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"origin-repos\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"probe-delta-alerting\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"publish-channels\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"publish-queue\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"sitemap-orphan-audit\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"speedrun-pipeline\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"vault-properties\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"property-map\"}]}, \"passed\": false, \"stderr\": \"\", \"total\": 17}\n",
        "elapsedSeconds": 1.063
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "e119528ad2f1db5a852fd1319b8ef385acac1e84",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-3rm7bl7y/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-3rm7bl7y/repo\", \"--revision\", \"97be8bdc905b9dd3276133f8a477317965fe7f4c\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-3rm7bl7y/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-3rm7bl7y/repo\", \"--revision\", \"97be8bdc905b9dd3276133f8a477317965fe7f4c\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-3rm7bl7y/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-3rm7bl7y/repo\", \"--revision\", \"b6df96221a5c732e4b0e139e57929a1d12c21066\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-3rm7bl7y/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-3rm7bl7y/repo\", \"--revision\", \"146bdc2b28d11ebc2d40087098e82258ce4d648e\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-3rm7bl7y/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-3rm7bl7y/repo\", \"--revision\", \"4abc6889054f076b1632aaa0e771c4f98b46a948\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-3rm7bl7y/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-3rm7bl7y/repo\", \"--revision\", \"8ec96287870290ecadfd2d4d4a7e2bd60e6419ab\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-3rm7bl7y/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-3rm7bl7y/repo\", \"--revision\", \"466cc5f7879b13fb647363b4df12b615eed19d79\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.059
      },
      "verdict": "killed"
    },
    {
      "id": "C1-38",
      "script": "measure_c1.py",
      "check": "Overall exit rejects any failed unit",
      "pattern": "accepted == len(units)",
      "replacement": "True",
      "expected": "killed",
      "expectationReason": "Invalid-anchor fixture expects exit 1, not 0.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-3rm7bl7y/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-3rm7bl7y/repo\", \"--revision\", \"97be8bdc905b9dd3276133f8a477317965fe7f4c\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-3rm7bl7y/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-3rm7bl7y/repo\", \"--revision\", \"97be8bdc905b9dd3276133f8a477317965fe7f4c\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-3rm7bl7y/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-3rm7bl7y/repo\", \"--revision\", \"b6df96221a5c732e4b0e139e57929a1d12c21066\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-3rm7bl7y/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-3rm7bl7y/repo\", \"--revision\", \"146bdc2b28d11ebc2d40087098e82258ce4d648e\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-3rm7bl7y/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-3rm7bl7y/repo\", \"--revision\", \"4abc6889054f076b1632aaa0e771c4f98b46a948\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-3rm7bl7y/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-3rm7bl7y/repo\", \"--revision\", \"8ec96287870290ecadfd2d4d4a7e2bd60e6419ab\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-3rm7bl7y/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-3rm7bl7y/repo\", \"--revision\", \"466cc5f7879b13fb647363b4df12b615eed19d79\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.059
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "e119528ad2f1db5a852fd1319b8ef385acac1e84",
      "mutatedSha256": {
        "measure_c1.py": "701829e0d4e79d7b95734b563cf3b0023f03aaf63e83d092013f37ab6d7b5f75",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "bc1b53520de6cd18b7d99c946bf7aefaf5a3672f",
      "committedMutationSha256": "701829e0d4e79d7b95734b563cf3b0023f03aaf63e83d092013f37ab6d7b5f75",
      "mutated": {
        "exit": 1,
        "stdout": "",
        "stderr": "counter_selftest: {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-keysek4c/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-keysek4c/repo\", \"--revision\", \"57a723f8f7faecc12c5102a6b7da1a0c5055ead1\"], \"errors\": [\"exit 0, expected 1\"], \"exit\": 0, \"expectedAccepted\": 16, \"expectedExit\": 1, \"output\": {\"accepted\": 16, \"claimVerdicts\": {\"HOLD\": 17, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"revision\": \"57a723f8f7faecc12c5102a6b7da1a0c5055ead1\", \"total\": 17, \"units\": [{\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": false, \"problems\": [\"claim fixture: anchor not in unit at base\"], \"unit\": \"drift-detection\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"fire-journal-codes\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"fleet-registry\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"free-read-verbs\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"ghp-subpath-spotcheck\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"keeper-timer-inert\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"kimi-subpath-audit\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"mirror-pitfalls\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"ops-automation\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"origin-repos\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"probe-delta-alerting\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"publish-channels\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"publish-queue\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"sitemap-orphan-audit\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"speedrun-pipeline\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"vault-properties\"}, {\"claims\": {\"HOLD\": 1, \"STALE\": 0, \"UNVERIFIABLE\": 0}, \"pass\": true, \"problems\": [], \"unit\": \"property-map\"}]}, \"passed\": false, \"stderr\": \"\", \"total\": 17}\n",
        "elapsedSeconds": 1.036
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "0fddda8f091c4e5182b0016df127530a678b4ed7",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-3xq656ue/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-3xq656ue/repo\", \"--revision\", \"ffdfd87a6fcc763a73efa49f9e180114aeecdb36\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-3xq656ue/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-3xq656ue/repo\", \"--revision\", \"ffdfd87a6fcc763a73efa49f9e180114aeecdb36\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-3xq656ue/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-3xq656ue/repo\", \"--revision\", \"a2647a2816c7ce226967ec1c6a303974528862b3\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-3xq656ue/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-3xq656ue/repo\", \"--revision\", \"182e342fe9a23a20dd7220768edd0c84af5092b3\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-3xq656ue/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-3xq656ue/repo\", \"--revision\", \"ee2cfdb0dccef1a7d66ea17256fc04ccfe4c0621\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-3xq656ue/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-3xq656ue/repo\", \"--revision\", \"492d630996a3201e838d27eb80b4158405e94e2a\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-3xq656ue/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-3xq656ue/repo\", \"--revision\", \"02fd9e8859bc2a9d998a048cb9100549ec4cebda\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.122
      },
      "verdict": "killed"
    },
    {
      "id": "C1-39",
      "script": "measure_c1.py",
      "check": "Section is gated on heading presence",
      "pattern": "position >= 0",
      "replacement": "True",
      "expected": "survived",
      "expectationReason": "No selftest fixture invalidates this check.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-3xq656ue/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-3xq656ue/repo\", \"--revision\", \"ffdfd87a6fcc763a73efa49f9e180114aeecdb36\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-3xq656ue/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-3xq656ue/repo\", \"--revision\", \"ffdfd87a6fcc763a73efa49f9e180114aeecdb36\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-3xq656ue/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-3xq656ue/repo\", \"--revision\", \"a2647a2816c7ce226967ec1c6a303974528862b3\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-3xq656ue/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-3xq656ue/repo\", \"--revision\", \"182e342fe9a23a20dd7220768edd0c84af5092b3\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-3xq656ue/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-3xq656ue/repo\", \"--revision\", \"ee2cfdb0dccef1a7d66ea17256fc04ccfe4c0621\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-3xq656ue/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-3xq656ue/repo\", \"--revision\", \"492d630996a3201e838d27eb80b4158405e94e2a\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-3xq656ue/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-3xq656ue/repo\", \"--revision\", \"02fd9e8859bc2a9d998a048cb9100549ec4cebda\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.122
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "0fddda8f091c4e5182b0016df127530a678b4ed7",
      "mutatedSha256": {
        "measure_c1.py": "23b09bde38c46c439bfa548c226b2d4643ca6b93e92c82d3ef46bef95c9866a2",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "1d5b5d4deb2a45e1c82d97f5e4df9c750030d02b",
      "committedMutationSha256": "23b09bde38c46c439bfa548c226b2d4643ca6b93e92c82d3ef46bef95c9866a2",
      "mutated": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-46fj78zp/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-46fj78zp/repo\", \"--revision\", \"e57ea1f5426375ce0d46b6cd51037ee64d6586fa\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-46fj78zp/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-46fj78zp/repo\", \"--revision\", \"e57ea1f5426375ce0d46b6cd51037ee64d6586fa\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-46fj78zp/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-46fj78zp/repo\", \"--revision\", \"c13df26b19a034f99953aa93a8aa83ead850ec93\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-46fj78zp/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-46fj78zp/repo\", \"--revision\", \"a37b1333237f5510acd0312c98058a70e8b19aad\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-46fj78zp/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-46fj78zp/repo\", \"--revision\", \"db9dcff101e0f5e8a52136a025553d25ee578136\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-46fj78zp/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-46fj78zp/repo\", \"--revision\", \"4aea1b086bf1c47dd9fdd9c87ade972a26ed7146\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-46fj78zp/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-46fj78zp/repo\", \"--revision\", \"26e0b2841b78541341c29d5729ae55eec8a4125c\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.126
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "b0ab290c3915d206b85786b3d1a4d2486e4819f8",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-en_c9du4/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-en_c9du4/repo\", \"--revision\", \"f91f67ca0d2a02c17ec21ae917284564c2998326\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-en_c9du4/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-en_c9du4/repo\", \"--revision\", \"f91f67ca0d2a02c17ec21ae917284564c2998326\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-en_c9du4/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-en_c9du4/repo\", \"--revision\", \"50dacec53e1cb5cdbfa643e5bef8aa8a1931716b\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-en_c9du4/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-en_c9du4/repo\", \"--revision\", \"7e230b846dd0829f558aa75ce25d7e4068cb7c36\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-en_c9du4/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-en_c9du4/repo\", \"--revision\", \"597b4de506e91d044394069ec373ae06de15f758\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-en_c9du4/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-en_c9du4/repo\", \"--revision\", \"51dc89ce8873804c0a6363b7dc3aae0e473b2161\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-en_c9du4/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-en_c9du4/repo\", \"--revision\", \"f2066b3e8060bf915428b8dbba45504ee5bb081c\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.073
      },
      "verdict": "survived"
    },
    {
      "id": "C1-40",
      "script": "measure_c1.py",
      "check": "Required field string type",
      "pattern": "not isinstance(claim.get(k), str)",
      "replacement": "False",
      "expected": "survived",
      "expectationReason": "No selftest fixture invalidates this check.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-en_c9du4/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-en_c9du4/repo\", \"--revision\", \"f91f67ca0d2a02c17ec21ae917284564c2998326\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-en_c9du4/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-en_c9du4/repo\", \"--revision\", \"f91f67ca0d2a02c17ec21ae917284564c2998326\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-en_c9du4/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-en_c9du4/repo\", \"--revision\", \"50dacec53e1cb5cdbfa643e5bef8aa8a1931716b\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-en_c9du4/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-en_c9du4/repo\", \"--revision\", \"7e230b846dd0829f558aa75ce25d7e4068cb7c36\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-en_c9du4/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-en_c9du4/repo\", \"--revision\", \"597b4de506e91d044394069ec373ae06de15f758\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-en_c9du4/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-en_c9du4/repo\", \"--revision\", \"51dc89ce8873804c0a6363b7dc3aae0e473b2161\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-en_c9du4/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-en_c9du4/repo\", \"--revision\", \"f2066b3e8060bf915428b8dbba45504ee5bb081c\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.073
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "b0ab290c3915d206b85786b3d1a4d2486e4819f8",
      "mutatedSha256": {
        "measure_c1.py": "d1664e99ae799318b7cf7fc859553458f990f4386c38ef45a5b4693618fdd234",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "cd61818b565777735dbe5dc177291cf50182bf10",
      "committedMutationSha256": "d1664e99ae799318b7cf7fc859553458f990f4386c38ef45a5b4693618fdd234",
      "mutated": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-c2_qjxp3/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-c2_qjxp3/repo\", \"--revision\", \"5e06bf1953a7eb30c16faffc6b25001f06138304\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-c2_qjxp3/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-c2_qjxp3/repo\", \"--revision\", \"5e06bf1953a7eb30c16faffc6b25001f06138304\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-c2_qjxp3/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-c2_qjxp3/repo\", \"--revision\", \"302d67ba3a0b66e07e6c3b010cc452c959233727\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-c2_qjxp3/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-c2_qjxp3/repo\", \"--revision\", \"f97675beb5f7ecf520f4930c6d92d7fe2b116636\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-c2_qjxp3/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-c2_qjxp3/repo\", \"--revision\", \"3bd49658573d0cefe7e55207c7c5df3b221f1f3e\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-c2_qjxp3/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-c2_qjxp3/repo\", \"--revision\", \"d889ba02cbed2506efc3406c33597488eb89df49\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-c2_qjxp3/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-c2_qjxp3/repo\", \"--revision\", \"8bc31c3ec18718ff9b2be7675151c7f949991dba\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.131
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "8aac1c8f8af1315c8b4b226753373f278b7926a5",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-qnqspwub/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-qnqspwub/repo\", \"--revision\", \"3a2a73b77964b636c92c265514e49df883b36d51\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-qnqspwub/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-qnqspwub/repo\", \"--revision\", \"3a2a73b77964b636c92c265514e49df883b36d51\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-qnqspwub/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-qnqspwub/repo\", \"--revision\", \"d728b653fc286b7bd3999a0e8b9b5a7d59233b6a\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-qnqspwub/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-qnqspwub/repo\", \"--revision\", \"de9b2747dc81c36983842fe631a0236b1ed409b0\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-qnqspwub/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-qnqspwub/repo\", \"--revision\", \"2da6e5045aacdb982990d4fdcfd7beda1cd924b6\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-qnqspwub/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-qnqspwub/repo\", \"--revision\", \"753d3dca33ff0b6cef8e343c4da71454ed9977a4\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-qnqspwub/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-qnqspwub/repo\", \"--revision\", \"b3538fe64ba1acc20d056edd6d5ce6d7ff3e6cf2\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.106
      },
      "verdict": "survived"
    },
    {
      "id": "C1-41",
      "script": "measure_c1.py",
      "check": "Required field nonblank",
      "pattern": "not claim[k].strip()",
      "replacement": "False",
      "expected": "survived",
      "expectationReason": "No selftest fixture invalidates this check.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-qnqspwub/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-qnqspwub/repo\", \"--revision\", \"3a2a73b77964b636c92c265514e49df883b36d51\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-qnqspwub/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-qnqspwub/repo\", \"--revision\", \"3a2a73b77964b636c92c265514e49df883b36d51\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-qnqspwub/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-qnqspwub/repo\", \"--revision\", \"d728b653fc286b7bd3999a0e8b9b5a7d59233b6a\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-qnqspwub/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-qnqspwub/repo\", \"--revision\", \"de9b2747dc81c36983842fe631a0236b1ed409b0\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-qnqspwub/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-qnqspwub/repo\", \"--revision\", \"2da6e5045aacdb982990d4fdcfd7beda1cd924b6\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-qnqspwub/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-qnqspwub/repo\", \"--revision\", \"753d3dca33ff0b6cef8e343c4da71454ed9977a4\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-qnqspwub/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-qnqspwub/repo\", \"--revision\", \"b3538fe64ba1acc20d056edd6d5ce6d7ff3e6cf2\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.106
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "8aac1c8f8af1315c8b4b226753373f278b7926a5",
      "mutatedSha256": {
        "measure_c1.py": "05a8c2b1b97c89e89fc5f0bb560638a0ac472eb99f68b1413654a807dde54aaa",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "1fbbe36bceb085c207d6e64173b28340046cf261",
      "committedMutationSha256": "05a8c2b1b97c89e89fc5f0bb560638a0ac472eb99f68b1413654a807dde54aaa",
      "mutated": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-v0t_dgdv/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-v0t_dgdv/repo\", \"--revision\", \"71d61244a84507e205d141219b307adbc5f712cf\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-v0t_dgdv/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-v0t_dgdv/repo\", \"--revision\", \"71d61244a84507e205d141219b307adbc5f712cf\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-v0t_dgdv/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-v0t_dgdv/repo\", \"--revision\", \"f52941516803a09ac8aacbeafe1d82cd8804b67b\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-v0t_dgdv/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-v0t_dgdv/repo\", \"--revision\", \"cf0a7168a5ca76bce79f684449bd5d73b6962c2c\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-v0t_dgdv/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-v0t_dgdv/repo\", \"--revision\", \"3b334c43c71f644fe5ac0b2bd3525bd741da02a6\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-v0t_dgdv/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-v0t_dgdv/repo\", \"--revision\", \"18e22459c668b1b45ad0cd87fc0ef7e1e8d2185c\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-v0t_dgdv/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-v0t_dgdv/repo\", \"--revision\", \"648a6a45a6f1492150e8824a4f1c91aa9a1654e2\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.127
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "ab6cd864ed30723772dff8755871d454b005e988",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-3mrv_cpl/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-3mrv_cpl/repo\", \"--revision\", \"c10d44ca4faa0f9213ea3331810e1db54e8dcb67\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-3mrv_cpl/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-3mrv_cpl/repo\", \"--revision\", \"c10d44ca4faa0f9213ea3331810e1db54e8dcb67\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-3mrv_cpl/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-3mrv_cpl/repo\", \"--revision\", \"681d6eed9e8886d5e95a93e48ccdd8222c31f1bf\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-3mrv_cpl/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-3mrv_cpl/repo\", \"--revision\", \"65713b1d366bb57856b6bb270ef62a8aa4744797\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-3mrv_cpl/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-3mrv_cpl/repo\", \"--revision\", \"d20b5057b2b034057dcf945b5a904a25de650311\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-3mrv_cpl/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-3mrv_cpl/repo\", \"--revision\", \"fe76d3746baff19c2eaf892d731b67aff4deb194\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-3mrv_cpl/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-3mrv_cpl/repo\", \"--revision\", \"8902369adfcc1e072db21334fc6fa65942173f47\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.063
      },
      "verdict": "survived"
    },
    {
      "id": "C2-01",
      "script": "measure_c2.py",
      "check": "Git show return code",
      "pattern": "done.returncode == 0",
      "replacement": "True",
      "expected": "survived",
      "expectationReason": "No selftest fixture invalidates this check.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-3mrv_cpl/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-3mrv_cpl/repo\", \"--revision\", \"c10d44ca4faa0f9213ea3331810e1db54e8dcb67\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-3mrv_cpl/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-3mrv_cpl/repo\", \"--revision\", \"c10d44ca4faa0f9213ea3331810e1db54e8dcb67\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-3mrv_cpl/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-3mrv_cpl/repo\", \"--revision\", \"681d6eed9e8886d5e95a93e48ccdd8222c31f1bf\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-3mrv_cpl/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-3mrv_cpl/repo\", \"--revision\", \"65713b1d366bb57856b6bb270ef62a8aa4744797\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-3mrv_cpl/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-3mrv_cpl/repo\", \"--revision\", \"d20b5057b2b034057dcf945b5a904a25de650311\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-3mrv_cpl/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-3mrv_cpl/repo\", \"--revision\", \"fe76d3746baff19c2eaf892d731b67aff4deb194\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-3mrv_cpl/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-3mrv_cpl/repo\", \"--revision\", \"8902369adfcc1e072db21334fc6fa65942173f47\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.063
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "ab6cd864ed30723772dff8755871d454b005e988",
      "mutatedSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "7b584d3f77f46369b9dfb3b98ee12e89f5c2dcaba12646428cdc7a04b00b4c3c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "f5080970750c6d4e0328284393b33b371e282af4",
      "committedMutationSha256": "7b584d3f77f46369b9dfb3b98ee12e89f5c2dcaba12646428cdc7a04b00b4c3c",
      "mutated": {
        "exit": 1,
        "stdout": "",
        "stderr": "counter_selftest: {\"accepted\": 11, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-kmlrddpb/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-kmlrddpb/repo\", \"--revision\", \"ab48df69e12ae4c8e5409f9eeb421379c2dde5b2\"], \"errors\": [\"exit 1, expected 0\", \"accepted 11, expected 12\", \"failed rows ['charter-kimi'], expected []\"], \"exit\": 1, \"expectedAccepted\": 12, \"expectedExit\": 0, \"output\": {\"accepted\": 11, \"revision\": \"ab48df69e12ae4c8e5409f9eeb421379c2dde5b2\", \"surfaces\": [{\"id\": \"ds4cc-primary\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"plazir15-ghp\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"charter-ghp\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"ds4cc-kimi\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"burnerchrome-kimi\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"vault-index-kimi\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"plazir27-kimi\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"ufo-fsd-kimi-pro\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"lucario-ghp\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"lucario-kimi\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"plazir15-kimi\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"charter-kimi\", \"pass\": false, \"problems\": [\"page.html stored for a non-served response\"], \"verdict\": \"not-served\"}], \"total\": 12, \"validatorSha256\": \"062ccc4db6ab506ecb274ac0da4e4c4e9041462562e23cc586a0168cc8e44387\"}, \"passed\": false, \"stderr\": \"\", \"total\": 12}\n",
        "elapsedSeconds": 0.989
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "93168926ced616c414fe943029af47aeddaa2fa2",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-n2a99czl/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-n2a99czl/repo\", \"--revision\", \"df17f7e7e3b28a05e2cff5c0d35e596196485467\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-n2a99czl/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-n2a99czl/repo\", \"--revision\", \"df17f7e7e3b28a05e2cff5c0d35e596196485467\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-n2a99czl/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-n2a99czl/repo\", \"--revision\", \"f25d46b78623510e1c5c661c2ad4cb33c533ae67\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-n2a99czl/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-n2a99czl/repo\", \"--revision\", \"1fdb28b37f3ebda31be2834fbc8d33e95ffa7d78\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-n2a99czl/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-n2a99czl/repo\", \"--revision\", \"df5749e2f0689856c20820bf35ce0aa1537c2ff3\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-n2a99czl/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-n2a99czl/repo\", \"--revision\", \"1b30f331a3d074bd71001174a9ab330cea354f87\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-n2a99czl/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-n2a99czl/repo\", \"--revision\", \"48bc0aa0b55648a89f21253fcad74021f933c8c4\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.094
      },
      "verdict": "killed"
    },
    {
      "id": "C2-02",
      "script": "measure_c2.py",
      "check": "Served status integer type",
      "pattern": "isinstance(status, int)",
      "replacement": "True",
      "expected": "survived",
      "expectationReason": "No selftest fixture invalidates this check.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-n2a99czl/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-n2a99czl/repo\", \"--revision\", \"df17f7e7e3b28a05e2cff5c0d35e596196485467\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-n2a99czl/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-n2a99czl/repo\", \"--revision\", \"df17f7e7e3b28a05e2cff5c0d35e596196485467\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-n2a99czl/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-n2a99czl/repo\", \"--revision\", \"f25d46b78623510e1c5c661c2ad4cb33c533ae67\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-n2a99czl/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-n2a99czl/repo\", \"--revision\", \"1fdb28b37f3ebda31be2834fbc8d33e95ffa7d78\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-n2a99czl/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-n2a99czl/repo\", \"--revision\", \"df5749e2f0689856c20820bf35ce0aa1537c2ff3\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-n2a99czl/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-n2a99czl/repo\", \"--revision\", \"1b30f331a3d074bd71001174a9ab330cea354f87\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-n2a99czl/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-n2a99czl/repo\", \"--revision\", \"48bc0aa0b55648a89f21253fcad74021f933c8c4\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.094
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "93168926ced616c414fe943029af47aeddaa2fa2",
      "mutatedSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "e833e8da38441bc42fe246f21ce13362e42df8401e92c8b66b014cb07309a25a",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "b65a0daf3eca182ebbb6a7c789375a1cf681ac43",
      "committedMutationSha256": "e833e8da38441bc42fe246f21ce13362e42df8401e92c8b66b014cb07309a25a",
      "mutated": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-h1ke3fz9/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-h1ke3fz9/repo\", \"--revision\", \"91c098cdad8989492ed084cecccdf625be13cd7d\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-h1ke3fz9/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-h1ke3fz9/repo\", \"--revision\", \"91c098cdad8989492ed084cecccdf625be13cd7d\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-h1ke3fz9/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-h1ke3fz9/repo\", \"--revision\", \"6a03cc3d9bb41696dc1d6c547d02812f42b56073\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-h1ke3fz9/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-h1ke3fz9/repo\", \"--revision\", \"8fd4c6a3e32b3b8331cd9f153839c7937ebbba29\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-h1ke3fz9/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-h1ke3fz9/repo\", \"--revision\", \"666e9e490dc6f7859042b2120eca0ff53ff37e8e\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-h1ke3fz9/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-h1ke3fz9/repo\", \"--revision\", \"d5abb082e1bb034e546636d22d58e4241a326cc2\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-h1ke3fz9/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-h1ke3fz9/repo\", \"--revision\", \"4634b44d85c8978e4a31d662e8c2a78e72929191\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.103
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "f7170ac17556fe5f0f2573c2837d4058707ee53c",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-36uvbpuc/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-36uvbpuc/repo\", \"--revision\", \"22729d9dba015a6717b5e68f891360703ee85c01\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-36uvbpuc/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-36uvbpuc/repo\", \"--revision\", \"22729d9dba015a6717b5e68f891360703ee85c01\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-36uvbpuc/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-36uvbpuc/repo\", \"--revision\", \"728b41376ad5f4f0da020ccefe27d02725e047d0\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-36uvbpuc/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-36uvbpuc/repo\", \"--revision\", \"3451458595cf939089a7f560d48f2ec8da448fca\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-36uvbpuc/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-36uvbpuc/repo\", \"--revision\", \"c6439f1366aa6beaf1295c8915663a7428860fad\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-36uvbpuc/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-36uvbpuc/repo\", \"--revision\", \"cd0d5bd4f10839db7da66d2daf02783869fbd913\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-36uvbpuc/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-36uvbpuc/repo\", \"--revision\", \"13c5f93756425e34e7a838f3c9507c444e936bd3\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.07
      },
      "verdict": "survived"
    },
    {
      "id": "C2-03",
      "script": "measure_c2.py",
      "check": "Served status lower bound",
      "pattern": "200 <= status < 300",
      "replacement": "status < 300",
      "expected": "survived",
      "expectationReason": "No selftest fixture invalidates this check.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-36uvbpuc/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-36uvbpuc/repo\", \"--revision\", \"22729d9dba015a6717b5e68f891360703ee85c01\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-36uvbpuc/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-36uvbpuc/repo\", \"--revision\", \"22729d9dba015a6717b5e68f891360703ee85c01\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-36uvbpuc/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-36uvbpuc/repo\", \"--revision\", \"728b41376ad5f4f0da020ccefe27d02725e047d0\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-36uvbpuc/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-36uvbpuc/repo\", \"--revision\", \"3451458595cf939089a7f560d48f2ec8da448fca\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-36uvbpuc/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-36uvbpuc/repo\", \"--revision\", \"c6439f1366aa6beaf1295c8915663a7428860fad\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-36uvbpuc/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-36uvbpuc/repo\", \"--revision\", \"cd0d5bd4f10839db7da66d2daf02783869fbd913\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-36uvbpuc/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-36uvbpuc/repo\", \"--revision\", \"13c5f93756425e34e7a838f3c9507c444e936bd3\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.07
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "f7170ac17556fe5f0f2573c2837d4058707ee53c",
      "mutatedSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "be7d3088a440bfdffb9ab062c55d86bce4e02b9010a1639d90733944dcec4645",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "3c46181abe702359f6fade45226da0aec02a9378",
      "committedMutationSha256": "be7d3088a440bfdffb9ab062c55d86bce4e02b9010a1639d90733944dcec4645",
      "mutated": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-1iqhe_hr/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-1iqhe_hr/repo\", \"--revision\", \"a783323ab3ec819186de6a071f0171d5754121e9\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-1iqhe_hr/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-1iqhe_hr/repo\", \"--revision\", \"a783323ab3ec819186de6a071f0171d5754121e9\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-1iqhe_hr/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-1iqhe_hr/repo\", \"--revision\", \"266fe0e694bb1e3edc38ae1c601eef69ae27933b\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-1iqhe_hr/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-1iqhe_hr/repo\", \"--revision\", \"b6f83b0ce16b9fad2858c02d5dc651d02b72fe63\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-1iqhe_hr/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-1iqhe_hr/repo\", \"--revision\", \"572e29f7da2d582872409fbdcfb2b0746edbda15\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-1iqhe_hr/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-1iqhe_hr/repo\", \"--revision\", \"efbdb189796d10f5c0db5f003f5b2040709738d8\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-1iqhe_hr/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-1iqhe_hr/repo\", \"--revision\", \"d1f193157558d817094499e9a457a17bbc3e810d\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.088
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "ed90f06414465f9611eb7906a05ad4e4824288af",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-rgtr4uf0/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-rgtr4uf0/repo\", \"--revision\", \"dbd9d4e32a87fe2326c6f4e1c5c99b8b3a8768ef\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-rgtr4uf0/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-rgtr4uf0/repo\", \"--revision\", \"dbd9d4e32a87fe2326c6f4e1c5c99b8b3a8768ef\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-rgtr4uf0/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-rgtr4uf0/repo\", \"--revision\", \"24c8efe967346561765648b0ebef57feb88e9f34\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-rgtr4uf0/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-rgtr4uf0/repo\", \"--revision\", \"769de11c0beb0b1c00888628ce5f83455a0cbdd6\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-rgtr4uf0/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-rgtr4uf0/repo\", \"--revision\", \"8b908df300964e09525216e20237d91d992e61bd\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-rgtr4uf0/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-rgtr4uf0/repo\", \"--revision\", \"68192131a7ccb3016348d379468483b6bc8b828a\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-rgtr4uf0/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-rgtr4uf0/repo\", \"--revision\", \"d0ca980896bc08796f0cfc8fa65aed7fe5561a75\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.113
      },
      "verdict": "survived"
    },
    {
      "id": "C2-04",
      "script": "measure_c2.py",
      "check": "Served status upper bound",
      "pattern": "200 <= status < 300",
      "replacement": "200 <= status",
      "expected": "killed",
      "expectationReason": "The valid 404 non-served fixture would be misclassified as served, then lack page bytes.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-rgtr4uf0/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-rgtr4uf0/repo\", \"--revision\", \"dbd9d4e32a87fe2326c6f4e1c5c99b8b3a8768ef\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-rgtr4uf0/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-rgtr4uf0/repo\", \"--revision\", \"dbd9d4e32a87fe2326c6f4e1c5c99b8b3a8768ef\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-rgtr4uf0/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-rgtr4uf0/repo\", \"--revision\", \"24c8efe967346561765648b0ebef57feb88e9f34\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-rgtr4uf0/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-rgtr4uf0/repo\", \"--revision\", \"769de11c0beb0b1c00888628ce5f83455a0cbdd6\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-rgtr4uf0/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-rgtr4uf0/repo\", \"--revision\", \"8b908df300964e09525216e20237d91d992e61bd\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-rgtr4uf0/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-rgtr4uf0/repo\", \"--revision\", \"68192131a7ccb3016348d379468483b6bc8b828a\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-rgtr4uf0/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-rgtr4uf0/repo\", \"--revision\", \"d0ca980896bc08796f0cfc8fa65aed7fe5561a75\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.113
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "ed90f06414465f9611eb7906a05ad4e4824288af",
      "mutatedSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "565871a6442449a227d547edad5abe985f885b020aa17c3cce025d94c963f781",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "a08f3d2df6e11491d147e57d4c813052f5891d0f",
      "committedMutationSha256": "565871a6442449a227d547edad5abe985f885b020aa17c3cce025d94c963f781",
      "mutated": {
        "exit": 1,
        "stdout": "",
        "stderr": "counter_selftest: {\"accepted\": 11, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ajwga4dy/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ajwga4dy/repo\", \"--revision\", \"f5a8c9fc460db0b4907f0e7453fc146bbb1242c8\"], \"errors\": [\"exit 1, expected 0\", \"accepted 11, expected 12\", \"failed rows ['charter-kimi'], expected []\", \"non-served target 'charter-kimi' did not report not-served\"], \"exit\": 1, \"expectedAccepted\": 12, \"expectedExit\": 0, \"output\": {\"accepted\": 11, \"revision\": \"f5a8c9fc460db0b4907f0e7453fc146bbb1242c8\", \"surfaces\": [{\"id\": \"ds4cc-primary\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"plazir15-ghp\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"charter-ghp\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"ds4cc-kimi\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"burnerchrome-kimi\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"vault-index-kimi\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"plazir27-kimi\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"ufo-fsd-kimi-pro\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"lucario-ghp\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"lucario-kimi\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"plazir15-kimi\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"charter-kimi\", \"pass\": false, \"problems\": [\"page.html missing or digest differs from fetch.sha256\"], \"verdict\": null}], \"total\": 12, \"validatorSha256\": \"062ccc4db6ab506ecb274ac0da4e4c4e9041462562e23cc586a0168cc8e44387\"}, \"passed\": false, \"stderr\": \"\", \"total\": 12}\n",
        "elapsedSeconds": 1.001
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "cb3ec235b5f12e08ac728de748c3392ef70b29d8",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-er4ofxd5/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-er4ofxd5/repo\", \"--revision\", \"fe9bc66ebb2e17455393b70d65915b10644ea979\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-er4ofxd5/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-er4ofxd5/repo\", \"--revision\", \"fe9bc66ebb2e17455393b70d65915b10644ea979\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-er4ofxd5/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-er4ofxd5/repo\", \"--revision\", \"f0124576564a2b757730d61ecc4cc595ef0075a7\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-er4ofxd5/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-er4ofxd5/repo\", \"--revision\", \"815e3ba843d8126a2cd15dad8e6d52aff111d03f\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-er4ofxd5/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-er4ofxd5/repo\", \"--revision\", \"901f4d4d99c14de4cc9baffb6c696210c061edd8\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-er4ofxd5/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-er4ofxd5/repo\", \"--revision\", \"0051058378455fe8374faa781a9287f31254bf34\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-er4ofxd5/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-er4ofxd5/repo\", \"--revision\", \"ed4e2cb8214df99a5de311241d02c94855ad169d\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.126
      },
      "verdict": "killed"
    },
    {
      "id": "C2-05",
      "script": "measure_c2.py",
      "check": "Served fetch has no error",
      "pattern": "fetch.get(\"error\") is None",
      "replacement": "True",
      "expected": "survived",
      "expectationReason": "No selftest fixture invalidates this check.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-er4ofxd5/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-er4ofxd5/repo\", \"--revision\", \"fe9bc66ebb2e17455393b70d65915b10644ea979\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-er4ofxd5/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-er4ofxd5/repo\", \"--revision\", \"fe9bc66ebb2e17455393b70d65915b10644ea979\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-er4ofxd5/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-er4ofxd5/repo\", \"--revision\", \"f0124576564a2b757730d61ecc4cc595ef0075a7\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-er4ofxd5/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-er4ofxd5/repo\", \"--revision\", \"815e3ba843d8126a2cd15dad8e6d52aff111d03f\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-er4ofxd5/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-er4ofxd5/repo\", \"--revision\", \"901f4d4d99c14de4cc9baffb6c696210c061edd8\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-er4ofxd5/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-er4ofxd5/repo\", \"--revision\", \"0051058378455fe8374faa781a9287f31254bf34\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-er4ofxd5/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-er4ofxd5/repo\", \"--revision\", \"ed4e2cb8214df99a5de311241d02c94855ad169d\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.126
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "cb3ec235b5f12e08ac728de748c3392ef70b29d8",
      "mutatedSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "977e339df3a532e831fe862ccb661073ad5cd2c3c3b2e58161c7087fea580ca0",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "f309a5b66d1d5f31aa46949adca6d6b1ae31f015",
      "committedMutationSha256": "977e339df3a532e831fe862ccb661073ad5cd2c3c3b2e58161c7087fea580ca0",
      "mutated": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-_lhoh1mc/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-_lhoh1mc/repo\", \"--revision\", \"5abfdcef5b51760d4c6ccbcb0b6ea2b737138b85\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-_lhoh1mc/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-_lhoh1mc/repo\", \"--revision\", \"5abfdcef5b51760d4c6ccbcb0b6ea2b737138b85\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-_lhoh1mc/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-_lhoh1mc/repo\", \"--revision\", \"62803b25914d299be4df67b894dcda349dda4dec\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-_lhoh1mc/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-_lhoh1mc/repo\", \"--revision\", \"e61984cfc94b0df7b0b9a209963acccc78e18eed\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-_lhoh1mc/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-_lhoh1mc/repo\", \"--revision\", \"0283c302127e411f634b4d5f7adf5f7af53d3c96\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-_lhoh1mc/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-_lhoh1mc/repo\", \"--revision\", \"18907079f529d2dc60c13e51f168d07ba265fafc\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-_lhoh1mc/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-_lhoh1mc/repo\", \"--revision\", \"dc000147112bb44b01256bdb22b6ab0a60c36d1a\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.084
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "b1f7040a7b35ee37be7de7b9eb6c10aba468a62b",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-6tknqg95/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-6tknqg95/repo\", \"--revision\", \"f3f83c8fb0ac078e0ab81f542fad91955445b84d\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-6tknqg95/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-6tknqg95/repo\", \"--revision\", \"f3f83c8fb0ac078e0ab81f542fad91955445b84d\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-6tknqg95/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-6tknqg95/repo\", \"--revision\", \"077990427462c38e2c88ae60a52d83df03f3844c\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-6tknqg95/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-6tknqg95/repo\", \"--revision\", \"0cc0e6dcb540b77a3cfbdfa350629974366b0fea\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-6tknqg95/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-6tknqg95/repo\", \"--revision\", \"e10af6b446dc11a7b591a147218e8b948666acb5\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-6tknqg95/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-6tknqg95/repo\", \"--revision\", \"c775f849f7bbe118fb0a3f258db758eec033fea7\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-6tknqg95/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-6tknqg95/repo\", \"--revision\", \"47eb63efda56c117ec69e74cd80f5877f780e0b0\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.049
      },
      "verdict": "survived"
    },
    {
      "id": "C2-06",
      "script": "measure_c2.py",
      "check": "Served fetch is not truncated",
      "pattern": "not fetch.get(\"truncated\")",
      "replacement": "True",
      "expected": "survived",
      "expectationReason": "No selftest fixture invalidates this check.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-6tknqg95/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-6tknqg95/repo\", \"--revision\", \"f3f83c8fb0ac078e0ab81f542fad91955445b84d\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-6tknqg95/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-6tknqg95/repo\", \"--revision\", \"f3f83c8fb0ac078e0ab81f542fad91955445b84d\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-6tknqg95/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-6tknqg95/repo\", \"--revision\", \"077990427462c38e2c88ae60a52d83df03f3844c\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-6tknqg95/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-6tknqg95/repo\", \"--revision\", \"0cc0e6dcb540b77a3cfbdfa350629974366b0fea\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-6tknqg95/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-6tknqg95/repo\", \"--revision\", \"e10af6b446dc11a7b591a147218e8b948666acb5\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-6tknqg95/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-6tknqg95/repo\", \"--revision\", \"c775f849f7bbe118fb0a3f258db758eec033fea7\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-6tknqg95/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-6tknqg95/repo\", \"--revision\", \"47eb63efda56c117ec69e74cd80f5877f780e0b0\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.049
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "b1f7040a7b35ee37be7de7b9eb6c10aba468a62b",
      "mutatedSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "da3483fc4f6667590484d1a75ac57145a7bb9b3517c528fe3e040182d0b3cb5c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "e9dde844fe7d725ccaa8642e311cd2c801140ddc",
      "committedMutationSha256": "da3483fc4f6667590484d1a75ac57145a7bb9b3517c528fe3e040182d0b3cb5c",
      "mutated": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-d1o_8zzp/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-d1o_8zzp/repo\", \"--revision\", \"da2b363e845f3ab0f48eee562bbd01c3210526c1\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-d1o_8zzp/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-d1o_8zzp/repo\", \"--revision\", \"da2b363e845f3ab0f48eee562bbd01c3210526c1\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-d1o_8zzp/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-d1o_8zzp/repo\", \"--revision\", \"b7798ab5094f25654553576e95a54f0528be7a37\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-d1o_8zzp/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-d1o_8zzp/repo\", \"--revision\", \"764498f955751f045f75a8eb55ec2e5f67cfb613\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-d1o_8zzp/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-d1o_8zzp/repo\", \"--revision\", \"e50ea89ca3c6d6854573545803951ef679d7d5a1\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-d1o_8zzp/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-d1o_8zzp/repo\", \"--revision\", \"e0234cd9ee5c16a5e34ac05b120a72476517767a\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-d1o_8zzp/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-d1o_8zzp/repo\", \"--revision\", \"0599b27906f4c251f832660a3a4de1d2388dbf4b\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.058
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "e59d5c5b8ca99c62f14519b24ec85d6bf17d4455",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-8gf66ttm/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-8gf66ttm/repo\", \"--revision\", \"6bc2900f80de3fa7801d8cb1c73606ba64f2a34f\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-8gf66ttm/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-8gf66ttm/repo\", \"--revision\", \"6bc2900f80de3fa7801d8cb1c73606ba64f2a34f\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-8gf66ttm/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-8gf66ttm/repo\", \"--revision\", \"dc98cfc0265f50b901957ecec63325a5d0442dd2\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-8gf66ttm/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-8gf66ttm/repo\", \"--revision\", \"ce5eed414ab4915fd00db54e9675edbbd5605887\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-8gf66ttm/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-8gf66ttm/repo\", \"--revision\", \"1f08706b251c79157b9d740223a111b4cc996c52\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-8gf66ttm/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-8gf66ttm/repo\", \"--revision\", \"7006b78204bd5f70a99cc8aebde831b941ef6968\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-8gf66ttm/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-8gf66ttm/repo\", \"--revision\", \"af1c1b96a9ccde23d4e4758886a93bceda7890c6\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.051
      },
      "verdict": "survived"
    },
    {
      "id": "C2-07",
      "script": "measure_c2.py",
      "check": "Served Content-Type HTML",
      "pattern": "ctype.split(\";\")[0].strip().lower() == \"text/html\"",
      "replacement": "True",
      "expected": "survived",
      "expectationReason": "No selftest fixture invalidates this check.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-8gf66ttm/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-8gf66ttm/repo\", \"--revision\", \"6bc2900f80de3fa7801d8cb1c73606ba64f2a34f\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-8gf66ttm/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-8gf66ttm/repo\", \"--revision\", \"6bc2900f80de3fa7801d8cb1c73606ba64f2a34f\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-8gf66ttm/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-8gf66ttm/repo\", \"--revision\", \"dc98cfc0265f50b901957ecec63325a5d0442dd2\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-8gf66ttm/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-8gf66ttm/repo\", \"--revision\", \"ce5eed414ab4915fd00db54e9675edbbd5605887\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-8gf66ttm/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-8gf66ttm/repo\", \"--revision\", \"1f08706b251c79157b9d740223a111b4cc996c52\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-8gf66ttm/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-8gf66ttm/repo\", \"--revision\", \"7006b78204bd5f70a99cc8aebde831b941ef6968\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-8gf66ttm/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-8gf66ttm/repo\", \"--revision\", \"af1c1b96a9ccde23d4e4758886a93bceda7890c6\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.051
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "e59d5c5b8ca99c62f14519b24ec85d6bf17d4455",
      "mutatedSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "0b389fa0624eeb489378bd27506f6113662af8483317934fbfc2e1b8d47fa46c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "fd82ac9aca7c582fc0fa07c19d4b713b77c461b7",
      "committedMutationSha256": "0b389fa0624eeb489378bd27506f6113662af8483317934fbfc2e1b8d47fa46c",
      "mutated": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-x8amlyr9/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-x8amlyr9/repo\", \"--revision\", \"2c478469f3aa8b3d1c5dedab14c9f7aca98ce800\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-x8amlyr9/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-x8amlyr9/repo\", \"--revision\", \"2c478469f3aa8b3d1c5dedab14c9f7aca98ce800\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-x8amlyr9/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-x8amlyr9/repo\", \"--revision\", \"0a88c1e74732aaefd36b2313ec903548385b4cfb\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-x8amlyr9/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-x8amlyr9/repo\", \"--revision\", \"2f0ba1521a7cdb99d84d50053e6595c6d514035b\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-x8amlyr9/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-x8amlyr9/repo\", \"--revision\", \"1bc419f1c8babd1fecf400041d265a616da75f97\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-x8amlyr9/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-x8amlyr9/repo\", \"--revision\", \"0be41c0adbc1081948bf8e938a1d5c05b2a0337e\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-x8amlyr9/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-x8amlyr9/repo\", \"--revision\", \"7d52b07ce9f93a49ee0a3f7b1bd4172e3f0155ba\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.023
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "324e9c8c053cb546716935e89f5bee1300fc6274",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-wrhyzi0_/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-wrhyzi0_/repo\", \"--revision\", \"56d089d256e7d94a5892aeda02e8c1652684651a\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-wrhyzi0_/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-wrhyzi0_/repo\", \"--revision\", \"56d089d256e7d94a5892aeda02e8c1652684651a\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-wrhyzi0_/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-wrhyzi0_/repo\", \"--revision\", \"4464b1e30eb5282d5d61d2bf3c1688c718e84331\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-wrhyzi0_/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-wrhyzi0_/repo\", \"--revision\", \"abbf21b4a2b99c6b2eeba975c1fccbf0a98608d2\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-wrhyzi0_/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-wrhyzi0_/repo\", \"--revision\", \"8327322400311bf7ba69d1510584437b9af12370\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-wrhyzi0_/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-wrhyzi0_/repo\", \"--revision\", \"5fe4d575d114ea8e1c1762f9b062f1c9623b3c1d\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-wrhyzi0_/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-wrhyzi0_/repo\", \"--revision\", \"81f31244725f8df79b140a926fd714b95a3efd56\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.045
      },
      "verdict": "survived"
    },
    {
      "id": "C2-08",
      "script": "measure_c2.py",
      "check": "Fetch metadata present",
      "pattern": "raw_fetch is None",
      "replacement": "False",
      "expected": "survived",
      "expectationReason": "No selftest fixture invalidates this check.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-wrhyzi0_/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-wrhyzi0_/repo\", \"--revision\", \"56d089d256e7d94a5892aeda02e8c1652684651a\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-wrhyzi0_/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-wrhyzi0_/repo\", \"--revision\", \"56d089d256e7d94a5892aeda02e8c1652684651a\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-wrhyzi0_/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-wrhyzi0_/repo\", \"--revision\", \"4464b1e30eb5282d5d61d2bf3c1688c718e84331\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-wrhyzi0_/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-wrhyzi0_/repo\", \"--revision\", \"abbf21b4a2b99c6b2eeba975c1fccbf0a98608d2\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-wrhyzi0_/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-wrhyzi0_/repo\", \"--revision\", \"8327322400311bf7ba69d1510584437b9af12370\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-wrhyzi0_/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-wrhyzi0_/repo\", \"--revision\", \"5fe4d575d114ea8e1c1762f9b062f1c9623b3c1d\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-wrhyzi0_/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-wrhyzi0_/repo\", \"--revision\", \"81f31244725f8df79b140a926fd714b95a3efd56\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.045
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "324e9c8c053cb546716935e89f5bee1300fc6274",
      "mutatedSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "bac59a78cd75404b5c8739ef6819b224bc91d975bba98d22b14572abad694adf",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "1d88febef411c1ae5dfd241ac1cf3543e9a63694",
      "committedMutationSha256": "bac59a78cd75404b5c8739ef6819b224bc91d975bba98d22b14572abad694adf",
      "mutated": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-bq55foa6/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-bq55foa6/repo\", \"--revision\", \"97777148eebcffb410414a69e87b753bf9c5dd7c\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-bq55foa6/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-bq55foa6/repo\", \"--revision\", \"97777148eebcffb410414a69e87b753bf9c5dd7c\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-bq55foa6/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-bq55foa6/repo\", \"--revision\", \"3cddd978255b1d851ae5eb266149515a5862df84\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-bq55foa6/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-bq55foa6/repo\", \"--revision\", \"a3dd37cc98706ce12c98e78fc6082926373a2c5f\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-bq55foa6/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-bq55foa6/repo\", \"--revision\", \"37bc0e9e0326d48f77ec554736f977c250dcb6f2\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-bq55foa6/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-bq55foa6/repo\", \"--revision\", \"b7b159cb6a6b5af4a6f80fb8b05c947ed3018cb2\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-bq55foa6/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-bq55foa6/repo\", \"--revision\", \"11afbe9c6aa3564694b819d56380c4c10b32248e\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.103
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "2094f7e1ec4d334a4909a1b25871381b23f5fd16",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-wzp9rirn/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-wzp9rirn/repo\", \"--revision\", \"fbc207c0ccc0714c87e88314a458c97d52a100f4\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-wzp9rirn/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-wzp9rirn/repo\", \"--revision\", \"fbc207c0ccc0714c87e88314a458c97d52a100f4\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-wzp9rirn/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-wzp9rirn/repo\", \"--revision\", \"5e4e8fdb37f11276f17b9a3de4590baff7936a50\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-wzp9rirn/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-wzp9rirn/repo\", \"--revision\", \"61ac4a0a28a6d0d4a47707509b8a2e367e1e08e9\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-wzp9rirn/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-wzp9rirn/repo\", \"--revision\", \"938c00c8b85da1d2cc4ac9b46e49d0d0174f23c5\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-wzp9rirn/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-wzp9rirn/repo\", \"--revision\", \"ace36f5b22aa3a9d9bf43607f238704f4696c483\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-wzp9rirn/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-wzp9rirn/repo\", \"--revision\", \"5064da4d8e0a913cea14e8150cb47c05441348f5\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.106
      },
      "verdict": "survived"
    },
    {
      "id": "C2-09",
      "script": "measure_c2.py",
      "check": "Audit receipt present",
      "pattern": "raw_audit is None",
      "replacement": "False",
      "expected": "survived",
      "expectationReason": "No selftest fixture invalidates this check.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-wzp9rirn/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-wzp9rirn/repo\", \"--revision\", \"fbc207c0ccc0714c87e88314a458c97d52a100f4\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-wzp9rirn/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-wzp9rirn/repo\", \"--revision\", \"fbc207c0ccc0714c87e88314a458c97d52a100f4\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-wzp9rirn/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-wzp9rirn/repo\", \"--revision\", \"5e4e8fdb37f11276f17b9a3de4590baff7936a50\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-wzp9rirn/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-wzp9rirn/repo\", \"--revision\", \"61ac4a0a28a6d0d4a47707509b8a2e367e1e08e9\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-wzp9rirn/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-wzp9rirn/repo\", \"--revision\", \"938c00c8b85da1d2cc4ac9b46e49d0d0174f23c5\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-wzp9rirn/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-wzp9rirn/repo\", \"--revision\", \"ace36f5b22aa3a9d9bf43607f238704f4696c483\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-wzp9rirn/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-wzp9rirn/repo\", \"--revision\", \"5064da4d8e0a913cea14e8150cb47c05441348f5\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.106
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "2094f7e1ec4d334a4909a1b25871381b23f5fd16",
      "mutatedSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "547dd95df3cf773d2a6c97e11981b122b671590e604470e21ad95f26eeb74156",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "065fe6510802914bdc6e08b7ab512e0d2bca2c06",
      "committedMutationSha256": "547dd95df3cf773d2a6c97e11981b122b671590e604470e21ad95f26eeb74156",
      "mutated": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-_frc5b8y/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-_frc5b8y/repo\", \"--revision\", \"56ea31800411d661e4573ab680b8a98acccf1b76\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-_frc5b8y/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-_frc5b8y/repo\", \"--revision\", \"56ea31800411d661e4573ab680b8a98acccf1b76\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-_frc5b8y/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-_frc5b8y/repo\", \"--revision\", \"26586f7ff8c702cdbe714c37603cd7d00de5941b\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-_frc5b8y/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-_frc5b8y/repo\", \"--revision\", \"e81eb9dbba80dc238f7b0d49074e43be22f2ca51\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-_frc5b8y/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-_frc5b8y/repo\", \"--revision\", \"c433d5327faf1dd4db38b0aa1a04267a5575542a\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-_frc5b8y/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-_frc5b8y/repo\", \"--revision\", \"7c94fb60ea984ead7f92bf0a24c5a815b8d66ba8\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-_frc5b8y/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-_frc5b8y/repo\", \"--revision\", \"46335b1ec4babfb610cd70ea792149cf24d87cf0\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.105
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "dfa1b718aba5ccc59137340615cd5251276dbade",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-t85gx86d/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-t85gx86d/repo\", \"--revision\", \"1cc7cc9659be0b9625f896d528fbf4efd8e5ce68\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-t85gx86d/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-t85gx86d/repo\", \"--revision\", \"1cc7cc9659be0b9625f896d528fbf4efd8e5ce68\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-t85gx86d/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-t85gx86d/repo\", \"--revision\", \"7031fda3f8eb59f4f92fcfec5886bc4890851ef7\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-t85gx86d/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-t85gx86d/repo\", \"--revision\", \"b9dbd4b43865645b72d2313df94f3c0b02e4a08d\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-t85gx86d/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-t85gx86d/repo\", \"--revision\", \"d6338d2bfccbf93fb79a04cffc406150d8a58f3b\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-t85gx86d/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-t85gx86d/repo\", \"--revision\", \"52fd73dd12a1b82080da5f829a7f8297a52fce91\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-t85gx86d/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-t85gx86d/repo\", \"--revision\", \"7c26890ece54df6268de10cc5170bbc7b8fc1a67\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.068
      },
      "verdict": "survived"
    },
    {
      "id": "C2-10",
      "script": "measure_c2.py",
      "check": "Receipt JSON parsing rejection",
      "pattern": "return [f\"receipt JSON invalid: {exc}\"], None",
      "replacement": "return [], None",
      "expected": "survived",
      "expectationReason": "No selftest fixture invalidates this check.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-t85gx86d/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-t85gx86d/repo\", \"--revision\", \"1cc7cc9659be0b9625f896d528fbf4efd8e5ce68\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-t85gx86d/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-t85gx86d/repo\", \"--revision\", \"1cc7cc9659be0b9625f896d528fbf4efd8e5ce68\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-t85gx86d/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-t85gx86d/repo\", \"--revision\", \"7031fda3f8eb59f4f92fcfec5886bc4890851ef7\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-t85gx86d/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-t85gx86d/repo\", \"--revision\", \"b9dbd4b43865645b72d2313df94f3c0b02e4a08d\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-t85gx86d/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-t85gx86d/repo\", \"--revision\", \"d6338d2bfccbf93fb79a04cffc406150d8a58f3b\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-t85gx86d/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-t85gx86d/repo\", \"--revision\", \"52fd73dd12a1b82080da5f829a7f8297a52fce91\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-t85gx86d/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-t85gx86d/repo\", \"--revision\", \"7c26890ece54df6268de10cc5170bbc7b8fc1a67\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.068
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "dfa1b718aba5ccc59137340615cd5251276dbade",
      "mutatedSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "61d7eefea8b6a37f509205eca57bffb143cd05affc59c88e9cb8ce06e0e6fde0",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "821dbe72a1a45b3e3886ea0ac6632d41442fd4ab",
      "committedMutationSha256": "61d7eefea8b6a37f509205eca57bffb143cd05affc59c88e9cb8ce06e0e6fde0",
      "mutated": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-0vvfxps6/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-0vvfxps6/repo\", \"--revision\", \"dc194f3b2e48582e3ce8ea503dc60e38f9487630\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-0vvfxps6/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-0vvfxps6/repo\", \"--revision\", \"dc194f3b2e48582e3ce8ea503dc60e38f9487630\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-0vvfxps6/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-0vvfxps6/repo\", \"--revision\", \"35eb02599d875c876394f9d0abea3ed9fe760494\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-0vvfxps6/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-0vvfxps6/repo\", \"--revision\", \"d5b218a67af78ff9bc4a6fd0fbf938189d2aaec5\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-0vvfxps6/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-0vvfxps6/repo\", \"--revision\", \"53b9b4a1ba9c5fc9c16c6b56e4a1728b8335ebb9\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-0vvfxps6/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-0vvfxps6/repo\", \"--revision\", \"c95ff0d377490c4a56186706cf086a7132d61319\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-0vvfxps6/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-0vvfxps6/repo\", \"--revision\", \"de683a732570fddb808bcfa3e94c738d097f95eb\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.037
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "1a583f943737128e41d86aa96281d7a85a6617ef",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-mjowh8t1/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-mjowh8t1/repo\", \"--revision\", \"ad6ecec48c8318724a818dd51ee99b19c13fdfce\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-mjowh8t1/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-mjowh8t1/repo\", \"--revision\", \"ad6ecec48c8318724a818dd51ee99b19c13fdfce\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-mjowh8t1/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-mjowh8t1/repo\", \"--revision\", \"0c7907b3bbdc289bd1ddfffac2aea2a1e12dfcdd\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-mjowh8t1/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-mjowh8t1/repo\", \"--revision\", \"ab6e00a88ff5c2c2ddaa1955f0355096b755ec40\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-mjowh8t1/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-mjowh8t1/repo\", \"--revision\", \"ef6cedd277b9b7e21a71ad2ee50f5656f9a69901\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-mjowh8t1/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-mjowh8t1/repo\", \"--revision\", \"2bb6fee38bbd68b90dfde8e590cdc7ccc7f2b33a\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-mjowh8t1/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-mjowh8t1/repo\", \"--revision\", \"f3f50327c2ac42902347ef5cb7899013fce3c31c\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.05
      },
      "verdict": "survived"
    },
    {
      "id": "C2-11",
      "script": "measure_c2.py",
      "check": "Fetch URL matches population",
      "pattern": "fetch.get(\"url\") != surface[\"url\"]",
      "replacement": "False",
      "expected": "survived",
      "expectationReason": "No selftest fixture invalidates this check.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-mjowh8t1/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-mjowh8t1/repo\", \"--revision\", \"ad6ecec48c8318724a818dd51ee99b19c13fdfce\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-mjowh8t1/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-mjowh8t1/repo\", \"--revision\", \"ad6ecec48c8318724a818dd51ee99b19c13fdfce\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-mjowh8t1/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-mjowh8t1/repo\", \"--revision\", \"0c7907b3bbdc289bd1ddfffac2aea2a1e12dfcdd\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-mjowh8t1/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-mjowh8t1/repo\", \"--revision\", \"ab6e00a88ff5c2c2ddaa1955f0355096b755ec40\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-mjowh8t1/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-mjowh8t1/repo\", \"--revision\", \"ef6cedd277b9b7e21a71ad2ee50f5656f9a69901\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-mjowh8t1/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-mjowh8t1/repo\", \"--revision\", \"2bb6fee38bbd68b90dfde8e590cdc7ccc7f2b33a\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-mjowh8t1/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-mjowh8t1/repo\", \"--revision\", \"f3f50327c2ac42902347ef5cb7899013fce3c31c\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.05
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "1a583f943737128e41d86aa96281d7a85a6617ef",
      "mutatedSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "a0df21c9627a1e0c97376dec43e4e7e9f07b3c8c7f1d4f36073ae9911707dea7",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "b347b0fc8f1afd177987afca8f9555b61d1fa7c1",
      "committedMutationSha256": "a0df21c9627a1e0c97376dec43e4e7e9f07b3c8c7f1d4f36073ae9911707dea7",
      "mutated": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-mfe946bf/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-mfe946bf/repo\", \"--revision\", \"15f596350135aa6dfd099c79af88a835cc24e1a5\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-mfe946bf/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-mfe946bf/repo\", \"--revision\", \"15f596350135aa6dfd099c79af88a835cc24e1a5\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-mfe946bf/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-mfe946bf/repo\", \"--revision\", \"7adf2b588c0d86cb42d98fec4d01da0045256c8d\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-mfe946bf/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-mfe946bf/repo\", \"--revision\", \"0a1e9293e7ef52e8a573038cbb779a9cfba4e43e\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-mfe946bf/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-mfe946bf/repo\", \"--revision\", \"d2743ebd1bab059e856300360f305df048c174b8\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-mfe946bf/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-mfe946bf/repo\", \"--revision\", \"535d1fb432a8ea6968f982e45584dd3e4ec75cd0\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-mfe946bf/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-mfe946bf/repo\", \"--revision\", \"52458d89b2939151608232446a2fdba1d6c8ded6\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.045
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "825fd34f962e89298afda202c464d4453846af1f",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-4n6ezb69/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-4n6ezb69/repo\", \"--revision\", \"a8957c3c8d2c5e96a3c53b315b8cc9b771355288\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-4n6ezb69/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-4n6ezb69/repo\", \"--revision\", \"a8957c3c8d2c5e96a3c53b315b8cc9b771355288\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-4n6ezb69/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-4n6ezb69/repo\", \"--revision\", \"84c3ef1aa5cd568ea2401484e8a184209ba050e1\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-4n6ezb69/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-4n6ezb69/repo\", \"--revision\", \"7bf75adbb40926af184bd7c1c2381e10bf94ed1c\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-4n6ezb69/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-4n6ezb69/repo\", \"--revision\", \"58a155265199d6f902ca0b4fb60dab737565c905\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-4n6ezb69/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-4n6ezb69/repo\", \"--revision\", \"6a41a9396afeea8f0a2cbe2864dfd5ab0482d5e3\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-4n6ezb69/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-4n6ezb69/repo\", \"--revision\", \"55445af56a6319628a4c9ba1e9aac2217ea2e641\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.014
      },
      "verdict": "survived"
    },
    {
      "id": "C2-12",
      "script": "measure_c2.py",
      "check": "Fetch method GET",
      "pattern": "fetch.get(\"method\") != \"GET\"",
      "replacement": "False",
      "expected": "killed",
      "expectationReason": "The non-GET fixture changes method to HEAD and expects rejection with a GET diagnostic.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-4n6ezb69/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-4n6ezb69/repo\", \"--revision\", \"a8957c3c8d2c5e96a3c53b315b8cc9b771355288\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-4n6ezb69/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-4n6ezb69/repo\", \"--revision\", \"a8957c3c8d2c5e96a3c53b315b8cc9b771355288\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-4n6ezb69/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-4n6ezb69/repo\", \"--revision\", \"84c3ef1aa5cd568ea2401484e8a184209ba050e1\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-4n6ezb69/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-4n6ezb69/repo\", \"--revision\", \"7bf75adbb40926af184bd7c1c2381e10bf94ed1c\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-4n6ezb69/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-4n6ezb69/repo\", \"--revision\", \"58a155265199d6f902ca0b4fb60dab737565c905\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-4n6ezb69/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-4n6ezb69/repo\", \"--revision\", \"6a41a9396afeea8f0a2cbe2864dfd5ab0482d5e3\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-4n6ezb69/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-4n6ezb69/repo\", \"--revision\", \"55445af56a6319628a4c9ba1e9aac2217ea2e641\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.014
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "825fd34f962e89298afda202c464d4453846af1f",
      "mutatedSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "4d44aa70c821cc3da7f94b1b12764c8ef6c4c39a44b993dee014fce429df587f",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "df5239bf4639cb534cd9a3ec8d81eb9319fd5a22",
      "committedMutationSha256": "4d44aa70c821cc3da7f94b1b12764c8ef6c4c39a44b993dee014fce429df587f",
      "mutated": {
        "exit": 1,
        "stdout": "",
        "stderr": "counter_selftest: {\"accepted\": 12, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-pvtf7t3x/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-pvtf7t3x/repo\", \"--revision\", \"a3b28997dc254233cbdb5a4173e0853825c028f1\"], \"errors\": [\"exit 0, expected 1\", \"accepted 12, expected 11\", \"failed rows [], expected ['plazir15-ghp']\", \"target 'plazir15-ghp' lacks problem 'GET'\"], \"exit\": 0, \"expectedAccepted\": 11, \"expectedExit\": 1, \"output\": {\"accepted\": 12, \"revision\": \"a3b28997dc254233cbdb5a4173e0853825c028f1\", \"surfaces\": [{\"id\": \"ds4cc-primary\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"plazir15-ghp\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"charter-ghp\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"ds4cc-kimi\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"burnerchrome-kimi\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"vault-index-kimi\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"plazir27-kimi\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"ufo-fsd-kimi-pro\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"lucario-ghp\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"lucario-kimi\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"plazir15-kimi\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"charter-kimi\", \"pass\": true, \"problems\": [], \"verdict\": \"not-served\"}], \"total\": 12, \"validatorSha256\": \"062ccc4db6ab506ecb274ac0da4e4c4e9041462562e23cc586a0168cc8e44387\"}, \"passed\": false, \"stderr\": \"\", \"total\": 12}\n",
        "elapsedSeconds": 2.016
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "798493f648889eb5d0ac965fd117ae486589eee0",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-yxwnvabe/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-yxwnvabe/repo\", \"--revision\", \"98a975310008ed5817a7857c1aa8652d73a94cd6\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-yxwnvabe/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-yxwnvabe/repo\", \"--revision\", \"98a975310008ed5817a7857c1aa8652d73a94cd6\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-yxwnvabe/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-yxwnvabe/repo\", \"--revision\", \"f09628011232539760c88ed40bb2bd2908dcde37\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-yxwnvabe/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-yxwnvabe/repo\", \"--revision\", \"52d9e77782365f7cdc47d1ed14d19f06844fdfe9\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-yxwnvabe/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-yxwnvabe/repo\", \"--revision\", \"fa492acc6a0bf2008b66cd01efaae90e9edba8ff\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-yxwnvabe/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-yxwnvabe/repo\", \"--revision\", \"2afbdf6d90a5d6cbdc7f2ecefec27957e5ccea67\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-yxwnvabe/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-yxwnvabe/repo\", \"--revision\", \"ed5809d174b69982e16ca6ea98740fe5bd24ee36\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.017
      },
      "verdict": "killed"
    },
    {
      "id": "C2-13",
      "script": "measure_c2.py",
      "check": "fetchedAt is a string",
      "pattern": "not isinstance(fetch.get(\"fetchedAt\"), str)",
      "replacement": "False",
      "expected": "survived",
      "expectationReason": "No selftest fixture invalidates this check.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-yxwnvabe/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-yxwnvabe/repo\", \"--revision\", \"98a975310008ed5817a7857c1aa8652d73a94cd6\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-yxwnvabe/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-yxwnvabe/repo\", \"--revision\", \"98a975310008ed5817a7857c1aa8652d73a94cd6\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-yxwnvabe/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-yxwnvabe/repo\", \"--revision\", \"f09628011232539760c88ed40bb2bd2908dcde37\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-yxwnvabe/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-yxwnvabe/repo\", \"--revision\", \"52d9e77782365f7cdc47d1ed14d19f06844fdfe9\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-yxwnvabe/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-yxwnvabe/repo\", \"--revision\", \"fa492acc6a0bf2008b66cd01efaae90e9edba8ff\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-yxwnvabe/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-yxwnvabe/repo\", \"--revision\", \"2afbdf6d90a5d6cbdc7f2ecefec27957e5ccea67\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-yxwnvabe/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-yxwnvabe/repo\", \"--revision\", \"ed5809d174b69982e16ca6ea98740fe5bd24ee36\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.017
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "798493f648889eb5d0ac965fd117ae486589eee0",
      "mutatedSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "4079d5507ead65ad465919f66bf6c9f3a8576f95eed3c3a93f73115bab059990",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "88b0a093c3def3d57a7f376b33c985cf397f038e",
      "committedMutationSha256": "4079d5507ead65ad465919f66bf6c9f3a8576f95eed3c3a93f73115bab059990",
      "mutated": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-dr2ebh17/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-dr2ebh17/repo\", \"--revision\", \"8b5ec42e63809888ef1005c42faaa5330bb5c2b3\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-dr2ebh17/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-dr2ebh17/repo\", \"--revision\", \"8b5ec42e63809888ef1005c42faaa5330bb5c2b3\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-dr2ebh17/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-dr2ebh17/repo\", \"--revision\", \"d78f347234406faaf0d15eb1f9bd99b441bffb30\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-dr2ebh17/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-dr2ebh17/repo\", \"--revision\", \"1d8753ec3fffe4b417601e19c05f87b2c13755e2\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-dr2ebh17/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-dr2ebh17/repo\", \"--revision\", \"cefbd60e8c3a2a768839b936dbf46d18c47f4843\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-dr2ebh17/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-dr2ebh17/repo\", \"--revision\", \"cc8b0e133745175df111605b37784e31ae2f481e\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-dr2ebh17/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-dr2ebh17/repo\", \"--revision\", \"1a682d1f814e433007fe8145b0185475321e1382\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.037
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "cde69a6b122b53aebfa39a482821762ace59df11",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-0bjljq04/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-0bjljq04/repo\", \"--revision\", \"06fe76689bc912e5e157d94a24f4c4599d385bbd\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-0bjljq04/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-0bjljq04/repo\", \"--revision\", \"06fe76689bc912e5e157d94a24f4c4599d385bbd\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-0bjljq04/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-0bjljq04/repo\", \"--revision\", \"6bda04602f2d8ad7907d239dc97cd39dc498cf1d\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-0bjljq04/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-0bjljq04/repo\", \"--revision\", \"bc99d71591c907c12f06d5cd50892c4dedb5964e\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-0bjljq04/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-0bjljq04/repo\", \"--revision\", \"181f634704847aef0677290d5c9bd14c5fa2438c\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-0bjljq04/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-0bjljq04/repo\", \"--revision\", \"f7dee3fe76973a7985ab49010cd1af7a90acb646\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-0bjljq04/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-0bjljq04/repo\", \"--revision\", \"d9a9d30ce6be5d8a5ea638718fbbec42fe371986\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.016
      },
      "verdict": "survived"
    },
    {
      "id": "C2-14",
      "script": "measure_c2.py",
      "check": "fetchedAt date cutoff",
      "pattern": "fetch[\"fetchedAt\"][:10] < \"2026-10-21\"",
      "replacement": "False",
      "expected": "survived",
      "expectationReason": "No selftest fixture invalidates this check.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-0bjljq04/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-0bjljq04/repo\", \"--revision\", \"06fe76689bc912e5e157d94a24f4c4599d385bbd\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-0bjljq04/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-0bjljq04/repo\", \"--revision\", \"06fe76689bc912e5e157d94a24f4c4599d385bbd\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-0bjljq04/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-0bjljq04/repo\", \"--revision\", \"6bda04602f2d8ad7907d239dc97cd39dc498cf1d\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-0bjljq04/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-0bjljq04/repo\", \"--revision\", \"bc99d71591c907c12f06d5cd50892c4dedb5964e\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-0bjljq04/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-0bjljq04/repo\", \"--revision\", \"181f634704847aef0677290d5c9bd14c5fa2438c\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-0bjljq04/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-0bjljq04/repo\", \"--revision\", \"f7dee3fe76973a7985ab49010cd1af7a90acb646\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-0bjljq04/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-0bjljq04/repo\", \"--revision\", \"d9a9d30ce6be5d8a5ea638718fbbec42fe371986\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.016
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "cde69a6b122b53aebfa39a482821762ace59df11",
      "mutatedSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec72ece7fb0d9ec2abdf9b73e821f05606a2646395c203637f6dabc7d0b88062",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "e7ed633910d945dc09356f4185cbb62bc2cc439b",
      "committedMutationSha256": "ec72ece7fb0d9ec2abdf9b73e821f05606a2646395c203637f6dabc7d0b88062",
      "mutated": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-zl8_sng4/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-zl8_sng4/repo\", \"--revision\", \"af1327158c0cc0c934e5d2a57828f8e78f33bb00\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-zl8_sng4/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-zl8_sng4/repo\", \"--revision\", \"af1327158c0cc0c934e5d2a57828f8e78f33bb00\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-zl8_sng4/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-zl8_sng4/repo\", \"--revision\", \"c3b32866722f5c863b99fff4d83fd5a324ad5419\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-zl8_sng4/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-zl8_sng4/repo\", \"--revision\", \"1ac278a8159fa190e5c3c3ec43e052e4b09a54c3\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-zl8_sng4/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-zl8_sng4/repo\", \"--revision\", \"f536931d368a05af203b342dc886006e5e6ab3ab\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-zl8_sng4/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-zl8_sng4/repo\", \"--revision\", \"a6086ead86bd3edea1fdbdae9d55cafcc8af11ad\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-zl8_sng4/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-zl8_sng4/repo\", \"--revision\", \"6486ec629b5a98fff359d5ff94e71ca10b7265af\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.016
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "3cb9d911fd880aa50ae26cedfe351ae6456757b9",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-49c_s22g/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-49c_s22g/repo\", \"--revision\", \"6dc934897f6b7391e5df6c8b1eee95a4c143136f\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-49c_s22g/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-49c_s22g/repo\", \"--revision\", \"6dc934897f6b7391e5df6c8b1eee95a4c143136f\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-49c_s22g/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-49c_s22g/repo\", \"--revision\", \"f198f42d08e3706566a505045680254fb330f3f0\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-49c_s22g/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-49c_s22g/repo\", \"--revision\", \"e8d649de9d36c63b156b97b6a763602f10b7b68a\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-49c_s22g/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-49c_s22g/repo\", \"--revision\", \"f0331b4155c78df772b6de8929f531301798ad22\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-49c_s22g/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-49c_s22g/repo\", \"--revision\", \"37d34a6f2a7b1eb6521149c2ef27bfb8a72c3ad9\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-49c_s22g/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-49c_s22g/repo\", \"--revision\", \"5944ba52e13540cfcb4d9ec9599b521b109132f4\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.024
      },
      "verdict": "survived"
    },
    {
      "id": "C2-15",
      "script": "measure_c2.py",
      "check": "Non-served branch dispatch",
      "pattern": "not served(fetch)",
      "replacement": "False",
      "expected": "killed",
      "expectationReason": "The valid 404 fixture would fall through to missing page/digest rejection.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-49c_s22g/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-49c_s22g/repo\", \"--revision\", \"6dc934897f6b7391e5df6c8b1eee95a4c143136f\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-49c_s22g/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-49c_s22g/repo\", \"--revision\", \"6dc934897f6b7391e5df6c8b1eee95a4c143136f\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-49c_s22g/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-49c_s22g/repo\", \"--revision\", \"f198f42d08e3706566a505045680254fb330f3f0\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-49c_s22g/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-49c_s22g/repo\", \"--revision\", \"e8d649de9d36c63b156b97b6a763602f10b7b68a\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-49c_s22g/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-49c_s22g/repo\", \"--revision\", \"f0331b4155c78df772b6de8929f531301798ad22\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-49c_s22g/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-49c_s22g/repo\", \"--revision\", \"37d34a6f2a7b1eb6521149c2ef27bfb8a72c3ad9\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-49c_s22g/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-49c_s22g/repo\", \"--revision\", \"5944ba52e13540cfcb4d9ec9599b521b109132f4\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.024
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "3cb9d911fd880aa50ae26cedfe351ae6456757b9",
      "mutatedSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "8524505132739c8fd3f53ce50b3aaaad3ca267deb0d25a722a97b31d9c5b7cfb",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "3dfb2f681daf2c0e25f52d42079a0f0821d078be",
      "committedMutationSha256": "8524505132739c8fd3f53ce50b3aaaad3ca267deb0d25a722a97b31d9c5b7cfb",
      "mutated": {
        "exit": 1,
        "stdout": "",
        "stderr": "counter_selftest: {\"accepted\": 11, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-bqj04in7/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-bqj04in7/repo\", \"--revision\", \"dae4050cce317c643fa5d69ec2b23a831fb31976\"], \"errors\": [\"exit 1, expected 0\", \"accepted 11, expected 12\", \"failed rows ['charter-kimi'], expected []\", \"non-served target 'charter-kimi' did not report not-served\"], \"exit\": 1, \"expectedAccepted\": 12, \"expectedExit\": 0, \"output\": {\"accepted\": 11, \"revision\": \"dae4050cce317c643fa5d69ec2b23a831fb31976\", \"surfaces\": [{\"id\": \"ds4cc-primary\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"plazir15-ghp\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"charter-ghp\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"ds4cc-kimi\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"burnerchrome-kimi\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"vault-index-kimi\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"plazir27-kimi\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"ufo-fsd-kimi-pro\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"lucario-ghp\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"lucario-kimi\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"plazir15-kimi\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"charter-kimi\", \"pass\": false, \"problems\": [\"page.html missing or digest differs from fetch.sha256\"], \"verdict\": null}], \"total\": 12, \"validatorSha256\": \"062ccc4db6ab506ecb274ac0da4e4c4e9041462562e23cc586a0168cc8e44387\"}, \"passed\": false, \"stderr\": \"\", \"total\": 12}\n",
        "elapsedSeconds": 0.953
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "6c3ac0a27b00164d8be333d930a4765a9ddf7b5f",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ui0nfpmk/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ui0nfpmk/repo\", \"--revision\", \"130e918b72525268778411781fb42ca6eacabbac\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ui0nfpmk/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ui0nfpmk/repo\", \"--revision\", \"130e918b72525268778411781fb42ca6eacabbac\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ui0nfpmk/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ui0nfpmk/repo\", \"--revision\", \"1dad297ba6c84a008fa346bb2558ea1dca0675d3\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ui0nfpmk/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ui0nfpmk/repo\", \"--revision\", \"9a7ed29d2407c70d4e4597f6e5847b4147835892\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ui0nfpmk/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ui0nfpmk/repo\", \"--revision\", \"1567b0de505bffade950660211346b3c9301dfda\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ui0nfpmk/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ui0nfpmk/repo\", \"--revision\", \"fba5c2c127cb4c867bdae74215f958eb6ef590e8\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ui0nfpmk/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ui0nfpmk/repo\", \"--revision\", \"a32a48758257e4dccac47ae7321c85fa2e30db64\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.009
      },
      "verdict": "killed"
    },
    {
      "id": "C2-16",
      "script": "measure_c2.py",
      "check": "Non-served response has no page",
      "pattern": "page is not None",
      "replacement": "False",
      "expected": "survived",
      "expectationReason": "No selftest fixture invalidates this check.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ui0nfpmk/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ui0nfpmk/repo\", \"--revision\", \"130e918b72525268778411781fb42ca6eacabbac\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ui0nfpmk/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ui0nfpmk/repo\", \"--revision\", \"130e918b72525268778411781fb42ca6eacabbac\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ui0nfpmk/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ui0nfpmk/repo\", \"--revision\", \"1dad297ba6c84a008fa346bb2558ea1dca0675d3\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ui0nfpmk/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ui0nfpmk/repo\", \"--revision\", \"9a7ed29d2407c70d4e4597f6e5847b4147835892\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ui0nfpmk/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ui0nfpmk/repo\", \"--revision\", \"1567b0de505bffade950660211346b3c9301dfda\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ui0nfpmk/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ui0nfpmk/repo\", \"--revision\", \"fba5c2c127cb4c867bdae74215f958eb6ef590e8\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ui0nfpmk/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ui0nfpmk/repo\", \"--revision\", \"a32a48758257e4dccac47ae7321c85fa2e30db64\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.009
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "6c3ac0a27b00164d8be333d930a4765a9ddf7b5f",
      "mutatedSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "af5821f85d28e85cb0df26077993ff1183cb3b9f6ba5b189a8338e9e8e6f92f2",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "742f22792009f260a01c42ade8c3c584b4b07d69",
      "committedMutationSha256": "af5821f85d28e85cb0df26077993ff1183cb3b9f6ba5b189a8338e9e8e6f92f2",
      "mutated": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-tfbmfcgr/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-tfbmfcgr/repo\", \"--revision\", \"6a067df74e64018c46200384dc9b470843bb6871\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-tfbmfcgr/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-tfbmfcgr/repo\", \"--revision\", \"6a067df74e64018c46200384dc9b470843bb6871\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-tfbmfcgr/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-tfbmfcgr/repo\", \"--revision\", \"ac4a7f2e2248bf2b38ead5ab05a583508a3318cd\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-tfbmfcgr/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-tfbmfcgr/repo\", \"--revision\", \"64271397771b58f783ba57aeadf2b21f65fcdc7b\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-tfbmfcgr/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-tfbmfcgr/repo\", \"--revision\", \"ce7970bccff5f8c8715931c64a878697f52eb2a5\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-tfbmfcgr/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-tfbmfcgr/repo\", \"--revision\", \"5f43820a10c4c45a6d152d1cad90192445128724\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-tfbmfcgr/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-tfbmfcgr/repo\", \"--revision\", \"32845ec46d4d2fd30f24bf742bf267e6779349a3\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.041
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "027ed41ed827528b12da9dcd7af819dabf79e2d8",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-bct__ht3/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-bct__ht3/repo\", \"--revision\", \"9c9611e24af8f44aefedb427c830081ce0fd3ad6\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-bct__ht3/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-bct__ht3/repo\", \"--revision\", \"9c9611e24af8f44aefedb427c830081ce0fd3ad6\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-bct__ht3/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-bct__ht3/repo\", \"--revision\", \"a429c9d2b85424c432a082bae5f6d4ecbb2c8470\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-bct__ht3/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-bct__ht3/repo\", \"--revision\", \"4777b9a7489725c6059f4daf014f251d94ddbae2\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-bct__ht3/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-bct__ht3/repo\", \"--revision\", \"2a0ff2a5377bc9c292c3b86479a05c3ea407fc39\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-bct__ht3/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-bct__ht3/repo\", \"--revision\", \"a11f09c2647c4b5e596d0ea09797bb190381a3c3\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-bct__ht3/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-bct__ht3/repo\", \"--revision\", \"aa170905a785a1cce1280550dacbd505706db318\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.161
      },
      "verdict": "survived"
    },
    {
      "id": "C2-17",
      "script": "measure_c2.py",
      "check": "Non-served receipt verdict",
      "pattern": "receipt.get(\"verdict\") != \"not-served\"",
      "replacement": "False",
      "expected": "survived",
      "expectationReason": "No selftest fixture invalidates this check.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-bct__ht3/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-bct__ht3/repo\", \"--revision\", \"9c9611e24af8f44aefedb427c830081ce0fd3ad6\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-bct__ht3/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-bct__ht3/repo\", \"--revision\", \"9c9611e24af8f44aefedb427c830081ce0fd3ad6\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-bct__ht3/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-bct__ht3/repo\", \"--revision\", \"a429c9d2b85424c432a082bae5f6d4ecbb2c8470\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-bct__ht3/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-bct__ht3/repo\", \"--revision\", \"4777b9a7489725c6059f4daf014f251d94ddbae2\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-bct__ht3/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-bct__ht3/repo\", \"--revision\", \"2a0ff2a5377bc9c292c3b86479a05c3ea407fc39\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-bct__ht3/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-bct__ht3/repo\", \"--revision\", \"a11f09c2647c4b5e596d0ea09797bb190381a3c3\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-bct__ht3/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-bct__ht3/repo\", \"--revision\", \"aa170905a785a1cce1280550dacbd505706db318\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.161
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "027ed41ed827528b12da9dcd7af819dabf79e2d8",
      "mutatedSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "0ef6a6bb65489648beff33d201a1510b554d25bfc558e55a8b891d2feaf13c4e",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "bcdcf95ccc96bd3d91d8992a7dc3b6d63137cd39",
      "committedMutationSha256": "0ef6a6bb65489648beff33d201a1510b554d25bfc558e55a8b891d2feaf13c4e",
      "mutated": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-2yycujaz/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-2yycujaz/repo\", \"--revision\", \"f5ac6029dfe6fc9e6f84ce23166c08636f868e12\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-2yycujaz/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-2yycujaz/repo\", \"--revision\", \"f5ac6029dfe6fc9e6f84ce23166c08636f868e12\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-2yycujaz/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-2yycujaz/repo\", \"--revision\", \"2f0776c0effb5870b96878c4e7b14ab97f7fc5c2\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-2yycujaz/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-2yycujaz/repo\", \"--revision\", \"be226c4ad16cffce453c5d49fd3a608816cee0c8\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-2yycujaz/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-2yycujaz/repo\", \"--revision\", \"7dd28490d08c4b17a1e6cb143c74efa8845722c2\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-2yycujaz/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-2yycujaz/repo\", \"--revision\", \"9073fcef3c4b6b049a13fc7da79e1c75cf6d1a05\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-2yycujaz/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-2yycujaz/repo\", \"--revision\", \"7b826c44f944dcea17616648c9c93dffc0f3bbea\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.178
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "968932c1176dcd7ff7becd568308563c69b6bf40",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-jd61gv8w/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-jd61gv8w/repo\", \"--revision\", \"8afba91394b50e41703957990e7fe570f3fb7678\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-jd61gv8w/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-jd61gv8w/repo\", \"--revision\", \"8afba91394b50e41703957990e7fe570f3fb7678\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-jd61gv8w/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-jd61gv8w/repo\", \"--revision\", \"82c43338f82ddd95d1d5ab72f21345776a2c729e\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-jd61gv8w/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-jd61gv8w/repo\", \"--revision\", \"67113b7e540c0cb7af388588ba9bf1a30b3f18b2\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-jd61gv8w/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-jd61gv8w/repo\", \"--revision\", \"b6e56ecc70c85470758d1c949bd6fcb63affd57d\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-jd61gv8w/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-jd61gv8w/repo\", \"--revision\", \"148dd5eebd9b800cdae4c2185862f1eeb491695c\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-jd61gv8w/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-jd61gv8w/repo\", \"--revision\", \"f78ed1266dd1102d1ee33e1c69632613f0a50415\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.208
      },
      "verdict": "survived"
    },
    {
      "id": "C2-18",
      "script": "measure_c2.py",
      "check": "Non-served receipt status matches",
      "pattern": "receipt.get(\"status\") != fetch.get(\"status\")",
      "replacement": "False",
      "expected": "survived",
      "expectationReason": "No selftest fixture invalidates this check.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-jd61gv8w/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-jd61gv8w/repo\", \"--revision\", \"8afba91394b50e41703957990e7fe570f3fb7678\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-jd61gv8w/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-jd61gv8w/repo\", \"--revision\", \"8afba91394b50e41703957990e7fe570f3fb7678\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-jd61gv8w/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-jd61gv8w/repo\", \"--revision\", \"82c43338f82ddd95d1d5ab72f21345776a2c729e\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-jd61gv8w/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-jd61gv8w/repo\", \"--revision\", \"67113b7e540c0cb7af388588ba9bf1a30b3f18b2\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-jd61gv8w/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-jd61gv8w/repo\", \"--revision\", \"b6e56ecc70c85470758d1c949bd6fcb63affd57d\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-jd61gv8w/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-jd61gv8w/repo\", \"--revision\", \"148dd5eebd9b800cdae4c2185862f1eeb491695c\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-jd61gv8w/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-jd61gv8w/repo\", \"--revision\", \"f78ed1266dd1102d1ee33e1c69632613f0a50415\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.208
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "968932c1176dcd7ff7becd568308563c69b6bf40",
      "mutatedSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "88e7c5bd07b10c66f591e607419ceee39f266632c825be5ead167c0f315b093e",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "b6aa26d2802b3ea4d755a51cf704a091f759b8b0",
      "committedMutationSha256": "88e7c5bd07b10c66f591e607419ceee39f266632c825be5ead167c0f315b093e",
      "mutated": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xebk5wr1/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xebk5wr1/repo\", \"--revision\", \"1f366ef280c7b9e4516ac1b5b86b21d62f17dcb8\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xebk5wr1/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xebk5wr1/repo\", \"--revision\", \"1f366ef280c7b9e4516ac1b5b86b21d62f17dcb8\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xebk5wr1/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xebk5wr1/repo\", \"--revision\", \"3a5266bb5a512c69654f0ea46b0611323fa6fd7b\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xebk5wr1/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xebk5wr1/repo\", \"--revision\", \"bac8fd3e7d14e11126dca50a4d868226446edce7\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xebk5wr1/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xebk5wr1/repo\", \"--revision\", \"be979f3b44e0da8da9daeb704d6a10e277336b72\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xebk5wr1/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xebk5wr1/repo\", \"--revision\", \"09cdb4064a9b42df281abf2660af2bcec603a974\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xebk5wr1/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xebk5wr1/repo\", \"--revision\", \"18ff2e072db0c0f2b8e3b2662a2c4e36895b07a0\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.244
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "a5beda796f1d6dd808ed3fa0386bb8e537b33c2c",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-jav4vh0b/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-jav4vh0b/repo\", \"--revision\", \"f3e2d9b5aa1e6ab09d28b5b2cb82e3c3bff1f0fd\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-jav4vh0b/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-jav4vh0b/repo\", \"--revision\", \"f3e2d9b5aa1e6ab09d28b5b2cb82e3c3bff1f0fd\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-jav4vh0b/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-jav4vh0b/repo\", \"--revision\", \"c47821706f69f075099d6082b5ceeff09dcda62d\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-jav4vh0b/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-jav4vh0b/repo\", \"--revision\", \"5153da429bf79a69743dae63c2a1952882f54f7b\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-jav4vh0b/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-jav4vh0b/repo\", \"--revision\", \"baddef4c7f0ffa2dfc333990ca09d8634c79695e\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-jav4vh0b/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-jav4vh0b/repo\", \"--revision\", \"5469d22f5f41a88b58a6ff88587022a9db2dd8e9\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-jav4vh0b/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-jav4vh0b/repo\", \"--revision\", \"6be41b1fce470929b70cef5097ce5c9bb518899a\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.302
      },
      "verdict": "survived"
    },
    {
      "id": "C2-19",
      "script": "measure_c2.py",
      "check": "Served page bytes present",
      "pattern": "page is None",
      "replacement": "False",
      "expected": "survived",
      "expectationReason": "No selftest fixture invalidates this check.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-jav4vh0b/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-jav4vh0b/repo\", \"--revision\", \"f3e2d9b5aa1e6ab09d28b5b2cb82e3c3bff1f0fd\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-jav4vh0b/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-jav4vh0b/repo\", \"--revision\", \"f3e2d9b5aa1e6ab09d28b5b2cb82e3c3bff1f0fd\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-jav4vh0b/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-jav4vh0b/repo\", \"--revision\", \"c47821706f69f075099d6082b5ceeff09dcda62d\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-jav4vh0b/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-jav4vh0b/repo\", \"--revision\", \"5153da429bf79a69743dae63c2a1952882f54f7b\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-jav4vh0b/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-jav4vh0b/repo\", \"--revision\", \"baddef4c7f0ffa2dfc333990ca09d8634c79695e\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-jav4vh0b/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-jav4vh0b/repo\", \"--revision\", \"5469d22f5f41a88b58a6ff88587022a9db2dd8e9\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-jav4vh0b/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-jav4vh0b/repo\", \"--revision\", \"6be41b1fce470929b70cef5097ce5c9bb518899a\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.302
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "a5beda796f1d6dd808ed3fa0386bb8e537b33c2c",
      "mutatedSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "3e1227ad22740a111d46f26bbaedb34e8e2742fe1435db194b526f86ab7d5e77",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "b874a85543fc1c9c8a182edb53bfdf96855ed176",
      "committedMutationSha256": "3e1227ad22740a111d46f26bbaedb34e8e2742fe1435db194b526f86ab7d5e77",
      "mutated": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-o230apha/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-o230apha/repo\", \"--revision\", \"2154f7c2de9878bd6d3b04342ea8faa783eaabc1\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-o230apha/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-o230apha/repo\", \"--revision\", \"2154f7c2de9878bd6d3b04342ea8faa783eaabc1\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-o230apha/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-o230apha/repo\", \"--revision\", \"2716dc093c58f4e93112a9f64b94dfe137739536\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-o230apha/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-o230apha/repo\", \"--revision\", \"135d3bf6bf896f8d99399527b24f7b110d8cfa93\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-o230apha/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-o230apha/repo\", \"--revision\", \"3bf49df3444d2400080c2ff5307b4f314ec113c8\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-o230apha/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-o230apha/repo\", \"--revision\", \"1bc21bf99bcc2dff3991b086ca416965e408165c\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-o230apha/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-o230apha/repo\", \"--revision\", \"f5487c55b29ee05cd6b874f6d1c442f971533eb2\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.223
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "86e437996787d8e1a684659e1320fafe7e4a073f",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-qmarhyac/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-qmarhyac/repo\", \"--revision\", \"8e6ee269911d915fccad42d513a56bbd51482154\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-qmarhyac/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-qmarhyac/repo\", \"--revision\", \"8e6ee269911d915fccad42d513a56bbd51482154\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-qmarhyac/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-qmarhyac/repo\", \"--revision\", \"216b631f1ac36d1fc1865bc01149555ac5f828ba\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-qmarhyac/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-qmarhyac/repo\", \"--revision\", \"2be43794c24f5793b5d22ca3ec8b9c197e63b681\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-qmarhyac/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-qmarhyac/repo\", \"--revision\", \"b253f26172a6432072894570c8508c6b73edd15e\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-qmarhyac/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-qmarhyac/repo\", \"--revision\", \"0d98a3a77b537ba4f7a5274a4dd437226eabe7bf\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-qmarhyac/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-qmarhyac/repo\", \"--revision\", \"583f41dffded9123efcfc0b8e68145bf0b28f26e\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.244
      },
      "verdict": "survived"
    },
    {
      "id": "C2-20",
      "script": "measure_c2.py",
      "check": "Served page digest matches fetch",
      "pattern": "hashlib.sha256(page).hexdigest() != fetch.get(\"sha256\")",
      "replacement": "False",
      "expected": "survived",
      "expectationReason": "No selftest fixture invalidates this check.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-qmarhyac/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-qmarhyac/repo\", \"--revision\", \"8e6ee269911d915fccad42d513a56bbd51482154\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-qmarhyac/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-qmarhyac/repo\", \"--revision\", \"8e6ee269911d915fccad42d513a56bbd51482154\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-qmarhyac/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-qmarhyac/repo\", \"--revision\", \"216b631f1ac36d1fc1865bc01149555ac5f828ba\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-qmarhyac/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-qmarhyac/repo\", \"--revision\", \"2be43794c24f5793b5d22ca3ec8b9c197e63b681\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-qmarhyac/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-qmarhyac/repo\", \"--revision\", \"b253f26172a6432072894570c8508c6b73edd15e\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-qmarhyac/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-qmarhyac/repo\", \"--revision\", \"0d98a3a77b537ba4f7a5274a4dd437226eabe7bf\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-qmarhyac/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-qmarhyac/repo\", \"--revision\", \"583f41dffded9123efcfc0b8e68145bf0b28f26e\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.244
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "86e437996787d8e1a684659e1320fafe7e4a073f",
      "mutatedSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "3de1d7594b4af741237aff1f2f61b9bb971bf27059b1673b8b8f1e3aa4ef20d5",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "08b57662bc2707ae1be0c03aa7c259dccda8f7ca",
      "committedMutationSha256": "3de1d7594b4af741237aff1f2f61b9bb971bf27059b1673b8b8f1e3aa4ef20d5",
      "mutated": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-gvlyb8be/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-gvlyb8be/repo\", \"--revision\", \"879768312e74a17e0b0a15e17fc5abe3156bba5b\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-gvlyb8be/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-gvlyb8be/repo\", \"--revision\", \"879768312e74a17e0b0a15e17fc5abe3156bba5b\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-gvlyb8be/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-gvlyb8be/repo\", \"--revision\", \"c25489d4f4f499df33234c528a65d5884a0e5263\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-gvlyb8be/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-gvlyb8be/repo\", \"--revision\", \"83499f9fc2b8e47f8c7ba7dac28b2ab012308bd5\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-gvlyb8be/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-gvlyb8be/repo\", \"--revision\", \"1366d7c8b809398ed4b8f4c2cb69457b5a8f205b\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-gvlyb8be/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-gvlyb8be/repo\", \"--revision\", \"c0ba4ec2d1932f440caf4690db06dad41d680193\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-gvlyb8be/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-gvlyb8be/repo\", \"--revision\", \"952f03ac63fd299089971d0a9eb03f4560f65ccd\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.19
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "244f9d064e6f706c1b714e505d01df0f9f09c53f",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-lqb0mm4l/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-lqb0mm4l/repo\", \"--revision\", \"9115e40e07f36e2278b365954dd7486e9aec187b\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-lqb0mm4l/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-lqb0mm4l/repo\", \"--revision\", \"9115e40e07f36e2278b365954dd7486e9aec187b\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-lqb0mm4l/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-lqb0mm4l/repo\", \"--revision\", \"0d38a70489c1820f4d425064ad185784eab630e1\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-lqb0mm4l/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-lqb0mm4l/repo\", \"--revision\", \"3e9c97a4963c66df171162e6be2d650adee9a621\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-lqb0mm4l/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-lqb0mm4l/repo\", \"--revision\", \"67c0190aa99ae20def7aa3399d6554462da8cbae\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-lqb0mm4l/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-lqb0mm4l/repo\", \"--revision\", \"bfeb89529ba8cca35832c212e5906c21535fa347\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-lqb0mm4l/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-lqb0mm4l/repo\", \"--revision\", \"ef51d123274b990d82690a3b7dc0b6539ce39af7\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.189
      },
      "verdict": "survived"
    },
    {
      "id": "C2-21",
      "script": "measure_c2.py",
      "check": "Validator emits JSON rejection",
      "pattern": "return problems + [\"validator did not emit JSON\"], None",
      "replacement": "return problems, None",
      "expected": "survived",
      "expectationReason": "No selftest fixture invalidates this check.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-lqb0mm4l/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-lqb0mm4l/repo\", \"--revision\", \"9115e40e07f36e2278b365954dd7486e9aec187b\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-lqb0mm4l/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-lqb0mm4l/repo\", \"--revision\", \"9115e40e07f36e2278b365954dd7486e9aec187b\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-lqb0mm4l/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-lqb0mm4l/repo\", \"--revision\", \"0d38a70489c1820f4d425064ad185784eab630e1\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-lqb0mm4l/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-lqb0mm4l/repo\", \"--revision\", \"3e9c97a4963c66df171162e6be2d650adee9a621\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-lqb0mm4l/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-lqb0mm4l/repo\", \"--revision\", \"67c0190aa99ae20def7aa3399d6554462da8cbae\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-lqb0mm4l/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-lqb0mm4l/repo\", \"--revision\", \"bfeb89529ba8cca35832c212e5906c21535fa347\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-lqb0mm4l/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-lqb0mm4l/repo\", \"--revision\", \"ef51d123274b990d82690a3b7dc0b6539ce39af7\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.189
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "244f9d064e6f706c1b714e505d01df0f9f09c53f",
      "mutatedSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "74962a273f5ca34698b83adf6c6e65178bad87c4e9c2065efa12816e0c61c8a4",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "979700c107388dc3224bb0605f1ec41d794f0fa1",
      "committedMutationSha256": "74962a273f5ca34698b83adf6c6e65178bad87c4e9c2065efa12816e0c61c8a4",
      "mutated": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-rlcb0989/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-rlcb0989/repo\", \"--revision\", \"1db6d6351531df9fd10ae1ac88d5b589cce53680\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-rlcb0989/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-rlcb0989/repo\", \"--revision\", \"1db6d6351531df9fd10ae1ac88d5b589cce53680\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-rlcb0989/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-rlcb0989/repo\", \"--revision\", \"63e6f66b2a58b06f42dddce97e6128178ae623d6\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-rlcb0989/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-rlcb0989/repo\", \"--revision\", \"9598139fcdd70e2a11b943e9e31656cbf7053270\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-rlcb0989/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-rlcb0989/repo\", \"--revision\", \"abea99c44387c73098db904c66b49547f2d1b028\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-rlcb0989/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-rlcb0989/repo\", \"--revision\", \"516c8c3c195b6728e79a7d347de2de057bd3044e\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-rlcb0989/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-rlcb0989/repo\", \"--revision\", \"d049e52e0cd3c496e3a12bbb7ad628e0db54514a\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.206
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "fd71d5cd638d6a3d4a3314ad78acc9dffbfa3ea1",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-vv_qa2e9/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-vv_qa2e9/repo\", \"--revision\", \"1f936e6069af680f2a1a5141a377057c8653101b\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-vv_qa2e9/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-vv_qa2e9/repo\", \"--revision\", \"1f936e6069af680f2a1a5141a377057c8653101b\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-vv_qa2e9/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-vv_qa2e9/repo\", \"--revision\", \"3d530041e14bd9e90223795e62056bb79e9441b8\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-vv_qa2e9/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-vv_qa2e9/repo\", \"--revision\", \"daa8eb57114fc1cb1dae058483357c0260aceb2a\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-vv_qa2e9/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-vv_qa2e9/repo\", \"--revision\", \"e3a8c4a161a17e84556362bfe544ebe9be0e4520\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-vv_qa2e9/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-vv_qa2e9/repo\", \"--revision\", \"4ba3b42bc2fe98f8d60a5c35b0c46b249e20ed5a\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-vv_qa2e9/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-vv_qa2e9/repo\", \"--revision\", \"8263178646c1e44fa6dd4ef89add288b2bb4378d\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.139
      },
      "verdict": "survived"
    },
    {
      "id": "C2-22",
      "script": "measure_c2.py",
      "check": "Stored audit equals reproduced audit",
      "pattern": "receipt != actual",
      "replacement": "False",
      "expected": "killed",
      "expectationReason": "The unreproducible-audit fixture changes verdict and expects one rejected surface.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-vv_qa2e9/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-vv_qa2e9/repo\", \"--revision\", \"1f936e6069af680f2a1a5141a377057c8653101b\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-vv_qa2e9/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-vv_qa2e9/repo\", \"--revision\", \"1f936e6069af680f2a1a5141a377057c8653101b\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-vv_qa2e9/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-vv_qa2e9/repo\", \"--revision\", \"3d530041e14bd9e90223795e62056bb79e9441b8\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-vv_qa2e9/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-vv_qa2e9/repo\", \"--revision\", \"daa8eb57114fc1cb1dae058483357c0260aceb2a\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-vv_qa2e9/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-vv_qa2e9/repo\", \"--revision\", \"e3a8c4a161a17e84556362bfe544ebe9be0e4520\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-vv_qa2e9/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-vv_qa2e9/repo\", \"--revision\", \"4ba3b42bc2fe98f8d60a5c35b0c46b249e20ed5a\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-vv_qa2e9/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-vv_qa2e9/repo\", \"--revision\", \"8263178646c1e44fa6dd4ef89add288b2bb4378d\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.139
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "fd71d5cd638d6a3d4a3314ad78acc9dffbfa3ea1",
      "mutatedSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "bb20d6dc24917cfdb910e5d41ad0899b0d49b6d38f0477b9d9f4baa13b764ff6",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "3218422da332205d0bb7f1705c9f7ea79a640af7",
      "committedMutationSha256": "bb20d6dc24917cfdb910e5d41ad0899b0d49b6d38f0477b9d9f4baa13b764ff6",
      "mutated": {
        "exit": 1,
        "stdout": "",
        "stderr": "counter_selftest: {\"accepted\": 12, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-sv5350cn/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-sv5350cn/repo\", \"--revision\", \"9b8dcea0b6ba0b5e253f417d7a5848cdfc845f3a\"], \"errors\": [\"exit 0, expected 1\", \"accepted 12, expected 11\", \"failed rows [], expected ['ds4cc-primary']\", \"target 'ds4cc-primary' lacks problem 'audit.json'\"], \"exit\": 0, \"expectedAccepted\": 11, \"expectedExit\": 1, \"output\": {\"accepted\": 12, \"revision\": \"9b8dcea0b6ba0b5e253f417d7a5848cdfc845f3a\", \"surfaces\": [{\"id\": \"ds4cc-primary\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"plazir15-ghp\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"charter-ghp\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"ds4cc-kimi\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"burnerchrome-kimi\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"vault-index-kimi\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"plazir27-kimi\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"ufo-fsd-kimi-pro\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"lucario-ghp\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"lucario-kimi\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"plazir15-kimi\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"charter-kimi\", \"pass\": true, \"problems\": [], \"verdict\": \"not-served\"}], \"total\": 12, \"validatorSha256\": \"062ccc4db6ab506ecb274ac0da4e4c4e9041462562e23cc586a0168cc8e44387\"}, \"passed\": false, \"stderr\": \"\", \"total\": 12}\n",
        "elapsedSeconds": 1.617
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "ab58b9f582c644c763106290a85644a6b1e23c70",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-m1u72oeb/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-m1u72oeb/repo\", \"--revision\", \"3ed4a52993d27e40c6802941b03d3cabfad4c5a8\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-m1u72oeb/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-m1u72oeb/repo\", \"--revision\", \"3ed4a52993d27e40c6802941b03d3cabfad4c5a8\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-m1u72oeb/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-m1u72oeb/repo\", \"--revision\", \"0fe396667f490baf7e6b818dbf0b6b596a735c46\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-m1u72oeb/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-m1u72oeb/repo\", \"--revision\", \"edd7c268664ecf6863336cd0037312a4ef778ced\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-m1u72oeb/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-m1u72oeb/repo\", \"--revision\", \"c076ac65131e2c2ad10113de3a162b883cf716e6\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-m1u72oeb/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-m1u72oeb/repo\", \"--revision\", \"dcb261826e4362490367b06264f46cfa007058b6\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-m1u72oeb/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-m1u72oeb/repo\", \"--revision\", \"2133e3b77b789db0f23c2a6c1a08e4c5bd3e1576\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.19
      },
      "verdict": "killed"
    },
    {
      "id": "C2-23",
      "script": "measure_c2.py",
      "check": "Revision resolves to a commit",
      "pattern": "resolved.returncode != 0",
      "replacement": "False",
      "expected": "survived",
      "expectationReason": "No selftest fixture invalidates this check.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-m1u72oeb/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-m1u72oeb/repo\", \"--revision\", \"3ed4a52993d27e40c6802941b03d3cabfad4c5a8\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-m1u72oeb/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-m1u72oeb/repo\", \"--revision\", \"3ed4a52993d27e40c6802941b03d3cabfad4c5a8\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-m1u72oeb/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-m1u72oeb/repo\", \"--revision\", \"0fe396667f490baf7e6b818dbf0b6b596a735c46\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-m1u72oeb/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-m1u72oeb/repo\", \"--revision\", \"edd7c268664ecf6863336cd0037312a4ef778ced\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-m1u72oeb/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-m1u72oeb/repo\", \"--revision\", \"c076ac65131e2c2ad10113de3a162b883cf716e6\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-m1u72oeb/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-m1u72oeb/repo\", \"--revision\", \"dcb261826e4362490367b06264f46cfa007058b6\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-m1u72oeb/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-m1u72oeb/repo\", \"--revision\", \"2133e3b77b789db0f23c2a6c1a08e4c5bd3e1576\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.19
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "ab58b9f582c644c763106290a85644a6b1e23c70",
      "mutatedSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "4583401ed50aafa316a978038e587c2f74824e6645a8de8d0564943cd41a7a2b",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "644cda9a44b55cbfb0b678ad12076d4448f809b8",
      "committedMutationSha256": "4583401ed50aafa316a978038e587c2f74824e6645a8de8d0564943cd41a7a2b",
      "mutated": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-19wt45_a/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-19wt45_a/repo\", \"--revision\", \"9a321f5675049f3f3f492b6cffdd59af3e1ac2e5\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-19wt45_a/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-19wt45_a/repo\", \"--revision\", \"9a321f5675049f3f3f492b6cffdd59af3e1ac2e5\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-19wt45_a/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-19wt45_a/repo\", \"--revision\", \"198bc6b6432be2cbf9038729dffb75072578599e\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-19wt45_a/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-19wt45_a/repo\", \"--revision\", \"d0865a83e10f8e51f5d9ae8b2cc0e6071f06924e\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-19wt45_a/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-19wt45_a/repo\", \"--revision\", \"b923b452956200c4beb533d0d6acb77bc1545ae0\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-19wt45_a/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-19wt45_a/repo\", \"--revision\", \"a6520e17a8844bd87d3bf084f1fa16a6df29d48e\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-19wt45_a/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-19wt45_a/repo\", \"--revision\", \"90456e67c9b04a9747344e49edfcf42992b5fbd1\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.095
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "e013e8f8546b6b46b9c04f730bf4d41bcae4f49a",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-cdw5zben/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-cdw5zben/repo\", \"--revision\", \"457309671f1b9b4d3b346b7b8c634e19d9d97854\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-cdw5zben/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-cdw5zben/repo\", \"--revision\", \"457309671f1b9b4d3b346b7b8c634e19d9d97854\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-cdw5zben/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-cdw5zben/repo\", \"--revision\", \"370532d1447585a2b982ad410ab703f21265b4ff\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-cdw5zben/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-cdw5zben/repo\", \"--revision\", \"06494880111f84c01ae546f75525c40c986528c7\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-cdw5zben/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-cdw5zben/repo\", \"--revision\", \"92508f57d6456ff13e1f351a561433bf065f9419\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-cdw5zben/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-cdw5zben/repo\", \"--revision\", \"59cf0f45f4c4ba7ab56c4c193da11220d95b840c\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-cdw5zben/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-cdw5zben/repo\", \"--revision\", \"ff9f89e640eca798eb884f80f0fcd48a9025f55b\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.174
      },
      "verdict": "survived"
    },
    {
      "id": "C2-24",
      "script": "measure_c2.py",
      "check": "Population readable",
      "pattern": "population is None",
      "replacement": "False",
      "expected": "survived",
      "expectationReason": "No selftest fixture invalidates this check.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-cdw5zben/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-cdw5zben/repo\", \"--revision\", \"457309671f1b9b4d3b346b7b8c634e19d9d97854\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-cdw5zben/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-cdw5zben/repo\", \"--revision\", \"457309671f1b9b4d3b346b7b8c634e19d9d97854\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-cdw5zben/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-cdw5zben/repo\", \"--revision\", \"370532d1447585a2b982ad410ab703f21265b4ff\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-cdw5zben/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-cdw5zben/repo\", \"--revision\", \"06494880111f84c01ae546f75525c40c986528c7\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-cdw5zben/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-cdw5zben/repo\", \"--revision\", \"92508f57d6456ff13e1f351a561433bf065f9419\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-cdw5zben/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-cdw5zben/repo\", \"--revision\", \"59cf0f45f4c4ba7ab56c4c193da11220d95b840c\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-cdw5zben/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-cdw5zben/repo\", \"--revision\", \"ff9f89e640eca798eb884f80f0fcd48a9025f55b\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.174
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "e013e8f8546b6b46b9c04f730bf4d41bcae4f49a",
      "mutatedSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ae40f2d34e99497f6710192773588b829a8f46af3fbe101a30917363c960a46e",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "aa1194b60de78489c646eae6c717ff26a6d459d1",
      "committedMutationSha256": "ae40f2d34e99497f6710192773588b829a8f46af3fbe101a30917363c960a46e",
      "mutated": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xjyjxom7/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xjyjxom7/repo\", \"--revision\", \"044543c5ed7b3d9d3a53714c2a7121caae5d66da\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xjyjxom7/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xjyjxom7/repo\", \"--revision\", \"044543c5ed7b3d9d3a53714c2a7121caae5d66da\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xjyjxom7/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xjyjxom7/repo\", \"--revision\", \"22a62591dbfc67274cc50615416ff427b13abfc6\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xjyjxom7/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xjyjxom7/repo\", \"--revision\", \"8d4019bd6cc6b681d4948eb81019a9b5d9e78612\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xjyjxom7/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xjyjxom7/repo\", \"--revision\", \"e9e09d5ed86570db8ceb3bfbe46288111c37c41c\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xjyjxom7/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xjyjxom7/repo\", \"--revision\", \"1291ad8ae4c464e2da71e02f9cbf18d180df7cf5\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xjyjxom7/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xjyjxom7/repo\", \"--revision\", \"a0f4915d8b0fc40835535176216cc30af675bfc9\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.163
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "c64ba0abc109c6d8fb9444841fb0ea58334e9887",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-41u4h73o/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-41u4h73o/repo\", \"--revision\", \"ff7341efc2a3e616af0c6493135c1b67cd511d4e\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-41u4h73o/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-41u4h73o/repo\", \"--revision\", \"ff7341efc2a3e616af0c6493135c1b67cd511d4e\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-41u4h73o/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-41u4h73o/repo\", \"--revision\", \"f0324cf9ed1e8d299c741cbaad623691fa441836\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-41u4h73o/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-41u4h73o/repo\", \"--revision\", \"b95e9c14b5375226e1937e57fc95b7a3d51a87a7\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-41u4h73o/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-41u4h73o/repo\", \"--revision\", \"0b71dba8be323580c801a404d3fd8d7c3c67a304\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-41u4h73o/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-41u4h73o/repo\", \"--revision\", \"66830f26b97d7734cbf3bffee21aade3f1aa6838\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-41u4h73o/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-41u4h73o/repo\", \"--revision\", \"9013ac330dcb07836ca08223f7dc4762a988252b\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.197
      },
      "verdict": "survived"
    },
    {
      "id": "C2-25",
      "script": "measure_c2.py",
      "check": "Validator readable",
      "pattern": "validator is None",
      "replacement": "False",
      "expected": "survived",
      "expectationReason": "No selftest fixture invalidates this check.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-41u4h73o/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-41u4h73o/repo\", \"--revision\", \"ff7341efc2a3e616af0c6493135c1b67cd511d4e\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-41u4h73o/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-41u4h73o/repo\", \"--revision\", \"ff7341efc2a3e616af0c6493135c1b67cd511d4e\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-41u4h73o/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-41u4h73o/repo\", \"--revision\", \"f0324cf9ed1e8d299c741cbaad623691fa441836\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-41u4h73o/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-41u4h73o/repo\", \"--revision\", \"b95e9c14b5375226e1937e57fc95b7a3d51a87a7\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-41u4h73o/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-41u4h73o/repo\", \"--revision\", \"0b71dba8be323580c801a404d3fd8d7c3c67a304\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-41u4h73o/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-41u4h73o/repo\", \"--revision\", \"66830f26b97d7734cbf3bffee21aade3f1aa6838\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-41u4h73o/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-41u4h73o/repo\", \"--revision\", \"9013ac330dcb07836ca08223f7dc4762a988252b\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.197
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "c64ba0abc109c6d8fb9444841fb0ea58334e9887",
      "mutatedSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "71e74fc44cbe5b446bb6a6787bc3e045e8544c775134ef44724a4cf9234ccbcf",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "b4db53269e858513fa6eb634602d95e9f23508fa",
      "committedMutationSha256": "71e74fc44cbe5b446bb6a6787bc3e045e8544c775134ef44724a4cf9234ccbcf",
      "mutated": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-b9anw8yr/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-b9anw8yr/repo\", \"--revision\", \"51c4b4ca7bc93bdb1657cfaa942c729056bafdc8\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-b9anw8yr/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-b9anw8yr/repo\", \"--revision\", \"51c4b4ca7bc93bdb1657cfaa942c729056bafdc8\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-b9anw8yr/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-b9anw8yr/repo\", \"--revision\", \"ecb5b8406b3d890799ab082ed5530c0ccbdb15c5\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-b9anw8yr/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-b9anw8yr/repo\", \"--revision\", \"fecd826f022f45f6e96d4ff9a5befda82fee5d31\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-b9anw8yr/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-b9anw8yr/repo\", \"--revision\", \"0a57ebc2389251f99681a554dcd2fa694a8631f2\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-b9anw8yr/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-b9anw8yr/repo\", \"--revision\", \"696f9b2d6246ead365bd6f3bb5e2e3e3a7a24c20\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-b9anw8yr/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-b9anw8yr/repo\", \"--revision\", \"dbc7d838257a0ccfa97d34dc9f9ce937aeeb5402\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.075
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "2243fa9fd47fe921c8716e2474129cc26f82b998",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-l0wj0w5r/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-l0wj0w5r/repo\", \"--revision\", \"65418e43f3e4df5afea7a1660bd01292bb5f484e\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-l0wj0w5r/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-l0wj0w5r/repo\", \"--revision\", \"65418e43f3e4df5afea7a1660bd01292bb5f484e\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-l0wj0w5r/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-l0wj0w5r/repo\", \"--revision\", \"425de029780bd5d71ab6bbcd38ae7fafa79559d8\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-l0wj0w5r/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-l0wj0w5r/repo\", \"--revision\", \"86a38771c5fb8384a45e454e2df68dacb818c007\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-l0wj0w5r/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-l0wj0w5r/repo\", \"--revision\", \"2509a5f9cc36e7d0afaee853c1aeb922763db4b7\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-l0wj0w5r/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-l0wj0w5r/repo\", \"--revision\", \"7c175875a8723546bfa930704b5d7820d2adc836\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-l0wj0w5r/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-l0wj0w5r/repo\", \"--revision\", \"b363ed3c57fff1a8b87106500578ead3ca94e5ad\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.048
      },
      "verdict": "survived"
    },
    {
      "id": "C2-26",
      "script": "measure_c2.py",
      "check": "Frozen population digest",
      "pattern": "hashlib.sha256(population).hexdigest() != POPULATION_SHA256",
      "replacement": "False",
      "expected": "survived",
      "expectationReason": "No selftest fixture invalidates this check.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-l0wj0w5r/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-l0wj0w5r/repo\", \"--revision\", \"65418e43f3e4df5afea7a1660bd01292bb5f484e\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-l0wj0w5r/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-l0wj0w5r/repo\", \"--revision\", \"65418e43f3e4df5afea7a1660bd01292bb5f484e\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-l0wj0w5r/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-l0wj0w5r/repo\", \"--revision\", \"425de029780bd5d71ab6bbcd38ae7fafa79559d8\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-l0wj0w5r/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-l0wj0w5r/repo\", \"--revision\", \"86a38771c5fb8384a45e454e2df68dacb818c007\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-l0wj0w5r/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-l0wj0w5r/repo\", \"--revision\", \"2509a5f9cc36e7d0afaee853c1aeb922763db4b7\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-l0wj0w5r/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-l0wj0w5r/repo\", \"--revision\", \"7c175875a8723546bfa930704b5d7820d2adc836\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-l0wj0w5r/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-l0wj0w5r/repo\", \"--revision\", \"b363ed3c57fff1a8b87106500578ead3ca94e5ad\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.048
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "2243fa9fd47fe921c8716e2474129cc26f82b998",
      "mutatedSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "aac57bcce8f277d7a1e1b5a8a3d16c92035e05b07b3b0dc97246f4711895cc3f",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "aa91eff4dafb095b8b360e2849160636611547b5",
      "committedMutationSha256": "aac57bcce8f277d7a1e1b5a8a3d16c92035e05b07b3b0dc97246f4711895cc3f",
      "mutated": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-__717ev2/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-__717ev2/repo\", \"--revision\", \"b6c9efa66f6bb51a444c798ec97af4e0a9f0934d\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-__717ev2/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-__717ev2/repo\", \"--revision\", \"b6c9efa66f6bb51a444c798ec97af4e0a9f0934d\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-__717ev2/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-__717ev2/repo\", \"--revision\", \"0ce742c17620196f33c7a10f6fe2f8a23c42eb7b\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-__717ev2/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-__717ev2/repo\", \"--revision\", \"afea110473d59b2888304ea70c3e39e10a75a0d0\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-__717ev2/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-__717ev2/repo\", \"--revision\", \"61a101430cd30f4f453aad69ef47cdaa5e7a5cfa\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-__717ev2/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-__717ev2/repo\", \"--revision\", \"141a68245f089132a8405c2bbe008162d3cab1c2\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-__717ev2/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-__717ev2/repo\", \"--revision\", \"4ff3e1fab2236a1fa72d7ed82d31f302059bd7d0\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.055
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "0c3bd89e4ca9000a554cc7f3b1ed1287cc4bd2f8",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xvxuv245/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xvxuv245/repo\", \"--revision\", \"5dc2463ba3b617a642845b22dc8a6a45a7600391\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xvxuv245/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xvxuv245/repo\", \"--revision\", \"5dc2463ba3b617a642845b22dc8a6a45a7600391\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xvxuv245/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xvxuv245/repo\", \"--revision\", \"e523c0b2d430cc22f3d4d94c8f7be0be1650999c\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xvxuv245/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xvxuv245/repo\", \"--revision\", \"5744607bcebd8fb46b7ed2b1bb709f872c10b68c\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xvxuv245/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xvxuv245/repo\", \"--revision\", \"dbea2ee20290b6ea4cb9408e3de80b7ff13cbfe0\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xvxuv245/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xvxuv245/repo\", \"--revision\", \"f919162111aff9c96ef6feaa90fcc66c6f96f33c\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xvxuv245/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xvxuv245/repo\", \"--revision\", \"61c134d28b41b9b96634735a0a666801b373c753\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.065
      },
      "verdict": "survived"
    },
    {
      "id": "C2-27",
      "script": "measure_c2.py",
      "check": "Per-surface acceptance uses problems",
      "pattern": "not problems",
      "replacement": "True",
      "expected": "killed",
      "expectationReason": "The unreproducible-audit fixture must mark the targeted surface failed and decrement accepted.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xvxuv245/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xvxuv245/repo\", \"--revision\", \"5dc2463ba3b617a642845b22dc8a6a45a7600391\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xvxuv245/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xvxuv245/repo\", \"--revision\", \"5dc2463ba3b617a642845b22dc8a6a45a7600391\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xvxuv245/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xvxuv245/repo\", \"--revision\", \"e523c0b2d430cc22f3d4d94c8f7be0be1650999c\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xvxuv245/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xvxuv245/repo\", \"--revision\", \"5744607bcebd8fb46b7ed2b1bb709f872c10b68c\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xvxuv245/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xvxuv245/repo\", \"--revision\", \"dbea2ee20290b6ea4cb9408e3de80b7ff13cbfe0\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xvxuv245/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xvxuv245/repo\", \"--revision\", \"f919162111aff9c96ef6feaa90fcc66c6f96f33c\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-xvxuv245/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-xvxuv245/repo\", \"--revision\", \"61c134d28b41b9b96634735a0a666801b373c753\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.065
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "0c3bd89e4ca9000a554cc7f3b1ed1287cc4bd2f8",
      "mutatedSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "106411a335788b52460c35673256bf5230c046795581b885d1980f0da794c8af",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "f1a5d66fea964c6e295c089828657235e8f2e82b",
      "committedMutationSha256": "106411a335788b52460c35673256bf5230c046795581b885d1980f0da794c8af",
      "mutated": {
        "exit": 1,
        "stdout": "",
        "stderr": "counter_selftest: {\"accepted\": 12, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-gs9ehbq8/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-gs9ehbq8/repo\", \"--revision\", \"50e98ca3b7892faa66ed93a5382eb01d1539dfb8\"], \"errors\": [\"exit 0, expected 1\", \"accepted 12, expected 11\", \"failed rows [], expected ['ds4cc-primary']\"], \"exit\": 0, \"expectedAccepted\": 11, \"expectedExit\": 1, \"output\": {\"accepted\": 12, \"revision\": \"50e98ca3b7892faa66ed93a5382eb01d1539dfb8\", \"surfaces\": [{\"id\": \"ds4cc-primary\", \"pass\": true, \"problems\": [\"audit.json {'exit': 0, 'result': {'findings': [], 'pagesChecked': 1, 'verdict': 'failed-policy'}} != reproduced {'exit': 0, 'result': {'findings': [], 'pagesChecked': 1, 'verdict': 'clean'}}\"], \"verdict\": \"clean\"}, {\"id\": \"plazir15-ghp\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"charter-ghp\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"ds4cc-kimi\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"burnerchrome-kimi\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"vault-index-kimi\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"plazir27-kimi\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"ufo-fsd-kimi-pro\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"lucario-ghp\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"lucario-kimi\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"plazir15-kimi\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"charter-kimi\", \"pass\": true, \"problems\": [], \"verdict\": \"not-served\"}], \"total\": 12, \"validatorSha256\": \"062ccc4db6ab506ecb274ac0da4e4c4e9041462562e23cc586a0168cc8e44387\"}, \"passed\": false, \"stderr\": \"\", \"total\": 12}\n",
        "elapsedSeconds": 1.561
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "a2b83c9fa27ef8014ccf39caefba148d60f5f969",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-7__02vgi/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-7__02vgi/repo\", \"--revision\", \"dbb9569efbbffc998fa637671d96357dbf6defd3\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-7__02vgi/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-7__02vgi/repo\", \"--revision\", \"dbb9569efbbffc998fa637671d96357dbf6defd3\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-7__02vgi/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-7__02vgi/repo\", \"--revision\", \"34fbc95d974df1af4b46d06cc76b386804497359\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-7__02vgi/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-7__02vgi/repo\", \"--revision\", \"d93aa3eff31517148aa8f8d5f770ddf12ef2130f\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-7__02vgi/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-7__02vgi/repo\", \"--revision\", \"e4e2728217193acf2b56c6b36ec6ee3b97d31b23\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-7__02vgi/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-7__02vgi/repo\", \"--revision\", \"a1c440d2e133e4143f49a64be1e635aed8b64499\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-7__02vgi/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-7__02vgi/repo\", \"--revision\", \"c8a806a433bb12d50ee8a48e1f09e6abf31ea53d\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.071
      },
      "verdict": "killed"
    },
    {
      "id": "C2-28",
      "script": "measure_c2.py",
      "check": "Overall exit rejects any failed surface",
      "pattern": "accepted == len(rows)",
      "replacement": "True",
      "expected": "killed",
      "expectationReason": "The unreproducible-audit fixture expects exit 1, not 0.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-7__02vgi/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-7__02vgi/repo\", \"--revision\", \"dbb9569efbbffc998fa637671d96357dbf6defd3\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-7__02vgi/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-7__02vgi/repo\", \"--revision\", \"dbb9569efbbffc998fa637671d96357dbf6defd3\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-7__02vgi/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-7__02vgi/repo\", \"--revision\", \"34fbc95d974df1af4b46d06cc76b386804497359\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-7__02vgi/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-7__02vgi/repo\", \"--revision\", \"d93aa3eff31517148aa8f8d5f770ddf12ef2130f\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-7__02vgi/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-7__02vgi/repo\", \"--revision\", \"e4e2728217193acf2b56c6b36ec6ee3b97d31b23\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-7__02vgi/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-7__02vgi/repo\", \"--revision\", \"a1c440d2e133e4143f49a64be1e635aed8b64499\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-7__02vgi/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-7__02vgi/repo\", \"--revision\", \"c8a806a433bb12d50ee8a48e1f09e6abf31ea53d\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.071
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "a2b83c9fa27ef8014ccf39caefba148d60f5f969",
      "mutatedSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "3da86d0e539e02045127ad2f22605ea3d9d5b4115adf210331910473b0f2f7c1",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "e840c31471c417d7e333ec44bad69d0c0952f386",
      "committedMutationSha256": "3da86d0e539e02045127ad2f22605ea3d9d5b4115adf210331910473b0f2f7c1",
      "mutated": {
        "exit": 1,
        "stdout": "",
        "stderr": "counter_selftest: {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-fgctvj2u/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-fgctvj2u/repo\", \"--revision\", \"8e4765664b348ba3fceb13afb713dfbf8e00088b\"], \"errors\": [\"exit 0, expected 1\"], \"exit\": 0, \"expectedAccepted\": 11, \"expectedExit\": 1, \"output\": {\"accepted\": 11, \"revision\": \"8e4765664b348ba3fceb13afb713dfbf8e00088b\", \"surfaces\": [{\"id\": \"ds4cc-primary\", \"pass\": false, \"problems\": [\"audit.json {'exit': 0, 'result': {'findings': [], 'pagesChecked': 1, 'verdict': 'failed-policy'}} != reproduced {'exit': 0, 'result': {'findings': [], 'pagesChecked': 1, 'verdict': 'clean'}}\"], \"verdict\": \"clean\"}, {\"id\": \"plazir15-ghp\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"charter-ghp\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"ds4cc-kimi\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"burnerchrome-kimi\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"vault-index-kimi\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"plazir27-kimi\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"ufo-fsd-kimi-pro\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"lucario-ghp\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"lucario-kimi\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"plazir15-kimi\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"charter-kimi\", \"pass\": true, \"problems\": [], \"verdict\": \"not-served\"}], \"total\": 12, \"validatorSha256\": \"062ccc4db6ab506ecb274ac0da4e4c4e9041462562e23cc586a0168cc8e44387\"}, \"passed\": false, \"stderr\": \"\", \"total\": 12}\n",
        "elapsedSeconds": 1.563
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "e2ef8501d62f218841139874428ec450cf3a2440",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-9vin3tb4/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-9vin3tb4/repo\", \"--revision\", \"b6b93e41f92a78c0500d0ca6ebb90c5ac8dc9efd\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-9vin3tb4/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-9vin3tb4/repo\", \"--revision\", \"b6b93e41f92a78c0500d0ca6ebb90c5ac8dc9efd\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-9vin3tb4/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-9vin3tb4/repo\", \"--revision\", \"99275af0d52eb2a15ad6cc1bec01c0fbf88201dc\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-9vin3tb4/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-9vin3tb4/repo\", \"--revision\", \"4f571b3100a71a0ee83ce9ef4a53ade5bac88b01\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-9vin3tb4/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-9vin3tb4/repo\", \"--revision\", \"b1fa0355b27d3c8daeed1a19d9aa3a1766301bea\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-9vin3tb4/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-9vin3tb4/repo\", \"--revision\", \"4c04d5e8512dd8f5bde8d18a057fde599008438c\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-9vin3tb4/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-9vin3tb4/repo\", \"--revision\", \"d5864430fe696791692815d854b6f0b48ffac1c7\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.039
      },
      "verdict": "killed"
    },
    {
      "id": "C2-29",
      "script": "measure_c2.py",
      "check": "Stored audit exit equals reproduced exit",
      "pattern": "receipt != actual",
      "replacement": "receipt.get(\"result\") != actual.get(\"result\")",
      "expected": "survived",
      "expectationReason": "No selftest fixture invalidates this check.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-9vin3tb4/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-9vin3tb4/repo\", \"--revision\", \"b6b93e41f92a78c0500d0ca6ebb90c5ac8dc9efd\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-9vin3tb4/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-9vin3tb4/repo\", \"--revision\", \"b6b93e41f92a78c0500d0ca6ebb90c5ac8dc9efd\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-9vin3tb4/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-9vin3tb4/repo\", \"--revision\", \"99275af0d52eb2a15ad6cc1bec01c0fbf88201dc\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-9vin3tb4/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-9vin3tb4/repo\", \"--revision\", \"4f571b3100a71a0ee83ce9ef4a53ade5bac88b01\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-9vin3tb4/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-9vin3tb4/repo\", \"--revision\", \"b1fa0355b27d3c8daeed1a19d9aa3a1766301bea\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-9vin3tb4/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-9vin3tb4/repo\", \"--revision\", \"4c04d5e8512dd8f5bde8d18a057fde599008438c\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-9vin3tb4/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-9vin3tb4/repo\", \"--revision\", \"d5864430fe696791692815d854b6f0b48ffac1c7\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.039
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "e2ef8501d62f218841139874428ec450cf3a2440",
      "mutatedSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "2e5bb253b9d4d7e801869bc86df1ac94f4328f6841fc5f0cf7adc802f503847c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "b1fed0118a42220d62bb433501da4d48e580bf39",
      "committedMutationSha256": "2e5bb253b9d4d7e801869bc86df1ac94f4328f6841fc5f0cf7adc802f503847c",
      "mutated": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ybdfjy6a/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ybdfjy6a/repo\", \"--revision\", \"6d120e1a72769465e7826c98ee583875dd74067d\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ybdfjy6a/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ybdfjy6a/repo\", \"--revision\", \"6d120e1a72769465e7826c98ee583875dd74067d\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ybdfjy6a/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ybdfjy6a/repo\", \"--revision\", \"be6b82f1980f60b1102106774b6c4e73c806cd40\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ybdfjy6a/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ybdfjy6a/repo\", \"--revision\", \"f6f074201cee9872c539eb6e4afad1fb92669711\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ybdfjy6a/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ybdfjy6a/repo\", \"--revision\", \"ed198ae6e27cc3200a60dddc4cdfca887e6a7c43\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ybdfjy6a/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ybdfjy6a/repo\", \"--revision\", \"f029065b282c4d542938ef99e0bedf827728f3d8\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ybdfjy6a/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ybdfjy6a/repo\", \"--revision\", \"1a4a90f67fdc77b2d7de9cc84a96988b128b69b5\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.053
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "28c0e5e4264a728cd4b880f14cdb169c47f2412e",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ntn10ka4/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ntn10ka4/repo\", \"--revision\", \"86952868c4d15022bbbf9321a4a84c4263758448\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ntn10ka4/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ntn10ka4/repo\", \"--revision\", \"86952868c4d15022bbbf9321a4a84c4263758448\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ntn10ka4/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ntn10ka4/repo\", \"--revision\", \"6da5867d18665ddbb0a2f37b0eb7a814dc236471\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ntn10ka4/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ntn10ka4/repo\", \"--revision\", \"e2e6d56f4b0c2b3623220e8ac5d6c47b9f1c18c6\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ntn10ka4/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ntn10ka4/repo\", \"--revision\", \"2f5862e723645c1e67bcf720824446d1500b9d8a\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ntn10ka4/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ntn10ka4/repo\", \"--revision\", \"f7a7348a060bdb2d67bd172fc33416343f1cb7a3\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ntn10ka4/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ntn10ka4/repo\", \"--revision\", \"9192612a7fb6af2807e6b24c495b2d752ed467ea\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.108
      },
      "verdict": "survived"
    },
    {
      "id": "C2-30",
      "script": "measure_c2.py",
      "check": "Stored audit result equals reproduced result",
      "pattern": "receipt != actual",
      "replacement": "receipt.get(\"exit\") != actual.get(\"exit\")",
      "expected": "killed",
      "expectationReason": "The unreproducible-audit fixture changes result verdict only; ignoring results accepts it.",
      "pristine": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ntn10ka4/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ntn10ka4/repo\", \"--revision\", \"86952868c4d15022bbbf9321a4a84c4263758448\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ntn10ka4/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ntn10ka4/repo\", \"--revision\", \"86952868c4d15022bbbf9321a4a84c4263758448\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ntn10ka4/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ntn10ka4/repo\", \"--revision\", \"6da5867d18665ddbb0a2f37b0eb7a814dc236471\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ntn10ka4/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ntn10ka4/repo\", \"--revision\", \"e2e6d56f4b0c2b3623220e8ac5d6c47b9f1c18c6\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ntn10ka4/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ntn10ka4/repo\", \"--revision\", \"2f5862e723645c1e67bcf720824446d1500b9d8a\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ntn10ka4/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ntn10ka4/repo\", \"--revision\", \"f7a7348a060bdb2d67bd172fc33416343f1cb7a3\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-ntn10ka4/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-ntn10ka4/repo\", \"--revision\", \"9192612a7fb6af2807e6b24c495b2d752ed467ea\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.108
      },
      "beforeSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "beforeHead": "28c0e5e4264a728cd4b880f14cdb169c47f2412e",
      "mutatedSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "d80b0c39d7a893e74b890930ecffe2b999f81a0567f741902ac1b73a651a0bcb",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "mutantHead": "6cf2ed1465045aee78aa503da1fe08d681b43697",
      "committedMutationSha256": "d80b0c39d7a893e74b890930ecffe2b999f81a0567f741902ac1b73a651a0bcb",
      "mutated": {
        "exit": 1,
        "stdout": "",
        "stderr": "counter_selftest: {\"accepted\": 12, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-x4h29_m_/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-x4h29_m_/repo\", \"--revision\", \"a8c266e4fcb08ebd72184facc1908acb3509d19b\"], \"errors\": [\"exit 0, expected 1\", \"accepted 12, expected 11\", \"failed rows [], expected ['ds4cc-primary']\", \"target 'ds4cc-primary' lacks problem 'audit.json'\"], \"exit\": 0, \"expectedAccepted\": 11, \"expectedExit\": 1, \"output\": {\"accepted\": 12, \"revision\": \"a8c266e4fcb08ebd72184facc1908acb3509d19b\", \"surfaces\": [{\"id\": \"ds4cc-primary\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"plazir15-ghp\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"charter-ghp\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"ds4cc-kimi\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"burnerchrome-kimi\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"vault-index-kimi\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"plazir27-kimi\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"ufo-fsd-kimi-pro\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"lucario-ghp\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"lucario-kimi\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"plazir15-kimi\", \"pass\": true, \"problems\": [], \"verdict\": \"clean\"}, {\"id\": \"charter-kimi\", \"pass\": true, \"problems\": [], \"verdict\": \"not-served\"}], \"total\": 12, \"validatorSha256\": \"062ccc4db6ab506ecb274ac0da4e4c4e9041462562e23cc586a0168cc8e44387\"}, \"passed\": false, \"stderr\": \"\", \"total\": 12}\n",
        "elapsedSeconds": 1.552
      },
      "restoredSha256": {
        "measure_c1.py": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5",
        "measure_c2.py": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c",
        "counter_selftest.py": "5d940ef3360391a47e05147278ae00a7b3ebc82f9592d27246e4f0961b35958d"
      },
      "restoredHead": "eefc66d36656c43cfd352f27559fa3fad5ae9093",
      "restored": {
        "exit": 0,
        "stdout": "{\"cases\": [{\"accepted\": 17, \"case\": \"C1 valid receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-s5rph327/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-s5rph327/repo\", \"--revision\", \"846f76e49afeea828739539d93109bc98fe4a6c0\"], \"exit\": 0, \"expectedAccepted\": 17, \"expectedExit\": 0, \"passed\": true, \"total\": 17}, {\"accepted\": 12, \"case\": \"C2 valid live receipts\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-s5rph327/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-s5rph327/repo\", \"--revision\", \"846f76e49afeea828739539d93109bc98fe4a6c0\"], \"exit\": 0, \"expectedAccepted\": 12, \"expectedExit\": 0, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 invalid receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-s5rph327/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-s5rph327/repo\", \"--revision\", \"0d4ec49d36e8134dc17120624e220d49d646ed79\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 16, \"case\": \"C1 missing heading rejected with diagnostic\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-s5rph327/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-s5rph327/repo\", \"--revision\", \"991dc29a2be4ac1f9974be7a0a4ee044adb0a319\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 unreproducible receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-s5rph327/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-s5rph327/repo\", \"--revision\", \"c25919aac0eb42056ef0d5f3b007d625668efd08\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}, {\"accepted\": 16, \"case\": \"C1 all-UNVERIFIABLE receipt rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-s5rph327/repo/.ufo/waves/round-23/measure_c1.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-s5rph327/repo\", \"--revision\", \"f08ed84a371fc438f450669827090e2cacc2939a\"], \"exit\": 1, \"expectedAccepted\": 16, \"expectedExit\": 1, \"passed\": true, \"total\": 17}, {\"accepted\": 11, \"case\": \"C2 non-GET fetch rejected\", \"command\": [\"/usr/bin/python3\", \"-B\", \"/tmp/kake-r23-counter-selftest-s5rph327/repo/.ufo/waves/round-23/measure_c2.py\", \"--root\", \"/tmp/kake-r23-counter-selftest-s5rph327/repo\", \"--revision\", \"fc8291f5196fb5fbcce1d224ba1b97a7f1f79f35\"], \"exit\": 1, \"expectedAccepted\": 11, \"expectedExit\": 1, \"passed\": true, \"total\": 12}], \"selftest\": \"passed\"}\n",
        "stderr": "",
        "elapsedSeconds": 2.03
      },
      "verdict": "killed"
    }
  ],
  "toolsInstalled": [],
  "summary": {
    "total": 71,
    "verdicts": {
      "survived": 58,
      "killed": 13
    },
    "byCounter": {
      "measure_c1.py": {
        "survived": 36,
        "killed": 5
      },
      "measure_c2.py": {
        "killed": 8,
        "survived": 22
      }
    },
    "detectorInvocations": 143,
    "pristineExit": 0,
    "restoredExits": {
      "0": 71
    },
    "restorationsMatch": true
  }
}
```
