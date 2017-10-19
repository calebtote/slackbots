#jbotCommander.py
import os
import slackutil
from jbotCreateIssuePrompt import JBotCreateIssuePrompt

from JIRAconn import JIRA_SERVER, JIRA_CONN
from jbotResponse import JBotResponse
from slackclient import SlackClient

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN').strip())

class JBotCommander(object):
    botResponse = None
    def __init__(self, JBotCommandObj, rtm):
        print rtm
        JBotCommander.botResponse = JBotResponse(channel=rtm[0]['channel'], th=rtm[0]['ts'], reply_as_thread=True)
        if JBotCommandObj.getCommand() and JBotCommandObj.getCommand() in JBotCommander.execute:
            JBotCommander.execute[JBotCommandObj.getCommand()](JBotCommandObj)
        
        if not JBotCommander.botResponse.msg:
            JBotCommander.botResponse.msg = "Hmm, I'm not sure what you mean."

    def CreateIssue(JBotCommandObj):
        print "create issue"
        JBotCommander.botResponse.msg = JBotCreateIssuePrompt().format
        print(JBotCommander.botResponse.Send())

    # list of available commands
    execute = {
            'create': CreateIssue
    }