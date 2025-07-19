# 🎵 MP3 Organiser 0.1a - Slimme Muziek Organisatie
# 📦 Imports
import os
import shutil
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
import json
import time
from datetime import datetime

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
            'font_family': 'Arial'
        }
        
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
                'library_detected_log': '📁 Muziek bibliotheek gedetecteerd: {path}'
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
                'library_detected_log': '📁 Music library detected: {path}'
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
        
        # Huidige taal en font instellingen
        self.current_language = self.config.get('language', 'Nederlands')
        self.current_font_size = self.config.get('font_size', 'Normaal')
        self.current_font_family = self.config.get('font_family', 'Arial')
        
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
        
        self.setup_ui()
        self.load_config()
    
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
        
        self.organize_btn = tk.Button(self.button_frame, text="🎵 Start Organisatie", 
                                     command=self.start_organization, bg='#4CAF50', fg='white')
        self.organize_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        scan_btn = tk.Button(self.button_frame, text="🔍 Scan Bestanden", 
                           command=self.scan_files, bg='#2196F3', fg='white')
        scan_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        duplicate_btn = tk.Button(self.button_frame, text="🔍 Zoek Duplicaten", 
                                command=self.find_duplicates, bg='#FF9800', fg='white')
        duplicate_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        clear_btn = tk.Button(self.button_frame, text="🗑️ Log Wissen", 
                            command=self.clear_log, bg='#f44336', fg='white')
        clear_btn.pack(side=tk.LEFT)
    
    def select_source_folder(self):
        """Selecteert map om te organiseren en detecteert automatisch bibliotheek"""
        folder = filedialog.askdirectory(title="Selecteer map met MP3 bestanden om te organiseren")
        if folder:
            self.source_var.set(folder)
            self.log_message(f"Map geselecteerd: {folder}")
            
            # Automatisch bibliotheek detecteren
            self.detect_music_library()
            self.log_message(f"📁 Muziek bibliotheek gedetecteerd: {self.detected_library}")
    
    def create_menu(self):
        """Maakt de menubalk aan"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Instellingen menu
        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="⚙️ Instellingen", menu=settings_menu)
        settings_menu.add_command(label="🔧 Instellingen", command=self.show_settings)
        
        # Thema menu
        theme_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="🎨 Thema", menu=theme_menu)
        theme_menu.add_command(label="🌞 Light Theme", command=lambda: self.change_theme("light"))
        theme_menu.add_command(label="🌙 Dark Theme", command=lambda: self.change_theme("dark"))
        theme_menu.add_command(label="🌊 Blue Theme", command=lambda: self.change_theme("blue"))
        theme_menu.add_command(label="🌿 Green Theme", command=lambda: self.change_theme("green"))
        theme_menu.add_command(label="🔥 Orange Theme", command=lambda: self.change_theme("orange"))
        
        # Debug menu
        debug_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="🐛 Debug", menu=debug_menu)
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
        
        # Hoofdtitel
        title_label = tk.Label(settings_window, text="🔧 MP3 Organiser Instellingen", 
                              font=('Arial', 16, 'bold'), bg=self.themes[self.current_theme]["bg"], 
                              fg=self.themes[self.current_theme]["fg"])
        title_label.pack(pady=10)
        
        # Hoofdframe voor tabs
        main_frame = tk.Frame(settings_window, bg=self.themes[self.current_theme]["bg"])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Linker frame voor tab knoppen
        left_frame = tk.Frame(main_frame, bg=self.themes[self.current_theme]["bg"], width=150)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_frame.pack_propagate(False)
        
        # Rechter frame voor content
        right_frame = tk.Frame(main_frame, bg=self.themes[self.current_theme]["bg"])
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Tab knoppen
        org_btn = tk.Button(left_frame, text="📁 Organisatie", 
                           command=lambda: self.show_org_settings(right_frame), 
                           bg='#4CAF50', fg='white', width=15, height=2)
        org_btn.pack(pady=5)
        
        log_btn = tk.Button(left_frame, text="📝 Log", 
                           command=lambda: self.show_log_settings(right_frame), 
                           bg='#2196F3', fg='white', width=15, height=2)
        log_btn.pack(pady=5)
        
        lang_btn = tk.Button(left_frame, text="🌐 Languages", 
                            command=lambda: self.show_language_settings(right_frame), 
                            bg='#FF9800', fg='white', width=15, height=2)
        lang_btn.pack(pady=5)
        
        # Knoppen frame
        button_frame = tk.Frame(settings_window, bg=self.themes[self.current_theme]["bg"])
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        save_btn = tk.Button(button_frame, text="💾 Opslaan", 
                           command=lambda: self.save_settings(settings_window), 
                           bg='#4CAF50', fg='white')
        save_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        cancel_btn = tk.Button(button_frame, text="❌ Annuleren", 
                             command=settings_window.destroy, 
                             bg='#f44336', fg='white')
        cancel_btn.pack(side=tk.LEFT)
        
        # Toon standaard organisatie instellingen
        self.show_org_settings(right_frame)
        
        # Update thema voor het instellingen venster
        self.update_settings_window_theme(settings_window)
    
    def show_org_settings(self, parent_frame):
        """Toont organisatie instellingen"""
        # Wis bestaande content
        for widget in parent_frame.winfo_children():
            widget.destroy()
        
        # Organisatie opties frame
        org_frame = tk.LabelFrame(parent_frame, text="📁 Organisatie Opties", 
                                 bg=self.themes[self.current_theme]["bg"], fg=self.themes[self.current_theme]["fg"])
        org_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Hiërarchische mappen
        hierarchical_frame = tk.Frame(org_frame, bg=self.themes[self.current_theme]["bg"])
        hierarchical_frame.pack(fill=tk.X, padx=10, pady=5)
        
        hierarchical_cb = tk.Checkbutton(hierarchical_frame, text="Hiërarchische mappen (A/B/C/etc.)", 
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
        
        # Duplicaten behandeling
        duplicate_action_frame = tk.Frame(org_frame, bg=self.themes[self.current_theme]["bg"])
        duplicate_action_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(duplicate_action_frame, text="Duplicaten behandeling:", 
                bg=self.themes[self.current_theme]["bg"], fg=self.themes[self.current_theme]["fg"]).pack(side=tk.LEFT)
        
        self.duplicate_action_var = tk.StringVar(value="ask")
        duplicate_action_combo = ttk.Combobox(duplicate_action_frame, textvariable=self.duplicate_action_var, 
                                            values=["ask", "skip", "overwrite", "rename"], 
                                            state="readonly", width=15)
        duplicate_action_combo.pack(side=tk.RIGHT)
        
        # Duplicaten behandeling uitleg
        duplicate_explanation_frame = tk.Frame(org_frame, bg=self.themes[self.current_theme]["bg"])
        duplicate_explanation_frame.pack(fill=tk.X, padx=10, pady=2)
        
        explanation_text = "ask = Vraag gebruiker, skip = Overslaan, overwrite = Overschrijven, rename = Hernoemen"
        explanation_label = tk.Label(duplicate_explanation_frame, text=explanation_text, 
                                   bg=self.themes[self.current_theme]["bg"], fg='#666666', 
                                   font=('Arial', 8), wraplength=400)
        explanation_label.pack(anchor=tk.W)
        
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
        lang_frame = tk.LabelFrame(parent_frame, text="🌐 Taal & Lettergrootte", 
                                  bg=self.themes[self.current_theme]["bg"], fg=self.themes[self.current_theme]["fg"])
        lang_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Taal selectie
        language_frame = tk.Frame(lang_frame, bg=self.themes[self.current_theme]["bg"])
        language_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(language_frame, text="Programma taal:", 
                bg=self.themes[self.current_theme]["bg"], fg=self.themes[self.current_theme]["fg"]).pack(side=tk.LEFT)
        
        self.language_var = tk.StringVar(value="Nederlands")
        language_combo = ttk.Combobox(language_frame, textvariable=self.language_var, 
                                     values=["Nederlands", "English", "Deutsch", "Français", "Español"], 
                                     state="readonly", width=15)
        language_combo.pack(side=tk.RIGHT)
        
        # Lettergrootte selectie
        font_size_frame = tk.Frame(lang_frame, bg=self.themes[self.current_theme]["bg"])
        font_size_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(font_size_frame, text="Lettergrootte:", 
                bg=self.themes[self.current_theme]["bg"], fg=self.themes[self.current_theme]["fg"]).pack(side=tk.LEFT)
        
        self.font_size_var = tk.StringVar(value="Normaal")
        font_size_combo = ttk.Combobox(font_size_frame, textvariable=self.font_size_var, 
                                      values=["Klein", "Normaal", "Groot", "Extra Groot"], 
                                      state="readonly", width=15)
        font_size_combo.pack(side=tk.RIGHT)
        
        # Font familie selectie
        font_family_frame = tk.Frame(lang_frame, bg=self.themes[self.current_theme]["bg"])
        font_family_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(font_family_frame, text="Lettertype:", 
                bg=self.themes[self.current_theme]["bg"], fg=self.themes[self.current_theme]["fg"]).pack(side=tk.LEFT)
        
        self.font_family_var = tk.StringVar(value="Arial")
        font_family_combo = ttk.Combobox(font_family_frame, textvariable=self.font_family_var, 
                                        values=["Arial", "Helvetica", "Times New Roman", "Verdana", "Tahoma"], 
                                        state="readonly", width=15)
        font_family_combo.pack(side=tk.RIGHT)
        
        # Preview frame
        preview_frame = tk.LabelFrame(lang_frame, text="👁️ Voorbeeld", 
                                     bg=self.themes[self.current_theme]["bg"], fg=self.themes[self.current_theme]["fg"])
        preview_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Preview tekst
        preview_text = "Dit is een voorbeeld van hoe de tekst eruit zal zien met de gekozen instellingen."
        self.preview_label = tk.Label(preview_frame, text=preview_text, 
                                     bg=self.themes[self.current_theme]["bg"], fg=self.themes[self.current_theme]["fg"],
                                     font=('Arial', 10))
        self.preview_label.pack(pady=10)
        
        # Bind events voor live preview
        language_combo.bind('<<ComboboxSelected>>', self.update_preview)
        font_size_combo.bind('<<ComboboxSelected>>', self.update_preview)
        font_family_combo.bind('<<ComboboxSelected>>', self.update_preview)
    
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
                    elif "Start Organisatie" in current_text:
                        child.configure(text=self.get_text('start_org'))
                    elif "Scan Bestanden" in current_text:
                        child.configure(text=self.get_text('scan_files'))
                    elif "Zoek Duplicaten" in current_text:
                        child.configure(text=self.get_text('find_duplicates'))
                    elif "Log Wissen" in current_text:
                        child.configure(text=self.get_text('clear_log'))
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
        self.config.update({
            'hierarchical': self.hierarchical_var.get(),
            'include_albums': self.albums_var.get(),
            'include_years': self.years_var.get(),
            'duplicate_check': self.duplicate_check_var.get(),
            'duplicate_action': getattr(self, 'duplicate_action_var', tk.StringVar(value="ask")).get(),
            'log_size': getattr(self, 'log_size_var', tk.StringVar(value="800x600")).get(),
            'auto_scroll': getattr(self, 'auto_scroll_var', tk.BooleanVar(value=True)).get(),
            'timestamp': getattr(self, 'timestamp_var', tk.BooleanVar(value=True)).get(),
            'log_level': getattr(self, 'log_level_var', tk.StringVar(value="Info")).get(),
            'save_log': getattr(self, 'save_log_var', tk.BooleanVar(value=False)).get(),
            'language': getattr(self, 'language_var', tk.StringVar(value="Nederlands")).get(),
            'font_size': getattr(self, 'font_size_var', tk.StringVar(value="Normaal")).get(),
            'font_family': getattr(self, 'font_family_var', tk.StringVar(value="Arial")).get()
        })
        
        # Pas taal en font wijzigingen toe
        new_language = getattr(self, 'language_var', tk.StringVar(value="Nederlands")).get()
        new_font_size = getattr(self, 'font_size_var', tk.StringVar(value="Normaal")).get()
        new_font_family = getattr(self, 'font_family_var', tk.StringVar(value="Arial")).get()
        
        if new_language != self.current_language:
            self.change_language(new_language)
        
        if new_font_size != self.current_font_size or new_font_family != self.current_font_family:
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
            self.log_window.title("📝 MP3 Organiser - Log")
            self.log_window.geometry("800x600")
            self.log_window.configure(bg=self.themes[self.current_theme]["bg"])
            
            # Log frame
            log_frame = tk.LabelFrame(self.log_window, text="📝 Log", bg=self.themes[self.current_theme]["bg"])
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
            
            clear_btn = tk.Button(button_frame, text="🗑️ Log Wissen", 
                                command=self.clear_log, bg='#f44336', fg='white')
            clear_btn.pack(side=tk.LEFT)
            
            close_btn = tk.Button(button_frame, text="❌ Sluiten", 
                                command=self.close_log_window, bg='#666666', fg='white')
            close_btn.pack(side=tk.RIGHT)
            
            # Update thema voor het nieuwe venster
            self.update_log_window_theme()
            
            # Reset auto-scroll voor nieuw venster
            self.auto_scroll_enabled = True
            
            self.log_message("📝 Log venster geopend")
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
            
            "duplicates": "🔍 Controleert op duplicaten:\n📁 Bestandsnaam: song.mp3 → song_1.mp3\n🎵 ID3 Tags: 'Michael Jackson - Thriller' → 'Thriller_1.mp3'\n💾 Behoudt origineel, hernoemt duplicaten"
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
    
    def clear_log(self):
        """Wist het log"""
        if self.log_text and self.log_window and self.log_window.winfo_exists():
            self.log_text.delete(1.0, tk.END)
            self.log_message("🗑️ Log gewist")
    
    def scan_files(self):
        """Scant bestanden in bron map en toont waar ze naartoe gaan"""
        source = self.source_var.get()
        
        if not source:
            messagebox.showerror("Fout", "Selecteer eerst een map om te organiseren!")
            return
        
        if not self.detected_library:
            messagebox.showerror("Fout", "Geen muziek bibliotheek gevonden!")
            return
        
        self.log_message("🔍 Scannen van MP3 bestanden...")
        
        mp3_files = []
        for root, dirs, files in os.walk(source):
            for file in files:
                if file.lower().endswith('.mp3'):
                    mp3_files.append(os.path.join(root, file))
        
        self.log_message(f"Gevonden: {len(mp3_files)} MP3 bestanden")
        
        # Analyseer bestanden en toon waar ze naartoe gaan
        artists_found = {}
        for file_path in mp3_files[:10]:  # Eerste 10 voor preview
            artist = self.detect_artist(file_path)
            if artist not in artists_found:
                artists_found[artist] = 0
            artists_found[artist] += 1
            
            # Toon waar het bestand naartoe gaat
            dest_folder = self.create_hierarchical_folders(self.detected_library, artist, file_path)
            filename = os.path.basename(file_path)
            self.log_message(f"📁 {filename} → {dest_folder}")
        
        self.log_message("📊 Artiesten gevonden:")
        for artist, count in artists_found.items():
            self.log_message(f"  - {artist}: {count} nummers")
    
    def find_duplicates(self):
        """Zoekt duplicaten in de bron map en toont overzicht"""
        source = self.source_var.get()
        
        if not source:
            messagebox.showerror("Fout", "Selecteer eerst een map om te organiseren!")
            return
        
        self.log_message("🔍 Zoeken naar duplicaten...")
        
        # Vind alle MP3 bestanden
        mp3_files = []
        for root, dirs, files in os.walk(source):
            for file in files:
                if file.lower().endswith('.mp3'):
                    mp3_files.append(os.path.join(root, file))
        
        if not mp3_files:
            self.log_message("❌ Geen MP3 bestanden gevonden!")
            return
        
        # Analyseer duplicaten
        file_hashes = {}
        id3_duplicates = {}
        duplicates = {}
        
        for file_path in mp3_files:
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
                    if audio.tags:
                        artist = audio.tags.get('TPE1', ['Unknown'])[0]
                        title = audio.tags.get('TIT2', ['Unknown'])[0]
                        id3_key = f"{artist} - {title}".lower()
                        
                        if id3_key in id3_duplicates:
                            if id3_key not in duplicates:
                                duplicates[id3_key] = []
                                duplicates[id3_key].append(id3_duplicates[id3_key])
                            duplicates[id3_key].append(file_path)
                        else:
                            id3_duplicates[id3_key] = file_path
                except:
                    # Als ID3 tags niet beschikbaar zijn, skip
                    pass
                    
            except Exception as e:
                self.log_message(f"❌ Fout bij {os.path.basename(file_path)}: {str(e)}")
        
        # Toon resultaten
        if duplicates:
            self.log_message(f"🔍 {len(duplicates)} duplicaten gevonden:")
            for filename, file_list in duplicates.items():
                self.log_message(f"📁 {filename}:")
                for file_path in file_list:
                    self.log_message(f"  - {file_path}")
            
            # Vraag gebruiker wat te doen
            self.handle_duplicates(duplicates)
        else:
            self.log_message("✅ Geen duplicaten gevonden!")
    
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
        """Detecteert artiest van MP3 bestand"""
        try:
            # Probeer ID3 tags
            audio = MP3(file_path, ID3=ID3)
            if audio.tags and 'TPE1' in audio.tags:
                artist = audio.tags['TPE1'][0]
                return self.normalize_artist_name(artist)
        except:
            pass
        
        # Analyseer bestandsnaam
        filename = os.path.basename(file_path).lower()
        filename = filename.replace('.mp3', '').replace('_', ' ').replace('-', ' ')
        
        # Zoek naar bekende artiesten
        for artist, songs in self.artist_patterns.items():
            for song in songs:
                if song in filename:
                    return self.normalize_artist_name(artist)
        
        # Zoek naar artiest naam in bestandsnaam
        for artist in self.artist_patterns.keys():
            if artist in filename:
                return self.normalize_artist_name(artist)
        
        return "Unknown Artist"
    
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
            'pink floyd': 'Pink Floyd'
        }
        
        if artist.lower() in artist_mappings:
            return artist_mappings[artist.lower()]
        
        return artist.title()
    
    def create_hierarchical_folders(self, base_folder, artist, filename):
        """Maakt hiërarchische mappen aan of vindt bestaande"""
        if self.hierarchical_var.get():
            # Hiërarchische structuur: Letter/Artiest/
            first_letter = artist[0].upper()
            letter_folder = os.path.join(base_folder, first_letter)
            
            # Controleer of hiërarchische structuur al bestaat
            if os.path.exists(letter_folder):
                # Zoek bestaande artiest map
                for existing_artist in os.listdir(letter_folder):
                    if existing_artist.lower() == artist.lower():
                        artist_folder = os.path.join(letter_folder, existing_artist)
                        break
                else:
                    # Maak nieuwe artiest map
                    artist_folder = os.path.join(letter_folder, artist)
                    os.makedirs(artist_folder, exist_ok=True)
            else:
                # Maak nieuwe hiërarchische structuur
                os.makedirs(letter_folder, exist_ok=True)
                artist_folder = os.path.join(letter_folder, artist)
                os.makedirs(artist_folder, exist_ok=True)
        else:
            # Directe structuur: Artiest/
            # Zoek bestaande artiest map
            for existing_artist in os.listdir(base_folder):
                if existing_artist.lower() == artist.lower():
                    artist_folder = os.path.join(base_folder, existing_artist)
                    break
            else:
                # Maak nieuwe artiest map
                artist_folder = os.path.join(base_folder, artist)
                os.makedirs(artist_folder, exist_ok=True)
        
        # Album organisatie
        if self.albums_var.get():
            try:
                audio = MP3(filename, ID3=ID3)
                if audio.tags and 'TALB' in audio.tags:
                    album_name = audio.tags['TALB'][0]
                    album_folder = os.path.join(artist_folder, album_name)
                    os.makedirs(album_folder, exist_ok=True)
                    artist_folder = album_folder
            except:
                pass
        
        # Jaar organisatie
        if self.years_var.get():
            try:
                audio = MP3(filename, ID3=ID3)
                if audio.tags and 'TYER' in audio.tags:
                    year = audio.tags['TYER'][0]
                    year_folder = os.path.join(artist_folder, year)
                    os.makedirs(year_folder, exist_ok=True)
                    artist_folder = year_folder
            except:
                pass
        
        return artist_folder
    
    def start_organization(self):
        """Start de organisatie in een aparte thread"""
        source = self.source_var.get()
        
        if not source:
            messagebox.showerror("Fout", "Selecteer eerst een map om te organiseren!")
            return
        
        if not self.detected_library:
            messagebox.showerror("Fout", "Geen muziek bibliotheek gevonden!")
            return
        
        # Update configuratie
        self.config.update({
            'hierarchical': self.hierarchical_var.get(),
            'include_albums': self.albums_var.get(),
            'include_years': self.years_var.get()
        })
        
        # Start organisatie in thread
        self.organize_btn.config(state=tk.DISABLED)
        thread = threading.Thread(target=self.organize_files, args=(source, self.detected_library))
        thread.daemon = True
        thread.start()
    
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
                return
            
            self.log_message(f"📁 Gevonden: {len(mp3_files)} MP3 bestanden")
            
            # Organiseer bestanden
            processed = 0
            artists_organized = {}
            
            for file_path in mp3_files:
                try:
                    # Detecteer artiest
                    artist = self.detect_artist(file_path)
                    
                    # Maak mappen
                    artist_folder = self.create_hierarchical_folders(dest_folder, artist, file_path)
                    
                    # Verplaats bestand
                    filename = os.path.basename(file_path)
                    dest_path = os.path.join(artist_folder, filename)
                    
                                        # Controleer duplicaten
                    if os.path.exists(dest_path):
                        if self.duplicate_check_var.get():
                            duplicate_action = getattr(self, 'duplicate_action_var', tk.StringVar(value="ask")).get()
                            
                            if duplicate_action == "ask":
                                # Vraag gebruiker wat te doen
                                result = messagebox.askyesnocancel(
                                    "Duplicaat Gevonden",
                                    f"Bestand {filename} bestaat al in {artist}.\n\n"
                                    "Ja = Overschrijven\n"
                                    "Nee = Overslaan\n"
                                    "Annuleren = Stoppen"
                                )
                                
                                if result is True:  # Overschrijven
                                    self.log_message(f"⚠️ Overschrijft bestaand bestand: {filename}")
                                elif result is False:  # Overslaan
                                    self.log_message(f"⏭️ Overslaat duplicaat: {filename}")
                                    continue
                                else:  # Annuleren
                                    self.log_message("❌ Organisatie gestopt door gebruiker")
                                    return
                                    
                            elif duplicate_action == "skip":
                                # Overslaan
                                self.log_message(f"⏭️ Overslaat duplicaat: {filename}")
                                continue
                                
                            elif duplicate_action == "overwrite":
                                # Overschrijven
                                self.log_message(f"⚠️ Overschrijft bestaand bestand: {filename}")
                                
                            elif duplicate_action == "rename":
                                # Hernoemen
                                base, ext = os.path.splitext(filename)
                                counter = 1
                                while os.path.exists(dest_path):
                                    new_filename = f"{base}_{counter}{ext}"
                                    dest_path = os.path.join(artist_folder, new_filename)
                                    counter += 1
                                self.log_message(f"🔄 Hernoemt duplicaat: {filename} → {os.path.basename(dest_path)}")
                        else:
                            # Overschrijf bestaande bestanden
                            self.log_message(f"⚠️ Overschrijft bestaand bestand: {filename}")
                    
                    shutil.move(file_path, dest_path)
                    
                    # Update statistieken
                    if artist not in artists_organized:
                        artists_organized[artist] = 0
                    artists_organized[artist] += 1
                    processed += 1
                    
                    # Update progress
                    progress = (processed / len(mp3_files)) * 100
                    self.progress_bar['value'] = progress
                    self.progress_var.set(f"Verwerkt: {processed}/{len(mp3_files)}")
                    
                    self.log_message(f"✅ {filename} → {artist}")
                    
                except Exception as e:
                    self.log_message(f"❌ Fout bij {os.path.basename(file_path)}: {str(e)}")
            
            # Toon resultaten
            self.log_message("🎉 Organisatie voltooid!")
            self.log_message("📊 Resultaten:")
            for artist, count in artists_organized.items():
                self.log_message(f"  - {artist}: {count} nummers")
            
            self.progress_var.set("Organisatie voltooid!")
            
        except Exception as e:
            self.log_message(f"❌ Fout tijdens organisatie: {str(e)}")
        finally:
            self.organize_btn.config(state=tk.NORMAL)
    

    
    def load_config(self):
        """Laadt configuratie"""
        try:
            if os.path.exists('mp3_organizer_config.json'):
                with open('mp3_organizer_config.json', 'r') as f:
                    saved_config = json.load(f)
                    self.config.update(saved_config)
        except:
            pass
    
    def save_config(self):
        """Slaat configuratie op"""
        try:
            with open('mp3_organizer_config.json', 'w') as f:
                json.dump(self.config, f, indent=2)
        except:
            pass
    
    def run(self):
        """Start de applicatie"""
        self.root.mainloop()
        self.save_config()

if __name__ == "__main__":
    app = MP3Organizer()
    app.run() 