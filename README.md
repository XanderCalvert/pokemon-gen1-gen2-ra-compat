# Pokémon Gen I & II — RetroAchievements Regional Compatibility

This repository is a public evidence/handoff snapshot for regional
compatibility work on RetroAchievements sets authored against the English
releases of the Game Boy / Game Boy Color Pokémon games, so they can also
work against other official regional ROM releases. The research, address
mapping, generation, and automated auditing are performed in a private
research repository; what's published here is the resulting evidence,
provenance, and testable output for a RetroAchievements maintainer or QA
team — not the internal research toolchain itself. It covers, or intends
to eventually cover:

- **Games:** Red, Blue, Yellow, Gold, Silver, Crystal
- **Potential regional targets:** Italian, French, German, Spanish

Each game/region combination is its own investigation: a different ROM, a
different WRAM layout, a different relocation model, and its own evidence.
Nothing here is assumed to generalize until it's actually been investigated
for that specific combination.

## Status

| Game | Italian | French | German | Spanish |
|---|---|---|---|---|
| Red | — | — | — | — |
| Blue | — | — | — | — |
| Yellow | [✅ Complete](games/yellow/italian/README.md) | [✅ Generated & validated, runtime testing pending](games/yellow/french/README.md) | [✅ Generated & validated, runtime testing pending](games/yellow/german/README.md) | [✅ Generated & validated, runtime testing pending](games/yellow/spanish/README.md) |
| Gold | — | — | — | — |
| Silver | — | — | — | — |
| Crystal | — | — | — | — |

`—` means not yet investigated — not "not compatible." Yellow/Italian has
been fully researched, generated, and runtime-verified; see its
[README](games/yellow/italian/README.md) for the full methodology, results,
and evidence. Yellow/French, Yellow/German, and Yellow/Spanish each have
the same address mapping and generation work done and audited,
independently, but none has yet been runtime-tested in RAIntegration — see
their own READMEs ([French](games/yellow/french/README.md),
[German](games/yellow/german/README.md), [Spanish](games/yellow/spanish/README.md))
for what's proven and what's still open.

### Bonus achievement sets (RetroAchievements Game 723, Yellow)

RA game 723 also has two bonus achievement sets layered on top of the core
set above. Both reuse addresses already proven for the core set — no new
address risk — so their own runtime coverage is scoped down to the
structural patterns each one introduces; see
[smoke-test-suite-8486.md](games/yellow/docs/smoke-test-suite-8486.md) for
the design and [smoke-test-results-8486.csv](games/yellow/docs/smoke-test-results-8486.csv)
for the PASS/FAIL/NOT RUN tracking grid.

| Set | Description | Status |
|---|---|---|
| 8486 | Prof. Oak Challenge | ✅ Generated & validated for all four locales, smoke-test suite designed, runtime testing pending |
| 3440 | — | ✅ Generated & validated for all four locales, runtime testing pending |

### Regional build matrix

Across the core set (723) and both bonus sets (8486, 3440), all four
additional European locales (Italian, French, German, Spanish) have now
been generated from the English source — **12 regional set/language
builds** in total. Every one of the 12:

- generates successfully from the English source,
- has zero unresolved address mappings,
- passes generation validation,
- regenerates byte-for-byte deterministically,
- preserves the source set's metadata and condition structure,
- uses shared, version-level address evidence (no per-set address remapping),
- has no cross-set address-mapping disagreements.

