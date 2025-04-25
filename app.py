from flask import Flask
from mongoengine import connect
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Configuración inicial de Flask
app = Flask(__name__)
app.secret_key = "adsocauca"

# Cargar configuración desde .env
uri = os.environ.get("URI")
db = os.environ.get("DB")

# Configurar carpeta de subida y base de datos
app.config["UPLOAD_FOLDER"] = "./static/imagenes"
app.config["MONGODB_SETTINGS"] = [{
    "db": db,
    "host": uri,
    "port": 27017
}]

# Conectar con MongoDB
connect(db, host=uri)

# Importar y registrar Blueprints
from routes.Guia import guia_bp
from routes.Instructor import instructor_bp


app.register_blueprint(guia_bp)
app.register_blueprint(instructor_bp)

# Ejecutar la aplicación
if __name__ == "__main__":
    
    app.run(port=3000, host="0.0.0.0", debug=True)
