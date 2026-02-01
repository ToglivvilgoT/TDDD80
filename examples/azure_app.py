from flask import Flask, request, jsonify  
from flask_sqlalchemy import SQLAlchemy
#http://www.ida.liu.se/~TDDD80
import os 
app = Flask(__name__)
if "AZURE_POSTGRESQL_CONNECTIONSTRING" in os.environ:
    conn = os.environ["AZURE_POSTGRESQL_CONNECTIONSTRING"]
    values = dict(x.split("=") for x in conn.split(' '))
    user = values['user']
    host = values['host']
    database = values['dbname']
    password = values['password']
    db_uri = f'postgresql+psycopg2://{user}:{password}@{host}/{database}'
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri 
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./our.db'
db = SQLAlchemy(app)
messages ={}

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String,unique=True)
    messages = db.relationship('Message',backref='user',lazy=True)

    def to_dict(self):
        return {'user':self.name,'uid':self.id,'messages':len(self.messages)}

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'), nullable=False)

@app.route('/user/create/<user_name>')
def create_user(user_name):
    u=User.query.filter_by(name=user_name).first()
    if u is not None:
        return jsonify({'status':'fail','message':"username taken"}),400
    u = User(name=user_name)
    db.session.add(u)
    db.session.commit()
    return jsonify({'status':'success','uid':u.id})

@app.route('/user/info/<int:uid>')
def user_info(uid):
    u=User.query.filter_by(id=uid).first()
    if u is None:
        return jsonify({'status':'fail','message':"No such user "}),400
    return jsonify(u.to_dict())

@app.route('/add_message',methods=['POST'])
def add_message():
    if request.is_json:
        data = request.get_json()
        uid = data["uid"]
        new_message = data["message"]
        u=User.query.filter_by(id=uid).first()
        if u is None:
            return jsonify({'status':'fail','message':"No such user "}),400
        m = Message(message=new_message)
        u.messages.append(m)
        db.session.add(u)
        db.session.commit()
        return jsonify({"status":"success"})
    else:
        return jsonify({"status":"Fail","message":"No json data"})

    
@app.route('/')
def hello_world():
    return "Hello World!"

def get_messages(user):
    return jsonify({"status":"success","message":messages[user]})
if __name__ == '__main__':
    app.run(debug=True)
