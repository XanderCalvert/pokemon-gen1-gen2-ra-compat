# Maintainer handoff

Two locales are covered so far, at different stages of readiness. Both
share the same methodology and generation engine; what differs is how far
each has been runtime-tested.

## Italian — ready for maintainer review

### What's proven

- All 131 WRAM addresses RetroAchievements Game 723 depends on are
  classified with 0 unresolved: 30 unchanged, 101 relocated (99 by the
  dominant `+5` within one bounded WRAM region — not a global offset — and
  2 tied to the documented 81978 literal exception below) (see
  [wram-relocation-model.md](../italian/docs/wram-relocation-model.md)).
- The relocation model is confirmed both statically (ROM cross-reference
  evidence) and dynamically (7/7 real-hardware tests against the actual
  Italian ROM, including local achievements firing in RAIntegration under
  real game logic — see [dynamic-testing.md](../italian/docs/dynamic-testing.md)).
- The full 76-achievement / 2-leaderboard / Rich Presence Italian set
  generates deterministically from the official set and passes an
  automated audit: 1:1 asset mapping, unchanged metadata, preserved
  condition structure, 0 unresolved addresses (see
  [generation-report.md](generation-report.md)).
- Exactly one asset (achievement 81978) needs a value/literal change rather
  than an address change, and that change is derived and documented from a
  live dialogue-buffer read, not guessed.
- The full generated set was manually loaded into RAIntegration against
  the Italian ROM: all 76 achievements loaded (458 points), and one
  triggered naturally from a fresh save.

### What's still open

- **Maintainer/QA review of the generated Italian condition strings**
  against RA's own submission and QA standards for a new supported ROM
  hash — this repo does not attempt to speak for that process.
- **Broader in-game soak testing** beyond the 7 targeted dynamic tests —
  those were chosen to stress the riskiest/most representative parts of
  the address space, not to exhaustively play through every achievement.
- **A decision on distribution mechanism** — whether this becomes an
  additional supported ROM hash on the existing Game 723, a separate
  entry, or something else, is a RetroAchievements policy question outside
  this project's scope.

## French — address mapping and generation complete, runtime testing not started

### What's proven

- All 131 WRAM addresses are classified with 0 unresolved: 20 unchanged,
  111 relocated (99 by the dominant `+5`, 1 tied to the 81978 exception),
  independently re-derived from the French ROM using the same method as
  Italian — see [wram-relocation-model.md](../french/docs/wram-relocation-model.md).
- The relocation model is confirmed by 8 phases of live BizHawk WRAM
  read/write captures against the real French ROM — see
  [dynamic-testing.md](../french/docs/dynamic-testing.md).
- The full 76-achievement / 2-leaderboard / Rich Presence French set
  generates deterministically and passes the same automated audit as
  Italian: `verify_phase8_remap.py --target-version french` passes in
  full, 0 unresolved addresses.
- The 81978 literal exception is derived from a direct live dialogue-buffer
  read against the French ROM, not by analogy to Italian's differently
  sized literal.

### What's still open — this is the material gap vs. Italian

- **No achievement has been loaded as a local achievement in RAIntegration
  and confirmed to fire under real game logic.** Every French dynamic test
  so far is a WRAM-level memory read/write, one step below Italian's
  achievement-firing confirmation.
- **No full-set RAIntegration smoke test has been run.** Italian's 76/458
  full-load result has no French equivalent yet.
- Everything else in Italian's "still open" list above (maintainer/QA
  review, broader soak testing, distribution-mechanism decision) applies
  here too, once the runtime gap above is closed.

**Do not represent French as RA-compatible or submission-ready** until the
runtime testing above happens — the static/generation work is done, the
in-game confirmation is not.

## Suggested path (both locales)

1. A Game 723 maintainer (or RA QA team member) reviews this repo's
   methodology and results — the evidence, provenance, and generated
   output here are sufficient for that review on their own, for Italian
   now and for French once its runtime gap is closed.
2. If the approach looks sound and a maintainer wants a candidate patch
   regenerated against a fresh official RA export (e.g. after upstream
   Game 723 changes), that's done from the private research repo this
   snapshot was published from — this repo intentionally doesn't include
   the generation pipeline itself, since it depends on RA's own raw
   achievement export, which isn't this project's to publish. Reach out to
   the project author to run a regeneration; the address-mapping/
   relocation result itself won't change for either locale, since both are
   already fully resolved and audited.
3. Route the generated candidate through RetroAchievements' normal
   ROM-hash-addition / achievement-set review process.

Questions about the investigation itself (the relocation model, the 81978
exception, the dynamic test results) can be answered from the docs in this
repo. Questions about RA's submission process should go through RA's
normal maintainer/QA channels.
