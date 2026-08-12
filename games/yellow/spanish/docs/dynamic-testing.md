# Dynamic (real-hardware) testing

**Scope note, read this first — same as [French's](../../french/docs/dynamic-testing.md)
and [German's](../../german/docs/dynamic-testing.md):** these are live
BizHawk WRAM-read/write captures against the real Spanish ROM, used to
independently confirm specific static classifications in
[`data/ra_address_triage.csv`](../data/ra_address_triage.csv). They are
**not** the same thing as Italian's dynamic tests, which additionally
loaded translated conditions as local achievements in RAIntegration and
confirmed they fired under real game logic. No achievement-firing test and
no full-set RAIntegration load has been performed against the Spanish ROM
— see **What hasn't been tested** below and
[maintainer-handoff.md](../../docs/maintainer-handoff.md).

## What was tested and found

Four BizHawk sessions were run against rows the static evidence genuinely
couldn't settle on its own — the same four categories German's own
investigation needed a dynamic test for:

| Session | Target | What it tested | Result |
|---|---|---|---|
| 1 | `wEventFlags+145` (`0xd7d6`, Route 12) | Trainer-defeat flag accumulation | **+5**, confirmed (`0xd7db` progressed `00`→`04`→`0C` across successive Route 12 trainer defeats — bit 2 then bit 3, exactly reproducing the transition German independently found at this same symbol; the old weak same-address candidate `0xd7d6` stayed `00` throughout) |
| 2 | `wStatusScreenHPBarColor+8` (`0xcf2c`) | Write breakpoint during party-menu/HP-bar rendering | **+5**, confirmed (`0xcf31` hit repeatedly across menu interaction, `A=04` at the write instruction) |
| 3 | `wEventFlags+128` (`0xd7c5`, Fish Out Of Water) | Event-flag bit set by the Mt. Moon Pokémon Center interaction | **+5**, confirmed (`0xd7ca` flipped `00`→`80`/bit 7 immediately after the interaction; the old candidate `0xd7c5` stayed `00`) |
| 4 | Achievement 81978 dialogue literal | Live tilemap read during the release-refusal dialogue | Address unshifted (as predicted); literal bytes read directly — see below |

A fifth, non-required sanity pass additionally corroborated by direct
observation the six Pokédex Owned/Seen offsets already closed by
structural inference (`0xd2f9`, `0xd2ff`, `0xd300`, `0xd303`, `0xd30a`,
`0xd315`) plus a seventh (`0xd301`, Gastly, found along the way) — all
seven confirmed `+5` on the exact capture/sighting transition, upgrading
them from `structural_inference` to `direct_dynamic_evidence` with no
address or classification changes.

Each of these is a before/after state transition captured live (a trainer
defeated, a menu entered, an interaction completed, a Pokémon
caught/sighted), not a static "already set" read — the same standard
Italian's, French's, and German's own dynamic tests used, chosen because
it can distinguish a real relocation from a stale save state.

## Achievement 81978 — the one non-address exception

"You're Not Getting Away from Me That Easily" hardcodes literal English
dialogue-tile bytes. A live BizHawk read of `wTileMap` (`0xc4e1`–`0xc4ef`)
during the equivalent Spanish dialogue ("¡A PIKACHU no le parece bien!")
confirms the address range itself is unshifted (as the relocation model
predicts) and reads the Spanish literal bytes directly — not derived by
analogy from any other localisation's differently sized literal. The
terminator lands at `0xc4ef`, one byte earlier than English's `0xc4f1`
span, matching the shorter Spanish translation. Applied in `overrides.csv`
as a value/address exception on achievement 81978, the same
documented-exception mechanism the other three localisations use. The
override's trailing gate term (`0xH00ccd3`, confirmed `IDENTICAL_ADDRESS`
by direct symbol match) and the leaderboard-only `S1056` term are copied
verbatim from Italian's/French's/German's identical override row, since
neither is a WRAM literal and neither has (or needs) Spanish-specific
evidence of its own.

## What hasn't been tested

Unlike Italian, and at the same stage as French and German: **no Spanish
achievement has been loaded as a local achievement in RAIntegration and
confirmed to fire**, and **no full 76-achievement set has been loaded and
smoke-tested** against the Spanish ROM. Everything above is a
WRAM-read/write-level confirmation of the address-relocation model — real
and direct, but one level below "the translated condition actually fires
under real game logic." Static generation and audit (0 unresolved
addresses) are complete — runtime achievement-level and full-set
verification are the open items — see
[maintainer-handoff.md](../../docs/maintainer-handoff.md) for what's
proven vs. still open before this is claimed as RA-compatible.
