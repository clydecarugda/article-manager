from celery import Celery
from pymongo import MongoClient
from bson.objectid import ObjectId

from config import Config

app = Celery('celery_app',
             broker=Config.REDIS_URI)

db_uri = Config.MONGO_URI
client = MongoClient(db_uri)

@app.task
def process_source_task(article_id, source_name, source_url, parsed):
  update_query = {
    '_id': ObjectId(article_id),
    'sources.name': source_name,
    'sources.url': source_url
  }
  
  update_data = {
    '$set': {
      'sources.$.parsed': parsed
    }
  }
  
  result = client.articles.update_one(update_query, update_data)
  
  print(result)