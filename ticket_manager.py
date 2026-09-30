

import sqlite3
import csv
from datetime import datetime

NOMBRE_BD = "incidencias.db"


def conectar():
    "Abre la conexión a la base de datos SQLite"
    return sqlite3.connect(NOMBRE_BD)


def crear_tablas():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prioridades (
            id INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS incidencias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descripcion TEXT,
            prioridad_id INTEGER,
            estado TEXT NOT NULL DEFAULT 'Abierta',
            fecha_creacion TEXT,
            FOREIGN KEY (prioridad_id) REFERENCES prioridades(id)
        )
    """)

    # Cargamos las prioridades básicas solo la primera vez
    cursor.execute("SELECT COUNT(*) FROM prioridades")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO prioridades (id, nombre) VALUES (?, ?)",
            [(1, "Baja"), (2, "Media"), (3, "Alta")]
        )

    conexion.commit()
    conexion.close()


def agregar_incidencia():
    """Pide datos al usuario y guarda una nueva incidencia (INSERT)."""
    print("\n--- Nueva incidencia ---")
    titulo = input("Título: ").strip()
    descripcion = input("Descripción: ").strip()

    print("Prioridad -> 1: Baja | 2: Media | 3: Alta")
    try:
        prioridad_id = int(input("Elegí una prioridad (1-3): "))
        if prioridad_id not in (1, 2, 3):
            raise ValueError
    except ValueError:
        print("Prioridad inválida, se asigna 'Media' por defecto.")
        prioridad_id = 2

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M")

    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO incidencias (titulo, descripcion, prioridad_id, estado, fecha_creacion)
        VALUES (?, ?, ?, 'Abierta', ?)
    """, (titulo, descripcion, prioridad_id, fecha))
    conexion.commit()
    conexion.close()

    print("Incidencia guardada correctamente.\n")


def listar_incidencias(filtro_estado=None):

    conexion = conectar()
    cursor = conexion.cursor()

    consulta = """
        SELECT incidencias.id, incidencias.titulo, prioridades.nombre,
               incidencias.estado, incidencias.fecha_creacion
        FROM incidencias
        JOIN prioridades ON incidencias.prioridad_id = prioridades.id
    """

    parametros = ()
    if filtro_estado:
        consulta += " WHERE incidencias.estado = ?"
        parametros = (filtro_estado,)

    cursor.execute(consulta, parametros)
    resultados = cursor.fetchall()
    conexion.close()

    if not resultados:
        print("\nNo hay incidencias para mostrar.\n")
        return

    print(f"\n{'ID':<4}{'Título':<25}{'Prioridad':<10}{'Estado':<12}{'Fecha':<18}")
    print("-" * 70)
    for fila in resultados:
        print(f"{fila[0]:<4}{fila[1]:<25}{fila[2]:<10}{fila[3]:<12}{fila[4]:<18}")
    print()


def cambiar_estado():
    """Permite actualizar el estado de una incidencia existente (UPDATE)."""
    listar_incidencias()
    try:
        id_incidencia = int(input("ID de la incidencia a actualizar: "))
    except ValueError:
        print("ID inválido.\n")
        return

    print("Nuevo estado -> 1: Abierta | 2: En proceso | 3: Resuelta")
    opciones = {"1": "Abierta", "2": "En proceso", "3": "Resuelta"}
    nuevo_estado = opciones.get(input("Elegí una opción (1-3): "), "Abierta")

    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute(
        "UPDATE incidencias SET estado = ? WHERE id = ?",
        (nuevo_estado, id_incidencia)
    )
    conexion.commit()
    conexion.close()
    print("Estado actualizado.\n")


def generar_reporte():
   
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT estado, COUNT(*) as cantidad
        FROM incidencias
        GROUP BY estado
    """)
    resultados = cursor.fetchall()
    conexion.close()

    if not resultados:
        print("\nNo hay datos suficientes para generar un reporte.\n")
        return

    nombre_archivo = "reporte_incidencias.csv"
    with open(nombre_archivo, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["Estado", "Cantidad"])
        escritor.writerows(resultados)

    print(f"\nReporte generado: {nombre_archivo}")
    for estado, cantidad in resultados:
        print(f"  {estado}: {cantidad}")
    print()


def menu():
    """Menú principal del programa."""
    crear_tablas()

    while True:
        print("=== Gestor de Incidencias de Soporte TI ===")
        print("1. Agregar incidencia")
        print("2. Listar todas las incidencias")
        print("3. Listar solo incidencias abiertas")
        print("4. Cambiar estado de una incidencia")
        print("5. Generar reporte (CSV)")
        print("6. Salir")

        opcion = input("Elegí una opción: ").strip()

        if opcion == "1":
            agregar_incidencia()
        elif opcion == "2":
            listar_incidencias()
        elif opcion == "3":
            listar_incidencias(filtro_estado="Abierta")
        elif opcion == "4":
            cambiar_estado()
        elif opcion == "5":
            generar_reporte()
        elif opcion == "6":
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida, probá de nuevo.\n")


if __name__ == "__main__":
    menu()
