import logging
import os
from datetime import datetime
from queue import Queue
from uuid import uuid4
from threading import Thread
import requests

import constants
from dao.downloading_dao import Downloading_DAO

logging.basicConfig(filename=os.path.join(constants.ROOT, 'logs', 'app.log'), filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')


class DownloadWorker(Thread):
    def __init__(self, q):
        super(DownloadWorker, self).__init__()
        self.q = q
        self.dao = Downloading_DAO()

    def run(self):
        while True:
            s, e, url, file_name, download_id = self.q.get()
            try:
                headers = {'Range': 'bytes={:d}-{:d}'.format(s, e)}
                data = requests.get(url, headers=headers, stream=True)
                new_chunk = {
                    constants.DOWNLOAD_CHUNK_COLUMNS.id: download_id,
                    constants.DOWNLOAD_CHUNK_COLUMNS.downloaded_chunk_size: e - s + 1 // 1024,
                    constants.DOWNLOAD_CHUNK_COLUMNS.chunk_status: 'Downloading',
                    constants.DOWNLOAD_CHUNK_COLUMNS.chunk_timestamp: str(datetime.now()),
                }
                self.dao.store_downloading_chunk_info(**new_chunk)
                with open(os.path.join(constants.ROOT, constants.DOWNLOADS, file_name), "rb+") as f:
                    f.seek(s)
                    f.write(data.content)
                self.dao.update_chunk_info(update_dict={constants.DOWNLOAD_CHUNK_COLUMNS.chunk_status: 'Completed'}, \
                                           where_dict={constants.DOWNLOAD_CHUNK_COLUMNS.id: download_id})
            finally:
                self.q.task_done()


class Downloader(object):
    def __init__(self):
        self.dao = Downloading_DAO()

    def download(self, url, file_name=None, no_of_threads=4):
        data = requests.get(url)
        if not file_name:
            file_name = url.split('/')[-1]
        try:
            file_size = int(data.headers['content-length'])
        except:
            logging.info("Invalid URL")
            return
        with open(os.path.join(constants.ROOT, constants.DOWNLOADS, file_name), "wb") as f:
            pass
        part = int(file_size) // no_of_threads
        download_id = uuid4().hex
        new_download = {
            constants.DOWNLOADS_COLUMNS.id: download_id,
            constants.DOWNLOADS_COLUMNS.url: url,
            constants.DOWNLOADS_COLUMNS.total_file_size: file_size // 1024
        }
        self.dao.store_downloading_info(**new_download)
        # Create a queue to communicate with the worker threads
        queue = Queue()
        for i in range(no_of_threads):
            worker = DownloadWorker(queue)
            worker.daemon = True
            worker.start()
            start = 0 if i == 0 else (part * i) - 1
            end = start + part
            queue.put((start, end, url, file_name, download_id))
        worker = DownloadWorker(queue)
        worker.daemon = True
        worker.start()
        start = (part * no_of_threads) - 1
        end = file_size
        queue.put((start, end, url, file_name, download_id))
        queue.join()
        # TODO: Update download status to completed
        self.dao.update_download_info(update_dict={constants.DOWNLOADS_COLUMNS.status: 'Completed'}, \
                                      where_dict={constants.DOWNLOADS_COLUMNS.id: download_id})
        logging.info('{} - downloaded successfully'.format(file_name))
        return download_id

    def get_link_info(self, url):
        data = requests.get(url)
        print('size' + str(int(data.headers['Content-Length']) // 1024) + 'kb')


if __name__ == '__main__':
    down = Downloader()
    down.download(url='http://cdn3.whatculture.com/images/2019/01/1c764a22939897fe-600x338.jpg',
                  file_name='ironman.jpg')
    # download(url='http://www.gasl.org/refbib/Carroll__Alice_1st.pdf', file_name='alice.pdf')
    # get_link_info('http://www.gasl.org/refbib/Carroll__Alice_1st.pdf')
