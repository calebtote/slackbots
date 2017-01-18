#jbotCommander.py
import os
import slackutil

from jbotResponse import JBotResponse
from slackclient import SlackClient

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN').strip())

class JBotCommander(object):   
    botResponse = JBotResponse()

    def __init__(self, JBotCommandObj):
        if JBotCommandObj.getCommand() and JBotCommandObj.getCommand() in JBotCommander.execute:
            JBotCommander.execute[JBotCommandObj.getCommand()](JBotCommandObj)
        
        if not botResponse.msg:
            botResponse.msg = "Hmm, I'm not sure what you mean."    
        
    # list of available commands
    execute = {
            
    }