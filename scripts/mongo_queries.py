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
from re import match

import numpy as np
import pandas as pd
from scipy.stats import pearsonr


def info_mongo(db):
    """ Affiche toutes les collections disponibles dans la base de données"""
    print(db.list_collection_names())


def affiche_mongo(db):
    """ Affiche tous les films stockés dans la collection 'films'"""
    for film in db.films.find():
        print(film)


def insert_movie(db,collection, movie):
    """ Insère un film dans la base de données mais il faut ajouter toute les caracteristique qu'il vont avec"""
    collection_ref = db[collection]
    collection_ref.insert_one(movie)


def update_movie(db, search_field, search_value, update_values, collection):
    """Met à jour un film en fonction d'un champ donné"""
    collection_ref = db[collection]
    collection_ref.update_one({search_field: search_value}, {"$set": update_values})



def find_movies(db, field, value, collection):
    """Recherche des films en fonction d'un champ spécifique"""
    collection_ref = db[collection]
    return list(collection_ref.find({field: {'$regex': value, '$options': 'i'}}))


def delete_movie(db, search_field, search_value, collection):
    """Supprime un film en fonction du champ et de la valeur spécifiés (ID, title, genre)"""
    collection_ref = db[collection]
    if search_field == "ID":
        collection_ref.delete_one({"_id": search_value})
    elif search_field == "Title":
        collection_ref.delete_one({"title": search_value})
    elif search_field == "Genre":
        collection_ref.delete_one({"genre": search_value})


def get_all_movies(db,collection):
    """ Retourne la liste de tous les films stockés dans la collection 'films'"""
    collection_ref = db[collection]
    return list(collection_ref.find())


#----------------------------------------------------



