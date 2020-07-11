from flask import Flask, request

app=Flask(__name__)

@app.route('/a')
def saluda():
    return 'hola'


### L1. User endpoints
# - (GET) `/user/create/<username>`





### L1. Chat endpoints
#- (GET) `/chat/create`
# (GET) `/chat/<conversation_id>/adduser`
# - (POST) `/chat/<conversation_id>/addmessage`
#- (GET) `/chat/<conversation_id>/list`