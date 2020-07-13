# 4-Chat-Sentiment-Analysis-Service
analyze conversations form a chat messaging app

<img src="/inputs/image.jpeg">

# Overview
*Analyze conversations form a chat messaging app (like slack or whatsapp).* 
The purpose of the analysis is to extract sentiment metrics people interactions.
We are going to create an api service for this purpose. In our current case, the chat service will call our api
endpoints and it's our task to create those endpoints for:
​
- A) Store the data in a `mongodb` database
- B) Do the analysis of the data inside `mongodb`


# Project Goals

- Write an API in `flask` just to store chat messages in a mongodb database.
- Extract sentiment from chat messages and perform a report over a whole conversation
- Recommend friends to a user based on the contents from chat `documents` using a recommender system with `NLP` analysis.
- Deploy the service with docker to heroku and store messages in a cloud database.
​

`/user/create/<username>`
​
  - **Purpose:** Create a user and save into DB
  - **Params:** `username` the user name
  - **Returns:** `user_id`


**@get**
### Create username
/user/create/<username>

With this extension of the URL it is possible to add a user into the Database.

url = http://localhost:3000/user/create/`Topolino`
res = requests.get(`url`)

### Create chat
/chat/create/<chat_name> params=`user_id` 

With this extension of the URL it is possible to create a new chat room
This endpoint returns JSON files to the web localhost and allows you to add new data to the mongoDb database. 
Various if conditions will try to avoid errors (if the room already exists, if the user IDs are incorrect or already existing etc ..)

url = http://localhost:3000/chat/create/`Dumbledore’s Army`?user_id=`5f0ca75239a4fd996c03d54c`
res = requests.get(`url`)

### Add user into a chat
/chat/<conversation_id>/adduser params=`user_id` 

This endpoint allows you to add a user to a conversation.
The system will allow you this only if the user is already present in the database and is not present yet in the conversation.

url = http://localhost:3000/chat/`5f0ca76d39a4fd996c03d553`/adduser?user_id=`5f0ca75239a4fd996c03d54c`
res = requests.get(`url`)

### Insert message into a chat
/chat/<conversation_id>/addmessage params=`user_id`,`text`

This endpoint allows you to insert a new message into a conversation.
The system will allow you this only if the user is already present in the database and also in the conversation.

url = http://localhost:3000/chat/`5f0ca76d39a4fd996c03d553`/addmessage?user_id=`5f0ca75239a4fd996c03d54c`&text=`Hello world`
res = requests.get(`url`)

### Get messages list from a chat
/chat/<conversation_id>/list

This endpoint allows you to download and view the messages of a conversation through a request from the API.

url =  http://localhost:3000/chat/`5f0ca76d39a4fd996c03d553`/list
res = requests.get(`url`)

### Recommender analisys
/user/<user_id>/recommend

This endpoint allows you to perform a recommendation analysis of similar users.
Based on the topics of the chats, it is possible to identify users who may have affinities with the selected user

url =  http://localhost:3000/user/`5f0ca75239a4fd996c03d54c`/recommend
res = requests.get(`url`)

### Sentiment analisys
/chat/<conversation_id>/sentiment

This endpoint receives an Id_conversation as a parameter, returning a sentiment analysis of all chat messages.
Are the issues positive or negative in the chat?

url =  http://localhost:3000/chat/`5f0ca76d39a4fd996c03d553`/sentiment
res = requests.get(`url`)



# Knowledge

For this project I use databases in MongoDB, I make queries and geoqueries to those databases. 
Through the geographic coordinates WGS84 (lat and long) it is possible to geolocalize Markers and display them in dynamic maps created with the folium library, or in tableau.



​
* Create an API using `flask`
* Use `pymongo` insert methods
* NLTK sentiment analysis
* Docker, Heroku and Cloud databases
* Recommender systems
* MongoDB
* Import external libraries
* Pandas and Numpy libraries


# Links & Resources

​
- [https://flask.palletsprojects.com/]
- [https://www.getpostman.com/]
- [https://api.mongodb.com/python/current/api/pymongo/collection.html#pymongo.collection.Collection.insert_one]
- [https://api.mongodb.com/python/current/tutorial.html]
- [https://mermaid-js.github.io/mermaid/#/entityRelationshipDiagram]
​
*NLP & Text Sentiment Analysis:*
​
- [https://www.nltk.org/]
- [https://towardsdatascience.com/basic-binary-sentiment-analysis-using-nltk-c94ba17ae386]
- [https://www.digitalocean.com/community/tutorials/how-to-perform-sentiment-analysis-in-python-3-using-the-natural-language-toolkit-nltk]
​
*Heroku & Docker*
​
- [<https://docs.docker.com/engine/reference/builder/]>
- [<https://runnable.com/docker/python/dockerize-your-python-application]>
- [<https://devcenter.heroku.com/articles/container-registry-and-runtime]>
- [<https://devcenter.heroku.com/categories/deploying-with-docker]>
​
*Mongodb Atlas*
​
- [<https://www.mongodb.com/cloud/atlas]>

*The datasets used can be downloaded from the following links*\
https://www.kaggle.com/coolcoder22/quotes-dataset