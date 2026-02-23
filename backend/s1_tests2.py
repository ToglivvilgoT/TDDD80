import requests


SERVER = 'http://localhost:5000'


class HttpStatus:
    OK = 200
    CREATED = 201
    NO_CONTENT = 204
    BAD_REQUEST = 400
    NOT_FOUND = 404


def add_message(message: str):
    data = {'message': message}
    return requests.post(SERVER + '/messages', json=data)


def get_message(id: str):
    return requests.get(SERVER + f'/messages/{id}')


def delete_message(id: str):
    return requests.delete(SERVER + f'/messages/{id}')


def mark_as_read(message_id: str, user_id: str):
    return requests.post(SERVER + f'/messages/{message_id}/read/{user_id}')


def get_all_messages():
    return requests.get(SERVER + '/messages')


def get_unread(id: str):
    return requests.get(SERVER + f'/messages/unread/{id}')


def test_add_message():
    response = add_message('test')
    assert response.status_code == HttpStatus.OK or \
           response.status_code == HttpStatus.CREATED


def test_add_message_too_long():
    response = add_message('test' * 100)
    assert response.status_code == HttpStatus.BAD_REQUEST


def test_get_message():
    text = 'The message'
    response = add_message(text)
    id = response.text
    response = get_message(id)
    assert response.status_code == HttpStatus.OK
    assert response.json()['message'] == text