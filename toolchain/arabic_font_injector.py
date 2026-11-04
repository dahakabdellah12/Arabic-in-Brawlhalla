import zlib
import struct
import os
import sys
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import DecomposingRecordingPen

class BitWriter:
    def __init__(self):
        self.bytes = bytearray()
        self.current_byte = 0
        self.bit_count = 0

    def write_bit(self, b):
        self.current_byte = (self.current_byte << 1) | (b & 1)
        self.bit_count += 1
        if self.bit_count == 8:
            self.bytes.append(self.current_byte)
            self.current_byte = 0
            self.bit_count = 0

    def write_ubits(self, val, n):
        for i in range(n - 1, -1, -1):
            self.write_bit((val >> i) & 1)

    def write_sbits(self, val, n):
        if val < 0:
            val += (1 << n)
        self.write_ubits(val, n)

    def finish(self):
        if self.bit_count > 0:
            self.current_byte <<= (8 - self.bit_count)
            self.bytes.append(self.current_byte)
            self.current_byte = 0
            self.bit_count = 0
        return bytes(self.bytes)

def bits_needed_signed(val):
    if val == 0:
        return 1
    if val < 0:
        v = -val
        b = 1
        while (1 << (b - 1)) < (v + 1):
            b += 1
        return b
    else:
        b = 1
        while (1 << (b - 1)) <= val:
            b += 1
        return b

def encode_glyph_shape(glyph_ops, scale=20.48):
    bw = BitWriter()
    bw.write_ubits(1, 4) # NumFillBits = 1
    bw.write_ubits(0, 4) # NumLineBits = 0
    
    cur_x, cur_y = 0, 0
    start_x, start_y = 0, 0
    first_contour = True
    
    for op, args in glyph_ops:
        if op == 'moveTo':
            pt = args[0]
            tx = int(round(pt[0] * scale))
            ty = int(round(-pt[1] * scale))
            start_x, start_y = tx, ty
            cur_x, cur_y = tx, ty
            
            bw.write_bit(0)
            state_fill0 = 1 if first_contour else 0
            flags = (state_fill0 << 1) | 1 # state_move_to
            bw.write_ubits(flags, 5)
            
            nb = max(bits_needed_signed(tx), bits_needed_signed(ty), 1)
            bw.write_ubits(nb, 5)
            bw.write_sbits(tx, nb)
            bw.write_sbits(ty, nb)
            
            if state_fill0:
                bw.write_ubits(1, 1)
                first_contour = False
                
        elif op == 'lineTo':
            pt = args[0]
            tx = int(round(pt[0] * scale))
            ty = int(round(-pt[1] * scale))
            dx = tx - cur_x
            dy = ty - cur_y
            cur_x, cur_y = tx, ty
            if dx == 0 and dy == 0:
                continue
                
            bw.write_bit(1)
            bw.write_bit(1)
            nb = max(bits_needed_signed(dx), bits_needed_signed(dy), 2)
            bw.write_ubits(nb - 2, 4)
            
            if dx != 0 and dy != 0:
                bw.write_bit(1)
                bw.write_sbits(dx, nb)
                bw.write_sbits(dy, nb)
            elif dy != 0:
                bw.write_bit(0)
                bw.write_bit(1)
                bw.write_sbits(dy, nb)
            else:
                bw.write_bit(0)
                bw.write_bit(0)
                bw.write_sbits(dx, nb)
                
        elif op == 'qCurveTo':
            pts = args
            for i in range(len(pts) - 1):
                c_pt = pts[i]
                if i < len(pts) - 2:
                    next_c = pts[i+1]
                    a_pt = ((c_pt[0] + next_c[0]) / 2.0, (c_pt[1] + next_c[1]) / 2.0)
                else:
                    a_pt = pts[-1]
                
                cx = int(round(c_pt[0] * scale))
                cy = int(round(-c_pt[1] * scale))
                ax = int(round(a_pt[0] * scale))
                ay = int(round(-a_pt[1] * scale))
                
                cdx = cx - cur_x
                cdy = cy - cur_y
                adx = ax - cx
                ady = ay - cy
                cur_x, cur_y = ax, ay
                
                bw.write_bit(1)
                bw.write_bit(0)
                nb = max(bits_needed_signed(cdx), bits_needed_signed(cdy),
                         bits_needed_signed(adx), bits_needed_signed(ady), 2)
                bw.write_ubits(nb - 2, 4)
                bw.write_sbits(cdx, nb)
                bw.write_sbits(cdy, nb)
                bw.write_sbits(adx, nb)
                bw.write_sbits(ady, nb)
                
        elif op == 'closePath':
            if cur_x != start_x or cur_y != start_y:
                dx = start_x - cur_x
                dy = start_y - cur_y
                cur_x, cur_y = start_x, start_y
                bw.write_bit(1)
                bw.write_bit(1)
                nb = max(bits_needed_signed(dx), bits_needed_signed(dy), 2)
                bw.write_ubits(nb - 2, 4)
                if dx != 0 and dy != 0:
                    bw.write_bit(1)
                    bw.write_sbits(dx, nb)
                    bw.write_sbits(dy, nb)
                elif dy != 0:
                    bw.write_bit(0)
                    bw.write_bit(1)
                    bw.write_sbits(dy, nb)
                else:
                    bw.write_bit(0)
                    bw.write_bit(0)
                    bw.write_sbits(dx, nb)
                    
    bw.write_bit(0)
    bw.write_ubits(0, 5)
    return bw.finish()

