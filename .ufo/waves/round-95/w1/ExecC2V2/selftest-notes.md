# selftest-notes.md — ExecC2V2 (round-95 wave w1)

Candidate: `scripts/conditional_eval.py` contract-v2 patch (R94-6 / R93-10),
diff `conditional_eval-v2.diff` (base = round base `fdd5fdbe…`, v1 sha256
`d3bac7de1c2d04fc355db795aebdf6012030ea5c5793d9362bc9cd8e0b8cac5e`; patched
candidate sha256 `9cff0c34128477dbe98e1449e074206e80b0985d223de720e1453fcc6b608848`).

Command: `python3 -B conditional_eval.py --selftest` → observed `selftest 99/99`,
rc=0 (first run after the r42 fix below; the run before it printed `selftest 98/99`,
rc=1, with the single failure quoted under "r42").

Case count: v1 carried 90 cases (d01–d45 decisions, r01–r45 refusals). The patch
replaces two refusal cases in place with acceptance cases (v2 semantics flips) and
adds a nine-case `contract v2` block — 99 total.

## Per-clause changes and pinning cases

### C1 — empty list members accepted and ignored (RFC 9110 §5.6.1.2/§5.6.3, row S478)
- `_precondition_members` no longer raises on an empty member: a `,` at member
  position sets `saw_empty` and moves on; a separator comma followed only by
  spaces (trailing empty member) also sets `saw_empty`; loop-top end-of-string
  breaks instead of raising.
- A list of only empty members returns `("tags", [])` — decides as the empty
  list (If-None-Match matches nothing → 200; If-Match matches nothing → 412).
- Whitespace-only field value still refused (`"%s must not be an empty value"`):
  r27/r28 unchanged.
- `*` mixed with any other member — tag **or empty** — still refused. The
  star branch now reads `items == ["*"] and not saw_empty`; a `*` that shares
  the field with even an empty member yields the `"mixes '*' with other
  members"` refusal (matches the frozen counter reference, where `parse_list`
  splits on commas so `*,` sees `*` among parts and refuses).
- Flip: old r29 (`'"a",,"b"'` refusal) → `v2c1-empty-member-middle`
  (`etag='"b"'` → 200, empty member ignored).
- New: `v2c1-empty-member-trailing` (`'"9", '` → 304), `v2c1-all-empty-members`
  (`" , "` under If-None-Match → 200), `v2c1-all-empty-members-ifmatch`
  (`" , "` under If-Match → 412).

### C2 — obs-text (0x80–0xFF) legal in opaque-tag (RFC 9110 §8.8.3 etagc, row S455)
- `_entity_tag` loop: allowed set extended with `0x80 <= o <= 0xFF`; the inline
  member scan in `_precondition_members` got the same extension (v1 checked
  opaque chars in two places).
- Everything ≥ 0x100 and control characters stay refused.
- New: `v2c2-obs-text-strong` (`'"a\x80"'` If-Match → 200),
  `v2c2-obs-text-weak` (`W/"a\x80"` current vs `"a\x80"` member → 304). Old
  r21 (`'"a\x7fb"'` refusal) unchanged and now pins the 0x7F edge.

### C3 — `"role": null` accepted, means origin (lane convention, S471/S476)
- `evaluate`: `if role is None: role = "origin"` before the origin/cache check.
  Wrong role strings stay refused (r05 unchanged).
- Flip: old r06 (`role=None` refusal) → `v2c3-role-null-default` (→ 200).
- New: `v2c3-role-null-412` (explicit null role, If-Match mismatch → 412).

### C4 — duplicate object keys in raw stdin bytes refused (S034)
- New `_no_duplicate_keys(pairs)` hook raising
  `InvalidInput("duplicate object key in input document")`; `_process` parses
  with `json.loads(data, object_pairs_hook=_no_duplicate_keys)` and maps the
  hook's `InvalidInput` to the `invalid_input:` refusal path before any
  decision. Applies to every object level (top-level, `current`, `request`).
- New: `v2c4-duplicate-keys` — raw bytes with a duplicated top-level
  `"method"` key → refusal, exact stderr asserted.

### C5 — GET/HEAD method-filter edges (RFC 9110 §13.1.2–§13.1.4, S473/S474)
- No code change (v1 already gated the 304 branch on `_SAFE_METHODS` and the
  If-Modified-Since clause likewise); pinned by new cases:
  `v2c5-options-inm-412` (OPTIONS + If-None-Match match → 412),
  `v2c5-options-ims-ignored` (OPTIONS + If-Modified-Since → 200).

## Refusal-message deltas (only two)
- r42 (`'*,',`): was `"if_match has an empty list member"`; under v2 the field
  is refused for the different reason `"if_match mixes '*' with other members"`
  (star sharing the field with an empty member). First selftest run after the
  C1 rewrite failed this case (`rc=0, out 200` — star was admitted); fixed by
  the `saw_empty` trailing-comma flag, then `selftest 99/99` rc=0.
- r29's message disappears with the flip (no remaining "has an empty list
  member" emission anywhere).

## Known reading divergence, outside the frozen population
The candidate keeps v1's sequential parser, so an opaque-tag **containing a
comma** inside a list member (`If-Match: "a,b"`) stays accepted — RFC-exact.
The frozen counter's reference `parse_list` splits on commas and would refuse
that shape. No hand case and no generated case (tags are drawn from
`'"a"' 'W/"a"' '"b"' 'W/"b"' '"c"' '"a\x80"'` with join-only separators)
exercises a comma inside an opaque-tag, so the divergence is unobservable by
`c95_conditional.py`; recorded here for the reviewer rather than silently kept.
