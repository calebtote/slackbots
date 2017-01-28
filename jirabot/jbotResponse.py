# jbotResponse.py
# JiraBot Response class
import json
import os
from slackclient import SlackClient
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN').strip())

class JBotResponse(object):
    def __init__(self, channel=None, resp=None, th=None):
        self.msg = resp
        self.channelID = channel
        if self.channelID:
            if slack_client.api_call("channels.info", channel=self.channelID)['ok']:  # public channel
                self.channelName = slack_client.api_call("channels.info", channel=self.channelID)['channel']['name']
            else: # private channel
                self.channelName = slack_client.api_call("groups.info", channel=self.channelID)['group']['name']
        self.thread = th
    
    # TODO: Make more generic external
    def Send(self):
        if (self.msg):
            print "\n\tSending response to channel: %s ...\n" % self.channelName
            print self.msg

            # TODO: Remove implicit thread reply - should be dynamic
            retVal = slack_client.api_call("chat.postMessage", channel=self.channelID, thread_ts=self.thread, attachments=self.msg, as_user=True)
            self.msg = None
            return retVal
        else:
            raise ValueError('JBotResponse.Send() was called, but response is {0}'.format(self.msg))