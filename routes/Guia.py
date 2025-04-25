# routes/Guia.py
from flask import Blueprint, render_template, request, send_from_directory, session, redirect, url_for, flash
from models.Guia import NombreGuia
from models.Instructor import Instructor
from werkzeug.utils import secure_filename
import os

guia_bp = Blueprint('guia', __name__)

UPLOAD_FOLDER = 'uploads/pdf'
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@guia_bp.route("/listarguia", methods=["GET"])
def listar_guias():
    guias = NombreGuia.objects()
    return render_template("listarguia.html", guias=guias)

@guia_bp.route("/agregarguia", methods=['GET', 'POST'])
def agregar_guia():
    if 'instructor_id' not in session:
        flash('Debes iniciar sesión para realizar esta acción', 'warning')
        return redirect(url_for('login'))

    mensaje = None
    estado = False
    instructores = Instructor.objects()

    if request.method == 'POST':
        try:
            if 'documento' not in request.files:
                mensaje = "No se ha cargado ningún archivo PDF."
                return render_template("agregarguia.html", mensaje=mensaje, estado=estado, instructores=instructores)
            documento = request.files['documento']
            if documento.filename == '':
                mensaje = "No seleccionaste un archivo PDF."
                return render_template("agregarguia.html", mensaje=mensaje, estado=estado, instructores=instructores)
            if documento and allowed_file(documento.filename):
                filename = secure_filename(documento.filename)
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                documento.save(filepath)
                nombreguia = request.form.get("nombreguia")
                descripcions = request.form.get("descripcions")
                programaformacion = request.form.get("programaformacion")
                fecha = request.form.get("fecha")
                instructor_id = request.form.get("intructordeproceso")
                instructor_ref = Instructor.objects(id=instructor_id).first()
                if instructor_ref:
                    nueva_guia = NombreGuia(
                        nombreguia=nombreguia,
                        descripcions=descripcions,
                        programaformacion=programaformacion,
                        documento=filename,
                        fecha=fecha,
                        intructordeproceso=instructor_ref
                    )
                    nueva_guia.save()
                    estado = True
                    mensaje = "Guía registrada exitosamente."
                else:
                    mensaje = "Instructor no encontrado."
            else:
                mensaje = "El archivo no es un PDF válido."
        except Exception as e:
            import traceback
            traceback.print_exc()
            mensaje = f"Error al guardar la guía: {str(e)}"
    return render_template("agregarguia.html", mensaje=mensaje, estado=estado, instructores=instructores)

@guia_bp.route('/uploads/pdf/<path:filename>')
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)
