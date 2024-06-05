from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'Uri de la base de datos' # Agregar la URI de la base de datos
db = SQLAlchemy(app)

@app.route('/')
def hola_mundo():
    return 

# Definición del modelo de Usuarios
class Usuario(db.Model):
    usuarios_id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    contraseña = db.Column(db.String(255), nullable=False)

# Definición del modelo de Emprendimientos
class Emprendimiento(db.Model):
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

# Endpoint para agregar emprendimientos
@app.route('/emprendimientos', methods=['POST'])
def agregar_emprendimiento():
    data = request.json
    nuevo_emprendimiento = Emprendimiento(**data)
    db.session.add(nuevo_emprendimiento)
    db.session.commit()
    return jsonify({'message': 'Emprendimiento agregado exitosamente'}), 201

# Endpoint para listar todos los emprendimientos
@app.route('/emprendimientos', methods=['GET'])
def listar_emprendimientos():
    emprendimientos = Emprendimiento.query.all()
    output = []
    for emprendimiento in emprendimientos:
        emprendimiento_data = {
            'id': emprendimiento.id,
            'nombre': emprendimiento.nombre,
            'descripcion': emprendimiento.descripcion,
            'categoria': emprendimiento.categoria,
            'direccion': emprendimiento.direccion,
            'latitud': emprendimiento.latitud,
            'longitud': emprendimiento.longitud,
            'contacto': emprendimiento.contacto,
            'usuario_id': emprendimiento.usuario_id
        }
        output.append(emprendimiento_data)
    return jsonify({'emprendimientos': output})

# Endpoint para mostrar un emprendimiento específico por su ID
@app.route('/emprendimientos/<int:id>', methods=['GET'])
def mostrar_emprendimiento(id):
    emprendimiento = Emprendimiento.query.get(id)
    if not emprendimiento:
        return jsonify({'message': 'Emprendimiento no encontrado'}), 404
    emprendimiento_data = {
        'id': emprendimiento.id,
        'nombre': emprendimiento.nombre,
        'descripcion': emprendimiento.descripcion,
        'categoria': emprendimiento.categoria,
        'direccion': emprendimiento.direccion,
        'latitud': emprendimiento.latitud,
        'longitud': emprendimiento.longitud,
        'contacto': emprendimiento.contacto,
        'usuario_id': emprendimiento.usuario_id
    }
    return jsonify(emprendimiento_data)

# Endpoint para actualizar un emprendimiento por su ID
@app.route('/emprendimientos/<int:id>', methods=['PUT'])
def actualizar_emprendimiento(id):
    emprendimiento = Emprendimiento.query.get(id)
    if not emprendimiento:
        return jsonify({'message': 'Emprendimiento no encontrado'}), 404
    data = request.json
    for key, value in data.items():
        setattr(emprendimiento, key, value)
    db.session.commit()
    return jsonify({'message': 'Emprendimiento actualizado exitosamente'})

# Endpoint para eliminar un emprendimiento por su ID
@app.route('/emprendimientos/<int:id>', methods=['DELETE'])
def eliminar_emprendimiento(id):
    emprendimiento = Emprendimiento.query.get(id)
    if not emprendimiento:
        return jsonify({'message': 'Emprendimiento no encontrado'}), 404
    db.session.delete(emprendimiento)
    db.session.commit()
    return jsonify({'message': 'Emprendimiento eliminado exitosamente'})

if __name__ == '__main__':
    app.run('127.0.0.1', port='8080', debug=True)