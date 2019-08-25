import sqlite3

import constants
from dao.dao_util import insertion_by_dict, get_all, update_table_with

from core import app

class DAO_Core(object):
    db = None
    def __init__(self, db_loc):
        self.database = db_loc

    def get_db(self):
        db = getattr(self, 'db', None)
        if db is None:
            self.db = sqlite3.connect(constants.downloads_database_loc, check_same_thread = False)
        return self.db

    def commit(f):
        def _wrapper(self, *args, **kwargs):
            f(self, *args, **kwargs)
            db = self.get_db()
            with app.app_context():
                db.commit()
        return _wrapper

    def get_cursor(self):
        return self.get_db().cursor()


class Downloading_DAO(DAO_Core):
    @DAO_Core.commit
    def __init__(self):
        super(Downloading_DAO, self).__init__(constants.downloads_database_loc)
        # with app.app_context():
        db = self.get_db()
        with app.open_resource('../sql_queries/create_download_table.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        with app.open_resource('../sql_queries/create_download_chunk_table.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

    @DAO_Core.commit
    def store_downloading_info(self, **kwargs):
        return insertion_by_dict(self.get_cursor(), constants.downloads, _dict=kwargs)

    @DAO_Core.commit
    def store_downloading_chunk_info(self, **kwargs):
        return insertion_by_dict(self.get_cursor(), constants.download_chunks, _dict=kwargs)

    def all_downloads(self):
        return get_all(self.get_cursor(), constants.downloads)

    def all_chunks(self):
        return get_all(self.get_cursor(), constants.download_chunks)

    @DAO_Core.commit
    def update_download_info(self, update_dict, where_dict):
        update_table_with(self.get_cursor(), constants.downloads, update_dict, where_dict)

    @DAO_Core.commit
    def update_chunk_info(self, update_dict, where_dict):
        update_table_with(self.get_cursor(), constants.download_chunks, update_dict, where_dict)
