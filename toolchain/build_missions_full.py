# -*- coding: utf-8 -*-
"""
Builder for Full Missions, Quests, Guild Missions, and Lessons (771 keys).
Generates translations_missions_full.py with competitive, concise, natural Arabic.
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

STAT_MAP = {"Strength": "قوة", "Dexterity": "مهارة", "Defense": "دفاع", "Speed": "سرعة"}

def translate_mission_string(text, key=""):
    s = text.strip()
    if not s:
        return text

    # Common exact missions
    exact = {
        # Battle Pass Missions & Quests (concise single-line)
        "Perform Back Dashes": "اندفاع للخلف",
        "Get KOs with Gravity-Canceled Attacks": "ضربات بإلغاء الجاذبية",
        "KOs with different Weapons": "إقصاء بأسلحة مختلفة",
        "Random Legend wins": "انتصارات باختيار عشوائي",
        "Play matches as random Legends. Wins count double!": "العب بأساطير عشوائية (فوز مضاعف)",
        "Completionist": "المُنجز الكامل",
        "Perform Chase Dodges": "تفادٍ ملاحق",
        "Perform Dash-Jumps": "قفز مع اندفاع",
        "Perform Team Combos": "كومبو جماعي",
        "Perform True Combos": "كومبو مؤكد",
        "Punish Dodges": "معاقبة التفادي",
        "Disarm opponents": "نزع سلاح الخصوم",
        "Catch Gadgets thrown by opponents": "التقاط أدوات الخصوم",
        "Catch fresh Items before they hit the ground": "التقاط أدوات قبل سقوطها",
        "Win consecutive matches": "انتصارات متتالية",
        "Win matches in under 150 seconds": "فوز في أقل من 150 ثانية",
        "Win matches without getting KO'd more than once": "فوز بسقوط واحد على الأكثر",
        "Win rematches": "الفوز في جولات الإعادة",
        "Solo queue in Ranked 2v2": "دخول فردي في 2 ضد 2 مصنف",
        "Replace Daily Missions": "استبدال المهمات اليومية",
        "Win matches as members of the Valhallan Ladies Book Club": "فوز بأساطير نادي الكتاب",
        "Play matches as members of the Valhallan Ladies Book Club. Wins count double!": "العب بأساطير نادي الكتاب (فوز مضاعف)",
        "Win matches as Legends with ties to Batavia": "فوز بأساطير Batavia",
        "Play matches as Legends with ties to Batavia. Wins count double!": "العب بأساطير Batavia (فوز مضاعف)",
        "Win matches as Legends who saw a dragon": "فوز بأساطير رأوا تنيناً",
        "Win matches as Legends who trained with Lin Fei": "فوز بأساطير دربهم Lin Fei",
        "Win matches as Legends brought to Valhalla by Brynn": "فوز بأساطير جلبتهم Brynn",
        "Play matches as Legends brought to Valhalla by Brynn. Wins count double!": "العب بأساطير جلبتهم Brynn (فوز مضاعف)",
        "Win matches with Legends from Thera": "فوز بأساطير Thera",
        "Win matches as Asgardian Legends": "فوز بأساطير Asgard",
        "Play matches as Asgardian Legends. Wins count double!": "العب بأساطير Asgard (فوز مضاعف)",
        "Win matches while wearing a hat": "فوز بأساطير ترتدي قبعة",
        "Win matches with Legends that have the ability to change their form": "فوز بأساطير تغير شكلها",
        "Win matches with Legends who never read anything before arriving at Valhalla": "فوز بأساطير أمية",
        "Win matches with different Stance types": "فوز بوقفات قتالية مختلفة",
        "Win 1v1 matches while dealing less damage than you take": "فوز بضرر أقل من المتلقى",
        "Emote first": "استخدم تعبيراً أولاً",
        "Emote with opponents": "تعبيرات مع الخصوم",
        "Slide-charged Emotes": "تعبيرات مشحونة بالتزحلق",
        "Slide-charged Damage": "ضرر مشحون بالتزحلق",
        "Signature Attack damage": "ضرر بهجمات خارقة",
        "Light Attack damage": "ضرر بهجمات خفيفة",
        "Heavy Attack damage": "ضرر بهجمات ثقيلة",
        "Aerial Light Attack damage": "ضرر بهجوم هوائي خفيف",
        "Aerial Heavy Attack damage": "ضرر بهجوم هوائي ثقيل",
        "Aerial Attack KOs": "إقصاء بهجمات هوائية",
        "Unarmed damage": "ضرر بالقتال الأعزل",
        "Unarmed Damage": "ضرر بالقتال الأعزل",
        "Dodge Signature Attacks": "تفادي هجمات خارقة",
        "Dodge Aerial Attacks": "تفادي هجمات هوائية",
        "Dodge Grounded Light Attacks": "تفادي ضربات أرضية خفيفة",
        "Perform 4-hit Strings": "سلاسل من 4 ضربات",
        "KOs with different Ground Pound Attacks": "إقصاء بسحقات أرضية مختلفة",
        "KOs with different Recovery Attacks": "إقصاء بهجمات صعود مختلفة",
        "Gravity-canceled KOs with different Weapons": "إقصاء بـ GC بأسلحة مختلفة",
        "Gravity-canceled Damage": "ضرر بإلغاء الجاذبية",
        "Gravity-canceled Light Attack damage": "ضرر خفيف بإلغاء الجاذبية",
        "Gravity-canceled Unarmed Heavy Attack KOs": "إقصاء بـ GC بالقتال الأعزل",
        "Gravity-canceled Blasters Light Attack damage": "ضرر بالمسدسين بإلغاء الجاذبية",
        "Gravity-Canceled or Slide-Charged Side Signature KOs": "إقصاء بـ SSig مشحونة أو GC",
        "Gravity-Canceled or Slide-Charged Neutral Signature KOs": "إقصاء بـ NSig مشحونة أو GC",
        "Gravity-Canceled or Slide-Charged Down Signature KOs": "إقصاء بـ DSig مشحونة أو GC",
        "Perform Gravity-Canceled Side Signatures": "تنفيذ SSig بإلغاء الجاذبية",
        "Perform Gravity-Canceled Down Signatures": "تنفيذ DSig بإلغاء الجاذبية",
        "Perform Gravity-Canceled Side Light Attacks": "تنفيذ SLight بإلغاء الجاذبية",
        "Perform Gravity-Canceled Down Light Attacks": "تنفيذ DLight بإلغاء الجاذبية",
        "Gravity-canceled hits": "إصابات بإلغاء الجاذبية",
        "Hit opponents with Gravity-canceled attacks twice in a match": "إصابتان بـ GC في مباراة",
        "Hit opponents with Gravity-canceled attacks 3 times in a match": "3 إصابات بـ GC في مباراة",
        "Be gravity-canceling an Emote at the end of matches": "تعليق تعبير بـ GC بنهاية المباراة",
        "Dominate": "هيمنة كاملة",
        "Get hits on opponents within 4 seconds of each other without getting hit": "ضرب متتالٍ دون تلقي ضرر",
        "Win matches as Legends that have been used to win a BCX 1v1 Championship": "فوز بأساطير بطولة BCX 1v1",
        "Win matches as Legends that have been used to win a BCX 2v2 Championship": "فوز بأساطير بطولة BCX 2v2",
        "Wins as Legends that were used to finish top 8 in the 2025 BCX 1v1 Championship": "فوز بأساطير نهائي BCX 2025",
        "Wins as Legends that were used to finish top 6 in the 2025 BCX 2v2 Championship": "فوز بأساطير نهائي BCX 2025",
        "Win matches as different Legends that were used to win a 2021 BCX 1v1 Championship": "فوز بأساطير بطولة BCX 2021",
        "Win matches as different Legends that were used to win a 2021 BCX 2v2 Championship": "فوز بأساطير بطولة BCX 2021",
        "Win matches as Legends used to finish top 3 in 2022 BCX 1v1": "فوز بأساطير بطولة BCX 2022",
        "Win matches as Legends used to finish top 3 in 2022 BCX 2v2": "فوز بأساطير بطولة BCX 2022",
        "Win matches with the current Battle Pass Color Scheme": "فوز بألوان تذكرة المعركة",
        "Deal damage by Chase-Dodging into Attacks": "ضرر بالتفادي الملاحق",
        "Deal damage by Dash-Jumping into Attacks": "ضرر بقفز الاندفاع",
        "Dash-Jump into Gravity-Canceled Signature Attack hits": "إصابات خارقة بقفز الاندفاع",
        "Get KOs by Dash-Jumping into aerial Light Attacks": "إقصاء بقفز الاندفاع نحو هجوم هوائي",
        "Get KOs by Dash-Jumping into different aerial Light Attacks": "إقصاء بقفز الاندفاع بهوائيات خفيفة",
        "Hit twice with the same Spike Ball": "إصابتان بنفس كرة الأشواك",
        "Send or accept an invite from the Scoreboard to form a team": "إرسال أو قبول دعوة فريق",
        "Grab Weapons as they're being carried by your Sidekick": "التقاط السلاح من المساعد",
        "Get KOs using Weapons from the Shovel Knight Crossovers": "إقصاء بأسلحة Shovel Knight",
        "End matches in first place using the [Victory] Emote": "إنهاء المباراة بتعبير النصر",
        "Transfer ownership of Sticky Bombs to opponents": "تمرير القنبلة اللاصقة للخصم",
        "Sticky Bomb damage": "ضرر بالقنبلة اللاصقة",
        "Bounce Bouncy Bombs into opponents": "إصابة بقنبلة مرتدة",
        "Boomerang damage": "ضرر بالبوميرانغ",
        "Boomerang hits": "إصابات بالبوميرانغ",
        "Boomerang hits on the way back": "إصابات بالبوميرانغ أثناء العودة",
        "Boomerang hits on the way out": "إصابات بالبوميرانغ أثناء الانطلاق",
        "Deal damage with the Active Input version of Scythe Attacks": "ضرر بالإدخال النشط للمنجل",
        "Interrupt Attacks with Rocket Lance Attacks": "مقاطعة هجمات الخصم بالرمح الصاروخي",
        'Play matches as Legends with "bot" in their bot name. Wins count double!': "العب بأساطير تحوي bot (فوز مضاعف)",
        'Win matches as Legends with "bot" in their bot name': "فوز بأساطير تحوي bot",
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
        "Play matches in casual queues. Wins count double!": "العب مباريات في الطوابير الودية (فوز مضاعف)",
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
        "Get KOs with the Active Input version of Attacks": "إحراز ضربات قاضية بنسخة الإدخال النشط من الهجمات",
        "Hit opponents with airborne Pressure Mines": "إصابة الخصوم بألغام الضغط أثناء تحليقها في الهواء",
        "Perform all 6 standard Aerial Dodges in a match": "تنفيذ جميع أنواع التفادي الهوائي القياسية الستة في مباراة واحدة",
        "Gain Elo of any kind in Ranked matches": "كسب نقاط تقييم Elo في المباريات المصنفة"
    }
    if s in exact:
        return exact[s]

    # --- Structured Patterns (Concise & Single-Line) ---
    # {Weapon} Damage
    m = re.match(r'^(.+) Damage$', s, re.IGNORECASE)
    if m:
        wep = m.group(1).strip()
        wep_ar = WEAPON_MAP.get(wep, wep)
        return f"ضرر ب{wep_ar}"

    # {Weapon} Heavy Attack Damage
    m = re.match(r'^(.+) Heavy Attack Damage$', s, re.IGNORECASE)
    if m:
        wep = m.group(1).strip()
        wep_ar = WEAPON_MAP.get(wep, wep)
        return f"ضرر هجوم ثقيل ب{wep_ar}"

    # {Weapon} Light Attack Damage
    m = re.match(r'^(.+) Light Attack Damage$', s, re.IGNORECASE)
    if m:
        wep = m.group(1).strip()
        wep_ar = WEAPON_MAP.get(wep, wep)
        return f"ضرر هجوم خفيف ب{wep_ar}"

    # {Weapon} (Neutral|Down|Side) (Air|Light) Attack hits
    m = re.match(r'^(.+) (Neutral|Down|Side) (Air|Light) Attack hits$', s, re.IGNORECASE)
    if m:
        wep, pos, typ = m.group(1).strip(), m.group(2).strip(), m.group(3).strip()
        wep_ar = WEAPON_MAP.get(wep, wep)
        pos_code = {'Neutral': 'N', 'Down': 'D', 'Side': 'S'}.get(pos, pos)
        return f"إصابات {pos_code}{typ} ب{wep_ar}"

    # {Weapon} {Move} hits
    m = re.match(r'^(.+) (Down Air|Side Air|Neutral Air|Down Light|Side Light|Neutral Light) hits$', s, re.IGNORECASE)
    if m:
        wep, mv = m.group(1).strip(), m.group(2).strip()
        wep_ar = WEAPON_MAP.get(wep, wep)
        mv_code = {'Down Air': 'DAir', 'Side Air': 'SAir', 'Neutral Air': 'NAir', 'Down Light': 'DLight', 'Side Light': 'SLight', 'Neutral Light': 'NLight'}.get(mv, mv)
        return f"إصابات {mv_code} ب{wep_ar}"

    # Gravity-canceled (Neutral|Down|Side) Light hits
    m = re.match(r'^Gravity-canceled (Neutral|Down|Side) Light hits$', s, re.IGNORECASE)
    if m:
        pos = m.group(1).strip()
        pos_code = {'Neutral': 'N', 'Side': 'S', 'Down': 'D'}.get(pos, pos)
        return f"إصابات GC {pos_code}Light"

    # Get KOs with (Down Air|Side Air|Neutral Air|Down Light|Side Light|Neutral Light|Down Heavy|Side Heavy|Neutral Heavy) Attacks
    m = re.match(r'^Get KOs with (Down Air|Side Air|Neutral Air|Down Light|Side Light|Neutral Light|Down Heavy|Side Heavy|Neutral Heavy) Attacks$', s, re.IGNORECASE)
    if m:
        mv = m.group(1).strip()
        mv_code = {'Down Air': 'DAir', 'Side Air': 'SAir', 'Neutral Air': 'NAir', 'Down Light': 'DLight', 'Side Light': 'SLight', 'Neutral Light': 'NLight', 'Down Heavy': 'DHeavy', 'Side Heavy': 'SHeavy', 'Neutral Heavy': 'NHeavy'}.get(mv, mv)
        return f"إقصاء بضربة {mv_code}"

    # {Weapon} (Down|Side|Neutral) Air KOs
    m = re.match(r'^(.+) (Down|Side|Neutral) Air KOs$', s, re.IGNORECASE)
    if m:
        wep, pos = m.group(1).strip(), m.group(2).strip()
        wep_ar = WEAPON_MAP.get(wep, wep)
        pos_code = {'Neutral': 'N', 'Down': 'D', 'Side': 'S'}.get(pos, pos)
        return f"إقصاء {pos_code}Air بـ{wep_ar}"

    # Punish Dodges with {X}
    m = re.match(r'^Punish Dodges with (.+)$', s, re.IGNORECASE)
    if m:
        target = m.group(1).strip()
        if 'Side Signature' in target: return "معاقبة التفادي بـ SSig"
        if 'Down Signature' in target: return "معاقبة التفادي بـ DSig"
        if 'Neutral Signature' in target: return "معاقبة التفادي بـ NSig"
        if 'Signature' in target: return "معاقبة التفادي بهجوم خارق"
        if 'Light' in target: return "معاقبة التفادي بهجوم خفيف"
        if 'Heavy' in target: return "معاقبة التفادي بهجوم ثقيل"
        return "معاقبة التفادي"

    # Dodge {Move}
    m = re.match(r'^Dodge (Neutral|Side|Down) (Signatures?|Light Attacks?)$', s, re.IGNORECASE)
    if m:
        pos, typ = m.group(1).strip(), m.group(2).strip()
        pos_code = {'Neutral': 'N', 'Side': 'S', 'Down': 'D'}.get(pos, pos)
        typ_code = 'Sig' if 'Sig' in typ else 'Light'
        return f"تفادي هجمات {pos_code}{typ_code}"

    # Disarm opponents with {X}
    m = re.match(r'^Disarm opponents with (.+)$', s, re.IGNORECASE)
    if m:
        typ = m.group(1).strip()
        if 'Heavy' in typ: return "نزع سلاح بهجوم ثقيل"
        if 'Light' in typ: return "نزع سلاح بهجوم خفيف"
        return "نزع سلاح الخصوم"

    # Play matches as {Weapon} Legends. Wins count double!
    m = re.match(r'^Play matches as (.+) Legends\. Wins count double!$', s, re.IGNORECASE)
    if m:
        wep = m.group(1).strip()
        wep_ar = WEAPON_MAP.get(wep, wep)
        return f"العب بأساطير {wep_ar} (فوز مضاعف)"

    # Play matches with {N} or less/more {Stat}. Wins count double!
    m = re.match(r'^Play matches with (\d+) or (less|more) (\w+)\. Wins count double!$', s, re.IGNORECASE)
    if m:
        amt, dir_str, stat_name = m.group(1), m.group(2), m.group(3)
        stat_ar = STAT_MAP.get(stat_name, stat_name)
        comp = "أقل" if dir_str == "less" else "أكثر"
        return f"العب بأساطير {amt} {stat_ar} أو {comp} (فوز مضاعف)"

    # Win matches with {N} or less/more {Stat}
    m = re.match(r'^Win matches with (\d+) or (less|more) (\w+)$', s, re.IGNORECASE)
    if m:
        amt, dir_str, stat_name = m.group(1), m.group(2), m.group(3)
        stat_ar = STAT_MAP.get(stat_name, stat_name)
        comp = "أقل" if dir_str == "less" else "أكثر"
        return f"فوز بأساطير {amt} {stat_ar} أو {comp}"

    # Win matches with {N} or {N} {Stat}
    m = re.match(r'^Win matches with (\d+) or (\d+) (\w+)$', s, re.IGNORECASE)
    if m:
        n1, n2, stat_name = m.group(1), m.group(2), m.group(3)
        stat_ar = STAT_MAP.get(stat_name, stat_name)
        return f"فوز بأساطير {n1} أو {n2} {stat_ar}"

    # Win matches with a {N} in any stat
    m = re.match(r'^Win matches with a (\d+) in any stat$', s, re.IGNORECASE)
    if m:
        n = m.group(1)
        return f"فوز بأساطير بها {n} في خاصية"

    # (Down|Neutral|Side) (Light|Heavy|Air|Signature) (Attack )?damage
    m = re.match(r'^(Down|Neutral|Side) (Light|Heavy|Air|Signature) (Attack )?damage$', s, re.IGNORECASE)
    if m:
        pos, typ = m.group(1).strip(), m.group(2).strip()
        pos_code = {'Neutral': 'N', 'Side': 'S', 'Down': 'D'}.get(pos, pos)
        typ_code = {'Light': 'Light', 'Heavy': 'Heavy', 'Air': 'Air', 'Signature': 'Sig'}.get(typ, typ)
        return f"ضرر بهجوم {pos_code}{typ_code}"

    # Get KOs with (Down|Neutral|Side) (Light|Heavy|Air|Signature) Attacks
    m = re.match(r'^Get KOs with (Down|Neutral|Side) (Light|Heavy|Air|Signature) Attacks$', s, re.IGNORECASE)
    if m:
        pos, typ = m.group(1).strip(), m.group(2).strip()
        pos_code = {'Neutral': 'N', 'Side': 'S', 'Down': 'D'}.get(pos, pos)
        typ_code = {'Light': 'Light', 'Heavy': 'Heavy', 'Air': 'Air', 'Signature': 'Sig'}.get(typ, typ)
        return f"إقصاء بهجوم {pos_code}{typ_code}"

    # Perform 4-hit Strings with {Weapon}
    m = re.match(r'^Perform 4-hit Strings with (.+)$', s, re.IGNORECASE)
    if m:
        wep = m.group(1).strip()
        wep_ar = WEAPON_MAP.get(wep, wep)
        return f"سلاسل 4 ضربات بـ{wep_ar}"

    # Deal damage by Dash-Jumping into {Weapon} Attacks
    m = re.match(r'^Deal damage by Dash-Jumping into (.+) Attacks$', s, re.IGNORECASE)
    if m:
        wep = m.group(1).strip()
        wep_ar = WEAPON_MAP.get(wep, wep)
        return f"ضرر بقفز الاندفاع بـ{wep_ar}"

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
        return f"ألحق {amt} ضرر بسلاحين في مباراة"

    # Get {X} KOs by Dash-Jumping into Ground Pound Attacks in a match
    m = re.match(r'^Get (\d+) KOs? by Dash-Jumping into Ground Pound Attacks in a match$', s, re.IGNORECASE)
    if m:
        amt = m.group(1)
        return f"حقق {amt} ضربات قاضية بسحقة الاندفاع"

    # Get {X} KOs with Ground Pound Attacks in a match
    m = re.match(r'^Get (\d+) KOs? with Ground Pound Attacks in a match$', s, re.IGNORECASE)
    if m:
        amt = m.group(1)
        return f"حقق {amt} ضربات قاضية بالسحقة الأرضية"

    # Hit with {X} different Signature Attacks in a match
    m = re.match(r'^Hit with (\d+) different Signature Attacks in a match$', s, re.IGNORECASE)
    if m:
        amt = m.group(1)
        return f"أصب بـ {amt} هجمات خارقة مختلفة"

    # KO with {X} different Signature Attacks in a match
    m = re.match(r'^KO with (\d+) different Signature Attacks in a match$', s, re.IGNORECASE)
    if m:
        amt = m.group(1)
        return f"أقصِ بـ {amt} هجمات خارقة مختلفة"

    # KO opponents at least {X} more times than you get KO'd
    m = re.match(r"^KO opponents at least (\d+) more times than you get KO'd$", s, re.IGNORECASE)
    if m:
        amt = m.group(1)
        return f"أقصِ الخصوم بفارق {amt} ضربات قاضية"

    # Deal {X} damage in a single Stock / life
    m = re.match(r'^Deal (\d+) damage in a single (Stock|life)$', s, re.IGNORECASE)
    if m:
        amt = m.group(1)
        return f"ألحق {amt} ضرر بروح قتالية واحدة"

    # Deal {X} damage in a row without getting hit
    m = re.match(r'^Deal (\d+) damage in a row without getting hit$', s, re.IGNORECASE)
    if m:
        amt = m.group(1)
        return f"ألحق {amt} ضرر متتالٍ دون إصابة"

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
        return f"ألحق {amt} ضرر بـ {wep_ar}"

    # Get {X} KOs in a single life
    m = re.match(r'^Get (\d+) KOs? in a single life$', s, re.IGNORECASE)
    if m:
        amt = m.group(1)
        return f"حقق {amt} ضربات قاضية بروح واحدة"

    # Get {X} KOs in a match
    m = re.match(r'^Get (\d+) KOs? in a match$', s, re.IGNORECASE)
    if m:
        amt = m.group(1)
        return f"حقق {amt} ضربات قاضية في مباراة"

    # Get {X} KOs with {Weapon/Attack}
    m = re.match(r'^Get (\d+) KOs? with (.+)$', s, re.IGNORECASE)
    if m:
        amt, move = m.group(1), m.group(2).strip()
        move_ar = WEAPON_MAP.get(move, MOVE_MAP.get(move, move))
        return f"حقق {amt} ضربات قاضية بـ {move_ar}"

    # Play {X} matches with {Weapon}
    m = re.match(r'^Play (\d+) matches with (.+)$', s, re.IGNORECASE)
    if m:
        amt, wep = m.group(1), m.group(2).strip()
        wep_ar = WEAPON_MAP.get(wep, wep)
        return f"العب {amt} مباريات بـ {wep_ar}"

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
            return "أتقن سلسلة ضربات المنجل لتنفيذ معاقبة التفادي فور استخدام الخصم لمراوغته!"
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
