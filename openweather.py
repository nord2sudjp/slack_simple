import requests
import json
import sys
import datetime
import configparser

API_KEY=''
API_URL=''

def time_converter(time):
    converted_time = datetime.datetime.fromtimestamp(
        int(time)
    ).strftime('%I:%M %p')
    return converted_time

def build_url(city_name):
  # build URL
  weather_api_url = API_URL.format(city = city_name, key = API_KEY)
  # print(url)
  return weather_api_url
  
def fetch_data(weather_api_url):
  response = requests.get(weather_api_url)
  raw_data = json.loads(response.text)
  return raw_data

def format_output(raw_data):
  main = raw_data.get('main')
  sys = raw_data.get('sys')

  data = dict(
    city=raw_data.get('name'),
    country=sys.get('country'),
    temp=main.get('temp'),
    temp_max=main.get('temp_max'),
    temp_min=main.get('temp_min'),
    humidity=main.get('humidity'),
    pressure=main.get('pressure'),
    sky=raw_data['weather'][0]['main'],
    sunrise=time_converter(sys.get('sunrise')),
    sunset=time_converter(sys.get('sunset')),
    wind=raw_data.get('wind').get('speed'),
    wind_deg=raw_data.get('deg'),
    dt=time_converter(raw_data.get('dt')),
    cloudiness=raw_data.get('clouds').get('all')
  )
  data['m_symbol'] = '\xb0' + 'C'
  s = '''---------------------------------------
  Current weather in: {city}, {country}:
  {temp}{m_symbol} {sky}
  Max: {temp_max}, Min: {temp_min}

  Wind Speed: {wind}, Degree: {wind_deg}
  Humidity: {humidity}
  Cloud: {cloudiness}
  Pressure: {pressure}
  Sunrise at: {sunrise}
  Sunset at: {sunset}

  Last update from the server: {dt}
  ---------------------------------------'''

  return s.format(**data)

if __name__ == '__main__':
  # load config
  config = configparser.ConfigParser()
  config.read('config.ini')
  API_KEY = config['openweather']['API_KEY']
  API_URL = config['openweather']['API_URL']
  try:
    city_name = sys.argv[1]
    weather_api_url = build_url(city_name)
    raw_data = fetch_data(weather_api_url)
    formated_string = format_output(raw_data)
    print(formated_string)

  except IOError:
     print('no internet')
