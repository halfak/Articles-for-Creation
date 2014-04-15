SELECT
    status_change.*
FROM nov13_status_change status_change
INNER JOIN nov13_creation creation USING (page_id)
WHERE 
    creation.rev_timestamp BETWEEN "200901" and "201311" AND
    status_change.timestamp BETWEEN "200901" and "201311";



