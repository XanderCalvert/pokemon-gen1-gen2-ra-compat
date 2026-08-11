# The +5 WRAM relocation: a bounded region, not a global offset

Derived from the full 1,002-symbol Phase 4 table (both ROMs, private
research repo only) and published here as
[`data/ra_address_triage.csv`](../data/ra_address_triage.csv) (the 131
RA-referenced addresses, each classified with its own evidence citation).

## The problem with naive evidence

A byte match between the two ROMs at "the same opcode found at the same ROM
offset, operand differing" is single-reference-site evidence — medium
confidence by construction. Naively trusting every such row produces
nonsense: scanning WRAM sequentially, the observed delta flips between `+0`,
`+5`, and assorted one-off values (`+1452`, `-3290`, `-4534`, ...) almost
every few symbols — not what a real, contiguous relocation looks like.

The fix is to weight evidence by the ROM **bank** the matching instruction
lives in. Pokémon Yellow's bank 0 is the fixed home bank (always mapped);
banks 1–3 are early, frequently switched-in engine code; most of the ROM's
remaining banks hold map scripts and text data, where a common opcode byte
recurring *by coincidence* is far more likely than a deliberate reference
to an internal engine variable.

Filtering to bank ≤ 5 evidence only collapses the noise into a clean
bimodal split:

```
delta   count
 +5       214
  0       207
(all other deltas: 1 each — nine of them, total 9)
```

Two real values, both massively corroborated by independent sites; every
other value is a singleton — exactly what coincidental collisions look
like, and exactly what a real, bounded relocation plus background noise
looks like. **`+5` is a structural signal, not the mode of a noisy
distribution.**

## Pinning the boundary

Scanning bank ≤5 evidence in address order across the transition:

```
0xcee9  wBuffer / wEvoOldSpecies / ...       delta +0   <- last unshifted
0xceed  wHPBarNewHP / wNamingScreenLetter    delta +0
0xcf06  wUsedItemOnWhichPokemon              delta +0
0xcf0b  wBattleResult                        delta +5   <- first shifted
0xcf0d  wNextSafariZoneGateScript            delta +5
0xcf0e  wTilePlayerStandingOn                delta +5
```

The public `pret/pokeyellow` source places exactly four single-byte fields
between these two anchors (`0xcf07`–`0xcf0a`) — none independently
evidenced in either ROM, and none themselves resizable (plain single-byte
fields, no macro expansion). **The 5-byte insertion falls in that 4-byte
gap** — tighter than ROM byte evidence alone can resolve without
disassembling the Italian binary directly, which this project did not do.
No thematic reason (e.g. extra accented-character state) shows up in this
specific window — the surrounding fields are generic engine scratch, not
text-rendering state.

The upper boundary is pinned the same way, landing inside a 25-byte window
covering the tail of a box-Pokémon species list — see
[`data/ra_address_triage.csv`](../data/ra_address_triage.csv) for the exact
resolved addresses on either side.

## What this establishes about the structure

The whole shifted span sits inside one physically contiguous run of
`pret/pokeyellow` `SECTION`s — confirmed by exact arithmetic on their
declared sizes, not just visual ordering — spanning battle/menu scratch,
player name, badges/map state, Pikachu state, the full party, Pokédex
flags, day-care, event flags, and play time. That's *why* the large
majority of RA-referenced addresses land inside this one region: it's not
a coincidence about achievements specifically, it's a coincidence about
what this region of WRAM holds.

**This is not a single global WRAM shift.** It's one bounded region that
grew by exactly 5 bytes in the Italian ROM. Everything strictly before the
lower boundary and everything at/after the upper boundary sits back at
delta 0, with strong multi-site corroboration on both sides.

## Independent dynamic confirmation

The structural argument above is static (ROM byte evidence only). It was
independently re-confirmed with real-hardware dynamic tests — reading live
WRAM in BizHawk/RAIntegration against the running Italian ROM and checking
that values change exactly where and when the `+5` model predicts, under
real game logic rather than static comparison. Every one of the handful of
addresses whose static evidence was ambiguous or conflicting (a party
move-list array, an in-game-trade flag byte, a set of gauntlet event-flag
bytes, two Pokédex bit-array offsets, and several map-ID literals) was
resolved this way, always landing on `+5`, never on any other value — see
[dynamic-testing.md](dynamic-testing.md).

## Result

All 131 RA-referenced addresses are now classified with 0 unresolved: 30
`IDENTICAL` (outside the shifted region) and 101 `RELOCATED` — 99 at
exactly `+5` (inside it), plus 2 addresses tied to the single documented
81978 literal exception (see [dynamic-testing.md](dynamic-testing.md)),
which aren't part of the address-substitution model at all: that
achievement's dialogue-tile bytes are replaced by a hand-drafted literal
override, not an address relocation, so their own deltas are irrelevant to
this model. Every address that *is* substituted by the model carries a
delta of exactly `0` or `+5` — no other value.
