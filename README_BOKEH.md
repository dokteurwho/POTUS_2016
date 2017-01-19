## Lancement du serveur ##

1. Se connecter en SSH sur la machine FRONT.

2. Aller dans le répertoire POTUS_2016/server/.

3. Lancer :

```
m$ bokeh serve myapp.py --host='*'
```

Bokeh indique sur quel port il écout (par exemple 5006).

## Connexion au serveur ##

4. Depuis le navigateur de votre PC faire:
```
http://35.157.87.69:5006/myapp
```
où _35.157.87.69_ doit être remplacé par l'IP du FRONT.
