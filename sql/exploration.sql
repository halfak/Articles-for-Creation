SELECT
    page_namespace,
    count(distinct page_id)
FROM nov13_status_change
INNER JOIN nov13_creation creation USING (page_id)
WHERE 
    status IN ("reviewing", "pending", "accepted", "declined") AND
    creation.rev_timestamp BETWEEN "200901" and "201311"
GROUP BY 1;

SELECT
    status_change.*
FROM nov13_status_change status_change
INNER JOIN nov13_creation creation USING (page_id)
WHERE 
    creation.rev_timestamp BETWEEN "200901" and "201311" AND
    status_change.timestamp BETWEEN "200901" and "201311"
ORDER BY status_change.page_id, status_change.timestamp
LIMIT 10;
