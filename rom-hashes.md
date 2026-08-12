# ROM Hash Master

MD5/SHA1 identifying hashes for the exact ROM dump this project targets, per
game and language. **No ROM file is included in this repository, or ever
will be** — these hashes exist purely so you can confirm your own
legally-owned dump is byte-for-byte identical to what this project's
evidence and generated output were produced against, not a bad dump or a
fan hack. Generated in the private working repo via PowerShell
`Get-FileHash`; filenames below follow that repo's internal
`roms/<game>/<language>/` layout convention, not a path in this one.

Only `games/yellow/` has evidence/generation output published in this repo
so far (see [games/yellow/](games/yellow/)) — the other games below are
listed for scope/reference: hashed and version-identified, not yet
researched.

No-Intro is a ROM-preservation project that maintains canonical checksums
for one verified-good, unmodified dump per game/region/revision — matching
its published MD5/SHA1 is how you confirm a file is byte-for-byte identical
to what actually shipped on the cartridge, not a bad dump or a hack.

**Verified** = cross-checked against the No-Intro database (via web search)
and confirmed an exact MD5/SHA1 match. **Unconfirmed** = file size matches a
legitimate dump (1 MiB for GB, 2 MiB for GBC) but no published No-Intro
checksum could be found to compare against — not flagged as wrong, just not
independently corroborated.

## Yellow

| Language | Filename | Size | MD5 | SHA1 | Status |
|---|---|---|---|---|---|
| English | `yellow/english/Pokemon - Yellow Version - Special Pikachu Edition.gb` | 1048576 | `d9290db87b1f0a23b89f99ee4469e34b` | `cc7d03262ebfaf2f06772c1a480c7d9d5f4a38e1` | Pre-existing (trusted) |
| French | `yellow/french/Pokemon - Version Jaune - Edition Speciale Pikachu (France) (GBC,SGB Enhanced).gb` | 1048576 | `2df6b439a35e0d511d52fa75c6a7849a` | `0aceec0ef7aa2ca5aa831554598d91f61a925591` | Pre-existing (trusted) |
| German | `yellow/german/Pokemon - Gelbe Edition - Special Pikachu Edition (Germany) (GBC,SGB Enhanced).gb` | 1048576 | `e93f10168e3c9b9d18e3ad4a1415e1d0` | `42f3714eec6eca25200d42461ff08d57c98f6d1d` | Pre-existing (trusted) |
| Italian | `yellow/italian/Pokemon - Versione Gialla - Speciale Edizione Pikachu (Italy).gb` | 1048576 | `3343ceca5dd6586e4774609526167d55` | `05bb8e99f24d498613930949730afa8024e77d08` | Pre-existing (trusted) |
| Spanish | `yellow/spanish/Pokemon - Edicion Amarilla - Edicion Especial Pikachu (Spain) (GBC,SGB Enhanced).gb` | 1048576 | `f0da8b1cff3aab898ecde9dcbda6d817` | `1dc242039218fba50928d1afb66b70565b6b9daf` | Pre-existing (trusted) |

## Red

| Language | Filename | Size | MD5 | SHA1 | Status |
|---|---|---|---|---|---|
| English | `red/english/Pokemon - Red Version (USA, Europe) (SGB Enhanced).gb` | 1048576 | `3d45c1ee9abd5738df46d2bdda8b57dc` | `ea9bcae617fdf159b045185467ae58b2e4a48b9a` | Verified (No-Intro) |
| German | `red/german/Pokemon - Rote Edition (Germany) (SGB Enhanced).gb` | 1048576 | `8ed0e8d45a81ca34de625d930148a512` | `87d523fe1a0c548db7c5477b451ddec1eb083c06` | Verified (No-Intro) |
| French | `red/french/Pokemon - Version Rouge (France) (SGB Enhanced).gb` | 1048576 | `669700657cb06ed09371cdbdef69e8a3` | `47a7622fa30e6402a3891fe65b3a930bf9bd7aec` | Verified (No-Intro) |
| Italian | `red/italian/Pokemon - Versione Rossa (Italy) (SGB Enhanced).gb` | 1048576 | `6468fb0652dde30eb968a44f17c686f1` | `65b97cf8f2f1cff711a6d08c6c894c8ce65ce522` | Unconfirmed |
| Spanish | `red/spanish/Pokemon - Edicion Roja (Spain) (SGB Enhanced).gb` | 1048576 | `463c241c8721ab1d1da17c91de9f8a32` | `fc17c5b904d551b1b908054ccd1c493f755f832a` | Verified (No-Intro) |

