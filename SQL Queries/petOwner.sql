DROP TABLE IF EXISTS petOwner cascade;

CREATE TABLE petOwner (
    email VARCHAR(100) NOT NULL PRIMARY KEY,
    FOREIGN KEY (email) REFERENCES user
);