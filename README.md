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

<code> /user/create/<username>`<code>
​
  - **Purpose:** Create a user and save into DB
  - **Params:** `username` the user name
  - **Returns:** `user_id`


@get
/user/create/<username>


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