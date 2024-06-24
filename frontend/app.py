from flask import Flask, render_template, request, jsonify, flash, redirect, url_for, abort, session
import requests

app = Flask(__name__)

API_URL = 'http://127.0.0.1:5000'
app.secret_key = 'mysecretkey'

@app.route('/test')
def test():
    try:
        response = requests.get(API_URL.replace('/emprendimientos','/test'))
        response.raise_for_status()
        return jsonify({'message': 'Estan conectado front y back', 'backend_reponde': response.json()}),200
    except requests.exceptions.RequestException as e:
        print(f'Error fetching data:{e}')
        return jsonify({'message':'no esta conectado al back'}),500

@app.route("/")
def index():
    session.clear()
    return render_template('index.html')

@app.route("/subir_emp")
def subir_emp():
    if 'email' not in session:
        return abort(403, "Acceso prohibido. Debes iniciar sesión para acceder a esta página.")
    return render_template('subir_emp.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/contacto")
def contacto():
    return render_template('contacto.html')

# aca tiene que haber try except?
@app.route("/emprendimientos/<categoria>")
def emprendimientos(categoria):
    if categoria == 'busqueda':
        categoria = request.args.get('categoria', 'busqueda')

    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        emprendimientos = response.json().get('emprendimientos', [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        emprendimientos = []

    return render_template('emprendimientos.html', categoria=categoria, emprendimientos=emprendimientos)


# Endpoint para registrar usuario
@app.route('/registrar_usuario', methods = ['POST'])
def registrar_usuario():
    if request.method == "POST":
        email = request.form.get('email')
        contraseña = request.form.get('contraseña')
        usuario = {'email': email, 'contraseña': contraseña}
        if (email and contraseña):
            response = requests.post(API_URL + "/crear_usuario", json=usuario)
            if response.status_code == 201:
                flash("Registro exitoso!", "success")
                return redirect(url_for('login')) 
            elif response.status_code == 409:
                flash("El usuario ya existe.", "error")
                return redirect(url_for('login')) 
            else:
                flash("Registro fallido!", "error")
                return render_template('login.html')
    return render_template('login.html')


# Endpoint para iniciar sesión con el usuario ya registrado.
@app.route('/iniciar_sesion', methods = ['GET','POST'])
def iniciar_sesion():
    if request.method == 'POST':
        email = request.form.get('email')
        contraseña = request.form.get('contraseña')

        if email and contraseña:
            usuario = {'email': email, 'contraseña': contraseña}
            response = requests.post(f'{API_URL}/inicio_de_sesion', json=usuario)
            
            if response.status_code == 200:
                session['email'] = email
                return redirect(url_for('subir_emp'))
            elif response.status_code == 404:
                flash('Usuario no encontrado. Por favor, regístrese.', 'error')
                return redirect(url_for('login'))
            elif response.status_code == 401:
                flash('Contraseña incorrecta. Por favor, inténtelo nuevamente.', 'error')
                return redirect(url_for('login'))
            else:
                flash('Credenciales incorrectas. Por favor, inténtelo nuevamente.', 'error')
                return redirect(url_for('login'))
        
        flash('Por favor, proporcione su email y contraseña.', 'error')
        return redirect(url_for('login'))

    # Si el método es GET, renderizará el template del formulario de login
    return render_template('login.html')


# Ruta para agregar emprendimientos.
@app.route('/subir_emprendimiento', methods=['POST', 'GET'])
def subir_emprendimiento():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        instagram = request.form.get('instagram')
        descripcion = request.form.get('descripcion')
        categoria = request.form.get('categoria')
        direccion = request.form.get('direccion')
        localidad = request.form.get('localidad')
        provincia = request.form.get('provincia')
        contacto = request.form.get('contacto')
        
        datos = {'nombre':nombre, 'instagram':instagram, 'descripcion':descripcion, 'categoria':categoria,
                 'direccion':direccion, 'localidad':localidad, 'provincia':provincia, 'contacto':contacto}
        
        if(nombre and instagram and descripcion and categoria and direccion and localidad and provincia and contacto):
            response = requests.post(API_URL + "/agregar_emprendimiento", json=datos)
            
            if response.status_code == 201:
                print(response.json())
                emp_id = response.json().get('emprendimiento_id')
                flash("Emprendimiento agregado.", "success")
                flash(f'id de tu emprendimiento: {emp_id}')
                return redirect(url_for('subir_emp'))
            elif response.status_code == 409:
                flash("El emprendimiento ya existe.", "error")
                return redirect(url_for('subir_emp'))
            else:
                flash("Error al agregar el emprendimiento", "error")
                return redirect(url_for('subir_emp'))
    return render_template('subir_emp.html')


# Eliminar un emprendimiento
@app.route('/eliminar_emp', methods = ['DELETE'])
def eliminar_emp():
    if request.method == 'DELETE':
        id_emp = request.form.get('emprendimiento_id')
        nombre = request.form.get('nombre')
        categoria = request.form.get('categoria')
        mensaje = request.form.get('descripcion')

        datos = {'emprendimiento_id':id_emp, 'nombre':nombre, 'categoria':categoria, 'descripcion':mensaje}

        if id_emp and nombre and categoria:
            response = requests.delete(API_URL + f'/eliminar_emprendimiento/{id_emp}')
            #response = requests.delete(API_URL.join('eliminar_emprendimiento/') + id_emp)
            
            if response.status_code == 201:
                flash('Emprendimiento eliminado.')
                return redirect(url_for('subir_emp'))
            else:
                flash('Error al eliminar el emprendimiento.')
                return redirect(url_for('subir_emp'))
   
    return render_template('subir_emp.html')


# Modificar un emprendimiento
@app.route('/modificar_emp', methods = ['PATCH'])
def modificar_emp():
    if request.method == 'PATCH':
        id_emp = request.form.get('emprendimiento_id')
        nombre = request.form.get('nombre')
        instagram = request.form.get('instagram')
        descripcion = request.form.get('descripcion')
        categoria = request.form.get('categoria')
        direccion = request.form.get('direccion')
        localidad = request.form.get('localidad')
        provincia = request.form.get('provincia')
        contacto = request.form.get('contacto')

        datos = {'emprendimiento_id':id_emp, 'nombre':nombre, 'instagram':instagram, 'descripcion':descripcion, 'categoria':categoria, 
                 'direccion':direccion, 'localidad':localidad, 'provincia':provincia, 'contacto':contacto}

        if id_emp:
            response = requests.patch(API_URL.join('modificar_emprendimiento'), json=datos)
            
            if response.status_code == 201:
                flash('Emprendimiento modificado.')
                return redirect(url_for('subir_emp'))
            else:
                flash('Error al modificar el emprendimiento.')
                return redirect(url_for('subir_emp'))
   
    return render_template('subir_emp.html')



# Endpoint para form de consultas
@app.route('/enviar_consulta', methods = ['POST'])
def enviar_consulta():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        email = request.form.get('email')
        asunto = request.form.get('asunto')
        mensaje = request.form.get('mensaje')

        datos = {'nombre':nombre, 'apellido':apellido, 'email':email, 'asunto':asunto, 'mensaje':mensaje}

        if (nombre and apellido and email and asunto and mensaje):
            response = requests.post(API_URL + "/agregar_consulta", json=datos)
            
            if response.status_code == 201:
                flash("Formulario enviado.", "success")
                return render_template('contacto.html')
            else:
                flash("Error al enviar el formulario.", "error")
                return render_template('contacto.html')
   
    return render_template('contacto.html')


@app.errorhandler(Exception)
def handle_error(error):
    error_code = getattr(error, 'code', 500)

    if error_code == 404:
        return render_template('error.html', error_code=404), 404
    elif error_code == 400:
        return render_template('error.html', error_code=400), 400
    elif error_code == 403:
        return render_template('error.html', error_code=403), 403
    else:
        return render_template('error.html', error_code=500), 500

if __name__ == "__main__":
    app.run("127.0.0.1", port="8000", debug=True)