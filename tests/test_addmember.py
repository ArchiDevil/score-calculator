ERROR = b'Make sure that you have entered both fields correctly.'

# проверить, что без правильного логина и пароля нельзя войти на сраницу /addmember
def test_check_privacy_addmember(client):
    response = client.get('/team/addmember')
    assert response.status_code == 302
    assert '/team/login' in response.location


def test_check_addmembers(logged_client):
    response = logged_client.get('/team/addmember')
    assert response.status_code == 200


def test_check_post(logged_client):
    response = logged_client.post('/team/addmember',
                                  data={
                                      'username': 'Banya',
                                      'userfactor': '0.7',
                                  })
    assert response.status_code == 302
    assert '/team/tables' in response.location

    response = logged_client.get('/team/tables')
    assert b'0.7' in response.data
    assert b'Banya' in response.data


def test_check_false_post(logged_client):
    response = logged_client.post('/team/addmember',
                                  data={
                                      'username': 'Sara',
                                      'userfactor': '1.7',
                                  })
    assert response.status_code == 200
    assert ERROR in response.data

    response = logged_client.post('/team/addmember',
                                  data={
                                      'username': 'Sara',
                                      'userfactor': '-0.7',
                                  })
    assert response.status_code == 200
    assert ERROR in response.data

    response = logged_client.post('/team/addmember',
                                  data={
                                      'username': 'Sara',
                                      'userfactor': '1,7',
                                  })
    assert response.status_code == 200
    assert ERROR in response.data

    response = logged_client.post('/team/addmember',
                                  data={
                                      'username': 'Sara',
                                      'userfactor': '0,7',
                                  })
    assert response.status_code == 200
    assert ERROR in response.data

    response = logged_client.post('/team/addmember',
                                  data={
                                      'username': 'Sara',
                                      'userfactor': '0.0',
                                  })
    assert response.status_code == 200
    assert ERROR in response.data

    response = logged_client.post('/team/addmember',
                                  data={
                                      'username': 'Sara',
                                      'userfactor': '',
                                  })
    assert response.status_code == 200
    assert ERROR in response.data

    response = logged_client.post('/team/addmember',
                                  data={
                                      'username': '',
                                      'userfactor': '0.8',
                                  })
    assert response.status_code == 200
    assert ERROR in response.data


def test_check_not_enough_params(logged_client):
    response = logged_client.post('/team/addmember',
                                  data={'username': 'Sara'})
    assert response.status_code == 403

    response = logged_client.post('/team/addmember',
                                  data={'userfactor': '1,7'})
    assert response.status_code == 403

    response = logged_client.post('/team/addmember',
                                  data={})
    assert response.status_code == 403
