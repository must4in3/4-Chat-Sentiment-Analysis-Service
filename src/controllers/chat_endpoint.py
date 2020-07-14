from src.db_mongo import client, db
from src.app import app
from flask import request
import json
from bson import json_util, ObjectId
from src.helpers.errorHelpers import errorHelper, APIError, Error404, checkValidParams
import re


@app.route("/chat/create/<chat_name>")
@errorHelper('user_id')
def get_chat(chat_name):
    '''
    Function that allows you to create a new chat-room.
    If "users" query parameters exist, you also can populate the room. 
    '''
    print(f'Requesting to create the chat-room {chat_name}')
    res = db.chatItem.find_one({'chat_name' : chat_name,}, {'_id':0})
    if res:
        raise APIError('Chat name already exist. Change name please! :)')
    # define query params and use the users_id array to check if the Ids are corrects 
    user_id = transform_strings_ObjectId(request.args.get('user_id'))
    if not user_id:
        raise APIError('Error. users_ids doesn\'t exist in database. It is not possible to create an empty chat')
    # create room with users
    db.chatItem.insert({'chat_name' : chat_name, 
                        'users_ids': [u_id if db.user.find_one({'_id': ObjectId(u_id)}) else None for u_id in user_id]})              
    res = db.chatItem.find_one({'chat_name' : chat_name})
    return json.loads(json_util.dumps(res))


@app.route("/chat/<conversation_id>/adduser")
@errorHelper('user_id')
def adduser(conversation_id):
    '''
    This function allows you to add a user to a conversation. 3 errors are reported.
    '''
    print(f'Requesting to add users in the chat-room {conversation_id}')
    chat = db.chatItem.find_one({'_id': ObjectId(conversation_id)})
    if len(list(chat)) > 0:
        user_id = request.args.get('user_id')  
        if not user_id:
            raise APIError('Error. user_id doesn\'t exist in database.')
        if not db.chatItem.find_one({"_id" : ObjectId(conversation_id),'users_ids': {'$eq': user_id}}, {'_id':0}):
            db.chatItem.update({ "_id" : ObjectId(conversation_id)}, {'$addToSet': {"users_ids" : ''.join(user_id)}})  
            return db.chatItem.find_one({"_id" : ObjectId(conversation_id)}, {'_id':0})       
        raise APIError('Error. user_id already in this chat')                  
    raise APIError('Error. chat doesn\'t exist') 


@app.route("/chat/<conversation_id>/addmessage")
@errorHelper(['user_id','text'])
def addmessage(conversation_id):
    '''
    This function allows you to add a new message in a conversation. 3 errors are reported.
    '''
    print(f'Requesting to add a message in a chat-room {conversation_id}')
    if db.chatItem.find_one({'_id': ObjectId(conversation_id)}):   
        user_id = request.args.get('user_id')
        text_add = request.args.get('text')
        if not user_id:
            raise APIError('Error. user_id doesn\'t exist in database.')
        check_usuario = db.chatItem.find_one({"_id" : ObjectId(conversation_id),'users_ids': {'$eq': f'{user_id}'}})
        username = db.user.find_one({'_id': ObjectId(user_id)})
        if check_usuario:
            db.chatItem.update({ "_id" : ObjectId(conversation_id)}, 
                                {'$addToSet':{"messages" : 
                                {'username':username['username'], 
                                'user_id':user_id, 
                                'message':text_add}}})
            return {
                    'conversation_id':conversation_id,
                    'messages': text_add
                    } 
        raise APIError('Error. user_id doesn\'t exist in this chat')
    raise APIError('Error. chat doesn\'t exist') 


@app.route("/chat/<conversation_id>/list")
@errorHelper()
def listMessage(conversation_id):
    '''
    This function allows you to download and view the messages of a conversation through a request from the API
    '''
    print(f'Requesting to list all message in the chat-room {conversation_id}')
    chat = db.chatItem.find_one({'_id': ObjectId(conversation_id)})
    if chat:
        try:
            chat_json = json.loads(json_util.dumps(chat))
            return { 
                    'conversation_id': chat_json['_id'],
                    'chat_name': chat_json['chat_name'],
                    'messages': chat_json['messages']
                    }
        except:
            raise Error404('List empty')
    raise APIError('Error. chat doesn\'t exist')    


import ast
def transform_strings_ObjectId(users):
    '''
    when the object_id is retrieved from the url it is in the form of a string.
    It must be transformed back into the original list.
    The ObjectId are also 24 characters long, we use this function to see if each 
    ID contains the appropriate characteristics, if not we discard it directly
    '''
    if users:
        users = re.findall(r"\'\w*\'", users)
        users = [user[1:-1] for user in users if len(user[1:-1])==24]
        users = [user_id for user_id in set(users) if db.user.find_one({'_id': ObjectId(user_id)})]
        return users
    return users