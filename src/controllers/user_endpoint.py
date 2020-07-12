from src.app import app
from flask import request
from pymongo import MongoClient
from src.config import DBURL
from src.helpers.errorHelpers import errorHelper, APIError, Error404, checkValidParams
import json
from bson import json_util, ObjectId

client = MongoClient(DBURL)
print(f'connected to db {DBURL}')
db = client.get_database()['user']


@app.route("/user/create/<username>")
@errorHelper()
def get_user(username):
    #username = request.args.get('username') this is for query parameter
    print(f'Requesting to create the username {username}')
    res = db.find_one({'username' : username,}, {'_id':0})
    if res:
        raise APIError('Username already exists. Please choose another one!')
    user = db.insert_one({'username' : username})
    res_ok = db.find_one({'username' : username})
    res_ok2 = json.loads(json_util.dumps(res_ok))
    return {
        'status':'ok',
        'data':res_ok2}

