CREATE TABLE swap (id SERIAL PRIMARY KEY, date TEXT, start_time TEXT, end_time TEXT, post TEXT, comment TEXT);
CREATE TABLE take (id SERIAL PRIMARY KEY, date TEXT, start_time TEXT, end_time TEXT, post TEXT, comment TEXT);
CREATE TABLE give (id SERIAL PRIMARY KEY, date TEXT, comment TEXT);
