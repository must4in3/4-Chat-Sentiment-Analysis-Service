from pymongo import MongoClient
from src.config import DBURL

client = MongoClient(DBURL)
print(f'connected to db {DBURL}')
db = client.get_database()