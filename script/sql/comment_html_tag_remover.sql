/* SELECT REGEXP_REPLACE(content, '<[^>]+>', ''), content FROM comment\G */
UPDATE comment SET content = REGEXP_REPLACE(content, '<[^>]+>', '');