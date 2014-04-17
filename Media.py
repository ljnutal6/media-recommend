import pymongo
from pymongo import MongoClient

client = MongoClient()
db = client.database
collection = db.mediaCollection
    
def add_book(title, authors, editors, illustrators, translators, publication):
    book = {"title": title, 
            "authors": authors,
            "editors": editors,
            "illustrators": illustrators,
            "translators": translators,
            "original publication date": publication}
    #author_list = user["authors"]
    #for author in authors
    #    author_list.append(author)
        
    book_id = collection.insert(book)
    return book_id
        
def add_movie(title, release, rating, studio, director, actors):
    movie = {"title": title, 
             "release year": release, 
             "MPAA rating": rating, 
             "studio": studio, 
             "director": director,
             "leading actors": actors}
    movie_id = collection.insert(movie)
    return movie_id
    
def add_tvshow(title, producer, seasons, episodes, actors, premier):
    tvshow = {"title": title, 
              "producer": producer, 
              "number of seasons": seasons, 
              "number of episodes": episodes, 
              "leading actors": actors, 
              "premier date": premier}
    tvshow_id = collection.insert(tvshow)
    return tvshow_id
    
def add_videogame(title, publisher, system, release, rating):
    videogame = {"title": title,
                 "publisher": publisher, 
                 "developer": developer, 
                 "system": system, 
                 "release year": release, 
                 "ESRB rating": rating}
    game_id = collection.insert(videogame)
    return game_id
    
def find(id):
    return collection.find_one({"_id": id})
