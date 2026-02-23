import requests

server = "http://localhost:5000"

data = {'username':"Ann", 'subject':"Read this", 'body':"This is the message"}
response = requests.post(server+"/api/user/addMessage", json=data)
print (response.status_code)
print (response.json()) 

def test_addMessage():
    data = {'username':"Ann", 'subject':"Read this", 'body':"This is the message"}
    response = requests.post(server+"/api/user/addMessage", json=data)
    assert "Message added to user" in response.json()['message']
