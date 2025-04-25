from mongoengine import *
class Programa(Document):
    nombre = StringField(max_length=50, unique=True, required=True)
    


    def __repr__(self):
        return f"{self.nombre}"