import os, sys, time, traceback

# custom modules
from torbotcmd import TorbotCommand
from torbotCommander import TorbotCommander, lookup_user_by_id

from slackclient import SlackClient
from pymongo import MongoClient

def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        This parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    bot_mention = "<@" + os.environ.get("BOT_ID").strip() + ">"
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            print output
            if output and 'text' in output and bot_mention in output['text']:
                # return text after the @ mention, whitespace removed
                return output
    return None

if __name__ == "__main__":
    if not os.environ.get('SLACK_BOT_TOKEN'):
        print("$SLACK_BOT_TOKEN env variable not set. Exiting.")
        sys.exit(1)

    # instantiate Slack & Twilio clients
    slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN').strip())

    if slack_client.rtm_connect():
        print("Torbot connected...")
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
            # we don't want to spam the firehose'
            time.sleep(1)
    else:
        print("rtm_connect() failed. Invalid Slack token or bot ID?")