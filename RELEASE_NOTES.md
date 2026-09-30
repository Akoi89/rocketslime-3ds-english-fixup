# Release notes

This is an unofficial fix-up on top of Team Rocket Slime's English RC1 translation of
Slime MoriMori Dragon Quest 3 on 3DS; the translation, the RC1 patch and the choices
in it are Team Rocket Slime's own work. This project only fixes things that were
broken in that release, applied as a single xdelta patch to your own decrypted
Japanese game file.

## What this build fixes

- **Dialogue that ran outside its text box.** Lines long enough that the game split
  them apart mid-word instead of at a natural break now have their line breaks placed
  so each line fits.
- **Lines cleared before you could read them.** Where part of a line was cleared
  from the screen before you had a chance to read it, the missing part is back.
- **The name entry keyboard and symbol page.** The keyboard now opens on the English
  letter page, its missing Z key is back, and leftover Japanese punctuation on the
  symbol page is gone.
- **Wrong or missing facts.** Every line was read against the Japanese script for
  facts: reversed instructions, wrong places, dropped facts, item descriptions that
  had never been translated, ship-part blurbs, and one name for the slime kingdom.
  Dr. Cid is Ducktor Cid everywhere, and a dropped tutorial page, Bo's missing first
  page and the item name in the shop prompt are back.
- **Naval-battle shouts and character voices.** The battle shout lines and the main
  cast's dialogue were checked line by line against the Japanese, restoring lines that
  had been softened, reversed, or made to sound like a different character, including
  one shout an earlier fix-up had cut short to just its last few letters.
- **Twelve recruitable monsters' own voice.** Each already had a signature verbal
  tic in its naval-battle shout; that same quirk now carries into its ordinary
  dialogue too.
- **Text that could run past the box when a name filled in.** Lines that insert an
  item or monster name while the game is running were checked against the game's full
  name list and re-broken or reworded so a long name always has room, and item, place
  and character names are capitalised to match the game's own spelling.
- **The HOME Menu.** The banner above the game's icon and the software's name on the
  HOME Menu now show in English instead of Japanese.
- **Lines with your name in them, typos and tone.** With a wide name, some dialogue ran
  past the box and was chopped partway through a word; those lines now break right
  after the name. Typos and grammar slips are fixed, crude wording in the 2019 script is
  toned down for an all-ages game, one speaker plate is corrected ("Wait up, Heady!!" is
  Taily calling after him), and one request line that had been translated as a question
  about the past reads as the request it is.

## Version history

- **Fix-up 11:** lines with your name in them break right after the name instead of
  running past the box, typos and grammar slips are fixed, crude wording is toned down,
  one speaker plate is corrected and one request line reads as a request. Only the script
  changed; the game's code is the same as fix-up 10. To use it, patch a clean copy of the
  game again.
- **Fix-up 10** (2026-09-16, patch re-uploaded 2026-09-26): HOME Menu banner and
  software name now read in English; the game itself is unchanged from fix-up 9. The
  re-uploaded patch also accepts cartridge dumps; to patch a cartridge dump with a copy
  downloaded before 27 September 2026, download it again.
- **Fix-up 9:** long item and monster names no longer run past their text box, and
  item, place and character names are capitalised to match the game's own spelling.
- **Fix-up 8:** twelve of the recruitable monsters gained their own speech quirk in
  ordinary dialogue, matching the one they already had in naval-battle shouts.
- **Fix-up 7:** the main cast's lines were checked against the Japanese to restore
  their established voice where it had slipped.
- **Fix-up 6:** naval-battle shouts checked against the Japanese, speaker names made
  consistent, and lines that fill in a reward or item name adjusted so a long name
  always starts its own line.
- **Fix-up 5:** every line read against the Japanese script found inside the game,
  for facts and for message formatting and page breaks.
- **Fix-up 4:** restored a naval warning line that an earlier fix-up had accidentally
  cut short, and corrected misspelled words across the dialogue, menus and shouts.
- **Fix-up 3:** centred area names in their plate on the map screen, and fixed rank
  names on the player card that were being cut off.
- **Fix-up 2:** the name keyboard opens on the English letter page, three lines that
  paused mid-sentence now pause at the end of a sentence instead, and the two
  game-over hints were retranslated from the Japanese.
- **Fix-up 1:** the first release, Team Rocket Slime's English RC1 translation with a
  set of fixes layered on top: dialogue that ran wider than its text box, lines
  cleared from the screen before they could be read, the missing keyboard letter and
  leftover Japanese punctuation, a clipped speaker name, and a few other small text
  issues.

## Known problems

- The title screen still says v1.0 RC1. This is a fix-up layered on Team Rocket
  Slime's release, not a new version of it, so their version number stays.
- No fluent Japanese reader has gone back over the fix-up's rewordings and
  corrections line by line; every change was checked against the Japanese script, but
  none of it has had a second human pass.
- Most of the game has never been seen running. The furthest anyone has reported is the
  end of the first island, which rjl77 played through on a console from a cartridge dump
  without seeing anything off. The customise screen, naval battles, the map and the
  player card were checked in the files and haven't been confirmed on screen.
  [TESTING.md](TESTING.md) is the full account of what has and hasn't been checked.
- If you play from a cartridge using the SD update method instead of patching a
  `.cci`, the HOME Menu banner stays Japanese, since the banner lives in a part of the
  game the SD card can't change. The game itself is unaffected either way.

## Files

- `Rocket-Slime-3DS-EN-RC1-fixup11.xdelta`: the patch on its own.
- `Rocket-Slime-3DS-EN-RC1-fixup11-RHDN.zip`: the same patch plus xdelta3.exe, a
  drag-and-drop `apply_patch.bat` and a plain-text readme.
- `Rocket-Slime-3DS-EN-RC1-fixup11-SD-Update.zip`: for playing from a cartridge, or an
  existing RC1 install, without dumping and patching a `.cci`; needs RC1's own patcher
  run first.
- The patch is built against a decrypted Japanese `.cci` (CTR-P-AMRJ), 393,957,376
  bytes.
- The patched result should have SHA-256 hash
  `1df12ba91fdebc5ebd7b8fb81e6ebbbb6bc702a28902bb874504796fd9e947f2`.

## Credits

Translation and the RC1 patch: Team Rocket Slime. Fix-up: Akoi89. Thanks to oho for
the first report from real hardware, and for confirming the patch builds cleanly on
Fedora. Thanks to rjl77 for sticking with the cartridge route through four rounds of
checks until it worked, and for the first cartridge dump played on a console.
