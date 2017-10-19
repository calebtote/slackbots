# jbotissue.py
import json
from JIRAconn import JIRA_SERVER, JIRA_CONN

class JBotIssue(object):
    def __init__(self, jiraIssueID):
        # max chars to print in summary
        self.maxSummary = 250 
        self.jiraIssueObj = JIRA_CONN.issue(jiraIssueID)
        if not self.jiraIssueObj:
            raise ValueError('jiraIssueObj: Could not locate %s' % jiraIssueID)
        else:
            if self.jiraIssueObj.fields.description: 
                self.description = self.jiraIssueObj.fields.description[0:self.maxSummary]
            else:
                self.description = "_No description._"
            self.link = "%s/browse/%s" % (JIRA_SERVER, self.jiraIssueObj)
            
            # TODO: Make more flexible
            self.format = [
                    {
                        "fallback": "%s, %s" % (self.jiraIssueObj.fields.summary, self.link),
                        "title": "[%s] %s" % (jiraIssueID.upper(), self.jiraIssueObj.fields.summary),
                        "title_link": self.link,
                        "text": self.description,
                        "color": "#7CD197",
                        "mrkdwn_in": ["text", "pretext", "fields"]
                    }
                ]