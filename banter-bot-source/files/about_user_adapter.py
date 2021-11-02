#libraries to implement a logic adapter
from chatterbot.logic import LogicAdapter
import re

#helper method that uses re module to replace pronouns for more grammatical accuracy 
def pronouce_processing(message):
    if 'I' in message and message[1] == " ":
        return re.sub('I', 'You', message)
    if 'My' in message and message[2] == " ":
        return re.sub('My', 'your', message)
    if "I'm" in message and message[3] == " ":
        return re.sub("I'm", "Youre", message)
    return message


"""

custom logic adapter:
this whole point of this class is to store user info (what user input)
the questions that user asks and person info about the user like (user's first name)
are two catogories of info that will be stored by this logic adapter.

"""
class AboutUserAdapter(LogicAdapter):
    
    #constructor
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.myDict = {"questions": [], "userInfo": []}

        self.userRules = ['My name is', 
        "My name's",
        'I was',
        "I'm",
        'I am', 
        'I want', 
        'I',
        'I',
        'I have',
        'I had']

        self.questionsRule =["What is", 
        "What's", 
        "How does", 
        "How", 
        "Where", 
        "When", 
        "Do", 
        "Does", 
        "What"]
    
    #overridened method to be called by the ChatBot using polymorphism.
    def can_process(self, statement):
        userText = statement.text

        if statement.text == "Tell me what you know about me.":
            return True
        else:
            if userText.endswith('?') or userText.startswith("Tell"):
                for rule in self.questionsRule:
                    match = re.search(rule, userText)
                    if match is not None:
                        correctGrammaText = pronouce_processing(userText)
                        self.myDict["questions"].append(correctGrammaText)
                        break
            else:        
                for rule in self.userRules:
                    match = re.search(rule, userText)
                    if match is not None:
                        correctGrammaText = pronouce_processing(userText)
                        self.myDict["userInfo"].append(correctGrammaText)
                        break
        return False      

    #overridened method to be called by the ChatBot using polymorphism.
    def process(self, input_statement, additional_response_selection_parameters):
        from chatterbot.conversation import Statement
        import time
        import sys
        import os

        if len(self.myDict["questions"]) == 0 and len(self.myDict["userInfo"]) == 0:
            responseStatement = Statement(text="You haven't told me anything about you. Tell me something cool about yourself")

        elif len(self.myDict["questions"]) != 0 and len(self.myDict["userInfo"]) != 0:
            text1 = ""
            for question in self.myDict["questions"]:
                text1 += str(question)
                text1 += ", "
            text2 = ""
            for info in self.myDict["userInfo"]:
                text2 += str(info)
                text2 += ", "
            responseStatement = Statement(text="You asked me: {} and you told me that: {} . Did I miss anything?".format(text1, text2))

        elif len(self.myDict["questions"]) != 0:
            text1 = ""
            for question in self.myDict["questions"]:
                text1 += str(question)
                text1 += ", "
            responseStatement = Statement(text="You asked me {} \n(You haven't told me anything about you though.)".format(text1))

        else:
            text2 = ""
            for info in self.myDict["userInfo"]:
                text2 += str(info)
                text2 += ", "
            responseStatement = Statement(text="You told me that {} \n(You haven't asked me any questions though.)".format(text2))

        responseStatement.confidence = 1
        return responseStatement