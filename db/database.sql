CREATE ROLE user WITH LOGIN PASSWORD '12345';
CREATE DATABASE iotdata OWNER user ENCODING 'UTF8';
\CONNECT iotdata;
CREATE TABLE readings(
    reading_id SERIAL PRIMARY KEY,
    sensor_id TEXT NOT NULL,
    heart_rate INTEGER NOT NULL,
    temperature NUMBER NOT NULL,
    pressure TEXT NOT NULL,
    record_time TIMESTAMP NOT NULL DEFAULT now()
);