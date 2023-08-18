-- For our first foray into aggregates, we're going to stick to something simple.
-- We want to know how many facilities exist - simply produce a total count.

SELECT COUNT(*)
FROM cd.facilities;

-- Produce a count of the number of facilities that have a cost to guests of 10 or more.

SELECT COUNT(*)
FROM cd.facilities
WHERE guestcost >= 10;

-- Produce a count of the number of recommendations each member has made. Order by member ID.

SELECT recommendedby, COUNT(*) AS count
FROM cd.members
WHERE recommendedby IS NOT NULL
GROUP BY recommendedby
ORDER BY recommendedby;

-- Produce a list of the total number of slots booked per facility.
-- For now, just produce an output table consisting of facility id and slots, sorted by facility id.

SELECT facid, SUM(slots)
FROM cd.bookings
GROUP BY facid
ORDER BY facid;

-- Produce a list of the total number of slots booked per facility in the month of September 2012.
-- Produce an output table consisting of facility id and slots, sorted by the number of slots.

SELECT facid, SUM(slots)
FROM cd.bookings
WHERE starttime >= '2012-09-01' AND
starttime < '2012-10-01'
GROUP BY facid
ORDER BY SUM(slots);

-- Produce a list of the total number of slots booked per facility per month in the year of 2012.
-- Produce an output table consisting of facility id and slots, sorted by the id and month.

SELECT facid, EXTRACT(MONTH FROM cd.bookings.starttime) AS month, SUM(slots)
FROM cd.bookings
WHERE EXTRACT(YEAR FROM cd.bookings.starttime) >= 2012 AND
EXTRACT(YEAR FROM cd.bookings.starttime) < 2013
GROUP BY facid, month
ORDER BY facid, month;

-- Find the total number of members (including guests) who have made at least one booking.

SELECT COUNT(DISTINCT memid)
FROM cd.bookings;

-- Produce a list of facilities with more than 1000 slots booked.
-- Produce an output table consisting of facility id and slots, sorted by facility id.

SELECT facid, SUM(slots)
FROM cd.bookings
GROUP BY facid
HAVING SUM(slots) > 1000
ORDER BY facid;

-- Produce a list of facilities along with their total revenue.
-- The output table should consist of facility name and revenue, sorted by revenue.
-- Remember that there's a different cost for guests and members!

SELECT name, SUM(slots *
CASE
	WHEN memid = 0 THEN guestcost
	ELSE membercost
END) AS revenue
FROM cd.facilities
JOIN cd.bookings
ON cd.facilities.facid = cd.bookings.facid
GROUP BY name
ORDER BY revenue;

-- Produce a list of facilities with a total revenue less than 1000.
-- Produce an output table consisting of facility name and revenue, sorted by revenue.
-- Remember that there's a different cost for guests and members!

SELECT name, revenue
FROM (
  	SELECT name, SUM(slots *
	CASE
		WHEN memid = 0 THEN guestcost
		ELSE membercost
	END) AS revenue
	FROM cd.facilities
	JOIN cd.bookings
	ON cd.facilities.facid = cd.bookings.facid
	GROUP BY name
) AS innercalc
WHERE revenue < 1000
ORDER BY revenue;

-- Output the facility id that has the highest number of slots booked.
-- For bonus points, try a version without a LIMIT clause. This version will probably look messy!

SELECT facid, SUM(slots) AS totalslots
FROM cd.bookings
GROUP BY facid
HAVING SUM(slots) = (
	SELECT MAX(total)
	FROM
	(
		SELECT facid, SUM(slots) AS total
		FROM cd.bookings
		GROUP BY facid
	) AS agg
)

-- Produce a list of the total number of slots booked per facility per month in the year of 2012.
-- In this version, include output rows containing totals for all months per facility, and a total for all months for all facilities.
-- The output table should consist of facility id, month and slots, sorted by the id and month.
-- When calculating the aggregated values for all months and all facids, return null values in the month and facid columns.

SELECT facid,  EXTRACT(MONTH FROM starttime) AS month, SUM(slots) AS slots
FROM cd.bookings
WHERE EXTRACT(YEAR FROM starttime) = '2012'
GROUP BY
	ROLLUP (
	  facid,
	  EXTRACT(MONTH FROM starttime)
	)
ORDER BY facid, month

-- Produce a list of the total number of hours booked per facility, remembering that a slot lasts half an hour.
-- The output table should consist of the facility id, name, and hours booked, sorted by facility id.
-- Try formatting the hours to two decimal places.

SELECT bks.facid, fac.name, ROUND(SUM(bks.slots) * 0.5::numeric, 2) AS TotalHours
FROM cd.bookings bks
JOIN cd.facilities fac ON bks.facid = fac.facid
GROUP BY bks.facid, fac.name
ORDER BY bks.facid

SELECT mem.surname, mem.firstname, mem.memid, bks.starttime
FROM cd.members mem
JOIN cd.bookings bks ON mem.memid = bks.memid
WHERE bks.starttime >= '2012-09-01'::date AND bks.starttime = (
  	SELECT MIN(starttime)
  	FROM cd.bookings
  	WHERE mem.memid = cd.bookings.memid
  	AND starttime >= '2012-09-01'::date AND starttime < '2012-09-02'::date
  )::date
