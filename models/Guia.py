from mongoengine import *
from models.Instructor import  Instructor



class Guia(Document):
    nombreGuia = IntField(unique=True, required=True)
    descripcion = StringField(max_length=80, required=True)
    programa_formacion = StringField(max_length=50, required=True)            
    documento_pdf = FileField(required=True)
    fecha_creacion = DateTimeField(required=True)    
    instructor = ReferenceField(Instructor, required= True) 

    def __repr__(self):
        return self.nombreGuia
    