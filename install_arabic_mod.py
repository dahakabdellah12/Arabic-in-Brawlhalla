# -*- coding: utf-8 -*-
"""
مثبت التعريب العربي للعبة Brawlhalla
Brawlhalla Arabic Localization Installer
يدعم الكشف التلقائي عن مسار اللعبة على Steam والتثبيت الآمن بنقرة واحدة مع إنشاء نسخة احتياطية للملفات الأصلية.
"""

import os
import shutil
import sys
import winreg

sys.stdout.reconfigure(encoding='utf-8')

def find_brawlhalla_dir():
    # 1. Check parent directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    parent = os.path.dirname(base_dir)
    if os.path.exists(os.path.join(parent, 'Brawlhalla.exe')):
        return parent
    if os.path.exists(os.path.join(base_dir, 'Brawlhalla.exe')):
        return base_dir

    # 2. Known default Steam library paths
    common_paths = [
        r'D:\SteamLibrary\steamapps\common\Brawlhalla',
        r'C:\Program Files (x86)\Steam\steamapps\common\Brawlhalla',
        r'C:\SteamLibrary\steamapps\common\Brawlhalla',
        r'E:\SteamLibrary\steamapps\common\Brawlhalla',
        r'F:\SteamLibrary\steamapps\common\Brawlhalla'
    ]
    for p in common_paths:
        if os.path.exists(os.path.join(p, 'Brawlhalla.exe')):
            return p

    # 3. Read Steam path from Windows Registry
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam")
        steam_path, _ = winreg.QueryValueEx(key, "SteamPath")
        winreg.CloseKey(key)
        reg_brawl = os.path.join(steam_path.replace('/', '\\'), 'steamapps', 'common', 'Brawlhalla')
        if os.path.exists(os.path.join(reg_brawl, 'Brawlhalla.exe')):
            return reg_brawl
    except Exception:
        pass

    return None

def install():
    print("=" * 65)
    print("      تثبيت التعريب العربي للعبة Brawlhalla")
    print("      Brawlhalla Arabic Localization Mod Installer")
    print("=" * 65)

    game_dir = find_brawlhalla_dir()
    if not game_dir:
        print("\nلم يتم العثور على مجلد تثبيت Brawlhalla تلقائياً.")
        user_input = input("يرجى إدخال المسار الكامل لمجلد لعبة Brawlhalla: ").strip().strip('"\'')
        if os.path.exists(os.path.join(user_input, 'Brawlhalla.exe')):
            game_dir = user_input
        else:
            print("خطأ: لم يتم العثور على Brawlhalla.exe في المسار المدخل!")
            sys.exit(1)

    print(f"\n[+] تم التعرف على مسار اللعبة: {game_dir}")

    # Local mod files
    base_dir = os.path.dirname(os.path.abspath(__file__))
    mod_lang = os.path.join(base_dir, 'game_files', 'languages', 'language.1.bin')
    if not os.path.exists(mod_lang):
        mod_lang = os.path.join(base_dir, 'language.1.arabic.bin')

    mod_font = os.path.join(base_dir, 'game_files', 'fontData', 'Font_Latin.swf')
    if not os.path.exists(mod_font):
        mod_font = os.path.join(base_dir, 'Font_Latin_Arabic.swf')

    # Target game files
    target_lang = os.path.join(game_dir, 'languages', 'language.1.bin')
    target_lang_bak = target_lang + '.original_backup'

    target_font = os.path.join(game_dir, 'fontData', 'Font_Latin.swf')
    target_font_bak = target_font + '.original_backup'

    # Step 1: Backup original files
    print("\n[1/3] التحقق من النسخ الاحتياطية الأصلية...")
    if not os.path.exists(target_lang_bak):
        if os.path.exists(target_lang):
            shutil.copy2(target_lang, target_lang_bak)
            print(f"  ✓ تم إنشاء نسخة احتياطية لملف اللغة: {target_lang_bak}")
    else:
        print("  ✓ النسخة الاحتياطية لملف اللغة موجودة بالفعل.")

    if not os.path.exists(target_font_bak):
        if os.path.exists(target_font):
            shutil.copy2(target_font, target_font_bak)
            print(f"  ✓ تم إنشاء نسخة احتياطية لملف الخط: {target_font_bak}")
    else:
        print("  ✓ النسخة الاحتياطية لملف الخط موجودة بالفعل.")

    # Step 2: Install Arabic language database
    print("\n[2/3] تثبيت ملف اللغة العربية...")
    if os.path.exists(mod_lang):
        os.makedirs(os.path.dirname(target_lang), exist_ok=True)
        shutil.copy2(mod_lang, target_lang)
        print(f"  ✓ تم تثبيت ملف اللغة العربي بنجاح ({os.path.getsize(target_lang):,} bytes)")
    else:
        print(f"  ✗ خطأ: ملف اللغة العربي غير موجود في حزمة التعريب: {mod_lang}")
        sys.exit(1)

    # Step 3: Install patched Arabic font SWF
    print("\n[3/3] تثبيت الخط العربي متعدد الأوزان...")
    if os.path.exists(mod_font):
        os.makedirs(os.path.dirname(target_font), exist_ok=True)
        shutil.copy2(mod_font, target_font)
        print(f"  ✓ تم تثبيت الخط العربي المعدل بنجاح ({os.path.getsize(target_font):,} bytes)")
    else:
        print(f"  ✗ خطأ: ملف الخط العربي غير موجود في حزمة التعريب: {mod_font}")
        sys.exit(1)

    print("\n" + "=" * 65)
    print("      تهانينا! تم تثبيت التعريب العربي بنجاح بنسبة 100%.")
    print("      يمكنك الآن فتح لعبة Brawlhalla والاستمتاع باللغة العربية!")
    print("=" * 65)

if __name__ == '__main__':
    install()
