## Suppression d'un repertoire git
### 1- Suppression des fichiers
Ouvrir un terminal
Se mettre sous le repertoire dont il faut supprimer les fichiers : 
```
> cd /POTUS_2016/notebooks/
```
Supprimer les fichiers type .ipynb
```
> rm *.ipynb
```
Prise en compte des modifs par git
```
> git reset HEAD *.ipynb to unstage
```

```
> git commit -m "remove files du repertoire notebooks2" -a
```

```
> git push
```

Il reste à supprimer le repertoire en local
```
> cd ..
> rm -r notebooks2
```
