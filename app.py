from flask import Flask, render_template, request, redirect, url_for

app = Flask("__main__")

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/emprendimientos/<categoria>")
def emprendimientos(categoria):
    return render_template('emprendimientos.html', categoria=categoria)

'''
@app.route('/emprendimientos2')
def emprendimientos2():
    categoria = request.args.get('categoria', default=None)
    palabra = request.args.get('palabra', default=None)
    provincia = request.args.get('provincia', default=None)
    return render_template('emprendimientos.html', categoria=categoria, palabra=palabra, provincia=provincia)
'''

@app.route("/subir_emp")
def subir_emp():
    return render_template('subir_emp.html')

@app.route("/contacto")
def contacto():
    return render_template('contacto.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error404.html'), 404


@app.route('/form', methods=['GET', 'POST'])
def registrar_emp():
    if request.method == 'POST':
        nombre = request.form['nombre']
        instagram = request.form['instagram']
        localidad = request.form['localidad']
        provincia = request.form['provincia']
        contacto = request.form['contacto']
        categoria  = request.form['categoria']
        descripcion = request.form['descripcion']

        '''    
        conexion_MySQLdb = connectionBD()
        cursor = conexion_MySQLdb.cursor(dictionary=True)
            
        sql = ("INSERT INTO empleados(nombre, instagram, localidad, provincia, contacto, categoria, descripcion) VALUES (%s, %s, %s, %s)")
        valores = (nombre, instagram, localidad, provincia, contacto, categoria, descripcion)
        cursor.execute(sql, valores)
        conexion_MySQLdb.commit()
        
        cursor.close() #Cerrando conexion SQL
        conexion_MySQLdb.close() #cerrando conexion de la BD
        msg = 'Registro con exito'
        
        print(cursor.rowcount, "registro insertado")
        print("1 registro insertado, id", cursor.lastrowid)
        '''

        return render_template('subir_emp.html', msg='Formulario enviado')
    else:
        return render_template('subir_emp.html', msg = 'Metodo HTTP incorrecto')


if __name__ == '__main__':
    app.run('127.0.0.1', port='8080', debug=True)