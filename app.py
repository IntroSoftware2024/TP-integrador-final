from flask import Blueprint, render_template

app = Blueprint('app', __name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/emprendimientos/<categoria>")
def emprendimientos(categoria):
    return render_template('emprendimientos.html', categoria=categoria)

@app.route("/subir_emp")
def subir_emp():
    return render_template('subir_emp.html')

@app.route("/contacto")
def contacto():
    return render_template('contacto.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error404.html'), 404
