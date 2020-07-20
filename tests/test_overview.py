from sqlalchemy.orm import session
from flaskr.db import get_db
from flaskr.schema import Stats

def test_check_initial_enter(client):
    response = client.get('/')
    assert response.status_code == 302
    assert '/team/tables' in response.location


# проверить, что без правильного логина и пароля нельзя войти на сраницу /tables
def test_check_privacy_tables(client):
    response = client.get('/team/tables')
    assert response.status_code == 302
    assert '/team/login' in response.location


def test_check_members(logged_client):
    response = logged_client.get('/team/tables')
    assert response.status_code == 200


def test_check_names(logged_client):
    response = logged_client.get('/team/tables')
    assert b'Anna' in response.data
    assert b'Alisa' in response.data
    assert b'Sasha' not in response.data
    assert b'Stepan' not in response.data
    assert b'Tasha' not in response.data
    assert b'Tomas' not in response.data


def test_check_factor(logged_client):
    response = logged_client.get('/team/tables')
    assert b'0.2' in response.data
    assert b'0.3' in response.data
    assert b'0.4' not in response.data
    assert b'0.5' not in response.data
    assert b'0.6' not in response.data
    assert b'0.7' not in response.data


def test_check_sprint_name(logged_client, app):
    with app.app_context():
        with get_db() as sess:
            sess.add_all([
                Stats(team_id=1, sprint_name="important_sprint", result=2500),
                Stats(team_id=1, sprint_name="clever_sprint", result=3267),
                Stats(team_id=2, sprint_name="another_sprint", result=12345),
                Stats(team_id=3, sprint_name="one_more_sprint", result=9876),
                        ])
            sess.commit()

    response = logged_client.get('/team/tables')
    assert b'important_sprint' in response.data
    assert b'2500' in response.data
    assert b'clever_sprint' in response.data
    assert b'3267' in response.data
    assert b'another_sprint' not in response.data
    assert b'12345' not in response.data
    assert b'one_more_sprint' not in response.data
    assert b'9876' not in response.data


# Проверяем, что поведший видит только участников свой команды
def test_check_visibility_members(client):
    response = client.post('/team/login',
                           data={
                               'userlogin': 'good',
                               'userpassword': 'morning',
                           })
    assert response.status_code == 302
    assert '/team/tables' in response.location

    response = client.get('/team/tables')
    assert b'Tasha' in response.data
    assert b'Tomas' in response.data
    assert b'Sasha' not in response.data
    assert b'Stepan'not in response.data

    response = client.post('/team/login',
                           data={
                               'userlogin': 'bad',
                               'userpassword': 'boy',
                           })
    assert response.status_code == 302
    assert '/team/tables' in response.location

    response = client.get('/team/tables')
    assert b'Sasha' in response.data
    assert b'Stepan' in response.data
    assert b'Tasha' not in response.data
    assert b'Tomas' not in response.data


def test_check_delete_name_inaccessible_wo_login(client):
    response = client.get('/team/members/delete/1')
    assert response.status_code == 302
    assert '/team/login' in response.location


# Тест который проверяет удаляются ли имена
def test_check_delete_name(logged_client):
    response = logged_client.get('/team/members/delete/1')
    assert response.status_code == 302
    assert '/team/tables' in response.location

    response = logged_client.get('/team/tables')
    assert b'Alisa' in response.data
    assert b'Anna' not in response.data


def test_check_delete_incorrect_name(logged_client):
    response = logged_client.get('/team/members/delete/42')
    assert response.status_code == 403


# Тест который проверяет удаляются ли спринты
def test_check_delete_sprint(logged_client):
    response = logged_client.get('/team/sprint/delete/1')
    assert response.status_code == 302
    assert '/team/tables' in response.location

    response = logged_client.get('/team/tables')
    assert b'Oppapa' in response.data
    assert b'Ollala' not in response.data


def test_check_delete_incorrect_sprint(logged_client):
    response = logged_client.get('/team/sprint/delete/42')
    assert response.status_code == 403


def test_check_button_is_disabled_for_no_stats(logged_client, app):
    with app.app_context():
        with get_db() as sess:
            data = sess.query(Stats).all()
            for el in data:
                sess.delete(el)
            sess.add_all([
                Stats(team_id=2, sprint_name="SOMETHING", result=22),
                ])
            sess.commit()


        # conn = get_db()
        # cursor = conn.cursor()
        # cursor.execute('DELETE FROM stats') #  удаляются все строки из таблицы, заполнить внизу
        # cursor.execute('INSERT INTO stats (team_id, sprint_name, result) VALUES (2, "SOMETHING", 22)')
        # conn.commit()

    response = logged_client.get('/team/tables')
    assert response.status_code == 200
    assert b'disabled' in response.data # ЧТО? какое 'disabled', откуда взялось и почему должно быть в response.data
