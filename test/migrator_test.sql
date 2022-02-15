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
        register_date)
SELECT
        member_srl,
        user_id,
        email_address,
        password,
        user_name,
        nick_name,
        IF(birthday<>"" AND birthday<>0 ,birthday,NULL),
        student_id,
        regdate
FROM keeper.xe_member;


INSERT INTO
    posting (
        id,
        title,
        clean_content,
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
    (
        document_srl,
        title,
        content,
        member_srl,
        readed_count,
        voted_count,
        blamed_count,
        comment_count,
        regdate,
        last_update,
        ipaddress,
        IF(comment_status="ALLOW",),
        is_notice,
        IF(status="SECRET",TRUE,FALSE),
        IF(status="TEMP",TRUE,FALSE),
        password,
        module_srl
    )
FROM keeper.xe_documents;

INSERT INTO
    comment (
        id,
        clean_content,
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
    (
        comment_srl,
        content,
        regdate,
        last_update,
        ipaddress,
        voted_count,
        blamed_count,
        parent_srl,
        member_srl,
        document_srl
    )
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
    (
        file_srl,
        source_filename,
        uploaded_filename,
        file_size,
        regdate,
        ipaddress,
        upload_target_srl
    )
FROM keeper.xe_files;

INSERT INTO
    category (
        id,
        name,
        parent_id
    )
SELECT
    (
        module_srl,
        browser_title,
        new_parent_srl
    )
FROM keeper.xe_modules;

INSERT INTO
    books (
        id,
        title,
        author
    )
SELECT
    (
        number,
        name,
        author
    )
FROM Library.books;

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
    (
        attendance_srl,
        regdate,
        member_srl,
        today_point,
        random_point,
        ipaddress,
        greetings,
        a_continuity
    )
FROM keeper.attendance;