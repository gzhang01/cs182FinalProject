####
 # game.py
 #
 # Initializes the blackjack game
 #
 # CS182 - Artificial Intelligence
 # Fall 2016
 # Final Project 
 ##

from card import Card 
from deck import BlackjackDeck
from player import Player
import constants as const
from randomAgent import RandomAgent
from basicStrategyAgent import BasicStrategyAgent
from qLearningAgent import QLearningAgent
import sys
import time

class Blackjack:
	def __init__(self, numDecks=8, player=Player(), **kwargs):
		self.numDecks = numDecks
		self.deck = BlackjackDeck(self.numDecks)
		# [player, bet]
		self.player = [player, 0]
		self.dealer = Player()
		self.reshuffle = False
		self.learning = False

		if isinstance(self.player[0], QLearningAgent):
			self.learning = True

		# Flags
		self.noPrint = False

		if "flags" in kwargs:
			if "-np" in kwargs['flags']:
				self.noPrint = True

	# Deals a card to player from the deck
	# If card dealt is cut card, plan to reshuffle at end of round
	def dealCard(self, player):
		card = self.deck.drawCard()
		if card.getValue() == "cut":
			self.reshuffle = True
			card = self.deck.drawCard()
		player.addToHand(card)

	def double(self, player):
		self.dealCard(player[0])
		player[1] = player[1] * 2
		player[0].doubleBet()

	# Deals cards to start a round
	def startRound(self):
		for _ in xrange(2):
			self.dealCard(self.player[0])
			self.dealCard(self.dealer)
		if self.learning:
			# initialize state for Q-Learning
			self.player[0].updateState((self.player[0].getHandValue(), self.dealer.getCardValue(self.getDealerUpcard())))

	# Gets the dealer's face up card (i.e. first card in hand)
	def getDealerUpcard(self):
		return self.dealer.getHand()[0]

	# Runs the game
	def playRound(self):
		self.startRound()

		# Gather bet
		bet = self.player[0].getBet(self.deck)
		if bet == False:
			return (False, self.player[0].winRate)
		self.player[1] = bet

		# Get dealer's face up card
		dealerUpcard = self.getDealerUpcard()
		lastAction = None
		lastState = None

		# Player turn
		while True:
			if not self.noPrint:
				print "\n\nDealer upcard: {0}".format(dealerUpcard)
			
			# Value of dealer's face-up card for qlearning
			dealerUpValue = self.dealer.getCardValue(dealerUpcard)

			# getAction determines next action according to agent
			action = self.player[0].getAction(dealerUpcard)

			lastState = self.player[0].getHandValue(), dealerUpValue

			if action == "bust":
				break
			if action == "stand":
				lastAction = 2
				break
			elif action == "hit":
				lastAction = 1
				self.dealCard(self.player[0])
				# Update Q-Values
				if self.learning:
					self.player[0].update(lastState, 1, (self.player[0].getHandValue(), dealerUpValue), None)
			elif action == "double":
				lastAction = 3
				self.double(self.player)
				# Update Q-Values
				if self.learning:
					self.player[0].update(lastState, 3, (self.player[0].getHandValue(), dealerUpValue), None)
				break

		# Dealer actions
		while True:
			# Don't care about hard vs. soft values
			dealerValue = self.dealer.getHandValue()[0]
		 	dealerBlackjack = True if dealerValue == const.blackjack else False

			if not self.noPrint:
				print "\n"
				print "Dealer hand: " + " ".join([str(card) for card in self.dealer.getHand()])
				print "Dealer hand value: {0}".format(dealerValue)
				if dealerValue == const.blackjack:
					print "Dealer has BLACKJACK"
				elif dealerValue > 21:
					print "Dealer BUST"
				elif dealerValue >= 17:
					print "Dealer STANDS on {0}".format(dealerValue)
				else:
					print "Dealer HITS"

			# Dealer stands on 17 (stand on soft 17)
			if dealerValue == const.blackjack or dealerValue >= 17:
				break

			# Else hit
			self.dealCard(self.dealer)

		# Determine winnings
		playerValue = self.player[0].getHandValue()[0]
	 	playerBlackjack = True if playerValue == const.blackjack else False

		if not self.noPrint:
			print "\n"

		if playerValue == const.blackjack and dealerValue == const.blackjack:		payout = self.player[1]
		elif playerValue == const.blackjack:										payout = 5 * self.player[1] / 2
		elif dealerValue == const.blackjack or playerValue > 21:					payout = 0
		elif dealerValue > 21 or playerValue > dealerValue:							payout = 2 * self.player[1]
		elif playerValue == dealerValue:											payout = self.player[1]
		else:																		payout = 0
		self.player[0].addMoney(payout)
		
		if not self.noPrint:
			if playerValue == const.blackjack and dealerValue == const.blackjack: 	print "Dealer got BLACKJACK and you got BLACKJACK\nPUSH"
			elif playerValue == const.blackjack: 									print "You got BLACKJACK\nYou win ${0}".format(3 * self.player[1] / 2)
			elif dealerValue == const.blackjack:									print "Dealer got BLACKJACK\nYou lose ${0}".format(self.player[1])
			elif playerValue > 21:													print "You BUST\nYou lose ${0}".format(self.player[1])
			elif dealerValue > 21:													print "Dealer BUSTS\nYou win ${0}".format(self.player[1])
			elif playerValue > dealerValue:											print "Dealer has value {0} and you have value {1}\nYou win ${2}".format(dealerValue, playerValue, self.player[1])
			elif playerValue == dealerValue:										print "Dealer has value {0} and you have value {1}\nPUSH".format(dealerValue, playerValue)
			else:																	print "Dealer has value {0} and you have value {1}\nYou lose ${2}".format(dealerValue, playerValue, self.player[1])

		reward = payout - self.player[1]
		result = self.player[0].roundEnd(reward, self.player[0].getHand(), self.dealer.getHand())
		if self.learning:
			self.player[0].update(lastState, lastAction, (self.player[0].getHandValue(), dealerUpValue), reward)

		# Clear cards
		self.player[0].discardHand()
		self.dealer.discardHand()

		# Reshuffle if needed:
		if self.reshuffle:
			if not self.noPrint: print "\n\nReshuffling!"
			self.deck.reshuffle()
			self.player[0].reshuffled()
			self.reshuffle = False

		return (True, 0)


