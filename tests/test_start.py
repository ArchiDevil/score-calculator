# проверить, что без правильного логина и пароля нельзя войти на сраницу / start
from flaskr.db import get_db
from flaskr.schema import Stats, Member


def test_check_privacy_start(client):
    response = client.get('/team/start')
    assert response.status_code == 302
    assert '/team/login' in response.location


# Входит на страницу start
def test_check_start(logged_client):
    response = logged_client.get('/team/start')
    assert response.status_code == 200
    assert b'Anna' in response.data
    assert b'Alisa' in response.data


# Проверяем, что после введение коррeктных данных появляется зеленая табличка
def test_check_green_table(logged_client, app):
    # Для того чтобы корректно посчитался startнадо подать хотя бы один finish
    with app.app_context():
        with get_db() as sess:
            data=sess.query(Stats).all()
            for el in data:
                sess.delete(el)
            sess.add_all([
                Stats(team_id=1, sprint_name="Olla_sprint", result=420),
            ])
            sess.commit()

    response = logged_client.post('/team/start',
                                  data={
                                      'workdays': '14',
                                      'missing_days1': '0',
                                      'missing_days2': '0',
                                  })

    assert response.status_code == 200
    assert b'Calculate number of points for the next sprint' in response.data
    assert b'420' in response.data


# Здесь тоже все должно работать как обычно, лишние аргументы missing отсекаются просто
def test_check_members_not_equal_to_data_elements(logged_client, app):
    # Для того чтобы корректно посчитался start надо подать хотя бы один finish
    with app.app_context():
        with get_db() as sess:
            data=sess.query(Stats).all()
            for el in data:
                sess.delete(el)
            sess.add_all([
                Stats(team_id=1, sprint_name="Olla_sprint", result=420),
            ])
            sess.commit()

    response = logged_client.post('/team/start',
                                  data={
                                      'workdays': '15',
                                      'missing_days1': '0',
                                      'missing_days2': '0',
                                      'missing_days3': '2'
                                  })
    assert response.status_code == 200
    assert b'Calculate number of points for the next sprint' in response.data
    assert b'420' in response.data


# Проверяем, что неверные данные правильно обрабатываются
def test_check_false_post_start(logged_client):
    error = b'The data was entered incorrectly.'
    # 1 ошибка: workdays - строка, а не число
    response = logged_client.post('/team/start',
                                  data={
                                      'workdays': "str",
                                      'missing_days1': '5',
                                      'missing_days2': '2',
                                  })
    assert response.status_code == 200
    assert error in response.data

    # 2 ошибка: 'missing_days1' - строка, а не число
    response = logged_client.post('/team/start',
                                  data={
                                      'workdays': '340',
                                      'missing_days1': "str",
                                      'missing_days2': '2',
                                  })
    assert response.status_code == 200
    assert error in response.data

    # 3 ошибка: 'missing_days2' - строка, а не число
    response = logged_client.post('/team/start',
                                  data={
                                      'workdays': '340',
                                      'missing_days1': '5',
                                      'missing_days2': "str",
                                  })
    assert response.status_code == 200
    assert error in response.data

    # 4 ошибка: missing_days больше чем рабочих дней - workdays
    response = logged_client.post('/team/start',
                                  data={
                                      'workdays': '15',
                                      'missing_days1': '45',
                                      'missing_days2': '2',
                                  })
    assert response.status_code == 200
    assert error in response.data

    # 5 ошибка: workdays не может быть 0
    response = logged_client.post('/team/start',
                                  data={
                                      'workdays': '0',
                                      'missing_days1': '0',
                                      'missing_days2': '0',
                                  })
    assert response.status_code == 200
    assert error in response.data

    response = logged_client.post('/team/start',
                                  data={
                                      'workdays': '15',
                                      'missing_days1': '-1',
                                      'missing_days2': '2',
                                  })
    assert response.status_code == 200
    assert error in response.data

    response = logged_client.post('/team/start',
                                  data={
                                      'workdays': '-15',
                                      'missing_days1': '0',
                                      'missing_days2': '0',
                                  })
    assert response.status_code == 200
    assert error in response.data


