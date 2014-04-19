import Rule
import Users

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
		if applicable:
			recommendations.append(rule[1])
	print str(recommendations)
