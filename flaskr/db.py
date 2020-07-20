from contextlib import contextmanager
import click

from flask import current_app, g
from flask.cli import with_appcontext
from flask.globals import session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash

from flaskr.schema import create_db, LoginPassword, Team


@contextmanager
def get_db(): # подключается к базе данных g - хранилище информации в flask
    """ Подключается к БД"""
    if 'engine' not in g:
        engine = create_engine(current_app.config['DATABASE'])
        g.engine = engine
        g.sessionmaker = sessionmaker(bind=engine)

    try:
        session = g.sessionmaker()
        yield session
    finally:
        session.close()


def close_db(e=None):
    """ Закрывает БД"""
    g.pop('sessionmaker', None)
    engine = g.pop('engine', None)
    if engine:
        engine.dispose()


def init_db():
    """Инициализирует БД"""
    with get_db():
        create_db(g.engine)

# Для того чтобы инициализировать БД нужно вручную в командную строку ввести команду init-db (или ту, которую задашь)
# Это нужно чтобы бы не потреять данные
# Если база данных инициализирована выводится сообщение
@click.command('init-db') # команда, вызывающая инициализ-ю БЗ: flask init-db
@with_appcontext
def init_db_command():
    """Инициализурует БД по команде init-db""" # В тройных кавычках пишется документация строго: 1-ая строчка внутри функции
    init_db() # инициализация БД
    click.echo('База данных в папке scheme.sql подключена, все работает.') # печать сообщения в консоль


def init_app(app): # ВАЖНО, эта функция должна быть вызвана в _init_/py
    """Закроет БД когда это нужно и добавит команду init-db. Эта функция д.б. вызвана в _init_/py"""
    app.teardown_appcontext(close_db) # говорит Flask вызвать эту функцию при очистке после возврата ответа.
    app.cli.add_command(init_db_command) # добавляет новую команду, которую можно вызвать с помощью flaskкоманды.
    app.cli.add_command(create_user_command)


def create_user(login, password, team_name): #здесь обрабатываются полученные данные
    with get_db() as session:
        # проверяем что такого логина еще не существует
        if session.query(LoginPassword.userlogin).filter(LoginPassword.userlogin==login).first() is None:
            # проверяем что нет команды с таким же названием
            if session.query(Team.team_name).filter(Team.team_name==team_name).first() is None:
                # Добавить назание команды в таблицу Team
                session.add_all([
                    Team(team_name=team_name)])
                session.commit()
                #узнать id, по которому записана название этой команды в Team
                id = session.query(Team.id).filter(Team.team_name==team_name).one()
                # заполнить строку в login_password данными
                session.add_all([
                    LoginPassword(userlogin=login,
                                userpassword=generate_password_hash(password),
                                id_command=id[0])
                                ])
                session.commit()
                click.echo("User {} has been added".format(login))
            else:
                click.echo("This team name already exists.")
                # Если такой логин уже есть
        else:
            click.echo("This login already exists.")
        session.commit()



@click.command('create-user')
@click.argument('login')
@click.argument('password')
@click.argument('team_name')
@with_appcontext
def create_user_command(login, password, team_name): #здесь вводится название команды
    create_user(login, password, team_name)



# def create_db():
#     # как добавлять значения в таблицу
#     session.add_all([
#         Login_password(userlogin="good",
#                        userpassword="pbkdf2:sha256:150000$dFGNPY9B$b17f13b33dc62b0ca95126c6a100fad9b15d7cf73072dfe6b289833b1199bb41",
#                        id_command=3),
#         Login_password(userlogin="bad",
#                        userpassword="pbkdf2:sha256:150000$6hzyuS0V$beab9a20230e3eb2555fa66c0d6666fdb0dba8bf60e272f7d29414c5e555ed9d",
#                        id_command=2)
#     ])
#     # добавленные значения нужно заливать
#     session.commit()

#     session.add_all([
#         Member(member_name="Anna", factor="0.2", number_team=1),
#         Member(member_name="Alisa", factor="0.3", number_team=1),
#         Member(member_name="Sasha", factor="0.4", number_team=2),
#         Member(member_name="Stepan", factor="0.5", number_team=2),
#         Member(member_name="Tasha", factor="0.6", number_team=3),
#         Member(member_name="Tomas", factor="0.7", number_team=3),
#     ])
#     session.commit()

#     session.add_all([
#         Stats(team_id=1, sprint_name="Ollala", result=15),
#         Stats(team_id=1, sprint_name="Oppapa", result=45),
#     ])
#     session.commit()
