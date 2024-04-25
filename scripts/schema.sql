CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT NOT NULL
);

INSERT INTO posts (title, content) VALUES ('Pahilo Post', 'This is the content of the first post.');
INSERT INTO posts (title, content) VALUES ('Dosro Post', 'This is the content of the second post.');