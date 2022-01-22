CREATE TABLE member_has_member_job (member_id int, member_job_id int);

INSERT INTO member_has_member_job
 (SELECT t1.member_srl AS member_id, t2.group_srl AS member_job_id FROM xe_member_group_member as t1, xe_member_group as t2
 WHERE t1.group_srl = t2.group_srl AND 
 (t1.group_srl = 34131 OR # 대외부장
  t1.group_srl = 34599 OR # 학술부장
  t1.group_srl = 34600 OR # 전산관리자
  t1.group_srl = 34601 OR # 서기
  t1.group_srl = 34602 OR # 총무
  t1.group_srl = 34603 OR # 회장
  t1.group_srl = 53180 OR # 부회장
  t1.group_srl = 75521    # 사서
 ));

UPDATE member_has_member_job SET member_job_id = 1 WHERE member_job_id = 34603; # 회장



