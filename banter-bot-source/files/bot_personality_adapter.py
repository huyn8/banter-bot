#libraries to implement a logic adapter
from chatterbot.logic import LogicAdapter
import re
import random

"""

custom logic adapter:
this whole point of this class is to make the chatbot appear to have more
of a personality by replying to certain phrases in a certain ways without giving
an actual answer. 

"""
class BotPersonalityAdapter(LogicAdapter):

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.newResponse = ""
        self.rules = {'Do you think (.*)': ['if {0}? Absolutely.', 'No chance'], 
        'Do you remember (.*)': ['Did you think I would forget {0}', "Why haven't you been able to forget {0}", 'What about {0}', 'Yes .. and?'], 
        'I want (.*)': ['What would it mean if you got {0}', 'Why do you want {0}', "What's stopping you from getting {0}"], 
        'What if (.*)': ["Do you really think it's likely that {0}", 'Do you wish that {0}', 'What do you think about {0}', 'Really--if {0}']}

    #overridened method to be called by the ChatBot using polymorphism.
    def can_process(self, statement):
        response, phrase = "default", None
        
        #find a pattern that matches with statement and find the approproriate response in return using regex
        for pattern, responses in self.rules.items():
            match = re.search(pattern, statement.text)
            if match is not None:
                response = random.choice(responses)
                if '{0}' in response:
                    phrase = match.group(1)
        self.newResponse = response.format(phrase)

        #using re module to replace pronouns for more grammatical accuracy 
        if self.newResponse != "default":
            message = self.newResponse
            if 'my' or 'My' in message:
                self.newResponse = re.sub('my', 'your', message)
            if 'your' in message:
                self.newResponse = re.sub('your', 'my', message)
            if 'you' in message:
                self.newResponse = re.sub('you', 'I', message)
            if 'I' in message:
                self.newResponse = re.sub('I', 'You', message)
            return True

        return False

    #overridened method to be called by the ChatBot using polymorphism.
    def process(self, input_statement, additional_response_selection_parameters):
        from chatterbot.conversation import Statement
        import time
        import sys
        import os

        responseStatement = Statement(text=self.newResponse)
        responseStatement.confidence = 1
        return responseStatement
