CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT, password TEXT, admin BOOLEAN);
INSERT INTO users (username,password,admin) VALUES ('ylläpitäjä','admin',TRUE);
CREATE TABLE restaurants (id SERIAL PRIMARY KEY, name TEXT);
CREATE TABLE restaurantInfo (id SERIAL PRIMARY KEY, restaurant_id INTEGER REFERENCES restaurants, title TEXT, info TEXT, visible BOOLEAN);
CREATE TABLE reviews (id SERIAL PRIMARY KEY, restaurant_id INTEGER REFERENCES restaurants, stars INTEGER, review TEXT, visible BOOLEAN, username TEXT, time TIMESTAMP);
CREATE TABLE groups (id SERIAL PRIMARY KEY, name TEXT, restaurants INTEGER REFERENCES restaurants);

