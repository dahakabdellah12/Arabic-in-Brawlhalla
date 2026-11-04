# -*- coding: utf-8 -*-
"""
Generator for Extended UI Translations (1,776 keys).
Creates translations_ui_extended.py with natural, competitive gaming Arabic.
"""

import sys
import os
import re

sys.path.insert(0, os.path.dirname(__file__))
from scratch_ui_to_translate import UI_REMAINING
from lexicon import COMBAT_LEXICON, STATS_LEXICON, WEAPON_LEXICON

# Dictionary of high-frequency UI terms and exact phrases
UI_EXACT_MAP = {
    # Single/short word UI elements
    "Emojis": "تعبيرات",
    "Back": "رجوع",
    "Default": "افتراضي",
    "Legend": "أسطورة",
    "Skin": "مظهر",
    "Battle Pass": "تذكرة المعركة",
    "Podium": "منصة التتويج",
    "Random": "عشوائي",
    "Select": "تحديد",
    "Sign In": "تسجيل الدخول",
    "Level": "المستوى",
    "Player": "لاعب",
    "Neutral": "محايد",
    "KOs": "ضربات قاضية",
    "Custom": "مخصص",
    "Recovery": "صعود تعافٍ",
    "Side Air": "ضربة هوائية جانبية",
    "Side Light": "ضربة خفيفة جانبية",
    "Sort": "ترتيب",
    "PURCHASES": "المشتريات",
    "views": "مشاهدة",
    "Side Signature": "هجوم خارق جانبي",
    "Insignia": "الشارة",
    "Power Cast Data": "بيانات تنفيذ الحركة",
    "I Agree": "أوافق",
    "Base Damage:": "الضرر الأساسي:",
    "Prev": "السابق",
    "Stock": "الأرواح",
    "Startup Frames": "إطارات بدء الحركة",
    "Down": "أسفل",
    "Page": "الصفحة",
    "Sort: Joined": "الترتيب: تاريخ الانضمام",
    "Sort: Level": "الترتيب: حسب المستوى",
    "Sort: Date": "الترتيب: حسب التاريخ",
    "Sort: A-Z": "الترتيب: أبجدياً",
    "Sort: Elo": "الترتيب: حسب التقييم",
    "Sort: XP": "الترتيب: نقاط الخبرة",
    "Sort: Activity": "الترتيب: حسب النشاط",
    "Sort: Name": "الترتيب: حسب الاسم",
    "Sort: Rank": "الترتيب: حسب الرتبة",
    "Sort: Wins": "الترتيب: حسب الانتصارات",
    
    # Months
    "Jan": "يناير",
    "Feb": "فبراير",
    "Mar": "مارس",
    "Apr": "أبريل",
    "May": "مايو",
    "Jun": "يونيو",
    "Jul": "يوليو",
    "Aug": "أغسطس",
    "Sep": "سبتمبر",
    "Oct": "أكتوبر",
    "Nov": "نوفمبر",
    "Dec": "ديسمبر",

    # Training & Fighting Controls
    "Air Attacks": "هجمات هوائية",
    "Ground Attacks": "هجمات أرضية",
    "Light Attacks": "هجمات خفيفة",
    "Signatures": "هجمات خارقة",
    "Down Air": "ضربة هوائية سفلية (DAir)",
    "Down Light": "ضربة خفيفة سفلية (DLight)",
    "Down Signature": "هجوم خارق سفلي (DSig)",
    "Ground Pound": "سحقة أرضية (GP)",
    "Neutral Air": "ضربة هوائية محايدة (NAir)",
    "Neutral Light": "ضربة خفيفة محايدة (NLight)",
    "Neutral Signature": "هجوم خارق محايد (NSig)",
    "D-Heavy": "ضربة ثقيلة سفلية",
    "N-Heavy": "ضربة ثقيلة محايدة",
    "S-Heavy": "ضربة ثقيلة جانبية",
    "Use Certain Attacks": "تقييد هجمات معينة",
    "Give Gadget": "منح أداة",
    "Give Weapon": "منح سلاح",
    "Evasive": "مراوغ",
    "Pushover": "سهل المنال",
    "Resume": "استئناف",
    "Attack Air": "هجوم هوائي",
    "Attack Heavy": "هجوم ثقيل",
    "Attack Light": "هجوم خفيف",
    "Jump": "قفز",
    "Dash": "اندفاع",
    "Backdash": "اندفاع للخلف",
    "Dash Jump": "قفزة الاندفاع",
    "Chain Dodge": "تفادٍ متسلسل",
    "Chase Dodge": "تفادي المطاردة",
    "Active Input": "إدخال نشط",
    "Gravity Cancel": "إلغاء الجاذبية",

    # PowersViewer / Frame Data
    "Active Frames": "إطارات النشاط",
    "Fixed Force:": "قوة دفع ثابتة:",
    "Cast Frame": "إطار التنفيذ",
    "Currently Active": "نشط حالياً",
    "Height:": "الارتفاع:",
    "Width:": "العرض:",
    "Hitbox Info": "معلومات صندوق الضرب (Hitbox)",
    "Hurtbox Info": "معلومات صندوق الإصابة (Hurtbox)",
    "Power Info": "معلومات الحركة",
    "Active Frames:": "إطارات النشاط:",
    "Cooldown:": "فترة التهدئة:",
    "Fixed Recovery:": "تعافٍ ثابت:",
    "Min Charge:": "الحد الأدنى للشحن:",
    "Recovery:": "التعافي:",
    "Startup Frames:": "إطارات بدء الحركة:",
    "Stun Time:": "زمن الصعق:",
    "Variable Force:": "قوة دفع متغيرة:",
    "No Current Power": "لا توجد حركة حالية",
    "Power Cast Timeline": "المخطط الزمني لتنفيذ الحركة",
    "Power ID:": "معرّف الحركة:",
    "X Offset:": "الإزاحة الأفقية X:",
    "Y Offset:": "الإزاحة الرأسية Y:",

    # Clan & Guilds
    "Games": "المباريات",
    "LEADERBOARD": "لوحة المتصدرين",
    "Members": "الأعضاء",
    "MESSAGE OF THE DAY": "رسالة اليوم",
    "PROGRESSION": "مستوى التقدم",
    "YOUR CONTRIBUTIONS": "مساهماتك",
    "About Guilds": "حول العشائر",
    "Guilds": "العشائر",
    "Guild": "العشيرة",
    "Leader": "القائد",
    "Officer": "المشرف",
    "Member": "عضو",
    "Recruit": "مستجد",
    "Promote": "ترقية",
    "Demote": "تخفيض الرتبة",
    "Kick": "طرد",
    "Leave Guild": "مغادرة العشيرة",
    "Disband Guild": "حل العشيرة",
    "Create Guild": "إنشاء عشيرة",
    "Guild Name": "اسم العشيرة",
    "Guild Tag": "شعار العشيرة",
    "Guild Level": "مستوى العشيرة",
    "Guild XP": "نقاط خبرة العشيرة",
    "Start Lobby": "بدء غرفة لعب",
    "Age": "العمر",
    "Avg. Elo": "متوسط التقييم",

    # Battle Pass
    "Next Rewards:": "المكافآت التالية:",
    "Light Path": "مسار النور",
    "Twilight Path": "مسار الشفق",
    "Dark Path": "مسار الظلام",
    "Past Path": "مسار الماضي",
    "Present Path": "مسار الحاضر",
    "Future Path": "مسار المستقبل",
    "Intro Path": "المسار التمهيدي",
    "Final Path": "المسار النهائي",
    "Arbiter Path": "مسار الحَكَم",
    "Justiciar Path": "مسار القاضي العادل",
    "Battle Pass Chest": "صندوق تذكرة المعركة",
    "NEW REWARD UNLOCKED!": "تم فتح مكافأة جديدة!",
    "You Unlocked Battle Pass Tiers": "لقد فتحت درجات جديدة في تذكرة المعركة",
    "Upgrade": "ترقية",
    "Claim All": "استلام الكل",
    "Claim Reward": "استلام المكافأة",
    "Battle Gems": "جواهر المعركة",
    "Weekly Missions": "المهمات الأسبوعية",
    "Daily Missions": "المهمات اليومية",

    # Store
    "View Bundle": "عرض الحزمة",
    "Store": "المتجر",
    "Purchase": "شراء",
    "Purchased": "تم الشراء",
    "Refund": "استرداد",
    "Refunds Left:": "الاستردادات المتبقية:",
    "Includes these weapon skins:": "يتضمن مظاهر الأسلحة التالية:",
    "Includes sidekick and animated weapon skins:": "يتضمن رفيقاً ومظاهر أسلحة متحركة:",
    "Includes emote and animated weapon skins:": "يتضمن تعبيراً ومظاهر أسلحة متحركة:",
    "Includes these additional items:": "يتضمن هذه العناصر الإضافية:",
    "Custom Signature FX": "مؤثرات بصرية خاصة للحركات الخارقة",
    "Dedicated Roster Spot": "مكان مخصص في قائمة المقاتلين",
    "New Pick Up Sound & Animation": "صوت وحركة التقاط جديدة كلياً",
    "Weapon & FX can Color Swap!": "يتغير لون السلاح والمؤثرات بتغير الألوان!",
    "Unique Cannon Sound FX": "مؤثرات صوتية فريدة للمدفع",
    "Unique Blasters Sound FX": "مؤثرات صوتية فريدة للمسدسين",
    "Animated Weapon Skins": "مظاهر أسلحة متحركة",

    # Hero Page / Stats
    "Damage Dealt": "الضرر الملحق",
    "Buy Skin": "شراء المظهر",
    "Games Played": "المباريات الملعوبة",
    "Rating": "التقييم",
    "Stats": "الإحصائيات",
    "Strength": "القوة",
    "Dexterity": "المهارة",
    "Defense": "الدفاع",
    "Speed": "السرعة",
    "Super Strength": "قوة فائقة",
    "Super Dexterity": "مهارة فائقة",
    "Super Defense": "دفاع فائق",
    "Super Speed": "سرعة فائقة",
    "Throws": "الرميات",
    "Time Held": "مدة حمل السلاح",
    "Total Damage": "إجمالي الضرر",
    "Total KOs": "إجمالي الضربات القاضية",
    "Total Legend Levels -": "إجمالي مستويات الأساطير -",
    "Unarmed": "قتال أعزل",
    "Unlock Legend": "فتح قفل الأسطورة",
    "Usage Rate": "معدل الاستخدام",
    "View in Battle Pass": "عرض في تذكرة المعركة",
    "Weapons": "الأسلحة",
    "Wins": "الانتصارات",
    "Overview": "نظرة عامة",
    "Lore": "القصة والتاريخ",
    "Career": "المسيرة القتالية",
    "Season": "الموسم",
    "Overall": "الإجمالي",

    # Tournament / Cups
    "Bracket:": "جدول البطولة:",
    "CONGRATULATIONS YOU GOT 3RD PLACE!": "تهانينا! حققت المركز الثالث!",
    "BEST SCORE:": "أفضل نتيجة:",
    "Homepage": "الصفحة الرئيسية",
    "CONGRATULATIONS!": "تهانينا الحارة!",
    "You placed FIRST in this tournament bracket!": "حققت المركز الأول في جدول البطولة هذا!",
    "You placed SECOND in this tournament bracket!": "حققت المركز الثاني في جدول البطولة هذا!",
    "You placed THIRD in this tournament bracket!": "حققت المركز الثالث في جدول البطولة هذا!",
    "You placed FOURTH in this tournament bracket!": "حققت المركز الرابع في جدول البطولة هذا!",
    "WELL PLAYED!": "لعب رائع!",
    "THANKS FOR PLAYING!": "شكراً لمشاركتك!",
    "Winners Round": "جولة الفائزين",
    "Elimination Round 1": "جولة الإقصاء الأولى",
    "Tournament begins in:": "تبدأ البطولة خلال:",

    # Inventory & Cross Progression
    "Cross Inventory": "المخزون المشترك",
    "Random Sidekick": "رفيق عشوائي",
    "Defeat Emote": "تعبير الهزيمة",
    "Manage Inventory": "إدارة المخزون",
    "Skirmishes": "المناوشات الكبرى",
    "Locked By Skirmish": "مقفل في المناوشة",
    "Refresh": "تحديث",
    
    # System Settings
    "Streamer Mode": "وضع البث",
    "Outdated Replays": "التسجيلات القديمة",
    "Keep": "احتفاظ",
    "Delete": "حذف",
    "Disabled": "معطل",
    "Enabled": "مفعل",
    "Performance": "الأداء",
    "Quality": "الجودة",
    "All": "الكل",
    "None": "لا شيء",
    "Close": "إغلاق",
    "Accept": "قبول",
    "Cancel": "إلغاء",
    "Confirm": "تأكيد",
    "Apply": "تطبيق",
    "Reset": "إعادة ضبط",
    "Save": "حفظ"
}

