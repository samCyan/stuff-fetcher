INSERT INTO downloads (id,
    url,
    total_file_size,
    downloaded_file_size,
    remaining_file_size,
    status,
    estimated_time_to_complete) VALUES (?,?,?,?,?,?,?)
);