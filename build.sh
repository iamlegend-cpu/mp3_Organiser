#!/bin/bash

# MP3 Organiser 0.1a - Build Script (Linux/Mac)
# Professionele build zonder console vensters

echo ""
echo "========================================"
echo "   MP3 Organiser 0.1a - Build Script"
echo "========================================"
echo ""

# Controleer of Python geïnstalleerd is
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 is niet geïnstalleerd"
    echo "Installeer Python3 en voer dit script opnieuw uit"
    exit 1
fi

# Controleer of PyInstaller geïnstalleerd is
echo "Controleer PyInstaller installatie..."
if ! pip3 show pyinstaller &> /dev/null; then
    echo "PyInstaller niet gevonden. Installeren..."
    pip3 install pyinstaller
    if [ $? -ne 0 ]; then
        echo "ERROR: Kon PyInstaller niet installeren"
        exit 1
    fi
fi

# Controleer of alle dependencies geïnstalleerd zijn
echo "Controleer dependencies..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "WAARSCHUWING: Niet alle dependencies konden worden geïnstalleerd"
    echo "Het programma zal nog steeds werken, maar met beperkte functionaliteit"
fi

# Maak build directory
mkdir -p build
mkdir -p dist

echo ""
echo "Start build proces..."
echo ""

# Verwijder oude builds
rm -rf build/MP3_Organiser
rm -rf dist/MP3_Organiser

# Start PyInstaller build
echo "Bouwen van MP3 Organiser..."
pyinstaller --clean MP3_Organiser.spec

if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Build gefaald!"
    echo "Controleer de foutmeldingen hierboven"
    exit 1
fi

echo ""
echo "========================================"
echo "   Build Succesvol Voltooid!"
echo "========================================"
echo ""
echo "Executable locatie: dist/MP3_Organiser/MP3_Organiser"
echo ""
echo "Om het programma te starten:"
echo "1. Ga naar de 'dist/MP3_Organiser' map"
echo "2. Voer uit: ./MP3_Organiser"
echo ""
echo "Om het programma te distribueren:"
echo "- Kopieer de hele 'dist/MP3_Organiser' map"
echo "- Alle benodigde bestanden zijn al inbegrepen"
echo ""

# Maak executable uitvoerbaar
chmod +x dist/MP3_Organiser/MP3_Organiser

echo "Build voltooid! Executable is beschikbaar in dist/MP3_Organiser/" 