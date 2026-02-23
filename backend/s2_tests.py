from flask.testing import FlaskClient
import pytest
import s2


HTTP_OK = 200
HTTP_BAD_REQUEST = 400
HTTP_NOT_FOUND = 404
HTTP_METHOD_NOT_ALLOWED = 405


@pytest.fixture()
def app():
    app = s2.app
    app.config.update({
        'TESTING': True,
    })

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def test_create_user(client: FlaskClient):
    response = client.post('/users/create')
    assert response.status_code == HTTP_OK


def test_add_message(client: FlaskClient):
    message = 'Hello World!'
    response = client.post('/messages', json={'message': message})
    assert response.status_code == HTTP_OK


def test_add_message_too_long(client: FlaskClient):
    message = 'Hi' * 140
    response = client.post('/messages', json={'message': message})
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
    response = client.post('/messages', json={'message': 'hello'})
    id = response.json
    response = client.delete(f'/messages/{id}')
    assert response.status_code == HTTP_OK
    response = client.get(f'/messages/{id}')
    assert response.status_code == HTTP_NOT_FOUND