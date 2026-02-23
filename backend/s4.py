import datetime
import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Table, Column, select
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
from dotenv_vault import load_dotenv


# global variables:
app = Flask(__name__)

if "AZURE_POSTGRESQL_CONNECTIONSTRING" in os.environ:
    conn = os.environ["AZURE_POSTGRESQL_CONNECTIONSTRING"]
    values = dict(x.split("=") for x in conn.split(' '))
    user = values['user']
    host = values['host']
    database = values['dbname']
    password = values['password']
    db_uri = f'postgresql+psycopg2://{user}:{password}@{host}/{database}'
    debug_flag = False
elif __name__ == '__main__': # deploy locally
    db_path = os.path.join(os.path.dirname(__file__), 'database.db')
    db_uri = f'sqlite:///{db_path}'
    debug_flag = True
else: # deploy for testing
    db_path = os.path.join(os.path.dirname(__file__), 'testDatabase.db')
    db_uri = f'sqlite:///{db_path}'
    debug_flag = True

app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy()
db.init_app(app)


load_dotenv()
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(hours=1)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)


read_messages = Table(
    "read_messages",
    db.Model.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("message_id", ForeignKey("message.id"), primary_key=True),
)


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    read_messages: Mapped[list['Message']] = relationship(
        secondary=read_messages, back_populates='read_by'
    )

    def __init__(self, name, password):
        self.name = name
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def to_json(self):
        return {'id': self.id, 'name': self.name}


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
            'readBy': [user.to_json() for user in self.read_by],
        }


class JWTBlocked(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    jit: Mapped[str] = mapped_column(nullable=False)

    def __init__(self, jit):
        self.jit = jit


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload:dict):
    jti = jwt_payload['jti']
    return db.session.execute(select(JWTBlocked).filter_by(jti=jti)).scalar_one_or_none() is not None


# http status codes
HTTP_OK = 200
HTTP_BAD_REQUEST = 400
HTTP_NOT_FOUND = 404


@app.route('/user', methods=['POST'])
def create_user():
    json = request.json
    try:
        name = json['name']
        password = json['password']
    except (AttributeError, TypeError):
        return '', HTTP_BAD_REQUEST

    if db.session.execute(select(User).filter_by(name=name)).scalar_one_or_none() is not None:
        return 'Name already taken', 400

    user = User(name, password)
    db.session.add(user)
    db.session.commit()

    return jsonify(user.to_json()), HTTP_OK


@app.route('/user/login', methods=['POST'])
def login():
    json = request.json
    try:
        name = json['name']
        password = json['password']
    except (AttributeError, TypeError):
        return jsonify(''), HTTP_BAD_REQUEST

    user = db.session.execute(select(User).filter_by(name=name)).scalar_one_or_none()
    if user is None:
        return jsonify('user not found'), 404

    if not bcrypt.check_password_hash(user.password, password):
        return jsonify('wrong password'), 400

    return jsonify({'token': create_access_token(name)}), 200


@app.route('/user/logout', methods=['POST'])
@jwt_required
def logout():
    jti = get_jwt_identity()
    block = JWTBlocked(jti)
    db.session.add(block)
    db.session.commit()
    return jsonify('Logout successful'), 200


@jwt_required
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


@jwt_required
@app.route('/messages/<id>', methods=['DELETE'])
def delete_message(id: int):
    message = db.session.execute(db.select(Message).filter_by(id=id)).scalar_one_or_none()
    if message is not None:
        db.session.delete(message)
        db.session.commit()

    return '', HTTP_OK


@jwt_required
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


@jwt_required
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
    app.run(debug=debug_flag, port=5000)
