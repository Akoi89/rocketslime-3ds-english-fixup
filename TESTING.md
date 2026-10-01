# Testing

This is an account of what has and hasn't been checked for this fix-up. The
translation is Team Rocket Slime's own work; this project only patches things that
were broken in it, and testing has been limited.

## What has been played

Only the opening of the game has actually been played through in detail, and that
was done in the Azahar emulator, with no SD files present. That covers the title screen, entering a name,
the prologue and the first tutorial. Dialogue lines changed by the fix-up were checked
on screen during that stretch by swapping them into those early scenes.

Fix-up 11 was booted in Azahar, and its changed lines were looked at there with the
widest possible name.

Fix-up 12 changes the script, two layout files and a few words of the game's code.

Fix-up 12 was booted in Azahar (title, name entry, the opening narration and the first
Hooly pages). A scratch build with two extra test words that fill every name slot at
boot showed two slots side by side holding a 30-letter test string each, intact; the
same test on fix-up 11's code cut both to 15 (that test loop copies one letter less
than the cap, so the real limits are 16 before and 31 now). The two re-broken naval
tutorial lines were shown the same way in an ordinary dialogue box, clean.

The shop and customise lists, the rank-up message and the naval battle tutorial are
places I couldn't reach on the emulator, so what fix-up 12 changed there was checked by
measuring each line and name against its box, not by watching it appear.

Fix-up 13 changes only the script; the game's code is the same as fix-up 12's. For it I
measured every line in the script again, against the box it really appears in, with the
widest player name and the widest item, crew member or place name the game can put in
it. Two things made that possible. The notice and narration boxes split words the same
way dialogue does, so those lines needed the same check. And I tested on the emulator
exactly how wide a line can be before the game wraps it: three test lines of exactly
340 px in the normal dialogue box (font size 17) did not wrap, and a fourth at 345 px
did, its last character dropping to the next row. About 120 lines failed that rule, and
most of them were already like that in the 2019 RC1 script. Each now breaks between
words. The reward messages ("<name> got" and then "1 Broadsword!") go on two lines so
a long reward name, some of which are crew members, still fits. A second sweep of the
built script leaves 4 lines over: a naval tutorial line a few pixels past the width I
used, a line whose box I couldn't identify, a line of the Japanese trial demo that can't
be reached in the game, and RC1's own test string "Did you eat your frosted flakes
today?". A further 26 system, StreetPass and internet notices that run to three rows or
more are left as they were, because the Japanese pages are that long too. All of this
is measurement; none of the changed lines has been seen running except the test lines
above.

[[TESTING]]

## What has only been checked in the files, not on screen

The customise screen, naval battles, the map screens and the player card have all been
checked by reading the game's files directly, not by playing that far and watching
them appear on screen. That includes things like the area names centred on the map
plates, the rank names on the player card, the naval battle shout corrections, and the
customise screen's slot labels. Nobody has confirmed by eye that any of these actually
look right once the game renders them, on an emulator or on hardware.

## What has been checked on real hardware

Fix-up 10 was booted and played on the maintainer's own 3DS. It started up and played,
including seeing the new HOME Menu banner and name, though the maintainer did not get
far into the game before stopping.

Separately, a user named oho installed the fix-up 10 patched `.cci` straight from
GodMode9 on a 3DS running Fedora on the PC side, without converting it to a CIA first,
and reported that the first few areas of the game looked fine on hardware.

A user named rjl77 dumped a Japanese retail cartridge, patched that dump with the
fix-up 10 xdelta, converted the result to a CIA and got it running on a New 3DS XL,
seeing the game start at the intro. rjl77 later played through the whole first island
and into the second, and part of a naval battle, and reported nothing off in the text,
menus or maps (issue #1, 29 September 2026). That is the furthest anyone has reported
so far. In the same report the game froze once when they pressed HOME from the pause
menu. It has not been reproduced on hardware and has not been tied to the patch; on
the emulator the HOME button misbehaves the same way on the unpatched game, so the
emulator cannot settle it.

Fix-up 11 has not been run on a 3DS yet. The hardware runs above were all fix-up 10,
and fix-up 11 changes only the script.

Fix-up 12 has not been run on a 3DS yet either, and neither has fix-up 13, which
changes only the script.

On 30 September 2026 rjl77 reported five text problems found on the console with fix-up
10 (issue #1). Each one was measured, and all five are fixed in fix-up 12:

- A naval battle tutorial line broke after the "a" of "and", leaving "a" and "nd" on
  separate lines. Two lines in that tutorial were too wide for its smaller text box.
- "Got the Platyside / plans!" put the item name on its own line. The fix-up had added
  that break; RC1 had the line whole.
- In the shop, "Ducktor Cid Body" pushed its last letter onto a second line. That was
  the only name reported; measuring the lists found "Ducktor Cid Head" and "Mast",
  "Edged Boomerang", "Metal King Sword" and "Megaton Hammer" close to the same edge, in
  the shop or the ship customise list. The letters in those two lists are set slightly
  closer together now, and no names changed.
- "<name> got 1 / Broadsword!" put the item on its own line, in the reward messages for
  the quests. The fix-up had added that break too.
- The rank-up message cut a rank name off as "Sun-bright Princ". The game held rank
  names in a 16-letter slot there; that slot now holds 31, which is a change to the
  game's code. The player card already showed full rank names.

Fix-up 13 later changed how the reward messages break: "got" and the reward now sit on
two lines instead of one, because a long reward name didn't fit on one.

## What is unknown

Most of the game has never been seen running by anyone, on an emulator or on
hardware. No fluent Japanese reader has gone back over the fix-up's rewordings and
corrections line by line, so while every change was checked against the Japanese
script, none of it has had a second human pass. Whether the naval battles, the customise screen, the map
screens and the player card actually display correctly once played is genuinely
unknown rather than assumed to be fine. If you get further than the areas described
above, on an emulator or a real console, a report in the issues tab is the only way
this list gets shorter.
