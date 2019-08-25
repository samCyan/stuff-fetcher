from flask import Flask, g
import os
app = Flask(__name__)

if not os.path.isdir('logs'):
    os.mkdir('logs')

if not os.path.isdir('data_store'):
    os.mkdir('data_store')

if not os.path.isdir('downloads'):
    os.mkdir('downloads')

CWD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or \
    'e5ac358c-f0bf-11e5-9e39-d3b532c10a28'


# def get_db():
#     if 'db' not in g:
#         g.db = sqlite3.connect(constants.downloads_database_loc)
#     return g.db
#
# @app.teardown_appcontext
# def teardown_db():
#     db = g.pop('db', None)
#     if db is not None:
#         db.close()