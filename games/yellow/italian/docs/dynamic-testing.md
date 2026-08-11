# Dynamic (real-hardware) testing

All static conclusions in this project (the `+5` bounded relocation model,
the 81978 literal exception) are backed by ROM cross-reference evidence
alone. The tests below independently re-confirm the load-bearing ones by
running the actual Italian ROM in BizHawk, watching live WRAM, and — for
the achievement-level tests — loading the translated condition as a **local
achievement** in RAIntegration (Compatibility Test mode) and confirming it
fires under real game logic, not just static byte comparison. Final
capture used RAIntegration's Pause on Trigger where applicable, to confirm
the exact triggering moment.

## Test matrix — 7 / 7 passed

| # | Test | What it confirms | Result |
|---|---|---|---|
| 1 | 81978 — You're Not Getting Away from Me That Easily | Live dialogue-buffer read matches the derived Italian literal bytes (see below) | **PASS** |
| 2 | King of the Dojo | `wEventFlags+107` relocates `+5` under a real Hitmonlee-prize event | **PASS** |
| 3 | Silph Co. Rival / Do We REALLY Have to Do This Now? | `wEventFlags+233` relocates `+5` under a real rival-defeat event; `wCurMap`-guard doesn't false-block | **PASS** |
| 4 | Pokédex Seen/Owned operand probes (two independent array offsets) | Two separate `wPokedexSeen`/`wPokedexOwned` byte offsets both relocate `+5`, with Seen and Owned firing independently and in the correct order (encounter vs. capture) | **PASS** |
| 5 | Showdown in Pewter City | Badge-flag bit relocates `+5`; `wCurMap` map-ID guard is unchanged | **PASS** |
| 6 | Fish Out Of Water | A rate-transition condition relocates `+5`; `wCurMap` map-ID guard is unchanged | **PASS** |
| 7 | That's Shocking! (full Elite Four/Champion sequence) | The full contiguous Elite Four `wEventFlags` block relocates `+5` end-to-end, including the delta-triggered final-rival condition | **PASS** |

Every test that depended on a `wCurMap` (current-map-ID) literal also
independently confirmed that literal's Italian value matched the source
condition's implicit assumption — a separate axis from address relocation,
resolved incidentally by the same test runs.

## Achievement 81978 — the one non-address exception

"You're Not Getting Away from Me That Easily" hardcodes 17 literal English
dialogue-tile bytes at `wTileMap+321..+337` (`0xc4e1`–`0xc4f1`) — the
condition reads the on-screen dialogue box and compares it against the
exact English text tiles for the "PIKACHU has a sad look on its face!"
refusal line.

A live BizHawk read of the Italian ROM during the equivalent dialogue
("PIKACHU ha un'aria triste!") shows:

- **The address range itself is unshifted.** This is the one place in the
  whole set where the relocation model correctly predicts *no* change (the
  dialogue tile buffer sits outside the shifted WRAM region — see
  [wram-relocation-model.md](wram-relocation-model.md)).
- **The literal byte values differ**, as expected for translated text —
  the first two tiles match (shared "PIKACHU" name tiles), then diverge.
- **The Italian string is two bytes shorter.** Its line-terminator tile
  lands two offsets earlier than the English terminator. The English
  condition's full 17-byte span can't be reused as-is against the Italian
  ROM — comparing past the Italian terminator would compare against blank
  padding with no diagnostic value.

The smallest stable Italian signature is the 15-byte span through and
including the Italian line terminator (`0xc4e1`–`0xc4ef`), which anchors
the match to this specific dialogue's length rather than to padding that
could coincidentally recur in other textboxes.

This is a **value/literal rewrite**, not an address relocation — the only
asset in the entire 76-achievement / 2-leaderboard / Rich Presence set that
needs one. It's tracked as an explicit, documented exception in the
generator and audit (`classification: EXCEPTION`, not `RELOCATED`) rather
than silently special-cased.

## Full-set RAIntegration smoke test

Separately from the 7 targeted tests above, the project author manually
loaded the **complete** generated 76-achievement Italian set into
RAIntegration against the Italian ROM (not just the 7-achievement test
pack used for the targeted tests) and observed all 76 achievements load
for **458 points**, with **Not Mad, Just Disappointed** triggering
naturally from a fresh Italian save under Pause on Trigger.

**This is a manual runtime observation, reported as-is. It is not
reproduced or independently verified.** — unlike the 7 tests above, which
are backed by recorded WRAM reads and which the private research repo
diffs future generator output against, so a regeneration can't silently
drift from what was physically confirmed to work.
