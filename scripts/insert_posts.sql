BEGIN;

-- Declare a variable to hold the user's id
DO $$
DECLARE
    user_id INT;
BEGIN
    -- Select the id of the user with the smallest id into the variable
    SELECT id INTO user_id FROM users ORDER BY id ASC LIMIT 1;

    -- Insert five posts for this user
    INSERT INTO posts (user_id, title, content) VALUES
    (user_id, 'Post Title 1', 'Content of post 1.'),
    (user_id, 'Post Title 2', 'Content of post 2.'),
    (user_id, 'Post Title 3', 'Content of post 3.'),
    (user_id, 'Post Title 4', 'Content of post 4.'),
    (user_id, 'Post Title 5', 'Content of post 5.');
END $$;

-- Commit the transaction
COMMIT;
