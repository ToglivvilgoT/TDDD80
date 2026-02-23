from flask import Flask, request, jsonify
import uuid


# data types
MessageId = str
UserId = str


class Message:
    id: MessageId
    message: str
    read_by: set[UserId] = set()

    def __init__(self, id, message):
        self.id = id
        self.message = message

    def to_json(self):
        return {
            'id': self.id,
            'message': self.message,
            'readBy': list(self.read_by),
        }


# global variables:
app = Flask(__name__)
messages: dict[MessageId, Message] = {}

# http status codes
class HttpStatus:
    OK = 200
    CREATED = 201
    NO_CONTENT = 204
    BAD_REQUEST = 400
    NOT_FOUND = 404


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
        return 'message too long', HttpStatus.BAD_REQUEST

    id = get_new_id().hex
    messages[id] = Message(id, message)

    return id, HttpStatus.CREATED


@app.route('/messages/<id>', methods=['GET'])
def get_message(id: MessageId):
    if id not in messages:
        return 'id not found', HttpStatus.NOT_FOUND
    
    message = jsonify(messages[id].to_json())
    
    return message, HttpStatus.OK


@app.route('/messages/<id>', methods=['DELETE'])
def delete_message(id: MessageId):
    if id in messages:
        del messages[id]
        return '', HttpStatus.NO_CONTENT
    else:
        return '', HttpStatus.NOT_FOUND


# should be a put request, not post?
@app.route('/messages/<message_id>/read/<user_id>', methods=['POST']) 
def mark_as_read(message_id: MessageId, user_id: UserId):
    try:
        message = messages[message_id]
        message.read_by.add(user_id)
        return '', HttpStatus.NO_CONTENT
    except KeyError:
        return '', HttpStatus.NOT_FOUND


@app.route('/messages', methods=['GET'])
def get_all_messages():
    return jsonify([message.to_json() for message in messages.values()]), HttpStatus.OK


@app.route('/messages/unread/<id>', methods=['GET'])
def get_unread(id: UserId):
    return jsonify([message.to_json() for message in messages.values() if id not in message.read_by]), HttpStatus.OK


if __name__ == '__main__':
    app.run(debug=True, port=5000)
