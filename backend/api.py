from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError


api = Flask(__name__)
engine = create_engine("mysql+mysqlconnector://root@localhost/basetp") #Agregar url base de datos.


# ---- Rutas de Emprendimientos ---- 

# Endpoint para agregar emprendimientos


# Endpoint para listar todos los emprendimientos


# Endpoint para eliminar emprendimientos
@api.route('/eliminar_emprendimiento/<id>', methods = ['DELETE'])
def eliminar_emplendimiento(id):
    conn = engine.connect()
#    data = request.get_json()

    query = f"""DELETE FROM emprendimientos
            WHERE id = {id};"""
          # WHERE id={data["id"]};"""

    val_query = f"SELECT * FROM emprendimientos WHERE id = {id}"

    try:
        val_result = conn.execute(text(val_query))
        if val_result.rowcount != 0:
            result = conn.execute(text(query))
            conn.commit()
            conn.close()
        else:
            conn.close()
            return jsonify({"message": "El emprendimiento con ese id no existe."}), 404
    except SQLAlchemyError as err:
        conn.close()
        return jsonify({'message': 'No se pudo borrar el emprendimiento con ese id.' + str(err.__cause__)}), 500
    return jsonify({'message': 'Se ha eliminado el emprendimiento correctamente.'}), 202


# Endpoint para modificar emprendimientos
@api.route('/modificar_emprendimiento/<id>', methods = ['PATCH'])
def modificar_emplendimiento(id):
    conn = engine.connect()
    emprendimiento = request.get_json()

    campos = ['nombre', 'instagram', 'descripcion', 'categoria', 'direccion', 'localidad', 'provincia', 'contacto']
    campos_a_actualizar = []

    if not campos_a_actualizar:
        return jsonify({'message': 'No se ha proporcionado ningún campo válido para actualizar.'}), 400

    for campo in campos:
        if campo in emprendimiento:
            valor = emprendimiento[campo]
            query = f"""UPDATE emprendimientos SET {campo} = '{valor}' 
                        WHERE id = {id};"""
            conn.execute(query)
            conn.commit()

    val_query = f"SELECT * FROM emprendimientos WHERE id = {id};"

    try:
        val_result = conn.execute(text(val_query))
        if val_result.rowcount!=0:
            result = conn.execute(text(query))
            conn.commit()
        else:
            return jsonify({'message': "No existe un emprendimiento con ese id."}), 404
        conn.close()
    except SQLAlchemyError as err:
        conn.close()
        return jsonify({'message': 'No se puedo modificar el emprendimiento con ese id. ' + str(err.__cause__)}), 500
    return jsonify({'message': 'se ha modificado correctamente el emprendimiento.' + query}), 200



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
