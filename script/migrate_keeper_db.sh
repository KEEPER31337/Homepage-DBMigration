#!/bin/bash

# make sure your mysql service is running
pip3 install -r requirements.txt
python3 setup.py develop

# run old DB dump
# mysql -u root -p < resource/dump/keeper_dump.sql

# copy old DB tables
echo "*Copying old DB tables..."
mysql -u root -p < resource/keeper_copy_setter.sql

# run new DB init.sql
echo "*Runnning new DB init.sql..."
mysql -u root -p < resource/new_init/keeper_new_init.sql

# delete new DB init category table rows
echo "*Removing new DB init category table rows..."
mysql -u root -p -e "DELETE FROM keeper_new.category;"

# fill right DB name at db_migration/__main__.py
# run main module
echo "*Running main module..."
python3 db_migration

# Duplicated equipment merging

# Remove copy & old db.
# echo "*Removing copy & old db..."
# mysql -u root -p -e "DROP DATABASE keeper; DROP DATABASE keeper_copy;"