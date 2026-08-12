# Runtime smoke-test suite (Game 723, all four regional sets)

**Design only — no ROM/emulator session has been run against this document
yet, and no generated set has changed as a result of it.** This is the
concrete plan for closing the gap flagged in every non-Italian locale's
[maintainer-handoff.md](maintainer-handoff.md) entry: French, German, and
Spanish all have complete, statically-audited generated sets with **no
achievement loaded and fired in RAIntegration, and no full-set smoke
test**. This suite is that missing runtime step, scoped down to something
actually runnable in one sitting per language instead of an exhaustive
76-achievement playthrough.

Purpose: catch **integration** mistakes in a generated regional set (wrong
set loaded, malformed syntax, stale English addresses, bad relocation
math, broken override handling, bad event-flag remaps, Pokédex bitfield
errors, leaderboard/RP breakage) — not to re-derive address correctness,
which the static pipeline (address-triage → address-mapping → generation)
already does exhaustively for all 131 addresses across every locale (see
[generation-report.md](generation-report.md) and each locale's own
`data/ra_address_triage.csv`).

Only **Yellow** has generated sets to test so far (Italian, French,
German, Spanish — see [the main README](../../../README.md) for status).
This suite is Game-723-specific; a future game would need its own.

This suite is deliberately small (7 achievements + 1 leaderboard + Rich
Presence, Tier 1; +3 items Tier 2) because it reuses game states and
address families already dynamically proven during the four language
investigations — it is not re-discovering addresses, only confirming the
*generated set* faithfully encodes what those investigations already
found. The underlying dynamic-test sessions this suite cross-references
(session IDs like "Italian T9", "German Session 2") are documented in the
private research repository, not reproduced here — see each locale's own
`docs/dynamic-testing.md` ([Italian](../italian/docs/dynamic-testing.md),
[French](../french/docs/dynamic-testing.md),
[German](../german/docs/dynamic-testing.md),
[Spanish](../spanish/docs/dynamic-testing.md)) for what's published from
them.

## Why these 8, not others

Every RA-referenced WRAM address in this game falls into one of three
buckets: `IDENTICAL_ADDRESS` (below the `+5` relocation boundary, e.g.
`wChannelSoundIDs` @ `0xc026`), `RELOCATED` (`+5`, the large majority — the
whole `0xC000`–`0xE000` region above `wBattleResult`), or a `+5` region
with a per-language literal override (map IDs stay numerically identical;
Pikachu-release dialogue tile bytes do not). No single achievement in the
131-address set is built from `IDENTICAL_ADDRESS` bytes alone — the `+5`
boundary sits so low (`0xceeb`→`0xcf06` unshifted, `0xcf0b`+ shifted) that
almost every gameplay-relevant struct (battle state, party, map, event
flags, Pokédex, box data) lives above it. That's a structural fact about
this ROM's memory map, not a gap in the picked achievements — so instead
of forcing a pure-`IDENTICAL` example, test #4 below deliberately pairs
one unshifted byte with several shifted ones *in the same condition set*,
which is a stronger regression check anyway (a remap bug that shifts
everything uniformly, including bytes that should stay put, is a real
failure mode this project has already seen — see the `wCurMap` negative
control and the German/Spanish Route 12 "coincidental same-address" false
positives documented in their respective `docs/wram-relocation-model.md`).

Each test below states which of the address/evidence categories it
exercises and cross-references the dynamic session that already proved the
underlying address for at least one language, so setup notes can be copied
rather than re-derived.

---

## Tier 1 — Fast smoke test (10–20 min from prepared save states)

Run this on **every** newly generated regional set before calling it
"locally validated." All seven items below share three save states (see
"Shared save states" at the end) — total new gameplay time is small; most
of the budget is menu navigation and address-watching, not travel.

### 1. Achievement 81655 — "Pokémon - I Choose You!"

