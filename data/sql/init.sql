CREATE TABLE IF NOT EXISTS song (
    id INTEGER PRIMARY KEY,
    filename TEXT NOT NULL UNIQUE,
    url TEXT
);

CREATE TABLE IF NOT EXISTS tempo (
    id INTEGER PRIMARY KEY,
    val REAL NOT NULL,
    FOREIGN KEY(id) REFERENCES song(id)
);

CREATE TABLE IF NOT EXISTS fft (
    id INTEGER PRIMARY KEY,
    data BLOB NOT NULL,
    FOREIGN KEY(id) REFERENCES song(id)
);

CREATE TABLE IF NOT EXISTS rms (
    id INTEGER PRIMARY KEY,
    data BLOB NOT NULL,
    FOREIGN KEY(id) REFERENCES song(id)
)

CREATE TABLE IF NOT EXISTS correlation (
    firstId INTEGER,
    secondId INTEGER,
    val REAL NOT NULL,
    FOREIGN KEY(firstId) REFERENCES song(id),
    FOREIGN KEY(secondId) REFERENCES song(id),
    PRIMARY KEY(firstId, secondId)
);

CREATE TABLE log (
    id INTEGER PRIMARY KEY,
    timestamp INTEGER,
    rate INTEGER,
    FOREIGN KEY(id) REFERENCES song(id)
)