def encode_rect(xmin, xmax, ymin, ymax):
    x1, x2 = min(xmin, xmax), max(xmin, xmax)
    y1, y2 = min(ymin, ymax), max(ymin, ymax)
    bw = BitWriter()
    nb = max(
        bits_needed_signed(x1),
        bits_needed_signed(x2),
        bits_needed_signed(y1),
        bits_needed_signed(y2),
        1
    )
    bw.write_ubits(nb, 5)
    bw.write_sbits(x1, nb)
    bw.write_sbits(x2, nb)
    bw.write_sbits(y1, nb)
    bw.write_sbits(y2, nb)
    return bw.finish()

def parse_df3(t_data):
    font_id = struct.unpack('<H', t_data[:2])[0]
    flags = t_data[2]
    lang = t_data[3]
    name_len = t_data[4]
    name = t_data[5:5+name_len].decode('latin1')
    p = 5 + name_len
    num_glyphs = struct.unpack('<H', t_data[p:p+2])[0]
    p += 2
    
    wide_offsets = bool(flags & 0x08)
    off_size = 4 if wide_offsets else 2
    offset_table_start = p
    offsets = [struct.unpack('<I' if wide_offsets else '<H', t_data[p + i*off_size : p + (i+1)*off_size])[0] for i in range(num_glyphs)]
    code_table_offset = struct.unpack('<I' if wide_offsets else '<H', t_data[p + num_glyphs*off_size : p + (num_glyphs+1)*off_size])[0]
    
    shapes = []
    for i in range(num_glyphs):
        start = offset_table_start + offsets[i]
        end = offset_table_start + (offsets[i+1] if i + 1 < num_glyphs else code_table_offset)
        shapes.append(t_data[start:end])
    
    ct_start = offset_table_start + code_table_offset
    codes = [struct.unpack('<H', t_data[ct_start + i*2 : ct_start + (i+1)*2])[0] for i in range(num_glyphs)]
    
    p = ct_start + num_glyphs * 2
    has_layout = bool(flags & 0x80)
    layout = None
    if has_layout:
        ascent, descent, leading = struct.unpack('<hhh', t_data[p:p+6])
        p += 6
        advances = [struct.unpack('<h', t_data[p + i*2 : p + (i+1)*2])[0] for i in range(num_glyphs)]
        p += num_glyphs * 2
        bounds = []
        for g in range(num_glyphs):
            rect_nbits = t_data[p] >> 3
            rect_total_bits = 5 + rect_nbits * 4
            b_len = (rect_total_bits + 7) // 8
            bounds.append(t_data[p:p+b_len])
            p += b_len
        kerning_count = struct.unpack('<H', t_data[p:p+2])[0]
        p += 2
        kerning_data = t_data[p:p + kerning_count * 6]
        p += kerning_count * 6
        layout = {
            'ascent': ascent,
            'descent': descent,
            'leading': leading,
            'advances': advances,
            'bounds': bounds,
            'kerning_count': kerning_count,
            'kerning_data': kerning_data
        }
        
    return {
        'font_id': font_id,
        'flags': flags,
        'lang': lang,
        'name': name,
        'shapes': shapes,
        'codes': codes,
        'layout': layout
    }

