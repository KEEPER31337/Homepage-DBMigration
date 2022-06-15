SELECT DISTINCT t1.id,t1.name,t1.parent_id,t3.name,t3.parent_id,t4.name,t4.parent_id,t5.name
    FROM category AS t1 
    INNER JOIN posting AS t2 ON t1.id = t2.category_id 
    LEFT JOIN category AS t3 ON t1.parent_id = t3.id 
    LEFT JOIN category AS t4 ON t3.parent_id = t4.id 
    LEFT JOIN category AS t5 ON t4.parent_id=t5.id 
    WHERE t1.id NOT IN(1,2,3,5,6,8,9,10,27,105,116,117,219,508,647,648,662,1377,2996,5125,6105,11302,23400,29422,30052,33777,34608,60024,63908,81570,84493,105900,106402,147718,5424,69250,97142,147785);


SELECT DISTINCT t1.id
    FROM category AS t1 
    INNER JOIN posting AS t2 ON t1.id = t2.category_id 
    JOIN category AS t3 ON t1.parent_id = t3.id 
    LEFT JOIN category AS t4 ON t3.parent_id = t4.id 
    LEFT JOIN category AS t5 ON t4.parent_id=t5.id 
    WHERE t1.id NOT IN(1,2,3,5,6,8,9,10,27,105,116,117,219,508,647,648,662,1377,2996,5125,6105,11302,23400,29422,30052,33777,34608,60024,63908,81570,84493,105900,106402,147718,5424,69250,97142,147785);

SELECT c.name, p.category_id, COUNT(p.title) 
    FROM posting AS p 
    JOIN category AS c 
    ON p.category_id = c.id 
    WHERE p.category_id NOT IN(1,2,3,5,6,8,9,10,27,105,116,117,219,508,647,648,662,1377,2996,5125,6105,11302,23400,29422,30052,33777,34608,60024,63908,81570,84493,105900,106402,147718,5424,69250,97142,147785)
    GROUP BY p.category_id;

SELECT p.category_id,t1.name,t3.name,t4.name,t5.name, COUNT(p.title)
    FROM posting AS p 
    LEFT JOIN category AS t1 ON p.category_id = t1.id 
    LEFT JOIN category AS t3 ON t1.parent_id = t3.id 
    LEFT JOIN category AS t4 ON t3.parent_id = t4.id 
    LEFT JOIN category AS t5 ON t4.parent_id = t5.id 
    WHERE p.category_id NOT IN(1,2,3,5,6,8,9,10,27,105,116,117,219,508,647,648,662,1377,2996,5125,6105,11302,23400,29422,30052,33777,34608,60024,63908,81570,84493,105900,106402,147718,5424,69250,97142,147785)
    GROUP BY p.category_id;


SELECT id, name FROM category WHERE id NOT IN(1,2,3,5,6,8,9,10,27,105,116,117,219,508,647,648,662,1377,2996,5125,6105,11302,23400,29422,30052,33777,34608,60024,63908,81570,84493,105900,106402,147718,5424,69250,97142,147785);

4942
4930
4891
4944

UPDATE posting AS p
    JOIN category AS t1 ON p.category_id = t1.id
    SET p.title=CONCAT(CONCAT_WS(t1.name,"[","]"),p.title)
    WHERE p.category_id IN(4942,4930,4891,4944);

UPDATE posting AS p
    JOIN category AS t1 ON p.category_id = t1.id
    SET p.category_id=2996
    WHERE p.category_id IN(4942,4930,4891,4944);

SELECT CONCAT(CONCAT_WS(t1.name,"[","]"),p.title)
    FROM posting AS p 
    LEFT JOIN category AS t1 ON p.category_id = t1.id
    WHERE p.category_id IN(4942,4930,4891,4944);

SELECT p.title, t1.name
    FROM posting AS p 
    LEFT JOIN category AS t1 ON p.category_id = t1.id
    WHERE p.category_id IN(4942,4930,4891,4944);

SELECT p.category_id,t1.name,t3.name,t4.name,t5.name,COUNT(p.title)
    FROM posting AS p 
    LEFT JOIN category AS t1 ON p.category_id = t1.id 
    LEFT JOIN category AS t3 ON t1.parent_id = t3.id 
    LEFT JOIN category AS t4 ON t3.parent_id = t4.id 
    LEFT JOIN category AS t5 ON t4.parent_id = t5.id 
    WHERE p.category_id IN(4942,4930,4891,4944)
    GROUP BY p.category_id;

5144,
5470,
6217,
6919,
6640,
6211,
6220,
6207,
6209,
6881,
6215,
7751,
8638,
12103,
12107,
12105,
12126,
22417,
23554,
27027,
27057,
34303,
34299,
34293,
34301,
34295,
34297,
67320,
35090,
36061,
37840,
55906,
55904,
55900,
55902,
55908,
55910,
55912,
56711,
67368,
67349,
61372

