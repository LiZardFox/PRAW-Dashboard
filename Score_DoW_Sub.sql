SELECT SUM(r.score),  
    CASE
        WHEN extract(dow from p.date) = 0 THEN 'Sunday'
        WHEN extract(dow from p.date) = 1 THEN 'Monday'
        WHEN extract(dow from p.date) = 2 THEN 'Tuesday'
        WHEN extract(dow from p.date) = 3 THEN 'Wednesday'
        WHEN extract(dow from p.date) = 4 THEN 'Thursday'
        WHEN extract(dow from p.date) = 5 THEN 'Friday'
        WHEN extract(dow from p.date) = 6 THEN 'Saturday'
    END AS "Day of the week",
    s.name AS Subreddit
FROM ratings r
JOIN (
        SELECT MAX(date) as max_date, r1.post_id
        FROM ratings r1
        GROUP BY post_id
    ) d ON d.post_id = r.post_id
JOIN posts p ON p.id = r.post_id
JOIN subreddits s ON s.id = p.subreddit_id
WHERE d.max_date = r.date
GROUP BY 2, 3
ORDER BY SUM(r.score) DESC;