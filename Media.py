import pymongo
from pymongo import MongoClient

class Media:
    def __init__(self):
        self.client = MongoClient()
        self.db = client.database
        self.collection = db.mediaCollection
    
    def add_book(self, title, authors, editors, illustrators, translators, publication):
        book = {"title": title, 
                "authors": authors,
                "editors": editors,
                "illustrators": illustrators,
                "translators": translators,
                "original publication date": publication}
        #author_list = user["authors"]
        #for author in authors
        #    author_list.append(author)
        
        book_id = self.collection.insert(book)
        return book_id
        
    def add_movie(self, title, release, rating, studio, director, actors):
        movie = {"title": title, 
                 "release year": release, 
                 "MPAA rating": rating, 
                 "studio": studio, 
                 "director": director,
                 "leading actors": actors}
        movie_id = self.collection.insert(movie)
        return movie_id
    
    def add_tvshow(self, title, producer, seasons, episodes, actors, premier):
        tvshow = {"title": title, 
                  "producer": producer, 
                  "number of seasons": seasons, 
                  "number of episodes": episodes, 
                  "leading actors": actors, 
                  "premier date": premier}
        tvshow_id = self.collection.insert(tvshow)
        return tvshow_id
    
    def add_videogame(self, title, publisher, system, release, rating):
        videogame = {"title": title,
                     "publisher": publisher, 
                     "developer": developer, 
                     "system": system, 
                     "release year": release, 
                     "ESRB rating": rating}
        game_id = self.collection.insert(videogame)
        return game_id
    
    def find(self, id):
        return self.collection.find_one({"_id": id})
