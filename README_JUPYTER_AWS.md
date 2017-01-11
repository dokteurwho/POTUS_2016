## Installer jupyter notebook sur AWS

Source: https://gist.github.com/iamatypeofwalrus/5183133

### 1. Télécharger et installer Anaconda

```
>wget http://repo.continuum.io/archive/Anaconda3-4.0.0-Linux-x86_64.sh
>bash Anaconda3-4.0.0-Linux-x86_64.sh
>source .bashrc
```

### 2. Créer un certificat qui servira à la connexion vers le notebook

Création du répertoire qui contiendra la clé privée.

```
>cd ec2-user/
>mkdir certificates
>cd certificates/
```

Génération de la clé privée.
```
>openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout mycert.pem -out mycert.pem
```

### 3. Modifier la configuration de jupyter

Création d'une configuration par défaut.

```
jupyter notebook --generate-config
vi /home/ec2-user/.jupyter/jupyter_notebook_config.py
```

Il convient d'éditer le fichier de configuration pour spécificer le certficat et le port de connexion.
Le sha1 est celui du mot de passe qui permettra de se connecter au notebook.
Les lignes à rajouter sont:

```python
# Set options for certfile, ip, password, and toggle off
# browser auto-opening
c.NotebookApp.certfile = u'/home/ec2-user/certificates/mycert.pem'
# Set ip to '*' to bind on all interfaces (ips) for the public server
c.NotebookApp.ip = '*'
c.NotebookApp.password = u'sha1:dda21f3225e4:b688ce73910c9d133a96c114d696295f4a7783b0'
c.NotebookApp.open_browser = False

# It is a good idea to set a known, fixed port for server access
c.NotebookApp.port = 9999
```

### 4. Lancer jupyter
Hop:
```
>jupyter notebook

[I 15:14:33.091 NotebookApp] Serving notebooks from local directory: /home/ec2-user/.ipython
[I 15:14:33.091 NotebookApp] 0 active kernels
[I 15:14:33.091 NotebookApp] The Jupyter Notebook is running at: https://[all ip addresses on your system]:9999/
[I 15:14:33.091 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
[I 15:19:09.487 NotebookApp] 302 GET / (137.194.22.171) 0.76ms
[I 15:19:09.508 NotebookApp] 302 GET /tree (137.194.22.171) 0.94ms
[I 15:19:15.394 NotebookApp] 302 POST /login?next=%2Ftree (137.194.22.171) 0.97ms
[I 15:20:48.163 NotebookApp] Creating new notebook in
[I 15:20:48.171 NotebookApp] Writing notebook-signing key to /home/ec2-user/.local/share/jupyter/notebook_secret
[I 15:20:49.129 NotebookApp] Kernel started: b4eb2144-dd3b-493f-9e80-d243e977726a
```


Finalement se connecter à l'adresse suivante depuis votre navigateur:
https://54.93.44.107:9999/
en remplaçant [54.93.44.107] par l'IP __publique__ de votre instance (celle-ci peut changer).

### 5. Si ça ne marche pas

C'est probablement un problème de firewall. Dans le tableau de bord AWS EC2, vérifier les règles de sécurité de l'instance:

|Security groups | launch-wizard-2.| __view inbound rules__|

Rajouter éventuellement la règle suivante:
```
Ports	Protocol	Source	launch-wizard-2
9999	tcp	      0.0.0.0/0
```
