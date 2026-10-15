"""csv-perfil: perfilado rápido de archivos CSV desde la terminal."""

from .perfil import PerfilColumna, perfilar_csv, perfilar_filas

__all__ = ["PerfilColumna", "perfilar_csv", "perfilar_filas", "__version__"]
__version__ = "0.1.0"
