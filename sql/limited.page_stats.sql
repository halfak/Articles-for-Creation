SELECT
    page_id,
    page_namespace,
    page_title,
    SUM(week_1_revisions) AS week_1_revisions,
    SUM(week_2_revisions) AS week_2_revisions,
    SUM(week_3_revisions) AS week_3_revisions,
    SUM(week_4_revisions) AS week_4_revisions,
    SUM(week_1_bytes) AS week_1_bytes,
    SUM(week_2_bytes) AS week_2_bytes,
    SUM(week_3_bytes) AS week_3_bytes,
    SUM(week_4_bytes) AS week_4_bytes,
    SUM(week_1_unique_anons) AS week_1_unique_anons,
    SUM(week_2_unique_anons) AS week_2_unique_anons,
    SUM(week_3_unique_anons) AS week_3_unique_anons,
    SUM(week_4_unique_anons) AS week_4_unique_anons,
    SUM(week_1_unique_users) AS week_1_unique_users,
    SUM(week_2_unique_users) AS week_2_unique_users,
    SUM(week_3_unique_users) AS week_3_unique_users,
    SUM(week_4_unique_users) AS week_4_unique_users
FROM (
    (SELECT
        page_id,
        page_namespace,
        page_title,
        SUM(DATEDIFF(rcurr.rev_timestamp, first_revision) < 7) AS week_1_revisions, 
        SUM(DATEDIFF(rcurr.rev_timestamp, first_revision) BETWEEN 8 AND 13) AS week_2_revisions,
        SUM(DATEDIFF(rcurr.rev_timestamp, first_revision) BETWEEN 14 AND 20) AS week_3_revisions,
        SUM(DATEDIFF(rcurr.rev_timestamp, first_revision) BETWEEN 21 AND 27) AS week_4_revisions,
        SUM(
            IF(DATEDIFF(rcurr.rev_timestamp, first_revision) < 7, 
               CAST(rcurr.rev_len AS INT) - CAST(rprev.rev_len AS INT), 
               0)
        ) AS week_1_bytes,
        SUM(
            IF(DATEDIFF(rcurr.rev_timestamp, first_revision) BETWEEN 8 AND 13, 
               CAST(rcurr.rev_len AS INT) - CAST(rprev.rev_len AS INT), 
               0)
        ) AS week_2_bytes,
        SUM(
            IF(DATEDIFF(rcurr.rev_timestamp, first_revision) BETWEEN 14 AND 20, 
               CAST(rcurr.rev_len AS INT) - CAST(rprev.rev_len AS INT), 
               0)
        ) AS week_3_bytes,
        SUM(
            IF(DATEDIFF(rcurr.rev_timestamp, first_revision) BETWEEN 21 AND 27, 
               CAST(rcurr.rev_len AS INT) - CAST(rprev.rev_len AS INT), 
               0)
        ) AS week_4_bytes,
        COUNT(DISTINCT
            IF(DATEDIFF(rcurr.rev_timestamp, first_revision) < 7 AND rcurr.rev_user > 0,
               rcurr.rev_user_text, 
               NULL)
        ) AS week_1_unique_users,
        COUNT(DISTINCT
            IF(DATEDIFF(rcurr.rev_timestamp, first_revision) < 7 AND rcurr.rev_user = 0,
               rcurr.rev_user_text, 
               NULL)
        ) AS week_1_unique_anons,
        COUNT(DISTINCT
            IF(DATEDIFF(rcurr.rev_timestamp, first_revision) BETWEEN 8 AND 13 AND rcurr.rev_user > 0,
               rcurr.rev_user_text, 
               NULL)
        ) AS week_2_unique_users,
        COUNT(DISTINCT
            IF(DATEDIFF(rcurr.rev_timestamp, first_revision) BETWEEN 8 AND 13 AND rcurr.rev_user = 0,
               rcurr.rev_user_text, 
               NULL)
        ) AS week_2_unique_anons,
        COUNT(DISTINCT
            IF(DATEDIFF(rcurr.rev_timestamp, first_revision) BETWEEN 14 AND 20 AND rcurr.rev_user > 0,
               rcurr.rev_user_text, 
               NULL)
        ) AS week_3_unique_users,
        COUNT(DISTINCT
            IF(DATEDIFF(rcurr.rev_timestamp, first_revision) BETWEEN 14 AND 20 AND rcurr.rev_user = 0,
               rcurr.rev_user_text, 
               NULL)
        ) AS week_3_unique_anons,
        COUNT(DISTINCT
            IF(DATEDIFF(rcurr.rev_timestamp, first_revision) BETWEEN 21 AND 27 AND rcurr.rev_user > 0,
               rcurr.rev_user_text, 
               NULL)
        ) AS week_4_unique_users,
        COUNT(DISTINCT
            IF(DATEDIFF(rcurr.rev_timestamp, first_revision) BETWEEN 21 AND 27 AND rcurr.rev_user = 0,
               rcurr.rev_user_text, 
               NULL)
        ) AS week_4_unique_anons
    FROM halfak.nov13_limited_page
    INNER JOIN revision rcurr USE INDEX (page_timestamp) ON 
        rcurr.rev_page = page_id AND
        rcurr.rev_timestamp <= DATE_FORMAT(DATE_ADD(first_revision, INTERVAL 28 DAY), "%Y%m%d%H%i%S")
    LEFT JOIN revision rprev ON
        rcurr.rev_parent_id = rprev.rev_id
    GROUP BY 1,2,3)
    UNION
    (SELECT
        page_id,
        page_namespace,
        page_title,
        SUM(DATEDIFF(acurr.ar_timestamp, first_revision) < 7) AS week_1_revisions,
        SUM(DATEDIFF(acurr.ar_timestamp, first_revision) BETWEEN 8 AND 13) AS week_2_revisions,
        SUM(DATEDIFF(acurr.ar_timestamp, first_revision) BETWEEN 14 AND 20) AS week_3_revisions,
        SUM(DATEDIFF(acurr.ar_timestamp, first_revision) BETWEEN 21 AND 27) AS week_4_revisions,
        SUM(
            IF(DATEDIFF(acurr.ar_timestamp, first_revision) < 7, 
               CAST(acurr.ar_len AS INT) - CAST(aprev.ar_len AS INT), 
               0)
        ) AS week_1_bytes,
        SUM(
            IF(DATEDIFF(acurr.ar_timestamp, first_revision) BETWEEN 8 AND 13, 
               CAST(acurr.ar_len AS INT) - CAST(aprev.ar_len AS INT), 
               0)
        ) AS week_2_bytes,
        SUM(
            IF(DATEDIFF(acurr.ar_timestamp, first_revision) BETWEEN 14 AND 20, 
               CAST(acurr.ar_len AS INT) - CAST(aprev.ar_len AS INT), 
               0)
        ) AS week_3_bytes,
        SUM(
            IF(DATEDIFF(acurr.ar_timestamp, first_revision) BETWEEN 21 AND 27, 
               CAST(acurr.ar_len AS INT) - CAST(aprev.ar_len AS INT), 
               0)
        ) AS week_4_bytes,
        COUNT(DISTINCT
            IF(DATEDIFF(acurr.ar_timestamp, first_revision) < 7 AND acurr.ar_user > 0,
               acurr.ar_user_text, 
               NULL)
        ) AS week_1_unique_users,
        COUNT(DISTINCT
            IF(DATEDIFF(acurr.ar_timestamp, first_revision) < 7 AND acurr.ar_user = 0,
               acurr.ar_user_text, 
               NULL)
        ) AS week_1_unique_anons,
        COUNT(DISTINCT
            IF(DATEDIFF(acurr.ar_timestamp, first_revision) BETWEEN 8 AND 13 AND acurr.ar_user > 0,
               acurr.ar_user_text, 
               NULL)
        ) AS week_2_unique_users,
        COUNT(DISTINCT
            IF(DATEDIFF(acurr.ar_timestamp, first_revision) BETWEEN 8 AND 13 AND acurr.ar_user = 0,
               acurr.ar_user_text, 
               NULL)
        ) AS week_2_unique_anons,
        COUNT(DISTINCT
            IF(DATEDIFF(acurr.ar_timestamp, first_revision) BETWEEN 14 AND 20 AND acurr.ar_user > 0,
               acurr.ar_user_text, 
               NULL)
        ) AS week_3_unique_users,
        COUNT(DISTINCT
            IF(DATEDIFF(acurr.ar_timestamp, first_revision) BETWEEN 14 AND 20 AND acurr.ar_user = 0,
               acurr.ar_user_text, 
               NULL)
        ) AS week_3_unique_anons,
        COUNT(DISTINCT
            IF(DATEDIFF(acurr.ar_timestamp, first_revision) BETWEEN 21 AND 27 AND acurr.ar_user > 0,
               acurr.ar_user_text, 
               NULL)
        ) AS week_4_unique_users,
        COUNT(DISTINCT
            IF(DATEDIFF(acurr.ar_timestamp, first_revision) BETWEEN 21 AND 27 AND acurr.ar_user = 0,
               acurr.ar_user_text, 
               NULL)
        ) AS week_4_unique_anons
    FROM halfak.nov13_limited_page
    INNER JOIN archive acurr USE INDEX (page_timestamp) ON 
        acurr.ar_page_id = page_id AND
        acurr.ar_timestamp <= DATE_FORMAT(DATE_ADD(first_revision, INTERVAL 28 DAY), "%Y%m%d%H%i%S")
    LEFT JOIN archive aprev ON
        acurr.ar_parent_id = aprev.ar_rev_id
    GROUP BY 1,2,3)
) AS unioned_page_stats
GROUP BY 1,2,3;

