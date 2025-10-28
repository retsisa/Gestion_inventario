import sqlite3
import os
from datetime import date

def crear_db():
    # Si el archivo ya existe, no hacemos nada
    if os.path.exists("Inventarios.db"):
        print("✅ Base de datos existente, no se recreará.")
        return
    
    print("🆕 Creando base de datos e insertando datos iniciales...")
    con = sqlite3.connect("Inventarios.db")
    cursor = con.cursor()

    # Crear tablas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre VARCHAR(80),
        cargo VARCHAR(20) CHECK(cargo IN ('Admin','Supervisor','Usuario'))
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS equipos(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre VARCHAR(80) NOT NULL,
            estado VARCHAR(20) CHECK(estado IN('DISPONIBLE', 'AGOTADO', 'PRESTADO', 'DAÑADO')),
            ubicacion TEXT 
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prestamos(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_equipo INTEGER,
            id_usuario INTEGER,
            fecha_prestamo DATE,
            fecha_devolucion DATE,
            FOREIGN KEY (id_equipo) REFERENCES equipos(id),
            FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
        )
    ''')

    # Insertar datos de ejemplo solo una vez
    usuarios_prueba = [
        ('Crispin', 'Admin'),
        ('Alex', 'Supervisor'),
        ('Carl', 'Usuario'),
        ('Tommy', 'Usuario'),
        ('Leo', 'Usuario')
    ]
    cursor.executemany('INSERT INTO usuarios(nombre, cargo) VALUES(?,?)', usuarios_prueba)

    equipos_prueba = [
        ('Laptop', 'DISPONIBLE', 'Oficina 101'),
        ('PC-Ryzen', 'DAÑADO', 'Taller de mantenimiento'),
        ('Taladro', 'AGOTADO', 'Oficina 101'),
        ('Cable UTP', 'PRESTADO', 'Laboratorio de electrónica'),
        ('Proyector Epson', 'PRESTADO', 'Colegio OCOMISTO'),
        ('Laptop DELL', 'DISPONIBLE', 'Oficina 101'),
        ('Multímetro', 'DISPONIBLE', 'Oficina 101')
    ]
    cursor.executemany('INSERT INTO equipos(nombre, estado, ubicacion) VALUES(?,?,?)', equipos_prueba)

    prestamos_prueba = [
        (1, 4, date.today(), '2026-02-28'),
        (6, 5, '2025-06-13', '2025-09-18'),
        (7, 3, '2025-07-30', '2025-10-30')
    ]
    cursor.executemany(
        'INSERT INTO prestamos(id_equipo,id_usuario,fecha_prestamo,fecha_devolucion) VALUES(?,?,?,?)',
        prestamos_prueba
    )

    con.commit()
    con.close()
    print("✅ Base de datos inicial creada con éxito.")
