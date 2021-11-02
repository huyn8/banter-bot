#libraries for training the chatbot
from app import chatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import pathlib

#training the chatbot
trainer = ChatterBotCorpusTrainer(chatBot)

#using the pre-defined english corpus to train the bot to folder "english"
trainer.train(
    str(pathlib.Path().absolute())+'/english/',
)
