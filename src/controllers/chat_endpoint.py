from src.app import app
from flask import request
from pymongo import MongoClient
import json
from bson import json_util, ObjectId
from src.config import DBURL
from src.helpers.errorHelpers import errorHelper, APIError, Error404, checkValidParams
import re


client = MongoClient(DBURL)
print(f'connected to db {DBURL}')
db = client.get_default_database()


@app.route("/chat/create/<chat_name>")
@errorHelper('user_id')
def get_chat(chat_name):
    '''
    Function that allows you to create a new chat-room.
    If "users" query parameters exist, you also can populate the room. 
    The function returns JSON files to the web localhost and allows you to add new data to the mongoDb database. 
    Various if conditions will try to avoid errors (if the room already exists,
    if the user IDs are incorrect or already existing etc ..)
    '''
    print(f'Requesting to create the chat-room {chat_name}')
    res = db.chatItem.find_one({'chat_name' : chat_name,}, {'_id':0})
    if res:
        raise APIError('Chat name already exist. Change name please! :)')
    # define query params and use the users_id array to check if the Ids are corrects through the function transform_strings_ObjectId() 
    user_id = request.args.get('user_id')
    user_id_2 = transform_strings_ObjectId(user_id)
    if not user_id_2:
        raise APIError('Error. users_ids doesn\'t exist in database. It is not possible to create an empty chat')
    # create room with users
    chat_room = db.chatItem.insert_one({'chat_name' : chat_name, 
                               'users_ids': [u_id if db.user.find_one({'_id': ObjectId(u_id)}) else None for u_id in user_id_2]})              
    res = db.chatItem.find_one({'chat_name' : chat_name})
    res_ok2 = json.loads(json_util.dumps(res))
    # check if every users are inside the room
    if len(user_id.split(',')) == len(user_id_2):
        res = get_response_dict('Ok','Ok',len(user_id_2),res_ok2)
        return res
    else:
        res = get_response_dict('Ok','Some user_id did not exist in the database, or you tried insert the same id many times',len(user_id_2),res_ok2)
        return res


@app.route("/chat/<conversation_id>/adduser")
@errorHelper('user_id')
def adduser(conversation_id):
    print(f'Requesting to add users in the chat-room {conversation_id}')
    chat = db.chatItem.find_one({'_id': ObjectId(conversation_id)})
    if chat:
        user_id = request.args.get('user_id')
        user_id_2 = transform_strings_ObjectId(user_id)      
        if not user_id_2:
            raise APIError('Error. user_id doesn\'t exist in database. It is not possible to add user in this chat')
        check_usuario = db.chatItem.find_one({"_id" : ObjectId(conversation_id),'users_ids': {'$eq': ''.join(user_id_2)}}, {'_id':0})
        if not check_usuario:  
            update = db.chatItem.update({ "_id" : ObjectId(conversation_id)}, {'$addToSet': {"users_ids" : ''.join(user_id_2)}})  
            update2 = db.chatItem.find_one({"_id" : ObjectId(conversation_id)}, {'_id':0})       
            res = get_response_dict('Ok','Ok',len(user_id_2),update2)
            return update2 
        raise APIError('Error. user_id already in this chat')                  
    raise APIError('Error. chat doesn\'t exist') 


@app.route("/chat/<conversation_id>/addmessage")
@errorHelper(['user_id','text'])
def addmessage(conversation_id):
    print(f'Requesting to add a message in a chat-room {conversation_id}')
    chat = db.chatItem.find_one({'_id': ObjectId(conversation_id)})
    if chat:     
        user_id = request.args.get('user_id')
        text_add = request.args.get('text') 
        text_add_2=request.args.to_dict(text_add)
        user_id_2 = transform_strings_ObjectId(user_id)
        if not user_id_2:
            raise APIError('Error. user_id doesn\'t exist in database. It is not possible to add user in this chat')
        check_usuario = db.chatItem.find_one({"_id" : ObjectId(conversation_id),'users_ids': {'$eq': ''.join(user_id_2)}}, {'_id':0})
        username = db.user.find_one({'_id': ObjectId(user_id)})
        if check_usuario:
            update = db.chatItem.update({ "_id" : ObjectId(conversation_id)}, 
                                        {'$addToSet':{"messages" : 
                                        {'username':username['username'], 'user_id':text_add_2['user_id'], 'message':text_add_2['text']}}})
            return {
                    'conversation_id':conversation_id,
                    'messages': text_add_2
                    } 
        raise APIError('Error. user_id doesn\'t exist in this chat')
    raise APIError('Error. chat doesn\'t exist') 


@app.route("/chat/<conversation_id>/list")
@errorHelper()
def listMessage(conversation_id):
    print(f'Requesting to list all message in the chat-room {conversation_id}')
    chat = db.chatItem.find_one({'_id': ObjectId(conversation_id)})
    if chat:
        chat_json = json.loads(json_util.dumps(chat))
        return { 
                'conversation_id': chat_json['_id'],
                'chat_name': chat_json['chat_name'],
                'messages': chat_json['messages']
                }
    raise APIError('Error. chat doesn\'t exist')    


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
        users = [user_id for user_id in set(users) if db.user.find_one({'_id': ObjectId(user_id)})]
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