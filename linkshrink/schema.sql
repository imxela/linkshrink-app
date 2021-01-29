DROP TABLE IF EXISTS url;

CREATE TABLE url (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    shrunk_url String(30) NOT NULL,
    target_url String(2048) NOT NULL
)