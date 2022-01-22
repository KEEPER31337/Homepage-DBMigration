USE migration_test;
CREATE TABLE intee(int_val int);
CREATE TABLE bigintee(bigint_val bigint);

INSERT INTO intee VALUES(2);
INSERT INTO intee VALUES(5);
INSERT INTO intee VALUES(0);
INSERT INTO intee VALUES(166556);
INSERT INTO intee VALUES(100000000);
SELECT * FROM intee;

INSERT INTO `bigintee` (bigint_val) SELECT int_val FROM `intee`;

SELECT * FROM bigintee;