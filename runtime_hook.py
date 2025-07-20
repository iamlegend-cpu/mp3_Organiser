# Runtime hook voor MP3 Organiser
# Lost multiprocessing en pickle problemen op

import sys
import os

# Zorg ervoor dat pickle beschikbaar is
try:
    import pickle
except ImportError:
    # Als pickle niet beschikbaar is, probeer het handmatig te laden
    import importlib.util
    spec = importlib.util.find_spec('pickle')
    if spec is not None:
        pickle = importlib.util.module_from_spec(spec)
        sys.modules['pickle'] = pickle
        spec.loader.exec_module(pickle)

# Fix voor multiprocessing in PyInstaller
def _fix_multiprocessing():
    """Fix multiprocessing voor PyInstaller"""
    try:
        import multiprocessing
        import multiprocessing.pool
        import multiprocessing.managers
        import multiprocessing.synchronize
        import multiprocessing.heap
        import multiprocessing.queues
        import multiprocessing.connection
        import multiprocessing.reduction
        
        # Zorg ervoor dat multiprocessing correct werkt
        if not hasattr(multiprocessing, '_fixup_main'):
            multiprocessing._fixup_main = lambda: None
            
    except ImportError as e:
        print(f"Warning: Multiprocessing import error: {e}")

# Fix voor pickle in PyInstaller
def _fix_pickle():
    """Fix pickle voor PyInstaller"""
    try:
        import pickle
        import pickletools
        
        # Zorg ervoor dat pickle correct werkt
        if not hasattr(pickle, 'loads'):
            raise ImportError("Pickle not properly loaded")
            
    except ImportError as e:
        print(f"Warning: Pickle import error: {e}")

# Fix voor unittest in PyInstaller
def _fix_unittest():
    """Fix unittest voor PyInstaller"""
    try:
        import unittest
        import unittest.mock
        import unittest.case
        import unittest.suite
        import unittest.loader
        import unittest.runner
        import unittest.result
        import unittest.signals
        import unittest.main
        
        # Zorg ervoor dat unittest correct werkt
        if not hasattr(unittest, 'TestCase'):
            raise ImportError("Unittest not properly loaded")
            
    except ImportError as e:
        print(f"Warning: Unittest import error: {e}")

# Fix voor scipy in PyInstaller
def _fix_scipy():
    """Fix scipy voor PyInstaller"""
    try:
        import scipy
        import scipy.sparse
        import scipy.sparse.csgraph
        
        # Zorg ervoor dat scipy correct werkt
        if not hasattr(scipy, '__version__'):
            raise ImportError("Scipy not properly loaded")
            
    except ImportError as e:
        print(f"Warning: Scipy import error: {e}")

# Fix voor numpy in PyInstaller
def _fix_numpy():
    """Fix numpy voor PyInstaller"""
    try:
        import numpy
        import numpy.core
        import numpy.__init__
        import numpy.core.__init__
        
        # Zorg ervoor dat numpy correct werkt
        if not hasattr(numpy, '__version__'):
            raise ImportError("Numpy not properly loaded")
            
    except ImportError as e:
        print(f"Warning: Numpy import error: {e}")

# Voer fixes uit bij import
_fix_multiprocessing()
_fix_pickle()
_fix_unittest()
_fix_scipy()
_fix_numpy()

# Zorg ervoor dat alle benodigde modules beschikbaar zijn
required_modules = [
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
    'multiprocessing',
    'multiprocessing.pool',
    'multiprocessing.managers',
    'multiprocessing.synchronize',
    'multiprocessing.heap',
    'multiprocessing.queues',
    'multiprocessing.connection',
    'multiprocessing.reduction',
    'numpy.__init__',
    'numpy.core.__init__',

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
]

for module_name in required_modules:
    try:
        __import__(module_name)
    except ImportError:
        print(f"Warning: Could not import {module_name}")

print("Runtime hook loaded successfully") 