# The +5 WRAM relocation: independently re-derived for Spanish

Derived fresh from the Spanish ROM, using the same byte-evidence
cross-reference engine used for [Italian](../../italian/docs/wram-relocation-model.md),
[French](../../french/docs/wram-relocation-model.md), and
[German](../../german/docs/wram-relocation-model.md), but **not seeded
from any of them** — see [`data/ra_address_triage.csv`](../data/ra_address_triage.csv)
(the 131 RA-referenced addresses, each classified with its own evidence
citation).

## Same shape, independently found a fourth time

Cross-referencing the full symbol map against the Spanish ROM finds the
same structural pattern all three other localisations found:

| | Below `0xcf07` | `0xcf07`–`0xda97` | At/after `0xda98` |
|---|---|---|---|
| Italian | `+0` | dominant `+5` (214 evidenced sites) | `+0` |
| French | `+0` | dominant `+5` (378 of 423 `RELOCATED` rows, 89.4%) | `+0` |
| German | `+0` | dominant `+5` (402/445 all-bank rows) | `+0` |
| Spanish | `+0` | dominant `+5` (388/445 all-region rows) | `+0` |

Same lower boundary (`0xcf06` unshifted, `0xcf07` first `+5`) and same
upper boundary (`0xda97` last `+5`, `0xda98` reverts to unshifted) as all
three other localisations, arrived at independently from the Spanish
binary alone. Of the 128 Spanish RA rows with a resolved address value
that also have a resolved value in at least one other localisation to
compare against: 120 match Italian, 122 match French, 127 match German
(closest, 99.2%), 116 match all three, and exactly 1 disagrees with all
three (`wTileMap+329`, `0xc4e9` — inside the 81978 literal-override span,
so it affects only that achievement's literal bytes, never the address
model). A descriptive resemblance between four independent results, not a
case of Spanish inheriting any other localisation's model.

## No secondary sub-boundary found

Unlike French (`+6` from `wEnemyPartyCount` onward) and German (`+6` at
`wBankswitchHomeSavedROMBank`, right at the lower boundary), Spanish shows
**no comparable anomaly** inside `[0xcf07, 0xda97]` — the `+5` delta reads
uniform throughout for every row checked. The `wPlayTimeHours`…
`wPlayTimeFrames` cluster that initially looked inconsistent in German's
first-pass recon (and was resolved by a whole-block diff) was closed the
same way here, independently, via a separate bank-28 code-block site — no
internal inconsistency needed correcting in Spanish's own recon pass.

## Result

All 131 RA-referenced addresses are classified with 0 unresolved: 25
`IDENTICAL_ADDRESS` and 106 `RELOCATED` (105 by the `+5` model, plus one
tied to the documented 81978 literal exception, whose address itself is
unshifted — see [dynamic-testing.md](dynamic-testing.md)). Evidence
quality across the 131 rows: 54 `structural_inference`, 33
`direct_symbol_match`, 24 `direct_rom_evidence`, 10 `structural_bracketing`,
10 `direct_dynamic_evidence`. As with French and German, several rows that
started as single-site coincidental `IDENTICAL_ADDRESS` matches (six
Pokédex bit-array offsets, `wSSAnne2FCurScript`, `wEventFlags+145`/Route
12) were caught by the same failure-mode check those investigations
established and closed via structural inference or live dynamic capture —
not force-closed on weak evidence. See
[dynamic-testing.md](dynamic-testing.md) for the four rows that needed a
BizHawk session specifically.
