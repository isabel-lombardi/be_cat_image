from flask import json

from cat_image.main import app


def test_route_login():
    response = app.test_client().post(
        '/login',
        data=json.dumps({'username': 'admin', 'password': 'Ab123$'}),
        content_type='application/json',
    )

    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert data['status'] == "OK"
    print(response)


def test_route_login_bad_username():
    response = app.test_client().post(
        '/login',
        data=json.dumps({'username': 'abc', 'password': 'Ab123$'}),
        content_type='application/json',
    )

    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 400
    assert data['status'] == "error"
    assert data['message'] == 'Incorrect username or email'


def test_route_login_bad_password():
    response = app.test_client().post(
        '/login',
        data=json.dumps({'username': 'admin', 'password': 'abc'}),
        content_type='application/json',
    )

    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 400
    assert data['status'] == "error"
    assert data['message'] == 'Incorrect password'


def test_route_login_bad_json():
    response = app.test_client().post(
        '/login',
        data=json.dumps({'XXX': 'admin', 'YYY': 'abc'}),
        content_type='application/json',
    )

    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 400
    assert data['status'] == "error"
    assert data['message'] == 'Incorrect json'


'''def test_route_login_get():
    response = app.test_client().get(
        '/login',
        data=json.dumps({'username': 'admin', 'password': 'admin'}),
        content_type='application/json',
    )

    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 405
    assert data['status'] == "error"
    print(response)'''
