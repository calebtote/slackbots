import os, sys, subprocess
from slackclient import SlackClient

BOT_NAME = 'torbot'

# sys.argv[1] should be the SlackBot API Token
slack_client = SlackClient(sys.argv[1])

if __name__ == "__main__":
    api_call = slack_client.api_call("users.list")
    if api_call.get('ok'):
        # retrieve all users so we can find our bot
        users = api_call.get('members')
        for user in users:
            if 'name' in user and user.get('name') == BOT_NAME:
                print user.get('id')