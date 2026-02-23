from flask import Flask, request, jsonify  
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_jwt_extended import get_jwt
from flask_bcrypt import Bcrypt
#http://www.ida.liu.se/~TDDD80
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./our.db'
app.config['JWT_SECRET_KEY']="London calling to the faraway towns..."
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
db = SQLAlchemy(app)
messages ={}
JWT_blocklist = []
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String,unique=True)
    password = db.Column(db.String(200),nullable=False)
    messages = db.relationship('Message',backref='user',lazy=True)

    def __init__(self,name,password):
        self.name=name
        self.password=bcrypt.generate_password_hash(password).decode('utf-8')

    def to_dict(self):
        return {'user':self.name,'uid':self.id,'messages':len(self.messages)}

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'), nullable=False)

@app.route('/user/register/<user_name>/<password>')
def create_user(user_name,password):
    u=User.query.filter_by(name=user_name).first()
    if u is not None:
        return jsonify({'status':'fail','message':"username taken"}),400
    u = User(name=user_name,password=password)
    db.session.add(u)
    db.session.commit()
    return jsonify({'status':'success','uid':u.id})


@app.route('/user/login/<username>/<password>')
def user_login(username,password):
    u=User.query.filter_by(name=username).first()
    if u is None:
        return jsonify({'message':'No such user or wrong password','status':'fail'}),400
    if bcrypt.check_password_hash(u.password,password):
       token = create_access_token(identity=u.name)
       return jsonify({'status':'success','access_token':token})
    else:
        return jsonify({'message':'No such user or wrong password','status':'fail'}),400

@app.route('/user/logout')
@jwt_required()
def logout():
    jti = get_jwt()['jti']
    JWT_blocklist.append(jti)
    return jsonify({'message':"logged out"})

@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header,jwt_payload:dict):
    jti=  jwt_payload['jti']
    return jti in JWT_blocklist

@app.route("/")
@jwt_required()
def hello_world():
    user_name = get_jwt_identity()
    u=User.query.filter_by(name=user_name).first()
    return jsonify({'message':'Hello, ' + u.name})








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
    
@app.route('/message/<user>',methods=['GET','PUT'])
def get_messages(user):
    return jsonify({"status":"success","message":messages[user]})
if __name__ == '__main__':
    app.run(debug=True)
