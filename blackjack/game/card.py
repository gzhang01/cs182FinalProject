####
 # card.py
 #
 # Class definition of a standard poker card
 #
 # CS182 - Artificial Intelligence
 # Fall 2016
 # Final Project 
 ##

import unittest

class Card:
	# Initializes poker card with given value and suit
	def __init__(self, value, suit):
		self.value = value
		self.suit = suit

	# Gets value of card
	def getValue(self):
		return self.value

	# Gets suit of card
	def getSuit(self):
		return self.suit

	# Auto string formatting
	def __str__(self):
		return self.value + self.suit


# Unit tests for card class
class TestCardMethods(unittest.TestCase):
	def setUp(self):
		self.card1, self.card2 = Card("A", "H"), Card("10", "S")

	def tearDown(self):
		self.card1, self.card2 = None, None

	def test_getValue(self):
		self.assertEqual(self.card1.getValue(), "A")
		self.assertEqual(self.card2.getValue(), "10")

	def test_getSuit(self):
		self.assertEqual(self.card1.getSuit(), "H")
		self.assertEqual(self.card2.getSuit(), "S")

	def test_toString(self):
		self.assertEqual(self.card1.__str__(), "AH")
		self.assertEqual(self.card2.__str__(), "10S")


# Run tests if run from terminal
if __name__ == "__main__":
	unittest.main()