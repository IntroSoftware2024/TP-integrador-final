from flask import Flask, render_template, request, jsonify, flash, redirect, url_for, abort, session
import requests

app = Flask(__name__)

API_URL = 'http://127.0.0.1:5000'
app.secret_key = 'mysecretkey'

@app.route("/")
def index():
    session.clear()
    return render_template('index.html', show_nav_buttons=True)

@app.route("/subir_emp")
def subir_emp():
    if 'email' not in session:
        return abort(403, "Acceso prohibido. Debes iniciar sesión para acceder a esta página.")
    return render_template('subir_emp.html', show_nav_buttons=True)

@app.route("/login")
def login():
    return render_template('login.html', show_nav_buttons=False)

@app.route("/contacto")
def contacto():
    return render_template('contacto.html', show_nav_buttons=True)

# Endpoint para registrar usuario.
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
    return render_template('login.html')

# Endpoint para agregar emprendimientos.
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
                flash("El Nombre, Instagram o el Contacto de emprendimiento ya existe.", "error")
                return redirect(url_for('subir_emp'))
            else:
                flash("Error al agregar el emprendimiento", "error")
                return redirect(url_for('subir_emp'))
    return render_template('subir_emp.html')

# Endpoint para mostrar emprendimientos por categoria.
@app.route("/emprendimientos/<categoria>", methods=['GET'])
def emprendimientos(categoria):
    response = requests.get(API_URL + f"/listar_emprendimientos/{categoria}")
    if response.status_code == 200:
        emprendimientos = response.json()
        return render_template("emprendimientos.html", emprendimientos=emprendimientos, categoria=categoria, show_nav_buttons=True)
    else:
        return render_template("emprendimientos.html", categoria=categoria, show_nav_buttons=True), 400

# Endpoint para eliminar un emprendimiento.
@app.route('/eliminar_emp', methods=['POST'])
def eliminar_emp():
    if request.method == 'POST':
        id_emp = request.form.get('emprendimiento_id')
        nombre = request.form.get('nombre')
        if id_emp and nombre:
            try:
                response = requests.delete(f'{API_URL}/eliminar_emprendimiento/{id_emp}?nombre={nombre}')
                if response.status_code == 200:
                    flash('Emprendimiento eliminado correctamente.', 'success')
                elif response.status_code == 404:
                    flash('No se encontró el emprendimiento para eliminar.', 'error')
                elif response.status_code == 400:
                    flash('El nombre de emprendimiento no coincide con el ID, intente nuevamente.', 'error')
                else:
                    flash('Error al eliminar el emprendimiento.', 'error')
            except requests.exceptions.RequestException as e:
                flash(f'Error en la solicitud al servidor API: {str(e)}', 'error')
        else:
            flash('Debe proporcionar el ID, nombre y categoría del emprendimiento.', 'error')
    return redirect(url_for('subir_emp'))

# Endpoint para modificar un emprendimiento.
@app.route('/modificar_emp', methods=['POST'])
def modificar_emp():
    if request.method == 'POST':
        id_emp = request.form.get('emprendimiento_id')
        nombreActual = request.form.get('nombreActual')
        nombre = request.form.get('nombre')
        instagram = request.form.get('instagram')
        descripcion = request.form.get('descripcion')
        categoria = request.form.get('categoria')
        direccion = request.form.get('direccion')
        localidad = request.form.get('localidad')
        provincia = request.form.get('provincia')
        contacto = request.form.get('contacto')

        if id_emp and nombreActual:
            datos = {
                'nombreActual': nombreActual,
                'nombre': nombre,
                'instagram': instagram,
                'descripcion': descripcion,
                'categoria': categoria,
                'direccion': direccion,
                'localidad': localidad,
                'provincia': provincia,
                'contacto': contacto
            }
            
            datos = {k: v for k, v in datos.items() if v}

            try:
                response = requests.patch(f'{API_URL}/modificar_emprendimiento/{id_emp}', json=datos)
                
                if response.status_code == 200:
                    flash('Emprendimiento modificado correctamente.', 'success')
                elif response.status_code == 400:
                    flash('No existe un emprendimiento con ese ID o no coincide con el nombre.', 'error')
                elif response.status_code == 404:
                    flash('No se encontró el emprendimiento para modificar.', 'error')
                else:
                    flash('Error al modificar el emprendimiento.', 'error')
            except requests.exceptions.RequestException as e:
                flash(f'Error en la solicitud al servidor API: {str(e)}', 'error')
        else:
            flash('Debe proporcionar el ID y el nombre actual del emprendimiento.', 'error')
    return redirect(url_for('subir_emp'))


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
                return render_template('contacto.html', show_nav_buttons=True)
            else:
                flash("Error al enviar el formulario.", "error")
                return render_template('contacto.html', show_nav_buttons=True)
    return render_template('contacto.html', show_nav_buttons=True)

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