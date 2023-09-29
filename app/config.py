import os

# Configuración de la base de datos (MySQL)
SQLALCHEMY_DATABASE_URI = 'mysql://usuario:contraseña@localhost/nombre_base_de_datos'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Configuración secreta para proteger la sesión de usuario (debes generar una clave secreta)
SECRET_KEY = 'tu_clave_secreta'

UPLOAD_FOLDER = 'ruta_de_tu_directorio_de_imagenes'
