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
| Yellow | [✅ Complete](games/yellow/italian/README.md) | [🟡 Address mapping + generation complete, runtime testing pending](games/yellow/french/README.md) | [🟡 Address mapping + generation complete, runtime testing pending](games/yellow/german/README.md) | — |
| Gold | — | — | — | — |
| Silver | — | — | — | — |
| Crystal | — | — | — | — |

`—` means not yet investigated — not "not compatible." Yellow/Italian has
been fully researched, generated, and runtime-verified; see its
[README](games/yellow/italian/README.md) for the full methodology, results,
and evidence. Yellow/French and Yellow/German each have the same address
mapping and generation work done and audited, independently, but neither
has yet been runtime-tested in RAIntegration — see their own READMEs
([French](games/yellow/french/README.md), [German](games/yellow/german/README.md))
for what's proven and what's still open.

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
shared/
    scripts/            reusable engine, shared across every game/locale
        asset_localizer.py      generic address-substitution engine (reference only)
        csv_safety.py           atomic CSV read/write helper it depends on
games/
    yellow/
        docs/            shared across every games/yellow/<locale>/ target
            methodology, generation report, maintainer handoff
        italian/         fully researched, generated, and runtime-verified
            README.md    maintainer-facing writeup for Game 723
            data/        the address-triage evidence + per-asset provenance report
            docs/        locale-specific: relocation model, dynamic testing
            generated/   the actual generated/testable output (canonical + local RA files, Rich Presence)
        french/          address mapping + generation complete, runtime testing pending
            (same structure as italian/ above)
        german/          address mapping + generation complete, runtime testing pending
            (same structure as italian/ above)
```

Red, Blue, Gold, Silver, Crystal, and the Spanish target don't have
directories yet — they'll be added under `games/<game>/<locale>/` following
the same structure as `games/yellow/italian/` once actually investigated.
The shared engine under `shared/scripts/` is game/locale-agnostic; a new
target only needs its own evidence data and a thin config on top of it, not
a copy of the engine — though, as with Yellow/Italian, Yellow/French, and
Yellow/German, the config and the driver scripts that actually run it stay
in the private research repo, since they depend on RA's own raw per-target
achievement export.

## Getting started

Pure standard library — see [requirements.txt](requirements.txt). This
repo has no generation pipeline to run: each target under `games/` is a
self-contained evidence snapshot — see its own README for its results and
how to load its generated output for local testing.
