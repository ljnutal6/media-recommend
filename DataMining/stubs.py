def getMediaIDs():
	return [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

def getUserIDs():
	return [0, 1, 2, 3]

def getRules():
	return [([7], 0, 1.0), ([0], 7, 0.6), ([9], 0, 1.0), ([0], 9, 0.6), ([12], 0, 1.0), ([0], 12, 0.6), ([13], 0, 0.6), ([0], 16, 0.6), ([13], 7, 0.6), ([7], 13, 1.0), ([14], 0, 0.75), ([0], 14, 1.0), ([14], 7, 0.5), ([7], 14, 1.0), ([14], 9, 0.5), ([9], 14, 1.0), ([14], 12, 0.5), ([12], 14, 1.0), ([14], 13, 0.75), ([13], 14, 1.0), ([15], 14, 1.0), ([14], 15, 0.5), ([7, 13], 0, 1.0), ([0,13], 7, 1.0), ([0,7], 13, 1.0), ([7, 14], 0, 1.0), ([0, 14], 7, 0.6), ([0,7], 14, 1.0), ([9,14], 0, 1.0), ([0,14], 9, 0.6), ([0,9], 14, 1.0), ([12,14], 0, 1.0), ([0,14], 12, 0.6), ([0,12], 14, 1.0), ([13,14], 0, 0.6), ([0,14], 13, 0.6), ([0,13], 14, 1.0), ([13,14], 7, 0.6), ([7,14], 13, 1.0), ([7,13], 14, 1.0), ([7,13,14], 0, 1.0), ([0,13,14], 7, 1.0), ([0,7,14], 13, 1.0), ([0,7,13], 14, 1.0)]

def getUserRating(user, media):
	database = {0:{7:5, 8:5, 9:4, 0:2, 1:1, 13:4, 14:1}, 1:{0:1, 9:3, 12:4, 14:1, 15:5}, 2:{11:4, 12:4, 7:5, 0:4, 13:4, 14:1}, 3:{4:1, 10:2, 13:4, 14:1, 15:5}}
	userdata = database[user]
	if media in userdata:
		return userdata[media]
	else:
		return -1

def userLikes(user, media):
	database = {0:[7, 8, 9, 0, 1, 13, 14], 1:[0, 9, 12, 14, 15], 2:[11, 12, 7, 0, 13, 14], 3:[4, 10, 13, 14, 15]}
	userlikes = database[user]
	return media in userlikes	