This is "generated and validated," not "live on RetroAchievements" —
Italian/723 is the only combination that's also been runtime-verified in
RAIntegration so far; see [Status](#status) above for what's proven per
locale. See [Build hashing / provenance](#build-hashing--provenance) below
for how each of these 12 builds is fingerprinted, and
[games/yellow/build_manifest.json](games/yellow/build_manifest.json) for
the full per-asset evidence.

## ROM versions

See [rom-hashes.md](rom-hashes.md) for the exact MD5/SHA1 of every ROM dump
this project targets or has targeted, across every game/language above, and
what's explicitly out of scope (fan translations, Japanese, Korean). No ROM
file is included in this repository, or ever will be — only identifying
hashes.

## Repository layout

```
README.md
requirements.txt
scripts/
    snapshot-manifest.txt    allowlist consumed by update-snapshot.sh (maintainer-only sync tool)
    update-snapshot.sh       pulls the allowlisted files from the private repo into this one
shared/
    scripts/            reusable engine, shared across every game/locale
        asset_localizer.py      generic address-substitution engine (reference only)
        csv_safety.py           atomic CSV read/write helper it depends on
games/
    yellow/
        build_manifest.json     imported provenance/hash record for all 12 generated
            set/language builds -- produced by the private repo's own build tooling
            against its raw generation inputs (not published here); this repo carries
            the resulting manifest as evidence, it does not regenerate it
        docs/            shared across every games/yellow/<locale>/ target
            methodology, generation report, maintainer handoff
            smoke-test-suite.md      cross-locale runtime smoke-test plan (design only)
            smoke-test-results.csv   PASS/FAIL/NOT RUN tracking grid, one row per test x locale
            smoke-test-suite-8486.md      Set 8486 (bonus) smoke-test plan (design only)
            smoke-test-results-8486.csv   Set 8486 PASS/FAIL/NOT RUN tracking grid
        italian/         fully researched, generated, and runtime-verified
            README.md    maintainer-facing writeup for Game 723
            data/        the address-triage evidence + per-asset provenance report
            docs/        locale-specific: relocation model, dynamic testing
            generated/   the actual generated/testable output (canonical + local RA files, Rich Presence)
        french/          address mapping + generation complete, runtime testing pending
            (same structure as italian/ above)
        german/          address mapping + generation complete, runtime testing pending
            (same structure as italian/ above)
        spanish/         address mapping + generation complete, runtime testing pending
            (same structure as italian/ above)
```

Red, Blue, Gold, Silver, and Crystal don't have directories yet — they'll
be added under `games/<game>/<locale>/` following the same structure as
`games/yellow/italian/` once actually investigated. The shared engine
under `shared/scripts/` is game/locale-agnostic; a new target only needs
its own evidence data and a thin config on top of it, not a copy of the
engine — though, as with every Yellow locale above, the config and the
driver scripts that actually run it stay in the private research repo,
since they depend on RA's own raw per-target achievement export.

## Build hashing / provenance

[games/yellow/build_manifest.json](games/yellow/build_manifest.json) is an
**imported provenance artefact**: it's produced by hashing/canonicalisation
tooling in the private research repo, run there against raw generation
inputs (per-locale `ra_asset_definitions.csv`, English source, etc.) that
aren't published here. This repo carries the resulting manifest as
published evidence of what was proven at generation time -- it does not,
and isn't meant to, regenerate it from raw inputs itself.

Every generated asset (achievement, leaderboard, Rich Presence) in the
manifest carries two SHA-256 fingerprints:

**`artifact_sha256`** — hashes the exact generated representation (the raw
CSV row, or raw file bytes for Rich Presence). Detects whether the generated
artefact itself changed byte-for-byte.

**`logic_sha256`** — hashes a canonicalised representation of the effective
RA logic: condition groups/order, flags, operands, addresses, operators,
literals, hit counts (or, for Rich Presence, the Format/Lookup/Display
structure). Insensitive to hex case, leading zeros, and other formatting
that doesn't change runtime behaviour. Detects whether achievement behaviour
changed, ignoring irrelevant formatting/serialisation differences.

The distinction is the useful part:

```
artifact changed + logic unchanged
= representation changed, achievement behaviour did not

logic changed
= runtime achievement logic changed and should be reviewed/retested
```

This supplements Git — it doesn't replace it. Git shows *that* a generated
file changed; the manifest says *whether that change could affect what an
achievement actually does in-game*, independent of incidental
regeneration/formatting noise.

Each manifest record also retains the source English RA asset ID, the local
RAIntegration test ID it was smoke-tested under, the language, the set ID,
and a nullable `target_ra_id`. Once a regional set is actually published on
RetroAchievements, its live RA ID can be filled into `target_ra_id` and
checked against the exact `logic_sha256` it was locally tested against —
so "what's live" can be verified against "what was proven," not just
assumed to match.

### The 12 build fingerprints

Aggregate `logic_sha256` per set/language build (each aggregate is a hash of
that build's own sorted per-asset hashes — reordering assets never changes
it). Per-achievement hashes live in
[build_manifest.json](games/yellow/build_manifest.json), not here.

| Set | Language | Logic SHA-256 |
|---|---|---|
| 723 | Italian | `a5a349fbd10f2c5c4a589861471c4c18de486ff9ce94de0fec580d7ec0016743` |
| 723 | French | `b7cfe02b10cfc9e8ec05166df7f2748125f44382bcbaaa9f6068c563a51f6ae9` |
| 723 | German | `5563d87bc33484a46ad6e3026e518f79b749b31f880138a2cad25d7df28afa55` |
| 723 | Spanish | `df967e0829ff1670d0e07c84379bfeb0741f71256a9f0c9ba82476024c7320f3` |
| 8486 | Italian | `44db84b18923ccc98bd28972f37ea7ad9f55dc0131a8f2ab939ca0a0dc647e30` |
| 8486 | French | `44db84b18923ccc98bd28972f37ea7ad9f55dc0131a8f2ab939ca0a0dc647e30` |
| 8486 | German | `44db84b18923ccc98bd28972f37ea7ad9f55dc0131a8f2ab939ca0a0dc647e30` |
| 8486 | Spanish | `44db84b18923ccc98bd28972f37ea7ad9f55dc0131a8f2ab939ca0a0dc647e30` |
| 3440 | Italian | `b17fc7304459a12c857e2ac266d506a536f76f85146106e181eb3d079748c904` |
| 3440 | French | `a6b2596897a0ad814ef8d9147b066f350501d2c52ce9836b1faaaa68410b68cf` |
| 3440 | German | `dc624ad66adf61babc3794bc121c6ec006803de30fd3252c3fa840f0625266b7` |
| 3440 | Spanish | `bdf8dbed9f7ed44e442bca8e43d8684d2afe3f2ef38f698ad048baff553952fc` |

8486's logic hash is identical across all four locales: it reuses addresses
already proven for the core set with no set-specific address remapping, so
there's no per-locale logic difference for the hash to pick up.

Whole-build aggregate (all 12 builds, all locales):
`logic_sha256 = f122df674d051d452800cc4407ef4a08e75dec665e9aab9a5e0983438613d4d7`

### Reproducing / verifying the hashes

Hashing and `--verify` are private-repo operations: they run against raw
generation inputs (`ra_asset_definitions.csv` per set/locale, English
source, etc.) that this repo deliberately doesn't publish, so the tooling
that produces `build_manifest.json` lives there, not here. What's here is
the resulting manifest and the per-build fingerprint table above, published
as evidence of what the private build proved — not a self-contained
reproduction pipeline.

### A localisation exception worth knowing about

Most Yellow localisation is address/value substitution against a fixed
tilemap layout. Occasionally translated text reflows the screen enough that
the substitution needs to become semantic rather than positional. Set 3440's
nickname-detection achievement is the example in this manifest: English,
Italian, French, and Spanish all use a species-independent nickname-prompt
text row at the same original tilemap location. German's sentence order
puts the species name in that row instead, so the German build watches the
invariant `Spitznamen geben?` row rather than the English screen coordinate
— preserving the achievement's original intent instead of copying a
location that no longer means the same thing in German. This is exactly
the kind of change `logic_sha256` is built to catch: the private repo's
regression suite for the hashing tool asserts the German and English logic
hashes for that achievement differ, and the published fingerprint table
above reflects it (3440's German hash differs from Italian/French/Spanish).

## Getting started

Pure standard library — see [requirements.txt](requirements.txt). This
repo has no generation pipeline to run: each target under `games/` is a
self-contained evidence snapshot — see its own README for its results and
how to load its generated output for local testing.
