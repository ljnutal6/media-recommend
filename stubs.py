def getMediaIDs():
	return [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

def getUserIDs():
	return [0, 1, 2, 3]

def getUserRating(user, media):
	database = {0:{7:5, 8:5, 9:4, 0:2, 1:1}, 1:{7:5, 0:1, 9:3, 12:4}, 2:{11:4, 12:4, 7:5, 0:4}, 3:{9:4, 4:1, 10:2}}
	userdata = database[user]
	if media in userdata:
		return userdata[media]
	else:
		return -1
