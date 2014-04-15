SELECT
    move.*
FROM nov13_move move
INNER JOIN nov13_creation creation USING (page_id)
INNER JOIN afc_page_20140331 page USING (page_id)
WHERE 
    creation.rev_timestamp BETWEEN "200901" and "201311" AND
    move.timestamp BETWEEN "200901" and "201311";

