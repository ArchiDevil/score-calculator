import os
from os import read

from flask import Flask, redirect, url_for


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE='sqlite:///' + os.path.join(app.instance_path, 'flaskr.sqlite'), #говорит где лежит база данных и как она называется
        # os.path.join - создает путь с /
    )

    if test_config is None: # для будущихх тестов
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)


    from . import db # импортировать из db.py (там все относящееся к базе данных)
    db.init_app(app) # функция из db, которая говорит....
    # теперь можем создать - инициализировать базу данных
    # с помощью flask init-db !!!!!!!!!!!!!!!!!!!!

    from . import blueprint # импортировать модуль blueprint (файл)
    app.register_blueprint(blueprint.bp) # из этого модуля достаем переменную bp


    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path) #пытается создать папку
    except OSError:
        pass

    @app.route('/')
    def index():
        return redirect(url_for('blueprint.tables'))

    return app