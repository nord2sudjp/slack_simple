import time
from slackclient import SlackClient
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
token = config['slack']['SLACK_KEY']
# found at https://api.slack.com/web#authentication
sc = SlackClient(token)
if sc.rtm_connect():
        while True:
                print(sc.rtm_read())
                time.sleep(1)
else:
        print("Connection Failed, invalid token?")