| | |
|---|---|
| Why useful | Cheapest possible achievement in the set (1 condition group, 4 addresses) — if this fails, the whole generated set is broken (wrong ROM loaded, malformed syntax, or the set didn't apply at all), before spending time on anything more complex. |
| Address/evidence category | `RELOCATED` (`wCurMap` `0xd35d`→`+5`) combined with an `IDENTICAL`-valued map-ID literal (`!=40`, Oak's Lab) and a delta-hit progression flag (`wPokedexCount`-family). |
| Setup | Fresh save, standing in Oak's Lab immediately before receiving the Pokédex (or a save-state saved at that exact moment — trivial to make once, reusable forever). |
| Trigger | Talk to Oak, receive the Pokédex. |
| Expected result | Achievement unlocks the instant the Pokédex is received; RA overlay shows no earlier false-positive unlock while still in the lab beforehand. |
| Same test across IT/FR/DE/ES? | Yes, byte-for-byte — no override exists for this achievement in any of the four locales, and the address is a plain `+5` in all four. |
| Language-specific variation | None. |
| Runtime | ~1 min (already at the save state). |

### 2. Achievement 81978 — "You're Not Getting Away from Me That Easily"

| | |
|---|---|
| Why useful | The one achievement in the whole set with a **per-language literal override** — every other item here only needs an address to be right, this one needs 12–17 raw tile-byte *values* to be right too. |
| Address/evidence category | Language-specific literal override (`IDENTICAL_ADDRESS` tilemap bytes `0xc4e1`+, content differs per language) + `IDENTICAL_ADDRESS` gate (`wCanEvolveFlags` `0xccd3`, unshifted in all four languages, confirmed `direct_symbol_match`). |
| Setup | Any save with a Pikachu in the active party slot, standing in front of a PC. |
| Trigger | Open PC box, select Pikachu, attempt to deposit/release it — triggers the "Pikachu doesn't want to..." refusal textbox. |
| Expected result | Achievement unlocks the moment the refusal dialogue box finishes rendering; text on screen matches the language (sanity-check the override wasn't copy-pasted from another language by mistake — this is the exact failure mode the override system exists to prevent). |
| Same test across IT/FR/DE/ES? | Same trigger action and same gate address, but **the literal condition string is different bytes for every one of the four locales** (see each locale's own `docs/dynamic-testing.md`) — this is the point of the test. |
| Language-specific variation | Byte values (already captured — see each locale's `docs/dynamic-testing.md`); Spanish/German strings are one byte shorter than English/Italian's, so the terminator lands at `c4ef`/`c4f0` instead of `c4f1` — verify the generated condition has the right *length*, not just right values, since a leftover length assumption is a plausible generation bug. |
| Runtime | ~2 min. |

### 3. Achievement 4439 — "Halfway"

| | |
|---|---|
| Why useful | The single largest `RELOCATED`-WRAM achievement usable as a quick edge-trigger (61 addresses, entirely the party-Pokémon-struct family — level bytes across all 6 slots plus species-exclusion bytes). Tests a *different* struct (party array) than #1/#5, so a relocation-math bug specific to the party block (as opposed to `wCurMap` or the Pokédex arrays) would show up here and nowhere else in this suite. |
| Address/evidence category | `RELOCATED` WRAM, dominant (`wPartyMon1-6Level` all `+5`, confirmed dynamically for all 6 slots in the Italian campaign). |
| Setup | Prepared save state: full party of 6 non-legendaries, slots 2–6 already Level ≥50, slot 1 sitting at Level 49 with enough XP that one more wild-battle win crosses 50. |
| Trigger | Win one wild battle that levels slot 1 from 49→50. |
| Expected result | Achievement unlocks on the level-up frame, not before. |
| Same test across IT/FR/DE/ES? | Yes — same 5 addresses (`wPartyMon2-6Level`), same `+5` delta, confirmed independently in Italian and structurally inherited by French/German/Spanish via the shared relocation model. |
| Language-specific variation | None — no override row exists for 4439 in any locale. |
| Runtime | ~3–5 min if the save state needs building from scratch once; ~30 sec on repeat runs once the state is saved. |

### 4. Achievement 81657 — "Prepare for Trouble!"

| | |
|---|---|
| Why useful | Deliberately mixes an unshifted `IDENTICAL_ADDRESS` byte (`wChannelSoundIDs` `0xc026` — distinguishes wild/trainer/gym battle music) with `RELOCATED` bytes (`wCurMap`, `wBattleMonSpecies`) inside **one** multi-condition achievement using RA's `R:`/`N:`/`P:` (Reset/AndNext/Pause) logic — the best available proxy for "IDENTICAL-address-dominant" in this game (see "Why these 8" above for why no purely-`IDENTICAL` achievement exists), and the multi-condition framework itself is a distinct integration risk (condition-group syntax surviving generation) that #1/#3 don't exercise. |
| Address/evidence category | Mixed `IDENTICAL_ADDRESS` + `RELOCATED`, multi-condition logic (`R:`/`N:`/`P:` groups), plus a battle-state address (`wBattleMonSpecies`, "must be Pikachu"). |
| Setup | Save state just outside the Mt. Moon room with the Jessie & James Team Rocket trainer pair, with Pikachu as the only usable/lead party member (or the rest fainted/boxed). |
| Trigger | Engage and defeat both Team Rocket trainers using only Pikachu. |
| Expected result | Unlocks after the second trainer's defeat; does **not** unlock if a different Pokémon lands the finishing blow (validates the `wBattleMonSpecies` species-gate condition, not just the map/flag gate). |
| Same test across IT/FR/DE/ES? | Yes — same 8 addresses, same delta pattern, no override row for 81657. |
| Language-specific variation | None. |
| Runtime | ~3–4 min (one two-trainer battle). |

### 5. Achievement 4450 — "Gotta Catch 'em All - Yellow" (Pokédex bitfield spot-check)

| | |
|---|---|
| Why useful | Exercises the Pokédex Owned/Seen bitfield arrays. Full completion (129 species) is not smoke-testable and is out of scope by design — the static verifier already checks all 148 of this achievement's addresses structurally. This test instead spot-checks that the **bit-level mechanics** (Seen sets on encounter, Owned sets on capture, correct byte+bit for a specific species) survived generation. |
| Address/evidence category | `RELOCATED` WRAM, sparse-bitfield addressing (`wPokedexOwned+N`/`wPokedexSeen+N`, `+5`) — a structurally different addressing pattern (byte-offset-into-array, not a flat struct) than #1/#3, so this is the one test that would catch an off-by-one or wrong-stride bug in the array-relocation logic specifically. |
| Setup | Save with a partially-filled Pokédex and standing on a route with an easy, distinctly-indexed wild species (Route 1 Rattata/Pidgey). |
| Trigger | Walk into one wild encounter (confirms the Seen bit), then catch it (confirms the Owned bit). |
| Expected result | The species' Pokédex entry flips from unseen→seen on encounter and seen→owned on capture; in-game dex counter increments by 1 at each step; **do not** expect the achievement itself to unlock (129 catches required) — this test is address/bit-mechanics only. |
| Same test across IT/FR/DE/ES? | Yes — same array base, same `+5`, same bit math in all four; already independently confirmed by dynamic testing for Italian, German, and Spanish (see each locale's `docs/dynamic-testing.md`). |
| Language-specific variation | None (species names differ on-screen, but the underlying byte/bit math does not). |
| Runtime | ~2 min. |

### 6. Leaderboard 175 — "Speedrun" (start-trigger check)

| | |
|---|---|
| Why useful | Only the **start** trigger is practical inside a 10–20 min budget — full submission requires an Elite Four clear, deferred to Tier 2 using a pre-built Hall-of-Fame save state. |
| Address/evidence category | `IDENTICAL_ADDRESS` (start condition keys off early-game state) mixed with `RELOCATED` timer-adjacent addresses. |
| Setup | None — start a brand-new save file. |
| Trigger | Begin a new game past the naming screens, into the first controllable frame. |
| Expected result | The Speedrun leaderboard appears active in the RA overlay (timer visibly running) and does **not** already show a stale/garbage value from a previous session. |
| Same test across IT/FR/DE/ES? | Yes — no override row for leaderboard 175 in any locale. |
| Language-specific variation | None. |
| Runtime | ~1 min. |

### 7. Rich Presence check (folded into checkpoints above — no added time)

| | |
|---|---|
| Why useful | RP references `wCurMap` (`0xd35d`, `RELOCATED`), `wPartyCount` (`0xd157`, `RELOCATED`), and the full Pokédex Owned/Seen bitcount arrays (`0xd2f6`–`0xd31b`, `RELOCATED`) — exactly the three address families #1/#3/#5 already put the emulator in front of, so this piggybacks for free. |
| Address/evidence category | `RELOCATED`, map + party-count + Pokédex-bitcount aggregate display. |
| Setup | None — reuse the save states from #1 (Oak's Lab), #3 (post-level-up), and #5 (post-catch). |
| Trigger | None — just read the RP string shown in the RA overlay/menu at each of those three checkpoints. |
| Expected result | RP text shows the correct map name, correct party count, and a Pokédex "X seen / Y caught"-style count that increments exactly in step with the #5 catch (e.g. seen count +1 after the encounter, caught count +1 after the capture). A stale/frozen RP string, or one that shows an obviously-wrong map name, indicates the RP script's addresses didn't generate correctly even though achievements passed. |
| Same test across IT/FR/DE/ES? | Yes — no override row for the rich-presence script in any locale. |
| Language-specific variation | Map/location display strings are localized text, not addresses — sanity-check they render as real words, not garbage tiles (a lookup-table generation bug would show as garbled text here, not as an address failure anywhere else). |
| Runtime | ~0 min additional. |

**Tier 1 total: ~10–15 min** of new gameplay once the three save states
exist (Oak's Lab pre-Pokédex, Halfway pre-level-up, Pokédex pre-encounter),
plus the one-time cost of building those states (~10 min, do once per ROM
and keep the `.State` files).

---

## Tier 2 — Extended confidence test (add for a new localisation model, or after anything unusual changed)

Run Tier 1 first; add these three only when warranted (new language
family, a change to the relocation-model generator itself, or a
suspicious Tier 1 result).

### 8. Achievement 81681 — "The Long Way Gauntlet"

| | |
|---|---|
| Why useful | The multi-event-flag / accumulation-style achievement — 83 addresses, 37 required delta-hits across 8 sub-byte bitfields spanning `wEventFlags+145` through `+152`. This is the best test in the whole suite for "conditions that parse statically but behave incorrectly in-game," since the bit-accumulation logic only proves itself out under a real sequence of writes, not a single read. It is also the test most likely to catch a coincidental same-address false-positive — the exact failure mode already caught once in German/Spanish Route 12, where a static `IDENTICAL_ADDRESS` guess turned out to be a coincidental match (see [German's wram-relocation-model.md](../german/docs/wram-relocation-model.md)). |
| Address/evidence category | `RELOCATED` WRAM, multi-condition/bitfield accumulation (event flags), plus one `IDENTICAL`-valued map-ID gate. |
| Setup | **Do not** play all four routes fresh — that alone busts the time budget. Instead pre-stage a save state with Routes 12–14's trainers already defeated (36 of 37 required bits already set — poke via RAM edit + save, or reuse the tail end of the original dynamic-test session's end-state) and only the final Route 15 trainer remaining, without having left the Route 12-15 area. |
| Trigger | Defeat the one remaining Route 15 trainer. |
| Expected result | Achievement unlocks on that trainer's defeat, not before — confirms the full 37-bit accumulation across all 8 relocated addresses landed correctly, using a single battle instead of ~20. |
| Same test across IT/FR/DE/ES? | Yes — same 8 addresses (`0xd7d6`–`0xd7dd`→`+5`), same bit masks; independently dynamically confirmed for Italian, German, and Spanish already (see their `docs/dynamic-testing.md`). |
| Language-specific variation | None. |
| Runtime | ~2 min once the staged save state exists (staging it the first time takes longer — reuse across languages, it's ROM-identical setup). |

### 9. Leaderboard 175 submit + Speedrun-adjacent address (Hall of Fame checkpoint)

| | |
|---|---|
| Why useful | Completes leaderboard coverage (#6 only checked start) and reuses the same save state to also positive-check `wTileInFrontOfBoulderAndBoulderCollisionResult` (`0xd71a`→`+5`), which backs the Speedrun leaderboard's value formula and was, for German, the one address in the whole project resolved by static evidence alone rather than a live write hit (see [German's dynamic-testing.md](../german/docs/dynamic-testing.md)) — worth a real confirmation once. |
| Address/evidence category | `RELOCATED`, leaderboard value/submit logic. |
| Setup | Pre-built save state standing in front of the Hall of Fame entry, Elite Four already defeated. |
| Trigger | Walk into the Hall of Fame. |
| Expected result | Speedrun leaderboard submits a plausible time value (not 0, not garbage); the RA overlay shows a "new leaderboard entry" toast. |
| Same test across IT/FR/DE/ES? | Yes. |
| Language-specific variation | None. |
| Runtime | ~1 min once the save state exists. |

### 10. Pokédex bitfield — second/third species spot-check

| | |
|---|---|
| Why useful | Cheap way to raise confidence in the array-wide `+5` inheritance for a *new* localisation model, where the array-stride assumption hasn't been independently exercised before (Italian/German/Spanish already have this; a brand-new 5th language would not). Reuses #5's save state — no new setup. |
| Address/evidence category | `RELOCATED` WRAM, sparse-bitfield addressing, different byte offsets than #5 (pick 2 species that land in different bytes of the 19-byte array, e.g. one early-index and one late-index species). |
| Setup | Same save state as #5, after the Route 1 encounter/catch. |
| Trigger | Encounter/catch 2 more wild species with dex indices in different bytes of the Owned/Seen arrays (e.g. one below index 8, one above index 120). |
| Expected result | Both flip their expected bit at their expected (base+5) byte offset; unshifted candidate addresses stay `0x00` throughout (negative control). |
| Same test across IT/FR/DE/ES? | Yes conceptually — for the four existing locales this is optional (already well-covered); treat as **required** the first time a fifth regional variant is added. |
| Language-specific variation | None. |
| Runtime | ~3–5 min for 2 more encounters/catches. |

**Tier 2 additional total: ~10–15 min** on top of Tier 1, once all save
states exist.

---

## Explicitly excluded as redundant

- **Achievement 81668 ("Make it Double!")** — same condition shape, same
  three address families (`wCurMap`, `wBattleMonSpecies`, `wChannelSoundIDs`)
  as #4 (81657), just at a different map (Celadon Rocket Hideout vs. Mt.
  Moon). Running both would test the same relocation math twice for no new
  coverage. Skip unless #4 fails and you need to isolate whether the bug is
  location-specific.
- **Achievement 4441 ("Attack of the Prehistoric Pokemon")** — uses the same
  delta-hit pattern already exercised by #8's more complex 37-bit version;
  the simple single-bit case adds no new failure mode over #4's `R:`/`N:`/`P:`
  framework or #8's accumulation logic.
- **Full 129-species completion of achievement 4450** — not a smoke test by
  any definition (hours of gameplay); the static verifier already checks
  all 148 addresses structurally, and #5/#10 cover the runtime bit-mechanics
  question that static analysis can't answer on its own.
- **Any of the 8 gym/trainer "Showdown" achievements (4428–4435)** — all
  share the single `wStatusScreenHPBarColor+8` gameplay-running-guard
  address (`0xcf2c`→`+5`) already exhaustively proven across all four
  locales; one of them would be redundant with the others, and none adds
  an address family not already covered elsewhere in this suite.

## Shared save states (build once per ROM, reuse across all Tier 1/2 items)

| State | Used by | Notes |
|---|---|---|
| Oak's Lab, pre-Pokédex | #1, #7 | New-game start, walk to the lab, stop before talking to Oak. |
| Mt. Moon, outside Rocket trainers, Pikachu-only party | #4 | |
| Route 1, partial Pokédex, pre-encounter | #5, #7, #10 | |
| Full party, 5×Level 50+, slot 1 at 49 (one battle from 50) | #3 | Reuses the exact recipe from Italian's own dynamic-testing session. |
| Route 12-15 corridor, 36/37 trainer flags set | #8 | Build once via RAM-poke + save, or replay the tail of the original dynamic-test session once and keep the state file. |
| Hall of Fame entrance, Elite Four defeated | #9 | Reuses Italian's own dynamic-testing session state. |
| New save file, first controllable frame | #6 | Trivial, no state file needed. |

These seven states, once captured for the **English** ROM baseline and for
one regional ROM, transfer directly to the other three regional ROMs
without re-navigation — RAM addresses differ, but the save file's *game
progress* (map, party, flags) is per-ROM-family, not per-language, so the
same button-input sequence from a fresh save reaches the same state in any
of Italian/French/German/Spanish.

## Results checklist

See [`smoke-test-results.csv`](smoke-test-results.csv) — one row per test
ID per locale, to be filled in `PASS`/`FAIL`/`NOT RUN` as each generated
set is smoke-tested. All rows are currently `NOT RUN`; this is the
concrete work item behind the "runtime testing pending" status on French,
German, and Spanish (see [maintainer-handoff.md](maintainer-handoff.md)).
