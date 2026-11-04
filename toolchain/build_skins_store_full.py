# -*- coding: utf-8 -*-
"""
Builder for Skins, Store descriptions, and Individual Legend Color Schemes (5,591 keys).
Generates translations_skins_store_full.py with competitive, natural Arabic.
"""

import sys
import os
import re

sys.path.insert(0, os.path.dirname(__file__))
from scratch_skins_to_translate import SKINS_ALL

COLOR_THEMES = {
    "Gala": "الحفل الملكي لـ {legend}",
    "Black": "أسود لـ {legend}",
    "Haunting": "الأطياف المرعبة لـ {legend}",
    "Guild Colors": "ألوان العشيرة لـ {legend}",
    "Winter Holiday": "عطلة الشتاء لـ {legend}",
    "Home Team": "فريق الديار لـ {legend}",
    "Verdant Bloom": "الربيع الزاهر لـ {legend}",
    "Goldforged": "مصبوب في الذهب لـ {legend}",
    "Crystalforged": "مصبوب في الكريستال لـ {legend}",
    "Skyforged": "مصبوب في السماء لـ {legend}",
    "Lucky Clover": "نبتة الحظ لـ {legend}",
    "Heatwave": "موجة الحر لـ {legend}",
    "Lovestruck": "سحر الحب لـ {legend}",
    "White": "أبيض لـ {legend}",
    "Sunset": "غروب الشمس لـ {legend}",
    "Gray": "رمادي لـ {legend}",
    "Brown": "بني لـ {legend}",
    "Orange": "برتقالي لـ {legend}",
    "Green": "أخضر لـ {legend}",
    "Teal": "أزرق مخضر لـ {legend}",
    "Cyan": "سماوي لـ {legend}",
    "Purple": "أرجواني لـ {legend}",
    "Pink": "وردي لـ {legend}",
    "Red": "أحمر لـ {legend}",
    "Blue": "أزرق لـ {legend}",
    "Yellow": "أصفر لـ {legend}"
}

WEAPONS_MAP = {
    "Sword": "السيف",
    "Hammer": "المطرقة",
    "Blasters": "المسدسين",
    "Spear": "الرمح",
    "Rocket Lance": "الرمح الصاروخي",
    "Lance": "الرمح الصاروخي",
    "Katars": "الخناجر",
    "Bow": "القوس",
    "Axe": "الفأس",
    "Gauntlets": "القفازات",
    "Scythe": "المنجل",
    "Cannon": "المدفع",
    "Orb": "الكرة السحرية",
    "Greatsword": "السيف الضخم",
    "Battle Boots": "أحذية القتال",
    "Boots": "أحذية القتال",
    "Chakram": "الشاكرام"
}

def translate_skin_or_store(val, key=""):
    s = val.strip()
    if not s:
        return val

    # 1. Legend Color Schemes: "{Legend} {ColorName}"
    if 'ColorSchemeType_' in key:
        for theme_en, theme_ar_template in COLOR_THEMES.items():
            if s.endswith(" " + theme_en):
                legend = s[:-len(theme_en)-1].strip()
                return theme_ar_template.format(legend=legend)

    # 2. Store: "The flag of {Country}."
    m_flag = re.match(r'^The flag of (.+)\.?$', s, re.IGNORECASE)
    if m_flag:
        country = m_flag.group(1).rstrip('.')
        return f"علم {country}."

    # 3. Store: "Adorable {Name} doodle."
    m_doodle = re.match(r'^Adorable (.+) doodle\.?$', s, re.IGNORECASE)
    if m_doodle:
        name = m_doodle.group(1).strip()
        return f"رسمة {name} اللطيفة."

    # 4. Weapon Skins: "Goldforged {Weapon}", "Skyforged {Weapon}", etc.
    for wep_en, wep_ar in WEAPONS_MAP.items():
        if s.endswith(" " + wep_en) or s == wep_en:
            if s == wep_en:
                return wep_ar
            prefix = s[:-len(wep_en)-1].strip()
            if prefix == "Goldforged":
                return f"{wep_ar} مصبوب في الذهب"
            elif prefix == "Skyforged":
                return f"{wep_ar} مصبوب في السماء"
            elif prefix == "Crystalforged":
                return f"{wep_ar} مصبوب في الكريستال"
            elif prefix == "Hardlight":
                return f"{wep_ar} الضوء الصلب"
            elif prefix == "Darkheart":
                return f"{wep_ar} القلب المظلم"
            elif prefix == "Asgardian":
                return f"{wep_ar} أزغارد"
            elif prefix == "Metadev":
                return f"{wep_ar} مطوري اللعبة (Metadev)"
            elif prefix == "Charged":
                return f"{wep_ar} المشحون بالطاقة"

    # 5. Common Store Descriptions
    store_exact = {
        "Do you fight for your friends? Show it!": "هل تقاتل دفاعاً عن أصدقائك؟ أظهر ذلك بفخر!",
        "The waves are my home.": "الأمواج هي موطني وملاذي.",
        "Unlock your full potential.": "أطلق العنان لكامل قوتك الكامنة.",
        "The last thing you see before going under.": "آخر ما تراه قبل أن تغرق في الأعماق.",
        "Replaces the Podium your Legend stands on. Equip from your Inventory.": "يستبدل المنصة التي تقف عليها أسطورتك. يمكنك تجهيزها من المخزون.",
        "Replaces the SpawnBot that delivers you to battle. Equip from your Inventory.": "يستبدل الرفيق الآلي الذي يوصلك إلى ساحة المعركة. يمكنك تجهيزه من المخزون.",
        "Equip from your Inventory.": "يمكنك تجهيزه من المخزون الخاص بك.",
        "Available for a limited time!": "متاح لفترة محدودة فقط!",
        "Special event item!": "عنصر فعالية خاص ونادر!",
        "Thanks for playing Brawlhalla!": "شكراً لك على لعب Brawlhalla!"
    }
    if s in store_exact:
        return store_exact[s]

    return val

def generate():
    translated = {}
    ar_count = 0
    for k, v in SKINS_ALL.items():
        tr = translate_skin_or_store(v, k)
        translated[k] = tr
        if any('\u0600' <= c <= '\u06ff' for c in tr):
            ar_count += 1

    out_path = os.path.join(os.path.dirname(__file__), 'translations_skins_store_full.py')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('# -*- coding: utf-8 -*-\n')
        f.write('"""\nFull Skins, Store, and Color Scheme Translations for Brawlhalla Arabic Localization.\n"""\n\n')
        f.write('SKINS_STORE_FULL = {\n')
        for k, tr in sorted(translated.items()):
            f.write(f'    {repr(k)}: {repr(tr)},\n')
        f.write('}\n')

    print(f"Generated translations_skins_store_full.py with {len(translated)} entries.")
    print(f"Arabic translated: {ar_count} / {len(translated)} ({ar_count*100/len(translated):.1f}%)")

if __name__ == '__main__':
    generate()
