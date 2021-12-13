# Points complétés pour le projet de session

> ⚠️Voir le fichier `README.md` pour les procédures de mise en fonction de la machine virtuelle et autres détails pertinents!
>
> ⚠️Noter que lorsque `eth1` est mentionné, il s'agit de l'adresse `ip` fournit par la machine virtuelle et il est toujours question du `port 5000`.

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

Pour tester la fonctionnalité *il n'est pas nécessaire* de lancer le script `db.sql` il suffit : 

1. D'attendre à minuit chaque jour **ou** simplement lancer la fonction (qui est beaucoup plus interessant pour la correction)  :

```python
scheduled_database_update();
```

2. Ensuite, on peut lancer les commandes `bash` suivantes dans le répertoire ` inf5190_projet_src/db/` :

   ```sqlite
   sqlite3
   sqlite> .open db.db
   sqlite> select * from piscines_installations_aquatiques; 
   …
   sqlite> select * from patinoires;
   …
   sqlite> select * from glissades;
   …
   ```

   Et en voir concrètement les résultats! 

## Point A2 (5 points)

> L'importation de données du point `A1` est faite *automatiquement* **chaque jour à minuit** à l’aide d’un <u>BackgroundScheduler</u>.
>
> ⚠️Pour que tout cela fonctionne bien **il est crucial** de programmer l'heure de la *machine virtuelle* à la bonne heure! La commande `bash` suivante fait le travail (pour l'heure local à Montréal) :
>
> ```bash
> sudo timedatectl set-timezone America/Toronto
> ```

Pour tester ce point il suffit d'**attendre à minuit chaque jour** pour voir le résultat <u>sinon</u> on peut modifier la fonctionnalité pour en voir les résultats rapidement comme ceci (pour la correction) :

```python
…
local_time = pytz.timezone("America/Toronto")
scheduler = BackgroundScheduler(timezone=local_time, daemon=True)

def scheduled_database_update():
    db.create_piscines_installations_aquatiques_table()
    db.add_piscines_installations_aquatiques_data_to_database()
    db.create_glissades_table()
    db.add_glissades_data_to_database()
    db.create_patinoires_table()
    db.add_patinoires_data_to_database()
    print('The database was updated at {}'.format(datetime.now(local_time)))

# Update database every day at midnight
scheduler.add_job(scheduled_database_update, 'cron', hour='0', day='*')
scheduler.start()
# On change la ligne 21 pour quelque chose comme :
scheduler.add_job(scheduled_database_update, 'interval',  minutes=1)
…
```

> 💡Pour en voir les résultats en une minute au lieu d'attendre plusieurs heures!
>
> Voir le fichier `app.py` pour plus de détails.

## Point A3 (5 points)

> Le système écoute les requêtes `HTTP` sur le `port 5000`. La route « `/doc` » fait apparaître la **documentation** de **tous** les `services REST`. La **documentation** est en `format HTML`, générée à partir de `fichiers RAML`. Ensuite, intégrer la fonctionnalité du `point A2` à l’application `Flask` créée au point `A3`.

Pour tester ce point il faut :

1. Installer `raml2html` sur son *ordinateur local* (voir note plus bas ⇩) :

   ```bash
   npm i -g raml2html
   …
   ```

1. Lancer la commande suivante pour convertir le fichier `raml` en fichier `HTML` :

   ```bash
   raml2html -p -v services.raml > templates/services.html
   ```

1. Lancer la route `http://eth1:5000/doc` dans un navigateur pour voir la documentation des `services REST ` de l'application.

> ⚠️Noter que j'ai essayé d'implémenter une fonction comme ceci :
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
> J'ai rencontré des problèmes de dépendances avec des versions de `npm` dans la *machine virtuelle* j'ai donc fait le choix d'installer sur ma *machine local* pour faire la conversion `.raml ⇒ .html` afin ne pas prendre le risque de corrompre les dépendances du `requirements.txt`.

## Point A4 (10 points)

> Le système offre un `service REST` permettant d'**obtenir la liste des installations** pour un *arrondissement spécifié en paramètre*. Les données retournées sont en `format JSON`.
>  Ex. `GET` /api/installations?arrondissement=LaSalle

Pour tester ce point il faut :

1. Écrire une route dans `l'URL` en spécifiant un <u>paramètre</u> au **query string** : 
   - Ex : `http://eth1:5000/installations?arrondissement=Verdun`
1. La fonction python attachée à la route `http://192.168.56.7:5000/installations` va être exécutée à l'aide de `Flask` . 
1. Cette fonction va aller chercher les données des trois tables dans la base de données contenant cette chaîne de caractère dans les enregistrements et va retourner les enregistrements des installations correspondants à l'arrondissement pour chacune des tables.
1. Le contenue des trois tables sera empilés dans une liste avant d'être transformé en `format JSON`.
1. Le résultat retournée par cette route sera affiché en `format JSON` <u>sur le navigateur</u>.

