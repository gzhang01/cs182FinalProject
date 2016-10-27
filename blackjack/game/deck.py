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
import unittest

class Deck:
 	# Initializes standard poker deck
 	def __init__(self):
 		values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
 		suits = ['H', 'D', 'S', 'C']

 		self.deck = [Card(v, s) for v in values for s in suits]
 		random.shuffle(self.deck)

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
 		self.__init__()


# Unit tests for card class
class TestCardMethods(unittest.TestCase):
	def setUp(self):
		self.deck = Deck()

	def tearDown(self):
		self.deck = None

	def test_getNumCardsLeft(self):
		self.assertEqual(self.deck.getNumCardsLeft(), 52)

	def test_drawCard(self):
		for i in xrange(52):
			self.deck.drawCard()
		with self.assertRaises(RuntimeError):
			self.deck.drawCard()

	def test_reshuffle(self):
		for i in xrange(random.randint(10, 52)):
			self.deck.drawCard()
		self.deck.reshuffle()
		self.assertEqual(self.deck.getNumCardsLeft(), 52)


# Run tests if run from terminal
if __name__ == "__main__":
	unittest.main()