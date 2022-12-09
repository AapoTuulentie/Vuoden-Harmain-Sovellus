DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS entries CASCADE;
DROP TABLE IF EXISTS tags CASCADE;


CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    password TEXT
);

CREATE TABLE entries (
    id SERIAL PRIMARY KEY,
    author TEXT,
    title TEXT,
    publisher TEXT,
    year INTEGER,
    doi TEXT,
    isbn TEXT,
    editor TEXT,
    pages TEXT,
    shorthand TEXT,
    user_id INTEGER REFERENCES users ON DELETE CASCADE,
    citationtype TEXT,
    journal TEXT
);

CREATE TABLE tags (
    id SERIAL PRIMARY KEY,
    entry_id INTEGER REFERENCES entries ON DELETE CASCADE,
    user_id INTEGER REFERENCES users ON DELETE CASCADE,
    tag TEXT
);
