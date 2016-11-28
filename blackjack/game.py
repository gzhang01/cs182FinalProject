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

class Blackjack:
	def __init__(self, numDecks=8, player=Player(), **kwargs):
		self.numDecks = numDecks
		self.deck = BlackjackDeck(self.numDecks)
		# [player, bet]
		self.player = [player, 0]
		self.dealer = Player()
		self.reshuffle = False

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

	# Deals cards to start a round
	def startRound(self):
		for _ in xrange(2):
			self.dealCard(self.player[0])
			self.dealCard(self.dealer)

	def getDealerUpcard(self):
		return self.dealer.getHand()[0]

	# Runs the game
	def playRound(self):
		self.startRound()

		# Gather bet
		bet = self.player[0].getBet()
		if bet == False:
			return False
		self.player[1] = bet

		# Player turn
		while True:
			if not self.noPrint:
				print "\n\nDealer upcard: {0}".format(self.getDealerUpcard())
			
			# Compile set of actions user has
			# Will need to change later!
			actions = {
				1: const.actions[1],
				2: const.actions[2]
			}

			# getAction determines next action according to agent
			action = self.player[0].getAction(actions)

			if action == "stand" or action == "bust":
				# TODO: update q-values here
				break
			elif action == "hit":
				# TODO: update q-values here
				self.dealCard(self.player[0])

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

		# TODO: update q-values here as well
		if playerValue == const.blackjack and dealerValue == const.blackjack:
			self.player[0].addMoney(self.player[1])
		elif playerValue == const.blackjack:
			self.player[0].addMoney(5 * self.player[1] / 2)
		elif dealerValue == const.blackjack or playerValue > 21:
			self.player[0].addMoney(0)
		elif dealerValue > 21 or playerValue > dealerValue:
			self.player[0].addMoney(2 * self.player[1])
		elif playerValue == dealerValue:
			self.player[0].addMoney(self.player[1])
		else:
			self.player[0].addMoney(0)
		
		if not self.noPrint:
			if playerValue == const.blackjack and dealerValue == const.blackjack: 	print "Dealer got BLACKJACK and you got BLACKJACK\nPUSH"
			elif playerValue == const.blackjack: 									print "You got BLACKJACK\nYou win ${0}".format(3 * self.player[1] / 2)
			elif dealerValue == const.blackjack:									print "Dealer got BLACKJACK\nYou lose ${0}".format(self.player[1])
			elif playerValue > 21:													print "You BUST\nYou lose ${0}".format(self.player[1])
			elif dealerValue > 21:													print "Dealer BUSTS\nYou win ${0}".format(self.player[1])
			elif playerValue > dealerValue:											print "Dealer has value {0} and you have value {1}\nYou win ${2}".format(dealerValue, playerValue, self.player[1])
			elif playerValue == dealerValue:										print "Dealer has value {0} and you have value {1}\nPUSH".format(dealerValue, playerValue)
			else:																	print "Dealer has value {0} and you have value {1}\nYou lose {2}".format(dealerValue, playerValue, self.player[1])

		# Clear cards
		self.player[0].discardHand()
		self.dealer.discardHand()

		# Reshuffle if needed:
		if self.reshuffle:
			#### TODO: Think about how to notify players that deck has been reshuffled
			print "\n\nReshuffling!"
			self.deck.reshuffle()
			self.reshuffle = False

		return True



if __name__ == "__main__":
	player = Player()

	if len(sys.argv) == 2:
		if sys.argv[1] == "random":
			player = RandomAgent()
		elif sys.argv[1] == "basic":
			player = BasicStrategyAgent()
		elif sys.argv[1] == "qlearning":
			player = QLearningAgent(0.1, 0.5, 0.2)

	game = Blackjack(8, player)
	while True:
		result = game.playRound()
		if result == False:
			break

