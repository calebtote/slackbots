#torbotCommander.py
import os
import slackutil
import re
import json

from jbotResponse import JBotResponse
from jbotIssue import JBotIssue
from slackclient import SlackClient

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN').strip())

class JBotScanner(object):   
    patternsToMatch = [ 'GOSOPS-' ]

    def __init__(self, input):
        if input:
            self.input = input
            for line in self.validate(): 
                self.parse(line)

    def parse(self, line):
        for pattern in JBotScanner.patternsToMatch:
            patternMatch = re.findall(r'\b(?:%s)\d*\b' % pattern.lower(), line['text'].lower(), re.IGNORECASE)
            if patternMatch:
                botResponse = JBotResponse(line['channel'], None, line['ts'])

                for pMatch in patternMatch:
                    botResponse.msg = "%s" % json.dumps(JBotIssue(pMatch).format, indent=4)
                    botResponse.Send()

    def validate(self):
        validLines = []
        if self.input and len(self.input) > 0:
            for line in self.input:
                if line and line['type'] == 'message' and 'user' in line and \
                line['user'] != os.environ.get("BOT_ID").strip() and 'thread_ts' not in line:
                    validLines.append(line)
        return validLines