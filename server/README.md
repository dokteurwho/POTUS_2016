## Electeurs.csv ##

Contient la liste des états avec le nombre de grands électeurs.

```
state;number of votes
Alabama;9
Alaska;3
Arizona;11
Arkansas;6
California;55
Colorado;9
Connecticut;7
Delaware;3
District of Columbia;3
Florida;29
Georgia;16
```

Code pour le charger:

```python
# Initialize DF containing the results.
df_electeurs = pd.read_csv("electeurs.csv", sep=";", names=["state", "voters"], skiprows=1)
```

### Lancer le serveur ###
Se mettre dans le répertoire de myapp.py et:
```
bokeh serve --show myapp.py


