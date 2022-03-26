
# Rows to update
UPDATE posting SET member_id = 1 WHERE member_id IN (SELECT id FROM member WHERE member_type_id = 5);
UPDATE book_borrow_info SET member_id = 1 WHERE member_id IN (SELECT id FROM member WHERE member_type_id = 5);
UPDATE equipment_borrow_info SET member_id = 1 WHERE member_id IN (SELECT id FROM member WHERE member_type_id = 5);
UPDATE point_log SET presented = 1 WHERE presented IN (SELECT id FROM member WHERE member_type_id = 5);
UPDATE comment SET member_id = 1 WHERE member_id IN (SELECT id FROM member WHERE member_type_id = 5);
UPDATE study SET head_member_id = 1 WHERE head_member_id IN (SELECT id FROM member WHERE member_type_id = 5);

# Rows to delete
DELETE FROM attendance WHERE member_id IN (SELECT id FROM member WHERE member_type_id = 5);
DELETE FROM point_log WHERE member_id IN (SELECT id FROM member WHERE member_type_id = 5);

# N:M tables
DELETE FROM study_has_member WHERE member_id IN (SELECT id FROM member WHERE member_type_id = 5);
DELETE FROM member_has_member_job WHERE member_id IN (SELECT id FROM member WHERE member_type_id = 5);
DELETE FROM friend WHERE follower IN (SELECT id FROM member WHERE member_type_id = 5);
DELETE FROM friend WHERE followee IN (SELECT id FROM member WHERE member_type_id = 5);
DELETE FROM member_has_posting_like WHERE member_id IN (SELECT id FROM member WHERE member_type_id = 5);
DELETE FROM member_has_posting_dislike WHERE member_id IN (SELECT id FROM member WHERE member_type_id = 5);
DELETE FROM member_has_comment_like WHERE member_id IN (SELECT id FROM member WHERE member_type_id = 5);
DELETE FROM member_has_comment_dislike WHERE member_id IN (SELECT id FROM member WHERE member_type_id = 5);


# DELETE OR UPDATE
DELETE FROM member WHERE id IN (SELECT id FROM (SELECT id FROM member WHERE member_type_id = 5) AS temp);
/* 
SELECT title FROM posting WHERE member_id IN (SELECT id FROM member WHERE member_type_id = 5);
SELECT t1.title,t2.real_name FROM posting AS t1 JOIN member AS t2 ON t1.member_id = t2.id WHERE member_id IN (SELECT id FROM member WHERE member_type_id = 5);
*/