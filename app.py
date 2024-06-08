from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from math import radians, cos, sin, asin, sqrt
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///emprendimientos.db'
db = SQLAlchemy(app)

class Emprendimiento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    categoria = db.Column(db.String(100))
    direccion = db.Column(db.String(200))
    contacto = db.Column(db.String(100))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=True)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    contraseña = db.Column(db.String(255), nullable=False)
    emprendimientos = db.relationship('Emprendimiento', backref='usuario', lazy=True)

@app.route('/emprendimientos', methods=['GET'])
def listar_emprendimientos():
    emprendimientos = Emprendimiento.query.all()
    emprendimientos_json = [{'id': emprendimiento.id, 'nombre': emprendimiento.nombre, 'descripcion': emprendimiento.descripcion, 'categoria': emprendimiento.categoria, 'direccion': emprendimiento.direccion, 'contacto': emprendimiento.contacto, 'usuario_id': emprendimiento.usuario_id} for emprendimiento in emprendimientos]
    return jsonify(emprendimientos_json)

@app.route('/emprendimientos', methods=['POST'])
def agregar_emprendimiento():
    if not request.json or not 'nombre' in request.json:
        abort(400)
    nuevo_emprendimiento = Emprendimiento(
        nombre=request.json['nombre'],
        descripcion=request.json.get('descripcion', ""),
        categoria=request.json.get('categoria', ""),
        direccion=request.json.get('direccion', ""),
        contacto=request.json.get('contacto', ""),
        usuario_id=request.json.get('usuario_id', None)
    )
    try:
        db.session.add(nuevo_emprendimiento)
        db.session.commit()
    except SQLAlchemyError as err:
        db.session.rollback()
        return jsonify({'message': str(err.__cause__)}), 500
    return jsonify({'id': nuevo_emprendimiento.id}), 201

@app.route('/emprendimientos/<int:id>', methods=['GET'])
def obtener_emprendimiento(id):
    emprendimiento = Emprendimiento.query.get_or_404(id)
    data = {
        'id': emprendimiento.id,
        'nombre': emprendimiento.nombre,
        'descripcion': emprendimiento.descripcion,
        'categoria': emprendimiento.categoria,
        'direccion': emprendimiento.direccion,
        'contacto': emprendimiento.contacto,
        'usuario_id': emprendimiento.usuario_id
    }
    return jsonify(data), 200

@app.route('/emprendimientos/<int:id>', methods=['PUT'])
def actualizar_emprendimiento(id):
    emprendimiento = Emprendimiento.query.get_or_404(id)
    if not request.json:
        abort(400)
    nombre = request.json.get('nombre', emprendimiento.nombre)
    descripcion = request.json.get('descripcion', emprendimiento.descripcion)
    categoria = request.json.get('categoria', emprendimiento.categoria)
    direccion = request.json.get('direccion', emprendimiento.direccion)
    contacto = request.json.get('contacto', emprendimiento.contacto)
    usuario_id = request.json.get('usuario_id', emprendimiento.usuario_id)
    
    emprendimiento.nombre = nombre
    emprendimiento.descripcion = descripcion
    emprendimiento.categoria = categoria
    emprendimiento.direccion = direccion
    emprendimiento.contacto = contacto
    emprendimiento.usuario_id = usuario_id
    
    try:
        db.session.commit()
    except SQLAlchemyError as err:
        db.session.rollback()
        return jsonify({'message': str(err.__cause__)}), 500
    
    return jsonify({'id': emprendimiento.id, 'nombre': emprendimiento.nombre, 'descripcion': emprendimiento.descripcion, 'categoria': emprendimiento.categoria, 'direccion': emprendimiento.direccion, 'contacto': emprendimiento.contacto, 'usuario_id': emprendimiento.usuario_id})

@app.route('/emprendimientos/<int:id>', methods=['DELETE'])
def eliminar_emprendimiento(id):
    emprendimiento = Emprendimiento.query.get_or_404(id)
    try:
        db.session.delete(emprendimiento)
        db.session.commit()
    except SQLAlchemyError as err:
        db.session.rollback()
        return jsonify({'message': str(err.__cause__)}), 500
    
    return jsonify({'resultado': True})

@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    usuarios = Usuario.query.all()
    usuarios_json = [{'id': usuario.id, 'nombre': usuario.nombre, 'email': usuario.email} for usuario in usuarios]
    return jsonify(usuarios_json)

