from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from app import db
from app.models import Usuario


auth_bp = Blueprint('auth', __name__)

# Ruta para registrar nuevos usuarios
@auth_bp.route('/registro', methods=['POST'])
def registro():
    data = request.get_json()  # Obtener datos del formulario en formato JSON

    # Validar que los datos requeridos estén presentes
    if 'nombre' not in data or 'contraseña' not in data:
        return jsonify({"message": "Nombre de usuario y contraseña son requeridos"}), 400

    nombre = data['nombre']
    contraseña = data['contraseña']

    # Verificar si el usuario ya existe en la base de datos
    usuario_existente = Usuario.query.filter_by(nombre=nombre).first()
    if usuario_existente:
        return jsonify({"message": "El nombre de usuario ya está en uso"}), 400

    # Crear un nuevo usuario y almacenar la contraseña de forma segura (hashing)
    nuevo_usuario = Usuario(nombre=nombre, contraseña=generate_password_hash(contraseña, method='sha256'))

    try:
        db.session.add(nuevo_usuario)
        db.session.commit()
        return jsonify({"message": "Usuario registrado con éxito"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500
    
# Ruta para iniciar sesión de usuarios
@auth_bp.route('/iniciar_sesion', methods=['POST'])
def iniciar_sesion():
    data = request.get_json()  # Obtener datos del formulario en formato JSON

    # Validar que los datos requeridos estén presentes
    if 'nombre' not in data or 'contraseña' not in data:
        return jsonify({"message": "Nombre de usuario y contraseña son requeridos"}), 400

    nombre = data['nombre']
    contraseña = data['contraseña']

    # Buscar al usuario en la base de datos por nombre
    usuario = Usuario.query.filter_by(nombre=nombre).first()

    # Verificar si el usuario existe y si la contraseña es válida
    if usuario and check_password_hash(usuario.contraseña, contraseña):
        # Establecer una sesión para el usuario logueado
        session['usuario_id'] = usuario.id
        return jsonify({"message": "Inicio de sesión exitoso"}), 200

    return jsonify({"message": "Nombre de usuario o contraseña incorrectos"}), 401

