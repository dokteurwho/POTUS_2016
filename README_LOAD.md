## Chargement des fichiers dans la base via mongoimport ##

### Python c'est pas bon ###
Sur les machines minimales de Amazon l'utilisation de python + panda + pymongo pour charger la base donne de mauvaises performances.
Typiquement:
* 3.3 secondes pour 100 000 records.
* Soit théoriquement plus d'une heure pour la base entière.

En revanche python permet de consulter efficacement l'état de la base.

## Utilisation de mongoimport ##

Donc on utilise mongoimport. Commme il n'accepte que des fichier csv séparés par des virgules
il convient transformer les fichiers si ce n'est pas déjà fait.

La commande ci-dessous permet de faire cette conversion pour un fichier, qui est très rapide.

```c
sed -i -e "s/;/,/g" 2016-11-08-20-04_Californie.txt
```

Ensuite il reste à charger le contenu du fichier avec la commande __mongoimport__.

Voici le résultat sur deux états. En particulier la Californie avec 14 Mn de votants.

Pour cet état il aura fallu environ 7 minutes (machine t2.micro).

Le nom et les ip du replica peuvent changer ...

```c
[ec2-user@ip-172-31-20-191 data_POTUS]$
[ec2-user@ip-172-31-20-191 data_POTUS]$
[ec2-user@ip-172-31-20-191 data_POTUS]$  mongoimport --db POTUS --collection election --file 2016-11-08-20-00_Minnesota.txt  --host replica-set/172.31.31.100:27017,172.31.31.101:27017,172.31.31.102:27017 --fields DATE,STATE,CANDIDATE --type csv
2017-01-12T16:46:21.556+0000	connected to: replica-set/172.31.31.100:27017,172.31.31.101:27017,172.31.31.102:27017
2017-01-12T16:46:24.553+0000	[........................] POTUS.election	2.7 MB/95.7 MB (2.8%)
2017-01-12T16:46:27.547+0000	[#.......................] POTUS.election	5.3 MB/95.7 MB (5.6%)

2017-01-12T16:48:00.549+0000	[######################..] POTUS.election	90.6 MB/95.7 MB (94.7%)
2017-01-12T16:48:03.551+0000	[#######################.] POTUS.election	93.5 MB/95.7 MB (97.8%)
2017-01-12T16:48:06.182+0000	imported 2944813 documents
[ec2-user@ip-172-31-20-191 data_POTUS]
[ec2-user@ip-172-31-20-191 data_POTUS]$ sed -i -e "s/;/,/g" 2016-11-08-20-04_Californie.txt
[ec2-user@ip-172-31-20-191 data_POTUS]$ mongoimport --db POTUS --collection election --file 2016-11-08-20-04_Californie.txt  --host replica-set/172.31.31.100:27017,172.31.31.101:27017,172.31.31.102:27017 --fields DATE,STATE,CANDIDATE --type csv
2017-01-12T16:55:54.050+0000	connected to: replica-set/172.31.31.100:27017,172.31.31.101:27017,172.31.31.102:27017
2017-01-12T16:55:57.048+0000	[........................] POTUS.election	3.1 MB/491.5 MB (0.6%)
2017-01-12T16:56:00.048+0000	[........................] POTUS.election	5.8 MB/491.5 MB (1.2%)

2017-01-12T17:05:45.048+0000	[#######################.] POTUS.election	488.5 MB/491.5 MB (99.4%)
2017-01-12T17:05:48.048+0000	[#######################.] POTUS.election	490.8 MB/491.5 MB (99.9%)
2017-01-12T17:05:49.189+0000	imported 14610499 documents
[ec2-user@ip-172-31-20-191 data_POTUS]$
```
