from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)

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