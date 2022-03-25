DELIMITER $$
CREATE PROCEDURE all_attend()
BEGIN

    DECLARE attend_day DATE DEFAULT "2022-03-16"; # Server stop date.

    DELETE FROM attendance WHERE date BETWEEN attend_day AND CURRENT_DATE(); # Delete exist rows.

    WHILE(attend_day <= CURRENT_DATE()) DO # Until current date

    INSERT INTO `attendance` (`time`,`date`,`ip_address`, `point`,`continuous_day`, `member_id`,`greetings`)
    SELECT attend_day, attend_day,
        "1.1.1.1",
        0,
        IFNULL(t1.continuous_day,0)+1,
        t2.id, # Get only exist member id.
        "서버교체에 따른 출석처리"
    FROM attendance AS t1 RIGHT JOIN member AS t2
        ON t1.member_id = t2.id AND t1.date = attend_day-1
    WHERE t2.id <> 1; # Except virtual member.

    SET attend_day = attend_day + 1;

    END WHILE;

END$$
DELIMITER ;

CALL all_attend();

DROP PROCEDURE all_attend;
