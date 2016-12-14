import os
import time
import traceback

# custom modules
from torbotcmd import TorbotCommand
from torbotCommander import TorbotCommander, lookup_user_by_id

from slackclient import SlackClient
from pymongo import MongoClient

# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN').strip())
AT_BOT = "<@" + os.environ.get("BOT_ID").strip() + ">"

def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        This parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            print output
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output

    return None

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            bot_message = parse_slack_output(slack_client.rtm_read())
            if bot_message:
                print bot_message
                try:
                    bot_command = TorbotCommand(bot_message)
                    print str(TorbotCommander(bot_command))
                except:
                    
                    errRespond = "Hey <@%s>! The following almost killed me!\n `[%s]` \n*Stack Trace:* \n ```%s```\
                    :rotating_light: Please file a bug here: https://github.com/calebtote/slackbots/issues :rotating_light: \n" % (lookup_user_by_id(bot_message['user']), bot_message, traceback.format_exc())
                    slack_client.api_call("chat.postMessage", channel=bot_message['channel'],
                          text=errRespond, as_user=True)
                    pass
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print slack_client.rtm_connect()
        print("Connection failed. Invalid Slack token or bot ID?")