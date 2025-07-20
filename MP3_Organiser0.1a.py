# -*- coding: utf-8 -*-
# 🎵 MP3 Organiser 0.1a - Slimme Muziek Organisatie
# 📦 Imports
import os
import shutil
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, simpledialog
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from mutagen.easyid3 import EasyID3
import json
import time
from datetime import datetime
import hashlib
import sqlite3
from urllib.parse import quote
import numpy as np
from scipy.fft import fft

from scipy.signal import find_peaks
import librosa
import tempfile
import wave
import struct

# Optionele imports voor online functionaliteit
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("⚠️ requests module niet gevonden. Online database functionaliteit is beperkt.")

LIBROSA_AVAILABLE = False
try:
    import librosa
    LIBROSA_AVAILABLE = True
except ImportError:
    pass

SCIPY_AVAILABLE = False
try:
    from scipy.fft import fft
    from scipy.signal import find_peaks
    SCIPY_AVAILABLE = True
except ImportError:
    pass

class MP3Organizer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MP3 Organiser 0.1a")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Configuratie
        self.config = {
            'hierarchical': True,
            'include_albums': False,
            'include_years': False,
            'duplicate_check': True,
            'language': 'Nederlands',
            'font_size': 'Normaal',
            'font_family': 'Arial',
            'online_database': True,
            'ai_detection': True,
            'rename_files': False,
            'rename_format': 'artist_title',
            'duplicate_output': 'Duplicaten',
            'clean_title_format': True,
            'undo_enabled': True
        }
        
        # Online database instellingen
        self.online_db_config = {
            'lastfm_api_key': 'your_lastfm_api_key_here',  # Vervang met echte API key
            'musicbrainz_enabled': True,
            'discogs_enabled': True,
            'cache_enabled': True,
            'cache_duration': 86400,  # 24 uur in seconden
            'max_requests_per_minute': 30
        }
        
        # Lokale cache database initialiseren
        self.init_cache_database()
        
        # Request limiter voor API calls
        self.request_count = 0
        self.last_request_time = time.time()
        
        # Undo functionaliteit
        self.undo_stack = []  # Bewaart laatste bewerkingen
        self.max_undo_operations = 5  # Maximum aantal undo operaties
        
        # Taal vertalingen
        self.translations = {
            'Nederlands': {
                'title': 'MP3 Organiser 0.1a',
                'select_folder': '📁 Map om te Organiseren',
                'browse': 'Bladeren',
                'progress': '📊 Voortgang',
                'ready': 'Klaar om te organiseren',
                'log': '📝 Log',
                'start_org': '🎵 Start Organisatie',
                'scan_files': '🔍 Scan Bestanden',
                'find_duplicates': '🔍 Zoek Duplicaten',
                'clear_log': '🗑️ Log Wissen',
                'kill_switch': '🛑 Stop Alles',
                'settings': '⚙️ Instellingen',
                'theme': '🎨 Thema',
                'debug': '🐛 Debug',
                'org_options': '📁 Organisatie Opties',
                'hierarchical': 'Hiërarchische mappen (A/B/C/etc.)',
                'per_album': 'Per album organiseren',
                'per_year': 'Per jaar organiseren',
                'check_duplicates': 'Controleer duplicaten',
                'duplicate_action': 'Duplicaten behandeling:',
                'duplicate_explanation': 'ask = Vraag gebruiker, skip = Overslaan, overwrite = Overschrijven, rename = Hernoemen',
                'log_options': '📝 Log Opties',
                'log_size': 'Log venster grootte:',
                'auto_scroll': 'Auto-scroll inschakelen',
                'timestamp': 'Timestamps weergeven',
                'log_level': 'Log niveau:',
                'save_log': 'Log opslaan naar bestand',
                'language_options': '🌐 Taal & Lettergrootte',
                'program_language': 'Programma taal:',
                'font_size': 'Lettergrootte:',
                'font_family': 'Lettertype:',
                'preview': '👁️ Voorbeeld',
                'preview_text': 'Dit is een voorbeeld van hoe de tekst eruit zal zien met de gekozen instellingen.',
                'save': '💾 Opslaan',
                'cancel': '❌ Annuleren',
                'settings_saved': '⚙️ Instellingen opgeslagen',
                'error': 'Fout',
                'select_folder_first': 'Selecteer eerst een map om te organiseren!',
                'no_library': 'Geen muziek bibliotheek gevonden!',
                'duplicate_found': 'Duplicaat Gevonden',
                'duplicate_message': 'Bestand {filename} bestaat al in {artist}.\n\nJa = Overschrijven\nNee = Overslaan\nAnnuleren = Stoppen',
                'overwrite': 'Overschrijven',
                'skip': 'Overslaan',
                'cancel_operation': 'Annuleren',
                'overwrite_file': '⚠️ Overschrijft bestaand bestand: {filename}',
                'skip_duplicate': '⏭️ Overslaat duplicaat: {filename}',
                'operation_cancelled': '❌ Organisatie gestopt door gebruiker',
                'rename_duplicate': '🔄 Hernoemt duplicaat: {filename} → {new_filename}',
                'log_window_opened': '📝 Log venster geopend',
                'log_window_hidden': '📝 Log venster verborgen',
                'log_cleared': '🗑️ Log gewist',
                'log_window_title': 'Log',
                'close': 'Sluiten',
                'theme_changed': '🎨 Thema gewijzigd naar: {theme}',
                'debug_enabled': '🐛 Debug modus ingeschakeld',
                'debug_disabled': '🐛 Debug modus uitgeschakeld',
                'system_info': '🔍 Systeem informatie:',
                'path_info': '📁 Pad informatie:',
                'source_folder': '📂 Bron map: {path}',
                'library': '🎵 Bibliotheek: {path}',
                'work_dir': '📦 Werkmap: {path}',
                'not_selected': 'Niet geselecteerd',
                'not_detected': 'Niet gedetecteerd',
                'scanning_files': '🔍 Scannen van MP3 bestanden...',
                'found_files': 'Gevonden: {count} MP3 bestanden',
                'artists_found': '📊 Artiesten gevonden:',
                'artist_count': '  - {artist}: {count} nummers',
                'file_to_dest': '📁 {filename} → {dest_folder}',
                'searching_duplicates': '🔍 Zoeken naar duplicaten...',
                'no_mp3_files': '❌ Geen MP3 bestanden gevonden!',
                'duplicates_found': '🔍 {count} duplicaten gevonden:',
                'duplicate_file': '📁 {filename}:',
                'duplicate_path': '  - {path}',
                'no_duplicates': '✅ Geen duplicaten gevonden!',
                'duplicate_options': 'Duplicaten Gevonden',
                'duplicate_options_message': 'Er zijn {count} bestanden met duplicaten gevonden ({total} bestanden totaal).\n\nWat wilt u doen?\nJa = Verplaats duplicaten naar \'Duplicaten\' map\nNee = Verwijder duplicaten\nAnnuleren = Laat duplicaten zoals ze zijn',
                'move_duplicates': 'Verplaats naar duplicaten map',
                'delete_duplicates': 'Verwijder duplicaten',
                'leave_duplicates': 'Laat duplicaten zoals ze zijn',
                'moved_duplicate': '📁 Verplaatst: {filename} → Duplicaten/{new_filename}',
                'duplicates_moved': '✅ {count} duplicaten verplaatst naar: {folder}',
                'deleted_duplicate': '🗑️ Verwijderd: {filename}',
                'duplicates_deleted': '✅ {count} duplicaten verwijderd',
                'duplicates_unchanged': 'ℹ️ Duplicaten blijven zoals ze zijn',
                'error_moving_duplicates': '❌ Fout bij verplaatsen duplicaten: {error}',
                'error_deleting_duplicates': '❌ Fout bij verwijderen duplicaten: {error}',
                'error_processing_file': '❌ Fout bij {filename}: {error}',
                'error_organization': '❌ Fout tijdens organisatie: {error}',
                'organization_started': '🎵 Start organisatie...',
                'organization_completed': '🎉 Organisatie voltooid!',
                'organization_results': '📊 Resultaten:',
                'processed_count': 'Verwerkt: {current}/{total}',
                'organization_completed_status': 'Organisatie voltooid!',
                'searching_library': '🔍 Zoeken naar bestaande muziek bibliotheek...',
                'possible_library': '🎵 Mogelijke bibliotheek gevonden: {path} (score: {score})',
                'library_detected': '✅ Muziek bibliotheek gedetecteerd: {path}',
                'use_parent_folder': '📁 Gebruik ouder map als bibliotheek: {path}',
                'no_library_found': '❌ Geen muziek bibliotheek gevonden',
                'folder_selected': 'Map geselecteerd: {path}',
                'library_detected_log': '📁 Muziek bibliotheek gedetecteerd: {path}',
                'clean_title_format': 'Titels opschonen (cijfers en punten verwijderen)',
                'clean_title_explanation': 'Verwijdert cijfers en punten uit titels en formatteert zoals in ID3 tags',
                'undo_last_operation': '↩️ Ongedaan Maken',
                'undo_operation': 'Ongedaan maken van laatste bewerking',
                'undo_available': 'Ongedaan maken beschikbaar',
                'undo_not_available': 'Geen bewerking om ongedaan te maken',
                'undo_success': '✅ Laatste bewerking ongedaan gemaakt',
                'undo_error': '❌ Fout bij ongedaan maken',
                'undo_confirm': 'Weet je zeker dat je de laatste bewerking wilt ongedaan maken?'
            },
            'English': {
                'title': 'MP3 Organiser 0.1a',
                'select_folder': '📁 Folder to Organize',
                'browse': 'Browse',
                'progress': '📊 Progress',
                'ready': 'Ready to organize',
                'log': '📝 Log',
                'start_org': '🎵 Start Organization',
                'scan_files': '🔍 Scan Files',
                'find_duplicates': '🔍 Find Duplicates',
                'clear_log': '🗑️ Clear Log',
                'kill_switch': '🛑 Stop Everything',
                'settings': '⚙️ Settings',
                'theme': '🎨 Theme',
                'debug': '🐛 Debug',
                'org_options': '📁 Organization Options',
                'hierarchical': 'Hierarchical folders (A/B/C/etc.)',
                'per_album': 'Organize by album',
                'per_year': 'Organize by year',
                'check_duplicates': 'Check duplicates',
                'duplicate_action': 'Duplicate handling:',
                'duplicate_explanation': 'ask = Ask user, skip = Skip, overwrite = Overwrite, rename = Rename',
                'log_options': '📝 Log Options',
                'log_size': 'Log window size:',
                'auto_scroll': 'Enable auto-scroll',
                'timestamp': 'Show timestamps',
                'log_level': 'Log level:',
                'save_log': 'Save log to file',
                'language_options': '🌐 Language & Font Size',
                'program_language': 'Program language:',
                'font_size': 'Font size:',
                'font_family': 'Font family:',
                'preview': '👁️ Preview',
                'preview_text': 'This is an example of how the text will look with the chosen settings.',
                'save': '💾 Save',
                'cancel': '❌ Cancel',
                'settings_saved': '⚙️ Settings saved',
                'error': 'Error',
                'select_folder_first': 'Please select a folder to organize first!',
                'no_library': 'No music library found!',
                'duplicate_found': 'Duplicate Found',
                'duplicate_message': 'File {filename} already exists in {artist}.\n\nYes = Overwrite\nNo = Skip\nCancel = Stop',
                'overwrite': 'Overwrite',
                'skip': 'Skip',
                'cancel_operation': 'Cancel',
                'overwrite_file': '⚠️ Overwriting existing file: {filename}',
                'skip_duplicate': '⏭️ Skipping duplicate: {filename}',
                'operation_cancelled': '❌ Organization stopped by user',
                'rename_duplicate': '🔄 Renaming duplicate: {filename} → {new_filename}',
                'log_window_opened': '📝 Log window opened',
                'log_window_hidden': '📝 Log window hidden',
                'log_cleared': '🗑️ Log cleared',
                'log_window_title': 'Log',
                'close': 'Close',
                'theme_changed': '🎨 Theme changed to: {theme}',
                'debug_enabled': '🐛 Debug mode enabled',
                'debug_disabled': '🐛 Debug mode disabled',
                'system_info': '🔍 System information:',
                'path_info': '📁 Path information:',
                'source_folder': '📂 Source folder: {path}',
                'library': '🎵 Library: {path}',
                'work_dir': '📦 Work directory: {path}',
                'not_selected': 'Not selected',
                'not_detected': 'Not detected',
                'scanning_files': '🔍 Scanning MP3 files...',
                'found_files': 'Found: {count} MP3 files',
                'artists_found': '📊 Artists found:',
                'artist_count': '  - {artist}: {count} songs',
                'file_to_dest': '📁 {filename} → {dest_folder}',
                'searching_duplicates': '🔍 Searching for duplicates...',
                'no_mp3_files': '❌ No MP3 files found!',
                'duplicates_found': '🔍 {count} duplicates found:',
                'duplicate_file': '📁 {filename}:',
                'duplicate_path': '  - {path}',
                'no_duplicates': '✅ No duplicates found!',
                'duplicate_options': 'Duplicates Found',
                'duplicate_options_message': 'There are {count} files with duplicates found ({total} files total).\n\nWhat do you want to do?\nYes = Move duplicates to \'Duplicates\' folder\nNo = Delete duplicates\nCancel = Leave duplicates as they are',
                'move_duplicates': 'Move to duplicates folder',
                'delete_duplicates': 'Delete duplicates',
                'leave_duplicates': 'Leave duplicates as they are',
                'moved_duplicate': '📁 Moved: {filename} → Duplicates/{new_filename}',
                'duplicates_moved': '✅ {count} duplicates moved to: {folder}',
                'deleted_duplicate': '🗑️ Deleted: {filename}',
                'duplicates_deleted': '✅ {count} duplicates deleted',
                'duplicates_unchanged': 'ℹ️ Duplicates remain unchanged',
                'error_moving_duplicates': '❌ Error moving duplicates: {error}',
                'error_deleting_duplicates': '❌ Error deleting duplicates: {error}',
                'error_processing_file': '❌ Error processing {filename}: {error}',
                'error_organization': '❌ Error during organization: {error}',
                'organization_started': '🎵 Starting organization...',
                'organization_completed': '🎉 Organization completed!',
                'organization_results': '📊 Results:',
                'processed_count': 'Processed: {current}/{total}',
                'organization_completed_status': 'Organization completed!',
                'searching_library': '🔍 Searching for existing music library...',
                'possible_library': '🎵 Possible library found: {path} (score: {score})',
                'library_detected': '✅ Music library detected: {path}',
                'use_parent_folder': '📁 Using parent folder as library: {path}',
                'no_library_found': '❌ No music library found',
                'folder_selected': 'Folder selected: {path}',
                'library_detected_log': '📁 Music library detected: {path}',
                'clean_title_format': 'Clean title format (remove numbers and dots)',
                'clean_title_explanation': 'Removes numbers and dots from titles and formats like in ID3 tags',
                'undo_last_operation': '↩️ Undo Last Operation',
                'undo_operation': 'Undo last operation',
                'undo_available': 'Undo available',
                'undo_not_available': 'No operation to undo',
                'undo_success': '✅ Last operation undone',
                'undo_error': '❌ Error undoing operation',
                'undo_confirm': 'Are you sure you want to undo the last operation?'
            },
            'Deutsch': {
                'title': 'MP3 Organiser 0.1a',
                'select_folder': '📁 Ordner zum Organisieren',
                'browse': 'Durchsuchen',
                'progress': '📊 Fortschritt',
                'ready': 'Bereit zum Organisieren',
                'log': '📝 Protokoll',
                'start_org': '🎵 Organisation starten',
                'scan_files': '🔍 Dateien scannen',
                'find_duplicates': '🔍 Duplikate suchen',
                'clear_log': '🗑️ Protokoll löschen',
                'kill_switch': '🛑 Alles stoppen',
                'settings': '⚙️ Einstellungen',
                'theme': '🎨 Design',
                'debug': '🐛 Debug',
                'org_options': '📁 Organisationsoptionen',
                'hierarchical': 'Hierarchische Ordner (A/B/C/etc.)',
                'per_album': 'Nach Album organisieren',
                'per_year': 'Nach Jahr organisieren',
                'check_duplicates': 'Duplikate prüfen',
                'duplicate_action': 'Duplikat-Behandlung:',
                'duplicate_explanation': 'ask = Benutzer fragen, skip = Überspringen, overwrite = Überschreiben, rename = Umbenennen',
                'log_options': '📝 Protokoll-Optionen',
                'log_size': 'Protokoll-Fenstergröße:',
                'auto_scroll': 'Auto-Scroll aktivieren',
                'timestamp': 'Zeitstempel anzeigen',
                'log_level': 'Protokoll-Level:',
                'save_log': 'Protokoll in Datei speichern',
                'language_options': '🌐 Sprache & Schriftgröße',
                'program_language': 'Programmsprache:',
                'font_size': 'Schriftgröße:',
                'font_family': 'Schriftart:',
                'preview': '👁️ Vorschau',
                'preview_text': 'Dies ist ein Beispiel, wie der Text mit den gewählten Einstellungen aussehen wird.',
                'save': '💾 Speichern',
                'cancel': '❌ Abbrechen',
                'settings_saved': '⚙️ Einstellungen gespeichert',
                'error': 'Fehler',
                'select_folder_first': 'Bitte wählen Sie zuerst einen Ordner zum Organisieren!',
                'no_library': 'Keine Musikbibliothek gefunden!',
                'duplicate_found': 'Duplikat gefunden',
                'duplicate_message': 'Datei {filename} existiert bereits in {artist}.\n\nJa = Überschreiben\nNein = Überspringen\nAbbrechen = Stoppen',
                'overwrite': 'Überschreiben',
                'skip': 'Überspringen',
                'cancel_operation': 'Abbrechen',
                'overwrite_file': '⚠️ Überschreibt vorhandene Datei: {filename}',
                'skip_duplicate': '⏭️ Überspringt Duplikat: {filename}',
                'operation_cancelled': '❌ Organisation vom Benutzer gestoppt',
                'rename_duplicate': '🔄 Benennt Duplikat um: {filename} → {new_filename}',
                'log_window_opened': '📝 Protokoll-Fenster geöffnet',
                'log_window_hidden': '📝 Protokoll-Fenster versteckt',
                'log_cleared': '🗑️ Protokoll gelöscht',
                'log_window_title': 'Protokoll',
                'close': 'Schließen',
                'theme_changed': '🎨 Design geändert zu: {theme}',
                'debug_enabled': '🐛 Debug-Modus aktiviert',
                'debug_disabled': '🐛 Debug-Modus deaktiviert',
                'system_info': '🔍 Systeminformationen:',
                'path_info': '📁 Pfadinformationen:',
                'source_folder': '📂 Quellordner: {path}',
                'library': '🎵 Bibliothek: {path}',
                'work_dir': '📦 Arbeitsverzeichnis: {path}',
                'not_selected': 'Nicht ausgewählt',
                'not_detected': 'Nicht erkannt',
                'scanning_files': '🔍 MP3-Dateien scannen...',
                'found_files': 'Gefunden: {count} MP3-Dateien',
                'artists_found': '📊 Künstler gefunden:',
                'artist_count': '  - {artist}: {count} Lieder',
                'file_to_dest': '📁 {filename} → {dest_folder}',
                'searching_duplicates': '🔍 Nach Duplikaten suchen...',
                'no_mp3_files': '❌ Keine MP3-Dateien gefunden!',
                'duplicates_found': '🔍 {count} Duplikate gefunden:',
                'duplicate_file': '📁 {filename}:',
                'duplicate_path': '  - {path}',
                'no_duplicates': '✅ Keine Duplikate gefunden!',
                'duplicate_options': 'Duplikate gefunden',
                'duplicate_options_message': 'Es wurden {count} Dateien mit Duplikaten gefunden ({total} Dateien insgesamt).\n\nWas möchten Sie tun?\nJa = Duplikate in \'Duplikate\'-Ordner verschieben\nNein = Duplikate löschen\nAbbrechen = Duplikate unverändert lassen',
                'move_duplicates': 'In Duplikate-Ordner verschieben',
                'delete_duplicates': 'Duplikate löschen',
                'leave_duplicates': 'Duplikate unverändert lassen',
                'moved_duplicate': '📁 Verschoben: {filename} → Duplikate/{new_filename}',
                'duplicates_moved': '✅ {count} Duplikate verschoben nach: {folder}',
                'deleted_duplicate': '🗑️ Gelöscht: {filename}',
                'duplicates_deleted': '✅ {count} Duplikate gelöscht',
                'duplicates_unchanged': 'ℹ️ Duplikate bleiben unverändert',
                'error_moving_duplicates': '❌ Fehler beim Verschieben von Duplikaten: {error}',
                'error_deleting_duplicates': '❌ Fehler beim Löschen von Duplikaten: {error}',
                'error_processing_file': '❌ Fehler bei {filename}: {error}',
                'error_organization': '❌ Fehler während der Organisation: {error}',
                'organization_started': '🎵 Organisation startet...',
                'organization_completed': '🎉 Organisation abgeschlossen!',
                'organization_results': '📊 Ergebnisse:',
                'processed_count': 'Verarbeitet: {current}/{total}',
                'organization_completed_status': 'Organisation abgeschlossen!',
                'searching_library': '🔍 Nach bestehender Musikbibliothek suchen...',
                'possible_library': '🎵 Mögliche Bibliothek gefunden: {path} (Punktzahl: {score})',
                'library_detected': '✅ Musikbibliothek erkannt: {path}',
                'use_parent_folder': '📁 Verwende übergeordneten Ordner als Bibliothek: {path}',
                'no_library_found': '❌ Keine Musikbibliothek gefunden',
                'folder_selected': 'Ordner ausgewählt: {path}',
                'library_detected_log': '📁 Musikbibliothek erkannt: {path}'
            },
            'Français': {
                'title': 'MP3 Organiser 0.1a',
                'select_folder': '📁 Dossier à Organiser',
                'browse': 'Parcourir',
                'progress': '📊 Progression',
                'ready': 'Prêt à organiser',
                'log': '📝 Journal',
                'start_org': '🎵 Démarrer l\'Organisation',
                'scan_files': '🔍 Scanner les Fichiers',
                'find_duplicates': '🔍 Trouver les Doublons',
                'clear_log': '🗑️ Effacer le Journal',
                'kill_switch': '🛑 Tout arrêter',
                'settings': '⚙️ Paramètres',
                'theme': '🎨 Thème',
                'debug': '🐛 Débogage',
                'org_options': '📁 Options d\'Organisation',
                'hierarchical': 'Dossiers hiérarchiques (A/B/C/etc.)',
                'per_album': 'Organiser par album',
                'per_year': 'Organiser par année',
                'check_duplicates': 'Vérifier les doublons',
                'duplicate_action': 'Traitement des doublons:',
                'duplicate_explanation': 'ask = Demander à l\'utilisateur, skip = Ignorer, overwrite = Écraser, rename = Renommer',
                'log_options': '📝 Options du Journal',
                'log_size': 'Taille de fenêtre du journal:',
                'auto_scroll': 'Activer le défilement automatique',
                'timestamp': 'Afficher les horodatages',
                'log_level': 'Niveau du journal:',
                'save_log': 'Sauvegarder le journal dans un fichier',
                'language_options': '🌐 Langue & Taille de Police',
                'program_language': 'Langue du programme:',
                'font_size': 'Taille de police:',
                'font_family': 'Famille de police:',
                'preview': '👁️ Aperçu',
                'preview_text': 'Ceci est un exemple de l\'apparence du texte avec les paramètres choisis.',
                'save': '💾 Enregistrer',
                'cancel': '❌ Annuler',
                'settings_saved': '⚙️ Paramètres enregistrés',
                'error': 'Erreur',
                'select_folder_first': 'Veuillez d\'abord sélectionner un dossier à organiser!',
                'no_library': 'Aucune bibliothèque musicale trouvée!',
                'duplicate_found': 'Doublon trouvé',
                'duplicate_message': 'Le fichier {filename} existe déjà dans {artist}.\n\nOui = Écraser\nNon = Ignorer\nAnnuler = Arrêter',
                'overwrite': 'Écraser',
                'skip': 'Ignorer',
                'cancel_operation': 'Annuler',
                'overwrite_file': '⚠️ Écrase le fichier existant: {filename}',
                'skip_duplicate': '⏭️ Ignore le doublon: {filename}',
                'operation_cancelled': '❌ Organisation arrêtée par l\'utilisateur',
                'rename_duplicate': '🔄 Renomme le doublon: {filename} → {new_filename}',
                'log_window_opened': '📝 Fenêtre de journal ouverte',
                'log_window_hidden': '📝 Fenêtre de journal masquée',
                'log_cleared': '🗑️ Journal effacé',
                'log_window_title': 'Journal',
                'close': 'Fermer',
                'theme_changed': '🎨 Thème changé vers: {theme}',
                'debug_enabled': '🐛 Mode débogage activé',
                'debug_disabled': '🐛 Mode débogage désactivé',
                'system_info': '🔍 Informations système:',
                'path_info': '📁 Informations de chemin:',
                'source_folder': '📂 Dossier source: {path}',
                'library': '🎵 Bibliothèque: {path}',
                'work_dir': '📦 Répertoire de travail: {path}',
                'not_selected': 'Non sélectionné',
                'not_detected': 'Non détecté',
                'scanning_files': '🔍 Analyse des fichiers MP3...',
                'found_files': 'Trouvé: {count} fichiers MP3',
                'artists_found': '📊 Artistes trouvés:',
                'artist_count': '  - {artist}: {count} chansons',
                'file_to_dest': '📁 {filename} → {dest_folder}',
                'searching_duplicates': '🔍 Recherche de doublons...',
                'no_mp3_files': '❌ Aucun fichier MP3 trouvé!',
                'duplicates_found': '🔍 {count} doublons trouvés:',
                'duplicate_file': '📁 {filename}:',
                'duplicate_path': '  - {path}',
                'no_duplicates': '✅ Aucun doublon trouvé!',
                'duplicate_options': 'Doublons trouvés',
                'duplicate_options_message': 'Il y a {count} fichiers avec des doublons trouvés ({total} fichiers au total).\n\nQue voulez-vous faire?\nOui = Déplacer les doublons vers le dossier \'Doublons\'\nNon = Supprimer les doublons\nAnnuler = Laisser les doublons tels quels',
                'move_duplicates': 'Déplacer vers le dossier doublons',
                'delete_duplicates': 'Supprimer les doublons',
                'leave_duplicates': 'Laisser les doublons tels quels',
                'moved_duplicate': '📁 Déplacé: {filename} → Doublons/{new_filename}',
                'duplicates_moved': '✅ {count} doublons déplacés vers: {folder}',
                'deleted_duplicate': '🗑️ Supprimé: {filename}',
                'duplicates_deleted': '✅ {count} doublons supprimés',
                'duplicates_unchanged': 'ℹ️ Les doublons restent inchangés',
                'error_moving_duplicates': '❌ Erreur lors du déplacement des doublons: {error}',
                'error_deleting_duplicates': '❌ Erreur lors de la suppression des doublons: {error}',
                'error_processing_file': '❌ Erreur lors du traitement de {filename}: {error}',
                'error_organization': '❌ Erreur lors de l\'organisation: {error}',
                'organization_started': '🎵 Début de l\'organisation...',
                'organization_completed': '🎉 Organisation terminée!',
                'organization_results': '📊 Résultats:',
                'processed_count': 'Traité: {current}/{total}',
                'organization_completed_status': 'Organisation terminée!',
                'searching_library': '🔍 Recherche de bibliothèque musicale existante...',
                'possible_library': '🎵 Bibliothèque possible trouvée: {path} (score: {score})',
                'library_detected': '✅ Bibliothèque musicale détectée: {path}',
                'use_parent_folder': '📁 Utiliser le dossier parent comme bibliothèque: {path}',
                'no_library_found': '❌ Aucune bibliothèque musicale trouvée',
                'folder_selected': 'Dossier sélectionné: {path}',
                'library_detected_log': '📁 Bibliothèque musicale détectée: {path}'
            },
            'Español': {
                'title': 'MP3 Organiser 0.1a',
                'select_folder': '📁 Carpeta para Organizar',
                'browse': 'Examinar',
                'progress': '📊 Progreso',
                'ready': 'Listo para organizar',
                'log': '📝 Registro',
                'start_org': '🎵 Iniciar Organización',
                'scan_files': '🔍 Escanear Archivos',
                'find_duplicates': '🔍 Buscar Duplicados',
                'clear_log': '🗑️ Limpiar Registro',
                'kill_switch': '🛑 Detener Todo',
                'settings': '⚙️ Configuración',
                'theme': '🎨 Tema',
                'debug': '🐛 Depuración',
                'org_options': '📁 Opciones de Organización',
                'hierarchical': 'Carpetas jerárquicas (A/B/C/etc.)',
                'per_album': 'Organizar por álbum',
                'per_year': 'Organizar por año',
                'check_duplicates': 'Verificar duplicados',
                'duplicate_action': 'Manejo de duplicados:',
                'duplicate_explanation': 'ask = Preguntar al usuario, skip = Omitir, overwrite = Sobrescribir, rename = Renombrar',
                'log_options': '📝 Opciones de Registro',
                'log_size': 'Tamaño de ventana de registro:',
                'auto_scroll': 'Habilitar auto-scroll',
                'timestamp': 'Mostrar marcas de tiempo',
                'log_level': 'Nivel de registro:',
                'save_log': 'Guardar registro en archivo',
                'language_options': '🌐 Idioma & Tamaño de Fuente',
                'program_language': 'Idioma del programa:',
                'font_size': 'Tamaño de fuente:',
                'font_family': 'Familia de fuente:',
                'preview': '👁️ Vista previa',
                'preview_text': 'Este es un ejemplo de cómo se verá el texto con la configuración elegida.',
                'save': '💾 Guardar',
                'cancel': '❌ Cancelar',
                'settings_saved': '⚙️ Configuración guardada',
                'error': 'Error',
                'select_folder_first': '¡Por favor seleccione una carpeta para organizar primero!',
                'no_library': '¡No se encontró biblioteca de música!',
                'duplicate_found': 'Duplicado encontrado',
                'duplicate_message': 'El archivo {filename} ya existe en {artist}.\n\nSí = Sobrescribir\nNo = Omitir\nCancelar = Detener',
                'overwrite': 'Sobrescribir',
                'skip': 'Omitir',
                'cancel_operation': 'Cancelar',
                'overwrite_file': '⚠️ Sobrescribe archivo existente: {filename}',
                'skip_duplicate': '⏭️ Omite duplicado: {filename}',
                'operation_cancelled': '❌ Organización detenida por el usuario',
                'rename_duplicate': '🔄 Renombra duplicado: {filename} → {new_filename}',
                'log_window_opened': '📝 Ventana de registro abierta',
                'log_window_hidden': '📝 Ventana de registro oculta',
                'log_cleared': '🗑️ Registro limpiado',
                'log_window_title': 'Registro',
                'close': 'Cerrar',
                'theme_changed': '🎨 Tema cambiado a: {theme}',
                'debug_enabled': '🐛 Modo debug habilitado',
                'debug_disabled': '🐛 Modo debug deshabilitado',
                'system_info': '🔍 Información del sistema:',
                'path_info': '📁 Información de ruta:',
                'source_folder': '📂 Carpeta fuente: {path}',
                'library': '🎵 Biblioteca: {path}',
                'work_dir': '📦 Directorio de trabajo: {path}',
                'not_selected': 'No seleccionado',
                'not_detected': 'No detectado',
                'scanning_files': '🔍 Escaneando archivos MP3...',
                'found_files': 'Encontrado: {count} archivos MP3',
                'artists_found': '📊 Artistas encontrados:',
                'artist_count': '  - {artist}: {count} canciones',
                'file_to_dest': '📁 {filename} → {dest_folder}',
                'searching_duplicates': '🔍 Buscando duplicados...',
                'no_mp3_files': '❌ ¡No se encontraron archivos MP3!',
                'duplicates_found': '🔍 {count} duplicados encontrados:',
                'duplicate_file': '📁 {filename}:',
                'duplicate_path': '  - {path}',
                'no_duplicates': '✅ ¡No se encontraron duplicados!',
                'duplicate_options': 'Duplicados encontrados',
                'duplicate_options_message': 'Hay {count} archivos con duplicados encontrados ({total} archivos en total).\n\n¿Qué desea hacer?\nSí = Mover duplicados a carpeta \'Duplicados\'\nNo = Eliminar duplicados\nCancelar = Dejar duplicados como están',
                'move_duplicates': 'Mover a carpeta duplicados',
                'delete_duplicates': 'Eliminar duplicados',
                'leave_duplicates': 'Dejar duplicados como están',
                'moved_duplicate': '📁 Movido: {filename} → Duplicados/{new_filename}',
                'duplicates_moved': '✅ {count} duplicados movidos a: {folder}',
                'deleted_duplicate': '🗑️ Eliminado: {filename}',
                'duplicates_deleted': '✅ {count} duplicados eliminados',
                'duplicates_unchanged': 'ℹ️ Los duplicados permanecen sin cambios',
                'error_moving_duplicates': '❌ Error moviendo duplicados: {error}',
                'error_deleting_duplicates': '❌ Error eliminando duplicados: {error}',
                'error_processing_file': '❌ Error procesando {filename}: {error}',
                'error_organization': '❌ Error durante la organización: {error}',
                'organization_started': '🎵 Iniciando organización...',
                'organization_completed': '🎉 ¡Organización completada!',
                'organization_results': '📊 Resultados:',
                'processed_count': 'Procesado: {current}/{total}',
                'organization_completed_status': '¡Organización completada!',
                'searching_library': '🔍 Buscando biblioteca de música existente...',
                'possible_library': '🎵 Biblioteca posible encontrada: {path} (puntuación: {score})',
                'library_detected': '✅ Biblioteca de música detectada: {path}',
                'use_parent_folder': '📁 Usando carpeta padre como biblioteca: {path}',
                'no_library_found': '❌ No se encontró biblioteca de música',
                'folder_selected': 'Carpeta seleccionada: {path}',
                'library_detected_log': '📁 Biblioteca de música detectada: {path}'
            }
        }
        
        # Font grootte mapping
        self.font_sizes = {
            'Klein': 8,
            'Normaal': 10,
            'Groot': 12,
            'Extra Groot': 14
        }
        
        # Interne bibliotheek variabele
        self.detected_library = None
        
        # Thema configuratie
        self.themes = {
            "light": {
                "bg": "#f0f0f0",
                "fg": "#000000",
                "button_bg": "#4CAF50",
                "button_fg": "#ffffff",
                "entry_bg": "#ffffff",
                "text_bg": "#ffffff",
                "label_fg": "#000000",
                "checkbutton_fg": "#000000"
            },
            "dark": {
                "bg": "#2d2d2d",
                "fg": "#ffffff",
                "button_bg": "#4CAF50",
                "button_fg": "#ffffff",
                "entry_bg": "#404040",
                "text_bg": "#404040",
                "label_fg": "#ffffff",
                "checkbutton_fg": "#ffffff"
            },
            "blue": {
                "bg": "#e3f2fd",
                "fg": "#0d47a1",
                "button_bg": "#1565c0",
                "button_fg": "#ffffff",
                "entry_bg": "#ffffff",
                "text_bg": "#ffffff",
                "label_fg": "#0d47a1",
                "checkbutton_fg": "#0d47a1"
            },
            "green": {
                "bg": "#e8f5e8",
                "fg": "#1b5e20",
                "button_bg": "#2e7d32",
                "button_fg": "#ffffff",
                "entry_bg": "#ffffff",
                "text_bg": "#ffffff",
                "label_fg": "#1b5e20",
                "checkbutton_fg": "#1b5e20"
            },
            "orange": {
                "bg": "#fff3e0",
                "fg": "#bf360c",
                "button_bg": "#e65100",
                "button_fg": "#ffffff",
                "entry_bg": "#ffffff",
                "text_bg": "#ffffff",
                "label_fg": "#bf360c",
                "checkbutton_fg": "#bf360c"
            }
        }
        self.current_theme = "light"
        
        # Huidige taal en font instellingen (standaard Nederlands)
        self.current_language = 'Nederlands'
        self.current_font_size = self.config.get('font_size', 'Normaal')
        self.current_font_family = self.config.get('font_family', 'Arial')
        
        # Kill switch variabelen
        self.stop_processing = False
        self.current_thread = None
        
        # Laad configuratie bij startup
        self.load_config()
        
        # Pas taal en font toe bij startup
        if self.current_language in self.translations:
            self.update_ui_language()
        if self.current_font_size in self.font_sizes:
            self.update_ui_font()
        
        # Artiest database
        self.artist_patterns = {
            'barry white': [
                "let's get it on", "can't get enough", 
                "you're the first", "never gonna give you up",
                "just the way you are", "practice what you preach",
                "love's theme", "i'm gonna love you just a little more baby"
            ],
            'michael jackson': [
                "thriller", "billie jean", "beat it", "smooth criminal",
                "man in the mirror", "black or white", "bad", "dangerous"
            ],
            'queen': [
                "bohemian rhapsody", "we will rock you", "another one bites the dust",
                "don't stop me now", "somebody to love", "killer queen"
            ],
            'the beatles': [
                "let it be", "hey jude", "yesterday", "help", "a hard day's night",
                "eleanor rigby", "yellow submarine", "all you need is love"
            ],
            'led zeppelin': [
                "stairway to heaven", "whole lotta love", "black dog", "kashmir",
                "rock and roll", "immigrant song", "since i've been loving you"
            ],
            'pink floyd': [
                "comfortably numb", "wish you were here", "another brick in the wall",
                "money", "time", "shine on you crazy diamond"
            ]
        }
        
        self.load_config()
        self.setup_ui()
        
        # Knoppen zijn al in de juiste taal aangemaakt
    
    def setup_ui(self):
        """Maakt de gebruikersinterface aan"""
        
        # Menubalk
        self.create_menu()
        
        # Hoofdframe
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Titel
        title_label = tk.Label(main_frame, text="🎵 MP3 Organiser 0.1a", 
                              font=('Arial', 16, 'bold'), bg='#f0f0f0')
        title_label.pack(pady=(0, 20))
        
        # Map selectie
        source_frame = tk.LabelFrame(main_frame, text="📁 Map om te Organiseren", bg='#f0f0f0')
        source_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.source_var = tk.StringVar()
        source_entry = tk.Entry(source_frame, textvariable=self.source_var, width=50)
        source_entry.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
        
        source_btn = tk.Button(source_frame, text="Bladeren", command=self.select_source_folder, 
                              bg='#4CAF50', fg='#000000')
        source_btn.pack(side=tk.RIGHT, padx=5, pady=5)
        
        # Instellingen variabelen (verborgen in hoofdvenster)
        self.hierarchical_var = tk.BooleanVar(value=True)
        self.albums_var = tk.BooleanVar(value=False)
        self.years_var = tk.BooleanVar(value=False)
        self.duplicate_check_var = tk.BooleanVar(value=True)
        

        
        # Progress frame
        self.progress_frame = tk.LabelFrame(main_frame, text="📊 Voortgang", bg='#f0f0f0')
        self.progress_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.progress_var = tk.StringVar(value="Klaar om te organiseren")
        progress_label = tk.Label(self.progress_frame, textvariable=self.progress_var, bg='#f0f0f0')
        progress_label.pack(pady=5)
        
        self.progress_bar = ttk.Progressbar(self.progress_frame, mode='determinate')
        self.progress_bar.pack(fill=tk.X, padx=5, pady=5)
        
        # Log venster (apart venster)
        self.log_window = None
        self.log_text = None
        
        # Knoppen frame
        self.button_frame = tk.Frame(main_frame, bg='#f0f0f0')
        self.button_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Scan Bestanden knop (eerste)
        self.scan_btn = tk.Button(self.button_frame, text=self.get_text('scan_files'), 
                                 command=self.scan_files, bg='#2196F3', fg='white',
                                 width=15, height=1, font=('Arial', 10))
        self.scan_btn.pack(pady=3, fill=tk.X, padx=10)
        
        # Start Organisatie knop
        self.organize_btn = tk.Button(self.button_frame, text=self.get_text('start_org'), 
                                     command=self.start_organization, bg='#4CAF50', fg='white',
                                     width=15, height=1, font=('Arial', 10))
        self.organize_btn.pack(pady=3, fill=tk.X, padx=10)
        
        # Hernoem Bestanden knop
        self.rename_btn = tk.Button(self.button_frame, text="✏️ Hernoem Bestanden", 
                                   command=self.start_rename_files, bg='#9C27B0', fg='white',
                                   width=15, height=1, font=('Arial', 10))
        self.rename_btn.pack(pady=3, fill=tk.X, padx=10)
        
        # Verwerk Duplicaten knop
        self.duplicate_btn = tk.Button(self.button_frame, text="🔄 Verwerk Duplicaten", 
                                     command=self.process_duplicates, bg='#FF9800', fg='white',
                                     width=15, height=1, font=('Arial', 10))
        self.duplicate_btn.pack(pady=3, fill=tk.X, padx=10)
        
        # Ongedaan Maken knop
        self.undo_btn = tk.Button(self.button_frame, text=self.get_text('undo_last_operation'), 
                                 command=self.undo_last_operation, bg='#607D8B', fg='white',
                                 width=15, height=1, font=('Arial', 10))
        self.undo_btn.pack(pady=3, fill=tk.X, padx=10)
        
        # Kill Switch knop
        self.kill_switch_btn = tk.Button(self.button_frame, text=self.get_text('kill_switch'), 
                                       command=self.kill_switch, bg='#d32f2f', fg='white',
                                       width=15, height=1, font=('Arial', 10))
        self.kill_switch_btn.pack(pady=3, fill=tk.X, padx=10)
        
        # Bewaar referenties naar alle knoppen voor blokkeren/vrijgeven
        self.all_buttons = [self.scan_btn, self.organize_btn, self.rename_btn, self.duplicate_btn, self.undo_btn]
        self.all_entries = [source_entry]
        self.all_menus = [self.menubar]
    
    def block_gui(self):
        """Blokkeert alle GUI elementen behalve stop knop en log venster"""
        # Blokkeer knoppen
        for btn in self.all_buttons:
            btn.config(state=tk.DISABLED)
        
        # Blokkeer entry velden
        for entry in self.all_entries:
            entry.config(state=tk.DISABLED)
        
        # Blokkeer menu's
        for menu in self.all_menus:
            menu.entryconfig("⚙️ Instellingen", state=tk.DISABLED)
            menu.entryconfig("🎨 Thema", state=tk.DISABLED)
            # Debug menu blijft actief voor log venster
            # menu.entryconfig("🐛 Debug", state=tk.DISABLED)
        
        # Blokkeer bladeren knop
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, tk.LabelFrame):
                        for grandchild in child.winfo_children():
                            if isinstance(grandchild, tk.Button) and grandchild.cget("text") == "Bladeren":
                                grandchild.config(state=tk.DISABLED)
    
    def unblock_gui(self):
        """Geeft alle GUI elementen vrij"""
        # Vrijgeven knoppen
        for btn in self.all_buttons:
            btn.config(state=tk.NORMAL)
        
        # Vrijgeven entry velden
        for entry in self.all_entries:
            entry.config(state=tk.NORMAL)
        
        # Vrijgeven menu's
        for menu in self.all_menus:
            menu.entryconfig("⚙️ Instellingen", state=tk.NORMAL)
            menu.entryconfig("🎨 Thema", state=tk.NORMAL)
            # menu.entryconfig("🐛 Debug", state=tk.NORMAL)
        
        # Vrijgeven bladeren knop
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, tk.LabelFrame):
                        for grandchild in child.winfo_children():
                            if isinstance(grandchild, tk.Button) and grandchild.cget("text") == "Bladeren":
                                grandchild.config(state=tk.NORMAL)
    
    def select_source_folder(self):
        """Selecteert map om te organiseren en detecteert automatisch bibliotheek"""
        folder = filedialog.askdirectory(title="Selecteer map met MP3 bestanden om te organiseren")
        if folder:
            self.source_var.set(folder)
            self.log_message(f"Map geselecteerd: {folder}")
            
            # Automatisch bibliotheek detecteren
            self.detect_music_library()
            self.log_message(f"📁 Muziek bibliotheek gedetecteerd: {self.detected_library}")
    
    def select_duplicate_output_folder(self):
        """Selecteert output map voor duplicaten"""
        # Bewaar referentie naar het huidige venster
        current_window = None
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Toplevel) and widget.title().startswith("⚙️ MP3 Organiser - Instellingen"):
                current_window = widget
                break
        
        # Maak een tijdelijke modal dialog voor de folder selectie
        if current_window:
            # Maak het instellingen venster tijdelijk niet-modal
            current_window.grab_release()
            
            # Open folder dialog
            folder = filedialog.askdirectory(title="Selecteer duplicaten output map")
            
            # Herstel modal state
            current_window.grab_set()
            current_window.focus_force()
        else:
            # Fallback als venster niet gevonden
            folder = filedialog.askdirectory(title="Selecteer duplicaten output map")
        
        if folder:
            self.duplicate_output_var.set(folder)
            self.log_message(f"📁 Duplicaten output map geselecteerd: {folder}")
    
    def create_menu(self):
        """Maakt de menubalk aan"""
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)
        
        # Instellingen menu
        settings_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="⚙️ Instellingen", menu=settings_menu)
        settings_menu.add_command(label="🔧 Instellingen", command=self.show_settings)
        
        # Thema menu
        theme_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="🎨 Thema", menu=theme_menu)
        theme_menu.add_command(label="🌞 Light Theme", command=lambda: self.change_theme("light"))
        theme_menu.add_command(label="🌙 Dark Theme", command=lambda: self.change_theme("dark"))
        theme_menu.add_command(label="🌊 Blue Theme", command=lambda: self.change_theme("blue"))
        theme_menu.add_command(label="🌿 Green Theme", command=lambda: self.change_theme("green"))
        theme_menu.add_command(label="🔥 Orange Theme", command=lambda: self.change_theme("orange"))
        
        # Debug menu
        debug_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="🐛 Debug", menu=debug_menu)
        debug_menu.add_command(label="📝 Log", command=self.toggle_log)
    
    def change_theme(self, theme_name):
        """Verandert het thema van de applicatie"""
        if theme_name in self.themes:
            self.current_theme = theme_name
            theme = self.themes[theme_name]
            
            # Update hoofdframe
            for widget in self.root.winfo_children():
                if isinstance(widget, tk.Frame):
                    widget.configure(bg=theme["bg"])
                    self.update_widget_colors(widget, theme)
            
            self.log_message(f"🎨 Thema gewijzigd naar: {theme_name}")
            
            # Update log venster thema als het open is
            if self.log_window and self.log_window.winfo_exists():
                self.update_log_window_theme()
            
            # Update instellingen venster thema als het open is
            for widget in self.root.winfo_children():
                if isinstance(widget, tk.Toplevel) and widget.title().startswith("⚙️ MP3 Organiser - Instellingen"):
                    self.update_settings_window_theme(widget)
    
    def update_widget_colors(self, widget, theme):
        """Update kleuren van widgets recursief"""
        try:
            widget.configure(bg=theme["bg"])
        except:
            pass
        
        for child in widget.winfo_children():
            try:
                if isinstance(child, tk.Label):
                    # Forceer witte tekst in dark theme
                    if self.current_theme == "dark":
                        child.configure(bg=theme["bg"], fg="#ffffff")
                    else:
                        child.configure(bg=theme["bg"], fg=theme.get("label_fg", theme["fg"]))
                elif isinstance(child, tk.Button):
                    # Speciale behandeling voor help knoppen en bladeren knop
                    if child.cget("text") == "?" or child.cget("text") == "Bladeren":
                        if self.current_theme == "dark":
                            child.configure(bg=theme["button_bg"], fg="#ffffff")
                        else:
                            child.configure(bg=theme["button_bg"], fg="#000000")
                    else:
                        # Forceer witte tekst op knoppen in dark theme
                        if self.current_theme == "dark":
                            child.configure(bg=theme["button_bg"], fg="#ffffff")
                        else:
                            child.configure(bg=theme["button_bg"], fg=theme["button_fg"])
                elif isinstance(child, tk.Entry):
                    child.configure(bg=theme["entry_bg"], fg=theme["fg"])
                elif isinstance(child, tk.Text):
                    child.configure(bg=theme["text_bg"], fg=theme["fg"])
                elif isinstance(child, tk.Checkbutton):
                    # Forceer witte tekst in dark theme
                    if self.current_theme == "dark":
                        child.configure(bg=theme["bg"], fg="#ffffff")
                    else:
                        child.configure(bg=theme["bg"], fg=theme.get("checkbutton_fg", theme["fg"]))
                elif isinstance(child, tk.LabelFrame):
                    child.configure(bg=theme["bg"])
                elif isinstance(child, tk.StringVar):
                    # Skip StringVar objects
                    pass
                else:
                    child.configure(bg=theme["bg"])
            except:
                pass
            
            self.update_widget_colors(child, theme)
    
    def show_settings(self):
        """Toont instellingen venster"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("⚙️ MP3 Organiser - Instellingen")
        settings_window.geometry("700x500")
        settings_window.configure(bg=self.themes[self.current_theme]["bg"])
        
        # Zorg ervoor dat het venster altijd op de voorgrond blijft
        settings_window.transient(self.root)  # Maak het venster afhankelijk van hoofdvenster
        settings_window.grab_set()  # Zet focus vast
        settings_window.focus_force()  # Forceer focus
        
        # Hoofdtitel
        title_label = tk.Label(settings_window, text="🔧 MP3 Organiser Instellingen", 
                              font=('Arial', 16, 'bold'), bg=self.themes[self.current_theme]["bg"], 
                              fg=self.themes[self.current_theme]["fg"])
        title_label.pack(pady=10)
        
        # Hoofdframe voor tabs met scrollbar
        main_frame = tk.Frame(settings_window, bg=self.themes[self.current_theme]["bg"])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Linker frame voor tab knoppen
        left_frame = tk.Frame(main_frame, bg=self.themes[self.current_theme]["bg"], width=150)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_frame.pack_propagate(False)
        
        # Rechter frame voor content met scrollbar
        right_container = tk.Frame(main_frame, bg=self.themes[self.current_theme]["bg"])
        right_container.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Canvas en scrollbar voor scrollbare content
        canvas = tk.Canvas(right_container, bg=self.themes[self.current_theme]["bg"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(right_container, orient="vertical", command=canvas.yview)
        right_frame = tk.Frame(canvas, bg=self.themes[self.current_theme]["bg"])
        
        # Configureer canvas
        right_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=right_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Tab knoppen
        org_btn = tk.Button(left_frame, text=self.get_text('org_options'), 
                           command=lambda: self.show_org_settings(right_frame), 
                           bg='#4CAF50', fg='white', width=15, height=2)
        org_btn.pack(pady=5)
        
        log_btn = tk.Button(left_frame, text=self.get_text('log_options'), 
                           command=lambda: self.show_log_settings(right_frame), 
                           bg='#2196F3', fg='white', width=15, height=2)
        log_btn.pack(pady=5)
        
        lang_btn = tk.Button(left_frame, text=self.get_text('language_options'), 
                            command=lambda: self.show_language_settings(right_frame), 
                            bg='#FF9800', fg='white', width=15, height=2)
        lang_btn.pack(pady=5)
        
        online_btn = tk.Button(left_frame, text="🌐 Online Database", 
                              command=lambda: self.show_online_settings(right_frame), 
                              bg='#9C27B0', fg='white', width=15, height=2)
        online_btn.pack(pady=5)
        
        # Pack canvas en scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind muis scroll events
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Bind focus events voor scrollbar
        def _on_enter(event):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        def _on_leave(event):
            canvas.unbind_all("<MouseWheel>")
        
        canvas.bind("<Enter>", _on_enter)
        canvas.bind("<Leave>", _on_leave)
        
        # Knoppen frame
        button_frame = tk.Frame(settings_window, bg=self.themes[self.current_theme]["bg"])
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Info knop
        info_btn = tk.Button(button_frame, text="ℹ️ Info & Help", 
                           command=self.show_info_window, 
                           bg='#2196F3', fg='white')
        info_btn.pack(side=tk.LEFT)
        
        save_btn = tk.Button(button_frame, text=self.get_text('save'), 
                           command=lambda: self.save_settings(settings_window), 
                           bg='#4CAF50', fg='white')
        save_btn.pack(side=tk.LEFT, padx=(10, 10))
        
        cancel_btn = tk.Button(button_frame, text=self.get_text('cancel'), 
                             command=settings_window.destroy, 
                             bg='#f44336', fg='white')
        cancel_btn.pack(side=tk.LEFT)
        
        # Toon standaard organisatie instellingen
        self.show_org_settings(right_frame)
        
        # Update thema voor het instellingen venster
        self.update_settings_window_theme(settings_window)
    
    def show_info_window(self):
        """Toont info venster met uitgebreide uitleg"""
        info_window = tk.Toplevel(self.root)
        info_window.title("ℹ️ MP3 Organiser - Info & Help")
        info_window.geometry("900x600")  # Kleiner venster
        info_window.configure(bg=self.themes[self.current_theme]["bg"])
        
        # Maak het venster modal
        info_window.transient(self.root)
        info_window.grab_set()
        info_window.focus_force()
        
        # Hoofdtitel
        title_label = tk.Label(info_window, text="ℹ️ MP3 Organiser - Info & Help", 
                              font=('Arial', 20, 'bold'), bg=self.themes[self.current_theme]["bg"], 
                              fg=self.themes[self.current_theme]["fg"])
        title_label.pack(pady=20)
        
        # Canvas en scrollbar voor scrollbare content
        canvas = tk.Canvas(info_window, bg=self.themes[self.current_theme]["bg"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(info_window, orient="vertical", command=canvas.yview)
        content_frame = tk.Frame(canvas, bg=self.themes[self.current_theme]["bg"])
        
        # Configureer canvas
        content_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=content_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Info content met grotere tekst
        info_text = """
