-- How can you produce a list of the start times for bookings by members named 'David Farrell'?

SELECT starttime
FROM cd.bookings
INNER JOIN cd.members ON cd.bookings.memid = cd.members.memid
WHERE cd.members.firstname = 'David'
AND cd.members.surname = 'Farrell';

-- How can you produce a list of the start times for bookings for tennis courts, for the date '2012-09-21'?
-- Return a list of start time and facility name pairings, ordered by the time.

SELECT starttime AS start, name
FROM cd.bookings
JOIN cd.facilities ON cd.bookings.facid = cd.facilities.facid
WHERE starttime::date = '2012-09-21'::date
AND name LIKE 'Tennis Court%'
ORDER BY starttime;

-- How can you output a list of all members who have recommended another member?
-- Ensure that there are no duplicates in the list, and that results are ordered by (surname, firstname).

SELECT DISTINCT cd.members.firstname, cd.members.surname
FROM cd.members
JOIN cd.members AS cdmem ON cd.members.memid = cdmem.recommendedby
ORDER BY cd.members.surname, cd.members.firstname;

-- How can you output a list of all members, including the individual who recommended them (if any)?
-- Ensure that results are ordered by (surname, firstname).

SELECT mem.firstname AS memfname, mem.surname AS memsname, rec.firstname AS recfname, rec.surname AS recsname
FROM cd.members mem
LEFT OUTER JOIN cd.members rec ON rec.memid = mem.recommendedby
ORDER BY mem.surname, mem.firstname;

-- How can you produce a list of all members who have used a tennis court?
-- Include in your output the name of the court, and the name of the member formatted as a single column.
-- Ensure no duplicate data, and order by the member name followed by the facility name.

SELECT DISTINCT firstname || ' ' || surname AS member, name AS facility
FROM cd.facilities
JOIN cd.bookings ON cd.facilities.facid = cd.bookings.facid
JOIN cd.members ON cd.bookings.memid = cd.members.memid
WHERE name LIKE '%Tennis Court%'
ORDER BY member, facility;

-- How can you produce a list of bookings on the day of 2012-09-14 which will cost the member (or guest) more than $30?
-- Remember that guests have different costs to members (the listed costs are per half-hour 'slot'), and the guest user is always ID 0.
-- Include in your output the name of the facility, the name of the member formatted as a single column, and the cost.
-- Order by descending cost, and do not use any subqueries.

SELECT firstname || ' ' || surname AS member, name AS facility,
	CASE
		WHEN cd.bookings.memid > 0 THEN membercost * slots
		WHEN cd.bookings.memid = 0 THEN guestcost * slots
	END AS cost
FROM cd.members
JOIN cd.bookings ON cd.bookings.memid = cd.members.memid
JOIN cd.facilities ON cd.facilities.facid = cd.bookings.facid
WHERE cd.bookings.starttime >= '2012-09-14' AND
cd.bookings.starttime < '2012-09-15' AND
(
	(cd.members.memid = 0 AND cd.bookings.slots * cd.facilities.guestcost > 30)
  	OR
  	(cd.members.memid != 0 AND cd.bookings.slots * cd.facilities.membercost > 30)

)
ORDER BY cost DESC;

-- How can you output a list of all members, including the individual who recommended them (if any), without using any joins?
-- Ensure that there are no duplicates in the list, and that each firstname + surname pairing is formatted as a column and ordered.

SELECT DISTINCT mem.firstname || ' ' || mem.surname AS member,
(
	SELECT DISTINCT rec.firstname || ' ' || rec.surname AS recommender
  	FROM cd.members rec
  	WHERE rec.memid = mem.recommendedby
)
FROM cd.members mem
ORDER BY member;

-- The Produce a list of costly bookings exercise contained some messy logic: we had to calculate the booking cost in both the WHERE clause and the CASE statement.
-- Try to simplify this calculation using subqueries

SELECT member, facility, cost FROM
(SELECT firstname || ' ' || surname AS member, name AS facility,
	CASE
		WHEN cd.bookings.memid > 0 THEN membercost * slots
		WHEN cd.bookings.memid = 0 THEN guestcost * slots
	END AS cost
FROM cd.members
JOIN cd.bookings ON cd.bookings.memid = cd.members.memid
JOIN cd.facilities ON cd.facilities.facid = cd.bookings.facid
WHERE cd.bookings.starttime >= '2012-09-14' AND
cd.bookings.starttime < '2012-09-15') AS bookings
WHERE cost > 30
ORDER BY cost DESC;




