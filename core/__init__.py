from flask import Flask, g
import os
import sqlite3
import constants

app = Flask(__name__)

if not os.path.isdir('{}/logs'.format(constants.ROOT)):
    os.mkdir('{}/logs'.format(constants.ROOT))

if not os.path.isdir('{}/data_store'.format(constants.ROOT)):
    os.mkdir('{}/data_store'.format(constants.ROOT))

if not os.path.isdir('{}/downloads'.format(constants.ROOT)):
    os.mkdir('{}/downloads'.format(constants.ROOT))


db = sqlite3.connect(constants.downloads_database_loc, check_same_thread = False)
with app.open_resource('../sql_queries/create_download_table.sql', mode='r') as f:
    db.cursor().executescript(f.read())
with app.open_resource('../sql_queries/create_download_chunk_table.sql', mode='r') as f:
    db.cursor().executescript(f.read())


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