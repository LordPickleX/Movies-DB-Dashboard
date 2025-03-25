P# Projet d’Exploration et d’Interrogation de Bases de Données NoSQL

## Description du projet

Ce projet a pour objectif d’explorer et d’interroger deux types de bases de données NoSQL :

- **MongoDB** : une base de données orientée document, utilisée pour stocker des films et leurs informations.
- **Neo4j** : une base de données orientée graphe, utilisée pour modéliser des relations entre des films et des acteurs.

L’application permet de :

- Se connecter à MongoDB et Neo4j.
- Interroger MongoDB pour afficher des films et leur genre.
- Visualiser les relations entre films et acteurs à l’aide de Neo4j.
- Afficher des graphiques pour analyser les données récupérées depuis MongoDB.

## Technologies utilisées

| Technologie                 | Description                                                                                     |
|-----------------------------|-------------------------------------------------------------------------------------------------|
| **MongoDB**                | Base de données orientée document.                                                             |
| **Neo4j**                 | Base de données orientée graphe.                                                              |
| **Python**                 | Langage de programmation principal.                                                           |
| **Streamlit**              | Framework pour l’interface utilisateur.                                                      |
| **Matplotlib** et **Seaborn** | Bibliothèques pour la visualisation des données.                                               |
| **PyMongo**                | Bibliothèque Python pour interagir avec MongoDB.                                              |
| **Neo4j Python Driver**    | Bibliothèque Python pour interagir avec Neo4j.                                                |
| **Neovis.js**              | Bibliothèque pour l’affichage des graphes interactifs de Neo4j dans Streamlit.               |

## Installation et configuration

### 1. Prérequis

Avant de commencer, assurez-vous que vous avez installé :

- [Python 3.x](https://www.python.org/downloads/)
- [MongoDB](https://www.mongodb.com/try/download/community) (si vous utilisez une base locale)
- [Neo4j](https://neo4j.com/download/) (si vous utilisez une base locale ou une instance cloud)

### 2. Cloner le projet

Clonez ce dépôt sur votre machine locale :

```bash
git clone https://github.com/votre-utilisateur/projet-nosql.git
cd projet-nosql
 ```


### 3. Créer un environnement virtuel

Créez un environnement virtuel et activez-le :

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
 ```
 
### 4. Installer les dépendances

Installez toutes les dépendances nécessaires :
```bash
pip install -r requirements.txt
```

### 5. Se connecter à MongoDB et Neo4j	
•	Pour MongoDB, remplacez les valeurs <user> et <password> par vos identifiants MongoDB si vous utilisez MongoDB Atlas.
•	Pour Neo4j, remplacez les valeurs <Username> et <Password> par vos identifiants.

### 6. Démarrer MongoDB (si utilisé localement)

Si vous utilisez une base de données MongoDB locale, lancez-le avec la commande suivante :
```bash
mongod
```

### 7. Démarrer l’application Streamlit

Lancez l’application Streamlit :

```bash
streamlit run app.py
```

Accédez à l’application via votre navigateur à l’adresse http://localhost:8501.

Fonctionnalités

1. Connexion à MongoDB et Neo4j
	•	Connexion sécurisée aux instances MongoDB et Neo4j.
	•	Vérification de la connexion et récupération des données depuis ces bases.

2. Interrogation de MongoDB
	•	Affichage des noms des collections disponibles.
	•	Recherche et affichage des films présents dans la collection movies et moviess.
	•	Fonction d’insertion, mise à jour et suppression de documents dans la collection.

3. Interrogation de Neo4j (avec Cypher)
	•	Création de nœuds pour les films et acteurs.
	•	Création de relations entre les films et les acteurs.
	•	Requêtes pour trouver des acteurs qui ont joué dans plusieurs films et pour trouver les chemins les plus courts entre deux acteurs.

4. Analyse et Visualisation
	•	Visualisation des films par genre sous forme de graphique à barres (avec Matplotlib).
	•	Affichage des relations entre les films et les acteurs via un graphique interactif (avec Neovis.js).

Structure du projet
```bash
/projet-nosql  
│── /data  
│   ├── movies.json  # Fichier de données pour MongoDB  
│── /scripts  
│   ├── database.py  # Fonctions pour la connexion à MongoDB et Neo4j  
│   ├── mongo_queries.py  # Requêtes MongoDB  
│   ├── neo4j_queries.py  # Requêtes Neo4j  
│── app.py  # Application Streamlit principale  
│── config.py  # Variables de configuration  
│── requirements.txt  # Dépendances du projet  
│── README.md  # Documentation du projet  
```

Dépannage
	 
•	Problème de connexion MongoDB : Vérifiez que MongoDB est en cours d’exécution sur votre machine ou que vous utilisez un bon URI MongoDB.
•	Problème de connexion Neo4j : Assurez-vous que vous avez les bonnes informations de connexion (URI, username, password).

Auteurs
•	Bretecher Erwan, Vincent Vaccarezza, Evan ...



