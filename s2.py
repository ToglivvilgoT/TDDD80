from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Table, Column, select


# global variables:
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy()
db.init_app(app)


read_messages = Table(
    "read_messages",
    db.Model.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("message_id", ForeignKey("message.id"), primary_key=True),
)


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    read_messages: Mapped[list['Message']] = relationship(
        secondary=read_messages, back_populates='read_by'
    )

    def to_json_simple(self):
        return self.id


class Message(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    message: Mapped[str] = mapped_column()
    read_by: Mapped[list[User]] = relationship(
        secondary=read_messages, back_populates='read_messages'
    )

    def to_json(self):
        return {
            'id': self.id,
            'message': self.message,
            'readBy': [user.to_json_simple() for user in self.read_by],
        }


# http status codes
HTTP_OK = 200
HTTP_BAD_REQUEST = 400
HTTP_NOT_FOUND = 404


@app.route('/users/create', methods=['POST'])
def create_user():
    user = User()
    db.session.add(user)
    db.session.commit()

    return jsonify(user.id), HTTP_OK


@app.route('/messages', methods=['POST'])
def add_message():
    message_data = request.json
    message: str = message_data['message']

    if len(message) > 140:
        return 'message too long', HTTP_BAD_REQUEST

    message = Message(message=message)
    db.session.add(message)
    db.session.commit()

    return jsonify(message.id), HTTP_OK


@app.route('/messages/<id>', methods=['GET'])
def get_message(id: int):
    message = db.session.execute(db.select(Message).filter_by(id=id)).scalar_one_or_none()
    if message is None:
        return 'id not found', HTTP_NOT_FOUND
    
    message = jsonify(message.to_json())
    
    return message, HTTP_OK


@app.route('/messages/<id>', methods=['DELETE'])
def delete_message(id: int):
    message = db.session.execute(db.select(Message).filter_by(id=id)).scalar_one_or_none()
    if message is not None:
        db.session.delete(message)
        db.session.commit()

    return '', HTTP_OK


@app.route('/messages/<message_id>/read/<user_id>', methods=['POST'])
def mark_as_read(message_id: int, user_id: int):
    user: User = db.session.execute(db.select(User).filter_by(id=user_id)).scalar_one_or_none()
    if user is None:
        return 'User not found', HTTP_NOT_FOUND

    message: Message = db.session.execute(db.select(Message).filter_by(id=message_id)).scalar_one_or_none()
    if message is None:
        return 'Message not found', HTTP_NOT_FOUND
    
    if user not in message.read_by:
        message.read_by.append(user)
        db.session.commit()

    return '', HTTP_OK


@app.route('/messages', methods=['GET'])
def get_all_messages():
    messages: list[Message] = db.session.execute(db.select(Message)).scalars()
    messages = [message.to_json() for message in messages]
    return jsonify(messages), HTTP_OK


@app.route('/messages/unread/<id>', methods=['GET'])
def get_unread(id: int):
    messages = db.session.execute(
        select(Message).where(
            ~Message.read_by.any(User.id == id)
        )
    ).scalars()
    messages = [message.to_json() for message in messages]
    return jsonify(messages), HTTP_OK


if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()
    app.run(debug=True, port=5000)