@app.route('/usuarios', methods=['POST'])
def agregar_usuario():
    if not request.json or not 'nombre' in request.json or not 'email' in request.json or not 'contraseña' in request.json:
        abort(400)
    nuevo_usuario = Usuario(
        nombre=request.json['nombre'],
        email=request.json['email'],
        contraseña=request.json['contraseña']
    )
    try:
        db.session.add(nuevo_usuario)
        db.session.commit()
    except SQLAlchemyError as err:
        db.session.rollback()
        return jsonify({'message': str(err.__cause__)}), 500
    return jsonify({'id': nuevo_usuario.id}), 201

@app.route('/usuarios/<int:id>', methods=['GET'])
def obtener_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    data = {
        'id': usuario.id,
        'nombre': usuario.nombre,
        'email': usuario.email
    }
    return jsonify(data), 200

@app.route('/usuarios/<int:id>', methods=['PUT'])
def actualizar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    if not request.json:
        abort(400)
    nombre = request.json.get('nombre', usuario.nombre)
    email = request.json.get('email', usuario.email)
    contraseña = request.json.get('contraseña', usuario.contraseña)
    
    usuario.nombre = nombre
    usuario.email = email
    usuario.contraseña = contraseña
    
    try:
        db.session.commit()
    except SQLAlchemyError as err:
        db.session.rollback()
        return jsonify({'message': str(err.__cause__)}), 500
    
    return jsonify({'id': usuario.id, 'nombre': usuario.nombre, 'email': usuario.email})

@app.route('/usuarios/<int:id>', methods=['DELETE'])
def eliminar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    try:
        db.session.delete(usuario)
        db.session.commit()
    except SQLAlchemyError as err:
        db.session.rollback()
        return jsonify({'message': str(err.__cause__)}), 500
    
    return jsonify({'resultado': True})

# Función para obtener coordenadas utilizando la API de OpenCage

# def obtener_coordenadas(direccion):
    llave_api = 'aca iria la api'
    url = f'https://api.opencagedata.com/geocode/v1/json?q={direccion}&{llave_api}'
    
    respuesta = requests.get(url)
    datos = respuesta.json()
    
    if datos['results']:
        lat = datos['results'][0]['geometry']['lat']
        lon = datos['results'][0]['geometry']['lng']
        return (lat, lon)
    else:
        return None

# Función  para calcular la distancia entre dos puntos geográficos
# def distancia(lat1, lon1, lat2, lon2):
    # Convertir grados a radianes
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    diferencia_longitud = lon2 - lon1
    diferencia_latitud = lat2 - lat1
    
    # Aplicar fórmula de haversine
    a = sin(diferencia_latitud/2)**2 + cos(lat1) * cos(lat2) * sin(diferencia_longitud/2)**2
    c = 2 * asin(sqrt(a))
    
    radio_tierra = 6371
    
    return c * radio_tierra

# Ruta para buscar emprendimientos cercanos a una dirección
#@app.route('/buscar', methods=['GET'])
#def buscar_emprendimientos_cercanos():
    direccion_usuario = request.args.get('direccion')
    
    # Obtener las coordenadas de la dirección del usuario
    coordenadas_usuario = obtener_coordenadas(direccion_usuario)
    
    if not coordenadas_usuario:
        return jsonify({'mensaje': 'No se pudo encontrar la dirección proporcionada.'}), 400
    
    lat_usuario, lon_usuario = coordenadas_usuario
    distancia_maxima = 5  # Distancia máxima en kilómetros
    
    emprendimientos = Emprendimiento.query.all()
    emprendimientos_cercanos = []
    
    for emprendimiento in emprendimientos:
        # Obtener las coordenadas de la dirección del emprendimiento
        coordenadas_emprendimiento = obtener_coordenadas(emprendimiento.direccion)
        
        if coordenadas_emprendimiento:
            lat_emp, lon_emp = coordenadas_emprendimiento
            distancia = distancia(lat_usuario, lon_usuario, lat_emp, lon_emp)
            
            if distancia <= distancia_maxima:
                emprendimientos_cercanos.append({
                    'id': emprendimiento.id,
                    'nombre': emprendimiento.nombre,
                    'descripcion': emprendimiento.descripcion,
                    'categoria': emprendimiento.categoria,
                    'direccion': emprendimiento.direccion,
                    'contacto': emprendimiento.contacto,
                    'usuario_id': emprendimiento.usuario_id,
                    'distancia': distancia
                })
    
    return jsonify(emprendimientos_cercanos), 200

if __name__ == '__main__':
    app.run('127.0.0.1', port=8080, debug=True)