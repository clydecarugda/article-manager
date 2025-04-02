from celery import Celery
from celery.utils.log import get_task_logger
from pymongo import MongoClient
from bson.objectid import ObjectId

from config import Config

app = Celery('celery_app',
             broker=Config.REDIS_URI)

db_uri = Config.MONGO_URI
client = MongoClient(db_uri)
db = client.get_database()

logger = get_task_logger(__name__)

@app.task
def process_source_task(article_id, source_name, source_url, source_text, parsed):
  logger.info(f'Updating Source: {source_name} in {article_id}')
  
  update_query = {
    '_id': ObjectId(article_id),
    'sources.name': source_name,
    'sources.url': source_url,
    'sources.text': source_text
  }
  
  update_data = {
    '$set': {
      'sources.$.parsed': parsed
    }
  }
  
  result = db.articles.update_one(update_query, update_data)
  
  return result