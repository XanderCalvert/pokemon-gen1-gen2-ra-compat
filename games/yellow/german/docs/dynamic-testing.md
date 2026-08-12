# Dynamic (real-hardware) testing

**Scope note, read this first — same as [French's](../../french/docs/dynamic-testing.md):**
these are live BizHawk WRAM-read/write captures against the real German
ROM, used to independently confirm or correct specific static
classifications in [`data/ra_address_triage.csv`](../data/ra_address_triage.csv).
They are **not** the same thing as Italian's dynamic tests, which
additionally loaded translated conditions as local achievements in
RAIntegration and confirmed they fired under real game logic. No
achievement-firing test and no full-set RAIntegration load has been
performed against the German ROM — see **What hasn't been tested** below
and [maintainer-handoff.md](../../docs/maintainer-handoff.md).

## What was tested and found

| Target | What it tested | Result |
|---|---|---|
| `wStatusScreenHPBarColor+8` (`0xcf2c`) | Write breakpoint entering/exiting the party menu | **+5**, confirmed (`0xcf31` fired with `A=04`, consistent with the party-menu HP-bar-color loop write; cross-validated against French's independently confirmed write-breakpoint result at the same semantic site) |
| `wPokedexOwned+3` (`0xd2f9`, catch Raichu) | Owned-bit flip on capture | **+5**, confirmed (`0xd2fe` observed `01`→`03`, gained bit `0x02`, exactly on capture) |
| `wPokedexOwned+9` (`0xd2ff`, catch Rapidash) | Owned-bit flip on capture | **+5**, confirmed (`0xd304` observed `00`→`20`) |
| `wPokedexOwned+10` (`0xd300`, catch Magnemite) | Owned-bit flip on capture | **+5**, confirmed (`0xd305` observed `00`→`01`) |
| `wPokedexOwned+11` (`0xd301`, catch Gastly) | Owned-bit flip on capture | **+5**, confirmed (`0xd306` observed `00`→`08`) |
| `wPokedexOwned+13` (`0xd303`, catch Hitmonlee) | Owned-bit flip on capture | **+5**, confirmed (`0xd308` observed `00`→`02`) |
| `wPokedexSeen+1` (`0xd30a`, see Weedle) | Seen-bit flip on sighting | **+5**, confirmed (`0xd30f` observed `80`→`90`) |
| `wPokedexSeen+12` (`0xd315`, see Cubone) | Seen-bit flip on sighting | **+5**, confirmed (`0xd31a` observed `00`→`80`) |
| `wEventFlags+145` (`0xd7d6`, Route 12) | Trainer-defeat flag accumulation | **+5**, confirmed (`0xd7db` accumulated `00`→`04`→`0C` across successive Route 12 trainer defeats; the old weak same-address candidate `0xd7d6` stayed `00` throughout, disproving its prior `IDENTICAL_ADDRESS` classification) |

Each of these is a before/after state transition captured live (a
Pokémon caught or seen, a trainer defeated, a menu entered), not a static
"already set" read — the same standard Italian's and French's own dynamic
tests used, chosen because it can distinguish a real relocation from a
stale save state.

`wTileInFrontOfBoulderAndBoulderCollisionResult` (`0xd71a`) was also
investigated dynamically (a live write breakpoint during Strength/boulder
gameplay found no hits) but resolved statically instead, once that null
result was understood: the byte only writes once, during new-save-file
creation, so it was never reachable mid-playthrough. It's resolved by a
site-identical-instruction ROM match (every operand in the same
instruction block shifted `+5` in lockstep) rather than counted among the
dynamic confirmations above.

## Achievement 81978 — the one non-address exception

"You're Not Getting Away from Me That Easily" hardcodes literal English
dialogue-tile bytes. A live BizHawk read of `wTileMap` (`0xc4e1`–`0xc4f0`)
during the equivalent German release-refusal dialogue confirms the address
range itself is unshifted (as the relocation model predicts) and reads the
German literal bytes directly — not derived by analogy from Italian's or
French's own (differently sized) literals. The German line is the longest
of the three localised literals, running the full 16-byte span. Applied in
`overrides.csv` as a value/address exception on achievement 81978, the
same documented-exception mechanism Italian and French both use. The
override's trailing gate term (`0xH00ccd3`, confirmed `IDENTICAL_ADDRESS`
by direct symbol match) and the leaderboard-only `S1056` term are copied
verbatim from Italian's/French's identical override row, since neither is
a WRAM literal and neither has (or needs) German-specific evidence of its
own.

## What hasn't been tested

Unlike Italian, and at the same stage as French: **no German achievement
has been loaded as a local achievement in RAIntegration and confirmed to
fire**, and **no full 76-achievement set has been loaded and smoke-tested**
against the German ROM. Everything above is a WRAM-read/write-level
confirmation of the address-relocation model — real and direct, but one
level below "the translated condition actually fires under real game
logic." Static generation and audit (0 unresolved addresses) are complete
— runtime achievement-level and full-set verification are the open items —
see [maintainer-handoff.md](../../docs/maintainer-handoff.md) for what's
proven vs. still open before this is claimed as RA-compatible.
