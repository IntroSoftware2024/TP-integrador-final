from flask import Blueprint, render_template, request

app = Blueprint('app', __name__)

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
        response = request.get(API_URL)
        response.raise_for_status()
        emprendimientos = response.json().get('emprendimientos', [])
    except request.exceptions.RequestException as e:
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
@app.route("/subir_emp")
def subir_emp():
    return render_template('subir_emp.html')

@app.route("/contacto")
def contacto():
    return render_template('contacto.html')
