# -*- coding: utf-8 -*-
r"""English HOME menu banner and HOME title text, made from the player's own files.

The retail banner.bnr (CBMD) holds one LZ11-compressed CGFX model. Its logo is a
separate 512x128 RGBA4 texture, and that texture is the title screen's logo
(Layout/Title_upper.arc, timg/title.bclim, 336x128 RGBA4) placed at x = 88.
The English banner puts RC1's English title.bclim at the same spot, texel for
texel (both RGBA4, so nothing is resampled), recompresses the model and keeps
the banner sound byte-identical. icon.icn (SMDH) gets English titles in all 12
language slots; nothing else in it changes.

No game data lives here: the model comes from the retail ROM, the logo from the
overlay. build_rom.py checks both outputs against the approved md5s.

Usage (standalone): home_banner.py <retail banner.bnr> <Title_upper.arc> <retail icon.icn> <out dir>
"""
import os
import struct
import sys

LOGO_X = 88
TEX_W, TEX_H = 512, 128
RGBA4 = 4                                   # PICA texture format code in the CGFX TXOB
CLIM_RGBA4 = 8                              # same format in CLIM numbering
SHORT = "Dragon Quest Heroes: Rocket Slime 3"
LONG = "Dragon Quest Heroes: Rocket Slime 3\nPirate & Platywag"
PUBLISHER = "SQUARE ENIX"


def lz11_decode(d, off=0):
    assert d[off] == 0x11, "not LZ11"
    size = struct.unpack_from("<I", d, off)[0] >> 8
    out = bytearray()
    i = off + 4
    while len(out) < size:
        flags = d[i]; i += 1
        for bit in range(7, -1, -1):
            if len(out) >= size:
                break
            if not (flags >> bit) & 1:
                out.append(d[i]); i += 1
                continue
            b0 = d[i]; ind = b0 >> 4
            if ind == 0:
                ln = (((b0 & 0xF) << 4) | (d[i + 1] >> 4)) + 0x11
                disp = (((d[i + 1] & 0xF) << 8) | d[i + 2]) + 1; i += 3
            elif ind == 1:
                ln = (((b0 & 0xF) << 12) | (d[i + 1] << 4) | (d[i + 2] >> 4)) + 0x111
                disp = (((d[i + 2] & 0xF) << 8) | d[i + 3]) + 1; i += 4
            else:
                ln = ind + 1
                disp = (((b0 & 0xF) << 8) | d[i + 1]) + 1; i += 2
            for _ in range(ln):
                out.append(out[-disp])
    return bytes(out)


def lz11_encode(data):
    """Greedy LZ11, window 0x1000."""
    n = len(data)
    out = bytearray(struct.pack("<I", 0x11 | (n << 8)))
    i = 0
    while i < n:
        flags = 0; chunk = bytearray()
        for bit in range(7, -1, -1):
            if i >= n:
                break
            best_len, best_disp = 0, 0
            start = max(0, i - 0x1000)
            j = data.rfind(data[i:i + 3], start, i + 2) if i + 3 <= n else -1
            while j != -1 and j >= start:
                ln = 0
                while i + ln < n and ln < 0x10110 and data[j + ln] == data[i + ln]:
                    ln += 1
                if ln > best_len:
                    best_len, best_disp = ln, i - j
                    if ln >= 0x10110:
                        break
                j = data.rfind(data[i:i + 3], start, j + 2) if j > start else -1
            if best_len >= 3:
                flags |= 1 << bit
                d = best_disp - 1
                if best_len <= 0x10:
                    chunk += bytes((((best_len - 1) << 4) | (d >> 8), d & 0xFF))
                elif best_len <= 0x110:
                    l = best_len - 0x11
                    chunk += bytes(((l >> 4), ((l & 0xF) << 4) | (d >> 8), d & 0xFF))
                else:
                    l = best_len - 0x111
                    chunk += bytes((0x10 | (l >> 12), (l >> 4) & 0xFF, ((l & 0xF) << 4) | (d >> 8), d & 0xFF))
                i += best_len
            else:
                chunk.append(data[i]); i += 1
        out.append(flags); out += chunk
    return bytes(out)


