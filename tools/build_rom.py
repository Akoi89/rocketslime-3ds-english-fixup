# -*- coding: utf-8 -*-
r"""Build a self-contained patched .cci: RC1 + the fix-up's files baked into the ROM.

No SD files, no Luma. Adapted from TGAA's build_rhdn_patches.py (same lessons:
--not-encrypt, --not-pad, zero the random card seed).

1. unpack the decrypted retail .cci (code decompressed with -u; must equal the
   known clean code.bin)
2. romfs: every data/Game file in the fix-up overlay (RC1's 135, some edited by
   the fix-up; all exist in retail) replaces the retail one, plus tables.bin at
   the romfs root
3. code: clean code + RC1 code.ips + loader edit: RC1 reads tables.bin from the
   SD card only (FSUSER_OpenFileDirectly, archive 9). It now reads the game's own
   RomFS raw (archive 3, binary 12-zero path, as libctru does) at tables.bin's
   offset in RomFS level 3, fixed size. RC1's data redirect (SD first, RomFS
   fallback) is untouched: with no SD folder it falls back to the files baked in.
   Plus one word outside the loader: the name keyboard opens on ABC (0x3B61E8).
3b. exefs banner.bnr / icon.icn: English HOME menu banner logo and title text
    (home_banner.py, from the retail ExeFS + the overlay's Title_upper.arc).
4. rebuild exefs (code recompressed with -z), cxi (--not-encrypt), cci (--not-pad),
   zero the card seed, verify by re-extraction.

Usage: build_rom.py <retail.cci> <overlay_fti_root> <out.cci> <work_dir>
"""

import hashlib
import os
import shutil
import struct
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.dirname(HERE)
T3 = os.path.join(ROOT, "_tools", "3dstool.exe")
CT = os.path.join(ROOT, "Batch CIA 3DS Decryptor", "ctrtool.exe")
IPS = os.path.join(HERE, "firm", "code.ips")
CLEAN_CODE_MD5 = "ab181c1d3b7b81acfbf99d1e7b7b6d36"
SEED_OFF, SEED_LEN = 0x1010, 0x30
# HOME banner / title text (home_banner.py): retail inputs and the approved outputs
BANNER_JP_MD5, BANNER_EN_MD5 = "bd1d319afdd743b5aa372420a1f753c5", "a07c524dae51a701c5233c0d0cc16be0"
ICON_JP_MD5, ICON_EN_MD5 = "0dad3af69858e85c93027885a0b61973", "49bb02860b053d8f3ab99781b2c35fd8"
BASE = 0x100000
TABLES_NAME = "tables.bin"

# loader edit: (va, expected old word, new word, what)
FREE = 0x3EBE70            # 400 zero bytes to 0x3EC000
PATH_AT = FREE             # 12 zero bytes = binary RomFS path
OFF_LIT = 0x3EBE80
SIZE_LIT = 0x3EBE84


def run(*a):
    a = [os.path.normpath(str(x)) if ("/" in str(x) or "\\" in str(x)) else str(x) for x in a]
    r = subprocess.run(a, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit("FAILED (%d): %s\n%s\n%s" % (r.returncode, " ".join(a), r.stdout, r.stderr))
    return r.stdout


def md5(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 24), b""):
            h.update(b)
    return h.hexdigest()


def apply_ips(patch, data):
    buf = bytearray(data)
    p = 5
    while patch[p:p + 3] != b"EOF":
        off = int.from_bytes(patch[p:p + 3], "big")
        sz = int.from_bytes(patch[p + 3:p + 5], "big")
        p += 5
        if sz == 0:
            n = int.from_bytes(patch[p:p + 2], "big")
            buf[off:off + n] = bytes([patch[p + 2]]) * n
            p += 3
        else:
            buf[off:off + sz] = patch[p:p + sz]
            p += sz
    return buf


def ldr_pc(rd, at, lit):
    imm = lit - (at + 8)
    assert 0 <= imm < 0x1000
    return 0xE59F0000 | (rd << 12) | imm


def romfs_file_offset(romfs_bin, name):
    """Offset of a root file's data inside RomFS level 3, and level 3's own offset."""
    d = open(romfs_bin, "rb").read(0x2000)
    assert d[:4] == b"IVFC"
    master = struct.unpack_from("<I", d, 0x08)[0]
    l3_bs = struct.unpack_from("<I", d, 0x4C)[0]
    l3 = (0x60 + master + (1 << l3_bs) - 1) & ~((1 << l3_bs) - 1)
    with open(romfs_bin, "rb") as f:
        f.seek(l3)
        hdr = f.read(0x28)
        (hl, dho, dhl, dmo, dml, fho, fhl, fmo, fml, fdo) = struct.unpack("<10I", hdr)
        f.seek(l3 + fmo)
        meta = f.read(fml)
    p = 0
    while p < len(meta):
        parent, sib, doff, dsize, hsib, nlen = struct.unpack_from("<IIQQII", meta, p)
        fname = meta[p + 0x20:p + 0x20 + nlen].decode("utf-16-le")
        if parent == 0 and fname == name:
            return l3, fdo + doff, dsize
        p += 0x20 + ((nlen + 3) & ~3)
    raise SystemExit("%s not found at romfs root" % name)


