# Rocket Slime 3DS: English RC1 with the unofficial fix-up

This is [Team Rocket Slime's English translation](https://github.com/teamrocketslime/RS3DS-Releases)
of Slime MoriMori Dragon Quest 3 (version 1.0 RC1) with an unofficial set of fixes
on top, as a single xdelta patch for the Japanese game file. It isn't from Team
Rocket Slime, and the translation is theirs. The title screen still says v1.0 RC1,
that's expected.

Everything is inside the patched game file. You don't need RC1's patcher, files on
the SD card, or Luma game patching.

Download the patch from the [Releases](../../releases) page. The latest release has
the bare `.xdelta` and a `-RHDN.zip` with the same patch, xdelta3.exe, a drag-and-drop
`apply_patch.bat` and a plain-text readme.

## What the fix-up changes

- Dialogue and menus corrected against the Japanese script, including
  mistranslations, dropped facts, missing control codes and page breaks,
  clipped or inconsistent character names, and lines that ran wider than
  their text box and got split mid-word.
- Character voices and the naval-battle shouts checked line by line against
  the Japanese, including one shout an earlier fix-up had accidentally cut
  short, and twelve of the recruitable monsters given their own speech quirk in
  ordinary dialogue to match the one they already had in battle.
- Smaller fixes throughout: the name keyboard, the two game-over hints, area
  names on the map, rank names on the player card, the customise screen's
  slot labels, and a number of misspellings.
- The HOME Menu banner and the software's name now show in English instead
  of Japanese.

## If something looks wrong

Tell me. [The playtesting thread](../../issues/1) is the place, and the screen it happened on
is enough to go on. Don't check first to see whether I already know about it. A
duplicate costs me nothing, and something you talked yourself out of reporting costs
me a bug.

Two things are already known, so they're not a surprise:

- **The title screen still says v1.0 RC1.** This is a fix-up layered on Team Rocket
  Slime's release, not a new version of it, so their version number stays.
- **Most of the game has never been seen running.** Only the opening has been played:
  the title, name entry, the prologue and the first tutorial. The customise screen,
  naval battles, the map and the player card were checked in the files and not on
  screen. Nobody has played far into it on a console. If you get further than that,
  I'd like to hear how it went either way. [TESTING.md](TESTING.md) is the full
  account of what has and hasn't been checked.

[RELEASE_NOTES.md](RELEASE_NOTES.md) has the full list of fixes and a short entry for every fix-up, newest first.

## What you need

A decrypted `.cci` of the Japanese game (CTR-P-AMRJ), the kind Batch CIA 3DS
Decryptor makes. It should be 393,957,376 bytes. The patch doesn't contain the game.

> **Dump the title as an encrypted CIA and decrypt it on the PC.** In GodMode9, dump
> the title to CIA with no decrypt and no trim option, copy that to your computer, and
> run Batch CIA 3DS Decryptor on it there. GodMode9's own decrypt hands you a file of
> the **right size** that isn't the same bytes, and the patch will refuse it. That has
> caught a few people on my other patches, so a size of 393,957,376 matching is not
> proof your file is the right one.

**Dumping from a cartridge?** There's no installed title to dump, so use GodMode9's
"Build CIA" on the cartridge, copy that CIA to your PC and run Batch CIA 3DS
Decryptor on it. The 393,957,376 byte `.cci` it gives you is the one to patch. Skip
the raw `.3ds` cartridge image: decrypted, it comes out bigger, because a cartridge
also carries a system update section, and the patch won't take it. The first upload
of the fix-up 10 patch refused cartridge dumps even when the game inside matched, so
if you downloaded it before 27 September 2026, download it again. A tester has since
patched a real cartridge dump with it and got the right file.

## How to apply

Use any xdelta patcher (xdelta UI, Delta Patcher, or xdelta3 itself) with your
decrypted `.cci` as the source and `Rocket-Slime-3DS-EN-RC1-fixup10.xdelta` as the
patch. With xdelta3 from a command line:

    xdelta3 -d -B 1073741824 -s "your-decrypted.cci" Rocket-Slime-3DS-EN-RC1-fixup10.xdelta Rocket-Slime-3DS-EN.cci

If the patcher says the source doesn't match, your file isn't the decrypted
Japanese game, or it was made a different way. The exact wording you'll see from
xdelta3 is `target window checksum mismatch`, and it almost always means the dump,
not the patch. Read the box above about GodMode9's own decrypt before anything else.

The patched file should have this SHA-256:

    2e39f00d8bc13a098de173f4da553bce8d52ec1d1b34d365fff9f4c4e4be0db4

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

The SD update's file name still says fixup9, and that's right: fix-up 10 only added the
HOME Menu banner and name, and those live in a part of the game an SD card can't change.
Everything the SD update does is the same as before, so the game itself matches fix-up 10.

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
in the files, not seen running.

It does run on a real 3DS. I launched fix-up 10 on mine and it booted and played,
though I didn't get far. oho built fix-up 10 on Fedora, installed the patched
`.cci` straight from GodMode9 without converting it to a CIA first, and said the
first few areas looked fine on hardware. rjl77 dumped a Japanese retail cartridge,
patched that dump, converted the result to a CIA and got it running on a New 3DS XL,
so the cartridge route works from start to finish too.

So you have a choice on a console: install the `.cci` directly with GodMode9, or
convert it to a CIA and install that. I've built a CIA here too, checked it reads
back byte for byte, and installed it in Azahar, where the HOME Menu shows the
English banner and name and the game starts from there.

## How it works

RC1 loads its script from the SD card at boot. This patch builds the script and
RC1's files into the game itself and changes where RC1's loader reads from. The
details are in [docs/ROM_PATCH.md](docs/ROM_PATCH.md). The English HOME Menu banner is
made the same way, from your own game file: the build takes the Japanese banner and puts
RC1's English title-screen logo into it.

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

Thanks to oho for the first report from real hardware, and for confirming the patch
builds cleanly on Fedora. Thanks to rjl77 for sticking with the cartridge route
through four rounds of checks until it worked, and for the first cartridge dump
played on a console.

The build scripts in `tools/` and the docs are under the MIT license
([LICENSE](LICENSE)). That covers my own work only. Team Rocket Slime's translation
and the game's content aren't mine to license, and the license doesn't cover them.
