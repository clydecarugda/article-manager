from flask import Blueprint, jsonify, request, current_app
from bson.objectid import ObjectId

from celery_app import process_source_task

articles_bp = Blueprint('articles_bp', __name__)

@articles_bp.route('/articles', methods=['POST'])
def create_article():
  try:
    mongo_db = current_app.config['mongo']
    
    data = request.get_json()
    
    title = data.get('title')
    description = data.get('description')
    tags = data.get('tags')
    
    if not title or not description:
      return jsonify({'error': "The 'Title' and 'Description' fields are required!"}), 400
    
    articles_doc = {
      "title": title,
      "description": description,
      "tags": tags
    }
    
    result = mongo_db.db.articles.insert_one(articles_doc)
    
    articles_doc['_id'] = str(result.inserted_id)
    
    return jsonify(articles_doc), 201
    
  except Exception as e:
    current_app.logger.error(e)
    return jsonify({'error', 'An unexpected error occured while creating the article'}), 500
  
@articles_bp.route('/articles/<string:article_id>/sources', methods=['PATCH'])
def insert_article_sources(article_id):
  try:
    mongo_db = current_app.config['mongo']
    
    data = request.get_json()
    
    name = data.get('name')
    url = data.get('url')
    text = data.get('text')
    parsed = False # Defaults to false
    
    if not name or not url or not text:
      return jsonify({'error': "The 'Name', 'URL', and text source fields are required!"}), 400
    
    source = {
      'name': name,
      'url': url,
      'text': text,
      'parsed': parsed
    }
    
    update_query = {
      '_id': ObjectId(article_id)
    }
    
    update_data = {
      '$push': {
        'sources': source
      }
    }
    
    # Insert source to article
    result = mongo_db.db.articles.update_one(update_query, update_data)
    
    # Check if any modifications was done
    if result.modified_count == 0:
      return jsonify({'error': f"Article id '{ObjectId(article_id)}' does not exist!"}), 404
    
    # Trigger Celery to run update task in the background
    celery_task = process_source_task.delay(article_id, name, url, text, True)
    # celery_task = process_source_task.apply_async((article_id, name, url, True), countdown=10)
    
    return jsonify(source), 201

  except Exception as e:
    current_app.logger.error(e)
    return jsonify({'error', 'An unexpected error occured while creating the article source'}), 500
  
@articles_bp.route('/articles', methods=['GET'])
def get_articles():
  try:
    mongo_db = current_app.config['mongo']
    
    articles = list(mongo_db.db.articles.find({}))
    
    return jsonify(articles)
    
  except Exception as e:
    current_app.logger.error(e)
    return jsonify({'error': 'An error occured while fetching the data!'}), 500
  
@articles_bp.route('/articles/<string:article_id>', methods=['GET'])
def get_article(article_id):
  try:
    mongo_db = current_app.config['mongo']
    
    article = mongo_db.db.articles.find_one({'_id': ObjectId(article_id)})
    
    if not article:
      return jsonify({'error': 'Unable to fetch data!'}), 404
    
    return jsonify(article)
    
  except Exception as e:
    current_app.logger.error(e)
    return jsonify({'error': 'An error occured while fetching the data!'}), 500
  
@articles_bp.route('/articles/<string:article_id>', methods=['PATCH'])
def update_article(article_id):
  try:
    mongo_db = current_app.config['mongo']
    
    data = request.get_json()
    update_data = {}
    
    query_selector = {'_id': ObjectId(article_id)}
    
    title = data.get('title')
    description = data.get('description')
    tags = data.get('tags')
    sources = data.get('sources')
    parsed = data.get('parsed')
    
    if not title or not sources:
      return jsonify({'error': "The 'Title' and 'Sources' field are required!"}), 400
    
    update_data = {
      '$set': {
        'title': title,
        'description': description,
        'tags': tags,
        'sources': sources,
        'parsed': parsed
      }
    }
    
    result = mongo_db.db.articles.update_one(query_selector, update_data)
    
    if result.matched_count == 0:
      return jsonify({'error': 'Failed to update article'}), 404
    
    return jsonify({'message': 'Article updated successfully!'}), 200
    
  except Exception as e:
    current_app.logger.error(e)
    return jsonify({'error': 'An error occured while fetching the data!'}), 500
  
@articles_bp.route('/articles/<string:article_id>', methods=['DELETE'])
def delete_article(article_id):
  try:
    mongo_db = current_app.config['mongo']
    
    result = mongo_db.db.articles.delete_one({'_id': ObjectId(article_id)})
    
    if result.deleted_count == 0:
      return jsonify({'error': 'Invalid Article. No data deleted!'}), 404
    
    return jsonify({'message': 'Article Deleted'}), 200
  
  except Exception as e:
    current_app.logger.error(e)
    return jsonify({'error': 'An unexpected error occured.'}), 500