@echo off
REM MP3 Organiser 0.1a - Build Script
REM Professionele build zonder console vensters

echo.
echo ========================================
echo    MP3 Organiser 0.1a - Build Script
echo ========================================
echo.

REM Controleer of Python geïnstalleerd is
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is niet geïnstalleerd of niet gevonden in PATH
    echo Installeer Python en voer dit script opnieuw uit
    pause
    exit /b 1
)

REM Controleer of PyInstaller geïnstalleerd is
echo Controleer PyInstaller installatie...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller niet gevonden. Installeren...
    pip install pyinstaller
    if errorlevel 1 (
        echo ERROR: Kon PyInstaller niet installeren
        pause
        exit /b 1
    )
)

REM Controleer of alle dependencies geïnstalleerd zijn
echo Controleer dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo WAARSCHUWING: Niet alle dependencies konden worden geïnstalleerd
    echo Het programma zal nog steeds werken, maar met beperkte functionaliteit
)

REM Maak build directory
if not exist "build" mkdir build
if not exist "dist" mkdir dist

echo.
echo Start build proces...
echo.

REM Verwijder oude builds
if exist "build\MP3_Organiser" rmdir /s /q "build\MP3_Organiser"
if exist "dist\MP3_Organiser" rmdir /s /q "dist\MP3_Organiser"

REM Start PyInstaller build
echo Bouwen van MP3 Organiser...
pyinstaller --clean MP3_Organiser.spec

if errorlevel 1 (
    echo.
    echo ERROR: Build gefaald!
    echo Controleer de foutmeldingen hierboven
    pause
    exit /b 1
)

echo.
echo ========================================
echo    Build Succesvol Voltooid!
echo ========================================
echo.
echo Executable locatie: dist\MP3_Organiser\MP3_Organiser.exe
echo.
echo Om het programma te starten:
echo 1. Ga naar de 'dist\MP3_Organiser' map
echo 2. Dubbelklik op 'MP3_Organiser.exe'
echo.
echo Om het programma te distribueren:
echo - Kopieer de hele 'dist\MP3_Organiser' map
echo - Alle benodigde bestanden zijn al inbegrepen
echo.

REM Open de dist map in explorer
explorer "dist\MP3_Organiser"

pause 