#!/bin/bash

#Verificar si se proporcionó un archivo como argumento.
if [ $# -eq 0 ]; then
    echo "Se debe proporcionar un archivo: $0 <archivo.py>"
    exit 1
fi

#Guardar el archivo que se proporcionó como argumento.
flask_file="$1"

#Verificar si el archivo existe.
if [ ! -f "$flask_file" ]; then
    echo "El archivo $flask_file no existe."
    exit 1
fi

# Verificar si pipenv está instalado
if ! command -v pipenv &> /dev/null; then
    echo "pipenv no está instalado. Instalando pipenv..."
    # Instalar pipenv para el usuario actual
    pip install --user pipenv

fi

#Verificar si existe una carpeta .venv; si no existe, crearla.
if [ ! -d ".venv" ]; then
    mkdir .venv
fi

#Instalar flask y flask-migrate.
pipenv install flask flask-migrate

#Activar el entorno virtual y ejecutar los comandos restantes dentro de él.
source "$(pipenv --venv)/bin/activate" && {

    #Instalar dependencias mysql.
    pip install flask_sqlalchemy
    pip install mysql-connector-python
    pip install requests

    #Activar el modo debug.
    export FLASK_DEBUG=1

    #Obtener el nombre del archivo sin la extensión .py
    flask_module=$(basename -s .py "$flask_file")

    #Setear el nombre del programa.
    export FLASK_APP="$flask_module"

    # Crear las tablas en la base de datos.
    flask db init
    flask db migrate -m "Initial migration."
    flask db upgrade

    #Ejecutar flask.
    flask run
}