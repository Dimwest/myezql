CREATE TABLE src_tab_15 AS
SELECT
    src_tab_16.col_1,
    src_tab_17.col_2,
    src_tab_18.col_3
FROM src_tab_16
LEFT JOIN src_tab_17 ON src_tab_16.col_4 = src_tab_17.col_4
LEFT JOIN src_tab_18 ON src_tab_16.col_5 = src_tab_18.col_5
;
