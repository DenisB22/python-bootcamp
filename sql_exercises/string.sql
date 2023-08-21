-- Output the names of all members, formatted as 'Surname, Firstname'

SELECT surname || ', ' || firstname AS name
FROM cd.members
GROUP BY memid
ORDER BY memid;

-- Find all facilities whose name begins with 'Tennis'. Retrieve all columns.

SELECT *
FROM cd.facilities
WHERE name LIKE 'Tennis%';

-- Perform a case-insensitive search to find all facilities whose name begins with 'tennis'. Retrieve all columns.

SELECT *
FROM cd.facilities
WHERE name ILIKE 'tennis%';

-- You've noticed that the club's member table has telephone numbers with very inconsistent formatting.
-- You'd like to find all the telephone numbers that contain parentheses, returning the member ID and telephone number sorted by member ID.

SELECT memid, telephone
FROM cd.members
WHERE telephone LIKE '(%)%';

