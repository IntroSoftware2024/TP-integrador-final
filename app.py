from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root@localhost/emprende_facil"
db = SQLAlchemy(app)

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

engine = create_engine("mysql+mysqlconnector://root@localhost/emprende_facil")

@app.route('/crear_emprendimiento', methods = ['POST'])
def create_user():
    conn = engine.connect()
    nuevo_emprend = request.get_json()
    query = f"""INSERT INTO Emprendimientos (nombre, descripcion, categoria, direccion, latitud, longitud,
    contacto, usuario_id) 
    VALUES ('{nuevo_emprend["nombre"]}', '{nuevo_emprend["descripcion"]}', '{nuevo_emprend["categoria"]}',
    '{nuevo_emprend["direccion"]}', '{nuevo_emprend["latitud"]}', '{nuevo_emprend["longitud"]}',
    '{nuevo_emprend["contacto"]}', '{nuevo_emprend["usuario_id"]}');"""
    try:
        result = conn.execute(text(query))
        conn.commit()
        conn.close()
    except SQLAlchemyError as err:
        return jsonify({'message': 'Se ha producido un error' + str(err.__cause__)})
    
    return jsonify({'message': 'El emprendimeinto se ha agregado correctamente' + query}), 201

@app.route('/emprendimientos/<id>', methods = ['GET'])
def mostrar_emprendimiento(id):
    conn = engine.connect()
    query = f"""SELECT *
            FROM Emprendimientos
            WHERE emprendimiento_id = {id};
            """
    try:
        result = conn.execute(text(query))
        conn.commit()
        conn.close()
    except SQLAlchemyError as err:
        return jsonify(str(err.__cause__))
    if result.rowcount !=0:
        data = {}
        row = result.first()
        data['id'] = row[0]
        data['nombre'] = row[1]
        data['descripcion'] = row[2]
        data['categoria'] = row[3]
        data['direccion'] = row[4]
        data['latitud'] = row[5]
        data['longitud'] = row[6]
        data['contacto'] = row[7]
        data['usuario_id'] = row[8]
        return jsonify(data), 200
    return jsonify({"message": "El emprendimiento buscado no existe"}), 404


if __name__ == '__main__':
    app.run('127.0.0.1', port='8080', debug=True)