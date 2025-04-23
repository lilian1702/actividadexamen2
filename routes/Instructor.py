from app import app, db
from flask import request, render_template, session, redirect, url_for
from models.Instructor import Instructor
from dotenv import load_dotenv

load_dotenv()


@app.route("/")
def login():
    return render_template("IniciarSesion.html")



@app.route("/iniciarSesion/", methods=["POST"])
def iniciarSesion():
    mensaje = None
    try:
        username = request.form["username"]
        password = request.form["password"]
        if not username or not password:
            mensaje = "Usuario y contraseña son requeridos"
            return render_template("IniciarSesion.html", mensaje=mensaje)
        instructor = Instructor.objects(nombreCompleto=username).first()
        if instructor:  
            session["username"] = username
            return render_template("contenido.html")
        else:
            mensaje = "Usuario o contraseña incorrectos"
    except Exception as error:
        mensaje = str(error)
    return render_template("IniciarSesion.html", mensaje=mensaje)



@app.route("/cerrarSesion/")
def cerrarSesion():
    session.clear()
    mensaje = "Sesión cerrada"
    return render_template("IniciarSesion.html", mensaje=mensaje)


