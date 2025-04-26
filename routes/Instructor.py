from app import app
from flask import request, render_template, redirect, url_for, flash, session
from models.Instructor import Instructor
from models.regional import Regional

import secrets, string
import yagmail

@app.route('/')
def index():
    print("Accediendo a la ruta principal...")
    return render_template('dashboard.html')

@app.route('/rutas')
def rutas():
    return render_template('dashboard.html')

def generar_contrasena(longitud=10):
    caracteres = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(caracteres) for _ in range(longitud))

def enviar_contrasena_por_correo(destinatario, nombre, contrasena):
    remitente = "quiraconstanza@gmail.com"
    contrasena_email = "cqzdobsjaynbjuzi"  # Usa tu app password de Gmail

    try:
        yag = yagmail.SMTP(remitente, contrasena_email)
        asunto = "Bienvenido al sistema de gestión de guías"
        contenido = f"Hola {nombre},\n\nTu contraseña es: {contrasena}"
        yag.send(to=destinatario, subject=asunto, contents=contenido)
        print("Correo enviado correctamente.")
    except Exception as e:
        print(f"Error al enviar correo: {e}")

@app.route("/agregarInstructor", methods=["GET", "POST"])
def agregar_instructor():
    if request.method == "POST":
        nombre = request.form.get("nombre_completo")
        correo = request.form.get("correo")
        idRregional = request.form.get("regional")
        contrasena = request.form.get("contrasena")
        regional = Regional.objects(id=idRregional).first()

        print("ID Regional:", idRregional)
        print("Nombre:", nombre)
        print("Correo:", correo)

        if not nombre or not correo or not regional:
            flash("Todos los campos son obligatorios.", "error")
            return redirect(url_for("agregar_instructor"))

        if nombre.strip() == "":
            flash("El nombre completo es obligatorio.", "error")
            return redirect(url_for("agregar_instructor"))

        nuevo_instructor = Instructor(
            nombre_completo=nombre,
            correo=correo,
            regional=regional,
            contrasena=contrasena
        )

        nuevo_instructor.save()
        enviar_contrasena_por_correo(correo, nombre, contrasena)
        flash("Instructor agregado correctamente. Se envió la contraseña al correo.", "success")
        return redirect(url_for("index"))

    regionales = Regional.objects()
    return render_template("agregar_instructor.html", regionales=regionales)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        correo = request.form.get("correo")
        contrasena = request.form.get("contrasena")
        instructor = Instructor.find_by_correo(correo)

        if instructor is None or instructor.contrasena != contrasena:
            flash("Correo o contraseña incorrectos", "error")
            return redirect(url_for("login"))

        session["instructor_id"] = str(instructor.id)
        flash("Inicio de sesión exitoso", "success")
        return redirect(url_for("index"))
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('instructor_id', None)
    flash('¡Has cerrado sesión!', 'info')
    return redirect(url_for('login'))
