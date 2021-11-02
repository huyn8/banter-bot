#libraries for implementing the chatbot
from chatterbot import ChatBot
from chatterbot.conversation import Statement
from flask import Flask, render_template, request
import chatterbot.response_selection 
from chatterbot.trainers import ChatterBotCorpusTrainer
import pathlib
import random

#using flask application 
app = Flask(__name__)

#initialzing a ChatBot instance
botName='Jarvis'
chatBot = ChatBot(botName, 
	logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch', #random banters logic adapter for random conversations and  certain specialized topics
        },
        {
            "import_path": "chatterbot.logic.MathematicalEvaluation", #logic adapter for doing math
        },
        {
            "import_path": "about_user_adapter.AboutUserAdapter", #logic adapter for storing user info
        },
        {
            "import_path": "bot_personality_adapter.BotPersonalityAdapter", #logic adapter to add more personality to the chatbot
        },
        {
            "import_path": "profanity_adapter.ProfanityAdapter", #logic adapter to preven bad words
        }
    ],
 )

#flask app stuff (for rendering)
@app.route("/")
def home():
    return render_template("index.html", botname = botName)

#flask app stuff (for front and bank-end data transfering)
@app.route("/get")
def get_bot_response():
	userInput = request.args.get('inputMessage')
	return str(chatBot.get_response(userInput))

#run the app
if __name__ == '__main__':
	app.run(port = 5500)
