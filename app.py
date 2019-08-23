from os import environ
from uuid import uuid4

from flask import Flask, jsonify, request

from core import download

app = Flask(__name__)

status = {
}


@app.route('/')
def hello():
    return jsonify('hello')


@app.route('/download')
def download_route():
    url = request.args.get('url')
    download(url)
    return jsonify({url: uuid4().hex})


if __name__ == '__main__':
    port = int(environ.get('PORT', 5000))
    # app.run(host='0.0.0.0', port=port)
    app.run(debug=True)
