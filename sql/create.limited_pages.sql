CREATE TABLE halfak.nov13_limited_page
SELECT
    page.*,
    afc.page_id IS NOT NULL AS is_afc
FROM nov13_page page
INNER JOIN nov13_page_origin origin USING (page_id)
LEFT JOIN afc_page_20140331 afc USING (page_id)
WHERE 
    page.first_revision BETWEEN "200901" and "201311" AND
    origin.original_namespace = 0 OR afc.page_id IS NOT NULL;

