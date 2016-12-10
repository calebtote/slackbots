import os
import time
from slackclient import SlackClient
from pymongo import MongoClient

client = MongoClient()
db = client.torbot

# starterbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "request"

# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))


def handle_command(input):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    command = input['text'].split(AT_BOT)[1].strip().lower()
    user = lookup_user_by_id(input['user'])
    response = ''

    if command.startswith(EXAMPLE_COMMAND):
        response = "Got your request " + user + ": `" + command + \
        "`\nUnfortunately, I'm still a babybot and don't know how to handle it."

        dbresult = db.requests.insert_one(
            {
                "requestor": user,
                "request": command.split(' ',1)[1]
            }
        )
    elif command.startswith('list'):
        response = "Current pending requests:\n"
        for document in db.requests.find():
            response = response + "`" + document['request'] + "`\n"
    else: 
        response = "Not sure what you mean " + user + ".. but I'm pretty new, so this shouldn't surprise anyone."

    slack_client.api_call("chat.postMessage", channel=input['channel'],
                          text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        This parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
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

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            command = parse_slack_output(slack_client.rtm_read())
            if command:
                handle_command(command)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")