## Blue

| Language | Filename | Size | MD5 | SHA1 | Status |
|---|---|---|---|---|---|
| English | `blue/english/Pokemon - Blue Version (USA, Europe) (SGB Enhanced).gb` | 1048576 | `50927e843568814f7ed45ec4f944bd8b` | `d7037c83e1ae5b39bde3c30787637ba1d4c48ce2` | Verified (No-Intro) |
| German | `blue/german/Pokemon - Blaue Edition (Germany) (SGB Enhanced).gb` | 1048576 | `a1ec7f07c7b4251d5fafc50622d546f8` | `20e72dc6f41493eee1fdd0cef54214e6c3389688` | Unconfirmed |
| French | `blue/french/Pokemon - Version Bleue (France) (SGB Enhanced).gb` | 1048576 | `35c8154c81abb2ab850689fd28a03515` | `47faa910d0e073c600665bf9c83b6bd17babdf8a` | Verified (No-Intro) |
| Italian | `blue/italian/Pokemon - Versione Blu (Italy) (SGB Enhanced).gb` | 1048576 | `ebe0742b472b3e80a9c6749f06181073` | `f69ed1a1332f04c24c7db899a09019bb045fa8b3` | Unconfirmed |
| Spanish | `blue/spanish/Pokemon - Edicion Azul (Spain) (SGB Enhanced).gb` | 1048576 | `6e7663f908334724548a66fc9c386002` | `7715e7b133e8634df48918b9138374110212a108` | Verified (No-Intro) |

## Gold

| Language | Filename | Size | MD5 | SHA1 | Status |
|---|---|---|---|---|---|
| English | `gold/english/Pokemon - Gold Version (USA, Europe) (SGB Enhanced).gbc` | 2097152 | `a6924ce1f9ad2228e1c6580779b23878` | `d8b8a3600a465308c9953dfa04f0081c05bdcb94` | Verified (No-Intro) |
| German | `gold/german/Pokemon - Goldene Edition (Germany) (SGB Enhanced).gbc` | 2097152 | `7542ec9b695d4fe38adfdaaa57364d83` | `9254195d461ea942eaaa08cc4b83de3cf82aea0d` | Verified (No-Intro) |
| French | `gold/french/Pokemon - Version Or (France) (SGB Enhanced).gbc` | 2097152 | `9af19423c5fa3dbe4fdcc78d2bc7d1c0` | `c147c0d8c2b71b7628a7233436f5c052b5b17081` | Verified (No-Intro) |
| Italian | `gold/italian/Pokemon - Versione Oro (Italy) (SGB Enhanced).gbc` | 2097152 | `89bb59dc49b59b0cd30b7384d9860bb8` | `032608fe8947b627584a4a0eccc7bf9ad3588426` | Unconfirmed |
| Spanish | `gold/spanish/Pokemon - Edicion Oro (Spain) (SGB Enhanced).gbc` | 2097152 | `9462bc81907e38c59acccd739690e6f9` | `162ea54c6a3cff374642e6dd842f9bffac847e7b` | Verified (No-Intro) |

## Silver

