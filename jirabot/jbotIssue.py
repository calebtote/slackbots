# jbotissue.py
from JIRAconn import JIRA_ENDPOINT, JIRA_CONN

class JBotIssue(object):
    def __init__(self, jiraIssueID):
        # max chars to print in summary
        self.maxSummary = 250 
        self.jiraIssueObj = JIRA_CONN.issue(jiraIssueID)
        if not self.jiraIssueObj:
            raise ValueError('jiraIssueObj: Could not locate %s' % jiraIssueID)
        else:
            self.link = "%s/browse/%s" % (JIRA_ENDPOINT, self.jiraIssueObj)
            self.format = {
                "attachments": [
                    {
                        "fallback": "%s, %s" % (self.jiraIssueObj.fields.summary, self.link),
                        "pretext": "Detail summary for %s" % self.jiraIssueObj,
                        "title": self.jiraIssueObj.fields.summary,
                        "title_link": self.link,
                        "text": self.jiraIssueObj.fields.description[0:self.maxSummary],
                        #"color": "#7CD197",
                        "mrkdwn_in": ["text", "pretext", "fields"]
                    }
                ]
            }
            