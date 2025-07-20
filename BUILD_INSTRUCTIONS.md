# MP3 Organiser 0.1a - Build Instructies

## 📦 Professionele Verpakking

Dit project bevat alle benodigde bestanden om de MP3 Organiser professioneel te verpakken zonder console vensters.

## 🎯 Build Opties

### **--onedir (Aanbevolen)**
- ✅ **Sneller opstarten**
- ✅ **Kleinere executable**
- ✅ **Makkelijker te debuggen**
- ✅ **Betere compatibiliteit**

### **--onefile (Alternatief)**
- ⚠️ **Langzamer opstarten**
- ⚠️ **Grotere executable**
- ✅ **Eén bestand voor distributie**

## 🚀 Snelle Build (Windows)

### Methode 1: Automatisch Build Script
```bash
# Dubbelklik op build.bat of voer uit in command prompt:
build.bat
```

### Methode 2: Handmatig
```bash
# Installeer dependencies
pip install -r requirements.txt
pip install pyinstaller

# Build het programma
pyinstaller --clean MP3_Organiser.spec
```

## 🐧 Linux/Mac Build

### Methode 1: Automatisch Build Script
```bash
# Maak script uitvoerbaar
chmod +x build.sh

# Voer build script uit
./build.sh
```

### Methode 2: Handmatig
```bash
# Installeer dependencies
pip3 install -r requirements.txt
pip3 install pyinstaller

# Build het programma
pyinstaller --clean MP3_Organiser.spec
```

## 📁 Build Resultaten

Na een succesvolle build vind je het programma in:
```
dist/
└── MP3_Organiser/
    ├── MP3_Organiser.exe (Windows)
    ├── MP3_Organiser (Linux/Mac)
    └── [alle benodigde bestanden]
```

## ⚙️ Spec File Configuratie

### **Professionele Instellingen**
- ✅ **Geen console vensters** (`console=False`)
- ✅ **UPX compressie** voor kleinere bestanden
- ✅ **Debug informatie verwijderd** (`strip=True`)
- ✅ **Metadata toegevoegd** (versie, beschrijving, etc.)
- ✅ **Icon ondersteuning** (als `icon.ico` beschikbaar is)

### **Inbegrepen Modules**
- ✅ **Tkinter** (GUI)
- ✅ **Mutagen** (MP3 metadata)
- ✅ **Requests** (online databases)
- ✅ **Librosa/Scipy/Numpy** (audio processing)
- ✅ **SQLite3** (cache database)
- ✅ **Threading** (multi-threading)

### **Uitgesloten Modules**
- ❌ **Test modules** (kleinere bestandsgrootte)
- ❌ **Development tools** (pylint, black, etc.)
- ❌ **Onnodige libraries** (matplotlib, PIL, etc.)

## 🎨 Icon Toevoegen

Voor een professionele uitstraling, voeg een `icon.ico` bestand toe aan de root van het project:

```
project/
├── MP3_Organiser0.1a.py
├── MP3_Organiser.spec
├── icon.ico          ← Voeg hier je icon toe
├── build.bat
└── build.sh
```

## 🔧 Troubleshooting

### **Build Fouten**
```bash
# Controleer Python versie
python --version

# Controleer PyInstaller
pip show pyinstaller

# Controleer dependencies
pip install -r requirements.txt
```

### **Executable Start Niet**
```bash
# Windows: Voer uit in command prompt
cd dist\MP3_Organiser
MP3_Organiser.exe

# Linux/Mac: Voer uit in terminal
cd dist/MP3_Organiser
./MP3_Organiser
```

### **Ontbrekende Modules**
```bash
# Installeer alle dependencies
pip install -r requirements.txt

# Of installeer handmatig
pip install mutagen requests librosa scipy numpy
```

## 📦 Distributie

### **Windows**
- Kopieer de hele `dist\MP3_Organiser` map
- Alle benodigde bestanden zijn inbegrepen
- Geen Python installatie nodig op doelcomputer

### **Linux/Mac**
- Kopieer de hele `dist/MP3_Organiser` map
- Maak executable uitvoerbaar: `chmod +x MP3_Organiser`
- Geen Python installatie nodig op doelcomputer

## 🎯 Build Optimalisaties

### **Kleinere Bestandsgrootte**
- ✅ **UPX compressie** ingeschakeld
- ✅ **Debug informatie** verwijderd
- ✅ **Onnodige modules** uitgesloten
- ✅ **Test bestanden** gefilterd

### **Snellere Opstarttijd**
- ✅ **--onedir** in plaats van --onefile
- ✅ **Lazy loading** van optionele modules
- ✅ **Efficiënte module imports**

### **Professionele Uitstraling**
- ✅ **Geen console vensters**
- ✅ **Metadata toegevoegd**
- ✅ **Icon ondersteuning**
- ✅ **Clean build process**

## 📋 Build Checklist

- [ ] Python 3.7+ geïnstalleerd
- [ ] Dependencies geïnstalleerd (`pip install -r requirements.txt`)
- [ ] PyInstaller geïnstalleerd (`pip install pyinstaller`)
- [ ] Spec file aangepast (indien nodig)
- [ ] Icon toegevoegd (optioneel)
- [ ] Build script uitgevoerd
- [ ] Executable getest
- [ ] Distributie map gecontroleerd

## 🎉 Succesvolle Build

Na een succesvolle build heb je een professionele, standalone executable die:
- ✅ **Geen console vensters** toont
- ✅ **Alle functionaliteit** bevat
- ✅ **Klein en snel** is
- ✅ **Professioneel** oogt
- ✅ **Makkelijker te distribueren** is 