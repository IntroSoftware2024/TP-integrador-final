from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError


api = Flask(__name__)
engine = create_engine("mysql+mysqlconnector://root@localhost/emprendimientos") #Agregar url base de datos.

# ---- Rutas de Usuarios ---- 

# Endpoint para agregar usuarios
@api.route('/crear_usuario', methods = ['POST'])
def crear_usuario():
    try:
        conn = engine.connect()
    except SQLAlchemyError as err:
        return jsonify({'message': 'Error al conectar con la base de datos.' + str(err.__cause__)}), 500
    except Exception as err:
        return jsonify({'message': 'Ocurrió un error inesperado al conectar con la base de datos.' + str(err)}), 500
    
    new_user = request.get_json()
    if not new_user:
        return jsonify({'message': 'No se enviaron datos en el cuerpo de la solicitud'}), 400

    email = new_user.get("email")
    password = new_user.get("contraseña")

    if not (email and password):
        return jsonify({'message': 'No se enviaron todos los datos necesarios por JSON'}), 400

    check_query = text("SELECT * FROM usuarios WHERE email = :email")
    try:
        result = conn.execute(check_query, {'email': email}).fetchone()
        if result:
            return jsonify({'message': 'El usuario ya existe.'}), 409
    except SQLAlchemyError as err:
        return jsonify({'message': 'Error al verificar la existencia del usuario. ' + str(err.__cause__)}), 500

    query = text("INSERT INTO usuarios (email, contraseña) VALUES (:email, :password)")

    try:
        with engine.connect() as conn:
            conn.execute(query, {'email': email, 'password': password})
            conn.commit()
    except SQLAlchemyError as err:
        return jsonify({'message': 'El usuario no pudo ser registrado. ' + str(err.__cause__)}), 400

    return jsonify({'message': 'El usuario se registró correctamente.'}), 201

# Endpoint para iniciar sesion
@api.route('/inicio_de_sesion', methods=['POST'])
def inicio_de_sesion():
    try:
        conn = engine.connect()
    except SQLAlchemyError as err:
        return jsonify({'message': 'Error al conectar con la base de datos: ' + str(err.__cause__)}), 500
    except Exception as err:
        return jsonify({'message': 'Ocurrió un error inesperado al conectar con la base de datos: ' + str(err)}), 500

    user = request.get_json()

    if 'email' not in user or 'contraseña' not in user:
        conn.close()
        return jsonify({'message': 'Se deben proporcionar el email y la contraseña.'}), 400

    email = user['email']
    contraseña = user['contraseña']
    
    query = text("SELECT * FROM usuarios WHERE email = :email")
    try:
        result = conn.execute(query, {'email': email}).fetchone()

        if not result:
            conn.close()
            return jsonify({'message': 'Usuario no encontrado.'}), 404
        
        contraseña_usuario = result[2]
        if contraseña_usuario != contraseña:
            conn.close()
            return jsonify({'message': 'Contraseña incorrecta.'}), 401

        conn.close()
        return jsonify({'message': 'Inicio de sesión exitoso.'}), 200
    
    except SQLAlchemyError as e:
        conn.close()
        return jsonify({'message': 'Error al iniciar sesión: ' + str(e.__cause__)}), 500

    except Exception as e:
        conn.close()
        return jsonify({'message': 'Error inesperado: ' + str(e)}), 500

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


# ---- Rutas de Emprendimientos ---- 

# Endpoint para agregar emprendimientos
@api.route('/agregar_emprendimiento', methods=['POST'])
def agregar_emprendimiento():
    conn = engine.connect()
    nuevo_emprendimiento = request.get_json() 

    if not (nuevo_emprendimiento.get("nombre") and nuevo_emprendimiento.get("instagram") and nuevo_emprendimiento.get("descripcion")
            and nuevo_emprendimiento.get("categoria") and nuevo_emprendimiento.get("direccion") and nuevo_emprendimiento.get("localidad") 
            and nuevo_emprendimiento.get("provincia") and nuevo_emprendimiento.get("contacto")):
        return jsonify({'message': 'No se enviaron todos los datos necesarios por JSON'}), 400

    query = f"""INSERT INTO emprendimientos (nombre, instagram, descripcion, categoria, direccion, localidad, provincia, contacto)
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
    
    emprendimiento = request.get_json()

    if not (emprendimiento['emprendimiento_id'] and emprendimiento['nombre'] and emprendimiento['categoria']):
        conn.close()
        return jsonify({'message': 'Se debee ingresar el id, el nombre y la categoría.'}), 400

    query = f"DELETE FROM emprendimientos WHERE emprendimiento_id = {id};"
    val_query = f"SELECT * FROM emprendimientos WHERE emprendimiento_id = {id};"

    try:
        result = conn.execute(text(val_query))
        if result.rowcount != 0:
            conn.execute(text(query))
            conn.commit()
            conn.close()
        else:
            conn.close()
            return jsonify({'message': 'No existe un emprendimiento con ese id.'}), 404
    except SQLAlchemyError as err:
        conn.close()
        return jsonify({'message': 'No se pudo borrar el emprendimiento con ese id. ' + str(err.__cause__)}), 500
    except Exception as err:
        conn.close()
        return jsonify({'message': 'Ocurrió un error inesperado al intentar eliminar el emprendimiento. ' + str(err)}), 500

    return jsonify({'message': 'Se ha eliminado el emprendimiento correctamente.'}), 202


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

    if not (emprendimiento['emprendimiento_id'] and emprendimiento['nombre']):
        conn.close()
        return jsonify({'message': 'Se debee ingresar el id, el nombre y lo que se desee modificar.'}), 400

    campos = ['nombre', 'instagram', 'descripcion', 'categoria', 'direccion', 'localidad', 'provincia', 'contacto']
    campos_a_actualizar = {campo: emprendimiento[campo] for campo in campos if campo in emprendimiento}

    if not campos_a_actualizar:
        conn.close()
        return jsonify({'message': 'No se ha proporcionado ningún campo válido para actualizar.'}), 400

    query = f"UPDATE emprendimientos SET {', '.join([f'{campo} = :{campo}' for campo in campos_a_actualizar])} WHERE id = :id"
#    campos_a_actualizar['id'] = id
    val_query = f"SELECT * FROM emprendimientos WHERE id = {id};"

    try:
        result = conn.execute(text(val_query))
        if result.rowcount != 0:
            conn.execute(text(query), campos_a_actualizar)
            conn.commit()
            conn.close()
        else:
            conn.close()
            return jsonify({'message': 'No existe un emprendimiento con ese id.'}), 404
    except SQLAlchemyError as err:
        conn.close()
        return jsonify({'message': 'No se pudo borrar el emprendimiento con ese id. ' + str(err.__cause__)}), 500
    except Exception as err:
        conn.close()
        return jsonify({'message': 'Ocurrió un error inesperado al intentar eliminar el emprendimiento. ' + str(err)}), 500

    return jsonify({'message': 'Se ha modificado correctamente el emprendimiento.'}), 202


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
