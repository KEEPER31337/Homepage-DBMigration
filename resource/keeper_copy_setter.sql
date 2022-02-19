DROP DATABASE IF EXISTS keeper_copy;

CREATE DATABASE keeper_copy;

CREATE TABLE keeper_copy.xe_comments (SELECT * FROM keeper.xe_comments);
CREATE TABLE keeper_copy.xe_documents (SELECT * FROM keeper.xe_documents);
CREATE TABLE keeper_copy.xe_member (SELECT * FROM keeper.xe_member);
CREATE TABLE keeper_copy.xe_member_group (SELECT * FROM keeper.xe_member_group);
CREATE TABLE keeper_copy.xe_member_group_member (SELECT * FROM keeper.xe_member_group_member);
CREATE TABLE keeper_copy.xe_menu_item (SELECT * FROM keeper.xe_menu_item);
CREATE TABLE keeper_copy.xe_modules (SELECT * FROM keeper.xe_modules);
CREATE TABLE keeper_copy.xe_point (SELECT * FROM keeper.xe_point);
CREATE TABLE keeper_copy.xe_files (SELECT * FROM keeper.xe_files);
CREATE TABLE keeper_copy.xe_attendance (SELECT * FROM keeper.xe_attendance);