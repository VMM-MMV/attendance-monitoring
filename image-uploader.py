import requests

url = 'https://api.postimages.org/upload'
files = {'file': open('fav32.png', 'rb')}
response = requests.post(url, files=files)

print(response.json())

