UPDATE src_tab_8 tab_8
JOIN src_tab_9 tab_9
USING (col_1, col_2)
SET tab_8.col_3 = tab_9.col4,
    tab_8.col_4 = tab_9.col5
WHERE tab_8.col_6 > 0;