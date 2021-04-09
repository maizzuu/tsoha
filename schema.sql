CREATE TABLE swap (id SERIAL PRIMARY KEY, date TEXT, start_time TEXT, end_time TEXT, post TEXT, comment TEXT);
CREATE TABLE take (id SERIAL PRIMARY KEY, date TEXT, start_time TEXT, end_time TEXT, post TEXT, comment TEXT);
CREATE TABLE give (id SERIAL PRIMARY KEY, date TEXT, comment TEXT);
CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT, password TEXT);
INSERT INTO swap (date, start_time, end_time, post, comment) VALUES ('20.4.', '5.00', '13.00', '2', 'vaihtuu samalle päivälle iltavuoroon');
INSERT INTO take (date, start_time, end_time, post, comment) VALUES ('15.4.', '13.30', '20,00', 'BLC', 'ramppiluvat tarvitaan');
INSERT INTO give (date, comment) VALUES ('12.4.', 'iltavuoro');
INSERT INTO users (username, password) VALUES ('Maija', pbkdf2:sha256:150000$iz6PzzEY$be436c8f09eb0341873344686a51711d837547f311f5be2811c0e5c5726ac742);
