### Déploiement d'une base de données postgresql dans un container docker et une api fastapi
-----------------

#### Connexion en ssh pour pouvoir afficher l'interface de l'api
-----------------
Exécuter les commandes suivantes pour afficher l'interface fastapi
```bash
$ ssh -i data_enginering_machine.pem -L 8000:127.0.0.1:8000 user@ip-machine-distante
```
-----------------

#### Excuter la commande suivante pour lancer l'api via le container
-----------------
```bash
$ docker docker image pull necene12/image_api_bdd_postgresql:2
$ docker container run -it necene12/image_api_bdd_postgresql:2
```
-----------------

#### Alternative par docker-compose pour lancer le container
-----------------
Exécuter les commandes suivante à la racine du répertoire où les fichiers github ont été clonés
```bash
$  cd /Apps
$  sh setup.sh
  ```
-----------------
