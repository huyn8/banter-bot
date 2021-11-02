#libraries to implement a logic adapter
from chatterbot.logic import LogicAdapter

"""

custom logic adapter:
this whole point of this class is to filter out profanity

"""
class ProfanityAdapter(LogicAdapter):

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.profanityCounter = 0

    #overridened method to be called by the ChatBot using polymorphism.
    def can_process(self, statement):
        words = ['fuck', 'f*ck', 'f**k', 'fuk', 'ass', 'a$$', 'f off', 'stupid', 'dumb', 'shit', 'shiet', 'hell']
        if any(x in statement.text.split() for x in words) and self.profanityCounter < 3:
            self.profanityCounter+=1
            return True
        else:
            return False

    #overridened method to be called by the ChatBot using polymorphism.
    def process(self, input_statement, additional_response_selection_parameters):
        from chatterbot.conversation import Statement
        import time
        import sys
        import os

        if self.profanityCounter < 3:
            responseStatement = Statement(text='You: [WARNING #{}] Please do not use profanity otherwise I will be forced to terminate this chat'
            .format(self.profanityCounter))

        elif self.profanityCounter > 2:
            responseStatement = Statement(text='You have used exessive language. Terminating chat')
            sys.exit()

        responseStatement.confidence = 1

        return responseStatement
