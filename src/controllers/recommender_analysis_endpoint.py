from src.app import app
from flask import request
from pymongo import MongoClient
import json
import pandas as pd
import numpy as np
from bson import json_util, ObjectId
from src.helpers.errorHelpers import errorHelper, APIError, Error404, checkValidParams
from src.config import DBURL
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity as distance


client = MongoClient(DBURL)
print(f'connected to db {DBURL}')
db = client.get_default_database()

@app.route("/user/<user_id>/recommend")
@errorHelper()
def recommenderAnalysis(user_id):
    print(f'Requesting by {user_id} for a recommendation of users with similar characteristics')
    user = db.chatItem.find({'users_ids' : {'$eq': user_id}})
    if len(list(user)) != 0:
        chat = db.chatItem.find({'_id': {'$ne': None}})
        chat_json = json.loads(json_util.dumps(chat))
        chat_mess = dict()
        count = 0
        for conversation in chat_json:
            for message in conversation.items():
                for mess in message[1]:
                    try:
                        chat_mess[f'{count}']= {'username': mess['username'], 'message' : mess['message']}
                        count += 1
                    except:
                        pass
        matrix = createMatrixSimilarity(chat_mess, user_id)
        user = matrix[:1].to_dict()
        reccom_user = matrix[1:6].to_dict()
        return {'Me':user, 'Recommended users' : reccom_user}
    raise APIError('The user is not present in any chat')
    


def createMatrixSimilarity(dictionary_chat_mess, user_id):
    # create pandas df
    df_quote = pd.DataFrame(dictionary_chat_mess)
    # dataframe aggregated with all users with the phrases said in every chat
    df_quote = df_quote.T.groupby('username').agg({'message':'sum'})
    # the same information but in a dictionary
    new_dict = dict()
    for i in range(len(df_quote['message'])):
        new_dict[df_quote.T.columns[i]] =  df_quote['message'][i]
    # create a sparse_matrix with the count of every word
    count_vectorizer = CountVectorizer()
    sparse_matrix = count_vectorizer.fit_transform(new_dict.values())
    m = sparse_matrix.todense()
    # Compute Cosine Similarity matrix (or selected distance) en put it in a dataframe
    doc_term_matrix = sparse_matrix.todense()
    df = pd.DataFrame(doc_term_matrix, 
                  columns=count_vectorizer.get_feature_names(), 
                  index=new_dict.keys())
    similarity_matrix = distance(df,df)
    # Similarity dataframe and Similarity heatmap 
    sim_df = pd.DataFrame(similarity_matrix, columns=new_dict.keys(), index=new_dict.keys())
    #print(sim_df)     #<------ display df
    #sns.heatmap(sim_df,annot=True) <------ heatmap
    #np.fill_diagonal(sim_df.values, 0) # Remove diagonal max values and set those to 0
    #matrix =  sorted(sim_df[f'{user_id}'].items(), key=lambda x: x[1], reverse=True)
    # find username that made the request
    username = db.user.find_one({'_id': ObjectId(user_id)})
    similarity_column = sim_df[f'{username["username"]}'].sort_values(ascending=False)
    return similarity_column

