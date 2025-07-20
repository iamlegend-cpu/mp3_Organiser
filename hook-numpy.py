# Custom hook voor numpy
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Verzamel alle numpy modules
numpy_modules = collect_submodules('numpy')
datas = collect_data_files('numpy')

# Voeg specifieke numpy modules toe
hiddenimports = [
    'numpy',
    'numpy.core',
    'numpy.core._multiarray_tests',
    'numpy.core._operand_flag_tests',
    'numpy.core._rational_tests',
    'numpy.core._struct_ufunc_tests',
    'numpy.core._umath_tests',
    'numpy.core.cversions',
    'numpy.core._dtype',
    'numpy.core._dtype_ctypes',
    'numpy.core._internal',
    'numpy.core._multiarray_umath',
    'numpy.core.arrayprint',
    'numpy.core.defchararray',
    'numpy.core.einsumfunc',
    'numpy.core.fromnumeric',
    'numpy.core.function_base',
    'numpy.core.getlimits',
    'numpy.core.numerictypes',
    'numpy.core.overrides',
    'numpy.core.records',
    'numpy.core.shape_base',
    'numpy.core.umath',
    'numpy.core._add_newdocs',
    'numpy.core.__init__',
    'numpy.__init__',
]

# Voeg alle verzamelde modules toe
hiddenimports.extend(numpy_modules) 