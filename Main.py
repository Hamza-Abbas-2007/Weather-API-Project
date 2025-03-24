import requests

API_KEY = 'PM66FQJM5T8WARQP2K4NH8UVM'
url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/cairo?unitGroup=metric&include=days&key={API_KEY}"
response = requests.get(url)
print(response.status_code)