from app import app
from flask import request, render_template, redirect, url_for, flash
from models.Instructor import Instructor
import secrets, string
import smtplib
from email.message import EmailMessage


@app.route('/')
def index():
    return render_template('dashboard.html')

def generar_contrasena(longitud=10):
    caracteres = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(caracteres) for _ in range(longitud))

def enviar_contrasena_por_correo(destinatario, nombre, contrasena):
    remitente = "quiraconstanza@gmail.com" 
    contrasena_email = "cqzdobsjaynbjuzi" 

    mensaje = EmailMessage()
    mensaje["Subject"] = "Tu acceso al sistema"
    mensaje["From"] = remitente
    mensaje["To"] = destinatario
    mensaje.set_content(f"Hola {nombre},\n\nTu contraseña temporal es: {contrasena}")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
            servidor.login(remitente, contrasena_email)
            servidor.send_message(mensaje)
        print("Correo enviado correctamente.")
    except Exception as e:
        print(f"Error al enviar correo: {e}")
        
@app.route("/agregarInstructor", methods=["GET", "POST"])
def agregar_instructor():
    if request.method == "POST":
        nombre = request.form.get("nombre_completo")
        correo = request.form.get("correo")
        regional = request.form.get("regional")

        if not nombre or not correo or not regional:
            flash("Todos los campos son obligatorios.", "error")
            return redirect(url_for("agregar_instructor"))

        if nombre is None or nombre.strip() == "":
            flash("El nombre completo es obligatorio.", "error")
            return redirect(url_for("agregar_instructor"))

        contrasena = generar_contrasena()
        nuevo_instructor = Instructor(
            nombre_completo=nombre,
            correo=correo,
            regional=regional
        )
        nuevo_instructor.establecer_contrasena(contrasena)
        nuevo_instructor.save()
        enviar_contrasena_por_correo(correo, nombre, contrasena)
        flash("Instructor agregado correctamente. Se envió la contraseña al correo.", "success")
        return redirect(url_for("agregar_instructor"))
    return render_template("agregar_instructor.html")

from flask import request, redirect, url_for, render_template, flash, session
from models.Instructor import Instructor

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        correo = request.form.get("correo")
        contrasena = request.form.get("contrasena")

        instructor = Instructor.find_by_correo(correo)

        if instructor and instructor.verificar_contrasena(contrasena):
            session["instructor_id"] = str(instructor.id)

            flash("Inicio de sesión exitoso", "success")
            return redirect(url_for("index"))  
        else:
            flash("Correo o contraseña incorrectos", "error")
            return redirect(url_for("login"))

    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('instructor_id', None)
    flash('¡Has cerrado sesión!', 'info')
    return redirect(url_for('login'))