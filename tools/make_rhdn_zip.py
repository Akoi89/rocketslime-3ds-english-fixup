# -*- coding: utf-8 -*-
r"""Release zip for romhacking.net and anyone who wants everything in one download.

Every fix-up release ships this zip next to the bare .xdelta. It holds:
  Rocket-Slime-3DS-EN-RC1-fixup<N>.xdelta   the release patch, unchanged
  xdelta3.exe                               xdelta 3.2.0 (Apache License 2.0)
  apply_patch.bat                           drag the decrypted .cci onto it
  README.txt                                steps, sizes, the result hash, SD cleanup, credits

Checks before it reports OK: the zip is re-opened and extracted to a work folder,
the extracted apply_patch.bat is run against a copy of the retail .cci with a new
random card seed (the decryptor writes a different one into every dump), and the
result must hash to the target. README.txt and apply_patch.bat must be pure ASCII,
CRLF, with no dash characters and no drive-letter paths.

Usage: make_rhdn_zip.py <N> <patch.xdelta> <xdelta3.exe> <target sha256> <retail.cci> <out.zip> <work>
"""

import hashlib
import os
import re
import shutil
import subprocess
import sys
import zipfile

SRC_SIZE = 393957376
SEED_OFF, SEED_LEN = 0x1010, 0x2C
OUT_NAME = "Rocket-Slime-3DS-EN.cci"
LEAK_RE = re.compile(r"(?<![A-Za-z])[A-Za-z]:[\\/]")  # sd:/ is fine, a Windows drive letter is not

BAT = r"""@echo off
setlocal
rem Rocket Slime 3DS English RC1, unofficial fix-up {N}
rem Drag your decrypted Japanese .cci onto this file, or run:
rem   apply_patch.bat "<your decrypted .cci>"
set "HERE=%~dp0"
set "PATCH=%HERE%Rocket-Slime-3DS-EN-RC1-fixup{N}.xdelta"
set "OUT=%HERE%{OUT}"
if "%~1"=="" (
  echo Drag your decrypted Japanese .cci onto apply_patch.bat.
  pause
  exit /b 1
)
if not "%~z1"=="{SIZE}" (
  echo That file is %~z1 bytes. The decrypted Japanese .cci is {SIZE} bytes.
  echo See README.txt for how to make it with Batch CIA 3DS Decryptor.
  pause
  exit /b 1
)
echo Patching, this takes under a minute...
"%HERE%xdelta3.exe" -d -f -B 1073741824 -s "%~1" "%PATCH%" "%OUT%"
if errorlevel 1 (
  echo.
  echo xdelta3 reported an error. The source is probably not the decrypted Japanese game.
  pause
  exit /b 1
)
for /f "usebackq delims=" %%H in (`powershell -NoProfile -Command "(Get-FileHash -Algorithm SHA256 -LiteralPath $env:OUT).Hash.ToLower()"`) do set "GOT=%%H"
echo.
if /i "%GOT%"=="{SHA}" (
  echo Done, and the hash matches: {OUT}
) else (
  echo Patched, but the SHA-256 does not match README.txt. Do not use this file.
  echo Got:      %GOT%
  echo Expected: {SHA}
)
pause
exit /b 0
"""

README = """Rocket Slime 3DS: English RC1 with the unofficial fix-up {N}
=============================================================

This is Team Rocket Slime's English translation of Slime MoriMori Dragon Quest 3
(v1.0 RC1) with an unofficial set of fixes on top. It isn't from Team Rocket
Slime, and the translation is theirs:
https://github.com/teamrocketslime/RS3DS-Releases

Everything is inside the patched game file. You don't need RC1's patcher, files
on the SD card, or Luma game patching. The title screen still says v1.0 RC1,
that's expected.


What's in this zip
------------------

  Rocket-Slime-3DS-EN-RC1-fixup{N}.xdelta   the patch
  apply_patch.bat                         applies it for you (Windows)
  xdelta3.exe                             xdelta 3.2.0, Apache License 2.0
  README.txt                              this file


What you need
-------------

A decrypted .cci of the Japanese game (CTR-P-AMRJ, title 000400000005C300), the
kind Batch CIA 3DS Decryptor makes from your own dump. It must be {SIZE_C} bytes.
The patch doesn't contain the game.


How to apply
------------

Windows: drag your decrypted .cci onto apply_patch.bat. It writes
{OUT} next to the .bat and checks its hash.

Anything else, or by hand (xdelta3 3.1 or newer):

  xdelta3 -d -B 1073741824 -s "your-decrypted.cci" Rocket-Slime-3DS-EN-RC1-fixup{N}.xdelta {OUT}

Delta Patcher and xdelta UI work too. If the patcher says the source doesn't
match, your file isn't the decrypted Japanese game.

The patched file should have this SHA-256:

  {SHA}

Play the .cci in Azahar, or on a 3DS convert it to a CIA with GodMode9 and
install it. The CIA route hasn't been tested on a real console yet.


If you had RC1 installed before
-------------------------------

RC1 puts files on the SD card and they get in the way. Delete or rename these
before playing:

  sd:/fti/rocket_slime_3ds/
  sd:/luma/titles/000400000005C300/code.ips

On an emulator, the same goes for its virtual SD card and any mod folder for
this title.


Reports and details
-------------------

What the fix-up changes, how it's built, and the issue tracker:
https://github.com/Akoi89/rocketslime-3ds-english-fixup

Tested in the Azahar emulator only. If you try it on a 3DS, I'd like to hear
how it went.


Credits
-------

Translation and the RC1 patch: Team Rocket Slime.
Fix-up: Akoi89. Provided as is.
xdelta3: Joshua MacDonald, Apache License 2.0.
"""


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 24), b""):
            h.update(b)
    return h.hexdigest()


