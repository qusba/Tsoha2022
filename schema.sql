CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT UNIQUE, password TEXT, admin BOOLEAN);
INSERT INTO users (username,password,admin) VALUES ('ylläpitäjä','pbkdf2:sha256:260000$61e7Vu6U6BSyiSfS$f2f9c724ab1c10141034a6d1d82f608ab7a1a5e06dede24e942e9967c4af82a8',TRUE);
CREATE TABLE restaurants (id SERIAL PRIMARY KEY, name TEXT, visible BOOLEAN);
CREATE TABLE restaurantInfo (id SERIAL PRIMARY KEY, restaurant_id INTEGER REFERENCES restaurants, title TEXT, info TEXT, visible BOOLEAN);
CREATE TABLE reviews (id SERIAL PRIMARY KEY, restaurant_id INTEGER REFERENCES restaurants, stars INTEGER, review TEXT, visible BOOLEAN, username TEXT, time TIMESTAMP);
CREATE TABLE groups (id SERIAL PRIMARY KEY, name TEXT UNIQUE, visible BOOLEAN);

