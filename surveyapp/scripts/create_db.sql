.open ../users.db

CREATE TABLE STUDENTS
        (ID TEXT PRIMARY KEY NOT NULL,
        PASSWORD TEXT NOT NULL);

CREATE TABLE STAFF
        (ID TEXT PRIMARY KEY NOT NULL,
        PASSWORD TEXT NOT NULL);

CREATE TABLE ADMINS
        (ID TEXT PRIMARY KEY NOT NULL,
        PASSWORD TEXT NOT NULL);
