import os
import time
import re
from slackclient import SlackClient

import requests
import json
import sys
import datetime

import configparser

config = configparser.ConfigParser()
config.read('config.ini')
token = config['slack']['SLACK_KEY']

# instantiate Slack client
slack_client = SlackClient(token)
# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None

# Openweather
API_KEY = config['openweather']['API_KEY']
API_URL = config['openweather']['API_URL']


# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
EXAMPLE_COMMAND = "do"
COMMAND_LIST = ['w' , 'do']
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

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
  if raw_data.get('cod') == "404":
     return "No City Found."
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


def chk_weather(city_name):
    weather_api_url = build_url(city_name)
    raw_data = fetch_data(weather_api_url)
    
    formated_string = format_output(raw_data)
    return formated_string

def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    print(slack_events)
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            message = event["text"]
            user_id = event["user"]
            print(user_id + ":" + starterbot_id)
            if user_id == starterbot_id:
                return message, event["channel"]
    return None, None

def handle_command(command, channel):
    """
        Executes bot command if the command is known
    """
    # Default response is help text for the user
    default_response = "Not sure what you mean. Try *{}*.".format(EXAMPLE_COMMAND)

    # Finds and executes the given command, filling in response
    response = None
    # This is where you start to implement more commands!
    # if 'at' in listOfStrings :
    #    print("Yes, 'at' found in List : " , listOfStrings)


    # if command.startswith(EXAMPLE_COMMAND):
    #    response = "Sure...write some more code then I can do that!"

    response = chk_weather(command)
    
    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )


if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")
