from os import environ
from uuid import uuid4

from flask import jsonify, request

import constants
from core import app, download_helper
from dao.downloading_dao import Downloading_DAO
from services import show_downloads_service, store_downloading_info_service, show_downloaded_chunks_service, download_file


@app.route('/')
def hello():
    return jsonify('hello')

@app.route('/show-downloads')
def show_downloads():
    return jsonify(show_downloads_service())

@app.route('/show-downloaded-chunks')
def show_downloaded_chunks():
    return jsonify(show_downloaded_chunks_service())

@app.route('/download')
def download_route():
    url = request.args.get('url')
    d_id = download_file(url)
    return jsonify({'id':d_id})


if __name__ == '__main__':
    port = int(environ.get('PORT', 5000))
    # app.run(host='0.0.0.0', port=port)
    app.run(debug=True)
