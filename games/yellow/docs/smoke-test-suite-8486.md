# Runtime smoke-test suite (Set 8486 — Prof. Oak Challenge, all regional sets)

Design only — no ROM/emulator session has been run against this document,
same status as [smoke-test-suite.md](smoke-test-suite.md) (Game 723's suite)
before its own first run. Purpose: catch **integration** mistakes in a generated regional
8486 set (wrong set/local file loaded, malformed syntax surviving the `S`
alt-group transform, a bad `AddSource`/`Measured` chain, wrong bit landing
after relocation) — not to re-derive address correctness, which the static
pipeline already did exhaustively (`games/yellow/sets/8486/resolved/non_address_localisation_audit.md`:
138/138 achievements, 0 non-address risks, 22/22 addresses `REUSED_RELOCATED`
from Game 723's own proven mapping) and the byte-level condition-parity
check already re-confirmed (all 138×4 languages parse and structurally
match the source, see the generation report).

## Relationship to Game 723's suite

8486 introduces **zero new addresses** — its 22 addresses are a strict
subset of the 131 already proven for 723. What it *does* introduce that
723's own Tier 1/2 suite never runtime-exercised is two structural
patterns unique to this set:

- **`wObtainedBadges` read as a `BitCount` (size code `K`)** — 723's own
  achievements never compare the badge byte's population count to a
  threshold; 8486's badge-gating (`0xKd355=0..8`, "before/after obtaining
  the Nth badge") is the first live test of that size code.
- **Large `AddSource`+`Measured` chains gating on `wObtainedBadges` bit
  edges** — 723's closest analogue is achievement 4450's 148-address
  Pokédex fold (Tier 1 #5 / Tier 2 #10 in the 723 suite, address-family
  proven there), but 8486's 9 badge achievements chain the *same*
  `wPokedexOwned` bits into `AddSource`/`Measured` combined with a
  `wObtainedBadges` bit-edge and a `wCurMap` delta guard in one condition
  set — a combination 723 never exercises.

Everything else (the `wPokedexOwned` bitfield array, the `wCurMap` delta
guard, the one `wEventFlags+289` bit) reuses address families 723's own
suite (or its phase8 local test pack — achievement 4449 "That's Shocking!"
already live-tested `wEventFlags+285..289`) already put in front of the
emulator. This suite is deliberately small for the same reason 723's is.

## Why these 8, not others

136 of the 138 achievements are the same "own species X before badge N"
template as achievement 298395 (Pikachu) below, differing only in which
`wPokedexOwned` bit and which `0xKd355` badge-count threshold they check —
already proven byte-identical in structure across all 4 languages by the
generation pipeline's own condition-parity check (see
`games/yellow/sets/8486/generated/<lang>/generation_report.md`). Runtime
coverage below picks one cheap example of that template (#1) plus one at a
non-zero badge threshold (#7, Tier 2), then spends the rest of the budget
on the small number of achievements that are **not** that template: the 9
`AddSource`/`Measured` badge-gate achievements (#2, #5, #6), the delta
moon-stone counters (#3), the `S`-separated OR-group achievements (#4), and
the lone event-flag achievement (#5 also covers this, see below).

---

## Tier 1 — Fast smoke test (15–20 min from prepared save states)

Run this on **every** newly generated regional 8486 set before calling it
"locally validated." Local IDs are for the **italian** local pack (block 1,
`111001001`–`111001138`) — identical local ID for the same asset in all
four languages (only the underlying addresses/trigger bytes differ); look
up any asset's ID in the language you're testing via
`games/yellow/sets/8486/resolved/<lang>/local_test_id_map.csv`.

### 1. Local ID 111001001 — "Pikachu" (RA 298395)

| | |
|---|---|
| Why useful | Cheapest achievement in the set (1 owned-bit edge + 2 gates) — if this fails, the set didn't load or apply at all, before spending time on anything more complex. Mirrors 723's own #1 ("Pokémon - I Choose You!") in role. |
| Address/evidence category | `wObtainedBadges` read as `BitCount` (`0xKd355=0`, size code `K`, badge count zero) + `wPokedexOwned+3` bit0 edge (`d0xMd2f9=0_0xMd2f9=1`) + `wCurMap` same-frame guard (`d0xHd35d=0xHd35d`). All three addresses `REUSED_RELOCATED` from 723's proven mapping. |
| Setup | Fresh save, standing right before receiving the starter Pikachu (no badges yet). |
| Trigger | Receive Pikachu from Oak. |
| Expected result | Unlocks the instant Pikachu is added to the party; no earlier false-positive. |
| Same test across IT/FR/DE/ES? | Yes — no override exists for any 8486 asset in any language (confirmed: 0 value substitutions in all 4 generation runs). |
| Language-specific variation | None. |
| Runtime | ~1 min. |

### 2. Local ID 111001018 — "Badge 1 - Brock" (RA 298412)

| | |
|---|---|
| Why useful | Smallest of the 9 badge/`AddSource`+`Measured` achievements (17 `A:` terms) — the cheapest live test of the pattern unique to this set: `A:`-chain summing `wPokedexOwned` bits, `M:0xMd2fd=17` measuring the sum, AND'd with a `wObtainedBadges` bit0 edge (`d0xMd355=0_0xMd355=1`) AND a `wCurMap` delta *inequality* guard (`d0xHd35d!=0`, "map just changed" — the opposite polarity from #1's "map unchanged" guard, worth confirming both survived generation correctly). |
| Address/evidence category | `wPokedexOwned` array (17 of its 19 bytes) via `AddSource`, `wObtainedBadges` bit-edge, `wCurMap` delta (`!=0` polarity). |
| Setup | Save state with all 17 pre-Brock species already owned (catch legitimately, or RAM-poke the 17 `wPokedexOwned` bits directly and save — same technique 723's suite #8 uses for its event-flag bitfield), standing just inside the Pewter Gym about to beat Brock. |
| Trigger | Defeat Brock, obtain the Boulder Badge. |
| Expected result | Unlocks on the same frame the badge bit flips **and** the map changes (leaving the gym) — verify it does *not* fire one frame early while badge is set but map hasn't changed yet, or vice versa. |
| Same test across IT/FR/DE/ES? | Yes — same 18 addresses, no override. |
| Language-specific variation | None. |
| Runtime | ~2 min once the save state exists (staging 17 species legitimately from a fresh game is the expensive part — RAM-poke is faster and is exactly what a "did the *condition*, not the *catching*, survive generation" test needs). |

### 3. Local ID 111001027 — "Moon Stone I" (RA 298421)

| | |
|---|---|
| Why useful | The small-scale version of the `AddSource`-sum pattern (same building block as the badge achievements in #2/#5/#6, just summing 4 terms instead of 17–128): `A:` sums the prior-frame owned-bits of all 4 eligible evolutions (Nidoqueen/Nidoking/Wigglytuff/Clefable), compared to 0; then sums their *current*-frame owned-bits, compared to 1 — i.e. "none of the four owned as of last frame, exactly one owned as of this frame." Moon Stone II/III/IV are the same sum crossing 1→2, 2→3, 3→4. Confirms the `AddSource`+delta-threshold pattern at its smallest scale before trusting it at 17+ terms in #2. |
| Address/evidence category | `wPokedexOwned` bits (4 terms, `A:`-summed, both prior- and current-frame) crossing an incrementing threshold. |
| Setup | Fresh Moon Stone use count (0), before the second badge, with a Moon Stone in inventory and an eligible Pokémon (e.g. Clefairy) ready to evolve. |
| Trigger | Use the Moon Stone on Clefairy (or any of the 4 eligible species) for the first time. |
| Expected result | Unlocks on that evolution; using a second Moon Stone afterward should NOT re-trigger this achievement (that's "Moon Stone II", local ID 111001028 — worth a quick negative check if time allows: confirm I doesn't refire and II unlocks instead). |
| Same test across IT/FR/DE/ES? | Yes — no override, same addresses. |
| Language-specific variation | None. |
| Runtime | ~2–3 min (one evolution). |

### 4. Local ID 111001085 — "Hitmonlee - Hitmonchan" (RA 298479)

| | |
|---|---|
| Why useful | Exercises the `S`-separated inline OR-group syntax (`..._d0xM00d2f9=1Sd0xN00d303=0_0xN00d303=1Sd0xO00d303=0_0xO00d303=1`) flagged in the non-address audit as "unusual RA syntax" — already confirmed to parse correctly and preserve condition-group shape across all 4 languages statically (see the audit), but this is the only *runtime* confirmation that the alt-group is evaluated as a real OR (either species satisfies) and not silently collapsed into an AND (which would make the achievement impossible, since you can only own one starting Hitmon at a time in this pool). |
| Address/evidence category | `wPokedexOwned+13` bits (2 alternates: Hitmonlee bit1, Hitmonchan bit2), OR'd via RA's `S` alt-group separator. |
| Setup | Before the 4th badge, Karate King's dojo prize Pokémon not yet claimed. |
| Trigger | Beat the Fighting Dojo, choose Hitmonlee (or Hitmonchan). |
| Expected result | Unlocks regardless of which of the two you pick — run it once with either choice; if budget allows, verify a second save picking the *other* one also unlocks it (proves both alt-groups work, not just whichever the pipeline happened to put first). |
| Same test across IT/FR/DE/ES? | Yes — same bit positions, no override. Three other achievements share this exact `S`-group shape (298496 Vaporeon/Jolteon/Flareon local ID 111001102, 298516/298517 Omanyte-Kabuto/Omastar-Kabutops local IDs 111001122/111001123) — skip them if this one passes, they're the same syntax pattern. |
| Language-specific variation | None. |
| Runtime | ~2 min. |

### 5. Local ID 111001132 / 111001133 — "Badge 6 - Sabrina or Blaine" / "Badge 7 - Blaine or Sabrina" (RA 298526 / 298527)

| | |
|---|---|
| Why useful | The single riskiest piece of logic in the set (flagged explicitly in the non-address audit, item #15): an `AddSource`-delta pair (`A:d0xRd355_d0xSd355=0_A:0xRd355_0xSd355=1` for #6, `=1`/`=2` for #7) that detects **which** of the two same-tier gyms was beaten *first*, since Yellow lets the player fight Sabrina or Blaine in either order. A relocation bug here wouldn't just misfire an achievement, it could make both or neither ever unlock. |
| Address/evidence category | `wObtainedBadges` bits R (Sabrina) and S (Blaine), summed via `AddSource` on both the prior and current frame to detect a 0→1 transition in "exactly one of the two." |
| Setup | Two short save states just before beating whichever of Sabrina/Blaine you pick to go first, all other pre-badge-6 species already owned (same M: threshold consideration as #2 — RAM-poke is the practical route). |
| Trigger | Test A: beat Sabrina first → confirm "Badge 6" (111001132) unlocks, "Badge 7" (111001133) does not. Test B (separate save, or continue after A): beat Blaine second → confirm "Badge 7" now unlocks. |
| Expected result | Exactly one of the pair fires per gym defeat, matching *whichever gym was actually fought first* — not fixed to "Sabrina is always 6." |
| Same test across IT/FR/DE/ES? | Yes — same two badge bits, no override, same evidence chain as #2. |
| Language-specific variation | None. |
| Runtime | ~4–5 min for both halves (two gym battles) — or ~2 min if you only test one direction and trust symmetry for the other, since it's the same two addresses either way. |

### 6. Local ID 111001136 — "Elite Four" (RA 298530)

| | |
|---|---|
| Why useful | The lone `wEventFlags` achievement in the set (`0xNd866`, `wEventFlags+289` bit1, "Defeat Champion") — already live-tested once under 723 (achievement 4449 "That's Shocking!" in the phase8 local pack uses the neighboring bits 285–288 of the same byte range), so this is a fast confirmatory re-check on the *same address family* under 8486's own generated file, not fresh ground. Also the largest `AddSource`/`Measured` chain that's still practically stageable (127 terms, `M:0xNd308=127`). |
| Address/evidence category | `wEventFlags+289` bit1 (event flag) + full `wPokedexOwned` array via `AddSource`/`Measured`. |
| Setup | Save state just before the Champion battle, near-complete pre-Elite-Four Pokédex (127 species) — RAM-poke recommended over legitimate catching for the same reason as #2. |
| Trigger | Defeat the Champion (Blue/Rival). |
| Expected result | Unlocks on Champion defeat, not on any earlier Elite Four member. |
| Same test across IT/FR/DE/ES? | Yes — `0xd866` independently confirmed `RELOCATED +5` for all four languages already (see `resolved/cross_version/localization_coverage.csv`). |
| Language-specific variation | None. |
| Runtime | ~2 min once staged. |

**Tier 1 total: ~15–20 min** of new gameplay/RAM-poke setup once save states exist. No Rich Presence check is included — 8486 has no Rich Presence of its own (it uses 723's shared script, already covered by 723's own Tier 1 #7).

---

## Tier 2 — Extended confidence test (add for a new localisation model, or after anything unusual changed)

### 7. Local ID 111001109 — "Psyduck" (RA 298503)

| | |
|---|---|
| Why useful | A "species before badge N" achievement at a **non-zero** badge threshold (`0xKd355=3`, before the 4th badge) — confirms the `BitCount` comparison works at a value other than 0 (#1 only proves the zero case). Also the condition where the shared "starter Pikachu owned" prerequisite gate (`0xM00d2f9=1`, plain steady-state, appended to nearly every one of the 136 template achievements) is easiest to see explicitly, since by this point in the run it's just confirming pre-existing state rather than being freshly set. |
| Address/evidence category | Same `wPokedexOwned`/`wObtainedBadges`/`wCurMap` families as #1, different bit + non-zero threshold. |
| Setup | 3 badges obtained, Psyduck not yet owned. |
| Trigger | Catch a Psyduck. |
| Expected result | Unlocks immediately; confirms the `BitCount` comparison generalizes past the zero-badge case. |
| Same test across IT/FR/DE/ES? | Yes, optional — treat as required only if #1 passes but you want extra confidence in the `0xKd355=N` family before trusting the other ~134 "before badge N" achievements untested. |
| Language-specific variation | None. |
| Runtime | ~2 min. |

### 8. Local ID 111001138 — "Mewtwo" (RA 298532)

| | |
|---|---|
| Why useful | The largest condition chain in the whole set (128 `A:` terms, `M:0xPd303=128`, gated behind `0xKd355=8` — all 8 badges) — the 8486 analogue of 723's 81681 "Long Way Gauntlet" (Tier 2 #8 there). Not required for confidence (structurally identical family to #2/#5/#6, already proven at smaller scale), but the best available stress test for whether a very long `AddSource` chain's relocation math holds up at full length. |
| Address/evidence category | Full `wPokedexOwned` array via `AddSource`/`Measured`, `wObtainedBadges` `BitCount`=8 gate. |
| Setup | Save state with all 127 other species already owned (post-Elite-Four), standing before the Cerulean Cave Mewtwo encounter. RAM-poke strongly recommended — legitimately owning 127 species is a full playthrough, well outside any smoke-test budget. |
| Trigger | Catch Mewtwo. |
| Expected result | Unlocks immediately on capture. |
| Same test across IT/FR/DE/ES? | Optional — run only when validating a new localisation model or after a change to the generation pipeline itself, same policy as 723's Tier 2 items. |
| Language-specific variation | None. |
| Runtime | ~2 min once staged (staging is the expensive part, and only needs doing once — reuse the save state across all 4 languages). |

**Tier 2 additional total: ~5–10 min** on top of Tier 1, once save states exist.

---

## Explicitly excluded as redundant

- **The other ~130 "species before badge N" achievements** — same template
  as #1/#7, differing only in bit position and badge threshold; already
  proven byte-identical across all 4 languages by the generation
  pipeline's own structural condition-parity check (title/description/
  points/flag/op/hits sequence compared programmatically for all 138
  assets × 4 languages, 0 mismatches). Runtime testing more than one
  zero-badge and one non-zero-badge example adds no new coverage.
- **The remaining 6 of the 9 badge/`AddSource` achievements** (Misty,
  Koga, Surge, Erika, Giovanni) — same `AddSource`+`Measured`+badge-bit-
  edge+map-delta-guard shape as #2, just longer chains and different
  badge bits; #2 (shortest) and #6 (longest practically stageable) already
  bracket the pattern.
- **Vaporeon/Jolteon/Flareon (298496), Omanyte-Kabuto (298516),
  Omastar-Kabutops (298517)** — identical `S`-alt-group shape to #4, just
  2–3 alternates instead of 2; skip unless #4 fails and you need a second
  data point on whether the OR-group issue is universal or specific to
  one achievement.
- **Moon Stone II/III/IV (298422/298447/298448)** — same delta-counter
  shape as #3 at counter values 1/2/3 instead of 0; the negative check
  suggested inside #3 (does II fire instead of I re-firing) already
  covers the boundary behavior that matters.
- **The `wPokedexOwned` array's bit/byte-stride mechanics generally** —
  already covered by 723's own Tier 1 #5 and Tier 2 #10, which exercise
  the exact same 19-byte array 8486 reuses unchanged (0 new addresses in
  this family, per the coverage report). Re-proving the array mechanics
  under 8486 specifically would be redundant with work already done under
  723.

## Shared save states (build once per ROM, reuse across all Tier 1/2 items)

| State | Used by | Notes |
|---|---|---|
| Fresh save, pre-Pikachu | #1 | New-game start, walk to the lab, stop before receiving Pikachu. |
| 17 pre-Brock species owned (RAM-poke), pre-Brock-battle | #2 | Poke the 17 `wPokedexOwned` bits `A:`-summed in RA 298412's condition, save. |
| Pre-second-badge, Moon Stone in inventory, eligible evolution ready | #3 | |
| Pre-4th-badge, dojo prize not yet claimed | #4 | |
| Pre-badge-6/7, all other pre-badge-6 species owned (RAM-poke), positioned to fight either Sabrina or Blaine first | #5 | Build twice (Sabrina-first and Blaine-first) or once and branch. |
| 127 pre-Elite-Four species owned (RAM-poke), pre-Champion | #6 | |
| 3 badges obtained, Psyduck not owned | #7 | |
| All 127 non-Mewtwo species owned (RAM-poke), pre-Cerulean-Cave | #8 | Reuse #6's staged Pokédex if convenient — same target count. |

These eight states, once captured for the **English** ROM baseline and for
one regional ROM, transfer directly to the other three regional ROMs
without re-navigation, same as Game 723's suite — RAM addresses differ,
but game progress (map, party, badges, Pokédex ownership) is per-ROM-
family, not per-language.

## Results checklist

See [`smoke-test-results-8486.csv`](smoke-test-results-8486.csv) — one row
per test ID per language, to be filled in `PASS`/`FAIL`/`NOT RUN` as each
generated regional 8486 set is smoke-tested.
