# The +5 WRAM relocation: independently re-derived for French

Derived fresh from the French ROM, using the same byte-evidence
cross-reference engine used for [Italian](../../italian/docs/wram-relocation-model.md)
but **not seeded from Italian's result** — see
[`data/ra_address_triage.csv`](../data/ra_address_triage.csv) (the 131
RA-referenced addresses, each classified with its own evidence citation).

## Same shape, independently found

Cross-referencing all 2,708 WRAM0/HRAM symbols against the French ROM
produces the same structural pattern Italian's investigation found:

| | Below `0xcf07` | `0xcf07`–`0xda97` | At/after `0xda98` |
|---|---|---|---|
| Italian | `+0` | dominant `+5` (214 evidenced sites) | `+0` |
| French | `+0` | dominant `+5` (378 of 423 `RELOCATED` rows, 89.4%) | `+0` |

Same lower boundary (`wUsedItemOnWhichPokemon` `0xcf06` unshifted,
`wAnimSoundID` `0xcf07` first `+5`), same upper boundary (`wBoxMon1BoxLevel`
`0xda98` reverts to unshifted, while `wBoxCount`/`wBoxMon1Species` just
below it stay `+5`) — byte-for-byte identical boundary addresses to
Italian, arrived at independently from the French binary alone. For the 34
of 131 RA addresses where both languages independently resolved a target
address, 32/34 (94%) land on the exact same numeric address — consistent
with both localisations inserting the same net 5 bytes in the same place in
WRAM, not two independently-sized rebuilds that happen to share a boundary.
This is a descriptive resemblance between two independent results, not a
case of French inheriting Italian's model.

## A second, real sub-boundary — and why it doesn't matter here

Unlike Italian, French evidence surfaced a genuine second cluster: 7
addresses inside the `+5` region initially read `+6` instead
(`wListPointer` `0xcf8a`, five sprite-decode pointers `0xd0aa`–`0xd0b2`,
`wItemListPointer` `0xd127`). Two rounds of targeted dynamic testing (see
[dynamic-testing.md](dynamic-testing.md)) resolved this:

- A live write-breakpoint on `wListPointer` while opening the Bag menu
  showed it is actually `+5`, not `+6` — refuting the static guess at that
  specific address (the other six in the cluster are the same
  `same_site_different_operand` evidence class and are now suspect for the
  same reason, not individually re-tested since none are RA-referenced).
- A separate live capture during a trainer battle (Route 22, Rival 2) found
  a **real** `+6` delta, but starting later — at `wEnemyPartyCount`
  (`0xd89a`) and running through the rest of the enemy-party battle struct.

`ram/wram.asm` declares this span as a `UNION`: the wild-encounter tables
(valid outside battle) and the enemy trainer-party struct (valid only
during a trainer battle) occupy the same physical bytes, both starting at
English `0xd885`. The leading hypothesis is that `wLinkEnemyTrainerName`
(a `NAME_LENGTH`-sized field) is one byte longer in the French binary than
in the `vendor/pokeyellow` checkout — the same class of bug this project
already found and fixed for Italian's `wDayCareMonName`. This narrows the
real `+5`→`+6` transition to somewhere in the 21-byte window
`0xd885`–`0xd899`, not yet pinned further.

**None of RetroAchievements Game 723's 131 addresses fall in or after this
union.** The transition only matters if a future RA asset references
`wLinkEnemyTrainerName` or the wild-encounter tables directly — for the
current set, every address is still governed by the single `+5`/`+0`
bounded-region model above.

## Result

All 131 RA-referenced addresses are classified with 0 unresolved: 20
`IDENTICAL_ADDRESS` and 111 `RELOCATED` (99 by direct evidence of the `+5`
model, plus one documented literal exception at achievement 81978 whose
address itself is unshifted — see [dynamic-testing.md](dynamic-testing.md)).
Evidence quality across the 131 rows: 66 `structural_inference`, 33
`direct_symbol_match`, 23 `direct_rom_evidence`, 9 `direct_dynamic_evidence`.
Zero rows remain resting on a single-site coincidental match — the last six
weak `IDENTICAL_ADDRESS` rows (five Pokédex bit-array offsets plus
`wSSAnne2FCurScript`) were each individually disproved and corrected to
`RELOCATED` by live dynamic capture (Phases J/K/L, see
[dynamic-testing.md](dynamic-testing.md)), the same failure mode Italian's
own investigation found and fixed at two of the same addresses.
