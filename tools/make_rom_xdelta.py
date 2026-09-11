# -*- coding: utf-8 -*-
r"""One xdelta: decrypted retail .cci -> self-contained patched .cci.

Method from TGAA's build_rhdn_patches.py:
  * the decryptor writes a random card seed at 0x1010..0x103B of every .cci, so
    no two dumps match there; the target has that block zeroed (build_rom.py)
  * encode against a copy whose whole 0x4000 header is random, so the patch never
    copies from the seed block or next to it
  * -a: xdelta 3.2.0 otherwise pins the patch to one exact source file (BLAKE3)
  * -A: no application header, so no local file paths inside the patch
Checks: decode against the real dump, and against two dumps with a different
random seed; all must equal the built .cci. No path text inside the patch.

Usage: make_rom_xdelta.py <xdelta3.exe> <retail.cci> <built.cci> <out.xdelta> <work>
"""

import hashlib
import os
import re
import shutil
import subprocess
import sys

SEED_OFF, SEED_LEN = 0x1010, 0x2C
LEAK_RE = re.compile(rb"[A-Za-z]:[\\/][^\x00-\x1f]{3,}")  # any drive-letter path


def run(*a):
    r = subprocess.run([str(x) for x in a], capture_output=True, text=True)
    if r.returncode:
        raise SystemExit("FAILED (%d): %s\n%s" % (r.returncode, " ".join(map(str, a)), r.stderr))


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 24), b""):
            h.update(b)
    return h.hexdigest()


def scrubbed(src, dst, off, n):
    shutil.copyfile(src, dst)
    with open(dst, "r+b") as f:
        f.seek(off)
        f.write(os.urandom(n))
    return dst


def main():
    xd, src, tgt, out, w = sys.argv[1:6]
    os.makedirs(w, exist_ok=True)
    want = sha(tgt)
    enc = scrubbed(src, os.path.join(w, "enc_src.cci"), 0, 0x4000)
    run(xd, "-e", "-f", "-a", "-A", "-9", "-S", "djw", "-B", "1073741824", "-s", enc, tgt, out)
    os.remove(enc)
    print("patch: %s, %d B (%.2f MB)" % (out, os.path.getsize(out), os.path.getsize(out) / 1048576))

    head = open(out, "rb").read(1 << 16)
    leaks = [m.decode(errors="replace") for m in LEAK_RE.findall(head)]
    print("path text in patch header: %s" % ("none" if not leaks else "LEAK %s" % leaks))

    chk = os.path.join(w, "applied.cci")
    run(xd, "-d", "-f", "-B", "1073741824", "-s", src, out, chk)
    ok = sha(chk) == want
    print("decode against this dump:              %s" % ("EXACT" if ok else "WRONG"))
    for k in range(2):
        pert = scrubbed(src, os.path.join(w, "pert.cci"), SEED_OFF, SEED_LEN)
        run(xd, "-d", "-f", "-B", "1073741824", "-s", pert, out, chk)
        good = sha(chk) == want
        ok &= good
        print("decode against a dump with new seed #%d: %s" % (k + 1, "EXACT" if good else "WRONG"))
        os.remove(pert)
    os.remove(chk)
    print("target sha256: %s" % want)
    return 0 if ok and not leaks else 1


if __name__ == "__main__":
    sys.exit(main())
