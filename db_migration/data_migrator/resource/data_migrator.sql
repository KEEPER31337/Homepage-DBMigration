USE {dstDB};

INSERT INTO
    member (
        id,
        login_id,
        email_address,
        password,
        real_name,
        nick_name,
        birthday,
        student_id,
        register_date,
        point)
SELECT
        m.member_srl,
        m.user_id,
        m.email_address,
        m.password,
        m.user_name,
        m.nick_name,
        IF(m.birthday<>"" AND m.birthday<>0 ,m.birthday,NULL),
        m.student_number,
        m.regdate,
        p.point
FROM {srcDB}.xe_member AS m

LEFT JOIN {srcDB}.xe_point AS p
ON m.member_srl = p.member_srl;

INSERT INTO
    category (
        id,
        name,
        parent_id
    )
SELECT
        module_srl,
        name,
        module_parent_srl
FROM {srcDB}.new_category;

INSERT INTO
    posting (
        id,
        title,
        content,
        member_id,
        visit_count,
        like_count,
        dislike_count,
        comment_count,
        register_time,
        update_time,
        ip_address,
        allow_comment,
        is_notice,
        is_secret,
        is_temp,
        password,
        category_id
    )
SELECT
        d.document_srl,
        d.title,
        IFNULL(d.clean_content,"."),
        IFNULL(m.member_srl,1),
        d.readed_count,
        d.voted_count,
        d.blamed_count,
        d.comment_count,
        d.regdate,
        d.last_update,
        d.ipaddress,
        IF(d.comment_status="ALLOW",TRUE,FALSE),
        IF(d.is_notice="Y",TRUE,FALSE),
        IF(d.status="SECRET",TRUE,FALSE),
        IF(d.status="TEMP",TRUE,FALSE),
        d.password,
        d.module_srl
FROM {srcDB}.xe_documents AS d

LEFT JOIN {srcDB}.xe_member AS m
ON d.member_srl = m.member_srl

INNER JOIN {srcDB}.new_category AS n
ON d.module_srl = n.module_srl;

INSERT INTO
    comment (
        id,
        content,
        register_time,
        update_time,
        ip_address,
        like_count,
        dislike_count,
        parent_id,
        member_id,
        posting_id
    )
SELECT
        c.comment_srl,
        IFNULL(c.clean_content,"."),
        c.regdate,
        c.last_update,
        c.ipaddress,
        c.voted_count,
        c.blamed_count,
        0,
        IFNULL(m.member_srl,1),
        c.document_srl
FROM {srcDB}.xe_comments AS c

LEFT JOIN {srcDB}.xe_member AS m
ON c.member_srl = m.member_srl

INNER JOIN {srcDB}.xe_documents AS d
ON c.document_srl = d.document_srl;

INSERT INTO
    file (
        id,
        file_name,
        file_path,
        file_size,
        upload_time,
        ip_address,
        posting_id
    )
SELECT
        f.file_srl,
        f.source_filename,
        f.uploaded_filename,
        f.file_size,
        f.regdate,
        f.ipaddress,
		d.document_srl
FROM {srcDB}.xe_files AS f

LEFT JOIN {srcDB}.xe_documents AS d
ON f.upload_target_srl = d.document_srl;


INSERT INTO
    attendance(
        id,
        time,
        date,
        member_id,
        point,
        random_point,
        ip_address,
        greetings,
        continuous_day
    )
SELECT
        attendance_srl,
        regdate,
        date_format(regdate,'%Y-%m-%d'),
        member_srl,
        today_point,
        today_random,
        ipaddress,
        IF(greetings="^auto^","자동 출석입니다.",greetings),
        IFNULL(a_continuity,0)
FROM {srcDB}.xe_attendance;
