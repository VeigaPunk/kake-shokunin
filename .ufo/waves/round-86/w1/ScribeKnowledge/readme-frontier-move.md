## Coverage — round 86 (integration draft)

| Area | Entry | Coverage |
|---|---|---|
| Value-level Cache-Control effective-freshness reading | `knowledge/cache-control-effective.md` (proposed S461; S457/S456 supporting); `scripts/cache_control_effective.py` | Separate bounded offline field-specific reader; shared s-maxage > max-age > Expires−Date, first-occurrence duplicate profile, no-store and directive flags; no general-header equivalence or browser cache model |

Frontier line: the round-85 declared value-level `cache-control` reading frontier now has a held bounded slice: explicit effective-freshness inputs and directive reporting over isolated response field values. Duplicate-valued directives remain order-sensitive under the first-occurrence profile; distinct no-store/max-age order does not affect the no-store result. Full cache behavior, Vary/Age/Pragma, must-understand store-permission, arbitrary-header equivalence and live property observations remain outside this slice. This line is an integration proposal, not this seat's evidence that C2 reached 15/15.

D84-2 and D84-3 stay retained-open; this is not a full D84-queue closure claim. L1 must preserve the debt row and its existing flip condition separately.
