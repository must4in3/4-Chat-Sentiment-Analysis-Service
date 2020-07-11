from src.app import app
from flask import request
from pymongo import MongoClient
from bson.objectid import ObjectId
from src.config import DBURL
import re


#app.config['MONGO_DBNAME'] = 'api_chat_sentiment_analysis'
client = MongoClient(DBURL)
print(f'connected to db {DBURL}')
db1 = client.get_default_database()['user']
db2 = client.get_default_database()['chatItem']


@app.route("/chat/create/<chat_name>")
def get_chat(chat_name):
    '''
    Function that allows you to create a new chat-room.
    If "users" query parameters exist, you also can populate the room. 
    The function returns JSON files to the web localhost and allows you to add new data to the mongoDb database. 
    Various if conditions will try to avoid errors (if the room already exists,
    if the user IDs are incorrect or already existing etc ..)
    '''
    print(f'Requesting to create the chat-room {chat_name}')
    res = db2.find_one({'chat_name' : chat_name,}, {'_id':0})
    if res:
        res = get_response_dict('Chat-room already exists. Please choose another one!','Error chat','information not available',res)
        return res
    # define query params and use the users_id array to check if the Ids are corrects through the function transform_strings_ObjectId() 
    users = request.args.get('users')
    users2 = transform_strings_ObjectId(users)
    # create empty room
    if not users2:
        chat_room = db2.insert_one({'chat_name' : chat_name})
        res = db2.find_one({'chat_name' : chat_name}, {'_id':0})
        res = get_response_dict('Ok','Error. users_ids doesn\'t exist in database',0,res)
        return res
    # create room with users
    chat_room = db2.insert_one({'chat_name' : chat_name, 
                               'users_ids': [user_id if db1.find_one({'_id': ObjectId(user_id)}) else None for user_id in users2]})              
    res = db2.find_one({'chat_name' : chat_name}, {'_id':0})
    # check if every users are inside the room
    if len(users) == len(users2):
        res = get_response_dict('Ok','Ok',len(users2),res)
        return res
    else:
        res = get_response_dict('Ok','Some user id did not exist in the database',len(users2),res)
        return res


def transform_strings_ObjectId(users):
    '''
    when the object_id is retrieved from the url it is in the form of a string.
    It must be transformed back into the original list.
    The ObjectId are also 24 characters long, we use this function to see if each 
    ID contains the appropriate characteristics, if not we discard it directly
    '''
    if users:
        users = ''.join(users).split(',')
        users = [''.join(re.findall('[\w*-]', user)) for user in users]
        users = [user for user in users if len(user)==24]
        users = [user_id for user_id in users if db1.find_one({'_id': ObjectId(user_id)})]
        return users
    return users


def get_response_dict(chat_status, user_status, len_users, res):
    '''
    This function contains the dictionary structure, which will be displayed 
    in localhost at the time of the reply. 
    It contains the data entered and any errors that occurred when the program was run.
    '''
    return {
        'create chat status':chat_status,
        'create users status':user_status,
        'data':res,
        'chat_users': len_users}   