# ExecScoreC2 — field-by-field comparison, reproduced slot controls vs pre-freeze receipts

Reproduced per the committed recipe in `.ufo/waves/round-97/controls.sh` (`fixture()`:
`git clone -q --shared` → `checkout -q --detach` the instruments revision
`a2208ac7b8ce6e1148e5069b4c884c78f97dfb3e` → apply the slot change → `git add -A` →
commit → score through the counter's public CLI). My fixture commits carry identity
`ExecScoreC2 <ExecScoreC2@example.invalid>` (controls used `c97-fixture`), so every
commit id differs from the pre-freeze one; the held-out population is seeded from
`int(revision[:15], 16)` (counter docstring), so held-out totals scale with the seed.
Declared expected differences: `revision=` and the held-out case **totals**. Everything
else must match — and does, in all four slots.

Pre-freeze receipts: `LANE/.ufo/waves/round-97/controls/ctl-c2-slot-{pos,table,oracle,absent}.txt`.
My receipts (same directory as this file): `slot-pos.txt`, `slot-table.txt`,
`slot-oracle.txt`, `slot-absent.txt`.

## slot-pos — frozen positive control in the candidate slot

| field | pre-freeze (`ctl-c2-slot-pos.txt`) | mine (`slot-pos.txt`) | verdict |
|---|---|---|---|
| revision | `f4f68e5ac49efeab1062ac163738eba2cbc9d0f9` | `4c2712d244cdc76bb7e4556440e09aa5018ef827` | differs (new commit) — expected |
| candidate | `present` | `present` | match |
| hand | `37/37` | `37/37` | match |
| generated | `104/104` | `104/104` | match |
| heldout | `52/52` | `58/58` | total differs — expected (seed follows commit id); all-pass holds in both |
| forgeries_refused | `7/7` | `7/7` | match |
| positive | `admitted` | `admitted` | match |
| mutants | `14/14` | `14/14` | match |
| survivors | `none` | `none` | match |
| anti_table | `ok` | `ok` | match |
| population | `ok` | `ok` | match |
| seed | `97` | `97` | match |
| met | `true` | `true` | match |
| exit | `0` | `0` | match |

## slot-table — lookup-table forgery in the candidate slot

| field | pre-freeze (`ctl-c2-slot-table.txt`) | mine (`slot-table.txt`) | verdict |
|---|---|---|---|
| revision | `3b141dd070435d517e04cd21fd53d10084f692e3` | `82805ff0a656a27a1dfdc7a489a62c9766b10074` | differs (new commit) — expected |
| candidate | `present` | `present` | match |
| hand | `37/37` | `37/37` | match |
| generated | `104/104` | `104/104` | match |
| heldout | `22/57` | `22/52` | totals differ — expected (seed follows commit id); held-out failure drives `met=false` in both |
| forgeries_refused | `7/7` | `7/7` | match |
| positive | `admitted` | `admitted` | match |
| mutants | `14/14` | `14/14` | match |
| survivors | `none` | `none` | match |
| anti_table | `ok` | `ok` | match |
| population | `ok` | `ok` | match |
| seed | `97` | `97` | match |
| met | `false` | `false` | match |
| exit | `1` | `1` | match |

## slot-oracle — oracle-import forgery in the candidate slot

| field | pre-freeze (`ctl-c2-slot-oracle.txt`) | mine (`slot-oracle.txt`) | verdict |
|---|---|---|---|
| revision | `07738724e96b2b7726db813c783d144db752e8b1` | `558012d4033cbfb8a17d389d7b3cf12b334db40d` | differs (new commit) — expected |
| candidate | `present` | `present` | match |
| hand | `20/37` | `20/37` | match |
| generated | `0/104` | `0/104` | match |
| heldout | `0/55` | `0/52` | totals differ — expected (seed follows commit id); zero in both |
| forgeries_refused | `7/7` | `7/7` | match |
| positive | `admitted` | `admitted` | match |
| mutants | `14/14` | `14/14` | match |
| survivors | `none` | `none` | match |
| anti_table | `ok` | `ok` | match |
| population | `ok` | `ok` | match |
| seed | `97` | `97` | match |
| met | `false` | `false` | match |
| exit | `1` | `1` | match |

## slot-absent — candidate deleted

| field | pre-freeze (`ctl-c2-slot-absent.txt`) | mine (`slot-absent.txt`) | verdict |
|---|---|---|---|
| revision | `a84bd0f89cf821abc63e7bfe07af085acf6e270c` | `d8141242cbdb1c13959d78b64a432a95b808e715` | differs (new commit) — expected |
| candidate | `absent` | `absent` | match |
| hand | `0/37` | `0/37` | match |
| generated | `0/120` | `0/120` | match (totals identical here: no seed dependence when absent) |
| heldout | `0/60` | `0/60` | match |
| forgeries_refused | `0/7` | `0/7` | match |
| positive | `refused` | `refused` | match |
| mutants | `0/14` | `0/14` | match |
| survivors | `none` | `none` | match |
| anti_table | `ok` | `ok` | match |
| population | `ok` | `ok` | match |
| seed | `97` | `97` | match |
| met | `false` | `false` | match |
| exit | `1` | `1` | match |

## Result

4/4 slot controls reproduced: every field matches except the declared expected
differences (revision id; held-out totals in candidate-present slots, seed-derived).
Note: the candidate-present generated totals (`104/104`, `0/104`) and all hand totals
also match exactly, so the seed only moved the held-out case draw, as the counter
docstring's seeding clause implies.

Incident note (transparency): sibling seat ConnectorScope-23 ran
`rm -rf /fast/scratch/hyaku/kake-r97` (~18:14Z), deleting my first clone mid-wave; my
first slots attempt therefore produced four invalid `checkout-fail` shells. That seat
self-reported the incident and stated frozen instruments/controls were untouched
(independently consistent with my digest verification, which passed before and after).
I re-derived the clone and all four fixtures from the frozen recipe; the receipts here
are from that clean re-derivation, and my tip-score and selftest runs completed before
the deletion window and are unaffected.
