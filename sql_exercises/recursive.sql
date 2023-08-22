-- Find the upward recommendation chain for member ID 27: that is, the member who recommended them, and the member who recommended that member, and so on.
-- Return member ID, first name, and surname. Order by descending member id.

SELECT memid, firstname, surname
FROM cd.members
JOIN (WITH RECURSIVE outerquery AS (
	SELECT recommendedby FROM  cd.members
  	WHERE memid = 27
  	UNION
  	SELECT mem.recommendedby
  	FROM cd.members mem
  	JOIN outerquery o ON mem.memid = o.recommendedby
) SELECT *
FROM outerquery) AS subq ON cd.members.memid = subq.recommendedby;

-- Find the downward recommendation chain for member ID 1: that is, the members they recommended, the members those members recommended, and so on.
-- Return member ID and name, and order by ascending member id.

SELECT cd.members.memid, cd.members.firstname, cd.members.surname
FROM cd.members
JOIN (WITH RECURSIVE outerquery AS (
	SELECT memid FROM  cd.members
  	WHERE recommendedby = 1
  	UNION
  	SELECT mem.memid
  	FROM cd.members mem
  	JOIN outerquery o ON mem.recommendedby = o.memid
) SELECT *
FROM outerquery) AS subq ON cd.members.memid = subq.memid
ORDER BY memid;

-- Produce a CTE that can return the upward recommendation chain for any member.
-- You should be able to select recommender from recommenders where member=x.
-- Demonstrate it by getting the chains for members 12 and 22.
-- Results table should have member and recommender, ordered by member ascending, recommender descending.

WITH RECURSIVE outerquery(recommender, member) AS (
  SELECT recommendedby, memid
  FROM cd.members
  UNION
  SELECT mem.recommendedby, outerq.member
  FROM outerquery outerq
  JOIN cd.members mem
  ON mem.memid = outerq.recommender
) SELECT outerq.member member, outerq.recommender, mem.firstname, mem.surname
FROM outerquery outerq
JOIN cd.members mem
ON outerq.recommender = mem.memid
WHERE outerq.member = 22 OR outerq.member = 12
ORDER BY outerq.member, outerq.recommender DESC;