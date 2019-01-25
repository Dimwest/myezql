DELIMITER ;;

DROP PROCEDURE IF EXISTS example.testproc;;
CREATE PROCEDURE example.testproc(IN test_arg int unsigned)

  fetchproc: BEGIN

  DECLARE var BOOLEAN DEFAULT TRUE;

  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    DO RELEASE_LOCK('lock_test');

    GET DIAGNOSTICS CONDITION 1 @p1 = RETURNED_SQLSTATE, @p2 = MESSAGE_TEXT;
    SET @msg = (SELECT CONCAT_WS('', 'ERROR! ', @p1, ':', @p2, ', at ', NOW()));
    CALL log(
        "testproc",
        @msg,
        thread_id,
        "ERROR"
    );
    RESIGNAL SET MESSAGE_TEXT = @msg;
  END;

  SET var = TRUE;

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

  REPLACE INTO mytable (col_1, col_2, col_3, col_4, col_5,
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


  UPDATE src_tab_8 tab_8
  JOIN src_tab_9 tab_9
  USING (col_1, col_2)
  SET tab_8.col_3 = tab_9.col4,
      tab_8.col_4 = tab_9.col5
  WHERE tab_8.col_6 > 0;

  DELETE FROM src_tab_10 tab_10 WHERE col_1 < 100;

  TRUNCATE TABLE src_tab_11;

  DROP TABLE IF EXISTS src_tab_12;

END

;;
