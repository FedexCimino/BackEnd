from flask import Blueprint, request, jsonify, session, current_app, Flask, render_template

from werkzeug.utils import secure_filename
from werkzeug.exceptions import HTTPException, BadRequest, NotFound, Forbidden, InternalServerError
import os
from app import db
from app.models import Usuario, Servidor, Canal, Mensaje

api_bp = Blueprint('api', __name__)

# Ruta para crear un nuevo servidor
@api_bp.route('/crear_servidor', methods=['POST'])
def crear_servidor():
    if 'usuario_id' not in session:
        return jsonify({"message": "Acceso no autorizado"}), 403

    data = request.get_json()
    nombre_servidor = data.get('nombre_servidor')
    descripcion_servidor = data.get('descripcion_servidor')

    if not nombre_servidor:
        return jsonify({"message": "El nombre del servidor es requerido"}), 400

    nuevo_servidor = Servidor(nombre=nombre_servidor, descripcion=descripcion_servidor)
    db.session.add(nuevo_servidor)

    # Asociar el servidor al usuario que lo creó
    usuario = Usuario.query.get(session['usuario_id'])
    nuevo_servidor.usuarios.append(usuario)

    try:
        db.session.commit()
        return jsonify({"message": "Servidor creado con éxito"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

# Ruta para buscar servidores por nombre
@api_bp.route('/buscar_servidores', methods=['GET'])
def buscar_servidores():
    if 'usuario_id' not in session:
        return jsonify({"message": "Acceso no autorizado"}), 403

    # Obtener el término de búsqueda desde los parámetros de la solicitud GET
    termino_busqueda = request.args.get('termino_busqueda')

    # Realizar la búsqueda en la base de datos
    servidores_encontrados = Servidor.query.filter(Servidor.nombre.like(f'%{termino_busqueda}%')).all()

    # Crear una lista de resultados
    resultados = []
    for servidor in servidores_encontrados:
        resultados.append({
            "id": servidor.id,
            "nombre": servidor.nombre,
            "descripcion": servidor.descripcion,
            "cantidad_usuarios": len(servidor.usuarios)
        })

    return jsonify({"resultados": resultados}), 200

# Ruta para actualizar el perfil de usuario
@api_bp.route('/perfil', methods=['PUT'])
def actualizar_perfil():
    if 'usuario_id' not in session:
        return jsonify({"message": "Acceso no autorizado"}), 403

    data = request.form  # Obtener datos del formulario

    # Obtener el usuario actualmente logueado
    usuario = Usuario.query.get(session['usuario_id'])

    # Validar que el usuario actual sea el propietario del perfil
    if usuario.nombre != data.get('nombre'):
        return jsonify({"message": "No tienes permiso para modificar este perfil"}), 403

    # Actualizar datos personales si se proporcionan
    nuevo_nombre = data.get('nuevo_nombre')
    nueva_descripcion = data.get('nueva_descripcion')

    if nuevo_nombre:
        usuario.nombre = nuevo_nombre
    if nueva_descripcion:
        usuario.descripcion = nueva_descripcion

    # Procesar la imagen de perfil si se carga
    if 'imagen_perfil' in request.files:
        imagen_perfil = request.files['imagen_perfil']

        # Verificar que la extensión del archivo sea válida (por ejemplo, solo permitir imágenes)
        if imagen_perfil and allowed_file(imagen_perfil.filename):
            # Generar un nombre de archivo seguro para la imagen
            filename = secure_filename(imagen_perfil.filename)
            # Guardar la imagen en el directorio de imágenes de perfil
            ruta_imagen = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            imagen_perfil.save(ruta_imagen)

            # Actualizar la ruta de la imagen en el perfil del usuario
            usuario.ruta_imagen_perfil = filename

    try:
        db.session.commit()
        return jsonify({"message": "Perfil actualizado con éxito"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

# Función para verificar si la extensión de archivo es válida
def allowed_file(filename):return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png', 'gif'}

# Ruta para cerrar la sesión de usuario
@api_bp.route('/cerrar_sesion', methods=['POST'])
def cerrar_sesion():
    # Verificar si el usuario está autenticado
    if 'usuario_id' in session:
        session.pop('usuario_id', None)  # Eliminar la sesión del usuario

    return jsonify({"message": "Sesión cerrada con éxito"}), 200

# Manejador de errores para HTTP 400 - Bad Request
@api_bp.errorhandler(BadRequest)
def handle_bad_request(e):
    response = jsonify({"message": "Solicitud incorrecta", "error": str(e)})
    response.status_code = 400
    return response

# Manejador de errores para HTTP 404 - Not Found
@api_bp.errorhandler(NotFound)
def handle_not_found(e):
    response = jsonify({"message": "Recurso no encontrado", "error": str(e)})
    response.status_code = 404
    return response

# Manejador de errores para HTTP 403 - Forbidden
@api_bp.errorhandler(Forbidden)
def handle_forbidden(e):
    response = jsonify({"message": "Acceso no autorizado", "error": str(e)})
    response.status_code = 403
    return response

# Manejador de errores para HTTP 500 - Internal Server Error
@api_bp.errorhandler(InternalServerError)
def handle_internal_server_error(e):
    response = jsonify({"message": "Error interno del servidor", "error": str(e)})
    response.status_code = 500
    return response

