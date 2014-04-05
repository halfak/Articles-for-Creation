CREATE TABLE halfak.afc_page_20140331
SELECT
    page_id,
    page_namespace,
    page_title,
    archived,
    identified_by
FROM (
    (
        SELECT
            page_id,
            page_namespace,
            page_title,
            FALSE AS archived,
            "namespace and title" AS identified_by
        FROM page
        WHERE page_namespace = 5
        AND page_title LIKE "Articles_for_creation/%"
    )
    UNION
    (
        SELECT
            ar_page_id,
            ar_namespace,
            ar_title,
            TRUE AS archived,
            "namespace and title (archive)" AS identified_by
        FROM archive
        WHERE ar_namespace = 5
        AND ar_title LIKE "Articles_for_creation/%"
        GROUP BY 1,2,3
    )
    UNION
    (
        SELECT
           main_page.page_id,
           main_page.page_namespace,
           main_page.page_title,
           FALSE AS archived,
           "categories" AS identified_by
        FROM page talk_page
        INNER JOIN page main_page ON
            main_page.page_namespace = 0 AND
            main_page.page_title = talk_page.page_title
        INNER JOIN categorylinks ON
            cl_from = talk_page.page_id AND
            cl_to IN (
                "Accepted AfC submissions",
                "Declined_AfC_submissions",
                "Pending_AfC_submissions",
                "Draft_AfC_submissions"
            )
        WHERE talk_page.page_namespace = 1
        GROUP BY 1,2,3
    )
) AS group_set
GROUP BY 1,2,3,4;
