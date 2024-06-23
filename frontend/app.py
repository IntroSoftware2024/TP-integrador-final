from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_URL = 'http://127.0.0.1:5000/emprendimientos'

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

if __name__ == "__main__":
    app.run("127.0.0.1", port="8000", debug=True)