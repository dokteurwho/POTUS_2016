# POTUS_2016

## Organisation des machines:

Trois instances MONGO qui forment replica-set:

* replica-set/172.31.31.100:27017,172.31.31.101:27017,172.31.31.102:27017

Une instance FRONT qui contient:

* un notebook python qui permet de jouer avec la base.
* les fichiers avec les états.

Il convient de se connecter à l'instance FRONT pour administrer MONGO.

```{r, engine='bash', count_lines}
ssh -i "AWS_02.pem" ec2-user@ec2-54-93-213-194.eu-central-1.compute.amazonaws.com
```

(ec2-54-93-213-194.eu-central-1.compute.amazonaws.com) peut changer.


## Organisation des répertoires:

```{r, engine='bash', count_lines}
[ec2-user@ip-172-31-20-191 ~]$ pwd
/home/ec2-user
[ec2-user@ip-172-31-20-191 ~]$ ls
anaconda3  Anaconda3-4.0.0-Linux-x86_64.sh  certificates  POTUS
[ec2-user@ip-172-31-20-191 ~]$ cd POTUS/
[ec2-user@ip-172-31-20-191 POTUS]$ ls
data_POTUS  data_POTUS.zip
```

# Connect to AWS

Prerequesite: you should have a ".pem" file, this is the _secret_ private key allowing ssh connection to your instance. You can try a ssh connection "as is".

```{r, engine='bash', count_lines}
dhcpwifi-23-237:AWS rom$ ls
AWS_02.pem
dhcpwifi-23-237:AWS rom$ ssh -i "AWS_02.pem" ubuntu@ec2-54-93-163-116.eu-central-1.compute.amazonaws.com
The authenticity of host 'ec2-54-93-163-116.eu-central-1.compute.amazonaws.com (54.93.163.116)' can't be established.
ECDSA key fingerprint is SHA256:wBME/td7g6vvelH1UZHdP/y9OAbPg97Epu9XRH0PQ9Y.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added 'ec2-54-93-163-116.eu-central-1.compute.amazonaws.com,54.XX' (ECDSA) to the list of known hosts.
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@         WARNING: UNPROTECTED PRIVATE KEY FILE!          @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
Permissions 0644 for 'AWS_02.pem' are too open.
It is required that your private key files are NOT accessible by others.
This private key will be ignored.
Load key "AWS_02.pem": bad permissions
Permission denied (publickey).
```
The issue is the key is no sufficiently protected. To perform a connection, you must first change security rights.


```{r, engine='bash', count_lines}
dhcpwifi-23-237:AWS rom$ chmod 400 AWS_02.pem
dhcpwifi-23-237:AWS rom$ ssh -i "AWS_02.pem" ubuntu@ec2-54-93-163-116.eu-central-1.compute.amazonaws.com
Welcome to Ubuntu 16.04.1 LTS (GNU/Linux 4.4.0-57-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  Get cloud support with Ubuntu Advantage Cloud Guest:
    http://www.ubuntu.com/business/services/cloud

0 packages can be updated.
0 updates are security updates.
ubuntu@ip-172-31-XX-XX:~$
```
