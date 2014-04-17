import pymongo
from pymongo import MongoClient

class Users:
    def __init__(self):
        self.client = MongoClient()
        self.db = client.database
        self.collection = db.userCollection
        #self.userDoc = open("users.txt", "a")
    
    def add_user(self, username, password, email):
        if email is None:
            email = ""
        
        user = {"username": username,
                "password": password,
                "email": email
                "favorites": []}
        user_id = self.collection.insert(user)
        return user_id
    
    def find(self, user_id):
        return self.collection.find_one({"_id": user_id})
    
    def add_favorite(self, user_id, favorite_id):
        user = self.find(user_id)
        user["favorites"].append(favorite_id)
        self.collection.save(user)
    
    def remove_favorite(self, user_id, favorite_id):
        user = self.find(user_id)
        favorites = user["favorites"]
        if favorite_id in favorites: 
            favorites.remove(favorite_id)
        self.collection.save(user)
