from rq import Queue
from rq.job import Job
from worker import conn

from os import environ

from flask import jsonify, request

from core import app
from services import show_downloads_service, show_downloaded_chunks_service, download_file

q = Queue(connection=conn)

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
    job = q.enqueue_call(
        func=download_file, args=(url,), result_ttl=5000)
    print(job.get_id())
    return jsonify({'id': job.get_id()})


@app.route("/status/<job_key>", methods=['GET'])
def get_status(job_key):
    job = Job.fetch(job_key, connection=conn)

    if job.is_finished:
        return str(job.result), 200
    else:
        return "Nay!", 202

if __name__ == '__main__':
    port = int(environ.get('PORT', 5000))
    # app.run(host='0.0.0.0', port=port)
    app.run(debug=True)
