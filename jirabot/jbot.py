import os, sys, time, traceback

# custom modules
import slackutil

from jbotScanner import JBotScanner
from jbotcmd import JBotCommand
from jbotCommander import JBotCommander
# ----------
from slackclient import SlackClient

if __name__ == "__main__":
    if not os.environ.get('SLACK_BOT_TOKEN'):
        print("$SLACK_BOT_TOKEN env variable not set. Exiting.")
        sys.exit(1)

    # Instantiate Slack & Twilio clients
    slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN').strip())

    if slack_client.rtm_connect():
        print("JiraBot connected...")
        botMention = "<@" + os.environ.get("BOT_ID").strip() + ">"
        while True:
            rtm = slack_client.rtm_read()
            botMessage = slackutil.parse_slack_output(rtm, botMention)
            #try:
            if botMessage:
                botCommand = JBotCommand(botMessage)
                print str(JBotCommander(botCommand))
            else:
                print str(JBotScanner(rtm))
            """except:
                    errRespond = "Hey <@%s>! The following almost killed me!\n `[%s]` \n*Stack Trace:* \n ```%s```\
                    :rotating_light: Please file a bug here: https://github.com/calebtote/slackbots/issues :rotating_light: \n" \
                    % (slackutil.lookup_user_by_id(botMessage['user']), botMessage, traceback.format_exc())
                    slack_client.api_call("chat.postMessage", channel=botMessage['channel'],
                          text=errRespond, as_user=True)
                    pass"""

            # we don't want to spam the firehose'
            time.sleep(1)
    else:
        print("rtm_connect() failed. Invalid Slack token or bot ID?")