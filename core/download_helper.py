import logging
import threading
from datetime import datetime
from uuid import uuid4

import requests

import constants
from dao.downloading_dao import Downloading_DAO

logging.basicConfig(filename='logs/app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

d_dao = Downloading_DAO()

def download_a_part(s, e, url, file_name, download_id):
    headers = {'Range': 'bytes={:d}-{:d}'.format(s, e)}
    data = requests.get(url, headers=headers, stream=True)

    new_chunk = {
        constants.DOWNLOAD_CHUNK_COLUMNS.id: download_id,
        constants.DOWNLOAD_CHUNK_COLUMNS.downloaded_chunk_size: e-s+1//1024,
        constants.DOWNLOAD_CHUNK_COLUMNS.chunk_status: 'Downloading',
        constants.DOWNLOAD_CHUNK_COLUMNS.chunk_timestamp: str(datetime.now()),
    }
    d_dao.store_downloading_chunk_info(**new_chunk)
    with open(file_name, "rb+") as f:
        f.seek(s)
        f.write(data.content)
    d_dao.update_chunk_info(update_dict = {constants.DOWNLOAD_CHUNK_COLUMNS.chunk_status: 'Completed'}, \
                      where_dict = {constants.DOWNLOAD_CHUNK_COLUMNS.id: download_id})


def download(url, file_name=None, no_of_threads=4):
    data = requests.get(url)
    if not file_name:
        file_name = url.split('/')[-1]
    try:
        file_size = int(data.headers['content-length'])
    except:
        logging.info("Invalid URL")
        return
    part = int(file_size) // no_of_threads
    download_id = uuid4().hex
    new_download = {
        constants.DOWNLOADS_COLUMNS.id: download_id,
        constants.DOWNLOADS_COLUMNS.url: url,
        constants.DOWNLOADS_COLUMNS.total_file_size:file_size//1024
    }
    d_dao.store_downloading_info(**new_download)

    for i in range(no_of_threads):
        start = part * i
        end = start + part
        t = threading.Thread(target=download_a_part,
                             kwargs={'s': start, 'e': end, 'url': url, 'file_name': file_name, 'download_id':download_id})
        t.setDaemon(True)
        t.start()

    #TODO: Update download status to completed
    d_dao.update_download_info(update_dict={constants.DOWNLOADS_COLUMNS.status: 'Completed'}, \
                               where_dict={constants.DOWNLOADS_COLUMNS.id: download_id})

    logging.info('{} - downloaded successfully'.format(file_name))
    return download_id

def get_link_info(url):
    data = requests.get(url)
    print('size' + str(int(data.headers['Content-Length'])//1024) + 'kb')

if __name__ == '__main__':
    # download(url='http://cdn3.whatculture.com/images/2019/01/1c764a22939897fe-600x338.jpg', file_name='ironman.jpg')
    download(url='http://www.gasl.org/refbib/Carroll__Alice_1st.pdf', file_name='alice.pdf')
    get_link_info('http://www.gasl.org/refbib/Carroll__Alice_1st.pdf')
