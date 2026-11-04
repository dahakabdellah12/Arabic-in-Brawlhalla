# -*- coding: utf-8 -*-
"""
Builder for Full Missions, Quests, Guild Missions, and Lessons (771 keys).
Generates translations_missions_full.py with competitive, natural Arabic.
"""

import sys
import os
import re

sys.path.insert(0, os.path.dirname(__file__))
from scratch_missions_to_translate import MISSIONS_ALL

WEAPON_MAP = {
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
    "Chakram": "الشاكرام",
    "Unarmed": "القتال الأعزل"
}

MOVE_MAP = {
    "Down Air": "ضربة هوائية سفلية (DAir)",
    "Down Light": "ضربة خفيفة سفلية (DLight)",
    "Down Signature": "هجوم خارق سفلي (DSig)",
    "Neutral Air": "ضربة هوائية محايدة (NAir)",
    "Neutral Light": "ضربة خفيفة محايدة (NLight)",
    "Neutral Signature": "هجوم خارق محايد (NSig)",
    "Side Air": "ضربة هوائية جانبية (SAir)",
    "Side Light": "ضربة خفيفة جانبية (SLight)",
    "Side Signature": "هجوم خارق جانبي (SSig)",
    "Ground Pound": "سحقة أرضية (GP)",
    "Recovery": "صعود تعافٍ (Rec)",
    "Gravity Cancel": "إلغاء الجاذبية",
    "Slide-Charged Heavy Attacks": "هجمات ثقيلة مشحونة أثناء التزحلق",
    "Slide-Charged": "مشحونة أثناء التزحلق",
    "Active Input": "الإدخال النشط"
}

