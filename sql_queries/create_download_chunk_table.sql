CREATE TABLE IF NOT EXISTS DOWNLOAD_CHUNKS (
    id TEXT NOT NULL,
    downloaded_chunk_size INT DEFAULT 0,
    chunk_status TEXT DEFAULT 'READY',
    chunk_timestamp TEXT,
    FOREIGN KEY (id) REFERENCES DOWNLOADS (id)
);