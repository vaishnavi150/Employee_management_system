
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT,
    username TEXT,
    password TEXT,
    role TEXT CHECK(role IN ('admin', 'emp')),
    profile_pic TEXT
);
CREATE TABLE employee (
    eid INTEGER PRIMARY KEY AUTOINCREMENT,
    ename TEXT,
    edept TEXT,
    esalary INTEGER,
    ephone TEXT,
    username TEXT
);