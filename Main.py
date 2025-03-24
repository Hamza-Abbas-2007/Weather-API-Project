import requests
import json

API_KEY = 'PM66FQJM5T8WARQP2K4NH8UVM'
url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/cairo?unitGroup=metric&include=days&key={API_KEY}"
response = requests.get(url)
print(response.status_code)
jsonData = response.json()

info = jsonData["days"][0]
temp = info["temp"]
print(temp) 