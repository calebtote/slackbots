#torbotCommander.py
import os
import slackutil

from jbotResponse import JBotResponse
from slackclient import SlackClient

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN').strip())

class JBotScanner(object):   
    patternsToMatch = [ 'GOSOPS-', 'GOSRM-' ]

    def __init__(self, input):
        print input
        if input:
            self.input = input
            self.parse()

    def parse(self):
        if self.input and len(self.input) > 0:
            for line in self.input:
                if line and line['type'] == 'message' and (line['user'] != os.environ.get("BOT_ID").strip()):
                    for pattern in JBotScanner.patternsToMatch:
                        if pattern.lower() in line['text'].lower():
                            botResponse = JBotResponse(line['channel'])
                            botResponse.msg = "Matched: `%s`" % pattern
                            botResponse.Send()