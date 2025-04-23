from mongoengine import *
from werkzeug.security import generate_password_hash, check_password_hash

class Instructor(Document):
    nombre_completo = StringField(max_length=50, unique=True, required=True)
    correo = StringField(max_length=50, unique=True, required=True)
    regional = StringField(
        max_length=50, 
        choices=["cauca", "huila", "antioquia", "valle", "cundinamarca"], 
        required=True
    )
    contrasena_segura = StringField(required=True)

    def establecer_contrasena(self, contrasena):
        self.contrasena_segura = generate_password_hash(contrasena)

    def verificar_contrasena(self, contrasena):
        return check_password_hash(self.contrasena_segura, contrasena)

    @classmethod
    def find_by_correo(cls, correo):
        return cls.objects(correo=correo).first()
    
    def __repr__(self):
        return f"{self.nombre_completo}"
