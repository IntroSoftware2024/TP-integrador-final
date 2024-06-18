from flask import Blueprint, render_template, request
import requests

app = Blueprint('app', __name__)

API_URL = 'http://127.0.0.1:5000/emprendimientos'

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/emprendimientos/<categoria>")
def emprendimientos(categoria):
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        emprendimientos = response.json().get('emprendimientos', [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        emprendimientos = []

    if categoria != 'busqueda':
        emprendimientos = [e for e in emprendimientos if categoria.lower() in e['categoria'].lower()]

    return render_template('emprendimientos.html', categoria=categoria, emprendimientos=emprendimientos)

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/contacto")
def contacto():
    return render_template('contacto.html')
