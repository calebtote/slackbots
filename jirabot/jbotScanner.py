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
    patternsToMatch = [ * ]

    def __init__(self, input):
        if input:
            self.input = input
            self.parse()

    def parse(self):
        if self.input and len(self.input) > 0:
            for line in self.input:
                if line and line['type'] == 'message' and ('user' in line) and (line['user'] != os.environ.get("BOT_ID").strip()):
                    for pattern in JBotScanner.patternsToMatch:
                        patternMatch = re.findall(r'\b(?:%s)\d*\b' % pattern.lower(), line['text'].lower(), re.IGNORECASE)
                        if patternMatch:
                            print line['ts']
                            botResponse = JBotResponse(line['channel'], None, line['ts'])

                            # eventually expand to recognize multiple mentions
                            botResponse.msg = "%s" % json.dumps(JBotIssue(patternMatch[0]).format, indent=4)
                            botResponse.Send()