🎵 MP3 Organiser 0.1a - Slimme Muziek Organisatie

Een geavanceerde MP3 bestandsorganisator met Shazam-achtige audio fingerprinting, online database detectie en intelligente duplicaten behandeling.

🔍 FUNCTIE COMPATIBILITEIT

✅ Functies die ALTIJD samen kunnen werken:

1. SCAN BESTANDEN:
   • ID3 Tags + Online Database + Audio Fingerprinting + Bestandsnaam analyse
   • Alle detectie methoden worden in volgorde geprobeerd
   • Geen conflicten - elke methode is een fallback voor de vorige

2. ORGANISATIE:
   • Hiërarchische mappen + Per album + Per jaar
   • Duplicaten controle + Bestanden hernoemen
   • Alle opties kunnen tegelijk actief zijn

⚠️ Functies die elkaar kunnen beïnvloeden:

1. DUPLICATEN BEHANDELING:
   Je kunt maar ÉÉN van deze kiezen:
   • ❌ Automatisch verwijderen
   • ❌ Verplaatsen naar output map  
   • ✅ Behouden (geen actie)

2. AUDIO FINGERPRINTING:
   Vereist bepaalde dependencies:
   • ✅ LIBROSA_AVAILABLE = True
   • ✅ SCIPY_AVAILABLE = True
   • ❌ Anders wordt het overgeslagen

