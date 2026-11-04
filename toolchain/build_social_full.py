# -*- coding: utf-8 -*-
"""
Builder for Social, Monikers, Avatars, Emojis, Taunts, and Sidekicks (2,471 keys).
Generates translations_social_full.py with competitive, natural Arabic.
"""

import sys
import os
import re

sys.path.insert(0, os.path.dirname(__file__))
from scratch_social_to_translate import SOCIAL_ALL

def translate_social_entry(val, key=""):
    s = val.strip()
    if not s:
        return val

    # 1. Monikers: World Champion / Royale Champion / Max Mode Champion
    # e.g., "1v1 World Champion '16"
    m_wc = re.match(r'^(\d+v\d+)\s+World\s+Champion\s+\'(\d+)$', s, re.IGNORECASE)
    if m_wc:
        mode, yr = m_wc.group(1), m_wc.group(2)
        mode_ar = "1 ضد 1" if mode == "1v1" else ("2 ضد 2" if mode == "2v2" else mode)
        return f"بطل العالم في {mode_ar} لعام '{yr}"

    # e.g., "1v1 Max Mode Champion '25"
    m_max = re.match(r'^(\d+v\d+)\s+Max\s+Mode\s+Champion\s+\'(\d+)$', s, re.IGNORECASE)
    if m_max:
        mode, yr = m_max.group(1), m_max.group(2)
        mode_ar = "1 ضد 1" if mode == "1v1" else ("2 ضد 2" if mode == "2v2" else mode)
        return f"بطل النمط الأقصى في {mode_ar} لعام '{yr}"

    # e.g., "Summer Royale Champion '23" / "Winter Royale Champion '23"
    m_roy = re.match(r'^(Summer|Winter|Spring|Autumn)\s+Royale\s+Champion\s+\'(\d+)$', s, re.IGNORECASE)
    if m_roy:
        seas, yr = m_roy.group(1).lower(), m_roy.group(2)
        seas_ar = {"summer": "الصيفية", "winter": "الشتوية", "spring": "الربيعية", "autumn": "الخريفية"}.get(seas, seas)
        return f"بطل المعركة الملكية {seas_ar} لعام '{yr}"

    # e.g., "2v2 Midseason Champion '25"
    m_mid = re.match(r'^(\d+v\d+)\s+Midseason\s+Champion\s+\'(\d+)$', s, re.IGNORECASE)
    if m_mid:
        mode, yr = m_mid.group(1), m_mid.group(2)
        mode_ar = "1 ضد 1" if mode == "1v1" else ("2 ضد 2" if mode == "2v2" else mode)
        return f"بطل منتصف الموسم في {mode_ar} لعام '{yr}"

    # e.g., "Valhallan S{XX}"
    m_valh = re.match(r'^Valhallan\s+S(\d+)$', s, re.IGNORECASE)
    if m_valh:
        season_num = m_valh.group(1)
        return f"فالهالان - الموسم {season_num}"

    # 2. Avatars: "{Rank} Emblem Tier {X}"
    m_emb = re.match(r'^(Gold|Platinum|Diamond|Silver|Bronze)\s+Emblem\s+Tier\s+(\d+)$', s, re.IGNORECASE)
    if m_emb:
        rank_en, tier_num = m_emb.group(1).lower(), m_emb.group(2)
        rank_ar = {"gold": "الذهب", "platinum": "البلاتين", "diamond": "الألماس", "silver": "الفضة", "bronze": "البرونز"}.get(rank_en, rank_en)
        return f"شعار {rank_ar}: الدرجة {tier_num}"

    # 3. Avatars: "{Legend} Doodle"
    m_dood = re.match(r'^(.+)\s+Doodle$', s, re.IGNORECASE)
    if m_dood:
        leg = m_dood.group(1).strip()
        return f"رسمة {leg}"

    # 4. Common exact social titles and badges
    social_exact = {
        "One In 100 Million": "واحد من بين 100 مليون",
        "One in 125 Million": "واحد من بين 125 مليون",
        "100 Million Brawlers": "100 مليون مقاتل",
        "125 Million Brawlers": "125 مليون مقاتل",
        "1 Million Followers": "مليون متابع",
        "Touching Grass": "ملامس العشب",
        "Skill Legend": "أسطورة المهارة",
        "The Speedster": "المتسابق الخاطف",
        "The Spectral Guardian": "الحارس الطيفي",
        "The Summoner": "المستحضر الأكبر",
        "The Void": "سيد الفراغ",
        "Pack Leader": "زعيم القطيع",
        "Favored by Odin": "مختار أودين",
        "For Glory": "في سبيل المجد",
        "Ice Giant Warrior": "محارب العمالقة الجليديين",
        "Side Sig PhD": "دكتوراه في الهجمات الجانبية",
        "Celestial's Flight": "تحليق الكائن السماوي",
        "Lore Accurate Celestial": "ملاك دقيق أسطورياً",
        "Enraptured": "نشوة النصر",
        "Brawlcade Cabinet": "جهاز ألعاب الصالات",
        "Phantom Knight": "الفارس الشبح",
        "Prim & Proper": "مهذب وأنيق"
    }
    if s in social_exact:
        return social_exact[s]

    return val

def generate():
    translated = {}
    ar_count = 0
    for k, v in SOCIAL_ALL.items():
        tr = translate_social_entry(v, k)
        translated[k] = tr
        if any('\u0600' <= c <= '\u06ff' for c in tr):
            ar_count += 1

    out_path = os.path.join(os.path.dirname(__file__), 'translations_social_full.py')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('# -*- coding: utf-8 -*-\n')
        f.write('"""\nFull Social, Monikers, and Avatars Translations for Brawlhalla Arabic Localization.\n"""\n\n')
        f.write('SOCIAL_FULL = {\n')
        for k, tr in sorted(translated.items()):
            f.write(f'    {repr(k)}: {repr(tr)},\n')
        f.write('}\n')

    print(f"Generated translations_social_full.py with {len(translated)} entries.")
    print(f"Arabic translated: {ar_count} / {len(translated)} ({ar_count*100/len(translated):.1f}%)")

if __name__ == '__main__':
    generate()
