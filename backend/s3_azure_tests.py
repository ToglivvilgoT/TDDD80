import requests


HTTP_OK = 200
HTTP_BAD_REQUEST = 400
HTTP_NOT_FOUND = 404
HTTP_METHOD_NOT_ALLOWED = 405


SERVER = 'https://tddd80-labs3-viljo690-2026-a0fmhhhyd5g7dmch.northeurope-01.azurewebsites.net'


def test_create_user():
    response = requests.post(SERVER + '/users/create')
    assert response.status_code == HTTP_OK


def test_add_message():
    message = 'Hello World!'
    response = requests.post(SERVER + '/messages', json={'message': message})
    assert response.status_code == HTTP_OK


def test_add_message_too_long():
    message = 'Hi' * 140
    response = requests.post(SERVER + '/messages', json={'message': message})
    assert response.status_code == HTTP_BAD_REQUEST


def test_get_message():
    message = 'London calling to the faraway towns'
    response = requests.post(SERVER + '/messages', json={'message': message})
    id = response.json()
    response = requests.get(SERVER + f'/messages/{id}')
    assert response.status_code == HTTP_OK
    assert response.json()['message'] == message


def test_get_non_existing_message():
    response = requests.get(SERVER + '/messages/873621')
    assert response.status_code == HTTP_NOT_FOUND


def test_delete_message():
    response = requests.post(SERVER + '/messages', json={'message': 'hello'})
    id = response.json()
    response = requests.delete(f'{SERVER}/messages/{id}')
    assert response.status_code == HTTP_OK
    response = requests.get(SERVER + f'/messages/{id}')
    assert response.status_code == HTTP_NOT_FOUND