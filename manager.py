
from flask import Flask, render_template, request, redirect, session
import sqlite3
import os
from openpyxl import load_workbook

app = Flask(__name__)
app.secret_key = "cecytos_clave_2026"
 

def crear_base_datos():
    conexion = sqlite3.connect("progreso.db")
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS progreso (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            alumno TEXT NOT NULL,
            materia TEXT NOT NULL,
            tema TEXT NOT NULL,
            completado INTEGER DEFAULT 0,
            UNIQUE(alumno, materia, tema)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS examenes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            alumno TEXT NOT NULL,
            materia TEXT NOT NULL,
            tipo TEXT NOT NULL,
            calificacion INTEGER NOT NULL
        )
    """)

    conexion.commit()
    conexion.close()


@app.route("/", methods=["GET", "POST"])
def inicio():
    return render_template("index.html")


@app.route("/bienvenida")
def bienvenida():
    if "alumno" in session:
        return render_template("bienvenida.html")
    else:
        return redirect("/")


@app.route("/matematicas")
def matematicas():
    return render_template("matematicas.html")


@app.route("/programacion")
def programacion():
    return render_template("programacion.html")


@app.route("/ciencias_naturales")
def ciencias_naturales():
    return render_template("ciencias_naturales.html")


@app.route("/lengua_comunicacion")
def lengua_comunicacion():
    return render_template("lengua_comunicacion.html")


@app.route("/humanidades")
def humanidades():
    return render_template("humanidades.html")


@app.route("/temas_matematicas.html")
def temas_matematicas():
    return render_template("temas_matematicas.html")


@app.route("/temas_comunicacion.html")
def temas_comunicacion():
    return render_template("temas_comunicacion.html")


@app.route("/temas_humanidades.html")
def temas_humanidades():
    return render_template("temas_humanidades.html")


@app.route("/temas_programacion.html")
def temas_programacion():
    return render_template("temas_programacion.html")


# Registrar alumnos
@app.route("/registrar", methods=["POST"])
def registrar():
    archivo = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "alumnos.xlsx"
    )

    Id = request.form.get("Id")
    nombre = request.form.get("nombre")
    edad = request.form.get("edad")
    correo = request.form.get("correo")
    grupo = request.form.get("grupo")
    contrasena = request.form.get("contrasena")

    libro = load_workbook(archivo)
    hoja = libro.active

    # Comprobar si el numero de control ya existe
    for fila in hoja.iter_rows(min_row=2, values_only=True):
        if str(fila[0]) == str(Id):
            libro.close()
            return "El numero de control ya esta registrado"

    # Guardar los datos del alumno
    hoja.append([
        Id, nombre, edad, correo, grupo, contrasena
    ])

    libro.save(archivo)
    libro.close()

    session["alumno"] = str(Id)

    return redirect("/bienvenida")


# Iniciar sesion
@app.route("/login", methods=["POST"])
def login():
    archivo = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "alumnos.xlsx"
    )

    Id = request.form.get("Id")
    contrasena = request.form.get("contrasena")

    libro = load_workbook(archivo)
    hoja = libro.active

    for fila in hoja.iter_rows(min_row=2, values_only=True):
        if (
            str(fila[0]) == str(Id)
            and str(fila[5]) == str(contrasena)
        ):
            libro.close()
            session["alumno"] = str(Id)
            return redirect("/bienvenida")

    libro.close()

    return "Numero de control o contrasena incorrectos"


# Cerrar sesion
@app.route("/cerrar_sesion")
def cerrar_sesion():
    session.clear()
    return redirect("/")


# Juegos educativos
@app.route("/juegos")
def juegos():
    if "alumno" not in session:
        return redirect("/")

    return render_template("juegos.html")


if __name__ == "__main__":
    crear_base_datos()
    app.run(debug=True)
 