> 💡Il est recommandé de tester ce point avec un outil comme `Postman`.
>
> ⚠️Il est important de noter que le service REST retourne **tous les installations** dont le query string de longueur entre 4 et 40 caractères **est contenue dans le nom de l'arrondissement**!
>
> Ex : `http://eth1:5000/installations?arrondissement=Verd` 
>
> Fonctionne aussi!
>
> 🔎Le but est de laisser la chance à l'utilisateur de trouver ce dont il cherche avec plus d'aisance.

## Point A5 (10 points)

> Une application JavaScript/HTML permet de saisir un arrondissement à partir d'un formulaire HTML. 
>
> Lorsque l'utilisateur lance la recherche, une requête asynchrone contenant l'arrondissement saisis est envoyée à la route définie en A4. Lorsque la réponse asynchrone revient, l'application affiche la liste des installations dans un tableau. L'application est disponible sur la page d'accueil du serveur (route
>
> « / »).

Pour tester ce point il faut :

1. Sur la page principale du logiciel (route '`/`') on doit cliquer sur le bouton `Search District Installations` pour se rendre sur la route `http://eth1:5000/installations` et ensuite on peut entrer la requête dans un champs texte approprié (Form input).
1. La requête asynchrone  retourne la réponse sous forme de tableau  généré par `Tabulate` sur une page du fureteur le `content type` est `charset=UTF-8`.

> ⚠️Noter que le tableau généré par `Tabulate` est parfois décalé (avec beaucoup d'espace vide principalement pour la table contenant les patinoires) pour fusionner les résultats des trois tables ensemble. J'ai manqué de temps pour fixer ce problème.

## Point A6 (10 points)

> L'application du point `A5` offre un mode de recherche par nom d'installation. La liste de toutes les installations est prédéterminée dans une **liste déroulante** et l'utilisateur choisira une installation parmi cette liste. Lorsque l'utilisateur **lance la recherche**, une **requête asynchrone** est envoyée à un `service REST` que vous devez créer à cet effet. Lorsque la réponse asynchrone revient, l'application `affiche l'information` connue sur cette installation.

Pour tester ce point il faut :

1. 

## Point C1 (10 points)

> Le système offre un `service REST` permettant d'obtenir la **liste des installations** dont les données ont été **mises à jour en 2021**. 
> Pour chaque installation, on indique **tout l'information connue**. 
> La liste est triée en **ordre croissant du nom** de l'installation.

Pour tester ce point il faut :

1. Lancer dans le navigateur la route : `http://eth1:5000/installations/2021`.
1. Cela va générer une page contenant la liste de **tous les informations** concernant les installations mise à jour en 2021 en `format JSON`. Sinon utiliser la barre de navigation de l'application, clicker sur le bouton `Installations-2021 XML Format`.

> ⚠️Le format de la liste n'était pas spécifié j'ai donc fait le choix d'utiliser le `format JSON`.

## Point C2 (10 points)

> Le système offre un service permettant d'obtenir exactement les mêmes données que le point `C1` mais en `format XML`. L'encodage de caractères doit être `UTF-8`.

Pour tester ce point il faut :

1. Lancer la route suivante dans un navigateur : `http://eth1:5000/installations/2021/installations-2021.xml` ou d'utiliser la barre de navigation et clicker sur  le bouton `Installations-2021 XML Format`.
1. Une page avec le contenue en `format XML` va s'afficher **sur le navigateur**.

## Point c3 (5 points)

> Le système offre un service permettant d'obtenir exactement les mêmes données que le point `C1` mais en format `CSV`. L'encodage de caractères doit être `UTF-8`.

Pour tester ce point il faut :

1. Lancer la route suivante dans un navigateur : `http://eth1:5000/installations/2021/installations-2021.csv` ou d'utiliser la barre de navigation et clicker sur le sur le bouton `Installations-2021 CSV Format`.
1. Un fichier  en `format CSV` va être téléchargé contenant le résultat.

> ⚠️Noter que le `format CSV` est un choix horrible pour la modélisation de données du logiciel cela rend la lecture difficile et plusieurs champs sont inutiles pour certains types de données. Comme par exemple, les conditions des patinoires qui sont propre à eux etc…
>
> Or, `JSON` et `XML` sont des choix de qualités (par préférence JSON).
>
> 💡Il est clair qu'il existe peut-être une façon de bien générer le format `CSV` mais on va en rester là avec le temps impartie.

