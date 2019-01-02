INSERT INTO mytable (col_1, col_2, col_3, col_4, col_5,
                                  col_6, col_7)
SELECT tab_1.id AS col_1,
       tab_1.col_2,
       tab_1.col_3,
       tab_1.col_4,
       COUNT(DISTINCT(tab_2.col_5)) AS col_5,
       SUM(ifnull(tab_3.col_6, 0)) AS col_6,
       SUM(ifnull(tab_3.col_7, 0)) AS col_7
FROM src_tab_1 tab_1
 JOIN src_tab_2 tab_2
  USING (col_1)
 LEFT JOIN src_tab_3 tab_3
  ON tab_3.col_2 = 1
  AND tab_1.id = tab_3.col_1
WHERE tab_1.col_2 = var
GROUP BY 1, 2, 3, 4

;
