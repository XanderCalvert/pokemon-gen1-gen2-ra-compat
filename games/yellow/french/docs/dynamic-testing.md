# Dynamic (real-hardware) testing

**Scope note, read this first:** these are live BizHawk WRAM-read/write
captures against the real French ROM, used to independently confirm or
correct specific static classifications in
[`data/ra_address_triage.csv`](../data/ra_address_triage.csv). They are
**not** the same thing as Italian's dynamic tests, which additionally
loaded translated conditions as local achievements in RAIntegration and
confirmed they fired under real game logic. No achievement-firing test and
no full-set RAIntegration load has been performed against the French ROM
— see **What hasn't been tested** below and
[maintainer-handoff.md](../../docs/maintainer-handoff.md).

## What was tested and found

| Phase | What it tested | Result |
|---|---|---|
| E — Route 22 Rival Battle 2 | Enemy-party battle struct (`wEnemyPartyCount` onward) | Found a **real `+6`** sub-boundary here — distinct from, and later than, the main `+5` region. Not RA-referenced by Game 723 (see [wram-relocation-model.md](wram-relocation-model.md)) |
| F — completed in-game trade | `wCompletedInGameTradeFlags`+1 (`0xd736`) | **+5**, direct confirmation (bit1 flip matched the trade performed) |
| G — 81978 dialogue literal | Live dialogue-tile read during the Pikachu release-refusal textbox | Address unshifted (as predicted); literal byte values read directly, not derived by analogy — see below |
| H — `wListPointer` boundary | `wListPointer` (`0xcf8a`) | **+5**, confirmed by write breakpoint — refutes the static `+6` guess at this specific address, narrows the real `+5`→`+6` transition to at-or-before `0xd89a` |
| I — party array deep offset | `wPartyMon2Level` (`0xd1b7`) | **+5**, confirmed by direct read (correct level for the party slot) |
| J — Route 12 / Hitmonlee | `wEventFlags+145` (`0xd7d6`), `wPokedexOwned+13` (`0xd303`) | Both **+5**, direct confirmation across trainer-defeat / capture state transitions — disproved two weak single-site `IDENTICAL_ADDRESS` matches |
| K — Pokédex sparse pattern | 5 more `wPokedexOwned`/`wPokedexSeen` offsets | All **+5**, direct confirmation across a seen→caught state transition for 5 distinct species — disproved the last 5 weak `IDENTICAL_ADDRESS` matches |
| L — `wSSAnne2FCurScript` | `0xd664` | **+5**, direct confirmation (bit2 flip exactly on the S.S. Anne 2F rival victory) — disproved the last remaining weak `IDENTICAL_ADDRESS` match project-wide |

Each of these is a before/after state transition captured live (a trade
completed, a trainer defeated, a Pokémon captured), not a static "already
set" read — the same standard Italian's own dynamic tests used, chosen
because it can distinguish a real relocation from a stale save state.

## Achievement 81978 — the one non-address exception

"You're Not Getting Away from Me That Easily" hardcodes literal English
dialogue-tile bytes at `wTileMap+321..` (`0xc4e1` onward). A live BizHawk
read of `wTileMap` during the equivalent French dialogue ("PIKACHU n'est
pas content!") shows:

- **The address range itself is unshifted** — as predicted, since
  `wTileMap` sits outside the shifted WRAM region (same conclusion Italian
  reached for this asset, not re-derived by analogy here, just consistent
  with French's own confirmed-`+0` `wTileMap`).
- **The literal byte values differ**, as expected for translated text.
- **The French string is shorter than the English original.** Its line
  terminator (`0xe7`) lands 12 bytes in, at `0xc4ec`.

The resulting signature — `0xc4e1`–`0xc4ec`, 12 bytes through and including
the terminator (`AF A0 B2 7F A2 AE AD B3 A4 AD B3 E7`) — was read directly
from a live capture, not derived by analogy from Italian's own (differently
sized) literal. It's applied in `overrides.csv` as a value/address exception
on achievement 81978, the same documented-exception mechanism Italian uses.
The override's trailing gate term (`0xH00ccd3`) and the leaderboard-only
`S1056` term are copied verbatim from Italian's override row, since neither
is a WRAM literal and neither has (or needs) French-specific evidence of
its own.

## What hasn't been tested

Unlike Italian, **no French achievement has been loaded as a local
achievement in RAIntegration and confirmed to fire**, and **no full
76-achievement set has been loaded and smoke-tested** against the French
ROM. Everything above is a WRAM-read/write-level confirmation of the
address-relocation model — real and direct, but one level below "the
translated condition actually fires under real game logic." Static
generation and audit (0 unresolved addresses, `verify_phase8_remap.py`
passing in full) are complete; runtime achievement-level and full-set
verification are the open items — see
[maintainer-handoff.md](../../docs/maintainer-handoff.md) for what's
proven vs. still open before this is claimed as RA-compatible.
