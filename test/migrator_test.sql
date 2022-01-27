INSERT INTO
    `member` (
        id,
        login_id,
        email_address,
        password,
        real_name,
        nick_name,
        birth_day,
        register_date
    )
SELECT
    (
        member_srl,
        user_id,
        email_address,
        password,
        user_name,
        nick_name,
        birthday,
        extravars,
        regdate
    )
FROM
    `xe_member`;