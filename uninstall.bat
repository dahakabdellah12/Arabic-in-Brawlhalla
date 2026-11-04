@echo off
chcp 65001 > nul
title استعادة ملفات Brawlhalla الأصلية
echo ============================================================
echo   إلغاء التعريب واستعادة ملفات Brawlhalla الأصلية
echo   Brawlhalla Arabic Localization Uninstaller
echo ============================================================
echo.

where python >nul 2>nul
if %errorlevel% equ 0 (
    python "%~dp0uninstall_arabic_mod.py"
) else (
    set "TARGET_DIR=%~dp0.."
    if exist "%TARGET_DIR%\Brawlhalla.exe" (
        if exist "%TARGET_DIR%\languages\language.1.bin.original_backup" (
            copy "%TARGET_DIR%\languages\language.1.bin.original_backup" "%TARGET_DIR%\languages\language.1.bin" >nul
            echo [✓] تم استعادة ملف اللغة الأصلي.
        )
        if exist "%TARGET_DIR%\fontData\Font_Latin.swf.original_backup" (
            copy "%TARGET_DIR%\fontData\Font_Latin.swf.original_backup" "%TARGET_DIR%\fontData\Font_Latin.swf" >nul
            echo [✓] تم استعادة ملف الخط الأصلي.
        )
    )
)

echo.
pause
