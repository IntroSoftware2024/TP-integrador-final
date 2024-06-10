from flask import Flask, render_template, request, redirect, url_for

app = Flask("__main__")

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/emprendimientos")
def emprendimientos():
    return render_template('emprendimientos.html')

@app.route("/subir_emp")
def subir_emp():
    return render_template('subir_emp.html')

@app.route("/contacto")
def contacto():
    return render_template('contacto.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error404.html'), 404

if __name__ == '__main__':
    app.run('127.0.0.1', port='8080', debug=True)