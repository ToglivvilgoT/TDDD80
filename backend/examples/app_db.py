from flask import Flask, request, jsonify 
from typing import List
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship 
from sqlalchemy import ForeignKey
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///demo.db"
db = SQLAlchemy()
db.init_app(app)
class User(db.Model):
    id:Mapped[int]= mapped_column(primary_key=True)
    username:Mapped[str]= mapped_column(unique=True)
    messages:Mapped[List['Message']] = relationship(back_populates="user")

class Message(db.Model):
     id:Mapped[int]= mapped_column(primary_key=True)
     subject:Mapped[str]
     body:Mapped[str]
     user_id:Mapped[int]= mapped_column(ForeignKey("user.id"))
     user:Mapped['User'] = relationship(back_populates="messages")


@app.route('/')
def hello_world():
    return "Hello, World!"
@app.route('/api/user/create/<name>')
def create_user(name):
    u = db.session.execute(db.select(User).filter_by(username=name)).scalar_one_or_none()
    if u is None:
        user = User(username=name)
        db.session.add(user)
        db.session.commit()
        return jsonify({'message':"Welcome %s you have id %d" %(user.username,user.id)})
    return jsonify({'message':"Username already taken"}) 

@app.route('/api/user/addMessage',methods=['POST'])
def addMessage():
    data = request.json
    username = data['username']
    subject = data['subject']
    body = data['body']
    u = db.session.execute(db.select(User).filter_by(username=username)).scalar_one_or_none()
    if u is None:
        return jsonify({'message':"No such user"}),404
    mess  = Message(subject=subject,body=body)
    u.messages.append(mess)
    return jsonify({'message':"Message added to user %s"% u.username})
@app.route('/api/user/all')
def get_all():
    users = db.session.execute(db.select(User)).scalars()
    listan = [x.username for x in users]
    return jsonify({'result':listan})
if __name__ == '__main__':
    app.run(debug=True)