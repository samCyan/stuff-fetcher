# db list
downloads_database = 'downloads_database'

# db loc list
downloads_database_loc = './data_store/downloads_database.db'

# tables list
downloads = 'DOWNLOADS'
download_chunks = 'DOWNLOAD_CHUNKS'

# Column names
class DOWNLOADS_COLUMNS:
    id = 'id'
    url = 'url'
    total_file_size = 'total_file_size'
    status = 'status'


class DOWNLOAD_CHUNK_COLUMNS:
    id = 'id'
    downloaded_chunk_size = 'downloaded_chunk_size'
    chunk_status = 'chunk_status'
    chunk_timestamp = 'chunk_timestamp'

