#torbotcmd.py

class TorbotCommand(object):
    def __init__(self, input):
        self.__input = input
        self.__command_string = self.__input['text'].split(' ', 1)[1].strip().lower()
        try:
            self.__command = self.__command_string.split(' ', 1)[0]
            self.__text = self.__command_string.split(' ', 1)[1]
        except: pass
    def getCommand(self): return self.__command
    def getText(self): return self.__text