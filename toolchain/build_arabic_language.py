import zlib
import struct
import os
import sys
import re

sys.path.insert(0, os.path.dirname(__file__))
from arabic_reshaper_bidi import format_arabic_text
from translation_rules import translate_string

def build_arabic_database(input_bin_path, output_bin_path):
    print(f"Loading {input_bin_path}...")
    with open(input_bin_path, 'rb') as f:
        file_bytes = f.read()

    uncompressed_size = struct.unpack('<I', file_bytes[:4])[0]
    raw = zlib.decompress(file_bytes[4:])
    count = struct.unpack('>I', raw[:4])[0]
    print(f"Total entries: {count}")

    idx = 4
    entries = []
    for _ in range(count):
        klen = struct.unpack('>H', raw[idx:idx+2])[0]
        idx += 2
        key = raw[idx:idx+klen].decode('utf-8', errors='replace')
        idx += klen
        vlen = struct.unpack('>H', raw[idx:idx+2])[0]
        idx += 2
        val = raw[idx:idx+vlen].decode('utf-8', errors='replace')
        idx += vlen
        entries.append((key, val))

    translated_entries = []
    arabic_count = 0

    print("Translating and formatting entries...")
    for i, (key, val) in enumerate(entries):
        tr = translate_string(val, key)
        # Apply BiDi and Arabic letter shaping
        formatted = format_arabic_text(tr)
        
        # Verify placeholders safety
        orig_phs = re.findall(r'(\{[^\}]+\}|%[0-9\.]*[sdfi])', val)
        for ph in orig_phs:
            if ph not in formatted:
                formatted = val
                break
                
        if any(0x0600 <= ord(c) <= 0x06FF or 0xFB50 <= ord(c) <= 0xFEFF for c in formatted):
            arabic_count += 1
            
        translated_entries.append((key, formatted))

    print(f"Translation completed: {arabic_count} entries contain reshaped Arabic text.")

    # Serialize back into binary format
    payload = bytearray()
    payload += struct.pack('>I', len(translated_entries))
    for k, v in translated_entries:
        k_bytes = k.encode('utf-8')
        v_bytes = v.encode('utf-8')
        payload += struct.pack('>H', len(k_bytes))
        payload += k_bytes
        payload += struct.pack('>H', len(v_bytes))
        payload += v_bytes

    uncomp_len = len(payload)
    compressed = zlib.compress(bytes(payload), level=9)
    out_file = struct.pack('<I', uncomp_len) + compressed

    os.makedirs(os.path.dirname(output_bin_path), exist_ok=True)
    with open(output_bin_path, 'wb') as f:
        f.write(out_file)

    print(f"Saved Arabic language binary to {output_bin_path} ({len(out_file)} bytes, uncompressed {uncomp_len})")
    return arabic_count, len(translated_entries)

if __name__ == '__main__':
    src = r'D:\SteamLibrary\steamapps\common\Brawlhalla\languages\language.1.bin.original_backup'
    dst = r'D:\SteamLibrary\steamapps\common\Brawlhalla\arabic_localization\language.1.arabic.bin'
    build_arabic_database(src, dst)