def translate_ui_entry(key, val):
    val_stripped = val.strip()
    if not val_stripped:
        return val

    # 1. Exact match in UI_EXACT_MAP
    if val_stripped in UI_EXACT_MAP:
        return UI_EXACT_MAP[val_stripped]

    # Clean punctuation match
    clean_punc = val_stripped.rstrip('.!?:;,')
    punc_suffix = val_stripped[len(clean_punc):]
    if clean_punc in UI_EXACT_MAP:
        return UI_EXACT_MAP[clean_punc] + punc_suffix

    # 2. Check legal / copyright texts -> Preserve verbatim
    if key.startswith('UI_PopUpLegal_') or '©' in val or 'All rights reserved' in val or 'All Rights Reserved' in val:
        return val

    # 3. Handle Sort: {X}
    if val_stripped.startswith('Sort: '):
        target = val_stripped.replace('Sort: ', '').strip()
        target_ar = UI_EXACT_MAP.get(target, target)
        return f"الترتيب: {target_ar}"

    # 4. Handle "You placed {X} in this tournament bracket!"
    m_cup = re.match(r'You placed (\w+) in this tournament bracket!', val_stripped, re.IGNORECASE)
    if m_cup:
        pos = m_cup.group(1).upper()
        pos_map = {
            "FIRST": "الأول", "SECOND": "الثاني", "THIRD": "الثالث", "FOURTH": "الرابع",
            "FIFTH": "الخامس", "SIXTH": "السادس", "SEVENTH": "السابع", "EIGHTH": "الثامن",
            "NINTH": "التاسع", "TENTH": "العاشر", "ELEVENTH": "الحادي عشر", "TWELFTH": "الثاني عشر",
            "THIRTEENTH": "الثالث عشر"
        }
        pos_ar = pos_map.get(pos, pos)
        return f"حققت المركز {pos_ar} في جدول البطولة هذا!"

    # 5. Handle Tooltips for PowersViewer
    if key.startswith('UI_PowersViewer_ToolTip_'):
        if key.endswith('_Title'):
            base = val_stripped
            return UI_EXACT_MAP.get(base, base)

    # 6. Fallback: if not mapped, return original text to avoid Frankenstein
    return val

def generate():
    translated = {}
    ar_count = 0
    for k, v in UI_REMAINING.items():
        tr = translate_ui_entry(k, v)
        translated[k] = tr
        if any('\u0600' <= c <= '\u06ff' for c in tr):
            ar_count += 1

    out_path = os.path.join(os.path.dirname(__file__), 'translations_ui_extended.py')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('# -*- coding: utf-8 -*-\n')
        f.write('"""\nExtended UI Translations for Brawlhalla Arabic Localization.\n"""\n\n')
        f.write('UI_EXTENDED = {\n')
        for k, tr in sorted(translated.items()):
            f.write(f'    {repr(k)}: {repr(tr)},\n')
        f.write('}\n')

    print(f"Generated translations_ui_extended.py with {len(translated)} entries.")
    print(f"Arabic translated: {ar_count} / {len(translated)} ({ar_count*100/len(translated):.1f}%)")

if __name__ == '__main__':
    generate()
