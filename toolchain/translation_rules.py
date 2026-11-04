# -*- coding: utf-8 -*-
"""
Master Translation Engine for Brawlhalla Arabic Localization.
Aggregates modular translation dictionaries and applies structured semantic rules.
Zero tolerance for Frankenstein strings: unmapped sentences remain clean original English.
"""

import re
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from translations_legends import HERO_TITLES, STATS_AND_STANCES
from translations_modes import PLAYLIST_MAP, GAMEMODE_MAP, SCORING_MAP, ITEM_MAP
from translations_hints_errors import HINTS_MAP, ERRORS_MAP
from translations_cosmetics import COLOR_MAP, TRAIL_MAP, PODIUM_MAP, ENTITLEMENT_MAP
from translations_ui import UI_TRANSLATIONS
from translations_core_ui import CORE_UI_TRANSLATIONS
from translations_ui_master import UI_MASTER
from translations_ui_extended import UI_EXTENDED
from translations_missions import MISSION_EXACT_MAP
from translations_missions_full import MISSIONS_FULL
from translations_skins_store_full import SKINS_STORE_FULL
from translations_social_full import SOCIAL_FULL
from translations_lore_full import LORE_FULL
from translations_tiles_modes import TILES_MAP, CUSTOM_GAMES_MAP

# Load base glossary
glossary_path = os.path.join(os.path.dirname(__file__), 'glossary.json')
with open(glossary_path, 'r', encoding='utf-8') as f:
    glossary_data = json.load(f)

GLOSSARY = {}
for cat_name, cat_dict in glossary_data.get('Categories', {}).items():
    for k, v in cat_dict.items():
        GLOSSARY[k] = v

# Aggregate all exact key maps
MASTER_KEY_MAP = {}
MASTER_KEY_MAP.update(UI_TRANSLATIONS)
MASTER_KEY_MAP.update(CORE_UI_TRANSLATIONS)
MASTER_KEY_MAP.update(UI_MASTER)
MASTER_KEY_MAP.update(UI_EXTENDED)
MASTER_KEY_MAP.update(MISSION_EXACT_MAP)
MASTER_KEY_MAP.update(MISSIONS_FULL)
MASTER_KEY_MAP.update(SKINS_STORE_FULL)
MASTER_KEY_MAP.update(SOCIAL_FULL)
MASTER_KEY_MAP.update(LORE_FULL)
MASTER_KEY_MAP.update(TILES_MAP)
MASTER_KEY_MAP.update(CUSTOM_GAMES_MAP)
MASTER_KEY_MAP.update(HERO_TITLES)
MASTER_KEY_MAP.update(PLAYLIST_MAP)
MASTER_KEY_MAP.update(GAMEMODE_MAP)
MASTER_KEY_MAP.update(SCORING_MAP)
MASTER_KEY_MAP.update(ITEM_MAP)
MASTER_KEY_MAP.update(HINTS_MAP)
MASTER_KEY_MAP.update(ERRORS_MAP)
MASTER_KEY_MAP.update(COLOR_MAP)
MASTER_KEY_MAP.update(TRAIL_MAP)
MASTER_KEY_MAP.update(PODIUM_MAP)
MASTER_KEY_MAP.update(ENTITLEMENT_MAP)

# Add stats & stances to glossary
GLOSSARY.update(STATS_AND_STANCES)

# Add item names directly to glossary as well
for k, v in ITEM_MAP.items():
    eng_name = k.replace("ItemType_", "")
    GLOSSARY[v] = v # self-map
    # e.g., "Axe": "الفأس"
    # Find original english from MASTER_KEY_MAP if needed

# Proper Names to NEVER translate (Keep authentic identity)
PROPER_NAMES = {
    "Bödvar", "Cassidy", "Orion", "Lord Vraxx", "Gnash", "Queen Nai", "Hattori",
    "Sir Roland", "Scarlet", "Thatch", "Ada", "Sentinel", "Lucien", "Teros",
    "Brynn", "Asuri", "Barraza", "Ember", "Azoth", "Koji", "Ulgrim", "Diana",
    "Jhala", "Kor", "Wu Shang", "Val", "Ragnir", "Cross", "Mirage", "Nix",
    "Mordex", "Yumiko", "Artemis", "Caspian", "Sidra", "Xull", "Kaya", "Isaiah",
    "Jiro", "Lin Fei", "Zariel", "Rayman", "Dusk", "Fait", "Thor", "Petra",
    "Vector", "Volkov", "Onyx", "Jaeyun", "Mako", "Magyar", "Reno", "Munin",
    "Arcadia", "Ezio", "Tezca", "Thea", "Red Raptor", "Loki", "Seven", "Vivi",
    "Imugi", "King Zuva", "Priya", "Valhalla", "Asgard", "Fangwild", "Brawlhalla",
    "Mallhalla", "Steam", "Ubisoft", "Blue Mammoth Games"
}

# Weapon name mapping for regex patterns
WEAPON_NAME_MAP = {
    "Sword": "السيف",
    "Hammer": "المطرقة",
    "Blasters": "المسدسين",
    "Spear": "الرمح",
    "Rocket Lance": "الرمح الصاروخي",
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
    "Unarmed": "أعزل"
}

