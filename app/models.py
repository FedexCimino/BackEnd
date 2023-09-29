from app import db

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(64), index=True, unique=True, nullable=False)
    contraseña = db.Column(db.String(128), nullable=False)
    # Agrega otros campos de usuario según sea necesario

class Servidor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(128), index=True, unique=True, nullable=False)
    descripcion = db.Column(db.String(256))
    # Agrega otros campos de servidor según sea necesario

class Canal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(128), index=True, unique=True, nullable=False)
    servidor_id = db.Column(db.Integer, db.ForeignKey('servidor.id'), nullable=False)
    # Agrega otros campos de canal según sea necesario

class Mensaje(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contenido = db.Column(db.String(512), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    canal_id = db.Column(db.Integer, db.ForeignKey('canal.id'), nullable=False)
    # Agrega otros campos de mensaje según sea necesario
