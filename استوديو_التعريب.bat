@echo off
setlocal
cd /d "%~dp0"
title Brawlhalla Arabic Studio

echo ============================================================
echo   Brawlhalla Arabic Studio
echo ============================================================
echo.

set "PY="

py -3 --version >nul 2>&1
if %errorlevel% equ 0 (
    set "PY=py -3"
    goto :found
)

python --version >nul 2>&1
if %errorlevel% equ 0 (
    set "PY=python"
    goto :found
)

if exist "%LOCALAPPDATA%\Python\bin\python.exe" (
    set "PY="%LOCALAPPDATA%\Python\bin\python.exe""
    goto :found
)

if exist "%LOCALAPPDATA%\Programs\Python\Launcher\py.exe" (
    set "PY="%LOCALAPPDATA%\Programs\Python\Launcher\py.exe""
    goto :found
)

for /d %%D in ("%LOCALAPPDATA%\Programs\Python\Python3*") do (
    if exist "%%D\python.exe" (
        set "PY="%%D\python.exe""
        goto :found
    )
)

:found
if not defined PY (
    echo [!] Python is not found on your system!
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

echo Starting Localization Studio...
%PY% "%~dp0arabic_localization\localization_studio.py"
if %errorlevel% neq 0 (
    echo.
    echo [!] Studio closed with error code: %errorlevel%
    pause
)
