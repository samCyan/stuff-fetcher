CREATE TABLE IF NOT EXISTS DOWNLOADS (
    id TEXT PRIMARY KEY,
    url TEXT NOT NULL,
    total_file_size INT DEFAULT 0,
    status TEXT DEFAULT 'downloading'
);