# Если не все данные переданы - ошибка 403
def test_check_not_enough_params_start(logged_client):
    response = logged_client.post('/team/start',
                                  data={
                                      'workdays': '7',
                                  })
    assert response.status_code == 403

    response = logged_client.post('/team/start',
                                   data={
                                      'workdays': '8',
                                     'missing_days1': '0',
                                  })
    assert response.status_code == 403

    response = logged_client.post('/team/start',
                                  data={
                                      'missing_days1': '0',
                                      'missing_days2': '0',
                                  })
    assert response.status_code == 403

    response = logged_client.post('/team/start',
                                  data={
                                      'workdays': '4',
                                      'missing_days2': '2',
                                  })
    assert response.status_code == 403

    response = logged_client.post('/team/start', data={})
    assert response.status_code == 403


def test_db_is_alive_after_second_request(logged_client):
    response = logged_client.get('/team/start')
    assert response.status_code == 200

    response = logged_client.get('/team/start')
    assert response.status_code == 200


def test_see_empty_results(logged_client, app):
    with app.app_context():
        with get_db() as sess:
            data=sess.query(Stats).all()
            for el in data:
                sess.delete(el)
            sess.add_all([Stats(team_id=2, sprint_name="SPRINT", result=42)])
            sess.commit()

    response = logged_client.get('/team/start')
    assert response.status_code == 403 # no stats available


def test_post_empty_results(logged_client, app):
    with app.app_context():
        with get_db() as sess:
            data=sess.query(Stats).all()
            for el in data:
                sess.delete(el)
            sess.add_all([Stats(team_id=2, sprint_name="SPRINT", result=42)])
            sess.commit()

    response = logged_client.post('/team/start',
                                  data={
                                      'workdays': '14',
                                      'missing_days1': '2',
                                      'missing_days2': '0',
                                  })
    assert response.status_code == 403 # no stats available

def test_many_sprints(logged_client, app):
    with app.app_context():
        with get_db() as sess:
            data=sess.query(Stats).all()
            for el in data:
                sess.delete(el)
            for _ in range(0, 4):
                sess.add_all([Stats(team_id=1, sprint_name="s1", result=81)])
            for _ in range(0, 4):
                sess.add_all([Stats(team_id=1, sprint_name="s1", result=420)])
            sess.commit()

    response = logged_client.post('/team/start',
                                  data={
                                      'workdays': '8',
                                      'missing_days1': '0',
                                      'missing_days2': '0',
                                  })
    assert response.status_code == 200
    assert b'420' in response.data


def test_check_empty_team(logged_client, app):
    with app.app_context():
        with get_db() as sess:
            data=sess.query(Stats).all()
            for el in data:
                sess.delete(el)
            sess.commit()

    response = logged_client.get('/team/start')
    assert response.status_code == 403

    response = logged_client.post('/team/start',
                                 data={
                                     'workdays': '8'
                                 })
    assert response.status_code == 403

# Тест который проверяет, что в не зависимости от корректности данных кнопки некуда не пропадают
def test_check_button(logged_client):
    response = logged_client.get('/team/start')
    assert response.status_code == 200
    assert b'Calculate' in response.data
    assert b'Cancel' in response.data

    #после введения корректных данных кнопки не пропадают
    response = logged_client.post('/team/start',
                                data={
                                    'workdays': '14',
                                    'missing_days1': '0',
                                    'missing_days2': '0',
                                })
    assert response.status_code == 200
    assert b'Calculate' in response.data
    assert b'Cancel' in response.data

    #после введения некорректных данных кнопки не пропадают
    response = logged_client.post('/team/start',
                                data={
                                    'workdays': '14',
                                    'missing_days1': '0',
                                    'missing_days2': '56',
                                })
    assert response.status_code == 200
    assert b'Calculate' in response.data
    assert b'Cancel' in response.data
