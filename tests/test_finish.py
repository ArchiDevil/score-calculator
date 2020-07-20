from flaskr.db import get_db
from flaskr.schema import Stats, Member

# Входит на страницу finish
def test_check_finish(logged_client):
    response = logged_client.get('/team/finish')
    assert response.status_code == 200
    assert b'Append' in response.data


# Проверяем, что после введение коррктных данных нас перенаправляет на главную страницу
def test_check_post_finish(logged_client):
    response = logged_client.post('/team/finish',
                                  data={
                                      'real_number': 42,
                                      'name_last_sprint': 'Olla_sprint',
                                      'working_days': 10,
                                      'missing_days1': 2,
                                      'missing_days2': 3,
                                  })
    assert response.status_code == 302
    assert '/team/tables' in response.location

    response = logged_client.get('/team/tables')
    assert b'Olla_sprint' in response.data
    assert b'56' in response.data


# Проверяем, что неверные данные правильно обрабатываются
def test_check_false_post_finish(logged_client):
    error = b'The data was entered incorrectly.'
    # Ошибка 1: real_number не число, а строка
    response = logged_client.post('/team/finish',
                                  data={
                                      'real_number': 'str',
                                      'name_last_sprint': 'Olla_sprint',
                                      'working_days': '340',
                                      'missing_days1': '2',
                                      'missing_days2': '3',
                                  })
    assert response.status_code == 200
    assert error in response.data

    # Ошибка 2: working_days не число, а строка
    response = logged_client.post('/team/finish',
                                  data={
                                      'real_number': '8',
                                      'name_last_sprint': 'Olla_sprint',
                                      'working_days': 'str',
                                      'missing_days1': '2',
                                      'missing_days2': '3',
                                  })
    assert response.status_code == 200
    assert error in response.data

    # Ошибка 3: missing_days1 не число, а строка
    response = logged_client.post('/team/finish',
                                  data={
                                      'real_number': '8',
                                      'name_last_sprint': 'Olla_sprint',
                                      'working_days': '15',
                                      'missing_days1': "str",
                                      'missing_days2': '3',
                                  })
    assert response.status_code == 200
    assert error in response.data

    # Ошибка 4: missing_days2 не число, а строка
    response = logged_client.post('/team/finish',
                                  data={
                                      'real_number': '8',
                                      'name_last_sprint': 'Olla_sprint',
                                      'working_days': '340',
                                      'missing_days1': '2',
                                      'missing_days2': 'str',
                                  })
    assert response.status_code == 200
    assert error in response.data

    # Ошибка 5: рабочих дней меньше, чем пропущенных working_days < missing_days1
    response = logged_client.post('/team/finish',
                                  data={
                                      'real_number': '8',
                                      'name_last_sprint': 'Olla_sprint',
                                      'working_days': '40',
                                      'missing_days1': '340',
                                      'missing_days2': '2',
                                  })
    assert response.status_code == 200
    assert error in response.data

    # Ошибка 6.1: real_number больше нуля
    response = logged_client.post('/team/finish',
                                  data={
                                      'real_number': '0',
                                      'name_last_sprint': 'Olla_sprint',
                                      'working_days': '40',
                                      'missing_days1': '340',
                                      'missing_days2': '2',
                                  })
    assert response.status_code == 200
    assert error in response.data

    # Ошибка 6.2: real_number больше нуля
    response = logged_client.post('/team/finish',
                                  data={
                                      'real_number': '-12',
                                      'name_last_sprint': 'Olla_sprint',
                                      'working_days': '40',
                                      'missing_days1': '340',
                                      'missing_days2': '2',
                                  })
    assert response.status_code == 200
    assert error in response.data

    # Ошибка 7: working_days = 0
    response = logged_client.post('/team/finish',
                                  data={
                                      'real_number': '-12',
                                      'name_last_sprint': 'Olla_sprint',
                                      'working_days': '0',
                                      'missing_days1': '340',
                                      'missing_days2': '2',
                                  })
    assert response.status_code == 200
    assert error in response.data

    response = logged_client.post('/team/finish',
                                  data={
                                      'real_number': '42',
                                      'name_last_sprint': 'Olla_sprint',
                                      'working_days': '-20',
                                      'missing_days1': '340',
                                      'missing_days2': '2',
                                  })
    assert response.status_code == 200
    assert error in response.data

    response = logged_client.post('/team/finish',
                                  data={
                                      'real_number': '42',
                                      'name_last_sprint': 'Olla_sprint',
                                      'working_days': '20',
                                      'missing_days1': '-20',
                                      'missing_days2': '2',
                                  })
    assert response.status_code == 200
    assert error in response.data

    response = logged_client.post('/team/finish',
                                  data={
                                      'real_number': '42',
                                      'name_last_sprint': 'Olla_sprint',
                                      'working_days': '20',
                                      'missing_days1': '20',
                                      'missing_days2': '-2',
                                  })
    assert response.status_code == 200
    assert error in response.data


# Если не все данные переданы ошибка 403
def test_check_not_enough_params_finish(logged_client):
    # Not missing_days2
    response = logged_client.post('/team/finish',
                                  data={
                                      'real_number': 12,
                                      'name_last_sprint': 'Olla_sprint',
                                      'working_days': 40,
                                      'missing_days1': 3,
                                  })
    assert response.status_code == 403

    # Not missing_days1
    response = logged_client.post('/team/finish',
                                  data={
                                      'real_number': 12,
                                      'name_last_sprint': 'Olla_sprint',
                                      'working_days': 40,
                                      'missing_days2': 4,
                                  })
    assert response.status_code == 403

    # Not working_days
    response = logged_client.post('/team/finish',
                                  data={
                                      'real_number': 12,
                                      'name_last_sprint': 'Olla_sprint',
                                      'missing_days1': 3,
                                      'missing_days2': 4
                                  })
    assert response.status_code == 403

    # Not name_last_sprint
    response = logged_client.post('/team/finish',
                                  data={
                                      'real_number': 12,
                                      'working_days': 40,
                                      'missing_days1': 3,
                                      'missing_days2': 4,
                                  })
    assert response.status_code == 403

    # Not real_number
    response = logged_client.post('/team/finish',
                                  data={
                                      'name_last_sprint': 'Olla_sprint',
                                      'working_days': 40,
                                      'missing_days1': 3,
                                      'missing_days2': 4,
                                  })
    assert response.status_code == 403

    # Почти ничего нет
    response = logged_client.post('/team/finish', data={'real_number': 8})
    assert response.status_code == 403

    # Ничего нет
    response = logged_client.post('/team/finish', data={})
    assert response.status_code == 403


# проверить, что без правильного логина и пароля нельзя войти на сраницу / finish
def test_check_privacy_finish(client):
    response = client.get('/team/finish')
    assert response.status_code == 302
    assert '/team/login' in response.location


def test_check_empty_team(logged_client, app):
    with app.app_context():
        with get_db() as sess:
            data=sess.query(Member).all()
            for el in data:
                sess.delete(el)
            sess.commit()

    response = logged_client.get('/team/finish')
    assert response.status_code == 403
