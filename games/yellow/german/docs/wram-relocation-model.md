# The +5 WRAM relocation: independently re-derived for German

Derived fresh from the German ROM, using the same byte-evidence
cross-reference engine used for [Italian](../../italian/docs/wram-relocation-model.md)
and [French](../../french/docs/wram-relocation-model.md), but **not seeded
from either** — see [`data/ra_address_triage.csv`](../data/ra_address_triage.csv)
(the 131 RA-referenced addresses, each classified with its own evidence
citation).

## Same shape, independently found a third time

Cross-referencing the full symbol map against the German ROM finds the
same structural pattern both other localisations found:

| | Below `0xcf07` | `0xcf07`–`0xda97` | At/after `0xda98` |
|---|---|---|---|
| Italian | `+0` | dominant `+5` (214 evidenced sites) | `+0` |
| French | `+0` | dominant `+5` (378 of 423 `RELOCATED` rows, 89.4%) | `+0` |
| German | `+0` | dominant `+5` (402/445 all-bank rows; 170/196 low-bank/trustworthy) | `+0` |

Same lower boundary (`0xcf07`) and same upper boundary (`0xda98`) as both
other localisations, arrived at independently from the German binary
alone. Of the 115 German RA rows with a resolved address value that also
have a resolved Italian and/or French value to compare against: 95 match
both, 10 match Italian only, 0 match French only, 10 match neither — a
descriptive resemblance between three independent results, not a case of
German inheriting either other localisation's model. Full comparison:
`evidence/comparison_with_italian_and_french.md` in the private research
repo.

## A different local anomaly — and why it doesn't matter here

Unlike French (whose extra sub-boundary is a real `+6` region starting at
`wEnemyPartyCount`, `0xd89a`), German's single-byte anomaly sits right at
the *lower* boundary instead: `wBankswitchHomeSavedROMBank` (`0xcf08`, one
address after the first confirmed `+5` row) reads `+6`. German resolves
the rest of the `0xcf8a`–`0xd127` span — where French found its own
anomaly — cleanly at `+5`; this is a German-specific one-byte insertion
that neither other localisation shares at that spot, not a repeat of
French's finding. **Not used by any of the 131 Game 723 addresses.**

German also surfaced its own internal inconsistency worth noting: the
five-address `wPlayTimeHours`…`wPlayTimeFrames` cluster (`0xda40`–`0xda44`)
initially classified with four different deltas (`+7`, `+0`,
`DYNAMIC_TEST_REQUIRED`, `+0`, `+2`) from single-site evidence, despite
sitting well inside the confirmed `+5` region. A direct whole-block byte
diff against the intact `TrackPlayTime` routine (`home/play_time.asm`,
found intact in German ROM bank 0) resolved the entire cluster to a
uniform `+5` — the single-site readings were coincidental collisions, not
a real irregularity in this cluster.

## Result

All 131 RA-referenced addresses are classified with 0 unresolved: 24
`IDENTICAL_ADDRESS` and 107 `RELOCATED` (106 by the `+5` model, plus one
tied to the documented 81978 literal exception, whose address itself is
unshifted — see [dynamic-testing.md](dynamic-testing.md)). Evidence
quality across the 131 rows: 53 `structural_inference`, 33
`direct_symbol_match`, 27 `direct_rom_evidence`, 9 `structural_bracketing`,
9 `direct_dynamic_evidence`. The one row that started out as the single
weakest classification project-wide — `wEventFlags+145` (`0xd7d6`, Route
12), the same offset French's own last weak row sat on — was closed by
live dynamic capture, not force-closed statically: see
[dynamic-testing.md](dynamic-testing.md).
