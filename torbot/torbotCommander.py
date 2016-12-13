#torbotCommander.py
import os

from mongoconn import MongoConnection
from slackclient import SlackClient

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN').strip())

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

class TorbotCommander(object):   
    botResponse = None

    def __init__(self, TorbotCommandObj):
        TorbotCommander.botResponse = None
        if TorbotCommandObj.getCommand():
            TorbotCommander.execute[TorbotCommandObj.getCommand()](TorbotCommandObj)
        
        if not TorbotCommander.botResponse:
            TorbotCommander.botResponse = "Hmm, I'm not sure what you mean."

        # send response
        slack_client.api_call("chat.postMessage", channel=TorbotCommandObj.getInput()['channel'],
                          text=TorbotCommander.botResponse, as_user=True)
    
    def TorrentRequest(TorbotCommandObj):
        print "request"
        titleRequest = TorbotCommandObj.getText().title()
        if not TorbotCommandObj.getText(): 
            TorbotCommander.botResponse = "I think you a word.."
            return
        mongodb = MongoConnection("torbot", "requests")
        if mongodb.mongoconn.find_one({ "request" : titleRequest}):
            TorbotCommander.botResponse = "`%s` has already been requested. \nUse `list` to see pending requests." % titleRequest
        else:
            dbresult = mongodb.mongoconn.insert_one(
                {
                    "requestor": lookup_user_by_id(TorbotCommandObj.getInput()['user']),
                    "request": titleRequest
                }
            )
            if dbresult:
                TorbotCommander.botResponse = "Request added: `%s`" % titleRequest
            else:
                TorbotCommander.botResponse = "Something went wrong..."

    def ListTorrents(TorbotCommandObj):
        print "list"
        TorbotCommander.botResponse = "_Current pending requests:_\n"
        mongodb = MongoConnection("torbot", "requests")
        for document in mongodb.mongoconn.find():
            TorbotCommander.botResponse = TorbotCommander.botResponse + "`[%s]`\n" % document['request']

    def FulfillRequest(TorbotCommandObj):
        print "fulfill"
        fulfillTitle = TorbotCommandObj.getText().title()
        mongodb = MongoConnection("torbot", "requests")
        requestor = mongodb.mongoconn.find_one({ "request" : fulfillTitle})['requestor']
        dbresult = mongodb.mongoconn.delete_one({ "request" : fulfillTitle })
        if dbresult.deleted_count > 0:
            TorbotCommander.botResponse = "Hey <@%s>! `[%s]` was just marked as fulfilled by <@%s>." % \
                (requestor, 
                fulfillTitle, 
                lookup_user_by_id(TorbotCommandObj.getInput()['user']))


        
    # list of available commands
    execute = {
            'request': TorrentRequest,
            'list': ListTorrents,
            'fulfill': FulfillRequest
    }