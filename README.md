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
- Fix-up 11: lines with your name in them break right after the name, so a wide
  name no longer gets dialogue chopped partway through a word. Typos and grammar
  slips are fixed, a few crude words in the 2019 script are toned down for an
  all-ages game, one speaker plate is corrected, and one request line that had
  been translated as a question about the past reads as the request it is.
- Fix-up 12: five problems rjl77 found on a 3DS. Two naval battle tutorial lines
  split a word across two lines, reward messages put the item on a line of its
  own ("got 1" and then "Broadsword!"), a few long names in the shop and ship
  customise lists lost their last letter to a second line, and a rank name over 16
  letters was cut off in the rank-up message ("Sun-bright Princ"). That last one
  is a change to the game's code, so it's in both the patch and the SD update.
- Fix-up 13: every line checked again against the box it really appears in, and the
  notice and narration boxes turned out to split words the same way dialogue does.
  About 120 lines could split a word onto a new line, or push the last word out of
  the box, when your name or an inserted item, crew member or place name was long.
  They now break between words. Reward messages put "got" and the reward on two lines
  (the name and "got", then "1 Broadsword!") so a long reward name, and some rewards
  are crew members, can't push the line out of the box; fix-up 12's one-line version
  only fit short ones. One naval tutorial line is reworded to fit with any name, and
  a rank name that carried a stray line break no longer pushes the rank-up "!" onto a
  third row. Only the script changed; the game's code is the same as fix-up 12's.

## If something looks wrong

Tell me. [The playtesting thread](../../issues/1) is the place, and the screen it happened on
is enough to go on. Don't check first to see whether I already know about it. A
duplicate costs me nothing, and something you talked yourself out of reporting costs
me a bug.

Two things are already known, so they're not a surprise:

- **The title screen still says v1.0 RC1.** This is a fix-up layered on Team Rocket
  Slime's release, not a new version of it, so their version number stays.
- **Most of the game has never been seen running.** The furthest anyone has reported
  is partway through the second island, which rjl77 reached on a console from a
  cartridge dump without seeing anything off in the text, menus or maps, along with
  part of a naval battle. The customise screen and the player card were checked in
  the files and haven't been confirmed on screen. If you get further than that,
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
also carries a system update section, and the patch won't take it. A tester patched
a real cartridge dump this way with fix-up 10 and got the right file.

## How to apply

Use any xdelta patcher (xdelta UI, Delta Patcher, or xdelta3 itself) with your
decrypted `.cci` as the source and `Rocket-Slime-3DS-EN-RC1-fixup13.xdelta` as the
patch. With xdelta3 from a command line:

    xdelta3 -d -B 1073741824 -s "your-decrypted.cci" Rocket-Slime-3DS-EN-RC1-fixup13.xdelta Rocket-Slime-3DS-EN.cci

If the patcher says the source doesn't match, your file isn't the decrypted
Japanese game, or it was made a different way. The exact wording you'll see from
xdelta3 is `target window checksum mismatch`, and it almost always means the dump,
not the patch. Read the box above about GodMode9's own decrypt before anything else.

The patched file should have this SHA-256:

    b24856aedbd932b4967376048ccdc69991feacbec779b6249b2c93eb72766fbc

In Windows PowerShell: `Get-FileHash Rocket-Slime-3DS-EN.cci`

## Playing from a cartridge: Cartridge / SD Update (Requires RC1)

If you own the cartridge and don't want to dump it, there's a second download:
`Rocket-Slime-3DS-EN-RC1-fixup13-SD-Update.zip`. It's a GodMode9 script that updates
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

This update changes the game's code as well as the script now: its `code.ips` is
RC1's plus the keyboard word and a few more words that let a rank name be 31 letters
long instead of 16 in the rank-up message. That code change is the same one fix-up 12
made; fix-up 13 added no further code changes. Nothing else about how it's installed
is different.

It's been checked here, not on a console: the script was run in a simulation of
GodMode9, and the fix-up 9 version's files were booted in Azahar with the untouched
Japanese game. This version's files differ from those in the script text, two layout
files and that code change, so they haven't had that boot test. If you try it on a
real 3DS, please tell me how it went in the [issues](../../issues) tab.

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
so the cartridge route works from start to finish too. rjl77 has since played into
the second island and part of a naval battle that way and hasn't seen anything off in
the text. The game froze once for them when they pressed HOME from the pause menu. I
haven't been able to tie that to the patch, so if it happens to you, please tell me
which menu you were on.

Fix-up 11 has been booted on the Azahar emulator, and I looked at the changed lines
there with the widest possible name. It hasn't been run on a 3DS yet. The runs on
hardware above were fix-up 10, and fix-up 11 changes only the script. If you try it
on a console, I'd like to hear how it went.

Fix-up 12 changes the script, two layout files and a few words of the game's code.

It boots on the Azahar emulator. A test build there also showed the longer name slot
holding a long test string in full, where fix-up 11's code cut the same string short,
and the two re-broken tutorial lines displayed cleanly in an ordinary dialogue box.

The shop and customise lists, the rank-up message and the naval battle tutorial are
places I couldn't reach on the emulator, so those fixes were checked by measuring the
text against the boxes, not by watching them. Fix-up 12 hasn't been run on a 3DS yet.
If you try it on a console, I'd like to hear how it went, the rank-up message and the
shop lists especially.

Fix-up 13 changes only the script. I re-measured every line against the box it appears
in, and on the emulator I checked how wide a line can be before the game wraps it.

[[TESTING]]

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

Compared with RC1, 521 script strings and 42 naval-battle shouts are now worded
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
through four rounds of checks until it worked, for the first cartridge dump
played on a console, and for the five text problems on a 3DS that fix-up 12 fixes.

The build scripts in `tools/` and the docs are under the MIT license
([LICENSE](LICENSE)). That covers my own work only. Team Rocket Slime's translation
and the game's content aren't mine to license, and the license doesn't cover them.
