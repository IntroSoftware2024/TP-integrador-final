from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError


api = Flask(__name__)
engine = create_engine("mysql+mysqlconnector://root@localhost/") #Agregar url base de datos.


# ---- Rutas de Emprendimientos ---- 

# Endpoint para agregar emprendimientos
@api.route('/agregar_emprendimiento', methods=['POST'])
def agregar_emprendimiento():
    conn = engine.connect()
    nuevo_emprendimiento = request.get_json()

    '''
    campos = ['nombre', 'instagram', 'descripcion', 'categoria', 'direccion', 'localidad', 'provincia', 'contacto']
    campos_validos = {campo: nuevo_emprendimiento.get(campo) for campo in campos}
    
    if not all(campos_validos.values()):
        return jsonify({'message': 'Todos los campos son obligatorios.'}), 400

    query = f"""INSERT INTO emprendimientos ({', '.join(campos_validos.keys())}) 
                VALUES ({', '.join([f"'{valor}'" for valor in campos_validos.values()])});"""
    '''   

    if not (nuevo_emprendimiento.get("nombre") and nuevo_emprendimiento.get("instagram") and nuevo_emprendimiento.get("descripcion")
            and nuevo_emprendimiento.get("categoria") and nuevo_emprendimiento.get("direccion") and nuevo_emprendimiento.get("localidad") 
            and nuevo_emprendimiento.get("provincia") and nuevo_emprendimiento.get("contacto")):
        return jsonify({'message': 'No se enviaron todos los datos necesarios por JSON'}), 400

    query = f"""INSERT INTO consultas (nombre, instagram, descripcion, categoria, direccion, localidad, provincia, contacto)
                VALUES
                ('{nuevo_emprendimiento["nombre"]}', '{nuevo_emprendimiento["instagram"]}', '{nuevo_emprendimiento["descripcion"]}', 
                '{nuevo_emprendimiento["categoria"]}', '{nuevo_emprendimiento["direccion"]}', '{nuevo_emprendimiento["localidad"]}', 
                '{nuevo_emprendimiento["provincia"]}', '{nuevo_emprendimiento["contacto"]}');"""
    
    try:
        result = conn.execute(text(query))
        conn.commit()
        conn.close()
    except SQLAlchemyError as err:
        conn.close()
        return jsonify({'message': 'Error al agregar emprendimiento. ' + str(err.__cause__)}), 500

    return jsonify({'message': 'Emprendimiento agregado exitosamente.'}), 201

# Endpoint para listar todos los emprendimientos
@api.route('/emprendimientos', methods=['GET'])
def listar_emprendimientos():
    try:
        conn = engine.connect()
    except SQLAlchemyError as err:
        return jsonify({'message': 'Error al conectar con la base de datos.' + str(err.__cause__)}), 500
    except Exception as err:
        return jsonify({'message': 'Ocurrió un error inesperado al conectar con la base de datos.' + str(err)}), 500

    query = "SELECT * FROM emprendimientos;"

    try:
        result = conn.execute(text(query))
    except SQLAlchemyError as err:
        conn.close()
        return jsonify({'message': 'Error al obtener emprendimientos.' + str(err.__cause__)}), 500
    except Exception as err:
        conn.close()
        return jsonify({'message': 'Ocurrió un error inesperado al obtener los emprendimientos.' + str(err)}), 500
    finally:
        conn.close()

    data = []
    for row in result:
        entity = {
            'id': row.id,
            'nombre': row.nombre,
            'instagram': row.instagram,
            'descripcion': row.descripcion,
            'categoria': row.categoria,
            'direccion': row.direccion,
            'localidad': row.localidad,
            'provincia': row.provincia,
            'contacto': row.contacto
        }
        data.append(entity)

    return jsonify({'emprendimientos': data}), 200


# Endpoint para eliminar emprendimientos
@api.route('/eliminar_emprendimiento/<id>', methods=['DELETE'])
def eliminar_emprendimiento(id):
    try:
        conn = engine.connect()
    except SQLAlchemyError as err:
        return jsonify({'message': 'Error al conectar con la base de datos.' + str(err.__cause__)}), 500
    except Exception as err:
        return jsonify({'message': 'Ocurrió un error inesperado al conectar con la base de datos.' + str(err)}), 500

    query = f"DELETE FROM emprendimientos WHERE id = {id};"
    val_query = f"SELECT * FROM emprendimientos WHERE id = {id};"

    try:
        val_result = conn.execute(text(val_query))
        if val_result.rowcount != 0:
            conn.execute(text(query))
            conn.commit()
            message = {'message': 'Se ha eliminado el emprendimiento correctamente.'}
            status_code = 202
        else:
            message = {"message": "El emprendimiento con ese id no existe."}
            status_code = 404
    except SQLAlchemyError as err:
        message = {'message': 'No se pudo borrar el emprendimiento con ese id. ' + str(err.__cause__)}
        status_code = 500
    except Exception as err:
        message = {'message': 'Ocurrió un error inesperado al intentar eliminar el emprendimiento. ' + str(err)}
        status_code = 500
    finally:
        conn.close()
    
    return jsonify(message), status_code


