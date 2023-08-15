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

-- TODO: continue with the examples





