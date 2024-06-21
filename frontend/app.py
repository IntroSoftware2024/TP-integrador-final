from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_URL = 'http://127.0.0.1:5000/emprendimientos'

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/emprendimientos/<categoria>")
def emprendimientos(categoria):
    if categoria == 'busqueda':
        categoria = request.args.get('categoria', 'busqueda')

    palabra = request.args.get('palabra', '')
    provincia = request.args.get('provincia', '')
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        emprendimientos = response.json().get('emprendimientos', [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        emprendimientos = []

    # Filtrar los emprendimientos según la categoría, palabra y provincia
    if palabra:
        emprendimientos = [e for e in emprendimientos if palabra.lower() in e['nombre'].lower() or palabra.lower() in e['descripcion'].lower()]
    if provincia:
        emprendimientos = [e for e in emprendimientos if provincia.lower() in e['provincia'].lower()]
    if categoria != 'busqueda':
        emprendimientos = [e for e in emprendimientos if categoria.lower() in e['categoria'].lower()]

    return render_template('emprendimientos.html', categoria=categoria, emprendimientos=emprendimientos, palabra=palabra, provincia=provincia)

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/contacto")
def contacto():
    return render_template('contacto.html')

# Errores (HAY DOS TIPOS ELEGIR CUAL USAR)

# -----OPCION 1 IGUAL A LA QUE EL PROFE DIJO MAL---------

"""

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', error_code=404), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('error.html', error_code=500), 500

@app.errorhandler(400)
def bad_request(error):
    return render_template('error.html', error_code=400), 400

"""

# OPCION 2 

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

if __name__ == "__main__":
    app.run("127.0.0.1", port="8000", debug=True)