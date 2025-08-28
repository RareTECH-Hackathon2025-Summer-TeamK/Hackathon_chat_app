
DROP DATABASE IF EXISTS chatapp;
DROP USER 'testuser';

CREATE USER 'testuser' IDENTIFIED BY 'testuser';
CREATE DATABASE chatapp;
USE chatapp;
GRANT ALL PRIVILEGES ON chatapp.* TO 'testuser';

CREATE TABLE users (
    user_id VARCHAR(255) PRIMARY KEY,
    is_admin boolean NOT NULL DEFAULT FALSE,
    user_name VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(128) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE channels (
    channel_id VARCHAR (255) PRIMARY KEY,
    channel_name VARCHAR (20) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE messages (
    message_id INT AUTO_INCREMENT PRIMARY KEY,
    message_content text NOT NULL,
    user_id VARCHAR(255) NOT NULL,
    channel_id VARCHAR(255) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (channel_id) REFERENCES channels(channel_id) ON DELETE CASCADE
);

INSERT INTO users(user_id, is_admin, user_name, email, password) VALUES('970af84c-dd40-47ff-af23-282b72b7cca8', 1, 'admin', 'test@gmail.com', '37268335dd6931045bdcdf92623ff819a64244b53d0e');
INSERT INTO users(user_id, is_admin, user_name, email, password) VALUES('970af84c-dd40-47ff-af23-282b72b7cca9', 1, 'admin2', 'test2@gmail.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8');
INSERT INTO channels(channel_id, channel_name) VALUES('1', 'Bookroom');
INSERT INTO channels(channel_id, channel_name) VALUES('2', 'Playroom');
INSERT INTO messages(message_id, message_content, user_id, channel_id) VALUES('1', 'Shall we talk about books with me? ', '970af84c-dd40-47ff-af23-282b72b7cca8', '1');