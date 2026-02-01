import requests
server="http://localhost:5000"
result = requests.get(server+"/hellowdata/Anna?age=49&last=f")
print(result.status_code)
print(result.text)

thedata={'name':'Anders', 'last':'Froberg','age':'49'}
result = requests.post(server+"/hellowjson", json=thedata)
print(result.status_code)
if result.status_code == 200:
    print(result.text)

for x in range(0,100):
    data = {"user":"Anna", "message":"This is message number " + str(x)}
    result = requests.post(server+"/api/addMessage", json=data)
    print(result.json())