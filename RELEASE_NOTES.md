# Release notes

This is an unofficial fix-up on top of Team Rocket Slime's English RC1 translation
of Slime MoriMori Dragon Quest 3 on 3DS. The translation, the RC1 patch and the
choices in it are Team Rocket Slime's own work. This project only fixes things that
were broken in that release, as a single xdelta patch you apply to your own decrypted
Japanese game file.

## Fix-up 10

The HOME Menu now shows the game in English. Before this release, the banner above
the game's icon on the 3DS home screen still carried the Japanese logo on the pirate
ship, even after you patched and played the English game. This release swaps that
logo for RC1's own English title screen logo, placed at the same size and in the same
spot, so nothing about the banner artwork is stretched, redrawn or otherwise touched.
The ship, its animation and its jingle are all exactly as they were. The software's
name on the HOME Menu also now reads in English instead of Japanese. None of the game
itself changed here, every file is byte for byte the same as fix-up 9, so if you are
running from an installed CIA, this release only changes what you see before you
launch the game. If you play from a cartridge with the SD update method, your HOME
Menu banner cannot be changed that way and stays Japanese, but the game you actually
play is unaffected either way.

## Fix-up 9

This release closes a gap the earlier text width fixes had missed. Many lines fill in
an item or monster name while the game is running, things like a request to collect a
certain number of monsters, or a reward you are given. The earlier translation laid
those lines out assuming a short name would go there, so a long name could run past
the edge of the box and get split apart mid-word. This release checked every such line
against the game's own list of names and fixed all of them that could break, either by
moving the line break so the name always has room, or with a small rewording where
that was not enough. The same pass also checked every item, place and character name
against the game's name list and fixed a number of mismatched capitalisations. Nothing
here changes what any line says, only how it is laid out. If you are running fix-up 8
or earlier, you should update; nothing from before needs to be redone by hand.

## Fix-up 8

This release gives twelve of the recruitable monsters their own voice in ordinary
dialogue. The translation already gave each of these monsters a signature verbal tic
in the naval battle shouts, little sound-alike puns worked into their battle cries,
but in regular conversation the same monsters spoke in plain, voiceless English. This
release carries each monster's own speech quirk into its normal dialogue lines,
worked in roughly once a page so it does not get tiring, without changing what any
line actually says. A handful of recruit request lines were also shortened slightly so
a filled in item count and monster name cannot push the line past the edge of its box.
This is the last item from an older outside review of the translation: text that ran
past the box was fixed in earlier releases, the main cast's voices were fixed last
release, and this one finishes the monster crew's voices. If you have an earlier
fix-up, patch again with this one; nothing needs to be redone.

## Fix-up 7

This release is about keeping each character's voice consistent. The translation gave
its main cast distinct personalities and speech patterns, and none of those choices
were changed here. Instead, every main character's lines were checked line by line
against the Japanese to find places where the English voice had slipped, sounding
polite where the character should be rude, tired where they should be eager, or
threatening where the original is a lighthearted challenge from a kid. A number of
lines are changed as a result, always adjusted to match the voice the translation had
already established for that character elsewhere, not a new one. On purpose, this
release leaves alone a separate group of monsters whose lines end in a signature sound
in Japanese; giving those monsters an equivalent voice in English dialogue would be
new writing rather than a fix, so it waits for a later release. If you have an earlier
fix-up, patch again with this one; nothing needs to be redone.

## Fix-up 6

This release follows up on an audit done after fix-up 5. The naval battle shouts were
checked line by line against the Japanese the same way the main script had been, and
several lines were found saying something different from, or the opposite of, the
original: a couple had their meaning reversed outright, some warnings about the ship
overdoing something had turned into plain damage descriptions, and a few instructions
about reviving at a church had lost the instruction itself. Two lines an earlier
release had accidentally cut short mid-word are whole again. Speaker names were also
made consistent, since several characters had more than one spelling of their name
across different lines, and each now has one only. Lines that fill in a reward or item
name at runtime were adjusted so a long name always starts its own line, and a few
smaller mismatches, including the customise screen's slot labels and one area name,
were corrected too. If you have an earlier fix-up, patch again with this one; nothing
needs to be redone.

## Fix-up 5

This release found and used something not available before: the original Japanese
script sitting inside the game itself, lined up entry for entry with the English
translation. That made two new checks possible. The first compared every line's
internal formatting, things like where a message ends or a page waits for a button
press, against the Japanese, and restored several places where that had gone missing,
including a couple of tutorial pages that had lost content entirely. The second read
all of the game's dialogue against the Japanese for plain factual accuracy, and a
substantial number of lines were corrected as a result: wrong instructions, lines
pointing you to the wrong place, item descriptions that had never actually been
translated and were still a copy of an unrelated block of text, and several stat
descriptions that had been read backwards. A recurring place name is now spelled
consistently, and a few menu and interface labels were corrected to match. If you have
an earlier fix-up, patch again with this one; nothing needs to be redone.

## Fix-up 4

This release fixes a mistake introduced by an earlier fix-up rather than by Team
Rocket Slime: one naval battle warning line about the ship being in danger had been
accidentally cut down to just its last few letters, because the original file stored
it sharing space with the line before it, and an earlier rewrite of that first line
ran over it. The line is restored, and the build process now checks for that kind of
overlap so it cannot happen again unnoticed. Separately, eighteen misspelled words are
corrected across the dialogue, menus and naval battle shouts, while leaving alone the
many deliberate misspellings, accents, dropped letters and monster wordplay that are
part of the translation's own style. If you have an earlier fix-up, patch again with
this one; nothing needs to be redone.

## Fix-up 3

This release centres area names within their plate on the large map screens, which
had been left anchored to one side, something that Japanese names happened to fill but
some shorter English names did not. One area's English name is also shortened slightly
because the full name did not fit its plate on the map or at its harbour. Separately,
rank names shown on the player card were being cut off because the card only had room
for a limited number of characters; the card now holds more, and the small number of
rank names that were still too long have been shortened a little to fit. If you have
fix-up 1 or 2, patch the clean game again with this one; nothing needs to be redone.

## Fix-up 2

This release makes the name entry keyboard open on the English letter page instead of
the Japanese character page, a one line change that leaves every other keyboard tab
working as it did. It also fixes three lines from fix-up 1 where a text box had been
made to wait for a button press in the middle of a sentence rather than at its natural
end, splitting each of those into its own separate page. Finally, the two game over
hint messages are retranslated from the Japanese: one now correctly describes what a
particular ship upgrade does, and the other correctly describes what a certain hint is
pointing you toward, rather than what the earlier translation had said. If you have
fix-up 1, patch the clean game again with this one; nothing needs to be redone.

## Fix-up 1

This is the first release: Team Rocket Slime's English RC1 translation with a set of
fixes layered on top, packed into a single patch for the decrypted Japanese game file.
It fixes roughly one hundred and fifty dialogue lines that ran wider than their text
box, since the game splits overlong lines wherever they hit the edge of the box rather
than at a word boundary, which had left them broken apart mid-word. It also restores
about a dozen places where part of a line was cleared from the screen before you had
a chance to read it, adds the missing letter to the name entry keyboard along with
fixing some leftover Japanese punctuation on its symbol page, un-clips a speaker name
that had been cut off at the edge of its nameplate, and makes one character's name
consistent throughout. A handful of other small text issues, including stray
characters the game's font could not display, are also cleaned up.
