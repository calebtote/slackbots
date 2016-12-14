#torbotcmd.py

class TorbotCommand(object):
    def __init__(self, input):
        self.__input = input

        # TODO: There has to be a better way..
        try:
            self.__command_string = self.__input['text'].split(' ', 1)[1].strip().lower()
        except:
            self.__command_string = None
            pass

        try:
            self.__command = self.__command_string.split(' ', 1)[0]
        except:
            self.__command = None
            pass

        try:
            self.__text = self.__command_string.split(' ', 1)[1]
        except: 
            self.__text = None
            pass

    def getCommand(self): return self.__command
    def getText(self): return self.__text
    def getInput(self): return self.__input