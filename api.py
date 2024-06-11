from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "Uri de la base" # Agregar la URI de la base de datos
db = SQLAlchemy(app)

# ---- Modelos ----

class Emprendimiento(db.Model):
    __tablename__ = 'emprendimientos'
    emprendimiento_id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    categoria = db.Column(db.String(50))
    direccion = db.Column(db.String(200))
    latitud = db.Column(db.Float)
    longitud = db.Column(db.Float)
    contacto = db.Column(db.String(50))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.usuarios_id'), nullable=True)
    usuario = db.relationship('Usuario', backref=db.backref('emprendimientos', lazy=True))

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    usuarios_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    contraseña = db.Column(db.String(255), nullable=False)

class Consultas(db.Model):
    __tablename__ = 'consultas'
    consulta_id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    asunto = db.Column(db.String(50))
    mensaje = db.Column(db.Text)

# ---- Rutas de Emprendimientos ---- 

# Endpoint para agregar emprendimientos
@app.route('/emprendimientos', methods=['POST'])
def agregar_emprendimiento():
    data = request.json
    try:
        nuevo_emprendimiento = Emprendimiento(**data)
        db.session.add(nuevo_emprendimiento)
        db.session.commit()
        return jsonify({'message': 'Emprendimiento agregado exitosamente'}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Error al agregar emprendimiento', 'error': str(e)}), 400

# Endpoint para listar todos los emprendimientos
@app.route('/emprendimientos', methods=['GET'])
def listar_emprendimientos():
    emprendimientos = Emprendimiento.query.all()
    output = []
    for emprendimiento in emprendimientos:
        emprendimiento_data = {
            'emprendimiento_id': emprendimiento.emprendimiento_id,
            'nombre': emprendimiento.nombre,
            'descripcion': emprendimiento.descripcion,
            'categoria': emprendimiento.categoria,
            'direccion': emprendimiento.direccion,
            'localidad': emprendimiento.localidad,
            'provincia': emprendimiento.provincia,
            'contacto': emprendimiento.contacto,
            'usuario_id': emprendimiento.usuario_id
        }
        output.append(emprendimiento_data)
    return jsonify({'emprendimientos': output}), 200

# Endpoint para mostrar un emprendimiento específico por su ID
@app.route('/emprendimientos/<int:id>', methods=['GET'])
def mostrar_emprendimiento(id):
    emprendimiento = Emprendimiento.query.get(id)
    if not emprendimiento:
        return jsonify({'message': 'Emprendimiento no encontrado'}), 404
    emprendimiento_data = {
        'emprendimiento_id': emprendimiento.emprendimiento_id,
        'nombre': emprendimiento.nombre,
        'descripcion': emprendimiento.descripcion,
        'categoria': emprendimiento.categoria,
        'direccion': emprendimiento.direccion,
        'localidad': emprendimiento.localidad,
        'provincia': emprendimiento.provincia,
        'contacto': emprendimiento.contacto,
        'usuario_id': emprendimiento.usuario_id
    }
    return jsonify(emprendimiento_data), 200

# Endpoint para actualizar un emprendimiento por su ID
@app.route('/emprendimientos/<int:id>', methods=['PUT'])
def actualizar_emprendimiento(id):
    emprendimiento = Emprendimiento.query.get(id)
    if not emprendimiento:
        return jsonify({'message': 'Emprendimiento no encontrado'}), 404
    data = request.json
    try:
        for key, value in data.items():
            setattr(emprendimiento, key, value)
        db.session.commit()
        return jsonify({'message': 'Emprendimiento actualizado exitosamente'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Error al actualizar emprendimiento', 'error': str(e)}), 400

# Endpoint para eliminar un emprendimiento por su ID
@app.route('/emprendimientos/<int:id>', methods=['DELETE'])
def eliminar_emprendimiento(id):
    emprendimiento = Emprendimiento.query.get(id)
    if not emprendimiento:
        return jsonify({'message': 'Emprendimiento no encontrado'}), 404
    try:
        db.session.delete(emprendimiento)
        db.session.commit()
        return jsonify({'message': 'Emprendimiento eliminado exitosamente'}), 202
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Error al eliminar emprendimiento', 'error': str(e)}), 400

# ---- Rutas de Usuarios ---- 

# Endpoint para agregar usuarios
@app.route('/usuarios', methods=['POST'])
def agregar_usuario():
    data = request.json
    try:
        nuevo_usuario = Usuario(**data)
        db.session.add(nuevo_usuario)
        db.session.commit()
        return jsonify({'message': 'Usuario agregado exitosamente'}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Error al agregar usuario', 'error': str(e)}), 400

# Endpoint para listar todos los usuarios
@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    usuarios = Usuario.query.all()
    output = []
    for usuario in usuarios:
        usuario_data = {
            'usuarios_id': usuario.usuarios_id,
            'email': usuario.email
        }
        output.append(usuario_data)
    return jsonify({'usuarios': output}), 200

# Endpoint para mostrar un usuario específico por su ID
@app.route('/usuarios/<int:id>', methods=['GET'])
def mostrar_usuario(id):
    usuario = Usuario.query.get(id)
    if not usuario:
        return jsonify({'message': 'Usuario no encontrado'}), 404
    usuario_data = {
        'usuarios_id': usuario.usuarios_id,
        'email': usuario.email
    }
    return jsonify(usuario_data), 200

# Endpoint para actualizar un usuario por su ID
@app.route('/usuarios/<int:id>', methods=['PUT'])
def actualizar_usuario(id):
    usuario = Usuario.query.get(id)
    if not usuario:
        return jsonify({'message': 'Usuario no encontrado'}), 404
    data = request.json
    try:
        for key, value in data.items():
            setattr(usuario, key, value)
        db.session.commit()
        return jsonify({'message': 'Usuario actualizado exitosamente'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Error al actualizar usuario', 'error': str(e)}), 400

# Endpoint para eliminar un usuario por su ID
@app.route('/usuarios/<int:id>', methods=['DELETE'])
def eliminar_usuario(id):
    usuario = Usuario.query.get(id)
    if not usuario:
        return jsonify({'message': 'Usuario no encontrado'}), 404
    try:
        db.session.delete(usuario)
        db.session.commit()
        return jsonify({'message': 'Usuario eliminado exitosamente'}), 202
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Error al eliminar usuario', 'error': str(e)}), 400
    
# ---- Rutas de Consultas ---- 

# Endpoint para agregar consultas
@app.route('/consultas', methods=['POST'])
def agregar_consulta():
    data = request.json
    try:
        nueva_consulta = Consultas(**data)
        db.session.add(nueva_consulta)
        db.session.commit()
        return jsonify({'message': 'Consulta agregada exitosamente'}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Error al agregar consulta', 'error': str(e)}), 400



if __name__ == '__main__':
    app.run('127.0.0.1', port='8080', debug=True)