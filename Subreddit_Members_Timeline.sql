SELECT m.date, s.name, MAX(m.members_count) AS max_members_count,
       (MAX(m.members_count) - LAG(MAX(m.members_count)) OVER (PARTITION BY s.name ORDER BY m.date)) AS diff
FROM members m
JOIN subreddits s ON s.id = m.subreddit_id
GROUP BY m.date, s.name
ORDER BY m.date;