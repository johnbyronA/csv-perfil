# Política de seguridad

## Versiones soportadas

| Versión | Soporte |
| ------- | ------- |
| 0.1.x   | ✅      |

## Reportar una vulnerabilidad

Por favor **no abras un issue público** para reportar vulnerabilidades.

Usa la opción privada de GitHub: pestaña **Security → Report a vulnerability** de este repositorio. Incluye:

- Descripción del problema y su impacto.
- Pasos para reproducirlo (con datos ficticios).
- Versión afectada.

Intentaremos responder en un plazo de 7 días.

## Buenas prácticas para usuarios

- `csv-perfil` procesa los archivos de forma local y **no envía datos a ningún servicio externo**.
- No incluyas datos reales, personales o confidenciales en issues, PRs ni en la carpeta `examples/`.
- Nunca subas archivos `.env`, llaves o credenciales; el `.gitignore` del proyecto ya los excluye.
