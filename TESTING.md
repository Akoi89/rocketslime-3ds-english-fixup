# Testing

This is an honest account of what has and has not been checked for this fix-up. The
translation is Team Rocket Slime's own work; this project only patches things that
were broken in it, and testing has been limited.

## What has been played

Only the opening of the game has actually been played, and only in the Azahar
emulator, with no SD files present. That covers the title screen, entering a name,
the prologue and the first tutorial. Dialogue lines changed by the fix-up were checked
on screen during that stretch by swapping them into those early scenes.

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
and reported that the first few areas of the game looked fine on hardware. That is the
only outside report received so far.

## What is unknown

Most of the game has never been seen running by anyone, on an emulator or on
hardware. No fluent Japanese reader has gone back over the fix-up's rewordings and
corrections line by line, so while every change was checked against the Japanese
script, none of it has had a second human pass. Whether the naval battles, the customise screen, the map
screens and the player card actually display correctly once played is genuinely
unknown rather than assumed to be fine. If you get further than the areas described
above, on an emulator or a real console, a report in the issues tab is the only way
this list gets shorter.
