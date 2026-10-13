@echo off
setlocal enabledelayedexpansion

echo ============================================================
echo   Skill Master - Global Antigravity Setup / Restore
echo ============================================================
echo.

set "SKILLS_SOURCE=D:\Code\Skill_Master\.agent\skills"
set "GEMINI_DIR=%USERPROFILE%\.gemini"
set "CONFIG_DIR=%GEMINI_DIR%\config"
set "GLOBAL_SKILLS=%CONFIG_DIR%\skills"
set "ANTIGRAVITY_SKILLS=%GEMINI_DIR%\antigravity\skills"
set "SKILLS_JSON=%CONFIG_DIR%\skills.json"

if not exist "!SKILLS_SOURCE!" (
    echo [ERROR] Master skills source not found at: !SKILLS_SOURCE!
    echo Please make sure Skill_Master is located at D:\Code\Skill_Master
    pause
    exit /b 1
)

echo [1/4] Ensuring .gemini directories exist...
if not exist "!CONFIG_DIR!" mkdir "!CONFIG_DIR!"
if not exist "%GEMINI_DIR%\antigravity" mkdir "%GEMINI_DIR%\antigravity"

echo [2/4] Registering global skills.json...
(
    echo {
    echo   "skills_paths": [
    echo     "D:/Code/Skill_Master/.agent/skills"
    echo   ]
    echo }
) > "!SKILLS_JSON!"
echo   - Saved !SKILLS_JSON!

echo [3/4] Establishing live NTFS Junction for ~/.gemini/config/skills...
if exist "!GLOBAL_SKILLS!" (
    rmdir "!GLOBAL_SKILLS!" 2>nul || del /q /f "!GLOBAL_SKILLS!" 2>nul
)
mklink /J "!GLOBAL_SKILLS!" "!SKILLS_SOURCE!"
if %errorlevel% neq 0 (
    echo [WARNING] Could not create Junction directly, trying PowerShell...
    powershell -NoProfile -Command "New-Item -ItemType Junction -Path '!GLOBAL_SKILLS!' -Target '!SKILLS_SOURCE!' -Force"
)

echo [4/4] Establishing compatibility Junction for ~/.gemini/antigravity/skills...
if exist "!ANTIGRAVITY_SKILLS!" (
    rmdir "!ANTIGRAVITY_SKILLS!" 2>nul || del /q /f "!ANTIGRAVITY_SKILLS!" 2>nul
)
mklink /J "!ANTIGRAVITY_SKILLS!" "!GLOBAL_SKILLS!"
if %errorlevel% neq 0 (
    powershell -NoProfile -Command "New-Item -ItemType Junction -Path '!ANTIGRAVITY_SKILLS!' -Target '!GLOBAL_SKILLS!' -Force"
)

echo.
echo ============================================================
echo   SUCCESS! Skill Master is fully connected to Antigravity!
echo ============================================================
echo.
pause
