Gestor de Incidencias de Soporte TI

Proyecto personal en Python para practicar y demostrar conocimientos básicos de programación y bases de datos.

Simula un sistema simple de registro de incidencias de soporte técnico, inspirado en mi experiencia trabajando en soporte TI e infraestructura.
- Registra incidencias (título, descripción, prioridad, estado) en una base de datos SQLite.
- Lista todas las incidencias o solo las que están abiertas.
- Permite actualizar el estado de una incidencia (Abierta / En proceso / Resuelta).
- Genera un reporte en CSV con la cantidad de incidencias por estado.

Tecnologías usadas

- Python (funciones, control de flujo, manejo de archivos)
- SQL con SQLite (CREATE TABLE, INSERT, SELECT, JOIN, WHERE, UPDATE, GROUP BY)
- CSV para exportar reportes

No requiere instalar dependencias externas: usa solo librerías incluidas en Python (`sqlite3`, `csv`, `datetime`).

Cómo ejecutarlo

```bash
python3 ticket_manager.py
```

Y seguir las opciones del menú en la terminal.

Estructura de la base de datos

- **prioridades**: id, nombre (Baja / Media / Alta)
- **incidencias**: id, título, descripción, prioridad_id (relacionado con `prioridades`), estado, fecha_creación

Quería practicar de forma concreta cómo se conecta Python con una base de datos relacional, aplicando conceptos que vengo aprendiendo (SQL, programación básica) a un caso real de mi experiencia laboral en soporte TI.
