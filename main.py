from flask import Flask
from app import app
from api import api, db

main = Flask(__name__)
main.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root@localhost/emprende_facil"
main.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(main)

main.register_blueprint(app)
main.register_blueprint(api)

if __name__ == '__main__':
    with main.app_context():
        db.create_all()  # Crear tablas en la base de datos
    main.run('127.0.0.1', port='8080', debug=True)