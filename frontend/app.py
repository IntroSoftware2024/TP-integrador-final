from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
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

@app.route("/subir_emp")
def emp():
    return render_template('subir_emp.html')

@app.route("/")
def index():
    return render_template('index.html')

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

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/contacto")
def contacto():
    return render_template('contacto.html')


@app.errorhandler(Exception)
def handle_error(error):
    # Determinar el código de error
    error_code = getattr(error, 'code', 500)
    # Mostrar un mensaje de error personalizado dependiendo del código de error
    if error_code == 404:
        return render_template('error.html', error_code=404), 404
    elif error_code == 400:
        return render_template('error.html', error_code=400), 400
    elif error_code == 403:
        return render_template('error.html', error_code=403), 403
    else:
        return render_template('error.html', error_code=500), 500



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
            else:
                flash("Registro fallido!", "error")
                return render_template('login.html')
    return render_template('login.html')


#login
@app.route('/iniciar_sesion', methods = ['GET','POST'])
def iniciar_sesion():
    if request.method == 'POST':
        email = request.form.get('email')
        contraseña = request.form.get('contraseña')
        usuario = {'email':email, 'contraseña':contraseña}

        if email and contraseña:
            response = requests.post(API_URL.join('iniciar_sesion'), json=usuario)
            
            if response.status_code == 201:
                return redirect(url_for('subir_emp'))
            else:
                flash('Error al iniciar sesión.')
                return redirect(url_for('login'))
   
    return render_template('login.html')


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


if __name__ == "__main__":
    app.run("127.0.0.1", port="8000", debug=True)