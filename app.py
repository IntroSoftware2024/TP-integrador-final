from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)

engine = create_engine("mysql+mysqlconnector://root@localhost/emprende_facil")

@app.route('/emprendimientos/<id>', methods = ['GET'])
def mostrar_emprendimiento(id):
    conn = engine.connect()
    query = f"""SELECT emprendimiento_id, nombre, descripcion, categoria, direccion, contacto
            FROM emprendimientos
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
        data['contacto'] = row[5]
        return jsonify(data), 200
    return jsonify({"message": "El emprendimiento buscado no existe"}), 404


if __name__ == '__main__':
    app.run('127.0.0.1', port='8080', debug=True)