# Endpoint para modificar emprendimientos
@api.route('/modificar_emprendimiento/<id>', methods=['PATCH'])
def modificar_emprendimiento(id):
    try:
        conn = engine.connect()
    except SQLAlchemyError as err:
        return jsonify({'message': 'Error al conectar con la base de datos.' + str(err.__cause__)}), 500
    except Exception as err:
        return jsonify({'message': 'Ocurrió un error inesperado al conectar con la base de datos.' + str(err)}), 500

    emprendimiento = request.get_json()

    campos = ['nombre', 'instagram', 'descripcion', 'categoria', 'direccion', 'localidad', 'provincia', 'contacto']
    campos_a_actualizar = {campo: emprendimiento[campo] for campo in campos if campo in emprendimiento}

    if not campos_a_actualizar:
        conn.close()
        return jsonify({'message': 'No se ha proporcionado ningún campo válido para actualizar.'}), 400

    query = f"UPDATE emprendimientos SET {', '.join([f'{campo} = :{campo}' for campo in campos_a_actualizar])} WHERE id = :id"
    campos_a_actualizar['id'] = id

    try:
        val_query = f"SELECT * FROM emprendimientos WHERE id = {id};"
        val_result = conn.execute(text(val_query))
        if val_result.rowcount != 0:
            conn.execute(text(query), campos_a_actualizar)
            conn.commit()
            message = {'message': 'Se ha modificado correctamente el emprendimiento.'}
            status_code = 200
        else:
            message = {'message': 'No existe un emprendimiento con ese id.'}
            status_code = 404
    except SQLAlchemyError as err:
        message = {'message': 'No se pudo modificar el emprendimiento con ese id. ' + str(err.__cause__)}
        status_code = 500
    except Exception as err:
        message = {'message': 'Ocurrió un error inesperado al intentar modificar el emprendimiento. ' + str(err)}
        status_code = 500
    finally:
        conn.close()

    return jsonify(message), status_code



# ---- Rutas de Usuarios ---- 

# Endpoint para agregar usuarios
@api.route('/crear_usuario', methods = ['POST'])
def crear_usuario():
    conn = engine.connect()
    new_user = request.get_json()
    if not (new_user.get("email") and new_user.get("contraseña")):
        return jsonify({'message': 'No se enviaron todos los datos necesarios por JSON'}), 400

    query = f"""INSERT INTO usuarios (email, contraseña)
    VALUES
    ('{new_user["email"]}', '{new_user["contraseña"]}');"""
    try:
        result = conn.execute(text(query))
        conn.commit()
        conn.close()
    except SQLAlchemyError as err:
        conn.close()
        return jsonify({'message': 'El usuario no pudo ser registrado. ' + str(err.__cause__)}), 400
    return jsonify({'message': 'El usuario se registro correctamente.'}), 201 


# Endpoint para iniciar sesion
@api.route('/iniciar_sesion', methods = ['POST'])
def iniciar_sesion():
    try:
        conn = engine.connect()
    except SQLAlchemyError as err:
        return jsonify({'message': 'Error al conectar con la base de datos.' + str(err.__cause__)}), 500
    except Exception as err:
        return jsonify({'message': 'Ocurrió un error inesperado al conectar con la base de datos.' + str(err)}), 500

    user = request.get_json()

    # Verificar si se recibieron los campos necesarios
    if 'email' not in user or 'contraseña' not in user:
        conn.close()
        return jsonify({'message': 'Se deben proporcionar el email y la contraseña.'}), 400

    query = f""""SELECT * FROM users WHERE email = {user['email']};"""

    try:
        conn.execute(text(query))
        conn.commit()
        conn.close()
    except SQLAlchemyError as e:
        conn.close()
        return jsonify({'message': 'Error al iniciar sesión.' + str(e.__cause__)}), 500
    except Exception as e:
        conn.close()
        return jsonify({'message': 'Error inesperado: ' + str(e)}), 500 
    
    return jsonify({'message': 'Se inició sesión exitosamente.' + query}), 201  


# Endpoint para listar todos los usuarios
@api.route('/usuarios', methods=['GET'])
def usuarios():
    try:
        conn = engine.connect()
    except SQLAlchemyError as err:
        return jsonify({'message': 'Error al conectar con la base de datos.' + str(err.__cause__)}), 500
    except Exception as err:
        return jsonify({'message': 'Ocurrió un error inesperado al conectar con la base de datos.' + str(err)}), 500
    
    query = "SELECT * FROM usuarios;"  


    try:
        query = "SELECT * FROM usuarios;"
        result = conn.execute(text(query))
        data = [{
            'usuario_id': row.usuario_id,
            'email': row.email,
            'contraseña': row.contraseña
        } for row in result]
    except SQLAlchemyError as err:
        return jsonify({'message': 'Error al obtener usuarios.' + str(err.__cause__)}), 500
    except Exception as err:
        return jsonify({'message': 'Ocurrió un error inesperado al obtener los usuarios.' + str(err)}), 500
    finally:
        conn.close()  

    return jsonify(data), 200  



# ---- Rutas de Consultas ---- 

# Endpoint para agregar consultas
@api.route('/agregar_consulta', methods=['POST'])
def agregar_consulta():
    conn = engine.connect()
    nueva_consulta = request.get_json()
    if not (nueva_consulta.get("nombre") and nueva_consulta.get("apellido") and nueva_consulta.get("email")
            and nueva_consulta.get("asunto") and nueva_consulta.get("mensaje")):
        return jsonify({'message': 'No se enviaron todos los datos necesarios por JSON'}), 400

    query = f"""INSERT INTO consultas (nombre, apellido, email, asunto, mensaje)
    VALUES
    ('{nueva_consulta["nombre"]}', '{nueva_consulta["apellido"]}', '{nueva_consulta["email"]}', '{nueva_consulta["asunto"]}', '{nueva_consulta["mensaje"]}');"""
    try:
        result = conn.execute(text(query))
        conn.commit()
        conn.close()
    except SQLAlchemyError as err:
        conn.close()
        return jsonify({'message': 'El mensaje no pudo ser enviado. ' + str(err.__cause__)}), 400
    return jsonify({'message': 'El mensaje se envió correctamente.'}), 201



if __name__ == "__main__":
    api.run("127.0.0.1", port="5000", debug=True)
