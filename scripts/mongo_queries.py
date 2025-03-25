"""
 exemple
{
'_id': '100',
'_rev': '1-5993984b95d0851d9cb12590ec576a7f',
'title': 'The Departed', 'genre': 'Crime,Drama,Thriller',
'Description': 'An undercover cop and a mole in the police attempt to _identify each other while infiltrating an Irish gang in South Boston.',
'Director': 'Martin Scorsese', 'Actors': 'Leonardo DiCaprio, Matt Damon, Jack Nicholson, Mark Wahlberg',
'year': 2006,
'Runtime (Minutes)': 151,
'rating': 'G',
'Votes': 937414,
'Revenue (Millions)': 132.37,
'Metascore': 85
 }

 """


def info_mongo(db):
    """ Affiche toutes les collections disponibles dans la base de données """
    print(db.list_collection_names())


def affiche_mongo(db):
    """ Affiche tous les films stockés dans la collection 'films' """
    for film in db.films.find():
        print(film)


def insert_movie(db, movie):
    """ Insère un film dans la base de données mais il faut ajouter toute les caracteristique qu'il vont avec"""
    db.films.insert_one(movie)


def update_movie(db, search_field, search_value, update_values):
    """
    Met à jour un film en fonction d'un champ donné.

    :param db: Base de données MongoDB
    :param search_field: Nom du champ à rechercher (ex: 'title', 'year')
    :param search_value: Valeur du champ à rechercher
    :param update_values: Dictionnaire contenant les mises à jour

    pour update mais pour chaque truc
    """
    db.films.update_one({search_field: search_value}, {"$set": update_values})


def find_movies(db, field, value):
    """
    Recherche des films en fonction d'un champ spécifique.

    :param db: Base de données MongoDB
    :param field: Champ sur lequel effectuer la recherche (ex: 'genre', 'Director')
    :param value: Valeur à rechercher
    :return: Liste des films trouvés
    """
    return list(db.films.find({field: {'$regex': value, '$options': 'i'}}))


def delete_movie(db, search_field, search_value):
    """
    Supprime un film en fonction du champ et de la valeur spécifiés (ID, title, genre).

    :param db: Base de données MongoDB
    :param search_field: Champ à rechercher (ID, Title, Genre)
    :param search_value: Valeur du champ à rechercher (ID, Title, Genre)
    """
    if search_field == "ID":
        db.films.delete_one({"_id": search_value})
    elif search_field == "Title":
        db.films.delete_one({"title": search_value})
    elif search_field == "Genre":
        db.films.delete_one({"genre": search_value})


def get_all_movies(db):
    """ Retourne la liste de tous les films stockés dans la collection 'films' """
    return list(db.films.find())