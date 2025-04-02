from celery import Celery
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Celery('celery_app',
             broker='redis://localhost:6379/0')

db_uri = 'mongodb://localhost:27017/'
client = MongoClient(db_uri)
database = client.get_database('test')

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
  
  result = database.articles.update_one(update_query, update_data)
  
  print(result)