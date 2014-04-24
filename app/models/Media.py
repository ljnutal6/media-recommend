import pymongo
from pymongo import MongoClient
import urllib
import urllib2
import simplejson

client = MongoClient()
db = client.database
collection = db.mediaCollection

def update_all():
    records = list(collection.find({"type":"book"}))
    for record in records:
        collection.update({"_id":record["_id"]},{'$set':{'url':getImageUrl("book" + record["title"])}}, multi=True)
        
    records = list(collection.find({"type":"tv show"}))
    for record in records:
        collection.update({"_id":record["_id"]},{'$set':{'url':getImageUrl("show" + record["title"])}}, multi=True)
    
    records = list(collection.find({"type":"movie"}))
    for record in records:
        collection.update({"_id":record["_id"]},{'$set':{'url':getImageUrl("movie" + record["title"])}}, multi=True)
    
    records = list(collection.find({"type":"videogame"}))
    for record in records:
        collection.update({"_id":record["_id"]},{'$set':{'url':getImageUrl("game" + record["title"])}}, multi=True)
    
def add_book(title, authors, editors, illustrators, translators, publication):
    book = {"type": "book", 
            "title": title,
            "searchable title": title.lower(), 
            "authors": authors,
            "editors": editors,
            "illustrators": illustrators,
            "translators": translators,
            "original publication date": publication, "url": getImageUrl("book " + title)}
    #author_list = user["authors"]
    #for author in authors
    # author_list.append(author)
        
    book_id = collection.insert(book)
    return book_id
        
def add_movie(title, release, rating, studio, director, actors):
    movie = {"type": "movie", 
             "title": title,
             "searchable title": title.lower(),
             "release year": release,
             "MPAA rating": rating,
             "studio": studio,
             "director": director,
             "leading actors": actors, "url": getImageUrl("movie " + title)}
    movie_id = collection.insert(movie)
    return movie_id
    
def add_tvshow(title, producer, seasons, episodes, actors, premier):
    tvshow = {"type": "tv show", 
              "title": title,
              "searchable title": title.lower(),
              "producer": producer,
              "number of seasons": seasons,
              "number of episodes": episodes,
              "leading actors": actors,
              "premier date": premier, "url": getImageUrl("show " + title)}
    tvshow_id = collection.insert(tvshow)
    return tvshow_id
    
def add_videogame(title, publisher, developer, system, release, rating):
    videogame = {"type": "videogame",
                 "title": title,
                 "searchable title": title.lower(),
                 "publisher": publisher,
                 "developer": developer,
                 "system": system,
                 "release year": release,
                 "ESRB rating": rating, "url": getImageUrl("game " + title)}
    game_id = collection.insert(videogame)
    return game_id
    
def find(media_id):
    return collection.find_one({"_id": media_id})
    
def getID(title, media_type, create=True):
    media = collection.find_one({"type": media_type, "searchable title": title.lower()})
    if media is None:
        if create:
            if media_type == "book":
                return add_book(title, "", "", "", "", "")
            elif media_type == "videogame":
                return add_videogame(title, "", "", "", "", "")
            elif media_type == "movie":
                return add_movie(title, "", "", "", "", "")
            else:
                return add_tvshow(title, "", "", "", "", "")
        else:
            return None
    else:
        return media["_id"]
    
def getMediaIDs():
    ids = []
    for item in collection.find():
    	ids.append(item["_id"])
    return ids

def getMediaIDsMinusAliases():
    ids = []
    for item in collection.find():
	if not "alias" in item:
    		ids.append(item["_id"])
    return ids
    
def isType(media_id, media_type):
	media = find(media_id)
	return media["type"] == media_type
	
def update(media_id, field, newValue):
	media = collection.update({"_id":media_id},{"$set":{field:newValue}})
	collection.save(media)

def listTitles():
	media = getMediaIDs()
	for i in range(0, len(media)):
		if "alias" in find(media[i]):
			print str(i) + " " + find(media[i])["title"] + " (alias for " + find(find(media[i])["alias"])["title"] + ")"
		else:
			print str(i) + " " + find(media[i])["title"]

def addAlias(master, duplicate):
	update(master, "alias", duplicate)

def removeAlias(item_id):
	item = find(item_id)
	item.pop("alias", None)
	collection.save(item)
	
#def search_byphrase(phrase):
	#return find( { "$text": { "$search": "\"" + phrase.lower() + "\"" } } )
#Rest Service used through Google API that returns a JSON file for image search

def getImageUrl(bookSearch):
    url = ('https://ajax.googleapis.com/ajax/services/search/images?' 
    + urllib.urlencode([('v',1.0),('q',bookSearch)]))
    print url
    response = urllib2.urlopen(url)
    # Process the JSON string.
    results = simplejson.load(response)
    data = results['responseData']
    if data:
        dataInfo = data['results']
    else:
        return ""
    if len(dataInfo) == 0:
        return ""
    imageObject = dataInfo[0]
    imageUrl = imageObject['tbUrl']    
    return imageUrl