CREATE TABLE category(
    id SERIAL PRIMARY KEY,
    label VARCHAR(100),
    description TEXT
);

INSERT INTO category(label, description)
VALUES
    ('Weekly chores', 'The chores that must be completed within a week.'),
    ('Daily chores', 'The chores that must be completed within a day.'),
    ('Monthly chores', 'The chores that must be completed within a month.');

CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    username VARCHAR(100),
    email VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    -- todo_list_id INT REFERENCES todo_list(id) ON DELETE CASCADE
);

INSERT INTO users(username, email)
VALUES
    ('DenisB22', 'denis@gmail.com'),
    ('George44', 'george@yahoo.com'),
    ('IvanB48', 'ivan@yahoo.com');

CREATE TABLE todo_list(
    id SERIAL PRIMARY KEY,
    title VARCHAR(100),
    summary TEXT,
    category_id INT REFERENCES category(id) ON DELETE CASCADE,
    user_id INT REFERENCES users(id) ON DELETE CASCADE
);

INSERT INTO todo_list(title, summary, category_id, user_id)
VALUES
    ('To Do Daily', 'To Do list for the daily tasks.', 2, 1),
    ('To Do Weekly', 'To Do list for the weekly tasks.', 1, 2),
    ('To Do Monthly', 'To Do list for the monthly tasks.', 3, 1);

CREATE TABLE entry(
	id SERIAL PRIMARY KEY,
	description VARCHAR(100),
	is_complete BOOLEAN,
	created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
	created_by_user_id INT REFERENCES users(id) ON DELETE CASCADE,
	updated_by_user_id INT REFERENCES users(id) ON DELETE CASCADE,
	todo_list_id INT REFERENCES todo_list(id) ON DELETE CASCADE
);

--

INSERT INTO entry(description, is_complete, created_by_user_id, updated_by_user_id, todo_list_id)
VALUES
    ('Clean the house', TRUE, 1, 1, 2),
    ('Wash the dishes', FALSE, 2, 2, 1),
    ('Sweeping and mopping the floor', TRUE, 1, 1, 2),
    ('Order the garage', FALSE, 3, 3, 3);

--

SELECT category_id, COUNT(*) AS count_of_todos
FROM todo_list
WHERE category_id = 1
GROUP BY category_id;

--

-- show information about the percentage of category of todo lists out of all todo lists
-- For example - if we have 3 categories (shopping, electric bills, car),
-- what is the percentage of the todo lists for each category?

SELECT category_id, COUNT(*) AS count_of_todos,
((SELECT COUNT(*) FROM todo_list
WHERE category_id = 1
)::FLOAT / (SELECT COUNT(category_id) FROM todo_list)::FLOAT) * 100 AS percentage
FROM todo_list
WHERE category_id = 1
GROUP BY category_id;

-- show the count of todo lists per user (for the user you can just show the username)

SELECT username, COUNT(*)
FROM todo_list
JOIN users ON todo_list.user_id = users.id
GROUP BY username;

-- show a summary of which entries are marked as done for each todo list

SELECT *
FROM entry
WHERE is_complete = 'true';

-- show a summary of how many entries are marked as done for each todo list

SELECT COUNT(*)
FROM entry
WHERE is_complete = 'true';

--show the entries in a single todo list with the following information:
    --todo_list.title
    --todo_list.summary
    --category.label
    --description
    --is_complete
    --timestamp of creation
    --timestamp of last update
    --user.username (the creator)
    --user.email (the creator)
    --user.username (the one who has last updated it)
    --user.email (the one who has last updated it)

SELECT title, summary, label, is_complete, e.created_at, e.updated_at, uc.username AS username_created, uc.email AS email_created, uu.username AS username_updated, uu.email AS email_updated
FROM todo_list tl
JOIN entry e ON tl.id = e.todo_list_id
JOIN category c  ON tl.category_id = c.id
JOIN users uc ON uc.id = (
	SELECT user_id
	FROM todo_list
	JOIN entry ON entry.created_by_user_id = todo_list.user_id
	WHERE todo_list.id = 1
	GROUP BY user_id
)
JOIN users uu ON uu.id = (
	SELECT user_id
	FROM todo_list
	JOIN entry ON entry.updated_by_user_id = todo_list.user_id
	WHERE todo_list.id = 1
	GROUP BY user_id
)
WHERE tl.id = 1;

-- show the entries in a single todo list with the following information

-- todo_list.title

SELECT title, description
FROM entry
JOIN todo_list ON entry.todo_list_id = todo_list.id
WHERE todo_list.id = 1;

-- todo_list.summary

SELECT summary, description
FROM entry
JOIN todo_list ON entry.todo_list_id = todo_list.id
WHERE todo_list.id = 1;

-- category.label

SELECT summary, label
FROM category
JOIN todo_list ON todo_list.category_id = category.id
WHERE todo_list.id = 1;

-- description

SELECT summary, description
FROM category
JOIN todo_list ON todo_list.category_id = category.id
WHERE todo_list.id = 1;

-- is_complete

SELECT title, is_complete
FROM entry
JOIN todo_list ON todo_list.id = entry.todo_list_id
WHERE todo_list.id = 1;


-- timestamp of creation

SELECT title, created_at
FROM entry
JOIN todo_list ON todo_list.id = entry.todo_list_id
WHERE todo_list.id = 1;

-- timestamp of last update

SELECT title, updated_at
FROM entry
JOIN todo_list ON todo_list.id = entry.todo_list_id
WHERE todo_list.id = 1;

-- user.username (the creator)

SELECT username
FROM users
WHERE users.id = (
	SELECT user_id
	FROM todo_list
	JOIN entry ON entry.created_by_user_id = todo_list.user_id
	WHERE todo_list.id = 1
	GROUP BY user_id
);

-- user.email (the creator)

SELECT email
FROM users
WHERE users.id = (
	SELECT user_id
	FROM todo_list
	JOIN entry ON entry.created_by_user_id = todo_list.user_id
	WHERE todo_list.id = 1
	GROUP BY user_id
);

-- user.username (the one who has last updated it)

SELECT username
FROM users
WHERE users.id = (
	SELECT user_id
	FROM todo_list
	JOIN entry ON entry.updated_by_user_id = todo_list.user_id
	WHERE todo_list.id = 1
	GROUP BY user_id
);

-- user.email (the one who has last updated it)

SELECT email
FROM users
WHERE users.id = (
	SELECT user_id
	FROM todo_list
	JOIN entry ON entry.updated_by_user_id = todo_list.user_id
	WHERE todo_list.id = 1
	GROUP BY user_id
);








