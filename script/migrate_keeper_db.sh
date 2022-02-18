#!/bin/bash

mysql -u root -p < script/keeper_copy_setter.sql
# mysql -u root -p < script/init.sql
# Remove category default values
python db_migration
# Category matching