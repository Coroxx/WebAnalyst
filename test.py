import requests

request = requests.get('https://github.com/sindresorhus/awesome')

print(request.text)
