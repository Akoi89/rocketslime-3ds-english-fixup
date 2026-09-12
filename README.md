# Rocket Slime 3DS: English RC1 with the unofficial fix-up

This is Team Rocket Slime's English translation of Slime MoriMori Dragon Quest 3
(version 1.0 RC1) with an unofficial set of fixes on top, as a single xdelta patch
for the Japanese game file. It isn't from Team Rocket Slime, and the translation is
theirs. The title screen still says v1.0 RC1, that's expected.

Everything is inside the patched game file. You don't need RC1's patcher, files on
the SD card, or Luma game patching.

Download the patch from the [Releases](../../releases) page.

## What the fix-up changes

- About 150 dialogue lines that were too wide for the text box, which the game
  splits mid-word
- 12 places where the first half of a line was wiped before you could read it
- the missing Z on the name keyboard, and the Japanese punctuation on the symbol page
- the one speaker name that was clipped at the edge of the nameplate
- the name keyboard opens on the ABC page
- the two game-over hints, retranslated from the Japanese
- Dr. Cid is Ducktor Cid everywhere now, and a few other text fixes

## What you need

A decrypted `.cci` of the Japanese game (CTR-P-AMRJ), the kind Batch CIA 3DS
Decryptor makes. It should be 393,957,376 bytes. The patch doesn't contain the game.

## How to apply

Use any xdelta patcher (xdelta UI, Delta Patcher, or xdelta3 itself) with your
decrypted `.cci` as the source and `Rocket-Slime-3DS-EN-RC1-fixup2.xdelta` as the
patch. With xdelta3 from a command line:

    xdelta3 -d -B 1073741824 -s "your-decrypted.cci" Rocket-Slime-3DS-EN-RC1-fixup2.xdelta Rocket-Slime-3DS-EN.cci

If the patcher says the source doesn't match, your file isn't the decrypted
Japanese game, or it was made a different way.

The patched file should have this SHA-256:

    0350e18df957018848e121712936e126d073210973b37dd67f0d0043bee5043a

In Windows PowerShell: `Get-FileHash Rocket-Slime-3DS-EN.cci`

## If you had RC1 installed before

RC1 puts files on the SD card, and they get in the way of this version. Delete or
rename these before playing:

- `sd:/fti/rocket_slime_3ds/` (the game uses these instead of the ones in the patched file)
- `sd:/luma/titles/000400000005C300/code.ips` (Luma would patch the game a second
  time and it would go back to looking for the SD files)

On an emulator, the same goes for its virtual SD card and any mod folder for this
title.

## Tested on

The Azahar emulator, booted with no SD files at all. It hasn't been tried on a real
3DS yet. On a console you'd need to convert the patched `.cci` to a CIA (GodMode9
can do that) and install it; I haven't done that myself. If you run it on one, I'd
like to hear how it went.

## How it works

RC1 loads its script from the SD card at boot. This patch builds the script and
RC1's files into the game itself and changes where RC1's loader reads from. The
details are in [docs/ROM_PATCH.md](docs/ROM_PATCH.md).

The tools were written with LLM assistance (Claude, through Claude Code). The
translation itself is Team Rocket Slime's. Most of the fixes are line breaks placed by
a script that measures each line against the game's own font. About 60 lines
needed rewording or a hand-placed break to fit; those were done from another LLM's
suggestions (Gemini), and each one was measured before it went in.

## Credits

Translation and the RC1 patch: Team Rocket Slime. Fix-up: Akoi89. The patch is
provided as is; the build scripts in `tools/` are free to reuse.