def main():
    src, fti, out, w = sys.argv[1:5]
    if os.path.exists(w):
        shutil.rmtree(w)
    os.makedirs(w)
    j = lambda *p: os.path.join(w, *p)

    # 1. unpack
    run(T3, "-xtf", "cci", src, "--header", j("ncsd.bin"), "-0", j("p0.cxi"))
    run(T3, "-xtf", "cxi", j("p0.cxi"), "--header", j("ncch.bin"), "--exh", j("exh.bin"),
        "--exefs", j("exefs.bin"), "--romfs", j("romfs.bin"), "--logo", j("logo.bin"),
        "--plain", j("plain.bin"))
    os.makedirs(j("exefs")); os.makedirs(j("romfs"))
    run(T3, "-xtuf", "exefs", j("exefs.bin"), "--header", j("exefs_hdr.bin"), "--exefs-dir", j("exefs"))
    run(T3, "-xtf", "romfs", j("romfs.bin"), "--romfs-dir", j("romfs"))
    got = md5(j("exefs", "code.bin"))
    assert got == CLEAN_CODE_MD5, "unpacked code.bin %s is not the known clean code" % got
    print("unpacked: code.bin decompressed = known clean code (%s)" % got)
    os.remove(j("p0.cxi")); os.remove(j("romfs.bin"))

    # 2. romfs overlay + tables.bin
    n = 0
    game = os.path.join(fti, "data", "Game")
    for r, _, fs in os.walk(game):
        for f in fs:
            rel = os.path.relpath(os.path.join(r, f), fti)
            dst = j("romfs", rel)
            if not os.path.exists(dst):
                raise SystemExit("overlay file not in retail romfs: " + rel)
            shutil.copyfile(os.path.join(r, f), dst)
            n += 1
    shutil.copyfile(os.path.join(fti, "tables.bin"), j("romfs", TABLES_NAME))
    tables = open(os.path.join(fti, "tables.bin"), "rb").read()
    print("romfs: %d data/Game files replaced, tables.bin added (%d B)" % (n, len(tables)))
    run(T3, "-ctf", "romfs", j("romfs_new.bin"), "--romfs-dir", j("romfs"))
    l3, toff, tsize = romfs_file_offset(j("romfs_new.bin"), TABLES_NAME)
    with open(j("romfs_new.bin"), "rb") as f:
        f.seek(l3 + toff)
        assert f.read(len(tables)) == tables and tsize == len(tables)
    print("romfs: level 3 at 0x%X, tables.bin at level-3 offset 0x%X (%d B), bytes verified"
          % (l3, toff, tsize))

    # 3. code
    code = apply_ips(open(IPS, "rb").read(), open(j("exefs", "code.bin"), "rb").read())
    edits = [
        (0x3EBD70, 0xE3A03009, 0xE3A03003, "archive 9 (SD) -> 3 (own RomFS)"),
        (0x3EBD84, 0xE3A05003, 0xE3A05002, "file path type ASCII -> BINARY"),
        (0x3EBD94, 0xE3A05021, 0xE3A0500C, "file path size 0x21 -> 12"),
        (0x3EBDBC, 0xE3A02000, ldr_pc(2, 0x3EBDBC, OFF_LIT), "read offset 0 -> tables.bin offset"),
        (0x3EBDCC, 0xE59D4010, ldr_pc(4, 0x3EBDCC, SIZE_LIT), "read size GetSize -> fixed"),
        # name-entry keyboard: reset routine at 0x3B61CC calls SetPage(this, 0);
        # page 2 is the ABC tab (KANA_TAB_RE.md, rendered 2026-09-11)
        (0x3B61E8, 0xE3A01000, 0xE3A01002, "keyboard initial page hiragana -> ABC"),
    ]
    lit_edits = [
        (0x3EBE68, 0x003EBCC8, PATH_AT, "file path ptr -> 12 zero bytes"),
    ]
    for va, old, new, what in edits + lit_edits:
        cur = struct.unpack_from("<I", code, va - BASE)[0]
        assert cur == old, "0x%X: expected 0x%08X, found 0x%08X (%s)" % (va, old, cur, what)
        struct.pack_into("<I", code, va - BASE, new)
    assert code[PATH_AT - BASE:PATH_AT - BASE + 12] == bytes(12)
    for va in (OFF_LIT, SIZE_LIT):
        assert code[va - BASE:va - BASE + 4] == bytes(4), "literal slot 0x%X not free" % va
    struct.pack_into("<I", code, OFF_LIT - BASE, toff)
    struct.pack_into("<I", code, SIZE_LIT - BASE, len(tables))
    open(j("exefs", "code.bin"), "wb").write(code)
    print("code: RC1 code.ips + %d loader edits applied" % (len(edits) + len(lit_edits) + 2))

    # 3b. HOME banner + HOME title text: made from the retail ExeFS and the overlay's title logo
    # (3dstool names the ExeFS entries banner.bnr / icon.icn)
    import home_banner
    ban, icn = j("exefs", "banner.bnr"), j("exefs", "icon.icn")
    assert md5(ban) == BANNER_JP_MD5, "banner.bnr in the source is not retail"
    assert md5(icn) == ICON_JP_MD5, "icon.icn in the source is not retail"
    arc = open(os.path.join(fti, "data", "Game", "Layout", "Title_upper.arc"), "rb").read()
    new_ban = home_banner.make_banner(open(ban, "rb").read(), arc)
    new_icn = home_banner.make_icon(open(icn, "rb").read())
    open(ban, "wb").write(new_ban)
    open(icn, "wb").write(new_icn)
    assert md5(ban) == BANNER_EN_MD5, "made banner.bnr is not the approved banner"
    assert md5(icn) == ICON_EN_MD5, "made icon.icn is not the approved icon"
    print("exefs: English HOME banner (%s) and title text (%s) made and verified" % (BANNER_EN_MD5[:8], ICON_EN_MD5[:8]))

    # 4. rebuild (this NCCH has no logo region, so logo/plain are passed only if present)
    opt = []
    for flag, f in (("--logo", "logo.bin"), ("--plain", "plain.bin")):
        if os.path.exists(j(f)):
            opt += [flag, j(f)]
    print("regions present besides exh/exefs/romfs: %s" % ([f for _, f in zip(opt[::2], opt[1::2])] or "none"))
    run(T3, "-ctzf", "exefs", j("exefs_new.bin"), "--exefs-dir", j("exefs"), "--header", j("exefs_hdr.bin"))
    run(T3, "-ctf", "cxi", j("p0_new.cxi"), "--header", j("ncch.bin"), "--exh", j("exh.bin"),
        "--exefs", j("exefs_new.bin"), "--romfs", j("romfs_new.bin"), *opt, "--not-encrypt")
    run(T3, "-ctf", "cci", out, "--header", j("ncsd.bin"), "-0", j("p0_new.cxi"), "--not-pad")
    with open(out, "r+b") as f:
        f.seek(SEED_OFF)
        f.write(bytes(SEED_LEN))
    info = run(CT, "-i", out)
    assert "Crypto key:          None" in info or "Crypto Key           None" in info, "not NoCrypto"
    print("built: %s (%d B), NoCrypto" % (out, os.path.getsize(out)))

    # verify by re-extraction
    v = j("verify"); os.makedirs(v)
    run(T3, "-xtf", "cci", out, "-0", os.path.join(v, "p0.cxi"))
    run(T3, "-xtf", "cxi", os.path.join(v, "p0.cxi"), "--exh", os.path.join(v, "exh.bin"),
        "--exefs", os.path.join(v, "exefs.bin"), "--romfs", os.path.join(v, "romfs.bin"),
        "--logo", os.path.join(v, "logo.bin"), "--plain", os.path.join(v, "plain.bin"))
    os.makedirs(os.path.join(v, "exefs"))
    run(T3, "-xtuf", "exefs", os.path.join(v, "exefs.bin"), "--exefs-dir", os.path.join(v, "exefs"))
    assert md5(os.path.join(v, "exefs", "code.bin")) == md5(j("exefs", "code.bin")), "code.bin differs after rebuild"
    assert md5(os.path.join(v, "exefs", "banner.bnr")) == BANNER_EN_MD5, "banner differs after rebuild"
    assert md5(os.path.join(v, "exefs", "icon.icn")) == ICON_EN_MD5, "icon differs after rebuild"
    for f in ("exh.bin", "logo.bin", "plain.bin"):
        if os.path.exists(j(f)):
            assert md5(os.path.join(v, f)) == md5(j(f)), f + " changed"
    assert md5(os.path.join(v, "romfs.bin")) == md5(j("romfs_new.bin")), "romfs differs"
    print("verified by re-extraction: code, exheader, romfs (and logo/plain if present) all as built")
    shutil.rmtree(v)
    return 0


if __name__ == "__main__":
    sys.exit(main())
