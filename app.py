from flask import Flask, render_template, request, redirect, url_for, session, flash
from mongoengine import connect
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Crear instancia de Flask
app = Flask(__name__)
app.secret_key="adsocauca"

uri=os.environ.get("URI")
db=os.environ.get("DB")
app.config["UPLOAD_FOLDER"] = "./static/imagenes"
app.config["MONGODB_SETTINGS"] = [{
    "db":db,
    "host":uri,
    "port": 27017
}]




connect(db, host=uri)





if __name__=="__main__":
    
    from routes.Guia import *
    from routes.Instructor import *
    
    app.run(port=3000, host="0.0.0.0",debug=True)
    