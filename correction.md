# Points complétés pour le projet de session

## Point A1 (15 points)

> Trois listes obtenues par requêtes `HTTP` et stocké dans une base de données 
> `SQLite` nommée `db.db`  dans un répertoire `/db`.
>
> - Comme ceci ⇒ `inf5190_projet_src/db/db.py`
>
> 1. La liste des **piscines et installations aquatiques** en format `CSV`
>    - Au lien ⇒ https://data.montreal.ca/dataset/4604afb7-a7c4-4626-a3ca-e136158133f2/resource/cbdca706-569e-4b4a-805d-9af73af03b14/download/piscines.csv
> 1. La liste *colossale* des **patinoires** en format `XML` :
>    - Au lien ⇒ https://data.montreal.ca/dataset/225ac315-49fe-476f-95bd-a1ce1648a98c/resource/5d1859cc-2060-4def-903f-db24408bacd0/download/l29-patinoire.xml 
> 1. La liste des aires de jeux d'hiver (glissades) en format XML :
>    - Au lien ⇒ http://www2.ville.montreal.qc.ca/services_citoyens/pdf_transfert/L29_GLISSADE.xml

Pour tester la fonctionnalité <u>il n'est pas nécessaire</u> de lancer le script `sb.sql` il suffit : 

1. D'*attendre à minuit chaque jour* ou simplement lancer la fonction (qui est beaucoup plus interessant pour la correction)  :

```python
scheduled_database_update();
```

2. Ensuite, on peut lancer les commandes `bash` suivantes dans le répertoire ` inf5190_projet_src/db/` :

   ```sqlite
   sqlite3
   sqlite> .open db.db
   sqlite> select * from piscines_installations_aquatiques; 
   sqlite> select * from patinoires;
   sqlite> select * from glissades;
   ```

   Et en voir concrètement les résultats! 

## Point A2 (5 points)

> L'importation de données du point `A1` est faite *automatiquement* **chaque jour à minuit** à l’aide d’un <u>BackgroundScheduler</u>.

Pour tester ce point il suffit d'**attendre à minuit chaque jour** pour voir le résultat <u>sinon</u> on peut modifier la fonctionnalité pour en voir les résultats rapidement comme ceci (pour la correction) :

```python
…
def scheduled_database_update():
    db.create_piscines_installations_aquatiques_table()
    db.add_piscines_installations_aquatiques_data_to_database()
    db.create_glissades_table()
    db.add_glissades_data_to_database()
    db.create_patinoires_table()
    db.add_patinoires_data_to_database()
    print('The database was updated at {}'.format(local_time_quebec_canada))


# Update database every day at midnight
scheduler.add_job(scheduled_database_update, 'cron', hour='0', day='*')
scheduler.start()
# On change la ligne 21 pour quelque chose comme :
scheduler.add_job(scheduled_database_update, 'interval',  minutes=1)
…
```

> 💡Pour en voir les résultats en une minute au lieu d'attendre plusieurs heures!
>
> Voir le fichier `app.py` pour plus de détails

## Point A3 (5 points)

> Le système écoute les requêtes `HTTP` sur le `port 5000`. La route « `/doc` » fait apparaître la **documentation** de *tous les services REST*. La **documentation** est en `format HTML`, généré à partir de `fichiers RAML`. Intégrez la fonctionnalité du `point A2` à l’application `Flask` créée au point `A3`.

Pour tester ce point il faut :

1. Installer `raml2html` sur son *ordinateur local* (voir note plus bas ⇩) :

   ```bash
   npm i -g raml2html
   ```

1. Lancer la commande suivante pour convertir le fichier `raml` en fichier `HTML` :

   ```bash
   raml2html services.raml > templates/services.html
   ```

1. Lancer la route `http://192.168.56.7:5000/doc` dans un navigateur pour voir la documentation des services REST de l'application.

> ⚠️Noter que j'ai essayé d'implementer une fonction comme ceci :
>
> ```python
> import os
> 
> @app.route('/doc')
> def doc():
>     os.system('npm i -g raml2html; raml2html services.raml > templates/services.html;') # fonctionne pas avec la machine virtuelle
>     return render_template('services.html'), 200
> ```
>
> J'ai rencontrer des problèmes de dépendances avec des versions de `npm` dans la *machine virtuelle* j'ai donc fait le choix d'installer sur ma *machine local* pour faire la conversion `.raml ⇒ .html`.

## Point A4 (10 points)

> 
