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
export PIPENV_IGNORE_VIRTUALENVS=1

#Instalar flask.
pipenv install flask 

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

    #Ejecutar flask.
    flask run
}