import pymongo
from pymongo import MongoClient

client = MongoClient()
db = client.database
collection = db.userCollection

def add_user(username, password, email):
	if email is None:
		email = ""
        
	user = {"username": username,
		"password": password,
		"email": email,
		"favorites": []}
	user_id = collection.insert(user)
	return user_id
    
def find(user_id):
	return collection.find_one({"_id": user_id})
    
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
