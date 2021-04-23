CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT, password TEXT, type TEXT);
CREATE TABLE swap (id SERIAL PRIMARY KEY, date TEXT, start_time TEXT, end_time TEXT, post TEXT, comment TEXT, username TEXT REFERENCES users(username), visibility INTEGER);
CREATE TABLE take (id SERIAL PRIMARY KEY, date TEXT, start_time TEXT, end_time TEXT, post TEXT, comment TEXT, username TEXT REFERENCES users(username), visibility INTEGER);
CREATE TABLE give (id SERIAL PRIMARY KEY, date TEXT, comment TEXT, username TEXT REFERENCES users(username), visibility INTEGER);
CREATE TABLE give_offers (id SERIAL PRIMARY KEY, give_id INTEGER REFERENCES give(id), offer TEXT, username TEXT REFERENCES users(username), date DATE, admin_visibility INTEGER, user_visibility INTEGER);
CREATE TABLE take_offers (id SERIAL PRIMARY KEY, take_id INTEGER REFERENCES take(id), username TEXT REFERENCES users(username), admin_visibility INTEGER, user_visibility INTEGER);
CREATE TABLE swap_offers (id SERIAL PRIMARY KEY, swap_id INTEGER REFERENCES swap(id), username TEXT REFERENCES users(username), offer TEXT, date DATE, admin_visibility INTEGER, user_visibility INTEGER);
