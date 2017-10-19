# jbotScheduled.py

import os, json
from JIRAconn import JIRA_SERVER, JIRA_CONN
from jbotIssue import JBotIssue
from jbotResponse import JBotResponse
from slackclient import SlackClient
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN').strip())

# TODO: Work in progress. 
#       Entire project needs refactored a bit before we can properly clean this up.
def RetrieveUpcomingMaintenances():
    upcomingMaintenances = JIRA_CONN.search_issues(\
        'project in ("GOS Production Maintenance") AND \
        type = "Request Maintenance" AND \
        status not in (Closed, "Request Cancelled") AND \
        "Maintenance Date" is not EMPTY \
        ORDER BY "Maintenance Date" DESC, updated DESC', maxResults=10)
    
    testChannel = 'C3XTQF2J3'
    testText = ':rotating_light: Upcoming Maintenances :rotating_light:'
    retVal = slack_client.api_call("chat.postMessage", channel=testChannel, text=testText, as_user=True)
    botResponse = JBotResponse(retVal['channel'], None, retVal['ts'])

    for m in upcomingMaintenances:
        botResponse.msg = "%s" % json.dumps(JBotIssue(m.key).format, indent=4)
        botResponse.Send()