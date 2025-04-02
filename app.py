from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS

from config import Config
from routes.articles_routes import articles_bp

app = Flask(__name__)
CORS(app)
app.config['MONGO_URI'] = Config.MONGO_URI
mongo_db = PyMongo(app)

# Store mongo_db inside Flask config
app.config['mongo'] = mongo_db

app.register_blueprint(articles_bp)

if __name__ == '__main__':
  port = int(Config.PORT)
  app.run(host='0.0.0.0', port=port)