def most_movies_year(db,collection):
    """Retourne l'année avec le plus grand nombre de films"""

    collection_ref = db[collection]
    return list(collection_ref.aggregate([
        {"$group": {"_id": "$year", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 1}
    ]))

def most_movies_year_range(db, min, max,collection):
    """Retourne l'année avec le plus grand nombre de films"""

    collection_ref = db[collection]
    return list(collection_ref.aggregate([
        {"$match": {"year": {"$gte": int(min), "$lte": int(max)}}},
        {"$group": {"_id": "$year", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 1}
    ]))


def count_movies_after_1999(db,collection):
    """Retourne le nombre de films sortis après 1999"""
    collection_ref = db[collection]
    return collection_ref.count_documents({"year": {"$gt": 1999}})


def avg_votes_2007(db,collection):
    """Retourne la moyenne des votes des films de 2007"""
    collection_ref = db[collection]
    return list(collection_ref.aggregate([
        {"$match": {"year": 2007}},
        {"$group": {"_id": None, "avg_votes": {"$avg": "$Votes"}}}
    ]))

def avg_votes_2007_range(db, min, max,collection):
    """Retourne la moyenne des votes des films de 2007"""
    collection_ref = db[collection]
    return list(collection_ref.aggregate([
        {"$match": {"year": {"$gte": int(min), "$lte": int(max)}}},
        {"$group": {"_id": None, "avg_votes": {"$avg": "$Votes"}}}
    ]))

def avg_score_2007_range(db, min, max,collection):
    """Retourne la moyenne des votes des films de 2007"""
    collection_ref = db[collection]
    return list(collection_ref.aggregate([
        {"$match": {"year": {"$gte": int(min), "$lte": int(max)}}},
        {"$group": {"_id": None, "avg_score": {"$avg": "$Metascore"}}}
    ]))

def movies_per_year(db, collection):
    """Retourne un dictionnaire du nombre de films par année"""
    collection_ref = db[collection]
    return list(collection_ref.aggregate([
        {"$group": {"_id": "$year", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ]))

def movies_per_year_range(db, min, max,collection):
    """Retourne un dictionnaire du nombre de films par année"""
    collection_ref = db[collection]
    return list(collection_ref.aggregate([
        {
            '$match': {
                'year': {
                    '$gte': int(min),
                    '$lte': int(max)
                }
            }
        }, {
            '$group': {
                '_id': '$year',
                'count': {
                    '$sum': 1
                }
            }
        }, {
            '$sort': {
                '_id': 1
            }
        }
    ]))


def distinct_genres(db, collection):
    """Retourne la liste unique des genres de films"""
    collection_ref = db[collection]
    return [doc["_id"] for doc in collection_ref.aggregate([
        {"$unwind": "$genre"},
        {"$group": {"_id": "$genre"}}
    ])]


def highest_revenue_movie(db,collection):
    """Retourne le film ayant généré le plus de revenus"""
    collection_ref = db[collection]
    return list(collection_ref.find(
        {"Revenue (Millions)": {"$ne": ""}},  # Exclut les valeurs vides
        {"title": 1, "Revenue (Millions)": 1}
    ).sort("Revenue (Millions)", -1).limit(1))

def highest_revenue_movie_range(db, min, max,collection):
    """Retourne le film ayant généré le plus de revenus"""
    collection_ref = db[collection]
    return list(collection_ref.aggregate([
    {
        '$match': {
            'Revenue (Millions)': {
                '$ne': ''
            },
            'year': {
                '$lte': int(max),
                '$gte': int(min)
            }
        }
    }, {
        '$sort': {
            'Revenue (Millions)': -1
        }
    }, {
        '$limit': 1
    }
]))

def directors_with_more_than_5_movies(db,collection):
    """Retourne les réalisateurs ayant réalisé plus de 5 films"""
    collection_ref = db[collection]
    # il dit que cela est vide ???
    return list(collection_ref.aggregate([
        {"$group": {"_id": "$Director", "count": {"$sum": 1}}},
        {"$match": {"count": {"$gt": 5}}},
        {"$sort": {"count": -1}}
    ]))


def most_profitable_genre(db, collection):
    """Retourne le genre de film avec le plus haut revenu moyen"""
    collection_ref = db[collection]
    return list(collection_ref.aggregate([
        {"$unwind": "$genre"},
        {"$group": {"_id": "$genre", "avg_revenue": {"$avg": "$Revenue (Millions)"}}},
        {"$sort": {"avg_revenue": -1}},
        {"$limit": 1}
    ]))


def top_movies_by_decade(db,collection):
    """Retourne les 3 films les mieux notés par décennie"""
    collection_ref = db[collection]
    return list(collection_ref.aggregate([
        {"$project": {"title": 1, "rating": 1, "decade": {"$subtract": ["$year", {"$mod": ["$year", 10]}]}}},
        {"$match": {"title": {"$ne": None}, "rating": {"$ne": None}}},  # Exclude None values
        {"$sort": {"decade": 1, "rating": -1}},
        {"$group": {"_id": "$decade", "top_movies": {"$push": {"title": "$title", "rating": "$rating"}}}},
        {"$project": {"decade": "$_id", "top_movies": {"$slice": ["$top_movies", 3]}}}
    ]))


def longest_movie_by_genre(db,collection):
    # Retourne le film le plus long par genre
    collection_ref = db[collection]
    return list(collection_ref.aggregate([
        {"$unwind": "$genre"},
        {"$sort": {"Runtime": -1}},
        {"$group": {"_id": "$genre", "longest_film": {"$first": "$title"}, "Runtime (Minutes)": {"$first": "$Runtime (Minutes)"}}}
    ]))


def create_high_rated_profitable_movies_view(db,collection):
    """Crée une vue des films avec un Metascore > 80 et un revenu > 50M"""
    collection_ref = db[collection]
    # il y a une erreur " TypeError: 'Collection' object is not callable. If you meant to call the 'create_view'
    # method on a 'Database' object it is failing because no such method exists.
    # Cela ne marche pas
    """
    db.create_view("high_rated_profitable_movies", "films", [
        {"$match": {"Metascore": {"$gt": 80}, "Revenue (Millions)": {"$gt": 50}}}
    ])"""
    return collection_ref.command("create", "high_rated_profitable_movies",
               viewOn="films",
               pipeline=[{"$match": {"Metascore": {"$gt": 80}, "Revenue (Millions)": {"$gt": 50}}}])


def movies_metascore_revenue(db, min_score, min_revenue,collection):
    collection_ref = db[collection]
    return list(collection_ref.aggregate([
    {
        '$match': {
            'Metascore': {
                '$gte': int(min_score),
            },
            'Revenue (Millions)': {
                '$gte': int(min_revenue)
            }
        }
    }, {
        '$project': {
            'Movie': '$title',
            'MetaScore': '$Metascore',
            'Revenue (M)': '$Revenue (Millions)'
        }
    }
]))



def correlation_runtime_revenue(db,collection):
    """Retourne la corrélation entre la durée des films et leur revenu"""
    collection_ref = db[collection]

    data = list(collection_ref.find({}, {"Runtime (Minutes)": 1, "Revenue (Millions)": 1, "_id": 0}))

    df = pd.DataFrame(data).dropna()

    if not df.empty:
        df["Runtime (Minutes)"] = pd.to_numeric(df["Runtime (Minutes)"], errors="coerce")
        df["Revenue (Millions)"] = pd.to_numeric(df["Revenue (Millions)"], errors="coerce")
        df = df.dropna()

        if len(df) > 1:  # Vérifier qu'il y a au moins deux valeurs
            corr, _ = pearsonr(df["Runtime (Minutes)"], df["Revenue (Millions)"])
            return corr
    return None


def avg_runtime_by_decade(db, collection):
    """Retourne l'évolution de la durée moyenne des films par décennie"""
    collection_ref = db[collection]
    return list(collection_ref.aggregate([
        {"$project": {"Runtime (Minutes)": 1, "decade": {"$subtract": ["$year", {"$mod": ["$year", 10]}]}}},
        {"$group": {"_id": "$decade", "avg_runtime": {"$avg": "$Runtime (Minutes)"}}},
        {"$sort": {"_id": 1}}
    ]))
