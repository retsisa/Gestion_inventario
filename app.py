from flask import Flask, render_template,request,session,redirect,url_for
import sqlite3
from datetime import date
from dotenv import load_dotenv
import os

load_dotenv()

app=Flask(__name__)
app.secret_key=os.getenv("SECRET_KEY")

@app.route("/", methods=["GET","POST"])
def login():
    if request.method=="POST":
        nombre=request.form["nombre"]
        conn=get_conexion()
        user=conn.execute("SELECT * FROM usuarios WHERE nombre=?",(nombre,)).fetchone()
        conn.close()
        
        if user:
            session["nombre"]=user["nombre"]
            return redirect(url_for("articulos"))
        else:
            return render_template("login.html", error="Usuario no encontrado")
    
    return render_template('login.html')

def get_conexion():
    #con=sqlite3.connect('Python-SQLite/practica_crispin/Inventarios.db')
    con=sqlite3.connect('Inventarios.db')
    con.row_factory=sqlite3.Row
    return con

@app.route("/articulos")
def articulos():
    if "nombre" not in session:
        return redirect(url_for("login"))
    
    conn=get_conexion()
    equipos=conn.execute("SELECT * FROM equipos").fetchall()
    vencidos = equipos_vencidos()
    
    conn.close()
    return render_template("articulos.html", equipos=equipos, nombre=session["nombre"], vencidos=vencidos)

@app.route('/nuevo', methods=["GET","POST"])
def nuevo():
    if request.method=="POST":
        nombre=request.form["nombre"]
        estado=request.form["estado"]
        ubicacion=request.form["ubicacion"]
        
        conn=get_conexion()
        conn.execute(
            "INSERT INTO equipos(nombre, estado, ubicacion) VALUES(?,?,?)",
            (nombre, estado, ubicacion),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("articulos"))
    return render_template("editar_articulo.html", titulo="Nuevo articulo", boton="Guardar")

@app.route("/editar/<int:id>", methods=["GET","POST"])
def editar(id):
    conn=get_conexion()
    equipo=conn.execute("SELECT * FROM equipos WHERE id=?",(id,)).fetchone()
    if request.method=="POST":
        nombre=request.form["nombre"]
        estado=request.form["estado"]
        ubicacion=request.form["ubicacion"]
        conn.execute("UPDATE equipos SET nombre=?, estado=?, ubicacion=? WHERE id=?",
                     (nombre, estado, ubicacion, id),)
        conn.commit()
        conn.close()
        return redirect(url_for("articulos"))
    conn.close()
    return render_template("editar_articulo.html", equipo=equipo, titulo="Editar Artículo", boton="Actualizar")

@app.route('/eliminar/<int:id>')
def eliminar(id):
    conn=get_conexion()
    conn.execute("DELETE FROM equipos WHERE id=?",(id,))
    conn.commit()
    conn.close()
    return redirect(url_for("articulos"))

def equipos_vencidos():
    conn=get_conexion()
    cursor=conn.cursor()
    hoy=date.today().strftime("%Y-%m-%d")
    cursor.execute('''
                 SELECT e.nombre, p.id_usuario, u.nombre as usuario,p.fecha_devolucion  FROM prestamos p
                 JOIN equipos e ON p.id_equipo=e.id
                 JOIN usuarios u ON p.id_usuario=u.id
                 WHERE p.fecha_devolucion < ? AND e.estado='PRESTADO'
                 ''',(hoy,))
    
    vencidos=cursor.fetchall()
    conn.close()
    return vencidos

@app.route('/reportes_usuarios')
def reportes_usuarios():
    conn=get_conexion()
    cursor=conn.cursor()
    cursor.execute("""
        SELECT u.nombre as usuario, e.nombre as equipo, p.fecha_prestamo, p.fecha_devolucion
        FROM prestamos p
        JOIN usuarios u ON p.id_usuario = u.id
        JOIN equipos e ON p.id_equipo = e.id
        ORDER BY u.nombre, p.fecha_prestamo
    """)
    
    reportes = cursor.fetchall()
    conn.close()
    
    return render_template("reportes.html", reportes=reportes)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__=="__main__":
    app.run(debug=True)