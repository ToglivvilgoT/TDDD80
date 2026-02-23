from flask.testing import FlaskClient
import pytest
import s4


HTTP_OK = 200
HTTP_BAD_REQUEST = 400
HTTP_UNAUTHORIZED = 401
HTTP_NOT_FOUND = 404
HTTP_METHOD_NOT_ALLOWED = 405


@pytest.fixture()
def app():
    app = s4.app
    app.config.update({
        'TESTING': True,
    })

    with app.app_context():
        s4.db.drop_all()
        s4.db.create_all()
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def create_user(client: FlaskClient, name, password):
    return client.post('/user', json={'name': name, 'password': password})


def login(client: FlaskClient, name, password):
    return client.post('/user/login', json={'name': name, 'password': password})


def create_and_login(client: FlaskClient, name='Algot', password='MyLittlePony123'):
    create_user(client, name, password)
    response = login(client, name, password)
    token = response.json['token']
    return {'Authorization':'Bearer ' + token}


def test_create_user(client: FlaskClient):
    name = 'Alice'
    response = create_user(client, name=name, password='Bob')
    assert response.status_code == HTTP_OK
    assert response.json['name'] == name


def test_add_message(client: FlaskClient):
    message = 'Hello World!'
    headers = create_and_login(client)
    response = client.post('/messages', json={'message': message}, headers=headers)
    assert response.status_code == HTTP_OK


def test_add_message_too_long(client: FlaskClient):
    message = 'Hi' * 140
    headers = create_and_login(client)
    response = client.post('/messages', json={'message': message}, headers=headers)
    assert response.status_code == HTTP_BAD_REQUEST


def test_get_message(client: FlaskClient):
    message = 'London calling to the faraway towns'
    response = client.post('/messages', json={'message': message})
    id = response.json
    response = client.get(f'/messages/{id}')
    assert response.status_code == HTTP_OK
    assert response.json['message'] == message


def test_get_non_existing_message(client: FlaskClient):
    response = client.get('/messages/873621')
    assert response.status_code == HTTP_NOT_FOUND


def test_delete_message(client: FlaskClient):
    headers = create_and_login(client)
    response = client.post('/messages', json={'message': 'hello'}, headers=headers)
    id = response.json
    response = client.delete(f'/messages/{id}', headers=headers)
    assert response.status_code == HTTP_OK
    response = client.get(f'/messages/{id}')
    assert response.status_code == HTTP_NOT_FOUND