import stubs

def recommend(user):
	rules = stubs.getRules()
	rules = sorted(rules, key=lambda x: x[2], reverse=True)
	recommendations = []
	for rule in rules:
		preconditions = rule[0]
		applicable = True
		for cond in preconditions:
			if not stubs.userLikes(user, cond):
				applicable = False
		if stubs.userLikes(user, rule[1]):
			applicable = False
		if applicable:
			recommendations.append(rule)
	print str(recommendations)

recommend(4)
