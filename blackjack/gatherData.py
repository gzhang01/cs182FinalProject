from game import Blackjack
from card import Card 
from deck import BlackjackDeck
from player import Player
import constants as const
from randomAgent import RandomAgent
from basicStrategyAgent import BasicStrategyAgent
from qLearningAgent import QLearningAgent
import sys


args = {"flags": ["-np"]}
numGames = 100
trainingRounds = 1000000
wr = []

def getValue(player, playerValue, soft, dealerValue, action):
	try:
		return player.qVals[(((playerValue, soft), dealerValue), action)]
	except KeyError:
		return 0

def getDesiredAction(player, playerValue, soft, dealerValue, actions):
	def isAllEmpty(player, playerValue, soft, dealerValue, actions):
		for action in actions:
			if abs(getValue(player, playerValue, soft, dealerValue, 1) - getValue(player, playerValue, soft, dealerValue, 2)) > 0.2:
				return False
		return True
	if isAllEmpty(player, playerValue, soft, dealerValue, actions):
		return "., "
	action = player.getPolicy(((playerValue, soft), dealerValue), actions)
	return "H, " if action == 1 else "S, " if action == 2 else "D, " if action == 3 else "FOOP"

#### Getting average win rate for random and basic
# wins = 0
# total = 0
# for i in xrange(numGames):
# 	print i
# 	player = RandomAgent(**args)
# 	# player = BasicStrategyAgent(**args)
# 	game = Blackjack(8, player, **args)
	
# 	# testing cycle
# 	rounds = 0
# 	while True:
# 		rounds += 1
# 		result = game.playRound()
# 		if result[0] == False:
# 			wins += result[1] / 100.0 * rounds
# 			total += rounds
# 			break

# print "Average win rate: {0:.2f}%".format(100.0 * wins / total)
# print "Average number rounds before bust: {0:.2f}".format(1.0 * total / numGames)



## Getting win rate for qlearner
trainingRounds = 1000000
# file = "qLearningDoublingData"
# args = {"flags": ["-np",  "-cd"], "file": file}
args = {"flags": ["-np"]}
player = QLearningAgent(0.8, 0.1, 1, **args)
game = Blackjack(8, player, **args)
rounds = 0
player.setTraining(True)
wins = 0
total = 0
while rounds < trainingRounds:
	result = game.playRound()
	if rounds % 1000 == 0:
		print rounds
	rounds += 1

# Writes best action to file
s1 = ""
s2 = ""
for j in xrange(20, 3, -1):
	for i in xrange(2, 12):
		# print j, i, player.qVals[(((j, False), i), 1)], player.qVals[(((j, False), i), 2)], player.getPolicy(((j, False), i), {1: "hit", 2: "stand"})
		s1 += getDesiredAction(player, j, False, i, {1: "hit", 2: "stand", 3: "double"})
		s2 += "({0:.4f}, {1:.4f}, {2:.4f}), ".format(getValue(player, j, False, i, 1), getValue(player, j, False, i, 2), getValue(player, j, False, i, 3))
	s1 += "\n"
	s2 += "\n"
s1 += "\n"
s2 += "\n"
for j in xrange(20, 11, -1):
	for i in xrange(2, 12):
		s1 += getDesiredAction(player, j, True, i, {1: "hit", 2: "stand", 3: "double"})
		s2 += "({0:.4f}, {1:.4f}, {2:.4f}), ".format(getValue(player, j, True, i, 1), getValue(player, j, True, i, 2), getValue(player, j, False, i, 3))
	s1 += "\n"
	s2 += "\n"
with open("../data/qDoublingActions.csv", "w") as f:
	f.write(s1)
with open("../data/qDoublingActionsValues.csv", "w") as f:
	f.write(s2)

player.setTraining(False)
player.epsilon = 0
game.deck.reshuffle()

# testing cycle
for i in xrange(numGames):
	# with open("../data/"file + ".csv", "w") as f:
	# 	pass
	print i
	rounds = 0
	player.setMoney(const.startingMoney)
	while True:
		rounds += 1
		result = game.playRound()
		if result[0] == False:
			wins += result[1] / 100.0 * rounds
			total += rounds
			break

print "Average win rate: {0:.2f}%".format(100.0 * wins / total)
print "Average number rounds before bust: {0:.2f}".format(1.0 * total / numGames)



# ### Get q value for given state
# args = {"flags": ["-np"]}
# player = QLearningAgent(0.8, 0.05, 1, **args)
# game = Blackjack(8, player, **args)
# rounds = 0
# player.setTraining(True)
# trainingRounds = 100000
# s = ""
# while rounds < trainingRounds:
# 	result = game.playRound()
# 	if rounds % 1000 == 0:
# 		print rounds
# 	rounds += 1
# 	with open("../data/qLearningDataQValue.csv", "a") as f:
# 		s += "{0}, {1}\n".format(getValue(player, 4, False, 10, 1), getValue(player, 4, False, 10, 2))
# with open("../data/qLearningDataQValue.csv", "w") as f:
# 	f.write(s)
