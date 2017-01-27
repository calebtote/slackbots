# util.py
# Generic Slack Utility Functions

def parse_slack_output(slack_rtm_output, matchString):
    """
        The Slack Real Time Messaging API is an events firehose.
        This parsing function returns None unless a message contains
        the `matchString` passed in.
    """
    outputList = slack_rtm_output
    if outputList and len(outputList) > 0:
        for output in outputList:
            if output and 'text' in output and matchString in output['text']:
                # return text after the `matchString`, whitespace removed
                return output
    return None

def lookup_user_by_id(userID):
        """
        Lookup a user by the Slack UID
        """
        api_call = slack_client.api_call("users.list")
        if api_call.get('ok'):
            # retrieve all users so we can find our bot
            users = api_call.get('members')
            for user in users:
                if 'id' in user and user.get('id') == userID:
                    return user['name']
        else:
            print("could not find user with the ID " + userID)