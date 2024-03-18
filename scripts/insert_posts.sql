BEGIN;

INSERT INTO posts (user_id, title, content)
SELECT id, 'Common Post Title', 'This is a common post content for all users.'
FROM users;

-- Commit the transaction
COMMIT;
