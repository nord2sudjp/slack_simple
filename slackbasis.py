from slackclient import SlackClient

import configparser

config = configparser.ConfigParser()
config.read('config.ini')
token = config['slack']['SLACK_KEY']
sc = SlackClient(token)
sc.api_call("api.test")
sc.api_call("channels.info", channel="CCMHXC6J1")
sc.api_call(
        "chat.postMessage", channel="#starterbot-test", text="Hello from Python! :tada:",
        username='pybot', icon_emoji=':robot_face:'
)
