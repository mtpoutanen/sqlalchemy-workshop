CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    title VARCHAR(200),
    content TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