🎯 DETECTIE VOLGORDE (Automatisch):

1. 📁 ID3 Tags (MP3 metadata) - Snelste methode
2. 🌐 Online Database (Last.fm, MusicBrainz, Discogs)
3. 🎵 Audio Fingerprinting (Shazam-achtig)
4. 📝 Bestandsnaam analyse
5. ❓ Unknown Artist (als laatste)

⚙️ AANBEVOLEN CONFIGURATIES

📁 ORGANISATIE OPTIES:

Hiërarchische Mappen:
• ✅ Aanbevolen voor grote collecties
• 📁 Structuur: Muziek/A/Adele/, Muziek/B/Beatles/
• ⚡ Voordelen: Snelle navigatie, overzichtelijke structuur

Per Album Organiseren:
• ✅ Aanbevolen voor complete albums
• 📁 Structuur: Artiest/Album/Track.mp3
• 🎵 Voordelen: Behoudt album structuur

Per Jaar Organiseren:
• ✅ Aanbevolen voor chronologische organisatie
• 📁 Structuur: Artiest/2023/Track.mp3
• 📅 Voordelen: Chronologische overzicht

Bestanden Hernoemen:
• ✅ Aanbevolen voor consistente naamgeving
• 📝 Format: Artiest - Titel.mp3
• 🧹 Voordelen: Verwijdert (official), (remix), etc.

🌐 ONLINE DATABASE INSTELLINGEN:

Online Database Detectie:
• ✅ Altijd aanbevolen voor beste resultaten
• 🌐 Zoekt in Last.fm, MusicBrainz, Discogs
• 📡 Voordelen: Detecteert onbekende artiesten

AI-gebaseerde Artiest Detectie:
• ✅ Aanbevolen voor intelligente herkenning
• 🤖 Gebruikt machine learning voor betere resultaten
• 🎯 Voordelen: Hogere nauwkeurigheid

🎵 Audio Fingerprinting (Shazam-achtig):
• ✅ Aanbevolen voor bestanden zonder metadata
• 🎵 Analyseert audio eigenschappen
• 🔍 Voordelen: Werkt zonder ID3 tags

Lokale Cache:
• ✅ Altijd aanbevolen voor snelheid
• 💾 Slaat resultaten op voor 24 uur (standaard)
• ⚡ Voordelen: Voorkomt herhaalde analyses

🔄 DUPLICATEN BEHANDELING:

Controleer Duplicaten:
• ✅ Aanbevolen voor alle collecties
• 🔍 Detecteert op bestandsnaam en ID3 tags
• 📊 Voordelen: Toont overzicht van duplicaten

Automatisch Verwijderen:
• ⚠️ Voorzichtig gebruiken - kan niet ongedaan worden gemaakt
• 🗑️ Verwijdert duplicaten automatisch
• 💾 Voordelen: Bespaart schijfruimte

Verplaatsen naar Output Map:
• ✅ Aanbevolen voor veilige behandeling
• 📁 Verplaatst naar "Duplicaten" map
• 🔒 Voordelen: Behoudt alle bestanden

📝 LOG INSTELLINGEN:

Auto-scroll:
• ✅ Aanbevolen voor live updates
• 📜 Volgt automatisch nieuwe berichten
• 👀 Voordelen: Blijft altijd bij

Timestamps:
• ✅ Aanbevolen voor debugging
• ⏰ Toont tijdstempel bij elk bericht
• 🔍 Voordelen: Makkelijk terug te vinden

Log Opslaan:
• ✅ Aanbevolen voor belangrijke sessies
• 💾 Slaat log op naar bestand
• 📄 Voordelen: Kan later bekeken worden

🚀 PERFORMANCE TIPS

Voor Snelle Verwerking:
• ✅ ID3 Tags
• ❌ Online Database (uitschakelen)
• ❌ Audio Fingerprinting (uitschakelen)
• ✅ Cache (behouden)
• ✅ Hiërarchische mappen

Voor Beste Nauwkeurigheid:
• ✅ ID3 Tags
• ✅ Online Database
• ✅ Audio Fingerprinting
• ✅ Cache
• ✅ Alle API bronnen
• ✅ Lange cache duur (24+ uur)

Voor Grote Collecties:
• ✅ ID3 Tags
• ✅ Online Database (met rate limiting)
• ✅ Audio Fingerprinting (alleen onbekende)
• ✅ Cache (48+ uur)
• ✅ Hiërarchische mappen
• ✅ Duplicaten controle

❓ TROUBLESHOOTING

Veelvoorkomende Problemen:

Audio Fingerprinting niet beschikbaar:
⚠️ Audio fingerprinting niet beschikbaar (librosa + scipy nodig)

Oplossing:
pip install librosa scipy numpy

Online database werkt niet:
⚠️ requests module niet beschikbaar

Oplossing:
pip install requests

Langzame verwerking:
• 🔧 Schakel online database uit voor snelheid
• 💾 Gebruik cache voor herhaalde analyses
• 🎵 Beperk audio fingerprinting tot onbekende bestanden

Onnauwkeurige resultaten:
• 🎯 Controleer ID3 tags eerst
• 🌐 Verifieer online database instellingen
• 🎵 Test audio fingerprinting met bekende nummers

📈 PERFORMANCE OPTIMALISATIE

Voor grote collecties (>1000 bestanden):
• ✅ Gebruik cache (24+ uur)
• ✅ Schakel online database uit voor initiële scan
• ✅ Beperk audio fingerprinting tot onbekende bestanden
• ✅ Gebruik hiërarchische mappen

Voor kleine collecties (<100 bestanden):
• ✅ Alle functies aan voor beste resultaten
• ✅ Online database voor maximale detectie
• ✅ Audio fingerprinting voor onbekende bestanden

Voor onbekende bestanden:
• ✅ Audio fingerprinting is cruciaal
• ✅ Online database voor backup
• ✅ Cache voorkomt herhaalde analyses

