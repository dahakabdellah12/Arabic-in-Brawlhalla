# -*- coding: utf-8 -*-
"""
Updater for all targeted UI keys and mission keys.
Ensures every key from user's screenshots has concise, non-wrapping, authentic Arabic translation.
"""
import sys
import os

TARGET_UPDATES = {
    # --- Rejoin Dialog ---
    "UI_Rejoin_Header": "المباراة جارية",
    "UI_Rejoin_RejoinGame": "العودة للمباراة",

    # --- Match End Podium Stats (super concise to prevent column cutoff) ---
    "UI_CharacterSlotScoreboard_Score": "النقاط",
    "UI_CharacterSlotScoreboard_Kills": "الإقصاء",
    "UI_CharacterSlotScoreboard_Deaths": "السقوط",
    "UI_CharacterSlotScoreboard_Accidents": "سقوط ذاتي",
    "UI_CharacterSlotScoreboard_DamageDone": "ضرر ملحق",
    "UI_CharacterSlotScoreboard_DamageTaken": "ضرر متلقى",
    "UI_CharacterSlotScoreboard_BallResets": "ضبط الكرة",
    "UI_CharacterSlotScoreboard_BallSaves": "صد الكرات",
    "UI_CharacterSlotScoreboard_Ball_Hits": "ضربات الكرة",
    "UI_CharacterSlotScoreboard_BigHits": "ضربات كبرى",
    "UI_CharacterSlotScoreboard_SmallHits": "ضربات خفيفة",
    "UI_CharacterSlotScoreboard_SuperHits": "ضربات خارقة",
    "UI_CharacterSlotScoreboard_Harassments": "مقاطعة الهجوم",
    "UI_Emoijis_Text": "تعبيرات",
    "UI_SendEmoji_Prompt": "إرسال تعبير",

    # --- Battle Pass Header, Tabs, and Missions ---
    "UI_Progress_Caps": "التقدم",
    "UI_Paths_Caps": "تغيير المسار",
    "UI_About_Caps": "معلومات",
    "UI_Completed": "مكتملة",
    "UI_CupHub_Completed": "مكتملة",
    "UI_BattlePass_WeeklyBonus": "مهمات مكتملة",
    "UI_BattlePass_WeeklyBonusPrefix": "مكافأة:",
    "UI_BattlePass_WeeklyBonusMissionDesc": "مكافأة: إكمال مهمات الأسبوع",
    "UI_BattlePass_BattlePointsMissionDesc": "خبرة تذكرة المعركة",
    "MissionType_Desc_Completionist": "إكمال التحديات",
    "UI_BattlePass_RequiresBP": "تتطلب تذكرة المعركة",
    "QuestType_Desc_BackDash": "اندفاعات للخلف",
    "QuestType_Desc_GCKOs": "إقصاءات بإلغاء الجاذبية",
    "QuestType_Desc_RandomWins": "انتصارات باختيار عشوائي",
    "QuestType_Desc_RandomGames": "العب باختيار عشوائي (الفوز مضاعف)",
    "QuestType_Desc_FistsNAirHits": "ضربات قفازات جوية محايدة",
    "QuestType_Desc_ScytheDmg": "ضرر بهجمات المنجل",
    "QuestType_Desc_KODiffWeapons": "إقصاءات بأسلحة مختلفة",

    # --- Ranked Cards (Single line, max 26 chars) ---
    "UI_Ranked_Header": "النمط المصنف",
    "UI_Ranked_1": "1 ضد 1 مصنف",
    "UI_Ranked_1_Desc": "نزال فردي لإثبات المهارة",
    "UI_Ranked_2": "2 ضد 2 مصنف",
    "UI_Ranked_2_Desc": "تعاون وتنسيق كفريق للانتصار",
    "UI_CrewBattleSoloQueue_Desc": "العب بمفردك أو مع أصدقائك",
    "UI_Ranked_Room": "الانضمام للمصنف",
    "UI_Ranked_Room_Desc": "ادخل مباشرة عبر رقم الغرفة",

    # --- Offline Play Cards (Single line, max 25 chars) ---
    "UI_Offline_Header": "اللعب دون اتصال",
    "UI_Offline_Couch_Party": "جلسة لعب منزلية",
    "UI_Offline_Couch_Party_Desc": "تنافس محلي مع أصدقائك",
    "UI_Offline_Training": "غرفة التدريب",
    "UI_Offline_Training_Desc": "تدرب على الحركات والقتال",
    "UI_Offline_Tournament": "تحدي الأدوار الإقصائية",
    "UI_Offline_Tournament_Desc": "بطولة ضد مقاتلي الكمبيوتر",
    "UI_Offline_Tutorials": "أكاديمية التدريب",
    "UI_Offline_Tutorials_Desc": "تعلم حركات وأساسيات اللعب",
    "UI_Offline_Challenges": "معاينة التحديات المهارية",

    # --- Challenges / Tutorials screen ---
    "UI_LessonSelector_Header": "التحديات",
    "LessonCategoryType_Name_Tutorials": "التعليم",
    "LessonType_Title_NewTutorialPickUpAndAttack": "التقاط السلاح والهجوم",
    "LessonType_Desc_NewTutorialPickUpAndAttack": "التقط السلاح واضرب الخصم",
    "LessonType_Title_Recovering": "العودة للحلبة",
    "LessonType_Desc_Recovering": "اقفز للوصول إلى المنصة",
    "LessonType_Title_AdvancedRecovering": "التعافي المتقدم",
    "LessonType_Desc_AdvancedRecovering": "استخدم التعافي لبلوغ المنصة",

    # --- Tutorials Welcome Screen ---
    "Tutorial_Attacking_DisplayName": "الهجوم",
    "Tutorial_Platforming_DisplayName": "القفز والمنصات",
    "Tutorial_DamageMeters_DisplayName": "مقياس الضرر",
    "UI_Reward": "المكافأة",
    "UI_Begin": "ابدأ",

    # --- Store Redeem Code & Packs ---
    "UI_RedeemCode_Header": "استرداد رمز",
    "UI_RedeemCode_EnterCode": "أدخل الرمز هنا…",
    "UI_RedeemCode_Redeem": "استرداد",
    "UI_Store_AllLegends_Header": "فتح كل الأساطير",
    "UI_Store_AllLegends_Subheader": "افتح كل الأساطير الحالية والمستقبلية",
    "UI_Store_AllLegends_ButtonText": "شراء حزمة الأساطير",

    # --- Custom Rooms ---
    "UI_Custom_Header": "غرفة مخصصة",
    "UI_Custom_Create": "إنشاء غرفة",
    "UI_Custom_Create_Desc": "غرف عامة وخاصة",
    "UI_Custom_Join": "انضمام لغرفة",
    "UI_Custom_Join_Desc": "ادخل برقم الغرفة",
    "UI_Custom_Browse": "تصفح الغرف",
    "UI_Custom_Browse_Desc": "استعراض الغرف العامة",
    "UI_Custom_Create_Header": "نوع الغرفة",
    "UI_Custom_Create_Private": "غرفة خاصة",
    "UI_Custom_Create_Private_Desc": "متاحة للمحددين فقط",
    "UI_Custom_Create_Public": "غرفة عامة",
    "UI_Custom_Create_Public_Desc": "متاحة للجميع للانضمام",

    # --- Browse Rooms ---
    "UI_GameList_OpenGames": "غرفة متاحة",
    "UI_GameList_ChangeFilters": "تعديل التصفية",
    "UI_GameList_Server": "الخادم",
    "UI_GameList_Players": "اللاعبون",
    "UI_GameList_Gamemode": "نمط اللعب",
    "UI_GameList_SpecialRules": "قواعد خاصة",
    "UI_GameList_Creator": "المنشئ",
    "UI_GameList_Description": "الوصف",
    "UI_Team": "فرق",
    "LSM_Leader_Chooses": "اختيار القائد",

    # --- Numpad Join ---
    "UI_Numpad_Header": "الانضمام لغرفة",
    "UI_Numpad_Hide": "إخفاء رقم الغرفة",
    "UI_SelectCharacter_HideRoomNumber": "إخفاء رقم الغرفة",
    "UI_Numpad_Join": "دخول"
}

def update_dictionaries():
    print("Updating translations_ui_master.py...")
    sys.path.append('arabic_localization')
    from translations_ui_master import UI_MASTER
    UI_MASTER.update(TARGET_UPDATES)

    # Save to translations_ui_master.py
    with open('arabic_localization/translations_ui_master.py', 'w', encoding='utf-8') as f:
        f.write("# -*- coding: utf-8 -*-\n")
        f.write("UI_MASTER = " + repr(UI_MASTER) + "\n")

    print(f"Updated UI_MASTER with {len(TARGET_UPDATES)} target overrides. Total keys: {len(UI_MASTER)}")

if __name__ == '__main__':
    update_dictionaries()
