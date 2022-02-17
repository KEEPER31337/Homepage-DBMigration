USE keeper_new;

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
        m.student_id,
        m.regdate,
        p.point
FROM keeper.xe_member AS m
LEFT JOIN keeper.xe_point AS p
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
FROM keeper.new_category;


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
        document_srl,
        title,
        IFNULL(clean_content,"."),
        member_srl,
        readed_count,
        voted_count,
        blamed_count,
        comment_count,
        regdate,
        last_update,
        ipaddress,
        IF(comment_status="ALLOW",TRUE,FALSE),
        IF(is_notice="Y",TRUE,FALSE),
        IF(status="SECRET",TRUE,FALSE),
        IF(status="TEMP",TRUE,FALSE),
        password,
        module_srl
FROM keeper.xe_documents;

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
        comment_srl,
        IFNULL(clean_content,"."),
        regdate,
        last_update,
        ipaddress,
        voted_count,
        blamed_count,
        parent_srl,
        member_srl,
        document_srl
FROM keeper.xe_comments;

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
        file_srl,
        source_filename,
        uploaded_filename,
        file_size,
        regdate,
        ipaddress,
        upload_target_srl
FROM keeper.xe_files;


INSERT INTO
    attendance(
        id,
        time,
        member_id,
        point,
        random_point,
        ip_address,
        greetings,
        continous_day
    )
SELECT
        attendance_srl,
        regdate,
        member_srl,
        today_point,
        today_random,
        ipaddress,
        greetings,
        IFNULL(a_continuity,0)
FROM keeper.xe_attendance;