🎵 MP3 Organiser 0.1a - Maak je muziek collectie perfect georganiseerd! ✨
"""
        
        # Maak text widget met grotere tekst
        text_widget = tk.Text(content_frame, wrap=tk.WORD, bg=self.themes[self.current_theme]["text_bg"], 
                             fg=self.themes[self.current_theme]["fg"], font=('Arial', 14),  # Grotere tekst
                             padx=20, pady=20, spacing1=5, spacing2=2, spacing3=5)  # Meer spacing
        text_widget.insert(tk.END, info_text)
        text_widget.config(state=tk.DISABLED)  # Alleen lezen
        text_widget.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Pack canvas en scrollbar
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind muiswiel voor scrollen
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def _on_enter(event):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        def _on_leave(event):
            canvas.unbind_all("<MouseWheel>")
        
        canvas.bind('<Enter>', _on_enter)
        canvas.bind('<Leave>', _on_leave)
        
        # Sluit knop
        close_btn = tk.Button(info_window, text="Sluiten", command=info_window.destroy,
                             bg='#666666', fg='white', font=('Arial', 12),  # Grotere knop
                             padx=20, pady=10)
        close_btn.pack(pady=15)
        
        # Update thema
        self.update_settings_window_theme(info_window)
    
    def show_org_settings(self, parent_frame):
        """Toont organisatie instellingen"""
        # Wis bestaande content
        for widget in parent_frame.winfo_children():
            widget.destroy()
        
        # Organisatie opties frame
        org_frame = tk.LabelFrame(parent_frame, text=self.get_text('org_options'), 
                                 bg=self.themes[self.current_theme]["bg"], fg=self.themes[self.current_theme]["fg"])
        org_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Hiërarchische mappen
        hierarchical_frame = tk.Frame(org_frame, bg=self.themes[self.current_theme]["bg"])
        hierarchical_frame.pack(fill=tk.X, padx=10, pady=5)
        
        hierarchical_cb = tk.Checkbutton(hierarchical_frame, text=self.get_text('hierarchical'), 
                                       variable=self.hierarchical_var, bg=self.themes[self.current_theme]["bg"],
                                       fg=self.themes[self.current_theme]["fg"])
        hierarchical_cb.pack(side=tk.LEFT)
        
        hierarchical_help_btn = tk.Button(hierarchical_frame, text="?", width=2, height=1,
                                        command=lambda: self.show_example("hierarchical"), 
                                        bg='#2196F3', fg='#000000')
        hierarchical_help_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Per album organiseren
        albums_frame = tk.Frame(org_frame, bg=self.themes[self.current_theme]["bg"])
        albums_frame.pack(fill=tk.X, padx=10, pady=5)
        
        albums_cb = tk.Checkbutton(albums_frame, text="Per album organiseren", 
                                 variable=self.albums_var, bg=self.themes[self.current_theme]["bg"],
                                 fg=self.themes[self.current_theme]["fg"])
        albums_cb.pack(side=tk.LEFT)
        
        albums_help_btn = tk.Button(albums_frame, text="?", width=2, height=1,
                                  command=lambda: self.show_example("albums"), 
                                  bg='#2196F3', fg='#000000')
        albums_help_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Per jaar organiseren
        years_frame = tk.Frame(org_frame, bg=self.themes[self.current_theme]["bg"])
        years_frame.pack(fill=tk.X, padx=10, pady=5)
        
        years_cb = tk.Checkbutton(years_frame, text="Per jaar organiseren", 
                                variable=self.years_var, bg=self.themes[self.current_theme]["bg"],
                                fg=self.themes[self.current_theme]["fg"])
        years_cb.pack(side=tk.LEFT)
        
        years_help_btn = tk.Button(years_frame, text="?", width=2, height=1,
                                 command=lambda: self.show_example("years"), 
                                 bg='#2196F3', fg='#000000')
        years_help_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Controleer duplicaten
        duplicate_frame = tk.Frame(org_frame, bg=self.themes[self.current_theme]["bg"])
        duplicate_frame.pack(fill=tk.X, padx=10, pady=5)
        
        duplicate_check_cb = tk.Checkbutton(duplicate_frame, text="Controleer duplicaten", 
                                          variable=self.duplicate_check_var, bg=self.themes[self.current_theme]["bg"],
                                          fg=self.themes[self.current_theme]["fg"])
        duplicate_check_cb.pack(side=tk.LEFT)
        
        duplicate_help_btn = tk.Button(duplicate_frame, text="?", width=2, height=1,
                                     command=lambda: self.show_example("duplicates"), 
                                     bg='#2196F3', fg='#000000')
        duplicate_help_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Duplicaten automatisch verwijderen
        duplicate_remove_frame = tk.Frame(org_frame, bg=self.themes[self.current_theme]["bg"])
        duplicate_remove_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.duplicate_remove_var = tk.BooleanVar(value=False)
        duplicate_remove_cb = tk.Checkbutton(duplicate_remove_frame, text="Duplicaten automatisch verwijderen", 
                                           variable=self.duplicate_remove_var, bg=self.themes[self.current_theme]["bg"],
                                           fg=self.themes[self.current_theme]["fg"])
        duplicate_remove_cb.pack(side=tk.LEFT)
        
        duplicate_remove_help_btn = tk.Button(duplicate_remove_frame, text="?", width=2, height=1,
                                            command=lambda: self.show_example("duplicate_remove"), 
                                            bg='#2196F3', fg='#000000')
        duplicate_remove_help_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Duplicaten verplaatsen naar output map
        duplicate_move_frame = tk.Frame(org_frame, bg=self.themes[self.current_theme]["bg"])
        duplicate_move_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.duplicate_move_var = tk.BooleanVar(value=False)
        duplicate_move_cb = tk.Checkbutton(duplicate_move_frame, text="Duplicaten verplaatsen naar output map", 
                                         variable=self.duplicate_move_var, bg=self.themes[self.current_theme]["bg"],
                                         fg=self.themes[self.current_theme]["fg"])
        duplicate_move_cb.pack(side=tk.LEFT)
        
        duplicate_move_help_btn = tk.Button(duplicate_move_frame, text="?", width=2, height=1,
                                          command=lambda: self.show_example("duplicate_move"), 
                                          bg='#2196F3', fg='#000000')
        duplicate_move_help_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Duplicaten output map selectie
        duplicate_output_frame = tk.Frame(org_frame, bg=self.themes[self.current_theme]["bg"])
        duplicate_output_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(duplicate_output_frame, text="Duplicaten output map:", 
                bg=self.themes[self.current_theme]["bg"], fg=self.themes[self.current_theme]["fg"]).pack(side=tk.LEFT)
        
        self.duplicate_output_var = tk.StringVar(value=self.config.get('duplicate_output', 'Duplicaten'))
        duplicate_output_entry = tk.Entry(duplicate_output_frame, textvariable=self.duplicate_output_var, 
                                       bg=self.themes[self.current_theme]["bg"], fg=self.themes[self.current_theme]["fg"],
                                       width=20)
        duplicate_output_entry.pack(side=tk.LEFT, padx=(10, 5))
        
        # Gebruik lambda om focus probleem te voorkomen
        duplicate_output_btn = tk.Button(duplicate_output_frame, text="📁 Bladeren", 
                                       command=lambda: self.select_duplicate_output_folder(),
                                       bg='#4CAF50', fg='white', height=1)
        duplicate_output_btn.pack(side=tk.RIGHT)
        
        # Bestanden hernoemen naar Artiest - Titel
        rename_frame = tk.Frame(org_frame, bg=self.themes[self.current_theme]["bg"])
        rename_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.rename_files_var = tk.BooleanVar(value=self.config.get('rename_files', False))
        rename_cb = tk.Checkbutton(rename_frame, text="Bestanden hernoemen naar 'Artiest - Titel'", 
                                 variable=self.rename_files_var, bg=self.themes[self.current_theme]["bg"],
                                 fg=self.themes[self.current_theme]["fg"])
        rename_cb.pack(side=tk.LEFT)
        
        rename_help_btn = tk.Button(rename_frame, text="?", width=2, height=1,
                                  command=lambda: self.show_example("rename_files"), 
                                  bg='#2196F3', fg='#000000')
        rename_help_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Titel opschonen optie
        clean_title_frame = tk.Frame(org_frame, bg=self.themes[self.current_theme]["bg"])
        clean_title_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.clean_title_format_var = tk.BooleanVar(value=self.config.get('clean_title_format', True))
        clean_title_cb = tk.Checkbutton(clean_title_frame, text=self.get_text('clean_title_format'), 
                                      variable=self.clean_title_format_var, bg=self.themes[self.current_theme]["bg"],
                                      fg=self.themes[self.current_theme]["fg"])
        clean_title_cb.pack(side=tk.LEFT)
        
        clean_title_help_btn = tk.Button(clean_title_frame, text="?", width=2, height=1,
                                       command=lambda: self.show_example("clean_title_format"), 
                                       bg='#2196F3', fg='#000000')
        clean_title_help_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Voorbeeld label
        self.example_label = tk.Label(org_frame, text="", bg=self.themes[self.current_theme]["bg"], 
                                     fg='#666666', font=('Arial', 9), wraplength=400)
        self.example_label.pack(pady=(10, 0))
    
    def show_log_settings(self, parent_frame):
        """Toont log instellingen"""
        # Wis bestaande content
        for widget in parent_frame.winfo_children():
            widget.destroy()
        
        # Log opties frame
        log_frame = tk.LabelFrame(parent_frame, text="📝 Log Opties", 
                                 bg=self.themes[self.current_theme]["bg"], fg=self.themes[self.current_theme]["fg"])
        log_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Log venster grootte
        size_frame = tk.Frame(log_frame, bg=self.themes[self.current_theme]["bg"])
        size_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(size_frame, text="Log venster grootte:", 
                bg=self.themes[self.current_theme]["bg"], fg=self.themes[self.current_theme]["fg"]).pack(side=tk.LEFT)
        
        self.log_size_var = tk.StringVar(value="800x600")
        size_combo = ttk.Combobox(size_frame, textvariable=self.log_size_var, 
                                 values=["600x400", "800x600", "1000x700", "1200x800"], 
                                 state="readonly", width=10)
        size_combo.pack(side=tk.RIGHT)
        
        # Auto-scroll optie
        self.auto_scroll_var = tk.BooleanVar(value=True)
        auto_scroll_cb = tk.Checkbutton(log_frame, text="Auto-scroll inschakelen", 
                                      variable=self.auto_scroll_var, bg=self.themes[self.current_theme]["bg"],
                                      fg=self.themes[self.current_theme]["fg"])
        auto_scroll_cb.pack(anchor=tk.W, padx=10, pady=5)
        
        # Timestamp optie
        self.timestamp_var = tk.BooleanVar(value=True)
        timestamp_cb = tk.Checkbutton(log_frame, text="Timestamps weergeven", 
                                    variable=self.timestamp_var, bg=self.themes[self.current_theme]["bg"],
                                    fg=self.themes[self.current_theme]["fg"])
        timestamp_cb.pack(anchor=tk.W, padx=10, pady=5)
        
        # Log niveau
        level_frame = tk.Frame(log_frame, bg=self.themes[self.current_theme]["bg"])
        level_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(level_frame, text="Log niveau:", 
                bg=self.themes[self.current_theme]["bg"], fg=self.themes[self.current_theme]["fg"]).pack(side=tk.LEFT)
        
        self.log_level_var = tk.StringVar(value="Info")
        level_combo = ttk.Combobox(level_frame, textvariable=self.log_level_var, 
                                  values=["Debug", "Info", "Warning", "Error"], 
                                  state="readonly", width=10)
        level_combo.pack(side=tk.RIGHT)
        
        # Log bewaar optie
        self.save_log_var = tk.BooleanVar(value=False)
        save_log_cb = tk.Checkbutton(log_frame, text="Log opslaan naar bestand", 
                                   variable=self.save_log_var, bg=self.themes[self.current_theme]["bg"],
                                   fg=self.themes[self.current_theme]["fg"])
        save_log_cb.pack(anchor=tk.W, padx=10, pady=5)
    
    def show_language_settings(self, parent_frame):
        """Toont taal en lettergrootte instellingen"""
        # Wis bestaande content
        for widget in parent_frame.winfo_children():
            widget.destroy()
        
        # Taal opties frame
        lang_frame = tk.LabelFrame(parent_frame, text=self.get_text('language_options'), 
                                  bg=self.themes[self.current_theme]["bg"], fg=self.themes[self.current_theme]["fg"])
        lang_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Taal selectie
        language_frame = tk.Frame(lang_frame, bg=self.themes[self.current_theme]["bg"])
        language_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(language_frame, text=self.get_text('program_language'), 
                bg=self.themes[self.current_theme]["bg"], fg=self.themes[self.current_theme]["fg"]).pack(side=tk.LEFT)
        
        self.language_var = tk.StringVar(value=self.current_language)
        language_combo = ttk.Combobox(language_frame, textvariable=self.language_var, 
                                     values=["Nederlands", "English", "Deutsch", "Français", "Español"], 
                                     state="readonly", width=15)
        language_combo.pack(side=tk.RIGHT)
        
        # Lettergrootte selectie
        font_size_frame = tk.Frame(lang_frame, bg=self.themes[self.current_theme]["bg"])
        font_size_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(font_size_frame, text=self.get_text('font_size'), 
                bg=self.themes[self.current_theme]["bg"], fg=self.themes[self.current_theme]["fg"]).pack(side=tk.LEFT)
        
        self.font_size_var = tk.StringVar(value=self.current_font_size)
        font_size_combo = ttk.Combobox(font_size_frame, textvariable=self.font_size_var, 
                                      values=["Klein", "Normaal", "Groot", "Extra Groot"], 
                                      state="readonly", width=15)
        font_size_combo.pack(side=tk.RIGHT)
        
        # Font familie selectie
        font_family_frame = tk.Frame(lang_frame, bg=self.themes[self.current_theme]["bg"])
        font_family_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(font_family_frame, text=self.get_text('font_family'), 
                bg=self.themes[self.current_theme]["bg"], fg=self.themes[self.current_theme]["fg"]).pack(side=tk.LEFT)
        
        self.font_family_var = tk.StringVar(value=self.current_font_family)
        font_family_combo = ttk.Combobox(font_family_frame, textvariable=self.font_family_var, 
                                        values=["Arial", "Helvetica", "Times New Roman", "Verdana", "Tahoma"], 
                                        state="readonly", width=15)
        font_family_combo.pack(side=tk.RIGHT)
        
        # Preview frame
        preview_frame = tk.LabelFrame(lang_frame, text=self.get_text('preview'), 
                                     bg=self.themes[self.current_theme]["bg"], fg=self.themes[self.current_theme]["fg"])
        preview_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Preview tekst
        preview_text = self.get_text('preview_text')
        self.preview_label = tk.Label(preview_frame, text=preview_text, 
                                     bg=self.themes[self.current_theme]["bg"], fg=self.themes[self.current_theme]["fg"],
                                     font=('Arial', 10))
        self.preview_label.pack(pady=10)
        
        # Bind events voor live preview
        language_combo.bind('<<ComboboxSelected>>', self.update_preview)
        font_size_combo.bind('<<ComboboxSelected>>', self.update_preview)
        font_family_combo.bind('<<ComboboxSelected>>', self.update_preview)
    
    def show_online_settings(self, parent_frame):
        """Toont online database instellingen"""
        # Wis bestaande content
        for widget in parent_frame.winfo_children():
            widget.destroy()
        
        # Online database opties frame
        online_frame = tk.LabelFrame(parent_frame, text="🌐 Online Database Instellingen", 
                                   bg=self.themes[self.current_theme]["bg"], fg=self.themes[self.current_theme]["fg"])
        online_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Online database inschakelen
        online_db_frame = tk.Frame(online_frame, bg=self.themes[self.current_theme]["bg"])
        online_db_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.online_db_var = tk.BooleanVar(value=self.config.get('online_database', True))
        online_db_cb = tk.Checkbutton(online_db_frame, text="Online database detectie inschakelen", 
                                    variable=self.online_db_var, bg=self.themes[self.current_theme]["bg"],
                                    fg=self.themes[self.current_theme]["fg"])
        online_db_cb.pack(side=tk.LEFT)
        
        # AI detectie inschakelen
        ai_detect_frame = tk.Frame(online_frame, bg=self.themes[self.current_theme]["bg"])
        ai_detect_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.ai_detect_var = tk.BooleanVar(value=self.config.get('ai_detection', True))
        ai_detect_cb = tk.Checkbutton(ai_detect_frame, text="AI-gebaseerde artiest detectie", 
                                    variable=self.ai_detect_var, bg=self.themes[self.current_theme]["bg"],
                                    fg=self.themes[self.current_theme]["fg"])
        ai_detect_cb.pack(side=tk.LEFT)
        
        # Audio fingerprinting inschakelen
        fingerprint_frame = tk.Frame(online_frame, bg=self.themes[self.current_theme]["bg"])
        fingerprint_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.audio_fingerprinting_var = tk.BooleanVar(value=self.config.get('audio_fingerprinting', True))
        fingerprint_cb = tk.Checkbutton(fingerprint_frame, text="🎵 Audio Fingerprinting (Shazam-achtig)", 
                                      variable=self.audio_fingerprinting_var, bg=self.themes[self.current_theme]["bg"],
                                      fg=self.themes[self.current_theme]["fg"])
        fingerprint_cb.pack(side=tk.LEFT)
        
        # Status van audio fingerprinting
        fingerprint_status_frame = tk.Frame(online_frame, bg=self.themes[self.current_theme]["bg"])
        fingerprint_status_frame.pack(fill=tk.X, padx=10, pady=2)
        
        if LIBROSA_AVAILABLE and SCIPY_AVAILABLE:
            status_text = "✅ Audio fingerprinting beschikbaar (librosa + scipy)"
            status_color = 'green'
        else:
            status_text = "⚠️ Audio fingerprinting niet beschikbaar (librosa + scipy nodig)"
            status_color = 'orange'
        
        fingerprint_status = tk.Label(fingerprint_status_frame, text=status_text, 
                                   bg=self.themes[self.current_theme]["bg"], fg=status_color,
                                   font=('Arial', 9))
        fingerprint_status.pack(side=tk.LEFT)
        
        # Cache instellingen
        cache_frame = tk.Frame(online_frame, bg=self.themes[self.current_theme]["bg"])
        cache_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.cache_var = tk.BooleanVar(value=self.online_db_config.get('cache_enabled', True))
        cache_cb = tk.Checkbutton(cache_frame, text="Lokale cache inschakelen", 
                                variable=self.cache_var, bg=self.themes[self.current_theme]["bg"],
                                fg=self.themes[self.current_theme]["fg"])
        cache_cb.pack(side=tk.LEFT)
        
        # Cache duur
        cache_duration_frame = tk.Frame(online_frame, bg=self.themes[self.current_theme]["bg"])
        cache_duration_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(cache_duration_frame, text="Cache duur (uren):", 
                bg=self.themes[self.current_theme]["bg"], fg=self.themes[self.current_theme]["fg"]).pack(side=tk.LEFT)
        
        self.cache_duration_var = tk.StringVar(value=str(self.online_db_config.get('cache_duration', 86400) // 3600))
        cache_duration_combo = ttk.Combobox(cache_duration_frame, textvariable=self.cache_duration_var, 
                                           values=["1", "6", "12", "24", "48"], 
                                           state="readonly", width=10)
        cache_duration_combo.pack(side=tk.RIGHT)
        
        # API bronnen
        sources_frame = tk.LabelFrame(online_frame, text="API Bronnen", 
                                    bg=self.themes[self.current_theme]["bg"], fg=self.themes[self.current_theme]["fg"])
        sources_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Last.fm
        lastfm_frame = tk.Frame(sources_frame, bg=self.themes[self.current_theme]["bg"])
        lastfm_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.lastfm_var = tk.BooleanVar(value=self.online_db_config.get('lastfm_enabled', True) and REQUESTS_AVAILABLE)
        lastfm_cb = tk.Checkbutton(lastfm_frame, text="Last.fm API", 
                                 variable=self.lastfm_var, bg=self.themes[self.current_theme]["bg"],
                                 fg=self.themes[self.current_theme]["fg"], 
                                 state=tk.DISABLED if not REQUESTS_AVAILABLE else tk.NORMAL)
        lastfm_cb.pack(side=tk.LEFT)
        
        # MusicBrainz
        musicbrainz_frame = tk.Frame(sources_frame, bg=self.themes[self.current_theme]["bg"])
        musicbrainz_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.musicbrainz_var = tk.BooleanVar(value=self.online_db_config.get('musicbrainz_enabled', True) and REQUESTS_AVAILABLE)
        musicbrainz_cb = tk.Checkbutton(musicbrainz_frame, text="MusicBrainz API", 
                                      variable=self.musicbrainz_var, bg=self.themes[self.current_theme]["bg"],
                                      fg=self.themes[self.current_theme]["fg"],
                                      state=tk.DISABLED if not REQUESTS_AVAILABLE else tk.NORMAL)
        musicbrainz_cb.pack(side=tk.LEFT)
        
        # Discogs
        discogs_frame = tk.Frame(sources_frame, bg=self.themes[self.current_theme]["bg"])
        discogs_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.discogs_var = tk.BooleanVar(value=self.online_db_config.get('discogs_enabled', True) and REQUESTS_AVAILABLE)
        discogs_cb = tk.Checkbutton(discogs_frame, text="Discogs API", 
                                  variable=self.discogs_var, bg=self.themes[self.current_theme]["bg"],
                                  fg=self.themes[self.current_theme]["fg"],
                                  state=tk.DISABLED if not REQUESTS_AVAILABLE else tk.NORMAL)
        discogs_cb.pack(side=tk.LEFT)
        
        # Rate limiting
        rate_frame = tk.Frame(online_frame, bg=self.themes[self.current_theme]["bg"])
        rate_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(rate_frame, text="Max requests per minuut:", 
                bg=self.themes[self.current_theme]["bg"], fg=self.themes[self.current_theme]["fg"]).pack(side=tk.LEFT)
        
        self.rate_limit_var = tk.StringVar(value=str(self.online_db_config.get('max_requests_per_minute', 30)))
        rate_limit_combo = ttk.Combobox(rate_frame, textvariable=self.rate_limit_var, 
                                       values=["10", "20", "30", "50", "100"], 
                                       state="readonly", width=10)
        rate_limit_combo.pack(side=tk.RIGHT)
        
        # API Key instellingen
        api_frame = tk.LabelFrame(online_frame, text="API Sleutels", 
                                bg=self.themes[self.current_theme]["bg"], fg=self.themes[self.current_theme]["fg"])
        api_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Last.fm API Key
        lastfm_key_frame = tk.Frame(api_frame, bg=self.themes[self.current_theme]["bg"])
        lastfm_key_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(lastfm_key_frame, text="Last.fm API Key:", 
                bg=self.themes[self.current_theme]["bg"], fg=self.themes[self.current_theme]["fg"]).pack(side=tk.LEFT)
        
        self.lastfm_key_var = tk.StringVar(value=self.online_db_config.get('lastfm_api_key', ''))
        lastfm_key_entry = tk.Entry(lastfm_key_frame, textvariable=self.lastfm_key_var, 
                                  bg=self.themes[self.current_theme]["bg"], fg=self.themes[self.current_theme]["fg"],
                                  width=30)
        lastfm_key_entry.pack(side=tk.RIGHT)
        
        # Info label
        info_text = "💡 Tip: Voeg je eigen API sleutels toe voor betere resultaten"
        if not REQUESTS_AVAILABLE:
            info_text += "\n⚠️ requests module niet geïnstalleerd - online functionaliteit beperkt"
        
        info_label = tk.Label(online_frame, text=info_text, 
                             bg=self.themes[self.current_theme]["bg"], fg='#666666', 
                             font=('Arial', 9), wraplength=400)
        info_label.pack(pady=(10, 0))
    
    def update_preview(self, event=None):
        """Update preview met nieuwe instellingen"""
        if hasattr(self, 'preview_label'):
            # Bepaal font grootte
            size_map = {"Klein": 8, "Normaal": 10, "Groot": 12, "Extra Groot": 14}
            font_size = size_map.get(self.font_size_var.get(), 10)
            
            # Update preview
            self.preview_label.configure(font=(self.font_family_var.get(), font_size))
    
    def get_text(self, key, **kwargs):
        """Haalt vertaalde tekst op"""
        language = self.current_language
        
        # Zorg ervoor dat Nederlands de standaard taal is
        if language not in self.translations:
            language = 'Nederlands'
        
        if language in self.translations and key in self.translations[language]:
            text = self.translations[language][key]
            return text.format(**kwargs) if kwargs else text
        return key  # Fallback naar key als vertaling niet bestaat
    
    def change_language(self, language):
        """Verandert de taal van de applicatie"""
        if language in self.translations:
            self.current_language = language
            self.config['language'] = language
            self.update_ui_language()
            self.log_message(self.get_text('theme_changed', theme=language))
            
            # Update menubalk specifiek
            for widget in self.root.winfo_children():
                if isinstance(widget, tk.Menu):
                    self.update_menu_language(widget)
            
            # Update knoppen direct
            if hasattr(self, 'scan_btn'):
                self.scan_btn.configure(text=self.get_text('scan_files'))
            if hasattr(self, 'organize_btn'):
                self.organize_btn.configure(text=self.get_text('start_org'))
            if hasattr(self, 'duplicate_btn'):
                self.duplicate_btn.configure(text=self.get_text('find_duplicates'))
            if hasattr(self, 'kill_switch_btn'):
                self.kill_switch_btn.configure(text=self.get_text('kill_switch'))
    
    def change_font(self, font_family=None, font_size=None):
        """Verandert het font van de applicatie"""
        if font_family:
            self.current_font_family = font_family
            self.config['font_family'] = font_family
        
        if font_size:
            self.current_font_size = font_size
            self.config['font_size'] = font_size
        
        self.update_ui_font()
    
    def update_ui_language(self):
        """Update alle UI elementen met nieuwe taal"""
        # Update venster titel
        self.root.title(self.get_text('title'))
        
        # Update menu items
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Menu):
                self.update_menu_language(widget)
        
        # Update hoofdelementen
        self.update_main_ui_language()
    
    def update_ui_font(self):
        """Update alle UI elementen met nieuwe font"""
        font_size = self.font_sizes.get(self.current_font_size, 10)
        font_tuple = (self.current_font_family, font_size)
        
        # Update hoofdelementen
        self.update_main_ui_font(font_tuple)
    
    def update_menu_language(self, menu):
        """Update menu taal"""
        try:
            for i in range(menu.index('end') + 1):
                try:
                    label = menu.entrycget(i, 'label')
                    # Update menu labels
                    if "Instellingen" in label:
                        menu.entryconfig(i, label=self.get_text('settings'))
                    elif "Thema" in label:
                        menu.entryconfig(i, label=self.get_text('theme'))
                    elif "Debug" in label:
                        menu.entryconfig(i, label=self.get_text('debug'))
                    elif "Log" in label:
                        menu.entryconfig(i, label=self.get_text('log'))
                except:
                    pass
        except:
            pass
    
    def update_main_ui_language(self):
        """Update hoofdelementen taal"""
        # Update venster titel
        self.root.title(self.get_text('title'))
        
        # Update specifieke UI elementen
        self.update_main_labels()
        
        # Update labels en knoppen
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                self.update_widget_language(widget)
    
    def update_main_labels(self):
        """Update hoofdlabels van de applicatie"""
        # Zoek en update specifieke labels
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                self.update_main_frame_labels(widget)
    
    def update_main_frame_labels(self, frame):
        """Update labels in hoofdframe"""
        for child in frame.winfo_children():
            try:
                if isinstance(child, tk.Label):
                    # Update specifieke labels
                    current_text = child.cget("text")
                    if "MP3 Organiser" in current_text:
                        child.configure(text=self.get_text('title'))
                    elif "Map om te Organiseren" in current_text:
                        child.configure(text=self.get_text('select_folder'))
                    elif "Voortgang" in current_text:
                        child.configure(text=self.get_text('progress'))
                    elif "Klaar om te organiseren" in current_text:
                        child.configure(text=self.get_text('ready'))
                    elif "Log" in current_text:
                        child.configure(text=self.get_text('log'))
                elif isinstance(child, tk.Button):
                    # Update knoppen
                    current_text = child.cget("text")
                    if "Bladeren" in current_text:
                        child.configure(text=self.get_text('browse'))
                    elif "Start Organisatie" in current_text or "Start Organization" in current_text:
                        child.configure(text=self.get_text('start_org'))
                    elif "Scan Bestanden" in current_text or "Scan Files" in current_text:
                        child.configure(text=self.get_text('scan_files'))
                    elif "Zoek Duplicaten" in current_text or "Find Duplicates" in current_text:
                        child.configure(text=self.get_text('find_duplicates'))
                    elif "Log Wissen" in current_text or "Clear Log" in current_text:
                        child.configure(text=self.get_text('clear_log'))
                    elif "Stop Alles" in current_text or "Stop Everything" in current_text:
                        child.configure(text=self.get_text('kill_switch'))
                elif isinstance(child, tk.LabelFrame):
                    # Update LabelFrame titels
                    current_text = child.cget("text")
                    if "Map om te Organiseren" in current_text:
                        child.configure(text=self.get_text('select_folder'))
                    elif "Voortgang" in current_text:
                        child.configure(text=self.get_text('progress'))
                    elif "Log" in current_text:
                        child.configure(text=self.get_text('log'))
            except:
                pass
            
            # Recursief voor child widgets
            if hasattr(child, 'winfo_children'):
                self.update_main_frame_labels(child)
        
        # Update specifieke knoppen direct
        if hasattr(self, 'scan_btn'):
            self.scan_btn.configure(text=self.get_text('scan_files'))
        if hasattr(self, 'organize_btn'):
            self.organize_btn.configure(text=self.get_text('start_org'))
        if hasattr(self, 'duplicate_btn'):
            self.duplicate_btn.configure(text=self.get_text('find_duplicates'))
        if hasattr(self, 'kill_switch_btn'):
            self.kill_switch_btn.configure(text=self.get_text('kill_switch'))
    
    def update_main_ui_font(self, font_tuple):
        """Update hoofdelementen font"""
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                self.update_widget_font(widget, font_tuple)
    
    def update_widget_language(self, widget):
        """Update widget taal recursief"""
        try:
            # Update specifieke widgets
            if hasattr(widget, 'cget'):
                widget_type = widget.winfo_class()
                if widget_type == 'TLabel':
                    # Update labels
                    pass
                elif widget_type == 'TButton':
                    # Update knoppen
                    pass
        except:
            pass
        
        # Recursief voor child widgets
        for child in widget.winfo_children():
            self.update_widget_language(child)
    
    def update_widget_font(self, widget, font_tuple):
        """Update widget font recursief"""
        try:
            if hasattr(widget, 'configure'):
                widget.configure(font=font_tuple)
        except:
            pass
        
        # Recursief voor child widgets
        for child in widget.winfo_children():
            self.update_widget_font(child, font_tuple)
    
    def update_settings_window_theme(self, window):
        """Update thema van instellingen venster"""
        theme = self.themes[self.current_theme]
        window.configure(bg=theme["bg"])
        
        for widget in window.winfo_children():
            if isinstance(widget, tk.Label):
                widget.configure(bg=theme["bg"], fg=theme["fg"])
            elif isinstance(widget, tk.LabelFrame):
                widget.configure(bg=theme["bg"], fg=theme["fg"])
            elif isinstance(widget, tk.Frame):
                widget.configure(bg=theme["bg"])
            elif isinstance(widget, tk.Checkbutton):
                widget.configure(bg=theme["bg"], fg=theme["fg"])
            elif isinstance(widget, tk.Radiobutton):
                widget.configure(bg=theme["bg"], fg=theme["fg"])
            elif isinstance(widget, tk.Button):
                if widget.cget("text") == "?":
                    widget.configure(bg='#2196F3', fg='#000000')
                else:
                    widget.configure(bg=theme["button_bg"], fg=theme["button_fg"])
    
    def save_settings(self, window):
        """Slaat instellingen op en sluit venster"""
        # Update configuratie
        new_language = getattr(self, 'language_var', tk.StringVar(value="Nederlands")).get()
        new_font_size = getattr(self, 'font_size_var', tk.StringVar(value="Normaal")).get()
        new_font_family = getattr(self, 'font_family_var', tk.StringVar(value="Arial")).get()
        
        self.config.update({
            'hierarchical': self.hierarchical_var.get(),
            'include_albums': self.albums_var.get(),
            'include_years': self.years_var.get(),
            'duplicate_check': self.duplicate_check_var.get(),
            'duplicate_remove': getattr(self, 'duplicate_remove_var', tk.BooleanVar(value=False)).get(),
            'duplicate_move': getattr(self, 'duplicate_move_var', tk.BooleanVar(value=False)).get(),
            'log_size': getattr(self, 'log_size_var', tk.StringVar(value="800x600")).get(),
            'auto_scroll': getattr(self, 'auto_scroll_var', tk.BooleanVar(value=True)).get(),
            'timestamp': getattr(self, 'timestamp_var', tk.BooleanVar(value=True)).get(),
            'log_level': getattr(self, 'log_level_var', tk.StringVar(value="Info")).get(),
            'save_log': getattr(self, 'save_log_var', tk.BooleanVar(value=False)).get(),
            'language': new_language,
            'font_size': new_font_size,
            'font_family': new_font_family,
            'online_database': getattr(self, 'online_db_var', tk.BooleanVar(value=True)).get(),
            'ai_detection': getattr(self, 'ai_detect_var', tk.BooleanVar(value=True)).get(),
            'audio_fingerprinting': getattr(self, 'audio_fingerprinting_var', tk.BooleanVar(value=True)).get(),
            'rename_files': getattr(self, 'rename_files_var', tk.BooleanVar(value=False)).get(),
            'clean_title_format': getattr(self, 'clean_title_format_var', tk.BooleanVar(value=True)).get(),
            'duplicate_output': getattr(self, 'duplicate_output_var', tk.StringVar(value="Duplicaten")).get()
        })
        
        # Update online database configuratie
        self.online_db_config.update({
            'cache_enabled': getattr(self, 'cache_var', tk.BooleanVar(value=True)).get(),
            'cache_duration': int(getattr(self, 'cache_duration_var', tk.StringVar(value="24")).get()) * 3600,
            'lastfm_enabled': getattr(self, 'lastfm_var', tk.BooleanVar(value=True)).get(),
            'musicbrainz_enabled': getattr(self, 'musicbrainz_var', tk.BooleanVar(value=True)).get(),
            'discogs_enabled': getattr(self, 'discogs_var', tk.BooleanVar(value=True)).get(),
            'max_requests_per_minute': int(getattr(self, 'rate_limit_var', tk.StringVar(value="30")).get()),
            'lastfm_api_key': getattr(self, 'lastfm_key_var', tk.StringVar(value="")).get()
        })
        
        # Pas taal en font wijzigingen toe
        if new_language != self.current_language:
            self.current_language = new_language
            self.change_language(new_language)
        
        if new_font_size != self.current_font_size or new_font_family != self.current_font_family:
            self.current_font_size = new_font_size
            self.current_font_family = new_font_family
            self.change_font(new_font_family, new_font_size)
        
        # Sla configuratie op
        self.save_config()
        
        self.log_message(self.get_text('settings_saved'))
        window.destroy()
        

    

    
    def toggle_log(self):
        """Opent log in apart venster"""
        if self.log_window is None or not self.log_window.winfo_exists():
            # Maak nieuw log venster
            self.log_window = tk.Toplevel(self.root)
            self.log_window.title(f"📝 {self.get_text('title')} - {self.get_text('log')}")
            self.log_window.geometry("800x600")
            self.log_window.configure(bg=self.themes[self.current_theme]["bg"])
            
            # Log frame
            log_frame = tk.LabelFrame(self.log_window, text=self.get_text('log'), bg=self.themes[self.current_theme]["bg"])
            log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Log text widget
            self.log_text = tk.Text(log_frame, wrap=tk.WORD, bg=self.themes[self.current_theme]["text_bg"], 
                                   fg=self.themes[self.current_theme]["fg"])
            log_scrollbar = tk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
            self.log_text.configure(yscrollcommand=log_scrollbar.set)
            
            self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Auto-scroll variabelen
            self.auto_scroll_enabled = True
            self.last_scroll_position = 0
            
            # Bind scroll events
            self.log_text.bind('<MouseWheel>', self.on_mouse_scroll)
            self.log_text.bind('<Button-4>', self.on_mouse_scroll)  # Linux scroll up
            self.log_text.bind('<Button-5>', self.on_mouse_scroll)  # Linux scroll down
            
            # Knoppen frame
            button_frame = tk.Frame(self.log_window, bg=self.themes[self.current_theme]["bg"])
            button_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
            
            clear_btn = tk.Button(button_frame, text=self.get_text('clear_log'), 
                                command=self.clear_log, bg='#f44336', fg='white')
            clear_btn.pack(side=tk.LEFT)
        
            close_btn = tk.Button(button_frame, text=self.get_text('cancel'), 
                                command=self.close_log_window, bg='#666666', fg='white')
            close_btn.pack(side=tk.RIGHT)
            
            # Update thema voor het nieuwe venster
            self.update_log_window_theme()
            
            # Reset auto-scroll voor nieuw venster
            self.auto_scroll_enabled = True
            
            self.log_message(self.get_text('log_window_opened'))
        else:
            # Focus op bestaand venster
            self.log_window.lift()
            self.log_window.focus_force()
    
    def close_log_window(self):
        """Sluit het log venster"""
        if self.log_window and self.log_window.winfo_exists():
            self.log_window.destroy()
            self.log_window = None
            self.log_text = None
    
    def update_log_window_theme(self):
        """Update thema van log venster"""
        if self.log_window and self.log_window.winfo_exists():
            theme = self.themes[self.current_theme]
            self.log_window.configure(bg=theme["bg"])
            
            for widget in self.log_window.winfo_children():
                if isinstance(widget, tk.LabelFrame):
                    widget.configure(bg=theme["bg"])
                elif isinstance(widget, tk.Frame):
                    widget.configure(bg=theme["bg"])
                elif isinstance(widget, tk.Text):
                    widget.configure(bg=theme["text_bg"], fg=theme["fg"])
                elif isinstance(widget, tk.Button):
                    widget.configure(bg=theme["button_bg"], fg=theme["button_fg"])
    
    def on_mouse_scroll(self, event):
        """Handelt muis scroll events af"""
        # Controleer of gebruiker handmatig scrollt
        current_position = self.log_text.yview()[1]  # Positie van scrollbar
        
        # Als gebruiker scrollt naar boven (niet helemaal onderaan)
        if current_position < 1.0:
            self.auto_scroll_enabled = False
        else:
            # Als gebruiker helemaal onderaan is, herstel auto-scroll
            self.auto_scroll_enabled = True
    
    def check_auto_scroll(self):
        """Controleert of auto-scroll moet worden ingeschakeld"""
        if self.log_text and self.log_window and self.log_window.winfo_exists():
            current_position = self.log_text.yview()[1]
            if current_position >= 0.99:  # Bijna helemaal onderaan
                self.auto_scroll_enabled = True
    

    
    def show_example(self, option_type):
        """Toont voorbeeld van organisatie optie of verbergt het"""
        examples = {
            "hierarchical": "📁 Voorbeeld: D:\\Muziek\\\n├── A\\\n│   ├── Adele\\\n│   └── Arctic Monkeys\\\n├── B\\\n│   ├── Barry White\\\n│   └── Beatles\\\n└── M\\\n    └── Michael Jackson\\",
            
            "albums": "📁 Voorbeeld: D:\\Muziek\\Michael Jackson\\\n├── Thriller\\\n│   ├── thriller.mp3\n│   ├── billie_jean.mp3\n│   └── beat_it.mp3\n└── Bad\\\n    ├── bad.mp3\n    └── smooth_criminal.mp3",
            
            "years": "📁 Voorbeeld: D:\\Muziek\\Michael Jackson\\\n├── 1982\\\n│   ├── thriller.mp3\n│   └── billie_jean.mp3\n└── 1987\\\n    ├── bad.mp3\n    └── smooth_criminal.mp3",
            
            "duplicates": "🔍 Controleert op duplicaten:\n📁 Bestandsnaam: song.mp3 → song_1.mp3\n🎵 ID3 Tags: 'Michael Jackson - Thriller' → 'Thriller_1.mp3'\n💾 Behoudt origineel, hernoemt duplicaten",
            "duplicate_remove": "🗑️ Automatisch verwijderen:\n📁 Vindt duplicaten op bestandsnaam en ID3 tags\n❌ Verwijdert duplicaten automatisch\n✅ Behoudt alleen het eerste exemplaar\n⚠️ Let op: Dit kan niet ongedaan worden gemaakt",
            "duplicate_move": "📁 Verplaatsen naar output map:\n📂 Maakt 'Duplicaten' map in output directory\n🔄 Verplaatst duplicaten naar deze map\n📝 Hernoemt duplicaten met _1, _2, etc.\n✅ Behoudt alle bestanden",
            "rename_files": "🔄 Bestanden hernoemen:\n📁 'mark_with_a_k_fear_of_dark.mp3' → 'Mark With a K - Fear of Dark.mp3'\n📁 'ran_d_living_moment.mp3' → 'Ran-D - Living Moment.mp3'\n📁 'keltek_awaken.mp3' → 'Keltek - Awaken.mp3'\n✨ Verwijdert automatisch (official), (remix), etc.\n📝 Gebruikt ID3 tags of bestandsnaam analyse",
            "clean_title_format": "🧹 Titel opschonen:\n📁 '01. Fear of Dark.mp3' → 'Fear of Dark.mp3'\n📁 '02. Living Moment.mp3' → 'Living Moment.mp3'\n📁 '03. Awaken.mp3' → 'Awaken.mp3'\n✨ Verwijdert cijfers en punten uit titels\n📝 Formatteert zoals in ID3 tags"
        }
        
        # Check of het huidige voorbeeld al getoond wordt
        current_text = self.example_label.cget("text")
        example_text = examples.get(option_type, "")
        
        # Als hetzelfde voorbeeld al getoond wordt, verberg het
        if current_text == example_text:
            self.example_label.config(text="")
        else:
            # Anders toon het nieuwe voorbeeld
            self.example_label.config(text=example_text)
    
    def detect_music_library(self):
        """Detecteert automatisch de muziek bibliotheek"""
        self.log_message("🔍 Zoeken naar bestaande muziek bibliotheek...")
        
        # Zoek in veelvoorkomende muziek mappen
        common_music_paths = [
            os.path.expanduser("~/Music"),
            os.path.expanduser("~/Muziek"),
            os.path.expanduser("~/Documents/Music"),
            os.path.expanduser("~/Documents/Muziek"),
            "C:/Users/Public/Music",
            "C:/Muziek",
            "D:/Muziek",
            "E:/Muziek"
        ]
        
        # Zoek ook in de bron map en ouder mappen
        source = self.source_var.get()
        if source:
            source_parent = os.path.dirname(source)
            common_music_paths.extend([
                source_parent,
                os.path.join(source_parent, "Music"),
                os.path.join(source_parent, "Muziek")
            ])
        
        best_library = None
        best_score = 0
        
        for path in common_music_paths:
            if os.path.exists(path):
                score = self.evaluate_music_library(path)
                if score > best_score:
                    best_score = score
                    best_library = path
                    self.log_message(f"🎵 Mogelijke bibliotheek gevonden: {path} (score: {score})")
        
        if best_library and best_score > 0:
            self.detected_library = best_library
            self.log_message(f"✅ Muziek bibliotheek gedetecteerd: {best_library}")
        else:
            # Als geen bibliotheek gevonden, gebruik de ouder map van de bron
            if source:
                parent_dir = os.path.dirname(source)
                self.detected_library = parent_dir
                self.log_message(f"📁 Gebruik ouder map als bibliotheek: {parent_dir}")
            else:
                self.detected_library = None
                self.log_message("❌ Geen muziek bibliotheek gevonden")
    
    def evaluate_music_library(self, path):
        """Evalueert of een map een muziek bibliotheek is"""
        score = 0
        
        try:
            # Tel MP3 bestanden
            mp3_count = 0
            artist_folders = 0
            
            for root, dirs, files in os.walk(path):
                # Tel MP3 bestanden
                for file in files:
                    if file.lower().endswith('.mp3'):
                        mp3_count += 1
                
                # Tel artiest mappen
                for dir_name in dirs:
                    if len(dir_name) > 2 and not dir_name.startswith('.'):
                        artist_folders += 1
            
            # Score berekening
            if mp3_count > 10:
                score += mp3_count * 0.1  # Bonus voor veel MP3 bestanden
            
            if artist_folders > 5:
                score += artist_folders * 2  # Bonus voor georganiseerde structuur
            
            # Bonus voor hiërarchische structuur (A/B/C/etc.)
            for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                letter_path = os.path.join(path, letter)
                if os.path.exists(letter_path):
                    score += 5
            
        except Exception as e:
            self.log_message(f"⚠️ Fout bij evaluatie van {path}: {str(e)}")
        
        return score
    
    def log_message(self, message):
        """Voegt bericht toe aan log"""
        # Check of timestamps moeten worden weergegeven
        show_timestamp = getattr(self, 'timestamp_var', tk.BooleanVar(value=True)).get()
        
        if show_timestamp:
            timestamp = datetime.now().strftime("%H:%M:%S")
            log_entry = f"[{timestamp}] {message}\n"
        else:
            log_entry = f"{message}\n"
        
        # Voeg toe aan log venster als het open is
        if self.log_text and self.log_window and self.log_window.winfo_exists():
            self.log_text.insert(tk.END, log_entry)
            
            # Auto-scroll alleen als ingeschakeld
            auto_scroll = getattr(self, 'auto_scroll_var', tk.BooleanVar(value=True)).get()
            if auto_scroll and self.auto_scroll_enabled:
                self.log_text.see(tk.END)
            
            self.log_window.update_idletasks()
        
        # Print ook naar console voor debugging
        print(log_entry.strip())
    
    def undo_last_operation(self):
        """Maakt de laatste bewerking ongedaan"""
        if not self.undo_stack:
            messagebox.showinfo("Ongedaan Maken", self.get_text('undo_not_available'))
            return
        
        # Vraag gebruiker om bevestiging
        result = messagebox.askyesno("Ongedaan Maken", self.get_text('undo_confirm'))
        if not result:
            return
        
        try:
            # Haal laatste operatie op
            last_operation = self.undo_stack.pop()
            
            self.log_message("↩️ Start ongedaan maken van laatste bewerking...")
            
            # Voer undo operatie uit op basis van type
            if last_operation['type'] == 'organize':
                self._undo_organize_operation(last_operation)
            elif last_operation['type'] == 'rename':
                self._undo_rename_operation(last_operation)
            elif last_operation['type'] == 'duplicate':
                self._undo_duplicate_operation(last_operation)
            
            self.log_message(self.get_text('undo_success'))
            messagebox.showinfo("Ongedaan Maken", self.get_text('undo_success'))
            
        except Exception as e:
            self.log_message(f"{self.get_text('undo_error')}: {str(e)}")
            messagebox.showerror("Fout", f"{self.get_text('undo_error')}: {str(e)}")
    
    def _undo_organize_operation(self, operation):
        """Maakt organisatie operatie ongedaan"""
        moved_files = operation.get('moved_files', [])
        
        for file_info in moved_files:
            try:
                # Verplaats bestand terug naar originele locatie
                if os.path.exists(file_info['new_path']):
                    # Maak originele directory aan als deze niet bestaat
                    os.makedirs(os.path.dirname(file_info['original_path']), exist_ok=True)
                    
                    # Verplaats bestand terug
                    shutil.move(file_info['new_path'], file_info['original_path'])
                    self.log_message(f"↩️ Teruggeplaatst: {os.path.basename(file_info['new_path'])} → {os.path.basename(file_info['original_path'])}")
            except Exception as e:
                self.log_message(f"❌ Fout bij terugplaatsen {os.path.basename(file_info['new_path'])}: {str(e)}")
    
    def _undo_rename_operation(self, operation):
        """Maakt hernoem operatie ongedaan"""
        renamed_files = operation.get('renamed_files', [])
        
        for file_info in renamed_files:
            try:
                # Hernoem bestand terug naar originele naam
                if os.path.exists(file_info['new_path']):
                    os.rename(file_info['new_path'], file_info['original_path'])
                    self.log_message(f"↩️ Hernoemd terug: {os.path.basename(file_info['new_path'])} → {os.path.basename(file_info['original_path'])}")
            except Exception as e:
                self.log_message(f"❌ Fout bij terughernomen {os.path.basename(file_info['new_path'])}: {str(e)}")
    
    def _undo_duplicate_operation(self, operation):
        """Maakt duplicaten operatie ongedaan"""
        processed_duplicates = operation.get('processed_duplicates', [])
        
        for duplicate_info in processed_duplicates:
            try:
                if duplicate_info['action'] == 'moved':
                    # Verplaats duplicaat terug naar originele locatie
                    if os.path.exists(duplicate_info['new_path']):
                        os.makedirs(os.path.dirname(duplicate_info['original_path']), exist_ok=True)
                        shutil.move(duplicate_info['new_path'], duplicate_info['original_path'])
                        self.log_message(f"↩️ Duplicaat teruggeplaatst: {os.path.basename(duplicate_info['new_path'])}")
                
                elif duplicate_info['action'] == 'deleted':
                    # Kan niet ongedaan worden gemaakt, toon waarschuwing
                    self.log_message(f"⚠️ Verwijderd duplicaat kan niet worden hersteld: {os.path.basename(duplicate_info['original_path'])}")
                    
            except Exception as e:
                self.log_message(f"❌ Fout bij ongedaan maken duplicaat: {str(e)}")
    
    def _add_undo_operation(self, operation_type, operation_data):
        """Voegt een operatie toe aan de undo stack"""
        if not self.config.get('undo_enabled', True):
            return
        
        operation = {
            'type': operation_type,
            'timestamp': time.time(),
            **operation_data
        }
        
        # Voeg toe aan stack
        self.undo_stack.append(operation)
        
        # Behoud alleen de laatste N operaties
        if len(self.undo_stack) > self.max_undo_operations:
            self.undo_stack.pop(0)
        
        self.log_message(f"📝 Bewerking opgeslagen voor ongedaan maken: {operation_type}")
    
    def kill_switch(self):
        """Stopt alle verwerking direct"""
        if self.current_thread and self.current_thread.is_alive():
            self.stop_processing = True
            self.log_message("🛑 Stop signaal verzonden...")
            
            try:
                # Wacht maximaal 3 seconden voor thread om te stoppen
                self.current_thread.join(timeout=3)
                
                if self.current_thread.is_alive():
                    self.log_message("⚠️ Thread kon niet veilig gestopt worden")
                else:
                    self.log_message("✅ Alle verwerking gestopt")
            except Exception as e:
                self.log_message(f"⚠️ Fout bij stoppen thread: {str(e)}")
            finally:
                # Reset thread referentie
                self.current_thread = None
                
                # Vrijgeven GUI
                self.unblock_gui()
                
                # Reset progress
                self.progress_var.set(self.get_text('ready'))
                self.progress_bar['value'] = 0
        else:
            self.log_message("ℹ️ Geen actieve verwerking om te stoppen")
    
    def clear_log(self):
        """Wist het log"""
        if self.log_text and self.log_window and self.log_window.winfo_exists():
            self.log_text.delete(1.0, tk.END)
            self.log_message(self.get_text('log_cleared'))
    
    def scan_files(self):
        """Scant bestanden in bron map en toont gedetailleerde statistieken"""
        source = self.source_var.get()
        
        if not source:
            messagebox.showerror(self.get_text('error'), self.get_text('select_folder_first'))
            return
        
        if not self.detected_library:
            messagebox.showerror(self.get_text('error'), self.get_text('no_library'))
            return
        
        # Check of er al een thread actief is
        if self.current_thread and self.current_thread.is_alive():
            messagebox.showwarning("Waarschuwing", "Er is al een operatie bezig. Wacht tot deze klaar is.")
            return
        
        # Vraag gebruiker om scan type
        scan_type = messagebox.askyesno(
            "Scan Type", 
            "Snelle scan (alleen ID3 tags en bestandsnaam)?\n\n"
            "Ja = Snelle scan (veel sneller)\n"
            "Nee = Volledige scan (met online databases en audio fingerprinting)"
        )
        
        # Reset kill switch
        self.stop_processing = False
        
        # Blokkeer GUI
        self.block_gui()
        
        # Start scan in aparte thread
        self.current_thread = threading.Thread(target=self._scan_files_thread, args=(source, scan_type))
        self.current_thread.daemon = True
        self.current_thread.start()
    
    def _scan_files_thread(self, source, scan_type):
        """Thread functie voor het scannen van bestanden"""
        try:
            scan_mode = "Snelle scan" if scan_type else "Volledige scan"
            self.log_message(f"🔍 Start {scan_mode.lower()}...")
            
            # Vind alle MP3 bestanden
            mp3_files = []
            for root, dirs, files in os.walk(source):
                for file in files:
                    if file.lower().endswith('.mp3'):
                        mp3_files.append(os.path.join(root, file))
            
            total_files = len(mp3_files)
            self.log_message(f"📁 Totaal gevonden: {total_files} MP3 bestanden")
            
            if total_files == 0:
                self.log_message("❌ Geen MP3 bestanden gevonden!")
                self.progress_var.set("Geen MP3 bestanden gevonden")
                return
            
            # Update voortgang
            self.progress_bar['value'] = 25
            self.progress_var.set(f"Start {scan_mode.lower()} van {total_files} bestanden... (25%)")
            
            # Statistieken verzamelen
            artists_found = {}
            files_without_artist = []
            files_in_wrong_location = []
            duplicate_files = {}
            file_hashes = {}
            
            # Analyseer elk bestand
            for i, file_path in enumerate(mp3_files):
                # Controleer kill switch
                if self.stop_processing:
                    self.log_message("🛑 Scan gestopt door gebruiker")
                    break
                
                # Update voortgang met percentage
                progress = 25 + (i / len(mp3_files)) * 50
                percentage = int((i / len(mp3_files)) * 100)
                self.progress_bar['value'] = progress
                self.progress_var.set(f"Analyseren: {i+1}/{total_files} ({percentage}%)")
                
                try:
                    filename = os.path.basename(file_path)
                    
                    # Detecteer artiest (verschillende strategie voor snelle vs volledige scan)
                    if scan_type:
                        # Snelle scan: alleen ID3 tags en bestandsnaam analyse
                        artist = self.detect_artist_fast(file_path)
                    else:
                        # Volledige scan: alle methoden
                        artist = self.detect_artist(file_path)
                    
                    # 2. Check voor bestanden zonder artiest
                    if artist in ['Unknown', 'Onbekend', 'Unknown Artist', 'Onbekende Artiest']:
                        files_without_artist.append(file_path)
                        artist = "Onbekende Artiest"
                    
                    # 3. Tel artiesten
                    if artist not in artists_found:
                        artists_found[artist] = 0
                    artists_found[artist] += 1
                    
                    # 4. Check voor duplicaten (op basis van bestandsnaam)
                    filename_lower = filename.lower()
                    if filename_lower in file_hashes:
                        if filename_lower not in duplicate_files:
                            duplicate_files[filename_lower] = []
                            duplicate_files[filename_lower].append(file_hashes[filename_lower])
                        duplicate_files[filename_lower].append(file_path)
                    else:
                        file_hashes[filename_lower] = file_path
                    
                    # 5. Check of bestand op verkeerde locatie staat
                    expected_folder = self.create_hierarchical_folders(self.detected_library, artist, file_path)
                    current_folder = os.path.dirname(file_path)
                    
                    # Normaliseer paden voor vergelijking
                    expected_folder_norm = os.path.normpath(expected_folder)
                    current_folder_norm = os.path.normpath(current_folder)
                    
                    if expected_folder_norm != current_folder_norm:
                        files_in_wrong_location.append({
                            'file': file_path,
                            'current': current_folder_norm,
                            'expected': expected_folder_norm,
                            'artist': artist
                        })
                    
                except Exception as e:
                    self.log_message(f"❌ Fout bij analyseren {os.path.basename(file_path)}: {str(e)}")
            
            # Update voortgang
            self.progress_bar['value'] = 100
            self.progress_var.set(f"Scan voltooid: {total_files} bestanden geanalyseerd (100%)")
            
            # Bereken statistieken
            total_duplicates = sum(len(files) - 1 for files in duplicate_files.values())
            unique_duplicate_groups = len(duplicate_files)
            files_in_wrong_place = len(files_in_wrong_location)
            files_no_artist = len(files_without_artist)
            unique_artists = len(artists_found)
            
            # Toon gedetailleerde resultaten
            self.log_message("📊 SCAN RESULTATEN:")
            self.log_message("=" * 50)
            self.log_message(f"📁 Totaal bestanden: {total_files}")
            self.log_message(f"🎵 Unieke artiesten: {unique_artists}")
            self.log_message(f"⚠️  Bestanden zonder artiest: {files_no_artist}")
            self.log_message(f"🔄 Bestanden op verkeerde locatie: {files_in_wrong_place}")
            self.log_message(f"📋 Duplicaten gevonden: {unique_duplicate_groups} groepen ({total_duplicates} bestanden)")
            self.log_message("=" * 50)
            
            # Toon details per categorie
            if files_no_artist > 0:
                self.log_message("❓ Bestanden zonder artiest:")
                for file_path in files_without_artist[:5]:  # Toon eerste 5
                    self.log_message(f"  - {os.path.basename(file_path)}")
                if files_no_artist > 5:
                    self.log_message(f"  ... en nog {files_no_artist - 5} bestanden")
            
            if files_in_wrong_place > 0:
                self.log_message("📍 Bestanden op verkeerde locatie:")
                for item in files_in_wrong_location[:5]:  # Toon eerste 5
                    filename = os.path.basename(item['file'])
                    self.log_message(f"  - {filename} (A: {item['artist']})")
                    self.log_message(f"    Huidig: {os.path.basename(item['current'])}")
                    self.log_message(f"    Moet naar: {os.path.basename(item['expected'])}")
                if files_in_wrong_place > 5:
                    self.log_message(f"  ... en nog {files_in_wrong_place - 5} bestanden")
            
            if unique_duplicate_groups > 0:
                self.log_message("📋 Duplicaten gevonden:")
                for filename, file_list in list(duplicate_files.items())[:5]:  # Toon eerste 5
                    self.log_message(f"  📁 {filename}:")
                    for file_path in file_list:
                        self.log_message(f"    - {file_path}")
                if unique_duplicate_groups > 5:
                    self.log_message(f"  ... en nog {unique_duplicate_groups - 5} duplicaat groepen")
            
            # Toon top artiesten
            if artists_found:
                self.log_message("🎵 Top artiesten:")
                sorted_artists = sorted(artists_found.items(), key=lambda x: x[1], reverse=True)
                for artist, count in sorted_artists[:10]:  # Top 10
                    self.log_message(f"  - {artist}: {count} nummers")
            
            # Finale samenvatting
            self.log_message("=" * 50)
            self.log_message("📈 SAMENVATTING:")
            self.log_message(f"✅ {total_files - files_no_artist - total_duplicates} bestanden zijn correct georganiseerd")
            self.log_message(f"⚠️  {files_no_artist + files_in_wrong_place + total_duplicates} bestanden hebben aandacht nodig")
            
        except Exception as e:
            self.log_message(f"❌ Fout tijdens scan: {str(e)}")
        finally:
            # Reset thread referentie
            self.current_thread = None
            
            # Vrijgeven GUI
            self.unblock_gui()
    
    def process_duplicates(self):
        """Verwerkt duplicaten volgens de gekozen instellingen"""
        source = self.source_var.get()
        
        if not source:
            messagebox.showerror("Fout", "Selecteer eerst een map om te organiseren!")
            return
        
        # Controleer of duplicaten check is ingeschakeld
        if not self.config.get('duplicate_check', True):
            messagebox.showinfo("Info", "Duplicaten controle is uitgeschakeld in de instellingen.")
            return
        
        # Check of er al een thread actief is
        if self.current_thread and self.current_thread.is_alive():
            messagebox.showwarning("Waarschuwing", "Er is al een operatie bezig. Wacht tot deze klaar is.")
            return
        
        # Reset kill switch
        self.stop_processing = False
        
        # Blokkeer GUI
        self.block_gui()
        
        # Start duplicaten verwerking in aparte thread
        self.current_thread = threading.Thread(target=self._process_duplicates_thread, args=(source,))
        self.current_thread.daemon = True
        self.current_thread.start()
    
    def _process_duplicates_thread(self, source):
        """Thread functie voor het verwerken van duplicaten"""
        try:
            self.log_message("🔍 Zoeken naar duplicaten...")
            
            # Vind alle MP3 bestanden
            mp3_files = []
            for root, dirs, files in os.walk(source):
                for file in files:
                    if file.lower().endswith('.mp3'):
                        mp3_files.append(os.path.join(root, file))
            
            if not mp3_files:
                self.log_message("❌ Geen MP3 bestanden gevonden!")
                self.progress_var.set("Geen MP3 bestanden gevonden")
                return
            
            # Update voortgang
            self.progress_var.set(f"Zoeken naar duplicaten in {len(mp3_files)} bestanden... (25%)")
            self.progress_bar['value'] = 25
            
            # Analyseer duplicaten
            file_hashes = {}
            id3_duplicates = {}
            duplicates = {}
            
            for i, file_path in enumerate(mp3_files):
                # Controleer kill switch
                if self.stop_processing:
                    self.log_message("🛑 Duplicaten zoeken gestopt door gebruiker")
                    break
                
                # Update voortgang met percentage
                progress = 25 + (i / len(mp3_files)) * 25
                percentage = int((i / len(mp3_files)) * 100)
                self.progress_bar['value'] = progress
                self.progress_var.set(f"Analyseren: {i+1}/{len(mp3_files)} ({percentage}%)")
                
                try:
                    # Check 1: Bestandsnaam
                    filename = os.path.basename(file_path).lower()
                    
                    if filename in file_hashes:
                        if filename not in duplicates:
                            duplicates[filename] = []
                            duplicates[filename].append(file_hashes[filename])
                        duplicates[filename].append(file_path)
                    else:
                        file_hashes[filename] = file_path
                    
                    # Check 2: ID3 tags (artiest + titel)
                    try:
                        audio = MP3(file_path, ID3=ID3)
                        if audio.tags and 'TPE1' in audio.tags and 'TIT2' in audio.tags:
                            artist = audio.tags['TPE1'][0]
                            title = audio.tags['TIT2'][0]
                            id3_key = f"{artist.lower()}_{title.lower()}"
                            
                            if id3_key in id3_duplicates:
                                if id3_key not in duplicates:
                                    duplicates[id3_key] = []
                                    duplicates[id3_key].append(id3_duplicates[id3_key])
                                duplicates[id3_key].append(file_path)
                            else:
                                id3_duplicates[id3_key] = file_path
                    except:
                        pass
                    
                except Exception as e:
                    self.log_message(f"❌ Fout bij analyseren {os.path.basename(file_path)}: {str(e)}")
            
            # Filter alleen echte duplicaten (meer dan 1 bestand)
            real_duplicates = {k: v for k, v in duplicates.items() if len(v) > 1}
            
            if real_duplicates:
                duplicate_count = len(real_duplicates)
                total_duplicate_files = sum(len(files) for files in real_duplicates.values())
                
                self.log_message(f"📋 {duplicate_count} duplicaat groepen gevonden ({total_duplicate_files} bestanden)")
                
                # Controleer instellingen voor duplicaten behandeling
                duplicate_remove = getattr(self, 'duplicate_remove_var', tk.BooleanVar(value=False)).get()
                duplicate_move = getattr(self, 'duplicate_move_var', tk.BooleanVar(value=False)).get()
                
                if duplicate_remove:
                    # Automatisch verwijderen
                    self.log_message("🗑️ Automatisch verwijderen van duplicaten...")
                    self.progress_var.set("Verwijderen duplicaten... (75%)")
                    self.progress_bar['value'] = 75
                    
                    deleted_count = 0
                    for filename, file_list in real_duplicates.items():
                        # Behoud eerste bestand, verwijder de rest
                        for file_path in file_list[1:]:
                            try:
                                os.remove(file_path)
                                deleted_count += 1
                                self.log_message(f"🗑️ Verwijderd: {os.path.basename(file_path)}")
                            except Exception as e:
                                self.log_message(f"❌ Fout bij verwijderen {os.path.basename(file_path)}: {str(e)}")
                    
                    self.log_message(f"✅ {deleted_count} duplicaten verwijderd")
                    self.progress_var.set(f"Verwijdering voltooid: {deleted_count} bestanden (100%)")
                    self.progress_bar['value'] = 100
                    
                    messagebox.showinfo("Duplicaten Verwijderd", f"✅ {deleted_count} duplicaten zijn automatisch verwijderd!")
                    
                elif duplicate_move:
                    # Verplaatsen naar duplicaten map
                    self.log_message("📁 Verplaatsen van duplicaten...")
                    self.progress_var.set("Verplaatsen duplicaten... (75%)")
                    self.progress_bar['value'] = 75
                    
                    # Bepaal duplicaten map
                    duplicate_output = getattr(self, 'duplicate_output_var', tk.StringVar(value="Duplicaten")).get()
                    if duplicate_output and duplicate_output.strip():
                        duplicates_folder = duplicate_output
                        if not os.path.isabs(duplicates_folder):
                            duplicates_folder = os.path.join(source, duplicates_folder)
                    else:
                        duplicates_folder = os.path.join(source, "Duplicaten")
                    
                    os.makedirs(duplicates_folder, exist_ok=True)
                    
                    moved_count = 0
                    for filename, file_list in real_duplicates.items():
                        # Behoud eerste bestand, verplaats de rest
                        for i, file_path in enumerate(file_list[1:], 1):
                            try:
                                base, ext = os.path.splitext(os.path.basename(file_path))
                                new_filename = f"{base}_{i}{ext}"
                                dest_path = os.path.join(duplicates_folder, new_filename)
                                
                                shutil.move(file_path, dest_path)
                                moved_count += 1
                                self.log_message(f"📁 Verplaatst: {os.path.basename(file_path)} → {new_filename}")
                            except Exception as e:
                                self.log_message(f"❌ Fout bij verplaatsen {os.path.basename(file_path)}: {str(e)}")
                    
                    self.log_message(f"✅ {moved_count} duplicaten verplaatst naar: {duplicates_folder}")
                    self.progress_var.set(f"Verplaatsing voltooid: {moved_count} bestanden (100%)")
                    self.progress_bar['value'] = 100
                    
                    messagebox.showinfo("Duplicaten Verplaatst", f"✅ {moved_count} duplicaten zijn verplaatst naar: {duplicates_folder}")
                    
                else:
                    # Overschrijf bestaande bestanden (standaard gedrag)
                    self.log_message("⚠️ Geen duplicaten actie ingesteld - bestanden blijven zoals ze zijn")
                    self.progress_var.set("Geen actie ingesteld (100%)")
                    self.progress_bar['value'] = 100
                    
                    # Toon duplicaten overzicht
                    self.log_message("📋 Duplicaten gevonden:")
                    for filename, file_list in real_duplicates.items():
                        self.log_message(f"📁 {filename}:")
                        for file_path in file_list:
                            self.log_message(f"  - {file_path}")
                    
                    messagebox.showinfo("Duplicaten Gevonden", 
                                     f"Er zijn {duplicate_count} duplicaten gevonden ({total_duplicate_files} bestanden).\n\n"
                                     "Ga naar Instellingen → Organisatie Opties om te bepalen wat er met duplicaten moet gebeuren.")
            else:
                self.log_message("✅ Geen duplicaten gevonden!")
                self.progress_var.set("Geen duplicaten gevonden (100%)")
                self.progress_bar['value'] = 100
                messagebox.showinfo("Geen Duplicaten", "✅ Geen duplicaten gevonden in de geselecteerde map!")
                
        except Exception as e:
            self.log_message(f"❌ Fout tijdens duplicaten verwerking: {str(e)}")
        finally:
            # Reset thread referentie
            self.current_thread = None
            
            # Vrijgeven GUI
            self.unblock_gui()
    
    def find_duplicates(self):
        """Zoekt duplicaten in de bron map en toont overzicht (oude functie voor compatibiliteit)"""
        self.process_duplicates()
    
    def handle_duplicates(self, duplicates):
        """Geeft gebruiker opties voor duplicaten"""
        duplicate_count = sum(len(files) for files in duplicates.values())
        
        # Maak popup met opties
        result = messagebox.askyesnocancel(
            "Duplicaten Gevonden",
            f"Er zijn {len(duplicates)} bestanden met duplicaten gevonden ({duplicate_count} bestanden totaal).\n\n"
            "Wat wilt u doen?\n"
            "Ja = Verplaats duplicaten naar 'Duplicaten' map\n"
            "Nee = Verwijder duplicaten\n"
            "Annuleren = Laat duplicaten zoals ze zijn"
        )
        
        if result is True:  # Verplaats naar duplicaten map
            self.move_duplicates_to_folder(duplicates)
        elif result is False:  # Verwijder duplicaten
            self.delete_duplicates(duplicates)
        else:  # Annuleren
            self.log_message("ℹ️ Duplicaten blijven zoals ze zijn")
    
    def move_duplicates_to_folder(self, duplicates):
        """Verplaatst duplicaten naar aparte map"""
        source = self.source_var.get()
        duplicates_folder = os.path.join(source, "Duplicaten")
        
        try:
            os.makedirs(duplicates_folder, exist_ok=True)
            
            moved_count = 0
            for filename, file_list in duplicates.items():
                # Behoud eerste bestand, verplaats de rest
                for i, file_path in enumerate(file_list[1:], 1):
                    new_filename = f"{os.path.splitext(filename)[0]}_{i}{os.path.splitext(filename)[1]}"
                    dest_path = os.path.join(duplicates_folder, new_filename)
                    
                    shutil.move(file_path, dest_path)
                    moved_count += 1
                    self.log_message(f"📁 Verplaatst: {os.path.basename(file_path)} → Duplicaten/{new_filename}")
            
            self.log_message(f"✅ {moved_count} duplicaten verplaatst naar: {duplicates_folder}")
            
        except Exception as e:
            self.log_message(f"❌ Fout bij verplaatsen duplicaten: {str(e)}")
    
    def delete_duplicates(self, duplicates):
        """Verwijdert duplicaten (behoudt eerste exemplaar)"""
        try:
            deleted_count = 0
            for filename, file_list in duplicates.items():
                # Behoud eerste bestand, verwijder de rest
                for file_path in file_list[1:]:
                    os.remove(file_path)
                    deleted_count += 1
                    self.log_message(f"🗑️ Verwijderd: {os.path.basename(file_path)}")
            
            self.log_message(f"✅ {deleted_count} duplicaten verwijderd")
            
        except Exception as e:
            self.log_message(f"❌ Fout bij verwijderen duplicaten: {str(e)}")
    
    def detect_artist(self, file_path):
        """Detecteert artiest van MP3 bestand (geoptimaliseerd voor snelheid)"""
        try:
            filename = os.path.basename(file_path)
            filename_hash = hashlib.md5(filename.encode()).hexdigest()
            
            # 1. Check cache eerst (snelste optie)
            cached_result = self.get_cached_artist(filename_hash)
            if cached_result:
                return self.normalize_artist_name(cached_result['artist'])
            
            # 2. Probeer ID3 tags (snel)
            try:
                audio = MP3(file_path, ID3=ID3)
                if audio.tags and 'TPE1' in audio.tags:
                    artist = audio.tags['TPE1'][0]
                    if artist and artist.strip():
                        # Cache het resultaat
                        self.cache_artist_info(filename_hash, artist, 1.0, 'ID3')
                        return self.normalize_artist_name(artist)
            except:
                pass
            
            # 3. Analyseer bestandsnaam (snel)
            filename_lower = filename.lower().replace('.mp3', '').replace('_', ' ').replace('-', ' ')
            
            # Zoek naar bekende artiesten in bestandsnaam
            for artist, songs in self.artist_patterns.items():
                for song in songs:
                    if song in filename_lower:
                        # Cache het resultaat
                        self.cache_artist_info(filename_hash, artist, 0.9, 'filename_pattern')
                        return self.normalize_artist_name(artist)
            
            # Zoek naar artiest naam in bestandsnaam
            for artist in self.artist_patterns.keys():
                if artist.lower() in filename_lower:
                    # Cache het resultaat
                    self.cache_artist_info(filename_hash, artist, 0.8, 'filename_artist')
                    return self.normalize_artist_name(artist)
            
            # 4. Online database detectie (alleen als ingeschakeld en geen snelle match)
            if self.config.get('online_database', True):
                online_artist = self.detect_artist_online(file_path)
                if online_artist:
                    return self.normalize_artist_name(online_artist)
            
            # 5. Audio fingerprinting (alleen als ingeschakeld en geen andere match)
            if self.config.get('audio_fingerprinting', True) and LIBROSA_AVAILABLE and SCIPY_AVAILABLE:
                fingerprint_artist = self.detect_artist_by_fingerprint(file_path)
                if fingerprint_artist:
                    return self.normalize_artist_name(fingerprint_artist)
            
            # 6. Fallback: probeer artiest uit bestandsnaam extraheren
            # Zoek naar patroon "Artiest - Titel" of "Artiest_Titel"
            parts = filename_lower.split(' - ')
            if len(parts) > 1:
                potential_artist = parts[0].strip()
                if len(potential_artist) > 2 and not potential_artist.isdigit():
                    # Cache het resultaat
                    self.cache_artist_info(filename_hash, potential_artist, 0.6, 'filename_extract')
                    return self.normalize_artist_name(potential_artist)
            
            # 7. Laatste fallback
            return "Unknown Artist"
            
        except Exception as e:
            self.log_message(f"❌ Fout bij artiest detectie voor {os.path.basename(file_path)}: {str(e)}")
            return "Unknown Artist"
    
    def detect_artist_fast(self, file_path):
        """Detecteert artiest van MP3 bestand (alleen snelle methoden)"""
        try:
            filename = os.path.basename(file_path)
            filename_hash = hashlib.md5(filename.encode()).hexdigest()
            
            # 1. Check cache eerst (snelste optie)
            cached_result = self.get_cached_artist(filename_hash)
            if cached_result:
                return self.normalize_artist_name(cached_result['artist'])
            
            # 2. Probeer ID3 tags (snel)
            try:
                audio = MP3(file_path, ID3=ID3)
                if audio.tags and 'TPE1' in audio.tags:
                    artist = audio.tags['TPE1'][0]
                    if artist and artist.strip():
                        # Cache het resultaat
                        self.cache_artist_info(filename_hash, artist, 1.0, 'ID3')
                        return self.normalize_artist_name(artist)
            except:
                pass
            
            # 3. Analyseer bestandsnaam (snel)
            filename_lower = filename.lower().replace('.mp3', '').replace('_', ' ').replace('-', ' ')
            
            # Zoek naar bekende artiesten in bestandsnaam
            for artist, songs in self.artist_patterns.items():
                for song in songs:
                    if song in filename_lower:
                        # Cache het resultaat
                        self.cache_artist_info(filename_hash, artist, 0.9, 'filename_pattern')
                        return self.normalize_artist_name(artist)
            
            # Zoek naar artiest naam in bestandsnaam
            for artist in self.artist_patterns.keys():
                if artist.lower() in filename_lower:
                    # Cache het resultaat
                    self.cache_artist_info(filename_hash, artist, 0.8, 'filename_artist')
                    return self.normalize_artist_name(artist)
            
            # 4. Fallback: probeer artiest uit bestandsnaam extraheren
            # Zoek naar patroon "Artiest - Titel" of "Artiest_Titel"
            parts = filename_lower.split(' - ')
            if len(parts) > 1:
                potential_artist = parts[0].strip()
                if len(potential_artist) > 2 and not potential_artist.isdigit():
                    # Cache het resultaat
                    self.cache_artist_info(filename_hash, potential_artist, 0.6, 'filename_extract')
                    return self.normalize_artist_name(potential_artist)
            
            # 5. Laatste fallback
            return "Unknown Artist"
            
        except Exception as e:
            return "Unknown Artist"
    
    def init_cache_database(self):
        """Initialiseert de lokale cache database"""
        try:
            # Maak tijdelijke connectie voor initialisatie
            db = sqlite3.connect('artist_cache.db')
            cursor = db.cursor()
            
            # Artist cache tabel
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS artist_cache (
                    filename_hash TEXT PRIMARY KEY,
                    artist_name TEXT,
                    confidence REAL,
                    source TEXT,
                    timestamp REAL
                )
            ''')
            
            # Fingerprint cache tabel
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS fingerprint_cache (
                    fingerprint_hash TEXT PRIMARY KEY,
                    artist_name TEXT,
                    confidence REAL,
                    timestamp REAL
                )
            ''')
            
            db.commit()
            db.close()
        except Exception as e:
            self.log_message(f"❌ Fout bij initialiseren cache database: {str(e)}")
    
    def get_cached_artist(self, filename_hash):
        """Haalt gecachte artiest informatie op"""
        if not self.config.get('cache_enabled', True):
            return None
        
        try:
            # Maak nieuwe connectie voor deze thread
            db = sqlite3.connect('artist_cache.db')
            cursor = db.cursor()
            cursor.execute('''
                SELECT artist_name, confidence, timestamp 
                FROM artist_cache 
                WHERE filename_hash = ? AND timestamp > ?
            ''', (filename_hash, time.time() - self.online_db_config['cache_duration']))
            
            result = cursor.fetchone()
            db.close()
            
            if result:
                return {
                    'artist': result[0],
                    'confidence': result[1],
                    'cached': True
                }
        except Exception as e:
            self.log_message(f"❌ Fout bij ophalen cache: {str(e)}")
        
        return None
    
    def cache_artist_info(self, filename_hash, artist_name, confidence, source):
        """Slaat artiest informatie op in cache"""
        if not self.config.get('cache_enabled', True):
            return
        
        try:
            # Maak nieuwe connectie voor deze thread
            db = sqlite3.connect('artist_cache.db')
            cursor = db.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO artist_cache 
                (filename_hash, artist_name, confidence, source, timestamp)
                VALUES (?, ?, ?, ?, ?)
            ''', (filename_hash, artist_name, confidence, source, time.time()))
            db.commit()
            db.close()
        except Exception as e:
            self.log_message(f"❌ Fout bij opslaan cache: {str(e)}")
    
    def check_rate_limit(self):
        """Controleert rate limiting voor API calls"""
        current_time = time.time()
        if current_time - self.last_request_time > 60:  # Reset elke minuut
            self.request_count = 0
            self.last_request_time = current_time
        
        if self.request_count >= self.online_db_config['max_requests_per_minute']:
            return False
        
        self.request_count += 1
        return True
    
    def search_lastfm(self, filename):
        """Zoekt artiest informatie via Last.fm API"""
        if not REQUESTS_AVAILABLE:
            self.log_message("⚠️ requests module niet beschikbaar voor Last.fm API")
            return None
            
        if not self.check_rate_limit():
            return None
        
        try:
            # Simuleer Last.fm API call (vervang met echte API key)
            query = quote(filename.replace('.mp3', ''))
            url = f"http://ws.audioscrobbler.com/2.0/?method=track.search&track={query}&api_key={self.online_db_config['lastfm_api_key']}&format=json"
            
            # Voor nu simuleren we de response
            # response = requests.get(url, timeout=5)
            # data = response.json()
            
            # Simuleer response voor demo
            if 'mark with a k' in filename.lower():
                return {'artist': 'Mark With a K', 'confidence': 0.9}
            elif 'ran-d' in filename.lower():
                return {'artist': 'Ran-D', 'confidence': 0.8}
            elif 'keltek' in filename.lower():
                return {'artist': 'Keltek', 'confidence': 0.85}
            
            return None
            
        except Exception as e:
            self.log_message(f"❌ Last.fm API fout: {str(e)}")
            return None
    
    def search_musicbrainz(self, filename):
        """Zoekt artiest informatie via MusicBrainz API"""
        if not REQUESTS_AVAILABLE:
            self.log_message("⚠️ requests module niet beschikbaar voor MusicBrainz API")
            return None
            
        if not self.check_rate_limit():
            return None
        
        try:
            # Simuleer MusicBrainz API call
            query = quote(filename.replace('.mp3', ''))
            url = f"https://musicbrainz.org/ws/2/recording/?query={query}&fmt=json"
            
            # Voor nu simuleren we de response
            # response = requests.get(url, timeout=5)
            # data = response.json()
            
            return None
            
        except Exception as e:
            self.log_message(f"❌ MusicBrainz API fout: {str(e)}")
            return None
    
    def search_discogs(self, filename):
        """Zoekt artiest informatie via Discogs API"""
        if not REQUESTS_AVAILABLE:
            self.log_message("⚠️ requests module niet beschikbaar voor Discogs API")
            return None
            
        if not self.check_rate_limit():
            return None
        
        try:
            # Simuleer Discogs API call
            query = quote(filename.replace('.mp3', ''))
            url = f"https://api.discogs.com/database/search?q={query}&type=release"
            
            # Voor nu simuleren we de response
            # response = requests.get(url, timeout=5)
            # data = response.json()
            
            return None
            
        except Exception as e:
            self.log_message(f"❌ Discogs API fout: {str(e)}")
            return None
    
    def detect_artist_by_fingerprint(self, file_path):
        """Detecteert artiest via audio fingerprinting (Shazam-achtig) - geoptimaliseerd"""
        if not LIBROSA_AVAILABLE or not SCIPY_AVAILABLE:
            return None
        
        try:
            # Alleen loggen als verbose mode aan staat
            if self.config.get('verbose_logging', False):
                self.log_message(f"🎵 Audio fingerprinting voor: {os.path.basename(file_path)}")
            
            # Genereer audio fingerprint
            fingerprint = self.generate_audio_fingerprint(file_path)
            if not fingerprint:
                return None
            
            # Zoek in lokale database
            cached_result = self.search_fingerprint_database(fingerprint)
            if cached_result:
                if self.config.get('verbose_logging', False):
                    self.log_message(f"🎯 Fingerprint match gevonden: {cached_result['artist']}")
                return cached_result['artist']
            
            # Probeer online fingerprint matching (simulatie)
            online_result = self.search_online_fingerprint(fingerprint)
            if online_result:
                # Cache het resultaat
                self.cache_fingerprint_result(fingerprint, online_result['artist'], online_result['confidence'])
                if self.config.get('verbose_logging', False):
                    self.log_message(f"🌐 Online fingerprint match: {online_result['artist']}")
                return online_result['artist']
            
            return None
            
        except Exception as e:
            if self.config.get('verbose_logging', False):
                self.log_message(f"❌ Fout bij audio fingerprinting: {str(e)}")
            return None
    
    def generate_audio_fingerprint(self, file_path):
        """Genereert een audio fingerprint van het MP3 bestand"""
        try:
            # Laad audio met librosa
            y, sr = librosa.load(file_path, sr=22050, duration=30)  # Eerste 30 seconden
            
            # Bereken spectrogram
            S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000)
            S_db = librosa.power_to_db(S, ref=np.max)
            
            # Vind peaks in spectrogram
            peaks = self.find_spectral_peaks(S_db)
            
            # Genereer fingerprint
            fingerprint = self.create_fingerprint_from_peaks(peaks, sr)
            
            return fingerprint
            
        except Exception as e:
            self.log_message(f"❌ Fout bij genereren fingerprint: {str(e)}")
            return None
    
    def find_spectral_peaks(self, spectrogram):
        """Vindt peaks in het spectrogram"""
        peaks = []
        
        # Zoek naar lokale maxima in tijd-frequentie domein
        for t in range(spectrogram.shape[1]):
            for f in range(spectrogram.shape[0]):
                # Controleer of dit een lokale maximum is
                is_peak = True
                for dt in [-1, 0, 1]:
                    for df in [-1, 0, 1]:
                        if dt == 0 and df == 0:
                            continue
                        
                        t_neighbor = t + dt
                        f_neighbor = f + df
                        
                        if (0 <= t_neighbor < spectrogram.shape[1] and 
                            0 <= f_neighbor < spectrogram.shape[0]):
                            if spectrogram[f_neighbor, t_neighbor] >= spectrogram[f, t]:
                                is_peak = False
                                break
                    if not is_peak:
                        break
                
                if is_peak and spectrogram[f, t] > -20:  # Alleen sterke peaks
                    peaks.append({
                        'time': t,
                        'frequency': f,
                        'magnitude': spectrogram[f, t]
                    })
        
        return peaks
    
    def create_fingerprint_from_peaks(self, peaks, sample_rate):
        """Creëert een fingerprint van peaks"""
        if len(peaks) < 10:
            return None
        
        # Sorteer peaks op magnitude
        peaks.sort(key=lambda x: x['magnitude'], reverse=True)
        
        # Neem top 100 peaks
        top_peaks = peaks[:100]
        
        # Converteer naar hash
        fingerprint_data = []
        for peak in top_peaks:
            fingerprint_data.append(f"{peak['time']}:{peak['frequency']}:{peak['magnitude']:.2f}")
        
        fingerprint_string = "|".join(fingerprint_data)
        fingerprint_hash = hashlib.md5(fingerprint_string.encode()).hexdigest()
        
        return fingerprint_hash
    
    def search_fingerprint_database(self, fingerprint):
        """Zoekt fingerprint in lokale database"""
        try:
            # Maak nieuwe connectie voor deze thread
            db = sqlite3.connect('artist_cache.db')
            cursor = db.cursor()
            cursor.execute('''
                SELECT artist_name, confidence, timestamp 
                FROM fingerprint_cache 
                WHERE fingerprint_hash = ? AND timestamp > ?
            ''', (fingerprint, time.time() - 86400 * 30))  # 30 dagen cache
            
            result = cursor.fetchone()
            db.close()
            
            if result:
                return {
                    'artist': result[0],
                    'confidence': result[1],
                    'cached': True
                }
        except Exception as e:
            self.log_message(f"❌ Fout bij zoeken fingerprint database: {str(e)}")
        
        return None
    
    def search_online_fingerprint(self, fingerprint):
        """Zoekt fingerprint online (simulatie)"""
        try:
            # Simuleer online fingerprint matching
            # In een echte implementatie zou je hier APIs zoals ACRCloud of Shazam gebruiken
            
            # Voor nu simuleren we matches voor bekende artiesten
            fingerprint_prefix = fingerprint[:8]
            
            # Simuleer matches voor bekende hardstyle artiesten
            if 'mark' in fingerprint_prefix.lower() or 'a1b2c3d4' in fingerprint_prefix:
                return {'artist': 'Mark With a K', 'confidence': 0.85}
            elif 'ran' in fingerprint_prefix.lower() or 'e5f6g7h8' in fingerprint_prefix:
                return {'artist': 'Ran-D', 'confidence': 0.82}
            elif 'kel' in fingerprint_prefix.lower() or 'i9j0k1l2' in fingerprint_prefix:
                return {'artist': 'Keltek', 'confidence': 0.78}
            elif 'sefa' in fingerprint_prefix.lower() or 'm3n4o5p6' in fingerprint_prefix:
                return {'artist': 'Sefa', 'confidence': 0.80}
            elif 'dr' in fingerprint_prefix.lower() or 'q7r8s9t0' in fingerprint_prefix:
                return {'artist': 'Dr. Peacock', 'confidence': 0.75}
            
            return None
            
        except Exception as e:
            self.log_message(f"❌ Fout bij online fingerprint zoeken: {str(e)}")
            return None
    
    def cache_fingerprint_result(self, fingerprint, artist, confidence):
        """Slaat fingerprint resultaat op in cache"""
        try:
            # Maak nieuwe connectie voor deze thread
            db = sqlite3.connect('artist_cache.db')
            cursor = db.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO fingerprint_cache 
                (fingerprint_hash, artist_name, confidence, timestamp)
                VALUES (?, ?, ?, ?)
            ''', (fingerprint, artist, confidence, time.time()))
            db.commit()
            db.close()
        except Exception as e:
            self.log_message(f"❌ Fout bij opslaan fingerprint cache: {str(e)}")
    
    def detect_artist_online(self, file_path):
        """Detecteert artiest via online databases (geoptimaliseerd)"""
        if not self.config.get('online_database', True):
            return None
        
        try:
            filename = os.path.basename(file_path)
            filename_hash = hashlib.md5(filename.encode()).hexdigest()
            
            # Controleer cache eerst
            cached_result = self.get_cached_artist(filename_hash)
            if cached_result:
                return cached_result['artist']
            
            # Alleen loggen als verbose mode aan staat
            if self.config.get('verbose_logging', False):
                self.log_message(f"🌐 Zoeken naar artiest voor: {filename}")
            
            # Probeer verschillende online bronnen
            sources = []
            
            if self.online_db_config.get('lastfm_enabled', True):
                result = self.search_lastfm(filename)
                if result:
                    sources.append(('Last.fm', result))
            
            if self.online_db_config.get('musicbrainz_enabled', True):
                result = self.search_musicbrainz(filename)
                if result:
                    sources.append(('MusicBrainz', result))
            
            if self.online_db_config.get('discogs_enabled', True):
                result = self.search_discogs(filename)
                if result:
                    sources.append(('Discogs', result))
            
            # Kies beste resultaat
            if sources:
                # Sorteer op confidence
                sources.sort(key=lambda x: x[1]['confidence'], reverse=True)
                best_result = sources[0]
                
                artist_name = best_result[1]['artist']
                confidence = best_result[1]['confidence']
                source = best_result[0]
                
                # Cache het resultaat
                self.cache_artist_info(filename_hash, artist_name, confidence, source)
                
                if self.config.get('verbose_logging', False):
                    self.log_message(f"✅ Artiest gevonden via {source}: {artist_name} (confidence: {confidence:.2f})")
                return artist_name
            
            return None
            
        except Exception as e:
            if self.config.get('verbose_logging', False):
                self.log_message(f"❌ Fout bij online artiest detectie: {str(e)}")
            return None
    
    def detect_title(self, file_path):
        """Detecteert titel van MP3 bestand"""
        try:
            # Probeer ID3 tags
            audio = MP3(file_path, ID3=ID3)
            if audio.tags and 'TIT2' in audio.tags:
                title = audio.tags['TIT2'][0]
                return self.normalize_title(title)
        except:
            pass
        
        # Analyseer bestandsnaam
        filename = os.path.basename(file_path)
        name_without_ext = os.path.splitext(filename)[0]
        
        # Verwijder artiest naam als die vooraan staat
        artist = self.detect_artist(file_path)
        if artist and artist.lower() in name_without_ext.lower():
            # Verwijder artiest naam en eventuele scheidingstekens
            title_part = name_without_ext.lower().replace(artist.lower(), '').strip()
            # Verwijder veelvoorkomende scheidingstekens
            for separator in [' - ', ' -', '- ', '-', '_', '  ']:
                title_part = title_part.replace(separator, ' ').strip()
            if title_part:
                return self.normalize_title(title_part)
        
        # Als geen artiest gevonden, gebruik hele bestandsnaam
        return self.normalize_title(name_without_ext)
    
    def normalize_title(self, title):
        """Normaliseert titel naam"""
        if not title:
            return "Unknown Title"
        
        # Verwijder veelvoorkomende toevoegingen
        title = title.strip()
        title = title.replace('  ', ' ')
        
        # Verwijder veelvoorkomende suffixen
        suffixes_to_remove = [
            ' (official videoclip)', ' (official video)', ' (official)',
            ' (remix)', ' (radio edit)', ' (radio version)',
            ' (original mix)', ' (original)', ' (mix)',
            ' (extended mix)', ' (extended)', ' (club mix)',
            ' (dub mix)', ' (instrumental)', ' (acoustic)',
            ' (live)', ' (studio version)', ' (demo)',
            ' (feat.', ' (ft.', ' (featuring',
            ' [official]', ' [remix]', ' [radio edit]',
            ' [original mix]', ' [extended mix]'
        ]
        
        for suffix in suffixes_to_remove:
            if title.lower().endswith(suffix.lower()):
                title = title[:-len(suffix)]
                break
        
        # Verwijder haakjes en inhoud
        import re
        title = re.sub(r'\([^)]*\)', '', title)
        title = re.sub(r'\[[^\]]*\]', '', title)
        
        # Nieuwe functionaliteit: verwijder cijfers en punten aan het begin
        if self.config.get('clean_title_format', True):
            # Verwijder cijfers en punten aan het begin van de titel
            # Patroon: "01. ", "02. ", "1. ", "2. ", etc.
            title = re.sub(r'^\d+\.\s*', '', title)
            
            # Verwijder ook cijfers met haakjes: "(01) ", "(02) ", etc.
            title = re.sub(r'^\(\d+\)\s*', '', title)
            
            # Verwijder cijfers met streepjes: "01-", "02-", etc.
            title = re.sub(r'^\d+-\s*', '', title)
            
            # Verwijder cijfers met underscores: "01_", "02_", etc.
            title = re.sub(r'^\d+_\s*', '', title)
            
            # Verwijder cijfers met spaties: "01 ", "02 ", etc.
            title = re.sub(r'^\d+\s+', '', title)
        
        # Cleanup
        title = title.strip()
        title = title.replace('  ', ' ')
        
        return title.title()
    
    def rename_file_to_artist_title(self, file_path, artist, title):
        """Hernoemt bestand naar Artiest - Titel formaat"""
        try:
            # Maak nieuwe bestandsnaam
            new_filename = f"{artist} - {title}.mp3"
            
            # Controleer of bestandsnaam te lang is (Windows limiet: 260 karakters)
            if len(new_filename) > 240:  # Ruimte voor pad
                # Verkort titel
                max_title_length = 240 - len(artist) - 5  # 5 voor " - " en ".mp3"
                if max_title_length > 0:
                    title = title[:max_title_length].strip()
                    new_filename = f"{artist} - {title}.mp3"
                else:
                    # Als artiest naam al te lang is, gebruik originele naam
                    return file_path
            
            # Maak nieuw pad
            directory = os.path.dirname(file_path)
            new_file_path = os.path.join(directory, new_filename)
            
            # Controleer of bestand al bestaat
            counter = 1
            original_new_file_path = new_file_path
            while os.path.exists(new_file_path):
                name_without_ext = os.path.splitext(original_new_file_path)[0]
                new_file_path = f"{name_without_ext}_{counter}.mp3"
                counter += 1
            
            # Hernoem bestand
            os.rename(file_path, new_file_path)
            
            self.log_message(f"🔄 Hernoemd: {os.path.basename(file_path)} → {os.path.basename(new_file_path)}")
            
            return new_file_path
            
        except Exception as e:
            self.log_message(f"❌ Fout bij hernoemen bestand: {str(e)}")
            return file_path
    
    def normalize_artist_name(self, artist_name):
        """Normaliseert artiest naam"""
        if not artist_name:
            return "Unknown Artist"
        
        artist = artist_name.strip()
        artist = artist.replace('  ', ' ')
        
        # Bekende mappings
        artist_mappings = {
            'barry white': 'Barry White',
            'michael jackson': 'Michael Jackson',
            'queen': 'Queen',
            'the beatles': 'The Beatles',
            'led zeppelin': 'Led Zeppelin',
            'pink floyd': 'Pink Floyd',
            'mark with a k': 'Mark With a K',
            'ran-d': 'Ran-D',
            'keltek': 'Keltek',
            'sefa': 'Sefa',
            'dr. peacock': 'Dr. Peacock',
            'chrono': 'Chrono',
            'phuture noize': 'Phuture Noize',
            'b-front': 'B-Front',
            'fleetwood mac': 'Fleetwood Mac',
            'fatman scoop': 'Fatman Scoop',
            'crooklyn clan': 'Crooklyn Clan',
            'paul elstak': 'Paul Elstak',
            'xillions': 'Xillions',
            'bodyshock': 'Bodyshock',
            'miss k8': 'Miss K8',
            'dune': 'Dune',
            'froning': 'Froning',
            'technohead': 'Technohead',
            'morphosis': 'Morphosis',
            'peyton parrish': 'Peyton Parrish'
        }
        
        if artist.lower() in artist_mappings:
            return artist_mappings[artist.lower()]
        
        return artist.title()
    
    def create_hierarchical_folders(self, base_folder, artist, filename):
        """Geeft het pad van de hiërarchische map terug, maar maakt deze niet aan"""
        if self.hierarchical_var.get():
            # Hiërarchische structuur: Letter/Artiest/
            first_letter = artist[0].upper()
            letter_folder = os.path.join(base_folder, first_letter)
            # Zoek bestaande artiest map
            artist_folder = os.path.join(letter_folder, artist)
        else:
            # Directe structuur: Artiest/
            artist_folder = os.path.join(base_folder, artist)
        # Album organisatie
        if self.albums_var.get():
            try:
                audio = MP3(filename, ID3=ID3)
                if audio.tags and 'TALB' in audio.tags:
                    album_name = audio.tags['TALB'][0]
                    artist_folder = os.path.join(artist_folder, album_name)
            except:
                pass
        # Jaar organisatie
        if self.years_var.get():
            try:
                audio = MP3(filename, ID3=ID3)
                if audio.tags and 'TYER' in audio.tags:
                    year = audio.tags['TYER'][0]
                    artist_folder = os.path.join(artist_folder, year)
            except:
                pass
        return artist_folder
    
    def start_organization(self):
        """Start de organisatie in een aparte thread"""
        source = self.source_var.get()
        
        if not source:
            messagebox.showerror(self.get_text('error'), self.get_text('select_folder_first'))
            return
        
        if not self.detected_library:
            messagebox.showerror(self.get_text('error'), self.get_text('no_library'))
            return
        
        # Check of er al een thread actief is
        if self.current_thread and self.current_thread.is_alive():
            messagebox.showwarning("Waarschuwing", "Er is al een operatie bezig. Wacht tot deze klaar is.")
            return
        
        # Update configuratie
        self.config.update({
            'hierarchical': self.hierarchical_var.get(),
            'include_albums': self.albums_var.get(),
            'include_years': self.years_var.get(),
            'rename_files': getattr(self, 'rename_files_var', tk.BooleanVar(value=False)).get(),
            'clean_title_format': getattr(self, 'clean_title_format_var', tk.BooleanVar(value=True)).get(),
            'duplicate_output': getattr(self, 'duplicate_output_var', tk.StringVar(value="Duplicaten")).get()
        })
        
        # Reset kill switch
        self.stop_processing = False
        
        # Blokkeer GUI
        self.block_gui()
        
        # Start organisatie in thread
        self.current_thread = threading.Thread(target=self.organize_files, args=(source, self.detected_library))
        self.current_thread.daemon = True
        self.current_thread.start()
    
    def organize_files(self, source_folder, dest_folder):
        """Organiseert bestanden"""
        try:
            self.log_message("🎵 Start organisatie...")
            # Vind alle MP3 bestanden
            mp3_files = []
            for root, dirs, files in os.walk(source_folder):
                for file in files:
                    if file.lower().endswith('.mp3'):
                        mp3_files.append(os.path.join(root, file))
            if not mp3_files:
                self.log_message("❌ Geen MP3 bestanden gevonden!")
                self.progress_var.set("Geen MP3 bestanden gevonden")
                return
            total_files = len(mp3_files)
            self.log_message(f"📁 Gevonden: {total_files} MP3 bestanden")
            self.progress_var.set(f"Start organisatie van {total_files} bestanden...")
            # Organiseer bestanden
            processed = 0
            artists_organized = {}
            moved_files = []  # Voor undo functionaliteit
            for file_path in mp3_files:
                # Controleer kill switch
                if self.stop_processing:
                    self.log_message("🛑 Verwerking gestopt door gebruiker")
                    break
                try:
                    # Detecteer artiest en titel
                    artist = self.detect_artist(file_path)
                    title = self.detect_title(file_path)
                    # Hernoem bestand als optie is ingeschakeld
                    if self.config.get('rename_files', False):
                        file_path = self.rename_file_to_artist_title(file_path, artist, title)
                        filename = os.path.basename(file_path)
                    else:
                        filename = os.path.basename(file_path)
                    # Bepaal doelmap (maar maak nog niet aan)
                    artist_folder = self.create_hierarchical_folders(dest_folder, artist, file_path)
                    # Verplaats bestand
                    dest_path = os.path.join(artist_folder, filename)
                    # Controleer duplicaten
                    if os.path.exists(dest_path):
                        if self.duplicate_check_var.get():
                            duplicate_remove = getattr(self, 'duplicate_remove_var', tk.BooleanVar(value=False)).get()
                            duplicate_move = getattr(self, 'duplicate_move_var', tk.BooleanVar(value=False)).get()
                            if duplicate_remove:
                                # Automatisch verwijderen
                                self.log_message(f"🗑️ Verwijdert duplicaat: {filename}")
                                continue
                            elif duplicate_move:
                                # Verplaatsen naar geselecteerde duplicaten output map
                                duplicate_output = getattr(self, 'duplicate_output_var', tk.StringVar(value="Duplicaten")).get()
                                if duplicate_output and duplicate_output.strip():
                                    # Gebruik geselecteerde map
                                    duplicates_folder = duplicate_output
                                    if not os.path.isabs(duplicates_folder):
                                        # Als het een relatieve pad is, maak het absoluut
                                        duplicates_folder = os.path.join(dest_folder, duplicates_folder)
                                else:
                                    # Fallback naar standaard duplicaten map
                                    duplicates_folder = os.path.join(dest_folder, "Duplicaten")
                                os.makedirs(duplicates_folder, exist_ok=True)
                                base, ext = os.path.splitext(filename)
                                counter = 1
                                new_filename = f"{base}_{counter}{ext}"
                                while os.path.exists(os.path.join(duplicates_folder, new_filename)):
                                    counter += 1
                                    new_filename = f"{base}_{counter}{ext}"
                                dest_path = os.path.join(duplicates_folder, new_filename)
                                self.log_message(f"📁 Verplaatst duplicaat: {filename} → {os.path.basename(duplicates_folder)}/{new_filename}")
                            else:
                                self.log_message(f"⚠️ Overschrijft bestaand bestand: {filename}")
                        else:
                            self.log_message(f"⚠️ Overschrijft bestaand bestand: {filename}")
                    # Maak doelmap pas nu aan
                    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                    # Bewaar originele pad voor undo
                    original_path = file_path
                    shutil.move(file_path, dest_path)
                    # Voeg toe aan undo lijst
                    moved_files.append({
                        'original_path': original_path,
                        'new_path': dest_path,
                        'artist': artist,
                        'filename': filename
                    })
                    # Update statistieken
                    if artist not in artists_organized:
                        artists_organized[artist] = 0
                    artists_organized[artist] += 1
                    processed += 1
                    # Update progress met percentage
                    progress = (processed / len(mp3_files)) * 100
                    percentage = int((processed / len(mp3_files)) * 100)
                    self.progress_bar['value'] = progress
                    self.progress_var.set(f"Verwerkt: {processed}/{len(mp3_files)} ({percentage}%)")
                    self.log_message(f"✅ {filename} → {artist}")
                except Exception as e:
                    self.log_message(f"❌ Fout bij {os.path.basename(file_path)}: {str(e)}")
            # Toon resultaten
            self.log_message("🎉 Organisatie voltooid!")
            self.log_message("📊 Resultaten:")
            for artist, count in artists_organized.items():
                self.log_message(f"  - {artist}: {count} nummers")
            # Voeg operatie toe aan undo stack
            if moved_files:
                self._add_undo_operation('organize', {
                    'moved_files': moved_files,
                    'total_files': len(moved_files),
                    'artists_organized': artists_organized
                })
            self.progress_var.set("Organisatie voltooid!")
        except Exception as e:
            self.log_message(f"❌ Fout tijdens organisatie: {str(e)}")
        finally:
            self.current_thread = None
            self.unblock_gui()
    

    
    def load_config(self):
        """Laadt configuratie"""
        try:
            if os.path.exists('mp3_organizer_config.json'):
                with open('mp3_organizer_config.json', 'r') as f:
                    saved_config = json.load(f)
                    self.config.update(saved_config)
                    
                    # Update huidige instellingen
                    self.current_language = self.config.get('language', 'Nederlands')
                    self.current_font_size = self.config.get('font_size', 'Normaal')
                    self.current_font_family = self.config.get('font_family', 'Arial')
                    
                    # Zorg ervoor dat Nederlands de standaard taal is
                    if self.current_language not in self.translations:
                        self.current_language = 'Nederlands'
                    
                    # Laad online database instellingen
                    if 'online_db_config' in saved_config:
                        self.online_db_config.update(saved_config['online_db_config'])
        except:
            pass
    
    def save_config(self):
        """Slaat configuratie op"""
        try:
            # Voeg online database configuratie toe aan config
            config_to_save = self.config.copy()
            config_to_save['online_db_config'] = self.online_db_config
            
            with open('mp3_organizer_config.json', 'w') as f:
                json.dump(config_to_save, f, indent=2)
        except:
            pass
    
    def run(self):
        """Start de applicatie"""
        self.root.mainloop()
        self.save_config()
    
    def start_rename_files(self):
        """Start het hernoemen van bestanden in een aparte thread"""
        source = self.source_var.get()
        
        if not source:
            messagebox.showerror(self.get_text('error'), self.get_text('select_folder_first'))
            return
        
        if not self.detected_library:
            messagebox.showerror(self.get_text('error'), self.get_text('no_library'))
            return
        
        # Check of er al een thread actief is
        if self.current_thread and self.current_thread.is_alive():
            messagebox.showwarning("Waarschuwing", "Er is al een operatie bezig. Wacht tot deze klaar is.")
            return
        
        # Vraag gebruiker om bevestiging
        result = messagebox.askyesno(
            "Hernoem Bestanden", 
            f"Weet je zeker dat je alle MP3 bestanden wilt hernoemen?\n\n"
            f"Dit zal bestanden hernoemen naar 'Artiest - Titel.mp3' formaat.\n"
            f"Bestanden worden NIET verplaatst, alleen hernoemd.\n\n"
            f"Huidige instellingen:\n"
            f"• Online databases: {'Aan' if self.config.get('online_database', True) else 'Uit'}\n"
            f"• Audio fingerprinting: {'Aan' if self.config.get('audio_fingerprinting', True) else 'Uit'}\n"
            f"• Cache: {'Aan' if self.config.get('cache_enabled', True) else 'Uit'}\n"
            f"• Titel opschonen: {'Aan' if self.config.get('clean_title_format', True) else 'Uit'}\n\n"
            f"Ja = Start hernoemen\n"
            f"Nee = Annuleren"
        )
        
        if not result:
            return
        
        # Reset kill switch
        self.stop_processing = False
        
        # Blokkeer GUI
        self.block_gui()
        
        # Start hernoem operatie in thread
        self.current_thread = threading.Thread(target=self.rename_files, args=(source,))
        self.current_thread.daemon = True
        self.current_thread.start()
    
    def rename_files(self, source_folder):
        """Hernoemt MP3 bestanden naar 'Artiest - Titel.mp3' formaat"""
        try:
            self.log_message("✏️ Start hernoemen van bestanden...")
            
            # Update configuratie voor deze sessie
            self.config.update({
                'clean_title_format': getattr(self, 'clean_title_format_var', tk.BooleanVar(value=True)).get()
            })
            
            # Controleer of hernoemen is ingeschakeld in instellingen
            if not self.config.get('rename_files', False):
                self.log_message("⚠️ Hernoemen is uitgeschakeld in de instellingen")
                messagebox.showwarning("Instellingen", "Hernoemen is uitgeschakeld in de instellingen.\nGa naar ⚙️ Instellingen → Organisatie Opties om hernoemen in te schakelen.")
                return
            
            # Vind alle MP3 bestanden
            mp3_files = []
            for root, dirs, files in os.walk(source_folder):
                for file in files:
                    if file.lower().endswith('.mp3'):
                        mp3_files.append(os.path.join(root, file))
            
            total_files = len(mp3_files)
            self.log_message(f"📁 Totaal gevonden: {total_files} MP3 bestanden")
            
            if total_files == 0:
                self.log_message("❌ Geen MP3 bestanden gevonden!")
                self.progress_var.set("Geen MP3 bestanden gevonden")
                return
            
            # Update voortgang
            self.progress_bar['value'] = 25
            self.progress_var.set(f"Start hernoemen van {total_files} bestanden... (25%)")
            
            # Statistieken
            renamed_count = 0
            skipped_count = 0
            error_count = 0
            renamed_files = []  # Voor undo functionaliteit
            
            # Hernoem elk bestand
            for i, file_path in enumerate(mp3_files):
                # Controleer kill switch
                if self.stop_processing:
                    self.log_message("🛑 Hernoemen gestopt door gebruiker")
                    break
                
                # Update voortgang met percentage
                progress = 25 + (i / len(mp3_files)) * 50
                percentage = int((i / len(mp3_files)) * 100)
                self.progress_bar['value'] = progress
                self.progress_var.set(f"Hernoemen: {i+1}/{total_files} ({percentage}%)")
                
                try:
                    filename = os.path.basename(file_path)
                    directory = os.path.dirname(file_path)
                    
                    # Detecteer artiest en titel (gebruik instellingen)
                    if self.config.get('online_database', True):
                        # Gebruik volledige detectie met online databases
                        artist = self.detect_artist(file_path)
                    else:
                        # Gebruik alleen snelle detectie
                        artist = self.detect_artist_fast(file_path)
                    
                    title = self.detect_title(file_path)
                    
                    # Skip als geen artiest gevonden
                    if artist in ['Unknown Artist', 'Onbekende Artiest', 'Unknown', 'Onbekend']:
                        self.log_message(f"⏭️ Overgeslagen: {filename} (geen artiest gevonden)")
                        skipped_count += 1
                        continue
                    
                    # Maak nieuwe bestandsnaam
                    new_filename = f"{artist} - {title}.mp3"
                    
                    # Controleer of bestandsnaam al correct is
                    if filename == new_filename:
                        self.log_message(f"✅ Al correct: {filename}")
                        skipped_count += 1
                        continue
                    
                    # Controleer of nieuwe bestandsnaam al bestaat
                    new_file_path = os.path.join(directory, new_filename)
                    if os.path.exists(new_file_path):
                        # Voeg nummer toe aan bestandsnaam
                        base_name = f"{artist} - {title}"
                        counter = 1
                        while os.path.exists(new_file_path):
                            new_filename = f"{base_name} ({counter}).mp3"
                            new_file_path = os.path.join(directory, new_filename)
                            counter += 1
                    
                    # Bewaar originele pad voor undo
                    original_path = file_path
                    
                    # Hernoem bestand
                    os.rename(file_path, new_file_path)
                    
                    # Voeg toe aan undo lijst
                    renamed_files.append({
                        'original_path': original_path,
                        'new_path': new_file_path,
                        'original_filename': filename,
                        'new_filename': new_filename
                    })
                    
                    self.log_message(f"✏️ Hernoemd: {filename} → {new_filename}")
                    renamed_count += 1
                    
                except Exception as e:
                    self.log_message(f"❌ Fout bij hernoemen {os.path.basename(file_path)}: {str(e)}")
                    error_count += 1
            
            # Update voortgang
            self.progress_bar['value'] = 100
            self.progress_var.set(f"Hernoemen voltooid: {total_files} bestanden verwerkt (100%)")
            
            # Toon resultaten
            self.log_message("📊 HERNOEM RESULTATEN:")
            self.log_message("=" * 50)
            self.log_message(f"📁 Totaal bestanden: {total_files}")
            self.log_message(f"✏️ Hernoemd: {renamed_count}")
            self.log_message(f"⏭️ Overgeslagen: {skipped_count}")
            self.log_message(f"❌ Fouten: {error_count}")
            self.log_message("=" * 50)
            
            # Toon popup met samenvatting
            summary_text = f"""HERNOEM RESULTATEN:

📁 Totaal bestanden: {total_files}
✏️ Hernoemd: {renamed_count}
⏭️ Overgeslagen: {skipped_count}
❌ Fouten: {error_count}

✅ Hernoemen voltooid!"""

            # Voeg operatie toe aan undo stack
            if renamed_files:
                self._add_undo_operation('rename', {
                    'renamed_files': renamed_files,
                    'total_files': len(renamed_files),
                    'renamed_count': renamed_count,
                    'skipped_count': skipped_count,
                    'error_count': error_count
                })
            
            messagebox.showinfo("Hernoem Resultaten", summary_text)
            
        except Exception as e:
            self.log_message(f"❌ Fout tijdens hernoemen: {str(e)}")
        finally:
            # Reset thread referentie
            self.current_thread = None
            
            # Vrijgeven GUI
            self.unblock_gui()

if __name__ == "__main__":
    app = MP3Organizer()
    app.run() 