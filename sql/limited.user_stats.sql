SELECT
    users.*
FROM nov13_user_stats users
INNER JOIN nov13_creation creation USING (user_id)
WHERE 
    creation.rev_timestamp BETWEEN "200901" and "201311"

