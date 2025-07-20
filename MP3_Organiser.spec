# -*- mode: python ; coding: utf-8 -*-

# MP3 Organiser 0.1a - PyInstaller Spec File
# Professionele verpakking zonder console vensters

import os
import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Basis configuratie
block_cipher = None

# Verzamel alle benodigde modules en data
datas = []
binaries = []



# Voeg applicatie data toe
datas += [
    ('LICENSE', '.'),
    ('README.md', '.'),
]

# Verzamel mutagen data
try:
    mutagen_datas = collect_data_files('mutagen')
    datas.extend(mutagen_datas)
except:
    pass

# Verzamel librosa data (als beschikbaar)
try:
    librosa_datas = collect_data_files('librosa')
    datas.extend(librosa_datas)
except:
    pass

# Verzamel scipy data (als beschikbaar)
try:
    scipy_datas = collect_data_files('scipy')
    datas.extend(scipy_datas)
except:
    pass





# Verzamel numpy data
try:
    numpy_datas = collect_data_files('numpy')
    datas.extend(numpy_datas)
except:
    pass

# Verzamel alle submodules
hiddenimports = []

# Core modules
hiddenimports += [
    'tkinter',
    'tkinter.filedialog',
    'tkinter.messagebox',
    'tkinter.ttk',
    'tkinter.simpledialog',
    'threading',
    'multiprocessing',
    'multiprocessing.pool',
    'multiprocessing.managers',
    'multiprocessing.synchronize',
    'multiprocessing.heap',
    'multiprocessing.queues',
    'multiprocessing.connection',
    'multiprocessing.reduction',
    'pickle',
    'pickletools',
    'unittest',
    'unittest.mock',
    'unittest.case',
    'unittest.suite',
    'unittest.loader',
    'unittest.runner',
    'unittest.result',
    'unittest.signals',
    'unittest.main',
    'json',
    'os',
    'shutil',
    'time',
    'datetime',
    'hashlib',
    'sqlite3',
    'urllib.parse',
    'tempfile',
    'wave',
    'struct',
]

# Mutagen modules
try:
    mutagen_modules = collect_submodules('mutagen')
    hiddenimports.extend(mutagen_modules)
except:
    pass

# Audio processing modules (optioneel)
try:
    librosa_modules = collect_submodules('librosa')
    hiddenimports.extend(librosa_modules)
except:
    pass

try:
    scipy_modules = collect_submodules('scipy')
    hiddenimports.extend(scipy_modules)
except:
    pass

# Voeg specifieke scipy modules toe
hiddenimports += [
    'scipy.sparse.csgraph._shortest_path',
    'scipy.sparse.csgraph._validation',
    'scipy.sparse.csgraph._tools',
    'scipy.sparse.csgraph._min_spanning_tree',
    'scipy.sparse.csgraph._connected_components',
    'scipy.sparse.csgraph._flow',
    'scipy.sparse.csgraph._reordering',
    'scipy.sparse.csgraph._traversal',
    'scipy.sparse.csgraph._laplacian',
    'scipy.sparse.csgraph._spectral',
    'scipy.sparse.csgraph._matching',
    'scipy.sparse.csgraph._validation',
    'scipy.sparse.csgraph._tools',
    'scipy.sparse.csgraph._shortest_path',
    'scipy.sparse.csgraph._min_spanning_tree',
    'scipy.sparse.csgraph._connected_components',
    'scipy.sparse.csgraph._flow',
    'scipy.sparse.csgraph._reordering',
    'scipy.sparse.csgraph._traversal',
    'scipy.sparse.csgraph._laplacian',
    'scipy.sparse.csgraph._spectral',
    'scipy.sparse.csgraph._matching',
]





try:
    numpy_modules = collect_submodules('numpy')
    hiddenimports.extend(numpy_modules)
except:
    pass

# Requests modules
try:
    requests_modules = collect_submodules('requests')
    hiddenimports.extend(requests_modules)
except:
    pass

# Exclude onnodige modules om grootte te verminderen
excludes = [
    'matplotlib',
    'PIL',
    'cv2',
    'pandas',
    'seaborn',
    'plotly',
    'bokeh',
    'jupyter',
    'IPython',
    'notebook',
    'sphinx',
    'docutils',
    'pytest',
    'doctest',
    'pdb',
    'profile',
    'pstats',
    'cProfile',
    'trace',
    'pickletools',
    'shelve',
    'dbm',
    'sqlite3.test',
    'test',
    'tests',
    'testing',
]

# Hoofdconfiguratie
a = Analysis(
    ['MP3_Organiser0.1a.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=['.'],
    hooksconfig={},
    runtime_hooks=['runtime_hook.py'],
    excludes=excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Verwijder onnodige bestanden
a.binaries = [x for x in a.binaries if not any(exclude in x[0].lower() for exclude in [
    'test', 'tests', 'testing', 'example', 'demo', 'sample'
])]

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Executable configuratie
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='MP3_Organiser',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Geen console venster
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if os.path.exists('icon.ico') else None,
)

# Directory configuratie (--onedir)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='MP3_Organiser',
)

# Extra opties voor professionele uitstraling
# Voeg metadata toe aan executable
exe.version_info = {
    'FileVersion': (0, 1, 0, 0),
    'ProductVersion': (0, 1, 0, 0),
    'CompanyName': 'MP3 Organiser',
    'FileDescription': 'MP3 Organiser 0.1a - Slimme Muziek Organisatie',
    'ProductName': 'MP3 Organiser',
    'LegalCopyright': 'Copyright © 2024',
    'OriginalFilename': 'MP3_Organiser.exe',
}

# Optimalisaties voor kleinere bestandsgrootte
# Verwijder debug informatie
exe.strip = True

# Compressie instellingen
exe.upx = True
exe.upx_exclude = []

# Console instellingen
exe.console = False  # Geen console venster
exe.disable_windowed_traceback = False

# Icon instellingen (als beschikbaar)
if os.path.exists('icon.ico'):
    exe.icon = 'icon.ico' 