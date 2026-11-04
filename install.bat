@echo off
chcp 65001 > nul
title تثبيت التعريب العربي للعبة Brawlhalla
echo ============================================================
echo   تثبيت التعريب العربي الأصلي للعبة Brawlhalla
echo   Brawlhalla Arabic Localization Installer
echo ============================================================
echo.

where python >nul 2>nul
if %errorlevel% equ 0 (
    python "%~dp0install_arabic_mod.py"
) else (
    echo [!] لم يتم العثور على Python، جاري التثبيت المباشر بالنسخ...
    set "TARGET_DIR=%~dp0.."
    if exist "%TARGET_DIR%\Brawlhalla.exe" (
        if not exist "%TARGET_DIR%\languages\language.1.bin.original_backup" (
            copy "%TARGET_DIR%\languages\language.1.bin" "%TARGET_DIR%\languages\language.1.bin.original_backup" >nul
        )
        if not exist "%TARGET_DIR%\fontData\Font_Latin.swf.original_backup" (
            copy "%TARGET_DIR%\fontData\Font_Latin.swf" "%TARGET_DIR%\fontData\Font_Latin.swf.original_backup" >nul
        )
        copy "%~dp0game_files\languages\language.1.bin" "%TARGET_DIR%\languages\language.1.bin" >nul
        copy "%~dp0game_files\fontData\Font_Latin.swf" "%TARGET_DIR%\fontData\Font_Latin.swf" >nul
        echo [✓] تم نسخ وتثبيت ملفات التعريب بنجاح!
    ) else (
        echo [✗] يرجى تثبيت Python أو وضع مجلد التعريب داخل مجلد اللعبة مباشرة.
    )
)

echo.
pause