def texel_order(w, h):
    """PICA texel order: 8x8 tiles, Morton order inside each tile."""
    morton = [((k & 1) | ((k & 4) >> 1) | ((k & 16) >> 2), ((k & 2) >> 1) | ((k & 8) >> 2) | ((k & 32) >> 3))
              for k in range(64)]
    return [(tx + mx, ty + my) for ty in range(0, h, 8) for tx in range(0, w, 8) for mx, my in morton]


def darc_file(arc, want):
    """Bytes of the file named `want` anywhere in a darc archive."""
    assert arc[:4] == b"darc"
    tbl = struct.unpack_from("<I", arc, 0x10)[0]
    count = struct.unpack_from("<I", arc, tbl + 8)[0]
    names = tbl + count * 12
    for i in range(count):
        name_off, off, size = struct.unpack_from("<III", arc, tbl + i * 12)
        if name_off >> 24:
            continue
        p = names + (name_off & 0xFFFFFF); e = p
        while arc[e:e + 2] != b"\0\0":
            e += 2
        if arc[p:e].decode("utf-16-le") == want:
            return arc[off:off + size]
    raise SystemExit("%s not in archive" % want)


def clim_texels(blob):
    """RGBA4 CLIM -> {(x, y): u16 word} for the visible w x h area."""
    assert blob[-0x28:-0x24] == b"CLIM"
    w, h, fmt = struct.unpack_from("<HHI", blob, len(blob) - 0x14 + 8)
    assert fmt == CLIM_RGBA4, "title.bclim is not RGBA4"
    pw, ph = 1 << (w - 1).bit_length(), 1 << (h - 1).bit_length()
    words = struct.unpack_from("<%dH" % (pw * ph), blob, 0)
    return w, h, {xy: v for xy, v in zip(texel_order(pw, ph), words) if xy[0] < w and xy[1] < h}


def make_banner(retail_banner, title_upper_arc):
    b = retail_banner
    assert b[:4] == b"CBMD"
    offs = struct.unpack_from("<14I", b, 8); cwav = struct.unpack_from("<I", b, 0x84)[0]
    assert offs[0] == 0x88 and not any(offs[1:]), "unexpected banner layout"
    model = bytearray(lz11_decode(b[0x88:cwav]))
    hits = []
    p = model.find(b"TXOB")
    while p != -1:
        h, w = struct.unpack_from("<II", model, p + 0x14)
        if (w, h) == (TEX_W, TEX_H) and struct.unpack_from("<I", model, p + 4 + 11 * 4)[0] == RGBA4:
            n = struct.unpack_from("<I", model, p + 4 + 15 * 4)[0]
            data = p + 4 + 16 * 4 + struct.unpack_from("<I", model, p + 4 + 16 * 4)[0]
            hits.append((data, n))
        p = model.find(b"TXOB", p + 4)
    assert len(hits) == 1 and hits[0][1] == TEX_W * TEX_H * 2, hits
    data, n = hits[0]
    w, h, logo = clim_texels(darc_file(title_upper_arc, "title.bclim"))
    assert h == TEX_H and LOGO_X + w <= TEX_W
    words = [logo.get((x - LOGO_X, y), 0) for x, y in texel_order(TEX_W, TEX_H)]
    model[data:data + n] = struct.pack("<%dH" % len(words), *words)
    chunk = lz11_encode(bytes(model))
    end = 0x88 + len(chunk); pad = (-end) % 0x20        # the sound must start 0x20-aligned
    hdr = bytearray(b[:0x88]); struct.pack_into("<I", hdr, 0x84, end + pad)
    out = bytes(hdr) + chunk + bytes(pad) + b[cwav:]
    assert lz11_decode(out[0x88:end]) == bytes(model)
    return out


def make_icon(retail_icon):
    d = bytearray(retail_icon)
    assert d[:4] == b"SMDH"
    for lang in range(12):
        o = 8 + lang * 0x200
        for text, at, size in ((SHORT, 0, 0x80), (LONG, 0x80, 0x100), (PUBLISHER, 0x180, 0x80)):
            raw = text.encode("utf-16-le"); assert len(raw) < size
            d[o + at:o + at + size] = raw + bytes(size - len(raw))
    return bytes(d)


if __name__ == "__main__":
    ban, arc, icn, out = sys.argv[1:5]
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, "banner.bnr"), "wb").write(make_banner(open(ban, "rb").read(), open(arc, "rb").read()))
    open(os.path.join(out, "icon.icn"), "wb").write(make_icon(open(icn, "rb").read()))
