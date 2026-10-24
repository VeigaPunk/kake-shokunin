# honest control fixture

`ctl1.py` is a byte copy of `.ufo/waves/round-44/controls-r43/headtail-V1-prefix-cache64.py`; the one-row `controls.tsv` retains the committed source SHA-256. No counter receipt is planted here. The invocation uses the real frozen `.ufo/waves/round-44/c44_count_v5.py`; its receipt and three build receipts are generated during the driver's run, with the counter's own seed, generated run data, verdict, ratios, and note. `caughtBy` is derived by `c44_audit.py`, not stored in the raw counter receipt.
