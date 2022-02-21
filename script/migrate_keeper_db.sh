#!/bin/bash

pip3 install -r requirements.txt
python3 setup.py develop

# 구 DB명 바꿔서 dump 적용
# copy DB set
mysql -u root -p < resource/keeper_copy_setter.sql

# 신 DB init.sql의 category 기본값 삭제
# 신 DB init.sql을 resource/로 옮기기
mysql -u root -p < resource/keeper_new_init.sql

# db_migration/__main__.py에서 copy DB명, 신 DB명 맞추기
python3 db_migration

# Duplicated equipment merging
# 구 DB 및 copy DB삭제