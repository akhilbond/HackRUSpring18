import requests
import yaml
import json

#import face.face_recog as test

#wunderground API
def get_weather():

    with open('creds.yml', 'r') as txt:
        key = yaml.load(txt)

    key = key['wunderground']
    url = 'http://api.wunderground.com/api/{}/hourly/forecast/q/NY/NewYork.json'.format(key)
    r = requests.get(url)
    
    json_string = r.text
    parsed_json = json.loads(json_string)

    forecast_prefix = parsed_json['forecast']['txt_forecast']['forecastday'][2]
    forecast = str(forecast_prefix['fcttext_metric']).split(".")
    forecast_msg = (forecast)
    return forecast_msg

#test
print(get_weather())