| Language | Filename | Size | MD5 | SHA1 | Status |
|---|---|---|---|---|---|
| English | `silver/english/Pokemon - Silver Version (USA, Europe) (SGB Enhanced).gbc` | 2097152 | `2ac166169354e84d0e2d7cf4cb40b312` | `49b163f7e57702bc939d642a18f591de55d92dae` | Verified (No-Intro) |
| German | `silver/german/Pokemon - Silberne Edition (Germany) (SGB Enhanced).gbc` | 2097152 | `f1f013cd591bc4ea77305bbc9f8cbb3c` | `8ecc58d621faaedf2a934bd2583d527220df7bb9` | Verified (No-Intro) |
| French | `silver/french/Pokemon - Version Argent (France) (SGB Enhanced).gbc` | 2097152 | `72448fe75f534f70cd90469da95ef76f` | `a4a7e8079b7a53e4d9ef43382bbb1090b9d45d1a` | Verified (No-Intro) |
| Italian | `silver/italian/Pokemon - Versione Argento (Italy) (SGB Enhanced).gbc` | 2097152 | `9357c3dab850692ac8184ccf655d4efd` | `c9eca9d0a837beb9137bb7d779e469c54e9f8d77` | Unconfirmed |
| Spanish | `silver/spanish/Pokemon - Edicion Plata (Spain) (SGB Enhanced).gbc` | 2097152 | `2d83fb454dd5687a802425c501854dc2` | `05bd978ab2cb104b0aff3f696896e30885203a18` | Unconfirmed |

## Crystal

| Language | Filename | Size | MD5 | SHA1 | Status |
|---|---|---|---|---|---|
| English | `crystal/english/Pokemon - Crystal Version (USA, Europe) (Rev A).gbc` | 2097152 | `301899b8087289a6436b0a241fbbb474` | `f2f52230b536214ef7c9924f483392993e226cfb` | Verified (No-Intro) |
| German | `crystal/german/Pokemon - Kristall-Edition (Germany).gbc` | 2097152 | `a35c0fa2e3b3d1c1779cd9f2352bc427` | `accb584293ba056152f1fd908439b019017ff2fe` | Unconfirmed |
| French | `crystal/french/Pokemon - Version Cristal (France).gbc` | 2097152 | `45d988bdb6cfcc334134dd212cefb7b8` | `c055992b16b7399c687647725cdd1f4f13a2f75c` | Unconfirmed |
| Italian | `crystal/italian/Pokemon - Versione Cristallo (Italy).gbc` | 2097152 | `7c513823f65b92a75e29067745839cc8` | `6cee05e5b95beeae74b8365ad18ec4a07a8c4af8` | Unconfirmed |
| Spanish | `crystal/spanish/Pokemon - Edicion Cristal (Spain).gbc` | 2097152 | `8a626340f6b16ba45c1d4e07f2134875` | `889a06fc0bb863666865aa69def0adf97945ac2a` | Verified (No-Intro) |

Every game above now has all 5 target languages hashed and version-identified
in the private working repo.

**Unconfirmed rows are not a red flag** — No-Intro's checksum for those
specific regional dumps just didn't surface in search results. Sizes match
known-good dumps (1 MiB GB / 2 MiB GBC, no header anomalies). Re-run
`Get-FileHash` and diff against No-Intro's DAT-o-MATIC directly if you want
a harder guarantee on those six.

## Fan translations are out of scope

This project only covers **official commercial releases**. Fan translation
patches are explicitly excluded, not just deprioritized.

Reason: fan patches don't just translate text, some rewrite game logic —
e.g. changing type-chart matchups to match a later generation, which isn't
in the original Gen 1 engine. A patch like that changes what counts as a
correct trigger condition, not just the strings around it, which breaks the
entire premise this project runs on (that every language version is the
same game logic at a relocated address). Vetting each fan patch for silent
gameplay changes isn't something this project takes on — official carts
only.

**Japanese** — not just another language variant. Japanese Red/Green/Blue/
Yellow and Gold/Silver/Crystal run on meaningfully different engines/data
(different map IDs, different move data, no Time Capsule compatibility with
Western Gen 1, etc.) — closer to a different game than a relocated address
map. Out of scope for the same reason a fan translation is: the core
premise here is "same game logic, different address," and Japanese doesn't
meet that bar.

**Korean** — no official Korean release exists for Yellow, or for Gen 1 at
all (Red/Blue/Yellow never shipped in Korean). Gold/Silver *did* get an
official Korean release in 2002 — a real commercial cart, not a fan patch —
but it was built off the *Japanese* ROM rather than the Western one, so it
inherits the same Japanese-base exclusion above. Korean Crystal was never
officially localized at all; any Korean Crystal in the wild is a fan
translation. Net result: there's no official Korean Yellow ROM this project
could ever add.
