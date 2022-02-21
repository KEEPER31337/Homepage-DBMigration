#!/bin/bash

pip install -r requirements.txt
mysql -u root -p < resource/keeper_copy_setter.sql
# mysql -u root -p < resource/init.sql
# Remove category default values
python db_migration
# Category matching
# Duplicated equipment merging