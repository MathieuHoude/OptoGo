# OptoGo

### Pour lancer le projet
- Installer les packages Python: ``pip install -r requirements.txt``
- Installer les packages Node: ``npm i``
- Démarrer le serveur MySQL
- Créer le fichier ``.env`` contenant les variables nécessaires à la connection à MySQL (USERNAME, PASSWORD, DBNAME)
- Pour que Tailwind recompile le CSS lors de modifications: ``npx tailwindcss -i ./static/src/input.css -o ./static/dist/css/output.css --watch``
- Dans un 2e terminal: ``flask run``

### Pour initialiser la base de données
 - Créer la base de données ``optogo`` dans MySQL
 - Lancer le script de migrations: ``python DB/migrations.py``
 - Lancer le script d'insertion de données: ``python DB/seed_db.py``


### Sources
- https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3
- https://flowbite.com/docs/getting-started/flask/
