# Projet de session inf5190-Programmation web avancée-Automne 2021

**Auteur** : 
Carl Montpetit

**Code permanent** : 
MONC08069000

**Date** : 
20 novembre 2021

---
## Description
>Le projet consiste à récupérer un ensemble de données provenant de la ville de Montréal et d'offrir des services à partir de ces données. Il s'agit de données ouvertes à propos d'installations pour faire des activités sportives.
## Technologies utilisées

- HTML5
- CSS3
- JavaScript
- Python3
- Bootstrap3
- SQLite3
- Vagrant 2.2.19
- Virtualbox 6.1
- Git 2.34.0
- Flask 2.0.2
- Werkzeug 2.0.2
- Jinja2

## Instructions

#### Pour lancer l'application avec **Vagrant** :

> Initialement, à la racine du projet :

1. Lancer la commande `vagrant up` pour créer la machine virtuel (avec le provider `virtualbox`).

2. Lancer la commande `vagrant ssh` pour s'y connecter.

2. Le nom d'utilisateur est `vagrant` et le mot de passe est aussi `vagrant` !

2. Le `port` est toujours `5000`.

3. ⚠️Noter l'`adresse ip (eth1)` de la machine virtuelle qui est mentionnée.

4. Lancer la commande `source /home/vagrant/inf5190_projet_venv/bin/activate` pour activer l'environnement virtuel de `Python🐍`.

5. Se déplacer dans le répertoire partagé avec la commande `cd /vagrant`.

6. Installer les librairies du projet avec la commande `sudo pip install -r requirements.txt`.

7. Se déplacer dans le répertoire `inf5190_projet_src` avec la commande `cd inf5190_projet_src/`.

8. Lancer l'application `flask` avec la commande `python app.py`.

9. Ouvrir un fureteur et entrer le `URL` `http://eth1:5000` avec `eth1`, l'`adresse ip ` offert lors du lancement de la machine virtuelle avec `Vagrant`.

   - Sinon, il est possible de tester la connection avec l'application à l'aide de la commande `curl` sur la connection `ssh` de la machine virtuelle en utilisant :

     - ```zsh
       curl http://localhost:5000/
       # ou (avec localhost = 127.0.0.1 avec flask)
       curl http://localhost:5000/…(si on veut une route en particulier)
       # si on veut seulement l'en-tête 
       curl --head http://localhost:5000/
       ```

#### Initialiser la base de données :

> Dans le répertoire `db/` :

1. Executer la commande `sqlite3`.
2. Executer `.open db.db`.
3. Executer `.read db.sql`.
4. On peut maintenant créer des tables avec lignes et des colonnes dans la base de données  `db.sql` et y insérer des données  à partir de l'application web.

## Détails

#### Détails concernant la machine virtuelle utilisée lors du développement :

> - **IP address for eth0**: `10.0.2.15 `
>
> - **IP address for eth1**: `192.168.56.7` (l'ordinateur local qui utilise la machine virtuelle)
> - **user name** : `vagrant`
> - **Password** : `vagrant`

![image-20211125123522340](https://tva1.sinaimg.cn/large/008i3skNgy1gwrx0e7y4tj31440tmdnm.jpg)

## Sources

- Source pour la barre de navigation avec bootstrap3 utilisée :
  - `https://getbootstrap.com/docs/3.4/components/#navbar`

---
