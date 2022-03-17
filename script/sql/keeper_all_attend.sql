/* INSERT INTO `attendance` (`ip_address`, `continuous_day`, `member_id`) VALUES ('1.1.1.1', 1, 1); */

INSERT INTO `attendance` (`date`,`ip_address`, `point`,`continuous_day`, `member_id`)
    SELECT "2022-03-16",0,IFNULL(t1.continuous_day,0)+1,t2.real_name
    FROM attendance AS t1 RIGHT JOIN member AS t2
        ON t1.member_id = t2.id AND t1.date = "2022-03-15" 
    WHERE t2.id <> 1;

INSERT INTO `attendance` (`date`,`ip_address`, `point`,`continuous_day`, `member_id`)
    SELECT "2022-03-17",0,IFNULL(t1.continuous_day,0)+1,t2.real_name
    FROM attendance AS t1 RIGHT JOIN member AS t2
        ON t1.member_id = t2.id AND t1.date = "2022-03-16" 
    WHERE t2.id <> 1;
    