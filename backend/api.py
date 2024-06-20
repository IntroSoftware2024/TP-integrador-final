from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError


api = Flask(__name__)
engine = create_engine("URL_BASE") #Agregar url base de datos.


# ---- Rutas de Emprendimientos ---- 

# Endpoint para agregar emprendimientos

# Endpoint para listar todos los emprendimientos

# Endpoint para modificar emprendimientos

# Endpont para eliminar emprendimientos


# ---- Rutas de Usuarios ---- 

# Endpoint para agregar usuarios
@api.route('/crear_usuario', methods = ['POST'])
def crear_usuario():
    conn = engine.connect()
    new_user = request.get_json()
    query = f"""INSERT INTO usuarios (email, contraseña) VALUES ('{new_user["email"]}', '{new_user["contraseña"]}');"""
    try:
        #result = conn.execute(text(query))
        conn.commit()
        conn.close()
    except SQLAlchemyError as err:
        return jsonify({'message': 'Se ha producido un error' + str(err.__cause__)})
    
    return jsonify({'message': 'El usuario se ha creado exitosamente.' + query}), 201

# Endpoint para listar todos los usuarios
@api.route('/usuarios', methods = ['GET'])
def usuarios():
    conn = engine.connect()
    query = "SELECT * FROM usuarios;"
    try:
        result = conn.execute(text(query))
        conn.close() 
    except SQLAlchemyError as err:
        return jsonify(str(err.__cause__))

    data = []
    for row in result:
        entity = {}
        entity['usuario_id'] = row.usuario_id
        entity['email'] = row.email
        entity['contraseña'] = row.contraseña
        data.append(entity)

    return jsonify(data), 200

# ---- Rutas de Consultas ---- 

# Endpoint para agregar consultas
    
if __name__ == "__main__":
    api.run("127.0.0.1", port="5000", debug=True)
