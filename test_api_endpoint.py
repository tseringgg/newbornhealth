import requests

url = 'http://127.0.0.1:5000/ask'
#data = {'question': 'What are birth injuries?'}
data = {'question': 'What is the most common cause of birth injuries?'}
response = requests.post(url, json=data)
print(response.json())