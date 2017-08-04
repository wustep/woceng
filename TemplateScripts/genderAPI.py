import json

from urllib.request import urlopen



myKey = "emmPNzJCHxyzRbvqYv"

url = "https://gender-api.com/get?key=" + myKey + "&name=Kenneth"

response = urlopen(url)

decoded = response.read().decode('utf-8')

data = json.loads(decoded)

print( "Gender: " + data["gender"]); #Gender: male

 