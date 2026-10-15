# Guía de contribución

¡Gracias por tu interés en mejorar **csv-perfil**!

## Cómo reportar un problema

1. Busca primero en los [issues](https://github.com/johnbyronA/csv-perfil/issues) por si ya existe.
2. Abre un issue con la plantilla correspondiente (error o mejora).
3. Si compartes un CSV de ejemplo, **usa datos ficticios**: nunca subas información personal, de clientes o de tu empresa.

## Cómo proponer cambios

1. Haz un *fork* y crea una rama descriptiva: `git checkout -b feat/soporte-excel`.
2. Instala el entorno de desarrollo: `pip install -e ".[dev]"`.
3. Escribe o actualiza las pruebas en `tests/`.
4. Verifica que todo pase:
   ```bash
   ruff check .
   pytest
   ```
5. Usa mensajes de commit claros, idealmente con [Conventional Commits](https://www.conventionalcommits.org/es/) (`feat:`, `fix:`, `docs:`...).
6. Abre un Pull Request completando la plantilla y describe el *qué* y el *por qué*.

## Estilo de código

- Python 3.9+ y solo biblioteca estándar en el código del paquete.
- Formato y linting con `ruff` (línea máxima de 120 caracteres).
- Funciones públicas con *docstrings* en español.

## Código de conducta

Este proyecto sigue el [Código de Conducta](CODE_OF_CONDUCT.md). Al participar, aceptas cumplirlo.
