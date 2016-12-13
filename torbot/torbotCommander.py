#torbotCommander.py

from mongoconn import MongoConnection

class TorbotCommander(object):   
    def __init__(self, TorbotCommandObj):
        TorbotCommander.execute[TorbotCommandObj.getCommand()](TorbotCommandObj)
    
    def TorrentRequest(TorbotCommandObj):
        print "request"
    def ListTorrents(TorbotCommandObj):
        print "list"
    def FulfillRequest(TorbotCommandObj):
        print "fulfill"
        
    execute = {
            'request': TorrentRequest,
            'list': ListTorrents,
            'fulfill': FulfillRequest
    }