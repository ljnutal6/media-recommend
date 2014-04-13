from __future__ import division
import stubs

#Arbitrary parameters. Can be adjusted up or down to more or fewer rules that are less impressive.
# Value of 1 is so picky that it rejects every rule that isn't supported by every dataset
# Value of 0 is so permissive that it finds every association that occurs even once.
minSupport = 0.26
minConf = 0.3

def frequentItemSets():
	itemSets = []
	firstRound = []
	mostRecentRound = []
	items = stubs.getMediaIDs()
	candidates = []
	for item in items:
		candidates.append([item])
	round = 0
	while candidates:
		mostRecentRound = []
		for candidate in candidates:
			if support(candidate) > minSupport:
				itemSets.append(candidate)
				mostRecentRound.append(candidate)
				if round == 0:
					firstRound.append(candidate)
		candidates = genNewCandidates(firstRound, mostRecentRound, round)
		round = round + 1
	return itemSets

def support(itemset):
	count = 0
	users = stubs.getUserIDs()
	userCount = len(users)
	for user in users:
		missing = False
		for item in itemset:
			if stubs.userLikes(user, item):
				missing = missing
			else:
				missing = True
		if not missing:
			count = count + 1
	#print str(count/userCount)
	#print str(count)	
	return count / userCount

def confidence(lhs, rhs):
	supp = support(lhs)
	lhs.append(rhs)
	supportUnion = support(lhs)
	return supportUnion/supp

def genRulesets(itemset):
	ruleset = []
	if len(itemset) < 2:
		return ruleset
	for item in itemset:
		tempset = list(itemset)
		tempset.remove(item)
		conf = confidence(tempset, item)
		tempset.remove(item)
		if conf > minConf:
			ruleset.append((tempset, item, conf))
	return ruleset

def Rulesets(itemset):
	rules = []
	for set in itemset:
		r = genRulesets(set)
		rules.extend(r)
	return rules

def genNewCandidates(firstRound, mostRecentRound, round):
	#print "firstround:"
	#for item in firstRound:
		#print str(item)
	#print "recentround:"
	#for item in mostRecentRound:
		#print str(item)
	dround = round + 1
	candidates = []
	for solo in firstRound:
		for set in mostRecentRound:
			if isNotPartOf(solo[0], set):
				z = list(set)
				z.append(solo[0])
				if len(z) > dround and isSorted(z):
					candidates.append(z)
	return candidates

def isNotPartOf(newMember, oldList):
	for num in oldList:
		if newMember == num:
			return False
	return True



def isSorted(list):
	for i in range(0,len(list)-1):
		if list[i] > list[i+1]:
			return False
	return True
			

rules = Rulesets(frequentItemSets())
for rule in rules:
	print str(rule)
