# 🎵 MP3 Organiser 0.1a - Slimme Muziek Organisatie

Een geavanceerde MP3 bestandsorganisator met Shazam-achtige audio fingerprinting, online database detectie en intelligente duplicaten behandeling.

## 📋 Inhoudsopgave

- [🎯 Wat doet het?](#-wat-doet-het)
- [🚀 Snelle Start](#-snelle-start)
- [⚙️ Instellingen & Configuratie](#️-instellingen--configuratie)
- [🔍 Functie Compatibiliteit](#-functie-compatibiliteit)
- [🎵 Audio Fingerprinting](#-audio-fingerprinting)
- [🌐 Online Database Detectie](#-online-database-detectie)
- [📁 Organisatie Opties](#-organisatie-opties)
- [🔄 Duplicaten Behandeling](#-duplicaten-behandeling)
- [📝 Log & Debugging](#-log--debugging)
- [🌐 Taal & Interface](#-taal--interface)
- [🔧 Geavanceerde Instellingen](#-geavanceerde-instellingen)
- [❓ Troubleshooting](#-troubleshooting)
- [📈 Performance Tips](#-performance-tips)

## 🎯 Wat doet het?

### **Hoofdfunctionaliteiten:**

- ✅ **Intelligente Artiest Detectie**: ID3 tags, online databases, audio fingerprinting
- ✅ **Automatische Organisatie**: Hiërarchische mappen, per album, per jaar
- ✅ **Duplicaten Beheer**: Detectie, verwijdering, verplaatsing
- ✅ **Shazam-achtige Audio Fingerprinting**: Detecteert artiesten via audio analyse
- ✅ **Online Database Integratie**: Last.fm, MusicBrainz, Discogs
- ✅ **Lokale Cache**: Slaat resultaten op voor snellere herkenning
- ✅ **Gedetailleerde Statistieken**: Scan resultaten en organisatie overzichten

### **Detectie Methoden (in volgorde):**

1. **📁 ID3 Tags**: MP3 metadata (snelste methode)
2. **🌐 Online Database**: Last.fm, MusicBrainz, Discogs
3. **🎵 Audio Fingerprinting**: Shazam-achtige audio analyse
4. **📝 Bestandsnaam Analyse**: Fallback voor onbekende bestanden
5. **❓ Unknown Artist**: Als laatste optie

## 🚀 Snelle Start

### **Installatie:**

```bash
# Installeer alle dependencies
pip install -r requirements.txt

# Of handmatig
pip install mutagen requests librosa scipy numpy
```

### **Gebruik:**

```bash
# Start de applicatie
python MP3_Organiser0.1a.py
```

### **Eerste Stappen:**

1. **Selecteer bron map** met je MP3 bestanden
2. **Ga naar Instellingen** → **Online Database**
3. **Schakel Audio Fingerprinting in** voor beste resultaten
4. **Scan je bestanden** om te zien wat er gevonden wordt
5. **Start organisatie** om bestanden te organiseren

## ⚙️ Instellingen & Configuratie

### **📁 Organisatie Opties:**

**Hiërarchische Mappen:**

- ✅ **Aanbevolen voor grote collecties**
- 📁 Structuur: `Muziek/A/Adele/`, `Muziek/B/Beatles/`
- ⚡ **Voordelen**: Snelle navigatie, overzichtelijke structuur

**Per Album Organiseren:**

- ✅ **Aanbevolen voor complete albums**
- 📁 Structuur: `Artiest/Album/Track.mp3`
- 🎵 **Voordelen**: Behoudt album structuur

**Per Jaar Organiseren:**

- ✅ **Aanbevolen voor chronologische organisatie**
- 📁 Structuur: `Artiest/2023/Track.mp3`
- 📅 **Voordelen**: Chronologische overzicht

**Bestanden Hernoemen:**

- ✅ **Aanbevolen voor consistente naamgeving**
- 📝 Format: `Artiest - Titel.mp3`
- 🧹 **Voordelen**: Verwijdert (official), (remix), etc.

### **🌐 Online Database Instellingen:**

**Online Database Detectie:**

- ✅ **Altijd aanbevolen** voor beste resultaten
- 🌐 Zoekt in Last.fm, MusicBrainz, Discogs
- 📡 **Voordelen**: Detecteert onbekende artiesten

**AI-gebaseerde Artiest Detectie:**

- ✅ **Aanbevolen** voor intelligente herkenning
- 🤖 Gebruikt machine learning voor betere resultaten
- 🎯 **Voordelen**: Hogere nauwkeurigheid

**🎵 Audio Fingerprinting (Shazam-achtig):**

- ✅ **Aanbevolen** voor bestanden zonder metadata
- 🎵 Analyseert audio eigenschappen
- 🔍 **Voordelen**: Werkt zonder ID3 tags

**Lokale Cache:**

- ✅ **Altijd aanbevolen** voor snelheid
- 💾 Slaat resultaten op voor 24 uur (standaard)
- ⚡ **Voordelen**: Voorkomt herhaalde analyses

### **🔄 Duplicaten Behandeling:**

**Controleer Duplicaten:**

- ✅ **Aanbevolen** voor alle collecties
- 🔍 Detecteert op bestandsnaam en ID3 tags
- 📊 **Voordelen**: Toont overzicht van duplicaten

**Automatisch Verwijderen:**

- ⚠️ **Voorzichtig gebruiken** - kan niet ongedaan worden gemaakt
- 🗑️ Verwijdert duplicaten automatisch
- 💾 **Voordelen**: Bespaart schijfruimte

**Verplaatsen naar Output Map:**

- ✅ **Aanbevolen** voor veilige behandeling
- 📁 Verplaatst naar "Duplicaten" map
- 🔒 **Voordelen**: Behoudt alle bestanden

### **📝 Log Instellingen:**

**Auto-scroll:**

- ✅ **Aanbevolen** voor live updates
- 📜 Volgt automatisch nieuwe berichten
- 👀 **Voordelen**: Blijft altijd bij

**Timestamps:**

- ✅ **Aanbevolen** voor debugging
- ⏰ Toont tijdstempel bij elk bericht
- 🔍 **Voordelen**: Makkelijk terug te vinden

**Log Opslaan:**

- ✅ **Aanbevolen** voor belangrijke sessies
- 💾 Slaat log op naar bestand
- 📄 **Voordelen**: Kan later bekeken worden

## 🔍 Functie Compatibiliteit

### **✅ Functies die ALTIJD samen kunnen werken:**

**1. Scan Bestanden:**

- ✅ **ID3 Tags** + **Online Database** + **Audio Fingerprinting** + **Bestandsnaam analyse**
- ✅ **Alle detectie methoden** worden in volgorde geprobeerd
- ✅ **Geen conflicten** - elke methode is een fallback voor de vorige

**2. Organisatie:**

- ✅ **Hiërarchische mappen** + **Per album** + **Per jaar**
- ✅ **Duplicaten controle** + **Bestanden hernoemen**
- ✅ **Alle opties** kunnen tegelijk actief zijn

### **⚠️ Functies die elkaar kunnen beïnvloeden:**

**1. Duplicaten Behandeling:**

```python
# Je kunt maar ÉÉN van deze kiezen:
- ❌ Automatisch verwijderen
- ❌ Verplaatsen naar output map  
- ✅ Behouden (geen actie)
```

**2. Audio Fingerprinting:**

```python
# Vereist bepaalde dependencies:
- ✅ LIBROSA_AVAILABLE = True
- ✅ SCIPY_AVAILABLE = True
- ❌ Anders wordt het overgeslagen
```

## 🎵 Audio Fingerprinting

### **Wat is Audio Fingerprinting?**

Audio fingerprinting is een techniek die een unieke "vingerafdruk" maakt van een audio bestand door de spectrale eigenschappen te analyseren. Dit is vergelijkbaar met hoe Shazam werkt om muziek te herkennen.

### **Hoe werkt het in deze applicatie?**

1. **Spectrogram Analyse**: De applicatie analyseert de eerste 30 seconden van elk MP3 bestand
2. **Peak Detectie**: Zoekt naar unieke frequentie-tijd combinaties (peaks) in het spectrogram
3. **Fingerprint Generatie**: Creëert een unieke hash op basis van de belangrijkste peaks
4. **Database Zoeken**: Vergelijkt de fingerprint met een lokale cache en online databases
5. **Artiest Detectie**: Identificeert de artiest op basis van audio eigenschappen

### **Voordelen van Audio Fingerprinting:**

- ✅ **Werkt zonder ID3 tags**: Detecteert artiesten zelfs als metadata ontbreekt
- ✅ **Ongevoelig voor bestandsnamen**: Herkent muziek ongeacht bestandsnaam
- ✅ **Hoge nauwkeurigheid**: Gebruikt audio eigenschappen in plaats van tekst
- ✅ **Lokale cache**: Slaat resultaten op voor snellere herkenning
- ✅ **Online backup**: Kan online databases raadplegen voor onbekende nummers

### **Technische Details:**

**Spectrogram Analyse:**

```python
# Laad audio met librosa
y, sr = librosa.load(file_path, sr=22050, duration=30)

# Bereken mel-spectrogram
S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000)
S_db = librosa.power_to_db(S, ref=np.max)
```

**Peak Detectie:**

```python
# Zoek lokale maxima in tijd-frequentie domein
for t in range(spectrogram.shape[1]):
    for f in range(spectrogram.shape[0]):
        # Controleer of dit een lokale maximum is
        if is_peak and spectrogram[f, t] > -20:
            peaks.append({'time': t, 'frequency': f, 'magnitude': spectrogram[f, t]})
```

**Fingerprint Generatie:**

```python
# Sorteer peaks op magnitude en neem top 100
top_peaks = peaks[:100]

# Converteer naar hash
fingerprint_string = "|".join(fingerprint_data)
fingerprint_hash = hashlib.md5(fingerprint_string.encode()).hexdigest()
```

## 🌐 Online Database Detectie

### **Ondersteunde APIs:**

**Last.fm:**

- 🎵 **Muziek database** met uitgebreide metadata
- 🔑 **API key vereist** voor volledige functionaliteit
- 📊 **Confidence scoring** voor betrouwbaarheid

**MusicBrainz:**

- 🎼 **Open source** muziek database
- 🌐 **Gratis** te gebruiken
- 📝 **Uitgebreide metadata** beschikbaar

**Discogs:**

- 💿 **Vinyl en CD** database
- 🎯 **Hoge nauwkeurigheid** voor oudere releases
- 📚 **Uitgebreide release informatie**

### **Rate Limiting:**

De applicatie respecteert API limieten:

- ⏱️ **30 requests per minuut** (standaard)
- 🔄 **Automatische retry** bij fouten
- 💾 **Cache** voorkomt onnodige API calls

## 📁 Organisatie Opties

### **Hiërarchische Mappen:**

**Structuur:**

```text
Muziek/
├── A/
│   ├── Adele/
│   └── Arctic Monkeys/
├── B/
│   ├── Barry White/
│   └── Beatles/
└── M/
    └── Michael Jackson/
```

**Voordelen:**

- ✅ **Snelle navigatie** in grote collecties
- ✅ **Overzichtelijke structuur**
- ✅ **Schaalbaar** voor duizenden artiesten

### **Per Album Organiseren:**

**Structuur:**

```text
Michael Jackson/
├── Thriller/
│   ├── thriller.mp3
│   ├── billie_jean.mp3
│   └── beat_it.mp3
└── Bad/
    ├── bad.mp3
    └── smooth_criminal.mp3
```

**Voordelen:**

- ✅ **Behoudt album structuur**
- ✅ **Chronologische organisatie**
- ✅ **Complete albums** blijven bij elkaar

### **Per Jaar Organiseren:**

**Structuur:**

```text
Michael Jackson/
├── 1982/
│   ├── thriller.mp3
│   └── billie_jean.mp3
└── 1987/
    ├── bad.mp3
    └── smooth_criminal.mp3
```

**Voordelen:**

- ✅ **Chronologische overzicht**
- ✅ **Eenvoudige tijdlijn**
- ✅ **Muziekgeschiedenis** per jaar

## 🔄 Duplicaten Behandeling

### **Detectie Methoden:**

**Bestandsnaam Vergelijking:**

- 📁 **Exacte match** van bestandsnamen
- 🔍 **Case-insensitive** vergelijking
- ⚡ **Snelle detectie** voor identieke bestanden

**ID3 Tag Vergelijking:**

- 🎵 **Artiest + Titel** combinatie
- 🎼 **Album informatie** voor context
- 🎯 **Hoge nauwkeurigheid** voor metadata

### **Behandeling Opties:**

**Automatisch Verwijderen:**

- ⚠️ **Permanent** - kan niet ongedaan worden gemaakt
- 🗑️ **Verwijdert** duplicaten automatisch
- 💾 **Bespaart** schijfruimte

**Verplaatsen naar Output Map:**

- ✅ **Veilig** - behoudt alle bestanden
- 📁 **Georganiseerd** in "Duplicaten" map
- 🔄 **Hernoemt** met _1,_2, etc.

**Behouden (Geen Actie):**

- ℹ️ **Informatief** - toont alleen overzicht
- 📊 **Statistieken** zonder wijzigingen
- 🔍 **Analyse** zonder risico

## 📝 Log & Debugging

### **Log Niveaus:**

**Info (Standaard):**

- ℹ️ **Algemene informatie** over verwerking
- 📊 **Statistieken** en resultaten
- ✅ **Succesvolle** operaties

**Debug:**

- 🐛 **Gedetailleerde** informatie
- 🔍 **Technische details** voor troubleshooting
- 📝 **API responses** en fouten

**Error:**

- ❌ **Alleen fouten** en waarschuwingen
- ⚠️ **Kritieke problemen**
- 🚨 **Systeem fouten**

### **Auto-scroll Functionaliteit:**

**Ingeschakeld (Aanbevolen):**

- 📜 **Volgt automatisch** nieuwe berichten
- 👀 **Blijft altijd** bij de laatste updates
- ⚡ **Real-time** monitoring

**Uitgeschakeld:**

- 🖱️ **Handmatige scroll** mogelijk
- 📍 **Vaste positie** in log
- 🔍 **Terug zoeken** in geschiedenis

## 🌐 Taal & Interface

### **Ondersteunde Talen:**

**Nederlands (Standaard):**

- 🇳🇱 **Volledige vertaling**
- 🎯 **Nederlandse muziek termen**
- 📝 **Lokale datum/tijd** format

**Engels:**

- 🇺🇸 **Engelse interface**
- 🌍 **Internationale standaard**
- 📚 **Uitgebreide documentatie**

### **Lettertype Instellingen:**

**Lettergrootte:**

- **Klein (8pt)**: Compacte interface
- **Normaal (10pt)**: Standaard grootte
- **Groot (12pt)**: Verbeterde leesbaarheid
- **Extra Groot (14pt)**: Toegankelijkheid

**Lettertype:**

- **Arial**: Standaard, goed leesbaar
- **Helvetica**: Modern, clean design
- **Times New Roman**: Klassiek, formeel
- **Verdana**: Web-optimalized
- **Tahoma**: Compact, efficiënt

## 🔧 Geavanceerde Instellingen

### **Cache Configuratie:**

**Cache Duur:**

- **1 uur**: Voor snelle updates
- **6 uur**: Balans tussen snelheid en nauwkeurigheid
- **12 uur**: Standaard voor meeste gebruik
- **24 uur**: Aanbevolen voor stabiele collecties
- **48 uur**: Voor zelden wijzigende collecties

**Cache Inhoud:**

- 🎵 **Artiest informatie** van online databases
- 🎯 **Audio fingerprints** voor snelle herkenning
- 📊 **Confidence scores** voor betrouwbaarheid
- ⏰ **Timestamps** voor cache validatie

### **API Configuratie:**

**Rate Limiting:**

- **10 requests/min**: Voor trage verbindingen
- **20 requests/min**: Balans tussen snelheid en limieten
- **30 requests/min**: Standaard voor meeste APIs
- **50 requests/min**: Voor snelle verwerking
- **100 requests/min**: Voor grote collecties

**API Keys:**

- 🔑 **Last.fm API Key**: Voor volledige Last.fm functionaliteit
- 🌐 **MusicBrainz**: Gratis, geen key vereist
- 💿 **Discogs**: Optioneel voor uitgebreide metadata

## ❓ Troubleshooting

### **Veelvoorkomende Problemen:**

**Audio Fingerprinting niet beschikbaar:**

```text
⚠️ Audio fingerprinting niet beschikbaar (librosa + scipy nodig)
```

**Oplossing:**

```bash
pip install librosa scipy numpy
```

**Online database werkt niet:**

```text
⚠️ requests module niet beschikbaar
```

**Oplossing:**

```bash
pip install requests
```

**Langzame verwerking:**

- 🔧 **Schakel online database uit** voor snelheid
- 💾 **Gebruik cache** voor herhaalde analyses
- 🎵 **Beperk audio fingerprinting** tot onbekende bestanden

**Onnauwkeurige resultaten:**

- 🎯 **Controleer ID3 tags** eerst
- 🌐 **Verifieer online database** instellingen
- 🎵 **Test audio fingerprinting** met bekende nummers

### **Performance Optimalisatie:**

**Voor grote collecties (>1000 bestanden):**

- ✅ **Gebruik cache** (24+ uur)
- ✅ **Schakel online database uit** voor initiële scan
- ✅ **Beperk audio fingerprinting** tot onbekende bestanden
- ✅ **Gebruik hiërarchische mappen**

**Voor kleine collecties (<100 bestanden):**

- ✅ **Alle functies aan** voor beste resultaten
- ✅ **Online database** voor maximale detectie
- ✅ **Audio fingerprinting** voor onbekende bestanden

**Voor onbekende bestanden:**

- ✅ **Audio fingerprinting** is cruciaal
- ✅ **Online database** voor backup
- ✅ **Cache** voorkomt herhaalde analyses

## 📈 Performance Tips

### **Optimale Configuratie per Gebruik:**

**Voor Snelle Verwerking:**

```text
✅ ID3 Tags
❌ Online Database (uitschakelen)
❌ Audio Fingerprinting (uitschakelen)
✅ Cache (behouden)
✅ Hiërarchische mappen
```

**Voor Beste Nauwkeurigheid:**

```text
✅ ID3 Tags
✅ Online Database
✅ Audio Fingerprinting
✅ Cache
✅ Alle API bronnen
✅ Lange cache duur (24+ uur)
```

**Voor Grote Collecties:**

```text
✅ ID3 Tags
✅ Online Database (met rate limiting)
✅ Audio Fingerprinting (alleen onbekende)
✅ Cache (48+ uur)
✅ Hiërarchische mappen
✅ Duplicaten controle
```

### **Cache Optimalisatie:**

**Lokale Database:**

```sql
-- Artist cache (voor online detectie)
CREATE TABLE artist_cache (
    filename_hash TEXT PRIMARY KEY,
    artist_name TEXT,
    confidence REAL,
    source TEXT,
    timestamp REAL
);

-- Fingerprint cache (voor audio fingerprinting)
CREATE TABLE fingerprint_cache (
    fingerprint_hash TEXT PRIMARY KEY,
    artist_name TEXT,
    confidence REAL,
    timestamp REAL
);
```

### **Voorbeeld Resultaten:**

```text
🔍 Start gedetailleerde scan...
📁 Totaal gevonden: 1250 MP3 bestanden
Analyseren: 1/1250
📡 Cache hit voor: mark_with_a_k_song.mp3
Analyseren: 2/1250
🎵 Audio fingerprinting voor: unknown_song.mp3
🎯 Fingerprint match gevonden: Mark With a K
Analyseren: 3/1250
🌐 Online fingerprint match: Ran-D

📊 SCAN RESULTATEN:
==================================================
📁 Totaal bestanden: 1250
🎵 Unieke artiesten: 89
⚠️  Bestanden zonder artiest: 23 (waarvan 15 via audio fingerprinting opgelost)
🔄 Bestanden op verkeerde locatie: 156
📋 Duplicaten: 12 groepen (28 bestanden)
==================================================
```

## 🚀 Toekomstige Verbeteringen

- [ ] Echte Shazam API integratie
- [ ] ACRCloud fingerprinting service
- [ ] Machine learning voor betere herkenning
- [ ] Batch processing voor grote collecties
- [ ] GPU versnelling voor audio analyse
- [ ] Cloud sync voor cache databases
- [ ] Real-time muziek herkenning
- [ ] Playlist generatie functionaliteit
- [ ] Muziek aanbevelingen
- [ ] Statistieken en analytics dashboard

---

**🎵 MP3 Organiser 0.1a** - Maak je muziek collectie perfect georganiseerd! ✨
