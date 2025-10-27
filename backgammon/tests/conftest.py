<<<<<<< HEAD
import sys
import os

# Agregar ra?z al path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# Importar backgammon para que el m?dulo est? disponible
import backgammon
=======
# Adaptador de imports para que funcionen ambos estilos:
# - from backgammon.core import ...
# - from backgammon.backgammon.core import ...
import sys, os, importlib

# Asegurá que la raíz del repo esté en sys.path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# Si existe el paquete "doble" (backgammon/backgammon), alias para el "simple"
try:
    # Importa el paquete interno
    importlib.import_module("backgammon.backgammon")
    # Alias: backgammon.core -> backgammon.backgammon.core
    sys.modules.setdefault(
        "backgammon.core",
        importlib.import_module("backgammon.backgammon.core")
    )
except Exception:
    # Si no existe el doble paquete, no hacemos nada.
    pass
>>>>>>> origin/main
