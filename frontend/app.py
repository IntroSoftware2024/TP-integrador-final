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

#Errores

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', error_code=404), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('error.html', error_code=500), 500


@app.errorhandler(400)
def bad_request(error):
    return render_template('error.html', error_code=400), 400



if __name__ == "__main__":
    app.run("127.0.0.1", port="8000", debug=True)