def crlf(s):
    return s.replace("\r\n", "\n").replace("\n", "\r\n").encode("ascii")


def text_ok(name, data):
    bad = []
    if any(b > 0x7E and b not in (0x0D, 0x0A) for b in data):
        bad.append("non-ASCII byte")
    if b"\n" in data.replace(b"\r\n", b""):
        bad.append("bare LF")
    if LEAK_RE.search(data.decode("ascii", "replace")):
        bad.append("drive-letter path")
    print("  %-16s %s" % (name, "clean" if not bad else "BAD: " + ", ".join(bad)))
    return not bad


def main():
    n, patch, xd, want, retail, out, work = sys.argv[1:8]
    patch, xd, retail, out, work = map(os.path.abspath, (patch, xd, retail, out, work))
    want = want.lower()
    os.makedirs(work, exist_ok=True)
    if os.path.getsize(retail) != SRC_SIZE:
        raise SystemExit("retail .cci is not %d bytes" % SRC_SIZE)

    fields = dict(N=n, SIZE=SRC_SIZE, SIZE_C="{:,}".format(SRC_SIZE), SHA=want, OUT=OUT_NAME)
    bat = crlf(BAT.format(**fields))
    readme = crlf(README.format(**fields))
    pname = "Rocket-Slime-3DS-EN-RC1-fixup%s.xdelta" % n
    if os.path.basename(patch) != pname:
        raise SystemExit("patch file should be named %s" % pname)

    ok = text_ok("apply_patch.bat", bat) & text_ok("README.txt", readme)

    if os.path.exists(out):
        os.remove(out)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for arc, src in ((pname, patch), ("xdelta3.exe", xd)):
            info = zipfile.ZipInfo(arc, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            with open(src, "rb") as f:
                z.writestr(info, f.read())
        for arc, data in (("apply_patch.bat", bat), ("README.txt", readme)):
            info = zipfile.ZipInfo(arc, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, data)
    print("zip: %s, %d B" % (out, os.path.getsize(out)))

    ext = os.path.join(work, "extracted")
    shutil.rmtree(ext, ignore_errors=True)
    with zipfile.ZipFile(out) as z:
        print("  members: %s" % ", ".join(z.namelist()))
        z.extractall(ext)
    ok &= sha(os.path.join(ext, pname)) == sha(patch)

    src = os.path.join(work, "seeded.cci")
    shutil.copyfile(retail, src)
    with open(src, "r+b") as f:
        f.seek(SEED_OFF)
        f.write(os.urandom(SEED_LEN))
    # run from the extracted folder, the source path keeps its spaces (as a user's would)
    r = subprocess.run('cmd /c call "%s" "%s"' % (os.path.join(ext, "apply_patch.bat"), src), cwd=ext,
                       stdin=subprocess.DEVNULL, capture_output=True, text=True)
    if r.stderr.strip():
        print("  bat stderr: %s" % r.stderr.strip())
    print("  bat output: %s" % " | ".join(l.strip() for l in r.stdout.splitlines() if l.strip() and "Press any" not in l))
    got = sha(os.path.join(ext, OUT_NAME))
    good = got == want and "hash matches" in r.stdout
    print("  bat on a new-seed dump: %s" % ("EXACT, bat reports match" if good else "WRONG " + got))
    ok &= good
    os.remove(src)
    shutil.rmtree(ext, ignore_errors=True)
    print("zip sha256: %s" % sha(out))
    print("RESULT: %s" % ("OK" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