def pack_df3(info):
    name_bytes = info['name'].encode('latin1')
    res = bytearray()
    flags = info['flags'] | 0x08 | 0x04 # wide offsets + wide codes
    res += struct.pack('<HBB', info['font_id'], flags, info['lang'])
    res.append(len(name_bytes))
    res += name_bytes
    
    num_glyphs = len(info['shapes'])
    res += struct.pack('<H', num_glyphs)
    
    offset_table_len = (num_glyphs + 1) * 4
    current_shape_off = offset_table_len
    
    offsets = []
    shapes_bytes = bytearray()
    for s in info['shapes']:
        offsets.append(current_shape_off)
        shapes_bytes += s
        current_shape_off += len(s)
    code_table_offset = current_shape_off
    
    for off in offsets:
        res += struct.pack('<I', off)
    res += struct.pack('<I', code_table_offset)
    res += shapes_bytes
    
    for c in info['codes']:
        res += struct.pack('<H', c)
        
    if info['layout']:
        lay = info['layout']
        res += struct.pack('<hhh', lay['ascent'], lay['descent'], lay['leading'])
        for a in lay['advances']:
            res += struct.pack('<h', a)
        for b in lay['bounds']:
            res += b
        res += struct.pack('<H', lay['kerning_count'])
        res += lay['kerning_data']
        
    return bytes(res)

def extract_glyphs_from_ttf(ttf_path):
    print(f"  Extracting Arabic glyphs from: {os.path.basename(ttf_path)}...")
    tt = TTFont(ttf_path)
    cmap = tt.getBestCmap()
    units_per_em = tt['head'].unitsPerEm
    scale = 20480.0 / units_per_em
    glyph_set = tt.getGlyphSet()
    hmtx_table = tt['hmtx']

    arabic_codes = set()
    ranges = [
        (0x0600, 0x06FF),
        (0x0750, 0x077F),
        (0x08A0, 0x08FF),
        (0xFB50, 0xFDFF),
        (0xFE70, 0xFEFF)
    ]
    for start, end in ranges:
        for c in range(start, end + 1):
            if c in cmap:
                arabic_codes.add(c)

    arabic_glyph_cache = {}
    for code in sorted(arabic_codes):
        gname = cmap[code]
        if gname not in arabic_glyph_cache:
            # Use DecomposingRecordingPen to fully unpack composite glyphs (dots, accents, hamzas)
            pen = DecomposingRecordingPen(glyph_set)
            glyph_set[gname].draw(pen)
            shape_bytes = encode_glyph_shape(pen.value, scale)
            adv = int(round(hmtx_table[gname][0] * scale))
            adv = max(-32768, min(32767, adv))
            
            # Compute exact bounding box from decomposed Bézier outline points
            all_pts = []
            for op, args in pen.value:
                if op in ('moveTo', 'lineTo'):
                    all_pts.append(args[0])
                elif op == 'qCurveTo':
                    all_pts.extend(args)

            if all_pts:
                p_xmin = min(p[0] for p in all_pts)
                p_xmax = max(p[0] for p in all_pts)
                p_ymin = min(p[1] for p in all_pts)
                p_ymax = max(p[1] for p in all_pts)
                xmin = int(round(p_xmin * scale))
                xmax = int(round(p_xmax * scale))
                ymin = int(round(-p_ymax * scale))
                ymax = int(round(-p_ymin * scale))
            else:
                xmin, xmax, ymin, ymax = 0, 0, 0, 0
            rect_bytes = encode_rect(xmin, xmax, ymin, ymax)
            arabic_glyph_cache[gname] = (shape_bytes, adv, rect_bytes)

    return arabic_codes, cmap, arabic_glyph_cache

