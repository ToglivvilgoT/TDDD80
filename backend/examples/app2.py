from flask import Flask, request,jsonify


app = Flask(__name__)

data = {}
@app.route('/api/addMessage',methods=['POST'])
def addMessgae():
    resd= request.json
    user = resd['user']
    message = resd['message']
    if user not in data:
        data[user]=[]
    data[user].append(message)
    return jsonify ({'result':"Added message to " + user}),200
@app.route('/api/readMssages', methods=['POST'])
def getAllJson():
    resd= request.json
    user = resd['user']
    if user not in data:
        return jsonify({'result':"No such user"}),400
    return jsonify({'messages':data[user]}),200

@app.route('/api/readMssages/<user>', methods=['GET'])
def getAll(user):
    if user not in data:
        return jsonify({'result':"No such user"}),400
    return jsonify({'messages':data[user]}),200

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/hello/<name>')
def hello_you(name):
    return 'Hello,' + name

@app.route('/hellowdata/<name>')
def hello_with_data(name):
    #/hello/Anders?last=FrÃ¶berg&age=49 
    age = request.args['age']
    last = request.args['last']
    return 'Hello,' + name + " "+last + " you are " + age + "  years old"

@app.route('/hellowjson', methods=['GET','POST'])
def get_data_with_json():
    mydata = request.json
    name = mydata['name']
    last = mydata['last']
    age = mydata['age']
    return 'Hello,' + name + " "+last + " you are " + age + "  years old"





if __name__ == '__main__':
    app.run(debug=True,port=5000)
