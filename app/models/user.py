import pymongo
from pymongo import MongoClient

class User():
    client = MongoClient()
    db = client.database
    collection = db.userCollection
    
    def __init__(self, record):
        self.username = record.username
        self.password = record.password
        self.favorites = record.favorites
    
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
    
    #Static methods
    def add_user(username, password):
        user = {"username": username,
          "password": password,
          "favorites": []}
        user_id = collection.insert(user)
        return user_id
        
    def get(user_id):
        return User(collection.find_one({"_id": user_id}))
      
    def validate(username, password):
        users = collection.find({"username": username, "password": password}).count()
        if users == 1:
		        return True
        else:
    	  	  return False
        
    def get_userID(username, password):
        users = collection.find_one({"username": username, "password": password})
        return users["_id"]

    def add_favorite(user_id, favorite_id):
        user = find(user_id)
        user["favorites"].append(favorite_id)
        collection.save(user)

    def remove_favorite(user_id, favorite_id):
        user = find(user_id)
        favorites = user["favorites"]
        if favorite_id in favorites: 
            favorites.remove(favorite_id)
        collection.save(user)
