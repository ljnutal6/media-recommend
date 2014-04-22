import Rule
import Users
import Media

def recommend(user):
	rules = Rule.getRules()
	rules = sorted(rules, key=lambda x: x[2], reverse=True)
	recommendations = []
	for rule in rules:
		preconditions = rule[0]
		applicable = True
		for cond in preconditions:
			if not Users.userLikes(user, cond):
				applicable = False
		if Users.userLikes(user, rule[1]):
			applicable = False
		if rule[1] in recommendations:
			applicable = False
		if applicable:
			recommendations.append(rule[1])
	return recommendations

def recommend_anon(mediaIDs):
	rules = Rule.getRules()
	rules = sorted(rules, key=lambda x: x[2], reverse=True)
	recommendations = []
	for rule in rules:
		preconditions = rule[0]
		applicable = True
		for cond in preconditions:
			if not cond in mediaIDs:
				applicable = False
		if rule[1] in mediaIDs:
			applicable = False
		if rule[1] in recommendations:
			applicable = False
		if applicable:
			recommendations.append(rule[1])
	return recommendations
	
def recommend_by_type(user, mediaType):
	rules = Rule.getRules()
	rules = sorted(rules, key=lambda x: x[2], reverse=True)
	recommendations = []
	for rule in rules:
		preconditions = rule[0]
		applicable = True
		for cond in preconditions:
			if not Users.userLikes(user, cond):
				applicable = False
		if Users.userLikes(user, rule[1]):
			applicable = False
		if rule[1] in recommendations:
			applicable = False
		if applicable and Media.isType(rule[1], mediaType):
			recommendations.append(rule[1])
	return recommendations

def recommend_anon_by_type(mediaIDs, mediaType):
	rules = Rule.getRules()
	rules = sorted(rules, key=lambda x: x[2], reverse=True)
	recommendations = []
	for rule in rules:
		preconditions = rule[0]
		applicable = True
		for cond in preconditions:
			if not cond in mediaIDs:
				applicable = False
		if rule[1] in mediaIDs:
			applicable = False
		if rule[1] in recommendations:
			applicable = False
		if applicable and Media.isType(rule[1], mediaType):
			recommendations.append(rule[1])
	return recommendations

#recommend(4)