def translate_mission_string(text, key=""):
    s = text.strip()
    if not s:
        return text

    # Common exact missions
    exact = {
        "Finish all Event Daily Missions": "أكمل جميع المهمات اليومية للفعالية",
        "Free-for-All top two": "المركبان الأولان في قتال حر للجميع",
        "Free-for-All matches": "مباريات قتال حر للجميع",
        "Ranked 3v3 matches": "مباريات 3 ضد 3 مصنفة",
        "Ranked 2v2 wins": "انتصارات في 2 ضد 2 مصنف",
        "Ranked 2v2 matches": "مباريات 2 ضد 2 مصنفة",
        "Ranked 1v1 wins": "انتصارات في 1 ضد 1 مصنف",
        "Ranked 1v1 matches": "مباريات 1 ضد 1 مصنفة",
        "Win matches in casual queues": "الفوز بمباريات في الطوابير الودية",
        "Play matches in casual queues": "العب مباريات في الطوابير الودية",
        "Play matches in casual queues. Wins count double!": "العب مباريات في الطوابير الودية. الانتصارات تُحسب مضاعفة!",
        "Complete all Daily Missions": "أكمل جميع المهمات اليومية",
        "Reach Diamond in Ranked 1v1": "الوصول إلى رتبة الألماس في 1 ضد 1 مصنف",
        "Reach Diamond in Ranked 2v2": "الوصول إلى رتبة الألماس في 2 ضد 2 مصنف",
        "Reach Diamond in Ranked 3v3": "الوصول إلى رتبة الألماس في 3 ضد 3 مصنف",
        "Reach Platinum in Ranked 1v1": "الوصول إلى رتبة البلاتين في 1 ضد 1 مصنف",
        "Reach Platinum in Ranked 2v2": "الوصول إلى رتبة البلاتين في 2 ضد 2 مصنف",
        "Reach Platinum in Ranked 3v3": "الوصول إلى رتبة البلاتين في 3 ضد 3 مصنف",
        "Reach Gold in Ranked 1v1": "الوصول إلى رتبة الذهب في 1 ضد 1 مصنف",
        "Reach Gold in Ranked 2v2": "الوصول إلى رتبة الذهب في 2 ضد 2 مصنف",
        "Reach Gold in Ranked 3v3": "الوصول إلى رتبة الذهب في 3 ضد 3 مصنف",
        "Ranked 2v2 Matches with Guildmates": "مباريات 2 ضد 2 مصنفة مع أعضاء العشيرة",
        "Ranked 3v3 Matches with Guildmates": "مباريات 3 ضد 3 مصنفة مع أعضاء العشيرة",
        "Kung Foot Games": "مباريات كونغ فوت",
        "Gain XP": "كسب نقاط الخبرة",
        "Play 1v1 Ranked Games": "لعب مباريات 1 ضد 1 مصنفة",
        "Play 2v2 Friendly Games": "لعب مباريات 2 ضد 2 ودية",
        "Play 2v2 Ranked Games": "لعب مباريات 2 ضد 2 مصنفة",
        "Win Guild Battles": "الفوز في معارك العشائر",
        "Horde Mode Waves": "موجات نمط الحشود",
        "Play Brawlball Games": "لعب مباريات كرة الشجار",
        "Play Crew Battle Games": "لعب مباريات معارك الفرق",
        "Play Custom Games": "لعب مباريات مخصصة",
        "Play Free-For-All Games": "لعب مباريات قتال حر للجميع",
        "Any online games count.": "أي مباريات عبر الإنترنت تُحسب في التقدم.",
        "Any online games count. Reaching higher waves will count toward future missions which require it.": "أي مباريات عبر الإنترنت تُحسب في التقدم. بلوغ موجات أعلى يُحسب للمهمات المستقبلية.",
        "Must play on the Nightmare Horde map. Any online games count.": "يجب اللعب في خريطة كابوس الحشود. أي مباريات عبر الإنترنت تُحسب في التقدم.",
        "Or win a match at Diamond or above": "أو الفوز في مباراة برتبة الألماس أو أعلى",
        "Or win a match at Platinum or above": "أو الفوز في مباراة برتبة البلاتين أو أعلى",
        "Or win a match at Gold or above": "أو الفوز في مباراة برتبة الذهب أو أعلى",
        "Crew Battle Games": "مباريات معارك الفرق",
        "Brawlball Games": "مباريات كرة الشجار",
        "Brawl of the Week Wins": "انتصارات في معركة الأسبوع",
        "Hit opponents with Slide-Charged Heavy Attacks": "أصب الخصوم بهجمات ثقيلة مشحونة أثناء التزحلق",
        "Down Air hits": "إصابات بضربة هوائية سفلية (DAir)",
        "Dash-Jump Ground Pound KOs": "ضربات قاضية بسحقة أرضية مع قفزة الاندفاع",
        "Unarmed KOs": "ضربات قاضية بالقتال الأعزل",
        "FirstStep": "الخطوة الأولى",
        "ThirdStep": "الخطوة الثالثة",
        "Dash Jumping": "قفزة الاندفاع",
        "Dodge Attacks": "تفادي الهجمات",
        "Win 1v1 matches": "الفوز في مباريات 1 ضد 1",
        "Win 2v2 matches": "الفوز في مباريات 2 ضد 2",
        "Lose 1v1 matches": "خوض مباريات 1 ضد 1 حتى النهاية",
        "Hit opponents 3 times while airborne": "إصابة الخصوم 3 مرات أثناء التحليق في الهواء",
        "Pick up 3 Gadgets in a single match": "التقاط 3 أدوات في مباراة واحدة",
        "Deal damage with the Active Input version of Attacks": "إلحاق ضرر بنسخة الإدخال النشط من الهجمات",
        "Get 4 hits with the same Boomerang": "إصابة الخصوم 4 مرات بنفس البوميرانغ",
        "Perform 4-hit Strings": "تنفيذ سلاسل ضربات من 4 إصابات متتالية",
        "Aerial Heavy Attack damage": "ضرر بالهجمات الهوائية الثقيلة",
        "Aerial Light Attack damage": "ضرر بالهجمات الهوائية الخفيفة",
        "Get KOs with the Active Input version of Attacks": "إحراز ضربات قاضية بنسخة الإدخال النشط من الهجمات",
        "Hit opponents with airborne Pressure Mines": "إصابة الخصوم بألغام الضغط أثناء تحليقها في الهواء",
        "Perform all 6 standard Aerial Dodges in a match": "تنفيذ جميع أنواع التفادي الهوائي القياسية الستة في مباراة واحدة",
        "Gain Elo of any kind in Ranked matches": "كسب نقاط تقييم Elo في المباريات المصنفة"
    }
    if s in exact:
        return exact[s]

    # Reach Wave {N} in {Mode}
    m = re.match(r'^Reach Wave (\d+) in (.+)$', s, re.IGNORECASE)
    if m:
        wave, mode = m.group(1), m.group(2).strip()
        mode_ar = "نمط الحشود" if "Horde" in mode else ("كابوس الحشود" if "Nightmare" in mode else mode)
        return f"الوصول إلى الموجة {wave} في {mode_ar}"

    # Deal {X} damage each with 2 Weapons in a match
    m = re.match(r'^Deal (\d+) damage each with 2 Weapons in a match$', s, re.IGNORECASE)
    if m:
        amt = m.group(1)
        return f"ألحق {amt} من الضرر بسلاحين مختلفين في مباراة واحدة"

    # Get {X} KOs by Dash-Jumping into Ground Pound Attacks in a match
    m = re.match(r'^Get (\d+) KOs? by Dash-Jumping into Ground Pound Attacks in a match$', s, re.IGNORECASE)
    if m:
        amt = m.group(1)
        return f"حقق {amt} ضربات قاضية بقفزة الاندفاع نحو سحقة أرضية في مباراة واحدة"

    # Get {X} KOs with Ground Pound Attacks in a match
    m = re.match(r'^Get (\d+) KOs? with Ground Pound Attacks in a match$', s, re.IGNORECASE)
    if m:
        amt = m.group(1)
        return f"حقق {amt} ضربات قاضية بهجمات السحقة الأرضية في مباراة واحدة"

    # Hit with {X} different Signature Attacks in a match
    m = re.match(r'^Hit with (\d+) different Signature Attacks in a match$', s, re.IGNORECASE)
    if m:
        amt = m.group(1)
        return f"أصب بهجمات خارقة مختلفة لـ {amt} أساطير في مباراة واحدة"

    # KO with {X} different Signature Attacks in a match
    m = re.match(r'^KO with (\d+) different Signature Attacks in a match$', s, re.IGNORECASE)
    if m:
        amt = m.group(1)
        return f"أقصِ الخصوم بـ {amt} هجمات خارقة مختلفة في مباراة واحدة"

    # KO opponents at least {X} more times than you get KO'd
    m = re.match(r"^KO opponents at least (\d+) more times than you get KO'd$", s, re.IGNORECASE)
    if m:
        amt = m.group(1)
        return f"أقصِ الخصوم بفارق {amt} ضربات قاضية على الأقل عن عدد مرات إقصائك"

    # Deal {X} damage in a single Stock / life
    m = re.match(r'^Deal (\d+) damage in a single (Stock|life)$', s, re.IGNORECASE)
    if m:
        amt = m.group(1)
        return f"ألحق {amt} من الضرر خلال روح قتالية واحدة"

    # Deal {X} damage in a row without getting hit
    m = re.match(r'^Deal (\d+) damage in a row without getting hit$', s, re.IGNORECASE)
    if m:
        amt = m.group(1)
        return f"ألحق {amt} من الضرر على التوالي دون تلقي أي ضربة"

    # Deal {X} damage in a match
    m = re.match(r'^Deal (\d+) damage in a match$', s, re.IGNORECASE)
    if m:
        amt = m.group(1)
        return f"ألحق {amt} من الضرر في مباراة واحدة"

    # Deal {X} damage with {Weapon}
    m = re.match(r'^Deal (\d+) damage with (.+)$', s, re.IGNORECASE)
    if m:
        amt, wep = m.group(1), m.group(2).strip()
        wep_ar = WEAPON_MAP.get(wep, wep)
        return f"ألحق {amt} من الضرر باستخدام {wep_ar}"

    # Get {X} KOs in a single life
    m = re.match(r'^Get (\d+) KOs? in a single life$', s, re.IGNORECASE)
    if m:
        amt = m.group(1)
        return f"حقق {amt} ضربات قاضية خلال روح قتالية واحدة"

    # Get {X} KOs in a match
    m = re.match(r'^Get (\d+) KOs? in a match$', s, re.IGNORECASE)
    if m:
        amt = m.group(1)
        return f"حقق {amt} ضربات قاضية في مباراة واحدة"

    # Get {X} KOs with {Weapon/Attack}
    m = re.match(r'^Get (\d+) KOs? with (.+)$', s, re.IGNORECASE)
    if m:
        amt, move = m.group(1), m.group(2).strip()
        move_ar = WEAPON_MAP.get(move, MOVE_MAP.get(move, move))
        return f"حقق {amt} ضربات قاضية باستخدام {move_ar}"

    # Play {X} matches with {Weapon}
    m = re.match(r'^Play (\d+) matches with (.+)$', s, re.IGNORECASE)
    if m:
        amt, wep = m.group(1), m.group(2).strip()
        wep_ar = WEAPON_MAP.get(wep, wep)
        return f"العب {amt} مباريات باستخدام {wep_ar}"

    # {Weapon} Legend wins
    m = re.match(r'^(.+) Legend wins$', s, re.IGNORECASE)
    if m:
        wep = m.group(1).strip()
        wep_ar = WEAPON_MAP.get(wep, wep)
        return f"انتصارات بأساطير {wep_ar}"

    # {Weapon} KOs
    m = re.match(r'^(.+) KOs$', s, re.IGNORECASE)
    if m:
        wep = m.group(1).strip()
        wep_ar = WEAPON_MAP.get(wep, wep)
        return f"ضربات قاضية بـ {wep_ar}"

    # Play matches with {N} or less {Stat}. Wins count double!
    m = re.match(r'^Play matches with (\d+) or less (\w+)\. Wins count double!$', s, re.IGNORECASE)
    if m:
        stat_amt, stat_name = m.group(1), m.group(2)
        stat_map = {"Strength": "قوة", "Dexterity": "مهارة", "Defense": "دفاع", "Speed": "سرعة"}
        stat_ar = stat_map.get(stat_name, stat_name)
        return f"العب مباريات بأساطير ذات {stat_amt} {stat_ar} أو أقل. الانتصارات تُحسب مضاعفة!"

    # Play matches as {Weapon} Legends. Wins count double!
    m = re.match(r'^Play matches as (.+) Legends\. Wins count double!$', s, re.IGNORECASE)
    if m:
        wep = m.group(1).strip()
        wep_ar = WEAPON_MAP.get(wep, wep)
        return f"العب مباريات بأساطير {wep_ar}. الانتصارات تُحسب مضاعفة!"

    # KO opponents off the {direction} of the screen
    for dir_en, dir_ar in [("top", "أعلى"), ("bottom", "أسفل"), ("left side", "يسار"), ("right side", "يمين")]:
        if s == f"KO opponents off the {dir_en} of the screen":
            return f"إقصاء الخصوم عبر {dir_ar} الشاشة"

    # Lessons descriptions
    if key.startswith("LessonType_Desc_"):
        if "Sword" in s and "combo" in s:
            return "تعلم كومبو مؤكد وسهل التنفيذ بالسيف لإقصاء الخصم بضربة قاضية!"
        elif "Spear" in s and "combo" in s:
            return "الكومبو الأساسي والأهم لتعلمه واستخدامه باحتراف مع الرمح!"
        elif "Axe" in s and "combo" in s:
            return "تعلم هذا الكومبو الجوهري للفأس الفعال ضد الخصوم عند انخفاض الضرر."
        elif "Orb" in s and "combo" in s:
            return "كومبو عالي الضرر ومؤكد للكرة السحرية فعال حتى 60 من الضرر."
        elif "Scythe" in s:
            return "أتقن سلسلة ضربات المجل لتنفيذ معاقبة التفادي فور استخدام الخصم لمراوغته!"
        elif "Unarmed" in s:
            return "أساسيات القتال الأعزل: تعلم الكومبوهات الأساسية لتطوير مستواك القتالي دون سلاح!"
        elif "Recovering" in s or "recovering" in s:
            return "تحدي العودة إلى الحلبة! استخدم قفزاتك وصعود التعافي بذكاء للوصول بأمان."
        elif "Gravity Cancel" in s:
            return "أتقن تقنية إلغاء الجاذبية (Gravity Cancel) لتنفيذ حركات أرضية أثناء التحليق في الهواء!"

    return text

def generate():
    translated = {}
    ar_count = 0
    for k, v in MISSIONS_ALL.items():
        tr = translate_mission_string(v, k)
        translated[k] = tr
        if any('\u0600' <= c <= '\u06ff' for c in tr):
            ar_count += 1

    out_path = os.path.join(os.path.dirname(__file__), 'translations_missions_full.py')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('# -*- coding: utf-8 -*-\n')
        f.write('"""\nFull Missions, Quests, Guild Missions, and Lessons for Brawlhalla Arabic Localization.\n"""\n\n')
        f.write('MISSIONS_FULL = {\n')
        for k, tr in sorted(translated.items()):
            f.write(f'    {repr(k)}: {repr(tr)},\n')
        f.write('}\n')

    print(f"Generated translations_missions_full.py with {len(translated)} entries.")
    print(f"Arabic translated: {ar_count} / {len(translated)} ({ar_count*100/len(translated):.1f}%)")

if __name__ == '__main__':
    generate()
