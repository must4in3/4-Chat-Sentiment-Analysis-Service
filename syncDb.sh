#!/bin/bash

source .env
LOCALDBURI=$DBURL
echo "WARNING!!! REMOTE DATA WILL BE DESTROYED"
echo "Copy from $LOCALDBURI"
echo "Paste your MongoDBAtlas URI:"
read $REMOTEDBURI
echo "Sync data from $LOCALDBURI to $REMOTEDBURI"

mongodump --uri $LOCALDBURI
mongorestore --uri $REMOTEDBURI --drop
'''
LOCAL_DB="mongodb://localhost/api_chat_sentiment_analysis"
source .private.env

echo "Importing from local db: $LOCAL_DB"
echo "\t ... to remote: $REMOTE_DB"

mongodump --uri=$LOCAL_DB
mongorestore --uri=$REMOTE_DB
'''