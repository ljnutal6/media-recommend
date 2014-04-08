from __future__ import division
import stubs

#Arbitrary parameters. Can be adjusted up or down to more or fewer rules that are less impressive.
# Value of 1 is so picky that it rejects every rule that isn't supported by every dataset
# Value of 0 is so permissive that it finds every association that occurs even once.
minSupport = 0.1
minConf = 0.2

powerset = [[], [1], [2], [3], [4], [5], [1,2], [1,3], [1,4], [1,5], [2,3], [2,4], [2,5], [3,4], [3,5], [4,5], [1,2,3], [1,2,4], [1,2,5], [1,3,4], [1,3,5], [1,4,5], [2,3,4], [2,3,5], [2,4,5], [3,4,5], [1,2,3,4], [1,2,3,5], [1,2,4,5], [1,3,4,5], [2,3,4,5], [1,2,3,4,5]]

def frequentItemSets():
	itemSets = []
	items = stubs.getMediaIDs()
	candidates = []
	for item in items:
		for set in powerset:
			candidates.append({item:set})
	for candidate in candidates:
		if support(candidate) > minSupport:
			itemSets.append(candidate)
	print str(itemSets)

def support(itemset):
	count = 0
	users = stubs.getUserIDs()
	userCount = len(users)
	for user in users:
		missing = False
		for item,values in itemset.iteritems():
			rating = stubs.getUserRating(user, item)
			#print rating, values
			if rating in values:
				missing = missing
			else:
				missing = True
		if not missing:
			count = count + 1
	#print str(count/userCount)
	#print str(count)	
	return count / userCount
			

frequentItemSets()
