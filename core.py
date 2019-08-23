import logging
import threading

import requests

logging.basicConfig(filename='logs/app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')


def download_a_part(s, e, url, file_name):
    headers = {'Range': 'bytes={:d}-{:d}'.format(s, e)}
    data = requests.get(url, headers=headers, stream=True)
    with open(file_name, "rb+") as f:
        f.seek(s)
        f.write(data.content)


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
    fp = open(file_name, "wb")
    fp.write(b'\0' * file_size)
    fp.close()

    for i in range(no_of_threads):
        start = part * i
        end = start + part
        t = threading.Thread(target=download_a_part,
                             kwargs={'s': start, 'e': end, 'url': url, 'file_name': file_name})
        t.setDaemon(True)
        t.start()
    main_thread = threading.current_thread()
    # for t in threading.enumerate():
    #     if t is main_thread:
    #         continue
    #     t.join()
    logging.info('{} - downloaded successfully'.format(file_name))


if __name__ == '__main__':
    download(url='http://cdn3.whatculture.com/images/2019/01/1c764a22939897fe-600x338.jpg', file_name='ironman.jpg')
