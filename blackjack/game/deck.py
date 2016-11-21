####
 # deck.py
 #
 # Class definition of a standard poker deck
 #
 # CS182 - Artificial Intelligence
 # Fall 2016
 # Final Project 
 ##

from card import Card
import random
import math
import unittest

class BlackjackDeck:
 	# Initializes standard poker deck
 	def __init__(self, decks=8):
 		values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
 		suits = ['H', 'D', 'S', 'C']

 		self.numDecks = decks
 		self.deck = [Card(v, s) for v in values for s in suits for _ in xrange(self.numDecks)]
 		random.shuffle(self.deck)
 		self.deck.insert(int(math.floor(0.75 * self.getNumCardsLeft())), Card("cut", "cut"))

 	# Returns number of cards left in deck
 	def getNumCardsLeft(self):
 		return len(self.deck)

 	# Draws a card from deck
 	def drawCard(self):
 		if self.getNumCardsLeft() == 0:
 			raise RuntimeError("Deck is empty. Cannot draw another card!")
 		return self.deck.pop()

 	# Resets the deck
 	def reshuffle(self):
 		self.__init__(self.numDecks)


# Unit tests for BlackjackDeck class
class TestBlackjackDeckMethods(unittest.TestCase):
	def setUp(self):
		self.numDecks = 8
		self.deck = BlackjackDeck(self.numDecks)

	def tearDown(self):
		self.deck = None

	def test_getNumCardsLeft(self):
		self.assertEqual(self.deck.getNumCardsLeft(), 52 * self.numDecks + 1)

	def test_drawCard(self):
		for i in xrange(52 * self.numDecks + 1):
			self.deck.drawCard()
		with self.assertRaises(RuntimeError):
			self.deck.drawCard()

	def test_reshuffle(self):
		for i in xrange(random.randint(10, 52 * self.numDecks)):
			self.deck.drawCard()
		self.deck.reshuffle()
		self.assertEqual(self.deck.getNumCardsLeft(), 52 * self.numDecks + 1)


# Run tests if run from terminal
if __name__ == "__main__":
	unittest.main()