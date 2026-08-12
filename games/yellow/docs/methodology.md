# Methodology

## Goal

Determine whether RetroAchievements [Game 723](https://retroachievements.org/game/723)
(Pokémon Yellow, authored against the English ROM) can be made to work
against the official Italian retail ROM, and produce exact, evidence-backed
documentation of exactly what has to change if not.

## Ground rules

- ROMs are never committed or redistributed by this repo. Only their
  identifying hashes are published (see the main [README](../../../README.md)).
- No claim of "compatible" without evidence. Every address in
  [`data/ra_address_triage.csv`](../italian/data/ra_address_triage.csv) carries a
  classification and an evidence column.
- The English ROM is the reference for WRAM/HRAM/SRAM naming, using the
  public `pret/pokeyellow` decompilation's symbol layout (its SHA-1 matches
  what that project builds from, so its symbol table is trustworthy as a
  reference here).
- Static (ROM cross-reference) evidence first — cheap, exhaustive,
  reproducible; real-hardware dynamic (emulator) testing only where static
  evidence can't settle a question on its own.

## Pipeline

1. **Provenance** — hash both ROMs; fail loudly on mismatch.
2. **Binary diff** — bank- and byte-level comparison between the two ROMs to
   see *where* localisation changed the cartridge image structurally. This
   is a ROM-offset diff, not a RAM-address diff — useful context, not proof
   that runtime addresses moved or stayed put.
3. **Symbol import** — WRAM/HRAM/SRAM symbol names and addresses computed
   from the public `pret/pokeyellow` source layout, then validated (not
   blindly trusted) against real ROM byte evidence in the next step, so a
   miscomputed symbol address falls out as `UNRESOLVED` rather than
   silently producing a false correspondence.
4. **Address mapping** — for every candidate WRAM/HRAM/SRAM symbol, search
   both ROMs for the actual machine-code instructions that reference that
   address, and classify English→Italian by direct byte evidence (identical
   bytes at the same site, same site with a different operand, the operand
   found at a different site, or no match). This full table — 1,002
   symbols, both ROMs — lives in the private research repo; the 131 rows
   RetroAchievements' Game 723 actually depends on, each with its own
   evidence citation, are published in
   [`data/ra_address_triage.csv`](../italian/data/ra_address_triage.csv) (see
   step 5).
5. **RA-address join** — cross-reference the 131 addresses RetroAchievements'
   Game 723 actually depends on against that table, filtering to
   high-confidence (low ROM-bank) evidence only, which is what exposes the
   clean bimodal `+5`/`+0` relocation pattern — see
   [wram-relocation-model.md](../italian/docs/wram-relocation-model.md). Result:
   [`data/ra_address_triage.csv`](../italian/data/ra_address_triage.csv).
6. **Dynamic confirmation** — a targeted set of real-hardware
   (BizHawk + RAIntegration) tests to independently confirm the structural
   `+5` model under actual game logic, not just static byte comparison —
   see [dynamic-testing.md](../italian/docs/dynamic-testing.md).
7. **Generation** — a deterministic address-substitution engine applies the
   confirmed mapping to the official RA asset definitions, producing a
   translated Italian set — see [generation-report.md](generation-report.md).
8. **Audit** — automated checks that the generated set is a faithful,
   metadata-preserving, fully-resolved translation of the official set,
   with exactly one documented exception (achievement 81978).

## Why "bounded region", not "global offset"

A naive global offset (e.g. "add 5 to every WRAM0 address") produces
garbage on either side of the actual insertion point. The falsification
test in [wram-relocation-model.md](../italian/docs/wram-relocation-model.md) rules that out
structurally: filtering ROM cross-reference evidence to trustworthy banks
collapses the observed address deltas into two dominant values (`+5` and
`+0`), each independently corroborated by over 200 evidenced reference
sites, with every other observed delta a one-off coincidental opcode match.
The boundary between the two regions is then pinned from both sides using
the `pret/pokeyellow` source layout.
