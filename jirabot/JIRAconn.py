# JIRAconn.py
import json
import re
from jira import JIRA

JIRA_ENDPOINT = "*"
options = {
    'server': JIRA_ENDPOINT
    }

JIRA_CONN = JIRA(options, basic_auth=('*','*') )