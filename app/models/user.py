import pymongo
from pymongo import MongoClient

class User():
    #client = MongoClient()
    #db = client.database
    #collection = db.userCollection
    
    def __init__(self, record=None):
        if record:
            self.username = record["username"]
            self.password = record["password"]
            self.favorites = record["favorites"]
        else:
            self.favorites = []
    
    def get_id(self):
        return self.username
        
    def is_authenticated(self):
        return True
        
    def is_active(self):
        return True
        
    def is_anonymous(self):
        return False
        
    def save(self):
        collection.update({"username":self.username},{"$set":{"favorites",self.favorites}})

    def add_books(books):
        return
    def add_shows(books):
        return
    def add_movies(books):
        return
    def add_games(books):
        return
    
    #Static methods
    @staticmethod
    def add_user(username, password):
        user = {"username": username,
          "password": password,
          "favorites": []}
        user_id = collection.insert(user)
        return user_id
    @staticmethod        
    def get(user_id):
        return User({"username":user_id, "password":"abc", "favorites":[]})
        #return User(collection.find_one({"_id": user_id}))
    @staticmethod      
    def validate(username, password):
        return True
        #users = collection.find({"username": username, "password": password}).count()
        #if users == 1:
		    #    return True
        #else:
    	  #	  return False
    @staticmethod        
    def get_userID(username, password):
        users = collection.find_one({"username": username, "password": password})
        return users["_id"]
    @staticmethod
    def add_favorite(user_id, favorite_id):
        user = find(user_id)
        user["favorites"].append(favorite_id)
        collection.save(user)
    @staticmethod
    def remove_favorite(user_id, favorite_id):
        user = find(user_id)
        favorites = user["favorites"]
        if favorite_id in favorites: 
            favorites.remove(favorite_id)
        collection.save(user)
