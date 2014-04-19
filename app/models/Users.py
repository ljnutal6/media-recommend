import pymongo
from pymongo import MongoClient

client = MongoClient()
db = client.database
collection = db.userCollection

def add_user(username, password):
	user = {"username": username,
		"password": password,
		"favorites": []}
	user_id = collection.insert(user)
	return user_id
    
def get(user_id):
	return collection.find_one({"_id": user_id})
	
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

def getUserIDs():
	ids = []
	for item in collection.find():
		ids.append(item["_id"])
	return ids

def userLikes(user_id, media_id):
	user = get(user_id)
	likes = user["favorites"]
	return media_id in likes
