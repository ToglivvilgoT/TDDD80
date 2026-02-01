from typing import Any, Callable
import requests


SERVER = 'http://localhost:5000'


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


current_test = 0
def test(
        response: requests.Response,
        expected_status_code: int | None=None,
        expected_text: str | None=None,
        expected_json: Any | None=None,
        text_predicate: Callable[[str], bool] | None=None,
        json_predicate: Callable[[Any], bool] | None=None,
        ):
    global current_test
    current_test += 1
    print(f'Running rest number {current_test}')

    if expected_status_code is not None:
        assert response.status_code == expected_status_code
    
    if expected_text is not None:
        assert response.text == expected_text

    if expected_json is not None:
        assert response.json() == expected_json

    if text_predicate is not None:
        assert text_predicate(response.text)

    if json_predicate is not None:
        assert json_predicate(response.json())

    print(f'Finished test number {current_test} without errors')

    return response


if __name__ == '__main__':
    test(requests.get(SERVER + '/wrong/url'), 404)
    test(requests.delete(SERVER + '/messages'), 405)
    MAX_MESSAGE_LENGTH = 140
    test(add_message('a' * (MAX_MESSAGE_LENGTH + 1)), 400)
    text1 = 'Hello World'
    id = 'user1'
    message1_id = test(add_message(text1), 201).text
    message2_id = test(add_message('Bye World'), 201).text
    test(get_all_messages(), 200, json_predicate=lambda messages: len(messages) == 2)
    test(get_unread(id), 200, json_predicate=lambda messages: len(messages) == 2)
    test(get_message(message1_id), 200, json_predicate=lambda msg: msg['message'] == text1)
    test(delete_message(message1_id), 204)
    test(delete_message(message1_id), 404)
    test(get_message(message1_id), 404)
    test(get_all_messages(), 200, json_predicate=lambda messages: len(messages) == 1)
    test(get_unread(id), 200, json_predicate=lambda messages: len(messages) == 1)
    test(mark_as_read(message2_id, id), 204)
    test(get_all_messages(), 200, json_predicate=lambda messages: len(messages) == 1)
    test(get_unread(id), 200, json_predicate=lambda messages: len(messages) == 0)
    print('All tests passed!')