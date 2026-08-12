# Pokémon Yellow (Spanish) — RetroAchievements Game 723 Compatibility

**Status: address mapping and generation complete and audited; runtime
achievement-level and full-set testing not yet performed. Do not claim
official RA compatibility yet** — see **What's not yet done** below. Same
stage as [French](../french/README.md) and [German](../german/README.md),
reached independently.

The official Spanish release of Pokémon Yellow ("Pokémon — Edición
Amarilla: Edición Especial Pikachu") does not share all of the WRAM
addresses used by [RetroAchievements Game 723](https://retroachievements.org/game/723)
(76 achievements, 2 leaderboards, Rich Presence — authored against the
English release). This project independently re-derives, for Spanish, the
same kind of result already published for [Italian](../italian/README.md),
[French](../french/README.md), and [German](../german/README.md): a
single, bounded WRAM region that's structurally larger in the localised
ROM, with every RA-referenced address either unshifted or relocated by a
fixed amount. All 131 addresses are resolved and a translated Spanish
asset set is generated and statically audited — but, like French and
German and unlike Italian, it has not yet been loaded into RAIntegration
and confirmed to actually work in game.

This is a **working snapshot of a complete-but-not-runtime-verified
target** in the [Gen I/II regional compatibility project](../../../README.md)
this repo is part of. The full research process — every dead end, every
intermediate hypothesis — lives in a separate private working repository
and is not reproduced here.

## Headline results

| | |
|---|---|
| Game | Pokémon Yellow — official Spanish retail release |
| RetroAchievements | [Game 723](https://retroachievements.org/game/723) — 76 achievements, 2 leaderboards, Rich Presence |
| RA addresses resolved | **131 / 131 (100%), 0 unresolved** — 25 unchanged, 106 relocated (105 by the dominant `+5`, plus 1 tied to the 81978 exception below) |
| Relocation model | Bounded WRAM region, same boundaries as Italian/French/German (`0xcf07`–`0xda98`), independently re-derived from the Spanish ROM — no secondary sub-boundary found — see [docs/wram-relocation-model.md](docs/wram-relocation-model.md) |
| Evidence quality | 54 structural inference, 33 direct symbol match, 24 direct ROM evidence, 10 structural bracketing, 10 direct dynamic (live BizHawk) evidence — 0 addresses left resting on a single-site coincidental match |
| Localisation-specific exception | Exactly one: achievement 81978 (value rewrite, not an address change — see below) |
| Targeted dynamic (real-hardware) WRAM captures | 4 BizHawk sessions covering the rows static evidence couldn't settle alone, plus a 5th corroborating sanity pass — see [docs/dynamic-testing.md](docs/dynamic-testing.md) |
| Offline generation + audit | Full 76-achievement / 2-leaderboard / Rich Presence set generates cleanly, 0 unresolved addresses |
| Achievement-level RAIntegration test | **Not yet performed** |
| Full-set RAIntegration smoke test | **Not yet performed** |

## Try it locally

Copy these two generated files into your RetroAchievements `RACache/Data/`
folder (with the Spanish ROM loaded and RAIntegration in Compatibility
Test mode):

| Generated file | Copy to |
|---|---|
| [`generated/723-Spanish-User.txt`](generated/723-Spanish-User.txt) | `RACache/Data/723-User.txt` |
| [`generated/rich_presence_spanish.txt`](generated/rich_presence_spanish.txt) | `RACache/Data/723-Rich.txt` |

Use the **User** file, not
[`generated/723-Spanish-canonical.txt`](generated/723-Spanish-canonical.txt),
for local testing — the local file uses synthetic IDs at or above
RAIntegration's `FirstLocalId` (`111000001`), which is the only form
RAIntegration will load against an unrecognized ROM hash in Compatibility
Test mode. See Italian's [Generated files, two formats](../italian/README.md#generated-files-two-formats--read-this-before-loading-anything)
for the full explanation — it applies identically here. **This has not
been tried by the project author yet** for Spanish, same as French and
German.

## What differs in the Spanish ROM

Cross-referencing the full symbol map against the Spanish ROM (the same
engine and method used for Italian, French, and German, run fresh — not
seeded from any of them) finds the same structural shape: unshifted below
`0xcf07`, a dominant `+5` delta from `0xcf07` through `0xda97` (388 of 445
all-region `RELOCATED` rows), unshifted again at/after `0xda98` —
identical boundary addresses to all three other localisations, arrived at
independently, with no secondary sub-boundary anomaly (unlike French's
`+6` enemy-party region or German's `+6` at `0xcf08`). Full derivation,
including the one address where Spanish's own evidence disagrees with all
three other localisations (inside the 81978 literal span, not the address
model): [docs/wram-relocation-model.md](docs/wram-relocation-model.md).

## The 131-address mapping

Every RA-referenced address (achievements + leaderboards + Rich Presence)
is individually classified — `IDENTICAL_ADDRESS` (25) or `RELOCATED` (106,
105 at `+5`, 1 tied to the 81978 exception below) — with its own evidence
citation inline, in
[`data/ra_address_triage.csv`](data/ra_address_triage.csv). The per-asset
result of applying that classification is in
[`data/spanish_provenance_report.csv`](data/spanish_provenance_report.csv).

## Achievement 81978 — the one non-address exception

"You're Not Getting Away from Me That Easily" hardcodes literal English
dialogue-tile bytes. A live BizHawk capture of the equivalent Spanish
dialogue ("¡A PIKACHU no le parece bien!") confirms the address range
itself is unshifted (as the relocation model predicts) and reads the
Spanish literal bytes directly — not derived by analogy from any other
localisation's differently sized literal. Full derivation:
[docs/dynamic-testing.md](docs/dynamic-testing.md).

## Generation architecture

The Spanish asset set was produced by the same generic
address-substitution engine used for Italian, French, and German
([`shared/scripts/asset_localizer.py`](../../../shared/scripts/asset_localizer.py)),
driven by a thin per-locale `LocalizationConfig` — no new engine code, only
a new address-triage CSV and overrides file. The config and driver script
live in the private research repo, since both need RA's own raw
achievement export to run. Details: [docs/generation-report.md](../docs/generation-report.md).

## Automated validation

Generation totals: 78 assets (76 achievements + 2 leaderboards), 693
conditions processed, 279 memory references processed (33 unchanged, 701
relocated across all conditions, 1 explicit exception), **0 unresolved
addresses**. Same class of static/audit validation Italian's, French's,
and German's snapshots include — see [docs/generation-report.md](../docs/generation-report.md)
for the shared 7-check audit this passed.

## What's not yet done

Unlike the [Italian target](../italian/README.md), and at the same stage
as [French](../french/README.md) and [German](../german/README.md), this
snapshot does **not** yet include:

- Any achievement loaded as a local achievement in RAIntegration and
  confirmed to fire under real game logic.
- A full-set RAIntegration smoke test (all 76 achievements loaded against
  the real Spanish ROM).

The concrete plan for closing this gap — a 7-item Tier 1 (~10–15 min) plus
3-item Tier 2 (~10–15 min) test set, reusing the same save states across
all four locales — is
[games/yellow/docs/smoke-test-suite.md](../docs/smoke-test-suite.md);
results are tracked per locale in
[smoke-test-results.csv](../docs/smoke-test-results.csv).

Everything published here is static generation plus live WRAM-level
dynamic confirmation of the address model (see
[docs/dynamic-testing.md](docs/dynamic-testing.md)) — real evidence, but
one level below "confirmed working in game." **Do not treat this as RA
Game 723 Spanish compatibility being confirmed** until that runtime
testing happens — see [docs/maintainer-handoff.md](../docs/maintainer-handoff.md)
for the full status and suggested next step.

## Reproduction

This is a **published evidence/handoff snapshot**, not a runnable
reproduction of the generation pipeline — same scope note as
[Italian's README](../italian/README.md#reproduction). What you *can*
verify directly from this repo, without any RA export:

- **Read the evidence.** [`data/ra_address_triage.csv`](data/ra_address_triage.csv)
  classifies all 131 addresses with an inline evidence citation per row;
  [`data/spanish_provenance_report.csv`](data/spanish_provenance_report.csv)
  shows the resulting per-asset substitution.
- **Load the output.** [`generated/723-Spanish-User.txt`](generated/723-Spanish-User.txt)
  and [`generated/rich_presence_spanish.txt`](generated/rich_presence_spanish.txt)
  are the actual generated files — see **Try it locally** above.
- **Read the engine.** [`shared/scripts/asset_localizer.py`](../../../shared/scripts/asset_localizer.py)
  is the actual substitution engine that produced the output above.

## Generated files, two formats — read this before loading anything

Same distinction as Italian's, French's, and German's — **canonical file**
(`generated/723-Spanish-canonical.txt`, official RA asset IDs, the
submission/provenance reference) vs. **local smoke-test file**
(`generated/723-Spanish-User.txt`, synthetic local IDs, the only form
RAIntegration will actually load against an unrecognized ROM hash). Full
explanation: [Italian README, same section](../italian/README.md#generated-files-two-formats--read-this-before-loading-anything).

## ROM / legal note

**No ROM is provided in this repository, and none will be.** The ROM
hashes below are provided purely for identification.

| ROM | MD5 | SHA-1 |
|---|---|---|
| English ("Yellow Version — Special Pikachu Edition") | `d9290db87b1f0a23b89f99ee4469e34b` | `cc7d03262ebfaf2f06772c1a480c7d9d5f4a38e1` |
| Spanish ("Edición Amarilla — Edición Especial Pikachu") | `f0da8b1cff3aab898ecde9dcbda6d817` | `1dc242039218fba50928d1afb66b70565b6b9daf` |

The English SHA-1 matches the hash the `pret/pokeyellow` disassembly builds
from, so its public symbol table is used as the reference for WRAM naming
throughout this project.

## Repository contents

This target lives at `games/yellow/spanish/` within the larger
[Gen I/II regional compatibility project](../../../README.md); paths below
are relative to this directory unless noted.

```
README.md  (this file)
../docs/                       shared across every games/yellow/<locale>/ target
    methodology.md            how the investigation approached the problem
    generation-report.md      what was generated and how it was audited
    maintainer-handoff.md     current status + suggested next step, per locale
docs/                          Spanish-specific
    wram-relocation-model.md  the +5 bounded-region proof, re-derived for Spanish
    dynamic-testing.md        the BizHawk sessions + the 81978 case
data/
    ra_address_triage.csv           the 131 RA-referenced addresses, classified,
                                     with an inline evidence citation per row
    spanish_provenance_report.csv   per-asset result of applying that classification
generated/
    723-Spanish-canonical.txt   official RA asset IDs — submission/provenance reference
    723-Spanish-User.txt        synthetic local IDs — load this one locally, see above
    rich_presence_spanish.txt   translated Rich Presence
```

## Current next step

Address mapping and generation are complete and audited. Before this can
be claimed as RA Game 723 Spanish compatibility, it needs the runtime
testing Italian's target already has: local achievement-firing tests and a
full-set RAIntegration smoke test against a real Spanish ROM. See
[docs/maintainer-handoff.md](../docs/maintainer-handoff.md) for the full
status and suggested path.
