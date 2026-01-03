from flask import Flask, request, jsonify
import uuid


# data types
MessageId = str
UserId = str


class Message:
    id: MessageId
    message: str
    read_by: list[UserId] = []


# global variables:
app = Flask(__name__)
messages: dict[MessageId, Message] = {}

# http status codes
HTTP_OK = 200
HTTP_BAD_REQUEST = 400
HTTP_NOT_FOUND = 404


def get_new_id():
    id = uuid.uuid1()
    while id in messages:
        id = uuid.uuid1()
    return id


@app.route('/messages', methods=['POST'])
def add_message():
    message_data = request.json
    message = message_data['message']

    if len(message) > 140:
        return 'message too long', HTTP_BAD_REQUEST

    id = get_new_id().bytes
    messages[id] = message

    return id, HTTP_OK


@app.route('/messages/<id>', methods=['GET'])
def get_message(id: MessageId):
    if id not in messages:
        return 'id not found', HTTP_NOT_FOUND
    
    message = jsonify(messages[id])
    
    return message, HTTP_OK
