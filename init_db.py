import sqlite3
from datetime import date

#para subirlo al onrender 
#con=sqlite3.connect('Inventarios.db')
#esto para la prueba de escritorio en tu locacion
con=sqlite3.connect('Python-SQLite/practica_crispin/Inventarios.db')
cursor=con.cursor()
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
    
""" 
equipos_prueba=[('Laptop','DISPONIBLE','En la Oficina 101'),('PC-RYSEN','DAÑADO','Taller de mantenimiento "Confia"'),
                ('Taladro','AGOTADO','En la Oficina 101'),('Cable UTP','PRESTADO','Laboratorio de electronica'),
                ('Proyector Epson','PRESTADO','Colegio "OCOMISTO"'), ('LapTop DELL','DISPONIBLE','En la oficina 101'),
                ('Multimetro','DISPONIBLE','En la oficina 101')]
        
for nombre, estado, ubicacion in equipos_prueba:
    cursor.execute('INSERT INTO equipos(nombre, estado, ubicacion) VALUES(?,?,?)',
                (nombre,estado, ubicacion))
    
prestamos_prueba=[(1,4,date.today(),'2026-02-28'),(6,5,'2025-06-13','2025-09-18'),(7,3,'2025-07-30','2025-10-30')]
    
for id_equipo,id_usuario,fecha_prestamo,fecha_devolucion in prestamos_prueba:
    cursor.execute('INSERT INTO prestamos(id_equipo,id_usuario,fecha_prestamo, fecha_devolucion) VALUES(?,?,?,?)',
                (id_equipo,id_usuario,fecha_prestamo,fecha_devolucion)) 
    
usuarios_prueba=[('Crispin','Admin'),('Alex','Supervisor'),('Carl','Usuario'),('Tommy','Usuario'),('Leo','Usuario')]
    
for nombre, cargo in usuarios_prueba:
    cursor.execute('INSERT INTO usuarios(nombre, cargo) VALUES(?,?)',
                (nombre,cargo))

con.commit()"""

usu=cursor.execute('SELECT * FROM usuarios')
print(usu.fetchall())
print("--------")
usu=cursor.execute('SELECT * FROM equipos')
print(usu.fetchall())
print("--------")
usu=cursor.execute('SELECT * FROM prestamos')
print(usu.fetchall())
print("--------")
hoy = date.today().strftime("%Y-%m-%d")
usu=cursor.execute(''' SELECT e.nombre, p.id, u.nombre as usuario,p.fecha_devolucion FROM prestamos p
                 JOIN equipos e ON p.id_equipo=e.id
                 JOIN usuarios u ON p.id_usuario=u.id
                 WHERE p.fecha_devolucion < ? AND e.estado='PRESTADO'
                 ''',(hoy,))
print(usu.fetchall())