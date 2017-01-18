# jbotResponse.py
# JiraBot Response class
import os
from slackclient import SlackClient
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN').strip())

class JBotResponse(object):
    def __init__(self, channel=None, resp=None):
        self.msg = resp
        self.channel = channel
    
    def Send(self):
        if (self.msg):
            slack_client.api_call("chat.postMessage", channel=self.channel, text=self.msg, as_user=True)
            self.msg = None
        else:
            raise ValueError('JBotResponse.Send() was called, but response is {0}'.format(self.msg))