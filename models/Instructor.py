from mongoengine import *


class Instructor(Document):
    nombreCompleto= StringField(max_length=50, unique=True,required=True)
    correo= StringField(max_length=50, unique=True,required=True)
    regional = StringField(max_length=50, choices=["cauca", "huila", "antioquia", "valle", "cundinamarca"], required=True)
    
    def __repr__(self):
        return f"{self.nombreCompleto}"
    



