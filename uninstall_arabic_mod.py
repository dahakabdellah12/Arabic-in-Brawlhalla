# -*- coding: utf-8 -*-
"""
أداة استعادة ملفات Brawlhalla الأصلية وإلغاء التعريب
Brawlhalla Arabic Localization Mod Uninstaller
"""

import os
import shutil
import sys
import winreg

sys.stdout.reconfigure(encoding='utf-8')

def find_brawlhalla_dir():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    parent = os.path.dirname(base_dir)
    if os.path.exists(os.path.join(parent, 'Brawlhalla.exe')):
        return parent
    if os.path.exists(os.path.join(base_dir, 'Brawlhalla.exe')):
        return base_dir

    common_paths = [
        r'D:\SteamLibrary\steamapps\common\Brawlhalla',
        r'C:\Program Files (x86)\Steam\steamapps\common\Brawlhalla',
        r'C:\SteamLibrary\steamapps\common\Brawlhalla',
        r'E:\SteamLibrary\steamapps\common\Brawlhalla'
    ]
    for p in common_paths:
        if os.path.exists(os.path.join(p, 'Brawlhalla.exe')):
            return p

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

def uninstall():
    print("=" * 65)
    print("      إلغاء التعريب واستعادة ملفات Brawlhalla الأصلية")
    print("      Brawlhalla Arabic Localization Mod Uninstaller")
    print("=" * 65)

    game_dir = find_brawlhalla_dir()
    if not game_dir:
        user_input = input("\nيرجى إدخال المسار الكامل لمجلد لعبة Brawlhalla: ").strip().strip('"\'')
        if os.path.exists(os.path.join(user_input, 'Brawlhalla.exe')):
            game_dir = user_input
        else:
            print("خطأ: لم يتم العثور على Brawlhalla.exe في المسار المدخل!")
            sys.exit(1)

    print(f"\n[+] مسار اللعبة: {game_dir}")

    target_lang = os.path.join(game_dir, 'languages', 'language.1.bin')
    target_lang_bak = target_lang + '.original_backup'

    target_font = os.path.join(game_dir, 'fontData', 'Font_Latin.swf')
    target_font_bak = target_font + '.original_backup'

    restored_any = False

    if os.path.exists(target_lang_bak):
        shutil.copy2(target_lang_bak, target_lang)
        print(f"  ✓ تم استعادة ملف اللغة الأصلي بنجاح ({os.path.getsize(target_lang):,} bytes)")
        restored_any = True
    else:
        print(f"  ! تنبيه: لم يتم العثور على النسخة الاحتياطية لملف اللغة: {target_lang_bak}")

    if os.path.exists(target_font_bak):
        shutil.copy2(target_font_bak, target_font)
        print(f"  ✓ تم استعادة ملف الخط الأصلي بنجاح ({os.path.getsize(target_font):,} bytes)")
        restored_any = True
    else:
        print(f"  ! تنبيه: لم يتم العثور على النسخة الاحتياطية لملف الخط: {target_font_bak}")

    if restored_any:
        print("\n" + "=" * 65)
        print("      تمت استعادة الملفات الأصلية للعبة Brawlhalla بنجاح 100%.")
        print("=" * 65)
    else:
        print("\nتعذر العثور على ملفات النسخ الاحتياطي التلقائي.")
        print("يمكنك دائماً استعادة الملفات عبر Steam: كليك يمين على Brawlhalla > خصائص > الملفات المثبتة > التحقق من سلامة ملفات اللعبة.")

if __name__ == '__main__':
    uninstall()