def translate_string(text, key=""):
    stripped = text.strip()
    if not stripped:
        return text

    # 1. Exact key match (Highest priority)
    if key in MASTER_KEY_MAP:
        return MASTER_KEY_MAP[key]

    # 2. Exact glossary match
    if stripped in GLOSSARY:
        return GLOSSARY[stripped]

    # 3. Clean punctuation match
    clean_punc = stripped.rstrip('.!?:;,')
    punc_suffix = stripped[len(clean_punc):]
    if clean_punc in GLOSSARY:
        return GLOSSARY[clean_punc] + punc_suffix

    # 4. Proper names protection
    if clean_punc in PROPER_NAMES:
        return stripped

    # 5. Numbered prefixes (Round, Level, Tier, Season, Page, Week)
    for prefix_en, prefix_ar in [
        ("Round", "الجولة"),
        ("Level", "المستوى"),
        ("Tier", "الدرجة"),
        ("Season", "الموسم"),
        ("Page", "الصفحة"),
        ("Week", "الأسبوع")
    ]:
        m = re.match(rf'^{prefix_en}\s+(\d+)$', stripped, re.IGNORECASE)
        if m:
            return f"{prefix_ar} {m.group(1)}"

    # 6. Best of X / First to X wins
    m_bo = re.match(r'^Best-of-(\d+)\s+Set$', stripped, re.IGNORECASE)
    if m_bo:
        return f"مباراة الأفضل من {m_bo.group(1)}"

    m_ft = re.match(r'^First\s+to\s+(\d+)\s+wins$', stripped, re.IGNORECASE)
    if m_ft:
        return f"أول من يحرز {m_ft.group(1)} انتصارات"

    # 7. Quest / Mission Regex Patterns
    # "Win {X} matches/games"
    m_win = re.match(r'^Win\s+(\d+)\s+(matches|games)$', stripped, re.IGNORECASE)
    if m_win:
        return f"فز في {m_win.group(1)} مباريات"

    # "Deal {X} damage with {Weapon}"
    m_dmg = re.match(r'^Deal\s+(\d+)\s+damage\s+with\s+(.+)$', stripped, re.IGNORECASE)
    if m_dmg:
        amt = m_dmg.group(1)
        wep = m_dmg.group(2).strip()
        wep_ar = WEAPON_NAME_MAP.get(wep, wep)
        return f"ألحق {amt} من الضرر باستخدام {wep_ar}"

    # "Get {X} KOs with {Weapon}"
    m_ko = re.match(r'^Get\s+(\d+)\s+KOs?\s+with\s+(.+)$', stripped, re.IGNORECASE)
    if m_ko:
        amt = m_ko.group(1)
        wep = m_ko.group(2).strip()
        wep_ar = WEAPON_NAME_MAP.get(wep, wep)
        return f"حقق {amt} ضربات قاضية باستخدام {wep_ar}"

    # "Play {X} matches with {Weapon}"
    m_play = re.match(r'^Play\s+(\d+)\s+matches\s+with\s+(.+)$', stripped, re.IGNORECASE)
    if m_play:
        amt = m_play.group(1)
        wep = m_play.group(2).strip()
        wep_ar = WEAPON_NAME_MAP.get(wep, wep)
        return f"العب {amt} مباريات باستخدام {wep_ar}"

    # "{Weapon} Legend wins"
    m_leg_win = re.match(r'^(.+)\s+Legend\s+wins$', stripped, re.IGNORECASE)
    if m_leg_win:
        wep = m_leg_win.group(1).strip()
        wep_ar = WEAPON_NAME_MAP.get(wep, wep)
        return f"انتصارات بأساطير {wep_ar}"

    # "{Weapon} KOs"
    m_wep_ko = re.match(r'^(.+)\s+KOs$', stripped, re.IGNORECASE)
    if m_wep_ko:
        wep = m_wep_ko.group(1).strip()
        wep_ar = WEAPON_NAME_MAP.get(wep, wep)
        return f"ضربات قاضية بـ {wep_ar}"

    # "Play matches as {Weapon} Legends. Wins count double!"
    m_double = re.match(r'^Play\s+matches\s+as\s+(.+)\s+Legends\.\s+Wins\s+count\s+double!$', stripped, re.IGNORECASE)
    if m_double:
        wep = m_double.group(1).strip()
        wep_ar = WEAPON_NAME_MAP.get(wep, wep)
        return f"العب مباريات بأساطير {wep_ar}. الانتصارات تُحسب مضاعفة!"

    # "KO opponents off the {direction} of the screen"
    for dir_en, dir_ar in [("top", "أعلى"), ("bottom", "أسفل"), ("left side", "يسار"), ("right side", "يمين")]:
        if stripped == f"KO opponents off the {dir_en} of the screen":
            return f"إقصاء الخصوم عبر {dir_ar} الشاشة"

    # 8. Weapon Skin Naming Template: "{Legend/Name} {Weapon}"
    # e.g., "Goldforged Sword" -> "سيف مصبوب في الذهب"
    for wep_en, wep_ar in WEAPON_NAME_MAP.items():
        if stripped.endswith(" " + wep_en) and len(stripped.split()) <= 4:
            prefix = stripped[:-len(wep_en)-1].strip()
            if prefix == "Goldforged":
                return f"{wep_ar} مصبوب في الذهب"
            elif prefix == "Skyforged":
                return f"{wep_ar} مصبوب في السماء"

    # Fallback to clean original text (STRICT: NO naive token chopping)
    return stripped
