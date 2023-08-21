-- Produce a timestamp for 1 a.m. on the 31st of August 2012.

SELECT '2012-08-31 01:00:00'::timestamp AS timestamp;

-- Find the result of subtracting the timestamp '2012-07-30 01:00:00' from the timestamp '2012-08-31 01:00:00'

SELECT  '2012-08-31 01:00:00'::timestamp - '2012-07-30 01:00:00'::timestamp AS interval;

-- Produce a list of all the dates in October 2012. They can be output as a timestamp (with time set to midnight) or a date.

SELECT GENERATE_SERIES(
	'2012-10-01'::timestamp,
	'2012-10-31',
  	'1 day'
) AS ts;

-- Get the day of the month from the timestamp '2012-08-31' as an integer.

SELECT EXTRACT(DAY FROM '2012-08-31'::timestamp)::integer AS date_part;

-- Work out the number of seconds between the timestamps '2012-08-31 01:00:00' and '2012-09-02 00:00:00'

SELECT (EXTRACT(DAY FROM '2012-09-02 00:00:00'::timestamp - '2012-08-31 01:00:00'::timestamp) * 24 + EXTRACT(HOURS FROM '2012-09-02 00:00:00'::timestamp - '2012-08-31 01:00:00'::timestamp)) * 3600 AS date_part;

-- For each month of the year in 2012, output the number of days in that month.
-- Format the output as an integer column containing the month of the year, and a second column containing an interval data type.

SELECT EXTRACT(MONTH FROM month_date) AS month,
       DATE_TRUNC('month', month_date + INTERVAL '1 MONTH')
       - month_date AS days_in_month
FROM generate_series(
    '2012-01-01'::date,
    '2012-12-01'::date,
    INTERVAL '1 month'
) AS month_date;

-- For any given timestamp, work out the number of days remaining in the month.
-- The current day should count as a whole day, regardless of the time. Use '2012-02-11 01:00:00' as an example timestamp for the purposes of making the answer.
-- Format the output as a single interval value.

SELECT DATE_TRUNC('month', '2012-02-11 01:00:00'::timestamp + INTERVAL '1 month') -
DATE_TRUNC('day', '2012-02-11 01:00:00'::timestamp) AS remaining;

-- Return a list of the start and end time of the last 10 bookings (ordered by the time at which they end, followed by the time at which they start) in the system.

SELECT starttime, starttime + INTERVAL '30 minutes' * slots AS endtime
FROM cd.bookings
ORDER BY endtime DESC, starttime DESC
LIMIT 10;

-- Return a count of bookings for each month, sorted by month

SELECT
	DATE_TRUNC('month', starttime) m,
	COUNT(starttime)
FROM
	cd.bookings
GROUP BY m
ORDER BY m;

-- Work out the utilisation percentage for each facility by month, sorted by name and month, rounded to 1 decimal place.
-- Opening time is 8am, closing time is 8.30pm.
-- You can treat every month as a full month, regardless of if there were some dates the club was not open.

SELECT name, m AS month, ROUND(((sum / ((12.5 * days) * 2)) * 100)::numeric, 1) AS utilization
FROM (
	SELECT
	name,
	DATE_TRUNC('month', starttime) m,
	DATE_PART('days',
        DATE_TRUNC('month', starttime::timestamp)
        + '1 MONTH'::INTERVAL
        - '1 DAY'::INTERVAL
    ) AS days,
	SUM(slots)
	FROM
	cd.bookings bks
	JOIN
	cd.facilities fac ON bks.facid = fac.facid
	GROUP BY name, m
) AS outertable
ORDER BY name;

