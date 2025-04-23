from app import app
from flask import request, render_template, redirect, url_for
from models.Guia import Guia
from models.Instructor import Instructor
from datetime import datetime

@app.route("/agregarguia/", methods=["POST"])
def registrar_guia():
    estado = False
    mensaje = None
    try:
        nombre = int(request.form.get("txtNombre_guia"))
        descripcion = request.form.get("txtDescripcion")
        programa = request.form.get("txtPrograma_formacion")
        documento = request.files.get("fileDocumento")
        fecha = request.form.get("fechaGuia")
        instructor_id = request.form.get("txtNombre_instructor")
        instructor = Instructor.objects.get(id=instructor_id)
        nueva_guia = Guia(
            nombreGuia=nombre,
            descripcion=descripcion,
            programa_formacion=programa,
            documento_pdf=documento,
            fecha_creacion=datetime.strptime(fecha, "%Y-%m-%d"),
            instructor=instructor
        )
        nueva_guia.save()
        estado = True
        mensaje = "Guía registrada exitosamente"
    except Exception as e:
        mensaje = str(e)
    return {"estado": estado, "mensaje": mensaje}

@app.route("/guiaslistar", methods=["GET"])
def listar_guias():
    guias = Guia.objects()
    return render_template("ListarGuias.html", guias=guias)


