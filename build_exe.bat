@echo off
title LemonWeather+ EXE Builder

echo ====================================
echo     LemonWeather+ EXE Builder
echo ====================================
echo.

REM Check if PyInstaller exists
pyinstaller --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo PyInstaller not found. Installing...
    python -m pip install pyinstaller
)

echo Cleaning old builds...
rmdir /s /q build 2>nul
rmdir /s /q dist 2>nul
del *.spec 2>nul

echo.
echo Building executable...
pyinstaller --clean --onefile --windowed ^
--icon=icon.ico ^
--name "LemonWeather+" ^
--hidden-import=ttkbootstrap ^
--hidden-import=matplotlib ^
--hidden-import=PIL ^
--hidden-import=geocoder ^
LemonWeatherPLUS.py

echo.
echo Moving executable to current directory...
move "dist\LemonWeather+.exe" .

echo Removing dist and build folders...
rmdir /s /q dist 2>nul
rmdir /s /q build 2>nul

echo.
echo =========================================
echo Build finished!
echo EXE file is now in main directory.
echo =========================================
pause