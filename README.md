# POTUS_2016

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


wget http://repo.continuum.io/archive/Anaconda3-4.0.0-Linux-x86_64.sh
--2017-01-10 12:43:50--  http://repo.continuum.io/archive/Anaconda3-4.0.0-Linux-x86_64.sh
Resolving repo.continuum.io (repo.continuum.io)... 104.16.19.10, 104.16.18.10, 2400:cb00:2048:1::6810:120a, ...
Connecting to repo.continuum.io (repo.continuum.io)|104.16.19.10|:80... connected.
HTTP request sent, awaiting response... 301 Moved Permanently
Location: https://repo.continuum.io/archive/Anaconda3-4.0.0-Linux-x86_64.sh [following]
--2017-01-10 12:43:50--  https://repo.continuum.io/archive/Anaconda3-4.0.0-Linux-x86_64.sh
Connecting to repo.continuum.io (repo.continuum.io)|104.16.19.10|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 417798602 (398M) [application/octet-stream]
Saving to: ‘Anaconda3-4.0.0-Linux-x86_64.sh’

Anaconda3-4.0.0-Lin 100%[===================>] 398.44M  17.0MB/s    in 27s     

2017-01-10 12:44:17 (14.7 MB/s) - ‘Anaconda3-4.0.0-Linux-x86_64.sh’ saved [417798602/417798602]

