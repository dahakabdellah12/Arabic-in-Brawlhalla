import zlib
import struct
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(__file__))

from arabic_font_injector import parse_df3

font_curr_path = r'D:\SteamLibrary\steamapps\common\Brawlhalla\arabic_localization\Font_Latin_Arabic.swf'
lang_bin_path = r'D:\SteamLibrary\steamapps\common\Brawlhalla\arabic_localization\language.1.arabic.bin'

print("=" * 70)
print("  Comprehensive Verification of Full Game Arabic Localization")
print("=" * 70)

# 1. Parse all fonts in SWF
with open(font_curr_path, 'rb') as f:
    f_bytes = f.read()
f_payload = zlib.decompress(f_bytes[8:]) if f_bytes[:3] == b'CWS' else f_bytes[8:]

pos = (5 + (f_payload[0] >> 3) * 4 + 7) // 8 + 4
font_codes = {}
font_names = {}

while pos < len(f_payload):
    hdr = struct.unpack('<H', f_payload[pos:pos+2])[0]
    pos += 2
    t_type = hdr >> 6
    t_len = hdr & 0x3f
    if t_len == 0x3f:
        t_len = struct.unpack('<I', f_payload[pos:pos+4])[0]
        pos += 4
    t_data = f_payload[pos:pos+t_len]
    pos += t_len
    if t_type == 75:
        parsed = parse_df3(t_data)
        fid = parsed['font_id']
        font_codes[fid] = set(parsed['codes'])
        font_names[fid] = parsed['name'].strip()

print(f"Fonts loaded from SWF: {len(font_codes)}")
for fid in sorted(font_codes.keys()):
    print(f"  • Font ID {fid} ({font_names[fid]}): {len(font_codes[fid])} glyphs")

# 2. Parse language binary
with open(lang_bin_path, 'rb') as f:
    dec = zlib.decompress(f.read()[4:])

count = struct.unpack('>I', dec[:4])[0]
print(f"\nLanguage entries in binary: {count}")

idx = 4
arabic_entries = 0
all_arabic_chars = set()
placeholder_errors = 0

for _ in range(count):
    klen = struct.unpack('>H', dec[idx:idx+2])[0]; idx += 2
    key = dec[idx:idx+klen].decode('utf-8', errors='replace'); idx += klen
    vlen = struct.unpack('>H', dec[idx:idx+2])[0]; idx += 2
    val = dec[idx:idx+vlen].decode('utf-8', errors='replace'); idx += vlen
    
    # Check if entry contains Arabic
    has_ar = any(0x0600 <= ord(c) <= 0x06FF or 0xFB50 <= ord(c) <= 0xFEFF for c in val)
    if has_ar:
        arabic_entries += 1
        for c in val:
            if ord(c) > 127:
                all_arabic_chars.add(ord(c))

print(f"Total Arabic entries: {arabic_entries}")
print(f"Total unique non-ASCII / Arabic glyph codes needed: {len(all_arabic_chars)}")

# 3. Check font coverage
all_fonts_ok = True
for fid in sorted(font_codes.keys()):
    missing = [c for c in all_arabic_chars if c not in font_codes[fid]]
    if not missing:
        print(f"  ✓ Font ID {fid} ({font_names[fid]}): 100% COVERAGE (0 missing glyphs)")
    else:
        print(f"  ✕ Font ID {fid} ({font_names[fid]}): {len(missing)} missing glyphs! Sample: {[hex(c) for c in missing[:10]]}")
        all_fonts_ok = False

print("\n" + "=" * 70)
if all_fonts_ok:
    print("  RESULT: FULL SUCCESS! ALL ARABIC GLYPHS ARE 100% SUPPORTED IN ALL 5 FONTS!")
else:
    print("  RESULT: Some glyphs missing.")
print("=" * 70)
