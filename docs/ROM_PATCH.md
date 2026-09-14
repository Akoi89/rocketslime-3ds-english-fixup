# The self-contained ROM patch

One xdelta turns the decrypted Japanese .cci into a .cci with Team Rocket Slime's
RC1 translation and the fix-up's changes inside. No SD files, no patcher, no Luma.

## Why RC1 needed the SD card, and what changed

RC1's `code.ips` adds a loader in the padding after the end of .text (va 0x3EBCC8)
and hooks the game in three places:

| where | what RC1 does | ROM patch |
|---|---|---|
| va 0x100000 (entry) | reserves 1 MB RW at 0x0C000000 for the script | unchanged |
| va 0x105900 | mounts the SD card as `_:` and reads `/fti/rocket_slime_3ds/tables.bin` with FSUSER_OpenFileDirectly (archive 9), no fallback | reads the game's own RomFS instead (below) |
| va 0x2B0E1C (game's file open) | tries `_:/fti/rocket_slime_3ds/<path>` first, falls back to the RomFS file | unchanged: with no SD folder it falls back to the files built into RomFS |

Loader edits (each old word is asserted before patching):

| va | old | new |
|---|---|---|
| 0x3EBD70 | `mov r3, #9` (SD) | `mov r3, #3` (own RomFS) |
| 0x3EBD84 | `mov r5, #3` (ASCII path) | `mov r5, #2` (binary path) |
| 0x3EBD94 | `mov r5, #0x21` | `mov r5, #0xc` |
| 0x3EBDBC | `mov r2, #0` (read offset) | `ldr r2, =0x4BD10` |
| 0x3EBDCC | `ldr r4, [sp, #0x10]` (GetSize) | `ldr r4, =942610` |
| literal 0x3EBE68 | 0x3EBCC8 (path string) | 0x3EBE70 (12 zero bytes) |

One more word, outside the loader, since fix-up 2: the name-entry keyboard's reset
routine calls its set-page function with page 0 (hiragana). The edit makes it page 2,
the ABC tab.

| va | old | new |
|---|---|---|
| 0x3B61E8 | `mov r1, #0` (hiragana) | `mov r1, #2` (ABC) |

Archive 3 with a 12-byte zero binary path opens RomFS level 3 raw, the same way
libctru's romfsInit does. 0x4BD10 is where `tables.bin` sits in level 3 of the
rebuilt RomFS; the build script computes it and checks the bytes. Call targets were
confirmed by their IPC headers: 0x2B99C4 sends 0x08030204 (OpenFileDirectly),
0x2E63A4 sends 0x080200C2 (Read), 0x2E64A8 sends 0x08040000 (GetSize).

## Building it

The build scripts are `tools/build_rom.py` and `tools/make_rom_xdelta.py` (they
need 3dstool, ctrtool, xdelta3 and RC1's `code.ips`). The build uses 3dstool with
`--not-encrypt` and `--not-pad`, recompresses the code with `-z`, zeroes the card
seed at 0x1010, and re-extracts every part to compare it with what went in. The patch is encoded against a copy of the retail
file with its 0x4000 header scrambled (the decryptor writes a random card seed at
0x1010..0x103B, so no two dumps match there), with `-a` and `-A`.

## Verified for fix-up 9 (2026-09-14)

- unpacked code.bin equals the known clean code (md5 ab181c1d...)
- `tables.bin` sits at level-3 offset 0x4BD10, 942,610 bytes, same as in fix-up 1
- patched .cci boots in Azahar with no SD folder and no mods: English title,
  menus, narration and tutorial
- patch 4,460,185 B, no local paths inside; decodes to the same .cci
  (sha256 57dc9c5ba7b6f35ad86b11775259273fcaa3e58cec21c81a9010f4ef7d5a3958) from the
  real dump and from two dumps with a different random seed

Each release is checked the same way. The patch size and result hash for every
release are on its release page.

Players who had RC1 installed must remove `sd:/fti/rocket_slime_3ds/` (it overrides
the RomFS files) and `sd:/luma/titles/000400000005C300/code.ips` (Luma would apply
RC1's code patch again and undo the loader edit).