110724,
110720,
110726

36448



SELECT p.category_id,t1.name,t3.name,t4.name,t5.name,COUNT(p.title)
    FROM posting AS p 
    LEFT JOIN category AS t1 ON p.category_id = t1.id 
    LEFT JOIN category AS t3 ON t1.parent_id = t3.id 
    LEFT JOIN category AS t4 ON t3.parent_id = t4.id 
    LEFT JOIN category AS t5 ON t4.parent_id = t5.id 
    WHERE p.category_id IN (5144,5470,6217,6919,6640,6211,6220,6207,6209,6881,6215,7751,8638,12103,12107,12105,12126,22417,23554,27027,27057,34303,34299,34293,34301,34295,34297,67320,35090,36448,36061,37840,55906,55904,55900,55902,55908,55910,55912,56711,67368,67349,61372,110724,110720,110726)
    GROUP BY p.category_id;

SELECT CONCAT(CONCAT(CONCAT_WS(t3.name,"[","]"),CONCAT_WS(t1.name,"[","]")),p.title) AS T
    FROM posting AS p 
    LEFT JOIN category AS t1 ON p.category_id = t1.id
    LEFT JOIN category AS t3 ON t1.parent_id = t3.id 
    WHERE p.category_id IN(5144,5470,6217,6919,6640,6211,6220,6207,6209,6881,6215,7751,8638,12103,12107,12105,12126,22417,23554,27027,27057,34303,34299,34293,34301,34295,34297,67320,35090,36061,37840,55906,55904,55900,55902,55908,55910,55912,56711,67368,67349,61372);

UPDATE posting AS p 
    LEFT JOIN category AS t1 ON p.category_id = t1.id 
    LEFT JOIN category AS t3 ON t1.parent_id = t3.id 
    SET p.title=CONCAT(CONCAT(CONCAT_WS(t3.name,"[","]"),CONCAT_WS(t1.name,"[","]")),p.title),
        p.category_id=5424
    WHERE p.category_id IN(5144,5470,6217,6919,6640,6211,6220,6207,6209,6881,6215,7751,8638,12103,12107,12105,12126,22417,23554,27027,27057,34303,34299,34293,34301,34295,34297,67320,35090,36061,37840,55906,55904,55900,55902,55908,55910,55912,56711,67368,67349,61372);

SELECT CONCAT(
    CONCAT(
        CONCAT_WS(t4.name,"[","]"),
        CONCAT(
            CONCAT_WS(t3.name,"[","]"),
            CONCAT_WS(t1.name,"[","]"))
        )
        ,p.title) AS T
    FROM posting AS p 
    LEFT JOIN category AS t1 ON p.category_id = t1.id
    LEFT JOIN category AS t3 ON t1.parent_id = t3.id 
    LEFT JOIN category AS t4 ON t3.parent_id = t4.id 
    WHERE p.category_id IN(110724,110720,110726);

UPDATE posting AS p 
    LEFT JOIN category AS t1 ON p.category_id = t1.id 
    LEFT JOIN category AS t3 ON t1.parent_id = t3.id 
    LEFT JOIN category AS t4 ON t3.parent_id = t4.id 
    SET p.title=
        CONCAT(
            CONCAT(
                CONCAT_WS(t4.name,"[","]"),
                CONCAT(
                    CONCAT_WS(t3.name,"[","]"),
                    CONCAT_WS(t1.name,"[","]"))
                )
            ,p.title),
        p.category_id=5424
    WHERE p.category_id IN(110724,110720,110726);

UPDATE posting AS p 
    LEFT JOIN category AS t1 ON p.category_id = t1.id 
    SET p.title=CONCAT(CONCAT_WS(t1.name,"[","]"),p.title),
        p.category_id=5424
    WHERE p.category_id IN(36448);

SELECT CONCAT(CONCAT_WS(t1.name,"[","]"),p.title)
    FROM posting AS p 
    LEFT JOIN category AS t1 ON p.category_id = t1.id
    WHERE p.category_id IN(36448);

    6837

27471,
66091,
68251


SELECT name FROM category WHERE id IN (6837,
27471,
66091,
68251)

SELECT p.category_id,t1.name,t3.name,t4.name,t5.name,COUNT(p.title)
    FROM posting AS p 
    LEFT JOIN category AS t1 ON p.category_id = t1.id 
    LEFT JOIN category AS t3 ON t1.parent_id = t3.id 
    LEFT JOIN category AS t4 ON t3.parent_id = t4.id 
    LEFT JOIN category AS t5 ON t4.parent_id = t5.id 
    WHERE p.category_id IN (6837,27471,66091,68251)
    GROUP BY p.category_id;

SELECT CONCAT(CONCAT_WS(t1.name,"[","]"),p.title)
    FROM posting AS p 
    LEFT JOIN category AS t1 ON p.category_id = t1.id
    WHERE p.category_id IN(6837,27471,66091,68251);



