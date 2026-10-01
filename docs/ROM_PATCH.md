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

Two more words change with those: the literal pool slots the two `ldr` rows read from,
at 0x3EBE80 (0x4BD10) and 0x3EBE84 (942610), which the build script writes into the free
space after the loader. Nine words of the loader differ from RC1's. A word-by-word diff
of the shipped code against retail plus RC1's `code.ips` finds those nine, the keyboard
word and the six rank-name words below, and nothing else.

One more word, outside the loader, since fix-up 2: the name-entry keyboard's reset
routine calls its set-page function with page 0 (hiragana). The edit makes it page 2,
the ABC tab.

| va | old | new |
|---|---|---|
| 0x3B61E8 | `mov r1, #0` (hiragana) | `mov r1, #2` (ABC) |

Six more words since fix-up 12, for the rank-up message. The game keeps the names it
drops into a line (the `{1F:xA0}` inserts; slot 10 is the rank name) in 32 slots of 17
halfwords, 16 characters and a NUL, so a longer rank name was cut off ("Sun-bright
Princ"). Each slot is now 32 halfwords, 31 characters and a NUL. The table is allocated,
initialised, written and read in four places and all of them use the slot size, so they
change together. The slot count stays 32.

| va | old | new |
|---|---|---|
| 0x100AA0 | alloc size 2+32*0x22 (`0x442`) | 2+32*0x40 (`0x802`) |
| 0x101900 | constructor stride `ip*17` | `ip*32` (`lsl r2, ip, #5`) |
| 0x10190C | constructor cap `mov r4, #16` | `mov r4, #0x1f` (cosmetic) |
| 0x27F5B4 | setter stride `r1*17` | `r1*32` (`lsl r1, r1, #5`) |
| 0x27F5C4 | setter cap `mov r3, #0x11` | `mov r3, #0x20` |
| 0x3BBED0 | getter stride `r1*17` | `r1*32` (`lsl r1, r1, #5`) |

The player card has its own buffer, widened in fix-up 3; this one is the rank-up
notice's. The SD update's `code.ips` carries the same six words, which is why that
download now changes the game's code too.

Archive 3 with a 12-byte zero binary path opens RomFS level 3 raw, the same way
libctru's romfsInit does. 0x4BD10 is where `tables.bin` sits in level 3 of the
rebuilt RomFS; the build script computes it and checks the bytes. Call targets were
confirmed by their IPC headers: 0x2B99C4 sends 0x08030204 (OpenFileDirectly),
0x2E63A4 sends 0x080200C2 (Read), 0x2E64A8 sends 0x08040000 (GetSize).

## The HOME Menu banner and name

The HOME Menu banner is `banner.bnr` in the ExeFS: a CBMD holding one LZ11-compressed
CGFX model and the banner sound. The model's logo is its own 512x128 RGBA4 texture,
and it's the title screen's logo (`Layout/Title_upper.arc`, `timg/title.bclim`,
336x128 RGBA4) placed 88 texels from the left. `tools/home_banner.py` copies RC1's
English `title.bclim` into that texture texel for texel, recompresses the model and
keeps the sound byte-identical, 0x20-aligned. Nothing is resampled because both
textures are RGBA4. The new banner is 125,816 bytes against the retail 125,976, so
it fits the ExeFS as it was.

`icon.icn` (SMDH) gets "Dragon Quest Heroes: Rocket Slime 3" as the short title,
"Dragon Quest Heroes: Rocket Slime 3" / "Pirate & Platywag" as the long title and
"SQUARE ENIX" as publisher, in all 12 language slots. The icon picture and every
other field are unchanged.

Neither file is stored in this repo: both are made at build time from the player's
retail ExeFS and the overlay, and `build_rom.py` checks the inputs are retail and the
outputs match the approved md5s (banner a07c524d..., icon 49bb0286...).

## Building it

The build scripts are `tools/build_rom.py` (with `tools/home_banner.py`) and `tools/make_rom_xdelta.py` (they
need 3dstool, ctrtool, xdelta3 and RC1's `code.ips`, which is inside
`RS3DS-v1.0RC1.zip` on
[Team Rocket Slime's releases page](https://github.com/teamrocketslime/RS3DS-Releases/releases)).
The build uses 3dstool with `--not-encrypt` and `--not-pad`, recompresses the code
with `-z`, zeroes the card
seed at 0x1010, and re-extracts every part to compare it with what went in. The patch is encoded against a copy of the retail
file with its 0x4000 header scrambled (the decryptor writes a random card seed at
0x1010..0x103B, so no two dumps match there), with `-a` and `-A`.

## Verified for fix-up 12

- three things changed: the script (`tables.bin`), two layout files (`Layout/Shop_lower.arc`
  and `Layout/Customize/Ship_lower.arc`) and six words of code. Compared with fix-up 11's
  .cci, the RomFS file list is identical (3,820 files) and the differing RomFS files are
  those three, each equal to its source file; the two layout files are the same size and
  differ only in six edited letter-spacing floats (five in the shop, one in the customise
  list's parts-name pane)
- the decompressed code differs from fix-up 11's in the six words above and nothing else;
  read back from the built .cci, 0x100AA0 is 0x802, 0x101900 is `lsl r2, ip, #5`,
  0x10190C is `mov r4, #0x1f`, 0x27F5B4 and 0x3BBED0 are `lsl r1, r1, #5` and 0x27F5C4 is
  `mov r3, #0x20`; the recompressed `.code` went from 2,090,524 to 2,090,528 bytes
- the ExeFS banner, icon and logo, the exheader and the plain region are identical to
  fix-up 11's, so the HOME Menu banner and name are unchanged
- the .cci is 395,370,496 bytes
- patch 5,407,997 B, no local paths inside and no application header; decodes to the
  same .cci (sha256 189afd6e502c501f194a5dbdd7ef4856e220088ae9ffbd508184c44971b5f8b9)
  from the real dump, from two dumps with a different random seed and from two
  card-like dumps with the header, ExeFS header and icon bytes also randomised; a copy
  with one real game byte changed in the RomFS is refused
- the SD update's `code.ips` (RC1's code plus the keyboard word and these six) applied to
  the clean code gives the same code as the ROM's, except for the loader words that only
  the ROM build changes (the own-RomFS `tables.bin` loader above)
- [[TESTING]]

## Verified for fix-up 11

- only the script (`tables.bin`) changed: compared with fix-up 10's .cci, the differing
  bytes are `tables.bin`'s data, the RomFS hash tree (levels 1 and 2 and the master
  hash) and the NCCH header with its card-info copy, and nothing else; the RomFS file
  layout is identical, `tables.bin` is the same size and in the same place (0x4BD10)
- the ExeFS is identical to fix-up 10's (same sha256; `code.bin`, banner, icon and
  exheader compare equal), so the loader edits above and the keyboard word are unchanged
- the patched .cci boots in Azahar
- patch 4,561,373 B, no local paths inside and no application header; decodes to the
  same .cci (sha256 1df12ba91fdebc5ebd7b8fb81e6ebbbb6bc702a28902bb874504796fd9e947f2)
  from the real dump, from two dumps with a different random seed and from two
  card-like dumps with the header, ExeFS header and icon bytes also randomised; a copy
  with one real game byte changed is refused

## Verified for fix-up 10 (2026-09-16, patch re-encoded 2026-09-26)

- built from the same overlay as fix-up 9; compared sector by sector with fix-up 9's
  .cci, only the NCCH and ExeFS headers, the card-info copy of the NCCH header and the
  banner and icon bytes differ (code and RomFS identical)
- banner and icon re-extracted from the built .cci match the approved md5s
- installed in Azahar from a CIA of this .cci: the HOME Menu shows the English banner
  and name, and the game starts from the HOME Menu to the English title screen
- the released patch also scrubs the card-info header at 0x4000..0x4A00, the ExeFS
  header and the ExeFS icon before encoding, on top of the 0x4000 header scramble
  above, so it decodes a cartridge dump whose block-0 bytes differ from a console
  install's; the first upload, encoded against the 0x4000 header alone, refused those
  dumps
- patch 4,561,520 B, no local paths inside; decodes to the same .cci
  (sha256 2e39f00d8bc13a098de173f4da553bce8d52ec1d1b34d365fff9f4c4e4be0db4) from the
  real dump, from dumps with a different random seed, and from a card-like dump with
  the header, ExeFS header and icon bytes also randomised

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
