import re
import arabic_reshaper
from bidi.algorithm import get_display

reshaper_config = {
    'delete_harakat': False,
    'support_ligatures': True,
    'RIAL SIGN': True,
}
_reshaper = arabic_reshaper.ArabicReshaper(configuration=reshaper_config)

def is_arabic_char(c):
    code = ord(c)
    return (0x0600 <= code <= 0x06FF or
            0x0750 <= code <= 0x077F or
            0x08A0 <= code <= 0x08FF or
            0xFB50 <= code <= 0xFDFF or
            0xFE70 <= code <= 0xFEFF)

def has_arabic(text):
    if not text:
        return False
    return any(is_arabic_char(c) for c in text)

def format_arabic_text(text):
    """
    Reshapes Arabic letters into connected cursive forms and reorders them
    visually (BiDi) for left-to-right Flash text rendering, while strictly preserving:
    - Format placeholders ({0}, {1}, {player}, %s, %d, etc.)
    - Syntax tags (<message>, <font...>, </font>, etc.)
    - Multi-line structure (new-lines \n and \r\n)
    - Numbers and embedded Latin words/names
    """
    if not text or not has_arabic(text):
        return text

    has_crlf = '\r\n' in text
    lines = text.split('\r\n' if has_crlf else '\n')
    out_lines = []

    token_pat = re.compile(r'(\{[^}]+\}|<[^>]+>|%[0-9\.]*[sdfi]|<!--[^>]*-->)')

    for line in lines:
        if not has_arabic(line):
            out_lines.append(line)
            continue

        tokens = []
        def mask_token(m):
            idx = len(tokens)
            tokens.append(m.group(0))
            return f"\u200ePH{idx:02d}X\u200e"

        masked = token_pat.sub(mask_token, line)

        # 1. Reshape Arabic letters into connected cursive presentation forms
        reshaped = _reshaper.reshape(masked)

        # 2. Visual reordering for LTR rendering (Flash engine renders LTR character-by-character)
        # Using base_dir='R' ensures correct paragraph direction for Arabic sentences
        visual = get_display(reshaped, base_dir='R')

        # 3. Restore placeholders
        for idx, tok in enumerate(tokens):
            visual = visual.replace(f"\u200ePH{idx:02d}X\u200e", tok)
            visual = visual.replace(f"PH{idx:02d}X", tok)

        visual = visual.replace('\u200e', '').replace('\u200f', '')
        out_lines.append(visual)

    newline = '\r\n' if has_crlf else '\n'
    return newline.join(out_lines)
