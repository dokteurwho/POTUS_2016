## Copier les données (zippées) vers AWS

### ZIP is your friend

* Le zip original pèse 12 mb, dézipé il fait 5 gb ... il vaut mieux envoyer le zip sur AWS et le dézipper sur AWS.

* Le fichier orginal data.gzip se décompresse de manière incorrecte sur ubuntu.

* Le plus simple est de re-ziper les donner au format zip, puis de les transférer sur la machine cible pour les décompresser.

### Copier le ZIP vers AWS

Depuis votre machine (pas AWS) transférer les données:


```c
>scp -i "AWS_02.pem" /Users/rom/Downloads/data_POTUS.zip ec2-user@ec2-54-93-44-107.eu-central-1.compute.amazonaws.com:/home/ec2-user/POTUS
data_POTUS.zip            
```
Puis connexion vers AWS:

```c
> ssh -i "AWS_02.pem" ec2-user@ec2-54-93-44-107.eu-central-1.compute.amazonaws.com
```

Et enfin on dézippe ...

```c
[ec2-user@ip-172-31-20-191 ~]$ ls
anaconda3  Anaconda3-4.0.0-Linux-x86_64.sh  certificates  POTUS
[ec2-user@ip-172-31-20-191 ~]$ pwd
/home/ec2-user
[ec2-user@ip-172-31-20-191 ~]$ ls
anaconda3  Anaconda3-4.0.0-Linux-x86_64.sh  certificates  POTUS
[ec2-user@ip-172-31-20-191 ~]$ cd POTUS
[ec2-user@ip-172-31-20-191 POTUS]$ ls
data_POTUS.zip
[ec2-user@ip-172-31-20-191 POTUS]$ unzip data_POTUS.zip
Archive:  data_POTUS.zip
   creating: data_POTUS/
```

Vérification ..

```c
[ec2-user@ip-172-31-20-191 POTUS]$ ls
data_POTUS  data_POTUS.zip  __MACOSX
[ec2-user@ip-172-31-20-191 POTUS]$ cd data_POTUS
[ec2-user@ip-172-31-20-191 data_POTUS]$ ls
2016-11-08-20-00_Minnesota.txt             2016-11-08-20-09_Vermont.txt      
...
[ec2-user@ip-172-31-20-191 data_POTUS]$
```
