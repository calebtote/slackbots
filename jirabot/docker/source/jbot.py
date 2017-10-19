import os, schedule, sys, time, traceback

# custom modules
import slackutil

from jbotScanner import JBotScanner
from jbotcmd import JBotCommand
from jbotCommander import JBotCommander
from jbotScheduled import RetrieveUpcomingMaintenances
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

        # enable via: schedule.run_pending()
        schedule.every(1).hours.do(RetrieveUpcomingMaintenances)

        while True:
            # run all pending scheduled jobs
            #schedule.run_pending()

            rtm = slack_client.rtm_read()
            botMessage = slackutil.parse_slack_output(rtm, botMention)
            try:
                if botMessage:
                    botCommand = JBotCommand(botMessage)
                    print str(JBotCommander(botCommand, rtm))
                else:
                    JBotScanner(rtm)
            except:
                    print traceback.format_exc()
                    pass

            # we don't want to spam the firehose
            time.sleep(0.3)
    else:
        print("rtm_connect() failed. Invalid Slack token or bot ID?")