# Gets index of first element in search that matches an element in find
# Returns None on fail
def multIndex(search, find):
	# If intersection of lists is empty, then return None
	if len(set(search) & set(find)) == 0:
		return None

	# Find first index; use set for better performance
	findSet = set(find)
	for i in xrange(len(search)):
		if search[i] in find:
			return i

	# Should never fail to find something if intersection is not empty
	raise RuntimeError("Expected item to be found")


if __name__ == "__main__":
	# Arguments
	args = {"flags": []}
	qlearning = False
	trainingRounds = 1000000

	# Searching for noPrint
	i = multIndex(sys.argv, ["-np", "-noPrint"])
	if i != None:
		args["flags"].append("-np")

	# Searching for money argument
	i = multIndex(sys.argv, ["-m", "-money"])
	if i != None and i != len(sys.argv) - 1:
		try:
			args["money"] = int(sys.argv[i + 1])
		except ValueError:
			raise RuntimeError("Excepted number after money argument")

	# Searching for collectData flag
	i = multIndex(sys.argv, ["-cd", "-collectData"])
	if i != None:
		args["flags"].append("-cd")

	# Searching for file argument
	i = multIndex(sys.argv, ["-f", "-file"])
	if i != None and i != len(sys.argv) - 1:
		args["file"] = sys.argv[i + 1]

	# Q learner iterations
	i = multIndex(sys.argv, ["-qiter"])
	if i != None and i != len(sys.argv) - 1:
		trainingRounds = int(sys.argv[i + 1])

	# Searching for which agent to use
	player = Player(**args)
	i = multIndex(sys.argv, ["-a", "-agent"])
	if i != None and i != len(sys.argv) - 1:
		if sys.argv[i + 1] == "random":
			player = RandomAgent(**args)
		elif sys.argv[i + 1] == "basic":
			player = BasicStrategyAgent(**args)
		elif sys.argv[i + 1] == "qlearning":
			player = QLearningAgent(0.8, 0.1, 1, **args)
			qlearning = True


	game = Blackjack(8, player, **args)
	
	rounds = 0
	if qlearning:
		# training cycle
		player.setTraining(True)
		while rounds < trainingRounds:
			result = game.playRound()
			if rounds % 1000 == 0:
				print rounds
			rounds += 1
		player.setTraining(False)
		player.setMoney(const.startingMoney)
		player.epsilon = 0
		player.alpha = 0

	# testing cycle
	while True:
		result = game.playRound()
		if result[0] == False:
			break



