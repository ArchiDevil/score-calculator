def test_check_login(client):
    response = client.get('/team/login')
    assert response.status_code == 200


# Проверяет, что после входа пользователя перебрасывает на главную страницу
def test_check_ent(client):
    response = client.post('/team/login',
                           data={
                               'userlogin': 'LOGIN',
                               'userpassword': 'PASSWORD',
                           })
    assert response.status_code == 302
    assert '/team/tables' in response.location


# Проверить, что когда вводится неправильный логин или пароль, входа не происходит
def test_wrong_login_password(client):
    response = client.post('/team/login',
                           data={
                               'userlogin': 'LOG',
                               'userpassword': 'PASSWORD',
                           })
    assert response.status_code == 200
    assert b'Incorrect login or password' in response.data

    response = client.post('/team/login',
                           data={
                               'userlogin': 'LOGIN',
                               'userpassword': 'PASS',
                           })
    assert response.status_code == 200
    assert b'Incorrect login or password' in response.data

    response = client.post('/team/login',
                           data={
                               'userlogin': 'LOG',
                               'userpassword': 'PASS',
                           })
    assert response.status_code == 200
    assert b'Incorrect login or password' in response.data


# проверяет все поля заполнены
def test_check_not_login_password(client):
    response = client.post('/team/login', data={'userlogin': 'LOGIN'})
    assert response.status_code == 403

    response = client.post('/team/login', data={'userpassword': 'PASSWORD'})
    assert response.status_code == 403

    response = client.post('/team/login', data={})
    assert response.status_code == 403
