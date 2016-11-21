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

class Blackjack:
	def __init__(self, players=[Player()], numDecks=8, **kwargs):
		self.numDecks = numDecks
		self.deck = BlackjackDeck(self.numDecks)
		self.players = list(players)
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

	#### TODO: Think about how to notify players that deck has been reshuffled

	# Deals cards to start a round
	def startRound(self):
		for _ in xrange(2):
			for p in self.players:
				self.dealCard(p)
			self.dealCard(self.dealer)

	# Runs the game
	def playRound(self):
		self.startRound()

		# Players take turns
		for p in self.players:
			while True: 
				if not self.noPrint:
					print "\n"
					print "Dealer upcard: {0}".format(self.dealer.getHand()[0])
				action = p.getAction(self.noPrint)

				if action == "stand":
					break
				elif action == "hit":
					self.dealCard(p)

				# TODO: list of active players for busting?



if __name__ == "__main__":
	game = Blackjack()
	game.playRound()