def patch_font_file(src_swf, dst_swf, font_weights_map):
    print(f"Reading base font SWF: {src_swf}")
    with open(src_swf, 'rb') as f:
        swf_bytes = f.read()

    sig = swf_bytes[:3]
    version = swf_bytes[3]
    payload = zlib.decompress(swf_bytes[8:]) if sig == b'CWS' else swf_bytes[8:]

    nbits = payload[0] >> 3
    pos = (5 + nbits * 4 + 7) // 8 + 4
    header_prefix = payload[:pos]

    # Pre-extract glyphs for each unique TTF
    extracted_ttf = {}
    for fid, ttf_p in font_weights_map.items():
        if ttf_p not in extracted_ttf:
            extracted_ttf[ttf_p] = extract_glyphs_from_ttf(ttf_p)

    tags = []
    p_read = pos
    while p_read < len(payload):
        tag_hdr = struct.unpack('<H', payload[p_read:p_read+2])[0]
        p_read += 2
        t_type = tag_hdr >> 6
        t_len = tag_hdr & 0x3f
        if t_len == 0x3f:
            t_len = struct.unpack('<I', payload[p_read:p_read+4])[0]
            p_read += 4
        t_data = payload[p_read:p_read+t_len]
        p_read += t_len
        tags.append((t_type, t_data))
        if t_type == 0:
            break

    new_tags = []
    glyphs_added = {}

    for t_type, t_data in tags:
        if t_type == 75: # DefineFont3
            parsed = parse_df3(t_data)
            fid = parsed['font_id']
            ttf_p = font_weights_map.get(fid)
            
            if ttf_p and ttf_p in extracted_ttf:
                arabic_codes, cmap, glyph_cache = extracted_ttf[ttf_p]
                existing_codes = set(parsed['codes'])
                codes_to_add = [c for c in sorted(arabic_codes) if c not in existing_codes]
                
                for code in codes_to_add:
                    gname = cmap[code]
                    shape_bytes, adv, rect_bytes = glyph_cache[gname]
                    parsed['codes'].append(code)
                    parsed['shapes'].append(shape_bytes)
                    if parsed['layout']:
                        parsed['layout']['advances'].append(adv)
                        parsed['layout']['bounds'].append(rect_bytes)
                
                glyphs_added[fid] = len(codes_to_add)
                print(f"  Injected {len(codes_to_add)} Arabic glyphs into Font {fid} ({parsed['name'].strip()}) using {os.path.basename(ttf_p)}")
            else:
                glyphs_added[fid] = 0

            repacked_data = pack_df3(parsed)
            new_tags.append((75, repacked_data))
            
        elif t_type == 73: # FontAlignZones
            font_id = struct.unpack('<H', t_data[:2])[0]
            num_added = glyphs_added.get(font_id, 0)
            patched_zone_data = bytearray(t_data)
            patched_zone_data += b'\x00\x00' * num_added
            new_tags.append((73, bytes(patched_zone_data)))
        else:
            new_tags.append((t_type, t_data))

    new_payload = bytearray(header_prefix)
    for t_type, t_data in new_tags:
        t_len = len(t_data)
        if t_len < 0x3f:
            tag_hdr = (t_type << 6) | t_len
            new_payload += struct.pack('<H', tag_hdr)
        else:
            tag_hdr = (t_type << 6) | 0x3f
            new_payload += struct.pack('<H', tag_hdr)
            new_payload += struct.pack('<I', t_len)
        new_payload += t_data

    uncompressed_len = len(new_payload) + 8
    compressed_body = zlib.compress(bytes(new_payload), level=9)
    out_swf = b'CWS' + bytes([version]) + struct.pack('<I', uncompressed_len) + compressed_body

    os.makedirs(os.path.dirname(dst_swf), exist_ok=True)
    with open(dst_swf, 'wb') as f:
        f.write(out_swf)
    print(f"Patched multi-weight font SWF saved: {dst_swf} ({len(out_swf)} bytes)")

if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.abspath(__file__))
    fonts_dir = os.path.join(base_dir, 'fonts')
    
    font_weights_map = {
        1: os.path.join(fonts_dir, 'NotoSansArabic-Medium.ttf'),     # BMG Author Medium (500)
        2: os.path.join(fonts_dir, 'NotoSansArabic-ExtraBold.ttf'),  # BMG Bespoke Sans Extrabold (800)
        3: os.path.join(fonts_dir, 'NotoSansArabic-SemiBold.ttf'),   # BMG Author Semibold (600)
        4: os.path.join(fonts_dir, 'NotoSansArabic-Bold.ttf'),       # BMG Author Bold (700)
        5: os.path.join(fonts_dir, 'NotoSansArabic-Bold.ttf'),       # BMG Bespoke Sans Bold (700)
    }

    src = r'D:\SteamLibrary\steamapps\common\Brawlhalla\fontData\Font_Latin.swf.original_backup'
    dst = os.path.join(base_dir, 'Font_Latin_Arabic.swf')
    patch_font_file(src, dst, font_weights_map)
