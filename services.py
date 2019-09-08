from dao.downloading_dao import Downloading_DAO

from core import download_helper

d_dao = Downloading_DAO()

def download_file(url):
    return download_helper.Downloader().download(url)

def show_downloads_service():
    return d_dao.all_downloads()

def show_downloaded_chunks_service():
    return d_dao.all_chunks()

def store_downloading_info_service(new_download):
    d_dao.store_downloading_info(**new_download)