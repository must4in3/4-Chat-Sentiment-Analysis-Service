from src.app import app
from flask import request
from pymongo import MongoClient
import json
from bson import json_util, ObjectId
from src.config import DBURL
from src.helpers.errorHelpers import errorHelper, APIError, Error404, checkValidParams
#nltk libraries and modules
from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('vader_lexicon')
nltk.download('averaged_perceptron_tagger')

client = MongoClient(DBURL)
print(f'connected to db {DBURL}')
db = client.get_default_database()


@app.route("/chat/<conversation_id>/sentiment")
@errorHelper()
def sentimentAnalysis(conversation_id):
    '''
    This function receives an Id_conversation as a parameter, returning a sentiment analysis of all chat messages
    '''
    print(f'Requesting to a sentiment analysis from the chat-room {conversation_id}')
    chat = db.chatItem.find_one({'_id': ObjectId(conversation_id)})
    if chat:
        chat_json = json.loads(json_util.dumps(chat))
        chat_mess = []
        for message in chat_json.items():
            for mess in message[1]:
                try:
                    chat_mess.append(mess['message'])
                except:
                    pass
        pol = polarityBySentence(chat_mess)
        return json.dumps(pol)
    raise APIError('Error. chat doesn\'t exist')   


def polarityBySentence(phrases_list):
    '''
    This function performs a part of the sentimentAnalysis function process.
    In particular, it carries out the process of dividing sentences into shorter sentences and carrying out a polarity analysis
    '''
    sid = SentimentIntensityAnalyzer()
    pol = []
    for phrase in phrases_list:
        tokenized_text=sent_tokenize(phrase)
        print(tokenized_text)
        for sentence in tokenized_text:
            scores = sid.polarity_scores(sentence)
            pol.append({'sentence': sentence, 'sentiment': scores})
    return pol