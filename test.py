import requests

request = requests.get('https://google.com')

print(request.text)
