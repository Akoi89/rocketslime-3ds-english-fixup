# Rocket Slime 3DS: English RC1 with the unofficial fix-up

This is [Team Rocket Slime's English translation](https://github.com/teamrocketslime/RS3DS-Releases)
of Slime MoriMori Dragon Quest 3 (version 1.0 RC1) with an unofficial set of fixes
on top, as a single xdelta patch for the Japanese game file. It isn't from Team
Rocket Slime, and the translation is theirs. The title screen still says v1.0 RC1,
that's expected.

Everything is inside the patched game file. You don't need RC1's patcher, files on
the SD card, or Luma game patching.

Download the patch from the [Releases](../../releases) page. Each release has the
bare `.xdelta` and a `-RHDN.zip` with the same patch, xdelta3.exe, a drag-and-drop
`apply_patch.bat` and a plain-text readme.

## What the fix-up changes

- About 150 dialogue lines that were too wide for the text box, which the game
  splits mid-word
- 12 places where the first half of a line was wiped before you could read it
- the missing Z on the name keyboard, and the Japanese punctuation on the symbol page
- the one speaker name that was clipped at the edge of the nameplate
- the name keyboard opens on the ABC page
- the two game-over hints, retranslated from the Japanese
- area names centred in their plate on the map screen
- rank names on the player card no longer cut off
- Dr. Cid is Ducktor Cid everywhere now, 18 misspelled words put right, and a few
  other text fixes
- one naval-battle line that fix-ups 1 to 3 had cut to "nger!" (my mistake, not
  Team Rocket Slime's) reads "Huh? Ship's in danger!" again
- control codes and page breaks checked line by line against the Japanese script:
  six lost codes restored, four pages no longer open with a blank line, a dropped
  tutorial page and Bo's missing first page are back, the shop prompt names the item
- every line read against the Japanese for facts: 273 lines corrected (reversed
  instructions, wrong places, dropped facts, item descriptions that had never been
  translated, ship-part blurbs, one name for the slime kingdom)
- the naval-battle shouts read against the Japanese too: 39 corrected, two that RC1 had
  cut mid-word made whole
- one English name per speaker (34 speakers had two or more), and reward names given
  their own line so the widest can't run off the box
- the customise screen's slot labels re-lettered HULL, BOW, MAST, DECOR (one was
  misspelled and two no longer matched the menu text)
- 59 lines where a character dropped their own voice or contradicted the Japanese
  (a threat where the Japanese is a challenge, weary where it's eager, an invented
  outburst from the politest character), put back in the voice RC1 gave them
- 45 dialogue lines for twelve recruitable monsters whose Japanese sentences end in
  a signature tic; the naval shouts already punned it, their dialogue now does too
- 227 lines that could run past the box once the game filled in a long item or monster
  name (199 re-broken, 28 reworded), and item, place and character names capitalised
  the way the game's own name table spells them

## What you need

A decrypted `.cci` of the Japanese game (CTR-P-AMRJ), the kind Batch CIA 3DS
Decryptor makes. It should be 393,957,376 bytes. The patch doesn't contain the game.

## How to apply

Use any xdelta patcher (xdelta UI, Delta Patcher, or xdelta3 itself) with your
decrypted `.cci` as the source and `Rocket-Slime-3DS-EN-RC1-fixup9.xdelta` as the
patch. With xdelta3 from a command line:

    xdelta3 -d -B 1073741824 -s "your-decrypted.cci" Rocket-Slime-3DS-EN-RC1-fixup9.xdelta Rocket-Slime-3DS-EN.cci

If the patcher says the source doesn't match, your file isn't the decrypted
Japanese game, or it was made a different way.

The patched file should have this SHA-256:

    57dc9c5ba7b6f35ad86b11775259273fcaa3e58cec21c81a9010f4ef7d5a3958

In Windows PowerShell: `Get-FileHash Rocket-Slime-3DS-EN.cci`

## Playing from a cartridge: Cartridge / SD Update (Requires RC1)

If you own the cartridge and don't want to dump it, there's a second download:
`Rocket-Slime-3DS-EN-RC1-fixup9-SD-Update.zip`. It's a GodMode9 script that updates
Team Rocket Slime's RC1 install on your SD card to this fix-up, the same files RC1
uses, so the game keeps running straight from the cartridge (or an installed copy).

You need Luma3DS and GodMode9, and RC1's own patcher has to have been run first
(`RS3DS-v1.0RC1.zip` from [their releases](https://github.com/teamrocketslime/RS3DS-Releases/releases)).
Then copy the zip's `gm9` folder to your SD card and run the script from GodMode9's
HOME menu under Scripts. It checks every file before it touches the game's folder,
keeps RC1's files as a backup (about 100 MB), and running it again is harmless. Keep Luma's game patching turned on. Full steps are in the zip's
README.txt.

This one needs the SD files, so skip the "If you had RC1 installed before" section
below: that's only for the patched `.cci`.

It's been checked two ways here, not on a console: the files it produces were booted
in Azahar with the untouched Japanese game, and the script was run in a simulation of
GodMode9. If you try it on a real 3DS, please tell me how it went in the
[issues](../../issues) tab.

## If you had RC1 installed before

RC1 puts files on the SD card, and they get in the way of this version. Delete or
rename these before playing:

- `sd:/fti/rocket_slime_3ds/` (the game uses these instead of the ones in the patched file)
- `sd:/luma/titles/000400000005C300/code.ips` (Luma would patch the game a second
  time and it would go back to looking for the SD files)

On an emulator, the same goes for its virtual SD card and any mod folder for this
title.

## Tested on

The Azahar emulator, booted with no SD files at all. Only the start of the game has
been played that way: title, name entry, the prologue and the first tutorial. Changed
dialogue was checked on screen by swapping lines into those early scenes, but the
customise screen, naval battles, the map and the player card have only been checked
in the files, not seen running. It hasn't been tried on a real 3DS yet. On a
console you'd need to convert the patched `.cci` to a CIA (GodMode9
can do that) and install it. I've built a CIA from it here and checked it reads
back byte for byte, but I've never installed one or run this on hardware. If you
do, I'd like to hear how it went: the [issues](../../issues) tab is the place.

## How it works

RC1 loads its script from the SD card at boot. This patch builds the script and
RC1's files into the game itself and changes where RC1's loader reads from. The
details are in [docs/ROM_PATCH.md](docs/ROM_PATCH.md).

The tools were written with LLM assistance (Claude, through Claude Code). The
translation itself is Team Rocket Slime's. Most of the width fixes are line breaks
placed by a script that measures each line against the game's own font.

Compared with RC1, 470 script strings and 42 naval-battle shouts are now worded
differently. Fix-up 1's rewordings, about 60, came from Gemini's suggestions. The
later ones (the game-over hints, the misspellings, the full read against the Japanese
script, the character voice lines, the long-name rewordings) were drafted by Claude
and reviewed by Gemini before they went in. Each line was measured against its box.
Nobody fluent in Japanese has checked them by hand, so if something reads wrong to
you, please open an [issue](../../issues).

## Credits

Translation and the RC1 patch:
[Team Rocket Slime](https://github.com/teamrocketslime/RS3DS-Releases).
Fix-up: Akoi89. The patch is provided as is.

The build scripts in `tools/` and the docs are under the MIT license
([LICENSE](LICENSE)). That covers my own work only. Team Rocket Slime's translation
and the game's content aren't mine to license, and the license doesn't cover them.
