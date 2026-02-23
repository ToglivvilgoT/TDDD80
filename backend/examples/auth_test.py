import requests
base_url="http://127.0.0.1:5000"
first = requests.get(base_url)
print (first.text)
second = requests.get(base_url+"/user/login/anders/nisse")
print (second.text)
token = second.json()['access_token']
print(token)
first = requests.get(base_url, headers={'Authorization':'Bearer '+token})
print(first.text)

third = requests.get(base_url+"/user/logout", 
headers={'Authorization':'Bearer '+token})
print (third.text)

first = requests.get(base_url,
headers={'Authorization':'Bearer '+token})
print(first.text)

