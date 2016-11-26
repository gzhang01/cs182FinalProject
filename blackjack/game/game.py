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

class Blackjack:
	def __init__(self, numDecks=8, players=[Player()], **kwargs):
		self.numDecks = numDecks
		self.deck = BlackjackDeck(self.numDecks)
		# [player, bet]
		self.players = [[p, 0] for p in players]
		self.dealer = Player()
		self.reshuffle = False

		# Flags
		self.noPrint = False

		if "flags" in kwargs:
			if "-np" in kwargs.flags:
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
			for p in self.players:
				self.dealCard(p[0])
			self.dealCard(self.dealer)

	def printUpcard(self):
		print "\n"
		print "Dealer upcard: {0}".format(self.dealer.getHand()[0])

	# Runs the game
	def playRound(self):
		self.startRound()

		# Gather bets
		for p in self.players:
			bet = p[0].getBet(self.noPrint)
			p[1] = bet

		# Players take turns
		for p in self.players:
			while True:
				if not self.noPrint:
					self.printUpcard()
				action = p[0].getAction(self.noPrint)

				if action == "stand" or action == "bust":
					break
				elif action == "hit":
					self.dealCard(p[0])

		# Dealer actions
		while True:
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

			# Dealer stands on 17
			if dealerValue == const.blackjack or dealerValue >= 17:
				break

			# Else hit
			self.dealCard(self.dealer)

		# Determine winnings
		for p in self.players:
			playerValue = p[0].getHandValue()[0]
		 	playerBlackjack = True if playerValue == const.blackjack else False

			if not self.noPrint:
				print "\n"

			if playerValue == const.blackjack and dealerValue == const.blackjack:
				p[0].addMoney(p[1])
			elif playerValue == const.blackjack:
				p[0].addMoney(5 * p[1] / 2)
			elif dealerValue == const.blackjack or playerValue > 21:
				p[0].addMoney(0)
			elif dealerValue > 21 or playerValue > dealerValue:
				p[0].addMoney(2 * p[1])
			elif playerValue == dealerValue:
				p[0].addMoney(p[1])
			else:
				p[0].addMoney(0)
			
			if not self.noPrint:
				if playerValue == const.blackjack and dealerValue == const.blackjack: 	print "Dealer got BLACKJACK and you got BLACKJACK\nPUSH"
				elif playerValue == const.blackjack: 									print "You got BLACKJACK\nYou win ${0}".format(3 * p[1] / 2)
				elif dealerValue == const.blackjack:									print "Dealer got BLACKJACK\nYou lose ${0}".format(p[1])
				elif playerValue > 21:													print "You BUST\nYou lose ${0}".format(p[1])
				elif dealerValue > 21:													print "Dealer BUSTS\nYou win ${0}".format(p[1])
				elif playerValue > dealerValue:											print "Dealer has value {0} and you have value {1}\nYou win ${2}".format(dealerValue, playerValue, p[1])
				elif playerValue == dealerValue:										print "Dealer has value {0} and you have value {1}\nPUSH".format(dealerValue, playerValue)
				else:																	print "Dealer has value {0} and you have value {1}\nYou lose {2}".format(dealerValue, playerValue, p[1])

		# Clear cards
		for p in self.players:
			p[0].discardHand()
		self.dealer.discardHand()

		# Reshuffle if needed:
		if self.reshuffle:
			#### TODO: Think about how to notify players that deck has been reshuffled
			print "\n\nReshuffling!"
			self.deck.reshuffle()
			self.reshuffle = False



if __name__ == "__main__":
	game = Blackjack(8, [Player()])
	while True:
		game.playRound()
