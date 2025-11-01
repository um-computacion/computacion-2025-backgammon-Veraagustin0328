import sys
import os

# Agregar raíz al path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# Importar backgammon para que el módulo esté disponible
import backgammon

