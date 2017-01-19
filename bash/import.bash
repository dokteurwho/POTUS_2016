#!/bin/bash -v


filename=$1
colname=$2
mongoimport --db POTUS --collection $colname  --file $filename --host replica-set/172.31.31.100:27017,172.31.31.101:27017,172.31.31.102:27017 --fields DATE,STATE,CANDIDATE --type csv
exit 0
