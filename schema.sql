DROP TABLE IF EXISTS pastes;

CREATE TABLE pastes (
    id INTEGER PRIMARY KEY, 
    body TEXT NOT NULL,
    private_paste BOOLEAN,
    user TEXT,
    FOREIGN KEY(user) REFERENCES users(user)
);

DROP TABLE IF EXISTS users; 

CREATE TABLE users (
    user TEXT, 
    pw TEXT, 
    email TEXT
);

INSERT INTO users VALUES ('admin', 'admin', 'admin@ad.ad'); 
INSERT INTO users VALUES ('ted', 'ted', 'ted@ted.ted');