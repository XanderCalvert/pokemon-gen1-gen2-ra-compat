# Maintainer handoff

## What's proven

- All 131 WRAM addresses RetroAchievements Game 723 depends on are
  classified with 0 unresolved: 30 unchanged, 101 relocated (99 by the
  dominant `+5` within one bounded WRAM region — not a global offset — and
  2 tied to the documented 81978 literal exception below) (see
  [wram-relocation-model.md](wram-relocation-model.md)).
- The relocation model is confirmed both statically (ROM cross-reference
  evidence) and dynamically (7/7 real-hardware tests against the actual
  Italian ROM — see [dynamic-testing.md](dynamic-testing.md)).
- The full 76-achievement / 2-leaderboard / Rich Presence Italian set
  generates deterministically from the official set and passes an
  automated audit: 1:1 asset mapping, unchanged metadata, preserved
  condition structure, 0 unresolved addresses (see
  [generation-report.md](generation-report.md)).
- Exactly one asset (achievement 81978) needs a value/literal change rather
  than an address change, and that change is derived and documented from a
  live dialogue-buffer read, not guessed.

## What's still open

This is a compatibility investigation and a generated candidate patch, not
yet a submitted or reviewed one. Before this becomes a live Italian-ROM
achievement set on RetroAchievements, it still needs:

- **Maintainer/QA review of the generated Italian condition strings**
  against RA's own submission and QA standards for a new supported ROM
  hash — this repo does not attempt to speak for that process.
- **Broader in-game soak testing** beyond the 7 targeted dynamic tests —
  those were chosen to stress the riskiest/most representative parts of
  the address space (array offsets, multi-byte event-flag blocks, a
  literal-value rewrite, map-ID guards), not to exhaustively play through
  every one of the 76 achievements.
- **A decision on distribution mechanism** — whether this becomes an
  additional supported ROM hash on the existing Game 723, a separate
  entry, or something else, is a RetroAchievements policy question outside
  this project's scope.

## Suggested path

1. A Game 723 maintainer (or RA QA team member) reviews this repo's
   methodology and results — the evidence, provenance, and generated
   output here are sufficient for that review on their own.
2. If the approach looks sound and a maintainer wants the candidate patch
   regenerated against a fresh official RA export (e.g. after upstream
   Game 723 changes), that's done from the private research repo this
   snapshot was published from — this repo intentionally doesn't include
   the generation pipeline itself, since it depends on RA's own raw
   achievement export, which isn't this project's to publish. Reach out to
   the project author to run a regeneration; the address-mapping/
   relocation result itself won't change, since it's already fully
   resolved and audited.
3. Route the generated candidate through RetroAchievements' normal
   ROM-hash-addition / achievement-set review process.

Questions about the investigation itself (the relocation model, the 81978
exception, the dynamic test results) can be answered from the docs in this
repo. Questions about RA's submission process should go through RA's
normal maintainer/QA channels.