GROUP BY mem.surname, mem.firstname, mem.memid, bks.starttime
ORDER BY mem.memid;

-- Produce a list of each member name, id, and their first booking after September 1st 2012. Order by member ID.

SELECT mem.surname, mem.firstname, mem.memid, MIN(bks.starttime)
FROM cd.bookings bks
JOIN cd.members mem ON bks.memid = mem.memid
WHERE bks.starttime >= '2012-09-01' AND bks.starttime < '2012-10-01'
GROUP BY mem.memid
ORDER BY mem.memid;

-- Produce a list of member names, with each row containing the total member count. Order by join date, and include guest members.

SELECT (
	SELECT DISTINCT COUNT(memid)
	FROM cd.members
), firstname, surname
FROM cd.members
GROUP BY memid
ORDER BY joindate

-- Produce a monotonically increasing numbered list of members (including guests), ordered by their date of joining.
-- Remember that member IDs are not guaranteed to be sequential.

SELECT ROW_NUMBER () OVER (ORDER BY cd.members.memid),
	firstname,
	surname
FROM cd.members;

-- Output the facility id that has the highest number of slots booked.
-- Ensure that in the event of a tie, all tieing results get output.

SELECT facid, total
FROM (
	SELECT facid, SUM(slots) total,
	RANK() OVER (
		ORDER BY SUM(slots) DESC
	) AS ranked
	FROM cd.bookings
	GROUP BY facid
) AS ranked
WHERE ranked = 1;

-- Produce a list of members (including guests), along with the number of hours they've booked in facilities, rounded to the nearest ten hours.
-- Rank them by this rounded figure, producing output of first name, surname, rounded hours, rank. Sort by rank, surname, and first name.

SELECT firstname, surname, ROUND((SUM(bks.slots) * 0.5)::numeric, -1) hours,
RANK() OVER (
	ORDER BY  ROUND((SUM(bks.slots) * 0.5)::numeric, -1) DESC
) rank
FROM cd.bookings bks
JOIN cd.members mem ON bks.memid = mem.memid
GROUP BY mem.firstname, mem.surname
ORDER BY rank, surname, firstname;

-- Produce a list of the top three revenue generating facilities (including ties).
-- Output facility name and rank, sorted by rank and facility name.

SELECT name, RANK() OVER (
	ORDER BY SUM(slots *
		CASE
			WHEN memid = 0 THEN guestcost
		ELSE membercost
	END) DESC
) AS rank
FROM cd.facilities
JOIN cd.bookings
ON cd.facilities.facid = cd.bookings.facid
GROUP BY name
ORDER BY rank
LIMIT 3;

-- Classify facilities into equally sized groups of high, average, and low based on their revenue.
-- Order by classification and facility name.

SELECT name,
CASE
	WHEN col = 3 THEN 'low'
	WHEN col = 2 THEN 'average'
	WHEN col = 1 THEN 'high'
END revenue
FROM (
	SELECT name,
	NTILE(3) OVER (
		ORDER BY SUM(slots *
			CASE
				WHEN memid = 0 THEN guestcost
				ELSE membercost
			END) DESC
	) AS col
	FROM cd.facilities
	JOIN cd.bookings
	ON cd.facilities.facid = cd.bookings.facid
	GROUP BY name
) AS initial
ORDER BY col, name

-- Based on the 3 complete months of data so far, calculate the amount of time each facility will take to repay its cost of ownership.
-- Remember to take into account ongoing monthly maintenance.
-- Output facility name and payback time in months, order by facility name.
-- Don't worry about differences in month lengths, we're only looking for a rough value here!

SELECT name, totalsum / (revenue / 3) AS months
FROM
(
	SELECT name, (SUM(slots *
	CASE
		WHEN memid = 0 THEN guestcost
		ELSE membercost
	END) - (monthlymaintenance * 3)) AS revenue, (initialoutlay) TotalSum
	FROM cd.facilities
	JOIN cd.bookings
	ON cd.facilities.facid = cd.bookings.facid
	GROUP BY name, TotalSum, monthlymaintenance
) AS abc
ORDER BY name

-- For each day in August 2012, calculate a rolling average of total revenue over the previous 15 days.
-- Output should contain date and revenue columns, sorted by the date.
-- Remember to account for the possibility of a day having zero revenue.
-- This one's a bit tough, so don't be afraid to check out the hint!

SELECT date,
       (
          SELECT SUM(slots *
            CASE
	            WHEN memid = 0 THEN guestcost
	            ELSE membercost
            END) / 15 AS rev
          FROM cd.bookings bks
          INNER JOIN cd.facilities facs ON bks.facid = facs.facid
          WHERE bks.starttime > dategen.date - INTERVAL '14 days'
          AND bks.starttime < dategen.date + INTERVAL '1 day'
       ) AS revenue
FROM
    (
        SELECT CAST(generate_series(TIMESTAMP '2012-08-01', '2012-08-31', '1 day') AS DATE) AS date
    ) AS dategen
ORDER BY dategen.date;





