mongoimport --db POTUS --collection col1 --file 2016-11-08-20-01_Utah.txt  --host replica-set/172.31.31.100:27017,172.31.31.101:27017,172.31.31.102:27017 --fields DATE,STATE,CANDIDATE --type csv
