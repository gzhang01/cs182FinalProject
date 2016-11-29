####
 # automatedAgent.py
 #
 # Base agent for automated gameplay
 # NOTE: this agent should never be run
 # Bets uniformly
 #
 # CS182 - Artificial Intelligence
 # Fall 2016
 # Final Project 
 ##

from card import Card 
from deck import BlackjackDeck
from player import Player 
import constants as const

import unittest

# AutomatedAgent inherits from Player, overwriting chooseBet and 
# chooseAction methods to play randomly
class AutomatedAgent(Player):
	# Returns constant bet if money allows, else all money
	def chooseBet(self):
		bet = const.betValue if const.betValue < self.money else self.money
		if not self.noPrint: print bet
		return bet

	# Returns random valid action
	def chooseAction(self, actions, dealerUpcard):
		raise RuntimeError("Choose Action Not Implemented")


# Unit tests for AutomatedAgent class
class TestAutomatedAgentMethods(unittest.TestCase):
	def setUp(self):
		self.player = AutomatedAgent()
		self.player.noPrint = True

	def tearDown(self):
		self.player = None

	def test_chooseBet(self):
		self.assertEqual(self.player.chooseBet(), const.betValue)
		self.player.money = const.betValue - 1
		self.assertEqual(self.player.chooseBet(), const.betValue - 1)

	def test_chooseAction(self):
		with self.assertRaises(RuntimeError):
			self.player.chooseAction({})


# Run tests if run from terminal
if __name__ == "__main__":
	unittest.main()