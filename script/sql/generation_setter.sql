UPDATE member SET generation = YEAR(register_date) - 2009 + IF(MONTH(register_date) > 7, 0.5, 0);

UPDATE member SET generation = CASE id
    WHEN 186 THEN 0
    WHEN 3675 THEN 0
    WHEN 5908 THEN 0
    WHEN 156 THEN 1
    WHEN 248 THEN 1
    WHEN 139 THEN 1
    WHEN 307 THEN 1
    WHEN 197 THEN 2
    WHEN 4 THEN 2
    WHEN 188 THEN 2
    WHEN 918 THEN 3
    WHEN 1755 THEN 3

    ELSE generation
END;