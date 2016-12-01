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

# for i in xrange(numGames):
# 	print i
# 	# player = RandomAgent(**args)
# 	# player = BasicStrategyAgent(**args)
# 	player = QLearningAgent(0.4, 0.01, 0.9, **args)
# 	game = Blackjack(8, player, **args)

# 	rounds = 0
# 	player.setTraining(True)
# 	while rounds < trainingRounds:
# 		result = game.playRound()
# 		if rounds % 1000 == 0:
# 			print rounds
# 		rounds += 1
# 	player.setTraining(False)
# 	player.setMoney(const.startingMoney)
# 	player.epsilon = 0
# 	player.alpha = 0
# 	game.deck.reshuffle()
	
# 	# testing cycle
# 	while True:
# 		result = game.playRound()
# 		if result[0] == False:
# 			wr.append(result[1])
# 			break

# print "Average win rate: {0:.2f}%".format(sum(wr) / len(wr))




args = {"flags": ["-np",  "-cd"], "file": "qLearningData"}
player = QLearningAgent(0.4, 0.01, 0.9, **args)
game = Blackjack(8, player, **args)
rounds = 0
player.setTraining(True)
while rounds < trainingRounds:
	result = game.playRound()
	if rounds % 1000 == 0:
		print rounds
	rounds += 1

s = ""
for j in xrange(20, 3, -1):
	for i in xrange(2, 12):
		# print j, i, player.qVals[(((j, False), i), 1)], player.qVals[(((j, False), i), 2)], player.getPolicy(((j, False), i), {1: "hit", 2: "stand"})
		s += "H, " if player.getPolicy(((j, False), i), {1: "hit", 2: "stand"}) == 1 else "S, "
	s += "\n"
s += "\n"
for j in xrange(20, 11, -1):
	for i in xrange(2, 12):
		s += "H, " if player.getPolicy(((j, True), i), {1: "hit", 2: "stand"}) == 1 else "S, "
	s += "\n"
with open("../data/qActions.csv", "w") as f:
	f.write(s)

player.setTraining(False)
player.epsilon = 0
player.alpha = 0
game.deck.reshuffle()

# testing cycle
for i in xrange(numGames):
	print i
	player.setMoney(const.startingMoney)
	while True:
		result = game.playRound()
		if result[0] == False:
			wr.append(result[1])
			break

print "Average win rate: {0:.2f}%".format(sum(wr) / len(wr))



