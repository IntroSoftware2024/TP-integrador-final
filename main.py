from flask import Flask, render_template
from flask_migrate import Migrate
from app import app
from api import api, db

main = Flask(__name__)
main.config['SQLALCHEMY_DATABASE_URI'] = "URL_BASE" #Agregar URL de la base de datos acá.
main.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(main)
migrate = Migrate(main, db)

main.register_blueprint(app)
main.register_blueprint(api)

@main.errorhandler(404)
def page_not_found(error):
    return render_template('error404.html'), 404

if __name__ == '__main__':
    main.run('127.0.0.1', port='5000', debug=True)