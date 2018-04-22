import requests
import yaml
import json

#import face.face_recog as test

#wunderground API
def get_weather(zip_code):

    with open('creds.yml', 'r') as txt:
        key = yaml.load(txt)

    key = key['wunderground']
    url = 'http://api.wunderground.com/api/{}/geolookup/forecast/conditions/q/{}.json'.format(key,zip_code)
    r = requests.get(url)
    # f = urllib2.urlopen(url)
    
    json_string = r.text
    parsed_json = json.loads(json_string)
    location = parsed_json['location']['city']

    # #next day's forecast
    forecast_prefix = parsed_json['forecast']['txt_forecast']['forecastday'][2]
    day = forecast_prefix['title']
    forecast = forecast_prefix['fcttext']

    forecast_msg = (forecast)
    return forecast_msg

#test
print(get_weather('07922'))